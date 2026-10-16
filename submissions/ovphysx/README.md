# ovphysx NVIDIA submission materials

The current skill is [ovphysx-selection 0.2.0](../../skills/ovphysx/ovphysx-selection/SKILL.md). It replaces `physical-ai-ovphysx-selection` 0.1.0. This directory holds the supporting submission files without creating another installable copy. Publishing this repository does not register or approve the skill in NVIDIA's catalog.

## Submission files

| File | Purpose |
| --- | --- |
| [SOURCE-PR.md](SOURCE-PR.md) | Proposed product-repository PR title and body |
| [CATALOG-PR.md](CATALOG-PR.md) | Proposed NVIDIA/skills catalog PR and pending affirmations |
| [catalog-component.yml](catalog-component.yml) | Copy to NVIDIA/skills as `components.d/ovphysx.yml` after the approved source path exists |
| [request-nvskills-ci.yml](request-nvskills-ci.yml) | Approved workflow template for the owning product repository; inactive in this directory |
| [extended-evals.json](extended-evals.json) | All 23 original cases converted to NVIDIA's dataset format |
| [extended-source-cases.json](extended-source-cases.json) | Original 23-case dataset preserved for comparison |
| [BENCHMARK-ASD-STE100.md](BENCHMARK-ASD-STE100.md) | Complete ASD-STE100-style alternative to the pending benchmark |
| [SKILL-CARD-ASD-STE100.md](SKILL-CARD-ASD-STE100.md) | Complete ASD-STE100-style alternative to the draft skill card |
| [validation-preparation.json](validation-preparation.json) | Actual preparation-time evaluator output; local path prefixes replaced for publication |

## Readiness record — 2026-10-16

The prepared skill has a 113-line entrypoint, four references, a standard-library metadata probe, a complete Apache-2.0 license, nine initial CI cases, evaluation configuration/guidance, and pending benchmark/card drafts. Its nine CI cases comprise seven positive and two negative cases. The 23 extended cases remain outside the installed skill. The runtime documentation baseline remains ovphysx 0.6.4 at PhysX commit `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`.

During preparation, the skill-creator validator, official dataset/configuration loaders, package checks, and 16 relative-link checks passed. The metadata probe ran, and all three probe tests passed. These checks did not execute a physics runtime. The source skill files in this repository match that prepared package; their repository parent path has changed.

The public NVIDIA evaluator was pinned to `NVIDIA/SkillEvaluator@a53af93d0059409679179a0d6bd2f594a351a32e`, package version 0.5.0. The command used `--external --tiers 1 --no-llm`; its final report time was 2026-10-16 15:17:45 UTC. Eight of 11 validator results passed. Three scanner results were incomplete because SkillSpector, Bandit, Semgrep, and Gitleaks were unavailable. The overall result was **incomplete**, with exit code 1. The static quality heuristic was 89.5/100, grade B; this is not measured agent effectiveness or uplift. Seven non-blocking findings remain: three medium and four low. The published JSON preserves the results and replaces local path prefixes only.

No paired Claude Code/Codex evaluation, CPU/GPU simulation, performance benchmark, complete NVIDIA security run, or signature was completed for this version. The one-hour CI limit has not been measured. See [repository validation notes](../../docs/VALIDATION.md) for the checks after replacement.

## Submission sequence

1. Have the ovphysx owning team confirm `NVIDIA-Omniverse/PhysX` as the destination, the maintainer, proposed copyright attribution, and required release/IP approvals. The proposed product path is `skills/ovphysx-selection/`; this personal repository retains the `skills/ovphysx/` grouping.
2. Confirm Apache-2.0 placement within the product repository, whose root license is BSD-3-Clause. Do not replace that root license. Resolve the catalog template's “no new license” affirmation. The existing PhysX contribution guide includes the full DCO; the contributor must certify and sign off actual submission commits.
3. Copy the complete current skill into the product path. Reconcile the workflow template with any existing workflow and the current approved version. Complete the approved App, dispatch-secret, maintainer, and signing setup. No secret value or repository access change is supplied here.
4. Open the source PR. An authorized maintainer requests `/nvskills-ci`. Complete required security checks and paired runs with and without the skill on Claude Code and Codex. Record actual models, revisions, results, tokens, elapsed time, and comparable uplift. Let the pipeline regenerate the benchmark/card and create `skill.oms.sig`. Revalidate and sign after later content changes.
5. After approved source content exists on the registered branch, submit the separate catalog PR. Its source path must contain one `SKILL.md`. Recheck `catalog_dir` uniqueness. Do not edit the generated catalog mirror directly or check unconfirmed affirmations.

Public templates: [ovnewton-usage](https://github.com/NVIDIA/skills/tree/main/skills/ovnewton-usage), [registry contract](https://github.com/NVIDIA/skills/blob/main/components.d/README.md), [catalog PR template](https://github.com/NVIDIA/skills/blob/main/.github/PULL_REQUEST_TEMPLATE.md), [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator/tree/a53af93d0059409679179a0d6bd2f594a351a32e), and [PhysX contribution guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/CONTRIBUTING.md). No internal publishing guide is included.

---

# ASD-STE100-style version

## ovphysx NVIDIA submission materials

The current skill is [ovphysx-selection 0.2.0](../../skills/ovphysx/ovphysx-selection/SKILL.md). It replaces `physical-ai-ovphysx-selection` 0.1.0. This directory contains supporting submission files. It does not create another installable copy. Publication of this repository does not register the skill in NVIDIA's catalog. It does not approve the skill.

## Submission files

| File | Purpose |
| --- | --- |
| [SOURCE-PR.md](SOURCE-PR.md) | Proposed product-repository PR title and body |
| [CATALOG-PR.md](CATALOG-PR.md) | Proposed NVIDIA/skills catalog PR and pending affirmations |
| [catalog-component.yml](catalog-component.yml) | Copy to NVIDIA/skills as `components.d/ovphysx.yml` after the approved source path exists |
| [request-nvskills-ci.yml](request-nvskills-ci.yml) | Approved workflow template for the owning product repository; inactive in this directory |
| [extended-evals.json](extended-evals.json) | All 23 original cases converted to NVIDIA's dataset format |
| [extended-source-cases.json](extended-source-cases.json) | Original 23-case dataset for comparison |
| [BENCHMARK-ASD-STE100.md](BENCHMARK-ASD-STE100.md) | Complete ASD-STE100-style alternative to the pending benchmark |
| [SKILL-CARD-ASD-STE100.md](SKILL-CARD-ASD-STE100.md) | Complete ASD-STE100-style alternative to the draft skill card |
| [validation-preparation.json](validation-preparation.json) | Actual evaluator output from preparation; local path prefixes replaced for publication |

## Readiness record — 2026-10-16

The prepared skill has a 113-line entrypoint. It has four references and a metadata probe that uses the Python standard library. It has the full Apache-2.0 license. It has nine initial CI cases, evaluation configuration, and evaluation guidance. Its benchmark and card are pending drafts.

Seven CI cases are positive. Two are negative. The 23 extended cases remain outside the installed skill. The runtime documentation baseline remains ovphysx 0.6.4. The PhysX commit is `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`.

During preparation, the skill-creator validator passed. The official dataset and configuration loaders passed. Package checks passed. All 16 relative-link checks passed. The metadata probe ran. All three probe tests passed. These checks did not run a physics runtime. The source skill files in this repository match the prepared package. Their repository parent path changed.

The public NVIDIA evaluator used commit `a53af93d0059409679179a0d6bd2f594a351a32e` from `NVIDIA/SkillEvaluator`. Its package version was 0.5.0. The command used `--external --tiers 1 --no-llm`. The final report time was 2026-10-16 15:17:45 UTC.

Eight of 11 validator results passed. Three scanner results were incomplete. SkillSpector, Bandit, Semgrep, and Gitleaks were unavailable. The overall result was **incomplete**. The exit code was 1. The static quality heuristic was 89.5/100, grade B. This score is not measured agent effectiveness or uplift. Seven non-blocking findings remain. Three are medium. Four are low. The published JSON preserves the results. Only local path prefixes were replaced.

No paired Claude Code/Codex evaluation was completed for this version. No CPU or GPU simulation was completed. No performance benchmark was completed. No complete NVIDIA security run or signature was completed. The one-hour CI limit has not been measured. See [repository validation notes](../../docs/VALIDATION.md) for checks after replacement.

## Submission sequence

1. The ovphysx owning team must confirm `NVIDIA-Omniverse/PhysX` as the destination. It must confirm the maintainer and proposed copyright attribution. It must complete required release/IP approvals. The proposed product path is `skills/ovphysx-selection/`. This personal repository retains the `skills/ovphysx/` grouping.
2. Confirm Apache-2.0 placement in the product repository. Its root license is BSD-3-Clause. Do not replace that root license. Resolve the catalog template's “no new license” affirmation. The existing PhysX contribution guide includes the full DCO. The contributor must certify and sign off actual submission commits.
3. Copy the complete current skill to the product path. Reconcile the workflow template with any existing workflow and the current approved version. Complete approved App, dispatch-secret, maintainer, and signing setup. This directory supplies no secret value or repository access change.
4. Open the source PR. An authorized maintainer requests `/nvskills-ci`. Complete required security checks. Run Claude Code and Codex with and without the skill. Record actual models, revisions, results, tokens, elapsed time, and comparable uplift. Let the pipeline generate the benchmark and card again. Let it create `skill.oms.sig`. Validate and sign again after later content changes.
5. Wait until approved source content exists on the registered branch. Then submit the separate catalog PR. Its source path must contain one `SKILL.md`. Check `catalog_dir` uniqueness again. Do not directly edit the generated catalog mirror. Do not check unconfirmed affirmations.

Public templates: [ovnewton-usage](https://github.com/NVIDIA/skills/tree/main/skills/ovnewton-usage), [registry contract](https://github.com/NVIDIA/skills/blob/main/components.d/README.md), [catalog PR template](https://github.com/NVIDIA/skills/blob/main/.github/PULL_REQUEST_TEMPLATE.md), [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator/tree/a53af93d0059409679179a0d6bd2f594a351a32e), and [PhysX contribution guide](https://github.com/NVIDIA-Omniverse/PhysX/blob/main/CONTRIBUTING.md). No internal publishing guide is included.

This is an ASD-STE100-style rewrite. It has not been checked for full compliance with the standard's writing rules and dictionary.
