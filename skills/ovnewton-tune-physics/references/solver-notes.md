# Solver-specific reasoning

This reference explains decisions rather than prescribing numeric presets. Confirm exact options in the installed release. Contact stiffness, iteration counts, and drive gains do not have interchangeable effects across backends.

## XPBD

Use as the documented basic-example starting point when its feature set fits the task. Check timestep, substeps, iteration convergence, contact geometry, and actual supported joint properties. Do not infer effort-limit or friction enforcement merely because the model stores those arrays.

## MuJoCo-Warp

The documented ovnewton path registers `SolverMuJoCo` custom attributes before population and uses Newton contacts through `use_mujoco_contacts=False`. Selecting this solver does not require MuJoCo-authored USD schemas.

Distinguish contact-capacity failures from convergence failures. Inspect the installed constructor before changing capacities such as `njmax` or `nconmax`, or options such as integrator, iterations, tolerances, and friction cone. Do not use native MuJoCo CPU execution as an unexplained replacement for the intended Warp backend.

Newton material stiffness/damping can map into MuJoCo constraint parameters. Interpret the active mapping and backend, rather than treating every value as a simple world-space spring. Stiffer contact can worsen conditioning or jitter. Do not import private constants or use guessed enum integers to select undocumented behavior.

## VBD

Register custom attributes before `add_ovstage`, then call `builder.color()` before finalization. Confirm the installed VBD contact formulation and defaults. Compliant ALM and legacy penalty settings can behave differently across releases. A legacy knob may exist but not affect the active formulation.

VBD supports more deformable workflows in Newton than ovnewton can necessarily populate. Verify the bridge's cloth/soft-body support before proposing a solver switch as a solution. Newton's detailed VBD tuning guide is under development; do not present its planned sections as tested recipes.

## Updating the model

Prefer explicit builder defaults before import or correctly applied scene properties when those express the user's intent. After finalization, some solvers cache model values. Use their documented change-notification or rebuild mechanism. Recreate bindings after changes to topology or identity mappings.

Do not let unconditional stage ingress overwrite newly computed Newton state with an old stage snapshot. For an external controller, distinguish direct Newton controls from the narrower stage-edit ingress contract.

## Sources

- [Newton solver capability tables](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst)
- [Tuning reference](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_solvers.rst)
- [MuJoCo tuning](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_mujoco.rst)
- [VBD tuning status](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_vbd.rst)
- [Ovnewton solver preparation](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/getting-started.md)
