on_ev_phs_tool â€” what is this for?

A repeatable, on-every-push analysis that rebuilds text/JSON/MD reports so an AI (or a human) can understand your projectâ€™s structure and health. It does not modify your code â€” think of it as always-on x-ray vision.

Repo tool: dev_tools/on_every_push_tool/on_ev_phs_tool.py
Outputs: dev_tools/results_report/
Scope rules: Only .py files; skip any path containing the word deprecated
Artifacts: ASCII/TXT, JSON, MD (no PNG/HTML)

What you get on each run (no auto-fix)

Architecture overview & flows (text)
Dependency hotspots (which files/modules are most coupled)
Cyclomatic complexity per function/method
Architecture violations (e.g., circular imports, simple layer checks)
Tech-debt scan (TODO/FIXME)
Optional: similar-code pairs and basic performance hints

Everything lands in dev_tools/results_report/, plus two machine-readable files:

ci_quality_summary.json â€” compact numeric metrics
ci_quality_gates.json â€” thresholds used + pass/fail details

What it does not do

No code changes, no formatters, no autofix.
No diagrams (PNG/HTML). Pure text/JSON/MD.

How it decides what to scan

Walks the repo from the project root (adds the root to sys.path so imports work).
Ignores any directory whose path contains deprecated.
Parses only .py files (analyzer default behavior).

Setup

Python 3.10+
Install deps once (runner or venv):

pip install -U radon jinja2 pyyaml graphviz

Optional (makes imports bullet-proof on some IDEs/Windows setups):


ni dev_tools\__init__.py -Type File -Force
ni dev_tools\project_analysis\__init__.py -Type File -Force
ni dev_tools\on_every_push_tool\__init__.py -Type File -Force

Basic usage (run from the repo root)
Run analysis + quality gates (text/JSON only)

python -m dev_tools.on_every_push_tool.on_ev_phs_tool run


With thresholds

python -m dev_tools.on_every_push_tool.on_ev_phs_tool run --max-cx 15 --max-debt 0

Persist a baseline (compare future runs against it)


Show the latest summary (or run a quick pass if missing)


python -m dev_tools.on_every_push_tool.on_ev_phs_tool summary





What each command teaches you about the project

Run (default)
Generates fresh reports and two JSONs. You learn:
complexity_max â€” the spikiest functionâ€™s cyclomatic complexity
functions_analyzed â€” coverage of the pass
architecture_violations â€” boundary/cycle issues across modules
dependency_warnings â€” fragile or suspicious imports/coupling
tech_debt_items â€” current TODO/FIXME load (quick workload proxy)
similar_code_pairs â€” duplicated logic (if similarity is enabled)
perf_flags â€” deep nesting/large structures (if performance is enabled)

Run with thresholds (--max-cx, --max-debt, --fail-on-arch, --fail-on-deps)
Same discovery, but turns signals into guardrails. You immediately see if:
any function exceeds your complexity tolerance
debt silently grew beyond your budget
an architecture or dependency rule was violated

Write baseline
Creates dev_tools/project_analysis/quality_baseline.json anchoring todayâ€™s counts. Later runs with --use-baseline tell you did we regress vs. ourselves, even if absolute thresholds are generous.

Summary
Fast visibility without regenerating all text/MD. Prints (or builds) ci_quality_summary.json â€” your quick â€œproject healthâ€ readout for stand-ups/CI logs.

Flag glossary â€” and the extra knowledge each one unlocks

--max-cx <int>
Sets the maximum allowed cyclomatic complexity. Knowledge effect: highlights the worst offenders that drive cognitive load.

--max-debt <int>
Sets the maximum allowed TODO/FIXME count. Knowledge effect: keeps debt visible and forces triage if it grows.

--fail-on-arch {0,1}
Blocks on architecture violations (e.g., cycles, broken boundaries). Knowledge effect: surfaces boundary erosion immediately.

--fail-on-deps {0,1}
Blocks on dependency warnings. Knowledge effect: prevents fragile/back-channel imports from creeping in.

--use-baseline
Compares debt (and other counts) to the saved baseline instead of raw thresholds. Knowledge effect: answers â€œdid things get worse since the approved snapshot?â€

--enable-similarity
Turns on duplicate-code detection. Knowledge effect: surfaces consolidation opportunities to reduce bug-fix surface and maintenance cost.

--enable-performance
Adds lightweight perf smells (deep nesting, very large structures). Knowledge effect: points at readability and potential runtime hotspots without benchmarking.

Environment variables (optional)

MAX_CX, MAX_DEBT, FAIL_ON_ARCH, FAIL_ON_DEPS mirror the flags so you can set org-wide defaults.

Quick â€œWhat changed?â€ workflow

First clean run
python -m dev_tools.on_every_push_tool.on_ev_phs_tool run --max-cx 15 --max-debt 0

Freeze a baseline when the state is acceptable
python -m dev_tools.on_every_push_tool.on_ev_phs_tool write-baseline

Subsequent pushes
Run with --use-baseline to fail only on regressions.

CI snippets

Linux/macOS

pip install -U radon jinja2 pyyaml graphviz
python -m dev_tools.on_every_push_tool.on_ev_phs_tool run --max-cx 15 --max-debt 0


######################## Windows

pip install -U radon jinja2 pyyaml graphviz
python -m dev_tools.on_every_push_tool.on_ev_phs_tool run --max-cx 15 --max-debt 0


########################

Exit codes & gates

0 = all gates passed
1 = one or more gates failed (see ci_quality_gates.json and console output)

Gates evaluated
Architecture violations
Max complexity
Dependency warnings
Tech-debt threshold or regression vs baseline (when --use-baseline)

Expected artifacts

project_architecture_YYYYMMDD_HHMM.txt
flows_enriched_YYYYMMDD_HHMM.txt
method_details_YYYYMMDD_HHMM.txt
dependency_hotspots_YYYYMMDD_HHMM.md
technical_debt_YYYYMMDD_HHMM.md
ci_quality_summary.json
ci_quality_gates.json

Optional baseline
dev_tools/project_analysis/quality_baseline.json

Troubleshooting

ModuleNotFoundError for dev_tools...
Run from the repo root with -m as shown above. Optionally create __init__.py files under dev_tools/, dev_tools/project_analysis/, and dev_tools/on_every_push_tool/.

No artifacts appear
Verify write permissions to dev_tools/results_report/.

Slow run
Skip extras by omitting --enable-similarity and --enable-performance.

Over-exclusion
Any path containing deprecated is ignored; if thatâ€™s too broad, we can switch to regex or an explicit list.

FAQ

Can it auto-fix problems?
No â€” itâ€™s for visibility and drift detection. You do the refactors.

Why require graphviz if no images?
Some analyzer code paths import its Python bindings; keeping it installed avoids import errors even when exporting only text/MD/JSON.

Where is the code?
dev_tools/on_every_push_tool/on_ev_phs_tool.py

