Verdict: The design is sound and architecturally coherent. It correctly identifies the need for a lightweight, human-readable routing layer between the human intent and the specialist prompt library. However, it should be modified before creation to enforce strict size constraints, separate concerns (commands vs. routing), and add explicit guardrails against the index becoming a stealth master prompt.

1. Overall verdict:
modify — Keep the core concept, but harden it against scope creep and ambiguity before writing the file.
2. Recommended document name:
0000 PROMPT ROUTER INDEX v1.0.md(Keep the 0000 prefix if it signals "daily load order." "Router" is more precise than "Navigation" for a document whose only job is to decide which prompts to load for a task. If you prefer "Navigation," keep it, but the filename should match the metadata id field.)
3. Suggested section structure:

Header & Size Budget — Metadata, load mode, and a hard limit (e.g., "This index must stay under ~2000 tokens or 150 lines; if it grows larger, it must be split").
Negative Space Declaration — Explicit list of what this file must NOT contain (no embedded rules, no project paths, no full command syntax, no implementation detail).
Daily Load Order — Exact sequence of what is already in context before this file is read.
AI Routing Protocol — Step-by-step behavior: classify intent → resolve prompt set → request missing → verify → proceed or waive.
Prompt Catalog — Compact table of only audited and active prompts.
Unaudited / Pending Audit Pen — Segregated list of prompts with status: unaudited. Explicit rule: unaudited prompts may be suggested but never required.
Task-to-Prompt Quick Route — Minimal intent-to-prompt mapping (the routing table).
Symbolic Overlay Reference Guide — How to point to project data without naming projects.
AI NEED Protocol & Waiver Template — One global template for requests, plus one waiver template for human override when a prompt is missing.
Index Maintenance Rules — How and when this file may be edited (e.g., "Only during prompt audit sessions; never during implementation").
Future Dispatcher Note — Statement that this will inform prompt_index.json later.

4. Missing rules or fields:

Hard token/line budget for the index itself.
scope field (agnostic / overlay / specialist), distinct from status.
status: unaudited — a formal lifecycle state.
replaces / superseded_by — for deprecated prompts.
last_verified — date or version confirming the row is current.
symbolic_id — decoupled from filename, used for all routing logic.
overlay_key — e.g., OVERLAY:GOVERNANCE_FILES, instead of literal filenames.
Fallback rule — what to do when no specialist prompt exists yet (default: CORE + overlay + explicit human override).
Update protocol — who edits the index, when, and in which session type.
Dependency cycle warning — depends_on must not create loops.
"No embedded rules" clause — any rule longer than one sentence belongs in a specialist prompt.

5. Risks:

Index bloat / stealth master prompt: The most likely failure mode is pasting "just a few useful rules" into the index for convenience.
Drift: Prompt files change; the index becomes stale because it was updated outside an audit session.
Routing ambiguity: A task matches two groups; the AI silently picks one instead of asking.
Project leakage: Project names, paths, or package names slip into examples or filenames in the catalog.
Prompt fatigue: The AI requests 5 prompts for every micro-task; the human starts rubber-stamping "yes, load all."
Hallucinated IDs: The AI invents a prompt ID that does not exist and the human assumes it is real.
Circular dependencies: depends_on chains loop back on themselves.
Unaudited canonization: An unaudited prompt is listed in the main catalog and becomes de facto canon.

6. Suggestions to keep it project-agnostic:

Ban all absolute paths, repo URLs, package names, and project names. Use only symbolic placeholders: {{ACTIVE_PROJECT_OVERLAY}}, OVERLAY:ROOT_PATH, OVERLAY:GOVERNANCE_FILES.
Use abstract task intents ("create feature") rather than concrete domain examples ("add user login").
If an example is unavoidable, prefix it with [ILLUSTRATIVE ONLY] and use a fictional project.
Refer to the parent prompt by its symbolic ID (pyarchitect_general_prompt_stack_load_order) rather than describing its contents.

7. Suggestions to keep it small:

One global AI NEED template — remove AI request wording from every catalog entry.
Move human command definitions to a separate COMMAND_VOCABULARY specialist prompt. The index may list a task intent, but not command syntax or parameter definitions.
Single-line descriptions in the catalog. No multi-line "Purpose" paragraphs.
Segregate unaudited prompts to a sparse list (ID + status + one line) rather than full table rows.
No implementation examples inside the index. If a workflow example is needed, keep it under 3 lines.
Self-audit clause: If the index exceeds its token budget, the next task must be "audit and split the index."

8. Suggested prompt catalog entry template:
   Copied Symbolic ID: [UNIQUE_ID]
Scope: [agnostic | overlay | specialist]
Status: [unaudited | draft | active | frozen | deprecated | retired]
Group: [CORE | DELIVERY | IMPLEMENTATION | ARCHITECTURE | VALIDATION | GOVERNANCE | SESSION | PROMPT_LIBRARY | SPECIAL_RISK]
Purpose: [One line, max 15 words]
Use when: [Trigger condition]
Do not use when: [Exclusion condition]
Depends on: [LIST of Symbolic IDs]
Conflicts with: [LIST of Symbolic IDs]
Replaces: [Symbolic ID, if deprecated]
Overlay Key: [OVERLAY:KEY if project data is required] 9. Suggested task-to-prompt routing table:
Use a compact markdown table. Keep it to the most common intents; rare tasks can be resolved by the AI using the catalog.
   Copied | Task Intent | Min Load (Always) | Required Specialist Prompts | Optional | Overlay Key |
|-------------|-------------------|-----------------------------|----------|-------------|
| START_DAY | load_order, router_index, overlay | — | latest_handoff | OVERLAY:PROJECT |
| CREATE_OR_UPDATE_CODE | load_order, router_index, overlay | delivery_protocol, impl_rules, validation_protocol | box_architecture | OVERLAY:PROJECT |
| LARGE_MODULE_REFACTOR | load_order, router_index, overlay | large_refactor_protocol, arch_canon, validation_protocol | — | OVERLAY:PROJECT |
| GOVERNANCE_UPDATE | load_order, router_index, overlay | governance_update_protocol | validation_evidence, latest_handoff | OVERLAY:GOVERNANCE |
| AUDIT_PROMPT | load_order, router_index, overlay | prompt_audit_canon, substitution_map | relevant_source_prompts | — |
| (No match / novel task) | load_order, router_index, overlay | — | — | OVERLAY:PROJECT | Note: For "No match," the AI must ask the human to classify or explicitly waive the missing specialist prompt.
10. Final recommendation:
Create a minimal viable index first: include the header with a strict size budget, the AI NEED protocol, the 5–7 most common task routes, and a sparse catalog containing only prompts that are already audited and active. Move all human command syntax, detailed examples, and unaudited prompt descriptions into separate files. Do not allow edits to this index during implementation sessions; treat it as a config file that changes only during prompt audit sessions. This prevents the index from becoming a master prompt and keeps the human-AI contract explicit.
 agentic with Kimi-K2.6 via  fireworks-ai   Copied       Pasted Content Clipboard source  answer   Edit  Copy    Specialist Review: Prompt Audit Canon Design
You have built a rigorous architecture. The audit canon is the correct next step after the Navigation Index. It correctly treats the prompt library as a codebase that needs version control, traceability, and separation of concerns. The design is fundamentally sound, but it is in danger of becoming its own master prompt if all 22 proposed sections and overlapping taxonomies are included.
Below are the answers to your twenty questions, followed by the requested 13-point output.

Answers to the 20 Questions

Name: Keep it. 0000 0.3 PYARCHITECT PROMPT AUDIT CANON v1.0.md is consistent with your core load-order numbering and clearly signals its authority.
Too broad? It is necessarily deep, but not too broad if you guard its perimeter: it must contain no software engineering rules (e.g., how to write Python). It is a pure audit protocol. However, 22 sections is excessive; consolidate to ~15 to keep it usable.
Sections to remove: Remove "Changelog" (metadata), "Relationship to future dispatcher" (architectural commentary), and "Freeze and deprecation rules" if they duplicate the parent load-order prompt. Merge "Human decision gate" into "Conflict review protocol." Merge "Audit input requirements" into "Required AI behavior."
Decision categories: You need only seven actions: KEEP, UPDATE, SPLIT, EXTRACT_INTEGRATION_CANDIDATE, DEPRECATE, RETIRE, BLOCKED. Eliminate MERGE (it creates bloat) and eliminate the KEEP_AS_* variants (those are classifications, not decisions).
Status values: unaudited, in_review, active, deprecated, retired, blocked_by_conflict. Treat needs_update as a transitory finding before a decision is applied. Treat pending_integration as the status of the IC file, not the audited prompt.
Decision vs. status separate? Yes. Decision is the verb the auditor performs. Status is the noun the prompt becomes in the library. They must be separate fields in the audit report.
Evidence for "audited": (a) Scope verified (agnostic/overlay/specialist), (b) Project-leakage scan clean, (c) Single-responsorship confirmed, (d) Related prompt overlap inspected, (e) No unresolved conflicts, (f) Dissonant logic extracted or justified, (g) Human approval for all canon-level changes.
Evidence for deprecation: Proven supersession by a newer audited prompt (SAME_IDEA_OLDER_VERSION or SUBSUMED), all unique rules migrated, replacement ID declared, human confirms replacement is canon.
Partial overlap: Never merge. Identify the owner prompt for the shared logic. Extract the overlap into an IC targeting the owner. Update the non-owner to reference the owner via depends_on. If the overlap is universal, consolidate into the project-agnostic parent.
Useful paragraph in wrong prompt: Immediately create an IC file. Never insert it into the target during the audit. If the target is unknown, use TARGET_UNKNOWN. If the target is unaudited, the IC is blocked until the target is audited.
Integration candidates: One file per candidate. The audit report serves as the ledger. A single ledger file becomes a second, un-audited document that needs its own audit.
Filename pattern: Good, but verbose. Use IC###__TARGET_<ID>__SOURCE_<ID>.md and IC###__TARGET_UNKNOWN__SOURCE_<ID>.md. It sorts by IC number, keeps components explicit, and avoids long path prefixes.
Force inspection: The AI must generate an INSPECTION_CHECKLIST before finalizing overlap. It must request the content of each related prompt explicitly. No file, no final overlap decision.
Block final decisions? Absolutely. If related content is unavailable, the RECOMMENDED_DECISION must be BLOCKED, the DECISION_GATE must be PROVISIONAL, and STATUS_AFTER must be in_review or blocked_by_conflict. Never active.
Navigation index update: The AI must never edit the index file directly. It must produce an INDEX_UPDATE_CANDIDATE block in the audit report (or a separate file). The human applies it in a distinct session.
Token count: Later. Token budgets belong in a separate Prompt Engineering Standards canon. The audit canon can flag anomalies but must not define the budget.
Maximum prompt size: Belongs in the separate standards canon, not here.
Audit report fields: See the required list in the 13-point output below.
Missing from design: (a) Audit session boundary rule (audit-only sessions), (b) Prohibition on editing the source prompt during audit, (c) IC orphan aging rule, (d) Batch audit prohibition (one prompt at a time), (e) Meta-audit rule (who audits the canon), (f) Dependency cycle detection, (g) Unowned prompt flag.
Changes before v1: Consolidate sections, separate decision/status/classification, ban MERGE, enforce read-only audit (no source edits), start with the minimal decision/status set.


Requested Output
   Copied 1. Overall verdict:
   modify

2. Recommended file name:
   0000 0.3 PYARCHITECT PROMPT AUDIT CANON v1.0.md

3. Best structure:
   1. Metadata & Scope
   2. What This Prompt Does NOT Do (negative space declaration)
   3. Audit Session Rules (one-at-a-time, no cross-editing, audit-only context)
   4. Required AI Behavior (classify, inspect, compare, extract, decide)
   5. Scope & Responsibility Classification (with leakage check)
   6. Related Prompt Inspection Rule (mandatory checklist before final overlap calls)
   7. Overlap, Upgrade & Conflict Analysis (single comparative phase)
   8. Dissonant Logic Extraction (integration candidate creation)
   9. Audit Decision Taxonomy (actions the AI may recommend)
   10. Audit Status Lifecycle (states a prompt can occupy)
   11. Audit Report Template (required fields)
   12. Navigation Index Effect Rule (produce candidate block, never edit index directly)
   13. Human Decision Gate (escalation triggers)
   14. Version & Deprecation Protocol (bump rules, notice format)
   15. Relationship to Other Canons (brief reference only)

4. Required audit decisions:
   - KEEP
   - UPDATE
   - SPLIT
   - EXTRACT_INTEGRATION_CANDIDATE
   - DEPRECATE (with replacement ID)
   - RETIRE
   - BLOCKED (pending human decision or missing evidence)

5. Required audit statuses:
   - unaudited
   - in_review
   - active
   - deprecated
   - retired
   - blocked_by_conflict

6. Required audit report fields:
   - AUDIT_ID
   - PROMPT_FILENAME
   - CANONICAL_ID
   - DECLARED_VERSION
   - SCOPE (agnostic / overlay / specialist)
   - TYPE (rule / protocol / index / overlay / template / specialist)
   - SINGLE_RESPONSIBILITY_PASS (YES / NO)
   - PROJECT_LEAKAGE_FOUND (YES / NO + list)
   - RELATED_PROMPT_INSPECTION_STATUS (prompt_id + reviewed YES/NO per item)
   - OVERLAP_ANALYSIS (existing_prompt_id + relationship + owning_prompt)
   - CONFLICTS_FOUND (YES / NO + details)
   - DISSONANT_LOGIC_EXTRACTED (list of IC filenames)
   - RECOMMENDED_DECISION
   - DECISION_GATE (CLEAR / HUMAN_REQUIRED / BLOCKED)
   - STATUS_AFTER
   - NAVIGATION_INDEX_EFFECT (NONE / ADD / UPDATE / DEPRECATE / REMOVE)
   - HUMAN_DECISION_REQUIRED (YES / NO + topic)
   - AUDIT_DATE

7. Required related-prompt inspection rule:
   Before any overlap, duplicate, or conflict classification is finalized, the AI must generate an INSPECTION_CHECKLIST of candidate related prompts derived from the Navigation Index, filename similarity, and purpose overlap. The AI must request the content of each unchecked prompt. The audit report field RELATED_PROMPT_CONTENT_REVIEWED must be YES for each candidate before OVERLAP_ANALYSIS or CONFLICTS_FOUND are marked final. If the human waives inspection, the DECISION_GATE must be set to BLOCKED and the STATUS_AFTER must be in_review or blocked_by_conflict, never active.

8. Integration candidate recommendation:
   hybrid: one discrete Markdown file per candidate (atomic, trackable), with the audit report serving as the ledger. Do not maintain a single separate ledger file.

9. Recommended integration candidate filename pattern:
   IC###__TARGET_<TARGET_ID>__SOURCE_<SOURCE_ID>.md
   If target is unknown:
   IC###__TARGET_UNKNOWN__SOURCE_<SOURCE_ID>.md
   Example: IC001__TARGET_box_architecture__SOURCE_large_module_refactor.md

10. Navigation index update recommendation:
    The AI must never edit the Navigation Index file during the audit session. It must produce an INDEX_UPDATE_CANDIDATE block in the audit report (or as a separate INDEX_UPDATE__<<AUDIT_ID>.md file). This block contains the exact rows or entries to add, modify, or deprecate. The human applies the block to the index in a distinct session. Deprecated prompts must be moved to a deprecated section with a SUPERSEDED_BY link. Unaudited prompts must never be added to active routes.

11. Risks not covered:
    - Audit session cross-contamination: The AI starts editing the prompt while still auditing it.
    - Meta-canon rot: The Audit Canon itself is never audited and slowly accretes scope.
    - IC orphanage: Integration candidates are created but never processed, forming a shadow library.
    - Batch audit synthesis: The AI audits multiple prompts at once instead of one-by-one.
    - Soft deprecation: A prompt is marked deprecated but no replacement is actually wired into the index.
    - Version drift: The prompt file changes during the audit session.
    - Over-audit paralysis: The bureaucratic overhead exceeds the value for small prompts.
    - Audit canon misuse: The AI invokes the audit canon during an implementation session to re-litigate frozen prompts.

12. Specific corrections:
    - Separate decision (action), status (state), and classification (type/scope). Do not use KEEP_AS_SPECIALIST_PROMPT as a decision.
    - Eliminate MERGE as a decision. It creates master prompts. Use DEPRECATE with a migration path or EXTRACT_INTEGRATION_CANDIDATE.
    - Rename audited_candidate to active once the audit is complete.
    - Move token size limits and budget rules to a separate Prompt Engineering Standards canon.
    - Remove HANDOFF as a prompt type; it is an artifact type.
    - Merge the proposed Step 6 (Duplicate check) and Step 7 (Conflict check) into a single Comparative Analysis phase.
    - Add a hard rule: The AI must not modify the source prompt file during the audit session. It produces only reports and IC files.
    - Add an IC orphan rule: If an IC is not processed within N audit sessions, it must be flagged as stale.
    - Add a batch audit prohibition: Only one prompt is audited per audit session.

13. Final recommendation:
    Treat this as a read-only protocol, not an editor. Consolidate the 22 proposed sections into the 15-section outline above. Enforce the minimal decision set (KEEP, UPDATE, SPLIT, EXTRACT_IC, DEPRECATE, RETIRE, BLOCKED) and the minimal status set (unaudited, in_review, active, deprecated, retired, blocked_by_conflict). The AI must never edit the source prompt or the Navigation Index during the audit; it produces only the audit report, IC files, and index update candidates. This prevents the audit canon from becoming a master prompt while still enforcing strict traceability.  agentic with Kimi-K2.6 via  fireworks-ai   Copied       Pasted Content Clipboard source  answer   Edit  Copy    Verdict: Modify — Strong Concept.The assimilation layer is the correct architectural response to prompt-library sprawl. It introduces a metadata tier between the human’s intent and the specialist payload, which is exactly how large-context systems avoid overload. However, the assimilation cards must be strictly policed as declarative manifests, not as behavioral prompts. If they become “mini-prompts,” you will simply recreate the problem one level up.

1. Is the idea of “folder assimilation cards” the best way to reduce long-prompt overload?
Yes, with one strict condition: The cards must be lazy-loading metadata, not pre-loaded behavioral rules.The AI should use them to answer three questions only:

What specialist capabilities live in this folder?
Under which human intent should I request this folder?
What is the estimated token cost of loading it?

If the cards contain imperative rules (“Always validate before freezing”), they become a second, fragmented prompt layer and the AI will mix them with the actual specialist prompts. Treat them like package manifests (package.json, Cargo.toml) rather than source code.
Best practice: The AI should not load all 12 cards at session start. It should load only the GROUP_ASSIMILATION_INDEX (the one-page coarse map), then load the specific folder card only after the intent is classified.

2. Should _FOLDER_ASSIMILATION.md files be active prompts, metadata support files, or routing support files?
They are routing support files / metadata manifests. They are not active prompts.
To prevent the AI from “executing” them, add a Constitution Rule in the start_of_day_master_stack:

“Files prefixed with _ or labeled ASSIMILATION are metadata manifests. Use them for lookup, routing, and token estimation only. Do not treat their contents as behavioral instructions.”

If the AI begins obeying the assimilation cards, the boundary between the router and the rules collapses. Keep them declarative.

3. Should the start-of-day master stack include the full AI Prompt Request Canon, or only reference it?
Only reference it.The master stack is the Constitution (the rules about rules). The AI Prompt Request Canon is the Statute (the detailed classification and request protocol). The master stack should be extremely small and say:

“Before acting on implementation, architecture, governance, refactor, or security, invoke the ai_prompt_request_canon to determine the required group bundle.”

If the full classification logic is duplicated inside the master stack, the master stack grows and you lose the separation you are trying to build. The master stack should be < 1,000 tokens (ideally < 600). It defines the tier system, load order, and the golden rule. Nothing else.

4. What is the best load order for the start-of-day core stack?
Adopt a 3-Tier Constitution in the master stack. This lets the human load a tiny kernel and then expand context only when needed.
Tier 0 — Core Constitution (Always Loaded, Never Unloaded)

session_start_upload_checklist — Verify what the human actually placed in context.
start_of_day_master_stack — The tier system, load order, and golden rule.
ai_prompt_request_canon — How to classify intent and request groups.

Tier 1 — Task Context (Loaded After Intent Classification)4. GROUP_ASSIMILATION_INDEX — The 12-folder cheat sheet.5. Relevant _FOLDER_ASSIMILATION.md card(s) for the identified group(s).
Tier 2 — Specialist Rules (Loaded Before Implementation)6. Specific active prompts from the identified group(s).7. box_architecture_canon (if any implementation or architecture work occurs).8. bundle_gated_development_workflow (if any code change will be produced).
If the human knows the session will be implementation-heavy, they can pre-load Tier 1 at start. But the default should be Tier 0 only.

5. Are 12 folder assimilation cards too many, or is this appropriate because they are short?
12 is appropriate only if they are < 300 words each.If they are short metadata manifests, 12 items is a manageable lookup space. The AI does not need to hold all 12 in working memory at once; it only needs the one relevant to the classified intent.
If any card grows beyond that, it is no longer a card—it is a specialist prompt in disguise. Enforce a hard cap.

6. Should there be a maximum size target for each assimilation card?
Yes. Strictly ≤ 300 words or ≤ 400 tokens.Use a rigid template to prevent prose bloat:
   Copied ---
folder: 10_python_api_data_async_config
triggers: ["database", "databank", "API", "async", "config"]
requires: ["04_box_architecture", "05_patch_delivery"]
estimated_tokens: 2500
---
- **Purpose**: Database design, API contracts, async patterns, config management.
- **Load when**: Data persistence, external interfaces, or I/O boundaries are involved.
- **Never load when**: Pure internal logic or UI-only changes with no data layer.
- **Safety note**: All database prompts require Box Architecture to define ownership.
- **Contains**: `python_database_design_optimisation`, `python_validation_serialisation_type_safety`, `python_security_threat_prevention`. No paragraphs. No imperative rules. No “how to” instructions. Just facts.

7. Should the group assimilation index be human-readable only, or also JSON?
Markdown is the canonical source; JSON is a derivative artifact.The GROUP_ASSIMILATION_INDEX.md should be a single markdown table that both humans and the AI read. If you need a group_assimilation_index.json for future tooling or a Tab Prompt Library, generate it from the Markdown. Do not maintain both manually.
Why: The AI parses Markdown tables well. The Markdown can contain human-intent language and comments. The JSON is for machines. If you dual-maintain, they will drift.

8. Should AI ask for missing prompt groups before every task, or only before implementation/refactor/governance changes?
Define a “Fast Path” in the AI Prompt Request Canon.
The AI should ask for specialist groups only when the task touches:

Code implementation or refactoring
Architecture or box ownership
Governance, freeze, or handoff
Security, validation, or audit
Prompt authoring or canon changes

The AI should not ask for groups when the task is:

Casual Q&A
Explanation of existing code
Brainstorming or draft writing
Reading or summarizing provided files
Navigation or metadata queries

Heuristic for the canon:  

“If the task changes state (code, canon, governance, or frozen status), request the group bundle. If the task only reads or discusses, proceed with Tier 0.”

This prevents over-asking for trivial turns.

9. How can we avoid over-asking the human for prompts when the needed behavior is already clear from the loaded Navigation Index?
Use Task Archetype Bundles and Human Shortcuts.
A. Task Archetypes (Pre-bundled group combinations)Embed 5–7 common task patterns in the ai_prompt_request_canon. Examples:



Human Intent Archetype
Default Group Bundle



“New feature / module”
04_box + 05_patch + 08_core


“Database / API / Config”
10_data + 04_box + 05_patch + 09_security


“Large refactor”
06_refactor + 04_box + 05_patch


“Freeze / Handoff”
03_governance + 05_patch


“Prompt audit”
07_audit + 02_routing


The AI should say:  

“This is a Database Architecture archetype. The standard bundle is Groups 10, 4, 5, and 9. Shall I load this bundle?”

B. Human ShortcutsAdd a command vocabulary to the canon so the human can bypass the request:

STANDARD_BUNDLE — Accept the archetype default.
QUICK_PATCH — Load only 05_patch_delivery + 08_core.
FULL_STACK — Load all implementation-relevant groups.
NO_PROMPTS — Proceed with Tier 0 only (human assumes risk).

C. One-Shot RequestThe AI must ask for all needed groups in a single message, not sequentially.

10. What minimal files should be loaded at the beginning of a session to make the AI reliable without overwhelming it?
Three files. That is the minimum viable core.

session_start_upload_checklist
start_of_day_master_stack (the Constitution)
ai_prompt_request_canon (the behavior protocol)

After the human states intent, the AI loads Tier 1 and Tier 2. If the human wants to pre-warm the session for a known task (e.g., “We are building a database today”), they can load Tier 1 at start. But the default should be 3 files.

Additional Risks Not Covered

Assimilation Card CreepThe cards will grow from 200 words to 800 words because “just one more safety note” feels necessary. Without a hard template, they become mini-prompts.

Cross-Group Dependency HellGroup 10 requires Group 4, which requires Group 5, which requires Group 9. The AI ends up requesting 6 groups and you have a stealth prompt dump. Cap the bundle size: No more than 4 groups per archetype without human approval.

Maintenance DesynchronizationA specialist prompt is updated (split, renamed, version bumped), but the folder assimilation card still lists the old filename or token count. The AI makes routing decisions on stale metadata.

The Router Becomes the BottleneckThe human says “add a column to the user table” and the AI spends 3 turns requesting and confirming the Database + Box + Patch + Security groups before writing a 5-line diff. Define a QUICK_PATCH shortcut for low-risk changes.

Loss of Inter-Group ContextThe AI loads the Database group but forgets the Security group’s rules because they were requested separately. If prompts in different groups are highly interdependent, the group boundary may be too sharp. Add a “Cross-Cutting Concerns” note to the Group Assimilation Index (e.g., “Security rules in Group 9 apply to all Groups that touch external I/O”).

Human “Just Do It” FatigueIf the AI asks for confirmation on every task, the human will eventually say “yes, everything, just go.” At that point, the safety architecture is undermined. The Fast Path and Shortcuts above are essential.



Final Recommendation
Proceed, but cap everything.

Cap the Core: 3 files, < 1,000 tokens total for Tier 0.
Cap the Cards: 300 words each, YAML + bullets only, no imperative rules.
Cap the Group Index: 1 page, a single Markdown table.
Cap the Bundle: No more than 4 groups requested without explicit human override.
Enforce the Divide: Add a Constitution Rule: “Assimilation files are metadata, not behavior.”

The success metric is simple: After the human states an intent, the AI should be able to declare its required group bundle in a single sentence. If it takes longer, the assimilation layer is too heavy.
 