# 🧠 What is `label_copilot_14.py` for?

This tool helps you **automatically suggest weak labels** (like `eye blink`, `seizure`, `movement artifact`) for EEG data windows using extracted statistical features and your local LLM.

---

## ✅ What It Does

- Reads a `.json` file containing extracted EEG features per window.
- Sends the features to your local LLM (WizardCoder) with instructions to:
  - Propose weak labels.
  - Justify the label using the feature data.
  - Suggest heuristic rules for automation.
- Saves the result into a `labeling_suggestions.md` file.

---

## 🧪 How to Run

1. Make sure your JSON has a list of per-window stats like:

```json
[
  {"window_id": 1, "band_power": [1.2, 3.4, 0.8], "kurtosis": 3.1, "line_noise": 0.05},
  {"window_id": 2, "band_power": [0.2, 5.0, 1.1], "kurtosis": 10.5, "line_noise": 0.20}
]
```

2. Run the script:

```bash
python dev_tools/labeling_copilot_14/label_copilot_14.py
```

3. Enter the path to your `.json` file relative to `EEG_KANDA/`.

4. Your output will be saved to:

```
dev_tools/labeling_copilot_14/labeling_suggestions.md
```

---

## 💡 Ideal Use Case

Perfect for offline EEG labeling pipelines, quality control, or preprocessing stages before manual review.
