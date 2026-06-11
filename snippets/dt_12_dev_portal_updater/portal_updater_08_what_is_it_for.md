# dev_tools/dev_portal_updater_08/portal_updater_08_what_is_it_for.md

# 🧭 What is `portal_updater_08.py` for?

This script helps auto-generate and update a **Developer Portal page** for your project. It leverages your local LLM (via the OpenAI-compatible API) to read your code structure and produce a Markdown report with the following:

### ✅ What It Does
- Runs `format_my_pys.py --dry-run` to get the structure and organization of your Python modules.
- Feeds that output to the LLM, asking for:
  - 🗂️ Module Overview
  - ⚠️ Known Sharp Edges
  - 👨‍🔧 Owners or Responsibilities
  - ✅ Refactor Suggestions
- Saves the response into `dev_tools/dev_portal_updater_08/dev_portal_report.md`.

### 🧪 How to Run
1. Make sure your local AI endpoint is running (WizardCoder via `text-generation-webui`, with `/v1/chat/completions` enabled).
2. Run the script:

```bash
python dev_tools/dev_portal_updater_08/portal_updater_08.py
```

### 🔄 Recommended Integrations

#### ⏰ Nightly Automation (Windows)
Use Task Scheduler to run the script daily. Set:
- Program: `E:\mne_py3.10\python.exe`
- Arguments: `dev_tools/dev_portal_updater_08/portal_updater_08.py`
- Start in: `E:\EEG_KANDA`

#### 🪝 Git Hook (Post-Commit)
Add this to `.git/hooks/post-commit`:

```bash
#!/bin/sh
E:/mne_py3.10/python.exe dev_tools/dev_portal_updater_08/portal_updater_08.py
```

Then make it executable.

---

### 📂 Output
The report is saved to:

```
dev_tools/dev_portal_updater_08/dev_portal_report.md
```

It includes AI-generated insights into code structure, sharp edges, and refactor suggestions.

✅ Purpose

This script generates a markdown report summarizing your Python project, using both:

format_my_pys.py to extract structure and organization from your code (without modifying it).

A local AI model (like DeepSeek or WizardCoder) to convert that structure into a developer-friendly Markdown document for your dev portal.

📦 Key Functional Roles
Section	Description
run_format_my_pys()	Runs the formatter tool in dry-run mode to get a text-based summary of all .py files — headers, class/function definitions, etc.
ask_llm(summary_text)	Sends the summary to your locally running AI (via HTTP POST to API_URL) and asks for a Markdown dev portal summary.
main()	Orchestrates the process: run formatter → send to LLM → write Markdown file.

🧠 What the AI is Prompted To Do

The AI is told:

“You're a documentation assistant. Based on the following summary, generate a Markdown dev portal entry with...”

With clear expected sections:

🗂️ Module Overview

⚠️ Known Sharp Edges

👨‍🔧 Responsibilities

✅ Refactor Suggestions

✅ Final Output

Produces a well-structured dev portal file like this:

# Dev Portal Overview

Generated: 2025-10-04 16:01:32

🗂️ Module Overview
- ...

⚠️ Known Sharp Edges
- ...

...
