# 📘 What is `run_timemap_21.py` for?

This module transforms runtime trace data into a **Markdown runtime report** that helps you visually inspect what parts of your application are running most often.

---

## ✅ What It Does

- Reads a runtime trace JSON from `.runmap/last.json`
- Tallies all Python function calls by file and function
- Outputs a Markdown summary with:
  - 📂 Most Called Files
  - 🔧 Most Called Functions

---

## 🧪 How It Works

1. A separate script (e.g., `runtime_map.py`) should generate `.runmap/last.json` using Python's `sys.setprofile`.
2. Then, this script parses that trace and:
   - Counts how often each file and function is hit.
   - Renders it as an easy-to-read Markdown list.
3. The output is saved to:

```
dev_tools/run_time_map_21/runtime_map_report.md
```

---

## 📌 Usage

```bash
python dev_tools/run_time_map_21/run_timemap_21.py
```

---

## 📂 Example Output

```md
# 🧠 EEG Runtime Map Report

Generated: 2025-10-04 03:33:00

## 📂 Most Called Files
- dev/main.py — 81 calls
- ui/plot_helpers.py — 67 calls

## 🔧 Most Called Functions
- draw_trace_plot — 45 calls
- apply_notch_filter — 40 calls
```

This helps guide your **profiling**, **refactoring**, and **test coverage** efforts.

---