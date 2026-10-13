# Using the scene inspector

`scripts/inspect_scene.py` requires a supported ovnewton installation. The helper's own Python syntax needs Python 3.10+, while the initial product baseline needs Python 3.11-3.14. Run the helper with the product environment's interpreter.

```console
python scripts/inspect_scene.py assets/falling-box.usda --solver xpbd --device cpu --output inspection.json
```

Resolve script and asset paths from this skill directory. Select a fresh output filename. The helper exits 0 when model construction/binding succeeds and its limited numeric checks pass. It exits 1 on import, binding, numeric-check, or runtime errors. Argument errors use exit 2.

The JSON contains:

- Installed package versions and selected preparation solver/device.
- Body, shape, and joint counts, plus whether orphan joints were reported.
- Body labels, mass, inertia, and center of mass, along with model gravity.
- Structured import diagnostics when emitted by ovnewton.
- A separate `simulation_tested: false` field.

It does not instantiate the solver or advance time. Selecting `--solver` prepares the builder for that solver; it does not prove that the solver can execute the full model. It does not establish positive-semidefinite inertia, material correctness, complete schema coverage, control behavior, or stable contact. Zero-body scenes are reported as a finding rather than automatically invalid because a scene can intentionally contain static geometry.

Use `--output` for reliable machine consumption. Native libraries may print additional console output. The source USD file is not modified; loading its references may still require asset access and may initialize normal dependency caches.

For an already populated application stage, do not use this file-loading helper. Preserve its sealed ordinal and runtime. Follow the public construction flow, collect equivalent values, and rebuild bindings after topology changes.

## Follow with a short run

For the bundled fixture, the public basic example provides a separate CPU check:

```console
python -m ovnewton.examples.example_ovnewton_basic --stage /absolute/path/falling-box.usda --device cpu --no-render --num-frames 8
```

This is a short execution check, not a settled-contact test. The fixture's box has a 0.2 m side, initial center height 0.5 m, and explicitly authored mass 1 kg. Gravity is 9.81 m/s^2 downward. A 0.1 m-thick ground box has its top at z=0. A longer task-specific run is needed to assess impact and resting contact.

See [the installed example's source](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/ovnewton/examples/example_ovnewton_basic.py) for release-specific arguments and model preparation.
