O nono prompt está registrado como ativo e on_request, mas o próprio arquivo declara always_on e manda carregá-lo primeiro em toda sessão. Isso conflita com o startup atual, cuja entrada canônica é tell_AI_read_before_all.md, seguida pelo pacote inicial, biblioteca sob demanda e segundo upload do projeto.

PROMPT AUDIT REPORT 009

AUDIT_ID:
A009-20260714-REVIEW

PROMPT_FILENAME:
general_prompt_stack_load_order.md

WORKSPACE PROMPT_ID:
general_prompt_stack_load_order

PROMPT-INTERNAL CANONICAL ID:
pyarchitect_general_prompt_stack_load_order

CANONICAL WORKSPACE PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/general_prompt_stack_load_order.md

CURRENT WORKSPACE SOURCE SHA-256:
7f8a2a93fd44f0c277a4b6784f9c613339d79e5fd8468f8367f87134bc36c0ba

CURRENT WORKSPACE METADATA SHA-256:
71f3e604d703632b4540c76c3e82570f62dee1e5e69831b535854bc8d6b243c5

SOURCE SIZE:
10,198 bytes

SOURCE LENGTH:
258 lines

DECLARED SOURCE VERSION:
1.1

SOURCE STATUS:
audited_candidate

METADATA STATUS:
active

SOURCE LOAD MODE:
always_on

METADATA LOAD TYPE:
on_request

PROMPT CODE:
MISSING

FOCUSED VALIDATOR:
NOT FOUND

LEGACY APPLICATION SOURCE:
kanda_reasoner_app/prompt_library/active/0000 0.1 PYARCHITECT GENERAL PROMPT STACK LOAD ORDER v1.0.md

LEGACY APPLICATION PROMPT ID:
0000_0_1_general_prompt_stack_load_order

LEGACY SOURCE SHA-256:
beedbfe1f79ab7b567c389aebc8fcd580d59432eb260d57f19e3ed0376a38b73

LEGACY AND WORKSPACE CONTENT IDENTICAL:
NO

AUDIT MODE:
Read-only, one-prompt audit

SOURCE MODIFIED:
NO

METADATA MODIFIED:
NO

ROUTING MODIFIED:
NO

PATCH CREATED:
NO

NEXT PROMPT OPENED FOR AUDIT:
NO

OVERALL VERDICT

This prompt should not remain an active canonical prompt.

Almost every substantive responsibility in it now has a stronger current owner:

* actual startup order;
* prompt routing;
* missing-context decisions;
* project overlays;
* handoff triggers;
* Box Logic;
* Tool-versus-Project separation;
* NO_LEAK_LOGIC_V1;
* patch delivery;
* terminal cleanup;
* validation;
* freeze;
* prompt auditing.

After those responsibilities are assigned to their current owners, the prompt has no sufficiently distinct remaining role.

RECOMMENDED ACTION:

DEPRECATE AND DELETE AFTER DEPENDENCY MIGRATION

Do not delete immediately.

Several current routing prompts, metadata records, groups, profiles, stacks, and the Prompt Audit Canon still reference this prompt or its legacy ID.

The safe sequence is:

1. Audit all dependent prompts.
2. Determine which dependencies are still semantically necessary.
3. Replace obsolete dependencies with current canonical owners.
4. Mark this prompt deprecated.
5. Preserve exact legacy IDs as temporary aliases.
6. Remove active routing and broad aliases.
7. Validate that no active prompt depends on it.
8. Delete both independently maintained source copies and their metadata.
9. Preserve only historical reconciliation records.

RECOMMENDED CURRENT STATUS:

blocked_by_conflict

RECOMMENDED INTERMEDIATE STATUS:

deprecated

LIKELY FINAL STATE:

deleted

DECISION GATE:

HUMAN_REQUIRED

UNIQUE CAPABILITY ASSESSMENT

UNIQUE CAPABILITY FOUND:

NO

The apparent capabilities are already owned as follows:

Current KANDA startup order:

* tell_AI_read_before_all.md
* start_of_day_master_stack
* session_start_upload_checklist
* current first_prompt_files and second_prompt_files workflow

Prompt selection and context request:

* ai_prompt_request_canon
* prompt_navigation_index
* prompt_router
* kanda_routing_system_canon

Project-specific overlay selection:

* project_overlay_selector

End-of-work behavior:

* handoff_at_end_of_work

Box and boundary behavior:

* box_architecture_canon
* project_tool_boundary_canon
* NO_LEAK_LOGIC_V1
* kanda_box_shielding_canon
* architecture_review_project_card_machine_canon, when applicable

Governed implementation:

* brick_wall_comprehensive_quality_gate

Patch, validation, and terminal behavior:

* pre_output_contract_gates
* relevant Class 05 owner
* terminal_cleanup_contract
* patch_install_delivery_error_register

Freeze behavior:

* freeze_code_intake_and_form_protocol
* current active freeze context

Prompt audit behavior:

* prompt_audit_canon
* prompt_canon_reconciliation_protocol

A separate general load-order prompt is no longer needed.

SINGLE RESPONSIBILITY ANALYSIS

The prompt currently combines:

1. Startup order
2. Prompt precedence
3. Prompt routing
4. Project overlay loading
5. Governance loading
6. Handoff loading
7. Source-evidence loading
8. End-of-chat warnings
9. Box Logic
10. Prompt audit behavior
11. Installation behavior
12. Terminal cleanup
13. Validation requirements
14. Freeze authorization
15. Human governance decisions
16. Project-agnostic prompt templating

SINGLE RESPONSIBILITY PASS:

FAIL

POSITIVE FINDINGS

P009-P001

TITLE:
Project-agnostic intent

RESULT:
PARTIAL PASS

The prompt correctly says:

* do not hardcode one Project root;
* do not assume one product package;
* do not treat examples as current Project truth;
* use current source and observed evidence;
* request missing evidence before implementation.

These principles remain useful, but they are already covered by current exact-source, Tool-versus-Project, routing, and Brick Wall owners.

P009-P002

TITLE:
Install success is not validation

RESULT:
PASS AS A PRINCIPLE

The prompt correctly distinguishes successful installation from successful validation.

This principle must remain, but its detailed implementation belongs to Class 05 and the terminal owner.

P009-P003

TITLE:
Validation success is not automatic freeze

RESULT:
PARTIAL PASS

The prompt explicitly states that validation success is not automatic freeze.

However, it later contradicts that statement by granting the AI “step-freeze authority.”

P009-P004

TITLE:
Current-source evidence has high precedence

RESULT:
PARTIAL PASS

The prompt places source files, runtime logs, GUI observations, screenshots, and validation output near the top of its precedence list.

The concept is useful, but the precedence ordering requires correction because the user instruction currently sits above implementation truth.

P009-P005

TITLE:
Prompt-audit isolation

RESULT:
PASS AS A PRINCIPLE

The prompt says only the currently selected prompt should be audited.

This matches the current one-prompt-at-a-time audit workflow.

However, the rule belongs to `prompt_audit_canon`, not to this load-order prompt.

P009-P006

TITLE:
Encoding and structural integrity

RESULT:
PASS

The workspace source has:

* valid UTF-8;
* no UTF-8 BOM;
* LF-only line endings;
* no prohibited control bytes;
* balanced Markdown fences.

Brick Wall Q27 passes for the source itself.

CRITICAL AND HIGH-SEVERITY FINDINGS

FINDING A009-F001

TITLE:
Direct violation of protected human freeze authority

SEVERITY:
CRITICAL

The prompt declares:

“The AI is authorized to freeze the current routine implementation step…”

It then permits the AI to state:

“Validation reviewed. All required gates passed. This step is frozen.”

PROBLEM:

This conflicts directly with the protected current freeze behavior.

The AI may:

* review evidence;
* state whether validation appears complete;
* state whether work appears eligible for freeze preparation;
* prepare read-only Preview;
* prepare freeze-intake material.

The AI may not independently write or declare canonical freeze memory.

Current protected behavior requires:

* genuine user-local validation;
* read-only Preview;
* explicit human Confirm and Write;
* correct Project Support freeze paths;
* startup freeze-context refresh after confirmed write.

“Step is frozen” also conflates:

* validation eligibility;
* workflow checkpoint;
* source state;
* canonical frozen memory.

CORRECTION:

Remove the entire AI step-freeze authority section.

Replace it with:

“After reviewing complete local validation evidence, the AI may state that the work appears eligible for freeze preparation. It must not claim that the feature or step is frozen. Canonical freeze remains subject to read-only Preview and explicit human Confirm and Write.”

FINDING A009-F002

TITLE:
The actual current startup has superseded this prompt’s load order

SEVERITY:
CRITICAL

TARGET RULE:

“Send first when starting a PyArchitect session.”

TARGET LOAD ORDER:

1. general_prompt_stack_load_order
2. Project overlay
3. Universal Delivery Protocol
4. Project startup canon
5. Daily loader
6. Active governance files or ZIP
7. Latest handoff
8. Task description
9. Source ZIP, logs, screenshots, validation

CURRENT KANDA STARTUP:

1. tell_AI_read_before_all.md
2. first_prompts_to_ai.zip
3. prompt_library.zip
4. STARTUP PACK LOAD CHECK
5. second_prompt_files
6. collector status
7. handoff upload readme
8. compact Error Memory
9. zipped structured handoff
10. source archive parts when exact source is required
11. PROJECT READY CHECK
12. WAIT_FOR_TASK
13. prompt_library direct retrieval only after routing selects a prompt

PROBLEM:

The target creates a competing startup order.

It omits:

* current startup kernel;
* current source-map manifest;
* compact Error Memory;
* active freeze context;
* current Tool-versus-Project bridge;
* second-upload validation state;
* source-archive manifest;
* current direct prompt-library retrieval.

CORRECTION:

Do not update this prompt with the current startup sequence.

The current startup owners already define it.

Deprecate this prompt.

FINDING A009-F003

TITLE:
Prompt identity mismatch

SEVERITY:
CRITICAL

WORKSPACE METADATA ID:

general_prompt_stack_load_order

PROMPT-INTERNAL CANONICAL ID:

pyarchitect_general_prompt_stack_load_order

LEGACY APPLICATION ID:

0000_0_1_general_prompt_stack_load_order

PROBLEM:

One semantic prompt has three active identities.

Dependencies may point to different IDs.

For example, `prompt_audit_canon` declares dependency on:

pyarchitect_general_prompt_stack_load_order

while current routing uses:

general_prompt_stack_load_order

CORRECTION:

During migration, choose one historical canonical reference key and preserve the others as aliases until deletion.

Because the final recommendation is deletion, do not assign a new permanent KPR identity unless the registry requires one for deprecated prompts.

Record all three IDs in migration metadata.

FINDING A009-F004

TITLE:
Two independently maintained active source copies

SEVERITY:
CRITICAL

WORKSPACE COPY:

* 258 lines
* version 1.1
* includes Box Logic
* includes Prompt Audit Boundary
* includes AI step-freeze authority

APPLICATION COPY:

* 121 lines
* version 1.0.1
* lacks several workspace additions
* has separate metadata and profile references

PROBLEM:

Different parts of the application can load different rules for the same semantic prompt.

This violates:

* one canonical source;
* stable identity;
* Box Logic;
* NO_LEAK;
* current prompt-library ownership.

CORRECTION:

Do not continue maintaining both.

During migration:

* workspace source is the temporary canonical audit source;
* application source becomes a legacy alias or generated compatibility surface;
* both are eventually removed after dependency migration.

FINDING A009-F005

TITLE:
Source status and metadata status disagree

SEVERITY:
HIGH

SOURCE:

status: audited_candidate

METADATA:

status: active

PROBLEM:

The source says the prompt is still a candidate.

Routing and inventory treat it as active.

CORRECTION:

For migration:

status: deprecated

Do not preserve either conflicting status.

FINDING A009-F006

TITLE:
Source load mode and metadata load type disagree

SEVERITY:
CRITICAL

SOURCE:

load_mode: always_on

METADATA:

load_type: on_request

CURRENT STARTUP SOURCE MAP:

The prompt is not part of the actual always-startup package.

PROBLEM:

The prompt tells the AI to load it first in every session, while the current machine system treats it as on-demand.

CORRECTION:

During migration, retain only on-request legacy resolution.

Then remove active routing entirely before deletion.

FINDING A009-F007

TITLE:
Circular dependencies with current routing prompts

SEVERITY:
CRITICAL

TARGET METADATA REQUIRES:

* prompt_navigation_index
* prompt_router

CURRENT ROUTING ENTRIES FOR THESE PROMPTS REQUIRE:

* general_prompt_stack_load_order

This creates cycles such as:

general load order
-> prompt navigation index
-> general load order

and:

general load order
-> prompt router
-> general load order

PROBLEM:

No prompt is a stable root owner.

The cycle also causes unnecessary context loading and makes deprecation harder.

CORRECTION:

Break the cycle.

Recommended ownership:

* `ai_prompt_request_canon` decides Fast Path versus Routed Work Path and missing context.
* `prompt_navigation_index` maps intent to candidate prompts.
* `prompt_router` selects among candidates.
* `kanda_routing_system_canon` owns routing architecture.
* current startup owners define startup order.

None should require this prompt after migration.

FINDING A009-F008

TITLE:
Manual prompt-upload request conflicts with direct prompt-library retrieval

SEVERITY:
HIGH

TARGET RULE:

“Please upload them or confirm they are already loaded.”

CURRENT CONTRACT:

The uploaded `prompt_library.zip` is the canonical on-demand prompt source.

After routing selects the required prompt path, the AI should open that specific prompt directly rather than repeatedly requesting manual upload.

PROBLEM:

The target creates unnecessary user work and may incorrectly block tasks despite the prompt already being available.

CORRECTION:

Remove the manual upload rule with the prompt’s deprecation.

Current routing should:

1. select prompt code, ID, or path;
2. open the addressed prompt from the current library;
3. request user upload only when the required artifact is genuinely absent.

FINDING A009-F009

TITLE:
Precedence order can place user instruction above implementation truth

SEVERITY:
HIGH

CURRENT ORDER:

1. Current user instruction, if safe and explicit.
2. Actual source files and runtime evidence.

PROBLEM:

The user controls goals and desired outcomes.

The user’s assumption does not override:

* actual source;
* runtime evidence;
* public contracts;
* safety boundaries;
* current ownership;
* validated frozen behavior.

A request such as:

“Assume this file already contains the function”

must not outrank exact source showing that it does not.

CORRECTION:

Current-safe authority model:

1. System and safety requirements
2. Exact current source and runtime evidence for implementation truth
3. Current public contracts, Box ownership, and frozen invariants
4. Current explicit user goal, when safe
5. Current validation state
6. Current Project overlay
7. Current handoff
8. Generated summaries
9. Historical prompts
10. AI memory

The user’s goal controls the destination, not factual source state.

FINDING A009-F010

TITLE:
Terminal behavior conflicts with the current terminal owner

SEVERITY:
HIGH

TARGET RULES:

* successful install may clear automatically;
* install failure must remain visible and not clear;
* validation may ask for Enter twice before clearing;
* failed validation should not clear unless the user confirms.

CURRENT TERMINAL CONTRACT:

Successful install:

* show success;
* wait approximately two seconds;
* Clear-Host;
* no Enter prompts;
* keep terminal open.

All non-install-success blocks, including install errors and validation errors:

* preserve relevant output;
* require Enter;
* require Enter again;
* perform one final Clear-Host;
* keep terminal open.

PROBLEM:

The target defines an older parallel footer policy.

CORRECTION:

Delete terminal behavior from this prompt.

Exact terminal behavior belongs only to `terminal_cleanup_contract`.

FINDING A009-F011

TITLE:
Patch and validation behavior invades Class 05

SEVERITY:
HIGH

The prompt defines:

* install script expectations;
* validation script requirements;
* output handling;
* user copy/paste requirements;
* validation gates;
* freeze eligibility.

PROBLEM:

A load-order prompt must not own patch mechanics.

CORRECTION:

Route patch and validation work to:

* pre_output_contract_gates;
* relevant Class 05 owner;
* terminal_cleanup_contract;
* patch_install_delivery_error_register;
* Brick Wall.

FINDING A009-F012

TITLE:
Obsolete governance-files model

SEVERITY:
CRITICAL

The prompt repeatedly requires:

* current active governance files;
* governance ZIP;
* end-of-chat governance update prompt.

PROBLEM:

The current Project-specific freeze and governance-memory workflow uses:

* active freeze context;
* Project Support freeze intake;
* Project Support frozen memory;
* read-only Preview;
* explicit Confirm and Write;
* startup refresh.

The target still uses the old active-governance-file package model found in other deprecated startup prompts.

CORRECTION:

Remove these rules through deprecation.

Do not rewrite this prompt into the current freeze canon.

FINDING A009-F013

TITLE:
Beginning-of-chat closure warning duplicates the handoff owner

SEVERITY:
HIGH

The prompt contains a complete end-of-chat warning and trigger workflow using:

* LETS TAKE A BREAK
* LETS STOP NOW

The current `handoff_at_end_of_work` prompt already owns:

* those triggers;
* pause and stop detection;
* contextualized handoff;
* no new implementation after closure trigger;
* what was completed, validated, frozen, or unfinished.

PROBLEM:

The target is a second closure-workflow owner.

CORRECTION:

Remove the closure section through deprecation.

Keep all closure behavior with `handoff_at_end_of_work`.

FINDING A009-F014

TITLE:
Prompt Audit Boundary Rule duplicates the Prompt Audit Canon

SEVERITY:
HIGH

The target requires:

* audit only one prompt;
* do not edit another prompt;
* create an integration candidate file;
* require later integration and approval.

PROBLEM:

These rules belong to `prompt_audit_canon`.

Keeping them here creates two audit owners.

CORRECTION:

Remove the audit section through deprecation.

The current audit canon remains the sole owner.

FINDING A009-F015

TITLE:
Partial Box Logic creates a weaker parallel owner

SEVERITY:
HIGH

The target asks for:

* active box;
* owner paths;
* allowed files;
* out-of-scope files;
* cross-box touches;
* public contracts;
* validation.

It omits:

* Tool-versus-Project identity;
* Project Support root;
* transient garbage root;
* NO_LEAK classifications;
* mutable-state owner;
* private internals;
* approved communication routes;
* generated-artifact-as-source risk;
* MCard;
* Shield Logic;
* Brick Wall authorization.

PROBLEM:

The partial checklist may be mistaken for complete architecture authorization.

CORRECTION:

Remove the local Box section.

Use the current architecture owners.

FINDING A009-F016

TITLE:
Project-agnostic placeholders are overbroad and outdated

SEVERITY:
HIGH

The prompt requires:

* PROJECT_ROOT
* PROJECT_NAME
* PRODUCT_PACKAGE
* TASK_DESCRIPTION
* TASK_SLUG
* GOVERNANCE_FOLDER
* PROMPT_LIBRARY_FOLDER
* AUDITED_PROMPT_FOLDER
* VALIDATION_COMMANDS
* OUTPUT_FOLDER
* SOURCE_FILES
* LOG_FILES

PROBLEM:

Not every Project has:

* product package;
* governance folder;
* audit folder;
* predefined logs;
* output folder;
* task slug.

The model also omits:

* Tool root;
* Project Support root;
* transient garbage root;
* selected Project identity.

This can encourage invented values and obsolete folder creation.

CORRECTION:

Do not repair the placeholder model here.

Project identity belongs to the project-startup template and Tool-versus-Project canon.

FINDING A009-F017

TITLE:
No focused validator protects current behavior

SEVERITY:
HIGH

Exact source inspection found no focused validator for:

general_prompt_stack_load_order

PROBLEM:

The prompt is broadly referenced but has no dedicated protection proving:

* one canonical identity;
* one source owner;
* deterministic load mode;
* no freeze bypass;
* no terminal duplication;
* no obsolete startup references;
* no circular routing dependencies.

CORRECTION:

Because deletion is recommended, do not build a large validator for the old prompt.

Build a focused migration validator that proves:

* all active dependencies were removed or redirected;
* all legacy IDs resolve predictably during migration;
* no active route selects the deprecated prompt;
* current startup and routing still work;
* no old freeze authority survives.

FINDING A009-F018

TITLE:
Broad aliases create severe routing ambiguity

SEVERITY:
CRITICAL

ACTIVE ALIASES INCLUDE:

* boot
* general
* load
* order
* session
* stack
* startup

`boot`, `session`, and `startup` each collide with approximately eight Class 01 prompts.

PROBLEM:

Generic requests can select this outdated prompt instead of the current startup or router.

CORRECTION:

At deprecation:

Remove all broad aliases.

Temporarily preserve only exact legacy aliases:

* general_prompt_stack_load_order
* general_prompt_stack_load_order.md
* pyarchitect_general_prompt_stack_load_order
* 0000_0_1_general_prompt_stack_load_order
* exact historical filename

Then remove those aliases after migration validation.

FINDING A009-F019

TITLE:
Supporting group metadata is stale

SEVERITY:
MEDIUM

The group assimilation index says Class 01 contains:

prompt_count: 9

The current canonical inventory contains:

16 prompts

PROBLEM:

Although this is not caused solely by Prompt 009, its registration environment is stale.

The old group list treats several deprecated startup prompts as principal Class 01 prompts and omits newer canonical startup owners.

CORRECTION:

Update the group index only during the later governed reconciliation phase.

Do not modify it during this individual audit.

FINDING A009-F020

TITLE:
Historical audit metadata is embedded in active runtime source

SEVERITY:
HIGH

The source contains:

* audit_id: P001
* status: audited_candidate
* created_from history
* tokenizer
* historical source filenames

PROBLEM:

Audit history and runtime behavior are mixed.

The metadata file separately contains:

* mechanically reconciled status;
* rename flags;
* routing coverage.

CORRECTION:

For deprecation:

Keep migration history in reconciliation records.

Do not preserve historical audit fields in active runtime behavior.

OVERLAP AND OWNER MATRIX

WITH tell_AI_read_before_all.md:

SUPERSEDED_BY_CURRENT_STARTUP

WITH start_of_day_master_stack:

SUBSUMED_BY_EXISTING FOR BEGINNING-OF-DAY GATES

WITH session_start_upload_checklist:

SUBSUMED_BY_EXISTING FOR HUMAN UPLOAD REQUIREMENTS

WITH ai_prompt_request_canon:

SUBSUMED_BY_EXISTING FOR MISSING-CONTEXT DECISIONS

WITH prompt_navigation_index:

SUBSUMED_BY_EXISTING FOR PROMPT DISCOVERY

WITH prompt_router:

SUBSUMED_BY_EXISTING FOR ROUTE SELECTION

WITH kanda_routing_system_canon:

SUBSUMED_BY_EXISTING FOR ROUTING ARCHITECTURE

WITH project_overlay_selector:

SUBSUMED_BY_EXISTING FOR OVERLAY SELECTION

WITH handoff_at_end_of_work:

SUBSUMED_BY_EXISTING FOR CLOSURE TRIGGERS

WITH terminal_cleanup_contract:

DIRECT CONFLICT

WITH freeze_code_intake_and_form_protocol:

DIRECT CONFLICT

WITH prompt_audit_canon:

SUBSUMED_BY_EXISTING FOR AUDIT ISOLATION

WITH Brick Wall:

SUBSUMED_BY_EXISTING FOR IMPLEMENTATION AUTHORIZATION

WITH LEGACY APPLICATION COPY:

SAME IDEA, CONFLICTING SOURCE OWNERSHIP

DISSONANT LOGIC FOUND:

YES

NEW PROMPT REQUIRED:

NO

NEW LOAD-ORDER ENGINE REQUIRED:

NO

NEW ROUTING SCHEMA REQUIRED:

NO

The current system already contains all needed capabilities.

RECOMMENDED FINAL DISPOSITION

FINAL TARGET:

DELETE

INTERMEDIATE STATE:

deprecated

MIGRATION SEQUENCE:

1. Complete the remaining Class 01 audits.
2. Audit the Class 02 prompts that declare this prompt as a dependency.
3. Audit `prompt_audit_canon`, which references its old canonical ID.
4. Build a dependency and alias migration map.
5. Replace dependencies with current owners.
6. Mark workspace metadata deprecated.
7. Mark legacy application metadata deprecated.
8. Replace both bodies temporarily with a short migration notice, if a staged deprecation is needed.
9. Remove broad aliases.
10. Preserve exact historical aliases temporarily.
11. Remove the prompt from active navigation.
12. Remove it from active groups and profiles.
13. Validate current startup, routing, audit, and handoff behavior.
14. Delete both Markdown sources and metadata files.
15. Preserve historical references only in reconciliation reports.

TEMPORARY DEPRECATION NOTICE

The temporary notice should state only:

* this prompt describes a retired prompt-stack and freeze workflow;
* it is not the current startup entrypoint;
* it does not authorize freeze;
* it does not define terminal behavior;
* it does not define prompt auditing;
* current startup uses `tell_AI_read_before_all.md`;
* prompt routing uses the current routing owners;
* legacy IDs remain temporarily for migration only.

REQUIRED VALIDATION BEFORE FINAL DELETION

Identity and references:

1. Search all active Markdown prompts.
2. Search all metadata.
3. Search human routing.
4. Search machine routing.
5. Search group indexes.
6. Search profiles.
7. Search stack definitions.
8. Search substitution maps.
9. Search audit prompts.
10. Search validators.
11. Search application Prompt Library assets.
12. Search startup generators and generated startup artifacts.

Dependency migration:

13. `prompt_navigation_index` no longer requires Prompt 009.
14. `prompt_router` no longer requires Prompt 009.
15. `prompt_substitution_map` no longer requires Prompt 009.
16. `project_overlay_selector` no longer requires Prompt 009.
17. `prompt_audit_canon` no longer depends on the old canonical ID.
18. Profiles and stacks use current owners.
19. No circular routing dependency remains.
20. No active owner depends on a deprecated alias.

Startup:

21. `tell_AI_read_before_all.md` remains the human entrypoint.
22. STARTUP PACK LOAD CHECK remains required.
23. second_prompt_files remains required.
24. compact Error Memory remains loaded.
25. PROJECT READY CHECK remains required.
26. WAIT_FOR_TASK remains the startup terminal state.
27. Prompt-library direct retrieval remains functional.
28. Generic startup requests route to the current startup owner.

Freeze:

29. No active prompt grants AI step-freeze authority.
30. No active prompt says “This step is frozen” without confirmed local write.
31. Preview remains read-only.
32. Confirm and Write remains human-controlled.
33. Freeze paths use Project Support.
34. Startup freeze context refresh remains required.

Terminal and delivery:

35. Only terminal_cleanup_contract owns terminal footers.
36. Install errors use the current non-install-success footer.
37. Validation errors use the current non-install-success footer.
38. Patch output passes pre_output_contract_gates.
39. No obsolete direct install or validation rule survives.
40. No old governance ZIP model survives.

Routing:

41. Broad aliases are removed.
42. Exact legacy aliases resolve deterministically during migration.
43. Generic `startup`, `session`, `boot`, `load`, and `order` do not route here.
44. Current router functions without Prompt 009.
45. Current navigation index functions without Prompt 009.
46. Current project-overlay selection functions without Prompt 009.

Negative tests:

47. Reject reintroduction of AI freeze authority.
48. Reject `always_on` status for the deprecated prompt.
49. Reject active duplicate source copies.
50. Reject circular routing dependencies.
51. Reject old governance-files load order.
52. Reject manual prompt upload when direct retrieval is available.
53. Reject terminal behavior outside the terminal owner.
54. Reject prompt-audit behavior outside the audit owner.
55. Reject broad legacy aliases.
56. Reject a user instruction overriding exact source truth.

Validator design:

57. Validate behavior rather than exact historical prose.
58. Do not require exact future version equality.
59. Inspect actual current routing keys.
60. Permit future stronger startup and routing contracts.
61. Preserve source and metadata provenance.
62. Confirm that deleted IDs are not silently reused.

ERROR MEMORY APPLICATION

Relevant compact lessons:

lesson-brick-wall-q01-validator-exact-phrase-count-assumption-v1

Application:

Migration validators must protect route and freeze behavior rather than exact sentences.

lesson-brick-wall-q01-validator-forward-version-rigidity-v1

Application:

Do not bind migration to one exact future prompt version.

lesson-brick-wall-q02-validator-forward-contract-rigidity-v1

Application:

Allow current routing and startup owners to strengthen their contracts without preserving Prompt 009’s wording.

lesson-brick-wall-focused-validator-task-route-key-assumption-v1

Application:

Inspect the actual current routing and group schemas before asserting dependency removal.

lesson-brick-wall-delivery-unextracted-bundle-path-assumption-v1

Application:

Do not preserve old generic install behavior; use current governed patch staging and delivery.

lesson-powershell-continuation-prompt-concatenated-scriptblock-v1

Application:

Terminal behavior remains solely with the current terminal owner.

Full Error Memory ZIP needed:

NO

Reason:

The compact lessons and exact current source are sufficient for this read-only prompt audit.

BRICK WALL STATUS

Project slug:
kanda_reasoner

Task:
Audit prompt 009 individually

Current phase:
Read-only canonical audit completed

Primary box:
Prompt Library / Session Start and Navigation

External owner boxes inspected:

* Startup Delivery
* Context Routing
* Prompt Audit
* Box Architecture
* Tool-versus-Project
* Patch Delivery and Validation
* Terminal Output
* Governance and Freeze
* Handoff

Tool root:
E:\kanda_reasoner

Active Project root:
E:\kanda_reasoner

Active Project support root:
E:\kanda_reasoner_show_project_to_AI

Same physical Tool/Project root:
YES

Selected target:
general_prompt_stack_load_order.md

Current workspace source fingerprint:
7f8a2a93fd44f0c277a4b6784f9c613339d79e5fd8468f8367f87134bc36c0ba

Legacy application source fingerprint:
beedbfe1f79ab7b567c389aebc8fcd580d59432eb260d57f19e3ed0376a38b73

Verified problem status:
COMPLETE

Admission decision:
DEPRECATE_AND_DELETE_AFTER_DEPENDENCY_MIGRATION

Unique capability:
NO

Error Memory:
Compact lessons reviewed

Full Error Memory:
NOT REQUIRED

Exact-source inspection:
COMPLETE

Tool/Project boundary in target:
FAIL

Reason:

The prompt uses an obsolete generic Project model and does not resolve Tool, Project Support, or transient roots.

Box Boundary:
FAIL

Reason:

It invades startup, routing, audit, delivery, validation, terminal, handoff, and freeze owners.

NO-LEAK in target:
FAIL

Reason:

Dual active source ownership, obsolete governance authority, and user-instruction precedence can leak identity and truth.

Audit operation NO-LEAK:
COMPLETE

No source, metadata, routing, or generated artifact was modified.

MCard:
N/A

Shield:
N/A for read-only audit

Encoding:
PASS

Regression plan:
PROPOSED

Validation plan:
PROPOSED

May begin coding:
NO

May write source:
NO

May deprecate now:
NO

May delete now:
NO

Reason:

Dependent Class 01 and Class 02 prompts must be audited and migrated first.

May modify routing:
NO

May claim validation passed:
NO

May freeze:
NO

Q01-Q40 SUMMARY

Q01:
COMPLETE

Verified problems:

* obsolete startup sequence;
* freeze-authority bypass;
* three prompt identities;
* two active source copies;
* status and load-mode conflicts;
* circular dependencies;
* terminal-owner conflict;
* governance-file obsolescence;
* broad routing aliases;
* no focused validator;
* no unique remaining capability.

Admission decision:

DEPRECATE_AND_DELETE_AFTER_DEPENDENCY_MIGRATION

Q02-Q04:
COMPLETE

Relevant compact Error Memory reviewed.

Q05:
COMPLETE

Workspace source, legacy source, both metadata records, routing entries, group entries, stack/profile references, current startup, current handoff, terminal, freeze, audit, boundary, and Brick Wall owners were inspected.

Q06-Q10:
FAIL IN TARGET

Tool/Project identity, Box boundaries, NO-LEAK, and owner separation are incomplete or violated.

Q11-Q18:
N/A

No MCard transaction, Preview mutation, Shadow run, or source write occurred.

Q19-Q25:
N/A

No runtime, Qt, property-based, mutation-testing, or GUI execution occurred.

Q26:
N/A

No ZIP was built.

Q27:
PASS

Encoding, control-byte, and Markdown structural checks passed.

Q28-Q30:
FAIL IN TARGET POLICY

The target grants AI freeze authority and conflates validation review with frozen state.

No freeze write occurred during the audit.

Q31:
IN PROGRESS

A future dependency-to-validator migration plan is proposed.

Q32:
COMPLETE

Workspace and legacy source fingerprints were captured.

Q33-Q36:
N/A

No AI-model, performance, benchmark, or Python implementation change occurred.

Q37:
FAIL

Multiple active owners, duplicate sources, circular dependencies, and cross-box responsibilities exist.

Q38:
COMPLETE

Current source archive, startup delivery, compact Error Memory, and current owners were used.

Q39:
PASS

No new startup engine, routing system, schema, prompt, or context layer is recommended.

Q40:
N/A

No governed release occurred.

FINAL AUDIT RECOMMENDATION

RECOMMENDED CLASSIFICATION:
OBSOLETE GENERAL STACK AND FREEZE ROUTER

RECOMMENDED ACTION:
DEPRECATE AND DELETE AFTER DEPENDENCY MIGRATION

CURRENT STATUS:
blocked_by_conflict

LIKELY INTERMEDIATE STATUS:
deprecated

LIKELY FINAL STATE:
deleted

PROMPT CODE:
DO NOT ASSIGN UNLESS DEPRECATED-PROMPT REGISTRY REQUIRES IT

NAVIGATION EFFECT:
REMOVE ACTIVE ROUTE AND MIGRATE EXACT LEGACY ALIASES

DEPENDENCY EFFECT:
REMOVE FROM CURRENT ROUTER, NAVIGATION, AUDIT, PROFILE, AND STACK DEPENDENCIES

FINAL DECISION:

Do not rewrite this prompt as another modern startup or routing canon.

It has no remaining unique responsibility.

Migrate its active dependencies to the current canonical owners, preserve exact historical IDs temporarily, validate current startup and routing, and then delete both source copies and their metadata.

A exclusão futura deve seguir uma migração com varredura completa de referências, porque o protocolo de manutenção proíbe deixar nomes obsoletos ativos após renomeação ou remoção.