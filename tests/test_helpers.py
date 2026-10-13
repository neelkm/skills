# SPDX-License-Identifier: Apache-2.0
"""Exercise observable helper behavior without a physics runtime."""

import importlib.util
from importlib import metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(skill, script):
    path = ROOT / "skills" / skill / "scripts" / f"{script}.py"
    spec = importlib.util.spec_from_file_location(script, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load_module("ovnewton-select-and-setup", "probe_environment")
compare = load_module("ovnewton-tune-physics", "compare_runs")
inspect = load_module("ovnewton-prepare-scene", "inspect_scene")


def sample(error=0.04):
    return {"schema_version": 1,
            "context": {"scene_id": "scene-a", "workload_id": "commands-a", "duration_s": 2.0,
                        "seed": 17, "device": "cpu", "solver": "xpbd",
                        "versions": {"ovnewton": "0.2.0", "newton": "1.6.0", "ovstage": "0.2.0.377349", "warp-lang": "1.17.0"},
                        "measurement": "no-render-wall-time-v1"},
            "settings": {"substeps": 2},
            "metrics": {"tracking_error": error, "penetration": 0.003, "runtime_s": 4.0, "nonfinite_states": 0},
            "units": {"tracking_error": "rad", "penetration": "m", "runtime_s": "s", "nonfinite_states": "count"}}


class ProbeTests(unittest.TestCase):
    def test_missing_packages_are_not_runtime_failure(self):
        def missing(name):
            raise metadata.PackageNotFoundError(name)
        result = probe.collect(missing, lambda _: self.fail("must not request absent package requirements"))
        self.assertTrue(all(value is None for value in result["packages"].values()))
        self.assertEqual(result["status"], "metadata_only")
        self.assertFalse(result["runtime_tested"])

    def test_declared_requirements_are_preserved(self):
        result = probe.collect(lambda _: "1.0", lambda _: ["ovstage>=0.2,<0.3", "ovrtx; extra == 'examples'"])
        self.assertEqual(len(result["ovnewton_declared_requirements"]), 2)
        self.assertFalse(result["gpu_tested"])


class ComparisonTests(unittest.TestCase):
    def test_accept_improvement_within_bounds(self):
        result = compare.compare(sample(), sample(0.02), "tracking_error", "minimize", {"penetration": 0.005}, 0.1)
        self.assertEqual(result["status"], "accepted")
        self.assertAlmostEqual(result["relative_improvement"], 0.5)

    def test_reject_faster_but_physical_limit_exceeded(self):
        trial = sample(0.02)
        trial["metrics"]["penetration"] = 0.02
        result = compare.compare(sample(), trial, "tracking_error", "minimize", {"penetration": 0.005})
        self.assertEqual(result["status"], "rejected")

    def test_numerical_failure_bound_cannot_be_weakened(self):
        trial = sample(0.02)
        trial["metrics"]["nonfinite_states"] = 1
        self.assertEqual(compare.compare(sample(), trial, "tracking_error", "minimize", {"nonfinite_states": 100})["status"], "rejected")
        with self.assertRaises(ValueError):
            compare.compare(sample(), trial, "tracking_error", "minimize", {"nonfinite_states": float("nan")})
        self.assertEqual(compare.compare(sample(), sample(0.02), "tracking_error", "minimize", {"nonfinite_states": -1})["status"], "rejected")

    def test_context_change_rejected(self):
        for key, value in (("device", "cuda:0"), ("scene_id", "other-scene"), ("solver", "vbd"), ("seed", 18)):
            trial = sample(0.02)
            trial["context"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                compare.compare(sample(), trial, "tracking_error", "minimize")

    def test_units_change_rejected(self):
        trial = sample(0.02)
        trial["units"]["tracking_error"] = "degrees"
        with self.assertRaises(ValueError):
            compare.compare(sample(), trial, "tracking_error", "minimize")

    def test_missing_metric_rejected(self):
        with self.assertRaises(ValueError):
            compare.compare(sample(), sample(0.02), "tracking_error", "minimize", {"missing": 1})

    def test_nonfinite_and_boolean_metrics_rejected(self):
        for value in (float("nan"), float("inf"), True):
            trial = sample(value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                compare.compare(sample(), trial, "tracking_error", "minimize")

    def test_zero_baseline_has_no_relative_improvement(self):
        result = compare.compare(sample(0.0), sample(-1.0), "tracking_error", "minimize", min_relative=0.1)
        self.assertIsNone(result["relative_improvement"])
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(compare.compare(sample(0), sample(-1), "tracking_error", "minimize", min_absolute=0.5)["status"], "accepted")

    def test_maximize_and_ties(self):
        self.assertEqual(compare.compare(sample(0.02), sample(0.04), "tracking_error", "maximize")["status"], "accepted")
        self.assertEqual(compare.compare(sample(), sample(), "tracking_error", "minimize")["status"], "rejected")

    def test_nonstandard_json_and_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for content in ('{"x": NaN}', '{"x": 1, "x": 2}'):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    compare.load_run(path)

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as temp:
            baseline, trial = Path(temp) / "baseline.json", Path(temp) / "trial.json"
            baseline.write_text(json.dumps(sample()), encoding="utf-8")
            command = [sys.executable, compare.__file__, str(baseline), str(trial), "--metric", "tracking_error", "--direction", "minimize"]
            for data, expected in ((sample(0.02), 0), (sample(0.05), 1), ({}, 2)):
                trial.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run(command, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertIn("status", json.loads(result.stdout))


class InspectionTests(unittest.TestCase):
    def test_zero_mass_is_not_automatically_invalid(self):
        self.assertEqual(inspect.numeric_findings([0, 1], [[[0.0]]], [[0, 0, 0]], [[0, 0, -9.81]]), [])

    def test_negative_mass_and_nonfinite_inertia_are_identified(self):
        findings = inspect.numeric_findings([-1], [[[float("nan")]]], [[0, 0, 0]], [[0, 0, -9.81]])
        self.assertTrue(any(item["field"] == "mass[0]" for item in findings))
        self.assertTrue(any(item["field"].startswith("inertia") for item in findings))
        json.dumps(inspect.json_safe({"findings": findings, "value": float("inf")}), allow_nan=False)

    def test_empty_static_scene_is_a_note(self):
        findings = inspect.numeric_findings([], [], [], [[0, 0, -9.81]])
        self.assertEqual(findings[0]["severity"], "note")

    def test_help_does_not_require_native_sdk(self):
        result = subprocess.run([sys.executable, inspect.__file__, "--help"], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0)

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result.json"
            output.write_text("keep-me", encoding="utf-8")
            asset = ROOT / "skills/ovnewton-prepare-scene/assets/falling-box.usda"
            result = subprocess.run([sys.executable, inspect.__file__, str(asset), "--output", str(output)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep-me")


if __name__ == "__main__":
    unittest.main()
