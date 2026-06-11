# run_time_map/render_runtime_map.py

import json
from pathlib import Path
from collections import Counter, defaultdict
import datetime

INPUT_FILE = Path(".runmap/last.json")
OUTPUT_FILE = Path("run_time_map/runtime_map.md")

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

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = "# 🧠 EEG Runtime Map Report\n\n"
    md += f"**Generated:** {timestamp}\n\n"

    md += "## 📁 Most Called Files\n\n"
    md += "| File | Call Count |\n|------|------------|\n"
    for file, count in file_counter.most_common(20):
        md += f"| `{file}` | {count} |\n"

    md += "\n## 🧠 Most Called Functions\n\n"
    md += "| Function | Call Count |\n|----------|------------|\n"
    for func, count in func_counter.most_common(20):
        md += f"| `{func}` | {count} |\n"

    return md

def main():
    if not INPUT_FILE.exists():
        print("❌ Trace file not found. Run with_trace.py first.")
        return

    trace = load_trace()
    markdown = generate_markdown(trace)
    OUTPUT_FILE.write_text(markdown, encoding="utf-8")
    print(f"✅ Markdown written to {OUTPUT_FILE.resolve()}")
    print("📄 Open it in VS Code, PyCharm, or any Markdown viewer.")

if __name__ == "__main__":
    main()
