# ovphysx-selection benchmark — pending validation

Prepared: 2026-10-16. Skill version: 0.2.0. **No live benchmark verdict or uplift is available.** This is a submission record for replacement by the official pipeline, not a completed evaluation report.

## Evaluation configuration

- Dataset: `evals/evals.json`, nine cases (seven positive, two negative).
- Planned agents: Claude Code and Codex; actual model versions remain unset.
- Conditions: with the target skill and without it, using comparable task inputs and environments.
- Policy: one attempt per case and two concurrent cases, as declared in `evals/config.yml`.
- Scope: selection and integration guidance, one executable standard-library metadata probe, and negative routing. The CPU first-run case grades code without running physics.
- Extended coverage: 23 original cases retained outside the installed skill for separate regression runs.
- Environment, source revision, evaluator container revision, trajectories, token usage, and elapsed time: not yet recorded for a live run.

## Results

| Dimension | Claude Code baseline | Claude Code with skill | Codex baseline | Codex with skill | Uplift |
| --- | --- | --- | --- | --- | --- |
| Security | Not run | Not run | Not run | Not run | Unavailable |
| Correctness | Not run | Not run | Not run | Not run | Unavailable |
| Discoverability | Not run | Not run | Not run | Not run | Unavailable |
| Effectiveness | Not run | Not run | Not run | Not run | Unavailable |
| Efficiency | Not run | Not run | Not run | Not run | Unavailable |

Task pass counts, token counts, total elapsed time, and compliance with the one-hour CI limit are unmeasured. Do not interpret pending cells as zeros or passing results. Assess routing from execution traces; do not apply target-skill routing requirements to a baseline that lacks the skill.

## Evidence and limits

Local format, dataset, and helper checks are recorded separately in the submission packet. They do not establish agent behavior, a complete security verdict, CPU/GPU simulation correctness, task fidelity, performance superiority, or sim-to-real transfer. No NVIDIA signature has been generated.

The technical reference snapshot is ovphysx 0.6.4 at PhysX commit `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`. Keep skill version, runtime version, source revision, and evaluator version distinct.

## Completion procedure

Run the approved NVIDIA pipeline on the owning product-repository PR. Use the paired conditions on both agents, retain actual artifacts, report the five dimensions and their underlying signals, and document incomparable metrics without fabricating uplift. Let the pipeline regenerate this report and the skill card, then sign the reviewed source. Any later content change requires revalidation and signing according to the release process.

See [EVAL.md](evals/EVAL.md), [NVIDIA evaluation dataset documentation](https://docs.nvidia.com/skills/skillevaluator/eval-datasets), [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator), and the [published ovnewton benchmark](https://github.com/NVIDIA/skills/blob/main/skills/ovnewton-usage/BENCHMARK.md).
