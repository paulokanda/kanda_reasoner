# KANDA Reasoner — Large File Refactor Planner / Workbench Continuation Handoff

Date context: 2026-07-05
Active project/tool root: `E:\kanda_reasoner`
Primary current workstream: Large File Refactor Planner → Large File Refactor Workbench completion pipeline
Human owner: Rafael Kanda

---

# 0. READ THIS FIRST

This handoff is authoritative for continuation of the current workstream, but it does not override canonical KANDA prompts, freeze memory, Router Bridge routing, Box Logic, KANDA Box Shielding, No-Leak Logic, or newer confirmed freeze entries.

Before implementing anything:

1. Load startup context and latest freeze entries newest-first.
2. Inspect the exact current local source tree.
3. Do not assume that every patch described below was installed.
4. Do not assume that every installed patch was frozen.
5. Do not infer canonical freeze status from a ZIP having been generated.
6. Do not infer canonical freeze status from validation success.
7. Freeze evidence merge is not final freeze.
8. Final freeze requires:
   `Freeze Feature After Update -> Preview -> Confirm and Write`.
9. If local source differs from this handoff, inspect:

   * latest freeze entries;
   * current source;
   * installed patch evidence;
   * Error Memory;
     before deciding which state is authoritative.
10. Do not silently repair by bypassing gates.

The human strongly prefers implementation over abstract advice, but correctness and governance are mandatory.

---

# 1. GLOBAL KANDA ARCHITECTURE RULES

## 1.1 Tool/project distinction

KANDA Reasoner is both:

* the tool being developed;
* and, sometimes, the selected current project.

Never confuse:

```text
tool-owned KANDA source
```

with:

```text
selected-project output
```

Tool-level refactor engines, GUI behavior, Planner logic, Workbench logic, routing, prompt-library logic, validation infrastructure, and freeze helpers belong to the KANDA tool root.

Generated refactor output for a selected project must not leak into KANDA source ownership.

---

## 1.2 Active architectural principles

The following are active design principles and must be preserved:

```text
Box Logic
KANDA Box Shielding
No-Leak Logic
```

No-Leak Logic is a named architecture object, not just wording.

It explicitly prevents:

```text
wrong-root writes
tool/project leakage
cross-box leakage
private reach-in
hidden mutable state
public API ownership leakage
generated-artifact-as-source leakage
validation/freeze evidence leakage
```

Before any implementation:

```text
identify active box
identify owner paths
identify allowed files
identify out-of-scope files
declare cross-box touches
preserve public contracts
validate active box
validate every touched external box
```

---

# 2. CONFIRMED PRE-EXISTING FROZEN GOVERNANCE CONTEXT

The following frozen features are known from prior project state and must not regress.

## 2.1 Patch Validate Freeze Recovery Blueprint v1

Active as of 2026-06-29.

Protected behavior includes:

```text
Show Project to AI must provide:
Copy Patch Validate Freeze Recovery Routine
```

The button reads:

```text
patch_validate_freeze_error_memory_routine_blueprint.md
```

from the selected active project root, with app-root fallback only if needed.

The wrapper prompt must remain thin and reference owner canons.

Routing must recognize:

```text
Show Project to AI file/ZIP creation failure
patch validate freeze routine requests
```

Do not bypass:

```text
ZIP contract validation
local validation
freeze evidence merge
Preview
Confirm and Write
```

Error Memory intake must use the governed `KANDA_ERROR_LESSON` workflow.

---

## 2.2 Startup Freeze Context Latest Entries v1

Active as of 2026-06-29.

Startup active-project freeze context must expose latest freeze entries newest-first from canonical external:

```text
<project>_show_project_to_AI/
project_freeze_after_update/
frozen_features_memory/
```

Compact freeze-report truncation must not hide newer frozen entries.

When newer entries conflict with older compact-report lines, newest canonical freeze entry wins.

---

# 3. IMPORTANT STATUS DISTINCTION FOR THIS CHAT

Many features were implemented, packaged, and validated during this workstream.

However:

> Do not assume all of them are canonically frozen.

The conversation contains delivery and freeze code for many patches, but there is no reliable explicit conversational confirmation that every corresponding:

```text
Freeze Feature After Update
-> Preview
-> Confirm and Write
```

was completed locally.

Therefore use these categories:

```text
CONFIRMED FROZEN
    only where latest freeze memory proves it

DELIVERED + VALIDATED
    patch ZIP built and sandbox-validated

INSTALLED
    only if local source/evidence proves installation

FROZEN
    only if canonical freeze memory proves Confirm and Write
```

Never collapse those states.

---

# 4. LARGE MODULE REFACTOR CANON

The existing core canon is:

```text
kanda_prompt_workspace/
prompt_library/
ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
large_module_refactor_protocol.md
```

The user supplied the existing v7.2 canon during this chat.

That canon already owns:

```text
module-size law
<=400 ideal
<=500 hard code-module maximum
practical helper granularity
avoid tiny helper hyperpopulation
AST-assisted split audit
public API preservation
dependency-direction mapping
wide responsibility-island mode
multi-island execution layer
patch trains
tiered validation
rollback
fragmentation audit
GUI inventory
freeze requirements
```

Do not create another competing general large-module canon.

An implementation patch was created to advance the intended canon to:

```text
v7.3
```

with a focused external Web AI delegation section.

Do not assume v7.3 is frozen until local canonical freeze proves it.

---

# 5. CURRENT LARGE FILE REFACTOR MENTAL MODEL

The intended architecture is:

```text
AST Split Audit
        ↓
Large File Refactor Planner
        ↓
selected isolated planning version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench-owned snapshot
        ↓
Large File Refactor Workbench
        ↓
real preview
        ↓
validation
        ↓
preflight
        ↓
backup
        ↓
shadow apply
        ↓
visual diff
        ↓
real refactor transaction
        ↓
post-apply validation
        ↓
behavior validation
        ↓
completion / rollback
```

Planner owns:

```text
analysis
planning
candidate architecture generation
docstring proposals
Local AI bounded planning
Imported Web AI planning review
version comparison
planning summary
```

Planner does not own source mutation.

Workbench owns:

```text
dependency readiness
preview generation
preview structural validation
preflight
backup
source-apply payload
shadow validation
actual apply
post-apply validation
behavior validation
rollback
completion transaction
```

Keep this boundary.

---

# 6. EARLY PLANNER UI / ARCHITECTURE WORK COMPLETED IN THIS STREAM

The following major changes were delivered during the broader Planner workstream.

## 6.1 Child-tab architecture

Planner parent remains under Architecture Review.

Child tabs:

```text
Input & Analysis
Plan & Actions
```

The implementation uses the inner-tab template.

---

## 6.2 Compact settings and Local AI visual treatment

Settings were compacted.

The Local AI checkbox:

```text
Use local AI when available
```

was visually emphasized with bold green text and black frame.

---

## 6.3 Planner action-surface cleanup

Planner `Plan & Actions` was moved toward pre-implementation ownership.

Intended actions included:

```text
Analyze File
Generate Split Plan
Generate Docstring Plan
Review & Refine Plan with Local AI
Show Planning Summary
Copy Planning Summary
```

Implementation actions were removed from Planner ownership.

---

## 6.4 Sonar activity feedback

A reusable green sonar activity monitor was added for long-running Planner actions.

It supports:

```text
start
finish_success
finish_error
set_idle
```

Split generation and Local AI actions use activity feedback.

---

# 7. WORKBENCH SNAPSHOT ISOLATION

A major architecture patch created the intended boundary:

```text
Planner
    ↓ explicit Load Latest Planner Plan
validated immutable Workbench snapshot
    ↓
Workbench owns implementation workflow
```

Important modules include:

```text
planner_workbench_handoff.py
workbench_gui.py
workbench_plan_intake.py
workbench_plan_snapshot.py
workbench_snapshot_bridge.py
```

Protected behavior:

```text
Planner changes must not silently mutate an already-loaded Workbench plan.

Workbench changes its plan only after explicit:
Load Latest Planner Plan
```

This architecture should remain.

---

# 8. PLANNER VERSION ARCHITECTURE

The Planner has three planning-version concepts.

Correct semantics:

```text
Heuristic
Local AI
Imported Web AI Version
```

## 8.1 Heuristic

Generated locally and deterministically.

## 8.2 Local AI

Starts from deterministic Planner evidence and uses bounded Local AI review/correction.

## 8.3 Imported Web AI Version

Not generated locally.

Correct workflow:

```text
Generate Heuristic or Local AI native plan
        ↓
latest native plan recorded
        ↓
Copy Comprehensive Planning for Web AI
        ↓
send package to online AI
        ↓
online AI creates governed import ZIP
        ↓
install pending imported Web AI artifact
        ↓
Receive Planning from Web AI
        ↓
validate against matching native base
        ↓
review
        ↓
Load as Imported Web AI Version
```

The Imported Web AI radio is a selectable imported version, not a local generation strategy.

---

# 9. VERSION ROUTING BEHAVIOR

The version radios are intended to be active before generation.

The selected route controls generation behavior.

Intended native routes:

```text
HEURISTIC
    deterministic plan
    automatic deterministic docstring proposals
    stop

LOCAL AI
    deterministic plan
    automatic deterministic docstring proposals
    staged Local AI architecture process
    tournament
    deterministic selection
```

Imported Web AI Version:

```text
does not locally generate
```

The Proposed Split Plan panel should explicitly rerender the selected isolated version and display:

```text
ACTIVE PLANNER VERSION: Heuristic
```

or:

```text
ACTIVE PLANNER VERSION: Local AI
```

or:

```text
ACTIVE PLANNER VERSION: Imported Web AI Version
```

---

# 10. HEURISTIC EVOLUTION IMPLEMENTED DURING THIS CHAT

A six-step deterministic/AI architecture improvement sequence was developed.

These are important because the next AI should not regress to the original simplistic split heuristic.

---

## STEP 1 — Multi-signal deterministic candidate generation

Original failure:

```text
facade 197

helpers:
38
100
371
41
51
37

4 tiny-helper blockers
status = blocked
```

Step 1 changed the Heuristic from approximately:

```text
dependency connected component
    ≈
one helper module
```

to:

```text
AST dependency clusters
        ↓
must-link atomic groups
        ↓
multi-signal affinity
    structural
    semantic vocabulary
    source proximity
    role compatibility
        ↓
multiple deterministic candidate strategies
        ↓
hard size constraints
        ↓
deterministic ranking
```

Candidate strategies:

```text
dependency-dominant
balanced
responsibility-dominant
```

Real target result:

```text
facade 197
helper 122
helper 452
status planned
```

This converted the original blocked plan to a valid plan.

Feature ID:

```text
large-file-refactor-planner-heuristic-multisignal-candidate-ranking-v1
```

Delivered ZIP:

```text
kanda_large_file_refactor_planner_heuristic_multisignal_candidate_ranking_v1_patch.zip
```

SHA-256:

```text
a92c4b11fb5434da25db76d0266b3b492369c36128beca59d81788228a689f66
```

---

## STEP 2 — Responsibility labeling and semantic naming

Added deterministic responsibility records:

```text
primary responsibility
secondary responsibilities
confidence
confidence score
evidence tokens
per-responsibility scores
```

The real target plan became semantically named:

```text
main_helper_mapper.py                         197

_main_helper_mapper_path_resolution.py       122

_main_helper_mapper_helper_selection.py      452
```

Evidence example:

```text
path_resolution
confidence high
tokens:
path
normalize
root
project
compare
find
```

and:

```text
helper_selection
confidence high
secondary:
decision_reporting
```

Feature ID:

```text
large-file-refactor-planner-responsibility-labeling-semantic-naming-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_responsibility_labeling_semantic_naming_v1_patch.zip
```

SHA-256:

```text
c57c6e96319f797c98ad0a1b523229525ccf4e57c348d42a127714f18cbbe32e
```

---

## STEP 3 — Projected dependency topology and quality scoring

Added deterministic directed module topology evidence.

Important distinction:

```text
helper-only cycle
    = hard blocker

helper -> facade back-reference
    = explicit boundary risk
    not silently treated as clean
    not automatically confused with helper-only cycle
```

Real target evidence:

```text
main_helper_mapper.py
    -> path_resolution
    -> helper_selection

helper_selection
    -> main_helper_mapper.py
```

Risks:

```text
FACADE_BACK_REFERENCE_RISK
FACADE_BOUNDARY_CYCLE_RISK
```

Quality scoring added:

```text
responsibility cohesion
topology score
mixed-responsibility penalty
facade back-reference penalty
```

Real target evidence:

```text
responsibility cohesion = 0.849312
topology score = 0.92
mixed-responsibility penalty = 0.150688
```

Feature ID:

```text
large-file-refactor-planner-topology-responsibility-quality-scoring-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_topology_responsibility_quality_scoring_v1_patch.zip
```

SHA-256:

```text
126de106bd373948382088729856783f8b1304637b8246d6dafb97511409d263
```

---

# 11. LOCAL AI EVOLUTION

## STEP 4 — Staged Local AI protocol

The original Local AI protocol overloaded a 7B model with:

```text
analyze architecture
merge
reassign
rename
answer 8 architecture questions
rationale
warnings
schema compliance
```

in one response.

This repeatedly failed.

Step 4 split Local AI into:

```text
1. Responsibility Analysis
2. Targeted Architecture Repair
3. Deterministic Validation
4. Exact-Rejection Targeted Retry
5. Semantic Naming Review
6. Final Architecture Audit
```

Core principle:

```text
AI suggestions
    ↓
deterministic validation
    ↓
targeted retry with exact rejection reason
```

Architecture actions remain bounded to known objects.

Feature ID:

```text
large-file-refactor-planner-staged-local-ai-protocol-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_staged_local_ai_protocol_v1_patch.zip
```

SHA-256:

```text
b4b101021f0796355a523ca98ed755d618ea86e9446bd55262f60b8e75d99bea
```

---

## STEP 5 — Local AI candidate tournament

Added:

```text
baseline control
Candidate A: conservative/minimal-change
Candidate B: responsibility/cohesion focused
Candidate C: topology/boundary focused
```

Each starts from the same immutable logical baseline.

Not:

```text
baseline -> A -> B -> C
```

but:

```text
          baseline
         /   |   \
        A    B    C
```

Each candidate is independently:

```text
AI-generated
bounded
deterministically validated
deterministically scored
```

KANDA chooses the winner.

The model does not self-select.

Important rule:

```text
AI candidate must beat deterministic baseline threshold
or baseline is preserved
```

Feature ID:

```text
large-file-refactor-planner-local-ai-candidate-tournament-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_local_ai_candidate_tournament_v1_patch.zip
```

SHA-256:

```text
25342cf97708ae704cda4ff83fe5b63f79ff7c15bd9d3ed716c1200251fada88
```

---

# 12. STEP 6 — OPTIONAL GIT CO-CHANGE EVIDENCE

Git history was added only as a supporting signal.

Authority hierarchy:

```text
AUTHORITATIVE

AST evidence
atomic clusters
public facade ownership
size gates
cycle gates
Box Shielding
No-Leak Logic

SUPPORTING

semantic affinity
source proximity
Git historical co-change
```

Git cannot override:

```text
atomic clusters
100–500 size policy
cycle blockers
public API ownership
box boundaries
```

The implementation uses read-only bounded Git queries and graceful fallback.

Feature ID:

```text
large-file-refactor-planner-git-cochange-history-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_git_cochange_history_v1_patch.zip
```

SHA-256:

```text
c9163c36a1a79a0326c5468ec74d4a9e50d9aee4738d5c23bae324c53e2ee65b
```

---

# 13. QUALITY HARDENING AFTER REAL LOCAL AI RUN

A real Heuristic vs Local AI comparison exposed four reporting/protocol weaknesses.

A focused correction patch addressed:

## 13.1 Tournament action accounting

Old ambiguity:

```text
Architecture actions applied: 0
```

while later:

```text
Accepted 22 repair actions
```

Correct distinction:

```text
Candidate exploration actions accepted: N

Final selected-version actions applied: M
```

A candidate may perform exploratory valid actions while baseline still wins.

---

## 13.2 Naming-stage empty array normalization

The Local AI returned:

```json
[]
```

The naming stage now treats this, only in that stage, as:

```json
{
  "module_renames": []
}
```

Do not globally loosen all JSON schemas.

---

## 13.3 Audit retries request missing fields only

Accepted architecture audit answers must be retained.

Retry only unresolved IDs.

Do not ask the 7B model to regenerate already accepted fields.

---

## 13.4 Git confidence weighting

A real project history showed:

```text
observed history commits = 2
raw co-change = 1.0
```

Raw 1.0 with only two commits was misleadingly strong.

Confidence model added:

```text
0 commits     none       0.00
1–2           very_low   0.15
3–5           low        0.35
6–15          moderate   0.65
16+           high       1.00
```

Expose:

```text
raw score
confidence level
confidence weight
effective score
```

Feature ID:

```text
large-file-refactor-planner-quality-hardening-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_quality_hardening_v1_patch.zip
```

SHA-256:

```text
e7ff4308cc69abe04f0ac3922487a9762783efe1748aa669c8f160daa0259bf7
```

Error Memory lesson associated with this correction:

```text
lesson-planner-review-evidence-consistency-and-history-confidence-v1
```

---

# 14. LOCAL AI JSON ADAPTER ERROR HISTORY

Earlier Local AI runs failed four times with:

```text
Local AI response must be JSON only:
Expecting value: line 1 column 1
```

The problem was transport-wrapper brittleness, not necessarily architecture logic.

A focused response adapter repair was created.

It accepts:

```text
plain JSON
fenced JSON
<think>...</think> + JSON
short prose prefix + one JSON object
marker-wrapped JSON
```

while preserving:

```text
schema validation
known symbol restrictions
known module restrictions
atomic cluster validation
size gates
cycle validation
deterministic revalidation
```

Feature ID:

```text
large-file-refactor-planner-local-ai-json-adapter-repair-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_local_ai_json_adapter_repair_v1_patch.zip
```

SHA-256:

```text
53d84b69b3dbfd63762a2ef83ac93e1a3ebcb03b1415becdf8c06a5ce3a787c3
```

Associated Error Memory lesson:

```text
lesson-planner-local-ai-json-wrapper-parse-failure-v1
```

---

# 15. REAL MAIN_HELPER_MAPPER CASE — CURRENT REFERENCE EVIDENCE

Target:

```text
E:\kanda_reasoner\
kanda_reasoner_app\
reasoner_symbol_atlas\
main_helper_mapper.py
```

Source hash:

```text
6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55
```

## 15.1 Heuristic result

Current useful Heuristic architecture:

```text
main_helper_mapper.py                         197

_main_helper_mapper_path_resolution.py       122

_main_helper_mapper_helper_selection.py      452
```

Status:

```text
planned
```

No validation blockers.

Current weighted Heuristic candidate evidence from the real run:

```text
heuristic:balanced
score = 0.698662

responsibility = 0.849312
topology = 0.92
mixed_penalty = 0.150688
effective_history = 0.15
```

Git history:

```text
commits observed = 2
confidence = very_low
weight = 0.15
```

This is correct behavior.

---

## 15.2 Local AI result

The Local AI tournament did not improve the final architecture.

Reference result:

```text
baseline_control  0.736690
candidate_a       0.736690
candidate_b       0.640690
candidate_c       0.736690
```

Final selection:

```text
baseline_control
```

Meaning:

```text
Local AI route executed
candidate exploration occurred
inferior alternatives were rejected
deterministic baseline preserved
```

This is now considered a useful guarded-search outcome even though the visible final architecture equals Heuristic.

---

## 15.3 Imported Web AI result

A bounded external Web AI proposal was created.

Native base plan hash:

```text
5b43bf2d61baf9139da5253121dab42b6733685128e4b5fd73091f9a0eebedb4
```

Bounded reassignment:

```text
_related_tests_to_run
```

from:

```text
_main_helper_mapper_helper_selection.py
```

to:

```text
_main_helper_mapper_path_resolution.py
```

Result:

```text
Heuristic:
122 / 452

Imported Web AI:
145 / 429
```

Deterministic comparison evidence:

```text
baseline = 0.736690
Imported Web AI = 0.783250
```

This external proposal was designed to be a small bounded improvement, not a complete redesign.

Corrected import ZIP:

```text
kanda_imported_web_ai_main_helper_mapper_v1_fixed.zip
```

SHA-256:

```text
31b6b73a859f14c4fa6232caed19b16e4f6218835a07d2de7d1a813f063b5686
```

Freeze-evidence bundle:

```text
kanda_imported_web_ai_main_helper_mapper_freeze_v1.zip
```

SHA-256:

```text
0f2a22e5f755a41b019882b11d36743a77aaa9f51816bd87062171991a1af2c7
```

Feature ID for that planning freeze evidence:

```text
imported-web-ai-main-helper-mapper-plan-v1
```

Again: confirm actual canonical freeze status from freeze memory. Do not infer it from bundle existence.

---

# 16. IMPORTED WEB AI INSTALLER BUG AND ERROR MEMORY

The first Web AI import installer falsely reported:

```text
Payload must contain exactly one Web AI begin marker.
```

Exact payload inspection showed one begin marker and one end marker.

Root cause:

```powershell
$PayloadText.Split($BeginMarker)
```

was incorrectly used as a literal substring occurrence counter.

PowerShell/.NET overload behavior can bind to separator semantics inconsistent with intended whole-string counting.

Correct pattern:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count
```

and equivalent for the end marker.

Do not repeat:

```powershell
$PayloadText.Split($BeginMarker)
```

for literal marker counting.

Error Memory lesson ID:

```text
lesson-web-ai-import-installer-literal-marker-count-v1
```

Future Web AI installer generation should validate:

```text
exactly one begin marker
exactly one end marker
valid JSON between markers
source hash match
base plan hash match
artifact copy equality
```

---

# 17. IMPORTED WEB AI VERSION SEMANTICS

A dedicated semantic correction changed the wrong earlier interpretation.

Correct model:

```text
Heuristic
    local native generator

Local AI
    local native generator + bounded AI refinement

Imported Web AI Version
    external artifact installed into Planner import inbox
```

`Copy Comprehensive Planning for Web AI` exports:

```text
the most recently generated native plan
```

which may be:

```text
Heuristic
or
Local AI
```

It does not follow the Imported Web AI display radio.

`Receive Planning from Web AI` reads the installed external artifact from:

```text
<drive>\
<project>_show_project_to_AI\
project_large_file_refactor_planner_web_ai_import\
pending_imported_web_ai_plan.txt
```

Then:

```text
validate source hash
validate base plan hash
apply bounded proposal
deterministically validate
show review
Load as Imported Web AI Version
```

Feature ID:

```text
large-file-refactor-planner-imported-web-ai-semantics-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_imported_web_ai_semantics_v1_patch.zip
```

SHA-256:

```text
05266e1c5ea91b391e8cb41c793f197a83cbefe11538c15200899a453cc7fa78
```

Associated Error Memory lesson:

```text
planner_imported_web_ai_semantic_conflation_v1
```

---

# 18. WEB AI SPECIALIST PROMPT / ROUTER / GUI WRAPPER WORK

The user requested a reusable online-AI workflow.

The correct architecture was determined to be:

```text
existing Large Module Refactor Protocol
        ↓
v7.3 delegation section
        ↓
specialist companion prompt
```

not a second competing general refactor canon.

Intended specialist prompt:

```text
KPR-06-001
```

Prompt ID:

```text
web_ai_large_module_refactor_exchange_protocol
```

Canonical intended location:

```text
kanda_prompt_workspace/
prompt_library/
ACTIVE_PROMPTS/
06_refactor_and_architecture_hardening/
web_ai_large_module_refactor_exchange_protocol.md
```

Purpose:

```text
teach online AI how to:
read comprehensive planning package
compare native architecture
search for bounded improvement
avoid merely copying native plan
avoid unnecessary redesign
create correct response
create installable import ZIP
create INSTALL.ps1
create VALIDATE.ps1
create FREEZE.ps1
create freeze hint
create manifest
respect import inbox
validate hashes
preserve Box Shielding / No-Leak
```

Router Bridge intended triggers include:

```text
external Web AI refactor version
online AI improve split plan
Imported Web AI Version
Copy Comprehensive Planning for Web AI
Receive Planning from Web AI
AI Refactor Version How To
```

A GUI wrapper button was added/intended:

```text
AI Refactor Version How To
```

Visual requirement:

```text
orange
bold
```

Position:

```text
immediately after:
Review & Refine Plan with Local AI
```

The button is a thin wrapper:

```text
click
    ↓
resolve canonical prompt-library path
    ↓
read KPR-06-001
    ↓
copy exact canonical prompt to clipboard
```

Do not embed a duplicate specialist prompt body in GUI code.

Feature ID:

```text
large-file-refactor-planner-web-ai-howto-prompt-button-v1
```

ZIP:

```text
kanda_large_file_refactor_planner_web_ai_howto_prompt_button_v1_patch.zip
```

SHA-256:

```text
9df31447640fa56021c45d32bd749d5f297e6dbf53affeb96eb05b1cdb7401fd
```

Verify local install/freeze state before relying on it.

---

# 19. COMPREHENSIVE WEB AI EXPORT REQUIREMENTS

The `Copy Comprehensive Planning for Web AI` package was intentionally improved.

It should provide:

```text
TASK
ACTIVE NATIVE BASE VERSION
SOURCE IDENTITY
SOURCE HASH
BASE PLAN HASH
PUBLIC API CONTRACT
CURRENT PLAN
HEURISTIC CANDIDATES
RESPONSIBILITY EVIDENCE
TOPOLOGY EVIDENCE
GIT HISTORY EVIDENCE + CONFIDENCE
QUALITY SCORES
LOCAL AI TOURNAMENT RESULT
KNOWN MODULES
KNOWN SYMBOLS
ATOMIC CLUSTERS
ALLOWED ACTIONS
FORBIDDEN ACTIONS
IMPROVEMENT GOAL
RESPONSE SCHEMA
ZIP CONTRACT
INSTALLER CONTRACT
VALIDATION CONTRACT
FREEZE-EVIDENCE CONTRACT
```

Core external AI instruction:

```text
Do not merely reproduce the native plan.

First determine whether a bounded,
evidence-backed architecture improvement exists.

Prefer:
one responsibility-outlier reassignment
one safe known-helper merge
one semantic rename
one bounded docstring improvement

Do not invent arbitrary modules or symbols.

If no bounded improvement is defensible,
return truthful no-improvement.
```

Allowed architecture actions remain bounded.

Typical response schema includes:

```text
module_merges
reassignments
module_renames
docstring_updates
architecture_answers
analysis_observations
rationale
warnings
```

Never allow Web AI to bypass deterministic validation.

---

# 20. CURRENT PRIMARY TASK: LARGE FILE REFACTOR WORKBENCH COMPLETION

This is now the next workstream.

The user explicitly requested that the Workbench be taken from current real-preview validation through a complete real refactor pipeline.

The user observed that:

```text
Large File Refactor Workbench
```

gets as far as real preview validation but downstream stages do not become usefully active.

User specifically mentioned:

```text
5. Preflight
Prepare Preflight Backup Readiness
Build Source Apply Payload
Apply Source Changes
Rollback Last Apply
Run Optional Behavior Validation
```

and noted there is no clear:

```text
Refactor Module
```

button.

An architecture audit was performed before implementation.

---

# 21. WORKBENCH AUDIT FINDINGS

## 21.1 Strong first half

The Workbench already has a strong conceptual first half:

```text
Planner selected version
        ↓
explicit Workbench plan intake
        ↓
immutable Workbench snapshot
        ↓
dependency readiness
        ↓
real preview generation
        ↓
real preview structural validation
```

Preserve this.

---

## 21.2 Do not force-enable Stage 5

The correct conclusion of the audit was:

> Do not simply enable downstream buttons.

The completion pipeline has deeper source and transaction issues.

---

## 21.3 Source-integrity gap around preflight

In the audited cumulative source reconstruction:

`workbench_gui.py` referenced preflight modules such as:

```text
source_apply_preflight_backup_contract.py

workbench_preflight_backup_readiness.py

workbench_preflight_backup_formatting.py
```

but these were not found in the provided reconstructed source state.

Important caveat:

The user's actual runtime opens the Workbench, so the live local tree may differ from the source archive used for audit.

Therefore next AI must:

```text
inspect exact local source
do not assume modules are absent
compare imports with actual files
run package import validation
```

The first Workbench patch should restore or reconcile the Stage 5 ownership seam.

---

## 21.4 Two overlapping apply architectures

Audit found two conceptually overlapping source-apply families.

Older governed family, approximately:

```text
final_guarded_source_apply_planning
source_apply_dry_run_validator
source_apply_preflight_backup_contract
guarded_source_apply_executor
post_apply_validation
source_apply_rollback_recovery
```

Newer Workbench family, approximately:

```text
workbench_preflight_backup_readiness
workbench_source_payload_builder
workbench_guarded_source_apply
workbench_post_apply_validator
workbench_rollback_executor
workbench_behavior_validation
```

Next AI must not create a third apply engine.

Required direction:

```text
one canonical interactive Workbench transaction owner
```

Older modules may become:

```text
internal reusable primitives
```

or be retired from active GUI ownership.

Do not leave split-brain ownership over:

```text
backup
transaction id
payload
apply state
rollback manifest
post-apply truth
completion state
```

---

## 21.5 Preview structural validity is not enough

Current Planner evidence can show:

```text
FACADE_BACK_REFERENCE_RISK
FACADE_BOUNDARY_CYCLE_RISK
```

A preview can be:

```text
syntactically valid
AST-valid
structurally plausible
```

while still having runtime problems such as:

```text
moved helper uses facade-owned global
missing runtime import
NameError
circular partial initialization
```

Therefore the Workbench needs a Shadow Apply Runtime Gate before real source mutation.

---

## 21.6 Visual diff exists conceptually but is not integrated into main completion flow

The audit found visual-diff support in the source family but not wired as a required Workbench gate.

Recommended:

```text
shadow apply pass
        ↓
Review Refactor Diff
        ↓
explicit Diff Reviewed state
        ↓
real apply may become armed
```

---

## 21.7 Import rewrite support exists but needs ownership integration

The source family includes import rewrite readiness/apply/rollback concepts.

Policy must remain:

```text
default:
preserve consumer imports through facade

optional explicit migration:
only when approved plan includes import migration
```

When import rewrites are needed, they should be part of the same transaction.

Do not create:

```text
split source transaction
then later separate import rewrite transaction
```

if that creates an intermediate broken state.

---

## 21.8 High-severity rollback enablement defect

The audit found a dangerous conceptual rule:

Rollback appeared to depend on both:

```text
apply status = applied
AND
post-apply status = validated
```

This is wrong.

When:

```text
source write succeeds
post-apply validation fails
```

that is exactly when rollback may be needed.

Correct rule:

```text
if any source mutation occurred
AND rollback manifest is valid
AND rollback has not already completed
    ↓
Rollback remains available
```

Post-apply failure should show:

```text
ROLLBACK RECOMMENDED
```

This is P0.

---

# 22. TARGET WORKBENCH STATE MACHINE

The recommended explicit state machine is:

```text
NO_PLAN
    ↓
PLAN_SNAPSHOT_READY
    ↓
DEPENDENCY_READY
    ↓
REAL_PREVIEW_READY
    ↓
PREVIEW_STRUCTURAL_PASS
    ↓
PREFLIGHT_READY
    ↓
SHADOW_APPLY_PASS
    ↓
VISUAL_DIFF_REVIEWED
    ↓
SOURCE_PAYLOAD_READY
    ↓
APPLY_ARMED
    ↓
REFACTORING
    ↓
APPLIED
    ↓
POST_APPLY_PASS
    ↓
BEHAVIOR_PASS
or
BEHAVIOR_NOT_RUN_ACCEPTED
    ↓
COMPLETED
```

Rollback availability is orthogonal:

```text
SOURCE_WRITE_STARTED
    ↓
ROLLBACK_AVAILABLE
```

until:

```text
rollback complete
or
transaction formally completed/superseded
```

---

# 23. REQUIRED DOWNSTREAM INVALIDATION RULES

Centralize state invalidation.

Examples:

## New Planner plan loaded

Invalidate:

```text
dependency readiness
preview
preview validation
preflight
shadow validation
visual diff review
payload
authorization token
```

## Preview regenerated

Invalidate:

```text
preview validation
preflight
shadow apply
visual diff review
payload
apply authorization
```

## Source changes externally

Invalidate:

```text
preflight
backup readiness
shadow validation
payload
apply authorization
```

Do not scatter this logic across ad hoc button handlers.

---

# 24. SHADOW APPLY REQUIREMENT

Recommended Workbench flow:

```text
preview structural pass
        ↓
preflight
        ↓
backup readiness
        ↓
build source payload
        ↓
SHADOW APPLY
        ↓
compile
        ↓
runtime import smoke
        ↓
dependency validation
        ↓
focused tests
        ↓
visual diff
        ↓
real apply authorization
```

Preferred isolation:

```text
Git worktree
```

when available.

Fallback:

```text
controlled project mirror under daily-work staging
```

Never shadow-apply in the active project root.

The shadow environment must preserve package-relative import behavior.

---

# 25. WORKBENCH TRANSACTION MODEL

Create one explicit transaction object, conceptually:

```text
WorkbenchRefactorTransaction
```

It should own at least:

```text
transaction_id

plan_snapshot_id
source_content_hashes
preview hashes
preflight evidence

backup directory
backup file hashes

payload manifest
payload file hashes
ordered operation list

applied operation index
generated helper list
modified source list

rollback manifest
rollback state

shadow validation evidence
post-apply validation evidence
behavior validation evidence

visual diff reviewed state
authorization state

completion state
```

Do not make the real apply reinterpret the plan independently from preview.

Preview and real apply should share one transformation/payload truth.

---

# 26. PREFLIGHT BACKUP READINESS TARGET

Preflight should prove:

```text
target source hash matches plan basis
expected project files unchanged
destination helper collisions absent
backup destination writable
backup snapshot created
backup hashes verified
rollback manifest prepared
payload basis hash matches preview basis
```

Backups should be under daily-work staging, e.g.:

```text
<project>_delete_after_daily_work/
large_file_refactor_workbench/
transactions/
<TX_ID>/
backup/
```

Do not put transient backup structures into active project root.

---

# 27. REQUIRED `REFACTOR MODULE` BUTTON

The user explicitly wants a clear completion action.

Recommended GUI:

```text
5. Preflight & Refactor

[ Prepare Preflight Backup Readiness ]

[ Run Shadow Apply Validation ]

[ Review Refactor Diff ]

[ Build Source Apply Payload ]

Authorization:
[ exact token ]

[ REFACTOR MODULE ]

[ Rollback Last Refactor ]
```

`Refactor Module` must be a wrapper over the canonical guarded Workbench transaction owner.

It must not become a third apply engine.

Enable only when:

```text
immutable plan snapshot valid
dependency readiness pass
real preview exists
preview structural validation pass
preflight backup ready
shadow apply pass
visual diff reviewed
payload ready
source hashes still match
authorization token exact
```

On click:

```text
REFACTOR MODULE
    ↓
canonical guarded apply transaction
    ↓
source write
    ↓
immediate post-apply validation
```

If validation fails:

```text
ROLLBACK RECOMMENDED
```

and rollback remains enabled.

---

# 28. POST-APPLY VALIDATION TARGET

Fast gate:

```text
expected files exist
file hashes match payload
py_compile touched files
compileall affected package
AST parse
public facade import smoke
direct consumer import smoke
dependency-cycle check
git diff --check when available
```

Medium gate:

```text
focused characterization tests
moved-symbol tests
public API compatibility tests
behavior presets
```

Full gate at phase boundary:

```text
broader project tests
architecture validation
fragmentation audit
workflow validation when applicable
```

Interpret pytest exit statuses explicitly.

A command that collected or ran zero intended tests is not strong behavior evidence.

---

# 29. BEHAVIOR VALIDATION TARGET

Existing behavior-validation safety should preserve:

```text
allowlisted commands
no arbitrary shell
timeout
exit status handling
```

Recommended GUI:

```text
Behavior Validation

Preset:
Focused tests inferred from target
Related tests from Planner evidence
Custom approved command

[ Collect Tests ]
[ Run Behavior Validation ]
```

Use collection evidence to avoid accidentally treating zero-test execution as success.

---

# 30. EXACT NEXT IMPLEMENTATION TRAIN

This is the recommended continuation sequence.

Do not skip directly to the `Refactor Module` button.

---

## PATCH 1 — Workbench Source Integrity and Preflight Restoration

Goal:

```text
restore coherent Stage 5 ownership
```

Tasks:

```text
inspect exact live Workbench source
reconcile missing/stale preflight imports
restore or consolidate preflight owner modules
make package imports pass
add explicit blocking-reason model
verify passed_with_warnings preview validation can advance
verify source/hash drift blocks preflight explicitly
```

Required UI improvement:

Disabled button should have visible reason.

Examples:

```text
PREFLIGHT BLOCKED:
PREVIEW_VALIDATION_NOT_ACCEPTED

PREFLIGHT BLOCKED:
SOURCE_HASH_DRIFT

PREFLIGHT BLOCKED:
PREFLIGHT_OWNER_UNAVAILABLE
```

This patch should not yet create the final Refactor Module action.

---

## PATCH 2 — Canonical Workbench Transaction Owner

Goal:

```text
one active apply ownership model
```

Create transaction model.

Reconcile overlapping apply families.

Decide explicitly which older modules are:

```text
reused primitives
or
retired from active GUI
```

Do not delete potentially useful governed logic without inspection.

---

## PATCH 3 — Shadow Apply and Runtime Readiness

Goal:

```text
prove transformed project works before real mutation
```

Implement:

```text
worktree when possible
or controlled mirror

apply exact payload
compile
import smoke
dependency topology validation
focused test validation
shadow result evidence
```

No real source mutation.

---

## PATCH 4 — Workbench Completion GUI

Wire:

```text
Preflight gate reason
Shadow Apply
Visual Diff Review
Build Payload
Authorization
REFACTOR MODULE
Rollback Last Refactor
Behavior Validation presets
```

Critical fix:

```text
rollback available after any real write
```

---

## PATCH 5 — End-to-End Refactor Transaction Validator

Build a real fixture with:

```text
large >500-line module
public facade
consumer imports
tests
cohesive helper targets
global dependency references
one intentionally risky dependency
```

Prove:

```text
Planner plan
→ Workbench snapshot
→ dependency readiness
→ preview
→ structural validation
→ preflight
→ backup
→ payload
→ shadow apply
→ runtime import
→ visual diff
→ Refactor Module
→ post-apply validation
→ behavior validation
→ rollback
→ exact restoration
→ second apply
→ successful completion
```

Also verify:

```text
public API preserved
consumer imports preserved
no unrelated file mutation
no helper cycles
no unresolved globals
no rollback residue
```

---

## PATCH 6 — Canon / Tutorial / Freeze Completion Update

Only after a successful end-to-end fixture and controlled real local refactor.

Then update:

```text
Workbench tutorial
Large Module Refactor Protocol completion section
freeze evidence schema
GUI help text
```

Do not freeze:

```text
Workbench can complete a real refactor
```

before it actually completes one successfully.

---

# 31. WORKBENCH PRIORITY LEVELS

## P0

```text
preflight source-integrity gap
one canonical transaction owner
runtime unresolved-global/import validation
rollback available after failed post-apply validation
```

## P1

```text
shadow apply
runtime import smoke
visual diff integration
import rewrite ownership
end-to-end validator
```

## P2

```text
Refactor Module primary button
explicit gate reasons
behavior preset integration
pytest collection awareness
stale wording cleanup
```

The button is intentionally after core safety repairs.

---

# 32. RESEARCH-DERIVED DESIGN PRINCIPLES TO KEEP

Prior web research produced several architectural conclusions that should continue guiding implementation.

## Heuristic

Line count is:

```text
a gate
```

not:

```text
the grouping algorithm
```

Use:

```text
structural dependency
semantic responsibility
dependency direction
source proximity
test affinity
optional Git co-change
```

to produce candidates.

Then apply:

```text
100–500 helper constraints
cycle detection
public API ownership
No-Leak
```

---

## Local AI

Local AI should be:

```text
bounded architectural search and critique
```

not:

```text
one-shot sovereign planner
```

Use:

```text
small tasks
targeted rejection feedback
separate naming
separate audit
multiple isolated candidates
deterministic KANDA selection
```

---

## Workbench

Real refactor should follow small, behavior-preserving, validated steps.

The real apply should not independently reinterpret the Planner plan.

Use a transaction model with:

```text
preview truth
payload truth
backup truth
apply truth
rollback truth
validation truth
```

---

# 33. DELIVERY RULES FOR CONTINUATION

For every implementation patch:

```text
deliver ZIP
install code
validate code
freeze-evidence code
```

When the work is a correction/error event:

```text
also deliver Error Memory intake staging code
```

This is an explicit human preference.

Error Memory flow:

```text
ZIP
→ install
→ validate
→ stage pending lesson under:

<project>_show_project_to_AI/
project_error_memory/
pending_ai_assisted_error_lesson_intake/

→ human review
→ Memorize Error
```

Never direct-write canonical Lessons.

---

# 34. POWERSHELL DELIVERY RULES

Use:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Do not derive drive root with fragile slash trimming.

Wrapper scripts should use independent `if` blocks.

Do not create detachable `else` patterns in copy/paste terminal snippets.

For marker counts:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($Marker)
).Count
```

Do not use:

```powershell
$PayloadText.Split($Marker)
```

as a literal substring occurrence counter.

---

# 35. GUI IMPLEMENTATION STYLE

Do not force-enable actions.

Every blocked stage should expose a reason.

Prefer:

```text
button disabled
+
visible machine-readable reason
```

over silent inactivity.

Long-running actions should use existing sonar/activity feedback patterns.

Do not introduce fixed geometry that breaks smaller displays.

The user prefers a functional strong UI rather than decorative complexity.

---

# 36. CURRENT HUMAN WORKING STYLE / EXPECTATIONS

The human prefers:

```text
implementation rather than prolonged theory
focused patches
exact install code
exact validation code
freeze code every time
Error Memory code on error/correction events
clear comparison of actual outputs
evidence-based architecture decisions
```

When the user says:

```text
go
```

continue the planned next implementation step without reopening settled architectural questions unless source evidence contradicts them.

When a runtime error is reported:

```text
inspect exact error
inspect exact source
repair narrowly
validate exact ZIP
stage Error Memory lesson
provide freeze code
```

Do not simply explain the error.

---

# 37. DO NOT REGRESS THESE SPECIFIC LESSONS

Do not:

```text
make version radios cosmetic
disable route selection before generation
reset selected route during Analyze File
show action completion feedback only on another hidden tab
treat Imported Web AI as a local generation route
export Web AI base according to display radio instead of last native plan
use whole-response json.loads only for local model transport
ask 7B Local AI to solve actions + names + 8 audits in one response
let AI choose tournament winner
treat two Git commits as strong historical evidence
mix exploratory action count with final winner action count
reject [] in the semantic naming stage as a fatal error
repeat all audit fields when only some are missing
count PowerShell markers with String.Split(marker)
create another general refactor canon that competes with large_module_refactor_protocol
embed canonical prompt text inside GUI wrapper
force-enable Workbench preflight/apply buttons without repairing state ownership
disable rollback after post-apply failure
create a third source-apply engine
```

---

# 38. SAFE CONTINUATION ENTRYPOINT

The next AI should begin with:

```text
TASK:
Large File Refactor Workbench Patch 1
Source Integrity and Preflight Restoration
```

First actions:

```text
1. Inspect exact local current source tree.

2. Read:
   - latest freeze context
   - large_module_refactor_protocol current canonical version
   - Workbench tutorial
   - Workbench GUI
   - plan snapshot/intake modules
   - preview renderer
   - structural validator
   - preflight modules/imports
   - payload builder
   - guarded apply modules
   - post-apply validator
   - rollback modules
   - behavior validation modules
   - visual diff modules
   - import rewrite modules

3. Build an ownership map.

4. Reproduce why Stage 5 does not become operational.

5. Do not force-enable it.

6. Repair source ownership and explicit gate reasons.

7. Validate:
   package imports
   stage transition
   passed_with_warnings transition
   blocked reason visibility
   preview/source hash invalidation
   no Workbench/Planner ownership leakage

8. Deliver:
   patch ZIP
   install code
   validation code
   Error Memory intake if a defect is corrected
   freeze-evidence code

9. Stop before Patch 2 unless the user explicitly says go/continue.
```

---

# 39. FINAL STATE SUMMARY

At the pause point:

```text
PLANNER:
substantially improved

Heuristic:
multi-signal
candidate-based
responsibility-aware
topology-aware
Git-confidence-aware

Local AI:
staged
targeted-retry capable
candidate tournament
KANDA-selected

Imported Web AI:
external artifact workflow
bounded validation
review before load
specialist prompt architecture
Router Bridge integration intended
GUI how-to wrapper delivered

WORKBENCH:
strong first half
incomplete second half
must be repaired as one transaction pipeline
```

The current next milestone is not another Planner feature.

The current milestone is:

> Make Large File Refactor Workbench safely complete a real module refactor from validated preview through preflight, backup, shadow apply, visual review, guarded source mutation, post-apply validation, behavior validation, rollback, and completed transaction state.

Do this incrementally.

Do not bypass gates.

Do not create competing owners.

Do not freeze completion claims before real end-to-end proof.

# SESSION_HANDOFF: 2026-07-05 | PROJECT: KANDA Reasoner

# STATUS: PAUSED | CONTEXT_WINDOW_USAGE: HIGH — USE THIS HANDOFF AS PRIMARY CONTINUATION MAP

---

## 1. CANON (IMMUTABLE GROUND TRUTHS)

*Do not alter, bypass, reinterpret loosely, or refactor these principles without an explicit canon update and governed validation/freeze process.*

### Core Architectural Paradigm

* **Architecture model**: Box Logic + KANDA Box Shielding + No-Leak Logic.
* **Active root**: `E:\kanda_reasoner`.
* **Tool/project distinction is mandatory**:

  * KANDA Reasoner tool code belongs to the KANDA tool source tree.
  * Selected-project output must never leak into KANDA tool ownership.
  * Tool-owned refactor engines may analyze and transform selected projects only through explicit governed contracts.

### No-Leak Logic

No-Leak Logic is a named architecture object.

It must explicitly prevent:

* wrong-root writes;
* tool/project leakage;
* cross-box leakage;
* private reach-in;
* hidden mutable state;
* public API ownership leakage;
* generated-artifact-as-source leakage;
* validation/freeze evidence leakage.

Before implementation, the AI must identify:

```text
active box
owner paths
allowed files
out-of-scope files
cross-box touches
public contracts
validation scope
```

### Planner / Workbench Ownership Boundary

The canonical mental model is:

```text
AST Split Audit
        ↓
Large File Refactor Planner
        ↓
selected isolated planning version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench-owned snapshot
        ↓
Large File Refactor Workbench
        ↓
implementation transaction
```

The Planner owns:

```text
analysis
architecture planning
candidate generation
version comparison
docstring proposals
Local AI bounded review
Imported Web AI planning review
planning summaries
```

The Planner must not mutate source.

The Workbench owns:

```text
dependency readiness
real preview
preview validation
preflight
backup
source payload
shadow apply
real apply
post-apply validation
behavior validation
rollback
transaction completion
```

### Planner Version Semantics

The valid planning versions are:

```text
Heuristic
Local AI
Imported Web AI Version
```

Their meanings are immutable unless canonically updated.

#### Heuristic

Locally generated deterministic architecture.

#### Local AI

Deterministic native architecture plus bounded Local AI architectural search, deterministic validation, candidate tournament, and KANDA-owned winner selection.

#### Imported Web AI Version

An externally generated planning version.

It is not locally generated by selecting its radio.

Correct flow:

```text
Generate Heuristic or Local AI
        ↓
latest generated native plan stored
        ↓
Copy Comprehensive Planning for Web AI
        ↓
external online AI analyzes package
        ↓
external AI returns governed import ZIP
        ↓
install imported artifact
        ↓
Receive Planning from Web AI
        ↓
validate
        ↓
review
        ↓
Load as Imported Web AI Version
```

### Public API Preservation

Large-module refactors must preserve public import contracts unless a separate explicit API migration is approved.

The default first-pass model is:

```text
existing public import path
        ↓
thin public facade
        ↓
private responsibility helpers
```

Consumers should continue importing through the public facade by default.

### Module Size Law

For Python source modules:

```text
ideal: <= 400 physical lines
hard maximum: <= 500 physical lines
practical new-helper minimum: approximately 80–100 substantive lines
```

Small helper exceptions require explicit architectural justification.

Line count is a constraint, not the grouping algorithm.

Group primarily by:

```text
responsibility
dependency direction
semantic cohesion
atomic clusters
public API ownership
topology
test affinity
optional historical coupling
```

### Freeze Law

Never claim something is frozen merely because:

```text
a ZIP was created
a patch installed
validation passed
freeze evidence merged
```

Final canonical freeze requires:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

Latest canonical freeze memory is authoritative.

### Error Memory Law

On a correction/error event:

```text
repair
→ validate
→ stage KANDA_ERROR_LESSON into pending intake
→ human review
→ Memorize Error
```

Never direct-write canonical Lessons.

Pending intake path:

```text
<project>_show_project_to_AI/
project_error_memory/
pending_ai_assisted_error_lesson_intake/
```

### PowerShell Rules

Use:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Do not use fragile slash trimming.

For literal marker counting use:

```powershell
[regex]::Matches(
    $PayloadText,
    [regex]::Escape($Marker)
).Count
```

Do not use:

```powershell
$PayloadText.Split($Marker)
```

as a literal whole-marker occurrence counter.

### Delivery Requirement

Every governed implementation patch should provide:

```text
patch ZIP
install terminal code
validation terminal code
freeze-evidence terminal code
```

When fixing an actual error:

```text
also provide Error Memory staging code
```

---

## 2. FROZEN (COMPLETED & LOCKED MODULES)

*Only items whose frozen status is known from existing project context belong here. Do not infer that every patch built in this session is frozen.*

### Patch Validate Freeze Recovery Blueprint v1

Status: frozen feature active as of 2026-06-29.

Protected behavior:

* Show Project to AI exposes `Copy Patch Validate Freeze Recovery Routine`.
* The wrapper reads:
  `patch_validate_freeze_error_memory_routine_blueprint.md`.
* Selected active project root is preferred.
* App-root fallback is allowed only when necessary.
* The wrapper remains thin and references owner canons.
* Routing recognizes:

  * Show Project to AI file/ZIP creation failures;
  * patch/validate/freeze recovery routine requests.
* ZIP validation, local validation, freeze evidence merge, Preview, and Confirm and Write may not be bypassed.

### Startup Freeze Context Latest Entries v1

Status: frozen feature active as of 2026-06-29.

Protected behavior:

* startup freeze context loads latest entries newest-first;
* canonical external freeze memory location is:

```text
<project>_show_project_to_AI/
project_freeze_after_update/
frozen_features_memory/
```

* compact freeze-report truncation may not hide newer entries;
* newer canonical entries override older compact-report lines when they conflict.

### Important Freeze Caution

The Planner patches created during this workstream are not automatically listed here.

Before changing or replacing any of them, inspect:

```text
latest canonical freeze entries
current source tree
installed patch evidence
```

Some session patches were delivered and validated, but canonical freeze completion must be verified locally.

---

## 3. ACTIVE CONTEXT (WHAT WE ARE DOING)

### Current Epic

Complete the KANDA Large File Refactor architecture as a safe end-to-end system:

```text
Planner
        ↓
selected architecture version
        ↓
immutable Workbench snapshot
        ↓
real preview
        ↓
validated implementation transaction
        ↓
successful module refactor
        ↓
post-apply validation
        ↓
behavior validation
        ↓
rollback capability
        ↓
completion state
```

### Current Sprint Goal

Repair and complete the **Large File Refactor Workbench** from the current preview-validation stage through:

```text
Preflight
Backup Readiness
Source Apply Payload
Shadow Apply
Visual Diff Review
Refactor Module
Post-Apply Validation
Behavior Validation
Rollback
Completion
```

### Work Done So Far in This Chat Session

#### Planner architecture was substantially strengthened

The Planner evolved from an initial dependency-cluster splitter that generated:

```text
facade: 197 lines

helpers:
38
100
371
41
51
37

status: blocked
```

into a multi-signal deterministic planner producing:

```text
facade: 197

path_resolution: 122

helper_selection: 452

status: planned
```

#### Step 1 — Multi-signal Heuristic

Implemented:

```text
structural affinity
semantic affinity
source proximity
role compatibility
multiple candidate strategies
hard size gates
deterministic ranking
```

Strategies:

```text
dependency-dominant
balanced
responsibility-dominant
```

Reference feature:

```text
large-file-refactor-planner-heuristic-multisignal-candidate-ranking-v1
```

#### Step 2 — Responsibility Labeling and Semantic Naming

Implemented deterministic labels:

```text
primary responsibility
secondary responsibilities
confidence
evidence tokens
semantic filenames
```

Reference result:

```text
_main_helper_mapper_path_resolution.py
_main_helper_mapper_helper_selection.py
```

Reference feature:

```text
large-file-refactor-planner-responsibility-labeling-semantic-naming-v1
```

#### Step 3 — Topology and Quality Scoring

Added projected module topology and quality evidence.

Distinguishes:

```text
helper-only cycle
    = hard blocker

facade back-reference
    = explicit boundary risk
```

Real case evidence included:

```text
responsibility cohesion: 0.849312
topology score: 0.92
mixed-responsibility penalty: 0.150688
```

Reference feature:

```text
large-file-refactor-planner-topology-responsibility-quality-scoring-v1
```

#### Step 4 — Staged Local AI Protocol

Changed Local AI from one oversized request into:

```text
Responsibility Analysis
        ↓
Targeted Architecture Repair
        ↓
Deterministic Validation
        ↓
Exact-Rejection Targeted Retry
        ↓
Semantic Naming Review
        ↓
Final Architecture Audit
```

Reference feature:

```text
large-file-refactor-planner-staged-local-ai-protocol-v1
```

#### Step 5 — Local AI Candidate Tournament

Added:

```text
baseline control

Candidate A:
conservative/minimal-change

Candidate B:
responsibility/cohesion

Candidate C:
topology/boundary safety
```

Each starts from the same logical baseline.

KANDA deterministically validates and scores them.

The model does not choose the winner.

Reference feature:

```text
large-file-refactor-planner-local-ai-candidate-tournament-v1
```

#### Step 6 — Git Historical Coupling

Added optional read-only Git co-change evidence.

Git evidence is supporting only.

It cannot override:

```text
atomic cluster authority
size gates
cycle gates
public facade ownership
Box Shielding
No-Leak Logic
```

Reference feature:

```text
large-file-refactor-planner-git-cochange-history-v1
```

#### Quality Hardening

Real Local AI output exposed four issues.

Fixed:

```text
exploration action count
vs
final selected action count
```

Naming stage now tolerates:

```json
[]
```

as a stage-specific no-op.

Audit retries request only missing fields.

Git history confidence weighting was added.

Reference model:

```text
0 commits       none       0.00
1–2 commits     very_low   0.15
3–5 commits     low        0.35
6–15 commits    moderate   0.65
16+ commits     high       1.00
```

Reference feature:

```text
large-file-refactor-planner-quality-hardening-v1
```

#### Local AI JSON Adapter Repair

Earlier Local AI outputs failed due to transport-wrapper parsing.

The adapter was expanded to safely extract one bounded JSON object from:

```text
plain JSON
fenced JSON
<think>...</think> + JSON
light prose + JSON
marker-wrapped JSON
```

Schema and architecture validation remain strict.

Reference feature:

```text
large-file-refactor-planner-local-ai-json-adapter-repair-v1
```

#### Imported Web AI Semantics

Corrected the architecture so Imported Web AI is not treated as a local generation route.

Reference feature:

```text
large-file-refactor-planner-imported-web-ai-semantics-v1
```

#### Real Web AI Example

For:

```text
main_helper_mapper.py
```

the Heuristic architecture was:

```text
122 / 452
```

A bounded external Web AI proposal moved:

```text
_related_tests_to_run
```

from:

```text
helper_selection
```

to:

```text
path_resolution
```

producing:

```text
145 / 429
```

Deterministic comparison evidence used during planning:

```text
baseline: 0.736690
Imported Web AI: 0.783250
```

This demonstrated the intended external Web AI role:

```text
small bounded evidence-backed improvement
```

rather than:

```text
copy native plan unchanged
```

or:

```text
invent an entirely unrelated architecture
```

#### Web AI Specialist Prompt Architecture

The existing Large Module Refactor Protocol remains the core owner.

The intended architecture is:

```text
large_module_refactor_protocol v7.3
        ↓ delegates
KPR-06-001
Web AI Large Module Refactor Exchange and Import Protocol
```

The specialist prompt teaches external online AI to:

```text
read Comprehensive Planning package
evaluate native plan
search for bounded improvement
respect known symbols/modules
preserve atomic clusters
create correct response schema
create governed ZIP
create correct installer
validate hashes
create freeze-evidence bundle
```

A thin GUI wrapper was delivered:

```text
AI Refactor Version How To
```

Requirements:

```text
orange
bold
immediately after Review & Refine Plan with Local AI
```

The button should read the canonical specialist prompt and copy it to clipboard.

It must not embed a duplicate prompt body in GUI source.

Reference feature:

```text
large-file-refactor-planner-web-ai-howto-prompt-button-v1
```

---

## 4. METHODOLOGY & STACK (HOW WE ARE DOING IT)

### Language and Runtime

Primary implementation language:

```text
Python
```

GUI:

```text
PySide6 / Qt
```

PowerShell is used for governed:

```text
install
validation
freeze-evidence merge
Error Memory staging
```

### Source Transformation Philosophy

Prefer:

```text
whole-symbol movement
responsibility islands
format-preserving transformation
deterministic evidence
```

Avoid:

```text
arbitrary line slicing
physical half/half splitting
statement-block extraction
source stored as runtime ZIP payload architecture
tiny helper proliferation
```

LibCST or equivalent formatting-preserving editing is preferred for deterministic source edits.

### Planner Methodology

The Planner architecture is:

```text
deterministic evidence first
        ↓
multiple candidates
        ↓
hard gates
        ↓
quality scoring
        ↓
optional bounded Local AI search
        ↓
optional external Web AI proposal
        ↓
deterministic validation
```

### AI Authority Rule

AI may propose.

AI does not become source truth.

KANDA owns:

```text
validation
candidate scoring
winner selection
source mutation
rollback truth
freeze evidence
```

### Testing Strategy

For each implementation patch:

```text
focused validator
Python compilation
package import smoke
box-boundary validation
No-Leak validation
module-size validation
ZIP contract validation
previous-step regression validators
```

For real refactor execution, target validation ladder is:

#### Fast Gate

```text
expected files exist
hashes match
py_compile
compileall
AST parse
public facade import smoke
consumer import smoke
cycle check
git diff --check when available
```

#### Medium Gate

```text
characterization tests
moved-symbol tests
public API compatibility tests
behavior presets
```

#### Full Gate

```text
broader project tests
architecture validation
fragmentation audit
workflow validation when applicable
```

### Error Handling Pattern

Do not silently fail.

Long-running GUI actions should use visible activity feedback.

Disabled actions should expose blocking reasons.

Preferred:

```text
PREFLIGHT BLOCKED:
SOURCE_HASH_DRIFT
```

instead of an unexplained disabled button.

### Delivery Strategy

Each governed patch must be independently:

```text
installable
validatable
freeze-preparable
rollback-aware
```

Sequential patch trains must remain:

```text
Patch A:
install → validate → freeze

Patch B:
install → validate → freeze
```

Never:

```text
install A
install B
install C
validate everything later
```

---

## 5. CURRENT STATE (EXACT CHECKPOINT)

### Active Development Focus

```text
Large File Refactor Workbench
```

### Current Known Good Conceptual Pipeline

```text
Planner selected version
        ↓
explicit Load Latest Planner Plan
        ↓
immutable Workbench snapshot
        ↓
Dependency Readiness
        ↓
Generate Real Preview
        ↓
Validate Real Preview
```

The Workbench's first half is conceptually strong.

### Current Problem

The Workbench does not yet form one proven end-to-end source-refactor transaction.

The user reports the downstream flow around:

```text
5. Preflight

Prepare Preflight Backup Readiness
Build Source Apply Payload
Apply Source Changes
Rollback Last Apply
Run Optional Behavior Validation
```

does not behave as a complete usable pipeline.

There is also no clear primary:

```text
Refactor Module
```

button.

### Important Audit Findings

#### Finding A — Do Not Force-Enable Stage 5

The issue is not merely button enablement.

The completion pipeline has deeper ownership and runtime-validation gaps.

#### Finding B — Possible Preflight Source-Integrity Gap

The audited reconstruction showed GUI references to modules such as:

```text
source_apply_preflight_backup_contract.py
workbench_preflight_backup_readiness.py
workbench_preflight_backup_formatting.py
```

while those modules were not found in the reconstructed archive state.

The live runtime may differ.

Therefore first continuation action is:

```text
inspect exact local source
reproduce exact Stage 5 blocker
validate package imports
```

Do not assume the files are actually missing locally.

#### Finding C — Two Overlapping Apply Architectures

Older apply family approximately:

```text
final_guarded_source_apply_planning
source_apply_dry_run_validator
source_apply_preflight_backup_contract
guarded_source_apply_executor
post_apply_validation
source_apply_rollback_recovery
```

Newer Workbench family approximately:

```text
workbench_preflight_backup_readiness
workbench_source_payload_builder
workbench_guarded_source_apply
workbench_post_apply_validator
workbench_rollback_executor
workbench_behavior_validation
```

There must be one active transaction owner.

Do not create a third apply engine.

#### Finding D — Structural Preview Validation Is Insufficient

A generated preview can be:

```text
syntax-valid
AST-valid
structurally valid
```

while still having runtime errors due to:

```text
unresolved global
missing import
facade back-reference
partial circular initialization
```

Therefore real apply must eventually be preceded by:

```text
Shadow Apply Runtime Validation
```

#### Finding E — Rollback Gating Is Potentially Dangerous

Rollback must remain available after any real source mutation.

Correct model:

```text
SOURCE_WRITE_STARTED
        ↓
ROLLBACK_AVAILABLE
```

Post-apply failure should produce:

```text
ROLLBACK RECOMMENDED
```

not disable rollback.

#### Finding F — Visual Diff Needs Main-Flow Integration

Visual diff support exists conceptually but should become an explicit gate:

```text
Shadow Apply Pass
        ↓
Review Refactor Diff
        ↓
Diff Reviewed
        ↓
real apply may be armed
```

### Branch / Commit Status

Unknown from this handoff.

Upon resume:

```text
inspect git status
inspect current branch
inspect latest commits
do not automatically rewrite history
```

Do not assume any specific branch or commit hash.

### Uncommitted Changes

Unknown.

The AI must inspect the actual local tree before patching.

### Environment Requirements

Known project root:

```text
E:\kanda_reasoner
```

Expected external workflow roots derive from:

```powershell
[System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Typical generated external locations include:

```text
E:\kanda_reasoner_delete_after_daily_work\
E:\kanda_reasoner_show_project_to_AI\
```

Do not invent alternate roots.

---

## 6. BLOCKERS / UNRESOLVED EDGE CASES

### 1. Workbench Stage 5 Source Ownership

Need to inspect exact live source and determine whether:

```text
preflight modules are absent
preflight imports are stale
preflight owner exists under another architecture
GUI state transition is incorrect
```

Do not repair by blindly enabling controls.

### 2. Apply Architecture Split-Brain

Two source-apply families appear to overlap.

Need an ownership map for:

```text
preflight
backup
payload
apply
post-apply validation
rollback
behavior validation
completion state
```

Exactly one active GUI transaction owner must emerge.

### 3. Runtime Import Safety

Current preview validation must be audited for:

```text
moved helper unresolved globals
missing synthesized imports
facade-helper circular initialization
consumer import compatibility
```

This is a major reason to add Shadow Apply.

### 4. Multi-File Apply Transaction Safety

Per-file `os.replace` is not equivalent to a whole-refactor atomic transaction.

Need an explicit transaction manifest tracking:

```text
ordered operations
applied operation index
backups
generated helper files
rollback plan
post-apply evidence
```

### 5. Rollback Availability

Rollback must not depend on successful post-apply validation.

Any real write should activate rollback capability.

### 6. Visual Diff Review

Need a human-visible required diff review state before real apply.

### 7. Import Rewrite Ownership

Import migration logic must remain optional and explicit.

Default:

```text
consumers continue importing from facade
```

When import migration is approved, it should be part of the same transaction.

### 8. Behavior Validation Strength

Need to distinguish:

```text
tests truly executed and passed
```

from:

```text
zero intended tests collected
```

Consider collection verification before behavior execution.

### 9. Freeze Status Uncertainty for Session Patches

Do not assume session-delivered Planner patches are frozen.

Check canonical freeze memory before modifying their protected behavior.

---

## 7. IMMEDIATE NEXT ACTIONS (FOR THE AI TO EXECUTE)

Execute sequentially.

### ACTION 1 — Inspect Exact Current Workbench Source

Read and map:

```text
workbench_gui.py

planner_workbench_handoff.py
workbench_plan_intake.py
workbench_plan_snapshot.py
workbench_snapshot_bridge.py

preview renderer modules
real preview validator modules

preflight modules
backup modules

source payload builder
guarded apply modules

post-apply validator
rollback modules

behavior validation modules

visual diff modules
import rewrite modules

Workbench tutorial
current large_module_refactor_protocol.md
latest freeze entries
Error Memory lessons relevant to Workbench
```

### ACTION 2 — Reproduce the Stage 5 Blocker

Determine precisely why:

```text
Prepare Preflight Backup Readiness
```

does not become operational after a valid real preview.

Test at least:

```text
preview status = passed
preview status = passed_with_warnings
preview hash changed
source hash changed
preflight owner import missing
```

Output explicit machine-readable reason.

### ACTION 3 — Produce Box Ownership Audit

State:

```text
active box
owner paths
allowed changes
out-of-scope changes
cross-box touches
public contracts
validation scope
```

Do not implement before this audit.

### ACTION 4 — Build Patch 1

Patch title:

```text
Workbench Source Integrity and Preflight Restoration
```

Goals:

```text
repair/reconcile preflight owner modules
make package imports pass
restore valid preview → preflight transition
add explicit gate-reason model
block stale preview/source hashes
preserve Planner/Workbench isolation
```

Do not yet add the final `Refactor Module` button.

### ACTION 5 — Validate Patch 1

Required proof:

```text
Workbench package import: PASS
preflight owner import: PASS

passed preview:
preflight available

passed_with_warnings:
preflight available when contract allows

blocked preview:
preflight unavailable
blocking reason visible

preview hash drift:
preflight blocked

source hash drift:
preflight blocked

Planner snapshot mutation:
does not silently contaminate Workbench

Box Shielding: PASS
No-Leak Logic: PASS
module-size gate: PASS
ZIP contract: PASS
```

### ACTION 6 — Deliver Governed Artifact

Provide:

```text
patch ZIP
install terminal code
validate terminal code
freeze-evidence terminal code
```

If the repair fixes an actual defect:

```text
also include Error Memory staging terminal code
```

### ACTION 7 — Stop After Patch 1

Do not automatically continue into transaction-owner consolidation unless the human says:

```text
go
continue
```

---

## 8. CONTINUATION PROTOCOL (SAFETY GUARDRAILS)

### First Action Upon Resume

Do not start by editing code.

First:

```text
1. inspect current source tree
2. inspect latest canonical freeze entries
3. inspect git status and current branch
4. inspect relevant Error Memory lessons
5. inspect current Workbench imports/state transitions
6. reproduce Stage 5 blocker
```

### Autonomy Threshold

The AI may autonomously:

```text
inspect source
run static analysis
run focused validation
repair narrowly scoped implementation defects
add focused validators
stage Error Memory pending lesson
package governed patch ZIP
```

The AI must not autonomously:

```text
bypass Workbench gates
force-enable source mutation
direct-write canonical freeze memory
direct-write Error Memory Lessons
replace Planner/Workbench ownership model
invent a third apply engine
alter frozen behavior without explicit override
```

### Stoppage Conditions

Stop the current patch train when:

```text
package import fails unexpectedly
freeze memory conflicts with handoff assumptions
exact local source differs materially from audited architecture
source ownership is ambiguous
a patch would require bypassing validation
rollback cannot be made reliable
cross-box ownership cannot be resolved
```

When blocked, produce exact evidence rather than a speculative patch.

### Error Event Protocol

When a runtime/install/validation/freeze error occurs:

```text
inspect exact traceback
inspect exact source
inspect Error Memory formulary
repair narrowly
validate exact package
stage pending lesson
provide Error Memory terminal code
provide freeze code
```

### Freeze Protocol

Do not say:

```text
feature frozen
```

after only:

```text
validation pass
freeze hint creation
freeze evidence merge
```

Canonical completion is:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

### Context Compression Rule

When context becomes large, preserve in full:

```text
CANON
FROZEN
ACTIVE CONTEXT
CURRENT STATE
BLOCKERS
IMMEDIATE NEXT ACTIONS
CONTINUATION PROTOCOL
```

Lower-priority raw source excerpts may be dropped.

Never compress away:

```text
Planner/Workbench ownership boundary
No-Leak Logic
version semantics
freeze law
Error Memory law
exact next Workbench patch order
rollback availability rule
do-not-create-third-apply-engine rule
```

### Do-Not-Regress List

Do not:

```text
make version radios cosmetic
disable version selection until after generation
reset selected version during Analyze File
treat Imported Web AI as a local generator
export Web AI package based on display radio instead of latest native plan
embed canonical prompts in GUI wrappers
use whole-response-only JSON parsing for Local AI transport
ask small Local AI models to solve actions + naming + audit in one response
let AI choose tournament winner
treat weak Git history as strong evidence
mix candidate exploration action counts with final applied action counts
reject [] as fatal in naming stage
retry complete audit when only fields are missing
count PowerShell markers with String.Split(marker)
create a competing general large-module refactor canon
force-enable Workbench preflight/apply controls
disable rollback after post-apply failure
create a third source-apply engine
allow real apply to reinterpret the plan differently from preview
freeze end-to-end Workbench completion before proving it
```

### Planned Workbench Train After Patch 1

After explicit human continuation:

```text
PATCH 2
Canonical Workbench Transaction Owner

PATCH 3
Shadow Apply and Runtime Readiness

PATCH 4
Workbench Completion GUI
including:
Refactor Module
Visual Diff Review
Rollback Last Refactor
Behavior Validation integration

PATCH 5
End-to-End Refactor Transaction Validator

PATCH 6
Tutorial / Canon / Freeze Completion Update
```

The final target architecture is:

```text
PLANNER VERSION
        ↓
IMMUTABLE WORKBENCH SNAPSHOT
        ↓
DEPENDENCY READINESS
        ↓
REAL PREVIEW
        ↓
STRUCTURAL VALIDATION
        ↓
PREFLIGHT
        ↓
BACKUP
        ↓
SOURCE PAYLOAD
        ↓
SHADOW APPLY
        ↓
COMPILE + IMPORT + TEST GATES
        ↓
VISUAL DIFF REVIEW
        ↓
EXACT AUTHORIZATION
        ↓
REFACTOR MODULE
        ↓
POST-APPLY VALIDATION
        ↓
BEHAVIOR VALIDATION
        ↓
COMPLETED
```

From the first real source mutation onward:

```text
ROLLBACK AVAILABLE
```

until:

```text
rollback complete
```

or:

```text
transaction formally completed or superseded
```

---

# END OF SESSION HANDOFF

Primary continuation entrypoint:

```text
Large File Refactor Workbench
Patch 1:
Source Integrity and Preflight Restoration
```

Do not begin with the final `Refactor Module` button.

Repair the source ownership seam and state transition first.

Do not bypass gates.

Do not create competing owners.

Do not claim frozen status without canonical evidence.

Do not allow a source write unless rollback remains available afterward.

