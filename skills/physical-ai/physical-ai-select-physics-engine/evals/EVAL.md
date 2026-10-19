# Evaluating physical-ai-select-physics-engine

`evals.json` follows the catalog reference shape: `skill_name` and an `evals` array with unique `id`, `prompt`, `expected_skill`, `expected_output`, and `assertions` fields. Negative cases use `expected_skill: null`.

Run paired with-skill and without-skill evaluations under the same tools, source snapshots, runtime access, and budgets. Grade observable decisions and skill-load traces rather than exact phrasing. The expected answer may be conditional when an artifact or runtime is unavailable. Do not install a simulator for selection-only cases. For cases requesting a plan without a runtime, accurately labeled unrun checks are expected.

The cases cover balanced selection, direct versus bridge integration, hard requirements, version/device limits, stage ownership, repository routing, tuning, unsupported claims, and preservation of an existing engine. They are author-written evaluation inputs, not evidence that the skill has passed.

The dataset now contains 32 cases, including six additions from the local paired trials: small-task routing, executable handoffs, missing contact evidence, preserving a chosen engine despite starter availability, controlled comparisons, and limits on uplift claims. The original paired study and subsequent starter validation are recorded in [local evidence](local-evidence.md) and [machine-readable results](local-results.json). Keep this local evidence separate from official CI results.

## Local checks

Validate frontmatter, folder/name agreement, relative references, JSON structure, unique case IDs, positive/negative routing targets, and Python helper syntax. Execute the metadata probe using an available interpreter; verify that missing packages remain null and that no native simulation library is imported. These checks do not establish physics fidelity, useful gradients, runtime compatibility, or agent-quality uplift.

For the optional starters, copy each selected folder to a separate working directory, use its pinned environment, and follow [the run and check commands](../references/tested-starters.md). Verify process completion as well as numerical output. Run the grasp with and without friction. The unextended grasp must fail `--require-contact-evidence` while reporting its measured lift/release behavior accurately.

Exercise the checker with altered copies of outputs: a stale stage pose, wrong gradient sign, non-finite samples, duplicate timestamps, missing required contact fields, a no-lift trajectory, and a control with another parameter changed must fail. Synthetic checker fixtures are unit checks, not physics evidence. Keep logs/caches/generated outputs outside the skill and the published archive. Re-run paired agents separately before claiming the revised skill improves build effort.

## NVIDIA publication workflow

Follow the owning source repository's current contribution and NVSkills CI process, the [catalog contribution guide](https://github.com/NVIDIA/skills/blob/main/CONTRIBUTING.md), and the [release checklist](https://github.com/NVIDIA/skills/blob/main/docs/release-checklist.mdx).

1. Confirm source ownership, license/open-source clearance, and the repository registration route. Review overlap with the existing selection skills rather than silently replacing them.
2. Run the official evaluation workflow, including Tier 1 scanning, Tier 2 semantic deduplication, and Tier 3 live-agent evaluation. Resolve release-blocking findings.
3. Retain actual benchmark evidence and generate `BENCHMARK.md` through that workflow. Update or regenerate the authoring skill card from the reviewed results. Do not reuse scores from either source skill.
4. Obtain the legitimate detached `skill.oms.sig` for the exact reviewed directory and verify against the approved trust chain. Do not create a placeholder signature or copy one from another skill.
5. Submit through the source-owner/catalog process. Local structural validation alone is not catalog acceptance.

The current `skill-card.md` is explicitly an authoring draft. The final generated evaluation card, benchmark, official reports, and signature are outside this local-only authoring task.
