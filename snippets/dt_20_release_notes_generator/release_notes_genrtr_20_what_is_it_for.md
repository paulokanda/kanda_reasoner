# 📄 What is `release_notes_genrtr_20.py` for?

This script automates the generation of clean, developer- and user-friendly **release notes** based on your Git commit history.

---

## ✅ What It Does

- Runs `git log` with a consistent format.
- Sends the commit history to your local LLM via OpenAI-compatible API.
- Prompts the model to:
  - Extract **highlights** and **new features**
  - Flag any **breaking changes**
  - Suggest **migration steps** if needed
- Saves the result as `release_notes.md`.

---

## 🧪 How to Use

1. Make sure your local model is running at `http://127.0.0.1:5000`.
2. Ensure you have recent commits.
3. Run the script:

```bash
python dev_tools/release_notes_generator_20/release_notes_genrtr_20.py
```

---

## 📂 Output

Creates a file:

```
dev_tools/release_notes_generator_20/release_notes.md
```

Great for:
- Release packaging
- Internal changelogs
- Developer summaries
