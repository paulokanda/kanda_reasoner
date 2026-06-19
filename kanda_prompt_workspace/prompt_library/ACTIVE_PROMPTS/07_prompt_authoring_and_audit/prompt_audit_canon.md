---
audit_id: P003
canonical_id: pyarchitect_prompt_audit_canon
name: PyArchitect Prompt Audit Canon
version: 1.0
status: audited_candidate
project_agnostic: true
type: protocol
group: prompt_library
load_mode: specialist_only
session_mode: audit_session_only
description: Read-only protocol for auditing prompt files, detecting overlap, extracting dissonant logic, and producing audit reports, integration candidates, and index update candidates.
depends_on:
  - pyarchitect_general_prompt_stack_load_order
  - prompt_navigation_index
companion_files:
  - INTEGRATION_CANDIDATE_LEDGER.md
---

# Prompt Audit Canon

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Status: Audited candidate
Use: Load only during prompt-audit sessions.

## 1. Purpose

This canon tells the AI how to audit prompt files safely, one prompt at a time.

It is a read-only audit protocol. It classifies prompts, detects overlap, identifies conflicts, extracts dissonant logic, and produces audit reports, integration candidate files, and index update candidates.

It does not replace specialist prompts, project overlays, delivery protocols, validation protocols, or governance files.

## 2. What This Canon Does NOT Do

This canon must not:

- edit the source prompt during the audit session;
- edit previously audited prompts during the audit session;
- edit the Prompt Navigation Index directly;
- edit project overlays directly;
- edit governance files directly;
- edit runtime source code;
- define software engineering rules such as how to write Python;
- define terminal install or validation behavior;
- define token budgets or maximum prompt sizes;
- act as a dispatcher;
- become a master prompt.

If a rule belongs to another prompt, extract it as an integration candidate instead of inserting it immediately.

## 3. Audit Session Rules

1. Audit one prompt per audit session unless the human explicitly opens a comparison audit.
2. Treat the source prompt as read-only.
3. Produce audit artifacts, not direct edits.
4. Do not canonize anything from memory.
5. Do not finalize overlap, supersession, or conflict decisions without inspecting the actual related prompt content.
6. Do not add unaudited or blocked prompts to the active catalog of the Prompt Navigation Index.
7. If uncertain, choose NEEDS_MORE_EVIDENCE or BLOCKED and ask the human.

The Prompt Audit Canon must not casually audit itself. Changes to this canon require explicit human review and preferably external specialist review.

## 4. Required AI Behavior

During a prompt audit, the AI must:

1. inventory the prompt and assign or confirm a canonical ID;
2. classify scope, type, status, and responsibility;
3. request related prompt files when overlap is possible;
4. compare only against related prompt content actually loaded and read in the current session;
5. identify project leakage, mixed responsibility, overlap, conflicts, and dissonant logic;
6. create integration candidate files for useful content that belongs elsewhere;
7. produce a separate audit report file;
8. produce an index update candidate when the Navigation Index should change;
9. request human decision for canon conflicts, unresolved replacement decisions, or governance-level meaning changes.

## 5. Audit Input Requirements

Before a final audit decision, the AI should have:

- the source prompt file under audit;
- the current Prompt Navigation Index or a summary of audited prompt IDs;
- related previously audited prompt files when overlap is suspected;
- the Prompt Substitution Map, if available;
- prior audit reports, if available;
- the current project overlay only when project-specific separation must be evaluated.

If related prompt content is unavailable, affected overlap decisions stay provisional.

## 6. Core Classifications

### Scope

| Scope | Meaning |
|---|---|
| project_agnostic | Reusable across projects; no project facts. |
| project_overlay | Resolves facts for one project only. |
| specialist | Contains rules for one specific workflow or responsibility. |
| index | Maps tasks to prompts; does not contain full rules. |
| mixed | Mixes responsibilities or scopes and likely needs split. |

### Type

Closed type list:

| Type | Meaning |
|---|---|
| RULE | Small rule set or canon fragment. |
| PROTOCOL | Procedure for a defined task. |
| INDEX | Routing or catalog document. |
| OVERLAY | Project-specific resolver. |
| SPECIALIST | Specialized workflow prompt. |

### Action

| Action | Meaning |
|---|---|
| KEEP | Keep prompt as currently useful. |
| UPDATE | Produce update recommendation or candidate. |
| SPLIT | Separate mixed responsibilities into distinct prompts or overlay. |
| EXTRACT_INTEGRATION_CANDIDATE | Extract useful wrong-place logic to an IC file. |
| DEPRECATE | Mark as replaced but keep for traceability. |
| RETIRE | Remove from normal use because it has no remaining value. |
| BLOCKED | Cannot finalize because evidence or human decision is missing. |
| NEEDS_MORE_EVIDENCE | More files, reports, or human context are required. |

MERGE is not a primary action. If merging seems needed, express it as extraction, update of the owner prompt, and deprecation of the duplicate source.

### Status

| Status | Meaning |
|---|---|
| unaudited | Not reviewed yet. |
| in_review | Currently being audited or partially audited. |
| audited_candidate | Reviewed and suitable, but not necessarily promoted to live canon. |
| active | Accepted into active prompt routing or canon. |
| deprecated | Replaced but kept for traceability. |
| retired | No longer useful for normal trace or routing. |
| blocked_by_conflict | Cannot be promoted until conflict or human gate is resolved. |

## 7. Five-Step Audit Method

### Step 1 - Inventory, Scope, and Responsibility

Extract or infer:

- prompt filename;
- title;
- declared version;
- declared status;
- canonical ID;
- purpose;
- scope;
- type;
- one-sentence responsibility;
- dependencies;
- apparent replacement history.

Check whether the prompt has one clear responsibility. If it mixes load order, delivery, validation, architecture, governance, prompt audit, or project facts, mark mixed responsibility.

Check project leakage in project-agnostic prompts. Flag real project names, absolute paths, package names, local commands, governance filenames, and environment-specific values.

### Step 2 - Related Prompt Inspection

Identify potentially related prompts using:

- Prompt Navigation Index;
- Prompt Substitution Map;
- previous audit reports;
- filename similarity;
- purpose overlap;
- task routing overlap;
- human-provided context.

If related prompt content is needed, ask:

```text
To audit this safely, I need the related previously audited prompt:
- <prompt_id or filename>
Reason: possible overlap with <topic>.
Please upload it or confirm it is already loaded.
```

The AI may continue inventory-only work while waiting.

No actual related prompt file means no final overlap, duplication, supersession, or conflict decision for that relationship.

### Step 3 - Overlap, Upgrade, and Conflict Analysis

After inspecting related prompt content, classify overlap as:

| Relationship | Meaning |
|---|---|
| SAME_IDEA_OLDER_VERSION | Current prompt has older or weaker version. |
| SAME_IDEA_NEWER_VERSION | Current prompt has newer, clearer, safer, or more complete version. |
| SAME_IDEA_EQUIVALENT | Same idea with no meaningful improvement. |
| SAME_IDEA_CONFLICTING | Similar idea changes meaning or contradicts. |
| PARTIAL_OVERLAP | Some shared logic, but each prompt has distinct responsibility. |
| SUBSUMED_BY_EXISTING | Current prompt is fully covered by an audited prompt. |
| SUPERSEDES_EXISTING | Current prompt appears to replace an audited prompt. |

Rules:

- If current content is older or weaker, mark it superseded or recommend deprecation.
- If current content is equivalent, do not duplicate it.
- If current content is newer or better, create an integration candidate targeting the existing owner prompt.
- If content conflicts, create a conflict review entry and require human decision.
- If related content was not reviewed, mark the overlap decision as provisional.

### Step 4 - Dissonant Logic Extraction

Dissonant logic is useful content that belongs to a different prompt responsibility.

Threshold: create an integration candidate only for at least one complete rule, paragraph, workflow step, code block, or command block. Single words or minor clarifications are edits, not integration candidates.

Do not delete useful dissonant logic. Do not keep it silently in the wrong prompt. Do not insert it into the target prompt during the same audit.

Create a separate Markdown integration candidate file.

Required filename pattern:

```text
TO_BE_INSERTED_IN_PROMPT_<TARGET_ID>__FROM_<SOURCE_ID>__IC001.md
```

If target is unknown:

```text
TO_BE_CLASSIFIED_FROM_<SOURCE_ID>__IC001.md
```

Integration candidate files must include YAML frontmatter and must record whether the ledger was updated.

### Step 5 - Decision and Index Update Candidate

Produce:

1. audit report file;
2. integration candidate files, if any;
3. index update candidate, if needed;
4. human decision request, if needed.

Do not edit the Navigation Index directly unless the human opens a separate index-update session.

## 8. Conflict Protocol

A conflict exists when two prompt rules cannot both be true.

Conflict output must include:

```text
Conflict ID:
Prompt A:
Prompt B:
Conflict type:
Issue:
Possible canon options:
AI recommendation:
Human decision required: YES
```

The AI may recommend, but the human decides canon when the conflict affects prompt rules, governance, architecture, validation authority, freeze authority, or broad workflow.

Unresolved conflicts block active promotion.

## 9. Related Prompt Inspection Rule

Core rule:

```text
Index tells us where to look. Actual prompt file proves what is inside.
```

Before classifying content as duplicate, superseded, conflicting, or already covered, the AI must have access to the actual content of the related previously audited prompt.

If a related prompt is unavailable, the audit report must mark:

```text
related_prompt_content_reviewed: NO
overlap_decision_confidence: provisional
final_decision_blocked_for_relationship: YES
```

A missing related prompt may block only the affected comparison. However, if the affected comparison could change whether the prompt becomes active, the prompt must not be marked active.

## 10. Integration Candidate Rule

Each integration candidate gets one Markdown file.

Each integration candidate file must include:

```text
Integration Candidate ID:
Source prompt:
Target prompt:
Extracted snippet:
Why this is dissonant in the source prompt:
Why it may belong in the target prompt:
Does the target prompt need inspection: YES / NO
Related prompt content reviewed: YES / NO
Risk if inserted:
Risk if ignored:
Recommended action:
Human decision required: YES / NO
Status: pending_integration
Ledger updated: YES / NO
```

Also update or create:

```text
INTEGRATION_CANDIDATE_LEDGER.md
```

Ledger columns:

```text
IC_ID | source_prompt | target_prompt | filename | status | human_decision_required | date_created | notes
```

Integration candidates never become canon automatically.

Before any prompt is promoted from audited_candidate to active, all integration candidates targeting it should be resolved, rejected, or explicitly deferred by the human.

## 11. Prompt Navigation Index Update Rule

The audit canon does not edit the Prompt Navigation Index directly.

It produces an INDEX_UPDATE_CANDIDATE block in the audit report.

Allowed effects:

| Effect | Meaning |
|---|---|
| NONE | No index change. |
| ADD | Add active catalog entry. |
| UPDATE | Update an existing row or route. |
| DEPRECATE | Move prompt to deprecated/historical section. |
| REMOVE | Remove active route. |
| REDIRECT | Preserve old route as redirect to replacement. |
| BLOCK | Do not activate because conflict or evidence gap remains. |

Rules:

- Audited active prompt: suggest ADD or UPDATE.
- Deprecated prompt: suggest DEPRECATE or REDIRECT.
- Unaudited prompt: pending audit only, not active.
- Unresolved conflict: BLOCK.
- Integration candidate: never active route.
- Split parent: parent becomes deprecated or redirect; child prompts remain unaudited until each is audited separately.
- Load mode change: include exact route update candidate.

## 12. Deprecation and Retirement Rules

Deprecate before retiring.

A prompt can be deprecated only when:

- replacement or superseding prompt is identified;
- unique useful content was migrated, extracted, or explicitly rejected;
- replacement ID is recorded;
- human decision is obtained if canon meaning changes.

A deprecated prompt is kept for audit trace.

A prompt can be retired only when it has no remaining traceability, replacement, or useful historical role.

## 13. Version and Metadata Rules

Internal metadata is the version authority.

If filename version and metadata version disagree, record the mismatch in the audit report.

Any update that changes canon meaning requires:

- version bump;
- changelog entry or version note;
- index update candidate if routing changes;
- human approval if canon meaning changes.

## 14. Audit Report Template

Each audit should produce a separate file:

```text
AUDIT_REPORT__<AUDIT_ID>__<CANONICAL_ID>.md
```

Required fields:

```text
AUDIT_ID:
PROMPT_FILENAME:
CANONICAL_ID:
DECLARED_VERSION:
AUDIT_CANON_VERSION:
AUDIT_DATE:
SCOPE:
TYPE:
GROUP_FROM_INDEX_IF_ANY:
ONE_SENTENCE_RESPONSIBILITY:
SINGLE_RESPONSIBILITY_PASS:
PROJECT_LEAKAGE_FOUND:
PROJECT_LEAKAGE_ITEMS:
RELATED_PROMPT_INSPECTION_STATUS:
RELATED_PROMPTS_INSPECTED:
OVERLAP_ANALYSIS:
OVERLAP_DECISION_CONFIDENCE:
CONFLICTS_FOUND:
CONFLICT_IDS:
DISSONANT_LOGIC_FOUND:
INTEGRATION_CANDIDATES_CREATED:
RECOMMENDED_CLASSIFICATION:
RECOMMENDED_ACTION:
STATUS_AFTER:
DECISION_GATE:
HUMAN_DECISION_REQUIRED:
NAVIGATION_INDEX_EFFECT:
INDEX_UPDATE_CANDIDATE:
FINAL_AUDIT_RECOMMENDATION:
```

Decision gate values:

```text
CLEAR
HUMAN_REQUIRED
BLOCKED
PROVISIONAL
```

## 15. Human Decision Gate

Human decision is required for:

- prompt conflict resolution;
- canon meaning changes;
- deprecating a prompt with unique useful content;
- accepting unresolved warnings or provisional decisions;
- promoting a prompt to active when related prompt comparisons are incomplete;
- changing this Prompt Audit Canon.

If no human decision is available, use BLOCKED, HUMAN_REQUIRED, or NEEDS_MORE_EVIDENCE.

## 16. Relationship to Other Canons

This canon references, but does not duplicate:

- general load-order prompt;
- project overlay;
- Prompt Navigation Index;
- delivery protocol;
- validation protocol;
- governance update protocol;
- prompt engineering standards, if created later.

If this prompt starts explaining how to implement code, deliver ZIPs, validate runtime behavior, or design application architecture, that content belongs elsewhere.

## 17. Version History

v1.0 - First read-only Prompt Audit Canon. Defines prompt audit sessions, related prompt inspection, overlap and upgrade handling, dissonant logic extraction, integration candidate files, ledger usage, index update candidates, and audit report template.

<!-- T9T013_KANDA_AWARENESS_START -->

## T9T013 Cross-Prompt Awareness Rules

When auditing or updating prompt assets, cross-prompt awareness must be precise and bounded.

Do not update a prompt merely because it is topically similar. Update another prompt only when at least one of these is true:

1. it explicitly references the changed prompt by prompt ID, filename, or declared dependency;
2. it declares the changed prompt as a required companion;
3. it owns a routing/index responsibility that must be updated for the changed prompt to be discoverable;
4. the user explicitly asks for a cross-prompt propagation pass.

Forbidden behavior:

```text
- Do not update every prompt containing the word "prompt".
- Do not update unrelated folder cards for visibility.
- Do not change governance/source/runtime/GUI files during text-only prompt-library work.
- Do not create a duplicate prompt when an existing active prompt already owns the behavior.
- Do not use unrelated project roots in new instructions.
```

If cross-prompt awareness is needed but not proven, produce a follow-up audit candidate instead of editing the related prompt immediately.

<!-- T9T013_KANDA_AWARENESS_END -->

