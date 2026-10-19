#!/usr/bin/env python3
"""Read package metadata only; do not import native simulation libraries."""

import json
import platform
import sys
from importlib import metadata


PACKAGES = (
    "newton",
    "ovnewton",
    "ovphysx",
    "ovstage",
    "warp-lang",
    "physx-usd-schemas",
    "newton-usd-schemas",
)


def collect_metadata():
    packages = {}
    for name in PACKAGES:
        try:
            distribution = metadata.distribution(name)
        except metadata.PackageNotFoundError:
            packages[name] = None
        else:
            packages[name] = {
                "version": distribution.version,
                "requires_python": distribution.metadata.get("Requires-Python"),
                "requires_dist": distribution.requires or [],
            }
    return {
        "status": "metadata_only",
        "python": platform.python_version(),
        "executable": sys.executable,
        "system": platform.system(),
        "machine": platform.machine(),
        "packages": packages,
        "limits": [
            "No native simulation libraries were imported.",
            "Dependencies were not resolved or checked for compatibility.",
            "CPU features, GPUs, drivers, rendering, and physics were not tested.",
            "Missing packages are null; SDK-only installs may have no Python metadata.",
        ],
    }


def main():
    try:
        result = collect_metadata()
    except Exception as error:
        print(json.dumps({"status": "probe_failed", "error": str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
