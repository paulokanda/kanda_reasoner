# 🧠 What is `json_adviceout_13.py` for?

This tool reads small JSON logs (such as traces, diffs, crash reports) and sends them to your local AI model (via OpenAI-compatible API) to get a human-readable summary and next-step recommendations.

---

## ✅ Use Cases

- Explain profiling output (`runtime_map.json`)
- Analyze failed test snapshots
- Review diffs or symbol maps
- Summarize runtime logs

---

## 🧪 How It Works

1. You pass in a path to a `.json` file with developer-relevant structure.
2. The script loads the JSON and sends it to your local LLM.
3. The LLM replies with:
   - Summary of what the JSON shows
   - Concrete next steps for testing, cleanup, or debugging

---

## ▶️ Example Usage

```bash
python dev_tools/json_in_advice_out_13/json_adviceout_13.py .runmap/last.json
```

Make sure your LLM API is available at:

```
http://127.0.0.1:5000/v1/chat/completions
```

---

## 🛠️ Integration Ideas

- Run automatically after `run_with_trace.py`
- Hook into pytest post-failure
- Convert diffs into JSON and analyze change impact
