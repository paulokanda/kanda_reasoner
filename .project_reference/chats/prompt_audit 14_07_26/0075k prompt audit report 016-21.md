PROMPT AUDIT CYCLE 016–021

Project:
kanda_reasoner

Audit mode:
Read-only, one prompt at a time

Prompts audited:

16. start_of_day_master_stack
17. chatgpt_kanda_routing_choice_output_protocol
18. kanda_routing_system_canon
19. project_overlay_selector
20. prompt_navigation_index
21. prompt_router

Source modified:
NO

Metadata modified:
NO

Routing modified:
NO

Validators modified:
NO

Generated startup delivery modified:
NO

Patch created:
NO

Validation claimed:
NO

Freeze performed:
NO

======================================================================
PROMPT AUDIT REPORT 016
=======================

AUDIT_ID:
A016-20260714-REVIEW

PROMPT:
start_of_day_master_stack.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md

CANONICAL SOURCE SHA-256:
8db49e65b52f507a084ffcb755515f00d1468f3a5ef72664ead90746132436e9

CANONICAL METADATA SHA-256:
c16e0de5a35f6c87a70e9c7b8cd99e550d7d17f9e327f68f562bc91d5e2f6220

SOURCE SIZE:
19,505 bytes

SOURCE LENGTH:
409 lines

DECLARED VERSION:
1.0

DECLARED STATUS:
active_candidate

METADATA LOAD TYPE:
tier_0_session_kernel

STARTUP SOURCE-MAP ROLE:
always_startup

GENERATED STARTUP FILE:
05_start_of_day_master_stack.md

GENERATED STARTUP SHA-256:
d04c73e0a131309cff66be0e4ce657283479dc94d8840ab0f37ac3a3801799dd

CANONICAL-TO-GENERATED SYNC:
PASS

SECOND ACTIVE SOURCE:

Path:
prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md

SHA-256:
8dc13422c48ebd1fd48637876957d1859eca926b361bd0f82c4a986b3b841fcb

Length:
300 lines

PROMPT CODE:
MISSING

ENCODING:
PASS

OVERALL VERDICT

The prompt has a necessary and distinct role and should remain active.

Its proper role is:

Carry a compact, always-loaded startup kernel containing only the minimum hard bridges needed before task-specific routing.

The current canonical source is not compact enough. At 409 lines, it has become a partial compiled governance prompt.

RECOMMENDED ACTION:

KEEP, REDUCE, AND CONSOLIDATE

RECOMMENDED FINAL STATUS:

active

RECOMMENDED FINAL LOAD TYPE:

always_startup

MAJOR FINDINGS

F016-001 — Two active sources diverge

The workspace canonical copy contains newer bridges for:

* NO_LEAK_LOGIC_V1;
* governed architecture companion routing;
* durable-document routing;
* boundary-first repair;
* expanded helper-module rules.

The other active copy retains an older Patch/Validate/Freeze Recovery Routine startup hook that the canonical source no longer contains.

The startup ZIP correctly follows the workspace source, but the second independently maintained copy remains a source-authority conflict.

Correction:

Keep one canonical source and remove or generate the other copy.

F016-002 — The “smallest safe stack” is no longer small

The prompt says it is a bootstrap router rather than a master prompt.

It nevertheless contains detailed implementations of:

* Box Logic;
* NO_LEAK;
* architecture-companion routing;
* durable-document routing;
* module-size policy;
* terminal cleanup;
* tier routing;
* route tables;
* missing-context levels;
* response schemas.

This exceeds a thin startup-bridge responsibility.

Correction:

Retain only brief invariants and exact owner references.

Detailed rules must remain in their canonical prompts.

F016-003 — The phase model is stale

The prompt still says:

Current phase:
Phase 1 — Context Routing Kernel

It says not to require all 12 folder cards because Phase 2 has not created them.

The current library already contains the folder-card system and many later routing phases.

Correction:

Remove historical Phase 1 implementation status from active startup behavior.

Phase history belongs in reconciliation or migration records.

F016-004 — Task intake can occur before Project readiness

Tier 0 lists these as optional continuation inputs:

* latest handoff;
* current task description;
* current source/evidence ZIP.

The current startup contract requires the real Project task only after:

PROJECT READY CHECK

ending with:

WAIT_FOR_TASK

Correction:

The startup master stack should defer Project task intake to the session upload checklist and Project handoff owner.

F016-005 — Terminal behavior is reproduced in detail

The source contains exact terminal cleanup behavior rather than only routing to:

* terminal_cleanup_contract;
* pre_output_contract_gates.

This creates a second detailed terminal owner and risks future drift.

Correction:

Keep one compact terminal bridge and remove the operational footer specification.

F016-006 — Durable-document rules repeat known weaknesses

The bridge classifies generated `.txt`, `.md`, and similar files primarily by extension.

Durability should be based on purpose, authority, lifetime and future need.

It also does not include the complete sensitivity and redaction protection identified during Prompt 007.

Correction:

Refer to the durable-document canon instead of reproducing its full logic.

F016-007 — Routing tables are manually maintained

The prompt contains a task-to-group table for:

* implementation;
* refactoring;
* UI;
* storage;
* prompt audit;
* freeze;
* handoff;
* productization.

These mappings overlap:

* prompt_navigation_index;
* prompt_router;
* group assimilation;
* ai_prompt_request_canon.

Correction:

Remove the detailed route table.

The startup stack should state only the escalation sequence.

F016-008 — Metadata is incomplete

Missing or inconsistent identity fields include:

* prompt_code;
* canonical lifecycle status;
* version in metadata;
* canonical path;
* owner-box synchronization;
* current phase;
* duplicate-source status.

Correction:

Modernize metadata during the later governed update.

F016-009 — Validators overprotect copied wording

Current validators reference exact startup markers and bridge wording for:

* module quality;
* terminal cleanup;
* durable documentation;
* governed architecture companion registration.

This can freeze duplicated prose rather than the underlying behavior.

Correction:

Validate semantic invariants and owner references rather than complete copied blocks.

FINAL RECOMMENDATION

Classification:
Always-startup governance bridge

Action:
KEEP, REDUCE, AND CONSOLIDATE

Delete:
NO

Deprecate:
NO

Unique capability:
YES

Future shield required:
YES

Protected invariants:

* startup remains compact;
* Brick Wall remains final coding authority;
* Tool/Project, Box and NO_LEAK are visible from startup;
* detailed specialist logic remains on request;
* no task begins before Project readiness;
* one canonical source exists.

======================================================================
PROMPT AUDIT REPORT 017
=======================

AUDIT_ID:
A017-20260714-REVIEW

PROMPT:
chatgpt_kanda_routing_choice_output_protocol.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/chatgpt_kanda_routing_choice_output_protocol.md

SOURCE SHA-256:
efd4cd46cf6c701b04acc2f35ed371515d0a9e9c426089432b500adba5aa0387

METADATA SHA-256:
500b242270cc417dfbba2e368db287a4be9388b46a25a882105151d169625b99

SOURCE SIZE:
6,307 bytes

SOURCE LENGTH:
138 lines

VERSION:
2.1.0

PROMPT CODE:
KPR-02-001

STATUS:
always_startup

GENERATED STARTUP FILE:
11_chatgpt_kanda_routing_choice_output_protocol.md

GENERATED STARTUP SHA-256:
452abe40261bc89373dfb23f66778577b2b23b8fe3040befa92a292321d86591

DUPLICATE SOURCE:
NOT FOUND

ENCODING:
PASS

OVERALL VERDICT

The prompt has stable identity information, clean encoding and a unique KPR code.

Its current content, however, no longer matches its file name, prompt ID, folder-card description or routing references.

The prompt was transformed from:

ChatGPT KANDA Routing Choice Output Protocol

into:

ChatGPT KANDA Prompt Library Direct Retrieval Protocol

without changing its prompt ID or code.

RECOMMENDED ACTION:

RESTORE IDENTITY, NARROW RESPONSIBILITY, AND MOVE DIRECT-RETRIEVAL RULES TO THEIR CORRECT OWNER

MAJOR FINDINGS

F017-001 — Prompt identity and body disagree

File name and prompt ID:

chatgpt_kanda_routing_choice_output_protocol

Prompt code:

KPR-02-001

Current body purpose:

Retrieve exact prompts from prompt_library.zip.

Current metadata display name:

ChatGPT KANDA Prompt Library Direct Retrieval Protocol

Class 02 folder card:

Teaches browser ChatGPT to emit safe advisory KANDA_ROUTING_CHOICE blocks.

These are different responsibilities.

Correction:

Preserve KPR-02-001 for the original routing-choice output protocol unless the complete registry audit proves a different approved identity migration.

F017-002 — Required KANDA_ROUTING_CHOICE schema is absent

The navigation index expects this prompt to produce:

```text
KANDA_ROUTING_CHOICE_START
{ valid advisory JSON }
KANDA_ROUTING_CHOICE_END
```

The current prompt instead says not to output a machine block unless explicitly requested and does not define the complete validated schema.

Correction:

Restore the advisory output contract, including:

* event type;
* prompt code when known;
* prompt ID;
* folder path;
* prompt path;
* advisory-only status;
* no mutation authority;
* no freeze authority;
* no ML activation.

F017-003 — Direct retrieval is useful but belongs elsewhere

The current direct-retrieval behavior is valid:

* do not read the whole prompt library;
* open only selected prompt paths;
* do not ask the user to paste a prompt already in prompt_library.zip;
* treat browser ChatGPT as non-authoritative.

This behavior belongs primarily in:

* session_start_upload_checklist;
* prompt-navigation behavior;
* startup generated instructions;
* prompt-router retrieval handling.

It should not replace the output protocol’s identity.

F017-004 — Load mode likely needs reconsideration

The original output protocol is only needed when:

* the user asks for route-choice output;
* manual Prompt Router Reasoner capture is requested;
* machine-readable advisory output is needed.

That suggests `on_request`, not necessarily `always_startup`.

The direct retrieval rule is startup-relevant, but it should be owned by another startup bridge.

Final load mode should be decided after the complete Class 02 audit.

F017-005 — No focused validator exists

No dedicated validator was found that verifies:

* valid start and end markers;
* valid JSON;
* advisory-only authority;
* exact prompt address fields;
* rejection of invented prompt codes;
* no local mutation claims;
* no ML or freeze authority.

Correction:

Create a focused semantic validator after identity restoration.

F017-006 — Cross-prompt contradiction already exists

Prompt 020 still defines KPR-02-001 as the machine-readable output protocol.

Prompt 017 defines KPR-02-001 as direct retrieval.

The system therefore has two incompatible interpretations of one stable prompt code.

FINAL RECOMMENDATION

Classification:
Advisory routing-choice output protocol

Action:
KEEP KPR-02-001, RESTORE OUTPUT-PROTOCOL SEMANTICS, AND RELOCATE DIRECT-RETRIEVAL RULES

Delete:
NO

Deprecate:
NO

Current status:
blocked_by_conflict

Likely final load type:
on_request, subject to final Class 02 owner decision

Unique capability:
YES

Future shield required:
YES

Protected invariants:

* output remains advisory;
* browser ChatGPT is non-authoritative;
* no invented prompt code;
* canonical prompt paths are validated;
* no mutation, freeze or ML authority;
* one prompt code has one semantic identity.

======================================================================
PROMPT AUDIT REPORT 018
=======================

AUDIT_ID:
A018-20260714-REVIEW

PROMPT:
kanda_routing_system_canon.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md

CANONICAL SOURCE SHA-256:
4e57b18047d32d0cf080d95837bf809d9ab418587463a4e294569c36b69aa528

CANONICAL METADATA SHA-256:
e3d9710db7c5c5b93f54c25049c5544e98a61e79d4225d9bb182f060239745d3

CANONICAL SIZE:
43,980 bytes

CANONICAL LENGTH:
1,627 lines

SECOND ACTIVE SOURCE:

Path:
prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md

SHA-256:
0c15d2e7c1f373ed88aac109edf3433042e75cc0d793b9b9aeb1dbc489ec4503

Length:
1,614 lines

DECLARED UPDATE VERSION:
2026-06-17

METADATA STATUS:
active

LOAD TYPE:
on_request

PROMPT CODE:
MISSING

ENCODING:
PASS

OVERALL VERDICT

The prompt has an important and unique responsibility:

Define the architecture and authority boundaries of the KANDA prompt-routing system.

It should remain active and on request.

Its current form is not acceptable as a canon because it has become a 1,600-line historical compilation that contradicts its own statement that it must not become a giant master prompt.

RECOMMENDED ACTION:

KEEP, RADICALLY CONSOLIDATE, AND RECONCILE DUPLICATE SOURCES

MAJOR FINDINGS

F018-001 — The prompt violates its own non-mega-prompt rule

The source explicitly says:

* it is not an always-loaded startup prompt;
* it must not become a giant master prompt.

It nevertheless embeds:

* startup boot files;
* Fast Path and Routed Work Path;
* prompt registration;
* shielding;
* similarity scoring;
* context package manifests;
* freeze behavior;
* historical roadmap phases;
* pilot results;
* detailed scenario outputs;
* Error Memory bridges;
* implementation planning.

Correction:

Retain only stable routing-system architecture and authority rules.

F018-002 — Two active sources diverge

The root duplicate contains a second-upload handoff gate.

The workspace canonical source does not contain that gate.

The canonical metadata and duplicate metadata also differ in their trigger phrases and description.

Correction:

Reconcile valid changes into one source and remove independent duplicate maintenance.

F018-003 — Startup boot instructions are stale

The source says:

* upload first_prompts_to_ai.zip;
* then paste tell_AI_read_before_all.md;
* inspect startup files 00 through 09;
* wait for WAIT_FOR_TASK.

The current startup requires:

* tell_AI_read_before_all.md to be read first;
* prompt_library.zip as part of stage 1;
* startup files extending beyond 09;
* second_prompt_files;
* PROJECT READY CHECK before WAIT_FOR_TASK.

Correction:

The routing-system canon should refer to the startup owner rather than reproduce the startup sequence.

F018-004 — The canonical source lacks the second-upload gate

The noncanonical copy contains a safer second-upload rule.

The canonical workspace copy does not.

This repeats the canonical-source leakage pattern found in Prompts 013 and 015.

F018-005 — Historical implementation status is mixed into canon

The source includes:

* Phase 1 completion;
* Phase 2 plan;
* pre-Phase 2 scaffold;
* RG-025, RG-026 and RG-027 pilot results;
* decisions not to create validators yet;
* current roadmap recommendations.

These are historical Project-state records, not timeless routing canon.

Correction:

Move them to handoff, roadmap, freeze or reconciliation records.

F018-006 — Prompt Registration rules overlap Class 07 ownership

The prompt defines:

* prompt identity;
* registration;
* context packages;
* registration targets;
* overlap checks;
* call examples.

Prompt creation and registration are already owned by Class 07 canons.

Correction:

The routing-system canon may state that registered prompts require identity and route metadata, but detailed authoring workflow must remain with Class 07.

F018-007 — Box and shield logic are duplicated

The source contains its own versions of:

* Box Architecture;
* KBSC;
* project/tool identity;
* freeze-aware routing;
* shield requirements.

Current owners already exist.

Correction:

Use explicit owner references and retain only routing-specific implications.

F018-008 — Brick Wall and NO_LEAK are not properly integrated

The source predates or incompletely reflects current:

* Brick Wall authorization;
* NO_LEAK classifications;
* changed-file-to-validator mapping;
* Error Memory preflight;
* exact-source baseline;
* MCard lifecycle gates.

Correction:

Add compact authority relationships without copying their full bodies.

F018-009 — Freeze example is too permissive

The prompt says a freeze request may proceed if validation evidence is already provided.

Current freeze behavior additionally requires:

* evidence tied to the current feature;
* correct Project Support placement;
* read-only Preview;
* explicit Confirm and Write;
* current freeze intake;
* startup freeze-context refresh.

Correction:

The routing canon must only select the freeze owner, not authorize the freeze itself.

F018-010 — Project-specific memory placement is outdated

The source includes language suggesting project-specific state stays inside the active Project root.

Current Tool-versus-Project rules place durable Project-support state in the external sibling support root.

F018-011 — Metadata is incomplete

Missing:

* prompt_code;
* formal semantic version;
* canonical path;
* owner-box normalization;
* duplicate-source state;
* current Brick Wall relationship;
* current NO_LEAK relationship.

F018-012 — Validator dependencies are fragmented

Several validators inspect this prompt for route fragments, including:

* Project Tool Boundary bridges;
* MCard routing;
* transient garbage ownership.

This risks freezing duplicated excerpts rather than the routing-system contract.

FINAL RECOMMENDATION

Classification:
On-request routing-system architecture canon

Action:
KEEP, RADICALLY CONSOLIDATE, AND RECONCILE

Delete:
NO

Deprecate:
NO

Unique capability:
YES

Target size:
A concise architecture canon rather than a historical implementation record

Future shield required:
YES

Protected invariants:

* deterministic routing remains authoritative;
* similarity and ML remain advisory unless separately governed;
* prompts are registered rather than globally injected;
* routing requests the smallest complete context;
* startup, authoring, freeze and implementation retain separate owners;
* one canonical source exists.

======================================================================
PROMPT AUDIT REPORT 019
=======================

AUDIT_ID:
A019-20260714-REVIEW

PROMPT:
project_overlay_selector.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/project_overlay_selector.md

SOURCE SHA-256:
b678117dca5b8c511e39b4e8001a6bd00206a5043889919518478fcaf110941e

METADATA SHA-256:
caafe191a78f53f813039eec67b13173a608289ed4c8ccd6c58b2a920610740e

SOURCE SIZE:
5,423 bytes

SOURCE LENGTH:
172 lines

FRONT-MATTER VERSION:
1.0

FRONT-MATTER STATUS:
audited_candidate

BODY STATUS:
Project-specific audited candidate

METADATA STATUS:
active

LOAD TYPE:
on_request

PROMPT CODE:
MISSING

DUPLICATE SOURCE:
NOT FOUND

ENCODING:
PASS

OVERALL VERDICT

A Project Overlay Selector is a useful and distinct capability.

The current prompt is not a selector.

It is a hardcoded, historical KANDA Reasoner overlay containing outdated paths, startup behavior, delivery rules and freeze storage.

RECOMMENDED ACTION:

KEEP THE PROMPT ID, REWRITE AS A TRUE SELECTOR, AND REMOVE THE EMBEDDED LEGACY OVERLAY

MAJOR FINDINGS

F019-001 — Identity and behavior disagree

Prompt ID:

project_overlay_selector

Actual behavior:

A specific KANDA Reasoner Project overlay.

The source directly defines:

* Project name;
* Project root;
* application package;
* prompt-library folder;
* audited prompt destination;
* daily load order;
* delivery behavior.

Correction:

The selector should discover, validate and select an existing overlay rather than become the overlay.

F019-002 — Hardcoded Project paths are obsolete

The prompt hardcodes:

```text
E:\kanda_reasoner
E:\kanda_reasoner\kanda_reasoner_app
E:\kanda_reasoner\kanda_reasoner_app\prompt_library
E:\kanda_reasoner\project_freeze_ledger\KANDA_PROMPTS_AUDITED
```

Problems:

* prompt library canon now lives in the workspace source;
* Project-specific freeze state belongs under external Project Support;
* project_freeze_ledger is not current Project freeze authority;
* a selector must work for Projects other than KANDA.

F019-003 — Legacy startup stack is embedded

The source requires:

* general prompt stack load order;
* universal delivery protocol;
* startup canon;
* daily loader;
* governance ZIP;
* handoff;
* task description;
* source evidence.

This is the obsolete startup family identified in Prompts 004, 005, 014 and 015.

F019-004 — Delivery and freeze authority are unsafe

The source says ZIPs should preserve Project-relative paths and that the AI may freeze a routine implementation step after clean validation.

It omits:

* Brick Wall;
* pre-output contract gates;
* exact ZIP contract;
* user-local validation distinction;
* read-only Preview;
* Confirm and Write;
* Project Support freeze placement.

A selector must not own patch or freeze behavior.

F019-005 — Box Logic is incomplete and duplicated

The local Box checklist omits:

* Tool/Project identities;
* Project Support;
* transient garbage;
* NO_LEAK;
* mutable-state ownership;
* MCard;
* Shield;
* Brick Wall.

Correction:

A selector should route to the architecture owners when overlay selection affects ownership.

F019-006 — Overlay storage and authority are undefined

A real selector needs to determine:

* where overlays are registered;
* which Project root they match;
* whether the overlay is current;
* whether it is source or generated evidence;
* whether more than one overlay matches;
* what happens when no overlay matches.

The current prompt does none of these.

F019-007 — The required companion is outdated

The prompt requires:

general_prompt_stack_load_order

That prompt has not yet been corrected and belongs to the older stack architecture.

The selector should depend on:

* current Project identity;
* current overlay registry or metadata;
* project_tool_boundary_canon;
* project_startup_canon_template when a new overlay must be created;
* prompt reconciliation when multiple overlays conflict.

F019-008 — Routing aliases are too broad

Current aliases include:

* project;
* overlay;
* router;
* selector;
* navigator;
* index.

These overlap heavily with other routing prompts.

Correction:

Use narrow overlay-selection triggers only.

F019-009 — No focused validator exists

Required negative cases should include:

* wrong Project root;
* multiple overlays;
* stale overlay;
* generated overlay treated as source;
* overlay for another Project;
* hardcoded KANDA paths;
* selector writing Project files;
* selector authorizing implementation or freeze.

FINAL RECOMMENDATION

Classification:
On-request Project overlay selector

Action:
KEEP ID, REWRITE AS TRUE SELECTOR, REMOVE EMBEDDED LEGACY OVERLAY

Delete:
NO

Deprecate current body:
YES

Unique capability:
YES

Future shield required:
YES

Protected invariants:

* selector does not become overlay;
* overlay Project identity must match;
* Tool and Project roots remain separate;
* no hardcoded KANDA path;
* no implementation or freeze authority;
* ambiguous overlay selection fails closed.

======================================================================
PROMPT AUDIT REPORT 020
=======================

AUDIT_ID:
A020-20260714-REVIEW

PROMPT:
prompt_navigation_index.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md

SOURCE SHA-256:
ce9292f0a291e514a93f86934cb78fae4969883d1f86d41ebcc9922d15cab548

METADATA SHA-256:
bce36afff0ae2031d69c3523a7aa0dcb2376c802e27ef1b0d9bc3c1b38f666fa

SOURCE SIZE:
77,306 bytes

SOURCE LENGTH:
1,322 lines

VERSION:
2.1

STATUS:
active_candidate

METADATA LOAD TYPE:
tier_0_authoritative_router

STARTUP ROLE:
always_startup

GENERATED STARTUP FILE:
02_prompt_navigation_index.md

GENERATED STARTUP SHA-256:
8eadb29d9a2958e7495219d907b2cde4c81e2c1623346b2bb5decee1554f1a86

DUPLICATE SOURCE:
NOT FOUND

PROMPT CODE:
MISSING

ENCODING:
PASS

OVERALL VERDICT

The prompt has a necessary and central role:

Serve as the authoritative human-readable index for exact prompt selection.

It should remain active and startup-visible.

Its current form is not an index. It is a 77 KB compiled mega-prompt containing large portions of many specialist protocols.

RECOMMENDED ACTION:

KEEP AS AUTHORITATIVE HUMAN INDEX, RADICALLY REDUCE, AND DERIVE IT FROM CURRENT ROUTE METADATA

MAJOR FINDINGS

F020-001 — The index embeds complete specialist protocols

The source includes detailed bodies for:

* prompt insertion;
* prompt identity;
* Brick Wall;
* ChatGPT routing choice;
* Project Tool Boundary;
* MCard;
* patch delivery;
* freeze delivery;
* user correction;
* boundary repair;
* shield behavior;
* Pilot/Copilot;
* LAB;
* semantic readiness;
* Error Memory;
* anti-hallucination;
* architecture companion.

An index should locate owners, not duplicate them.

F020-002 — RG-015 historical blocks are duplicated repeatedly

The source contains:

* first-position override V8;
* T9T013 routing bridge;
* exact-name V3;
* exactness V5;
* delivery repair V6;
* hard override V7.

This repeats the same accumulation identified in `ai_prompt_request_canon`.

Correction:

Keep one current semantic route and remove historical active blocks.

F020-003 — Unrelated medical-residency residue is present

The first-position RG-015 block recommends:

“Domain-specific medical residency curriculum scoring source/rubric”

and refers to expected scoring criteria.

This is unrelated to general prompt-library authoring.

Correction:

Replace it with generic domain-authority language or remove it from the index entirely.

F020-004 — Numbering is internally corrupted

The RG-015 required list repeats item numbers 3 and 4.

Other embedded lists also contain manually accumulated numbering.

This indicates that exact copied route bodies are no longer reliably maintained.

F020-005 — The source claims authority over Prompt Router

The index says:

* it is the primary readable router;
* prompt_router is only a compatibility/helper prompt;
* this index wins on conflict.

This owner decision is sensible.

However, the index then reproduces all route implementation, becoming the same competing mega-router it is intended to replace.

Correction:

Keep the owner decision and remove embedded specialist content.

F020-006 — The phase model is stale

The source still describes:

* Phase 1;
* folder cards not yet created;
* restricted allowed outputs;
* no live app integration.

The current library and application have progressed far beyond that state.

F020-007 — Prompt 017 conflict is visible inside the index

The index correctly describes KPR-02-001 as an advisory `KANDA_ROUTING_CHOICE` output protocol.

Prompt 017’s current body defines it as direct ZIP retrieval.

This proves a current cross-prompt identity conflict.

F020-008 — Patch ZIP contract is duplicated and conflicting

The index contains detailed patch/freeze delivery sequences.

Previous audits found that different prompts disagree about whether the ZIP contains:

* only changed files plus KANDA_FREEZE_HINT.json; or
* installer, validator, freeze script, README and changed files.

An index must not choose or reproduce the operational ZIP contract.

F020-009 — Human-readable and machine-readable route sources can drift

The system contains:

* this Markdown index;
* PROMPT_NAVIGATION_INDEX.md;
* prompt_navigation_index.json;
* route coverage CSV;
* group index;
* metadata;
* folder cards.

The current Markdown prompt appears manually accumulated rather than generated from one canonical route dataset.

Correction:

Establish one machine-readable route authority and derive or validate the human index from it.

F020-010 — Metadata is incomplete

Missing:

* prompt_code;
* synchronized version;
* canonical path;
* current lifecycle status;
* current route-data owner;
* generation policy;
* do-not-regress fields.

F020-011 — Startup context cost is excessive

Loading 1,322 lines at every startup contradicts the smallest-safe-context principle.

A startup index should contain:

* escalation order;
* route lookup rules;
* exact owner addresses;
* conflict behavior.

It should not include full protocols.

F020-012 — Existing validation likely protects textual accumulation

Routing tests and startup synchronization confirm presence and current output, but the source’s semantic duplication has still accumulated.

Future validation must check:

* every active prompt has one route;
* IDs and paths resolve;
* no duplicate authority;
* no historical active route blocks;
* human and machine representations agree.

FINAL RECOMMENDATION

Classification:
Authoritative human-readable exact-prompt navigation index

Action:
KEEP, RADICALLY REDUCE, AND DERIVE FROM CURRENT ROUTE METADATA

Delete:
NO

Deprecate:
NO

Unique capability:
YES

Future shield required:
YES

Protected invariants:

* one authoritative route data source;
* index locates but does not replace prompts;
* no domain-specific leakage;
* no historical active override blocks;
* no duplicate router authority;
* exact prompt IDs and paths resolve;
* startup context remains compact.

======================================================================
PROMPT AUDIT REPORT 021
=======================

AUDIT_ID:
A021-20260714-REVIEW

PROMPT:
prompt_router.md

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md

SOURCE SHA-256:
4e2e723a894b937fee35b44a80dcdf5dba994d602a705c7622597f530a565d2f

METADATA SHA-256:
265049147ee6d931d6a92837e92ba75af28fce7458580bb1b516c328f453db63

SOURCE SIZE:
41,401 bytes

SOURCE LENGTH:
1,370 lines

VERSION:
1.0.4

SOURCE STATUS:
Reusable beginning-of-day prompt router

SOURCE PROMPT ID:
kanda_prompt_router

METADATA PROMPT ID:
prompt_router

METADATA LOAD TYPE:
on_request

PROMPT CODE:
MISSING

LEGACY APPLICATION ROUTER:

Path:
kanda_reasoner_app/prompt_library/active/KANDA_PROMPT_ROUTER.md

SHA-256:
789ba93e633230ddb0b8b44bcc10934621b807e869080a3e43acdb9cf2dbba55

Version:
1.0.0

Prompt ID:
kanda_prompt_router

Legacy metadata SHA-256:
7f50ca6cb06a08cf4841f584d648227e13d54ef1a6247d7a3c7b63a54d17b83c

ENCODING:
PASS

OVERALL VERDICT

This prompt no longer has a safe unique responsibility.

Prompt 020 explicitly establishes `prompt_navigation_index` as the authoritative human-readable router and describes `prompt_router` as a compatibility helper.

The current Prompt 021 is nevertheless another 1,370-line routing mega-prompt with overlapping and sometimes conflicting operational rules.

RECOMMENDED ACTION:

DEPRECATE AND DELETE AFTER ROUTE, APPLICATION AND VALIDATOR MIGRATION

Do not rewrite it into another complete router.

If a lightweight compatibility helper is still needed, it should only redirect to the authoritative index and machine route data.

MAJOR FINDINGS

F021-001 — Prompt identity is inconsistent

Source prompt ID:

kanda_prompt_router

Workspace metadata prompt ID:

prompt_router

Application prompt ID:

kanda_prompt_router

Routes use:

prompt_router

This creates unstable identity across:

* source;
* metadata;
* application Prompt Library;
* groups;
* navigation.

F021-002 — A conceptual duplicate exists in the application Prompt Library

The workspace prompt and application `KANDA_PROMPT_ROUTER.md` share:

* the same legacy identity;
* the same beginning-of-day router purpose;
* much of the same initial content.

They have different:

* versions;
* sizes;
* paths;
* metadata;
* later route coverage.

This is another dual-source ownership conflict.

F021-003 — The prompt competes directly with Prompt 020

Prompt 020 says it is authoritative and wins on conflict.

Prompt 021 contains its own:

* task classification;
* route table;
* prompt selection;
* specialist requirements;
* output expectations;
* missing-context rules.

Keeping both as active full routers guarantees drift.

F021-004 — It is a specialist mega-prompt

The source contains detailed operational content for:

* Project Tool Boundary;
* MCard;
* large-module refactor;
* AST audit;
* patch delivery;
* freeze;
* Error Memory;
* prompt creation;
* Pilot/Copilot;
* LAB;
* productization;
* GUI prototypes;
* EEG project generalization;
* plugins;
* rendering;
* decision tables;
* transform resolvers.

A router should point to these owners, not reproduce their implementation.

F021-005 — Project-specific EEG routes leaked into a reusable router

The heading:

“EEG Project Generalization Routes — Added from CANON.zip and PROMPTS.zip”

demonstrates Project/domain-specific accumulation in a reusable global router.

Correction:

Project-specific routes belong in an overlay or Project profile, not the global router.

F021-006 — Patch and freeze contracts are duplicated

The prompt contains a complete canonical freeze-ready patch delivery sequence.

This duplicates Class 05 and freeze owners and preserves the same conflicting ZIP structure found elsewhere.

F021-007 — Brick Wall and NO_LEAK are not integrated as final authorities

The source contains many hard gates but does not make current Brick Wall and NO_LEAK the central admission model.

It therefore preserves a parallel pre-Brick-Wall implementation route.

F021-008 — Metadata companions are obsolete and overbroad

Metadata requires:

* general_prompt_stack_load_order;
* prompt_substitution_map;
* Error Memory owner;
* bundle workflow;
* large-module protocols;
* Tool Boundary.

This means loading the router can pull a large specialist stack before a route is even selected.

F021-009 — Broad aliases conflict with Prompt 020 and Prompt 019

Aliases such as:

* router;
* index;
* navigator;
* prompt router;

overlap the authoritative navigation index and overlay selector.

F021-010 — Many validators and application components depend on router fragments

Current validators reference `prompt_router.md` for:

* large-module binding;
* MCard routes;
* Workbench ownership;
* Error Memory buttons;
* patch-recovery blueprint;
* planner Web AI behavior;
* transient garbage rules.

These validators make the router a duplicate canonical owner.

Before deletion, every validator must be redirected to the actual specialist owner.

F021-011 — The application Prompt Library still actively registers the legacy ID

Application teaching metadata and PROMPT_GROUPS.json still reference:

kanda_prompt_router

Immediate deletion would break these registrations.

F021-012 — No unique remaining capability was found

The intended capabilities are already owned by:

* prompt_navigation_index;
* machine-readable prompt-navigation JSON;
* group assimilation;
* ai_prompt_request_canon;
* specialist prompts;
* Prompt Router Reasoner manual capture.

A full second router is unnecessary.

FINAL RECOMMENDATION

Classification:
Obsolete compatibility router / duplicated mega-router

Action:
DEPRECATE AND DELETE AFTER MIGRATION

Delete now:
NO

Intermediate status:
deprecated

Final status:
deleted

Unique capability:
NO

Prompt-code recommendation:
Do not consume a new KPR code unless deprecated-ID policy explicitly requires it.

Migration requirements:

1. Migrate all active routes to Prompt 020 or machine route data.
2. Migrate application Prompt Library groups.
3. Migrate teaching metadata.
4. Migrate every validator to the real specialist owner.
5. Preserve the old `kanda_prompt_router` ID only as a temporary alias.
6. Remove broad aliases.
7. Replace the body with a short deprecation redirect if an intermediate release is required.
8. Delete both workspace and application active source copies after validation.

======================================================================
CYCLE CHECKPOINT 016–021
========================

AUDITED PROMPTS:

016:
start_of_day_master_stack

Disposition:
KEEP, REDUCE, CONSOLIDATE

Unique capability:
YES

017:
chatgpt_kanda_routing_choice_output_protocol

Disposition:
KEEP KPR-02-001, RESTORE OUTPUT-PROTOCOL IDENTITY

Unique capability:
YES

018:
kanda_routing_system_canon

Disposition:
KEEP, RADICALLY CONSOLIDATE, RECONCILE DUPLICATES

Unique capability:
YES

019:
project_overlay_selector

Disposition:
KEEP ID, REWRITE AS TRUE SELECTOR

Unique capability:
YES

020:
prompt_navigation_index

Disposition:
KEEP AS AUTHORITATIVE INDEX, RADICALLY REDUCE

Unique capability:
YES

021:
prompt_router

Disposition:
DEPRECATE AND DELETE AFTER MIGRATION

Unique capability:
NO

CROSS-PROMPT CONFLICT MATRIX

Conflict 1:
Prompt 017 versus Prompt 020

Prompt 017 currently defines KPR-02-001 as direct ZIP retrieval.

Prompt 020 defines KPR-02-001 as advisory KANDA_ROUTING_CHOICE output.

Required decision:
Restore one stable semantic identity.

Conflict 2:
Prompt 020 versus Prompt 021

Prompt 020 declares itself authoritative.

Prompt 021 remains a complete competing router.

Required decision:
Keep Prompt 020 as owner and migrate/delete Prompt 021.

Conflict 3:
Prompt 016 canonical source versus duplicate source

Canonical source contains newer architecture bridges.

Duplicate source contains an older patch-recovery hook.

Required decision:
One canonical source only.

Conflict 4:
Prompt 018 canonical source versus duplicate source

The duplicate contains a second-upload gate absent from canonical source.

Required decision:
Reconcile valid behavior without preserving the mega-prompt.

Conflict 5:
Prompt 019 selector identity versus overlay body

The prompt says selector but embeds one historical KANDA overlay.

Required decision:
Rewrite as selector and relocate or retire the old overlay facts.

Conflict 6:
Routing prompts versus specialist owners

Prompts 018, 020 and 021 reproduce:

* patch contracts;
* freeze rules;
* Box rules;
* Tool Boundary;
* MCard;
* Error Memory;
* prompt authoring;
* ML routing;
* specialist implementation rules.

Required decision:
Routing assets point to owners; they do not copy owner protocols.

LIBRARY-WIDE PATTERNS CONFIRMED

1. Duplicate active source trees

Valid corrections are repeatedly applied to the noncanonical tree while startup generation continues to follow the older canonical workspace source.

2. Perfect synchronization can still preserve stale semantics

Generated startup files match their source hashes, but the canonical source may itself be outdated or internally conflicting.

3. Routing assets have become compiled mega-prompts

The router, navigation index and routing-system canon reproduce specialist behavior rather than selecting specialists.

4. Historical repair blocks remain active

Versioned overrides, pilot outcomes and repair generations are retained as current runtime rules.

5. Validators freeze duplicated prose

Multiple validators depend on copied route fragments inside general routers instead of validating the actual specialist owner.

6. Prompt identity drift

Stable filenames, prompt IDs, prompt codes, metadata display names and actual responsibilities no longer consistently describe the same behavior.

7. Startup context is larger than necessary

Always-startup files contain detailed operational contracts better suited to on-request prompts.

DEPENDENCY-ORDER IMPLICATIONS FOR THE CORRECTION PHASE

The current evidence strengthens the recommendation to audit all prompts before editing.

The likely correction order is:

1. Prompt identity and registry canons
2. Prompt audit and reconciliation canons
3. Machine-readable routing authority
4. Prompt Navigation Index
5. ChatGPT routing-choice output protocol
6. Routing-system canon
7. Start-of-Day Master Stack
8. Session upload checklist
9. Project overlay selector
10. Prompt Router deprecation and deletion
11. Specialist-owner validators
12. Startup generation and delivery

QUALITY CHECK

Prompts opened simultaneously:
NO

Primary target overlap:
NO

Prompt 016 closed before Prompt 017:
YES

Prompt 017 closed before Prompt 018:
YES

Prompt 018 closed before Prompt 019:
YES

Prompt 019 closed before Prompt 020:
YES

Prompt 020 closed before Prompt 021:
YES

Exact fingerprints recorded:
YES

Dependencies recorded:
YES

Generated-artifact relationships recorded:
YES

Duplicate-source relationships recorded:
YES

Source modifications:
NO

Unsupported validation claims:
NO

Full Error Memory required:
NO

Context quality remains safe for another cycle:
YES, but a fresh checkpoint is now established.

STOPPING POINT

Last audited prompt:
021 — prompt_router.md

Next prompt:
022 — prompt_substitution_map.md

Prompt 022 has not been opened as a primary audit target.
