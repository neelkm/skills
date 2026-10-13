#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Linux CPU integration checks; run only with the pinned product environment."""

import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ovnewton-prepare-scene"
ASSET = SKILL / "assets/falling-box.usda"


def main():
    with tempfile.TemporaryDirectory() as temp:
        for solver in ("xpbd", "vbd"):
            output = Path(temp) / f"{solver}.json"
            subprocess.run([sys.executable, str(SKILL / "scripts/inspect_scene.py"), str(ASSET),
                            "--solver", solver, "--device", "cpu", "--output", str(output)], check=True, timeout=300)
            result = json.loads(output.read_text(encoding="utf-8"))
            assert result["status"] == "imported", result
            assert result["counts"]["bodies"] == 1, result["counts"]
            assert result["counts"]["shapes"] == 2, result["counts"]
            assert result["body_labels"] == ["/World/Box"], result["body_labels"]
            assert math.isclose(result["mass"][0], 1.0, rel_tol=1e-5), result["mass"]
            assert math.isclose(result["gravity"][0][2], -9.81, rel_tol=1e-5), result["gravity"]
            assert not result["simulation_tested"]
            subprocess.run([sys.executable, "-m", "ovnewton.examples.example_ovnewton_basic",
                            "--solver", solver, "--device", "cpu", "--no-render", "--num-frames", "8"],
                           check=True, timeout=300)
            print(f"PASS {solver}: model inspection and eight-frame CPU smoke", flush=True)


if __name__ == "__main__":
    main()
