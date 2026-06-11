# ⛑️ What is `rtime_guardr_22.py` for?

This module provides **runtime guardrails** for your GPU-based EEG processing code (e.g. `torch`, `llama.cpp`, `exllama`, etc.).

## ✅ What It Does
- Wraps risky GPU or native extension calls.
- Logs full traceback to a file in case of crash.
- Tries a fallback function if available (e.g. CPU version of a loader or visualizer).
- Ensures your PyQt or analysis tool degrades gracefully instead of crashing.

## 💡 Example Use Cases
- Llama.cpp model crashes if VRAM is low.
- Torch model fails on some edge-case tensor.
- Custom Qt widget with OpenGL fails on driver issue.

## 🧪 How to Use

```python
from dev_tools.runtime_guardrails_22.rtime_guardr_22 import safe_gpu_call

result = safe_gpu_call(run_on_gpu, fallback_cpu, arg1, arg2)
```

## 📂 Logs
All GPU-related errors will be saved to:

```
dev_tools/runtime_guardrails_22/guardrail_logs/gpu_guard_<timestamp>.log
```

Perfect for debugging tricky CUDA or backend issues without crashing the whole EEG app.
