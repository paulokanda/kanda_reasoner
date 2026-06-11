# 🧪 What is `syntheticeeg_cases_24.py` for?

This tool generates small, synthetic EEG-like signal snippets to simulate common edge cases during testing and UI development.

## ✅ What It Generates

- **Eye Blink**: Simulated as a sharp Gaussian pulse in the middle of the timeline.
- **Line Noise**: A continuous 60Hz sinusoid to simulate power line interference.
- **Electrode Drop**: A flatline halfway through to simulate electrode failure.

## 📁 Output

- `.npy` files saved into: `dev_tools/synthetic_eeg_cases_24/generated_cases/`
- Each file contains a NumPy array representing a synthetic EEG segment.

## 🧪 How to Use

1. Run the script:

```bash
python dev_tools/synthetic_eeg_cases_24/syntheticeeg_cases_24.py
```

2. Load the `.npy` files in your viewer or tests.

## 🤖 Why Useful?

These cases allow you to:

- Test signal overlay logic (e.g. blink highlighting).
- Validate line noise removal filters.
- Harden plotting or auto-scaling logic against flatline data.

