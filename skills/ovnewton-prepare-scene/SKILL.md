---
name: ovnewton-prepare-scene
description: Inspect and prepare existing USD physics for import through ovstage into Newton. Use for ovnewton compatibility checks, import failures, missing masses or drives, joint and collision issues, and unsupported schemas. Covers physics semantics and binding readiness, not CAD conversion or general USD rendering optimization.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: physical-ai
---

# Prepare a scene for ovnewton

Produce a scene whose imported physics matches the intended task. Explain each problem in terms of its affected prim and physical effect.

**For human readers:** a USD file can open and look correct while its imported mass, collisions, or joints are wrong. Successful model construction is one check; a short simulation and task-specific acceptance checks are still needed.

## Establish intent and inspect

Identify the source scene, composed layers/assets, intended mechanism, expected units, solver, and installed ovnewton/Newton versions. Reuse an existing populated stage when the application owns it. The bundled file inspector is only for a standalone process starting from a USD file.

Read [scene checks](references/scene-checks.md) for authoring semantics and feature boundaries. Compare the selected release's support guide with the actual scene. Keep findings in three categories: invalid input, unsupported physics, and recoverable import decisions. Do not silently remove constraints or deformables to obtain a successful import.

Inspect the composed physics, not only the root layer's text:

1. Check `metersPerUnit`, up axis, gravity, dimensions, and transforms. Verify the physical scale using a known dimension.
2. Check rigid/kinematic body intent, applied collision and mass schemas, final mass/inertia/center of mass, and collider ownership.
3. Check articulation roots, joint body relationships, axes, anchors, limits, drives, initial state, and intended self-collisions.
4. Check effective physics material bindings and collision filters. Confirm that the selected solver consumes the properties the task needs.
5. Identify physics instancing, unsupported schemas, D6 runtime requirements, and deformable requirements before changing the scene.

**Mass note:** an authored `physics:mass` property is not sufficient. Verify that `PhysicsMassAPI` is applied and inspect the final Newton mass. Do not assume a sample asset's apparent intent proves its imported value.

## Verify the import

Use the selected release's public `add_ovstage` / `attach_ovstage` APIs. Register schemas before the first schema read. Populate with `PopulationDomain.ALL`, seal population, then build from that sealed stage. Register solver attributes before import; color the VBD builder before finalization. Keep all assets in one composed stage for the documented one-stage/empty-builder construction path.

For a standalone file check, read [import inspection](references/import-inspection.md), then run [the inspector](scripts/inspect_scene.py) in the simulation environment:

```console
python scripts/inspect_scene.py /absolute/path/scene.usda --solver xpbd --device cpu --output inspection.json
```

Paths to the helper resolve from this skill directory. The output path is user-selected and must not already exist. The helper never saves the input stage. It builds and binds a model, captures ovnewton diagnostics, and reports final mass/inertia/gravity data and counts. It does not validate all geometry, material bindings, or dynamic behavior. Use the printed findings as evidence, not a blanket certification.

Run native USD authoring/import tools in separate processes when they use a different USD runtime. Do not mix a separately installed `pxr` authoring runtime with ovstage in the inspector process. For an application-owned stage, adapt the public flow inside its runtime instead of reloading the asset in a second stage.

## Make targeted corrections

For requested fixes, preserve source layers and make changes in an explicit output layer or copy. State changes that affect physics, including collider simplification, mass changes, material replacement, or removal of instances. Preserve joint relationships and identities. If a necessary correction requires a physical assumption the user has not supplied, explain the specific choice before making that change.

After edits, repeat model inspection and compare expected versus imported body/joint/shape counts and physical properties. Rebuild the Newton model and binding when scene topology changes. A binding prepared for the old topology cannot be reused as if its mappings updated automatically.

Run a bounded simulation using the matching installed example or application loop. Start from a collision-free initial state where the task permits. Check finite state, motion direction, joint limits, contact behavior, and any task requirement such as a fixed base or gripper coupling. A settled image alone does not prove correct masses or control semantics.

## Return useful evidence

Report the input and output scene paths, tested versions/solver, affected prim paths, import diagnostics, physical changes, final model checks, and short-run results. Keep unresolved or unsupported requirements explicit. If execution was unavailable, distinguish source inspection from unrun import and simulation checks.

The [falling-box asset](assets/falling-box.usda) is a minimal inspection fixture with an explicitly applied mass schema. It is for checking this workflow, not a task-specific tuning preset.

## Public references

- [Support and limits](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/support.md)
- [Construction, labels, diagnostics, and topology](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/concepts.md)
- [Getting started](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/getting-started.md)
- [Newton mass and inertia](https://github.com/newton-physics/newton/blob/main/docs/concepts/mass_inertia.rst)
- [Newton solver support](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst)

Main-branch pages can describe newer behavior. Confirm release-specific details before applying them.
