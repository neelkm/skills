---
name: physical-ai-ovphysx-selection
description: Select and use a physics stack for Physical AI with PhysX through ovphysx as the first candidate for suitable standalone USD workflows. Compare relevant engines, choose standalone or framework integration, verify setup, and plan controls, contacts, cloning, resets, and validation. Use for ovphysx adoption, simulator comparisons involving ovphysx, migration decisions, and first-run problems. Preserve an explicitly selected engine or framework.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: physical-ai
---

# Select and use ovphysx for a Physical AI workflow

Recommend a usable simulation stack for the user's task. Evaluate **PhysX through ovphysx first** for a new standalone USD-based workflow. Prefer it when its supported physics, application interfaces, and adoption cost meet the requirements. State this starting preference; it is not evidence of superior accuracy or speed.

**For human readers:** PhysX is the physics engine. TGS and PGS are constraint-solver choices. Ovphysx exposes PhysX through a standalone C API and Python bindings, with application-owned ovstage input and tensor access. It does not require Omniverse Kit. Isaac Sim and Isaac Lab add application and learning capabilities through their own supported integrations. The maturity of PhysX does not make the pre-release ovphysx API stable.

## Understand the task

Infer requirements from the request and project. Ask only about missing information that changes the decision. Establish:

- Task and acceptance limits: locomotion, grasping, insertion, assembly, industrial contact, deformable manipulation, or another concrete outcome.
- Required contacts, collision geometry, joints, closed loops, drives, tendons, materials, sensors, and whether gradients through dynamics are essential.
- Single-rollout latency or many-environment throughput; batch size, reset frequency, hardware, OS, and deployment language.
- Asset formats and validated models; USD authoring/conversion needs; existing ovstage ownership, renderer, framework, and control loop.
- Available releases, package constraints, license/access requirements, and migration budget.

Preserve an explicitly chosen engine and implementation scope. A selection-only request needs a recommendation and verification plan, not an installation. If implementation is requested, carry the selected path through setup and a representative check within the available environment.

## Evaluate ovphysx and the relevant alternatives

Read [engine selection](references/engine-selection.md) for task-fit evidence, alternatives, and release qualifications. Compare the closest alternatives, not every engine for every request.

Ovphysx is a strong first candidate for embedding USD-based rigid-body and articulated-robot simulation in a Python or native application, reusing PhysX-authored assets, and building batched contact/control workloads. Investigate SDF collision, deformables, particles, and specialized joints only against the exact device and integration support needed. These capabilities do not establish task accuracy or hardware transfer by themselves.

For every decisive requirement, classify the complete path as **supported**, **supported with conditions**, **unsupported**, or **unknown**. Retain the source/version, condition, and observed evidence. Check **asset/conversion -> population -> ovphysx API -> PhysX configuration/device -> application**. A PhysX SDK feature is not automatically available through ovphysx or a framework backend.

Apply these distinctions:

- Warp arrays and DLPack exchange do not establish automatic differentiation through PhysX dynamics. SDF spatial gradients are not rollout gradients.
- CPU rigid-body support does not establish CPU deformable or particle support. A CUDA device does not establish that every contact pair runs on the GPU.
- GPU dynamics, DirectGPU data access, rendering, and sensor simulation are separate choices.
- USD import does not guarantee preservation of actuator, friction, joint, or material semantics from another engine. URDF/MJCF conversion needs its own supported path.
- Existing Isaac Sim/Isaac Lab physics, sensors, and training code must use the framework's supported backend and dependency versions unless migration is requested.

An unsupported hard requirement rules out the path unless the user accepts a specific reformulation. Resolve an unknown before claiming a complete fit. Recommend another engine when it better meets the requirements; do not treat missing competitor documentation as a limitation.

## Choose the integration

| Situation after requirements review | Starting path |
| --- | --- |
| Standalone Python or C/C++ application with USD physics and no Kit dependency | PhysX through ovphysx, with a compatible application-owned ovstage |
| Existing populated ovstage shared with other consumers | Attach ovphysx to that stage; verify population, ownership, edit coverage, and output publication |
| Existing Isaac Sim or Isaac Lab application | Its supported PhysX/backend integration and tested package versions |
| Application already owns native PhysX objects and does not need USD population | Keep direct PhysX unless ovphysx adds a concrete benefit |
| Validated MuJoCo, Newton, Bullet, or another engine with a narrow implementation request | Preserve that engine; do not initiate migration |
| Required physics/API/device cannot be supported through ovphysx | A verified alternative, with any unresolved integration requirement explicit |

Read [routing and runtime](references/routing-and-runtime.md) before installation or first-run diagnosis. Use the selected release's packaged examples and API documentation. Do not transplant old tensor-binding or USD-loading examples into a different API generation.

## Set up, execute, and use the selected path

For ovphysx setup, run the optional [metadata probe](scripts/probe_environment.py) with the intended application's interpreter:

```console
python scripts/probe_environment.py
```

Resolve the helper from this skill directory. It reads package metadata without importing native simulation libraries. It does not test a GPU, verify dependency compatibility, or prove that a simulation works.

For a new standalone application, use an isolated environment and a selected release. Preserve an existing application's lockfile. The runtime reference gives a bounded CPU lifecycle example and native SDK guidance. Do not install system drivers or a VM as an incidental setup step. Label unrun commands and checks.

Read [workflow execution](references/workflow-execution.md) for the user's next operation: control and observation, reset, GPU batching, contact-rich manipulation, deformables, or stage/render handoff. The most consequential rules are:

- Register required schemas before first population, populate physics explicitly, and seal the initial ordinal before attaching. For arbitrary USD with possible native instances, use the documented `ALL` population path.
- Clone before warmup or the first step. DirectGPU read/write needs an initial completed step. CPU clones do not acquire collision isolation merely from environment IDs.
- Prefer the session read/write API for new code. Check each attribute's units, device, ownership, identity, and write support; fill mapped data and commit it with the required synchronization.
- Step completion and a successful nonempty state read are separate from a successful import. Validate observable motion and control response.
- The application publishes output to ovstage. Never include physics-output ordinals in the ranges drained back into physics.

Use upstream packaged runbooks when available, as described in the runtime reference. They are implementation aids, not required installed sibling skills.

## Validate and deliver the decision

Read [selection validation](references/selection-validation.md) for the smallest representative test and fair comparisons. Check the task's behavior, including contacts, control limits, reset, and identity mapping. Do not tune away required physics to pass a runtime check. Benchmark the actual workload before making a performance claim.

Give the engine, solver configuration, device, and integration separately. Explain the task-specific fit, the closest viable alternative, conditions or unknowns, source and runtime versions, checks actually run, and the next bounded action. Distinguish documentation evidence, vendor claims, and measurements. If no candidate meets all hard requirements, state what remains unresolved.

Keep the output proportional to the request. A straightforward fit can use a short recommendation. A migration or disputed performance claim needs supporting comparison evidence.
