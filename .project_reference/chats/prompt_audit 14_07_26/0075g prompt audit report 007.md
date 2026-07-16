O sétimo prompt está corretamente registrado como KPR-01-013, ativo e always_startup. Diferentemente dos prompts legados anteriores, ele possui responsabilidade própria e necessária. A recomendação é mantê-lo, com correções específicas no conteúdo, metadados e principalmente no validador.

PROMPT AUDIT REPORT 007

AUDIT_ID:
A007-20260714-REVIEW

PROMPT_FILENAME:
durable_document_artifact_routing_canon.md

PROMPT_CODE:
KPR-01-013

CANONICAL_ID:
durable_document_artifact_routing_canon

CANONICAL_LIBRARY_PATH:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/durable_document_artifact_routing_canon.md

CURRENT SOURCE SHA-256:
779ad5007be144ab858404184331f69d6d8f372e360bd15694cb9f12669aedd7

CURRENT SOURCE SIZE:
7,333 bytes

CURRENT SOURCE LENGTH:
213 lines

DECLARED VERSION:
1.0

SOURCE STATUS:
active

METADATA STATUS:
active

SOURCE LOAD MODE:
always_startup

METADATA LOAD TYPE:
always_startup

PROMPT CODE UNIQUENESS:
PASS

GENERATED STARTUP FILE:
13_durable_document_artifact_routing_canon.md

GENERATED STARTUP SOURCE HASH:
MATCHES CANONICAL SOURCE

AUDIT MODE:
Read-only, one-prompt audit

SOURCE MODIFIED:
NO

METADATA MODIFIED:
NO

VALIDATOR MODIFIED:
NO

PATCH CREATED:
NO

NEXT PROMPT OPENED FOR AUDIT:
NO

OVERALL VERDICT

This prompt has a valid, distinct, and currently necessary canonical responsibility.

It should not be deleted, deprecated, retired, or merged into another prompt.

Its central rules are correct:

* `_delete_after_daily_work` is transient and owns nothing;
* durable Project-specific documentation belongs under the external sibling Project Support root;
* canonical source documentation remains with its source owner;
* specialized Project Support owners take precedence;
* successful validation evidence must not remain only in daily-work;
* Tool and Active Project identities remain separate during self-hosting;
* unresolved ownership must fail closed.

RECOMMENDED ACTION:

KEEP AND UPDATE

The prompt itself requires targeted semantic clarification.

Its metadata requires dependency cleanup and modernization.

Its focused validator requires substantial repair because it currently protects exact wording, a concrete example, a fixed startup position, duplicated source-map content, and references to legacy or conflicting prompts.

RECOMMENDED CURRENT STATUS:

active

The current defects do not justify removing it from startup.

RECOMMENDED STATUS DURING A FUTURE CORRECTION PATCH:

in_review or blocked_by_conflict only while owner and validator changes are being made.

RECOMMENDED FINAL STATUS:

active

DECISION GATE:

HUMAN_REQUIRED for meaning-changing corrections and startup regeneration.

UNIQUE CAPABILITY ASSESSMENT

UNIQUE CAPABILITY EXISTS:

YES

ONE-SENTENCE RESPONSIBILITY:

Classify generated documentary artifacts by authority, lifetime, Project ownership, and specialized support owner so durable Project evidence survives transient cleanup without becoming duplicate source truth.

SINGLE RESPONSIBILITY PASS:

MOSTLY PASS

The prompt stays focused on durable documentary-artifact ownership.

It contains limited patch, validation, freeze, handoff, and Tool-versus-Project references, but these are primarily routing and ownership implications of its main responsibility.

It does not attempt to define complete:

* patch installation;
* terminal cleanup;
* freeze-form generation;
* Error Memory schema;
* handoff schema;
* source mutation;
* implementation authorization.

This is materially better scoped than Prompts 3, 4, and 5.

POSITIVE FINDINGS

P007-P001

TITLE:
Stable canonical identity

RESULT:
PASS

The source and metadata agree on:

* prompt code;
* prompt ID;
* status;
* load mode;
* canonical path;
* category.

`KPR-01-013` has one metadata owner.

P007-P002

TITLE:
Canonical source and generated startup copy are synchronized

RESULT:
PASS

The generated startup file identifies:

* the canonical source path;
* the canonical source SHA-256;
* the generator;
* the instruction not to edit the generated file directly.

The recorded source SHA-256 matches the current canonical source.

P007-P003

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
* no corrupted prompt identifiers.

Brick Wall Q27 passes.

P007-P004

TITLE:
Correct transient-garbage rule

RESULT:
PASS

The prompt correctly states that:

`<project>_delete_after_daily_work`

may contain:

* temporary extraction trees;
* temporary helpers;
* transient logs;
* staging material;
* regenerable artifacts.

It must not be the sole owner of durable documentation or evidence.

P007-P005

TITLE:
Correct external Project Support ownership

RESULT:
PASS

The prompt correctly derives:

`<project_drive>\<project_name>_show_project_to_AI`

as the sibling durable support root.

It explicitly prohibits hardcoding KANDA Reasoner’s support root for another selected Project.

P007-P006

TITLE:
Correct source-document protection

RESULT:
PASS

The prompt correctly distinguishes canonical source documentation from generated Project-support documentation.

It does not instruct the AI to move:

* repository README files;
* prompt-library canon;
* checked-in architecture files;
* source-controlled specifications;

into `_show_project_to_AI` merely because they use `.md` or `.txt`.

P007-P007

TITLE:
Specialized-owner precedence

RESULT:
PASS

The prompt correctly gives precedence to specialized support owners such as:

* project_validation_evidence;
* project_error_memory;
* project_freeze_after_update;
* large_file_refactor_workbench;
* first_prompt_files;
* second_prompt_files.

This prevents `project_documentation` from becoming a second generic authority.

P007-P008

TITLE:
Self-hosting handling

RESULT:
PASS

The prompt correctly states that physical equality between Tool root and Active Project root does not collapse logical ownership.

P007-P009

TITLE:
Fail-closed behavior

RESULT:
PASS

The prompt blocks durable writing when:

* Active Project root is unresolved;
* support root cannot be derived;
* another Project’s support root would be used;
* daily-work would become the sole owner;
* duplicate durable authorities would be created.

P007-P010

TITLE:
No unnecessary new system

RESULT:
PASS

The prompt uses the existing Project Support structure.

It does not propose:

* a new document database;
* a new evidence engine;
* a new project-context schema;
* a new artifact registry;
* a new routing system.

HIGH-SEVERITY FINDINGS

FINDING A007-F001

TITLE:
Metadata creates circular and inverted dependencies

SEVERITY:
HIGH

CURRENT METADATA REQUIRES:

* start_of_day_master_stack
* daily_patch_delivery_guardrails
* project_tool_boundary_canon

CURRENT ACTUAL RELATIONSHIPS:

* `start_of_day_master_stack` contains a bridge pointing to this canon.
* `daily_patch_delivery_guardrails` contains a bridge pointing to this canon.
* This canon is the detailed owner of durable documentary routing.

PROBLEM:

The detailed canonical owner is declared as depending on its own downstream startup summaries.

This reverses authority.

It also creates a circular conceptual dependency:

durable canon
-> requires startup bridge
-> startup bridge says durable canon is the full owner

and:

durable canon
-> requires patch guardrail
-> patch guardrail routes durable evidence back to durable canon

CORRECTION:

Remove these as semantic requirements:

* start_of_day_master_stack
* daily_patch_delivery_guardrails

Keep them as downstream consumers or bridge surfaces.

Recommended metadata relationship:

requires:

* project_tool_boundary_canon

recommended_companions:

* start_of_day_master_stack
* daily_patch_delivery_guardrails
* pre_output_contract_gates, when emitting evidence or patch artifacts
* freeze_code_intake_and_form_protocol, when freeze applies
* brick_wall_comprehensive_quality_gate, for governed implementation

The owner must not depend on its summaries.

FINDING A007-F002

TITLE:
Artifact classification relies too heavily on file extension

SEVERITY:
HIGH

CURRENT RULE:

Generated Project-specific `.txt`, `.md`, or similar human-readable artifacts default to durable Project Support unless explicitly transient.

PROBLEM:

Durability is determined by purpose, authority, lifetime, and future use—not by extension.

Important documentary artifacts may use:

* `.json`
* `.csv`
* `.html`
* `.pdf`
* `.docx`
* `.yaml`
* `.xml`
* structured receipts or manifests

Conversely, a temporary `.txt` or `.md` file may be entirely disposable.

The current wording may:

* under-route durable non-text-extension artifacts;
* over-route temporary text files;
* encourage extension-based rather than ownership-based decisions.

CORRECTION:

Make purpose and lifetime primary.

Recommended rule:

“Generated Project-specific documentary artifacts default to durable Project Support when they must survive cleanup, support later reasoning, preserve a decision, prove validation, support handoff, support Error Memory, or support freeze, regardless of file extension. File extension alone does not determine ownership.”

Retain `.txt` and `.md` only as common examples.

FINDING A007-F003

TITLE:
The classification model mixes authority, lifetime, and destination in one flat list

SEVERITY:
HIGH

CURRENT EXACTLY-ONE CLASSIFICATIONS:

* CANONICAL_SOURCE_DOCUMENT
* DURABLE_PROJECT_DOCUMENT
* TRANSIENT_DAILY_WORK_ARTIFACT
* SPECIALIZED_PROJECT_SUPPORT_ARTIFACT

PROBLEM:

The categories mix different conceptual dimensions.

Examples:

* `CANONICAL_SOURCE_DOCUMENT` describes authority.
* `TRANSIENT_DAILY_WORK_ARTIFACT` describes lifetime and location.
* `SPECIALIZED_PROJECT_SUPPORT_ARTIFACT` describes destination.
* `DURABLE_PROJECT_DOCUMENT` describes lifetime and general destination.

A specialized Project Support artifact is also durable, so the categories are not fully exclusive semantically even though the prompt requires exactly one.

CORRECTION:

Do not introduce a new schema.

Clarify the classification sequence:

1. Is the artifact canonical source or generated?
2. If generated, is it transient or durable?
3. If durable, does a specialized owner exist?
4. If no specialized owner exists, use `project_documentation`.

This preserves the current folders while eliminating category ambiguity.

FINDING A007-F004

TITLE:
No sensitivity, secret, privacy, or redaction gate before durable persistence

SEVERITY:
CRITICAL

CURRENT BEHAVIOR:

Generated Project-specific documentary artifacts needed later should be written or copied into Project Support.

MISSING:

* secret detection;
* credential and token exclusion;
* private-data minimization;
* sensitive source-content review;
* redaction;
* export-safety classification;
* least-necessary evidence.

PROBLEM:

A durable artifact may contain:

* API keys;
* passwords;
* tokens;
* private environment values;
* personal data;
* confidential source excerpts;
* patient information;
* raw exception payloads;
* local machine details;
* unrelated Project data.

Persisting such content into handoff or AI-readable support folders may create a security or privacy leak even when the ownership path is otherwise correct.

CORRECTION:

Add a compact safety gate:

“Before durable persistence, remove secrets, credentials, tokens, unnecessary private data, and unrelated source content. Persist the smallest evidence necessary for the artifact’s purpose. When an artifact is intended for AI handoff or export, require explicit export-safe redaction.”

Do not make this prompt the complete security canon.

Route high-risk cases to the current security and redaction owners.

FINDING A007-F005

TITLE:
Failed validation evidence is not adequately protected

SEVERITY:
HIGH

CURRENT RULE:

After successful validation, evidence must be written or copied to the durable validation-evidence owner.

PROBLEM:

A failed validation may also produce evidence that must survive when it:

* defines the current blocker;
* supports Error Memory;
* explains a correction;
* supports a handoff;
* proves a regression;
* is needed for the next session;
* is required to compare a later rerun.

The current wording can be interpreted as allowing all failed-validation evidence to disappear with daily-work cleanup.

CORRECTION:

Clarify:

* routine disposable failure noise may remain transient;
* failure evidence that supports a blocker, correction, Error Memory lesson, handoff, regression analysis, or later comparison is durable;
* successful freeze-ready evidence is always durable;
* evidence ownership must be selected before cleanup.

FINDING A007-F006

TITLE:
Freeze wording is weaker than the current protected contract

SEVERITY:
HIGH

CURRENT WORDING:

“Freeze preparation should prefer the durable evidence copy when the current freeze tooling supports it.”

PROBLEM:

“Prefer” and “when tooling supports it” make durable evidence optional.

The current freeze contract requires Project-specific freeze data and evidence to remain under the selected Project Support root. Freeze must not depend on a daily-work-only copy.

CORRECTION:

Replace with:

“Freeze-ready workflows must use durable Project-owned evidence. If required evidence exists only in daily-work or cannot be resolved to its durable owner, freeze preparation is blocked.”

Compatibility with a legacy transient consumer may be retained only if the durable copy is also created and proven.

FINDING A007-F007

TITLE:
Evidence-path reporting does not distinguish expected path from verified existing path

SEVERITY:
HIGH

CURRENT RULE:

“The final response must identify the durable evidence path.”

PROBLEM:

An AI may know the intended canonical path without having verified that:

* the directory exists;
* the evidence file was written;
* the bytes correspond to the completed validation;
* the file belongs to the current feature;
* the path is not stale.

This can create a false provenance claim.

CORRECTION:

Require explicit provenance labels:

* EXPECTED DURABLE PATH
* WRITTEN DURABLE PATH
* VERIFIED DURABLE PATH
* NOT YET CREATED
* LOCAL VALIDATION REQUIRED

Do not say that durable evidence exists unless it was actually verified.

FINDING A007-F008

TITLE:
No explicit Brick Wall and NO_LEAK bridge

SEVERITY:
HIGH

The prompt already implements part of Tool-versus-Project and ownership classification, but it does not explicitly state that:

* Brick Wall governs admission and authorization;
* NO_LEAK_LOGIC_V1 governs wrong-root, cross-Project, generated-source, and evidence leakage;
* this prompt does not authorize source writing, validation claims, delivery, or freeze.

CORRECTION:

Add a compact bridge:

“This canon classifies documentary ownership only. Governed implementation and release remain subject to Brick Wall, `project_tool_boundary_canon`, Box Logic, and NO_LEAK_LOGIC_V1. Durable routing does not itself authorize source mutation, validation claims, patch delivery, or freeze.”

Do not copy Q01-Q40 into this prompt.

VALIDATOR FINDINGS

VALIDATOR PATH:

tools/validate_durable_document_artifact_routing_canon_v1.py

VALIDATOR SIZE:

365 lines

MODULE-SIZE STATUS:

PASS

The validator remains below the 500-line physical maximum.

However, its contract design requires significant repair.

FINDING A007-F009

TITLE:
Validator protects exact prose instead of durable behavior

SEVERITY:
CRITICAL

The validator requires exact text fragments including:

* `Prompt code: KPR-01-013`
* `Load mode: always_startup`
* `DURABLE_PROJECT_DOCUMENT`
* `TRANSIENT_DAILY_WORK_ARTIFACT`
* a concrete validation filename;
* exact heading phrases;
* exact startup-bridge wording;
* exact README phrases.

PROBLEM:

A semantically stronger future version could be rejected merely because wording or classification labels changed.

This reproduces the exact Error Memory failures already documented for:

* phrase-count assumptions;
* forward contract rigidity;
* version rigidity.

CORRECTION:

Validate semantic invariants:

* daily-work cannot be durable owner;
* support root is external sibling;
* source documentation remains source-owned;
* specialized owners win;
* successful freeze-ready evidence is durable;
* wrong-Project paths fail closed;
* provenance is explicit;
* generated artifacts cannot become source truth.

Do not require examples or explanatory sentences.

FINDING A007-F010

TITLE:
Validator freezes one concrete example filename and Project path

SEVERITY:
HIGH

The validator requires:

`code_module_quality_canon_v1_validation_evidence.txt`

The prompt also contains a concrete self-hosting path under:

`E:\kanda_reasoner_show_project_to_AI\...`

PROBLEM:

The example is not part of the durable behavioral contract.

Requiring it causes:

* project-specific leakage;
* obsolete example retention;
* inability to simplify the prompt;
* accidental treatment of one feature as canonical.

CORRECTION:

Remove the example from validator requirements.

The prompt may retain a short clearly labeled example, but no specific feature ID or absolute path should be a permanent validation gate.

Prefer a placeholder example:

`<project_support_root>\project_validation_evidence\<feature_id>\<feature_id>_validation_evidence.txt`

FINDING A007-F011

TITLE:
Validator freezes the prompt at startup position 13

SEVERITY:
HIGH

CURRENT ASSERTION:

`load_order` must equal `13`.

PROBLEM:

A future compatible startup artifact inserted before this prompt would move its numeric position without changing:

* its identity;
* its always-startup behavior;
* its generated filename contract, if renamed through a governed migration;
* its semantic role.

The fixed integer is release-specific rather than behavioral.

CORRECTION:

Validate:

* exactly one source-map entry exists;
* load mode is `always_startup`;
* canonical source resolves;
* generated filename is unique;
* ordering is deterministic and contiguous;
* required owner precedes dependent summaries when ordering matters.

Do not permanently require position 13 unless position 13 is explicitly declared a public compatibility contract.

FINDING A007-F012

TITLE:
Validator hardcodes a duplicate Python source map

SEVERITY:
CRITICAL

CURRENT BEHAVIOR:

The validator requires the durable prompt to exist in both:

* STARTUP_ROUTING_KERNEL_SOURCES.json
* startup_kernel/startup_source_map.py

The Python file contains a hardcoded `DEFAULT_SOURCE_MAP` with the same source records.

PROBLEM:

The startup-maintenance canon says the JSON source map is canonical and the generator must not hardcode a second source list when the source map exists.

The validator currently protects duplicate source ownership.

CORRECTION:

Choose one source-map authority.

Recommended:

`STARTUP_ROUTING_KERNEL_SOURCES.json`

The Python module should:

* parse the canonical JSON;
* expose typed records;
* validate schema;
* fail closed when the canonical source map is unavailable;

rather than independently maintaining the same list.

This is a startup-maintenance correction and must be handled through the startup-delivery maintenance protocol, not through an isolated prompt edit.

FINDING A007-F013

TITLE:
Validator depends on prompts already identified as conflicting or obsolete

SEVERITY:
CRITICAL

The validator requires durable-routing markers in:

* daily_patch_delivery_guardrails.md
* reasoner_startup_canon.md
* start_of_day_master_stack.md

Prompt Audit 003 found that `daily_patch_delivery_guardrails` requires major consolidation.

`reasoner_startup_canon` has not yet been audited but belongs to the same legacy startup family as the deprecated candidates already found.

PROBLEM:

The durable canon’s validator can block cleanup of unrelated legacy prompts.

It effectively requires multiple parallel copies of the durable rule to remain active.

CORRECTION:

Validate the canonical owner and one compact startup bridge.

Do not require every legacy startup or patch prompt to duplicate the full behavior.

Recommended required surfaces:

* canonical prompt;
* canonical metadata;
* canonical source map;
* generated startup copy;
* one beginning-of-day bridge;
* Tool-versus-Project owner;
* focused negative tests.

Other prompts may reference the canon, but their exact prose should not be frozen by this validator.

FINDING A007-F014

TITLE:
Validator requires historical generated-file numbering and README wording

SEVERITY:
HIGH

The validator requires:

* `13_durable_document_artifact_routing_canon.md`
* “Confirm `00`, `01` to `13`”
* “13. 13_durable_document_artifact_routing_canon.md”

PROBLEM:

This couples semantic validation to one release’s total startup-file count.

The current startup already includes later files, so wording based on `00` to `13` is inherently historical.

CORRECTION:

Inspect the current source map dynamically.

Validate that:

* every current source has one generated file;
* generated order matches current map;
* start-here lists all current required files;
* no stale upper-bound count remains;
* the durable prompt is present by current identity.

FINDING A007-F015

TITLE:
Validator lacks negative routing and ownership tests

SEVERITY:
HIGH

CURRENT VALIDATOR:

Mostly checks that required strings exist.

MISSING NEGATIVE CASES:

* nested support root;
* another Project’s support root;
* daily-work-only durable evidence;
* duplicate durable authorities;
* source document copied and treated as generated authority;
* transient file incorrectly promoted;
* sensitive artifact persisted without redaction;
* failed blocker evidence deleted;
* expected path reported as verified;
* hardcoded KANDA path for another Project;
* specialized owner bypassed by general project_documentation.

CORRECTION:

Add focused behavior-level negative tests.

Do not expand the validator through more text-fragment assertions.

METADATA FINDINGS

FINDING A007-F016

TITLE:
Canonical metadata lacks version and owner-box fields

SEVERITY:
MEDIUM

SOURCE CONTAINS:

* Version: 1.0
* Owner box: Context Routing Kernel Box

METADATA DOES NOT CONTAIN:

* version;
* owner_box;
* title separate from display_name;
* updated_for;
* source_stage;
* last_updated;
* when_not_to_load;
* validation owner;
* supersession information.

PROBLEM:

The machine-readable record is less complete than the source.

CORRECTION:

Add synchronized metadata during a governed update.

Do not make exact version equality a permanent validator requirement.

Validate current source/metadata self-consistency and minimum compatible behavior.

FINDING A007-F017

TITLE:
Manual discoverability is incomplete

SEVERITY:
MEDIUM

The prompt is:

* in the startup source map;
* in the folder card;
* in metadata;
* always loaded.

However, the machine prompt-navigation index has no direct route whose selected prompt ID is:

`durable_document_artifact_routing_canon`

PROBLEM:

A user explicitly asking:

* where should generated reports be saved;
* where should validation evidence persist;
* can this file remain in daily-work;
* which folder owns a durable handoff;

may not route directly to the canonical owner.

CORRECTION:

Add a narrow direct route or deterministic route alias for documentary ownership questions.

Do not add broad aliases such as:

* document;
* file;
* report.

Recommended triggers:

* durable documentation routing
* validation evidence persistence
* daily-work cleanup safety
* Project Support artifact ownership
* where should generated reports persist
* daily-work versus show_project_to_AI

FINDING A007-F018

TITLE:
The prompt uses a concrete KANDA path as an example inside a cross-Project canon

SEVERITY:
MEDIUM

The prompt contains a concrete example under:

`E:\kanda_reasoner_show_project_to_AI\...`

The prompt later correctly warns against hardcoding KANDA paths for another Project.

PROBLEM:

A concrete path can still be copied as if it were a default.

CORRECTION:

Prefer placeholders in the main rule.

Retain the KANDA path only in a clearly labeled self-hosting example if it adds real explanatory value.

Do not require it in validators.

OVERLAP AND OWNER ANALYSIS

WITH project_tool_boundary_canon:

PARTIAL OVERLAP WITH VALID SEPARATION

`project_tool_boundary_canon` owns:

* Tool versus Active Project identity;
* source root;
* external Project Support root;
* transient garbage root;
* nested-support prohibition;
* broad Project-specific support ownership.

`durable_document_artifact_routing_canon` owns:

* documentary artifact classification;
* durable documentation lifetime;
* general versus specialized documentation owner;
* durable validation-evidence routing;
* documentary fail-closed behavior.

Both should remain.

The durable canon must require the boundary canon, not duplicate its full architecture.

WITH start_of_day_master_stack:

VALID OWNER-TO-BRIDGE RELATIONSHIP

The master stack may contain a concise bridge.

It must not become the full owner.

The durable canon must not declare the downstream bridge as a semantic dependency.

WITH daily_patch_delivery_guardrails:

VALID BRIDGE RELATIONSHIP, CURRENTLY OVERCOUPLED

Patch delivery may reference durable evidence ownership.

The durable canon should not depend on the complete patch guardrail.

WITH pre_output_contract_gates:

CONDITIONAL COMPANION

When the AI emits validation evidence, paths, patch artifacts, or freeze-related output, pre-output gates apply.

The durable canon should not reproduce terminal or ZIP behavior.

WITH freeze_code_intake_and_form_protocol:

CONDITIONAL COMPANION

Freeze requires durable evidence, but this prompt must not own freeze-form behavior.

WITH Error Memory:

CONDITIONAL SPECIALIZED OWNER

Error Memory artifacts belong under the Error Memory owner.

The durable canon should route them there and require redaction but must not define the Error Memory schema.

WITH project_documentation:

GENERAL FALLBACK OWNER

This is not a competing owner.

It applies only when no specialized owner exists.

DISSONANT LOGIC FOUND:

YES, primarily in the focused validator and startup source-map implementation.

NEW PROMPT REQUIRED:

NO

NEW ARTIFACT DATABASE REQUIRED:

NO

NEW SCHEMA REQUIRED:

NO

The current prompt can be repaired through clarification and owner consolidation.

RECOMMENDED CORRECTED STRUCTURE

1. Identity and ownership
2. Purpose
3. Authority hierarchy
4. Classification sequence
5. Canonical source documents
6. Generated transient artifacts
7. Generated durable artifacts
8. Specialized support-owner precedence
9. Validation evidence
10. Failed-validation and blocker evidence
11. Sensitivity and redaction
12. Provenance labels
13. Tool-versus-Project and NO-LEAK bridge
14. Patch, handoff, Error Memory, and freeze owner references
15. Failure behavior
16. Do-not-regress rules
17. Version history

RECOMMENDED CLASSIFICATION SEQUENCE

STEP 1:
SOURCE AUTHORITY

* CANONICAL SOURCE
* GENERATED ARTIFACT

STEP 2:
LIFETIME, IF GENERATED

* TRANSIENT
* DURABLE

STEP 3:
OWNER, IF DURABLE

* SPECIALIZED PROJECT SUPPORT OWNER
* GENERAL project_documentation FALLBACK

STEP 4:
EXPORT SAFETY

* INTERNAL ONLY
* REDACTED EXPORT SAFE
* BLOCKED FROM PERSISTENCE OR EXPORT

This is a clarification of the existing model, not a new Project-wide schema.

SMALLEST SAFE FUTURE CORRECTION PLAN

Do not implement now.

After the full prompt-library audit:

Phase 1:
Confirm detailed owner prompts:

* project_tool_boundary_canon
* start_of_day_master_stack
* pre_output_contract_gates
* freeze_code_intake_and_form_protocol
* Error Memory owner
* reasoner_startup_canon
* daily_patch_delivery_guardrails

Phase 2:
Correct the canonical prompt semantics.

Phase 3:
Modernize metadata and remove circular dependencies.

Phase 4:
Repair the focused validator.

Phase 5:
Resolve the JSON-versus-Python startup source-map duplication through the startup-maintenance owner.

Phase 6:
Update narrow manual routing.

Phase 7:
Regenerate startup delivery from canonical sources.

Phase 8:
Run focused semantic, negative, startup-sync, external-Project, and self-hosting validation.

Phase 9:
Require user-local validation before freeze.

REQUIRED VALIDATION AFTER FUTURE CORRECTION

Identity and metadata:

1. Prompt code remains KPR-01-013.
2. Prompt code remains unique.
3. Prompt ID is unchanged.
4. Status is active.
5. Load mode remains always_startup.
6. Version is synchronized.
7. Owner box is synchronized.
8. Canonical path is correct.
9. Metadata contains no circular semantic dependency.
10. Source and metadata agree.

Core ownership:

11. Daily-work owns nothing durable.
12. Project Support remains an external sibling.
13. Nested Project Support is rejected.
14. Another Project’s support root is rejected.
15. Canonical source documents remain with source owner.
16. Generated artifacts never become source truth.
17. Specialized support owners take precedence.
18. General project_documentation is fallback only.
19. Duplicate durable authorities are rejected.
20. Self-hosting does not collapse Tool and Project.

Artifact semantics:

21. Lifetime is based on purpose, not extension.
22. Durable `.json`, `.csv`, `.html`, `.pdf`, and similar outputs are supported.
23. Temporary `.txt` and `.md` may remain transient when correctly classified.
24. Failed blocker evidence persists when required.
25. Routine disposable noise may remain transient.
26. Freeze-ready evidence is always durable.
27. Error Memory uses its specialized owner.
28. Handoff uses its specialized owner.
29. First and second prompt files use their specialized owners.
30. Workbench Preview and Shadow remain separated.

Security and provenance:

31. Secrets and credentials are excluded.
32. Sensitive data is minimized or redacted.
33. Export-safe artifacts are explicitly classified.
34. Expected paths are not reported as verified paths.
35. Durable write success is proven before existence is claimed.
36. Evidence is tied to the current feature and validation run.
37. Stale evidence is rejected.
38. Wrong-feature evidence is rejected.

Startup and routing:

39. Canonical JSON source map has one owner.
40. Python generator does not independently own a duplicate source list.
41. The prompt appears exactly once in the current source map.
42. Generated startup copy derives from canonical source.
43. Generated copy hash matches.
44. Start-of-day bridge remains concise.
45. Direct manual routing is narrow and deterministic.
46. No legacy prompt is required to duplicate full durable rules.
47. Startup load check remains complete.
48. Current startup filename ordering is derived dynamically.

Validator design:

49. No concrete feature filename is required.
50. No concrete KANDA absolute path is required.
51. No exact explanatory phrase is a permanent contract.
52. No fixed future version equality is required.
53. No fixed startup position is required unless explicitly public.
54. Current routing and source-map keys are inspected.
55. Negative wrong-root tests exist.
56. Negative duplicate-authority tests exist.
57. Negative sensitivity-leak test exists.
58. Negative failed-evidence-loss test exists.
59. Negative false-provenance test exists.
60. External-Project and self-hosting cases both pass.

ERROR MEMORY APPLICATION

Relevant compact lessons:

lesson-brick-wall-q01-validator-exact-phrase-count-assumption-v1

Application:

Replace text-fragment proxy checks with semantic ownership and negative-path tests.

lesson-brick-wall-q01-validator-forward-version-rigidity-v1

Application:

Do not require one exact future prompt version or startup position.

lesson-brick-wall-q02-validator-forward-contract-rigidity-v1

Application:

Allow later compatible strengthening without preserving old explanatory prose.

lesson-brick-wall-focused-validator-task-route-key-assumption-v1

Application:

Inspect actual current source-map and routing keys.

lesson-project-tool-boundary-workbench-preview-router-bridge-v1

Application:

Durable Preview and evidence belong under Project Support; disposable Shadow and temporary assembly belong under transient garbage.

Full Error Memory ZIP needed:

NO

Reason:

Compact lessons and exact current source are sufficient for this read-only audit.

BRICK WALL STATUS

Project slug:
kanda_reasoner

Task:
Audit prompt 007 individually

Current phase:
Read-only canonical audit completed

Primary box:
Prompt Library / Context Routing Kernel

Primary semantic responsibility:
Durable documentary artifact ownership

External owner boxes inspected:

* Project Tool Boundary
* Startup Delivery
* Patch Delivery and Validation
* Governance and Freeze
* Error Memory
* Project Support

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
durable_document_artifact_routing_canon.md

Current source fingerprint:
779ad5007be144ab858404184331f69d6d8f372e360bd15694cb9f12669aedd7

Verified problem status:
COMPLETE

Admission decision:
KEEP_AND_UPDATE

Unique capability:
YES

Error Memory:
Compact lessons reviewed

Full Error Memory:
NOT REQUIRED

Exact-source inspection:
COMPLETE

Canonical-to-generated sync:
PASS

Prompt-code uniqueness:
PASS

Tool/Project boundary:
MOSTLY PASS IN TARGET

Box Boundary:
MOSTLY PASS IN TARGET

NO-LEAK:
PARTIAL PASS IN TARGET

Reason:

Path ownership is strong, but sensitivity leakage, failed-evidence persistence, and false path-provenance require clarification.

Audit operation NO-LEAK:
COMPLETE

No file was written.

MCard:
N/A for this read-only prompt audit

Shield:
LIKELY REQUIRED FOR FUTURE CORRECTION

Recommended protected invariants:

* daily-work owns nothing;
* Project Support remains external;
* specialized owner precedence;
* source docs remain source-owned;
* freeze-ready evidence is durable;
* no cross-Project write;
* no secret persistence;
* no false provenance.

Encoding:
PASS

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

May modify validator:
NO

May modify startup source map:
NO

May regenerate startup delivery:
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

* circular metadata dependencies;
* extension-based ambiguity;
* missing sensitivity gate;
* incomplete failed-evidence handling;
* weak freeze wording;
* false provenance risk;
* rigid validator;
* duplicate source-map ownership;
* legacy-prompt validator coupling.

Admission decision:

KEEP_AND_UPDATE

Q02-Q04:
COMPLETE

Relevant compact Error Memory reviewed.

Q05:
COMPLETE

Canonical prompt, metadata, generated startup copy, source maps, focused validator, startup bridge, folder card, Tool/Project owner, and current output/freeze hooks were inspected.

Q06-Q10:
PARTIAL PASS

Core Tool, Project, support, and transient roles are correct.

NO-LEAK requires sensitivity and provenance strengthening.

Q11-Q18:
N/A

No MCard transaction, Preview mutation, Shadow run, or source write occurred.

Q19-Q25:
N/A

No Qt, runtime, property-based, mutation-testing, or GUI work occurred.

Q26:
N/A

No ZIP was built.

Q27:
PASS

Encoding, control-byte, and Markdown structural checks passed.

Q28-Q30:
N/A

No execution, exception, freeze write, or human confirmation occurred.

Q31:
IN PROGRESS

A future changed-file-to-validator map is proposed.

Q32:
COMPLETE

Canonical source and generated-copy provenance were verified.

Q33-Q36:
N/A

No AI model, optimization, benchmark, or Python implementation change occurred.

Q37:
PARTIAL FAIL

The prompt responsibility is distinct, but its metadata and validator create circular and duplicate ownership.

Q38:
COMPLETE

Current source archive, startup delivery, metadata, and current owner prompts were used.

Q39:
PASS

No new context engine, document database, evidence schema, or scanner is recommended.

Q40:
N/A

No governed release occurred.

FINAL AUDIT RECOMMENDATION

RECOMMENDED CLASSIFICATION:
SPECIALIST ALWAYS-STARTUP CANON

RECOMMENDED ACTION:
KEEP AND UPDATE

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
KEEP KPR-01-013

NAVIGATION EFFECT:
ADD NARROW MANUAL ROUTE

VALIDATOR EFFECT:
MAJOR REPAIR REQUIRED

STARTUP EFFECT:
REGENERATE ONLY AFTER GOVERNED CORRECTION

FINAL DECISION:

Keep this prompt as the canonical owner of durable documentary-artifact routing.

Clarify artifact classification, failed evidence, redaction, and provenance.

Remove circular metadata dependencies.

Repair the validator so it protects behavior rather than exact prose, fixed numbering, legacy prompt duplication, and concrete examples.

Resolve the duplicated JSON/Python startup source-map ownership through the startup-maintenance canon, not through a direct isolated edit.

A regra atual de freeze confirma que evidência necessária para congelamento deve permanecer no Project Support e que Preview e Confirm and Write continuam protegidos. O Error Memory atual também reforça que Preview durável e Shadow descartável devem permanecer separados.

