# HOW TO INSERT A NEW PROMPT AND CONNECT IT TO THE ROUTER

Purpose: this file explains the safe workflow for adding a new prompt to the KANDA prompt workspace, placing it in the correct ACTIVE_PROMPTS folder, making the router or startup delivery aware of it, testing it, validating it, and freezing it.

This is a guide for future AI-assisted work. It is not a shortcut around prompt audit, routing audit, validation, or freeze governance.

Last updated: 2026-06-23

---

## 1. Core rule

Do not put every new prompt in the same folder.

The correct folder depends on what the prompt is for.

The KANDA prompt workspace separates:

```text
kanda_prompt_workspace/
  prompt_library/        canonical prompt source
  prompt_tools/          generator and source-map machinery
  first_AI_deliver/      generated human-facing startup artifacts
```

The canonical prompt source is:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library
```

The active prompt folders are:

```text
E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS
```

Generated startup artifacts are not canonical source:

```text
E:\kanda_reasoner\kanda_prompt_workspace\first_AI_deliver
```

Do not directly edit files inside:

```text
first_prompts_to_ai.zip
paste_after_first_prompts_to_ai.md
```

as if they were source of truth. They are generated outputs.

---

## 2. The exact ACTIVE_PROMPTS folder depends on prompt type

Current active folder taxonomy:

```text
ACTIVE_PROMPTS/
  01_session_start_and_navigation/
  02_prompt_routing_and_indexing/
  03_governance_freeze_and_handoff/
  04_box_architecture_and_boundaries/
  05_patch_delivery_and_validation/
  06_refactor_and_architecture_hardening/
  07_prompt_authoring_and_audit/
  08_python_engineering_core/
  09_python_quality_security_observability/
  10_python_api_data_async_config/
  11_productization_and_release_readiness/
  12_generalized_project_canons/
```

Use this placement table.

| Prompt type | Correct folder | Examples |
|---|---|---|
| Startup, beginning-of-day, session load, upload-check, startup safety, first response shape | `01_session_start_and_navigation` | startup loader, session start checklist, Prompt Router Reasoner startup check |
| Prompt routing, prompt selection, prompt maps, route classification, navigation index, router behavior | `02_prompt_routing_and_indexing` | prompt_router, prompt_navigation_index, routing signal scorer canon |
| Freeze workflow, handoff, governance, freeze entry intake, pre-output gates | `03_governance_freeze_and_handoff` | freeze_code_intake_and_form_protocol, pre_output_contract_gates |
| Project architecture boundaries, box boundaries, shielding, folder organization, stateful control | `04_box_architecture_and_boundaries` | box architecture canon, project folder organization canon |
| Patch building, patch delivery, validation, bundle workflow, install contract | `05_patch_delivery_and_validation` | bundle_gated_development_workflow, universal_delivery_protocol |
| Refactor planning, architecture hardening, large-module refactor, codebase audits | `06_refactor_and_architecture_hardening` | large module refactor protocol, architecture hardening triage |
| Prompt creation, prompt auditing, duplicate detection, canon reconciliation, prompt generalization | `07_prompt_authoring_and_audit` | prompt_audit_canon, prompt_canon_reconciliation_protocol |
| Python code quality, architecture, clean code, DDD, design patterns, performance, legacy workflow | `08_python_engineering_core` | python_clean_code, python_refactoring |
| Testing, security, observability, logging, type safety, validation, documentation quality | `09_python_quality_security_observability` | python_testing_pytest, python_security_threat_prevention |
| APIs, data, async, parallelism, configuration, databases | `10_python_api_data_async_config` | python_api_design, python_configuration_feature_flags |
| Release readiness, versioning, SRE, deployment, infrastructure, productization | `11_productization_and_release_readiness` | productization readiness, lifecycle versioning |
| General reusable project canons not tied to Python-only work | `12_generalized_project_canons` | domain decision tables, shared visual render engine canon |

If a prompt could fit more than one folder, do not guess. Run a routing/folder audit first.

---

## 3. First decision: what kind of prompt is this?

Before adding a prompt, classify it.

### 3.1 Always-startup prompt

Use this when the prompt must be loaded every serious AI session at the beginning of day.

Examples:

```text
startup safety rule
startup load checklist
first response shape
Prompt Router Reasoner startup readiness check
```

Required behavior:

```text
load_mode: always_startup
```

Likely folder:

```text
ACTIVE_PROMPTS\01_session_start_and_navigation
```

Must update:

```text
prompt_tools\STARTUP_ROUTING_KERNEL_SOURCES.json
prompt_tools\sync_startup_routing_kernel_pack.py if the output shape or generator behavior changes
first_AI_deliver generated outputs after sync
```

### 3.2 Normal routed prompt

Use this when the prompt should be called only when a task matches its intent.

Examples:

```text
a prompt for a specific class of refactor
a prompt for prompt-library audit
a prompt for API design
a prompt for validation planning
```

Must update the correct prompt-library folder and the routing/navigation indexes that make the prompt discoverable.

Do not add it to startup unless it truly must load every session.

### 3.3 On-request specialist prompt

Use this when the prompt is useful only if explicitly requested or selected by a routed workflow.

Examples:

```text
cooperative implementation methodology
specialist audit protocol
deep review template
```

Must not be auto-loaded unless a separate governed startup change is approved.

### 3.4 Maintenance-only prompt

Use this for prompts that modify startup delivery, prompt tools, generated artifacts, or other governance machinery.

Examples:

```text
paste_if_modify_startup_delivery
startup delivery maintenance protocol
```

These should not be included in normal daily startup unless explicitly required by the startup maintenance workflow.

---

## 4. Safe insertion workflow

Use this sequence for a new normal prompt.

### Step 1 - Read current prompt routing context

Before adding anything, inspect these:

```text
kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\<target_folder>\_FOLDER_ASSIMILATION.md
kanda_prompt_workspace\prompt_library\METADATA\
kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\
```

For governed prompt-library changes, request or apply:

```text
07_prompt_authoring_and_audit
prompt_canon_reconciliation_protocol
prompt_audit_canon
project_specific_prompt_generalization
relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION
existing prompt-library indexes needed to inspect overlap
validation command or manual validation steps
```

### Step 2 - Check for duplicates and overlap

Before creating a new prompt, search existing prompts for:

```text
same purpose
same title
same trigger words
same routing intent
same workflow step
same expected output
same governance boundary
```

Decide:

```text
create new prompt
update existing prompt
link/register existing prompt
split prompt
merge prompt
do not add prompt
```

Do not add a duplicate just because the wording is new.

### Step 3 - Choose the correct folder

Use the folder table in section 2.

Examples:

```text
Prompt about startup readiness:
ACTIVE_PROMPTS\01_session_start_and_navigation

Prompt about router selection logic:
ACTIVE_PROMPTS\02_prompt_routing_and_indexing

Prompt about freeze entry intake:
ACTIVE_PROMPTS\03_governance_freeze_and_handoff

Prompt about patch ZIP delivery:
ACTIVE_PROMPTS\05_patch_delivery_and_validation

Prompt about Python testing:
ACTIVE_PROMPTS\09_python_quality_security_observability
```

### Step 4 - Create the prompt file

Use a stable lowercase filename:

```text
my_new_prompt_name.md
```

Place it in:

```text
kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\<correct_folder>\my_new_prompt_name.md
```

Recommended prompt structure:

```text
# Prompt Title

## Purpose

## When to use

## When not to use

## Required context

## Required behavior

## Output shape

## Safety and governance rules

## Validation expectations

## Do-not-regress rules
```

### Step 5 - Add metadata

Create or update:

```text
kanda_prompt_workspace\prompt_library\METADATA\my_new_prompt_name.meta.json
```

Recommended fields:

```json
{
  "prompt_id": "my_new_prompt_name",
  "title": "My New Prompt Name",
  "folder": "ACTIVE_PROMPTS/<folder_name>",
  "path": "ACTIVE_PROMPTS/<folder_name>/my_new_prompt_name.md",
  "load_mode": "routed",
  "status": "active",
  "owner": "prompt_library",
  "created_for": "short purpose",
  "routing_intents": [
    "intent keyword 1",
    "intent keyword 2"
  ],
  "requires": [
    "related prompt or folder card"
  ],
  "do_not_regress": [
    "specific invariant"
  ]
}
```

Allowed load modes depend on the current router/startup design, but commonly include:

```text
always_startup
routed
on_request
maintenance_only
```

Do not mark a prompt `always_startup` unless it must be loaded every session.

### Step 6 - Update folder assimilation

Update:

```text
ACTIVE_PROMPTS\<correct_folder>\_FOLDER_ASSIMILATION.md
```

Add the prompt under the correct folder summary section.

Include:

```text
prompt name
purpose
when to use
when not to use
routing notes
dependencies
```

The folder assimilation file helps future AI choose the right prompt without loading every prompt blindly.

### Step 7 - Connect to the router

The exact router connection depends on prompt type.

#### For always-startup prompts

Update:

```text
kanda_prompt_workspace\prompt_tools\STARTUP_ROUTING_KERNEL_SOURCES.json
```

Add the prompt source with:

```json
{
  "id": "my_new_prompt_name",
  "source": "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/my_new_prompt_name.md",
  "output_name": "10_my_new_prompt_name.md",
  "load_mode": "always_startup"
}
```

The exact output number depends on current source order. Do not reuse an existing number.

Regenerate startup delivery:

```powershell
Set-Location "E:\kanda_reasoner\kanda_prompt_workspace"
python .\prompt_tools\sync_startup_routing_kernel_pack.py --dry-run
python .\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes
python .\prompt_tools\sync_startup_routing_kernel_pack.py --check
```

#### For normal routed prompts

Update the routing/navigation files that expose the prompt to the AI router.

Likely files to inspect before changing:

```text
ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_navigation_index.md
ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_router.md
ACTIVE_PROMPTS\02_prompt_routing_and_indexing\kanda_routing_system_canon.md
ACTIVE_PROMPTS\02_prompt_routing_and_indexing\_FOLDER_ASSIMILATION.md
```

The exact router file depends on the current design. Do not guess blindly.

Add routing entries that define:

```text
task classification
trigger signals
required prompt/group
recommended prompt/group
missing context behavior
anti-bypass behavior if applicable
```

The router should call the prompt when necessary, not every time.

#### For on-request specialist prompts

Do not add to startup.

Register it in the relevant folder assimilation and navigation index so the AI can request it when needed.

Examples:

```text
Recommended prompts/groups:
1. cooperative_implementation_methodology
```

The prompt remains available but not loaded automatically.

#### For maintenance-only prompts

Only connect it to maintenance workflows.

Example startup-maintenance rule:

```text
If the task modifies prompt_tools, first_AI_deliver, STARTUP_ROUTING_KERNEL_SOURCES.json, sync_startup_routing_kernel_pack.py, first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, or startup delivery naming/content/validation, request paste_if_modify_startup_delivery.md before implementation.
```

Do not include maintenance-only prompts in normal startup unless specifically approved.

---

## 5. Validation requirements

A new prompt is not done when the file exists.

It is done only when tests prove:

```text
prompt file exists in correct ACTIVE_PROMPTS folder
metadata exists and matches prompt_id/path/load_mode
folder assimilation references it
router/navigation can discover it
startup source map includes it if always_startup
generated startup ZIP includes it if always_startup
generated paste file mentions it if startup output shape changed
no generated artifact is treated as canonical source
no duplicate prompt was created
wrong tasks do not over-call the prompt
right tasks do call or request the prompt
```

For startup prompts, validate:

```text
first_prompts_to_ai.zip contains the expected output file at ZIP root
paste_after_first_prompts_to_ai.md contains the expected startup instruction
sync_startup_routing_kernel_pack.py --check returns STATUS: IN_SYNC
```

For normal routed prompts, validate with a targeted routing test:

```text
input task that should call prompt -> prompt is selected or requested
input task that should not call prompt -> prompt is not selected
ambiguous task -> router requests missing context or folder card instead of guessing
anti-bypass task -> router refuses bypass and routes correctly
```

---

## 6. Patch delivery requirements

If delivering this as a patch, include:

```text
KANDA_FREEZE_HINT.json at ZIP root
new prompt file
metadata file
updated _FOLDER_ASSIMILATION.md
updated router/navigation files
updated startup source map if startup prompt
updated generated startup artifacts if startup delivery changed
tests
```

Do not put `KANDA_FREEZE_HINT.json` inside the project root during install. It is ZIP delivery metadata only unless the local freeze workflow consumes it.

Use the project patch validator before delivery:

```powershell
python "scripts\validate_patch_zip.py" "<path_to_patch_zip>"
```

---

## 7. Freeze requirements

After install and validation pass, freeze the feature through the local freeze workflow.

The correct freeze memory location is:

```text
E:\kanda_reasoner\project_freeze_after_update\frozen_features_memory
```

Do not store project-specific frozen memory inside:

```text
E:\kanda_reasoner\project_freeze_ledger
```

Freeze entry should include:

```text
feature title
feature id
installed files
validation evidence
do-not-regress rules
known warnings
planned next step
```

After local freeze write, startup freeze context must be refreshed so future AI sessions become aware of the frozen prompt behavior.

---

## 8. Do-not-regress rules for prompt insertion

Use these as default invariants:

```text
- New prompts must live under prompt_library/ACTIVE_PROMPTS, not first_AI_deliver.
- The exact ACTIVE_PROMPTS folder depends on prompt type.
- Metadata must match the prompt path and load mode.
- Folder assimilation must expose the prompt purpose and when-to-use rules.
- Router/navigation changes must be targeted, not broad.
- Startup prompts must use STARTUP_ROUTING_KERNEL_SOURCES.json and generator sync.
- Generated first_AI_deliver artifacts are not canonical source files.
- Normal routed prompts must not become always_startup without explicit approval.
- Maintenance-only prompts must not load during normal startup.
- Validation output is the evidence; install success is not validation.
- Freeze memory belongs under project_freeze_after_update/frozen_features_memory.
- project_freeze_ledger remains reusable engine logic only.
```

---

## 9. Minimal checklist before adding any prompt

```text
[ ] I know the prompt type.
[ ] I know the correct ACTIVE_PROMPTS folder.
[ ] I searched existing prompts for duplicates and overlap.
[ ] I inspected the target folder _FOLDER_ASSIMILATION.md.
[ ] I inspected relevant routing/navigation indexes.
[ ] I created the prompt file.
[ ] I created or updated metadata.
[ ] I updated folder assimilation.
[ ] I connected it to the router, startup source map, or on-request index as appropriate.
[ ] I wrote tests.
[ ] I validated.
[ ] I packaged with KANDA_FREEZE_HINT.json if delivering a patch.
[ ] I froze only after validation passed.
[ ] I refreshed startup freeze context after freeze.
```

---

## 10. Fast examples

### Example A - Add a beginning-of-day checklist prompt

Place:

```text
ACTIVE_PROMPTS\01_session_start_and_navigation\my_startup_check.md
```

Connect:

```text
prompt_tools\STARTUP_ROUTING_KERNEL_SOURCES.json
load_mode: always_startup
```

Regenerate:

```powershell
python .\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes
python .\prompt_tools\sync_startup_routing_kernel_pack.py --check
```

Validate:

```text
first_prompts_to_ai.zip contains the new startup file
paste_after_first_prompts_to_ai.md includes required response shape
STATUS: IN_SYNC
```

### Example B - Add a new Python testing prompt

Place:

```text
ACTIVE_PROMPTS\09_python_quality_security_observability\my_testing_prompt.md
```

Connect:

```text
folder assimilation
prompt navigation index
router rules for testing tasks
```

Do not add to startup unless it must always load.

### Example C - Add a new patch delivery prompt

Place:

```text
ACTIVE_PROMPTS\05_patch_delivery_and_validation\my_patch_protocol.md
```

Connect:

```text
patch-delivery route
validation route
pre-output gates if it changes delivery behavior
```

Test:

```text
patch request routes to prompt
non-patch request does not route to prompt
delivery commands still follow guarded install/validation patterns
```

---

## 11. Common mistakes

```text
Mistake: Editing first_prompts_to_ai.zip directly.
Fix: Edit canonical prompt source and regenerate delivery.

Mistake: Putting every new prompt in 01_session_start_and_navigation.
Fix: Use the folder taxonomy. Startup folder is only for startup/session prompts.

Mistake: Adding a prompt without metadata.
Fix: Add metadata so future tools and AI can identify it.

Mistake: Adding a prompt without folder assimilation.
Fix: Update _FOLDER_ASSIMILATION.md so routing can understand the folder role.

Mistake: Making a normal prompt always_startup.
Fix: Use routed or on_request unless it must load every serious session.

Mistake: Freezing after install without validation.
Fix: Freeze only after validation output is available.

Mistake: Putting project freeze memory into project_freeze_ledger.
Fix: Use project_freeze_after_update/frozen_features_memory.
```

---

## 12. Final rule

A prompt is truly connected only when all are true:

```text
1. It is in the correct ACTIVE_PROMPTS folder.
2. Its metadata exists.
3. Its folder assimilation exposes it.
4. The correct router/startup/on-request index can discover it.
5. Tests prove it is called when necessary and not called when inappropriate.
6. Validation passes.
7. Freeze memory records the implemented behavior.
8. Startup context is refreshed after freeze.
```
