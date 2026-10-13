#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build and bind a USD scene without editing it or advancing simulation.

Use a fresh process with a supported ovnewton runtime. --output writes a new
JSON file, because native libraries may also emit console output.
"""

import argparse
import contextlib
from importlib import metadata
import json
import logging
import math
from pathlib import Path
import sys


def numeric_findings(masses, inertias, centers, gravity):
    """Detect limited numeric faults; zero masses are not automatically invalid."""
    findings = []

    def visit(value, field):
        if isinstance(value, (list, tuple)):
            for index, item in enumerate(value):
                visit(item, f"{field}[{index}]")
        elif not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            findings.append({"severity": "error", "field": field, "reason": "non-finite or non-numeric value"})

    for field, values in (("mass", masses), ("inertia", inertias), ("center_of_mass", centers), ("gravity", gravity)):
        visit(values, field)
    for index, mass in enumerate(masses):
        if isinstance(mass, (int, float)) and math.isfinite(mass) and mass < 0:
            findings.append({"severity": "error", "field": f"mass[{index}]", "reason": "negative mass"})
    if not masses:
        findings.append({"severity": "note", "field": "body_count", "reason": "no bodies; verify scene intent"})
    return findings


def json_safe(value):
    """Keep error results valid JSON even when a model contains NaN or Inf."""
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


class DiagnosticCapture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append({"level": record.levelname, "message": record.getMessage(),
                             "diagnostic_code": getattr(record, "diagnostic_code", None),
                             "prim_path": getattr(record, "prim_path", None)})


def inspect_scene(scene, solver_name, device):
    # Native imports stay inside this function: --help and unit tests need no SDK.
    import warp as wp
    import newton
    import ovnewton

    ovnewton.register_usd_schemas()
    import ovstage
    from ovstage import PopulationDomain, population

    solver_class = {"xpbd": newton.solvers.SolverXPBD,
                    "mujoco": newton.solvers.SolverMuJoCo,
                    "vbd": newton.solvers.SolverVBD}[solver_name]
    with wp.ScopedDevice(device):
        stage = ovstage.Stage()
        population.open_usd(stage, str(scene), ordinal=1, domains=PopulationDomain.ALL)
        stage.advance_write_floor(1).wait()
        builder = newton.ModelBuilder()
        solver_class.register_custom_attributes(builder)
        imported = ovnewton.add_ovstage(builder, stage, ordinal=1)
        if solver_name == "vbd":
            builder.color()
        model = builder.finalize(skip_validation_joints=imported.has_orphan_joints)
        # Binding verifies stage identity mappings. This is not a solver test.
        binding = ovnewton.attach_ovstage(stage, model=model, ordinal=1)
        masses = model.body_mass.numpy().tolist()
        inertias = model.body_inertia.numpy().tolist()
        centers = model.body_com.numpy().tolist()
        gravity = model.gravity.numpy().tolist()
        findings = numeric_findings(masses, inertias, centers, gravity)
        return {
            "status": "numeric_check_failed" if any(f["severity"] == "error" for f in findings) else "imported",
            "device": str(binding.model.device),
            "counts": {"bodies": model.body_count, "shapes": model.shape_count, "joints": model.joint_count},
            "has_orphan_joints": bool(imported.has_orphan_joints),
            "body_labels": list(model.body_label), "mass": masses, "inertia": inertias,
            "center_of_mass": centers, "gravity": gravity, "findings": findings,
            "units_note": "Model/stage units; values are not normalized to SI by this inspector.",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", type=Path, help="Source USD file; its referenced assets must be accessible")
    parser.add_argument("--solver", choices=("xpbd", "mujoco", "vbd"), default="xpbd", help="Builder preparation only")
    parser.add_argument("--device", default="cpu", help="Warp device for the imported model")
    parser.add_argument("--output", type=Path, help="New JSON file; existing files are never overwritten")
    args = parser.parse_args()
    if not args.scene.is_file():
        parser.error("scene must be an existing file")
    if args.output and args.output.exists():
        parser.error("output already exists; choose a new filename")
    result = {"schema_version": 1, "source": str(args.scene.resolve()),
              "preparation_solver": args.solver, "simulation_tested": False, "versions": {}}
    capture = DiagnosticCapture()
    logger = logging.getLogger("ovnewton")
    old_level = logger.level
    logger.addHandler(capture)
    logger.setLevel(logging.INFO)
    try:
        for package in ("ovnewton", "newton", "ovstage", "warp-lang"):
            result["versions"][package] = metadata.version(package)
        with contextlib.redirect_stdout(sys.stderr):
            result.update(inspect_scene(args.scene.resolve(), args.solver, args.device))
    except Exception as exc:
        result.update(status="import_failed", error_type=type(exc).__name__, error=str(exc))
    finally:
        logger.removeHandler(capture)
        logger.setLevel(old_level)
    result["diagnostics"] = capture.records
    text = json.dumps(json_safe(result), indent=2, allow_nan=False) + "\n"
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(text)
        except OSError as exc:
            print(f"Cannot create output: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return 0 if result["status"] == "imported" else 1


if __name__ == "__main__":
    raise SystemExit(main())
