# heisenbug_capturer_11/heisenbug_cap_11.py

import traceback
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR / "heisenbug_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"heisenbug_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def capture_heisenbug(main_function, *args, **kwargs):
    try:
        main_function(*args, **kwargs)
    except Exception:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("⚠️ Exception occurred in run:\n")
            f.write(traceback.format_exc())
            f.write("\n📦 Args: " + str(args))
            f.write("\n🧩 Kwargs: " + str(kwargs))
        print(f"❌ Crash log written to {LOG_FILE.resolve()}")
        raise

# Example usage
if __name__ == "__main__":
    def buggy_function():
        raise RuntimeError("Simulated intermittent crash.")
    capture_heisenbug(buggy_function)
