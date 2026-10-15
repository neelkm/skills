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
    "ovphysx": {"physical-ai-ovphysx-selection"},
}


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
    cases = json.loads((directory / "evals" / "cases.json").read_text(encoding="utf-8"))
    if cases.get("schema_version") != 1 or cases.get("skill") != name or len(cases.get("cases", [])) < 1:
        raise ValueError("invalid evaluation dataset")
    seen = set()
    for case in cases["cases"]:
        if not isinstance(case.get("id"), str) or not case["id"] or case["id"] in seen:
            raise ValueError("invalid or duplicate evaluation id")
        seen.add(case["id"])
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("missing evaluation prompt")
        if not isinstance(case.get("expected"), list) or not case["expected"] or any(
                not isinstance(x, str) or not x.strip() for x in case["expected"]):
            raise ValueError("missing behavioral acceptance criteria")
    return len(cases["cases"])


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
