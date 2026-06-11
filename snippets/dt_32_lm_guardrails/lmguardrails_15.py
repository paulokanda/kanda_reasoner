import traceback
from pathlib import Path

def safe_gpu_wrapper(fn, fallback_fn=None, description=""):
    try:
        return fn()
    except Exception:
        log_path = Path("lm_guardrails_15/gpu_guard_log.txt")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(f"🔥 GPU backend failure during: {description}\n")
            f.write(traceback.format_exc() + "\n")
        print(f"⚠️ GPU failure during '{description}', falling back... Log written to {log_path}")
        if fallback_fn:
            return fallback_fn()
        else:
            print("❌ No fallback function provided.")
            return None

# Example usage
if __name__ == "__main__":
    def primary():
        import torch
        return torch.randn(3).cuda()  # Trigger if CUDA unavailable

    def fallback():
        import torch
        return torch.randn(3)  # CPU fallback

    result = safe_gpu_wrapper(primary, fallback_fn=fallback, description="Torch CUDA test")
    print("✅ Result:", result)
