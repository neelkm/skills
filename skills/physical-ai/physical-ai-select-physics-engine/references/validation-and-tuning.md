# Task validation and physics tuning

Use when a candidate needs confirmation, a performance claim needs evidence, or the selected simulation needs tuning. Follow the [verified skill/document routes](repositories-and-skills.md). Preserve the user's physical requirements and baseline configuration.

## Distinguish evidence levels

1. **Source review:** a feature is documented for a specific version/path.
2. **Metadata check:** packages and declared dependencies were inspected.
3. **Runtime check:** a bounded example completed and returned expected finite, nonempty changing state.
4. **Task check:** representative contacts, control, reset, and task metrics met the agreed limits.
5. **Comparative measurement:** candidates ran under recorded comparable conditions.

Do not present one level as proof of a later level. A visible animation, successful import, or a passing metadata probe is not a fidelity result.

## Use the smallest discriminating task

For small matching CPU tasks, [tested starters](tested-starters.md) provide producers, explicit limit profiles, and [a reusable saved-output checker](../scripts/check_rollout.py). Use the chosen path only. The checker recomputes behavior from measurements and lists missing evidence; it cannot prove that recorded data came from a simulator or that a gradient came from autodifferentiation. Inspect actual execution and the producing code as well.

| Workflow | Representative check | Metrics to establish with the user/project |
| --- | --- | --- |
| Locomotion | One stance/contact/control rollout, then a representative batch | Foot slip, joint tracking, constraint error, falls, reset correctness, throughput |
| Grasp and lift | Close, lift, hold, release with the intended geometry/materials | Slip distance, force/effort bounds, penetration, successful holds |
| Insertion or assembly | Approach, first contact, insertion, and release under expected offsets | Success rate, insertion force, depth, penetration, jams, latency |
| Closed-loop mechanism | Drive through the operating range under load | Closure error, tracking, effort, jitter, numerical failures |
| Deformable manipulation | Representative deformation and rigid/deformable interaction | Shape/displacement error, material response, attachment error, contact and reset coverage |
| Large RL batches | Multiple independent environments with action/read/reset cycles | Isolation, stable identity mapping, reset latency, memory, rollouts/s, numerical failures |
| Differentiable optimization | Small rollout containing required controls, parameters, and contacts | Finite gradients, agreement with an appropriate numerical check, loss behavior, cost |
| Shared-stage application | Input edit -> solve -> output publication -> consumer read | Identity and units, correct input/output ownership, motion, update latency, stale-state failures |

Set units and acceptance limits before the comparison. Derive them from the task or available physical evidence; do not invent universal pass thresholds. A smoke scene can isolate runtime faults but cannot substitute for the representative task.

For grasp tests, separate **failed to lift**, **held**, **slipped**, and **released** when evidence permits. Measure the block relative to the gripper over a stated interval; a range during hold does not include earlier slip during lift. Check bilateral contacts, lack of floor support, and penetration when claiming a physically supported grasp. Contact counts alone do not prove contact identity or force. An unattached block that fails to lift under a zero-friction control helps test the mechanism; keep the other physical/control settings unchanged and report that expected failure separately from nominal task failure. Missing force or penetration telemetry remains unverified, even when height and release checks pass.

For gradient checks, identify the loss, parameters, differentiable operations, contact transitions, horizon, and initial state. Compare against finite differences where meaningful with appropriate perturbation sizes. Explain discontinuities and noisy/ill-conditioned results. A finite-difference check validates a claimed gradient path; it does not replace a user's requirement for automatic differentiation without agreement.

## Diagnose before tuning

Inspect the imported model as well as the source scene. Check physical scale, gravity, up axis, mass/inertia, center of mass, collision shapes and normals, initial overlap, joint axes/limits, actuator/drive semantics, friction/material bindings, and controller units. Inspect effective values and whether the selected solver consumes them.

Then separate synchronization faults from dynamics: completed writes, current state after swapping, input ownership, stage ordinal ranges, and device completion. Do not increase stiffness to compensate for a stale control target or missing mass schema.

| Symptom | First investigation | Bounded experiment after model/integration checks |
| --- | --- | --- |
| Slip | Contact geometry/locations, friction, normal force, effort limits | Change justified contact/drive settings and measure slip and forces |
| Penetration or missed contacts | Collider representation, initial overlap, offsets, contact capacity, collision frequency | Reduce timestep or increase substeps; check supported convergence and geometry settings |
| Jitter or explosion | Overlap, constraint conflict, extreme mass ratios, stiff drives, wrong units | Timestep/substep and damping/convergence experiments with numerical-failure bounds |
| Tracking error | Command/state identity, mode, limits, physical loading, update rate | Tune supported drive settings without exceeding required effort/speed |
| Slow runtime | Solve, collisions, compilation, transfers, reset, stage publication, rendering | Optimize the measured bottleneck while keeping task acceptance limits |

Change one factor at a time to identify causes. If measurements show an interaction, test the smallest justified combination. Bound trial count, duration, and output size to the task budget. Save the original configuration and retain only trials that improve the chosen objective while satisfying all required bounds.

## Engine-specific tuning route

**Newton:** start with [simulation tuning](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning.rst), then [solver-specific controls](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_solvers.rst) and the feature table. Inspect the installed constructor/configuration before setting parameters. Refresh contacts every substep as a debugging baseline when using Newton's collision pipeline, then measure any reduction. Notify or rebuild solvers that cache changed model data. Treat a solver change as a model port. When using ovnewton, route through scene preparation and bridge-aware tuning first if import or synchronization is suspect.

**Ovphysx:** use the [collision](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/collision_tuning.md), [articulation](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/articulation_stability.md), [gripper](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/gripper_tuning.md), and [performance](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/performance.md) guides according to the symptom. Verify TGS/PGS, scene settings, position/velocity iterations, device/contact mode, and write support. Iteration counts do not have identical cost or physical effect across engines. Example gripper parameters are tied to its mechanism and test conditions.

Changes to friction, contact geometry, inertia, actuator force, damping, or compliance change the physical model. Explain that effect and use measurement/calibration where possible. Do not improve visual smoothness by disabling required contacts or constraints. Preserve baseline settings when no trial passes.

## Make comparisons fair and reproducible

Record scene/asset revision, conversion steps, solver and package versions, hardware/driver, device/data mode, initial states, random seeds, control law/rate, simulated duration, timestep/substeps, collision settings, environment count, reset strategy, observation payload, and acceptance criteria.

- Match the physical task and fidelity targets; identical numeric parameter values across different solvers do not guarantee equivalent physics.
- Measure startup/compilation and steady-state cost separately. Warm up consistently and synchronize CUDA work before stopping timers.
- Separate physics-only, physics plus control/read/reset, stage-publication, and rendered-application costs when useful.
- Report simulated seconds per wall-clock second, steps/s, or rollouts/s with batch size and timing boundaries. Do not interchange these metrics.
- Repeat representative trials and report spread or failure rate when variability affects the decision. Do not extrapolate one scene's ranking to all workflows.
- Keep both successful and failed trials when they explain the decision. Never use synthetic example numbers as measured results.

A useful recommendation states why the selected path meets the task, which alternative remains viable, what was actually measured, and which next check could change the choice.
