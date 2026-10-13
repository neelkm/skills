---
name: ovnewton-tune-physics
description: Diagnose and tune an existing ovnewton simulation for grasp slip, penetration, jitter, joint tracking, instability, or excessive runtime. Use bounded experiments with measured task metrics and solver-specific controls. Separate imported-model and stage-synchronization faults from Newton solver behavior; pure Newton work can use the linked Newton guidance directly.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: physical-ai
---

# Diagnose and tune ovnewton physics

Improve a reproducible physical task while preserving its required behavior. Work from measurements and a specific failure, not a universal parameter preset.

**For human readers:** ovnewton transfers model and state data. Newton performs the solve. An import error, stale stage value, or incorrect controller can look like a weak solver. More stiffness or more iterations does not reliably fix those problems.

## Establish a baseline

Identify the installed product versions, active solver/backend, scene, initial state, command sequence, timestep/substeps, control frequency, collision frequency, and stage publication/render rates. Confirm the required behavior and acceptable limits. Use the smallest scene that reproduces the failure.

Choose a primary metric appropriate to the task, such as grasp slip, tracking error, or completed task rate. Set bounds for numerical failures, penetration or constraint error, and runtime where measurable. State units and sample definitions. Do not invent a pass threshold from an attractive-looking frame.

Save the original configuration and reproduce the problem before changing it. Read [measurement and comparison](references/measurement.md) when recording experiments. For backend choices and parameter interpretation, read [solver notes](references/solver-notes.md).

## Diagnose before tuning

Classify the observed failure and resolve the earliest supported cause:

| Evidence | Inspect first |
| --- | --- |
| Wrong scale, unexpected acceleration, unstable initial frame | Stage units, gravity, body/joint initial state, initial penetration, imported mass/inertia |
| Missing motion or poor target tracking | Applied drive schemas, joint mapping, units, control mode, target continuity, and solver feature support |
| Motion correct in Newton but stale in the stage | Current state after swapping, publication ordering, sealed write floor, and consumer synchronization |
| Slip or excessive penetration | Collider geometry, friction, contact locations/capacity, effort limits, then contact model and convergence |
| Jitter or explosive motion | Overlapping shapes, mass/inertia ratios, conflicting constraints, stiff drives, timestep, and damping |
| Low displayed frame rate | Separate solve/collision time, bridge publication, rendering, and one-time compilation |

Inspect final imported values and ovnewton diagnostic codes/prim paths. In particular, verify applied mass/drive APIs and effective material bindings. Stage length units and angular conversions must match control and metric units. Do not tune away a failed import assumption.

`update_from_ovstage(state, control)` applies the latest sealed supported state and drive fields together. It is not a targets-only read. Do not call it blindly every substep against stale authored state: reason about which component owns each update and when the stage is refreshed. Use the same control object for stepping.

## Run bounded experiments

For contact-dominated problems, validate the model and contact representation first. Reduce timestep or increase substeps when temporal resolution is insufficient. Test convergence settings supported by the selected solver. Then refine contacts and drives as indicated by the failure. For controller-dominated failures, correct the controller/drive issue before contact tuning.

Change one factor at a time when identifying causes. If evidence points to an interaction, test the smallest justified combination. Limit the sweep size and simulated duration to the task budget. Keep trial outputs separate from the baseline.

Check each parameter against the installed public solver constructor/configuration and feature table. Do not copy keywords from a different solver. A stored Newton property may be ignored by a backend. After model edits, use the backend's supported notification/rebuild procedure if it caches model data.

For an application using Newton's collision pipeline, refreshing contacts every substep is a useful debugging baseline. Measure before reducing refresh frequency. Treat a solver change as a model port: recheck supported drives, constraints, contact semantics, units, and capacity before comparing outcomes.

Avoid silent model changes. Altering friction, inertia, actuator effort, or collision geometry changes physics, even if the simulation becomes smoother. Explain the evidence and expected effect. Keep changes only when the primary metric improves and all required bounds remain satisfied.

## Separate fidelity from runtime cost

Exclude initialization, kernel compilation, and warmup from steady-state measurements. Synchronize the measured CUDA work; timing host enqueue calls alone understates GPU work. Record whether rendering and publication are included.

Measure physics-only, physics-plus-publication, and rendered application runs where useful. Reuse the same workload and metric definitions. Do not describe a rendering-only improvement as a faster physics solve. Stage ordinals and output-read placeholder metadata are not reliable simulation timestamps; record application-owned step/time identifiers.

The optional [comparison helper](scripts/compare_runs.py) checks two measured JSON summaries:

```console
python scripts/compare_runs.py baseline.json trial.json --metric tracking_error --direction minimize --max penetration=0.005 --max runtime_s=5
```

The helper path is relative to this skill directory. Input paths are the user's result files. Read the measurement reference for the schema. The helper requires matching context and units, finite metrics, zero non-finite states, improvement in the selected objective, and satisfaction of the supplied upper bounds. It does not run simulations, generate metrics, establish statistical significance, or discover omitted acceptance criteria.

## Return a reproducible result

Report the diagnosed cause, original and proposed settings, exact trial conditions, measured differences, physical tradeoffs, and remaining limits. Include failed trials when they explain the retained choice. If no candidate meets the criteria, preserve the baseline and identify the unresolved cause. Do not claim improvement from unrun experiments or synthetic example data.

## Public references

- [Newton diagnosis and tuning](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning.rst)
- [Solver-specific parameters](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning_solvers.rst)
- [Solver and joint feature support](https://github.com/newton-physics/newton/blob/main/docs/solvers/index.rst)
- [Ovnewton synchronization](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/concepts.md)
- [Output layouts, units, and lifetimes](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/output-reads.md)

Newton-main guidance can be newer than the installed runtime. Use its diagnostic reasoning, but verify exact settings against the installed public API.
