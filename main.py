from __future__ import annotations

import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable


def run_step(script_path: Path) -> None:
    completed = subprocess.run([PYTHON_EXE, str(script_path)], check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> None:
    run_step(BASE_DIR / "src" / "data_cleaninig.py")
    run_step(BASE_DIR / "src" / "build_initial_reaction_dataset.py")


if __name__ == "__main__":
    main()
