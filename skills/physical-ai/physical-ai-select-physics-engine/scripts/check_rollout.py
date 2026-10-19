# SPDX-License-Identifier: Apache-2.0
"""Check saved starter outputs with explicit task limits; no physics imports.

Exit 0: requested checks passed. Exit 2: failed check or invalid evidence.
This verifies recorded behavior, not simulator execution, calibration, or fidelity.
See references/tested-starters.md for the CSV/JSON producers and commands.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def read_json(path):
    def invalid(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    return json.loads(path.read_text(encoding="utf-8-sig"), parse_constant=invalid)


def number(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite measurement")
    return result


def read_csv(path, columns):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"time_s", *columns}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Missing CSV columns: {sorted(required - set(reader.fieldnames or []))}")
        data = list(reader)
    if len(data) < 2:
        raise ValueError("At least two measured samples are required")
    for row in data:
        for key in required:
            row[key] = number(row[key])
    if data[0]["time_s"] < 0 or any(b["time_s"] <= a["time_s"] for a, b in zip(data, data[1:])):
        raise ValueError("Timestamps must be nonnegative and strictly increasing")
    return data


def common(data, limits):
    duration = number(limits["duration_s"])
    samples = int(limits["samples"])
    if duration <= 0 or samples < 2:
        raise ValueError("Duration and sample count must be positive")
    return {"sample_count": len(data) == samples,
            "duration": math.isclose(data[-1]["time_s"], duration, abs_tol=1e-8)}


def check_drop(root, limits):
    data = read_csv(root / "positions.csv", ["x_m", "y_m", "z_m", "vx_m_s", "vy_m_s", "vz_m_s"])
    metrics = read_json(root / "simulation_result.json")
    checks = common(data, limits)
    tail = [r for r in data if r["time_s"] >= data[-1]["time_s"] - limits["tail_window_s"]]
    if len(tail) < 2:
        raise ValueError("Insufficient samples in settling window")
    z = [r["z_m"] for r in data]
    span = max(r["z_m"] for r in tail) - min(r["z_m"] for r in tail)
    speed = max(math.sqrt(sum(r[k] ** 2 for k in ("vx_m_s", "vy_m_s", "vz_m_s"))) for r in tail)
    published = metrics["stage_position_m"]
    if len(published) != 3:
        raise ValueError("Stage position must contain three components")
    stage_error = max(abs(number(p) - data[-1][key]) for p, key in zip(published, ("x_m", "y_m", "z_m")))
    checks.update({
        "initial_height": abs(z[0] - limits["initial_center_m"]) <= limits["position_tolerance_m"],
        "fell": z[0] - min(z) >= limits["minimum_fall_m"],
        "rest_height": abs(z[-1] - limits["rest_center_m"]) <= limits["position_tolerance_m"],
        "penetration_bound": min(z) >= limits["rest_center_m"] - limits["maximum_penetration_m"],
        "settled_position": span <= limits["maximum_tail_span_m"],
        "settled_speed": speed <= limits["maximum_tail_speed_m_s"],
        "stage_matches_physics": stage_error <= limits["stage_tolerance_m"],
    })
    return checks, {"final_height_m": z[-1], "minimum_height_m": min(z), "stage_error_m": stage_error}, ["viewer", "driverless host", "arbitrary scene fidelity"]


def check_spring(root, limits):
    data = read_csv(root / "trajectory.csv", ["target_m", "initial_estimate_m", "fitted_m", "analytic_m"])
    metric = read_json(root / "metrics.json")
    checks = common(data, limits)
    initial = sum((r["target_m"] - r["initial_estimate_m"]) ** 2 for r in data) / len(data)
    final = sum((r["target_m"] - r["fitted_m"]) ** 2 for r in data) / len(data)
    analytic_error = max(abs(r["target_m"] - r["analytic_m"]) for r in data)
    auto = number(metric["automatic_gradient"])
    finite_difference = number(metric["finite_difference_gradient"])
    error = abs(auto - finite_difference) / max(abs(auto), abs(finite_difference), 1e-12)
    target = number(metric["target_stiffness_N_per_m"])
    if target <= 0:
        raise ValueError("Target stiffness must be positive")
    stiffness_error = abs(number(metric["estimated_stiffness_N_per_m"]) - target) / target
    checks.update({
        "initial_loss_nonzero": initial > 0,
        "loss_reduced": final < initial * limits["maximum_loss_ratio"],
        "loss_records_match_csv": all(math.isclose(actual, number(metric[key]), rel_tol=1e-4, abs_tol=1e-12) for actual, key in [(initial, "initial_loss_m_squared"), (final, "final_loss_m_squared")]),
        "stiffness_recovered": stiffness_error <= limits["maximum_stiffness_relative_error"],
        "automatic_gradient_nonzero": abs(auto) > limits["minimum_gradient_magnitude"],
        "finite_difference_perturbation_positive": number(metric["finite_difference_epsilon_N_per_m"]) > 0,
        "gradient_agreement": error <= limits["maximum_gradient_relative_error"],
        "analytic_agreement": analytic_error <= limits["maximum_analytic_error_m"],
    })
    return checks, {"initial_loss_m2": initial, "final_loss_m2": final, "gradient_relative_error": error, "stiffness_relative_error": stiffness_error, "analytic_error_m": analytic_error}, ["real-data identification", "contact gradients", "other solvers"]


def grasp_measurements(root, limits):
    height, relative = limits["height_column"], limits["relative_column"]
    data = read_csv(root / "block_height.csv", [height, relative])
    hold = [r for r in data if r.get("phase") == "hold"]
    if len(hold) < 2:
        raise ValueError("Hold phase needs at least two measured samples")
    rise = min(r[height] for r in hold) - data[0][height]
    # Range is movement during hold; it does not measure earlier slip during lift.
    slip = max(r[relative] for r in hold) - min(r[relative] for r in hold)
    release_present = any(r.get("phase") in ("release", "fall") for r in data)
    release_drop = hold[-1][height] - data[-1][height]
    return data, hold, {"hold_rise_m": rise, "hold_relative_range_m": slip,
                        "release_present": release_present, "release_drop_m": release_drop}


def check_grasp(root, limits, control=None, require_contacts=False):
    data, hold, observed = grasp_measurements(root, limits)
    metrics = read_json(root / "metrics.json")
    checks = common(data, limits)
    checks.update({"lifted": observed["hold_rise_m"] >= limits["minimum_lift_m"],
                   "held": observed["hold_relative_range_m"] <= limits["maximum_hold_slip_m"],
                   "force_cap": 0 <= number(metrics["max_command_force_N"]) <= limits["maximum_command_force_N"]})
    unverified = ["calibration", "timestep convergence", "hardware transfer"]
    if limits["require_release"]:
        checks["released"] = observed["release_present"] and observed["release_drop_m"] >= limits["minimum_release_drop_m"]
    else:
        unverified.append("release")
    fields = {"left_normal_N", "right_normal_N", "floor_normal_N", "penetration_m"}
    if fields.issubset(data[0]):
        for row in data:
            for field in fields:
                row[field] = number(row[field])
        checks["bilateral_contact"] = all(r["left_normal_N"] > 0 and r["right_normal_N"] > 0 for r in hold)
        checks["floor_free"] = all(abs(r["floor_normal_N"]) <= limits["maximum_floor_force_N"] for r in hold)
        checks["penetration_bound"] = all(0 <= r["penetration_m"] <= limits["maximum_penetration_m"] for r in data)
    else:
        unverified.extend(["bilateral contact forces", "floor contact force", "penetration"])
        if require_contacts:
            checks["contact_evidence_present"] = False
    if control is not None:
        ctrl_data, _, ctrl = grasp_measurements(control, limits)
        ctrl_metrics = read_json(control / "metrics.json")
        checks["control_samples_and_duration"] = all(common(ctrl_data, limits).values())
        checks["control_has_zero_friction"] = number(ctrl_metrics["settings"]["friction"]) == 0
        # Only the intended independent variable may change for this control.
        baseline_settings = {k: v for k, v in metrics["settings"].items() if k != "friction"}
        control_settings = {k: v for k, v in ctrl_metrics["settings"].items() if k != "friction"}
        checks["control_other_settings_match"] = baseline_settings == control_settings
        checks["zero_friction_did_not_lift"] = ctrl["hold_rise_m"] <= limits["maximum_control_lift_m"]
        observed["control_hold_rise_m"] = ctrl["hold_rise_m"]
    else:
        unverified.append("zero-friction control")
    return checks, observed, unverified


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("drop", "spring", "grasp"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--limits", type=Path, required=True, help="Explicit limits for this scene, not universal tolerances")
    parser.add_argument("--control", type=Path, help="Grasp zero-friction output directory")
    parser.add_argument("--require-contact-evidence", action="store_true")
    args = parser.parse_args()
    try:
        limits = read_json(args.limits)
        if limits["kind"] != args.kind:
            raise ValueError("Limit profile does not match the selected check")
        if args.kind == "grasp":
            checks, measured, unverified = check_grasp(args.run, limits, args.control, args.require_contact_evidence)
        else:
            if args.control or args.require_contact_evidence:
                raise ValueError("Contact/control options apply only to grasp checks")
            checks, measured, unverified = (check_drop if args.kind == "drop" else check_spring)(args.run, limits)
        result = {"passed": all(checks.values()), "checks": checks, "measured": measured,
                  "unverified": unverified, "scope": "Saved measurements; does not prove execution, authenticity, or general physical accuracy"}
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        result = {"passed": False, "error": str(error)}
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
