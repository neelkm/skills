# Public source provenance

Reviewed on 2026-10-13. The skill prose, helpers, evaluation cases, and minimal fixture are independently authored. Product behavior is grounded in the public sources below. No internal product documents are included or required.

## Product baselines

| Project | Reviewed public revision | Use |
| --- | --- | --- |
| ovnewton | [`f5febec0718c19a23cb8c4cfd9cfdb9a2069515e`](https://github.com/NVIDIA-Omniverse/ovnewton/tree/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e), package version 0.2.0 | Public support, requirements, bridge APIs, examples, and output contracts |
| Newton | [`1624cc70e2e030ca3dca6772b4243900202d24fb`](https://github.com/newton-physics/newton/tree/1624cc70e2e030ca3dca6772b4243900202d24fb) | Diagnostic reasoning and solver documentation; exact options still require installed-version checks |

The CPU CI baseline pins ovnewton 0.2.0, Newton 1.6.0, and Warp 1.17.0. Other transitive dependencies resolve within the package constraints. This is not a fully locked environment; record the actual resolved package versions when reproducing a run.

## Ovnewton references

- [Requirements](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/pyproject.toml)
- [Getting started](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/docs/site/getting-started.md)
- [Support](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/docs/site/support.md)
- [Concepts](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/docs/site/concepts.md)
- [Output reads](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/docs/site/output-reads.md)
- [Basic example](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/ovnewton/examples/example_ovnewton_basic.py)

## Newton references

- [Installation](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/guide/installation.rst)
- [Solver capabilities](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/solvers/index.rst)
- [Tuning](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/concepts/simulation_tuning.rst)
- [Solver tuning reference](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/concepts/simulation_tuning_solvers.rst)
- [USD parsing](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/concepts/usd_parsing.rst)
- [Viewers](https://github.com/newton-physics/newton/blob/1624cc70e2e030ca3dca6772b4243900202d24fb/docs/guide/visualization.rst)

## Expanded engine selection (skill version 0.2.0)

Reviewed on 2026-10-13. These current sources support the broader task-selection guidance, not a claim that every engine was installed or benchmarked. Latest/main pages can describe features newer than the pinned CPU runtime. Recommendations are task-dependent interpretations of the documented capabilities.

- [Newton overview and asset formats](https://newton-physics.github.io/newton/latest/guide/overview.html)
- [Newton replicated worlds](https://newton-physics.github.io/newton/latest/concepts/worlds.html)
- [Newton solver and differentiation matrix](https://newton-physics.github.io/newton/latest/solvers/index.html)
- [Newton deformable objects](https://newton-physics.github.io/newton/latest/concepts/deformable_objects.html)
- [Newton experimental coupled solvers](https://newton-physics.github.io/newton/latest/concepts/coupling.html)
- [Newton manipulation and contact capabilities](https://developer.nvidia.com/blog/newton-adds-contact-rich-manipulation-and-locomotion-capabilities-for-industrial-robotics/)
- [Isaac Lab](https://developer.nvidia.com/isaac/lab)
- [Isaac Sim 6.1 Newton integration and limitations](https://docs.isaacsim.omniverse.nvidia.com/6.1.0/physics/newton_physics.html)
- [PhysX](https://developer.nvidia.com/physx-sdk)
- [MuJoCo MJX implementations and differentiation](https://mujoco.readthedocs.io/en/stable/mjx.html)
- [Bullet/PyBullet](https://github.com/bulletphysics/bullet3)
- [VSim Robotics technology](https://www.vsimrobotics.ai/simulations-and-training)
- [Genesis World](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/what_is_genesis.html)
- [Drake](https://drake.mit.edu/)

VSim refers to VSim Robotics at vsimrobotics.ai. Its public technology page was read directly when the web reader could not load it. The page's capabilities are vendor claims; detailed API/gradient coverage and comparable performance were not verified. Its reviewed page labels USD support as incoming. Missing public details are treated as unknown, not as unsupported.

## Ovphysx selection and execution (skill version 0.1.0)

Reviewed on 2026-10-14 against public ovphysx 0.6.4 and [NVIDIA-Omniverse/PhysX commit `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`](https://github.com/NVIDIA-Omniverse/PhysX/tree/6dc53585d7db07346f53d0598a5fd3bfdce47d8d/ovphysx), dated 2026-10-09. The new skill uses the existing selection skill's structure and public product sources. No internal SDK documentation is included or required.

The skill's references link directly to the corresponding versioned overview, quickstart, developer guide, simulation-setup pages, population/ordinal contract, session read/write contract, clone tutorial, and upstream runbook index. The CPU example is adapted from the documented lifecycle and session API; it is not a runtime test result. Alternative-engine links are routes for task-specific verification, not a new cross-engine qualification or benchmark.

The current source snapshot resolves a packaging difference in older pages: USD ingestion and its runtime come from the matching ovstage package. It also supplies important conditions for early schema registration, native-instance population, clone ordering and isolation, DirectGPU initialization, mixed angular units, and explicit output publication. Check the selected artifact's documentation when a later release changes these contracts.

## Packaging and installation

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills host integration](https://agentskills.io/client-implementation/adding-skills-support)
- [Codex local skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [NVIDIA catalog registration](https://github.com/NVIDIA/skills/blob/main/components.d/README.md)

The last link informs future catalog layout only. Publishing this repository does not register, sign, or verify these skills in NVIDIA's catalog. That would be a separate contribution using the catalog's current requirements.
