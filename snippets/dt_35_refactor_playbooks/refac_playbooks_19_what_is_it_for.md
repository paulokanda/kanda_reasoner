# 🛠️ What is `refac_playbooks_19.py` for?

This script helps you **refactor complex or messy Python code** by generating an LLM-powered playbook.

## ✅ What It Does

- Reads a target `.py` file.
- Sends the code to your local LLM (via OpenAI-compatible API).
- Receives a Markdown report with:
  - 🧩 Areas of concern
  - 🔧 Refactor strategy
  - 📦 Suggested module breakdown
  - ✅ Benefits of refactor
- Saves it to: `dev_tools/refactor_playbooks_19/refactor_plan.md`

---

## 🧪 How to Use

```bash
python dev_tools/refactor_playbooks_19/refac_playbooks_19.py path/to/your_script.py
```

Ensure your local LLM (e.g. WizardCoder) is running and available at:
```
http://127.0.0.1:5000/v1/chat/completions
```

---

## 🧠 Example Refactor Prompts Used

- “Split this 800-line widget”
- “Extract model-view separation”
- “Replace globals with dependency injection”
