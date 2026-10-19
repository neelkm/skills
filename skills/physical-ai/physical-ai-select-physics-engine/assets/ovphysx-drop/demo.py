# SPDX-License-Identifier: Apache-2.0
"""CPU box drop; application-owned OVStage, explicit output publication."""
from pathlib import Path
import os
import csv
import json
import argparse
import importlib

ROOT = Path(__file__).resolve().parent
os.environ['WARP_CACHE_PATH'] = str(ROOT / '.cache' / 'warp')
for folder in ('warp', 'cooking'):
    (ROOT / '.cache' / folder).mkdir(parents=True, exist_ok=True)

import numpy as np
import warp as wp
import ovstage
from ovphysx import PhysX
from ovphysx.config import PhysXConfig
from ovphysx.types import SimObjectType, ObjectScope
from ovphysx.utils import OvStageOutputCache, step_and_write_to_ovstage
from ovphysx.samples.python_samples.schema_support import physx_schema_paths


class DropDemo:
    """Use with a context manager; stage remains alive until context exit.

    A future in-process viewer can consume self.stage after each sealed ordinal.
    No cross-process transport or viewer server is implied by a Stage name.
    """
    def __init__(self, scene=ROOT / 'scene.usda'):
        PhysX.set_cpu_mode(True)
        ovstage.population.register_usd_schemas([str(p) for p in physx_schema_paths()])
        self.physx = PhysX(config=PhysXConfig(cooked_collider_cache_dir=str(ROOT / '.cache/cooking')))
        self.stage = ovstage.Stage('cpu-box-drop')
        self.cache = None
        self.ordinal = 1
        try:
            ovstage.population.open_usd(self.stage, str(Path(scene).resolve()), ordinal=1,
                                       domains=ovstage.PopulationDomain.ALL)
            self.stage.advance_write_floor(ordinal=1).wait()
            self.physx.wait_task(self.physx.attach_ovstage(self.stage, read_ordinal=1))
            self.cache = OvStageOutputCache(self.physx)
        except Exception:
            self.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        if self.cache is not None:
            self.cache.close()
            self.cache = None
        if self.physx.is_stage_attached(self.stage):
            # If detach fails, preserve stage lifetime; do not destroy it.
            self.physx.wait_task(self.physx.detach_ovstage())
        self.stage.destroy()
        self.physx.destroy()

    def body(self, attribute):
        values = {}
        with ovstage.PathDictionary(self.stage) as paths:
            with self.physx.read_sync(SimObjectType.RIGID_BODY, [attribute],
                                     scope=ObjectScope.ALL, pattern='/World/Box') as result:
                for group in result.groups:
                    if group.is_delete or group.is_array or not group.tensors:
                        continue
                    if group.index_map is not None or group.prim_index_map is not None:
                        raise RuntimeError('Unexpected sparse body output')
                    if not group.tensors[0].device.is_cpu:
                        raise RuntimeError('Readback is not on CPU')
                    data = group.tensors[0].numpy().copy()
                    for path, row in zip(paths.get_path_strings(group.prim_list), data):
                        values[path] = row
        if set(values) != {'/World/Box'}:
            raise RuntimeError(f'Expected one named box, got {list(values)}')
        return values['/World/Box']

    def verify_stage(self):
        """Read the shared stage as a consumer and compare its world position."""
        expected = self.body('position')
        found = None
        with ovstage.PathDictionary(self.stage) as dictionary:
            matrix_token = dictionary.intern_token('omni:fabric:worldMatrix')
        with self.physx.read_sync(SimObjectType.RIGID_BODY, ['position'],
                                 pattern='/World/Box') as result:
            for pg in result.groups:
                with self.stage.query_from_path_list(pg.prim_list) as query:
                    with self.stage.read_attributes(query, [matrix_token],
                                                    ovstage.OrdinalRange.latest(self.ordinal)) as read:
                        read.wait()
                        for group in read.groups():
                            try:
                                matrix = np.asarray(group.array(0)).copy().reshape(-1, 4, 4)
                                found = matrix[0, 3, :3].copy()
                            finally:
                                self.stage.release_group(group)
        if found is None or not np.allclose(found, expected, atol=1e-5):
            raise RuntimeError(f'Stage publication mismatch: {found} versus {expected}')
        return found.tolist()

    def run(self, csv_path=ROOT / 'positions.csv', seconds=2.0, dt=1/480, on_frame=None):
        n = round(seconds / dt)
        if n <= 0 or abs(n * dt - seconds) > 1e-8:
            raise ValueError('Duration must be a positive whole number of time steps')
        rows = []
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['time_s', 'x_m', 'y_m', 'z_m', 'vx_m_s', 'vy_m_s', 'vz_m_s'])
            for step in range(n + 1):
                if step:
                    self.ordinal += 2
                    # Only output ordinals are authored; never drain them into physics.
                    step_and_write_to_ovstage(self.physx, dt=dt, output_ordinal=self.ordinal,
                        cache=self.cache, outputs={SimObjectType.RIGID_BODY: ['position', 'orientation']})
                p, v = self.body('position'), self.body('linearVelocity')
                row = [step * dt, *map(float, p), *map(float, v)]
                if not np.isfinite(row).all():
                    raise RuntimeError('Non-finite simulation output')
                rows.append(row)
                writer.writerow(row)
                if on_frame is not None:
                    on_frame(self.stage, self.ordinal, step * dt)
        a = np.asarray(rows)
        tail = a[a[:, 0] >= seconds - 0.25]
        checks = {
            'duration_two_seconds': abs(a[-1, 0] - 2.0) < 1e-8,
            'initial_height_1m': abs(a[0, 3] - 1) < 1e-5,
            'fell_at_least_0_5m': float(a[0, 3] - a[:, 3].min()) > 0.5,
            'rest_center_near_0_1m': abs(float(a[-1, 3]) - 0.1) <= 0.01,
            'no_floor_penetration_over_1cm': float(a[:, 3].min()) >= 0.09,
            'tail_position_span_below_1mm': float(np.ptp(tail[:, 3])) <= 0.001,
            'tail_speed_below_1cm_per_second': float(np.linalg.norm(tail[:, 4:7], axis=1).max()) <= 0.01,
            'all_values_finite': bool(np.isfinite(a).all()),
            'stage_matches_physics': True,
        }
        stage_position = self.verify_stage()
        checks = {key: bool(value) for key, value in checks.items()}
        return {'actual_simulation': True, 'checks': checks, 'passed': all(checks.values()),
                'samples': len(rows), 'simulated_seconds': float(a[-1, 0]), 'dt_s': dt,
                'initial_z_m': float(a[0, 3]), 'final_z_m': float(a[-1, 3]),
                'min_z_m': float(a[:, 3].min()), 'tail_z_span_m': float(np.ptp(tail[:, 3])),
                'tail_max_speed_m_s': float(np.linalg.norm(tail[:, 4:7], axis=1).max()),
                'stage_position_m': stage_position, 'final_ordinal': self.ordinal}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scene', default=str(ROOT / 'scene.usda'))
    parser.add_argument('--csv', default=str(ROOT / 'positions.csv'))
    parser.add_argument('--viewer', help='Optional in-process module:function callback(stage, ordinal, time_s)')
    args = parser.parse_args()
    callback = None
    if args.viewer:
        module, name = args.viewer.split(':', 1)
        callback = getattr(importlib.import_module(module), name)
    with DropDemo(args.scene) as demo:
        result = demo.run(args.csv, on_frame=callback)
    (ROOT / 'simulation_result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
