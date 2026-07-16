PROMPT AUDIT REPORT 012

AUDIT_ID:
A012-20260714-REVIEW

PROMPT_FILENAME:
project_startup_canon_template.md

CANONICAL_ID:
project_startup_canon_template

CANONICAL_LIBRARY_PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/project_startup_canon_template.md

CURRENT SOURCE SHA-256:
4b6bd936ae3ebb58403fac36118127c455879e222c0c3649502ff78f7c3ad391

CURRENT METADATA SHA-256:
058ba269e5de4d81601723d180037bb24952895e55c5f6fd6831eb4614a376a9

CURRENT SOURCE SIZE:
2,477 bytes

CURRENT SOURCE LENGTH:
89 lines

LEGACY APPLICATION COPY:

Path:
kanda_reasoner_app/prompt_library/active/0000 1.0 PYARCHITECT PROJECT STARTUP CANON TEMPLATE v1.0.md

Legacy prompt ID:
0000_1_0_project_startup_canon_template

Legacy source SHA-256:
4a32868035903937eb5cdac019779c01fd5d654c78992ee1a531b9b6211d59c6

Legacy source size:
2,106 bytes

Legacy source length:
76 lines

LEGACY METADATA SHA-256:
61cacabdcd68e08f704813938e6e019f086d347a1bcac86781c67277e322f49d

DECLARED VERSION:
1.0.0

SOURCE STATUS:
Reusable project profile template

METADATA STATUS:
active

METADATA LOAD TYPE:
on_request

PROMPT CODE:
MISSING

DEDICATED FOCUSED VALIDATOR:
MISSING

AUDIT CANON:
prompt_audit_canon version 1.0

AUDIT MODE:
Read-only, one-prompt audit

SOURCE MODIFIED:
NO

METADATA MODIFIED:
NO

LEGACY COPY MODIFIED:
NO

PATCH CREATED:
NO

NEXT PROMPT OPENED FOR AUDIT:
NO

OVERALL VERDICT

This prompt has a legitimate and distinct capability and should not be deleted.

Its correct long-term role is to help create a project-specific startup canon or project profile containing stable Project identity, architecture, ownership, domain invariants, validation profile, and Project-specific operating constraints.

However, the current prompt is not sufficiently aligned with the current KANDA canon, Brick Wall, Tool-versus-Project Logic, Box Logic, NO_LEAK_LOGIC_V1, prompt-authoring governance, or the current prompt identity model.

RECOMMENDED ACTION:

KEEP, UPDATE, REFRAME, AND CONSOLIDATE

The prompt should remain an on-request authoring template.

It must not be treated as:

* a live startup prompt;
* a current Project overlay;
* an implementation authority;
* a validation authority;
* a delivery protocol;
* a freeze protocol;
* a universal Python engineering prompt.

RECOMMENDED CURRENT STATUS:

blocked_by_conflict

RECOMMENDED FINAL STATUS AFTER CORRECTION AND VALIDATION:

active

DECISION GATE:

HUMAN_REQUIRED

UNIQUE CAPABILITY ASSESSMENT

UNIQUE CAPABILITY EXISTS:

YES

The prompt can own:

Creation of a draft Project Startup Canon or Project Profile for one selected software project.

That draft may describe:

* Project identity;
* Project roots and ownership;
* Project architecture;
* Project-specific owner boxes;
* public contracts;
* domain invariants;
* source-truth hierarchy;
* validation profile;
* Project-specific technology constraints;
* Project-specific do-not-regress rules;
* conditional workflow owners;
* unresolved variables.

This responsibility is distinct from:

daily_startup_loader_template:
Defines what a work session loads and how missing session evidence is handled.

session_start_upload_checklist:
Tells the human which files to upload for the current KANDA startup workflow.

start_of_day_master_stack:
Provides the compact current KANDA beginning-of-day governance kernel.

project_overlay_selector:
Selects or loads an existing Project-specific overlay.

project_specific_prompt_generalization:
Extracts reusable engineering patterns from Project-specific material.

prompt_canon_reconciliation_protocol:
Decides whether prompt content should create, update, link, deprecate, or remain reference-only.

RECOMMENDED CLASSIFICATION

SCOPE:
project_agnostic authoring prompt

TYPE:
SPECIALIST or PROTOCOL

GENERATED OUTPUT TYPE:
OVERLAY

LOAD TYPE:
on_request

OWNER GROUP:
01_session_start_and_navigation

AUTHORING-METHOD OWNER:
07_prompt_authoring_and_audit

ONE-SENTENCE RESPONSIBILITY:

Create a reviewable draft Project Startup Canon that records stable Project-specific identity, ownership, architecture, invariants, validation profile, and operating constraints without executing the Project workflow or authorizing implementation.

SINGLE RESPONSIBILITY PASS:

PARTIAL FAIL

The central responsibility is recognizable, but the prompt currently mixes:

* Project profile authoring;
* live Box Architecture enforcement;
* current-task intake;
* generic Python coding rules;
* generic GUI implementation advice;
* truth-source precedence;
* delivery-protocol selection;
* freeze authorization.

The future prompt should create the Project profile.

It must not itself become the complete implementation governance stack.

POSITIVE FINDINGS

P012-P001

TITLE:
A valid unique purpose exists

RESULT:
PASS

The prompt clearly aims to define one Project’s identity and Project-specific rules.

That capability is useful and not fully replaced by another current prompt.

P012-P002

TITLE:
Project-agnostic intent

RESULT:
PASS

The prompt explicitly says:

* do not hardcode one Project root;
* do not assume one product package;
* do not treat examples as active Project truth;
* request missing evidence before implementation.

These principles should be retained in updated form.

P012-P003

TITLE:
On-request load mode

RESULT:
PASS

The template is not loaded at every startup.

This is appropriate because it is needed only when creating or revising a Project profile.

P012-P004

TITLE:
Encoding and structural integrity

RESULT:
PASS

The canonical source has:

* valid UTF-8;
* no UTF-8 BOM;
* LF-only line endings;
* no prohibited control bytes;
* balanced Markdown fences;
* ASCII-only content.

BRICK WALL Q27:

PASS

P012-P005

TITLE:
Short and manageable source

RESULT:
PASS

At 89 lines, the prompt is small enough to remain a focused authoring template.

The correction should preserve this compact size.

P012-P006

TITLE:
Current and legacy copies are easy to compare

RESULT:
PASS FOR AUDITABILITY

The current workspace source differs from the legacy application copy only by:

* a renamed title;
* an added Box Logic section at the beginning.

This makes the dual-source conflict clear and recoverable.

CRITICAL AND HIGH-SEVERITY FINDINGS

FINDING A012-F001

TITLE:
Two independently editable active source copies and two prompt identities exist

SEVERITY:
CRITICAL

CURRENT WORKSPACE SOURCE:

Prompt ID:
project_startup_canon_template

Path:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/project_startup_canon_template.md

LEGACY APPLICATION SOURCE:

Prompt ID:
0000_1_0_project_startup_canon_template

Path:
kanda_reasoner_app/prompt_library/active/0000 1.0 PYARCHITECT PROJECT STARTUP CANON TEMPLATE v1.0.md

The two sources have different hashes and different content.

The workspace source contains a Box Logic section that the application copy does not contain.

PROBLEM:

The Project has two active representations of the same conceptual prompt:

* different prompt IDs;
* different paths;
* different metadata;
* different hashes;
* different content;
* different grouping and profile references.

The result delivered to a user may depend on which Prompt Library surface is used.

This violates:

* one canonical source;
* stable identity;
* Box ownership;
* NO_LEAK source-authority rules;
* Brick Wall duplicate-responsibility protection.

CORRECTION:

Establish one canonical source:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/project_startup_canon_template.md

Use:

project_startup_canon_template

as the canonical prompt ID.

Preserve:

0000_1_0_project_startup_canon_template

only as a migration alias.

The application Prompt Library should consume:

* the canonical source directly; or
* a generated synchronized copy.

It must not maintain a separate manually editable behavioral source.

FINDING A012-F002

TITLE:
The prompt does not explicitly declare itself an authoring template

SEVERITY:
CRITICAL

The metadata and route say the prompt is used to create a Project startup canon template.

The prompt body says:

“Adapt this file to define project-specific architecture, safety, validation, and box rules.”

It does not explicitly state whether the AI should:

* create a draft Project profile;
* execute the instructions as the current Project profile;
* treat the placeholders as active;
* install or activate the result.

PROBLEM:

The source can be copied into a session and interpreted as current Project governance before its variables have been resolved or reviewed.

CORRECTION:

Add a first-position non-execution rule:

“This prompt creates or revises a draft Project Startup Canon. It is not itself the current Project canon, does not start a session, does not authorize implementation, and must not be promoted to active use until all mandatory Project variables are resolved, reviewed, registered, and validated.”

FINDING A012-F003

TITLE:
Stable Project identity is mixed with task-specific session data

SEVERITY:
CRITICAL

CURRENT REQUIRED VARIABLES INCLUDE:

* TASK_DESCRIPTION;
* TASK_SLUG;
* SOURCE_FILES;
* LOG_FILES;
* OUTPUT_FOLDER.

PROBLEM:

A Project Startup Canon should represent stable Project truth.

A task description, task slug, current source-file subset, current logs, and one output folder change from task to task.

Embedding them in the Project profile creates:

* stale task state;
* current-session leakage into durable Project canon;
* unnecessary profile rewrites;
* overlap with the daily startup loader;
* overlap with handoff and task-routing prompts.

CORRECTION:

Remove task-specific values from the durable Project profile.

Route them to:

* daily startup loader;
* current workflow handoff;
* current task intake;
* Brick Wall Verified Problem Record;
* implementation roadmap, when justified.

The Project profile may instead define stable source roots, source authority, default validation commands, durable output owners, and task-intake owner prompts.

FINDING A012-F004

TITLE:
The required-variable and adaptation-variable lists conflict

SEVERITY:
HIGH

REQUIRED VARIABLES INCLUDE:

* PROJECT_ROOT;
* PROJECT_NAME;
* PRODUCT_PACKAGE;
* TASK_DESCRIPTION;
* TASK_SLUG;
* GOVERNANCE_FOLDER;
* VALIDATION_COMMANDS;
* OUTPUT_FOLDER;
* SOURCE_FILES;
* LOG_FILES.

ADAPTATION VARIABLES INCLUDE:

* PROJECT_NAME;
* PROJECT_ROOT;
* PRODUCT_PACKAGE;
* NON_CANONICAL_FOLDERS;
* DOMAIN_CRITICAL_STATE;
* DOMAIN_PIPELINE_RULES;
* GUI_FRAMEWORK;
* VALIDATION_COMMANDS.

Several values appear in only one list.

PROBLEM:

There is no authoritative placeholder set.

An AI cannot determine:

* which variables are mandatory;
* which are optional;
* which are task-specific;
* which may remain unresolved;
* which block promotion.

CORRECTION:

Define one authoritative variable matrix.

Recommended mandatory stable variables:

* PROJECT_NAME;
* PROJECT_SLUG;
* ACTIVE_PROJECT_ROOT;
* PROJECT_PURPOSE;
* SOURCE_AUTHORITY;
* PRIMARY_TECHNOLOGY_OR_RUNTIME;
* DEFAULT_VALIDATION_PROFILE.

Recommended conditional variables:

* TOOL_ROOT;
* ACTIVE_PROJECT_SUPPORT_ROOT;
* TRANSIENT_GARBAGE_ROOT;
* PRODUCT_PACKAGE;
* GUI_FRAMEWORK;
* DOMAIN_INVARIANTS;
* DATA_OR_PIPELINE_INVARIANTS;
* OWNER_BOXES;
* PUBLIC_CONTRACTS;
* NON_CANONICAL_OR_GENERATED_PATHS;
* DEFAULT_OUTPUT_OWNERS;
* FREEZE_CONTEXT_OWNER;
* ERROR_MEMORY_OWNER.

Task description, task slug, current logs, and current source subset should not be Project-profile variables.

FINDING A012-F005

TITLE:
The template cannot represent Tool-versus-Project separation

SEVERITY:
CRITICAL

The prompt uses only:

<PROJECT_ROOT>

It has no representation for:

* Tool root;
* Active Project root;
* Active Project Support root;
* transient garbage root;
* same physical Tool/Project root;
* forbidden nested support root.

PROBLEM:

This is unsafe for KANDA self-hosting and for any reusable Tool operating on another Project.

A generated Project profile may collapse:

* reusable Tool source;
* target Project source;
* Project-specific support state;
* disposable staging.

CORRECTION:

The generated profile must explicitly resolve:

```text
tool_root
active_project_root
active_project_support_root
transient_garbage_root
same_physical_tool_project_root
```

When a role does not apply, it must be marked:

N/A

It must never be silently omitted or invented.

FINDING A012-F006

TITLE:
No Project Support or transient ownership model exists

SEVERITY:
HIGH

The prompt has:

OUTPUT_FOLDER

but does not classify:

* source output;
* generated durable support output;
* validation evidence;
* handoff output;
* Error Memory;
* freeze memory;
* temporary staging;
* disposable Shadow output.

PROBLEM:

One generic output folder cannot safely own every Project artifact.

CORRECTION:

Replace OUTPUT_FOLDER with owner-aware categories:

* Active Project source owner;
* durable Project Support owner;
* specialized validation-evidence owner;
* handoff owner;
* Error Memory owner;
* freeze owner;
* transient garbage owner.

The Project profile should record routing rules and owner roots, not one universal output directory.

FINDING A012-F007

TITLE:
The truth hierarchy is outdated and ambiguous

SEVERITY:
CRITICAL

CURRENT HIERARCHY:

1. Actual source files and logs.
2. Current user instruction for goals.
3. Active governance files, if present.
4. Current handoff.
5. This Project profile.
6. Universal delivery protocol.
7. Older prompts and examples.

PROBLEMS:

“Active governance files” is ambiguous and reflects the older five-file governance model.

“Current handoff” is generated evidence and may be stale.

“Universal delivery protocol” is not source truth.

The hierarchy omits:

* current public contracts;
* Tool-versus-Project ownership;
* current runtime evidence;
* current validation state;
* active freeze context;
* exact source fingerprints;
* generated-artifact non-authority;
* Error Memory’s role as prevention guidance rather than source truth.

CORRECTION:

Recommended authority hierarchy:

1. Exact current source and current runtime behavior.
2. Current explicit human goal, when safe and compatible with higher authority.
3. Current owner-box public contracts and Project ownership rules.
4. Current validation state and evidence tied to the exact source.
5. Current active freeze context, when relevant.
6. Current Project profile or overlay.
7. Current handoff as contextual evidence.
8. Compact Error Memory as prevention guidance, not source truth.
9. Generated summaries, reports, older prompts, examples, and historical artifacts.

Delivery protocols govern artifact delivery; they are not Project truth.

FINDING A012-F008

TITLE:
Local Box Logic is incomplete and creates a weaker parallel architecture owner

SEVERITY:
HIGH

CURRENT BOX REQUIREMENTS INCLUDE:

* active box;
* owner paths;
* allowed files;
* out-of-scope files;
* cross-box touches;
* public contracts;
* validation.

MISSING:

* Tool-versus-Project identity;
* Project Support ownership;
* transient garbage ownership;
* NO_LEAK_LOGIC_V1 classification;
* private internals;
* approved communication routes;
* mutable-state owner;
* hidden shared state;
* generated-artifact-as-source leakage;
* wrong-root writes;
* MCard lifecycle;
* Shield Logic;
* Brick Wall authorization.

PROBLEM:

The Project profile template may generate a weaker local Box Architecture contract and present it as sufficient.

CORRECTION:

The template should not reproduce generic Box Logic.

It should collect Project-specific Box information such as:

* Project box names;
* responsibilities;
* owner paths;
* public contracts;
* dependencies;
* Project-specific boundary risks.

Generic architecture enforcement remains owned by:

* box_architecture_canon;
* kanda_box_shielding_canon;
* project_tool_boundary_canon;
* NO_LEAK_LOGIC_V1;
* architecture_review_project_card_machine_canon, when applicable;
* Brick Wall.

FINDING A012-F009

TITLE:
Generic Python engineering rules invade Class 08 ownership

SEVERITY:
HIGH

CURRENT RULE:

“Use standard Python 3.10+ when the project is Python. Preserve platform assumptions supplied by the project. Avoid import side effects, wildcard imports, circular imports, and hidden global state changes.”

PROBLEM:

This is generic implementation guidance, not Project-profile content.

It partially duplicates:

* Python Clean Code;
* Python Clean Architecture;
* Python Refactoring;
* Python Validation and Type Safety;
* Python Engineering Core.

It also assumes Python 3.10+ without proving the selected Project’s runtime.

CORRECTION:

The Project profile should record Project-specific facts:

```text
language:
runtime version:
package manager:
supported platforms:
formatters:
linters:
type checkers:
test framework:
module-size policy:
Project-specific prohibited patterns:
```

Generic engineering behavior should remain with the appropriate Class 08 or Class 09 owner.

Do not impose Python rules on non-Python projects.

FINDING A012-F010

TITLE:
Generic GUI rules invade GUI and architecture owners

SEVERITY:
HIGH

CURRENT RULE:

“If the project has a GUI, use layouts, screen-aware sizing, safe signal blocking, and manual GUI checklists where relevant.”

PROBLEM:

This is generic GUI implementation advice.

It does not define Project-specific GUI truth and is too incomplete to serve as a GUI safety canon.

CORRECTION:

The generated profile should record only Project-specific GUI information, for example:

* GUI framework;
* main window owner;
* controller/view separation;
* UI state owner;
* persistence owner;
* screen-scaling requirements;
* critical user flows;
* required GUI validators;
* known do-not-regress behaviors.

Detailed GUI implementation rules remain with specialist architecture and engineering prompts.

FINDING A012-F011

TITLE:
Freeze rule is incomplete and may be interpreted as sufficient

SEVERITY:
HIGH

CURRENT RULE:

“Do not update canon before validation and explicit user approval.”

POSITIVE:

It preserves validation and human authority in broad terms.

MISSING:

* genuine user-local validation;
* read-only Preview;
* explicit Confirm and Write;
* feature-specific freeze evidence;
* Project Support freeze paths;
* startup freeze-context refresh;
* separation between prompt activation and Project freeze;
* prohibition on automatic Error Memory or freeze writes.

CORRECTION:

Use a compact bridge:

“This template does not write Project canon or freeze memory. Promotion of a generated profile remains manual. Governed freeze requires genuine user-local validation, read-only Preview, and explicit human Confirm and Write through the current freeze owner.”

Do not copy the full freeze protocol into this template.

FINDING A012-F012

TITLE:
Prompt-authoring governance is missing

SEVERITY:
CRITICAL

Creating or adapting a Project startup canon is prompt-authoring work.

CURRENT REQUIRED COMPANIONS:

* prompt_navigation_index;
* prompt_router.

MISSING:

* ai_prompt_request_canon;
* 07_prompt_authoring_and_audit;
* prompt_canon_reconciliation_protocol;
* prompt_audit_canon;
* project_specific_prompt_generalization;
* prompt_identity_code_registry_canon;
* prompt_insertion_and_router_registration_protocol;
* relevant folder assimilation card;
* existing Project profiles and overlays;
* duplicate and overlap inspection;
* validation plan.

PROBLEM:

The prompt can create a new Project canon without checking whether:

* an existing Project profile already exists;
* the current request should update an overlay;
* the output belongs in another owner;
* the prompt ID collides;
* metadata exists;
* routing is needed;
* the result is Project-specific rather than reusable.

CORRECTION:

Class 01 owns the semantics of a Project startup profile.

Class 07 must govern the process of creating, updating, registering, validating, and promoting it.

FINDING A012-F013

TITLE:
No create-versus-update-versus-select decision exists

SEVERITY:
HIGH

The prompt assumes the task is to adapt a new template.

It does not ask whether the correct action is:

* create a new Project profile;
* update an existing Project profile;
* select an existing overlay;
* link/register an existing profile;
* preserve the uploaded material as reference-only.

PROBLEM:

This can create duplicate Project canons.

CORRECTION:

Before drafting, require one decision:

```text
CREATE_NEW_PROJECT_PROFILE
UPDATE_EXISTING_PROJECT_PROFILE
SELECT_OR_LINK_EXISTING_PROFILE
REFERENCE_ONLY
BLOCKED_NEEDS_MORE_EVIDENCE
```

This decision must be based on inspection of existing Project overlays and prompt assets.

FINDING A012-F014

TITLE:
No hard placeholder-resolution and promotion gate exists

SEVERITY:
HIGH

The source says variables must be replaced.

It does not require:

* a resolved-variable list;
* an unresolved-variable list;
* proof that required paths exist;
* proof that values belong to the selected Project;
* a promotion decision;
* blocking activation when placeholders remain.

The legacy metadata recognizes this risk, but the canonical workspace metadata does not preserve the mitigation.

CORRECTION:

Every generated draft must output:

```text
RESOLVED VARIABLES
...

UNRESOLVED REQUIRED VARIABLES
...

UNRESOLVED CONDITIONAL VARIABLES
...

PROMOTION STATUS:
DRAFT_ONLY / READY_FOR_REVIEW / BLOCKED
```

Mandatory unresolved variables must block active promotion.

Never invent missing roots, package names, validators, or owner paths.

FINDING A012-F015

TITLE:
No defined output contract exists for the generated Project canon

SEVERITY:
HIGH

The source lists some variables and rules but does not define the structure of the resulting artifact.

PROBLEM:

Different AIs may generate incompatible Project profiles.

CORRECTION:

Define a concise output structure:

1. Project identity
2. Tool-versus-Project identity
3. Root and artifact ownership
4. Project purpose and scope
5. Source authority
6. Architecture and owner boxes
7. Public contracts
8. Domain and pipeline invariants
9. Technology and runtime profile
10. GUI profile, when applicable
11. Validation profile
12. Durable evidence and support owners
13. Error Memory and freeze owners
14. Do-not-regress rules
15. Conditional specialist prompts
16. Unresolved variables
17. Draft/promotion status
18. Version and provenance

The generated result remains a draft.

FINDING A012-F016

TITLE:
Canonical metadata is incomplete

SEVERITY:
HIGH

CURRENT CANONICAL METADATA CONTAINS:

* prompt_id;
* display_name;
* filename;
* category;
* status;
* load_type;
* source_stage;
* description;
* trigger phrases;
* required companions.

MISSING:

* prompt_code;
* version;
* title;
* canonical_path;
* relative_path;
* owner_box;
* prompt type;
* when_to_load;
* when_not_to_load;
* legacy alias;
* generated-output type;
* promotion policy;
* edit policy;
* validation owner;
* do-not-regress rules;
* supersession information.

CORRECTION:

Modernize canonical metadata during the later governed update.

Do not preserve the legacy application metadata as a second authority.

FINDING A012-F017

TITLE:
Source status is a role description rather than a lifecycle status

SEVERITY:
MEDIUM

SOURCE STATUS:

Reusable project profile template

METADATA STATUS:

active

PROBLEM:

These fields describe different concepts.

CORRECTION:

Use:

status: active

Store the role separately:

```text
prompt_type: specialist_authoring_template
generated_output_type: project_overlay
```

FINDING A012-F018

TITLE:
Version authority is incomplete

SEVERITY:
MEDIUM

SOURCE VERSION:

1.0.0

CANONICAL METADATA VERSION:

MISSING

LEGACY METADATA VERSION:

1.0.0

PROBLEM:

The old application metadata contains machine-readable version information that the canonical workspace metadata lacks.

This reinforces the dual-authority problem.

CORRECTION:

Add synchronized version information to canonical metadata.

The future meaning-changing correction requires a version increment.

Validators must protect minimum compatible behavior and current self-consistency, not permanent exact version equality.

FINDING A012-F019

TITLE:
Prompt code is missing

SEVERITY:
HIGH

The prompt is active and directly routed but has no KPR code.

CORRECTION:

During the correction phase:

* inspect the complete current Class 01 code registry;
* assign the next genuinely unused KPR-01 code;
* do not infer the number from apparent gaps;
* synchronize prompt source, metadata, routing, registries, and validators;
* preserve the code permanently after assignment.

Do not assign a code during this read-only audit.

FINDING A012-F020

TITLE:
Broad aliases create severe routing ambiguity

SEVERITY:
HIGH

CURRENT ALIASES INCLUDE:

* boot;
* project;
* session;
* startup.

Current routing shows that:

* boot matches eight active Class 01 prompts;
* session matches eight;
* startup matches eight;
* project matches several Project-related prompts.

PROBLEM:

A generic request such as:

“startup”

or:

“project”

may load this authoring template when the user actually wants:

* normal startup;
* current Project selection;
* current overlay;
* upload instructions;
* Project folder organization;
* project-specific prompt generalization.

CORRECTION:

Remove broad standalone aliases.

Recommended narrow aliases:

* project startup canon template;
* project_startup_canon_template;
* create project startup canon;
* create project profile prompt;
* define project-specific startup rules;
* build project canon template;
* update project startup profile.

FINDING A012-F021

TITLE:
Legacy group and stack registrations still use the old ID

SEVERITY:
CRITICAL

The legacy application system registers:

0000_1_0_project_startup_canon_template

inside:

* Daily Start Prompts;
* High-Risk Engineering;
* Project Prompt Stack Profile Template;
* General Project Daily Prompt Stack;
* legacy general prompt load order.

PROBLEM:

The old ID remains an active stack component rather than a migration alias.

The template is also treated as a live high-risk engineering prompt, even though it should be an authoring template.

CORRECTION:

Migrate all active registrations to the canonical ID.

Do not include this template automatically in:

* normal daily startup;
* every high-risk engineering task;
* current KANDA startup.

Load it only when creating or updating a Project profile.

FINDING A012-F022

TITLE:
Legacy profile references an obsolete startup and governance model

SEVERITY:
HIGH

The legacy Project Prompt Stack Profile still expects:

* Universal Delivery Protocol;
* Project Startup Canon;
* Daily Startup Loader;
* active governance files or ZIP;
* latest workflow handoff;
* old conditional governance prompts.

PROBLEM:

This profile belongs to the same older startup family identified in previous audits.

It should not determine the new canonical template’s output.

CORRECTION:

Treat these legacy stack files as migration evidence only.

Do not copy their full daily-upload model into the corrected Project profile template.

FINDING A012-F023

TITLE:
Legacy metadata has a misleading default output folder

SEVERITY:
HIGH

LEGACY DEFAULT OUTPUT FOLDER:

<PROJECT_ROOT>_project_reference\prompt_library

LEGACY METADATA ALSO SAYS:

creates_files: false

PROBLEM:

The record simultaneously says the prompt does not create files and defines a default file-creation destination.

The destination may also be wrong for the selected Project’s current ownership model.

CORRECTION:

Remove automatic output-path assumptions.

The authoring prompt should produce a draft in the current response or in a governed prompt-library update workflow.

Durable storage must be selected by the relevant source or Project Support owner.

FINDING A012-F024

TITLE:
The prompt lacks a source-versus-generated-artifact rule

SEVERITY:
HIGH

A generated Project profile, handoff, report, or copied prompt may be mistaken for current canonical Project truth.

CORRECTION:

Add:

“A generated draft, handoff, report, exported profile, or copied prompt is not canonical source merely because it describes the Project. Promotion requires explicit owner selection, metadata, validation, and human approval.”

FINDING A012-F025

TITLE:
The template does not define when it must not be loaded

SEVERITY:
MEDIUM

The routing index says not to load it when an existing Project already has a startup canon.

The prompt source itself does not say this.

CORRECTION:

Add a clear “When not to use” section:

Do not load for:

* normal current-session startup;
* implementation in an already configured Project;
* selecting an existing Project;
* patch delivery;
* validation;
* freeze preparation;
* handoff generation;
* generic architecture advice;
* current KANDA startup pack loading.

FINDING A012-F026

TITLE:
No focused validator protects the prompt

SEVERITY:
HIGH

Exact-source inspection found no dedicated validator or test for this prompt.

PROBLEM:

There is no deterministic protection against:

* duplicate active source copies;
* unresolved placeholders;
* task-specific data leaking into the durable profile;
* broad aliases;
* missing Tool/Project roots;
* automatic activation;
* missing Class 07 authoring owners;
* stale old ID registration;
* generic implementation rules becoming Project truth.

CORRECTION:

Create a focused semantic validator during the later correction phase.

The validator must test behavior and structure, not exact explanatory prose.

OVERLAP ANALYSIS

WITH daily_startup_loader_template:

PARTIAL OVERLAP, VALID SEPARATION

Project Startup Canon Template should define:

* stable Project identity;
* Project roots;
* architecture;
* owner boxes;
* public contracts;
* domain invariants;
* validation profile;
* durable ownership;
* Project-specific do-not-regress rules.

Daily Startup Loader Template should define:

* what is loaded for one working session;
* current task intake;
* current source and logs;
* missing-context behavior;
* Fast Path versus Routed Work Path;
* session handoff behavior.

Task-specific data must remain in the daily loader, not the Project profile. This separation was already identified during Prompt 006.

WITH project_overlay_selector:

PARTIAL OVERLAP, FINAL RELATIONSHIP PROVISIONAL

Recommended separation:

project_startup_canon_template:
Creates or updates a Project profile draft.

project_overlay_selector:
Selects the correct existing Project overlay for the current session.

The current `project_overlay_selector` contains old paths and workflows and has not yet been individually audited, so its final relationship remains provisional.

WITH project_specific_prompt_generalization:

MANDATORY COMPANION RELATIONSHIP

The template must prevent foreign Project facts from contaminating reusable prompt canon.

WITH prompt_canon_reconciliation_protocol:

MANDATORY COMPANION RELATIONSHIP

It must decide whether the correct action is create, update, select, link, or preserve as reference.

WITH prompt_audit_canon:

MANDATORY REVIEW RELATIONSHIP

A generated or updated profile must be audited before active promotion.

WITH prompt_identity_code_registry_canon:

MANDATORY WHEN REGISTERING

Every routed active prompt requires stable identity.

WITH box_architecture_canon:

OWNER-TO-PROJECT-FACT RELATIONSHIP

Box Architecture owns generic boundary laws.

The generated Project profile records Project-specific box facts.

WITH project_tool_boundary_canon:

MANDATORY OWNER RELATIONSHIP

The generated Project profile must resolve Tool, Active Project, Project Support, and transient roles.

WITH Brick Wall:

IMPLEMENTATION AUTHORITY OWNER

A Project profile provides Project context.

It never authorizes coding, patching, release, validation claims, or freeze.

WITH Class 08 and Class 09:

CONDITIONAL ENGINEERING OWNER RELATIONSHIP

The Project profile records the selected Project’s technology and validation profile.

It does not reproduce generic engineering canons.

DISSONANT LOGIC FOUND:

YES

NEW PROMPT REQUIRED:

NO

NEW PROJECT PROFILE ENGINE REQUIRED:

NO

NEW SCHEMA REQUIRED:

NO

The current prompt can be repaired through consolidation and clearer ownership.

RECOMMENDED CORRECTED STRUCTURE

1. Canonical identity
2. Purpose
3. Authoring-template declaration
4. Non-execution rule
5. When to use
6. When not to use
7. Create/update/select/reference decision
8. Required owner prompts
9. Stable mandatory variables
10. Conditional variables
11. Tool-versus-Project roles
12. Authority hierarchy
13. Project architecture and owner-box fields
14. Project-specific public contracts
15. Domain and pipeline invariants
16. Technology and runtime profile
17. GUI profile, when applicable
18. Validation profile
19. Durable artifact and evidence owners
20. Project-specific do-not-regress rules
21. Unresolved-variable gate
22. Draft output contract
23. Review and promotion gate
24. Legacy alias information
25. Version history

MANDATORY NON-EXECUTION RULE

The corrected prompt should state:

“This prompt creates or updates a draft Project Startup Canon. It does not start the current session, select the current Project, authorize implementation, modify source, validate a real Project, produce a patch, deliver a ZIP, write Error Memory, or write freeze memory.”

RECOMMENDED ROUTING

WHEN TO LOAD:

* create a Project startup canon;
* create a Project profile;
* define stable Project-specific AI rules;
* update an existing Project startup profile;
* separate stable Project facts from a daily loader;
* establish Project-specific architecture and validation context.

WHEN NOT TO LOAD:

* normal daily startup;
* current KANDA startup pack loading;
* current Project selection;
* current task intake;
* code implementation;
* patch delivery;
* freeze preparation;
* handoff generation;
* generic software architecture advice.

REQUIRED COMPANIONS:

* ai_prompt_request_canon;
* prompt_navigation_index;
* prompt_router;
* prompt_canon_reconciliation_protocol;
* prompt_audit_canon;
* project_specific_prompt_generalization;
* prompt_identity_code_registry_canon;
* prompt_insertion_and_router_registration_protocol;
* relevant Class 01 folder card;
* existing Project profiles and overlays;
* project_tool_boundary_canon;
* box_architecture_canon;
* Brick Wall when implementation is subsequently proposed.

CONDITIONAL COMPANIONS:

* architecture_review_project_card_machine_canon when target-card workflows apply;
* kanda_box_shielding_canon when the Project profile defines a meaningful protected milestone;
* Class 08 and Class 09 owners for technology-specific validation profiles;
* bundle_gated_development_workflow if an installable prompt-library update is created;
* startup-delivery maintenance canon only when first_prompt_files or generated startup delivery will change.

SMALLEST SAFE FUTURE CORRECTION PLAN

Do not implement now.

After the complete prompt-library audit:

Phase 1:
Confirm the canonical Project-profile and overlay ownership matrix.

Phase 2:
Choose the canonical ID:

project_startup_canon_template

Phase 3:
Preserve the legacy ID as a migration alias only:

0000_1_0_project_startup_canon_template

Phase 4:
Rewrite the canonical source as a non-executing authoring template.

Phase 5:
Remove task-specific session fields.

Phase 6:
Add Tool-versus-Project and ownership variables.

Phase 7:
Add the draft output contract and unresolved-variable gate.

Phase 8:
Modernize canonical metadata.

Phase 9:
Assign a unique KPR-01 code after inspecting the complete registry.

Phase 10:
Narrow routing aliases.

Phase 11:
Migrate legacy application groups, stacks, profiles, and metadata.

Phase 12:
Make the application copy generated from or resolved to the canonical source.

Phase 13:
Create a focused semantic validator.

Phase 14:
Validate route determinism, source ownership, placeholder behavior, and negative cases.

Phase 15:
Promote only after human review and user-local validation.

REQUIRED VALIDATION AFTER FUTURE CORRECTION

Identity and source ownership:

* One canonical source exists.
* Canonical prompt ID remains stable.
* Legacy ID is an alias only.
* No independently editable application source remains.
* Runtime copy matches canonical source when a runtime copy is required.
* Prompt code is unique.
* Prompt code matches Class 01.
* Version is synchronized.
* Status is synchronized.
* Canonical path is synchronized.
* Owner box is explicit.
* Generated output type is explicit.

Template behavior:

* Prompt declares itself an authoring template.
* Prompt does not execute startup.
* Prompt does not select an Active Project.
* Prompt does not authorize implementation.
* Prompt does not produce a default patch or ZIP.
* Prompt does not validate a real Project.
* Prompt does not write freeze or Error Memory.
* Generated profile remains draft-only.
* Human promotion remains explicit.
* Mandatory unresolved variables block promotion.

Responsibility separation:

* Stable Project profile contains no current task description.
* Stable Project profile contains no task slug.
* Stable Project profile contains no current log list.
* Stable Project profile contains no current source-file subset.
* Daily loader retains current task/session ownership.
* Handoff retains continuation context ownership.
* Brick Wall retains implementation authorization.
* Class 08 and 09 retain generic engineering rules.
* Freeze owner retains freeze behavior.
* Class 07 retains authoring and registration workflow.

Tool-versus-Project:

* Tool root is distinguishable from Active Project root.
* Active Project Support root is explicit when applicable.
* Transient garbage root is explicit when applicable.
* Self-hosting physical path equality does not collapse identity.
* Nested Project Support is rejected.
* Generated support state does not become source truth.
* Wrong-root output is rejected.

Project profile quality:

* Project identity is present.
* Project purpose is present.
* Source authority is present.
* Owner boxes are present when known.
* Public contracts are present when known.
* Domain invariants are explicit.
* Technology profile is explicit.
* Validation profile is explicit.
* GUI fields are conditional.
* Durable output owners are explicit.
* Project-specific do-not-regress rules are explicit.
* Unknown values remain visibly unresolved.

Prompt authoring:

* Existing profiles and overlays are inspected.
* Create-versus-update-versus-select decision is explicit.
* Class 07 companions are required.
* Metadata is generated or updated.
* Routing is generated or updated only when needed.
* Prompt-code registry is checked.
* Folder placement is validated.
* No duplicate Project canon is created.
* No foreign Project facts contaminate reusable canon.

Routing:

* Broad aliases are removed.
* Generic “startup” does not select this prompt.
* Generic “project” does not select this prompt.
* Exact Project-profile authoring requests select it.
* Human and machine routing agree.
* Legacy aliases resolve deterministically.
* The old ID is absent from active stacks.
* The template is absent from normal daily-start groups.
* The template is absent from default high-risk engineering groups.

Encoding:

* UTF-8 without BOM remains valid.
* No prohibited control byte exists.
* Line endings remain consistent.
* Placeholder syntax remains valid.

Negative tests:

* Reject a profile containing TASK_DESCRIPTION as stable canon.
* Reject a profile containing TASK_SLUG as stable canon.
* Reject a profile with invented roots.
* Reject a profile with unresolved mandatory placeholders promoted as active.
* Reject a profile that collapses Tool and Project.
* Reject a profile that uses one generic output folder for all ownership.
* Reject a profile that reproduces incomplete Box Logic as the full owner.
* Reject a profile that defines generic Python or GUI rules as Project truth.
* Reject a profile that directly freezes or canonizes itself.
* Reject two independently editable active source copies.
* Reject broad aliases such as boot, session, startup, and project.
* Reject registration without Class 07 authoring owners.
* Reject exact explanatory-phrase validation.
* Reject permanent exact-version equality.

ERROR MEMORY APPLICATION

Relevant compact lessons:

lesson-brick-wall-q01-validator-exact-phrase-count-assumption-v1

Application:

Validate Project-profile semantics and ownership rather than exact sentence counts.

lesson-brick-wall-q01-validator-forward-version-rigidity-v1

Application:

Do not make one exact future template version a permanent compatibility gate.

lesson-brick-wall-q02-validator-forward-contract-rigidity-v1

Application:

Allow future compatible strengthening of the Project-profile contract without retaining obsolete wording.

lesson-brick-wall-focused-validator-task-route-key-assumption-v1

Application:

Inspect the actual current routing and group schemas before asserting migration behavior.

FULL ERROR MEMORY ZIP NEEDED:

NO

Reason:

The compact lessons and exact current source are sufficient for this read-only audit.

BRICK WALL STATUS

Project slug:
kanda_reasoner

Task:
Audit Prompt 012 individually

Current phase:
Read-only canonical audit completed

Primary box:
Prompt Library / Session Start and Navigation

Authoring-method owner:
Prompt Authoring and Audit

Generated-output role:
Project-specific overlay/profile

External owner boxes inspected:

* Context Routing;
* Prompt Authoring and Audit;
* Box Architecture;
* Tool-versus-Project;
* Brick Wall Governance;
* Python Engineering;
* Freeze Workflow.

Tool root:
E:\kanda_reasoner

Active Project root:
E:\kanda_reasoner

Active Project support root:
E:\kanda_reasoner_show_project_to_AI

Transient garbage root:
E:\kanda_reasoner_delete_after_daily_work

Same physical Tool/Project root:
YES

Selected target:
project_startup_canon_template.md

Current source fingerprint:
4b6bd936ae3ebb58403fac36118127c455879e222c0c3649502ff78f7c3ad391

Legacy application fingerprint:
4a32868035903937eb5cdac019779c01fd5d654c78992ee1a531b9b6211d59c6

Verified problem status:
COMPLETE

Admission decision:
KEEP_UPDATE_REFRAME_AND_CONSOLIDATE

Unique capability:
YES

Compact Error Memory:
LOADED

Full Error Memory:
NOT REQUIRED

Exact-source inspection:
COMPLETE

Canonical metadata inspection:
COMPLETE

Legacy source and metadata inspection:
COMPLETE

Focused validator:
MISSING

Encoding:
PASS

Tool/Project boundary:
FAIL IN TARGET

Reason:

The template has only PROJECT_ROOT and cannot distinguish Tool, Active Project, Project Support, and transient ownership.

Box Boundary:
FAIL IN TARGET

Reason:

The prompt embeds a weak generic Box implementation and generic Python, GUI, delivery, and freeze rules.

NO-LEAK:
FAIL IN TARGET DESIGN

Reason:

Dual active source ownership, task-state leakage into durable profile fields, ambiguous output ownership, and generated-profile authority are unresolved.

Audit-operation NO-LEAK:
COMPLETE

No source, metadata, routing, application copy, validation artifact, or Project profile was written.

MCard:
N/A for this read-only audit

MCard may become conditional in generated profiles that govern selected-target workflows.

Shield:
LIKELY REQUIRED FOR FUTURE CORRECTION

Recommended protected invariants:

* one canonical Project-profile template source;
* stable Project facts separated from current task state;
* Tool/Project identity preserved;
* unresolved variables cannot become active truth;
* generated draft cannot promote itself;
* Project profile cannot authorize implementation;
* generic canons remain with their canonical owners;
* legacy ID remains alias-only.

Regression plan:
PROPOSED

Validation plan:
PROPOSED

May begin coding:
NO

May write prompt source:
NO

May modify metadata:
NO

May consolidate legacy copy:
NO

May assign prompt code:
NO

May update routing:
NO

May modify legacy groups or profiles:
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

Verified current problems:

* dual active source ownership;
* task-specific leakage into durable Project profile;
* incomplete root and ownership model;
* outdated truth hierarchy;
* weak parallel Box implementation;
* missing authoring governance;
* incomplete metadata;
* broad routing aliases;
* legacy stack registration;
* no focused validator.

Admission decision:

KEEP_UPDATE_REFRAME_AND_CONSOLIDATE

Q02-Q04:
COMPLETE

Relevant compact Error Memory lessons reviewed.

Q05:
COMPLETE

Canonical source, canonical metadata, legacy source, legacy metadata, routing, group/profile references, folder card, prompt-authoring owners, Box owner, and Tool-versus-Project owner were inspected.

Q06:
FAIL IN TARGET

Tool and Active Project identities are not separately represented.

Q07-Q10:
FAIL IN TARGET

Output ownership, Project Support, transient state, source/generated authority, and cross-owner responsibilities are incomplete.

Q11-Q18:
N/A

No current MCard transaction, source mutation, Preview, Shadow, asynchronous operation, or target switch occurred.

Q19-Q25:
N/A

No Qt, runtime, property-based, mutation-testing, or GUI execution occurred.

Q26:
N/A

No ZIP was built or delivered.

Q27:
PASS

Encoding, control bytes, line endings, and Markdown fences passed.

Q28-Q30:
N/A

No exception, execution, freeze write, or human confirmation operation occurred.

Q31:
IN PROGRESS

A future changed-file-to-validator map has been proposed, but no file was changed.

Q32:
COMPLETE

Canonical source, canonical metadata, legacy source, and legacy metadata fingerprints were recorded.

Q33-Q36:
N/A

No AI-model evidence, optimization, benchmark, or Python implementation work occurred.

Q37:
FAIL

Two active source identities exist, and the target mixes responsibilities owned by other canons.

Q38:
COMPLETE

Current source archive, current prompt inventory, current startup handoff, and exact comparison owners were used.

Q39:
PASS

No new Project-profile engine, schema system, routing engine, or prompt is recommended.

Q40:
N/A

No governed release occurred.

FINAL AUDIT RECOMMENDATION

RECOMMENDED CLASSIFICATION:
PROJECT STARTUP CANON AUTHORING SPECIALIST

GENERATED OUTPUT CLASSIFICATION:
PROJECT OVERLAY

RECOMMENDED ACTION:
KEEP, UPDATE, REFRAME, AND CONSOLIDATE

DELETE:
NO

DEPRECATE:
NO

CURRENT STATUS:
blocked_by_conflict

LIKELY FINAL STATUS:
active

CANONICAL ID:
project_startup_canon_template

LEGACY ID:
0000_1_0_project_startup_canon_template

LEGACY ID DISPOSITION:
MIGRATION ALIAS ONLY

CURRENT LOAD TYPE:
on_request

RECOMMENDED LOAD TYPE:
on_request

NAVIGATION EFFECT:
NARROW TO PROJECT-PROFILE AUTHORING REQUESTS

LEGACY STACK EFFECT:
REMOVE FROM NORMAL DAILY START AND HIGH-RISK DEFAULT STACKS

PROMPT CODE:
ASSIGN A UNIQUE KPR-01 CODE AFTER COMPLETE REGISTRY AUDIT

VALIDATOR EFFECT:
CREATE A FOCUSED SEMANTIC AND NEGATIVE-CASE VALIDATOR

FINAL DECISION

Keep this prompt because it has a legitimate unique function.

Rewrite it as a non-executing authoring template for stable Project-specific profiles.

Remove task-specific session fields, generic engineering instructions, weak parallel architecture rules, and incomplete freeze behavior.

Consolidate the legacy application copy under one canonical source and preserve the old ID only as a migration alias.

Do not modify it until the remaining prompt audits establish the final owner matrix and dependency-ordered correction roadmap.
