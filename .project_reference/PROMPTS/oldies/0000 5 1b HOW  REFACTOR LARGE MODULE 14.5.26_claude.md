PyArchitect — Master Refactor Prompt v5
"Unified Production" Edition
Zero-drift · AI-aware · No-tooling-required · Scales large · Explains why · CI‑ready · Domain‑overlay capable
DESIGN PHILOSOPHY (immutable) -SOLID and DRY

    THE CODE IS THE ONLY SOURCE OF TRUTH.
    Manifests and AI‑context headers are derived from the code, never hand‑authored in parallel.
    This eliminates drift by construction.

    Minimal headers → low maintenance

    Manifest generated → never contradicts code

    Generator = Validator → one script, two modes, zero duplication

    Manifest is plain JSON → paste‑able into any AI chat

Workflow:
EDIT CODE → RUN GENERATOR → COMMIT (code + manifest together)

AI workflow:
PASTE MANIFEST INTO CHAT → AI edits code → RE-RUN GENERATOR
INPUTS (fill before using)
Required	Description
ORIGIN_FILE	Path to the large module to refactor (e.g., a_py_file.py)
HELP_FOLDER	Folder where extracted helpers will live (e.g., a_py_file_help/)
MANIFEST_FILE	Path to the JSON manifest (e.g., a_py_file_help.json)
TOOL_SCRIPT	Path to the reusable generator/validator script (recommend tools/manifest_tool.py)
REFACTOR_GOAL	One sentence describing what logic to isolate (e.g., "separate a_py_file detection, validation, IO")

Optional v5 additions:

    ENTRY_RENAME – new name for entry point (default: keep original)

    TEST_COMMAND – shell command to run unit tests (e.g., pytest tests/test_a_py_file.py)

    DOMAIN_OVERLAY – one of: "EEG", "FINANCE", "GENERIC" (default: "GENERIC").
    When "EEG", the Project Overlay (Section E) applies.

Tool script location (v5):

    Single reusable script placed once in repository root or tools/.

    Per‑module config: <HELP_FOLDER>/../.refactor_config.json (or same folder as ORIGIN_FILE).

    Example config:

json

{
  "origin": "a_py_file.py",
  "help_folder": "a_py_file_help/",
  "manifest": "a_py_file_help.json",
  "refactor_goal": "separate a_py_file detection, validation, and IO",
  "entry_rename": null,
  "test_command": "pytest tests/test_a_py_file.py",
  "domain_overlay": "EEG",
  "pattern_hint": null
}

TASK 0 — PRE‑REFACTOR ANALYSIS (Phase‑0 gates)

Before any code is written, perform these checks and show results:
0.1 Structural Audit

    ARCHITECTURE.md exists at project root and is current?

    Package map lists all packages with their prefixes?

    __init__.py per package re‑exports + __all__ + submodule list?

    Any file ≥300 lines? (warn)

    Any file ≥500 lines? (block – split required)

    Duplicate symbol names detected across files?

0.2 Roadmap Authority Gate

If multiple plans exist, declare exactly one authoritative roadmap for this phase.
List conflicts resolved.
0.3 Phase Scope Lock

Freeze what is in scope and out of scope for this refactor.
If a later‑phase subsystem is deferred but its data contract is needed, define the contract early (defer only I/O).
0.4 Folder Ownership Mapping

If new folders are proposed, produce a mapping:
new folder → current closest owner → relationship (NEW / REPLACES / COEXISTS / TEMPORARY SHIM / RENAME TARGET)
0.5 Decision Table Gate (if ambiguous inference is required)

Write a priority‑ordered decision table with:

    highest‑authority evidence

    allowed heuristics

    confidence / ambiguity states

    fallback to unknown / mixed

    user‑visible consequence flags

If a domain overlay provides frozen canon, inherit it exactly unless explicit approval to change.
0.6 Evidence Limits

State: runtime observed? (yes/no), static blind spots, confidence level.

→ STOP. Wait for approval before Task 1.
TASK 1 — ROADMAP & FILE DECOMPOSITION

Analyze ORIGIN_FILE and produce a refactoring roadmap.

    Identify logical units (classes, functions, groups) that can be extracted.

    Propose canonical names for each helper file inside HELP_FOLDER:

        snake_case

        describes single responsibility

        forbidden: utils.py, helpers.py, misc.py, common.py

        exception: _constants.py allowed (constants only, __all__ = [])

    For each proposed helper file state:

        filename

        purpose (one line)

        symbols (classes/functions)

        intra-folder depends_on

        stability: stable | internal | migrating

        reason: one sentence why this boundary exists

    Show full folder structure.

    If DOMAIN_OVERLAY provides naming rules (e.g., EEG temporal/parietal canon), enforce them.

→ STOP. Wait for approval before Task 2.
TASK 2 — WRITE THE HELPER FILES
Mandatory Minimal Header (every helper file)
python

# ──────────────────────────────────────────────────────────
# ORIGIN   : <ORIGIN_FILE>
# PURPOSE  : one-line description
# REASON   : one sentence why this boundary exists
# STABILITY: stable | internal | migrating
# ──────────────────────────────────────────────────────────

Everything else (exports, depends_on, consumed_by) is read directly from __all__ and import statements by the generator.
__all__ rules (v5)

    Every helper file must define __all__ at module level.

    If the file has public symbols – list them.

    If the file is internal only (no public API) – set __all__ = [] and prefix all symbols with _.

    For _constants.py, __all__ = [] is required, and only constants (no functions/classes).

Helper‑file rules

    Single responsibility per file, no exceptions.

    Explicit imports between helpers (never import *).

    No circular imports.

    No catch‑all modules unless explicitly approved.

Domain‑specific header additions (optional)

If DOMAIN_OVERLAY defines extra header fields (e.g., EEG_CANON_RULE), include them after STABILITY.
TASK 3 — UPDATE THE ORIGIN FILE

Replace extracted logic with imports from helpers.
Add this AI CONTEXT docstring at the very top (below shebang/encoding):
python

"""
<Original module one-line description>

╔══════════════════════════════════════════════════════════╗
║  ⚠  AI CONTEXT — REFACTORED MODULE                      ║
║                                                          ║
║  This file is the sole public entry point.               ║
║  All logic lives in the helper submodules below.         ║
║                                                          ║
║  MANIFEST : <MANIFEST_FILE>                              ║
║  FOLDER   : <HELP_FOLDER>                                ║
║  EXPOSES  : <comma-separated public symbols — generated> ║
║                                                          ║
║  ➜ Paste MANIFEST_FILE into chat before editing.         ║
║  ➜ Run TOOL_SCRIPT after any edit to keep manifest fresh.║
╚══════════════════════════════════════════════════════════╝
"""

Keep ORIGIN_FILE as the single public entry point – all original public symbols must remain importable from it.
Define __all__ matching the public API.
No duplicate logic left behind unless a helper is marked migrating.
TASK 4 — MANIFEST SCHEMA (generated, not hand‑written)

The manifest is produced by running TOOL_SCRIPT --generate.
Schema (v5):
json

{
  "origin": "<ORIGIN_FILE>",
  "entry_point": "<ORIGIN_FILE>",
  "help_folder": "<HELP_FOLDER>",
  "refactor_date": "YYYY-MM-DD",
  "refactor_goal": "<REFACTOR_GOAL>",
  "pattern": "pipeline | strategy | service | state_machine | registry | facade | mixed",
  "pattern_note": "one-line description of data/control flow",
  "generated_by": "<TOOL_SCRIPT>",
  "ai_instruction": "Paste this manifest into chat before editing any file.",
  "summary": {
    "total_helpers": 12,
    "public_helpers": 10,
    "internal_helpers": 2,
    "entry_exports": ["classA", "functionB"],
    "high_level_flow": "validation → detection → transformation"
  },
  "helpers": {
    "<helper.py>": {
      "purpose": "<from header>",
      "reason": "<from header>",
      "stability": "<from header>",
      "exports": ["<from __all__>"],
      "depends_on": ["<intra-folder imports>"],
      "consumed_by": ["<inverse of depends_on>"]
    }
  },
  "dependency_graph": {
    "<helper.py>": {
      "<depended.py>": "inherits | instantiates | calls | type only | decorates | context_manager | protocol | uses"
    }
  },
  "domain_overlay": "<GENERIC | EEG | ...>",
  "domain_specific": { }
}

Key properties:

    purpose, reason, stability from minimal header (only human input).

    exports from __all__ – never mismatches.

    depends_on from parsed imports – never mismatches.

    consumed_by computed as symmetric inverse.

    dependency_graph annotations auto‑detected (heuristics) – may be manually refined.

TASK 5 — CREATE/REUSE THE TOOL SCRIPT

Do not generate per‑module copies. Use a single manifest_tool.py in your repository root or tools/.

The tool reads .refactor_config.json (next to ORIGIN_FILE or in parent directory).
Commands
bash

# Generate manifest for a module
python manifest_tool.py --config .refactor_config.json --generate

# Validate (CI mode)
python manifest_tool.py --config .refactor_config.json --validate

# Scan entire project (finds all .refactor_config.json)
python manifest_tool.py --scan-project

# Generate + run tests
python manifest_tool.py --config .refactor_config.json --generate --test

# Deep annotation mode (detects decorators, context managers, protocols)
python manifest_tool.py --config .refactor_config.json --generate --annotate-deep

# Show incremental refactor state
python manifest_tool.py --config .refactor_config.json --state

Required features of the tool script
Mode	Behaviour
--generate	Parse headers, __all__, imports; auto‑detect pattern (if not set in config); compute dependency annotations; write manifest; update EXPOSES in origin file docstring.
--validate	Regenerate manifest in memory; compare to disk; any difference → error. Also check: circular imports, mandatory headers, __all__ exists, stability values, pattern not empty.
--scan-project	Recursively find all .refactor_config.json, run --validate on each, print summary. Exit code 0 only if all pass.
--test	Run TEST_COMMAND from config; if fails, abort manifest write.
--annotate-deep	Use AST to detect decorators, context managers, protocol usage, higher‑order calls.
--state	Show incremental refactor state (.refactor_state.json).
Incremental refactoring state (optional)

If the refactor spans multiple commits, the tool maintains .refactor_state.json:
json

{
  "version": 1,
  "moved_symbols": {
    "validate_landmark": "validation.py",
    "detect_peaks": "detection.py"
  },
  "remaining_in_origin": ["load_data", "save_result"]
}

When --generate runs, the tool warns if a symbol is moved twice or left behind incorrectly.
Circular dependency handling

When --validate detects a cycle, it prints:
text

❌ Circular import detected: A.py → B.py → C.py → A.py
   Suggested fixes:
     1. Move shared interface to a new _types.py file.
     2. Invert dependency: make B depend on an abstract class in A.
     3. Use a callback or event bus.

TASK 6 — VERIFICATION (Three‑Pass Review)

Before delivering any files, run these passes and show results:
PASS 1 — Syntax & Completeness

    Valid Python syntax throughout?

    All imports resolve to files that exist in this refactor?

    No truncated functions/classes?

    No placeholder comments (# ..., # TODO, # rest unchanged)?

    All __init__.py re‑exports match actual symbols in helper files?

    __all__ matches re‑exports exactly?

PASS 2 — Consistency & Duplication

    No symbol defined in more than one file?

    No logic duplicated across files?

    All tombstones in origin files point to correct destination?

    File‑level docstrings match actual EXPORTS and DEPENDS?

    Cross‑file references symmetric? (if A says "USED BY B", B says "DEPENDS A")

PASS 3 — Logic, Scope & Architecture

    No business logic inside __init__.py?

    Each file owns exactly one responsibility?

    No circular imports introduced?

    ARCHITECTURE.md Navigation Quick‑Reference lists every public symbol?

    Decision Log updated with reason for every structural change?

    Line counts: no file above 500 lines?

    Locked phase scope respected?

    Domain decision tables implemented exactly as approved?

If any check fails → fix immediately → re‑run passes → only proceed when all passes are clean.
TASK 7 — DELIVERY & TERMINAL TEST
Deliverables (as a zip file)

    ARCHITECTURE.md (updated)

    All __init__.py files (one per package, outermost first)

    All new helper files (in dependency order)

    Modified ORIGIN_FILE

    .refactor_config.json

    manifest_tool.py (if not already in project)

    Any migration state files (.refactor_state.json)

Terminal validation commands to include
bash

# Generate fresh manifest
python manifest_tool.py --config .refactor_config.json --generate

# Validate everything
python manifest_tool.py --config .refactor_config.json --validate

# Run unit tests (if test_command defined)
python manifest_tool.py --config .refactor_config.json --generate --test

# Project‑wide validation
python manifest_tool.py --scan-project

Final checklist (v5)

    All helper files exist in HELP_FOLDER

    All helper files have the 4‑field minimal header (ORIGIN, PURPOSE, REASON, STABILITY)

    All helper files define __all__ (may be [] for internal)

    _constants.py (if any) contains only constants and __all__ = []

    ORIGIN_FILE has the AI CONTEXT docstring with correct EXPOSES line

    ORIGIN_FILE defines __all__ matching its public API

    All original public symbols are still exported from ORIGIN_FILE

    .refactor_config.json exists and is valid

    python manifest_tool.py --config ... --generate runs without errors

    python manifest_tool.py --config ... --validate exits with code 0

    python manifest_tool.py --scan-project exits with code 0

    No circular imports – if found, resolved

    No migrating files older than this refactor session

    PATTERN and pattern_note filled meaningfully (tool auto‑detects)

    All dependency graph edges have annotations (tool defaults to "uses")

    Unit tests pass after --generate --test

    Incremental state file (if used) correctly reflects remaining work

PROJECT OVERLAY — EEG IMPORT / PRE‑FILTER MIGRATION (v5)

Apply this overlay only when DOMAIN_OVERLAY = "EEG".
When active, it replaces generic naming rules with EEG‑specific canon.
E.1 Protected Truth Hierarchy

    RawOriginal owns imported acquisition truth

    RawCanonical owns stable working child truth

    ViewLayout owns display‑only ordering and visibility

    PlotWindow owns UI‑facing unfiltered render payload

    Filters, rereferencing, export, plugins, UI never own truth

E.2 Mandatory Scope Lock (pre‑filter phase)

In scope:

    file import / format dispatch

    RawOriginal creation

    AcquisitionProfile inference

    channel normalization / registry / type classification

    RawCanonical building

    ViewLayout building

    unfiltered PlotWindow building

    shell orchestration for new path

    user notice hook for non‑reversible bipolar truth

Out of scope (unless re‑authorized):

    CAR / LAR / bipolar derived views

    filter engine

    padded DSP processing

    export

    pseudo‑reconstruction

    persistence I/O (except contracts)

E.3 External Source‑of‑Truth Canon for EEG Code

    Official MNE stable documentation (https://mne.tools/stable) is the first external source of truth.

    Secondary sources may be used only as support, and must not override frozen project canon.

    If MNE documents multiple possibilities, project canon chooses behavior.

    If MNE does not define clinical naming canon, project canon governs.

E.4 Frozen EEG Label / Role Canon
E.4.1 Canonical text normalization

Before semantic decision:

    trim whitespace, collapse separators/underscores, case‑insensitive

    treat obvious alphanumeric variants as same label when unambiguous

    Example: fP1, __FP__1, fpone → Fp1

E.4.2 Temporal/parietal canon (immutable)

    Canonical clinical truth: T3, T4, T5, T6

    Newer labels are aliases only: T7→T3, T8→T4, P7→T5, P8→T6

E.4.3 Reference evidence canon

Recognized reference hints:

    A1, A2, M1, M2, TP9, TP10 (as evidence, not automatic truth)

    Metadata/text: referential, linked ears, average, REST, bipolar

E.4.4 Auxiliary channel canon

EMG, ECG, EOG families → auxiliary, not EEG truth.
They may be displayed but never counted as canonical EEG truth channels.
E.4.5 Contradictory role evidence

If MNE says EEG but label indicates ECG/EOG/EMG → contradictory.
Required: mark contradictory, surface to user, require manual resolution.
E.4.6 Resolution precedence

    Manual override

    Exact canonical truth‑name match

    Exact known‑alias match

    Normalized canonical/alias match

    Unresolved

E.4.7 Manual override canon

    Override outranks automatic inference

    No duplicate canonical EEG truth names allowed

    Contradictory auxiliary roles must be explicitly chosen

    Override must be traceable (user action, timestamp)

    Unresolved and conflict states remain representable

E.5 Acquisition Inference Decision Table (EEG)
Priority	Condition	Result
1	MNE metadata explicitly says average reference (proj present)	CAR_REFERENCED
2	Channel names contain - and pattern matches known bipolar pairs (e.g., Fp1-F7)	BIPOLAR_LABELLED
3	A1 and A2 present in channel list	REFERENTIAL_WITH_EARS
4	A1 or A2 present (one only)	REFERENTIAL_ONE_EAR
5	No reference channels, no bipolar labels, EEG names recognized	REFERENTIAL_UNKNOWN_REF
6	Cannot determine	UNKNOWN

Reversibility rule: Only BIPOLAR_LABELLED without source referential channels → NON_REVERSIBLE_BIPOLAR + limitation notice.
E.6 Coexistence Rule for Legacy EEG Path

Declare:

    Current legacy path: loader → preprocess → visualizer chain

    Future target path: ImportGateway → RawOriginal → AcquisitionProfile → ChannelRegistry → RawCanonical → ViewLayout → PlotWindow → viewer

    Retirement order: loader authority → preprocess authority → viewer wiring

Only one path may be the declared canonical owner at a time.
E.7 Validation Milestone (EEG phase)

    Supported EEG formats open through new import path

    Imported truth remains protected

    Acquisition classification deterministic

    Imported order preserved internally

    Display layout separate from structural truth

    Viewer can render unfiltered trace through PlotWindow

    Legacy mixed import/preprocess ownership no longer required for live path

ABSOLUTE CONSTRAINTS (never violated)

    Never show partial file contents – always complete, always runnable.

    Never proceed past Task 0 without receiving actual file contents.

    Never execute against two conflicting roadmaps at once.

    Never create a new folder/package without explicit user authorization.

    Never create a new branch without a folder ownership map.

    Never implement ambiguous inference without a written decision table.

    Never redefine frozen domain canon without explicit user approval.

    Never name a file without its module prefix (exception: _constants.py).

    Never reuse a symbol name that exists elsewhere in the project.

    Never deliver a file that failed any verification check.

    Never skip the three‑pass review, even for trivial changes.

    Never say “it might be in another file” – trace ARCHITECTURE.md first.

    Never add logic to __init__.py.

    Never let a file reach 500 lines without invoking the Split Protocol.

    Never leak later‑phase behavior into a locked earlier‑phase refactor.

INSTRUCTIONS FOR THE AI (using this prompt)

    Fill the INPUTS section with the actual paths and goal.

    Execute Task 0 and show results → wait for approval.

    Execute Task 1 (roadmap) → wait for approval.

    Execute Task 2 (write helpers, one file at a time, pausing after each).

    Execute Task 3 (update origin file).

    Execute Task 4 (manifest is generated via tool – you may need to instruct user to run the tool).

    Ensure Task 5 (tool script) exists – if not, provide the single manifest_tool.py.

    Perform Task 6 (three‑pass review) and show results.

    Deliver Task 7 (zip + terminal commands).

Remember: The AI never runs the tool script – that is the user’s responsibility. The AI writes code that conforms to the schema so that when the user runs the tool, validation passes.

*This prompt is the result of merging v3/v4 architectural intent, PyRefactor execution protocol, EEG project overlay, and production‑hardened CI practices. Use it to refactor any large module with zero drift and complete AI traceability.*

REFACTOR REQUEST – EXECUTION DEMAND

Using the PyArchitect Master Refactor Prompt v5 (Unified Production Edition) and the provided scalp_landmark_seed.py file, perform a complete refactoring following all tasks from Task 0 through Task 7.

Specific requirements:

    Refactor the main file

        Original file: scalp_landmark_seed.py (in the current folder)

        Extract all logical units into helper files located in a new folder:
        scalp_landmark_seed_help/

        The original file must become a thin public entry point that re‑exports all original public symbols via imports from the helpers.

    Produce a ZIP package

        Include all created and modified files in the correct folder structure:

            Updated scalp_landmark_seed.py

            All helper files under scalp_landmark_seed_help/

            The tool script manifest_tool.py (reusable, placed at project root or tools/)

            The per‑module config .refactor_config.json (next to the origin file)

            Any incremental state file (.refactor_state.json) if needed

    Provide Windows terminal test codes

        After delivering the ZIP, give a copy‑pasteable block of Windows terminal commands that will:

            Generate the manifest (--generate)

            Validate the refactor (--validate)

            Optionally run unit tests (--test) if a test command is defined in the config

            Project‑wide scan (--scan-project) to ensure no other module is broken

    All commands must assume the user is in the directory where scalp_landmark_seed.py lives.

    Validation criteria

        The original module must still export all original public symbols.

        No file may exceed 500 lines.

        No circular imports.

        Every helper file must have the mandatory 4‑field header (ORIGIN, PURPOSE, REASON, STABILITY).

        Every helper file must define __all__ (may be [] for internal helpers).

        The manifest must pass --validate with exit code 0.

Proceed immediately with the refactor following the prompt’s mandatory pause points (Task 0 audit, Task 1 roadmap approval, etc.). Deliver the ZIP and terminal test codes as the final output.

This version is specific, actionable, and references the exact prompt sections. It also respects the AI’s required stop‑and‑wait points.