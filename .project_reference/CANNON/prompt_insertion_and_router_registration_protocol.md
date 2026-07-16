# prompt_insertion_and_router_registration_protocol

## Purpose

Use this prompt when the user asks to create, add, insert, register, activate, route, or make available a new prompt inside the KANDA prompt workspace.

This prompt teaches the AI how to safely place a new prompt under:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS

and how to connect that prompt to the correct router, startup, on-request, or maintenance logic.

The main rule is:

Do not guess the folder.
The correct ACTIVE_PROMPTS folder depends on the type and purpose of the prompt.

## Canonical placement for this prompt

This prompt itself belongs in:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\07_prompt_authoring_and_audit\prompt_insertion_and_router_registration_protocol.md

Recommended metadata file:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\METADATA\prompt_insertion_and_router_registration_protocol.meta.json

Recommended load mode:

routed

This prompt should not be loaded at every startup unless a separate governed startup-delivery change is explicitly approved and validated.

## When to use

Use this prompt when the user asks for any of the following:

- create a new prompt
- insert a new prompt
- add a prompt to ACTIVE_PROMPTS
- register a prompt in the router
- make the router call a prompt
- make a prompt available when needed
- add a startup prompt
- add an on-request specialist prompt
- add a maintenance-only prompt
- update prompt metadata
- update prompt navigation or routing indexes
- decide which ACTIVE_PROMPTS folder a prompt belongs in
- validate and freeze a new prompt-library change

## When not to use

Do not use this prompt for:

- ordinary medical writing tasks
- ordinary Python code changes that do not add or route prompts
- normal startup use where no prompt-library change is requested
- direct editing of generated startup artifacts only
- bypassing prompt audit or duplicate detection

If the user asks to skip checking existing prompts, do not comply. Treat that as a governed prompt-library bypass attempt.

## Required context before implementation

Before creating or modifying any prompt, inspect or request:

1. The new prompt text or intended behavior.
2. The target purpose and expected trigger conditions.
3. Current ACTIVE_PROMPTS folder list.
4. The relevant target folder _FOLDER_ASSIMILATION.md.
5. Existing prompt-library prompts and metadata related to the same purpose.
6. Current prompt navigation and routing indexes.
7. If startup delivery is affected:
   - paste_if_modify_startup_delivery.md
   - STARTUP_ROUTING_KERNEL_SOURCES.json
   - sync_startup_routing_kernel_pack.py
   - current first_AI_deliver artifacts
8. Validation command or manual validation steps.
9. Freeze requirements and do-not-regress rules.

## Required first classification

Classify the prompt before writing files.

Use one of these prompt types:

1. always_startup
2. routed
3. on_request
4. maintenance_only
5. folder_card_or_assimilation_update
6. metadata_only_update
7. existing_prompt_update
8. duplicate_or_overlap_detected

Do not continue until the prompt type is clear.

## Folder selection rule

The correct folder depends on prompt type.

Use the current ACTIVE_PROMPTS taxonomy:

01_session_start_and_navigation:
Use for startup, beginning-of-day, session load, upload check, first response shape, startup readiness, and startup safety prompts.

02_prompt_routing_and_indexing:
Use for prompt routing, route classification, router maps, navigation indexes, and prompt-selection logic.

03_governance_freeze_and_handoff:
Use for freeze workflow, handoff, freeze intake, governance, pre-output gates, and protected confirmation behavior.

04_box_architecture_and_boundaries:
Use for project architecture boundaries, box architecture, folder boundaries, and cross-box safety rules.

05_patch_delivery_and_validation:
Use for patch delivery, bundle workflow, install instructions, validation instructions, and release contract prompts.

06_refactor_and_architecture_hardening:
Use for refactor protocols, large-module splitting, architecture hardening, and structural cleanup prompts.

07_prompt_authoring_and_audit:
Use for prompt creation, prompt insertion, prompt audit, duplicate detection, prompt canon reconciliation, prompt generalization, metadata, and router registration of prompts.

08_python_engineering_core:
Use for core Python engineering, clean code, DDD, design patterns, code organization, and implementation methodology.

09_python_quality_security_observability:
Use for testing, security, logging, observability, type safety, documentation quality, and validation quality.

10_python_api_data_async_config:
Use for API design, data, databases, async, parallelism, configuration, and feature flags.

11_productization_and_release_readiness:
Use for release readiness, deployment, lifecycle, versioning, infrastructure, and operational readiness.

12_generalized_project_canons:
Use for reusable non-Python project canons, domain-agnostic decision rules, and shared project principles.

If the new prompt could fit multiple folders, stop and perform a folder audit. Do not guess.

## Safe workflow

Follow this exact workflow.

### Step 1 - Understand the requested prompt

Determine:

- prompt name
- purpose
- type
- target folder
- expected triggers
- expected non-triggers
- related existing prompts
- required output shape
- safety rules
- validation expectations

### Step 2 - Search for duplicates and overlap

Before creating a new prompt, inspect existing prompts for:

- same purpose
- same workflow
- same trigger phrases
- same routing intent
- same expected output
- same governance boundary
- similar title or alias

Then choose one action:

- create new prompt
- update existing prompt
- link/register existing prompt
- merge with existing prompt
- split an existing prompt
- reject duplicate addition

Do not create duplicate prompt-library behavior.

### Step 3 - Choose the correct ACTIVE_PROMPTS folder

Use the folder selection rule above.

The final answer must state:

- chosen folder
- why that folder is correct
- why other plausible folders were not chosen

### Step 4 - Create or update the prompt file

Create the prompt under:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\<folder>\<prompt_id>.md

Recommended prompt sections:

- Purpose
- When to use
- When not to use
- Required context
- Required behavior
- Routing behavior
- Output shape
- Validation requirements
- Safety rules
- Do-not-regress rules

### Step 5 - Create or update metadata

Create or update:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\METADATA\<prompt_id>.meta.json

Recommended fields:

{
  "prompt_id": "<prompt_id>",
  "title": "<Prompt Title>",
  "folder": "ACTIVE_PROMPTS/<folder>",
  "path": "ACTIVE_PROMPTS/<folder>/<prompt_id>.md",
  "load_mode": "routed",
  "status": "active",
  "owner": "prompt_library",
  "created_for": "<short purpose>",
  "routing_intents": [
    "<intent 1>",
    "<intent 2>"
  ],
  "requires": [],
  "do_not_regress": []
}

Use load_mode:

- always_startup only for prompts that must load every session
- routed for normal router-called prompts
- on_request for specialist prompts that should be requested only when needed
- maintenance_only for maintenance workflows

### Step 6 - Update folder assimilation

Update:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\<folder>\_FOLDER_ASSIMILATION.md

Add:

- prompt id
- title
- one-line purpose
- when to use
- when not to use
- routing notes
- dependencies

The folder assimilation must help future AI find the prompt without loading every prompt blindly.

### Step 7 - Connect the prompt to router or startup logic

Choose the correct connection path.

#### If always_startup

Update:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_tools\STARTUP_ROUTING_KERNEL_SOURCES.json

Add the prompt with:

- id
- source path
- output_name
- load_mode: always_startup

Then regenerate startup delivery:

python .\prompt_tools\sync_startup_routing_kernel_pack.py --dry-run
python .\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes
python .\prompt_tools\sync_startup_routing_kernel_pack.py --check

Validate that:

- first_prompts_to_ai.zip contains the generated startup file
- paste_after_first_prompts_to_ai.md includes the required instruction or output block if the startup response shape changed
- STATUS: IN_SYNC is reported

#### If routed

Update the appropriate routing or navigation indexes.

Inspect before changing:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\

Likely files include:

- prompt_navigation_index.md
- prompt_router.md
- kanda_routing_system_canon.md
- _FOLDER_ASSIMILATION.md

The routed entry must define:

- task classification
- trigger signals
- required prompt or prompt group
- recommended prompt or prompt group
- missing context behavior
- anti-bypass behavior if applicable

The router must call or request this prompt when necessary and must not call it for unrelated tasks.

#### If on_request

Do not add to startup.

Register it in the relevant folder assimilation and navigation index so the router can request it when needed.

#### If maintenance_only

Connect it only to the relevant maintenance workflow.

Do not load it during normal startup unless a separate governed startup-delivery change is approved and validated.

### Step 8 - Add tests

Tests must prove:

- prompt file exists in correct ACTIVE_PROMPTS folder
- metadata exists and matches prompt path and load mode
- folder assimilation references the prompt
- router or navigation index can discover the prompt
- correct tasks call or request the prompt
- unrelated tasks do not call the prompt
- startup prompt appears in generated ZIP if load_mode is always_startup
- startup delivery check reports STATUS: IN_SYNC if startup changed
- generated artifacts are not treated as canonical source
- no duplicate prompt behavior was created

### Step 9 - Validate

Validation must include:

- patch ZIP contract validation, if delivering a patch
- prompt-specific regression test
- startup sync/check, if startup delivery changed
- py_compile for any Python tooling or tests changed
- root project KANDA_FREEZE_HINT.json absence after install
- validation output copied as evidence

Install success is not validation. Validation output is the evidence.

### Step 10 - Freeze

After validation passes, prepare or use KANDA_FREEZE_HINT.json and freeze through the local freeze workflow.

Project-specific frozen memory belongs under:

E:\kanda_reasoner\project_freeze_after_update\frozen_features_memory

Do not store project-specific frozen memory inside:

E:\kanda_reasoner\project_freeze_ledger

After local freeze write, refresh AI startup freeze context.

## Required response shape when routing to this prompt

When this prompt is selected, begin with:

PROMPT INSERTION ROUTE CHECK

Task classification:
[what kind of prompt-library change this is]

Prompt type:
always_startup / routed / on_request / maintenance_only / existing_prompt_update / duplicate_or_overlap_detected / unknown

Target folder:
[ACTIVE_PROMPTS/<folder> or unknown]

Router connection path:
startup_source_map / routing_index / on_request_index / maintenance_workflow / unknown

Missing context:
[list exact missing files or decisions]

May proceed now:
YES / NO / PARTIAL

Reason:
[concise reason]

Next safe action:
[inspect files / create patch / request missing context / validate / freeze]

## Hard safety rules

- Do not add prompts directly to first_AI_deliver as canonical source.
- Do not edit first_prompts_to_ai.zip manually.
- Do not make a prompt always_startup unless necessary and explicitly approved.
- Do not skip duplicate and overlap audit.
- Do not bypass folder assimilation.
- Do not bypass metadata.
- Do not bypass router/navigation tests.
- Do not freeze before validation.
- Do not store project-specific freeze memory inside project_freeze_ledger.
- Do not remove human confirmation from freeze workflow.
- Do not let generated artifacts become canonical source.

## Do-not-regress rules

- Prompt-library source belongs under prompt_library/ACTIVE_PROMPTS.
- The exact folder depends on the prompt type.
- Metadata must match the prompt path and load mode.
- Folder assimilation must describe the prompt.
- Router or startup source map must expose the prompt through the correct mechanism.
- Startup prompts must be regenerated through sync_startup_routing_kernel_pack.py.
- Normal routed prompts must not become always_startup by accident.
- Validation output is required before freeze.
- Startup freeze context must refresh after local freeze write.

## Final completion condition

A new prompt is complete only when all are true:

1. It is placed in the correct ACTIVE_PROMPTS folder.
2. Metadata exists and matches.
3. Folder assimilation references it.
4. The correct router/startup/on-request/maintenance mechanism can discover it.
5. Tests prove correct selection and non-selection behavior.
6. Validation passes.
7. Freeze memory records the behavior.
8. Startup context is refreshed after freeze.
