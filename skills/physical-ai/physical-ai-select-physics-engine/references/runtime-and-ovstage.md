# Runtime and ovstage integration

Read before installation, first-run diagnosis, or a shared-stage design. Use [repository routing](repositories-and-skills.md) to load the matching implementation skill. These notes identify contracts that can change the selection; they are not replacement API manuals.

For a matching small CPU request, [tested starters](tested-starters.md) supply complete pinned reproductions and API notes. Read only the relevant path here. The pins do not supersede an existing application's dependency contract.

## Select a coherent version set

| Reviewed source baseline | Relevant constraint | Required action |
| --- | --- | --- |
| Newton main, reviewed 2026-10-19 | Direct Newton documents Linux, Windows x86-64, and macOS CPU. CUDA requirements depend on the resolved Warp version. | Verify the selected Newton/solver/Warp combination and target artifact; do not infer bridge support. |
| Ovnewton 0.2.0 source | Python 3.11-3.14; Linux x86-64/aarch64 for supported non-rendering workflows; `ovstage>=0.2.0.377349,<0.3`; Newton >=1.6 and Warp >=1.17. | Resolve and record the full compatible environment; check platform/wheel availability and the intended solver. |
| Ovphysx 0.7.0 source | README documents Python 3.10+, Windows x86_64, Linux x86_64/aarch64, and AVX for prebuilt x86_64 binaries. The reviewed Python project pins `ovstage==0.3.0.1791986420`. | Inspect the selected wheel/SDK's actual dependencies and native version requirement; do not assert compatibility from broad Python/OS ranges. |
| Ovphysx 0.6.4 source skill | Earlier session/lifecycle API and bundled schema path | Use matching 0.6 docs when maintaining 0.6.4; do not paste 0.7 examples into it. |
| Ovstage main | Pre-release API and package behavior; own platform/runtime requirements | Use the engine-selected version and that version's skills/examples, not arbitrary latest ovstage. |

Evidence: [Newton README](https://github.com/newton-physics/newton/blob/0a210603f90e198fa9c8575f8d4a05f88a60d182/README.md), [ovnewton support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/e0803da8c7fd9b365f8d2e477196f06a1677b0f5/docs/site/support.md), [ovnewton package requirements](https://github.com/NVIDIA-Omniverse/ovnewton/blob/e0803da8c7fd9b365f8d2e477196f06a1677b0f5/pyproject.toml), [ovphysx quickstart](https://github.com/NVIDIA-Omniverse/PhysX/blob/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx/docs/tutorials/quickstart.md), [ovstage README](https://github.com/NVIDIA-Omniverse/ovstage/blob/fc62999ffe5abdb0330699bd2e13bbb7765f0335/README.md).

The reviewed ovnewton range excludes the ovstage version pinned by the reviewed ovphysx source. These two dependency sets cannot resolve together as written. Verify the chosen artifacts before deciding whether newer releases remove that conflict. Use isolated processes/environments for comparison when no common supported set exists. Stage exchange across processes requires a separately designed transport; two compatible-looking Python objects do not establish it. [Ovphysx Python dependency pin](https://github.com/NVIDIA-Omniverse/PhysX/blob/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx/python/pyproject.toml)

## Inspect and install within the requested scope

1. Identify the application's interpreter or native SDK, package manager, platform, lockfile, and existing stage owner. Use the optional [metadata probe](../scripts/probe_environment.py) with that interpreter. It reports package versions and declared requirements only.
2. Select a released artifact and matching documentation. Verify wheel/SDK availability, licenses, dependencies, and actual hardware requirements. Main-branch docs can precede a release.
3. Use an isolated environment for a new standalone application. Preserve a framework's tested dependencies. Prefer the project's package manager; install only the selected path and required extras.
4. Record resolved versions and run the package manager's dependency check. This confirms dependency consistency, not physics or GPU readiness.
5. Run a bounded packaged example on the selected device, then verify a representative application scene. Do not change system drivers, install a VM, or migrate a framework merely to make a setup example pass.

For Python, the package names are `newton`, `ovnewton`, and `ovphysx`; the Warp distribution is `warp-lang`. Choose version pins from the selected release. Ovphysx 0.7 requires separate `physx-usd-schemas` installation/registration. Add `newton-usd-schemas` when the chosen scene/example requires Newton schema definitions; this does **not** select the Newton engine. Optional caller-owned `pxr` authoring is separate from ovstage population. Avoid mixing incompatible USD runtimes in one process.

For native ovphysx, obtain the selected SDK and its matching ovstage archive. Follow that SDK's CMake and runtime-copy instructions. Keep package roots and resource/plugin/schema layouts intact. Rebuild native consumers when the API/ABI changes. [Quickstart](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/tutorials/quickstart.md)

## Ovphysx 0.6 to 0.7 is an API boundary

The source 0.7 changelog is dated 2026-10-14. The supplied ovphysx-selection skill used a 0.6.4 baseline. Apply the installed generation's contract:

| Operation | 0.6 pattern | Reviewed 0.7 pattern |
| --- | --- | --- |
| Attach, drain edits, detach | Checked execution before return | Returns a Task; collect success with `physx.wait_task(task)` |
| Convenient synchronous reads/writes | `read(...)`, `write(...)` with object type | `read_sync(...)`, `write_sync(...)`; low-level `read`/`write` use queries and operations |
| Write commit | Consult matching 0.6 API | `commit_sync(...)` or `commit(...).wait()`; leaving a context alone does not confirm the commit |
| Asynchronous step wait | Operation index and `wait_op` | Task and `wait_task`; integer indices are not accepted |
| PhysX schema resources | Earlier bundled-resource helpers | External `physx-usd-schemas`, registered before schema access |
| Teardown | Matching 0.6 lifecycle | Release output arrays/views, wait for detach, then destroy; preserve stage lifetime if detach fails |

Use the [migration guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx/docs/migrating_0_6_to_0_7.md) and the selected package's samples. This table is a routing aid; it is not a complete migration checklist.

The local 0.7 drop trial exposed two additional API traps: `prim_paths` can require interned IDs rather than strings, and `stage.read_attributes` requires interned attribute tokens. The [tested drop](tested-starters.md#ovphysx-drop-with-shared-stage) uses a string `pattern` filter and a stage dictionary's `intern_token` explicitly. Confirm these contracts against the installed generation rather than inferring them from similar method names.

## Shared-stage ownership and sequence

Agree on one application coordinator for stages, ordinals, controls, and publication. Reuse an existing compatible populated stage instead of reloading it. The coordinator must distinguish simulation time/step IDs from stage ordinals.

1. Register all required schemas **before the first schema read/population/export**. Late registration can leave schema fallbacks missing even if the registration call succeeds.
2. Populate the actual physics and required hierarchy. Follow the engine's documented `ALL` compatibility path for arbitrary scenes; `PHYSICS` alone can omit required native-instance traversal or transform information. Loading `ALL` does not make unsupported ovnewton physics instances supported.
3. Wait for population and seal the chosen ordinal before attachment. For an existing stage, use its actual committed ordinal, not a hard-coded 1.
4. Attach/build using the chosen engine's API and verify completion. For Newton, register solver-owned builder attributes before import, prepare/color the builder when required, and finalize before binding an existing model.
5. Apply supported inputs, complete/synchronize writes, step the solver, and read actual state. Check identity, units, device, strides, and lifetime. Use the same control object the solver consumes.
6. Publish supported output, seal its ordinal, and let rendering/other consumers read after completion. Keep output publication frequency separate from physics and control frequencies.
7. Release borrowed output resources and views before detachment/destruction. Keep the stage alive until all consumers have detached successfully.

**Ovphysx:** drain only application-authored ranges after the attached initial snapshot. Never include physics-output ordinals in the ranges sent back into physics. Clone before warmup/first step. DirectGPU data access needs the documented initialization step; read/write readiness is separate from attach success. [Integration](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/ovstage_integration.md), [cloning](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/ovphysx/docs/tutorials/cloning.md)

**Ovnewton:** the application owns solver, collision handling, states, controls, and stepping. `update_from_ovstage` applies supported state as well as drive fields. Reading stale authored state every substep can overwrite advancing simulation state. Publish the current state after state swaps. Topology changes require the documented model/binding rebuild. [Using ovnewton](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/skills/using-ovnewton/SKILL.md)

Stage ordinals control ordering/visibility; they are not historical state playback or proof of physical time. A common stage does not guarantee equivalent units, control laws, collision semantics, or object indexing across engines.

## Bounded first-run evidence

For a matching ovnewton installation on a supported host, the upstream skill provides:

```console
python -m ovnewton.examples.example_ovnewton_basic --device cpu --no-render --num-frames 8
```

This exercises a small CPU path. It does not validate GPU operation, rendering, task fidelity, or every solver. For direct Newton or ovphysx, use that version's packaged minimal example and bound its steps/duration. Inspect supported flags rather than inventing a CLI.

After the example, verify expected body/joint counts; nonempty, finite state with correct identities; motion in the expected direction; one control response; and a reset if needed. Observe a representative contact event and settling/constraint behavior before claiming task readiness. If execution is unavailable, provide the exact procedure and label it not run.

## Diagnose the failing layer

| Symptom | Check first |
| --- | --- |
| No wheel, dependency conflict, or native load failure | OS/architecture, interpreter, AVX/driver where relevant, package layout, exact dependency versions |
| Attach succeeds but bodies are absent | Schemas, population domains, disabled objects, query scope, unsupported physics |
| Empty or incomplete GPU reads | First-step readiness, task completion, attribute/device support, query identity |
| Target changes but robot does not respond | Applied drive schema, target versus state, effort limits, units, supported write and commit |
| Physics moves but renderer stays still | Current state after swap, publication, sealed ordinal, consumer ordering |
| State repeatedly jumps backward | Output fed into input, stale authored state replay, reset/controller ownership |
| Different behavior after engine migration | Imported units/mass/inertia, friction/contacts, actuator and joint semantics before parameter tuning |

Resolve the earliest failing layer. Do not remove a required physical feature merely to obtain a successful smoke test.
