import json
from pathlib import Path
from collections import Counter, defaultdict
import datetime

INPUT_FILE = Path(".runmap/last.json")
OUTPUT_FILE = Path("run_time_map_21/runtime_map_report.md")

def load_trace():
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(trace):
    file_counter = Counter()
    func_counter = Counter()
    file_func_map = defaultdict(list)

    for event in trace:
        if event["event"] == "call":
            file = event["file"]
            func = event["func"]
            file_counter[file] += 1
            func_counter[func] += 1
            file_func_map[file].append(func)

    md = "# 🧠 EEG Runtime Map Report\n\n"
    md += f"**Generated:** {datetime.datetime.now()}\n\n"

    md += "## 📂 Most Called Files\n"
    for k, v in file_counter.most_common(20):
        md += f"- `{k}` — **{v}** calls\n"

    md += "\n## 🔧 Most Called Functions\n"
    for k, v in func_counter.most_common(20):
        md += f"- `{k}` — **{v}** calls\n"

    return md

def main():
    if not INPUT_FILE.exists():
        print("❌ Trace file not found. Run your app with tracing first.")
        return

    trace = load_trace()
    md = generate_markdown(trace)
    OUTPUT_FILE.write_text(md, encoding="utf-8")
    print(f"✅ Markdown report written to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()