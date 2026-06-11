# 🛡️ What is `llm_sastassist_16.py` for?

This script enhances static analysis security tools like **Bandit** with the help of a local LLM. It adds intelligence to your SAST (Static Application Security Testing) process.

## ✅ What It Does
- Runs Bandit (`bandit -r .`) to scan your Python codebase.
- Sends the raw report to your LLM API.
- Gets back a clean **summary of real risks**, false positives, and **one-liner fixes**.
- Groups results by **file/module** and writes it to a Markdown report.

## 📦 Output
A file: `dev_tools/llm_sast_assist_16/last_sast_report.md` — ready to review or share in your PRs or security audits.

## 💡 Use Case
Run this before commits or periodically to catch:
- Dangerous `eval()` or subprocess usage
- Hardcoded secrets
- Insecure file access or deserialization

## 🧪 How to Run
Make sure Bandit is installed:

```bash
pip install bandit
```

Then run:

```bash
python dev_tools/llm_sast_assist_16/llm_sastassist_16.py
```

Ensure your local AI API (`text-generation-webui`) is running with OpenAI-compatible API enabled on port `5000`.

## 🔧 Customize
You can adapt it to work with other tools like:
- `ruff` (linter)
- `mypy` (type checker)
- `semgrep` (deep code patterns)

Use the same pattern: tool → LLM → Markdown insight.
