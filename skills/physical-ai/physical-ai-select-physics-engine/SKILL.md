---
name: physical-ai-select-physics-engine
description: Select Newton or PhysX through ovphysx for Physical AI, robotics, robot learning, manipulation, assembly, or simulation services. Compare task requirements, solver and device support, asset semantics, gradients, integration cost, and deployment constraints without a default engine preference. Route the selected path to its repository, ovstage setup, scene preparation, runtime skills, and physics tuning guidance. Use for engine comparisons, adoption, migration, and unresolved stack selection; preserve an explicitly selected engine.
license: Apache-2.0
metadata:
  author: Neelakantan Mani <neelakantanm@nvidia.com>
  version: "0.2.0"
  category: physical-ai
  tags: "newton, ovnewton, physx, ovphysx, ovstage, physics-engine-selection"
  reviewed: "2026-10-19"
---

# Select a physics engine for Physical AI

Recommend the smallest supported stack that satisfies the physical task and fits the application. Compare **Newton** with **PhysX through ovphysx** on the same requirements. Neither engine wins by default. Retain an established stack when changing it offers no demonstrated benefit. If neither candidate satisfies a hard requirement, say so and investigate a relevant alternative instead of forcing a choice.

For a human reader: Newton and PhysX are engines. Newton has several solver backends; PhysX offers TGS and PGS constraint solvers. **Ovnewton** connects Newton to ovstage. **Ovphysx** exposes PhysX to standalone C/C++ and Python applications using ovstage. **Ovstage** holds shared scene data; it does not solve physics. Isaac Sim and Isaac Lab are application/framework layers with their own backend contracts.

## Short path for a small request

Use this path when the request has a clear outcome and a small scene. Do not load every reference or install both engines to make a straightforward choice.

1. Identify the decisive requirement: an existing stack, rollout gradients, a shared stage, required physics, or deployment constraints. Confirm the selected **engine + solver + integration + device** meets it. If it is unknown, read only the relevant part of [capability evidence](references/engine-selection.md). Use the fuller comparison below for unresolved tradeoffs.
2. Give the choice and its reason briefly. Selection-only requests stop there with a next check. For implementation, follow the selected [repository/skill route](references/repositories-and-skills.md); read only the applicable runtime section.
3. For a small matching CPU task, use [tested starters and API notes](references/tested-starters.md): ovphysx shared-stage drop, direct Newton differentiable spring, or direct Newton grasp. Copy only the chosen starter into the user's working directory. Preserve an existing environment's dependencies; these version pins are reproductions, not upgrade instructions or engine preferences.
4. Run the example and its saved-output checks. Report task success separately from unmeasured fidelity, contacts, rendering, and hardware transfer. A failed run needs diagnosis of the failing layer, not an automatic engine switch.

These examples do not settle ambiguous robot-learning, contact-fidelity, GPU, or migration decisions. For those, use the requirements and comparison workflow below. Reusable checks are in [validation and tuning](references/validation-and-tuning.md).

## 1. Establish the decision and scope

Use the request, project files, and existing measurements before asking questions. Ask only about missing information that could change the choice. Separate hard requirements from preferences:

| Requirement | Information to establish |
| --- | --- |
| Outcome | Task, representative scene, success metric, fidelity tolerance, and unacceptable failures |
| Physics | Rigid bodies, contact geometry, friction, joints/closed loops, drives/actuators/tendons, deformables, particles, and required coupling |
| Learning/control | Control rate, reset behavior, observations, action semantics, and whether gradients through dynamics are essential |
| Workload | Batch size, single-rollout latency, end-to-end throughput, memory budget, run duration, and reproducibility needs |
| Assets | USD, URDF, MJCF, or CAD; validated models, conversion path, units, and semantics that must survive import |
| Deployment | OS/architecture, Python or C/C++, GPU/driver, CPU-only constraints, package availability, and distribution terms |
| Integration | Existing framework, stage owner, live edits, renderer/sensors, data interfaces, and dependency lockfile |
| Adoption cost | Team expertise, API stability needs, migration effort, and available validation budget |

Preserve a chosen engine when the user requests implementation. Do not activate a selection workflow for an unrelated USD edit or a narrow fix in an established simulator. Selection-only work ends with a recommendation and a verification plan. When implementation is requested, continue into the chosen setup and checks within that scope.

## 2. Compare complete candidate paths

For unresolved selection, read the relevant [decision criteria and capability evidence](references/engine-selection.md). Evaluate these paths as applicable:

- Direct Newton with a named solver and supported asset importer.
- Newton + ovnewton with a compatible ovstage and verified bridge coverage.
- PhysX through ovphysx with a named solver configuration and device/data-access mode.
- The existing framework's supported backend, when that framework owns the application.

For each decisive requirement, record **supported**, **supported with conditions**, **unsupported**, or **unknown**, plus the exact version/source, condition, and evidence. Check the whole path:

**asset/conversion -> population/import -> engine and solver -> device and data API -> integration -> application**.

An unsupported hard requirement excludes that path unless the user accepts a specific reformulation. An unknown remains unresolved until checked. Use preferences to choose among feasible paths; never hide a hard failure behind a weighted score. If both fit, prefer lower adoption cost and the better evidence for this task. If that does not distinguish them, propose the smallest representative comparison and give a provisional recommendation with its conditions.

Apply these distinctions throughout:

- GPU compute, batched simulation, USD input, and robot learning do not uniquely select either engine.
- Newton's differentiability is solver- and operation-specific. Warp arrays, DLPack, and SDF spatial gradients do not establish gradients through a PhysX rollout. Neither stage exchange nor rendering is automatically differentiable.
- Engine capability does not guarantee importer, bridge, framework, or device support. Ovnewton limitations are not direct Newton limitations.
- A shared data stage does not guarantee interchangeable engine state, compatible package versions, or coupled physics. Do not propose two engines driving the same bodies without a supported coupling design.
- A contact signal is not a calibrated tactile sensor. Neither standalone library supplies a complete training, ROS, rendering, or sensor application by itself.
- Do not invent relative speed, accuracy, determinism, or sim-to-real claims. Distinguish documented support, vendor claims, and measured results.

## 3. Choose the integration and hand off

| Selected situation | Path and next guidance |
| --- | --- |
| Newton with no live shared-stage requirement | [Direct Newton](https://github.com/newton-physics/newton); use its solver, import, and tuning documentation |
| Newton must exchange supported state with an application-owned ovstage | [Ovnewton](https://github.com/NVIDIA-Omniverse/ovnewton); follow the `using-ovnewton` skill after checking bridge support |
| Standalone USD-based Python or native PhysX application | [Ovphysx in the PhysX repository](https://github.com/NVIDIA-Omniverse/PhysX/tree/main/ovphysx); start with `basic-workflow` |
| Application already owns native PhysX objects and needs no ovstage | Preserve direct PhysX unless a concrete benefit justifies adopting ovphysx |
| Isaac Sim, Isaac Lab, or another existing framework | Use that release's supported backend and dependency set; do not insert arbitrary standalone packages |

Read [repository and skill routing](references/repositories-and-skills.md) for exact links and the sequence **runtime setup -> ovstage population -> engine attachment -> control/readback -> tuning**. The route names are upstream skills, not a promise that they are installed locally. Load the matching installed skill when available; otherwise read the selected release's upstream file and its linked examples. State the fallback if a skill cannot be accessed. Do not invent a skill name or infer NVIDIA catalog approval from its presence in a personal repository.

## 4. Establish a working runtime

Before installation or first-run work, read the applicable sections of [runtime and ovstage integration](references/runtime-and-ovstage.md), or the matching [tested starter](references/tested-starters.md) for its bounded reproduction. Record the selected artifact/release and its actual dependencies. Reuse application-owned stages and preserve lockfiles. For comparisons, use separate environments when dependency ranges differ.

The optional metadata-only probe is:

```console
python scripts/probe_environment.py
```

Resolve the helper from this skill directory and run it with the application's interpreter. It inventories versions and declared requirements without importing native simulation libraries. Missing packages are not simulation failures; successful metadata inspection is not runtime validation.

Use matching packaged examples for a bounded first run. Confirm populated objects, finite changing state, control response, and completed work. An import, successful attachment, empty query, or enqueued GPU operation is insufficient. Keep CPU physics, GPU physics, and rendering checks separate. Report anything not run.

## 5. Validate the task and route tuning

Read [task validation and physics tuning](references/validation-and-tuning.md). Confirm model correctness before tuning solver parameters. Check units, mass/inertia, joint mapping, collisions, controls, and stage synchronization. Then run bounded experiments against stated task metrics and acceptance limits.

For Newton, use the official solver feature/tuning guides; use `ovnewton-prepare-scene` and `ovnewton-tune-physics` when the bridge is involved. For ovphysx, use its authoring/control/readback skills and official collision, articulation, gripper, and performance guides. No dedicated ovphysx tuning skill was found in the reviewed upstream skill index; route to the guides rather than inventing one.

## 6. Return a decision the user can act on

Give the following, at a depth appropriate to the request:

1. Engine, solver/backend, device/data mode, and integration as separate choices; mark the recommendation provisional when evidence is incomplete.
2. The task-specific reasons and the closest alternative's tradeoffs, including migration cost.
3. Decisive capability statuses, unresolved requirements, versions, and source links.
4. Checks actually run, observed results, and remaining acceptance tests.
5. The exact repository and next skill/document, with a bounded setup or tuning action.

Honor the user's report format and writing preferences. A straightforward choice can use a short answer; a migration or performance claim needs supporting evidence.

## Examples

- "Choose Newton or ovphysx for a Windows C++ USD robot service." Check native SDK, platform, PhysX asset reuse, and required physics; distinguish direct Newton support from ovnewton support.
- "Select a stack for a GPU grasp-and-insert learner with URDF assets." Compare contacts, control, batching/reset, conversion, and framework integration. GPU or RL alone does not decide the engine.
- "We chose Newton and already own an ovstage; help with slipping grasps." Preserve Newton, check bridge and asset semantics, then route to measured tuning.

## Tools and provenance

Selection needs project-file access and authoritative documentation. Setup additionally needs an appropriate shell, package access, and a supported runtime; GPU checks need the selected hardware and driver. The probe needs only Python's standard library. No product credential or MCP server is required. Inspect schemas, dependencies, and source revisions before reusing examples from `main` or `latest`.

See [sources and provenance](references/sources.md) for the two source skills, reviewed snapshots, licensing distinctions, and evidence limits. This is a local authoring draft; evaluation and signing status is recorded in [the draft skill card](skill-card.md) and [evaluation instructions](evals/EVAL.md).
