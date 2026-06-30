# KANDA Reasoner Project Intelligence Engines Canon v1

Status: canonical implementation guide
Scope: selected future intelligence features for KANDA Reasoner
Audience: human project owner and AI implementation agents
Mode: reference before implementation, patch planning, validation, and future audits

## 1. Purpose

This document defines the canonical implementation direction for adding selected Project Intelligence features to KANDA Reasoner.

The goal is to increase KANDA Reasoner's ability to understand, explain, audit, and protect a Python project without bloating the user interface, duplicating existing tabs, or introducing unsafe AI-dependent behavior.

The selected features must be implemented as internal engines or contextual sections inside existing tabs, not as new top-level tabs.

KANDA Reasoner should become more intelligent, not more crowded.

## 2. Project role

KANDA Reasoner is a desktop Python application for AI-human software collaboration.

It helps the human user:

* show a project to an AI in a structured way;
* route tasks through the correct prompt and project governance context;
* understand architecture and workflows;
* identify risky changes before patching;
* validate patches;
* preserve validated behavior through freeze memory;
* preserve past mistakes through Error Memory;
* help non-programmer humans direct AI-assisted development safely.

KANDA Reasoner is not just a code scanner. It is a reasoning, governance, validation, handoff, and memory system.

## 3. Current major areas

The new intelligence engines must support the existing app, not replace it.

Existing areas include:

1. Brain Navigator

   * Main project-brain entry point.
   * Should eventually display living project knowledge.

2. Architecture Review

   * Reviews architecture, boundaries, ownership, imports, stale design, and architecture risks.

3. Workflow Review

   * Reviews workflow order, IO contracts, documentation drift, validation references, and GUI/workflow consistency.

4. Engineering Safety

   * Runs diagnostics, risk checks, crash triage, release hygiene, and pre-patch safety tools.

5. Docstring Assistant

   * Reviews and helps generate docstrings.

6. Show Project to AI

   * Builds structured AI handoff packages and source archives.

7. Error Memory

   * Stores active project-specific lessons from previous mistakes.

8. Refactor Report

   * Produces project state/refactor evidence.

9. Project Q&A

   * Lets the user ask questions about project evidence and JSON artifacts.

10. Freeze Feature After Update

* Writes validated feature memory only after explicit human confirmation.

11. Exclusion Rules

* Manages project-specific ignored files, folders, and extensions.

12. Prompt Library

* Browses and routes prompt-library content.

## 4. Core decision

The selected tools from the uploaded toolbox must not become one tab each.

Canonical rule:

* New tab only if there is a complete, independent, recurring workflow that cannot fit inside an existing tab.
* Internal engine if the tool produces reusable project intelligence.
* Existing-tab section if the tool supports a current workflow.
* Utility module if the tool is only a helper.

The current decision is:

* Do not add new top-level tabs for these tools.
* Build a Project Intelligence internal layer.
* Expose engine output inside existing tabs only after the engine contract is stable.
* Keep V1 deterministic, offline-safe, and read-only.
* Treat AI explanations as optional second-pass summaries, never as source-of-truth findings.

## 5. Non-goals

The following are explicitly out of scope for the first implementation wave:

* no new top-level tabs;
* no direct copying of old toolbox code without audit;
* no AI-dependent findings in V1;
* no automatic file modification by engines;
* no automatic freeze writing;
* no automatic ADR writing;
* no mandatory external tools such as Bandit, pytest plugins, graph libraries, or LLM APIs;
* no duplicated architecture scanner if Architecture Review already has equivalent logic;
* no duplicated workflow checker if Workflow Review already has equivalent logic;
* no duplicated docstring tool if Docstring Assistant already covers it;
* no replacement of Show Project to AI handoff packaging;
* no generated report treated as canonical source.

## 6. Implementation principles

Every new engine must follow these principles:

1. Deterministic first

   * V1 findings must come from code, paths, AST, config files, project metadata, or existing KANDA evidence.
   * AI may explain findings later but must not create primary findings.

2. Read-only by default

   * Engines must not edit target project files.
   * Engines must not write temporary files into the active project root.
   * Engine report output must go only to the dynamic daily-work folder unless a later explicit write feature is approved.

3. No source-truth confusion

   * Engine outputs are generated evidence.
   * Engine outputs help reasoning but never replace exact source inspection before patching.

4. Reuse existing KANDA logic

   * Respect Exclusion Rules.
   * Reuse existing scanners when available.
   * Feed Architecture Review, Workflow Review, Engineering Safety, Show Project to AI, Project Q&A, and Brain Navigator rather than competing with them.

5. Small patches

   * Each patch must introduce one coherent capability.
   * First patch must not include GUI changes unless source audit proves a tiny safe UI hook is better.

6. Validation before expansion

   * No second engine should be implemented until the shared engine contract and Symbol Indexer are validated.

7. Human-readable output

   * Every engine must produce clear, plain-language summaries.
   * Every report must include what was found, why it matters, what to inspect next, and what an AI must not assume.

## 7. Required pre-implementation audit

Before implementing Project Intelligence code, run a source audit.

Purpose:

* avoid duplicating existing KANDA features;
* identify safe integration points;
* identify current project naming conventions;
* identify current exclusion-rule APIs;
* identify current report panel patterns;
* identify existing validation command patterns.

Audit output must include:

```text
PROJECT INTELLIGENCE SOURCE AUDIT

Existing scanner/report utilities:
Existing AST or file-walk utilities:
Existing exclusion-rule API:
Existing validation command logic:
Existing UI report panels:
Existing JSON/report schemas:
Safe integration points:
Potential duplication risks:
Do not touch:
Recommended first patch:
```

No implementation patch should be created before this audit is completed.

## 8. Selected feature list

### 8.1 Selected for implementation

The following features are approved for staged implementation:

1. Project Intelligence base contract
2. Symbol Indexer / Function Indexer
3. Engine Report Formatter
4. Risk Change Radar v1
5. GUI Specs / Tab Audit
6. Error Memory Correlator
7. Validation Command Auto-Discovery
8. Import Dependency Cycle Sentinel
9. Deterministic SAST / Unsafe Operation Scanner
10. Project Health Scan Coordinator
11. Memory Map / Brotherhood Analyzer
12. ADR Writer
13. Property Test Idea Generator
14. File Path Helper

### 8.2 Delayed or lower priority

Delayed until core engines are stable:

* Project Health Scan Coordinator
* Memory Map / Brotherhood Analyzer
* ADR Writer
* Property Test Idea Generator
* File Path Helper

### 8.3 Not to duplicate

Do not reimplement these as separate systems:

* Architecture Review scanner logic
* Workflow Review scanner logic
* Engineering Safety diagnostics
* Docstring Assistant
* Show Project to AI archive/handoff logic
* Freeze Feature write workflow
* Error Memory storage and promotion workflow

## 9. Final implementation order

The canonical implementation order is:

1. Anti-duplication source audit
2. Base engine contract plus Symbol Indexer
3. Engine Report Formatter
4. Risk Change Radar v1
5. GUI Specs / Tab Audit
6. Error Memory Correlator
7. Validation Command Auto-Discovery
8. Import Dependency Cycle Sentinel
9. Deterministic SAST / Unsafe Operation Scanner
10. Project Health Scan Coordinator
11. Memory Map / Brotherhood Analyzer
12. ADR Writer
13. Property Test Idea Generator
14. File Path Helper

This order balances value, safety, dependency structure, and implementation risk.

## 10. Package architecture

Preferred namespace:

```text
kanda_reasoner_app/
    project_intelligence/
        __init__.py
        base_engine.py
        models.py
        scanner.py
        report_formatter.py
        symbol_indexer.py
        risk_radar.py
        gui_spec_audit.py
        error_memory_correlator.py
        validation_command_discovery.py
        import_cycle_sentinel.py
        unsafe_operation_scanner.py
        health_coordinator.py
        memory_map.py
        adr_writer.py
        property_test_ideas.py
        file_path_helper.py
```

Alternative names are allowed only if current source audit shows existing naming conventions that should be followed.

The preferred namespace is `kanda_reasoner_app/project_intelligence/` because it is explicit, isolated, and avoids blending new engine code into existing tabs.

## 11. Shared engine contract

Every Project Intelligence engine must follow a shared contract.

Recommended public interface:

```python
class BaseIntelligenceEngine:
    engine_id: str
    engine_name: str
    engine_version: str

    def run_scan(self, project_root, context_filter=None, options=None):
        raise NotImplementedError

    def to_markdown(self, report):
        raise NotImplementedError
```

V1 should use standard library dataclasses rather than Pydantic unless the current project already depends on Pydantic.

Required output object:

```python
@dataclass(frozen=True)
class EngineFinding:
    finding_id: str
    severity: str
    category: str
    title: str
    message: str
    file_path: str
    line_number: int
    evidence: str
    recommendation: str


@dataclass(frozen=True)
class EngineReport:
    engine_id: str
    engine_version: str
    status: str
    generated_at: str
    project_root_label: str
    summary: str
    findings: list[EngineFinding]
    warnings: list[str]
    errors: list[str]
    next_steps: list[str]
    ai_must_not_assume: list[str]
```

Severity vocabulary:

```text
info
advisory
warning
high
critical
```

Status vocabulary:

```text
ok
completed_with_findings
completed_with_warnings
failed_gracefully
blocked
```

Every engine report must include:

```text
This generated report is advisory evidence. It is not canonical source. Exact source files must be inspected before editing.
```

## 12. Report format

Every engine must support both:

1. JSON-safe output
2. Human-readable Markdown or plain text output

Standard human report sections:

```text
What this found
Why it matters
What to inspect next
What an AI must not assume
Findings
Warnings
Errors
Suggested validation
```

The human report must be written for a non-programmer user first, then provide technical details below.

Avoid jargon in the top summary.

Preferred UI wording:

* "Build project map" instead of "Run Symbol Indexer"
* "Check patch safety" instead of "Run Risk Radar"
* "Audit GUI tabs" instead of "Run Qt Spec Audit"
* "Explain this report" instead of "JSON In, Advice Out"
* "Find repeated mistake risks" instead of "Error Memory Correlator"

## 13. Storage and file placement

Project Intelligence engines are read-only against the active project root.

Default generated report location:

```text
<drive>:\<project>_delete_after_daily_work\intelligence\
```

Examples:

```text
<drive>:\<project>_delete_after_daily_work\intelligence\symbol_indexer.json
<drive>:\<project>_delete_after_daily_work\intelligence\symbol_indexer.md
<drive>:\<project>_delete_after_daily_work\intelligence\risk_radar.json
<drive>:\<project>_delete_after_daily_work\intelligence\risk_radar.md
```

Forbidden locations for transient engine outputs:

```text
<project_root>\
<project_root>\validation\
<project_root>\tests\
<project_root>\kanda_reasoner_app\
```

Exception:

* Source code patches may add real implementation files to the project only through a validated patch.
* Runtime report outputs and temporary artifacts must not be placed in the active project root.

## 14. Exclusion rules

Every engine must respect the existing Exclusion Rules system.

No engine may independently decide to scan:

```text
.git
__pycache__
.venv
venv
env
build
dist
node_modules
*.pyc
generated archives
daily-work folders
excluded project paths
```

File filtering must happen before file reading.

The shared scanner should apply exclusion rules once and pass the filtered file list to engines.

## 15. Performance rules

Project Intelligence must remain fast enough for large projects.

Required performance rules:

1. Shared file walk

   * The project tree should be walked once.
   * Filtered Python file lists should be reused.

2. AST reuse

   * Parse each Python file once per scan run.
   * Reuse parsed ASTs for Symbol Indexer, GUI Specs, Import Cycle Sentinel, and SAST.

3. Incremental cache

   * Cache per-file metadata using path plus mtime or hash.
   * Rescan changed files only when safe.

4. Quick versus deep scan

   * Default should be Quick Scan for UI use.
   * Deep Scan should be explicit.

5. GUI thread safety

   * Heavy scans should not block the main GUI thread once integrated into UI.
   * V1 command/test execution may be synchronous.
   * GUI integration should use the current app's worker/thread pattern if one exists.

6. Large output control

   * Reports should summarize top findings first.
   * Full detail should be expandable or written to report files.

## 16. Validation rules

Every engine patch must include validation.

Minimum validation per engine:

```text
1. Unit or script validation against fixture project.
2. Syntax-error handling test.
3. Exclusion rule handling test when applicable.
4. No-write-to-target-root test.
5. JSON serialization test.
6. Markdown/plain report generation test.
7. Expected validation marker.
8. STATUS: IN_SYNC marker when project contract requires it.
```

Expected marker pattern:

```text
VALIDATION OK: project-intelligence-<engine-id>-v1
STATUS: IN_SYNC
```

Patch ZIP delivery must also include:

```text
ZIP CONTRACT: PASS
```

## 17. First patch canon

The first implementation patch must be:

```text
Project Intelligence Foundation v1
```

It must include:

```text
kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py
```

It must not include:

```text
new GUI widgets
new top-level tabs
AI calls
Freeze Feature writes
Error Memory writes
patch delivery changes
startup delivery changes
prompt-library changes
```

The first patch must be read-only and standard-library only.

Expected validation command:

```text
python tests/test_project_intelligence_symbol_indexer.py
```

Expected validation output:

```text
VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
```

## 18. Feature specifications

### 18.1 Symbol Indexer / Function Indexer

Priority: 1
Risk: low
Value: foundational
Mode: deterministic only

Purpose:

* inspect Python files;
* detect functions, async functions, classes, methods, imports, docstrings, line numbers, and simple ownership metadata;
* produce a reusable symbol map for later engines.

Must detect:

* top-level functions;
* nested functions when feasible;
* classes;
* methods;
* async functions;
* import statements;
* from-import statements;
* docstring present or missing;
* file path;
* line number.

Must not:

* modify files;
* infer behavior beyond available source;
* perform AI summarization;
* scan excluded paths;
* create GUI dependencies.

Initial output:

* JSON report;
* Markdown/plain report;
* summary counts.

Example human summary:

```text
Project map completed. Found 312 functions, 58 classes, and 421 import statements across 96 Python files. This report is advisory and does not replace source inspection before editing.
```

### 18.2 Engine Report Formatter

Priority: 2
Risk: low
Value: high for human usability
Mode: deterministic first

Purpose:

* standardize human-readable explanations for all engine outputs.

Required sections:

* What this found
* Why it matters
* What to inspect next
* What an AI must not assume

Must not:

* invent findings;
* turn advisory reports into authorization to patch;
* hide technical detail entirely.

This may be implemented as `report_formatter.py` or as a method in `base_engine.py` if source audit shows a simpler pattern.

### 18.3 Risk Change Radar v1

Priority: 3
Risk: medium-low
Value: very high
Mode: deterministic only

Purpose:

* identify risk in changed files, proposed patch paths, or selected file paths.

V1 should be path/rule based.

Risk categories:

* GUI risk;
* import risk;
* validation risk;
* freeze-memory risk;
* prompt-routing risk;
* startup-delivery risk;
* patch-delivery risk;
* root-cleanliness risk;
* Error Memory risk;
* generated-file-versus-canonical-source risk.

Examples:

* files under startup delivery paths -> startup-delivery risk;
* files under freeze memory paths -> freeze-memory risk;
* files under prompt_library -> prompt-routing/canon risk;
* files under GUI modules -> GUI workflow risk;
* validation scripts -> validation contract risk;
* installer, ZIP, archive, subprocess, path files -> patch delivery or unsafe operation risk.

Must include:

* risk level;
* reason;
* required source inspection;
* suggested validation commands when discoverable;
* related Error Memory lesson candidates when correlator exists.

V1 must not:

* block patches by itself;
* invent validation success;
* inspect full AST unless Symbol Indexer is already stable.

### 18.4 GUI Specs / Tab Audit

Priority: 4
Risk: medium
Value: high
Mode: deterministic only

Purpose:

* inspect PySide/PyQt GUI code and identify tab workflow risks.

Should detect:

* visible buttons;
* button labels;
* connected callbacks;
* missing callback targets;
* likely run/preview/export/write flows;
* tabs with write actions but no apparent confirmation;
* tab names and tool specs when available;
* UI labels that imply a feature exists without obvious logic.

Destination:

* Workflow Review as "Audit GUI tabs"
* Engineering Safety as a future optional pre-patch GUI risk input

Must not:

* auto-edit GUI files;
* assume a missing callback is definitely broken without evidence;
* block patching without human review.

### 18.5 Error Memory Correlator

Priority: 5
Risk: medium
Value: very high
Mode: deterministic first

Purpose:

* compare current risks or touched files against compact Error Memory lessons.

Examples:

* patch touches installer/root staging logic -> correlate with delete-after-daily-work lesson;
* patch touches Project Q&A imports -> correlate with import-path regression lesson;
* validation output lacks `STATUS: IN_SYNC` -> correlate with validation marker lesson;
* response includes isolated ZIP -> correlate with no-isolated-ZIP lesson.

Must read:

* compact Error Memory export;
* lesson IDs;
* triggers;
* do-not-repeat rules;
* regression checks.

Must not:

* edit Error Memory;
* promote lessons;
* open full Error Memory by default;
* treat compact lesson text as source code truth.

Output:

* related lesson IDs;
* match strength: exact, partial, weak, none;
* avoidance rule;
* next safe action.

### 18.6 Validation Command Auto-Discovery

Priority: 6
Risk: medium-low
Value: high
Mode: deterministic only

Purpose:

* find likely validation commands for the project or patch.

Should inspect:

* validation/ directory;
* tests/ directory;
* pyproject.toml;
* pytest.ini;
* tox.ini;
* README validation sections;
* existing KANDA validation scripts;
* known expected markers.

Must output:

* candidate command;
* confidence;
* why it was selected;
* expected marker if discoverable;
* warning if command is inferred.

Must not:

* run commands automatically without user action;
* claim validation passed;
* replace patch-specific validation instructions.

### 18.7 Import Dependency Cycle Sentinel

Priority: 7
Risk: medium
Value: high
Mode: deterministic only

Purpose:

* detect circular imports and high-risk dependency relationships.

Should build on:

* Symbol Indexer import data;
* shared scanner.

Must output:

* cycle path;
* files involved;
* import lines where available;
* likely risk;
* suggested inspection.

Must not:

* rewrite imports;
* auto-resolve cycles;
* treat optional imports as definitely wrong without context.

### 18.8 Deterministic SAST / Unsafe Operation Scanner

Priority: 8
Risk: medium
Value: high
Mode: deterministic only in V1

Purpose:

* detect unsafe operations relevant to KANDA's responsibilities.

Rules should include:

* eval;
* exec;
* subprocess with shell=True;
* unsafe ZIP extraction patterns;
* path traversal risk;
* hardcoded absolute project roots;
* writes directly to project root;
* broad delete operations;
* secret-looking tokens;
* shell command construction from unchecked input.

Must be optional at first.

Must not:

* require Bandit;
* require internet;
* produce AI-only security findings;
* block all patching automatically.

### 18.9 Project Health Scan Coordinator

Priority: 9
Risk: medium
Value: high after prior engines exist
Mode: aggregation only

Purpose:

* aggregate existing Architecture Review, Workflow Review, Refactor Report, Symbol Indexer, Risk Radar, GUI Audit, and SAST findings.

Must not:

* duplicate scanner logic;
* become a parallel Architecture Review;
* run heavy deep scans without user awareness.

Output:

* health summary;
* biggest risk;
* top next actions;
* report links.

### 18.10 Memory Map / Brotherhood Analyzer

Priority: 10
Risk: high
Value: potentially high
Mode: delayed

Purpose:

* group related files, functions, classes, and modules into project families.

Depends on:

* stable Symbol Indexer;
* stable Import Cycle Sentinel;
* stable Health Coordinator or shared evidence format.

Must not:

* be implemented early;
* use vague AI grouping as primary logic;
* replace exact source inspection.

### 18.11 ADR Writer

Priority: 11
Risk: medium
Value: governance value
Mode: template first

Purpose:

* draft Architecture Decision Records after validated changes.

Must require:

* preview;
* explicit human confirmation before writing;
* validation evidence;
* linked feature ID or patch ID;
* optional freeze reference.

Must not:

* write automatically;
* bypass Freeze Feature confirmation;
* invent validation evidence.

### 18.12 Property Test Idea Generator

Priority: 12
Risk: low-medium
Value: niche
Mode: advisory only

Purpose:

* suggest property-based test ideas for pure functions, parsers, validators, and transformation logic.

Must not:

* auto-add tests in V1;
* create noisy or speculative test files;
* require Hypothesis unless separately approved.

### 18.13 File Path Helper

Priority: 13
Risk: low
Value: small UX improvement
Mode: utility only

Purpose:

* help user copy/select important paths for AI handoff or manual review.

Must not:

* duplicate Show Project to AI source archive logic;
* create a new tab;
* become a second handoff generator.

## 19. UI integration canon

No engine should get a new top-level tab by default.

Preferred destinations:

```text
Symbol Indexer -> Brain Navigator, Project Q&A, Architecture Review
Risk Change Radar -> Engineering Safety, patch preflight
GUI Specs / Tab Audit -> Workflow Review
Error Memory Correlator -> Engineering Safety, Error Memory, patch preflight
Validation Command Auto-Discovery -> Engineering Safety, patch delivery
Import Cycle Sentinel -> Architecture Review, Engineering Safety
SAST Scanner -> Engineering Safety
Health Coordinator -> Brain Navigator, Architecture Review, Engineering Safety
Memory Map -> Brain Navigator, Refactor Report
ADR Writer -> Architecture Review, Freeze Feature
Property Test Ideas -> Engineering Safety
File Path Helper -> Show Project to AI
```

UI wording must avoid developer-only jargon.

Use plain labels:

* Build project map
* Check patch safety
* Audit GUI tabs
* Find repeated mistake risks
* Suggest validation command
* Check import cycles
* Scan unsafe operations
* Create health summary

## 20. Patch delivery requirements

Any patch implementing this canon must follow normal KANDA patch delivery rules.

Patch delivery must include:

* patch ZIP;
* install instructions;
* validation instructions;
* expected validation markers;
* freeze handling when applicable;
* Error Memory handling when applicable.

No isolated ZIP delivery is allowed.

Install and temporary files must be staged under:

```text
<drive>:\<project>_delete_after_daily_work\
```

Patch ZIPs that are freezeable must include root-level:

```text
KANDA_FREEZE_HINT.json
```

unless explicitly declared non-freezeable with reason.

## 21. Freeze policy

Project Intelligence engine implementation patches may become freezeable after validation.

However:

* engine report outputs do not automatically become freeze memory;
* ADR Writer must not write ADRs without confirmation;
* Freeze Feature Confirm and Write must remain explicitly human-confirmed;
* validation evidence must include expected markers before freeze.

## 22. Error Memory policy

Before code editing:

* read compact Error Memory;
* apply relevant avoidance rules;
* do not open full Error Memory unless needed.

Project Intelligence features must not write active Error Memory automatically.

Error Memory Correlator may:

* read compact lessons;
* report related lesson IDs;
* warn about repeated risk patterns.

Error Memory Correlator must not:

* create lessons;
* promote lessons;
* alter active memory;
* open full memory by default.

## 23. AI usage policy

V1 engines must be deterministic.

Allowed AI usage later:

* explain deterministic findings;
* rewrite a human-readable summary;
* suggest next questions;
* draft ADR text from validated evidence;
* suggest test ideas from already-detected pure functions.

Forbidden AI usage:

* creating primary findings without deterministic evidence;
* claiming validation passed;
* deciding freeze eligibility without validation evidence;
* replacing source inspection;
* silently editing project files.

Canonical rule:

```text
AI explains and helps prioritize. Deterministic engines detect.
```

## 24. Acceptance checklist for first patch

First patch is accepted only if all are true:

```text
[ ] Source audit completed.
[ ] No duplicate existing scanner was created.
[ ] project_intelligence package added in isolated namespace.
[ ] Base engine contract exists.
[ ] Shared report models exist.
[ ] Symbol Indexer detects functions, classes, methods, imports, line numbers, and docstring presence.
[ ] Syntax errors are handled gracefully.
[ ] Excluded paths are not scanned.
[ ] No files are written to active project root during scan.
[ ] JSON report can serialize.
[ ] Human-readable report can render.
[ ] Validation script passes.
[ ] Validation output includes expected marker.
[ ] STATUS: IN_SYNC is present if required by current contract.
[ ] Patch ZIP contract passes.
```

## 25. Required first validation script behavior

The first validation script must:

* create or use a small fixture project;
* include at least one top-level function;
* include at least one async function;
* include at least one class;
* include at least one method;
* include at least one nested function if supported;
* include at least one import and one from-import;
* include at least one syntax-error file to test graceful failure;
* assert no output is written to the target fixture root;
* assert JSON output is valid;
* assert report text contains advisory source-truth warning.

Required final print markers:

```text
VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
```

If patch ZIP validation is included:

```text
ZIP CONTRACT: PASS
```

## 26. Future implementation rule

After each implemented feature, update this canon only if:

* the implementation revealed a better safe architecture;
* a feature was rejected;
* an engine was merged into existing logic;
* a validation rule changed;
* a new high-value engine was discovered.

Do not update this canon to justify scope creep.

Every future update must preserve:

* internal engines over new tabs;
* deterministic V1;
* no source-truth confusion;
* no root transient files;
* explicit human confirmation for writes;
* compact Error Memory before editing;
* exact source inspection before patching.

## 27. Canon summary

KANDA Reasoner's Project Intelligence layer should be implemented as a small, deterministic, shared, read-only engine system that feeds existing tabs.

Implementation must start with:

```text
Anti-duplication audit
Base engine contract
Symbol Indexer
```

Only after that should KANDA add:

```text
report formatting
risk radar
GUI audit
Error Memory correlation
validation discovery
import cycle detection
unsafe operation scanning
```

Large synthesis tools such as Memory Map, Health Coordinator, ADR Writer, and Property Test Ideas must wait until the foundation is stable.

The final design objective is:

```text
Make KANDA Reasoner safer, clearer, and more useful for a human directing AI-assisted development, without adding unnecessary tabs or duplicating existing app logic.
```
