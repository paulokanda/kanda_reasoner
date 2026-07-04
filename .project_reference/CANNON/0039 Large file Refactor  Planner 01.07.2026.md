# FINAL HANDOFF: Architecture Review - Large File Refactor Planner

## Feature name

Architecture Review -> Large File Refactor Planner

Feature id:

```text
architecture-review-large-file-refactor-planner-v1
```

## Purpose

Implement a new sub-tab inside the existing Architecture Review tab.

The sub-tab must help refactor large Python modules safely by producing a reviewable, validated split plan before any source write.

This is not an automatic refactor button.

It is a planner, previewer, validator, and patch-preparation workflow.

The feature must:

1. identify large Python files;
2. analyze symbols, imports, dependencies, globals, public API, docstrings, and risks;
3. propose a split plan;
4. preserve the original public facade when appropriate;
5. keep files near 400 lines when possible and always <=500 physical lines unless blocked;
6. avoid tiny helpers below 100 lines unless justified;
7. detect missing docstrings and propose adequate docstrings;
8. validate circular imports, public API preservation, lost symbols, lost decorators, stale source, and no-leak boundaries;
9. generate preview files only in the active project's daily-work preview area;
10. create a patch only after validation passes.

## Mandatory ownership rule: KANDA Reasoner tool vs KANDA Reasoner project

KANDA Reasoner has two identities:

1. KANDA Reasoner as the reusable tool.
2. KANDA Reasoner as the active project currently being edited.

The Large File Refactor Planner itself is tool-owned.

Concrete split/refactored files produced for a selected target module are project-owned.

### Tool-owned

Tool-owned files include:

```text
Architecture Review GUI sub-tab
large file refactor planner controller
AST analyzer
LibCST preview writer
dependency graph builder
cycle resolver
import migration planner
docstring planner
local LLM arbitration wrapper
preview writer
validation runner
no-leak gate
patch creator
```

### Project-owned

Project-owned files include:

```text
selected source file being refactored
generated split source files
project-specific helper files
generated project docstrings
project-specific preview files
project-specific validation evidence
project-specific refactor plan JSON
project-specific patch payload
project-specific freeze hint, if applicable
```

### Core no-leak rule

The refactor engine belongs to the KANDA Reasoner tool.

The refactored output belongs to the active project.

Do not write reusable tool logic into project output.

Do not write project-specific split files into reusable tool source unless the selected project source itself is intentionally being patched.

## Required pre-implementation checks

Before coding, complete:

```text
BOX CHECK

Task type:
Active box:
Owner path:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts:
Validation scope:
Boundary risks:
Tool/project ownership risk:
No-leak risk:
May proceed:
Next safe action:
```

And:

```text
NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:
```

If ownership is unclear, inspect source and routing manifests before writing.

## Required prompt/canon context before implementation

Load or apply:

```text
04_box_architecture_and_boundaries
box_architecture_canon.md
kanda_box_shielding_canon.md
project_tool_boundary_canon.md
NO_LEAK_LOGIC_V1 / No-Leak Logic Bridge
05_patch_delivery_and_validation
07_daily_patch_delivery_guardrails
08_python_engineering_core
09_python_quality_security_observability
09_active_project_freeze_context
compact Error Memory
large_module_refactor_protocol, if present
pre_output_contract_gates before patch/PowerShell output
freeze_code_intake_and_form_protocol if freeze-ready
```

Do not implement from memory alone.

## Sub-tab placement

Add a new local sub-tab inside Architecture Review:

```text
Run Selected Mode
Large Module AST Split Audit
Large File Refactor Planner
```

The new sub-tab must reuse existing Architecture Review results when possible.

It must not duplicate the whole Architecture Review scanner unless needed as fallback.

## Required integration with existing Architecture Review

The new sub-tab must discover candidate files in this order:

1. Use the last Large Module AST Split Audit result, if available.
2. Use parent Architecture Review controller state, if it exposes large-file findings.
3. Fall back to a limited active-project-root scan.

Create a tool-owned module such as:

```text
candidate_discovery.py
```

Its behavior:

```text
1. Try parent Architecture Review state.
2. Try last AST Split Audit result.
3. If none exists, scan active project root for Python files above threshold.
4. Exclude generated, evidence, preview, freeze, handoff, ZIP, and daily-work artifacts unless explicitly selected.
```

## Required integration with existing AI/model infrastructure

The tab must reuse the existing AI model selector/header pattern.

Do not create a separate independent Ollama model selector if one already exists.

The LLM arbitration module should reuse the same shared client or service used elsewhere in KANDA Reasoner, if present.

Suggested rule:

```text
llm_arbitration.py must receive:
- selected model name
- model settings
- timeout
- whether local LLM use is enabled
```

LLM support must be optional.

If Ollama/local model is unavailable, the tab must degrade gracefully to deterministic-only planning and show a warning badge.

## GUI layout

The sub-tab should have five sections.

### 1. Candidate file selector

Fields:

```text
candidate file list
manual file selector, if existing UI supports it
refresh candidates
line-count threshold
active project root display
source ownership status
```

Candidate columns:

```text
File
Lines
Public functions
Public classes
Total symbols
Imports
Global-state risks
Missing docstrings
External importers
Architecture warnings
Suggested action
```

Suggested actions:

```text
Analyze
Already compliant
Needs source inspection
Blocked: generated artifact
Blocked: wrong box
Blocked: global state
Blocked: not Python source
```

### 2. Settings panel

Defaults:

```text
Ideal physical lines: 400
Maximum physical lines: 500
Minimum helper physical lines: 100
Preserve public facade: ON
Generate missing docstrings: ON
Rewrite project imports: OFF in v1
Import migration preview: ON
Use local LLM: OFF by default or ON if configured
Preview only: ON
Create patch only after validation: ON
```

No "Apply now" button in v1.

Buttons:

```text
Analyze File
Generate Split Plan
Ask Local LLM for Ambiguous Symbols
Generate Preview
Validate Preview
Create Patch ZIP
Open Preview Folder
Copy Summary
Cancel
```

### 3. Analysis evidence panel

Show:

```text
module docstring present/missing
__all__ detected
public API symbols
external importers
top-level functions
top-level classes
constants
imports
relative imports
star imports
decorators
nested functions/classes
global state
module-level side effects
if __name__ == "__main__" block
dynamic imports
symbol references
line count per symbol
missing docstring count
```

Risk badges:

```text
GLOBAL_STATE
DYNAMIC_IMPORT
STAR_IMPORT
RELATIVE_IMPORT_RISK
PUBLIC_API_RISK
FACADE_REEXPORT_RISK
LAZY_EXPORT_REQUIRED
DECORATOR_RISK
NESTED_SYMBOL_CLUSTER
CIRCULAR_IMPORT_RISK
PRIVATE_REACH_IN_RISK
NO_LEAK_RISK
MISSING_DOCSTRING
TOO_LARGE_COHESIVE_GROUP
TOO_LARGE_CLASS
TOO_SMALL_HELPER
STALE_SOURCE
FILENAME_COLLISION
```

### 4. Proposed split plan panel

For each proposed output module, show:

```text
Output filename
Role
Estimated lines
Preview physical lines
Symbols included
Imports needed
Exports/re-exports
Docstrings generated
Docstring provenance
External importer impact
Risks
Status
```

Roles:

```text
public_facade
analysis_helper
partition_helper
import_helper
docstring_helper
validation_helper
io_helper
gui_helper
llm_helper
shared_helper
domain_helper
adapter_helper
manual_review_required
```

The base module must usually be a public facade/orchestrator, not the largest bin.

Wrong:

```text
largest bin becomes base module
```

Correct:

```text
base module preserves public API, __all__, external imports, and orchestration
implementation moves into private helper modules
```

### 5. Preview, validation, and patch panel

Stage statuses:

```text
Analysis: not run / ok / warning / blocked
Plan: not generated / ok / warning / blocked
LLM: disabled / ok / warning / unavailable
Docstrings: not generated / ok / warning / blocked
Preview: not generated / ok / warning / blocked
Validation: not run / passed / failed
Patch: not created / ready / blocked
```

Patch creation is blocked unless validation passes and source hash is fresh.

## Core workflow

### Stage 1: Candidate discovery

Input:

```text
active project root
Architecture Review findings
Large Module AST Split Audit results
manual selected file, if provided
```

Output:

```text
LargeFileCandidate[]
```

Candidate eligibility:

```text
file is .py
file belongs to active project source
file is not generated/evidence/freeze/handoff/preview output
file is not under _delete_after_daily_work unless explicitly preview
file is not a startup delivery artifact unless task is startup maintenance
file exceeds threshold, default >500 physical lines
```

Physical lines mean total file lines, including comments and blank lines.

Use Python/pathlib for line counting. Do not use shell-specific commands.

### Stage 2: AST analysis

Use Python AST for fast analysis.

Collect:

```text
module docstring
top-level classes
top-level functions
async functions
constants
assignments
imports
ImportFrom
__all__
decorators
type annotations
global statements
nonlocal statements
module-level expressions
module-level calls
if __name__ == "__main__" blocks
line spans
end line spans
symbol references
nested symbols
```

Do not use AST for final rewriting because AST does not preserve comments and formatting.

### Stage 3: LibCST readiness

Use LibCST for formatting-preserving preview writing and import/docstring transformation.

Parse with LibCST lazily:

```text
Run AST first.
Parse with LibCST only for preview generation, exact node movement, import rewrite preview, or docstring insertion.
Cache CST by file path + content hash.
```

### Stage 4: Symbol and cluster model

Use symbol records.

Required fields:

```text
schema_version
name
kind
visibility
start_line
end_line
physical_lines
decorators
signature
return_annotation
has_docstring
docstring_text
docstring_provenance
references
imports_used
globals_used
external_importers
risk_flags
assigned_module
content_hash
```

Nested functions/classes must remain with the parent.

Class methods must remain with the class.

Decorators must remain with the decorated function/class.

Atomic clusters:

```text
class + methods
decorator + decorated symbol
nested function/class + parent
strongly connected symbol group
module-level side-effect group
__all__ + facade exports
if __name__ == "__main__" block + facade/original module
```

### Stage 5: Import model

Create import records:

```text
schema_version
original_module
imported_name
alias
is_relative
relative_level
is_star
line_span
used_by_symbols
risk_flags
```

High-risk imports:

```text
star import
relative import
conditional import
try/except fallback import
dynamic importlib
getattr-based module access
string-based imports
plugin discovery
import side-effect dependency
```

For v1, project-wide import rewriting is preview-only unless deterministic and explicitly approved.

### Stage 6: Public API and external usage detection

Public API is determined by:

```text
__all__
top-level symbols not starting with "_"
symbols imported by other project files
symbols documented as public in module docstring
known facade entrypoints
existing package exports
```

Perform a project-wide text search for the old module name first.

Only parse likely importer files with AST/LibCST.

Mark symbols imported elsewhere as:

```text
public_contract = true
facade_critical = true
```

Validation must prove those symbols remain accessible through the original facade unless the user explicitly approves a breaking change.

### Stage 7: Global state and side-effect policy

Flag but do not automatically move:

```text
logging.basicConfig
environment reads
path setup
registry setup
global mutable containers
cache initialization
Tkinter or GUI initialization
thread/process startup
network/file/database side effects
plugin registration
monkeypatching
import-time execution
```

Default:

```text
Keep in original module/facade.
Move only when clearly pure or explicitly approved.
```

### Stage 8: Split planning

Targets:

```text
ideal: around 400 physical lines
maximum: 500 physical lines
minimum helper: 100 physical lines
```

Planning priority:

```text
1. Preserve behavior and public API.
2. Preserve box/no-leak ownership.
3. Preserve global-state ordering.
4. Group by responsibility.
5. Respect dependency graph.
6. Avoid cycles.
7. Respect line-count constraints.
8. Avoid tiny helper files.
```

Line count is a constraint, not the architecture principle.

### Oversized cohesive group policy

If a responsibility group exceeds max_lines:

```text
1. Try sub-partition by secondary responsibility.
2. Try sub-partition by dependency direction.
3. Try sub-partition by import/resource family.
4. Try shared helper extraction only if it reduces coupling.
5. If still oversized, flag TOO_LARGE_COHESIVE_GROUP.
6. Block automatic planning for that group.
```

Do not silently split by raw line cut.

### Oversized single class policy

If one class alone exceeds 500 physical lines:

```text
flag TOO_LARGE_CLASS
do not split methods into separate files automatically
route to manual class refactor workflow
allow docstring/comment-only improvements only if safe
```

The planner may suggest future manual refactors such as:

```text
extract collaborator class
extract dataclass/config object
extract strategy object
extract pure utility functions
split UI from logic
```

But v1 must not automatically split class methods across modules.

### Minimum helper justification

A helper below 100 physical lines is allowed only if at least one is true:

```text
required to break circular dependency
contains one cohesive class with at least 3 methods
contains at least 2 pure utilities used by multiple modules
is a public facade compatibility shim
isolates import side effects
isolates optional dependency integration
contains generated import migration adapter approved by validation
```

Otherwise merge it into the nearest related module.

### Filename collision check

Before preview writing:

```text
check proposed filenames against existing project files
check proposed filenames against other preview files
check repeated refactor runs do not collide
```

If collision exists:

```text
flag FILENAME_COLLISION
suggest target-specific prefix/suffix
block preview unless resolved
```

## Cycle detection and cycle resolution

Build a module dependency graph.

Use topological sorting or a deterministic fallback.

If cycle is detected, apply deterministic resolution in order:

```text
1. Merge involved modules if final line count <=500.
2. Keep one or more cycle-causing symbols in facade if facade remains <=500.
3. Extract shared pure symbols into a shared helper if it breaks the cycle and helper size is justified.
4. Use lazy facade export if cycle is only created by eager facade re-export.
5. Ask local LLM for semantic grouping only as advisory JSON.
6. If unresolved, flag CIRCULAR_IMPORT_RISK and block patch.
```

## Facade re-export policy

The original module should usually become the public facade.

Facade responsibilities:

```text
preserve public imports
preserve __all__
preserve external import compatibility
preserve if __name__ == "__main__" block when present
delegate implementation to private helpers
avoid duplicate public ownership
```

Default eager re-export:

```python
from ._helper import public_symbol
```

But eager re-export can create cycles.

If eager re-export causes a cycle, consider lazy export using module-level `__getattr__` as fallback.

Lazy export policy:

```text
Use lazy facade export only when:
- public API preservation requires facade access;
- eager re-export creates a cycle;
- symbol can be lazily imported safely;
- validation confirms no duplicate public ownership;
- the behavior is documented in the refactor plan.
```

Do not use lazy export as default.

## LLM arbitration policy

LLM use must be optional and bounded.

Allowed:

```text
assign ambiguous symbol to proposed module
suggest semantic helper filename
draft missing docstring
explain cycle cause
suggest merge vs shared-helper decision
```

Forbidden:

```text
rewrite whole module
create patch directly
decide ownership without source inspection
bypass validation
bypass no-leak
```

LLM output must be JSON-only.

Every LLM response must be schema-validated.

Invalid LLM response behavior:

```text
discard response
show warning badge
fall back to deterministic assignment
put symbol in facade if safest
or flag AMBIGUOUS_SYMBOL_NEEDS_REVIEW
```

LLM unavailable behavior:

```text
continue deterministic-only planning
show LLM_UNAVAILABLE warning
do not block analysis or deterministic plan
block only LLM-dependent optional actions
```

LLM cache key must include:

```text
schema_version
file_content_hash
symbol_name
symbol_line_span
symbol_body_hash
candidate_module_list_hash
model_name
temperature
llm_settings_hash
prompt_version
```

## Docstring completion stage

The planner must detect and propose missing docstrings.

Targets:

```text
module docstring
public classes
public functions
public methods
complex private helpers
generated helper modules
facade modules
```

Do not overwrite existing docstrings by default.

Docstring style:

```text
Google-style
triple double quotes
short summary first
Args when parameters exist
Returns when return value exists
Raises only when explicit raises are detected
use existing type hints
do not invent behavior
do not claim side effects unless statically evident
```

Docstring provenance must be recorded.

Allowed provenance values:

```text
existing
deterministic_template
llm_drafted
low_confidence_needs_review
manual_required
```

Docstring confidence rule:

```text
If function has non-obvious side effects, dynamic behavior, global writes, network/file/database calls, or unclear return semantics, mark low_confidence_needs_review.
```

Line count must be revalidated after docstring insertion.

If docstrings push a module above 500 physical lines:

```text
1. shorten docstrings using concise template;
2. re-plan if possible;
3. if not possible, flag DOCSTRING_LINE_LIMIT_RISK and block patch.
```

## Preview generation

Preview must not write directly to active source tree.

Preview location:

```text
active_project_daily_work_root / "large_file_refactor_preview" / feature_id_or_timestamp
```

Use project path resolver and pathlib.

Do not concatenate Windows strings manually.

Preview output must include:

```text
refactor_plan.json
symbol_map.json
import_migration_plan.json
docstring_proposals.json
risk_report.json
validation_report.json
README_PREVIEW.txt
README_IMPORTS.txt
facade_diff.patch or facade_diff.txt
generated preview modules
```

No Unix-only commands.

If import migration helper is generated, make it a plain Python helper preview, not sed/find commands.

## Centralized no-leak write gate

No write function may write paths directly.

All writes must pass through one centralized gate:

```text
assert_within_allowed_roots(path, allowed_roots, purpose)
```

This gate must be used by:

```text
preview writer
patch creator
docstring inserter
import migration preview writer
validation evidence writer
cache writer
```

The gate must reject:

```text
wrong active project root
tool/project ownership mismatch
writes into generated startup ZIP contents
writes into freeze memory from preview
writes outside allowed daily-work or patch payload roots
path traversal
ambiguous root
```

Every file-write function must call a shared `safe_write_text`, `safe_write_bytes`, or equivalent wrapper that invokes this gate.

## Staleness protection

Every plan must store:

```text
source_path
source_size
source_mtime
source_content_hash
analysis_timestamp
settings_hash
```

Before preview generation and before patch creation:

```text
re-read source file
recompute content hash
compare with plan hash
```

If mismatch:

```text
flag STALE_SOURCE
block patch creation
force re-analysis
```

This is a hard gate.

## Rollback metadata

Patch metadata should include:

```text
original file path
original file content hash
original file size
original mtime
preview source hash
generated file hashes
patch feature id
schema_version
```

If feasible, include a backup copy in the patch staging metadata or record enough hash/path data to support safe manual rollback.

## Validation

Validation must prove more than compile success.

Required validations:

```text
py_compile generated preview files
AST parse generated files
line count <=500 physical lines
helper >=100 physical lines or justified
public API preservation
external importers still resolved through facade
symbol preservation
decorator preservation
nested symbol preservation
__all__ preservation
if __name__ == "__main__" preservation
module dependency graph acyclic or justified lazy facade export
docstring validation
docstring provenance recorded
filename collision check
source hash fresh
no-leak write gate used
preview wrote only allowed roots
patch creation validation-gated
```

Behavior validation:

```text
If project tests are detected, offer "Run existing test suite against preview/patch" as a soft gate.
If no tests are found, show warning: TEST_SUITE_NOT_DETECTED.
```

Do not claim behavior equivalence from py_compile alone.

Also generate a normalized source-content comparison:

```text
Compare original movable symbol bodies with generated symbol bodies.
Allow expected differences:
- imports
- module docstrings
- inserted docstrings
- facade re-exports
- formatting preserved/normalized by LibCST
```

Flag unexpected body changes.

## Import migration preview

V1 default:

```text
Rewrite project imports: OFF
Import migration preview: ON
```

Generate:

```text
import_migration_plan.json
README_IMPORTS.txt
optional Python helper preview
```

Do not generate sed/find commands.

Relative imports:

```text
detect and flag high risk
only auto-preview rewrite if package path remains valid
otherwise require manual review
```

Star imports:

```text
flag high risk
do not auto-rewrite in v1
```

## GUI responsiveness

All long-running work must run in the existing GUI worker pattern.

If an existing worker exists, reuse it.

If not, create a small refactor-specific worker consistent with the app.

Long-running operations:

```text
AST scan over large project
LibCST parse
LLM call
preview generation
validation
import migration scan
project test detection
```

Worker requirements:

```text
progress messages
safe cancellation
structured result
structured error
no UI freeze
no direct UI mutation from worker thread
```

Add Cancel button.

## State machine

Use explicit states:

```text
IDLE
CANDIDATE_SELECTED
ANALYZING
ANALYZED
PLAN_READY
LLM_REVIEW_READY
DOCSTRING_READY
PREVIEW_GENERATING
PREVIEW_READY
VALIDATING
VALIDATION_PASSED
VALIDATION_FAILED
PATCH_READY
BLOCKED
STALE_SOURCE
CANCELLED
```

Patch creation allowed only from:

```text
VALIDATION_PASSED
```

Patch creation blocked from all other states.

## Data contracts

All persisted JSON must include:

```text
schema_version
feature_id
created_at
tool_version_or_patch_id
active_project_root
target_file
source_content_hash
settings_hash
```

### LargeFileCandidate

```text
schema_version
path
relative_path
line_count_physical
public_symbol_count
class_count
function_count
missing_docstring_count
external_importer_count
risk_flags
source_box
is_eligible
blocked_reason
```

### RefactorSymbol

```text
schema_version
name
kind
visibility
start_line
end_line
physical_lines
decorators
signature
return_annotation
has_docstring
docstring_text
docstring_provenance
references
imports_used
globals_used
external_importers
atomic_cluster_id
risk_flags
assigned_module
content_hash
```

### ProposedModule

```text
schema_version
filename
role
symbols
estimated_lines
preview_physical_lines
imports
exports
docstrings_generated
risk_flags
status
line_limit_justification
```

### RefactorPlan

```text
schema_version
feature_id
target_file
source_content_hash
settings
public_api_before
public_api_after_expected
symbols
atomic_clusters
proposed_modules
import_migration
docstring_proposals
risks
validation_blockers
status
```

### ValidationReport

```text
schema_version
feature_id
source_content_hash
line_count_ok
compile_ok
ast_cross_check_ok
docstrings_ok
public_api_ok
symbol_preservation_ok
decorator_preservation_ok
nested_symbol_ok
import_graph_ok
no_leak_ok
staleness_ok
filename_collision_ok
architecture_ok
test_suite_status
errors
warnings
success_markers
```

## Patch creation policy

Differentiate patch types:

```text
is_tool_patch
is_project_patch
is_mixed_patch
```

For v1 implementation of the tab itself:

```text
is_tool_patch = true
```

It should include only tool-owned modules, GUI registration changes, and validation scripts.

For future application of a split to a selected project:

```text
is_project_patch = true
```

It should include project-owned refactored source files and project-specific validation evidence.

Do not mix tool feature implementation and project refactor output in the same patch unless explicitly governed and validated.

Freeze hint:

```text
Tool-only patch: include freeze hint only if local freeze workflow expects it for validated tool features.
Project split patch: include project-specific freeze hint if freezeable.
Mixed patch: avoid unless explicitly approved.
```

## Validation script design

Focused validation script:

```text
validation/test_architecture_review_large_file_refactor_planner_v1.py
```

It must be self-contained and avoid broad project-wide imports.

Use synthetic sample modules and mock GUI/controller state where possible.

Checks:

```text
new sub-tab registration exists
candidate discovery fallback exists
shared AI model selection hook exists or is intentionally deferred
settings defaults 400/500/100 exist
facade preservation rule exists
oversized cohesive group rule exists
TOO_LARGE_CLASS rule exists
central no-leak write gate exists
source hash staleness gate exists
docstring provenance exists
LLM schema validation exists
LLM unavailable fallback exists
filename collision check exists
preview path uses pathlib/path resolver
import migration preview is ON and auto-rewrite OFF by default
relative import risk flag exists
nested symbols are atomic with parent
validation-gated patch creation exists
all new/touched Python modules <=500 physical lines
py_compile passes changed Python files
```

Expected markers:

```text
VALIDATION OK: architecture-review-large-file-refactor-planner-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
```

Keep the validation script itself under 500 physical lines.

If too large, split validation helpers into small validation modules under an appropriate validation helper folder, preserving module-size rules.

## Implementation phases

### Phase 1: Shell and contracts

Implement:

```text
sub-tab shell
settings panel
state machine
data models
candidate discovery stub
central no-leak write gate
staleness contract
validation skeleton
```

No preview generation yet.

Highest priority gates to implement now:

```text
central no-leak write gate
source hash staleness gate
```

### Phase 2: Analyzer

Implement:

```text
AST analyzer
symbol extraction
docstring detection
import detection
public API detection
global-state risk flags
nested symbol/atomic cluster detection
candidate discovery from parent Architecture Review state or fallback scan
```

### Phase 3: Split planner

Implement:

```text
responsibility classification
dependency graph
line constraints
oversized cohesive group policy
oversized single class policy
minimum helper justification
cycle resolver
filename collision check
facade preservation plan
```

### Phase 4: Docstring planner

Implement:

```text
missing docstring proposals
docstring provenance
low-confidence flag
line recount after docstrings
docstring validation
```

### Phase 5: LLM arbitration

Implement:

```text
shared model selection integration
JSON-only responses
schema validation
cache with model/settings hash
unavailable fallback
invalid response fallback
```

### Phase 6: Preview writer

Implement:

```text
LibCST-based preview generation
safe write through no-leak gate
preview folder creation via pathlib/path resolver
facade diff generation
import migration plan
README_PREVIEW
README_IMPORTS
```

### Phase 7: Validation and patch creation

Implement:

```text
py_compile
AST cross-check
symbol preservation
public API preservation
dependency graph validation
docstring validation
staleness recheck
no-leak validation
test-suite detection soft gate
patch ZIP creation after validation only
```

## Explicit non-goals for v1

Do not implement:

```text
automatic apply without preview
whole-project automatic refactor
LLM rewriting entire files
automatic class-method splitting
automatic moving of import-time side effects
automatic project-wide import rewrite
Unix sed/find command output
type stub rewriting
test generation
mixed tool/project patch unless explicitly approved
```

## Acceptance criteria

The feature is accepted when:

```text
1. Architecture Review contains Large File Refactor Planner sub-tab.
2. The tab reuses existing Architecture Review large-file evidence or falls back to active-project scan.
3. The tab uses shared AI model selection where available.
4. The tab can analyze a selected large Python file.
5. It shows symbols, imports, dependencies, globals, public API, external importers, and missing docstrings.
6. It proposes split modules using responsibility first and line count as constraint.
7. It enforces ideal 400, maximum 500, and minimum 100 physical line policy.
8. It blocks or flags oversized cohesive groups.
9. It blocks or flags oversized single classes.
10. It preserves facade/public API.
11. It detects facade re-export cycle risk and supports lazy facade fallback only when validated.
12. It proposes docstrings with provenance and confidence.
13. It validates LLM JSON responses and degrades gracefully if LLM is unavailable.
14. It checks source hash before preview and before patch creation.
15. It routes all writes through a centralized no-leak write gate.
16. It writes preview only to active project daily-work preview root.
17. It generates import migration preview without applying project-wide rewrites by default.
18. It validates generated preview files before patch creation.
19. It blocks patch creation on stale source, circular imports, public API mismatch, filename collision, no-leak violation, or validation failure.
20. It creates patch ZIP only after validation.
21. All new/touched source modules remain <=500 physical lines.
22. Focused validation prints:
    VALIDATION OK: architecture-review-large-file-refactor-planner-v1
    STATUS: IN_SYNC
23. Patch contract validation prints:
    ZIP CONTRACT: PASS
```

## Final implementation priority

Before Phase 1:

```text
1. Centralized no-leak write gate.
2. Source hash staleness gate.
```

Before Phase 3:

```text
1. Oversized cohesive group policy.
2. Oversized single class policy.
3. Minimum helper justification.
4. Filename collision check.
```

Before Phase 4 and 5:

```text
1. Docstring provenance.
2. LLM schema validation.
3. LLM unavailable fallback.
```

Before Phase 6 and 7:

```text
1. Public API/external importer preservation.
2. Facade re-export cycle handling.
3. Preview-only import migration.
4. Behavior-aware validation warning via optional test-suite detection.
```

## Final compact summary

Build the Large File Refactor Planner as a safe Architecture Review sub-tab that converts large-file architecture debt into a validated, reviewable plan.

It must not be a magic refactor button.

It must use:

```text
AST for fast analysis
LibCST for formatting-preserving preview generation
dependency graphs for cycle detection
public facade preservation
docstring completion with provenance
bounded JSON-only local LLM decisions
central no-leak write gate
source hash staleness gate
preview-only output
validation-gated patch creation
```

Most important rule:

```text
The refactor planner engine is KANDA Reasoner tool-owned.
The concrete split/refactored source files are active-project-owned.
Every write must prove its ownership and allowed root before it happens.
```
