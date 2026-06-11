# runtime_guardrails_22/rtime_guardr_22.py

import traceback
import datetime
from pathlib import Path

LOG_DIR = Path("runtime_guardrails_22/guardrail_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def safe_gpu_call(gpu_function, fallback_function=None, *args, **kwargs):
    """
    Attempt to run a GPU function, with a fallback if it fails.

    Parameters
    ----------
    gpu_function : Callable
        The function using CUDA/torch/llama.cpp/etc.
    fallback_function : Optional[Callable]
        A CPU-safe fallback.
    *args, **kwargs :
        Arguments for both functions.

    Returns
    -------
    Result of the GPU function, or fallback, or None if both fail.
    """
    try:
        return gpu_function(*args, **kwargs)
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"gpu_guard_{timestamp}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("⚠️ GPU Call Failed:
")
            f.write(traceback.format_exc())
        print(f"⚠️ GPU failure logged to {log_file.resolve()}")

        if fallback_function:
            print("🔁 Attempting fallback...")
            try:
                return fallback_function(*args, **kwargs)
            except Exception as e:
                print("❌ Fallback also failed.")
                return None
        else:
            return None

# Example usage
if __name__ == "__main__":
    def crash_gpu():
        raise RuntimeError("Simulated GPU backend failure")

    def fallback_cpu():
        print("Fallback CPU path executed.")
        return "CPU result"

    result = safe_gpu_call(crash_gpu, fallback_cpu)
    print("✅ Result:", result)
