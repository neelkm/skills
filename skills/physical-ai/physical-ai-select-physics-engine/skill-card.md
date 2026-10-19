# Skill Card: physical-ai-select-physics-engine

**Status: local authoring draft. This is not a CI-generated evaluation card or a signed NVIDIA release.**

## Description

Select Newton or PhysX through ovphysx from Physical AI workflow requirements, then route the selected stack to repository setup, ovstage integration, scene preparation, validation, and physics tuning guidance.

This draft is intended for local review and evaluation. Production readiness has not been established.

## Owner

Author: Neelakantan Mani <neelakantanm@nvidia.com>. Publication owner and maintaining product team must be established in the source-repository onboarding process; no NVIDIA ownership approval is asserted by this draft.

## License/Terms of Use

[Apache License 2.0](LICENSE) for this skill. Linked runtimes, binary packages, assets, and skills retain their own terms. [Sources and licensing boundaries](references/sources.md) records the distinctions.

## Use Case

Engineers, roboticists, simulation researchers, application developers, and agents choosing a usable physics stack or deciding whether migration is justified. Supports direct Newton, Newton with ovnewton, standalone ovphysx, and existing framework-owned integrations. Narrow implementation fixes in an explicitly selected simulator do not require a new comparison.

## Deployment Geography for Use

Global documentation use, subject to the terms and availability of selected software and assets. This statement does not establish export or deployment clearance.

## Requirements / Dependencies

- Selection: project context and access to primary documentation; no native physics runtime is needed for source-only analysis.
- Optional metadata probe: Python standard library, run with the intended interpreter.
- Saved-output checker: Python standard library and the selected scene's explicit limit profile. Optional starter examples include separate pinned requirements; copy only the selected example into a project before running it.
- Setup/validation: a compatible selected runtime and dependencies; GPU checks additionally need its supported hardware/driver.
- API key or external credential: none required by this skill. Optional credentials for private repositories/assets or package indexes belong to the application and must not appear in logs or output.
- Tool needs: file reads, optional public-document retrieval, and shell/file writes only for requested setup or implementation. The probe reads metadata and writes JSON to stdout; it does not install packages or use the network.

## Known Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| An engine feature is missing in its bridge, device mode, or importer | Evaluate the full candidate path and mark decisive unknowns explicitly |
| An older code example is used with ovphysx 0.7 or incompatible ovstage | Record runtime versions, preserve locks, and follow matching packaged examples and migration guidance |
| Shared-stage integration replays output as input or stale state | Establish ownership, separate application edits/output, and validate completed reads/writes |
| A recommendation overstates accuracy, speed, differentiability, or hardware transfer | Distinguish documentation, runtime checks, task evidence, and measured comparisons |
| Tuning hides a model error or changes required physics | Validate imported semantics first and retain changes only against task criteria |
| Selection is treated as permission to migrate or install | Preserve the user-selected engine and requested implementation scope |

## References

- [Sources and reviewed revisions](references/sources.md)
- [Selection evidence](references/engine-selection.md)
- [Repository and skill handoffs](references/repositories-and-skills.md)
- [Runtime and stage integration](references/runtime-and-ovstage.md)
- [Validation and tuning](references/validation-and-tuning.md)
- [Tested CPU starters and API notes](references/tested-starters.md)
- [Local evaluation evidence](evals/local-evidence.md)

## Skill Output

Output types: recommendation, capability comparison, implementation handoff, and optionally authorized setup/configuration changes. Output format: Markdown with source links; optional JSON metadata from the probe. Recommendations separate engine, solver, device/data mode, and integration, and identify evidence, unknowns, and the next bounded action.

## Skill Version

0.2.0. Source review and local test date: 2026-10-19. No signing identifier exists for this local draft.

## Evaluation Status

The [evaluation dataset](evals/evals.json) provides 32 cases: 28 positive and 4 negative routing/behavior cases in the published NVSkills JSON shape. These author-written cases have not been graded by the official workflow. Structural checks are separate from behavior evidence.

A local 0.1.0 paired study used three Windows CPU prompts with one fresh agent per condition: six builds ran and met their prototype checks. Both conditions selected suitable paths; no clear selection/build-effort advantage was observed. This is not a statistical uplift estimate. Version 0.2.0 adds a shorter path, three optional starters, and a saved-output checker in response. The packaged starters ran locally, including the grasp's zero-friction control; 13 checker regression cases passed, including expected rejections. See [evidence and limits](evals/local-evidence.md). No new paired agent study of 0.2.0 has run.

Official Tier 1 scanning, Tier 2 semantic deduplication, Tier 3 live-agent evaluation, and official uplift benchmarking have not run. No benchmark score, official PASS verdict, production qualification, or signature is claimed. [Evaluation instructions](evals/EVAL.md) describe remaining publication work.

## Ethical Considerations

A simulation recommendation does not certify a robot for physical deployment. Users remain responsible for validating the selected model and controller against their application's real operating conditions before relying on it. Preserve failure evidence and uncertainty rather than implying real-world readiness from a simulated success.
