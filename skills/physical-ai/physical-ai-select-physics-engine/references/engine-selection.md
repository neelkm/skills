# Decision criteria and capability evidence

Use this reference for an engine or integration decision. Sources were reviewed on **2026-10-19**. [Source snapshots](sources.md) distinguish reviewed main-branch documentation from installed releases. These are capability leads, not results from an executed simulation or benchmark.

## Make the recommendation from the workload

| Task signal | Newton path to investigate | PhysX/ovphysx path to investigate | What decides |
| --- | --- | --- | --- |
| Existing validated simulator | Keep Newton's model, controls, and solver when they meet the task | Keep PhysX assets/settings and the established integration when they meet the task | Required missing capability versus conversion, revalidation, and maintenance cost |
| New articulated-robot learning | Generalized-coordinate backends such as MuJoCo; choose from the solver feature table | Reduced-coordinate articulations, TGS/PGS, cloning, and session I/O | Required drives/constraints, reset correctness, framework support, and measured end-to-end throughput |
| Warp customization or solver research | User-defined Warp physics and multiple solver implementations | Native PhysX integration or application-side Warp processing | Whether the user must modify the dynamics implementation or only process simulation state |
| Standalone C/C++ USD service | Confirm an actual supported native embedding path; a Python Newton workflow alone does not meet a C API requirement | Documented standalone C API, native SDK, ovstage input, and DLTensor transport | Supported ABI, lifecycle, packaging, platform, and required physics |
| Python service with USD input | Direct USD import or ovnewton when live stage exchange adds value | Ovstage population plus ovphysx | Neither USD nor Python alone distinguishes the engines |
| Insertion, assembly, grasping | Verify solver/contact-pipeline combination, collision geometry, material fields, and force/effort limits | Verify primitive/convex/SDF pair support, device, cooking, offsets, friction, and force/effort limits | Measured penetration, slip, insertion success, force behavior, stability, and cost |
| Closed loops, mimic joints, tendons, specialized actuators | Check each solver's joint/property table and importer; investigate experimental Kamino or other relevant backends only with their limits explicit | Check articulation versus non-articulation constraints, mimic/tendon semantics, supported runtime writes, and device | Exact mechanism and controls must survive conversion and execute as intended |
| Required gradients through dynamics | Narrow to a documented differentiable solver and the precise state/control/parameter operations | Reviewed tensor APIs do not establish rollout automatic differentiation | Demonstrated gradient coverage and a representative numerical check; neither may meet the requirement |
| Cloth, cables, soft objects, particles | Check material law, coupling, solver, importer, and bridge separately | Check deformable/particle type, GPU requirements, contacts, attachments, I/O, and reset | Material and coupling fidelity, not the broad label "multiphysics" |
| Large replicated batches | World/environment construction, solver scaling, state/control layouts | Physics cloning and GPU data access | Isolation, reset latency, contact capacity, memory, observation transfer, and throughput |
| Live ovstage exchange | Ovnewton's import/update/publication coverage | Ovphysx's attachment, change-drain, read/write, and publication coverage | Required edits, ownership, dependency compatibility, identity preservation, and synchronization |
| Windows deployment | Direct Newton documents Windows; this does not establish standalone ovnewton support | Ovphysx documents Windows x86_64; verify the selected wheel/SDK and AVX | The complete integration, not the engine's platform list |
| CPU-only deployment | Check chosen solver/backend and all required features | CPU rigid bodies/articulations can be candidates; CPU deformables/particles are not established by CPU rigid-body support | Actual feature/device support and latency; no renderer or GPU should be added incidentally |
| Cameras, LiDAR, tactile sensing, ROS, training tasks | Existing framework integration or separately verified components | Existing framework integration or separately verified components | Full application requirements; contact data alone is not a sensor model |
| Stable deployment/distribution | Check engine, bridge, dependencies, and release policy separately | PhysX maturity does not imply a stable pre-1.0 ovphysx API | Supported artifacts, API change tolerance, licenses, and update/revalidation cost |

Primary evidence: [Newton solvers](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst), [Newton overview](https://github.com/newton-physics/newton), [ovnewton support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/support.md), [ovphysx overview](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/README.md), [ovphysx simulation setup](https://github.com/NVIDIA-Omniverse/PhysX/tree/main/ovphysx/docs/simulation_setup), and [ovphysx data limitations](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/read_write/limitations.md).

## Newton solver choice is a separate decision

The reviewed feature table distinguishes generalized coordinates from maximal coordinates. Do not rank solvers solely by their names or apply a parameter from one backend to another.

- **MuJoCo backend:** investigate for articulated rigid robots and MJCF/MuJoCo workflows. The reviewed Newton feature matrix does **not** mark it differentiable. Its default contact pipeline is MuJoCo's; choosing Newton-generated contacts changes the path that must be validated.
- **Featherstone and SemiImplicit:** the table marks basic differentiability. This does not prove every contact, actuator, friction parameter, or long rollout has usable gradients.
- **XPBD:** inspect supported joints and material behavior for the actual model. The reviewed table does not mark it differentiable.
- **VBD:** investigate unified rigid/cloth/soft-body problems. It is experimental, has limited joint support, and is not marked differentiable in the reviewed table.
- **Kamino:** investigate constrained rigid mechanisms and hard frictional contacts. It is experimental; verify joint and device coverage.
- **Steel and other/newer solvers:** use the selected release's feature and mode tables. Do not assume a solver seen on repository main exists in an older wheel.

The exact joint-property table can be decisive: a model may contain effort limits or friction fields that a solver does not enforce. Verify effective behavior, not just that an attribute can be stored. Source: [solver, contact-material, joint, and differentiation tables](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst).

## Bridge and device limits can override engine fit

**Ovnewton 0.2.0:** the reviewed support guide excludes native USD physics instances, physics PointInstancers, Newton actuators, cables, and volume deformables. Surface cloth is limited. D6 per-axis runtime state is not synchronized, and certain mimics involving D6 merges are rejected. Do not infer that direct Newton lacks these features. Do not remove a required shared-stage connection to make a direct Newton recommendation appear complete. [Support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/e0803da8c7fd9b365f8d2e477196f06a1677b0f5/docs/site/support.md)

**Ovphysx:** distinguish CPU simulation, GPU dynamics with CPU readback, and DirectGPU. Attribute availability, contact information, kinematic targets, live changes, and ownership differ across those modes. For example, the reviewed 0.7 documentation refuses kinematic-target writes on DirectGPU and does not provide detailed contact events there. Writing a pose teleports a body; it is not an equivalent kinematic target. Deformable/particle support does not imply contact-report support. [I/O limits](https://github.com/NVIDIA-Omniverse/PhysX/blob/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx/docs/read_write/limitations.md), [physics limits](https://github.com/NVIDIA-Omniverse/PhysX/blob/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx/docs/guides/limitations.md)

**Batching:** ovphysx internal clones do not create USD prims. Clone before warmup/first step. Environment IDs isolate collisions only with the documented GPU dynamics and GPU broadphase configuration; CPU copies need a validated isolation strategy such as disjoint placement. A stage clone is a different operation, and ovnewton's rejection of physics instancing must still be respected. [Cloning](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/tutorials/cloning.md)

## Record evidence without a fabricated score

Use a compact table when more than one requirement is decisive:

| Requirement and acceptance limit | Candidate path/version | Status | Source or observation | Condition or next check |
| --- | --- | --- | --- | --- |
| User's actual requirement | Engine + solver + importer/bridge + device + application | supported / supported with conditions / unsupported / unknown | Primary documentation or executed evidence | Exact constraint or discriminating test |

"Supported" means documented or demonstrated for the named path, not that the user's task has passed. Missing documentation means unknown, not unsupported. If an installed artifact contradicts main-branch documentation, preserve the observation and consult its matching release; do not silently substitute the newer contract.

When both candidates remain feasible, explain the tradeoff and use a small task comparison. Useful differentiators include existing validated assets, native API needs, custom-solver needs, gradient requirements, available framework integrations, and migration budget. Avoid defaulting to Newton for all research or to PhysX for all production.

When neither fits, name the failed requirement. Investigate a relevant alternative only as needed, such as a verified JAX/TPU path or a specialized material solver. Do not quietly relax hardware, sensor, gradient, or material requirements. Preserve a user's existing MuJoCo, Bullet, or Drake workflow when they asked only for an implementation fix.
