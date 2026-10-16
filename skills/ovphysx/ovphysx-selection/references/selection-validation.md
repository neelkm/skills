# Validate an ovphysx selection

Use a small experiment that can change the recommendation. A selection request does not require installing every alternative. Preserve the user's physical requirements and execution budget.

## Keep an evidence record

Record assets and versions, initial conditions, units, controls, required contacts/joints/materials, engine and integration versions, solver configuration, timestep/substeps, hardware, actual devices, environment count, observation/sensor work, and acceptance criteria. Separate documented behavior, vendor claims, measurements, and unresolved assumptions.

Treat these as different evidence levels:

1. Package metadata was inspected.
2. Native initialization, population, and attach succeeded.
3. Synchronized steps completed and expected state was read.
4. Representative motion, control, contact, and reset behavior met criteria.
5. Workload performance and, when required, physical-world correspondence were measured.

Do not report a higher level from a lower-level check. Empty or omitted read groups do not qualify an observation path.

## Choose the representative check

| Workflow | Test | Evidence to retain |
| --- | --- | --- |
| First run | Drop a known body and observe it through ground contact | Identity, finite positions, gravity direction, contact/settling tolerance, completed steps |
| Robot control | Command a known joint change under its drive/effort limits | Measured state rather than targets, units, tracking error, limits, control timing |
| RL batch | Clone a small batch, disturb one environment, reset a subset, then scale | Isolation, correct identities, unchanged neighbors, post-reset state, memory and total loop cost |
| Grasp or insertion | Repeat the representative contact sequence | Success definition, slip, penetration, contact force, actuator effort, trial variation |
| Deformable manipulation | Exercise required material, attachment, contact, and reset | Mesh/material settings, observable deformation, stability, sensitivity to resolution/timestep |
| Shared-stage application | Apply a control edit, step, publish motion, and consume it | Correct ordinal ownership, no output feedback, consumer motion and timing |
| Migration | Replay equivalent initial conditions and controls before/after | Lost or changed features, asset conversion, units, physical behavior, adoption cost |
| Required gradients | Check the actual loss and parameter through the selected alternative path | Supported derivative, finite values, comparison with an analytic/numerical reference, relevant contact regimes |

For mixed joints, include a rotational and a prismatic joint. For data interop, exercise the actual device and consumer stream. For reset, check the next transition, not just the write's return code. A no-contact example does not qualify a manipulation task.

## Compare fairly

Use equivalent geometry, masses, initial conditions, controls, simulated duration, and acceptance limits. Parameter names and numerical values are not necessarily interchangeable across engines. Tune each to the same physical objective and disclose remaining model differences. Changing the task to increase speed is not a valid win.

Separate scene loading, collision cooking, compilation/warmup, and steady-state time. Synchronize GPU work before stopping timers. Distinguish single-rollout latency from batched simulated experience per wall-clock second. State whether controls, resets, policy inference, rendering, sensors, and stage publication are included. Use repeated trials and variation when ranking close results. Compare contact accuracy and stability alongside speed; do not infer sim-to-real transfer without relevant physical tests.

If documentation conflicts, prefer the installed artifact's contract and matching source, then design the smallest check that resolves the uncertainty. Log diagnostics and inspect the realized scene. Do not silently relabel an unsupported feature as an optional improvement.

## Deliver a usable decision

State the selected engine, solver configuration, integration, and devices separately. Explain the requirements met, conditions, unresolved features, closest alternative, migration/setup cost, versions, tests actually run, results, and next bounded action. A provisional recommendation can remain useful when execution is unavailable; label its verification steps not run.

For an implementation request, provide the runnable entry point, required packages/assets, control and observation contract, reset behavior, and verification result. Do not end with an engine name when the user asked for a working loop.

## Evaluate this skill

[Evaluation cases](../evals/evals.json) contain the initial CI smoke prompts and acceptance criteria. They are case definitions, not execution results. Read [evaluation guidance](../evals/EVAL.md) for paired trials and the extended regression set. For discovery evaluation, use generic prompts without naming the skill; for behavior evaluation, provide this skill and permitted artifacts in the target agent host. Assess requirements coverage, integration choice, factual accuracy, execution quality, and honesty about measurements. A justified alternative is a successful selection. The fraction of ovphysx recommendations is not a quality metric.
