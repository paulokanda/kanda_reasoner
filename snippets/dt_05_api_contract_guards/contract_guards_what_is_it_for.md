
# 🛡️ API Contract Guards – What Is It For?

This module helps you **analyze your function signatures and usage patterns** to automatically propose runtime checks that enforce your intended behavior.

It uses your **local LLM** (running at `http://127.0.0.1:5000`) to infer **preconditions and postconditions** for Python functions—especially useful in EEG, signal processing, and GUI-heavy codebases.

---

## ✅ What It Does

Given a Python module file (e.g., `my_signal_utils.py`), it:

1. **Parses function signatures and docstrings**
2. Sends the content to your LLM for analysis
3. Generates a **Markdown report** suggesting:

   - 🔍 **Preconditions**: shape, dtype, range checks
   - ✅ **Postconditions**: guarantees on return values
   - 🔐 **Type guards, asserts, or Pydantic validators**
   - 🧪 Optional test cases to enforce those contracts

---

## 🧪 Example Use Case

If your function looks like:

```python
def compute_bandpower(signal: np.ndarray, sfreq: float) -> float:
    """Compute band power from EEG signal."""
    ...
```

The tool might recommend:

- `assert signal.ndim == 1`
- `assert sfreq > 0`
- `return must be a float >= 0.0`

---

## 🚀 How To Use

1. Stage a Python module file with functions you want analyzed.
2. Run the tool like this:

```bash
python api_cntrct_guards_03.py path/to/your_module.py
```

3. It creates a report like:

```
dev_tools/api_contract_guards_03/contract_guard_suggestions.md
```

---

## 🧠 Why It Matters

In signal-heavy apps (like EEG), small input bugs (wrong shape, type, or NaN values) can silently break your visualizations or analysis.

Instead of manually writing dozens of `assert` statements or Pydantic models, let the LLM give you a starting point.

---

## 📍 Where to Find Output

Output file:
```
dev_tools/api_contract_guards_03/contract_guard_suggestions.md
```

---

## ⚙️ Configuration

The script uses:

- **API**: `http://127.0.0.1:5000/v1/chat/completions`
- **Model**: `WizardCoder-Python-13B-GGUF`
- **Token**: dummy `"local-anything"`

Make sure your LLM server has the OpenAI-compatible extension enabled.

---
