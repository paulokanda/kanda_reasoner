"""Support profiling workflows for developer tooling."""

import os

import sys

import traceback

from pathlib import Path

import subprocess

from shell.kanda_main import main

def test_governance_probe():
    pass


def run_with_trace_main() -> int:
    os.environ["KANDA_DEBUG"] = os.environ.get("KANDA_DEBUG", "1")

    os.environ.setdefault("MPLCONFIGDIR", r"E:\EEG_KANDA\_cache\mpl")

    os.environ.setdefault("MPLBACKEND", "QtAgg")

    watchdog_script = Path("kanda_python_tools/ai_starter/watchdog_ai_repatcher.py")

    if watchdog_script.exists():
        subprocess.Popen(["python", str(watchdog_script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        print("[START] Launching main EEG app...\n")
        main()
    except Exception as e:
        crash_dir = Path("kanda_python_tools/run_with_trace_crash_log_files")
        crash_dir.mkdir(parents=True, exist_ok=True)

        crash_log_path = crash_dir / "last_crash.log"
        with open(crash_log_path, "w", encoding="utf-8") as f:
            f.write("[ERROR] Crash Traceback:\n")
            f.write(traceback.format_exc())

        print(f"[FAIL] Crash log written to: {crash_log_path.resolve()}")
        raise

    return 0


if __name__ == "__main__":
    raise SystemExit(run_with_trace_main())
