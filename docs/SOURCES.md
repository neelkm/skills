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

## Packaging and installation

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills host integration](https://agentskills.io/client-implementation/adding-skills-support)
- [Codex local skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [NVIDIA catalog registration](https://github.com/NVIDIA/skills/blob/main/components.d/README.md)

The last link informs future catalog layout only. Publishing this repository does not register, sign, or verify these skills in NVIDIA's catalog. That would be a separate contribution using the catalog's current requirements.
