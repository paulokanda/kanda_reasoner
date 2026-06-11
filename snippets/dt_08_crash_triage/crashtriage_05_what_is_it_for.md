# crashtriage_05_what_is_it_for.md

## 📌 What is it for?

`crashtriage_05.py` helps you diagnose runtime crashes in your EEG analysis app by sending captured Python tracebacks to your **local LLM**. It returns:

- A **root cause analysis** of the crash
- Probable **broken invariants**
- A **minimal reproduction snippet**
- A **3-step fix plan** (e.g., shape checks, API corrections)

Perfect for catching tricky bugs in PyQt, NumPy, SciPy, or EEG pipeline code.

---

## 🛠️ How it works

1. Simulates or captures a crash (`simulate_crash` method).
2. Formats the traceback and sends it to the OpenAI-compatible API at:
   ```
   http://127.0.0.1:5000/v1/chat/completions
   ```
3. Parses and writes the Markdown triage summary to:
   ```
   dev_tools/crash_triage_05/crash_triage_report.md
   ```

---

## ▶️ How to Use

### Run it manually
```bash
python dev_tools/crash_triage_05/crashtriage_05.py
```

### Use in your real app
Replace `simulate_crash()` with the real failing code inside your app, or trigger it conditionally in your crash handler.

---

## 🧪 Output Example

```md
# Crash Triage Report

Generated: 2025-10-03 20:45

## 🔍 Likely Cause
...

## 🧱 Broken Invariants
...

## 🧪 Reproduction Snippet
...

## 🛠️ Fix Plan
1. ...
2. ...
3. ...
```
