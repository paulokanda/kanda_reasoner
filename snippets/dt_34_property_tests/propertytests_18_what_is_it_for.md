# 🧪 What is `propertytests_18.py` for?

This script helps automatically **generate property-based tests** using the Hypothesis library by extracting function signatures and docstrings from any Python module in your EEG_KANDA project.

### ✅ What It Does
- Parses the specified `.py` file using `ast` to find functions and their arguments.
- Builds a prompt that asks your local LLM (like WizardCoder) to write meaningful `@given(...)` tests.
- Outputs the LLM-generated test functions directly in the console.

### 🔍 Why It’s Useful
Signal processing code often has invariants like:
- "Filter doesn’t change signal length"
- "Montage swap keeps data shape"
- "Output stays within expected value ranges"

These are **hard to test manually** but **ideal for property-based testing**.

### 🧪 How to Run

1. Start your local LLM with the OpenAI-compatible API.
2. Run the script from terminal:

```bash
python dev_tools/property_tests_18/propertytests_18.py
```

3. Enter the path to the target module (e.g., `k01_core_eeg/k01_3_eeg_filters/signal_utils.py`).
4. It will print a list of Hypothesis tests in the console.

### 📦 Requirements
- Local LLM running at `http://127.0.0.1:5000/v1/chat/completions`
- Python 3.10+
- A module in `EEG_KANDA` to analyze

You can copy and paste the generated tests into your test suite!
