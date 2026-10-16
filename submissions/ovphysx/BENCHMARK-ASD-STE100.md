# ASD-STE100-style version

## ovphysx-selection benchmark — pending validation

Preparation date: 2026-10-16. The skill version is 0.2.0. No live benchmark verdict is available. No uplift result is available. The official pipeline must replace this submission record. This record is not a completed evaluation report.

## Evaluation configuration

The dataset is `evals/evals.json`. It has nine cases. Seven cases are positive. Two cases are negative.

The planned agents are Claude Code and Codex. Their actual model versions are not yet set. Run each agent with the target skill. Also run each agent without the target skill. Use comparable task inputs and environments.

The policy permits one attempt per case. It permits two concurrent cases. File `evals/config.yml` declares this policy.

The cases assess selection and integration guidance. They include one executable metadata probe that uses the Python standard library. They also assess negative routing. The CPU first-run case assesses code. It does not run physics.

Keep the 23 original cases outside the installed skill. Use them for separate regression runs.

No live run has recorded the environment, source revision, or evaluator container revision. No live run has recorded trajectories, token usage, or elapsed time.

## Results

| Dimension | Claude Code baseline | Claude Code with skill | Codex baseline | Codex with skill | Uplift |
| --- | --- | --- | --- | --- | --- |
| Security | Not run | Not run | Not run | Not run | Unavailable |
| Correctness | Not run | Not run | Not run | Not run | Unavailable |
| Discoverability | Not run | Not run | Not run | Not run | Unavailable |
| Effectiveness | Not run | Not run | Not run | Not run | Unavailable |
| Efficiency | Not run | Not run | Not run | Not run | Unavailable |

Task pass counts are unmeasured. Token counts are unmeasured. Total elapsed time is unmeasured. Compliance with the one-hour CI limit is unmeasured. Pending cells do not mean zero. They do not mean a passing result.

Use execution traces to assess routing. Do not apply target-skill routing requirements to a baseline that does not contain the skill.

## Evidence and limits

The submission packet records local format, dataset, and helper checks separately. These checks do not establish agent behavior. They do not provide a complete security verdict. They do not establish CPU or GPU simulation correctness. They do not establish task fidelity, performance superiority, or sim-to-real transfer. No NVIDIA signature exists for this submission.

The technical reference snapshot is ovphysx 0.6.4. The PhysX commit is `6dc53585d7db07346f53d0598a5fd3bfdce47d8d`. Keep the skill version, runtime version, source revision, and evaluator version distinct.

## Completion procedure

Run the approved NVIDIA pipeline on the owning product-repository PR. Use paired conditions on both agents. Retain the actual artifacts. Report the five dimensions and their underlying signals. Identify metrics that cannot be compared. Do not invent uplift.

Let the pipeline generate this report and the skill card again. Then sign the reviewed source. If content changes later, validate it again. Sign it again as required by the release process.

See [EVAL.md](../../skills/ovphysx/ovphysx-selection/evals/EVAL.md), [NVIDIA evaluation dataset documentation](https://docs.nvidia.com/skills/skillevaluator/eval-datasets), [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator), and the [published ovnewton benchmark](https://github.com/NVIDIA/skills/blob/main/skills/ovnewton-usage/BENCHMARK.md).

This is an ASD-STE100-style rewrite. It has not been checked for full compliance with the standard's writing rules and dictionary.
