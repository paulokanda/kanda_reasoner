# INSUFFICIENT_EVIDENCE — Complete Diagnosis and Correction Guide
## Project Reasoner v10 — Based on Real Session Fixes

---

## WHAT IS INSUFFICIENT_EVIDENCE?

`INSUFFICIENT_EVIDENCE` appears in two forms:

**Form A — Validator rejection (answer produced then erased):**
```
INSUFFICIENT_EVIDENCE

The local model produced content that does not appear to be fully grounded
in the supplied evidence pack. Rejected by rule: <rule_name>
```
The model produced a valid answer, but the grounding validator in
`v10_ai_bridge.py._grounding_failure_reason()` rejected it post-generation.

**Form B — Model self-report (model genuinely cannot answer):**
```
INSUFFICIENT_EVIDENCE: No explicit evidence for X was found in the provided
evidence pack.
```
The model correctly reports that the evidence pack sent to it does not contain
the requested information.

These two forms have completely different root causes and require different fixes.

---

## THE 5 VALIDATOR REJECTION RULES

`_grounding_failure_reason()` in `v10_ai_bridge.py` runs after every model answer.
It checks five rules in order. The first rule that fires causes rejection.

```
Rule                        Risk of false positive   Branch where it runs
──────────────────────────  ───────────────────────  ────────────────────
looks_ungrounded_*          LOW                      all branches
forbidden_ids               LOW                      all branches
forbidden_paths             CRITICAL                 default + deterministic
forbidden_symbols           CRITICAL                 all branches
ignored_required_snippets   MEDIUM                   generative only
```

The branch (`deterministic`, `generative`, `default`) is determined by
`_is_deterministic_prompt()` and `_is_generative_prompt()` — both in
`v10_ai_bridge.py`, both with **independent** classification logic that does
NOT know about the router's `route_query_intent()` decision.

---

## ROOT CAUSE MAP — Why each rule fires incorrectly

### forbidden_symbols (MOST COMMON — was causing ~90% of false rejections)

**What it checks:**
Extracts all dotted names from the answer (e.g. `QTimer.singleShot`,
`self.v.main_window.showMaximized`, `EEGMainWindowBuilder.build_and_show`)
and rejects any not in the `allowed_symbols` set.

**What allowed_symbols originally contained (too narrow):**
- Only `Symbol:` lines from SYMBOL EVIDENCE
- Only `anchor=` lines from SOURCE SNIPPETS

**Why it fired on valid answers:**
Real LLM answers naturally contain:
- `self.*` expressions (instance attribute access)
- `Qt.*` dotted names (`QTimer.singleShot`, `QPushButton.clicked`)
- `clicked.connect` (signal connection pattern)
- Module paths as dotted names (`mne.viz.plot_topomap`)
- `EEGMainWindowBuilder.build_and_show` — IS in allowed_symbols but was
  dead code due to indentation bug (see below)
- Dotted names from `Functions:` / `Calls out:` lines in file evidence detail

**The indentation bug:**
Steps 5 and 22 added new allowlist checks, but they were accidentally placed
INSIDE the `if symbol in snippet_dotted: continue` block, making them
unreachable dead code. The only reachable path was `return True`.

**Fix applied (Steps 5, 22, 31, 32):**
```python
# Correct order — all at same indentation level inside the for loop:
for symbol in mentioned_symbols:
    low = symbol.lower()
    if low.startswith("self."):                              # Step 5
        continue
    if re.match(r"^(Q[A-Z]|PySide6|PyQt)", symbol):        # Step 5
        continue
    if symbol in snippet_dotted:                            # Step 5
        continue
    if symbol in allowed_symbols:                           # Step 5 (was dead)
        continue
    last_segment = symbol.split(".")[-1].lower()            # Step 22
    if last_segment in {"connect", "disconnect", "emit"}:  # Step 22
        continue
    if all(seg == seg.lower() for seg in symbol.split(".")): # Step 22
        continue
    return True
```

Also extended `_extract_allowed_symbols()` to read `Functions:` and
`Classes:` lines from FILE EVIDENCE detail (Step 32):
```python
file_detail_pattern = re.compile(
    r"^(?:Functions|Classes|Calls out):\s+(.+)$",
    flags=re.MULTILINE,
)
for detail_match in file_detail_pattern.findall(prompt):
    for token in re.findall(r"\b[A-Za-z_]...\b", detail_match):
        allowed.add(token)
```

---

### forbidden_paths (SECOND MOST COMMON)

**What it checks:**
Extracts path-like strings from the answer and rejects any not in the
retrieved FILE EVIDENCE pack.

**Why it fired on valid answers:**
A correct architectural answer about the startup chain legitimately mentions
`shell/splash/eeg_splash_screen.py` and `shell/timeline/eeg_timeline_attachment.py`
even if those files ranked 11th and 12th and were not in the top-N evidence.

Also fired for widget listing answers because widget file paths came from
`WIDGET REGISTRY` section, not from `FILE EVIDENCE`.

**Fix applied (Step 6, Step 40):**
```python
def _has_forbidden_paths(self, prompt, answer_text):
    # Generative answers legitimately reference files outside top-N evidence
    if self._is_generative_prompt(prompt):
        return False
    # Deterministic prompts still enforce strict path containment
    ...
```

Also: `_is_generative_prompt()` must recognize ALL generative question types.
If a new question type is added to the router but not to `_is_generative_prompt()`,
answers fall to the `default` branch where `forbidden_paths` runs again.

---

### ignored_required_snippets

**What it checks:**
For code-localization questions, verifies that the answer cites at least one
snippet by `[SN01]` id, full anchor qualname, or file path.

**Why it fired on valid answers:**
LLM writes `build_and_show` (short name) instead of
`EEGMainWindowBuilder.build_and_show` (full qualname) → `anchor_hits = 0`.
Even when the answer contains verbatim code from the snippet, no citation
token matches → rejected.

**Fix applied (Step 7):**
```python
# Also accept short anchor tail match
short_anchor_hits = sum(
    1 for block in snippet_blocks
    if str(block.get("anchor", "")).split(".")[-1].strip().lower() in answer_low
)
# Also accept verbatim code line match
snippet_code_hits = 0
for block in snippet_blocks:
    snippet_lines = [ln.strip() for ln in str(block.get("text","")).splitlines()
                     if len(ln.strip()) > 10]
    if any(ln.lower() in answer_low for ln in snippet_lines):
        snippet_code_hits += 1
return (snippet_id_hits + anchor_hits + path_hits
        + short_anchor_hits + snippet_code_hits) == 0
```

---

## THE BRANCH MISMATCH PROBLEM

This is the most subtle and recurring problem.

**The system has THREE independent intent classifiers:**

```
v10_query_router.py       route_query_intent()       → determines UI route
v10_retriever.py          detect_query_intents()      → determines scoring boosts
v10_prompt_builder.py     _is_* functions             → determines prompt style
v10_ai_bridge.py          _is_generative_prompt()     → determines validator branch
                          _is_deterministic_prompt()
```

**They are NOT connected.** A question can be routed as `generative/signal_action`
by the router but fall to the `default` validator branch because
`_is_generative_prompt()` does not know about `signal_action`.

**Every time a new route is added to `route_query_intent()`, the same
intent trigger MUST also be added to `_is_generative_prompt()` in
`v10_ai_bridge.py`.**

**History of this problem in this session:**
- Step 12 added `signal_action` route → Step 21 added it to `_is_generative_prompt()`
- Step 38 added `widget_listing` route → Step 40 added it to `_is_generative_prompt()`

**Pattern to follow every time a new route is added:**

```python
# 1. Add to route_query_intent() in v10_query_router.py:
if is_my_new_question(q):
    return QueryRouteDecision(route="generative", intent_name="my_new_intent", ...)

# 2. ALWAYS also add to _is_generative_prompt() in v10_ai_bridge.py:
my_new_terms = ["term1", "term2", ...]
has_my_new_intent = any(term in q for term in my_new_terms)
return (has_explanation_intent or ... or has_my_new_intent)
```

**Diagnostic check:** If a question routes correctly (you see the right intent
in the log) but the answer is still rejected by `forbidden_paths` or
`forbidden_symbols`, the branch mismatch is the cause. Run:

```python
q = "your question here".strip().lower()
# Check if _is_generative_prompt would return True
explanation_terms = ["explain", "summarize", "describe", ...]
signal_terms = ["signal", "slot", "connects", ...]
widget_terms = ["list all buttons", "buttons with their", ...]
print("is_generative:", any(t in q for t in explanation_terms + signal_terms + widget_terms))
```

---

## Form B — Model self-reports INSUFFICIENT_EVIDENCE

This is NOT a validator problem. The model is correct — the evidence pack
sent to it does not contain the answer.

**Root causes and fixes:**

### 1. Wrong JSON loaded / partial JSON

The assembled JSON must contain the `files` top-level key (a list of 243
file records). If `files_by_path` is empty after loading, retrieval returns
no file evidence → empty prompt → model correctly says INSUFFICIENT_EVIDENCE.

**Diagnostic:**
```python
import json
d = json.load(open("your_index.json"))
print("files count:", len(d.get("files", [])))  # Must be > 0
```

**Fix (Step 15):** Warning added to `index_loader._rebuild_indexes()` when
`files_by_path` is empty.

### 2. Type mismatches in index_loader silently drop data

The JSON has dict/list types that `index_loader` loads with the wrong
`_safe_*` method, silently returning empty structures.

**Known mismatches fixed in this session:**

| Field | JSON type | Loader (wrong) | Loader (correct) | Step |
|---|---|---|---|---|
| `execution_chains` | `dict` | `_safe_list()` → `[]` | `_safe_dict()` | 1 |
| `subsystems` | `list` | `_safe_dict()` → `{}` | `_safe_list()` | 2 |
| `qt_signal_map` | `list` | `_safe_dict()` → `{}` | `_safe_list()` | 27 |

**How to diagnose:** After loading, check:
```python
print(type(idx.execution_chains), len(idx.execution_chains))  # Should be dict, 4
print(type(idx.subsystems), len(idx.subsystems))              # Should be list, 11
print(type(idx.qt_signal_map), len(idx.qt_signal_map))        # Should be list, 115
```

### 3. Snippet retrieval falls back to disk

`_retrieve_snippets()` originally called `_read_snippet(abs_path)` which
reads from `E:\eeg_kernel_ai_neural_data_analysis\...` — unavailable at
query time. The JSON has pre-indexed snippets in `snippet_index`.

**Fix (Steps 3, 4):**
- `index_loader` builds `snippets_by_file` from `snippet_index`
- Retriever primary path reads from `snippets_by_file` before disk fallback

### 4. Question type has no evidence in scope

Some questions cannot be answered because the JSON only indexes
`eeg_kernel_ai_neural_data_analysis` project files. Questions about
`developer_tools/` (the reasoner tool itself) have no evidence.

**Fix (Step 30):** `is_allowed_project_path()` now blocks `developer_tools/`
from entering evidence, preventing noise from collector tool files leaking in.

### 5. Evidence exists but file scores too low to enter top-N

The correct file is in the JSON but never reaches top-10 evidence because
scoring heuristics do not recognize the question type.

**Pattern:** Model says evidence is missing but you know the data is there.

**Diagnostic:** Check what files actually score for the question by reading
the ranked evidence panel. If the correct file is not in F01-F10, a scoring
boost is missing.

**Fixes applied:**
- Signal questions: `qt_signal_map` boost with weighted scoring (Steps 24–28)
- Chain questions: `execution_chains` step membership boost (Step 8)
- Subsystem questions: `subsystems` membership boost (Step 9)
- Widget questions: `widget_registry` button boost (Step 37)

### 6. Evidence exists but detail is empty → LLM ignores it

A file scores high and enters evidence (e.g. F01) but its detail string is
nearly empty because it has no `files_by_path` entry. The LLM sees the file
name but no content → reports insufficient evidence.

**Fix (Step 28):** `_build_compact_file_evidence()` now appends a
`Qt signals:` line from `qt_signal_map` for files with signal connections,
injecting signal facts directly into the file evidence detail.

**General pattern:** For any new data type in the JSON that the LLM needs
to read, inject it into `_build_compact_file_evidence()` or add a dedicated
section to the prompt (as done with `WIDGET REGISTRY` in Step 39).

### 7. New question type has no route to generative path

Question falls to `ranked/discovery` or `ranked/default_ranked` which
shows the evidence panel without calling the LLM.

**Fix pattern:**
```python
# v10_query_router.py: add new function
def is_my_new_question(q: str) -> bool:
    terms = ["my", "trigger", "terms"]
    return _has_any(q, terms)

# route_query_intent(): add BEFORE is_listing_or_discovery_question check
if is_my_new_question(q):
    return QueryRouteDecision(route="generative", intent_name="my_new_intent", ...)

# v10_ai_bridge.py _is_generative_prompt(): add matching terms
my_new_terms = ["my", "trigger", "terms"]
has_my_new_intent = any(term in q for term in my_new_terms)
return (...existing... or has_my_new_intent)
```

### 8. Evidence data not injected into prompt

The JSON has the data, the retriever finds the right files, but the relevant
structured data (widget registry, signal connections, execution chains) is
never written into the prompt text the model reads.

**Fix pattern (Step 39 as template):**
```python
# In PromptBuilder.build(), add a new section before STRICT GROUNDING RULE:
if is_my_listing_question(question) and my_data:
    lines.append("MY DATA SECTION")
    lines.append("Use this data to answer the question. List ALL entries.")
    for key, rec in my_data.items():
        lines.append(format_record(rec))
    lines.append("")
```

---

## QUICK DIAGNOSIS CHECKLIST

When `INSUFFICIENT_EVIDENCE` appears, ask these questions in order:

```
1. Is it Form A (answer shown then erased) or Form B (model reports)?
   └─ Form A → check validator rules (forbidden_symbols, forbidden_paths)
   └─ Form B → check evidence pipeline

2. Form A: Which rule fired?
   Check status bar or log: "Grounding rejection: <rule_name>"
   └─ forbidden_symbols → check _has_forbidden_symbols indentation
                           check allowed_symbols coverage
                           check branch mismatch (_is_generative_prompt)
   └─ forbidden_paths   → check _is_generative_prompt covers this question type
   └─ ignored_required_snippets → check snippet citation relaxation (Step 7)

3. Form B: Is the data in the JSON?
   └─ No  → collector needs to index it
   └─ Yes → is it loaded correctly? (type mismatch check)
          → is it retrieved? (scoring check)
          → is it in the prompt? (evidence detail or new section)

4. Branch mismatch check:
   Simulate _is_generative_prompt for your question.
   If False but router says generative → add terms to _is_generative_prompt.
```

---

## FILES TO EDIT FOR EACH ROOT CAUSE

| Root cause | File to edit | Method/location |
|---|---|---|
| forbidden_symbols false positive | `v10_ai_bridge.py` | `_has_forbidden_symbols()` |
| allowed_symbols too narrow | `v10_ai_bridge.py` | `_extract_allowed_symbols()` |
| forbidden_paths false positive | `v10_ai_bridge.py` | `_has_forbidden_paths()` |
| ignored_required_snippets | `v10_ai_bridge.py` | `_answer_ignored_required_snippets()` |
| Branch mismatch | `v10_ai_bridge.py` | `_is_generative_prompt()` |
| New route not generative | `v10_query_router.py` + `v10_ai_bridge.py` | `route_query_intent()` + `_is_generative_prompt()` |
| Type mismatch in loader | `v10_index_loader.py` | `_load_full_sections()` + `__init__` |
| Snippet from disk | `v10_index_loader.py` + `v10_retriever.py` | `_build_snippet_lookup_index()` + `_retrieve_snippets()` |
| File scores too low | `v10_retriever.py` | `_retrieve_files()` scoring loop |
| Evidence detail empty | `v10_retriever.py` | `_build_compact_file_evidence()` |
| Data not in prompt | `v10_prompt_builder.py` | `PromptBuilder.build()` |
| Question type not routed | `v10_query_router.py` | `route_query_intent()` |

---

## VALIDATION COMMANDS AFTER ANY FIX

After any edit to `v10_ai_bridge.py`, always verify:

```powershell
@'
from pathlib import Path

path = Path(r"developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_ai_bridge.py")
lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

for i, line in enumerate(lines, 1):
    if "def _has_forbidden_symbols" in line:
        for j in range(i-1, min(i+55, len(lines))):
            print(str(j+1) + ": " + lines[j])
        break
'@ | python
```

Verify that EACH of these six checks is at 12-space indentation INSIDE
the `for symbol in mentioned_symbols:` loop, NOT nested inside each other:
1. `if low.startswith("self."):`
2. `if re.match(r"^(Q[A-Z]|PySide6|PyQt)", symbol):`
3. `if symbol in snippet_dotted:`
4. `if symbol in allowed_symbols:`
5. `if last_segment in {"connect", "disconnect", "emit"}:`
6. `if all(seg == seg.lower() for seg in symbol.split(".")):`

And `return True` must be at the SAME 12-space level, not nested inside any of them.

---

*Document generated from Project Reasoner v10 session — March 2026*
*All fixes referenced by Step number correspond to the implementation session log.*
