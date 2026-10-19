# Tested CPU starters and reusable checks

Read only the selected example's section. These small programs reduce API rediscovery after selection. They are optional starting points, not a reason to favor an engine. Keep an existing chosen engine, framework, stage, and lockfile. Use the [repository/skill handoff](repositories-and-skills.md) for other tasks, ovnewton, native code, or GPU execution.

## Choose a matching starter

| Starter | Tested dependency set | What it exercises | Important limit |
| --- | --- | --- | --- |
| [ovphysx-drop](../assets/ovphysx-drop/demo.py) | ovphysx 0.7.0.74035321; ovstage 0.3.0.1791986420; physx-usd-schemas 25.11.2.72696984; Warp 1.18.0; NumPy 2.5.4; packaging 23.2 | TGS CPU, USD population, stage attachment, completed stepping, position/velocity CSV, independent stage pose readback | One known box/floor fixture; no viewer or cross-process transport |
| [newton-spring](../assets/newton-spring/spring_fit.py) | Newton 1.6.1; Warp 1.18.0; NumPy 2.5.4 | Direct SemiImplicit CPU, a mass and spring, automatic gradients through the rollout, finite differences, analytic trajectory, stiffness fit | Smooth synthetic data with known mass and initial state; no contacts |
| [newton-grasp](../assets/newton-grasp/gripper.py) | Newton 1.7.0; Warp 1.18.0; NumPy 2.5.4 | Direct XPBD CPU, dynamic finger servos, close/lift/hold/release, CSV, zero-friction control | Independent bodies approximate fingers; no articulated mechanism, pair-specific force, or penetration measurements |

The sets were exercised on Windows x86_64, Python 3.13.12. They are reproduction pins, not minimum versions or a claim that other versions fail. The two Newton examples use the versions tested in their respective trials. Warp enumerated available GPUs, but the models and simulation kernels used CPU; driverless operation was not tested. Read [local evaluation evidence](../evals/local-evidence.md) for scope and limitations.

Copy one whole starter folder into a writable project directory. Keep its relative files together. Run the copy so generated CSV, JSON, and caches do not enter the installed skill. Each folder has `requirements.txt` and explicit scene-specific limits in `validation.json`. Install into a separate environment for this reproduction. For Windows, from the copied folder:

```console
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip check
```

For another platform, use its environment interpreter path and first verify wheel/runtime support. If the application already has a different dependency set, adapt against its installed source/examples and rerun the checks; do not overwrite its lockfile. A dependency check does not confirm simulation. Failures in a package index, writable cache, or temporary directory belong to runtime setup, not engine capability. Follow the host's permission process; do not disable safeguards or alter system drivers to reproduce these programs.

In the commands below, resolve `<skill-dir>` to this skill directory. The checker uses only Python's standard library and never imports a simulator. It returns 0 for the requested checks passing, or 2 for failed/missing/invalid evidence. It reads saved outputs; inspect execution logs and the producing code before claiming an actual simulation or automatic differentiation ran.

## Ovphysx drop with shared stage

```console
.venv/Scripts/python.exe demo.py
python <skill-dir>/scripts/check_rollout.py drop --run . --limits validation.json
```

`scene.usda` layers CPU/TGS scene settings over `source.usda`. The fixture has Z up, meter units, a 0.2 m box initially centered at 1 m, and a floor with its top at 0 m. The expected rest center is 0.1 m. The example simulates 2 s in 960 steps, with an initial sample. A 1/120 s trial had transient excessive penetration; the tested 1/480 s step resolved this fixture's bound. These numbers are not universal tuning advice.

The class owns its stage and keeps it alive inside its context. The optional `--viewer module:function` callback receives `(stage, ordinal, time_s)` after publication in the same process; no renderer is included or tested. An existing application-owned stage needs the upstream lifecycle route rather than creating a second stage.

Keep these API details when adapting the 0.7 example:

- Use `read_sync(..., pattern='/World/Box')` for the string-path filter shown here. Do not put string paths into an argument expecting interned path IDs.
- For `stage.read_attributes`, intern the attribute token with a dictionary for that stage. The starter uses `dictionary.intern_token('omni:fabric:worldMatrix')`. String convenience arguments in one API do not imply another accepts strings.
- Match output identities, copy borrowed data before releasing it, wait for reads/tasks, and release read groups. The stage comparison uses the published world matrix, not a second read of the physics pose.
- Publish only output ordinals; do not replay them through the input-update path. Close the output cache and complete detachment before destroying the stage.

The saved `simulation_result.json` records the stage pose. The checker compares it with the CSV, checks finite samples, falling, transient penetration, settling, and duration. Passing this fixture does not establish contact fidelity for another asset. The sample uses the pinned package's schema helper and cache configuration; review those APIs before upgrading.

## Differentiable Newton spring

```console
.venv/Scripts/python.exe spring_fit.py
python <skill-dir>/scripts/check_rollout.py spring --run . --limits validation.json
```

The example fits 25 N/m from a 10 N/m estimate. It uses a 1 kg particle, a 1 m rest length, an initial position of 1.2 m, and 100 steps of 0.01 s. It saves target, initial, fitted, and analytic trajectories plus the optimization history. The target comes from the same discrete solver; a small fit loss is not continuous-time accuracy or real-data identification.

Use `model.spring_stiffness` for this installed version, not the nonexistent `model.spring_ke`. The builder's `add_spring` argument name does not establish the finalized model field name. The model enables gradients and preserves intermediate states for Warp Tape. The selected solver consumes the same control and parameter arrays being differentiated. Check a new solver/operation explicitly rather than transferring this differentiation claim.

The checker recomputes trajectory losses and analytic error, checks finite nonzero gradients and their numerical agreement, and checks stiffness recovery. The limits are for this short smooth fixture. Keep timestep accuracy, numerical gradient agreement, and parameter fit as separate conclusions.

## Newton grasp, release, and negative control

```console
.venv/Scripts/python.exe gripper.py
.venv/Scripts/python.exe gripper.py --friction 0 --output output-zero-friction
python <skill-dir>/scripts/check_rollout.py grasp --run output --control output-zero-friction --limits validation.json
```

`config.json` exposes geometry, masses, friction, force/torque caps, gains, timestep/substeps, solver iterations, and phase durations. The simulation never attaches or teleports the block. It measures lift throughout the hold, relative movement during hold, and falling after release. Hold-relative range does not quantify earlier slip during the lift. The zero-friction trial must change only friction; failure to lift is the expected control result, not a failed test harness.

The checker reports contact forces and penetration as **unverified** for this starter. A positive lift and global contact count do not establish bilateral grip forces or bounded penetration. For tasks requiring those claims, add correctly mapped per-pair normal forces, floor force, and penetration measurements, then use:

```console
python <skill-dir>/scripts/check_rollout.py grasp --run output --control output-zero-friction --limits validation.json --require-contact-evidence
```

This stronger command intentionally fails for the unextended starter. It expects numeric CSV columns `left_normal_N`, `right_normal_N`, `floor_normal_N`, and nonnegative `penetration_m`. Map them to actual geometry identities and the solver's documented force/sign/unit conventions. The checker requires bilateral positive force and no floor support during hold, and bounded penetration throughout. Commanded finger force is not measured normal contact force. Missing evidence must not silently pass as zero.

Use a mechanically constrained/articulated gripper when the task needs joint or actuator realism. The paired trial's alternative Newton/MuJoCo implementation supplied stronger contact diagnostics; the simpler XPBD starter is not a claim of superior grasp accuracy. For MuJoCo, verify Newton, MuJoCo, and mujoco-warp compatibility together before running.

## Adapt the checks to a real task

The checker expects the producers' CSV/JSON field names; the grasp profile allows explicit height/relative-column mapping. Preserve separate measurements and limits. Change `validation.json` only to reflect agreed scene/task tolerances, duration, and sample count, not merely to turn a failure green. Update the example's built-in checks/configuration consistently. Keep pre-change evidence for comparisons.

Run the copied fixture first, then add the user's actual geometry, controls, observations, and reset behavior. Mark every required but missing measurement unverified or failing. A passing saved-output check is evidence about those samples, not a performance benchmark, sensor calibration, convergence proof, or hardware qualification.
