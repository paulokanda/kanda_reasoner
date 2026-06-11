# 🧹 deadcode_find_06.py — What Is It For?

This script analyzes a Python source file and finds **functions that are defined but never called** — also known as **dead code**.

---

## ✅ What It Detects

- Functions declared but not used within the same file.
- Helps clean up unused helpers, stubs, or legacy logic.

---

## 🚀 How To Use It

1. Run the script:
   ```bash
   python dev_tools/dead_code_finder_06/deadcode_find_06.py
   ```

2. When prompted, enter a path relative to your project root (`EEG_KANDA/`):
   ```
   📂 Enter path to your Python module (relative to EEG_KANDA/, e.g. k00_main/kanda_main.py):
   > k01_core_eeg/k01_3_eeg_visualizer/helpers/signal_tools.py
   ```

3. Output:
   - 🧹 A list of possibly unused functions.
   - ✅ Or confirmation that all functions are used.

---

## ⚠️ Limitations

- Only checks within the **same file**.
- Won’t catch usage from other files or dynamic calls.

---

## 💡 Tip

Run this regularly before big refactors to keep your code lean!
