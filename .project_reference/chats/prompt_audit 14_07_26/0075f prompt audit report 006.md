PROMPT AUDIT REPORT 006

AUDIT_ID:
A006-20260714-REVIEW

PROMPT_FILENAME:
daily_startup_loader_template.md

CANONICAL_ID:
daily_startup_loader_template

CANONICAL_LIBRARY_PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_startup_loader_template.md

CURRENT CANONICAL SOURCE SHA-256:
e7d6a07ed00cf70d53a2e9c3330a87b43998882f3576dc5f5c06d113c882a422

CURRENT METADATA SHA-256:
358c8125fa5069196f51a4e1f5f80ebd5eb7cfdde921fd5e10907bfc25f36707

CURRENT SOURCE SIZE:
2,230 bytes

CURRENT SOURCE LENGTH:
81 lines

LEGACY APPLICATION COPY:

Path:
kanda_reasoner_app/prompt_library/active/0000 2.1 PYARCHITECT DAILY STARTUP LOADER TEMPLATE v1.0.md

Legacy prompt ID:
0000_2_1_daily_startup_loader_template

Legacy source SHA-256:
8bb04d439e8a4e2ea09e1cca80b80ca572d18a25282f3f1833a21ab70d7f1c44

Legacy metadata path:
kanda_reasoner_app/prompt_library/metadata/0000_2_1_daily_startup_loader_template.meta.json

DECLARED VERSION:
1.0.0

SOURCE STATUS:
Reusable daily startup loader template

METADATA STATUS:
active

METADATA LOAD TYPE:
on_request

PROMPT CODE:
MISSING

AUDIT MODE:
Read-only, one-prompt audit

SOURCE MODIFIED:
NO

METADATA MODIFIED:
NO

PATCH CREATED:
NO

NEXT PROMPT OPENED FOR AUDIT:
NO

OVERALL VERDICT

This prompt should not be deleted.

It has a potentially valid and distinct responsibility:

Create or adapt a project-agnostic daily startup-loader prompt for a new software project.

However, the current implementation does not clearly perform that responsibility.

The routing metadata says the prompt should be loaded when designing or adapting a reusable startup template.

The prompt body instead behaves as a startup loader that should be executed at the beginning of every session.

This conflict must be corrected.

RECOMMENDED ACTION:

UPDATE, REFRAME, AND CONSOLIDATE

Do not deprecate it.

Do not execute it as the current KANDA startup workflow.

Do not allow it to authorize implementation, patch delivery, validation, or freeze.

RECOMMENDED STATUS DURING CORRECTION:

blocked_by_conflict

RECOMMENDED STATUS AFTER CORRECTION AND VALIDATION:

active

DECISION GATE:

HUMAN_REQUIRED

UNIQUE CAPABILITY ASSESSMENT

UNIQUE CAPABILITY EXISTS:

YES

The prompt can own a reusable project-agnostic template for creating a daily startup loader.

This is different from:

* `start_of_day_master_stack`, which owns current KANDA beginning-of-day gates;
* `session_start_upload_checklist`, which tells a human what to upload;
* `project_startup_canon_template`, which defines project identity and project-level rules;
* `general_prompt_stack_load_order`, which defines prompt-stack order;
* `ai_prompt_request_canon`, which decides what context must be requested;
* `tell_AI_read_before_all.md`, which owns the current KANDA startup delivery sequence.

Therefore, deletion would remove a legitimate template-authoring capability.

The prompt should remain only if it is narrowed to that capability.

RECOMMENDED CLASSIFICATION

PROMPT TYPE:
TEMPLATE

SCOPE:
PROJECT-AGNOSTIC

LOAD TYPE:
ON_REQUEST

SEMANTIC OWNER:
01_session_start_and_navigation

AUTHORING-METHOD OWNER:
07_prompt_authoring_and_audit

ONE-SENTENCE RESPONSIBILITY:

Generate a draft daily-startup-loader prompt for a specified project, using current startup, routing, architecture, evidence, and governance owners without executing the generated workflow or authorizing implementation.

SINGLE RESPONSIBILITY PASS:

FAIL IN CURRENT FORM

The prompt currently combines:

1. Template authoring
2. Live session startup
3. Prompt request behavior
4. Governance loading
5. Handoff loading
6. Complexity classification
7. Roadmap creation
8. Implementation
9. Bundle construction
10. Internal validation
11. ZIP delivery
12. User validation
13. Freeze and canonization
14. Local Box Logic

A template-authoring prompt must not itself own all downstream workflow behavior.

POSITIVE FINDINGS

P006-P001

TITLE:
Project-agnostic intent

RESULT:
PASS

The prompt explicitly prohibits:

* hardcoding one project root;
* assuming one product package;
* treating examples as active Project truth;
* implementing without current source evidence.

This is a useful base principle.

P006-P002

TITLE:
Clean encoding and text structure

RESULT:
PASS

The canonical source has:

* valid UTF-8;
* no UTF-8 BOM;
* LF-only line endings;
* no prohibited control bytes;
* ASCII-only content;
* balanced Markdown fences.

Brick Wall Q27 passes.

P006-P003

TITLE:
Reasonable source-evidence requirement

RESULT:
PARTIAL PASS

The prompt says current source files, logs, and validation output should be used as evidence.

It also says missing evidence must be requested before implementation.

This is directionally aligned with exact-source discipline.

However, it does not distinguish:

* exact current source;
* generated artifacts;
* handoff summaries;
* Error Memory;
* freeze memory;
* Tool source;
* Active Project source;
* Project Support state;
* transient state.

P006-P004

TITLE:
On-request routing

RESULT:
PASS

The prompt is not an always-startup prompt.

Its on-request load type is appropriate if it is used only to create or adapt a startup-loader template.

P006-P005

TITLE:
Short and manageable source

RESULT:
PASS

At 81 lines, this prompt is appropriately sized for a focused template.

The correction should preserve this small size rather than turning it into a compiled startup canon.

CRITICAL AND HIGH-SEVERITY FINDINGS

FINDING A006-F001

TITLE:
The prompt body and routing metadata define different tasks

SEVERITY:
CRITICAL

ROUTING INTENT:

The metadata and navigation index say to load the prompt:

“When designing or adapting a reusable daily-startup prompt template.”

Example request:

“Create a daily startup loader template for a new project.”

PROMPT BODY:

The source says:

“Use: Send after the load-order prompt and project startup canon at the beginning of a work session.”

It then directly instructs the AI to:

* collect current task information;
* load governance and handoff;
* classify complexity;
* implement a bundle;
* validate;
* deliver a ZIP;
* wait for validation;
* freeze or canonize.

PROBLEM:

The routing system treats the file as a template-authoring prompt.

The body treats itself as the executable startup loader.

An AI cannot determine whether it should:

* create a new loader; or
* execute this loader.

CORRECTION:

Choose one responsibility.

Recommended decision:

This prompt creates or adapts a startup-loader template.

Add an explicit first rule:

“This prompt is an authoring template. Do not execute it as the current session startup workflow. Produce a draft startup-loader artifact for review.”

Remove direct implementation behavior from the template itself.

FINDING A006-F002

TITLE:
Two active source copies and two prompt identities exist

SEVERITY:
CRITICAL

CURRENT WORKSPACE ID:

daily_startup_loader_template

CURRENT WORKSPACE PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_startup_loader_template.md

LEGACY APPLICATION ID:

0000_2_1_daily_startup_loader_template

LEGACY APPLICATION PATH:

kanda_reasoner_app/prompt_library/active/0000 2.1 PYARCHITECT DAILY STARTUP LOADER TEMPLATE v1.0.md

The two sources are not identical.

The workspace copy contains an added Box Logic section.

The application copy does not.

PROBLEM:

The Project has two active representations of the same prompt:

* different prompt IDs;
* different filenames;
* different hashes;
* different content;
* separate metadata;
* separate grouping and profile references.

Depending on which Prompt Library interface is used, the AI or user may receive different rules.

This violates:

* one canonical owner;
* no generated or legacy artifact as source truth;
* prompt identity stability;
* Box Logic;
* Brick Wall Q37 duplicate-responsibility gate.

CORRECTION:

Establish one canonical source.

Recommended ownership:

Canonical source:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_startup_loader_template.md

Canonical ID:
daily_startup_loader_template

Legacy alias:
0000_2_1_daily_startup_loader_template

The application Prompt Library must either:

* consume the canonical source; or
* receive a generated synchronized copy from it.

Do not manually maintain both source texts.

Preserve the old ID only as a migration alias.

FINDING A006-F003

TITLE:
The prompt authorizes implementation without Brick Wall admission

SEVERITY:
CRITICAL

CURRENT FLOW:

1. Classify complexity.
2. Roadmap first for complex updates.
3. Implement one focused bundle.
4. Validate internally.
5. Deliver ZIP.
6. Wait for user validation.
7. Freeze or canonize.

MISSING:

* Verified Problem Record;
* duplicate-current-owner comparison;
* smallest-intervention decision;
* Error Memory preflight;
* exact-source gate;
* Tool-versus-Project gate;
* Box and NO-LEAK gate;
* MCard gate when applicable;
* Shield requirement;
* pre-code authorization;
* changed-file-to-validator mapping;
* exact final ZIP gate;
* local-validation evidence;
* Confirm and Write.

PROBLEM:

A startup-loader template generated from this prompt could authorize work through an obsolete lightweight flow.

CORRECTION:

The template must not define implementation authorization.

It should generate a startup loader that says:

“For governed work, route to `brick_wall_comprehensive_quality_gate` and the relevant current owner prompts. Startup context alone never authorizes coding.”

Do not copy Q01-Q40 into this template.

FINDING A006-F004

TITLE:
“Roadmap first for complex updates” conflicts with verified-problem admission

SEVERITY:
HIGH

PROBLEM:

Complexity alone does not justify a roadmap or implementation campaign.

Brick Wall requires proof that:

* a real current problem exists;
* the current owner cannot already solve it;
* the intervention is smaller than competing alternatives;
* measurable benefit is expected;
* disconfirming evidence has been considered.

CORRECTION:

Replace with:

“For complex governed work, establish a Verified Problem Record and smallest justified intervention before creating an implementation roadmap.”

The generated loader should route this behavior to Brick Wall rather than owning it.

FINDING A006-F005

TITLE:
The template hardcodes bundle and ZIP delivery into every workflow

SEVERITY:
HIGH

CURRENT FLOW:

* Implement one focused bundle.
* Deliver ZIP.

PROBLEM:

Not every task requires:

* implementation;
* a bundle;
* a ZIP;
* source modification;
* local installation.

Examples:

* explanation;
* read-only audit;
* prompt review;
* architecture analysis;
* documentation;
* routing decision;
* handoff preparation;
* validation review.

The workflow also bypasses current Class 05 release gating.

CORRECTION:

Remove bundle and ZIP delivery from the default flow.

Use conditional routing:

“If the task produces a governed patch or release artifact, load the current Class 05 owner and `pre_output_contract_gates`.”

FINDING A006-F006

TITLE:
“Validate internally” is ambiguous and may create false validation claims

SEVERITY:
HIGH

PROBLEM:

“Validate internally” does not distinguish:

* static review;
* sandbox execution;
* isolated fixture validation;
* user-local validation;
* GUI validation;
* exact final ZIP validation;
* freeze-ready validation evidence.

An AI might claim that internal reasoning or sandbox execution proves the user’s real Project installation.

CORRECTION:

Generated startup loaders must distinguish:

* evidence review;
* sandbox validation;
* user-local validation;
* freeze-ready evidence.

They must explicitly prohibit invented local validation.

Detailed validation behavior remains with the current validation owners.

FINDING A006-F007

TITLE:
Freeze and canonization rule is incomplete

SEVERITY:
HIGH

CURRENT RULE:

“Freeze/canonize only if explicitly approved.”

POSITIVE ELEMENT:

Explicit approval is mentioned.

MISSING:

* genuine user-local validation;
* Preview is read-only;
* explicit Confirm and Write;
* correct Project Support paths;
* feature-specific freeze data;
* startup freeze-context refresh;
* no automatic Error Memory write;
* no automatic freeze.

CORRECTION:

Replace with a compact owner bridge:

“Freeze is never automatic. Governed freeze requires successful user-local validation, read-only Preview, and explicit human Confirm and Write through the current freeze owner.”

Do not put the complete freeze workflow in this template.

FINDING A006-F008

TITLE:
Local Box Logic is incomplete and creates a weaker parallel owner

SEVERITY:
HIGH

CURRENT BOX SECTION REQUIRES:

* active box;
* owner paths;
* allowed files;
* out-of-scope files;
* cross-box touches;
* public contracts;
* validation.

MISSING:

* Tool versus Project;
* Project Support root;
* transient garbage root;
* NO_LEAK_LOGIC_V1;
* mutable-state owner;
* private internals;
* approved communication routes;
* generated-artifact-as-source risk;
* wrong-root writes;
* MCard;
* Shield Logic;
* Brick Wall authorization.

PROBLEM:

The generated loader may treat this partial checklist as the complete architecture gate.

CORRECTION:

Remove the local Box implementation.

Replace it with:

“For consequential work, route to `box_architecture_canon`, `project_tool_boundary_canon`, NO_LEAK_LOGIC_V1, and Brick Wall. Apply MCard and Shield Logic when their conditions are present.”

FINDING A006-F009

TITLE:
Required placeholder set is overbroad and falsely universal

SEVERITY:
HIGH

CURRENT REQUIRED VARIABLES:

* PROJECT_ROOT
* PROJECT_NAME
* PRODUCT_PACKAGE
* TASK_DESCRIPTION
* TASK_SLUG
* GOVERNANCE_FOLDER
* VALIDATION_COMMANDS
* OUTPUT_FOLDER
* SOURCE_FILES
* LOG_FILES

PROBLEM:

Not every software project has:

* a product package;
* a governance folder;
* a task slug;
* predefined validation commands;
* logs;
* an output folder.

Requiring every value can cause:

* invented placeholders;
* fake paths;
* artificial project structures;
* irrelevant data requests.

The template also omits current root roles:

* Tool root;
* Active Project root;
* Project Support root;
* transient garbage root.

CORRECTION:

Separate variables into:

Required:

* PROJECT_NAME
* ACTIVE_PROJECT_ROOT
* TASK_DESCRIPTION or SESSION_PURPOSE

Conditional:

* TOOL_ROOT
* PROJECT_SUPPORT_ROOT
* TRANSIENT_GARBAGE_ROOT
* SOURCE_FILES
* VALIDATION_COMMANDS
* LOG_FILES
* OUTPUT_OWNER
* GOVERNANCE_OR_FREEZE_CONTEXT
* PRODUCT_PACKAGE
* TASK_SLUG

A conditional variable must remain visibly unresolved rather than being invented.

FINDING A006-F010

TITLE:
Prompt-authoring governance is not loaded

SEVERITY:
CRITICAL

The routing intent is to create or adapt a prompt.

The required companions are only:

* prompt_navigation_index;
* prompt_router.

CURRENT PROMPT-AUTHORING REQUIREMENTS:

A request to create or update a prompt requires inspection of:

* 07_prompt_authoring_and_audit;
* prompt_canon_reconciliation_protocol;
* prompt_audit_canon;
* project_specific_prompt_generalization;
* relevant folder assimilation card;
* existing prompt-library assets and indexes;
* validation steps;
* bundle workflow when producing installable delivery.

PROBLEM:

The prompt can generate a new startup prompt without:

* duplicate search;
* owner analysis;
* naming checks;
* metadata registration;
* route registration;
* create-versus-update decision;
* prompt-code assignment;
* audit;
* validation.

CORRECTION:

Update routing and metadata so template creation is governed through `ai_prompt_request_canon` and the Class 07 prompt-authoring owners.

The semantic content of a startup loader remains owned by Class 01.

The process of creating or modifying it is owned by Class 07.

FINDING A006-F011

TITLE:
Broad aliases create routing ambiguity

SEVERITY:
HIGH

ACTIVE ALIASES:

* boot
* daily
* loader
* session
* startup

CURRENT COLLISIONS:

`boot`, `session`, and `startup` each match eight active Class 01 prompts.

`daily` matches three.

`loader` matches two.

PROBLEM:

A generic request such as:

* “startup”
* “boot”
* “session”

may incorrectly load this template-authoring prompt instead of the current startup owner.

CORRECTION:

Remove broad aliases.

Recommended aliases:

* daily startup loader template
* daily_startup_loader_template
* daily_startup_loader_template.md
* create startup loader template
* reusable startup loader template
* project startup loader template

Do not use:

* boot
* daily
* loader
* session
* startup

as standalone aliases.

FINDING A006-F012

TITLE:
Status field is a role description rather than lifecycle status

SEVERITY:
MEDIUM

SOURCE STATUS:

Reusable daily startup loader template

METADATA STATUS:

active

PROBLEM:

The source and metadata use different concepts.

CORRECTION:

Use:

status: active

Store the role separately:

prompt_type: template

template_role: daily_startup_loader_authoring

FINDING A006-F013

TITLE:
Version authority is incomplete

SEVERITY:
MEDIUM

SOURCE VERSION:

1.0.0

WORKSPACE METADATA VERSION:

MISSING

LEGACY APPLICATION METADATA VERSION:

1.0.0

PROBLEM:

The canonical workspace metadata does not contain the version, while the legacy application metadata does.

This reinforces dual-source ambiguity.

CORRECTION:

Add version to canonical metadata.

The corrected prompt will require a meaning-changing version increment.

Do not use exact future version equality as a permanent validator condition.

FINDING A006-F014

TITLE:
Prompt code and canonical identity fields are missing

SEVERITY:
HIGH

MISSING:

* prompt_code;
* canonical_path;
* owner_box;
* version in canonical metadata;
* title;
* when_not_to_load in metadata;
* superseded legacy ID;
* current source owner;
* do-not-regress fields.

CORRECTION:

During the governed update:

1. Inspect the full Class 01 KPR registry.
2. Assign the next genuinely unused KPR-01-xxx code.
3. Do not guess the code during this audit.
4. Register the old `0000_2_1` ID as a legacy alias.
5. Synchronize source, metadata, routing, groups, profiles, and validators.

FINDING A006-F015

TITLE:
No output contract for the template-authoring result

SEVERITY:
HIGH

The prompt says to create or adapt a template, but it does not define what the resulting template must contain.

Instead, it directly executes a startup workflow.

CORRECTION:

Define a concise draft output contract.

The generated startup-loader draft should include:

1. Purpose
2. Project identity variables
3. Tool-versus-Project variables
4. Required startup evidence
5. Conditional evidence
6. Fast Path versus Routed Work Path
7. Brick Wall bridge
8. Box and NO-LEAK bridge
9. Current-source and generated-artifact hierarchy
10. Validation-level distinctions
11. Handoff behavior
12. Freeze-confirmation bridge
13. When to load
14. When not to load
15. Unresolved placeholders
16. Validation checklist

The template must be produced as a draft for review.

It must not execute implementation.

FINDING A006-F016

TITLE:
Governance and handoff terminology is too vague

SEVERITY:
MEDIUM

CURRENT ITEMS:

* Active governance files or ZIP, if the project uses governance.
* Latest workflow handoff output, if any.
* Audit request against frozen rules.

PROBLEM:

These phrases do not distinguish:

* canonical source;
* generated handoff;
* compact Error Memory;
* full Error Memory;
* freeze context;
* frozen memory;
* project-specific support state;
* historical governance files;
* current source truth.

CORRECTION:

Use authority-aware categories:

* current canonical source;
* current Project identity and roots;
* current handoff package;
* compact Error Memory;
* active freeze context, when relevant;
* validation state;
* source archive or exact files;
* generated artifacts as evidence only.

The exact artifact names should be project-overlay data, not hardcoded universal requirements.

FINDING A006-F017

TITLE:
The prompt can be used without replacing placeholders

SEVERITY:
MEDIUM

The legacy application metadata already identifies this risk.

The current prompt says variables must be replaced but defines no hard gate proving replacement.

CORRECTION:

Before generating the draft:

* list resolved variables;
* list unresolved variables;
* block invented values;
* preserve unresolved placeholders visibly;
* prohibit promotion to active status while mandatory variables remain unresolved.

FINDING A006-F018

TITLE:
The prompt lacks a current source-truth hierarchy

SEVERITY:
MEDIUM

The prompt mentions current source and logs but does not define authority ordering.

CORRECTION:

The generated template should use a hierarchy similar to:

1. Exact current source and current runtime evidence
2. Current explicit user goal, when safe
3. Current public contracts and owner-box rules
4. Current validation state
5. Current active freeze context
6. Current handoff
7. Project overlay
8. Generated summaries and older prompts

Error Memory remains prevention guidance, not source truth.

OVERLAP ANALYSIS

WITH project_startup_canon_template:

PARTIAL OVERLAP, VALID SEPARATION POSSIBLE

`project_startup_canon_template` should define:

* Project identity;
* Project architecture;
* Project-specific rules;
* validation profile;
* domain invariants.

`daily_startup_loader_template` should define:

* what is loaded at the start of each work session;
* what evidence is conditional;
* how missing context blocks work;
* how the session routes outward.

Keep both only if this separation is explicit.

WITH session_start_upload_checklist:

PARTIAL OVERLAP

The checklist is a human-facing current operational artifact.

The template creates a reusable loader for a project.

Do not let the template become another current KANDA upload checklist.

WITH general_prompt_stack_load_order:

PARTIAL OVERLAP

The load-order prompt defines precedence and sequence.

The daily loader template defines intake and routing behavior.

WITH ai_prompt_request_canon:

SUBSUMED_BY_EXISTING for missing-prompt request discipline

The generated loader should reference this owner rather than defining a second request system.

WITH Brick Wall:

SUBSUMED_BY_EXISTING for implementation authorization

The template must not define its own implementation sequence.

WITH Class 07 prompt-authoring canons:

MANDATORY COMPANION RELATIONSHIP

Class 01 owns startup-loader semantics.

Class 07 owns the process of creating, registering, validating, and auditing the prompt.

WITH LEGACY APPLICATION COPY:

SAME_IDEA_CONFLICTING SOURCE OWNERSHIP

One copy must become canonical.

DISSONANT LOGIC FOUND:

YES

NEW PROMPT REQUIRED:

NO

NEW STARTUP SYSTEM REQUIRED:

NO

NEW SCHEMA REQUIRED:

NO

The current capability can be repaired through consolidation.

RECOMMENDED CORRECTED STRUCTURE

1. Canonical identity
2. Purpose
3. Authoring-template declaration
4. When to use
5. When not to use
6. Required owner prompts
7. Required and conditional variables
8. Authority hierarchy
9. Template-generation procedure
10. Draft output structure
11. Non-execution rule
12. Brick Wall bridge
13. Box, Tool-versus-Project, and NO-LEAK bridge
14. Validation requirements
15. Promotion and human-review rule
16. Legacy alias information
17. Version history

MANDATORY NON-EXECUTION RULE

The corrected prompt should state:

“This prompt creates a draft startup-loader prompt. It does not start a session, authorize implementation, produce a patch, validate a real Project, deliver a ZIP, or write freeze memory.”

RECOMMENDED ROUTING

WHEN TO LOAD:

* create a startup loader template;
* adapt a daily startup prompt for a new project;
* design a reusable project session loader;
* update an existing startup-loader template.

WHEN NOT TO LOAD:

* normal daily startup;
* loading the current KANDA startup pack;
* code implementation;
* patch delivery;
* freeze preparation;
* handoff generation;
* asking what files to upload in the current KANDA session.

REQUIRED COMPANIONS:

* ai_prompt_request_canon
* prompt_navigation_index
* prompt_router
* prompt_canon_reconciliation_protocol
* prompt_audit_canon
* project_specific_prompt_generalization
* relevant Class 01 folder card
* existing startup prompt assets and indexes

CONDITIONAL COMPANIONS:

* bundle_gated_development_workflow, if an installable prompt-library patch is created;
* startup-delivery maintenance owner, if generated startup delivery changes;
* Brick Wall, when implementation begins;
* current project overlay and Tool-versus-Project canon.

SMALLEST SAFE FUTURE CORRECTION PLAN

Do not implement now.

After the full prompt-library audit:

Phase 1:
Confirm the canonical Prompt Library source owner.

Phase 2:
Choose the canonical ID:

daily_startup_loader_template

Phase 3:
Register the old ID as a migration alias:

0000_2_1_daily_startup_loader_template

Phase 4:
Rewrite the canonical prompt as an authoring template.

Phase 5:
Synchronize canonical metadata.

Phase 6:
Update routing aliases and required companions.

Phase 7:
Update application Prompt Library consumption so it uses the canonical source or a generated synchronized copy.

Phase 8:
Update groups and project-profile templates that still use the legacy ID.

Phase 9:
Run focused semantic and negative validation.

Phase 10:
Do not freeze until user-local validation and explicit human confirmation.

REQUIRED VALIDATION AFTER FUTURE CORRECTION

Identity and source ownership:

1. One canonical source exists.
2. Canonical ID is stable.
3. Legacy ID resolves as an alias only.
4. Application copy is generated or removed as an independent source.
5. Canonical and runtime copies have matching hashes when both must exist.
6. Prompt code is unique.
7. KPR code matches Class 01.
8. Version is synchronized.
9. Status is synchronized.
10. Canonical path is registered.
11. Owner box is registered.

Template behavior:

12. Prompt explicitly says it is an authoring template.
13. Prompt does not execute session startup.
14. Prompt does not authorize implementation.
15. Prompt does not require a roadmap solely because work is complex.
16. Prompt does not require a bundle for every task.
17. Prompt does not require a ZIP for every task.
18. Prompt does not claim internal validation proves local validation.
19. Prompt does not write freeze memory.
20. Prompt does not define a complete freeze workflow.
21. Prompt does not duplicate Q01-Q40.
22. Prompt routes governed work to Brick Wall.

Architecture:

23. Tool-versus-Project roles are present by reference.
24. Project Support and transient roots are recognized conditionally.
25. NO-LEAK is present by reference.
26. Box Logic is present by reference.
27. MCard is conditional.
28. Shield Logic is conditional.
29. Generated artifacts are not source truth.
30. Every durable output has an owner.

Prompt authoring:

31. Class 07 companions are mandatory.
32. Existing prompt overlap is inspected.
33. Create-versus-update decision is explicit.
34. Folder placement is validated.
35. Metadata is generated.
36. Routing is generated.
37. Prompt-code registry is checked.
38. Validation steps are defined.
39. Promotion remains manual.
40. Unresolved placeholders block active promotion.

Routing:

41. Broad aliases are removed.
42. Generic “startup” routes do not load this template.
43. Exact authoring requests do load it.
44. Human and machine routing agree.
45. Legacy aliases resolve deterministically.
46. No active routing entry uses the old ID as canonical.

Encoding:

47. UTF-8 passes.
48. No BOM is introduced.
49. No prohibited control byte exists.
50. Line endings remain consistent.
51. Placeholder syntax remains valid.

Negative tests:

52. Reject a version that says “implement one focused bundle” as default.
53. Reject a version that says “deliver ZIP” as default.
54. Reject a version that directly freezes or canonizes.
55. Reject a version that omits Class 07 prompt-authoring owners.
56. Reject two independently editable active source copies.
57. Reject generic aliases such as `startup` and `session`.
58. Reject invented values for unresolved variables.
59. Reject automatic active promotion.
60. Reject exact-phrase and exact-future-version validator rigidity.

ERROR MEMORY APPLICATION

Relevant compact lessons:

lesson-brick-wall-q01-validator-exact-phrase-count-assumption-v1

Application:

Validate template semantics rather than exact sentence counts.

lesson-brick-wall-q01-validator-forward-version-rigidity-v1

Application:

Do not require exact future prompt-version equality.

lesson-brick-wall-q02-validator-forward-contract-rigidity-v1

Application:

Permit future compatible strengthening of the startup-template contract.

lesson-brick-wall-focused-validator-task-route-key-assumption-v1

Application:

Inspect actual current routing and group keys before asserting migration behavior.

lesson-brick-wall-delivery-unextracted-bundle-path-assumption-v1

Application:

The generated template must not hardcode unsafe ZIP or extraction assumptions.

Full Error Memory ZIP needed:

NO

Reason:

The compact lessons are sufficient for this read-only audit.

BRICK WALL STATUS

Project slug:
kanda_reasoner

Task:
Audit prompt 006 individually

Current phase:
Read-only canonical audit completed

Primary box:
Prompt Library / Session Start and Navigation

Authoring-method owner:
Prompt Authoring and Audit

External owner boxes inspected:

* Context Routing
* Brick Wall Governance
* Box Architecture
* Tool-versus-Project
* Patch Delivery
* Freeze Workflow

Tool root:
E:\kanda_reasoner

Active Project root:
E:\kanda_reasoner

Active Project support root:
E:\kanda_reasoner_show_project_to_AI

Same physical Tool/Project root:
YES

Selected target:
daily_startup_loader_template.md

Canonical source fingerprint:
e7d6a07ed00cf70d53a2e9c3330a87b43998882f3576dc5f5c06d113c882a422

Legacy application source fingerprint:
8bb04d439e8a4e2ea09e1cca80b80ca572d18a25282f3f1833a21ab70d7f1c44

Verified problem status:
COMPLETE

Admission decision:
UPDATE_AND_CONSOLIDATE

Unique capability:
YES

Error Memory:
Compact lessons reviewed

Exact-source inspection:
COMPLETE

Tool/Project boundary:
PARTIAL FAIL IN TARGET

Reason:

Current root roles and generated-artifact ownership are incomplete.

Box Boundary:
FAIL IN TARGET

Reason:

The prompt defines partial Box Logic and downstream implementation behavior owned elsewhere.

NO-LEAK:
FAIL IN TARGET DESIGN

Reason:

The template does not identify durable output ownership and has two independently maintained source copies.

Audit operation NO-LEAK:
COMPLETE

No file was written.

MCard:
N/A for read-only audit

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

May consolidate duplicate copies now:
NO

May assign prompt code now:
NO

May build patch:
NO

May claim validation passed:
NO

May freeze:
NO

Q01-Q40 SUMMARY

Q01:
COMPLETE

Verified problems:

* body-versus-routing intent conflict;
* dual source ownership;
* old implementation flow;
* missing Brick Wall;
* incomplete Box Logic;
* missing prompt-authoring governance;
* broad aliases;
* incomplete metadata.

Admission decision:

UPDATE_AND_CONSOLIDATE

Q02-Q04:
COMPLETE

Relevant compact Error Memory reviewed.

Q05:
COMPLETE

Canonical source, metadata, routing, groups, profile references, and legacy application copy were inspected.

Q06:
PARTIAL FAIL IN TARGET

Tool and Project root roles are incomplete.

Q07-Q10:
FAIL IN TARGET

Duplicate active source ownership and incomplete NO-LEAK behavior exist.

Q11-Q18:
N/A

No MCard transaction, mutation, Preview, Shadow, or async operation occurred.

Q19-Q25:
N/A

No runtime, Qt, property-based, mutation-testing, or GUI work occurred.

Q26:
N/A

No ZIP was built or delivered.

Q27:
PASS

Encoding and structural checks passed.

Q28-Q30:
N/A

No exception, execution, freeze write, or human confirmation operation occurred.

Q31:
IN PROGRESS

A future changed-file-to-validator map is proposed.

Q32:
COMPLETE

Canonical and legacy source fingerprints were captured.

Q33-Q36:
N/A

No AI-model, performance, benchmark, or Python implementation work occurred.

Q37:
FAIL

Two independently maintained active representations exist.

Q38:
COMPLETE

Current source archive, metadata, routing, and legacy application assets were inspected.

Q39:
PASS

No new engine, startup system, schema, or prompt is recommended.

Q40:
N/A

No governed release occurred.

FINAL AUDIT RECOMMENDATION

RECOMMENDED_CLASSIFICATION:
PROJECT-AGNOSTIC STARTUP-LOADER AUTHORING TEMPLATE

RECOMMENDED_ACTION:
UPDATE, REFRAME, AND CONSOLIDATE

CURRENT STATUS:
blocked_by_conflict

LIKELY FINAL STATUS:
active

DELETE:
NO

DEPRECATE:
NO

CANONICAL ID:
daily_startup_loader_template

LEGACY ID:
0000_2_1_daily_startup_loader_template

LEGACY ID DISPOSITION:
MIGRATION ALIAS ONLY

NAVIGATION EFFECT:
NARROW ROUTING TO TEMPLATE-AUTHORING REQUESTS

FINAL DECISION:

Keep this prompt because it has a legitimate unique capability.

Rewrite it so that it creates a draft startup-loader template rather than executing a startup and implementation workflow.

Consolidate the duplicate application copy under one canonical source.

Do not modify it until the remaining prompt audits establish the complete canonical owner and dependency matrix.
