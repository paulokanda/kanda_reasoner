# TASKS.md — AI-Powered Local Docstring Inserter

This file is the local execution tracker for the AI-powered docstring inserter project.

Use these status values:
- `todo`
- `in_progress`
- `blocked`
- `done`

Suggested workflow:
1. Complete tasks in numeric order unless a dependency is already done.
2. Do not start parallelism or GUI work before the sequential AI + validator path is stable.
3. Update the `Status`, `Owner`, and `Notes` fields as work progresses.

---

## Task Overview

| ID | Title | Status | Owner | Depends On |
|---|---|---|---|---|
| 1 | Freeze generator contract | done | assistant | - |
| 2 | Implement AIConfig | done | assistant | 1 |
| 3 | Implement context builder | done | assistant | 1 |
| 4 | Implement baseline AI generator | done | assistant | 1,2,3 |
| 5 | Wire sequential AI into worker | done | assistant | 1,2,3,4 |
| 6 | Implement standalone validator | done | assistant | 1,2,3 |
| 7 | Upgrade generator to validator-gated mode | done | assistant | 2,4,6 |
| 8 | Patch worker runtime controls | done | assistant | 2,5,6,7 |
| 9 | Add docstring policy layer | done | assistant | 2,6 |
| 10 | Implement module summarizer | done | assistant | 2,3,4 |
| 11 | Apply Phase 3 worker patch | done | assistant | 3,7,10 |
| 12 | Add per-file parallelism | done | assistant | 5,6,7,8 |
| 13 | Upgrade GUI | done | assistant | 8,12 |
| 14 | Build benchmarks and rollout gates | done | assistant | 6,7,8,9,10,11,12,13 |

---

## Task 1 — Freeze generator contract

**Status:** done  
**Owner:** assistant  
**Depends on:** none

### Goal
Define one stable return contract for AI generation and remove ambiguity between:
- returning a raw string body
- returning a confidence-aware result

### Scope
- Standardize `AIDocstringGenerator.generate(...)`
- Standardize what the worker expects back
- Standardize what the GUI and validator consume
- Update integration notes to reflect the final contract

### Recommended contract
```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class GenerationResult:
    body: str
    source: Literal["ai", "cache", "heuristic"]
    confidence: Literal["high", "medium", "low"]
    issues: list[str] = field(default_factory=list)
    cache_hit: bool = False
    used_fallback: bool = False
    uncertain: bool = False
```

### Files
- `ai_docstring_generator.py`
- `insert_missing_docstrings.py`
- `INTEGRATION_GUIDE.py`

### Acceptance criteria
- All code and docs use one return contract only
- No remaining code assumes both `str` and `(str, confidence)` style returns
- Worker integration points are unambiguous

### Test notes
- Review-only task
- Confirm all stubs, docs, and code comments match the final contract

### Notes
-

---

## Task 2 — Implement AIConfig

**Status:** done  
**Owner:** assistant  
**Depends on:** 1

### Goal
Create the runtime control plane for AI behavior.

### Scope
Implement:
- endpoint and model configuration
- timeout and token settings
- fallback behavior
- cache settings
- worker count
- include-private behavior
- confidence threshold
- line-length and TODO-density limits
- uncertainty annotation toggle

### Files
- `ai_config.py`

### Acceptance criteria
- `from_json()` works
- `to_json()` works
- unknown keys fail fast
- defaults are sensible
- validator-related fields are exposed cleanly

### Test notes
- Round-trip a sample config file
- Verify unknown keys raise a clear error
- Verify default config loads without a file

### Notes
-

---

## Task 3 — Implement context builder

**Status:** done  
**Owner:** assistant  
**Depends on:** 1

### Goal
Build grounded symbol context from AST instead of relying on names and signatures only.

### Scope
Implement:
- `ParameterInfo`
- `AttributeInfo`
- `SymbolContext`
- `build_module_context()`
- `build_class_context()`
- `build_function_context()`

Support:
- source lines
- signature
- decorators
- enclosing class
- sibling docstrings
- imports
- return annotation
- `module_summary_block`
- `class_attributes`
- `raises_types`
- `overload_siblings`
- `is_property`
- `is_cached_property`
- `is_staticmethod`
- `is_classmethod`
- `is_overload`
- `is_dataclass`
- `is_init`

### Files
- `context_builder.py`

### Acceptance criteria
- Context builders work from one parsed module tree
- Property and cached-property contexts suppress parameters correctly
- Overload variants are collected as hints
- Explicit raises are extracted
- `__init__`-derived attribute data is available for classes

### Test notes
Create fixtures for:
- plain function
- property
- staticmethod
- classmethod
- overload stub + implementation
- explicit raise
- dataclass
- `__init__` with `self.attr = ...`

### Notes
-

---

## Task 4 — Implement baseline AI generator

**Status:** done  
**Owner:** assistant  
**Depends on:** 1, 2, 3

### Goal
Finish the first working generator with local AI calls and heuristic fallback.

### Scope
Implement:
- prompt building from `SymbolContext`
- local model HTTP call
- response cleanup
- cache lookup/store
- heuristic fallback on failure

Do not add module summarization or parallelism yet.

### Files
- `ai_docstring_generator.py`

### Acceptance criteria
- Generator returns a valid `GenerationResult`
- Timeout falls back safely
- Malformed model output falls back safely
- Cache behavior works when enabled

### Test notes
Mock:
- successful AI response
- timeout
- malformed JSON / malformed body
- fallback path
- cache hit path

### Notes
-

---

## Task 5 — Wire sequential AI into worker

**Status:** done  
**Owner:** assistant  
**Depends on:** 1, 2, 3, 4

### Goal
Integrate AI into the existing worker without changing its safety model.

### Scope
- Thread optional generator through:
  - `collect_changes()`
  - `collect_missing_docstring_insertions()`
- Add `--ai [CONFIG]`
- Load `AIConfig`
- Create `AIDocstringGenerator`
- Replace direct builder calls only when AI is enabled

### Files
- `insert_missing_docstrings.py`
- `INTEGRATION_GUIDE.py`

### Acceptance criteria
- `scan`, `diff`, and `write` work in AI mode
- Non-AI behavior remains unchanged
- Re-parse safety remains intact

### Test notes
Run:
```bash
python insert_missing_docstrings.py --root /path/to/project --scan --ai
python insert_missing_docstrings.py --root /path/to/project --diff --ai
```
Then verify `--write --ai` on a small test project only.

### Notes
-

---

## Task 6 — Implement standalone validator

**Status:** done  
**Owner:** assistant  
**Depends on:** 1, 2, 3

### Goal
Make validator the acceptance gate for AI output.

### Scope
Implement:
- `ValidationConfig`
- `ValidationResult`
- `validate()`

Checks should cover:
- empty output
- markdown fences
- echoed code
- invented parameters
- invented raises
- section ordering
- line length
- TODO density
- cleaned output
- confidence scoring

### Files
- `docstring_validator.py`

### Acceptance criteria
- Every AI output gets a deterministic validation result
- Fatal failures reject output
- Warning-level issues reduce confidence

### Test notes
Test:
- empty output
- code fence
- source echo
- invented parameter
- invented raises
- wrong section order
- long lines
- TODO-heavy but nonfatal output

### Notes
-

---

## Task 7 — Upgrade generator to validator-gated mode

**Status:** done  
**Owner:** assistant  
**Depends on:** 2, 4, 6

### Goal
Route all AI outputs through the standalone validator and add operational reporting.

### Scope
Implement:
- validator handoff
- `GenerationStats`
- `on_low_confidence` callback
- private-symbol routing
- optional uncertainty annotation support

### Files
- `ai_docstring_generator.py`
- `ai_config.py`

### Acceptance criteria
- Rejected AI output falls back to heuristic
- Stats track:
  - total
  - cached
  - ai_ok
  - fallback
  - low_confidence
  - medium_confidence
  - skipped_private
- Low-confidence events are exposed

### Test notes
Run generator against:
- public symbols
- private symbols
- low-confidence outputs
- rejected outputs

### Notes
-

---

## Task 8 — Patch worker runtime controls

**Status:** done  
**Owner:** assistant  
**Depends on:** 2, 5, 6, 7

### Goal
Expose Phase 4 operational controls in the worker.

### Scope
Add:
- `--private`
- `--no-private`
- `--min-confidence`
- `--no-uncertain`

Also:
- override config from CLI
- print AI generation stats
- emit low-confidence notices

### Files
- `insert_missing_docstrings.py`

### Acceptance criteria
- CLI overrides work correctly
- End-of-run stats are printed
- Low-confidence notices are visible in output

### Test notes
Run:
```bash
python insert_missing_docstrings.py --root . --diff --ai --no-private --min-confidence medium --no-uncertain
python insert_missing_docstrings.py --root . --diff --ai my_config.json --min-confidence high --workers 6
```

### Notes
-

---

## Task 9 — Add docstring policy layer

**Status:** done  
**Owner:** assistant  
**Depends on:** 2, 6

### Goal
Add project-specific documentation rules instead of relying only on generic NumPy-style behavior.

### Scope
Create:
- `docstring_policy.py` or equivalent local policy file

Policy should define:
- required sections
- rules by symbol kind
- private-symbol defaults
- module docstring behavior
- TODO allowance by context
- repo-specific phrasing or conventions

### Files
- `docstring_policy.py` (new)
- optionally `ai_config.py`
- optionally `docstring_validator.py`

### Acceptance criteria
- Repo-specific rules are centralized
- Generator and validator can consult the same policy
- Behavior is no longer purely generic

### Test notes
Create one sample policy and verify it affects:
- one module
- one class
- one function

### Notes
-

---

## Task 10 — Implement module summarizer

**Status:** done  
**Owner:** assistant  
**Depends on:** 2, 3, 4

### Goal
Add a shared module-level semantic pre-pass.

### Scope
Implement:
- `InitAttribute`
- `ClassProfile`
- `ModuleSummary`
- AST-only profiling
- optional AI one-liner + purpose paragraph generation
- prompt-ready `context_block`

### Files
- `module_summarizer.py`

### Acceptance criteria
- Module summary can be built even if AI is unavailable
- AI failures are non-fatal
- Class inventory and init-derived structure are exposed

### Test notes
Use a module with:
- multiple classes
- constants
- public functions
- `__init__` assignments
- annotated attributes

### Notes
-

---

## Task 11 — Apply Phase 3 worker patch

**Status:** done  
**Owner:** assistant  
**Depends on:** 3, 7, 10

### Goal
Make the worker module-aware and two-pass for class generation.

### Scope
- Import `build_module_summary`
- Replace `collect_missing_docstring_insertions()` body with the Phase 3 version
- Run module pre-pass once per file
- Pass module summary into context builders
- Process `__init__` first
- Then process classes
- Then process remaining functions/methods
- Skip `@overload` stubs as direct documentation targets

### Files
- `insert_missing_docstrings.py`

### Acceptance criteria
- Shared module context is used throughout a file
- Class generation can use init-derived information
- Overload stubs are skipped correctly

### Test notes
Run `--diff --ai` on a module containing:
- `__init__`
- property
- overload
- explicit raises
- multiple classes

### Notes
-

---

## Task 12 — Add per-file parallelism

**Status:** done  
**Owner:** assistant  
**Depends on:** 5, 6, 7, 8

### Goal
Scale AI mode with per-file concurrency while preserving output semantics.

### Scope
Implement:
- `FileProgress`
- `RunSummary`
- `run_parallel()`
- worker-side routing to parallel mode when `workers > 1`

Keep heuristic mode sequential.

### Files
- `parallel_runner.py`
- `insert_missing_docstrings.py`

### Acceptance criteria
- Parallel and sequential AI runs produce equivalent output
- Per-file progress is available
- Throughput improves for larger projects

### Test notes
Compare:
- `--workers 1`
- `--workers 4`

Confirm identical diffs on the same project.

### Notes
-

---

## Task 13 — Upgrade GUI

**Status:** done  
**Owner:** assistant  
**Depends on:** 8, 12

### Goal
Make GUI a correct frontend over the working CLI path.

### Scope
Add:
- AI enablement controls
- config path
- workers
- min-confidence selector
- private-symbol toggle
- uncertainty toggle
- progress bar
- output visibility for AI stats

### Files
- `insert_missing_docstrings_gui.py`

### Acceptance criteria
- GUI options actually affect backend behavior
- Progress is visible
- AI stats appear in the output panel or status area

### Test notes
Run GUI with:
- AI off
- AI on
- different confidence thresholds
- private-symbol toggle on/off
- multiple workers

### Notes
-

---

## Task 14 — Build benchmarks and rollout gates

**Status:** done  
**Owner:** assistant  
**Depends on:** 6, 7, 8, 9, 10, 11, 12, 13

### Goal
Create evidence-based rollout criteria.

### Scope
Build a benchmark corpus containing:
- utilities
- dataclasses
- async functions
- properties
- overloads
- explicit raises
- init-heavy classes
- package `__init__.py`

Track:
- validator rejection rate
- fallback rate
- cache hit rate
- low-confidence rate
- diff approval rate
- write-safety rate

### Files
- `benchmark/` or `tests/`
- sample projects
- reporting scripts

### Acceptance criteria
- Benchmark corpus exists
- Metrics are captured and reviewable
- Team has clear rollout gates before broad write-mode use

### Test notes
Run:
- `scan --ai`
- `diff --ai`
- restricted `write --ai`
on benchmark corpus and compare at least two model/config combinations.

### Notes
-

---

## Release Plan

### Release 1
Tasks:
- 1
- 2
- 3
- 4
- 5
- 6
- 7
- 8

Output:
- sequential AI generation
- validator gating
- fallback
- config
- stats
- operator controls

### Release 2
Tasks:
- 9
- 10
- 11

Output:
- repo policy
- module summarization
- two-pass class generation
- richer semantic context

### Release 3
Tasks:
- 12
- 13
- 14

Output:
- parallel execution
- GUI
- benchmarks
- controlled rollout gates

---

## Daily Update Template

Use this when tracking work locally.

```md
### Daily Update
- Date:
- Task ID:
- Owner:
- Status:
- What changed:
- What is blocked:
- Next action:
```

---

## Decision Log Template

```md
### Decision
- Date:
- Topic:
- Decision:
- Why:
- Affected tasks:
```


---

## Post-Release Hardening

| ID | Title | Status | Owner | Depends On |
|---|---|---|---|---|
| 15 | Build automated test suite | done | assistant | 6,7,8,10,11,12,13,14 |

---

## Task 15 — Build automated test suite

**Status:** done  
**Owner:** assistant  
**Depends on:** 6, 7, 8, 10, 11, 12, 13, 14

### Goal
Add a repeatable automated test suite that hardens validator, context extraction, and worker fallback behavior.

### Scope
Implemented:
- `tests/test_ai_config.py`
- `tests/test_context_builder.py`
- `tests/test_docstring_validator.py`
- `tests/test_worker_integration.py`

Coverage includes:
- config round-trip and unknown key rejection
- context extraction for properties, staticmethods, overloads, raises, and init-derived attributes
- validator acceptance, fatal rejection, TODO-density confidence lowering, and quote stripping
- worker write-mode behavior and AI fallback behavior when the local endpoint is unavailable

### Files
- `tests/`

### Acceptance criteria
- Tests run with `python -m unittest discover -s tests -v`
- Core backend behaviors are exercised without needing a live local model server

### Test notes
Run from project root:
```bash
python -m unittest discover -s tests -v
```

### Notes
- Added after the original 14 tasks to harden the implemented codebase.


---

## Task 19 — Harden AI output validation for quote-delimiter failures

**Status:** done  
**Owner:** local  
**Depends on:** 6, 7, 15

### Goal
Prevent accepted AI output from producing invalid Python when the model returns raw triple quotes or quote-only content.

### Scope
- reject quote-only output like `"""` or `'''`
- reject embedded triple-quote delimiters in AI output
- add regression tests around malformed module docstrings

### Notes
- Added validator guardrails and regression tests after a real scan run produced an unterminated string literal from accepted AI output.
