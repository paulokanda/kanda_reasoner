# 🧠 What is `signal_qassistant_23.py` for?

This script is a lightweight **Signal QA Assistant** that scores a short EEG signal segment (1D NumPy array) for basic **viewability** and offers advice for improving it. You can run it on extracted windows, spectrogram frames, or real-time previews.

---

## ✅ What It Does

- Computes simple EEG quality heuristics:
  - **SNR** (signal-to-noise ratio)
  - **Zero-crossing complexity**
  - **Signal power**
- Combines them into a normalized viewability `score` (0–1)
- Returns suggestions like:
  - Apply bandpass filter
  - Check gain/electrode flatness
  - Use notch filter or rescaling

---

## 🧪 Example Usage

```python
from signal_qassistant_23 import score_viewability
score = score_viewability(eeg_segment)
print(score["score"], score["advice"])
```

---

## 📁 Output (example):

```json
{
  "score": 0.78,
  "snr": 0.91,
  "complexity": 0.0546,
  "power": 4220.3,
  "advice": ["Try bandpass filtering (e.g., 1–40 Hz)."]
}
```

---

## 🧩 When to Use

Use it after preprocessing steps or on short EEG windows to guide:
- Visual QC
- Overlay coloring
- Pre-export filtering

It’s ideal for quick feedback when exploring EDF files.
