# 🐛 What is `heisenbug_cap_11.py` for?

This module is designed to **capture hard-to-reproduce or intermittent crashes** in your EEG application.

## ✅ What It Does

- Wraps your app's main function inside a try/except block.
- Automatically logs:
  - Full traceback
  - Time of crash
  - Arguments passed to the crashing function
- Stores crash logs in: `dev_tools/heisenbug_capturer_11/heisenbug_logs/`

## 💡 Why It Matters

Heisenbugs (bugs that disappear when you try to debug them) are common in:
- GUI event-driven code (PyQt, threading)
- NumPy array processing with edge cases
- Race conditions in file I/O or sensors

By capturing the **exact call and error details**, this tool helps you:

- 🧪 Reproduce crashes locally
- 📬 Share minimal logs with LLMs or team for analysis

## 🚀 How to Use

1. Import and wrap your main function:
```python
from dev_tools.heisenbug_capturer_11.heisenbug_cap_11 import capture_heisenbug

def main():
    # your app logic

capture_heisenbug(main)
```

2. On crash, check `heisenbug_logs/` for a detailed crash report.

## 🧠 Bonus: Pair with LLM

You can send the generated `.log` to your local LLM crash triage tool (`crash_triage_05.py`) for immediate explanation and fix suggestions.
