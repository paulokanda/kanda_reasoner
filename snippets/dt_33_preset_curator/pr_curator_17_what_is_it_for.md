# 🧠 What is `pr_curator_17.py` for?

This script analyzes recent user interactions in your EEG app GUI and asks your local LLM to suggest **presets** the user might want to save. These presets can include things like:

- Montage + filter + FFT combinations
- Colormap + gain + notch filter combinations
- Any repeated or useful GUI configurations

---

## ✅ What It Does

- Loads a `last_actions.json` file (log of recent UI settings).
- Sends this to the LLM (via local OpenAI-compatible API).
- Saves the output as a human-readable markdown file with suggested named presets.

---

## 📁 Input Format

A JSON file like:

```json
{
  "fft_window": "hann",
  "bandpass": [1, 40],
  "gain": 0.003,
  "colormap": "magma"
}
```

---

## 🚀 How to Run

Make sure your local AI endpoint is active (WizardCoder, etc.), then:

```bash
python dev_tools/preset_curator_17/pr_curator_17.py
```

---

## 📄 Output

Markdown suggestions saved to:

```
dev_tools/preset_curator_17/preset_suggestions.md
```

---

## 💡 Use Case

Helpful in surfacing reusable analysis/viewing configs across studies — especially useful when your users follow consistent workflows but forget to save presets manually.
