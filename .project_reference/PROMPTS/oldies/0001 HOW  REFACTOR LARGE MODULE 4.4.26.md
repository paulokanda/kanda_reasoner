Master Refactor Prompt Template

You are a senior Python architect. I need to refactor a large Python module
into smaller, cohesive helper submodules, following a strict traceability
convention so that any AI assistant or developer can understand the
relationships between files at any entry point.

═══════════════════════════════════════════
INPUTS (fill these before using the prompt)
═══════════════════════════════════════════

ORIGIN_FILE        = <path/to/original_file.py>
HELP_FOLDER        = <path/to/original_file_help/>
MANIFEST_FILE      = <path/to/original_file_help.json>
VALIDATOR_SCRIPT   = <same folder as ORIGIN_FILE>/<origin_base_name>_validate_manifests.py
REFACTOR_GOAL      = <describe what logic you want isolated, e.g.:
                      "isolate all filter logic into independent filter modules">

Validator naming/location rule:
- VALIDATOR_SCRIPT must live in the same folder as ORIGIN_FILE
- VALIDATOR_SCRIPT filename must be:
  <origin_base_name>_validate_manifests.py
- Example:
  ORIGIN_FILE      = core/signal/eeg_filter_state.py
  VALIDATOR_SCRIPT = core/signal/eeg_filter_state_validate_manifests.py

═══════════════════════════════════════════════
TASK 1 — ROADMAP & FILE DECOMPOSITION
═══════════════════════════════════════════════

Analyze ORIGIN_FILE and produce a refactoring roadmap:

1. Identify logical units inside ORIGIN_FILE that can be extracted
   (classes, functions, groups of related functions).

2. Propose canonical names for each new helper file inside HELP_FOLDER.
   Naming rules:
     - snake_case
     - name must describe the single responsibility of the file
     - no generic names like "utils.py" or "helpers.py"

3. For each proposed helper file state:
   - filename
   - single-line purpose
   - which symbols (classes/functions) it will contain
   - which other helper files it depends on (intra-folder deps)

4. Show the full proposed folder structure before writing any code.

5. Wait for my approval before proceeding to Task 2.

═══════════════════════════════════════════════
TASK 2 — WRITE THE HELPER FILES
═══════════════════════════════════════════════

For each helper file identified in Task 1, produce the full file content
following this mandatory header convention at the top of EVERY helper file:

  # ──────────────────────────────────────────────────────
  # MODULE ORIGIN : <ORIGIN_FILE>
  # MANIFEST      : <MANIFEST_FILE>
  # HELP FOLDER   : <HELP_FOLDER>
  # PURPOSE       : <one-line description of this file>
  # EXPORTS       : <comma-separated list of public symbols>
  # DEPENDS ON    : <other helper files this file imports from, or "none">
  # REFACTOR DATE : <today's date YYYY-MM-DD>
  # ──────────────────────────────────────────────────────

After the header, write clean, production-ready Python code.

Mandatory public-API rule:
- Every origin file and helper file that declares EXPORTS/EXPOSES
  must also define an explicit __all__ list.
- __all__ must exactly match the declared exported symbols.
- Any top-level helper function, alias, logger, constant, or validator-only
  utility that is not part of the intended public API must be underscore-prefixed.

Helper-file rules:
- Keep helpers cohesive and single-responsibility.
- Prefer explicit imports between helper files.
- Avoid circular imports.
- Do not introduce generic catch-all modules unless I explicitly approve them.

═══════════════════════════════════════════════
TASK 3 — UPDATE THE ORIGIN FILE
═══════════════════════════════════════════════

Update ORIGIN_FILE to:

1. Replace extracted logic with imports from the new helper files.

2. Add this docstring at the very top (below the shebang/encoding if any):

  """
  <Original module one-line description>

  ╔══════════════════════════════════════════════════════╗
  ║  ⚠️  AI CONTEXT — REFACTORED MODULE                  ║
  ║                                                      ║
  ║  This module has been decomposed into submodules.    ║
  ║  MANIFEST : <MANIFEST_FILE>                          ║
  ║  FOLDER   : <HELP_FOLDER>                            ║
  ║                                                      ║
  ║  ➜ Read the manifest before editing any logic here.  ║
  ╚══════════════════════════════════════════════════════╝
  """

3. Keep ORIGIN_FILE as the single public entry point —
   all symbols must remain importable from it.

4. ORIGIN_FILE must define an explicit __all__ that exactly matches
   its public API after the refactor.

5. Do not leave partial duplicate logic behind in ORIGIN_FILE unless
   I explicitly request a staged migration.

═══════════════════════════════════════════════
TASK 4 — CREATE / UPDATE THE JSON MANIFEST
═══════════════════════════════════════════════

Create or update MANIFEST_FILE with this exact schema:

{
  "origin"        : "<ORIGIN_FILE>",
  "help_folder"   : "<HELP_FOLDER>",
  "refactor_date" : "<YYYY-MM-DD>",
  "refactor_goal" : "<REFACTOR_GOAL>",
  "ai_instruction": "Read this manifest before editing any file in help_folder or origin.",
  "helpers": {
    "<helper_filename.py>": {
      "purpose"   : "<one-line description>",
      "exports"   : ["<SymbolA>", "<SymbolB>"],
      "depends_on": ["<other_helper.py>"]
    }
  },
  "dependency_graph": {
    "<helper_filename.py>": ["<files it imports from inside help_folder>"]
  }
}

Rules:
- Every file in HELP_FOLDER must appear in "helpers".
- "dependency_graph" must be consistent with "depends_on" fields.
- Do not list external packages in depends_on, only intra-folder files.
- __init__.py must be listed if it is part of the helper subpackage API.
- If a helper exports symbols, its manifest "exports" must match the file’s __all__ exactly.

═══════════════════════════════════════════════
TASK 5 — CREATE / UPDATE THE CI VALIDATOR
═══════════════════════════════════════════════

Create or update VALIDATOR_SCRIPT.

VALIDATOR_SCRIPT must:
- live in the same folder as ORIGIN_FILE
- be named <origin_base_name>_validate_manifests.py
- validate ALL manifests in the project, not just this one

The script must:

1. Scan the project recursively for all *_help.json files.

2. For each manifest:
   a. Check every file listed in "helpers" physically exists in help_folder.
   b. Check every file in help_folder appears in "helpers"
      (ignoring __pycache__ and optionally excluding files the manifest
       explicitly marks as non-helper support files if that convention exists).
   c. Check every file listed in "depends_on" exists in help_folder.
   d. Check every helper file contains the mandatory header fields:
        MODULE ORIGIN, MANIFEST, HELP FOLDER, PURPOSE, EXPORTS,
        DEPENDS ON, REFACTOR DATE
   e. Check ORIGIN_FILE contains the AI CONTEXT docstring.
   f. Treat __all__ as the canonical public API.
   g. If a module declares EXPOSES/EXPORTS, require __all__ and
      verify it matches exactly.
   h. Duplicate public-symbol checks must only consider symbols listed
      in __all__.
   i. Exclude validator scripts and extracted refactor-bundle directories
      from duplicate public-symbol ownership checks.
   j. Report missing __all__ as a dedicated error when EXPORTS/EXPOSES exists.
   k. Verify manifest "exports" matches helper-file __all__ exactly.

3. Print a clear report:
   ✅  PASS — <manifest path>
   ❌  FAIL — <manifest path>
       • <specific error message per check>

4. Exit with code 0 if all pass, exit code 1 if any fail
   (so CI pipelines catch it).

Produce the full validator as a single self-contained Python script
with no external dependencies beyond the standard library.

═══════════════════════════════════════════════
TASK 6 — FINAL CHECKLIST
═══════════════════════════════════════════════

After all tasks, confirm each item:

  [ ] All helper files exist in HELP_FOLDER
  [ ] All helper files have the mandatory header
  [ ] ORIGIN_FILE has the AI CONTEXT docstring
  [ ] ORIGIN_FILE still exports all original public symbols
  [ ] Every module that declares EXPORTS/EXPOSES defines matching __all__
  [ ] MANIFEST_FILE lists all helpers with purpose/exports/depends_on
  [ ] dependency_graph is consistent with depends_on fields
  [ ] CI validator passes with exit code 0 against this new manifest
  [ ] No circular imports introduced

═══════════════════════════════════════
HOW TO USE THIS PROMPT (meta-instructions)
═══════════════════════════════════════

- Fill ORIGIN_FILE, HELP_FOLDER, MANIFEST_FILE, VALIDATOR_SCRIPT, and REFACTOR_GOAL
  before submitting.
- Paste the content of ORIGIN_FILE into the chat after this prompt.
- If MANIFEST_FILE already exists (incremental refactor),
  paste it too so the AI merges instead of overwriting.
- Approve the roadmap in Task 1 before the AI writes any code.
- After the AI finishes, run:
  python <same folder as ORIGIN_FILE>/<origin_base_name>_validate_manifests.py
- If it exits 0, the refactor is complete and traceable.

Quick-Fill Example (EEG case)

ORIGIN_FILE      = core/signal/eeg_filter_state.py
HELP_FOLDER      = core/signal/eeg_filter_state_help/
MANIFEST_FILE    = core/signal/eeg_filter_state_help.json
VALIDATOR_SCRIPT = core/signal/eeg_filter_state_validate_manifests.py
REFACTOR_GOAL    = isolate all filter logic into independent
                   single-responsibility filter modules

The key design decisions in this prompt are:
- Task 1 always pauses for approval before any code is written
- the validator is project-wide so it grows with the codebase
- public API is explicit and deterministic through __all__
- every task produces an artifact that the validator independently verifies
- the prompt is self-auditing by design


- atention:

Canonical prompt audit
The prompt explicitly requires these five inputs:
ORIGIN_FILE
HELP_FOLDER
MANIFEST_FILE
VALIDATOR_SCRIPT
REFACTOR_GOAL
The prompt also explicitly requires the validator naming/location rule:
validator must live in the same folder as ORIGIN_FILE
validator filename must be <origin_base_name>_validate_manifests.py
The prompt explicitly requires the JSON manifest in Task 4, with:
origin
help_folder
refactor_date
refactor_goal
ai_instruction
helpers
dependency_graph
The prompt explicitly requires the validator script in Task 5, and says it must validate all manifests in the project, not just one manifest.
The prompt explicitly requires:
mandatory memo/header in every helper file,
explicit __all__,
AI CONTEXT docstring in the origin file,
manifest/export consistency checks,
final checklist validation.
Current status of our refactor work

deliver these required canonical artifacts as part of the refactor package:

ai_reasoner_main_window_help.json
ai_reasoner_main_window_validate_manifests.py
regenerated helper files with the mandatory memo/header
manifest-backed exports and depends_on
validator-backed enforcement for the helper package

canonize all of this:

regenerate every created helper file under
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\main_window_help
with:
mandatory header memo,
explicit __all__,
canonical exports,
canonical intra-helper dependency declaration.
create
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window_help.json
create
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window_validate_manifests.py
update
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window.py
with:
AI CONTEXT docstring,
explicit __all__,
canonical helper imports only,
no duplicate leftover logic beyond the approved staged boundary.
make the manifest list:
every helper file,
each purpose,
each export list,
each depends_on,
consistent dependency_graph.