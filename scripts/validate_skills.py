#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate portable metadata, local resource links, and evaluation case structure.

This is a packaging check. It does not execute an agent or certify its behavior.
Requires PyYAML, listed in requirements-dev.txt.
"""

import json
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "ovnewton": {"physical-ai-physics-selection", "ovnewton-prepare-scene", "ovnewton-tune-physics"},
    "ovphysx": {"ovphysx-selection"},
}


def check_evaluations(directory, name):
    paths = [directory / "evals" / filename for filename in ("evals.json", "cases.json")]
    present = [path for path in paths if path.is_file()]
    if len(present) != 1:
        raise ValueError("expected exactly one primary evaluation dataset")
    dataset = json.loads(present[0].read_text(encoding="utf-8"))
    if not isinstance(dataset, dict):
        raise ValueError("invalid evaluation dataset")
    nvidia_format = present[0].name == "evals.json"
    if nvidia_format:
        if dataset.get("skill_name") != name:
            raise ValueError("evaluation skill name mismatch")
        cases = dataset.get("evals")
        criteria_key = "assertions"
    else:
        if dataset.get("schema_version") != 1 or dataset.get("skill") != name:
            raise ValueError("invalid evaluation dataset")
        cases = dataset.get("cases")
        criteria_key = "expected"
    if not isinstance(cases, list) or not cases:
        raise ValueError("empty evaluation dataset")
    seen = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("invalid evaluation case")
        if not isinstance(case.get("id"), str) or not case["id"] or case["id"] in seen:
            raise ValueError("invalid or duplicate evaluation id")
        seen.add(case["id"])
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("missing evaluation prompt")
        criteria = case.get(criteria_key)
        if not isinstance(criteria, list) or not criteria or any(
                not isinstance(item, str) or not item.strip() for item in criteria):
            raise ValueError("missing behavioral acceptance criteria")
        if nvidia_format:
            if not isinstance(case.get("expected_output"), str) or not case["expected_output"].strip():
                raise ValueError("missing expected output")
            if "expected_skill" in case and case["expected_skill"] not in (None, name):
                raise ValueError("unexpected routing target")
            if "expected_script" in case:
                script = case["expected_script"]
                if not isinstance(script, str) or not script.strip():
                    raise ValueError("invalid expected script")
                resolved = (directory / script).resolve()
                if not resolved.is_relative_to((directory / "scripts").resolve()) or not resolved.is_file():
                    raise ValueError("expected script must exist within this skill's scripts directory")
    return len(cases)


def check_skill(directory):
    text = (directory / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    meta = yaml.safe_load(match.group(1))
    if not isinstance(meta, dict) or set(meta) - {"name", "description", "license", "compatibility", "metadata"}:
        raise ValueError("unexpected frontmatter; keep platform-specific controls out of the portable core")
    name = meta.get("name", "")
    if name != directory.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("invalid name")
    description = meta.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        raise ValueError("invalid description")
    metadata = meta.get("metadata", {})
    if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
        raise ValueError("metadata values must be strings")
    if len(text.splitlines()) >= 500:
        raise ValueError("entrypoint too long; move conditional detail into references")
    # Installed skills must not rely on sibling skills or repository-only files.
    for doc in directory.rglob("*.md"):
        content = doc.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (doc.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(directory.resolve()) or not resolved.exists():
                raise ValueError(f"broken or nonportable local resource link in {doc.name}: {target}")
        if "[TODO:" in content:
            raise ValueError(f"unfinished scaffold in {doc.name}")
    return check_evaluations(directory, name)


def main():
    seen_names = set()
    for group, names in EXPECTED.items():
        directories = sorted(p for p in (ROOT / "skills" / group).iterdir() if p.is_dir())
        if {p.name for p in directories} != names:
            raise ValueError(f"unexpected published skill directories under skills/{group}")
        for directory in directories:
            if directory.name in seen_names:
                raise ValueError(f"duplicate installable skill name: {directory.name}")
            seen_names.add(directory.name)
            count = check_skill(directory)
            print(f"PASS {directory.name}: portable metadata, resources, {count} evaluation cases")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
