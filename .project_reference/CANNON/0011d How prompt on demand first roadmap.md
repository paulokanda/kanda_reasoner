# Option 3 — CLI Prompt Dispatcher
## Numbered Implementation Roadmap

---

## PHASE 1 — Folder and file structure

1.1  Create root folder: `prompt_dispatcher/`

1.2  Create subfolders:
```
prompt_dispatcher/
├── prompts/
│   ├── core/
│   ├── patch/
│   ├── architecture/
│   ├── validation/
│   └── session/
├── dispatched/
├── logs/
├── tests/
├── dispatcher_config.json
├── prompt_index.json
├── dispatch.py
├── resolver.py
├── composer.py
├── matcher.py
├── api_sender.py
└── README.md
```

1.3  Place every existing prompt .md file into correct subfolder:
- Morning / general rules           → prompts/core/
- Master session + engineering      → prompts/core/
- Patch rules                       → prompts/patch/
- Code rules                        → prompts/patch/
- Architecture rules                → prompts/architecture/
- Validation chain                  → prompts/validation/
- Freeze protocol                   → prompts/validation/
- Handoff format                    → prompts/session/
- Partnership metrics               → prompts/session/

1.4  Add this metadata block to the TOP of every prompt .md file:
```
---
id: master_session
name: Master Session Protocol
phase: core
trigger_keywords: [session-start, new-session, start]
depends_on: []
description: Loads full AI+Human engineering protocol
version: 2.0
---
```

1.5  Fill metadata for every prompt using this id convention:
```
core/           → master_session, morning_rules
patch/          → patch_rules, code_rules
architecture/   → architecture_rules
validation/     → validation_chain, freeze_protocol
session/        → handoff_format, partnership_metrics
```

---

## PHASE 2 — prompt_index.json

2.1  Create `prompt_index.json` at root of prompt_dispatcher/:
```json
{
  "prompts": {
    "master_session": {
      "file": "prompts/core/master_session.md",
      "phase": "core",
      "triggers": ["session-start", "new-session", "start"],
      "depends_on": [],
      "description": "Full AI+Human engineering protocol"
    },
    "patch_rules": {
      "file": "prompts/patch/patch_rules.md",
      "phase": "patch",
      "triggers": ["new-patch", "patch", "implement"],
      "depends_on": ["master_session"],
      "description": "Surgical patch delivery rules"
    },
    "code_rules": {
      "file": "prompts/patch/code_rules.md",
      "phase": "patch",
      "triggers": ["new-patch", "implement"],
      "depends_on": ["master_session", "patch_rules"],
      "description": "Coding standards and conventions"
    },
    "architecture_rules": {
      "file": "prompts/architecture/architecture_rules.md",
      "phase": "architecture",
      "triggers": ["architecture-check", "arch", "review"],
      "depends_on": ["master_session"],
      "description": "Layer rules, ownership, boundary contracts"
    },
    "validation_chain": {
      "file": "prompts/validation/validation_chain.md",
      "phase": "validation",
      "triggers": ["validate", "validation", "freeze-review"],
      "depends_on": ["master_session"],
      "description": "Full 5-step validation chain"
    },
    "freeze_protocol": {
      "file": "prompts/validation/freeze_protocol.md",
      "phase": "validation",
      "triggers": ["freeze-review", "freeze"],
      "depends_on": ["master_session", "validation_chain"],
      "description": "9-gate freeze governance"
    },
    "handoff_format": {
      "file": "prompts/session/handoff_format.md",
      "phase": "session",
      "triggers": ["end-session", "handoff"],
      "depends_on": ["master_session"],
      "description": "Session end handoff document format"
    },
    "partnership_metrics": {
      "file": "prompts/session/partnership_metrics.md",
      "phase": "session",
      "triggers": ["metrics", "health-check"],
      "depends_on": ["master_session"],
      "description": "Partnership health scorecard"
    }
  },
  "contexts": {
    "session-start":       ["master_session", "morning_rules", "handoff_format"],
    "new-patch":           ["master_session", "patch_rules", "code_rules"],
    "architecture-check":  ["master_session", "architecture_rules"],
    "freeze-review":       ["master_session", "validation_chain", "freeze_protocol"],
    "end-session":         ["master_session", "handoff_format", "partnership_metrics"],
    "full":                ["master_session", "patch_rules", "code_rules",
                            "architecture_rules", "validation_chain",
                            "freeze_protocol", "handoff_format"]
  }
}
```

---

## PHASE 3 — dispatcher_config.json

3.1  Create `dispatcher_config.json`:
```json
{
  "projects": {
    "kanda": {
      "name": "Kanda Reasoner",
      "root": "E:\\developer_tools\\kanda_reasoner",
      "stack": "Python 3.11 / PySide6",
      "persona": "PyArchitect",
      "validation_cmds": [
        "python -m py_compile {file}",
        "python -m pytest tests/focused/ -v",
        "python -m pytest tests/regression/ -v",
        "python workflow_validator.py",
        "python architecture_validator.py"
      ]
    },
    "eeg": {
      "name": "EEG Kernel AI",
      "root": "E:\\eeg_kernel_ai_neural_data_analysis",
      "stack": "Python 3.11 / PySide6 / MNE",
      "persona": "PyArchitect v11.0",
      "validation_cmds": [
        "python -m py_compile {file}",
        "python -m pytest tests/focused/ -v",
        "python -m pytest tests/regression/ -v",
        "python pyarchitect_workflow.py --validate",
        "python pyarchitect_architecture.py --validate"
      ]
    }
  },
  "default_project": "kanda",
  "default_output": "clipboard",
  "prompt_library_path": "prompts/",
  "index_file": "prompt_index.json",
  "dispatched_dir": "dispatched/",
  "log_file": "logs/dispatch_audit.jsonl"
}
```

---

## PHASE 4 — resolver.py

4.1  Create `resolver.py`:
```python
# resolver.py
# Reads prompt_index.json, resolves dependency order, detects cycles.

import json
from pathlib import Path


def load_index(index_path: str) -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(prompt_ids: list[str], index: dict) -> list[str]:
    """
    Topological sort of prompt_ids respecting depends_on.
    Returns ordered list with no duplicates.
    Raises ValueError on circular dependency.
    """
    prompts = index["prompts"]
    visited = set()
    order = []

    def visit(pid: str, stack: set):
        if pid in stack:
            raise ValueError(f"Circular dependency detected: {pid}")
        if pid in visited:
            return
        stack.add(pid)
        for dep in prompts.get(pid, {}).get("depends_on", []):
            visit(dep, stack)
        stack.discard(pid)
        visited.add(pid)
        order.append(pid)

    for pid in prompt_ids:
        visit(pid, set())

    return order
```

---

## PHASE 5 — composer.py

5.1  Create `composer.py`:
```python
# composer.py
# Reads ordered prompt file list, strips metadata headers,
# injects project variables, returns composed string.

import re
from pathlib import Path


HEADER_PATTERN = re.compile(r"^---\n.*?^---\n", re.DOTALL | re.MULTILINE)
SEPARATOR = "\n\n---SECTION---\n\n"


def strip_header(content: str) -> str:
    return HEADER_PATTERN.sub("", content, count=1).strip()


def inject_variables(content: str, project: dict) -> str:
    replacements = {
        "[PROJECT NAME]":  project["name"],
        "[PROJECT ROOT]":  project["root"],
        "[LANGUAGE/STACK]": project["stack"],
        "[AI PERSONA NAME]": project["persona"],
    }
    for cmd_index, cmd in enumerate(project.get("validation_cmds", []), 1):
        replacements[f"[VALIDATION CMD {cmd_index}]"] = cmd

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def compose(ordered_ids: list[str], index: dict,
            project: dict, library_root: str) -> str:
    parts = []
    for pid in ordered_ids:
        file_path = Path(library_root) / index["prompts"][pid]["file"]
        raw = file_path.read_text(encoding="utf-8")
        clean = strip_header(raw)
        injected = inject_variables(clean, project)
        parts.append(f"# PROMPT: {pid}\n\n{injected}")
    return SEPARATOR.join(parts)
```

---

## PHASE 6 — matcher.py

6.1  Create `matcher.py`:
```python
# matcher.py
# Maps a keyword string to a list of prompt IDs.
# Supports exact context match, partial match, and fuzzy suggestion.

import difflib


def match(keyword: str, index: dict) -> list[str]:
    contexts = index["contexts"]

    # 1. Exact context match
    if keyword in contexts:
        return contexts[keyword]

    # 2. Partial match — keyword is substring of a context name
    partial = [k for k in contexts if keyword in k]
    if len(partial) == 1:
        return contexts[partial[0]]
    if len(partial) > 1:
        raise ValueError(
            f"Ambiguous keyword '{keyword}'. Matches: {partial}\n"
            f"Be more specific."
        )

    # 3. Trigger keyword match — search individual prompt triggers
    matched_ids = []
    for pid, meta in index["prompts"].items():
        if keyword in meta.get("triggers", []):
            if pid not in matched_ids:
                matched_ids.append(pid)
    if matched_ids:
        return matched_ids

    # 4. Fuzzy suggestion — nothing matched
    all_keys = list(contexts.keys())
    suggestions = difflib.get_close_matches(keyword, all_keys, n=3, cutoff=0.4)
    msg = f"Unknown keyword: '{keyword}'."
    if suggestions:
        msg += f"\nDid you mean: {suggestions}"
    else:
        msg += f"\nAvailable contexts: {all_keys}"
    raise ValueError(msg)
```

---

## PHASE 7 — dispatch.py (main entry point)

7.1  Create `dispatch.py`:
```python
# dispatch.py
# Main CLI entry point.
# Usage:
#   python dispatch.py session-start
#   python dispatch.py new-patch --project eeg --out file
#   python dispatch.py --interactive
#   python dispatch.py --list
#   python dispatch.py --report

import argparse
import json
import sys
import datetime
from pathlib import Path

from resolver import resolve, load_index
from composer import compose
from matcher  import match


CONFIG_FILE = "dispatcher_config.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_project(config: dict, project_key: str) -> dict:
    projects = config["projects"]
    if project_key not in projects:
        raise ValueError(f"Unknown project '{project_key}'. "
                         f"Available: {list(projects.keys())}")
    return projects[project_key]


def output_clipboard(text: str):
    try:
        import pyperclip
        pyperclip.copy(text)
        print("✓ Composed prompt copied to clipboard. Paste into your AI session.")
    except ImportError:
        print("pyperclip not installed. Run: pip install pyperclip")
        print("\n--- COMPOSED PROMPT ---\n")
        print(text)


def output_file(text: str, keyword: str, dispatched_dir: str) -> Path:
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{ts}_{keyword.replace('-','_')}.md"
    out_path = Path(dispatched_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"✓ Composed prompt written to: {out_path}")
    return out_path


def output_api(text: str, project: dict):
    # Requires: pip install anthropic
    try:
        import anthropic
        client = anthropic.Anthropic()
        print(f"Sending to claude-sonnet-4-20250514 as [{project['persona']}]...\n")
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=text,
            messages=[{"role": "user",
                        "content": "Confirm protocol loaded and state ready."}]
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
        print()
    except ImportError:
        print("anthropic not installed. Run: pip install anthropic")


def write_audit(keyword: str, resolved_ids: list,
                output_mode: str, project_name: str,
                token_estimate: int, log_file: str):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "keyword": keyword,
        "resolved_ids": resolved_ids,
        "output_mode": output_mode,
        "project": project_name,
        "token_estimate": token_estimate
    }
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def interactive_menu(index: dict) -> str:
    contexts = list(index["contexts"].keys())
    print("\nAvailable contexts:")
    for i, ctx in enumerate(contexts, 1):
        prompts = index["contexts"][ctx]
        print(f"  {i:2}. {ctx:<25} → {prompts}")
    choice = input("\nEnter number or keyword: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(contexts):
            return contexts[idx]
    return choice


def print_report(log_file: str):
    log_path = Path(log_file)
    if not log_path.exists():
        print("No dispatch log found yet.")
        return
    entries = [json.loads(l) for l in log_path.read_text().splitlines() if l.strip()]
    from collections import Counter
    counts = Counter(e["keyword"] for e in entries)
    print("\n--- DISPATCH USAGE REPORT ---")
    for keyword, count in counts.most_common():
        print(f"  {keyword:<30} {count} dispatches")
    print(f"\nTotal dispatch events: {len(entries)}")


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Dispatcher — load the right prompt stack for any AI session"
    )
    parser.add_argument("keyword", nargs="?",
                        help="Context keyword: session-start, new-patch, architecture-check...")
    parser.add_argument("--project", "-p", default=None,
                        help="Project key from dispatcher_config.json")
    parser.add_argument("--out", "-o",
                        choices=["clipboard", "file", "api", "print"],
                        default=None,
                        help="Output mode (default: from config)")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Show interactive context menu")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all available contexts and prompts")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Show dispatch usage report")

    args = parser.parse_args()

    config  = load_config()
    index   = load_index(config["index_file"])
    project_key = args.project or config["default_project"]
    project = get_project(config, project_key)
    out_mode = args.out or config["default_output"]

    # --list
    if args.list:
        print("\nAvailable contexts:")
        for ctx, ids in index["contexts"].items():
            print(f"  {ctx:<25} → {ids}")
        print("\nAll prompts:")
        for pid, meta in index["prompts"].items():
            print(f"  {pid:<30} triggers={meta['triggers']}")
        return

    # --report
    if args.report:
        print_report(config["log_file"])
        return

    # resolve keyword
    keyword = args.keyword
    if args.interactive or not keyword:
        keyword = interactive_menu(index)

    # match → resolve → compose
    matched_ids  = match(keyword, index)
    resolved_ids = resolve(matched_ids, index)
    composed     = compose(resolved_ids, index, project, ".")

    token_estimate = len(composed) // 4  # rough estimate

    # audit
    write_audit(keyword, resolved_ids, out_mode,
                project["name"], token_estimate, config["log_file"])

    # output
    print(f"\nContext : {keyword}")
    print(f"Prompts : {resolved_ids}")
    print(f"Project : {project['name']}")
    print(f"Tokens  : ~{token_estimate}")
    print(f"Output  : {out_mode}\n")

    if out_mode == "clipboard":
        output_clipboard(composed)
    elif out_mode == "file":
        output_file(composed, keyword, config["dispatched_dir"])
    elif out_mode == "api":
        output_api(composed, project)
    elif out_mode == "print":
        print(composed)


if __name__ == "__main__":
    main()
```

---

## PHASE 8 — tests/test_dispatcher.py

8.1  Create `tests/test_dispatcher.py`:
```python
import pytest
import json
import sys
sys.path.insert(0, "..")

from resolver import load_index, resolve
from matcher  import match
from composer import strip_header, inject_variables


INDEX = {
    "prompts": {
        "master_session": {"file": "x.md", "triggers": ["start"],
                           "depends_on": []},
        "patch_rules":    {"file": "y.md", "triggers": ["new-patch"],
                           "depends_on": ["master_session"]},
        "code_rules":     {"file": "z.md", "triggers": ["new-patch"],
                           "depends_on": ["master_session", "patch_rules"]},
    },
    "contexts": {
        "new-patch": ["patch_rules", "code_rules"],
        "session-start": ["master_session"],
    }
}


def test_exact_context_match():
    ids = match("new-patch", INDEX)
    assert "patch_rules" in ids


def test_partial_match():
    ids = match("patch", INDEX)
    assert "patch_rules" in ids


def test_unknown_keyword_raises():
    with pytest.raises(ValueError, match="Unknown keyword"):
        match("xyzzy", INDEX)


def test_dependency_order():
    ids = resolve(["code_rules"], INDEX)
    assert ids.index("master_session") < ids.index("patch_rules")
    assert ids.index("patch_rules") < ids.index("code_rules")


def test_no_duplicates():
    ids = resolve(["patch_rules", "code_rules"], INDEX)
    assert len(ids) == len(set(ids))


def test_cycle_detection():
    cyclic = {
        "prompts": {
            "a": {"file": "a.md", "depends_on": ["b"]},
            "b": {"file": "b.md", "depends_on": ["a"]},
        },
        "contexts": {}
    }
    with pytest.raises(ValueError, match="Circular"):
        resolve(["a"], cyclic)


def test_strip_header():
    raw = "---\nid: test\n---\nActual content here"
    assert strip_header(raw) == "Actual content here"


def test_inject_variables():
    content = "Project: [PROJECT NAME] on [LANGUAGE/STACK]"
    project = {"name": "MyApp", "stack": "Python 3.11",
                "root": "/app", "persona": "PyArch",
                "validation_cmds": []}
    result = inject_variables(content, project)
    assert "MyApp" in result
    assert "Python 3.11" in result
    assert "[PROJECT NAME]" not in result
```

---

## PHASE 9 — install dependencies and run

9.1  Create `requirements.txt`:
```
pyperclip>=1.8
anthropic>=0.25
pytest>=8.0
```

9.2  Install:
```bash
pip install -r requirements.txt
```

9.3  Run tests:
```bash
cd prompt_dispatcher
pytest tests/test_dispatcher.py -v
```

9.4  Run dispatcher:
```bash
# list all contexts
python dispatch.py --list

# interactive menu
python dispatch.py --interactive

# load session-start stack → clipboard
python dispatch.py session-start

# load new-patch stack for eeg project → file
python dispatch.py new-patch --project eeg --out file

# usage report
python dispatch.py --report
```

---

## PHASE 10 — self-hosting smoke test (freeze gate)

10.1  Run: `python dispatch.py session-start --out clipboard`
10.2  Open a new Claude session
10.3  Paste clipboard content
10.4  Confirm AI responds with `PROTOCOL LOADED` block
10.5  If confirmed → dispatcher is working correctly
10.6  Apply 9-gate freeze checklist to dispatcher itself
10.7  Human issues freeze command: `freeze prompt_dispatcher_v1`
10.8  Write session handoff doc for the dispatcher build session

---

## COMPLETE FILE LIST AT FREEZE

```
prompt_dispatcher/
├── dispatch.py                   ← main entry point
├── resolver.py                   ← dependency graph resolver
├── composer.py                   ← prompt file composer
├── matcher.py                    ← keyword → prompt ID matcher
├── prompt_index.json             ← routing table
├── dispatcher_config.json        ← per-project config
├── requirements.txt
├── README.md
├── prompts/
│   ├── core/
│   │   ├── master_session.md
│   │   └── morning_rules.md
│   ├── patch/
│   │   ├── patch_rules.md
│   │   └── code_rules.md
│   ├── architecture/
│   │   └── architecture_rules.md
│   ├── validation/
│   │   ├── validation_chain.md
│   │   └── freeze_protocol.md
│   └── session/
│       ├── handoff_format.md
│       └── partnership_metrics.md
├── dispatched/                   ← auto-generated per session
├── logs/
│   └── dispatch_audit.jsonl      ← auto-generated
└── tests/
    └── test_dispatcher.py
```
Updated Roadmap for Option 3 (CLI Prompt Dispatcher) – v2.0

The original roadmap is solid but missing several determinants that can be added without changing the core architecture. Below is the updated roadmap with additions marked [NEW].
PHASE 1 – Folder and file structure (unchanged)
PHASE 2 – prompt_index.json (unchanged)

Add freshness metadata to each prompt (already in Phase 1.4 – ensure last_validated_with_patch is present).
PHASE 3 – dispatcher_config.json

Add two new fields:
json

{
  "projects": { ... },
  "default_project": "...",
  "default_output": "clipboard",
  "prompt_library_path": "prompts/",
  "index_file": "prompt_index.json",
  "dispatched_dir": "dispatched/",
  "log_file": "logs/dispatch_audit.jsonl",
  "metrics_file": "logs/partnership_metrics.jsonl",   // [NEW]
  "evidence_required": true                            // [NEW]
}

PHASE 4 – resolver.py (unchanged)
PHASE 5 – composer.py

Add freshness check (new function and call):
python

# Add to composer.py

def check_freshness(prompt_id: str, prompt_meta: dict, project_root: str) -> list[str]:
    """Returns list of warnings if prompt is stale relative to project state."""
    warnings = []
    last_validated = prompt_meta.get("last_validated_with_patch", "")
    if not last_validated:
        warnings.append(f"Prompt {prompt_id} has no validation record.")
    else:
        # Simple heuristic: check if any source file in project root is newer than last_validated
        # (implement as needed – for now, placeholder warning)
        warnings.append(f"Prompt {prompt_id} last validated with {last_validated}. Consider re-validating.")
    return warnings

def compose(ordered_ids, index, project, library_root):
    parts = []
    all_warnings = []
    for pid in ordered_ids:
        meta = index["prompts"][pid]
        file_path = Path(library_root) / meta["file"]
        raw = file_path.read_text(encoding="utf-8")
        clean = strip_header(raw)
        injected = inject_variables(clean, project)
        parts.append(f"# PROMPT: {pid}\n\n{injected}")
        # freshness check
        warnings = check_freshness(pid, meta, project["root"])
        all_warnings.extend(warnings)
    if all_warnings:
        warning_block = "\n".join(f"WARNING: {w}" for w in all_warnings)
        parts.insert(0, f"# PROMPT FRESHNESS WARNINGS\n{warning_block}\n\n")
    return SEPARATOR.join(parts)

PHASE 6 – matcher.py (unchanged)
PHASE 7 – dispatch.py (main)

Add three new subcommands:

    dispatch --freeze-check – run the 9‑gate checklist for the dispatcher itself.

    dispatch --audit-summary – human‑readable summary of recent injections.

    dispatch handoff – generate a handoff document from the last session’s logs.

Add freeze-check command (new function):
python

def freeze_check(project_name: str, project: dict):
    """Run the 9‑gate freeze checklist against the dispatcher's own code."""
    gates = [
        ("1. All validation steps pass", "Run `pytest tests/ -v`"),
        ("2. No outstanding review comments", "Check open issues in repo"),
        ("3. Evidence log is complete", f"Check {config['log_file']} exists and has entries"),
        ("4. Architecture constraints verified", "Run `python -m architecture_validator` if exists"),
        ("5. Performance impact assessed", "Manual review"),
        ("6. Security / input validation reviewed", "Check CLI args and file reads"),
        ("7. Handoff document generated", "Run `dispatch handoff --last-session`"),
        ("8. Partnership health metrics updated", "Run `dispatch --metrics`"),
        ("9. Human issues explicit freeze command", "Type `freeze prompt_dispatcher_vX`")
    ]
    print("\n--- FREEZE GATE CHECKLIST ---")
    for gate, action in gates:
        print(f"{gate:<45} → {action}")

Add audit‑summary:
python

def audit_summary(log_file: str):
    from collections import Counter
    import json
    log_path = Path(log_file)
    if not log_path.exists():
        print("No audit log found.")
        return
    entries = [json.loads(l) for l in log_path.read_text().splitlines() if l.strip()]
    print(f"\n--- ORCHESTRATOR AUDIT SUMMARY (last {len(entries)} dispatches) ---")
    keyword_counts = Counter(e["keyword"] for e in entries[-50:])
    print("Recent keyword usage:")
    for kw, cnt in keyword_counts.most_common(10):
        print(f"  {kw}: {cnt}")
    # routing accuracy placeholder – requires human feedback integration
    print("\nRouting accuracy: not yet measured. Add `!/correct` / `!/wrong` to session logs.")

Add handoff generation:
python

def generate_handoff(project: dict, last_log: str = None):
    """Generate a handoff document from the most recent terminal log."""
    # For v1, produce a template handoff
    handoff = f"""# SESSION HANDOFF
Project: {project['name']}
Date: {datetime.datetime.now().isoformat()}

## Current State
(Load the last terminal log to fill this)

## Open Questions
(To be answered next session)

## Next Patch Candidates
(List from recent dispatch usage)

## Evidence Freshness
(Check timestamps of key source files)

## Partnership Metrics
Run `dispatch --metrics` to compute.
"""
    print(handoff)
    return handoff

Modify the argument parser to include:
python

parser.add_argument("--freeze-check", action="store_true", help="Run 9‑gate freeze checklist")
parser.add_argument("--audit-summary", action="store_true", help="Show recent dispatch audit")
parser.add_argument("--metrics", action="store_true", help="Show partnership health metrics")

Add metrics command (simplified v1):
python

def show_metrics(project: dict, log_file: str, dispatched_dir: str):
    """Compute basic partnership health metrics."""
    import os
    # Count patches created
    patch_files = list(Path(dispatched_dir).glob("*.md"))
    total_patches = len(patch_files)
    # Estimate success rate from audit log (requires manual flag)
    print(f"\n--- PARTNERSHIP METRICS for {project['name']} ---")
    print(f"Total dispatched prompt stacks: {total_patches}")
    print("Validation pass rate: (requires integration with test runner)")
    print("Freeze success rate: (requires freeze commands in logs)")
    print("\nNext step: Add `!/pass` / `!/fail` to session logs to track quality.")

PHASE 8 – tests/test_dispatcher.py

Add tests for freshness check and freeze‑check output (no major change).
PHASE 9 – install dependencies (unchanged)
PHASE 10 – self‑hosting smoke test (unchanged)

Add freeze command for the dispatcher itself (new Phase 11):
bash

# After building and testing:
python dispatch.py --freeze-check
# Human confirms each gate, then:
freeze prompt_dispatcher_v2.0
python dispatch.py handoff > handoff_prompt_dispatcher_v2.md

Summary of Updates to Original Roadmap
Original Phase	Added / Modified	Determinant Covered
Phase 3	Added metrics_file, evidence_required	Orchestrator auditability, evidence‑first
Phase 5	Freshness check in composer.py	Prompt freshness & versioning
Phase 7	New subcommands: --freeze-check, --audit-summary, handoff, --metrics	Freeze gate, auditability, handoff, health metrics
Phase 11 (new)	Freeze the dispatcher itself using its own checklist	Full 9‑gate governance

The updated roadmap respects the master framework without overcomplicating Option 3. The CLI dispatcher remains buildable in a few focused sessions, and it now produces the evidence and metrics needed to later build Options 5 and 6.
Next Step for You

    Review the updated roadmap above.

    Decide if you want me to produce the actual code files for the changed modules (composer.py, dispatch.py with new subcommands) – I can write them now.

    Or, proceed to build the dispatcher as per the updated roadmap, using your partnership method (AI writes surgical patches, you test and freeze).