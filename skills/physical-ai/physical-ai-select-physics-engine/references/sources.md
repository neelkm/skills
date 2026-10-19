# Sources and provenance

Reviewed **2026-10-19**. This skill combines two task-selection workflows and replaces their opposite starting preferences with a symmetric requirements-based decision. It adds explicit handoffs to verified repository skills and documents. It does not copy their evaluation results or signatures.

## Source skills

- [NVIDIA physical-ai-physics-selection](https://github.com/NVIDIA/skills/blob/main/skills/physical-ai-physics-selection/SKILL.md), version 0.2.0, authored by Neelakantan Mani. Reviewed file blob: `a673105b6a5f54ce8da9b546514f8f148b7e668a`. Its matching product-source snapshot is [ovnewton commit e0803da](https://github.com/NVIDIA-Omniverse/ovnewton/blob/e0803da8c7fd9b365f8d2e477196f06a1677b0f5/skills/physical-ai-physics-selection/SKILL.md).
- [Ovphysx-selection](https://github.com/neelkm/skills/blob/b1eed0c26d95a3df25ff566617be482664d864b2/skills/ovphysx/ovphysx-selection/SKILL.md), version 0.2.0, authored by Neelakantan Mani. Reviewed file blob: `a3496eb3ac11414ffb3d5ace90b86aa824193336`. Its references use ovphysx 0.6.4; the combined skill explicitly distinguishes that baseline from later 0.7 source documentation.

Both source skill entrypoints declare Apache-2.0. The new skill retains that license and source attribution. See [LICENSE](../LICENSE).

## Reviewed repository snapshots

| Repository | Commit | Evidence used |
| --- | --- | --- |
| [Newton](https://github.com/newton-physics/newton/tree/0a210603f90e198fa9c8575f8d4a05f88a60d182) | `0a210603f90e198fa9c8575f8d4a05f88a60d182` | README, solver/feature/differentiation tables, general and solver-specific tuning |
| [Ovnewton](https://github.com/NVIDIA-Omniverse/ovnewton/tree/e0803da8c7fd9b365f8d2e477196f06a1677b0f5) | `e0803da8c7fd9b365f8d2e477196f06a1677b0f5` | README, support, pyproject, changelog, `using-ovnewton`, selection skill/references |
| [PhysX/ovphysx](https://github.com/NVIDIA-Omniverse/PhysX/tree/b97365c6ddb32fda8469bc788ec18024862b0368/ovphysx) | `b97365c6ddb32fda8469bc788ec18024862b0368` | README, SKILLS index, basic workflow, Python dependencies, 0.7 changelog/migration, quickstart, stage integration, cloning, I/O/physics limits, tuning guides |
| [Ovstage](https://github.com/NVIDIA-Omniverse/ovstage/tree/fc62999ffe5abdb0330699bd2e13bbb7765f0335) | `fc62999ffe5abdb0330699bd2e13bbb7765f0335` | README, skill directory, Python/C setup, population, application lifecycle |
| [Author's skills](https://github.com/neelkm/skills/tree/b1eed0c26d95a3df25ff566617be482664d864b2) | `b1eed0c26d95a3df25ff566617be482664d864b2` | Ovphysx-selection and references; ovnewton scene-preparation and tuning skills |

Snapshot links are provenance, not recommended dependency pins. The listed Newton main may expose solvers absent from the Newton minimum accepted by ovnewton. Check the chosen runtime's own documentation and tests. Repository source content is not proof that a matching public wheel has shipped or that the user's hardware is supported.

## Catalog format and publication

The layout follows the NVIDIA catalog's flat `skills/<skill-name>/` source convention and the Agent Skills entrypoint/frontmatter format. Relevant catalog guidance:

- [Contribution and source ownership](https://github.com/NVIDIA/skills/blob/main/CONTRIBUTING.md)
- [Release checklist](https://github.com/NVIDIA/skills/blob/main/docs/release-checklist.mdx)
- [Skill-card fields](https://github.com/NVIDIA/skills/blob/main/docs/skill-cards.mdx)
- [Reference evaluation layout](https://github.com/NVIDIA/skills/tree/main/skills/physical-ai-physics-selection/evals)

This local draft includes an authoring skill card and Tier-3-shaped evaluation cases. A generated `BENCHMARK.md`, official scan/evaluation evidence, and `skill.oms.sig` must come from the applicable review/evaluation/signing workflow. They are deliberately not fabricated or copied from the source skills. Catalog publication is separate from local authoring.

The owning product/source repository is a publication decision, not established by this local folder. NVIDIA's contribution guide routes skill changes through that source repository. No source owner, open-source clearance, DCO sign-off, CI result, or NVIDIA endorsement is asserted here.

## Licensing boundaries

This skill's license does not cover all runtime packages, binary distributions, models, or assets. The reviewed ovphysx README distinguishes Apache-2.0 source from prebuilt binaries under NVIDIA Omniverse terms. The reviewed ovstage repository and skills identify their own proprietary terms. Newton documentation also carries its own notices. Linked third-party/product skill bodies are not bundled here. Check the selected artifact's notices for distribution decisions.

## Evidence limits and maintenance

Initial authoring reviewed source files and metadata. Subsequent local tests ran six paired agent builds for CPU box drop, spring identification, and gripper tasks. The 0.2.0 revision packages selected authored trial examples and reusable checks; its direct runtime validation is distinct from the original paired study. See [local evidence](../evals/local-evidence.md) and [recorded results](../evals/local-results.json). No GPU benchmark, real robot validation, official CI evaluation, or measured improvement for the revised skill is claimed.

The starter programs were authored during the local trials using the referenced APIs and installed matching examples; runtime libraries and upstream skill bodies are not bundled. Each starter preserves its tested requirements. These fixture-specific pins do not replace the source snapshots above or establish a universal engine preference.

Run the [evaluation cases](../evals/evals.json) before claiming agent-quality uplift. When updating this skill, recheck capability and platform tables, dependency ranges, schema packaging, async API changes, and every routed skill path. Preserve source dates and runtime distinctions rather than treating main/latest as a release contract.
