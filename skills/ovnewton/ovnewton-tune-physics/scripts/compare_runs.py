#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare measured run summaries under explicit objective and upper bounds.

No simulation is executed. Exit 0 means the supplied candidate passes, 1 means
it is valid but rejected, and 2 means the inputs are invalid or incomparable.
"""

import argparse
import json
import math
from pathlib import Path
import sys


CONTEXT_KEYS = {"scene_id", "workload_id", "duration_s", "seed", "device", "solver", "versions", "measurement"}
VERSION_KEYS = {"ovnewton", "newton", "ovstage", "warp-lang"}


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"non-standard JSON number: {value}")


def load_run(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        return json.load(stream, object_pairs_hook=unique_object, parse_constant=invalid_constant)


def validate_run(run):
    if not isinstance(run, dict) or type(run.get("schema_version")) is not int or run["schema_version"] != 1:
        raise ValueError("expected schema_version 1")
    context = run.get("context")
    if not isinstance(context, dict) or not CONTEXT_KEYS <= context.keys():
        raise ValueError("missing required run context")
    for key in CONTEXT_KEYS - {"duration_s", "seed", "versions"}:
        if not isinstance(context[key], str) or not context[key].strip():
            raise ValueError(f"context.{key} must be a nonempty string")
    if not finite_number(context["duration_s"]) or context["duration_s"] <= 0:
        raise ValueError("duration_s must be finite and positive")
    if type(context["seed"]) is not int:
        raise ValueError("seed must be an integer")
    versions = context["versions"]
    if not isinstance(versions, dict) or not VERSION_KEYS <= versions.keys() or any(
            not isinstance(v, str) or not v.strip() for v in versions.values()):
        raise ValueError("versions must identify ovnewton, newton, ovstage, and warp-lang")
    if not isinstance(run.get("settings"), dict):
        raise ValueError("settings must be an object")
    metrics, units = run.get("metrics"), run.get("units")
    if not isinstance(metrics, dict) or not metrics or not isinstance(units, dict) or metrics.keys() != units.keys():
        raise ValueError("metrics and units must have identical nonempty keys")
    for name, value in metrics.items():
        if not finite_number(value):
            raise ValueError(f"metric {name} must be a finite number")
        if not isinstance(units[name], str) or not units[name].strip():
            raise ValueError(f"metric {name} needs a unit")
    count = metrics.get("nonfinite_states")
    if type(count) is not int or count < 0 or units.get("nonfinite_states") != "count":
        raise ValueError("nonfinite_states must be a nonnegative integer with unit count")


def compare(baseline, trial, metric, direction, limits=None, min_relative=0.0, min_absolute=0.0):
    validate_run(baseline)
    validate_run(trial)
    if baseline["context"] != trial["context"]:
        raise ValueError("context differs; perform a separate model-port or workload comparison")
    if baseline["units"] != trial["units"]:
        raise ValueError("metric sets or units differ")
    if metric not in baseline["metrics"] or direction not in ("minimize", "maximize"):
        raise ValueError("unknown objective metric or direction")
    for threshold in (min_relative, min_absolute):
        if not finite_number(threshold) or threshold < 0:
            raise ValueError("improvement thresholds must be finite and nonnegative")
    bounds = dict(limits or {})
    for name, bound in bounds.items():
        if name not in trial["metrics"] or not finite_number(bound):
            raise ValueError(f"unknown or invalid upper bound: {name}")
    # Validate explicit bounds before applying the mandatory numerical limit.
    # Preserve a stricter user limit, but never allow numerical failures.
    bounds["nonfinite_states"] = min(bounds.get("nonfinite_states", 0), 0)
    before, after = baseline["metrics"][metric], trial["metrics"][metric]
    delta = before - after if direction == "minimize" else after - before
    relative = delta / abs(before) if before != 0 else None
    if not math.isfinite(delta) or (relative is not None and not math.isfinite(relative)):
        raise ValueError("objective difference overflowed; rescale the metric")
    reasons = []
    if delta <= 0 or delta < min_absolute:
        reasons.append("objective did not meet the required positive absolute improvement")
    if min_relative > 0 and (relative is None or relative < min_relative):
        reasons.append("relative improvement is undefined or below the required threshold")
    checks = {}
    for name, bound in bounds.items():
        value = trial["metrics"][name]
        checks[name] = {"value": value, "maximum": bound, "unit": trial["units"][name], "passed": value <= bound}
        if value > bound:
            reasons.append(f"{name} exceeds its upper bound")
    return {"status": "rejected" if reasons else "accepted", "metric": metric, "direction": direction,
            "unit": trial["units"][metric], "baseline": before, "trial": after,
            "absolute_improvement": delta, "relative_improvement": relative,
            "upper_bounds": checks, "reasons": reasons,
            "note": "Checks supplied summaries only; no simulation or statistical validation was performed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("trial", type=Path)
    parser.add_argument("--metric", required=True)
    parser.add_argument("--direction", required=True, choices=("minimize", "maximize"))
    parser.add_argument("--max", action="append", default=[], dest="bounds", metavar="METRIC=VALUE")
    parser.add_argument("--min-relative-improvement", type=float, default=0.0)
    parser.add_argument("--min-absolute-improvement", type=float, default=0.0)
    args = parser.parse_args()
    try:
        limits = {}
        for item in args.bounds:
            name, value = item.split("=", 1)
            if not name or name in limits:
                raise ValueError("upper bounds need unique metric names")
            limits[name] = float(value)
        result = compare(load_run(args.baseline), load_run(args.trial), args.metric, args.direction,
                         limits, args.min_relative_improvement, args.min_absolute_improvement)
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["status"] == "accepted" else 1


if __name__ == "__main__":
    sys.exit(main())
