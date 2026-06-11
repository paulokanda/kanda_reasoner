# 🧙‍♂️ What is `exp_wizards_09.py` for?

This script creates a **one-click export bundle** of runtime results from your EEG analysis session.

---

## ✅ What It Does

It collects:
- The most recent `trace.json` (from runtime map)
- A `spectrogram.png` image (your rendered plot)
- An `annotations.txt` file (e.g. manual tags or events)

Then:
- Creates a timestamped folder inside `exports/`
- Copies all those files into it with clean names:
  - `trace.json`
  - `spectrogram.png`
  - `annotations.txt`
- Confirms export with terminal feedback

---

## 📦 Output Example

```
exports/session_20251004_154321/
├── trace.json
├── spectrogram.png
└── annotations.txt
```

---

## 🧪 How to Use

```bash
python dev_tools/export_wizards_09/exp_wizards_09.py
```

You'll be prompted to paste paths for:
1. Trace file (JSON)
2. Spectrogram image (PNG)
3. Annotations file (TXT)

---

## 🧰 Uses

- Attach bundles to bug reports
- Save processing snapshots
- Share reproducible experiments

This ensures results are cleanly archived in one consistent place.
