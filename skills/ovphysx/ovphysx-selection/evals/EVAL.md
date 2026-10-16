# Evaluating ovphysx-selection

The initial CI dataset has nine cases: seven positive cases and two negative routing cases. It covers selection, an executable metadata check, a CPU lifecycle recipe, stage ownership, batching/reset, mixed units, and a required-gradient rejection. It contains explicit, implicit, contextual, and negative prompts. Cases request guidance or small code artifacts; only the standard-library metadata probe needs execution. No GPU, asset download, training job, or physics installation is required for this initial set.

## Questions

Use the prompts in `evals.json` unchanged for the paired runs. The engine-selection cases must permit a justified alternative. The selection preference is not the grading objective.

## Behaviors

- Positive cases read `ovphysx-selection/SKILL.md` and only the references needed for the task.
- Compare complete engine/device/integration paths against requirements.
- Preserve application-owned stages, package constraints, and explicit non-migration requests.
- Keep input and output ordinal ownership separate.
- Respect clone-before-step and DirectGPU initialization rules.
- Interpret units, identity, device, and lifetime per attribute.
- Distinguish documentation, metadata, and executed simulation evidence.
- Execute the metadata probe for its explicit probe case. Verify its JSON and exit status.

## Negative Cases

- A reset helper for a fixed MuJoCo application with no simulator-selection request.
- USD camera/light authoring without physics.

Check non-activation in skill-load traces. The agent's claim that it did not load a skill is not evidence.

## Notes

Run each case with and without the target skill on both Claude Code and Codex. Use identical operator-owned environments, public documentation access, and task inputs. Do not supply the skill's private guidance or helper to the baseline as fixture data. For the explicit probe case, the baseline can produce its own equivalent metadata inspection; score output semantics separately from target-skill execution. Expected skill/script routing applies to the with-skill condition, not to the baseline. Inspect the evaluator's baseline handling before comparing routing scores.

The public example's one-attempt, two-concurrent policy is used in `config.yml`. Record actual harness/model versions and total elapsed time. Keep the signing run within the documented one-hour limit; that duration has not yet been measured for this dataset. Do not reduce coverage based on an invented timing estimate.

The CPU recipe case grades the returned code and release contract. It does not qualify runtime physics. In a separate supported environment, install the pinned runtime, execute the returned program, verify motion/contact, and record package/hardware details. Native C/C++ builds, GPU batches, contact fidelity, deformables, rendering, physical calibration, and larger performance studies belong to extended/release validation.

The submission packet retains all 23 original behavioral cases outside the CI skill directory, along with a converted extended dataset. Keep extended data out of automatic CI discovery until its runtime is qualified. This prevents the broad suite from being mistaken for a completed or hour-bounded benchmark.

Capture trajectories, final artifacts, security/correctness/discoverability/effectiveness/efficiency scores, task completion, tokens, and wall time for both conditions. Generate `BENCHMARK.md` from real results. The current benchmark and skill card are explicitly pending drafts; NVIDIA's validation pipeline must replace them and generate `skill.oms.sig`. Never copy another skill's score or signature.

See [evaluation datasets](https://docs.nvidia.com/skills/skillevaluator/eval-datasets), [live evaluation](https://docs.nvidia.com/skills/skillevaluator/tier3-live-evaluation), and the [published ovnewton evaluation guidance](https://github.com/NVIDIA/skills/blob/main/skills/ovnewton-usage/evals/EVAL.md).
