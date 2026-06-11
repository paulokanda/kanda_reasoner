# 🧪 What is `gui_specs_10.py` for?

This script helps **automatically infer basic user interaction flows** from your Qt/PyQt/PySide6 code. It scans for widget show/set operations and generates an **outline of the typical GUI usage pattern**.

---

### ✅ What It Does

- Parses your code for GUI operations like:
  - `.show()`, `.setVisible(True)`, `.setText(...)`, `.setChecked(...)`, `.setCurrentIndex(...)`
- Infers a sequence of visible UI changes
- Prints a numbered list of the GUI steps

---

### 🧠 Why It's Useful

- Helps generate **pytest-qt or Playwright UI tests**
- Identifies **unreachable or skipped GUI paths**
- Assists in documenting complex Qt workflows

---

### 🧪 How To Use It

```bash
python dev_tools/gui_specs_10/gui_specs_10.py
```

Then, enter the file path (relative to `EEG_KANDA/`) of any file that defines UI logic (e.g., with `QPushButton`, `QMainWindow`, etc.).

---

### 📥 Output Example

```
🧪 GUI Flow (inferred):
  1. self.button_start.show()
  2. self.timeline.setVisible()
  3. self.label_status.setText()
```

---

This is a powerful way to extract **real UI usage** from code alone.
