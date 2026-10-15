# Integration and runtime setup

Use after engine selection or when diagnosing ovphysx setup. Baseline: public ovphysx 0.6.4, reviewed 2026-10-14. Use matching installed documentation if the runtime differs. The source baseline is [commit 6dc5358](https://github.com/NVIDIA-Omniverse/PhysX/tree/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx).

## Choose an owner and a supported runtime

Standalone ovphysx consumes an application-owned ovstage. Reuse an existing compatible stage and runtime. For an Isaac Sim/Isaac Lab project, use its release's backend and locked packages; installing the newest standalone wheel is not a framework upgrade procedure. Direct PhysX remains a reasonable path when the application already owns PhysX objects and needs no USD population.

The baseline documents Python 3.10+, Windows x86_64, and Linux x86_64/aarch64. Check actual wheel availability and dependencies for the selected Python version. Prebuilt x86_64 binaries require AVX. CPU rigid-body simulation needs no NVIDIA driver or CUDA Toolkit. GPU dynamics needs a supported NVIDIA GPU and compatible driver; the reviewed quickstart specifies Volta/SM 7.0 or later and CUDA 12.8 driver compatibility. Building from source has additional requirements. Do not infer rendering readiness from physics readiness. [Overview](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/ovphysx_overview.html), [Quickstart](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/tutorials/quickstart.html)

## Inspect before installing

Run [the metadata probe](../scripts/probe_environment.py) using the intended application interpreter:

```console
python scripts/probe_environment.py
```

It uses the standard library and records interpreter, platform, package versions, and ovphysx/ovstage requirements. It does not import simulation packages, resolve requirements, detect AVX, inspect a GPU, or run physics. A missing package is information, not a failed simulation. An SDK-only C++ installation may have no Python package metadata.

For a new standalone Python application, create an isolated environment using the project's package manager. A reproducible installation of the documented baseline is:

```console
python -m pip install "ovphysx==0.6.4"
python -m pip check
```

Verify that this artifact exists for the target before prescribing it. Let its declared dependency select ovstage; do not replace it with an arbitrary latest version. Record resolved versions after a successful test. The ovphysx runtime uses the matched ovstage package's USD ingestion/runtime; do not infer packaging from older documentation. Add `usd-core` only for caller-owned `pxr` authoring when needed. Add and register `newton-usd-schemas` if the scene actually authors `newton:*` attributes. This schema package does not select the Newton engine. [Source quickstart](https://github.com/NVIDIA-Omniverse/PhysX/blob/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx/docs/tutorials/quickstart.md)

## Bounded CPU lifecycle check

Run this in a fresh process after verifying the installed API. It uses the packaged rigid-body scene, forces CPU mode before creating an instance, runs eight steps, and checks that a rigid-body position read is nonempty. It is a lifecycle/data check, not proof of correct motion or task fidelity. Follow it with the motion check below. This example is source-derived; it is not a claim that the skill author executed it.

```python
from pathlib import Path

import ovphysx
import ovstage
from ovphysx import PhysX
from ovphysx.types import SimObjectType

scene = Path(ovphysx.__file__).resolve().parent / "samples/data/simple_physics_scene.usda"
if not scene.is_file():
    raise FileNotFoundError(scene)

PhysX.set_cpu_mode(True)
ovstage.population.register_usd_schemas([str(ovphysx.codeless_schema_root())])
stage = ovstage.Stage("ovphysx-cpu-check")
physx = None
attached = False
try:
    ovstage.population.open_usd(
        stage, str(scene), ordinal=1, domains=ovstage.PopulationDomain.ALL
    )
    stage.advance_write_floor(ordinal=1).wait()
    physx = PhysX()
    physx.attach_ovstage(stage, read_ordinal=1)
    attached = True
    for _ in range(8):
        physx.step_sync(1.0 / 60.0)
    with physx.read(SimObjectType.RIGID_BODY, ["position"]) as result:
        value_count = sum(t.size for group in result.groups for t in group.tensors)
    if value_count == 0:
        raise RuntimeError("No rigid-body positions were returned")
    print("CPU lifecycle check completed: 8 steps and a nonempty position read")
finally:
    try:
        if physx is not None:
            try:
                if attached:
                    physx.detach_ovstage()
            finally:
                physx.destroy()
    finally:
        stage.destroy()
```

Adapted from the [quickstart](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/tutorials/quickstart.html) and [session API](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/read_write/index.html). For a CPU-only guarantee, keep the hard CPU mode in a fresh process; it cannot be undone in that process. GPU checks require a separate process and GPU-authored scene settings.

For a meaningful motion check, identify a dynamic body by its returned prim identity and copy its positions at two completed steps while it is falling. Check finite values and displacement in the gravity direction against the scene's initial conditions. Extend the bounded run through ground contact and verify settling within chosen tolerances. Zero matching rows, omitted attributes, or merely successful attachment must not be reported as passed physics.

## Native C/C++ route

Download the selected ovphysx SDK and the matching ovstage native archive for the platform. The SDK's `ovphysx_OVSTAGE_VERSION` in `lib/cmake/ovphysx/ovphysxConfig.cmake` identifies the companion version. Keep the package roots separate. Configure the bundled `samples/c_samples/hello_world_c` using both roots in `CMAKE_PREFIX_PATH`, then build and run it with the documented runtime layout. Use the package's CMake runtime-copy helper on Windows. Do not overlay the archives or copy only the principal DLL while omitting plugins and schemas. [Native quickstart](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/tutorials/quickstart.html)

The C lifecycle includes process initialize/shutdown, instance create/destroy, schema registration, stage population/sealing, attach, synchronized stepping, and handle release. Capture the last error on the calling thread before cleanup overwrites it. Release read/write/contact resources before detaching; keep the stage alive through detachment. [Developer guide](https://nvidia-omniverse.github.io/PhysX/ovphysx/0.6.4/developer_guide.html)

## Use the shipped implementation guidance

Ovphysx wheels and native SDKs ship `SKILLS.md` and a `skills/` directory. Locate them inside the selected package; do not assume they are installed as discoverable host skills. Read only the relevant runbook: `basic-workflow`, `ovphysx-usd-authoring`, `ovphysx-session-write`, `ovphysx-output-read`, or `clone-environments`. Their public equivalents are indexed in [the upstream skills directory](https://github.com/NVIDIA-Omniverse/PhysX/blob/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx/SKILLS.md).

The tensor-binding API is deprecated in the 0.6 generation. Maintain it when required by existing code or a documented session-API gap; use session read/write for new supported work. Contact bindings are a separate current API. If upstream runbooks are unavailable, use matching API docs and samples; this skill has no installed sibling-skill dependency.

## Diagnose the failing layer

| Evidence | Next check |
| --- | --- |
| No matching wheel / dependency conflict | Interpreter, platform, artifact availability, application lockfile, exact ovstage requirement |
| Native initialization fails | AVX, package/plugin/schema layout, compatible libraries, actual error message |
| Attach succeeds but required bodies are missing | Population domain, schemas registered before population, native instancing, selected object type, disabled objects |
| GPU data is empty or write commit fails before stepping | DirectGPU first-step precondition; clone before that step |
| CPU works and CUDA fails | Selected device, scene GPU configuration, driver compatibility, collision/device requirements |
| Control target reads correctly but robot does not move | State rather than target readback, drive mode/limits, units, commit/synchronization, body enablement |
| Simulation advances but renderer is static | Explicit output publication, sealed output ordinal, consumer update ordering, pose/hierarchy semantics |
| Independent instances conflict | Process-global attachment and configuration constraints; use separate processes where required |

Do not remove constraints or change the physical task to make setup pass. Use a packaged minimal scene to distinguish runtime failure from asset failure. On an unsupported host, provide a concrete supported-host procedure and label it not run.
