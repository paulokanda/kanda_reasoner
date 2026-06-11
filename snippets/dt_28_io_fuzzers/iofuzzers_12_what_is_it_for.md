# 🧪 What is `iofuzzers_12.py` for?

This script helps **fuzz test your EDF/BDF file loaders** to ensure they can gracefully handle malformed or corrupted files.

---

## ✅ What It Does

- Generates small `.edf` files with:
  - Corrupted bytes,
  - Randomized headers,
  - Unexpected values or lengths.
- Useful to catch:
  - Crash bugs in your loader,
  - Uncaught decoding errors,
  - Shape mismatches or unhandled I/O exceptions.

---

## 📂 Output

Creates 5 small corrupted `.edf` files under:

```
dev_tools/io_fuzzers_12/fuzzed_edf_samples/
```

---

## 🧪 How to Use

1. Run the script:

```bash
python dev_tools/io_fuzzers_12/iofuzzers_12.py
```

2. Then, point your loader (e.g., `load_edf()`) at the generated files and confirm:
   - Exceptions are handled cleanly.
   - No crashes or silent misreads.
   - Proper validation or error reporting.

---

## 🧠 Why It’s Useful

I/O fuzzing is a proven way to bulletproof your EEG loader code, especially for edge-case patient files or exported data from legacy systems.