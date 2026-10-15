# SPDX-License-Identifier: Apache-2.0
"""Check metadata-only behavior without installing a physics runtime."""

import contextlib
import importlib.util
from importlib import metadata
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch


PATH = (Path(__file__).resolve().parents[1] / "skills" / "ovphysx" /
        "physical-ai-ovphysx-selection" / "scripts" / "probe_environment.py")
SPEC = importlib.util.spec_from_file_location("ovphysx_metadata_probe", PATH)
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


class OvphysxProbeTests(unittest.TestCase):
    def test_missing_packages_do_not_claim_runtime_failure(self):
        def missing(name):
            raise metadata.PackageNotFoundError(name)
        result = probe.collect(missing, lambda _: self.fail("absent package has no requirements"))
        self.assertTrue(all(value is None for value in result["packages"].values()))
        self.assertEqual(result["status"], "metadata_only")
        self.assertFalse(result["runtime_tested"])
        self.assertFalse(result["gpu_tested"])

    def test_requirements_preserve_pins_and_markers_without_claiming_compatibility(self):
        expected = {"ovphysx": ["ovstage==0.2.1.123", "warp-lang>=1.0; python_version >= '3.10'"],
                    "ovstage": ["numpy>=1.26"]}
        result = probe.collect(lambda _: "0.6.4", lambda name: expected[name])
        self.assertEqual(result["declared_requirements"], expected)
        self.assertFalse(result["dependency_compatibility_tested"])

    def test_unexpected_metadata_error_is_a_probe_failure(self):
        output = io.StringIO()
        with patch.object(probe, "collect", side_effect=OSError("unreadable metadata")), \
                patch("sys.argv", [str(PATH)]), contextlib.redirect_stdout(output):
            status = probe.main()
        self.assertEqual(status, 1)
        result = json.loads(output.getvalue())
        self.assertEqual(result["status"], "probe_failed")
        self.assertEqual(result["error_type"], "OSError")


if __name__ == "__main__":
    unittest.main()
