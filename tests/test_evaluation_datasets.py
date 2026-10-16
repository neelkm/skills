# SPDX-License-Identifier: Apache-2.0
"""Exercise both dataset contracts and reject ambiguous or nonportable cases."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class EvaluationDatasetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "sample-skill"
        (self.skill / "evals").mkdir(parents=True)

    def write(self, filename, data):
        (self.skill / "evals" / filename).write_text(json.dumps(data), encoding="utf-8")

    def nvidia_dataset(self):
        return {"skill_name": "sample-skill", "evals": [
            {"id": "negative", "prompt": "Perform an unrelated task.", "expected_skill": None,
             "expected_output": "Complete the unrelated task.", "assertions": ["Do not load this skill."]}
        ]}

    def test_both_formats_accept_behavioral_cases(self):
        self.write("evals.json", self.nvidia_dataset())
        self.assertEqual(validator.check_evaluations(self.skill, "sample-skill"), 1)
        (self.skill / "evals" / "evals.json").unlink()
        self.write("cases.json", {"schema_version": 1, "skill": "sample-skill", "cases": [
            {"id": "legacy", "prompt": "Inspect a task.", "expected": ["Report evidence."]}
        ]})
        self.assertEqual(validator.check_evaluations(self.skill, "sample-skill"), 1)

    def test_expected_script_cannot_escape_skill(self):
        outside = self.skill.parent / "outside.py"
        outside.write_text("pass\n", encoding="utf-8")
        data = self.nvidia_dataset()
        data["evals"][0]["expected_script"] = "../outside.py"
        self.write("evals.json", data)
        with self.assertRaisesRegex(ValueError, "expected script must exist"):
            validator.check_evaluations(self.skill, "sample-skill")

    def test_missing_output_and_duplicate_primary_dataset_are_rejected(self):
        data = self.nvidia_dataset()
        data["evals"][0]["expected_output"] = " "
        self.write("evals.json", data)
        with self.assertRaisesRegex(ValueError, "missing expected output"):
            validator.check_evaluations(self.skill, "sample-skill")
        self.write("evals.json", self.nvidia_dataset())
        self.write("cases.json", {"schema_version": 1, "skill": "sample-skill", "cases": []})
        with self.assertRaisesRegex(ValueError, "exactly one primary"):
            validator.check_evaluations(self.skill, "sample-skill")


if __name__ == "__main__":
    unittest.main()
