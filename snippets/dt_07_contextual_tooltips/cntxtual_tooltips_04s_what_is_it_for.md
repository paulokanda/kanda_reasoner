# 🧠 Contextual Tooltips Generator (cntxtual_tooltips_04.py)

This tool helps generate **meaningful tooltips** for Qt widgets (e.g., `QPushButton`, `QLabel`, `QComboBox`) in your EEG app, based on their variable names and code comments.

---

## ✅ What Is It For?

In GUI development, tooltips improve usability—especially for clinical users who rely on visual hints. This script scans your Qt-based Python file and suggests tooltip text based on the names of widgets and nearby comments.

It helps you:

- Detect where tooltips are missing
- Auto-suggest tooltip text using widget names and surrounding comments
- Improve UX without manually tracking every button or checkbox

---

## 📂 Where to Place It?

This script lives at:
```
dev_tools/contextual_tooltips_04/cntxtual_tooltips_04.py
```

---

## ▶️ How to Run

From the terminal or PyCharm green button, run:

```bash
python dev_tools/contextual_tooltips_04/cntxtual_tooltips_04.py
```

You'll be prompted:

```
📂 Enter path to your Qt/PyQt/PySide6 Python file (relative to EEG_KANDA/, e.g. k00_main/kanda_main.py):
```

🔁 **Do NOT include `EEG_KANDA/`** in your input—just the relative path. For example:

```
k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_template_helpers/class_ui_layout_cmbbx_template_helper.py
```

---

## 🧪 Output Example

If tooltips are detected, you'll see output like:

```
🧠 Tooltip Suggestions:
  - Line 45: `save_button` (QPushButton) → Tooltip: Save current selection
  - Line 72: `notch_checkbox` (QCheckBox) → Tooltip: No comment
```

---

## 🛠️ What It Looks For

- `QPushButton`, `QCheckBox`, `QComboBox`, `QSlider`, `QLabel`
- Assigned to variables like `submit_btn`, `notch_checkbox`, etc.
- Looks at line number and nearby comments to infer intent

---

## ❌ No Output?

- Ensure the file exists and is a `.py` file with Qt widgets
- Check your path is **relative to EEG_KANDA/** and valid
- No supported widget types? Script will say `✅ No tooltip candidates found.`

---

## 🚧 Future Ideas

- Connect to local LLM to autogenerate clinically correct tooltip descriptions
- Output a `.md` or `.json` file with tooltip suggestions for copy/paste