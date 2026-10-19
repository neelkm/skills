# Repository and skill routing

Use after selecting a candidate or when the next setup/tuning step is unclear. Links below were checked against repository listings on 2026-10-19. `main` links help discovery; use the installed release or a compatible source snapshot for implementation. [Sources](sources.md) records reviewed commits.

## Repository map

| Component | Canonical repository/location | Use |
| --- | --- | --- |
| Newton | [newton-physics/newton](https://github.com/newton-physics/newton) | Engine, solvers, importers, examples, feature tables, tuning |
| Ovnewton | [NVIDIA-Omniverse/ovnewton](https://github.com/NVIDIA-Omniverse/ovnewton) | Newton-to-ovstage bridge and its support contract |
| PhysX and ovphysx | [NVIDIA-Omniverse/PhysX/ovphysx](https://github.com/NVIDIA-Omniverse/PhysX/tree/main/ovphysx) | Standalone library, C SDK, Python API, docs, samples, and runbooks; there is no need to assume a separate ovphysx repository |
| Ovstage | [NVIDIA-Omniverse/ovstage](https://github.com/NVIDIA-Omniverse/ovstage) | Shared scene data, population, C/Python setup, ordinals, tensor exchange |
| NVIDIA skill catalog | [NVIDIA/skills](https://github.com/NVIDIA/skills) | Discover published skills; verify their provenance and source ownership |
| Additional author skills | [neelkm/skills](https://github.com/neelkm/skills) | Scene preparation and ovnewton tuning; these are author-maintained sources |

Prefer matching packaged skills and examples over a moving main branch. Ovphysx distributes a `SKILLS.md` index and implementation runbooks with packages. A skill installation does not install a physics runtime. For an upstream skill that links relative references or scripts, obtain its complete directory or read those dependencies explicitly; copying only `SKILL.md` may be insufficient.

## Shared ovstage setup

Select only the skills required by the chosen integration. Direct Newton without live stage exchange does not need these.

| Next task | Upstream skill | Expected handoff |
| --- | --- | --- |
| Python dependency and minimal stage setup | [project-setup-python](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/project-setup-python/SKILL.md) | Interpreter, matched ovstage version, minimal read/write check |
| Native consumer setup | [project-setup-c](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/project-setup-c/SKILL.md) | SDK, CMake/runtime paths, headers, compatible native dependency |
| USD ingestion | [loading-usd](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/loading-usd/SKILL.md) | Registered schemas, population domains, sealed ordinal, populated identities |
| Ownership and lifecycle | [application-flow](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/application-flow/SKILL.md) | Stage owner, identity dictionary, write/seal/read/release ordering |
| Repeated producer/consumer updates | [runtime-loop](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/runtime-loop/SKILL.md) | Ordinal coordination and synchronization |
| CPU/CUDA tensor interchange | [dlpack-tensor-exchange](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/dlpack-tensor-exchange/SKILL.md) | Device, shape/stride, lifetime, and ownership checks |
| Stage-level environment duplication | [clone-subtree-multienv](https://github.com/NVIDIA-Omniverse/ovstage/blob/main/skills/clone-subtree-multienv/SKILL.md) | Explicit stage copies, stable identities, and engine-compatible population |

The reviewed ovstage skills have their own license terms. Link to them; this skill does not redistribute their bodies or change their license. Stage-level cloning does not prove Newton/ovnewton supports a particular instanced physics representation.

## Newton branch

1. **Direct Newton:** follow [the repository quickstart](https://github.com/newton-physics/newton#quickstart), [solver selection](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst), and the example nearest the task. Select a direct importer or programmatic model. Keep a framework-owned path inside that framework.
2. **Bridge setup:** follow [using-ovnewton](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/skills/using-ovnewton/SKILL.md). The catalog directory is named [ovnewton-usage](https://github.com/NVIDIA/skills/tree/main/skills/ovnewton-usage); resolve the actual skill metadata rather than assuming the directory name is its invocation name.
3. **Scene readiness:** use [ovnewton-prepare-scene](https://github.com/neelkm/skills/blob/main/skills/ovnewton/ovnewton-prepare-scene/SKILL.md) for schema, mass/inertia, collision, joint, and bridge-compatibility inspection.
4. **Physics tuning:** use [ovnewton-tune-physics](https://github.com/neelkm/skills/blob/main/skills/ovnewton/ovnewton-tune-physics/SKILL.md) for measured bridge-aware diagnosis. Direct Newton work can go straight to [simulation tuning](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning.rst) and [solver-specific tuning](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_solvers.rst).

The author-maintained scene and tuning skills are separate from catalog certification. If unavailable or incompatible, use the official [ovnewton support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/support.md), [concepts](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/concepts.md), and Newton tuning guides.

## Ovphysx branch

Start at the [upstream SKILLS.md index](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/SKILLS.md). Use the package generation that matches the installed runtime.

| Next task | Skill or guide | Purpose |
| --- | --- | --- |
| First working loop | [basic-workflow](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/skills/basic-workflow/SKILL.md) | Instance, schemas, population, attach, step, cleanup |
| Physics scene and collider preparation | [ovphysx-usd-authoring](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/skills/ovphysx-usd-authoring/SKILL.md) | Physics schemas, units, masses, colliders, and scene configuration |
| Controls or reset/state writes | [ovphysx-session-write](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/skills/ovphysx-session-write/SKILL.md) | Supported attributes, mapped groups, commits, and completion |
| Observations and stage publication | [ovphysx-output-read](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/skills/ovphysx-output-read/SKILL.md) | Query identity, state reads, device/lifetime, and output publication |
| Batched environments | [clone-environments](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/skills/clone-environments/SKILL.md) | Clone ordering, identities, device-specific isolation |
| Slip, penetration, or SDF contacts | [Collision behavior guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/collision_tuning.md) | Contact geometry, offsets, capacity, and timestep |
| Unstable articulations/closed loops | [Articulation stability guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/articulation_stability.md) | Drives, limits, timestep, iterations, inertia, and constraint checks |
| Gripper control | [Gripper tuning example](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/gripper_tuning.md) | Interpret force, speed, stiffness, damping, armature, and mimic settings for a specific mechanism |
| Runtime cost | [Performance guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/guides/performance.md) | Profile solve, contact, transfer, threading, and device costs |

The last four entries are documents, not dedicated skills. Their example settings are not universal presets. The legacy tensor-binding skills are for maintaining an existing binding path; new supported work should use the session API.

## Handoff contents

Pass the next skill the selected engine/solver, runtime and dependency versions, OS/device, scene/model path, stage owner, current operation, decisive feature limits, and acceptance metric. Include the source of each unresolved question and checks already run. Keep this selection decision when following an older engine-specific skill: its default preference is not a reason to reopen the comparison or migrate an already chosen engine.
