# Measurement and comparison

## Record comparable runs

Measure the primary task outcome plus relevant physical and runtime limits. Define every metric and its units before comparing results. Preserve the input scene/asset fingerprint, initial conditions, control sequence, simulated duration, seed, device, solver/backend, dependency versions, and measurement method.

Use application-owned timestamps. Ovstage stores latest values, not trajectory history. Output-read metadata may be placeholders. Record snapshots explicitly if a metric needs a history.

For state reads, distinguish body-origin pose from center-of-mass velocity. Native joint angles use radians; shared joint fields use degrees. Model lengths can follow non-metre stage units. Handle prim-to-row mappings and keep borrowed arrays unchanged until their consumers finish. On CUDA, order reads and consumers with the documented streams/events.

## Helper input schema

The following is **synthetic format data**, not a measured result or a recommended physical configuration. Save actual observations in this structure:

```json
{
  "schema_version": 1,
  "context": {
    "scene_id": "sha256:replace-with-composed-asset-fingerprint",
    "workload_id": "gripper-command-sequence-v1",
    "duration_s": 2.0,
    "seed": 17,
    "device": "cpu",
    "solver": "xpbd",
    "versions": {"ovnewton": "0.2.0", "newton": "1.6.0", "ovstage": "0.2.0.377349", "warp-lang": "1.17.0"},
    "measurement": "steady-state-wall-time-with-publication-no-render-v1"
  },
  "settings": {"substeps": 2},
  "metrics": {"tracking_error": 0.03, "penetration": 0.004, "runtime_s": 4.0, "nonfinite_states": 0},
  "units": {"tracking_error": "rad", "penetration": "m", "runtime_s": "s", "nonfinite_states": "count"}
}
```

Both runs must include all context keys shown. Context must match exactly, including additional context fields. Put deliberately varied configuration values in `settings`. If changing the physical scene, solver, or versions, perform a model-port assessment first; this helper intentionally rejects those comparisons.

Metric keys and unit strings must match between files. Metrics must be finite numbers. `nonfinite_states` must be a nonnegative integer and must be zero in the candidate. JSON `NaN`, `Infinity`, and duplicate keys are rejected. The helper does not check whether supplied measurements are truthful.

```console
python scripts/compare_runs.py baseline.json trial.json --metric tracking_error --direction minimize --max penetration=0.005 --max runtime_s=5 --min-relative-improvement 0.05
```

`--max` is an absolute upper bound in the metric's declared unit. The example asks for at least 5% improvement in tracking error, with penetration no greater than 0.005 m and runtime no greater than 5 s, assuming those are the files' units. These are illustrative thresholds; use the task's actual limits. For a maximize objective, change `--direction`.

Improvement is signed according to the objective. Relative improvement divides by the absolute baseline value. When that value is zero, relative improvement is undefined; use `--min-absolute-improvement` instead. A tie is not an improvement.

The helper prints JSON and exits 0 for an accepted comparison, 1 for a valid but rejected candidate, and 2 for invalid or incomparable inputs. Acceptance only means the supplied summary passes these explicit checks. It is not physical validation or a statistical test.

## Experiment quality

Use fixed commands and initial states for diagnosis. For final acceptance, include repeated runs, representative scenarios, and recorded failures as appropriate to the task. Report variation; one favorable seed does not establish robustness. Synchronize CUDA timing and separate warmup from steady-state execution. Include bridge/render work only when the metric definition says so.

## Sources

- [Newton tuning workflow](https://github.com/newton-physics/newton/blob/main/docs/concepts/simulation_tuning.rst)
- [Ovnewton output reads](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/output-reads.md)
- [Ovnewton latest-value transport](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/concepts.md)
