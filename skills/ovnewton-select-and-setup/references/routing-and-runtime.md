# Routing and runtime notes

## Task selection

| Request | Preferred starting point | Reason |
| --- | --- | --- |
| Run a URDF/MJCF robot in a standalone loop | Direct Newton | No stage binding is required. |
| Import a USD file and inspect a trajectory | Direct Newton unless a shared stage is required | Newton has `ModelBuilder.add_usd()` and viewers. |
| Simulate physics in a populated ovstage | Ovnewton | The model is built from populated stage data. |
| Receive drive targets from stage edits | Ovnewton, after checking supported fields | The persistent binding consumes sealed updates. |
| Publish motion for an existing Omniverse consumer | Ovnewton | It maintains the stage-to-model identity mapping and state transfer. |
| Train in an established framework | The framework's supported runtime | Training, reset logic, and batched environments are application responsibilities. |

The bridge pipeline is **USD -> ovpopulation -> ovstage -> ovnewton -> Newton**. Newton does not parse USD in this path. An application-owned model can also be bound when its body and joint labels match stage paths.

## Public 0.2.0 baseline

This is a documentation baseline, not a promise about every dependency combination:

- Python 3.11 through 3.14.
- Linux is the documented ovnewton runtime; verify architecture-specific wheels for the chosen release. Newton's broader OS support does not extend the ovnewton package automatically.
- The public package declares `ovstage>=0.2.0.377349,<0.3`, Newton >=1.6.0, and Warp >=1.17.0. The examples extra declares OVRTX >=0.5.0.377615,<0.6.
- CPU non-rendering is supported. Rendering additionally requires a supported RTX-capable GPU and driver.
- Warp wheel versions have their own hardware/driver requirements. Do not infer GPU readiness from the presence of an NVIDIA device or the package name.

Read the selected release's requirements before reproducing these values. The exact qualified environment can be narrower than open dependency ranges. Save the resolved versions after a successful test.

## Diagnostic decisions

| Evidence | Next useful check |
| --- | --- |
| No compatible distribution | Python, OS, architecture, and selected package version |
| Resolver conflict | Existing application constraints and declared dependency ranges |
| Native library import fails | Wheel/platform compatibility and process library environment |
| CPU smoke succeeds, CUDA fails | Warp initialization, selected CUDA device, and driver compatibility |
| Simulation succeeds, rendering fails | OVRTX dependencies, RTX device, renderer initialization, and output configuration |
| Scene import fails | Applied schemas, supported physics, units, and the reported prim path |
| A stage consumer sees old data | Publication ordering, sealed write floor, and the consumer's synchronization |

Do not remove physical constraints to make an installation check pass. Use the packaged basic scene to separate runtime problems from the user's model problems.

## Runtime ownership

The application owns state allocation, controls, collision detection, solver stepping, and timing. MuJoCo and VBD need their solver attributes registered on the builder before `add_ovstage`; VBD needs builder coloring before finalization. Use the installed example as the starting point rather than translating parameter names between solvers.

For the documented ovnewton MuJoCo path, MuJoCo-Warp advances the model and Newton's collision pipeline supplies contacts (`use_mujoco_contacts=False`). Choosing this solver does not require authoring MuJoCo-specific USD schemas.

## Sources

- [Public 0.2.0 requirements snapshot](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/pyproject.toml)
- [Getting started](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/getting-started.md)
- [Newton installation and Warp compatibility](https://github.com/newton-physics/newton/blob/main/docs/guide/installation.rst)
