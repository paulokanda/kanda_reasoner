O décimo prompt permanece parte obrigatória do startup como 08_handoff_at_end_of_work.md, embora o inventário não consiga classificá-lo corretamente por falta de metadados padronizados. Ele tem uma função única e deve ser mantido: detectar encerramento de sessão e impedir que o contexto seja perdido. Contudo, o handoff produzido não pode substituir o startup e o segundo upload estruturado da próxima conversa.

PROMPT AUDIT REPORT 010

AUDIT_ID:
A010-20260714-REVIEW

PROMPT_FILENAME:
handoff_at_end_of_work.md

CANONICAL_ID:
handoff_at_end_of_work

CANONICAL_LIBRARY_PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md

CURRENT SOURCE SHA-256:
71821c191da66c2f68f8e8a1b77885daea07c0ce57ebea02d5894e4d4fba2e65

CURRENT METADATA SHA-256:
af1538ec27b1f7a633b426a6db38db63f033cfd585f033f4aa0f14df2c5511b1

SOURCE SIZE:
6,538 bytes

SOURCE LENGTH:
236 lines

APPROXIMATE WORD COUNT:
994 words

DECLARED VERSION:
1.0

SOURCE STATUS:
always-startup session-closure guardrail

STARTUP METADATA:

startup_kernel_include:
true

startup_load_mode:
always_startup

startup_generated_filename:
08_handoff_at_end_of_work.md

GENERATED STARTUP SOURCE HASH:
MATCHES CURRENT CANONICAL SOURCE

STANDARD PROMPT METADATA:
INCOMPLETE

PROMPT CODE:
MISSING

FOCUSED VALIDATOR IN CURRENT SOURCE TREE:
NOT FOUND

HISTORICAL RELEASE VALIDATION:
FOUND OUTSIDE CURRENT SOURCE TREE

AUDIT MODE:
Read-only, one-prompt audit

SOURCE MODIFIED:
NO

METADATA MODIFIED:
NO

STARTUP DELIVERY MODIFIED:
NO

PATCH CREATED:
NO

NEXT PROMPT OPENED FOR AUDIT:
NO

OVERALL VERDICT

This prompt has a real, distinct, and important responsibility.

It should not be:

* deleted;
* deprecated;
* retired;
* replaced by a generic handoff template;
* removed from always-startup context.

Its unique responsibility is:

Detect a genuine end-of-work or pause request during active governed Project work, stop further implementation, and require an evidence-grounded continuity handoff.

However, the prompt currently does more than this.

It also defines:

* a full handoff schema;
* freeze-preparation instructions;
* freeze-intake metadata;
* startup-delivery filename rules;
* `KANDA_FREEZE_HINT.json` handling;
* partial Box reporting;
* partial validation reporting.

These detailed responsibilities overlap with Class 03 handoff templates, the freeze owner, Brick Wall, startup-delivery maintenance, and durable-artifact routing.

RECOMMENDED ACTION:

KEEP, UPDATE, AND NARROW

The prompt should remain an always-startup closure guardrail.

It should become a concise trigger-and-minimum-contract owner.

Detailed handoff structure should be supplied by one audited Class 03 handoff-template owner.

Detailed freeze data should be supplied by `freeze_code_intake_and_form_protocol`.

Detailed startup filenames should be obtained from the current startup manifest rather than permanently copied here.

RECOMMENDED CURRENT STATUS:

active

RECOMMENDED STATUS DURING FUTURE CORRECTION:

in_review

RECOMMENDED FINAL STATUS:

active

DECISION GATE:

HUMAN_REQUIRED

UNIQUE CAPABILITY ASSESSMENT

UNIQUE CAPABILITY EXISTS:

YES

ONE-SENTENCE RESPONSIBILITY:

When active governed Project work is paused or ended, enter closure mode, prohibit new implementation, and produce a factual continuity handoff that identifies the exact next safe action without claiming unverified installation, validation, freeze, or source state.

SINGLE RESPONSIBILITY PASS:

PARTIAL FAIL

The trigger and closure behavior is focused.

The full template, freeze schema, startup filename list, and sidecar behavior exceed its proper responsibility.

POSITIVE FINDINGS

P010-P001

TITLE:
Mandatory closure protection

RESULT:
PASS

The prompt correctly prevents a long governed session from ending with only:

* a short farewell;
* a vague summary;
* no continuation instructions;
* no record of validation or unfinished work.

P010-P002

TITLE:
Implementation stops when closure is requested

RESULT:
PASS

The prompt correctly states that normal implementation should stop after a genuine closure trigger.

It also prohibits starting:

* new code;
* new patches;
* new tests;
* new freeze operations;

unless the user explicitly requested completion of that work before ending.

This is an important context-safety rule.

P010-P003

TITLE:
Validation honesty

RESULT:
PASS

The prompt correctly requires the AI to say when:

* validation is unknown;
* a patch was prepared but not installed;
* a patch was installed but not validated;
* evidence is missing.

It explicitly prohibits invented validation evidence.

P010-P004

TITLE:
Concrete operational handoff

RESULT:
PASS

The prompt appropriately requests:

* Project identity;
* paths;
* boxes;
* completed work;
* changed files;
* unresolved work;
* risks;
* exact next safe action;
* do-not-do instructions.

P010-P005

TITLE:
Casual-goodbye exception

RESULT:
PASS

The prompt distinguishes:

* an active Project session ending;
* a casual non-Project goodbye.

This avoids requiring a large engineering handoff after unrelated conversation.

P010-P006

TITLE:
Current startup filenames are presently correct

RESULT:
PASS FOR CURRENT SOURCE

The currently listed active startup names are:

* tell_AI_read_before_all.md
* first_prompts_to_ai.zip
* prompt_library.zip
* zz_read_only_if_modifying_startup_delivery.md, when maintenance applies

These names match the current startup-delivery contract.

P010-P007

TITLE:
Canonical source and generated startup copy are synchronized

RESULT:
PASS

The generated startup file:

08_handoff_at_end_of_work.md

contains:

* the current canonical source path;
* the current canonical source SHA-256;
* the generated-file warning;
* the current prompt content.

P010-P008

TITLE:
Encoding and structural integrity

RESULT:
PASS

The canonical source has:

* valid UTF-8;
* no UTF-8 BOM;
* LF-only line endings;
* no prohibited control bytes;
* balanced Markdown fences.

Brick Wall Q27 passes.

CRITICAL AND HIGH-SEVERITY FINDINGS

FINDING A010-F001

TITLE:
Freeze preparation is directed toward the final frozen-memory folder

SEVERITY:
CRITICAL

CURRENT TEXT:

When a validated feature is not yet frozen, the handoff says the next safe action is to prepare a Freeze Feature After Update entry under:

<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory

PROBLEM:

`frozen_features_memory` is the final governed frozen-memory destination.

The AI must not directly prepare or write a new entry there as the first freeze step.

The protected workflow requires:

1. Feature-specific freeze data.
2. Correct Project Support root.
3. Freeze intake or current matching freeze hint.
4. Read-only Preview.
5. Successful user-local validation.
6. Explicit human Confirm and Write.
7. Final local frozen-memory write.
8. Startup freeze-context refresh.

The current wording can be interpreted as authorizing direct preparation inside the final frozen-memory owner.

CORRECTION:

Replace with:

“Feature appears eligible for freeze preparation but is not frozen. Next safe action: route feature-specific data through `freeze_code_intake_and_form_protocol`, inspect the read-only Preview, and perform Confirm and Write only after successful user-local validation and explicit human confirmation.”

Do not name `frozen_features_memory` as the initial preparation location.

FINDING A010-F002

TITLE:
The sidecar rule allows the possibility that KANDA_FREEZE_HINT.json is installed as Project source

SEVERITY:
CRITICAL

CURRENT TEXT:

If a patch ZIP was delivered, state whether `KANDA_FREEZE_HINT.json` is:

* only delivery metadata; or
* also an installed file.

PROBLEM:

The current patch contract does not allow the freeze sidecar to become Active Project payload.

The sidecar must:

* exist once at patch ZIP root;
* not be duplicated inside install payload;
* not be installed into Active Project source;
* be staged into the selected Project Support freeze-intake owner when applicable.

The phrase “or also an installed file” normalizes an invalid delivery possibility.

CORRECTION:

Replace with:

“If a patch ZIP was delivered, state whether root-level `KANDA_FREEZE_HINT.json` was present, validated, kept outside the install payload, and staged into the correct Project Support freeze-intake owner. If it was installed into Active Project source, report a contract violation.”

FINDING A010-F003

TITLE:
The handoff is not explicitly classified as continuity evidence rather than source truth

SEVERITY:
CRITICAL

The prompt says the handoff should be self-contained enough for a new AI to continue without reading the whole chat.

PROBLEM:

A new AI may interpret the handoff as sufficient authority and skip:

* current startup loading;
* compact Error Memory;
* structured second-upload handoff;
* exact current source;
* current validation state;
* active freeze context;
* source fingerprints;
* current Box and Tool/Project verification.

A handoff is a continuity artifact.

It is not:

* current source truth;
* validation evidence by itself;
* canonical governance;
* freeze memory;
* a substitute for startup;
* a substitute for PROJECT READY CHECK.

CORRECTION:

Add an explicit authority statement:

“This handoff is continuity evidence only. It does not replace the next chat’s startup load, second-upload PROJECT READY CHECK, compact Error Memory, exact-source inspection, current validation evidence, or active freeze context.”

The phrase “self-contained” should mean:

The next AI knows what evidence to load and what safe action to take.

It must not mean:

The next AI may implement directly from the handoff.

FINDING A010-F004

TITLE:
Detailed handoff schema duplicates Class 03 handoff owners

SEVERITY:
HIGH

CURRENT PROMPT DEFINES:

* 17 mandatory content fields;
* a complete textual template;
* patch status;
* validation status;
* freeze state;
* stale names;
* file protection;
* risk reporting;
* freeze-intake metadata.

OTHER ACTIVE HANDOFF PROMPTS INCLUDE:

* current_workflow_handoff_template
* workflow_handoff_template
* end_of_chat_governance_update_template

PROBLEM:

There is no clear division between:

* closure-trigger owner;
* handoff-schema owner;
* Project-specific handoff owner;
* reusable handoff template;
* governance-update owner.

This creates competing templates.

CORRECTION:

Recommended ownership:

`handoff_at_end_of_work`:

* trigger detection;
* closure-mode entry;
* no-new-work rule;
* minimum factual continuity contract;
* owner-prompt routing.

One audited Class 03 prompt:

* detailed reusable handoff schema.

Project-specific overlay or handoff exporter:

* Project-specific fields and durable generated package.

Do not delete the current detailed schema until the Class 03 handoff prompts have been audited.

FINDING A010-F005

TITLE:
Trigger list contains ambiguous action phrases

SEVERITY:
HIGH

AMBIGUOUS EXAMPLES:

* finish this section
* chat is huge
* wrap this up
* end of day

PROBLEM:

“Finish this section” may mean:

Complete the current work before stopping.

The current prompt may instead immediately stop implementation.

“Chat is huge” may be:

* an observation;
* a request for a handoff;
* a request to move chats;
* a complaint without closure intent.

CORRECTION:

Separate hard triggers from contextual triggers.

Hard closure triggers:

* create handoff
* handoff for next time
* pause here
* stop for today
* we continue later
* let’s stop now

Contextual triggers requiring semantic confirmation:

* finish this section
* wrap this up
* end of day
* chat is huge

Rule:

Do not ask a follow-up when the intent is already clear.

When the phrase contains an explicit request to complete work first, finish only the already-authorized bounded step, then enter closure mode.

Do not start unrelated new work.

FINDING A010-F006

TITLE:
Required identity fields are incomplete for current Tool-versus-Project logic

SEVERITY:
HIGH

CURRENT TEMPLATE INCLUDES:

* Project name;
* Project root;
* important boxes.

MISSING:

* KANDA Tool root;
* Active Project root;
* Active Project support root;
* transient garbage root;
* same physical Tool/Project root;
* primary owner box;
* external boxes touched;
* mutable-state owner, when relevant;
* generated versus source artifacts;
* NO-LEAK status.

PROBLEM:

In self-hosting, one physical root may conceal different logical owners.

A continuation handoff without these distinctions may cause:

* Tool logic to be edited as Project output;
* Project support to be written under source;
* transient artifacts to become authority;
* wrong-box continuation.

CORRECTION:

Add these fields conditionally:

Tool root:
Active Project root:
Active Project support root:
Transient garbage root:
Same physical root:
Primary owner box:
External boxes touched:
NO-LEAK status:

Do not require irrelevant fields for a simple non-implementation handoff.

FINDING A010-F007

TITLE:
Patch and validation states are not granular enough

SEVERITY:
HIGH

CURRENT TEMPLATE USES BROAD CATEGORIES SUCH AS:

* installed patches;
* validation evidence;
* frozen behavior.

PROBLEM:

These terms can collapse materially different states:

* planned;
* generated;
* delivered;
* staged;
* extracted;
* installed;
* sandbox validated;
* locally validated;
* freeze-ready;
* Previewed;
* Confirmed and Written;
* frozen;
* superseded.

CORRECTION:

Require an explicit status per patch or feature:

Patch status:

* PLANNED
* BUILT
* DELIVERED
* STAGED
* INSTALLED
* INSTALL_FAILED
* SUPERSEDED

Validation status:

* NOT_RUN
* SANDBOX_ONLY
* USER_LOCAL_PENDING
* USER_LOCAL_PASSED
* USER_LOCAL_FAILED

Freeze status:

* NOT_APPLICABLE
* NOT_READY
* FREEZE_READY
* PREVIEWED
* FROZEN
* SUPERSEDED

Evidence should include:

* command or validator;
* expected marker;
* observed marker;
* evidence path;
* provenance;
* whether it was verified in the current session.

FINDING A010-F008

TITLE:
No durable-placement rule for the handoff itself

SEVERITY:
HIGH

CURRENT BEHAVIOR:

The prompt instructs the AI to output a handoff in the chat.

PROBLEM:

A chat-only handoff may be lost or omitted from the next structured Project upload.

The Project already has specialized handoff-generation and second-upload owners.

A handoff that must survive cleanup should not depend only on:

* chat history;
* transient daily-work;
* a copied text fragment.

CORRECTION:

Distinguish:

CHAT HANDOFF:
A human-readable continuity response in the conversation.

DURABLE PROJECT HANDOFF:
A generated Project-owned artifact under the specialized Project Support handoff/second-upload owner.

If the AI cannot write a durable artifact, it must say:

“Durable Project handoff artifact not created; this response is chat continuity evidence only.”

Do not create a second competing handoff authority.

FINDING A010-F009

TITLE:
No redaction or export-safety gate

SEVERITY:
CRITICAL

The prompt encourages exact paths, filenames, logs, patches, risks, and open questions.

PROBLEM:

A handoff may later be:

* uploaded to another AI;
* stored in second_prompt_files;
* copied into Project Support;
* shared with collaborators.

It may accidentally include:

* secrets;
* credentials;
* tokens;
* private user-home paths;
* patient information;
* unrelated personal data;
* confidential source snippets;
* raw exception payloads.

CORRECTION:

Add:

“Before output or durable persistence, remove credentials, tokens, secrets, unnecessary private paths, patient data, and unrelated personal information. Preserve the smallest evidence needed for safe continuation.”

Project-relative paths should be preferred when absolute paths are not necessary.

FINDING A010-F010

TITLE:
Freeze-intake field list duplicates the freeze owner schema

SEVERITY:
HIGH

CURRENT PROMPT DEFINES THESE FIELDS:

* latest_patch_name
* feature_title
* feature_id
* primary_box
* box_type
* installed_payload_files
* generated_files
* protected_paths
* validation_evidence_available
* validation_evidence_summary
* freeze_status
* next_freeze_action

PROBLEM:

The exact freeze form, freeze hint, and freeze-intake schemas are owned by the freeze protocol and application.

The handoff field list can drift from the real receiver.

CORRECTION:

The handoff should include a compact freeze summary, not redefine the receiver schema.

Recommended fields:

Freeze applicability:
Freeze status:
Feature ID:
Current validated feature:
Validation evidence location:
Current freeze-intake owner:
Next governed freeze action:

When actual receiver-ready data is needed, load:

freeze_code_intake_and_form_protocol

FINDING A010-F011

TITLE:
A frozen-state claim is not tied to verified current frozen memory

SEVERITY:
HIGH

CURRENT TEXT:

“If a feature was frozen and validation passed, say: Feature is frozen and validation evidence was accepted.”

PROBLEM:

The handoff may repeat an earlier conversational claim without proving:

* the frozen entry exists;
* the entry belongs to the current Project;
* the feature ID matches;
* validation evidence is current;
* the freeze is not superseded;
* startup freeze context was refreshed.

CORRECTION:

Use:

“Frozen status verified from current Project frozen memory: YES / NO.”

Only state `FROZEN` when the current entry or refreshed active freeze context proves it.

Otherwise state:

“Freeze was reported but not independently verified in the current handoff evidence.”

FINDING A010-F012

TITLE:
Hardcoded startup filenames may become stale inside a non-maintenance prompt

SEVERITY:
MEDIUM

The current names are correct today.

However, the prompt manually repeats them.

PROBLEM:

A later governed startup rename could update the startup manifest and maintenance canon while leaving this always-loaded handoff prompt stale.

CORRECTION:

Use:

“When startup delivery changed, read the current startup-delivery manifest and maintenance canon, then report active and deprecated names.”

Do not permanently validate one filename list inside the handoff prompt.

The current names may remain as examples, not as an independent source of truth.

FINDING A010-F013

TITLE:
“Files not to modify next” can overstate authority

SEVERITY:
MEDIUM

PROBLEM:

A file may have been out of scope for the previous task but become the correct owner for the next task.

A handoff can incorrectly transform a temporary scope decision into permanent protection.

CORRECTION:

Separate:

Protected or frozen paths:

* include authority and evidence.

Out-of-scope for the previous task:

* not automatically forbidden for future tasks.

Do not modify without re-routing:

* explain the owner prompt or gate required.

FINDING A010-F014

TITLE:
MCard and open transaction state are absent

SEVERITY:
HIGH WHEN ARCHITECTURE REVIEW APPLIES

For Architecture Review, refactor Workbench, or another selected-card workflow, a safe handoff must include:

* Active Project;
* selected target;
* source hash or freshness basis;
* lifecycle generation;
* current MCard state;
* active transaction;
* unresolved apply outcome;
* switch/eject blockers;
* stale-result risks;
* receipt or rollback status.

PROBLEM:

The next AI may switch target, eject state, or trust stale Planner/Workbench output while an operation is unresolved.

CORRECTION:

Add an MCard section only when applicable.

Do not load MCard details for unrelated handoffs.

FINDING A010-F015

TITLE:
Brick Wall state is not explicitly included

SEVERITY:
HIGH

The prompt asks for current decision state but does not require:

* current Brick Wall phase;
* Verified Problem decision;
* Error Memory status;
* exact-source status;
* pre-code authorization;
* changed-file-to-validator map;
* release eligibility;
* blocker state.

PROBLEM:

The next AI may assume coding is authorized merely because a handoff says what to do next.

CORRECTION:

For governed work, include a concise Brick Wall summary:

Verified Problem decision:
Relevant Error Memory:
Exact-source status:
Pre-code authorization:
Current validation phase:
Release eligibility:
Freeze eligibility:
Current blocker:

Do not copy Q01-Q40 into the handoff prompt.

FINDING A010-F016

TITLE:
No standard machine-readable metadata or prompt code

SEVERITY:
HIGH

CURRENT PROMPT-SPECIFIC METADATA CONTAINS ONLY:

* startup_kernel_include;
* startup_load_mode;
* startup_generated_filename;
* prompt_id;
* startup_role;
* canonical_source.

MISSING:

* prompt_code;
* display_name;
* category;
* lifecycle status;
* version;
* owner_box;
* canonical_path in current standard form;
* updated_for;
* source_stage;
* when_to_load;
* when_not_to_load;
* required companions;
* do-not-regress rules;
* validator owner.

PROBLEM:

The inventory falls back to:

active_by_location

instead of obtaining a complete status and load type.

CORRECTION:

Modernize metadata after the full registry audit.

Preserve the startup fields, but add the standard prompt identity model.

Assign the next genuinely unused `KPR-01-xxx` code only after checking the complete registry.

FINDING A010-F017

TITLE:
No current focused semantic validator

SEVERITY:
CRITICAL

Exact current source inspection found no focused Python validator for:

handoff_at_end_of_work

Historical validation evidence exists, but it checks exact text such as:

* `lets take a break`
* `complete contextualized handoff`
* `A short goodbye alone is a failure`

It also requires:

* exact load order 8;
* exact generated filename;
* exact historical startup names.

PROBLEM:

This protects wording and release position rather than behavior.

It does not test:

* false-positive casual goodbye;
* ambiguous trigger intent;
* no new implementation after closure;
* unverified validation claims;
* freeze-path safety;
* human Confirm and Write;
* handoff-as-non-authoritative evidence;
* redaction;
* MCard state;
* durable placement;
* next-chat startup requirement.

CORRECTION:

Create a focused semantic validator after correction.

Do not revive the historical exact-prose validator as the permanent contract.

FINDING A010-F018

TITLE:
Fixed startup load order 8 should not be a permanent behavioral contract

SEVERITY:
HIGH

The current source map and generated filename use position 8.

That is valid for the current release.

PROBLEM:

A later compatible startup prompt inserted earlier could change the numeric position without changing the handoff guardrail’s semantic role.

CORRECTION:

Validate:

* one canonical source entry;
* always-startup load mode;
* deterministic order;
* unique generated filename;
* inclusion in startup ZIP;
* presence before Project work begins.

Do not permanently require integer position 8 unless a separate public compatibility contract explicitly freezes that number.

OVERLAP AND OWNER MATRIX

handoff_at_end_of_work:

ALWAYS-STARTUP CLOSURE TRIGGER AND MINIMUM CONTINUITY CONTRACT OWNER

workflow_handoff_template:

LIKELY PROJECT-AGNOSTIC DETAILED HANDOFF TEMPLATE OWNER, PENDING ITS OWN AUDIT

current_workflow_handoff_template:

LEGACY OR PROJECT-SPECIFIC HANDOFF TEMPLATE CANDIDATE, PENDING ITS OWN AUDIT

handoff exporter and second_prompt_files:

DURABLE MACHINE-READABLE PROJECT HANDOFF PACKAGE OWNER

durable_document_artifact_routing_canon:

HANDOFF ARTIFACT LIFETIME AND PLACEMENT OWNER

Brick Wall:

CURRENT GOVERNED-WORK STATUS OWNER

freeze_code_intake_and_form_protocol:

FREEZE DATA AND CONFIRMATION OWNER

project_tool_boundary_canon:

TOOL, PROJECT, SUPPORT, AND TRANSIENT ROOT OWNER

architecture_review_project_card_machine_canon:

MCARD CONTINUITY OWNER WHEN APPLICABLE

Error Memory:

PREVENTION AND REGRESSION LESSON OWNER

DISSONANT LOGIC FOUND:

YES

NEW PROMPT REQUIRED:

NO

NEW HANDOFF ENGINE REQUIRED:

NO

NEW SCHEMA REQUIRED:

NO

The current system already has the required components.

RECOMMENDED CORRECTED STRUCTURE

1. Identity and role
2. Purpose
3. Hard closure triggers
4. Contextual closure triggers
5. Active-Project detection
6. Closure-mode behavior
7. Minimum handoff contract
8. Evidence and status honesty
9. Tool-versus-Project summary
10. Brick Wall summary
11. MCard summary when applicable
12. Durable versus chat handoff distinction
13. Redaction and export safety
14. Freeze-owner bridge
15. Detailed template owner bridge
16. Next-chat startup requirement
17. Scope exclusions
18. Version history

RECOMMENDED MINIMUM HANDOFF CONTRACT

Session status:
Project:
Tool root:
Active Project root:
Project Support root:
Same physical root:
Primary owner box:
Current task:
Completed:
Not completed:
Files changed:
Artifacts generated:
Patch status:
Validation status:
Freeze status:
Relevant Error Memory:
Current Brick Wall blocker:
MCard state, if applicable:
Next safe action:
Do not do next:
Evidence provenance:
Durable handoff created:
Redaction status:

Detailed optional fields should come from the selected Class 03 template or Project overlay.

RECOMMENDED SCOPE EXCLUSIONS

The corrected prompt should state:

This prompt does not:

* replace startup;
* replace PROJECT READY CHECK;
* replace exact-source inspection;
* define the full handoff schema;
* define freeze-form fields;
* define freeze-hint fields;
* write frozen memory;
* authorize Confirm and Write;
* define patch ZIP structure;
* claim local validation;
* own MCard implementation;
* own Error Memory schema;
* make chat handoff canonical source truth.

SMALLEST SAFE FUTURE CORRECTION PLAN

Do not implement now.

After the complete prompt-library audit:

Phase 1:
Audit all Class 03 handoff templates.

Phase 2:
Choose one detailed reusable handoff-schema owner.

Phase 3:
Define the relationship between:

* chat continuity handoff;
* durable Project handoff;
* generated second-upload handoff package.

Phase 4:
Reduce this prompt to the closure trigger and minimum continuity contract.

Phase 5:
Remove direct freeze-path and sidecar-schema behavior.

Phase 6:
Modernize metadata and assign a prompt code.

Phase 7:
Repair startup source-map validation.

Phase 8:
Add focused semantic and negative tests.

Phase 9:
Regenerate startup delivery through the startup-maintenance canon.

Phase 10:
Run sandbox and user-local validation.

Phase 11:
Freeze only through explicit human Preview and Confirm and Write.

REQUIRED VALIDATION AFTER FUTURE CORRECTION

Identity and startup:

1. Prompt ID remains stable.
2. Prompt code is unique.
3. KPR code matches Class 01.
4. Status is active.
5. Load mode remains always_startup.
6. Version is synchronized.
7. Owner box is synchronized.
8. Canonical path is correct.
9. Generated startup copy derives from canonical source.
10. Startup ZIP contains exactly one generated copy.
11. Startup load check remains complete.
12. Numeric load position is not treated as permanent unless explicitly public.

Trigger behavior:

13. Explicit closure requests trigger handoff.
14. Casual goodbye without active Project does not trigger full handoff.
15. Ambiguous contextual phrases are interpreted by intent.
16. “Finish this section” does not prematurely stop an explicitly authorized bounded completion.
17. No unrelated new implementation begins after closure.
18. Repeated closure triggers do not generate conflicting handoffs.
19. “Create handoff” works even without a farewell phrase.
20. A huge-context warning produces safe continuity behavior.

Evidence honesty:

21. Planned is not delivered.
22. Delivered is not installed.
23. Installed is not validated.
24. Sandbox validation is not user-local validation.
25. Freeze-ready is not frozen.
26. Previewed is not Confirmed and Written.
27. Frozen status requires current evidence.
28. Unknown status is reported as unknown.
29. Exact evidence markers are recorded when available.
30. Evidence provenance is explicit.

Authority and continuation:

31. Handoff is labeled continuity evidence.
32. Handoff is not source truth.
33. Handoff is not validation evidence by itself.
34. Handoff is not freeze memory.
35. Handoff does not replace next-chat startup.
36. Handoff does not replace second-upload PROJECT READY CHECK.
37. Handoff does not authorize coding.
38. Next AI is directed to exact current source.
39. Current Error Memory status is included when relevant.
40. Current Brick Wall blocker is included.

Tool, Project, and Box:

41. Tool root is identified.
42. Active Project root is identified.
43. Project Support root is identified.
44. Transient garbage is identified when relevant.
45. Same-root self-hosting is represented correctly.
46. Primary owner box is identified.
47. External box touches are identified.
48. Generated artifacts are separated from source.
49. Wrong-root continuation is rejected.
50. Out-of-scope files are not converted into permanent forbidden files.

MCard:

51. Active target is recorded when applicable.
52. Lifecycle generation is recorded when applicable.
53. Open transaction is recorded.
54. Unresolved apply outcome blocks switching.
55. Stale async result risk is recorded.
56. Receipt or rollback state is recorded.
57. Eject is not recommended while blocked.

Freeze:

58. No direct preparation under frozen_features_memory.
59. Preview remains read-only.
60. Confirm and Write remains explicit.
61. Freeze status is verified from current evidence.
62. `KANDA_FREEZE_HINT.json` is not installed into Active Project source.
63. Sidecar is not duplicated in payload.
64. Current freeze-intake owner is reported.
65. Detailed freeze schema is loaded from the freeze owner.
66. No automatic refreeze occurs.

Durability and security:

67. Chat-only handoff is labeled as chat-only.
68. Durable handoff uses the specialized Project Support owner.
69. Daily-work is not the sole durable owner.
70. Handoff does not become a duplicate canonical source.
71. Secrets are removed.
72. Credentials and tokens are removed.
73. Patient or personal data is removed or redacted.
74. Unnecessary absolute private paths are minimized.
75. Export safety is explicit.

Validator design:

76. Do not validate exact explanatory phrases.
77. Do not require exact future version equality.
78. Do not require fixed startup position 8.
79. Inspect current source-map keys.
80. Test semantic trigger behavior.
81. Test false-positive behavior.
82. Test freeze-confirmation protection.
83. Test next-chat startup requirement.
84. Test durable placement.
85. Test external Project and self-hosting cases.
86. Test no source or validation claim from handoff alone.

ERROR MEMORY APPLICATION

Relevant compact lessons:

lesson-brick-wall-q01-validator-exact-phrase-count-assumption-v1

Application:

Do not protect the handoff prompt through exact phrase checks such as one fixed farewell sentence.

lesson-brick-wall-q01-validator-forward-version-rigidity-v1

Application:

Do not require exact future prompt version or fixed startup position.

lesson-brick-wall-q02-validator-forward-contract-rigidity-v1

Application:

Allow stronger future handoff schemas while preserving the closure and honesty invariants.

lesson-brick-wall-focused-validator-task-route-key-assumption-v1

Application:

Inspect the current routing and startup source-map schema before writing assertions.

lesson-brick-wall-delivery-unextracted-bundle-path-assumption-v1

Application:

A handoff must accurately distinguish delivered, staged, installed, and validated patch states.

Full Error Memory ZIP needed:

NO

Reason:

This is not repeated-error debugging or Error Memory canon auditing. Compact lessons and exact current source are sufficient.

BRICK WALL STATUS

Project slug:
kanda_reasoner

Task:
Audit prompt 010 individually

Current phase:
Read-only canonical audit completed

Primary box:
Prompt Library / Session Closure and Continuity Bridge

External owner boxes inspected:

* Governance and Handoff
* Freeze Workflow
* Startup Delivery
* Durable Artifact Routing
* Tool-versus-Project
* Brick Wall
* MCard

Tool root:
E:\kanda_reasoner

Active Project root:
E:\kanda_reasoner

Active Project support root:
E:\kanda_reasoner_show_project_to_AI

Same physical Tool/Project root:
YES

Selected target:
handoff_at_end_of_work.md

Current source fingerprint:
71821c191da66c2f68f8e8a1b77885daea07c0ce57ebea02d5894e4d4fba2e65

Verified problem status:
COMPLETE

Admission decision:
KEEP_UPDATE_AND_NARROW

Unique capability:
YES

Compact Error Memory:
REVIEWED

Full Error Memory:
NOT REQUIRED

Exact-source inspection:
COMPLETE

Canonical-to-generated sync:
PASS

Encoding:
PASS

Tool/Project boundary in target:
PARTIAL FAIL

Reason:

Current template does not fully identify Tool, Project Support, transient, or self-hosting ownership.

Box Boundary:
PARTIAL FAIL

Reason:

The closure trigger is properly owned, but detailed handoff and freeze schemas overlap other owners.

NO-LEAK in target:
PARTIAL FAIL

Reason:

Missing redaction, durable-placement, and handoff-authority classification can leak sensitive or non-authoritative context.

Audit operation NO-LEAK:
COMPLETE

No source, metadata, startup artifact, handoff, freeze entry, or validation evidence was written.

MCard:
N/A FOR AUDIT

MCard requirement in future handoffs:
CONDITIONAL

Shield:
REQUIRED FOR FUTURE CORRECTION

Recommended protected invariants:

* genuine closure trigger;
* no new implementation after closure;
* evidence honesty;
* handoff is continuity evidence only;
* next-chat startup remains mandatory;
* no freeze bypass;
* no installed sidecar;
* durable placement;
* redaction;
* exact next safe action.

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

May modify startup source map:
NO

May modify handoff templates:
NO

May regenerate startup delivery:
NO

May claim validation passed:
NO

May freeze:
NO

Q01-Q40 SUMMARY

Q01:
COMPLETE

Verified problems:

* unsafe direct freeze-preparation path;
* sidecar installed-file ambiguity;
* handoff-authority ambiguity;
* duplicated detailed handoff schema;
* ambiguous triggers;
* incomplete Tool/Project fields;
* insufficient state granularity;
* missing durable placement;
* missing redaction;
* duplicated freeze metadata;
* missing MCard and Brick Wall summaries;
* incomplete metadata;
* fragile historical validation.

Admission decision:

KEEP_UPDATE_AND_NARROW

Q02-Q04:
COMPLETE

Relevant compact Error Memory reviewed.

Q05:
COMPLETE

Canonical source, metadata, startup source map, generated startup copy, current startup workflow, handoff templates, freeze owner, and historical validation evidence were inspected.

Q06-Q10:
PARTIAL FAIL IN TARGET

Tool, Project, Project Support, Box, and NO-LEAK reporting are incomplete.

Q11-Q18:
N/A FOR AUDIT

Future handoffs must report MCard state when applicable.

Q19-Q25:
N/A

No Qt, runtime, property-based, mutation-testing, or GUI execution occurred.

Q26:
N/A

No ZIP was built or delivered.

Q27:
PASS

Encoding and text structure passed.

Q28-Q30:
FAIL IN TARGET WORDING

Freeze-preparation and sidecar wording can bypass or confuse the protected human freeze workflow.

No freeze was performed during the audit.

Q31:
IN PROGRESS

A future changed-file-to-validator plan is proposed.

Q32:
COMPLETE

Current source and generated startup provenance were verified.

Q33-Q36:
N/A

No AI model, performance optimization, benchmark, or Python implementation change occurred.

Q37:
PARTIAL FAIL

Closure ownership is distinct, but detailed handoff and freeze schemas are duplicated.

Q38:
COMPLETE

Current source archive, startup contract, second-upload workflow, and owner prompts were used.

Q39:
PASS

No new handoff engine, schema, context system, or prompt is recommended.

Q40:
N/A

No governed release occurred.

FINAL AUDIT RECOMMENDATION

RECOMMENDED CLASSIFICATION:
ALWAYS-STARTUP SESSION-CLOSURE AND CONTINUITY GUARDRAIL

RECOMMENDED ACTION:
KEEP, UPDATE, AND NARROW

DELETE:
NO

DEPRECATE:
NO

RETIRE:
NO

CURRENT STATUS:
active

LIKELY FINAL STATUS:
active

PROMPT CODE:
ASSIGN AFTER COMPLETE CLASS 01 REGISTRY AUDIT

HANDOFF TEMPLATE EFFECT:
ROUTE DETAILED STRUCTURE TO ONE CLASS 03 OWNER AFTER ITS AUDIT

FREEZE EFFECT:
REMOVE DIRECT FREEZE-PATH AND RECEIVER-SCHEMA OWNERSHIP

VALIDATOR EFFECT:
CREATE SEMANTIC NEGATIVE-CASE VALIDATION

STARTUP EFFECT:
REGENERATE ONLY AFTER GOVERNED CORRECTION

FINAL DECISION:

Keep this prompt because the always-loaded closure trigger is valuable and unique.

Reduce it to:

* closure detection;
* no-new-work behavior;
* minimum factual continuity contract;
* evidence honesty;
* next-chat startup requirement;
* routing to detailed handoff, freeze, Brick Wall, MCard, and durable-artifact owners.

Do not preserve the current direct frozen-memory path, installed-sidecar ambiguity, or duplicated freeze-intake schema.
A correção futura deverá preservar Preview e Confirm and Write como ações humanas explícitas; o startup atual trata qualquer bypass desse gate como trabalho governado bloqueado. O validador histórico também deverá ser substituído, pois atualmente protege frases exatas e a posição fixa 8 em vez do comportamento de encerramento seguro.