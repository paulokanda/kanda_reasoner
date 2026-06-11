# 📘 What is `depend_risk_briefs_07.py` for?

This script uses your local LLM (running on http://127.0.0.1:5000) to analyze your `requirements.txt` for:

- 🔍 Version conflicts (e.g., Torch + CUDA mismatches, PyQt + Qt issues)
- 🚫 Deprecated or risky packages
- 🧱 Suggestions for stable pins (safe version combos)
- 💡 Comments on GPU/ML compatibility

## ✅ Use Case

You're working on an EEG app that mixes PyQt, NumPy/SciPy, deep learning, and visualization. This tool helps you ensure your `requirements.txt` isn't quietly sabotaging stability due to:

- Unmaintained packages
- Incompatible GPU drivers
- Wild version ranges

## ▶️ How to Run

From the root of your project:

```bash
python dev_tools/dependency_risk_briefs_07/depend_risk_briefs_07.py
```

### ✅ Output

It generates a file:

```
dev_tools/dependency_risk_briefs_07/dependency_risk_report.md
```

With:

- A full Markdown report
- Sectioned risks + recommendations
- Easy to copy pin set

## ⚠️ Prerequisites

- You must have `requirements.txt` at the root
- Your LLM API must be running at `http://127.0.0.1:5000/v1/chat/completions`
