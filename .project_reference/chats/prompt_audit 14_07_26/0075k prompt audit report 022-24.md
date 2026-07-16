PROMPT AUDIT REPORT 022

AUDIT_ID:
A022-20260714-REVIEW

PROMPT:
prompt_substitution_map.md

CANONICAL ID:
prompt_substitution_map

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md

SOURCE SHA-256:
836a241446a727c752ef31eaec19d5fa4b99a78d9faced5257622f400dfb5018

METADATA SHA-256:
d401031a5e3e17e71b3ebbb9a7aa89e485c0011c483502bb79f49ac435766475

SOURCE SIZE:
3,023 bytes

SOURCE LENGTH:
83 lines

VERSION:
1.1

METADATA STATUS:
active

LOAD TYPE:
on_request

PROMPT CODE:
missing

DUPLICATE ACTIVE SOURCE:
not found

STARTUP MEMBERSHIP:
not always-startup

ENCODING:
pass

FOCUSED VALIDATOR:
missing

OVERALL VERDICT

Keep, reframe, update, and consolidate.

The prompt has a valid capability:

Resolve historical, renamed, deprecated, merged, split, or deleted prompt identities to their current canonical status.

Its current body is unsafe because it acts as a manually maintained filename replacement note rather than a reliable identity and lifecycle map.

UNIQUE CAPABILITY

Yes.

A historical substitution map is needed to answer:

* What replaced this old prompt?
* Is the old name only an alias?
* Was the behavior split between several owners?
* Was the prompt deleted without replacement?
* Is the supposed replacement itself deprecated?
* Should routing fail because the replacement cannot be proven?

This is distinct from current task routing.

Prompt Navigation Index should route current intents.

Prompt Substitution Map should resolve historical identities.

KEY FINDINGS

F022-001 — Replacement targets include prompts recommended for retirement

The map still points historical prompts to:

* reasoner_startup_canon;
* daily_reasoner_startup_loader.

Previous audits recommend retirement of both.

The substitution map therefore preserves obsolete architecture.

Required correction:

Each record must show the current final lifecycle outcome, not merely the next historical version.

F022-002 — One destination is not a valid current canonical prompt

The map contains a historical end-of-chat governance filename as a replacement target.

No current active canonical prompt was found under that exact destination.

Required correction:

Every destination must resolve to:

* canonical prompt ID;
* canonical path;
* current lifecycle status;
* prompt code when available.

When no single destination exists, use `split_replacement` or `no_direct_replacement`.

F022-003 — The map records version succession rather than current resolution

Several entries only say that one historical version replaced another.

That does not answer which current owner should be used now.

Required correction:

Separate:

* historical immediate successor;
* current canonical destination;
* current lifecycle status.

F022-004 — Obsolete patch-delivery rules are embedded

The source says:

* normal prompt or source updates do not need an installer;
* no backup-script folder is required;
* the user extracts a Project-relative ZIP directly into the Project.

These rules conflict with current governed delivery.

Required correction:

Remove all patch, installation, ZIP, and delivery behavior.

F022-005 — Obsolete paths remain active

The prompt contains:

* `_bundle_temp`;
* `_project_reference\ACTIVE_PROJECT_ GOVERNANCE`;
* `_project_reference\PROMPTS\`.

These are not current canonical owners.

Required correction:

Remove all path and installation instructions.

F022-006 — The local Box Logic section is out of scope

The prompt includes a partial implementation-oriented Box checklist.

It omits current:

* Tool-versus-Project separation;
* Project Support;
* transient garbage;
* NO_LEAK;
* MCard;
* Shield;
* Brick Wall.

A historical lookup prompt should remain read-only.

Required correction:

Remove the detailed Box block and route actual migrations to current governance owners.

F022-007 — Lifecycle types are missing

The source uses only “substitutes.”

It cannot distinguish:

* alias;
* rename;
* merge;
* split;
* deprecation;
* deletion;
* compatibility alias;
* historical lineage;
* no replacement.

Required correction:

Add explicit lifecycle classification for each record.

F022-008 — Stable identity fields are missing

Current records are primarily filename-based.

Missing:

* legacy prompt ID;
* current prompt ID;
* old and current prompt code;
* canonical path;
* category;
* status;
* migration evidence.

Filename-only identity is fragile.

F022-009 — No ambiguity behavior exists

The prompt does not define what happens when:

* one legacy prompt maps to several owners;
* a target is deprecated;
* a substitution chain loops;
* metadata and source disagree;
* a target does not exist.

Required correction:

Fail closed and return one of:

* active replacement;
* split replacement;
* historical alias only;
* deleted without replacement;
* unresolved conflict;
* invalid target.

F022-010 — Rename history is duplicated across artifacts

Related data also exists in:

* INTUITIVE_RENAME_TABLE.json;
* rename reports;
* metadata;
* navigation JSON;
* route-coverage data.

Required correction:

Choose one machine-readable identity-history authority.

Prompt 022 should provide the human-readable lookup behavior.

F022-011 — Scope is unclear

The source describes a Project Reasoner substitution map.

Metadata describes broader KANDA prompt concepts.

Required correction:

Define it as a global KANDA Prompt Library historical identity map.

Project-specific aliases belong in Project overlays.

F022-012 — Routing aliases are too broad

Aliases such as:

* router;
* index;
* navigator;
* substitution

collide with current routing owners.

Keep only narrow historical-identity triggers.

F022-013 — Required companion is stale

The prompt requires `general_prompt_stack_load_order`.

A historical alias lookup should not require a global legacy stack.

Required correction:

No companion for simple lookup.

For actual identity migration, use:

* prompt_canon_reconciliation_protocol;
* prompt_identity_code_registry_canon;
* prompt_audit_canon;
* prompt registration owner when routing changes.

F022-014 — No focused validator exists

Required validation should verify:

* target exists;
* target status is valid;
* no loop;
* no unresolved chain;
* no deleted prompt presented as active;
* split replacements are explicit;
* aliases are narrow;
* no delivery rules are embedded;
* no obsolete paths remain.

RECOMMENDED FINAL RESPONSIBILITY

Map a historical prompt name, ID, filename, or code to its current lifecycle state and canonical destination without reproducing destination behavior or authorizing source changes.

RECOMMENDED RECORD MODEL

LEGACY IDENTITY:
Old filename, ID, or code

LIFECYCLE STATE:
active_alias
deprecated_alias
historical_alias
merged
split_replacement
deleted
no_direct_replacement
unresolved_conflict

CURRENT DESTINATION:
Canonical prompt ID or list of owners

CURRENT STATUS:
active
deprecated
deleted

MAY LOAD LEGACY PROMPT:
yes/no

MIGRATION EVIDENCE:
Audit, reconciliation record, or current registry

RECOMMENDED ROUTING

Load when:

* an old prompt name appears;
* a legacy ID must be resolved;
* references are being migrated;
* a user asks what replaced a prompt;
* an audit discovers a possible rename.

Do not load for:

* normal current task routing;
* implementation;
* patch delivery;
* startup;
* freeze;
* current prompt already known.

FINAL DISPOSITION

Classification:
Historical prompt alias, deprecation, and substitution lookup

Action:
KEEP, REFRAME, UPDATE, AND CONSOLIDATE

Delete:
no

Deprecate:
no

Current audit status:
blocked_by_conflict

Expected final status:
active

Final load type:
on_request

Prompt code:
assign only after complete Class 02 registry inspection

Focused verification before correction:
required

Primary unresolved dependency:
Final disposition of every listed replacement target

CLOSURE RECORD

Prompt 022 was fully audited and formally closed.

No source, metadata, routing, validator, generated artifact, or freeze state was modified.


PROMPT AUDIT REPORT 023

AUDIT_ID:
A023-20260714-REVIEW

PROMPT:
routing_signal_scorer_v3_lab_phase_entry_router_canon.md

CANONICAL ID:
routing_signal_scorer_v3_lab_phase_entry_router_canon

DISPLAY NAME:
RG-LAB-000 ML LAB Phase Entry Router Canon

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_lab_phase_entry_router_canon.md

SOURCE SHA-256:
50ec316d347d6850cd22078531d38dc74fdc307a46769d3ed4178c9acd1a28de

METADATA SHA-256:
e972dddac35738d13e85ad32e08efcbe8def09fedd1177cf1ce55256b2f749e7

SOURCE SIZE:
12,460 bytes

SOURCE LENGTH:
348 lines

VERSION:
1.0

STATUS:
active

LOAD TYPE:
on_request

PROMPT CODE:
missing

DUPLICATE ACTIVE SOURCE:
not found

ENCODING:
pass

FOCUSED PROMPT VALIDATOR:
missing

OVERALL VERDICT

Deprecate and remove from active routing after reference migration.

The prompt describes a historical phase-entry gate that has already been completed and surpassed.

Its active body claims:

* LAB is not started;
* RG-LAB-000 is the next action;
* LAB-0 is the first permitted milestone;
* later LAB milestones remain blocked.

Current source demonstrates:

* LAB-0 through LAB-13 exist;
* the LAB sequence is formally closed;
* later MLRT work was completed;
* MLRT expansion is now closed and paused;
* no runtime ML routing authority was granted.

The prompt therefore routes current work backward.

UNIQUE CAPABILITY

Current active capability:
no

Historical capability:
yes

The prompt remains useful only for explaining:

* what RG-LAB-000 was;
* why LAB entry preceded ML work;
* why LAB-0 was documentation-only;
* how the historical safety sequence was structured.

It should not remain a current route owner.

KEY FINDINGS

F023-001 — Current phase claim is false

The prompt says:

```text
LAB phase: NOT STARTED
```

Current source contains the complete LAB-0 through LAB-13 sequence.

Required correction:

Remove the prompt from active routing.

F023-002 — The advertised next milestone is complete

The prompt says LAB-0 is the first allowed milestone.

LAB-13 already closes the sequence.

Current requests such as “continue after P12” could therefore route backward.

F023-003 — The later MLRT phase is also closed

Current source records:

* later MLRT work;
* numerous controlled offline suites;
* extensive validation-only cases;
* final closure and pause policy.

The prompt is not one step behind; it is an entire major phase family behind.

F023-004 — The prompt conflicts with current Project strategy

Current direction prioritizes:

* consolidation;
* quality;
* deduplication;
* demonstrated defects;
* no new intelligence expansion without a proven gap.

Prompt 023 routes toward construction of a new LAB roadmap.

Required correction:

Current related work should route to:

* quality audit;
* coverage review;
* consolidation;
* defect repair;
* current reuse-policy assessment.

F023-005 — Active trigger phrases are stale

Unsafe current triggers include:

* continue after P12;
* start ML lab;
* start router lab;
* implement LAB-0;
* continue ML after lab.

These are historical transition phrases and should not initiate current implementation.

F023-006 — Historical roadmap is embedded as current canon

The prompt contains a fourteen-stage LAB ladder.

A roadmap should not remain present-tense routing authority after completion.

Historical progress belongs in:

* LAB README;
* closure review;
* freeze history;
* handoff history;
* source history.

F023-007 — Metadata and source authority disagree

Metadata says the prompt must not decide:

* required prompts;
* final route.

The body defines:

* a required context package;
* the current route;
* the next milestone;
* May-proceed behavior.

This is an internal authority contradiction.

F023-008 — Required context is overbroad

The prompt requests a large historical stack of:

* folders;
* prompts;
* indexes;
* freeze evidence;
* source ZIP;
* validation evidence.

This conflicts with smallest-safe context selection.

F023-009 — The “future” LAB box already exists

The prompt describes the LAB box as a preferred future location.

That box exists and contains the completed sequence.

F023-010 — LAB-0 restrictions are improperly globalized

The prohibition on Python and other implementation artifacts was valid for LAB-0.

Later governed milestones legitimately created:

* deterministic runner skeleton;
* self-validation gate;
* candidate harness.

The active historical prompt can incorrectly imply that these remain globally prohibited.

F023-011 — Corpus-growth targets are historical

The prompt prescribes staged corpus sizes.

Later actual source and MLRT work supersede those planning numbers.

Current corpus governance belongs to current LAB/MLRT owners.

F023-012 — “May proceed now” authorizes a completed historical action

The prompt allows a governed RG-LAB-000 patch.

That milestone already exists and has been surpassed.

F023-013 — Freeze workflow is incomplete

The prompt mentions:

* local validation;
* freeze;
* startup refresh;
* freeze-memory status.

It does not completely represent current:

* freeze intake;
* Project Support;
* Preview;
* Confirm and Write;
* feature-specific evidence.

A historical router should not own freeze procedure.

F023-014 — Project phase history is stored in a global active route folder

A highly specific historical phase prompt remains in the active global routing library.

It should move to historical provenance rather than active task routing.

F023-015 — No freshness validator exists

No focused validator checks whether:

* LAB remains unstarted;
* LAB-0 is still next;
* later milestones exist;
* MLRT has superseded the route;
* current strategy has paused expansion.

Current LAB self-validation does not validate this prompt.

F023-016 — Metadata status is still active

Definitive superseding evidence exists, but metadata remains active.

This demonstrates missing lifecycle transition when a phase closes.

CURRENT SOURCE-STATE COMPARISON

Prompt:
LAB not started.

Current source:
LAB closed through LAB-13.

Prompt:
LAB-0 is next.

Current source:
LAB-0 through LAB-13 are historical.

Prompt:
Later ML work follows LAB.

Current source:
Later MLRT work occurred and is now closed and paused.

Prompt:
Continue roadmap construction.

Current Project direction:
Consolidate and repair; no unnecessary intelligence expansion.

RECOMMENDED DEPRECATION NOTICE

This prompt is a historical RG-LAB-000 phase-entry record.

The LAB entry and LAB-0 through LAB-13 sequence have already been completed.

Later MLRT expansion has also completed its governed offline sequence and is now closed and paused.

Do not route current work to RG-LAB-000 or LAB-0.

Current work must inspect current LAB/MLRT closure and reuse-policy evidence and must demonstrate a present capability gap before proposing new expansion.

RECOMMENDED ROUTING AFTER DEPRECATION

Historical questions:

* What was RG-LAB-000?
* Why did LAB-0 come first?
* Explain the post-P12 LAB sequence.

Route to historical explanation.

Current quality work:

* audit current MLRT duplication;
* repair failing LAB tests;
* verify no runtime-authority leak;
* consolidate LAB documentation.

Route to current source and quality owners.

New ML expansion:

Require:

* a verified present failure;
* a demonstrated missing capability;
* existing-capability review;
* proof existing LAB/MLRT assets are insufficient;
* separate governed approval.

FINAL DISPOSITION

Classification:
Historical RG-LAB-000 phase-entry record

Action:
DEPRECATE AND REMOVE FROM ACTIVE ROUTING AFTER REFERENCE MIGRATION

Delete immediately:
no

Intermediate status:
deprecated

Final active-library status:
deleted

Historical provenance:
preserve

Prompt code:
do not assign unless historical-ID policy requires it

Current active capability:
none

Historical capability:
yes

Focused verification before correction:
required

Primary unresolved dependency:
Migration of active routes, metadata companions, and historical freeze lineage

CLOSURE RECORD

Prompt 023 was fully audited and formally closed.

No source, metadata, routing, validator, LAB source, freeze state, or generated artifact was modified.



PROMPT AUDIT REPORT 024

AUDIT_ID:
A024-20260714-REVIEW

PROMPT:
routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md

CANONICAL ID:
routing_signal_scorer_v3_pilot_copilot_phase0_router_canon

DISPLAY NAME:
RG-PILOT-000 Pilot/Copilot Phase 0 Router Canon

CANONICAL PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md

SOURCE SHA-256:
02a7218ad45f9da288e138dd485debafe2c2a1b4ff182cda8ba4f9ba0cdc4813

METADATA SHA-256:
9d039dd2c8e136876e29a7c29035da8c6d827cd1c694b1f73aa58a1cdb765601

SOURCE SIZE:
14,234 bytes

SOURCE LENGTH:
500 lines

VERSION:
1.0

STATUS:
active

LOAD TYPE:
on_request

PROMPT CODE:
missing

DUPLICATE ACTIVE SOURCE:
not found

ENCODING:
pass

FOCUSED PROMPT VALIDATOR:
missing

OVERALL VERDICT

Deprecate and remove from active routing after reference migration.

The prompt describes the historical entry into the P0 Pilot/Copilot sequence.

Its active body claims:

* Pilot is not started;
* Copilot is not started;
* the P-series is 0 of 13;
* P0 is the next safe milestone;
* P1–P12 remain blocked;
* RG-LAB-000 follows P12.

Current source demonstrates:

* P0 through P12 exist;
* P12 closes the non-runtime Pilot foundation sequence;
* the actual P6–P12 milestone names differ from the prompt’s roadmap;
* LAB was later completed through LAB-13;
* MLRT later completed a large controlled offline validation sequence;
* MLRT expansion is closed and paused.

The prompt therefore contains both stale phase state and contract drift.

UNIQUE CAPABILITY

Current active capability:
no

Historical capability:
yes

Useful historical principles include:

* Pilot output was non-authoritative;
* human review was mandatory;
* prompt-loading authority was prohibited;
* persistence was disabled by default;
* batch and training-data use were prohibited;
* runtime shadow was excluded;
* reproduction preceded disagreement.

These safety principles should remain in current contracts and historical source, not in an active P0 router.

KEY FINDINGS

F024-001 — Current phase statement is false

The prompt says:

```text
Pilot: NOT STARTED
Copilot: NOT STARTED
P-series: 0 done, 13 to go
```

Current source contains P0 through P12.

F024-002 — P0 is no longer the next milestone

The prompt directs “start Pilot” or “after M35” toward P0.

P0–P12 are already complete.

F024-003 — The planned P6–P12 ladder does not match actual implementation

Prompt roadmap:

* P6 Pilot Implementation Gate Design
* P7 Non-Runtime Pilot Projection Implementation
* P8 Router Reproduction Comparison
* P9 Passive Simulation Evidence
* P10 Readiness Gate
* P11 Copilot Boundary Charter
* P12 Copilot Scope Gate

Actual source:

* P6 Pilot Review Evidence Design
* P7 Pilot Implementation Gate Design
* P8 Non-Runtime Pilot Candidate
* P9 Candidate Contract Conformance
* P10 Candidate Readiness Gate
* P11 Candidate Review Evidence Packet
* P12 Pilot Phase Closure / Copilot Boundary Entry Gate

This is substantive contract drift.

F024-004 — Post-P12 route points to another obsolete phase router

The prompt routes to RG-LAB-000.

Prompt 023 is also historical and recommended for active-route removal.

This creates a chained stale route.

F024-005 — Current Project strategy conflicts with the roadmap

Current direction favors:

* quality;
* consolidation;
* demonstrated gaps;
* no unnecessary ML expansion.

Prompt 024 encourages restarting a multi-stage Pilot/Copilot roadmap.

F024-006 — Required context package is excessive

The prompt requests a large stack of:

* prompts;
* folders;
* indexes;
* delivery context;
* Python context;
* freeze context;
* source ZIP;
* validation evidence.

This violates smallest-safe context.

F024-007 — Metadata and body authority conflict

Metadata says the prompt cannot decide:

* required prompts;
* final route;
* May proceed now.

The body defines all three.

F024-008 — It is an implementation specification disguised as a router

The source defines:

* exact dataclass fields;
* exact constants;
* exact values;
* forbidden names;
* fixed Boolean semantics;
* test families;
* AST restrictions;
* provenance fields.

Those belong to the actual P-series source and focused validators.

F024-009 — Exact forbidden identifier list is too rigid

The prompt bans specific names such as:

* candidate_prompt_groups;
* simulated_required_prompt_groups;
* selected_prompt;
* prompt_loader.

Semantic authority and side effects should be validated instead of permanently banning words.

F024-010 — Exact constants belong to implementation owners

The prompt requires constants such as:

```text
ROUTING_EFFECT = "none"
PROMPT_LOADING_EFFECT = "none"
RUNTIME_EFFECT = "none"
ACTIVATION_EFFECT = "none"
STORAGE_STATUS = "in_memory_only"
```

These may be valid for specific modules but should not be globally owned by a phase router.

F024-011 — Test requirements are historical and overbroad

The prompt owns detailed test families for:

* output immutability;
* exact statements;
* AST restrictions;
* no file creation;
* no logging;
* earlier milestone regression.

Changed-file validation belongs to current source owners and Brick Wall.

F024-012 — Patch-delivery rules are embedded

The source defines:

* KANDA_FREEZE_HINT.json;
* root placement;
* patch provenance;
* freeze-ready patch contents.

This duplicates Class 05 and freeze owners.

F024-013 — Freeze workflow is incomplete

The source does not fully represent current:

* feature-specific evidence;
* Project Support;
* Preview;
* Confirm and Write;
* freeze intake.

A router should not own freeze procedure.

F024-014 — Fixed phase counter is permanently stale

The source records:

```text
P-series: 0 done, 13 to go
```

Current phase must derive from exact source and current closure evidence.

F024-015 — Active triggers are unsafe

Unsafe triggers include:

* after M35;
* start Pilot;
* start Copilot;
* create P0;
* implement P0;
* Limited Shadow Runtime.

These should not automatically select a completed historical roadmap.

F024-016 — No freshness or contract-alignment validator exists

No validator checks:

* whether P0 remains next;
* whether P0–P12 exist;
* whether the roadmap matches source;
* whether RG-LAB-000 remains current;
* whether Project strategy has paused expansion.

F024-017 — Metadata remains active after phase closure

Lifecycle state was not updated when the P-series completed.

F024-018 — The prompt preserves expansion recursion

Its pattern is:

* create milestone;
* validate;
* freeze;
* create next milestone;
* repeat.

This can create governance growth without a current user-facing deficiency.

CURRENT SOURCE-STATE COMPARISON

Prompt:
P0 is next.

Current source:
P0–P12 exist.

Prompt:
P-series is 0/13.

Current source:
P12 closure exists.

Prompt:
Original P6–P12 roadmap.

Current source:
P6–P12 implementation differs materially.

Prompt:
RG-LAB-000 is future.

Current source:
RG-LAB-000, LAB-0 through LAB-13, and MLRT work exist.

Prompt:
Continue Pilot/Copilot roadmap.

Current Project direction:
Require a present demonstrated gap before new intelligence expansion.

RECOMMENDED DEPRECATION NOTICE

This prompt is a historical RG-PILOT-000 phase-entry record.

P0 through P12 have already been implemented as governed non-runtime foundation milestones, and P12 closed the sequence.

The later LAB and MLRT phases have also completed their current governed sequences, and MLRT expansion is closed and paused.

Do not route current work to P0.

Do not infer Pilot, Copilot, prompt-loading, or runtime authority from this historical phase prompt.

Any new Pilot or Copilot work requires a separately governed current scope based on a demonstrated present capability gap.

RECOMMENDED ROUTING AFTER DEPRECATION

Historical questions:

* What was RG-PILOT-000?
* Why was P0 design-only?
* Explain P0–P12.
* Why was runtime shadow excluded?

Route to historical P-series source.

Current safety questions:

* Is Pilot active?
* Does ML have routing authority?
* Can Copilot load prompts?
* Is runtime shadow enabled?

Route to current public contracts and current Routing Signal Scorer owners.

Current quality tasks:

* audit P-series duplication;
* repair a failing non-runtime candidate test;
* consolidate transition-design documentation;
* verify no authority leak.

Route to current source and quality owners.

New Pilot/Copilot expansion:

Require:

* verified present gap;
* review of existing capabilities;
* boundary and risk analysis;
* separate approval;
* current Brick Wall admission.

FINAL DISPOSITION

Classification:
Historical RG-PILOT-000 / P0 phase-entry record

Action:
DEPRECATE AND REMOVE FROM ACTIVE ROUTING AFTER REFERENCE MIGRATION

Delete immediately:
no

Intermediate status:
deprecated

Final active-library status:
deleted

Historical provenance:
preserve

Prompt code:
do not assign unless historical-ID policy requires it

Current active capability:
none

Historical capability:
yes

Focused verification before correction:
required

Primary unresolved dependency:
Migration of current routes, metadata companions, P-series references, and closure history

CLOSURE RECORD

Prompt 024 was fully audited and formally closed.

No source, metadata, routing, validator, P-series source, freeze state, or generated artifact was modified.

