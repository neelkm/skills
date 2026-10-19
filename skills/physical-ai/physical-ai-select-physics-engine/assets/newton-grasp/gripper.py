# SPDX-License-Identifier: Apache-2.0
"""Headless Newton XPBD grasp test. SI units; Z up; no grasp attachment."""
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parent
os.environ['WARP_CACHE_PATH'] = str(ROOT / '.cache' / 'warp')
import argparse
import csv
import json
import time
import importlib.metadata


def target(t, c):
    """Open, close, lift, hold, release, fall. Smooth position interpolation."""
    def smooth(a):
        a = min(1., max(0., a))
        return a*a*(3.-2.*a)
    close = smooth((t-c['settle_s'])/c['close_s'])
    lift_start = c['settle_s']+c['close_s']
    lift = smooth((t-lift_start)/c['lift_s'])
    release_start = lift_start+c['lift_s']+c['hold_s']
    release = smooth((t-release_start)/c['release_s'])
    gap = c['open_gap_m'] + (c['closed_gap_m']-c['open_gap_m'])*close
    gap += (c['open_gap_m']-c['closed_gap_m'])*release
    z = c['finger_center_z_m']+c['lift_height_m']*lift
    phase = ('settle' if t<c['settle_s'] else 'close' if t<lift_start else
             'lift' if t<lift_start+c['lift_s'] else 'hold' if t<release_start else
             'release' if t<release_start+c['release_s'] else 'fall')
    return gap, z, phase


def run(c, output):
    import numpy as np
    import warp as wp
    import newton
    wp.init()
    wp.set_device('cpu')
    b = newton.ModelBuilder()
    b.default_shape_cfg.mu = c['friction']
    b.default_shape_cfg.mu_torsional = 0.0
    b.default_shape_cfg.mu_rolling = 0.0
    b.default_shape_cfg.gap = c['contact_gap_m']
    b.default_shape_cfg.margin = 0.0
    b.add_ground_plane()
    h = np.array(c['block_size_m'])/2
    block = b.add_body(xform=wp.transform((0.,0.,float(h[2]+.001)), wp.quat_identity()), label='block')
    cfg = b.default_shape_cfg.copy()
    cfg.density = c['block_mass_kg']/float(np.prod(c['block_size_m']))
    b.add_shape_box(block, hx=float(h[0]), hy=float(h[1]), hz=float(h[2]), cfg=cfg)
    fh = np.array(c['finger_size_m'])/2
    fingers = []
    for side in [-1, 1]:
        finger = b.add_body(xform=wp.transform((side*(c['open_gap_m']/2+float(fh[0])),0.,c['finger_center_z_m']),wp.quat_identity()),label=f'finger_{side}')
        cfg = b.default_shape_cfg.copy()
        cfg.density = c['finger_mass_kg']/float(np.prod(c['finger_size_m']))
        b.add_shape_box(finger,hx=float(fh[0]),hy=float(fh[1]),hz=float(fh[2]),cfg=cfg)
        fingers.append(finger)
    model = b.finalize(device='cpu')
    solver = newton.solvers.SolverXPBD(model, iterations=c['solver_iterations'])
    pipeline = newton.CollisionPipeline(model)
    contacts = pipeline.contacts()
    state, next_state = model.state(), model.state()
    control = model.control()
    frame_dt = 1./c['control_hz']
    dt = frame_dt/c['substeps']
    total = sum(c[k] for k in ['settle_s','close_s','lift_s','hold_s','release_s','fall_s'])
    rows = []
    begin = time.perf_counter()
    max_force = 0.
    max_contacts = 0
    for frame in range(round(total*c['control_hz'])):
        t = frame*frame_dt
        gap,z,phase = target(t,c)
        gap1,z1,_ = target(t+frame_dt,c)
        for sub in range(c['substeps']):
            q = state.body_q.numpy().copy()
            qd = state.body_qd.numpy().copy()
            forces = np.zeros((3,6),dtype=np.float32)
            for side,idx in zip([-1,1],fingers):
                desired = np.array([side*(gap/2+fh[0]),0.,z])
                velocity = np.array([side*(gap1-gap)/(2*frame_dt),0.,(z1-z)/frame_dt])
                f = c['kp_N_per_m']*(desired-q[idx,:3])+c['kd_Ns_per_m']*(velocity-qd[idx,:3])
                f[2] += 9.81*c['finger_mass_kg']
                f *= min(1.,c['max_force_N']/max(float(np.linalg.norm(f)),1e-12))
                # Quaternion vector gives a small-angle orientation error toward identity.
                torque = -2*c['rotation_kp_Nm']*q[idx,3:6]*np.sign(q[idx,6])-c['rotation_kd_Nms']*qd[idx,3:6]
                torque *= min(1.,c['max_torque_Nm']/max(float(np.linalg.norm(torque)),1e-12))
                forces[idx,:3],forces[idx,3:] = f,torque
                max_force = max(max_force,float(np.linalg.norm(f)))
            state.clear_forces()
            state.body_f.assign(forces)
            pipeline.collide(state,contacts)
            max_contacts = max(max_contacts,int(contacts.rigid_contact_count.numpy()[0]))
            solver.step(state,next_state,control,contacts,dt)
            state,next_state = next_state,state
            if not np.isfinite(state.body_q.numpy()).all():
                raise RuntimeError('Non-finite body state')
        q = state.body_q.numpy()
        jaw_z = float((q[fingers[0],2]+q[fingers[1],2])/2)
        rows.append({'time_s':(frame+1)*frame_dt,'phase':phase,'block_height_m':float(q[block,2]),
                     'block_x_m':float(q[block,0]),'block_y_m':float(q[block,1]),
                     'jaw_height_m':jaw_z,'relative_height_m':float(q[block,2])-jaw_z,
                     'jaw_gap_m':float(q[fingers[1],0]-q[fingers[0],0]-2*fh[0]),
                     'target_gap_m':gap,'target_height_m':z})
    output.mkdir(parents=True,exist_ok=True)
    with (output/'block_height.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    hold=[r for r in rows if r['phase']=='hold']
    initial=rows[0]['block_height_m']
    min_hold=min(r['block_height_m'] for r in hold)
    slip=max(r['relative_height_m'] for r in hold)-min(r['relative_height_m'] for r in hold)
    lifted=min_hold-initial >= c['minimum_lift_m']
    held=lifted and slip <= c['maximum_hold_slip_m']
    release_drop=hold[-1]['block_height_m']-rows[-1]['block_height_m']
    metrics={'classification':'held' if held else 'slipped_or_failed_to_lift','held':bool(held),
             'minimum_hold_height_m':min_hold,'lift_above_initial_m':min_hold-initial,
             'hold_relative_slip_m':slip,'release_drop_m':release_drop,
             'release_passed':release_drop>=c['minimum_release_drop_m'],
             'final_height_m':rows[-1]['block_height_m'],'max_command_force_N':max_force,
             'max_contact_count':max_contacts,'finite_states':True,'body_count':model.body_count,
             'simulated_seconds':total,'wall_seconds_including_first_kernel_compilation':time.perf_counter()-begin,
             'versions':{k:importlib.metadata.version(k) for k in ['newton','warp-lang','numpy']},
             'device':str(model.device),'settings':c,'samples':len(rows)}
    (output/'metrics.json').write_text(json.dumps(metrics,indent=2))
    print(json.dumps(metrics,indent=2))
    return metrics


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--config',type=Path,default=ROOT/'config.json')
    p.add_argument('--output',type=Path,default=ROOT/'output'); p.add_argument('--friction',type=float)
    a=p.parse_args(); c=json.loads(a.config.read_text())
    if a.friction is not None: c['friction']=a.friction
    run(c,a.output)
