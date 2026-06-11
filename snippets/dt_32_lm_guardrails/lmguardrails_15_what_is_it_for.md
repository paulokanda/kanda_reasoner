# 🛡️ What is `lmguardrails_15.py` for?

This module adds **robust runtime safety** for machine learning (ML) and GPU backend calls (like CUDA, `llama.cpp`, or `exllama`).

## ✅ What It Does

- Wraps GPU-heavy functions like `.cuda()` or model loading with a `safe_gpu_wrapper()`.
- If the GPU call fails (e.g., driver issue, out of memory, incompatible backend), it:
  - Logs the traceback to `gpu_guard_log.txt`
  - Falls back to a safe CPU version or user-defined recovery function.
  - Prints a clear warning in the console.
- Prevents your EEG GUI or batch scripts from crashing silently due to backend issues.

## 🧪 Example

```python
def primary():
    import torch
    return torch.randn(3).cuda()

def fallback():
    import torch
    return torch.randn(3)

result = safe_gpu_wrapper(primary, fallback_fn=fallback, description="Torch CUDA test")
```

## 📂 Output

- `gpu_guard_log.txt` will contain the stack trace of any GPU failure.
- `stdout` will warn and report fallback usage.

## 🚀 Use Cases

- Wrapping parts of EEG preprocessing that require GPU (e.g., `exllama`, spectrograms).
- Preventing crashes in environments where CUDA is not guaranteed (e.g., shared machines, CI).

## 📍 Where to Hook

- Model loaders (`llama.cpp`, `transformers`, etc.)
- PyTorch GPU ops
- TorchAudio or SciPy GPU integrations
