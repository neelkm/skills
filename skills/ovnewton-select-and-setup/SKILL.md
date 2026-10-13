---
name: ovnewton-select-and-setup
description: Assess whether a Physical AI workflow needs the Newton-to-ovstage bridge, then install and verify ovnewton. Use for Newton/Omniverse selection, CPU or CUDA setup, dependency conflicts, and first-run failures. Route standalone Newton tasks without stage integration to direct Newton.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: physical-ai
---

# Select and set up ovnewton

Help the user choose the smallest appropriate simulation stack and establish a verified starting point. Explain the choice in terms of the user's workflow.

**For human readers:** Newton computes physics. Ovnewton connects Newton to a populated Omniverse stage. A USD input file or a request for an RTX viewer does not, by itself, require this bridge.

## Decide whether the bridge is useful

Determine the input asset or existing stage, required physics, intended outputs, execution host, and whether the user already selected a framework. Infer these from the project where possible. Ask only for a missing decision that changes the implementation.

- Choose ovnewton when the application needs to build from an existing ovstage, consume supported stage state/drive changes, or publish Newton motion into a shared stage.
- Choose direct Newton when a standalone Python, URDF, MJCF, or USD simulation needs no ovstage binding. Newton already has importers and viewers. Do not add ovnewton merely for GPU physics or USD input.
- Preserve an established Isaac Sim, Isaac Lab, or other application runtime. Use its supported integration and dependency constraints rather than replacing its environment.
- Check required model features against the selected ovnewton release. A solver feature in Newton is not proof that ovstage population and ovnewton transport support it.

Read [routing and runtime notes](references/routing-and-runtime.md) when making the choice or resolving a setup failure.

## Inspect before installing

Use the intended application's Python interpreter to run [the metadata probe](scripts/probe_environment.py):

```console
python scripts/probe_environment.py
```

Resolve this path from the installed skill directory. The helper needs Python 3.10+ and only the standard library. It reads Python, OS, architecture, installed versions, and ovnewton's declared requirements. It does not import Newton/ovstage, inspect credentials, install packages, or test a GPU.

Record the requested product version, actual interpreter, platform, and intended physics/render devices. Treat metadata as evidence of installation only. Check the release's supported OS, Python range, dependency constraints, and Warp/driver compatibility before running native code.

**Version note:** the initial public baseline is ovnewton 0.2.0. Its dependency ranges differ from later development builds. Read the installed package metadata or the chosen release's `pyproject.toml`; do not substitute an arbitrary ovstage build or apply Newton-main APIs to an older installation.

## Establish the runtime

For a new standalone application, use an isolated environment on a supported host. For an existing application, follow its lockfile and package-management convention. Choose the package manager already used by the project.

Within that environment, the public installation paths are:

```console
python -m pip install ovnewton
python -m pip check
```

Pin the chosen version when reproducibility is required. Install `"ovnewton[examples]"` only when the workflow needs its rendering or MuJoCo-Warp dependencies. Package extras do not establish that the hardware supports rendering.

Start with the smallest relevant check. For an undecided standalone workflow, the documented CPU test avoids requiring a renderer:

```console
python -m ovnewton.examples.example_ovnewton_basic --device cpu --no-render --num-frames 8
```

For a selected CUDA or rendered workflow, follow the matching installed example's `--help` and public getting-started guide. Verify physics and rendering separately. CPU physics can coexist with GPU rendering, but OVRTX still needs a compatible RTX-capable GPU and driver. `--headless` can still render; `--no-render` disables rendering in the basic example.

On a host outside ovnewton's supported runtime, give a concrete supported-host path. Do not describe a successful direct-Newton Windows run as proof that ovnewton works there. Do not install a VM or change system drivers as an incidental setup step.

## Diagnose and finish

Separate package resolution, native-library loading, CUDA initialization, scene import, solver execution, and rendering failures. Preserve the failing command and actionable error. Check one evidence-based correction at a time; do not cycle through unrelated package versions.

The result should state:

- Why ovnewton or direct Newton fits the task, including any unsupported requirement.
- The environment and dependency versions actually observed.
- Which smoke command ran, its outcome, and what remains untested.
- The next task-specific action, such as importing the user's scene or enabling rendering.

If execution tools or a supported runtime are unavailable, provide the exact verification steps and label them **not run**. A metadata probe is not a passed simulation test.

## Public references

- [Ovnewton getting started](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/getting-started.md)
- [Ovnewton support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/support.md)
- [Ovnewton package requirements](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/pyproject.toml)
- [Newton installation](https://github.com/newton-physics/newton/blob/main/docs/guide/installation.rst)
- [Newton viewers](https://github.com/newton-physics/newton/blob/main/docs/guide/visualization.rst)

These links track main. For exact commands and APIs, select the corresponding release or inspect the installed public API.
