#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Read ovphysx-related metadata without importing native simulation libraries.

Run with the application's interpreter. This inventory does not resolve package
requirements, inspect AVX or GPUs, or establish runtime readiness.
"""

import argparse
from importlib import metadata
import json
import platform
import sys


PACKAGES = ("ovphysx", "ovstage", "warp-lang", "numpy", "usd-core",
            "newton-usd-schemas", "torch", "ovrtx")


def collect(version_reader=metadata.version, requirements_reader=metadata.requires):
    """Read declared metadata; missing distributions are not runtime failures."""
    packages = {}
    for name in PACKAGES:
        try:
            packages[name] = version_reader(name)
        except metadata.PackageNotFoundError:
            packages[name] = None
    requirements = {}
    for name in ("ovphysx", "ovstage"):
        requirements[name] = (requirements_reader(name) or []) if packages[name] is not None else []
    return {
        "schema_version": 1,
        "status": "metadata_only",
        "python": {"version": platform.python_version(), "executable": sys.executable},
        "host": {"os": platform.system(), "architecture": platform.machine()},
        "packages": packages,
        "declared_requirements": requirements,
        "dependency_compatibility_tested": False,
        "runtime_tested": False,
        "gpu_tested": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        result = collect()
    except Exception as exc:
        print(json.dumps({"status": "probe_failed", "error_type": type(exc).__name__,
                          "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
