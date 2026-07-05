# SESSION_HANDOFF: [YYYY-MM-DD] | PROJECT: [PROJECT_NAME]

# STATUS: [PAUSED / ACTIVE_BLOCKER / READY_TO_CONTINUE / VALIDATION_PENDING / FREEZE_PENDING]

# CONTEXT_WINDOW_USAGE: [LOW / MEDIUM / HIGH / CRITICAL]

---

## 0. READ THIS FIRST

This handoff is the operational continuation map for the next AI session.

It does not override:

```text
latest canonical freeze memory
active Prompt Library canons
Router Bridge routing
Box Logic
KANDA Box Shielding
No-Leak Logic
Error Memory
current local source truth
newer validated project evidence
```

Before implementation, the next AI must:

```text
1. Load startup context.
2. Read latest freeze entries newest-first.
3. Inspect the exact current source tree.
4. Inspect git status and current branch when Git is available.
5. Inspect relevant Error Memory lessons.
6. Compare this handoff against current source and freeze truth.
7. Resolve discrepancies before editing.
```

Do not assume:

```text
ZIP created = installed

installed = validated

validated = frozen

freeze evidence merged = canonically frozen
```

Canonical freeze requires:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

When this handoff conflicts with newer canonical freeze memory, the newer canonical freeze entry wins.

---

# 1. CANON — IMMUTABLE GROUND TRUTHS

*Record only architecture and governance truths that must survive context compression and session changes.*

## 1.1 Active Project Identity

```text
Project name: [PROJECT_NAME]

Project root:
[PROJECT_ROOT]

Project slug:
[PROJECT_SLUG]

Primary language/runtime:
[LANGUAGE_AND_RUNTIME]

Primary GUI/runtime framework:
[GUI_FRAMEWORK_OR_NONE]

Primary package/build environment:
[PACKAGE_ENVIRONMENT]
```

## 1.2 Architectural Paradigm

Active architectural model:

```text
[BOX_LOGIC / CLEAN_ARCHITECTURE / PLUGIN_ARCHITECTURE / OTHER]
```

Required ownership rules:

```text
[OWNER_RULE_1]
[OWNER_RULE_2]
[OWNER_RULE_3]
```

The project must distinguish clearly between:

```text
tool-owned source
project-owned source
generated artifacts
external handoff artifacts
validation evidence
freeze evidence
temporary daily-work artifacts
```

## 1.3 Box Logic Requirement

Before implementation, repair, refactor, prompt update, GUI change, bundle creation, or architecture change, the AI must state:

```text
active box
owner paths
files allowed to change
files explicitly out of scope
cross-box touches
public contracts
validation scope
```

Required format:

```text
IMPLEMENTATION GATE

Task domain:
Active box:
Owner paths:
Allowed changes:
Out of scope:
Cross-box touches:
Public contracts preserved:
Validation scope:
May implement: YES / NO
```

## 1.4 KANDA Box Shielding

Preserve box boundaries.

Do not:

```text
reach into another box's private internals
duplicate another box's owned logic
make hidden cross-box mutable state
bypass public contracts
move ownership merely for convenience
```

Cross-box interaction must use:

```text
public API
explicit adapter
explicit handoff artifact
approved shared contract
```

## 1.5 No-Leak Logic

No-Leak Logic is a named architecture object.

It must prevent:

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

Every implementation should explicitly check:

```text
NO-LEAK CHECK

Canonical source:
Generated artifacts:
Temporary artifacts:
External writes:
Forbidden writes:
Validation evidence ownership:
Freeze evidence ownership:
Safe next action:
```

## 1.6 Source of Truth

Canonical source truth for this project:

```text
[CANONICAL_SOURCE_PATHS]
```

Generated or derived artifacts that are not source truth:

```text
[GENERATED_PATHS]
```

Temporary staging root:

```text
<drive>/<project>_delete_after_daily_work/
```

External AI/show-project root:

```text
<drive>/<project>_show_project_to_AI/
```

Do not turn:

```text
ZIP payloads
generated reports
preview output
validation output
freeze hints
temporary source mirrors
```

into runtime source ownership.

## 1.7 Public Contract Law

Protected public contracts:

```text
[PUBLIC_API_CONTRACTS]
```

Default behavior:

```text
preserve existing public import path
preserve public facade ownership
preserve stable external names
preserve user-facing workflow semantics
```

Any public API migration must be explicit, separately validated, and separately frozen when required.

## 1.8 Validation Law

Minimum validation policy:

```text
compile/import validation
focused regression validation
box-boundary validation
No-Leak validation
public contract validation
module-size validation when code modules change
exact ZIP contract validation for delivery artifacts
workflow validation when workflow changes
```

Validation should use the cheapest sufficient gate during iteration and stronger gates at phase boundaries.

Example:

```text
Fast Gate
→ compile
→ import smoke
→ focused source contract

Medium Gate
→ focused tests
→ public API compatibility
→ moved-feature behavior

Full Gate
→ broader tests
→ architecture validation
→ workflow validation
→ fragmentation audit when applicable
```

## 1.9 Freeze Law

Never claim a feature is frozen because:

```text
patch exists
install passed
validation passed
freeze hint exists
freeze evidence merge passed
```

Final canonical freeze requires:

```text
Freeze Feature After Update
→ Preview
→ Confirm and Write
```

Latest canonical freeze entries must be read newest-first.

## 1.10 Error Memory Law

When an actual error, failed assumption, incorrect generated artifact, broken installer, regression, or repair event occurs:

```text
inspect exact failure
repair narrowly
validate repair
create pending Error Memory lesson
stage for human review
Memorize Error only after review
```

Pending intake path:

```text
<project>_show_project_to_AI/
project_error_memory/
pending_ai_assisted_error_lesson_intake/
```

Never write directly to canonical Lessons.

## 1.11 Delivery Law

For governed patch work, provide:

```text
patch ZIP
install terminal code
validation terminal code
freeze-evidence terminal code
rollback instructions when applicable
```

When the work fixes an actual error:

```text
also provide Error Memory staging code
```

## 1.12 PowerShell Rules

Use:

```powershell
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
```

Avoid fragile root derivation.

For literal marker counting:

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

as a literal full-marker occurrence counter.

---

# 2. FROZEN — COMPLETED AND LOCKED FEATURES

*List only features proven frozen by canonical freeze memory.*

Do not place merely delivered or validated features here.

## 2.1 Frozen Feature Inventory

### [FROZEN_FEATURE_1]

```text
Feature ID:
[FEATURE_ID]

Frozen date:
[DATE]

Owner box:
[OWNER_BOX]

Owner paths:
[PATHS]
```

Protected behavior:

```text
[PROTECTED_BEHAVIOR_1]
[PROTECTED_BEHAVIOR_2]
[PROTECTED_BEHAVIOR_3]
```

Do not regress:

```text
[NON_REGRESSION_RULES]
```

---

### [FROZEN_FEATURE_2]

```text
Feature ID:
[FEATURE_ID]

Frozen date:
[DATE]

Owner box:
[OWNER_BOX]

Owner paths:
[PATHS]
```

Protected behavior:

```text
[PROTECTED_BEHAVIOR]
```

---

## 2.2 Frozen-State Caution

The following items are not automatically frozen merely because they were worked on:

```text
[DELIVERED_BUT_FREEZE_UNCONFIRMED_FEATURES]
```

Before touching them:

```text
inspect latest canonical freeze memory
inspect installed source
inspect validation evidence
```

---

# 3. ACTIVE CONTEXT — WHAT WE ARE DOING

## 3.1 Current Epic

```text
[CURRENT_EPIC]
```

Narrative:

```text
[EXPLAIN_THE_HIGH_LEVEL_GOAL]
```

Example structure:

```text
current subsystem
        ↓
current limitation
        ↓
required architecture
        ↓
completion target
```

## 3.2 Current Sprint Goal

```text
[CURRENT_SPRINT_GOAL]
```

The current sprint is complete only when:

```text
[COMPLETION_CRITERION_1]
[COMPLETION_CRITERION_2]
[COMPLETION_CRITERION_3]
```

## 3.3 Current Workstream Architecture

```text
[STAGE_1]
    ↓
[STAGE_2]
    ↓
[STAGE_3]
    ↓
[STAGE_4]
    ↓
[FINAL_STAGE]
```

Ownership:

```text
[BOX_OR_MODULE_A]
owns:
[RESPONSIBILITIES]

[BOX_OR_MODULE_B]
owns:
[RESPONSIBILITIES]
```

Do not merge these responsibilities unless an explicit architecture update authorizes it.

---

# 4. WORK DONE TODAY

*Record only meaningful changes, decisions, evidence, patches, and errors.*

## 4.1 Architecture Decisions

Decision:

```text
[DECISION]
```

Reason:

```text
[WHY]
```

Rejected alternative:

```text
[REJECTED_ALTERNATIVE]
```

Why rejected:

```text
[WHY_REJECTED]
```

---

## 4.2 Features Implemented

### Feature: [FEATURE_NAME]

```text
Feature ID:
[FEATURE_ID]

Patch ZIP:
[ZIP_NAME]

SHA-256:
[SHA256]

Owner box:
[OWNER_BOX]
```

Behavior introduced:

```text
[BEHAVIOR_1]
[BEHAVIOR_2]
[BEHAVIOR_3]
```

Validation evidence:

```text
[VALIDATION_MARKERS]
```

Current status:

```text
DELIVERED / INSTALLED / VALIDATED / FREEZE_EVIDENCE_MERGED / FROZEN
```

Do not upgrade this status without evidence.

---

## 4.3 Repairs Completed

### Error: [ERROR_NAME]

Observed symptom:

```text
[ERROR_MESSAGE_OR_NORMALIZED_FAILURE]
```

Root cause:

```text
[ROOT_CAUSE]
```

Incorrect assumption:

```text
[WRONG_ASSUMPTION]
```

Repair:

```text
[CORRECT_FIX]
```

Regression prevention:

```text
[DO_NOT_REPEAT_RULE]
```

Error Memory lesson:

```text
[LESSON_ID_OR_PENDING_STATUS]
```

---

## 4.4 Research / External Evidence

Research conclusion:

```text
[RESEARCH_CONCLUSION]
```

How it affects architecture:

```text
[ARCHITECTURAL_IMPACT]
```

Do not retain raw research detail unless needed for implementation.

Preserve the derived design rule.

---

# 5. METHODOLOGY & STACK — HOW WE ARE WORKING

## 5.1 Language and Runtime

```text
Language:
[LANGUAGE]

Runtime:
[RUNTIME_VERSION_IF_RELEVANT]

GUI:
[GUI_STACK]

Testing:
[TEST_FRAMEWORK]

Packaging:
[PACKAGING_MODEL]
```

## 5.2 Implementation Style

Preferred:

```text
small governed patches
explicit ownership
deterministic evidence
behavior preservation
public API preservation
whole-symbol moves
focused validators
exact rollback boundary
```

Avoid:

```text
broad speculative rewrites
mixed unrelated cleanup
hidden fallback behavior
forced green validation
source mutation before readiness
duplicate ownership
```

## 5.3 AI Use Policy

AI may:

```text
analyze
generate candidates
review
suggest bounded corrections
explain risks
```

AI does not automatically own:

```text
architecture authority
validation truth
source mutation authority
freeze truth
rollback truth
```

KANDA-owned deterministic gates remain authoritative.

## 5.4 Testing Methodology

Every new feature or repair should define:

```text
what is being proven
fixture or real target
success markers
failure markers
regression scope
box-boundary checks
No-Leak checks
```

Where possible validate the exact final ZIP, not only a build directory.

## 5.5 GUI Methodology

For GUI work:

```text
preserve ownership boundaries
avoid fixed-size layouts when possible
show blocking reasons
show long-running activity
do not make buttons cosmetic
do not expose actions before state readiness
```

## 5.6 Refactor Methodology

For source refactors:

```text
audit
plan
immutable plan handoff
preview
validate preview
preflight
backup
shadow apply when needed
visual diff
guarded apply
post-apply validation
behavior validation
rollback capability
completion
```

---

# 6. CURRENT STATE — EXACT CHECKPOINT

## 6.1 Current Branch / Repository State

```text
Current branch:
[BRANCH_OR_UNKNOWN]

Last known commit:
[COMMIT_HASH_OR_UNKNOWN]

Git status:
[CLEAN / MODIFIED / UNKNOWN]
```

If unknown:

```text
NEXT AI MUST INSPECT BEFORE EDITING
```

## 6.2 Current Active Files

Modified:

```text
[MODIFIED_FILES]
```

New:

```text
[NEW_FILES]
```

Deleted:

```text
[DELETED_FILES]
```

Unknown/unverified:

```text
[UNKNOWN_FILES]
```

## 6.3 Current Runtime State

Current functional checkpoint:

```text
[WHAT_CURRENTLY_WORKS]
```

Current failing or incomplete transition:

```text
[WHAT_DOES_NOT_WORK]
```

Current latest successful validation:

```text
[VALIDATION_RESULT]
```

Current known source hashes or plan hashes:

```text
[SOURCE_HASHES]
[PLAN_HASHES]
```

## 6.4 Current Artifact Inventory

Latest patch:

```text
[PATCH_ZIP]
```

Latest validation result:

```text
[VALIDATION_STATUS]
```

Latest freeze evidence:

```text
[FREEZE_EVIDENCE_STATUS]
```

Latest Error Memory status:

```text
[ERROR_MEMORY_STATUS]
```

---

# 7. BLOCKERS / UNRESOLVED EDGE CASES

## Blocker 1 — [NAME]

Symptom:

```text
[SYMPTOM]
```

What is known:

```text
[KNOWN_FACTS]
```

What is not known:

```text
[UNKNOWN_FACTS]
```

Do not assume:

```text
[UNSAFE_ASSUMPTION]
```

Required investigation:

```text
[NEXT_DIAGNOSTIC_STEP]
```

---

## Blocker 2 — [NAME]

Symptom:

```text
[SYMPTOM]
```

Risk:

```text
[RISK]
```

Required decision:

```text
[DECISION_NEEDED]
```

---

## Technical Debt

```text
[TECH_DEBT_1]
[TECH_DEBT_2]
```

Mark whether each item is:

```text
blocking
non-blocking
deferred
```

---

# 8. IMMEDIATE NEXT ACTIONS

*Actions must be sequential and concrete.*

## ACTION 1 — Rebuild Exact Context

Read:

```text
[FILES_TO_READ]
```

Inspect:

```text
latest freeze context
git status
current branch
relevant Error Memory
current source imports
current test state
```

Do not edit yet.

## ACTION 2 — Reproduce Current Problem

Run:

```text
[REPRODUCTION_COMMAND_OR_WORKFLOW]
```

Capture:

```text
exact error
state transition
input hashes
relevant logs
```

## ACTION 3 — Produce Ownership Audit

State:

```text
active box
owner paths
allowed files
out-of-scope files
cross-box touches
public contracts
validation plan
```

## ACTION 4 — Implement Next Focused Patch

Patch purpose:

```text
[NEXT_PATCH_PURPOSE]
```

Allowed changes:

```text
[ALLOWED_CHANGES]
```

Forbidden scope:

```text
[FORBIDDEN_SCOPE]
```

## ACTION 5 — Validate

Required markers:

```text
[MARKER_1]
[MARKER_2]
[MARKER_3]
BOX_SHIELD: PASS
NO_LEAK_LOGIC: PASS
STATUS: IN_SYNC
ZIP CONTRACT: PASS
```

## ACTION 6 — Deliver Governed Artifact

Provide:

```text
patch ZIP
SHA-256
install code
validation code
freeze code
rollback code when relevant
Error Memory code when error repair occurred
```

## ACTION 7 — Stop or Continue Rule

Stop after:

```text
[STOP_POINT]
```

Continue automatically only when:

```text
[CONTINUATION_CONDITION]
```

---

# 9. PLANNED FOLLOW-UP TRAIN

*Describe future work but do not execute future patches prematurely.*

```text
PATCH 1
[NAME]
Purpose:
[PURPOSE]

PATCH 2
[NAME]
Purpose:
[PURPOSE]

PATCH 3
[NAME]
Purpose:
[PURPOSE]

PATCH 4
[NAME]
Purpose:
[PURPOSE]
```

Execution remains serial:

```text
Patch 1:
install
→ validate
→ freeze

Patch 2:
install
→ validate
→ freeze
```

Do not stack installations before validation.

---

# 10. KNOWN ERROR MEMORY LESSONS RELEVANT TO CURRENT WORK

## Lesson: [LESSON_ID]

Trigger:

```text
[WHEN_TO_RECALL_THIS_LESSON]
```

Do not repeat:

```text
[DO_NOT_REPEAT_RULE]
```

Correct pattern:

```text
[CORRECT_PATTERN]
```

---

## Lesson: [LESSON_ID]

Trigger:

```text
[TRIGGER]
```

Rule:

```text
[RULE]
```

---

# 11. DO-NOT-REGRESS RULES

Preserve these exact lessons:

```text
[NON_REGRESSION_RULE_1]

[NON_REGRESSION_RULE_2]

[NON_REGRESSION_RULE_3]

[NON_REGRESSION_RULE_4]
```

General project rules:

```text
do not bypass validation gates

do not force-enable a blocked workflow stage

do not create duplicate architecture ownership

do not direct-write frozen memory

do not direct-write Error Memory Lessons

do not confuse generated artifacts with source truth

do not claim frozen status without canonical evidence

do not silently change public API ownership

do not mutate selected-project source from a planning-only box

do not proceed to the next sequential patch after current validation failure
```

---

# 12. CONTINUATION PROTOCOL

## First Action Upon Resume

The AI must:

```text
1. Read this handoff.
2. Load current startup/freeze context.
3. Inspect latest freeze entries newest-first.
4. Inspect current local source.
5. Inspect git state.
6. Inspect relevant Error Memory.
7. Compare reality against this handoff.
8. Only then implement.
```

## Autonomy Threshold

The AI may autonomously:

```text
inspect
search source
run focused tests
run static validation
produce ownership audit
implement approved narrow patch
repair exact reproducible defects
build governed ZIP
stage pending Error Memory lesson
```

The AI may not autonomously:

```text
bypass gates
change frozen behavior
invent a replacement architecture
direct-write canonical Lessons
direct-write canonical frozen memory
force source mutation through failed readiness
hide failed validation
```

## Stoppage Conditions

Stop and report exact evidence when:

```text
current source materially conflicts with handoff

latest freeze memory contradicts planned changes

owner box cannot be determined

cross-box mutation would be required without contract

source mutation cannot be rolled back safely

validation cannot prove the required behavior

a later patch depends on an earlier failed patch
```

## Context Compression Rule

When context becomes large, keep fully:

```text
CANON
FROZEN
ACTIVE CONTEXT
CURRENT STATE
BLOCKERS
IMMEDIATE NEXT ACTIONS
DO-NOT-REGRESS RULES
CONTINUATION PROTOCOL
```

Compress first:

```text
raw logs
duplicated terminal output
old superseded source excerpts
repeated explanations
completed low-risk implementation detail
```

Never compress away:

```text
ownership boundaries
freeze status distinctions
current blocker
exact next action
rollback requirements
Error Memory rules
public API constraints
```

---

# 13. END-OF-DAY COMPLETION CHECKLIST

Before generating this handoff, verify:

```text
[ ] Current project root recorded

[ ] Current task and epic recorded

[ ] Latest freeze context checked

[ ] Frozen features separated from merely validated features

[ ] Patch ZIP names recorded

[ ] SHA-256 values recorded where available

[ ] Current source/plan hashes recorded where important

[ ] Current branch/git state recorded or explicitly marked unknown

[ ] Exact blockers documented

[ ] Next patch scope documented

[ ] Out-of-scope files documented

[ ] Known Error Memory lessons recorded

[ ] Install / Validate / Freeze status distinguished

[ ] Rollback state recorded when source mutation occurred

[ ] Immediate next action is concrete

[ ] AI continuation rules are explicit
```

---

# 14. DAILY STATUS SUMMARY

Use this compressed state map:

```text
PROJECT:
[PROJECT_NAME]

CURRENT EPIC:
[EPIC]

CURRENT PATCH:
[PATCH]

CURRENT STATE:
[STATE]

LAST SUCCESS:
[LAST_SUCCESS]

CURRENT BLOCKER:
[BLOCKER]

NEXT ACTION:
[NEXT_ACTION]

DO NOT:
[CRITICAL_DO_NOT_RULE]

FREEZE STATUS:
[FROZEN / FREEZE_PENDING / VALIDATED_ONLY / UNKNOWN]

ERROR MEMORY STATUS:
[NONE / PENDING_REVIEW / MEMORIZED / UNKNOWN]
```

---

# END OF SESSION HANDOFF

Primary continuation entrypoint:

```text
[NEXT_TASK_NAME]
```

First action:

```text
[EXACT_FIRST_ACTION]
```

Do not begin by guessing.

Inspect current source, freeze truth, and Error Memory first.

Preserve architecture ownership.

Preserve public contracts.

Validate before freeze.

Keep rollback available after real mutation.

Do not allow the next session to confuse work completed with work merely proposed, packaged, installed, validated, or freeze-prepared.
