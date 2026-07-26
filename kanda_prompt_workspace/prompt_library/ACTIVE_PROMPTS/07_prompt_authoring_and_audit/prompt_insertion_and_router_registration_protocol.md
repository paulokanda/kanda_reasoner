---
prompt_code: KPR-07-001
prompt_id: prompt_insertion_and_router_registration_protocol
title: Prompt Insertion and Router Registration Protocol
version: 2.0
status: active
load_type: routed
owner_box: 07_prompt_authoring_and_audit
---

# Prompt Insertion and Router Registration Protocol

## Purpose

Apply an already approved Prompt Library lifecycle decision through the smallest atomic source, metadata, folder, and routing mutation.

This prompt is the Class 07 implementation orchestrator. It consumes upstream decisions; it does not repeat audit, reconciliation, identity, routing architecture, delivery, or freeze doctrine.

## Required upstream decisions

Do not mutate files until all applicable evidence is current:

- completed prompt audit;
- Prompt Canon Reconciliation decision;
- Project-Specific Generalization record when external material is involved;
- Prompt Identity Decision, including `NO_CODE_REQUIRED` when appropriate;
- relevant target `_FOLDER_ASSIMILATION.md`;
- exact current source, metadata, routes, and fingerprints;
- Brick Wall authorization for the current operation;
- relevant compact Error Memory lessons;
- exact changed-file and validation plan.

Missing or stale evidence blocks mutation.

## Supported mutation types

Use one primary mutation type:

- `CREATE`
- `UPDATE`
- `LINK_OR_REGISTER`
- `MOVE_OR_RECLASSIFY`
- `SPLIT`
- `MERGE`
- `DEPRECATE`
- `DELETE_AFTER_MIGRATION`
- `METADATA_ONLY`
- `ROUTING_ONLY`

Prompt load type is a separate field: `always_startup`, `routed`, `on_request`, or `maintenance_only`.

## Immediate freshness gate

Immediately before writing, verify that:

- target source and metadata fingerprints still match the inspected snapshot;
- the selected prompt code remains available;
- target folder and folder card remain current;
- routing and index files have not changed;
- generated artifacts are still classified as outputs;
- operation identity, project root, and authorization still match.

Any mismatch resets authorization and blocks the write.

## Exact changed-file inventory

Declare:

- one primary box;
- every source and metadata file to change;
- bounded supporting routing or generator touches;
- generated artifacts expected to change;
- files explicitly out of scope;
- validator ownership for every changed file;
- rollback boundary.

Do not mutate an undeclared file.

## Atomic implementation

1. Stage all proposed files in an isolated transaction area.
2. Validate source identity, metadata schema, folder placement, and route decisions before replacing active files.
3. Apply prompt source and metadata together.
4. Update current folder, group, navigation, and route owners only when required by the approved mutation.
5. For always-startup changes, dispatch to the current startup-delivery maintenance owner and canonical generator; never edit generated ZIP contents as source.
6. Regenerate generated distributions only through their current generator.
7. Run mutation-specific focused validation before declaring the transaction successful.
8. Roll back all changed files if any required step fails.
9. Re-running the same approved operation must be idempotent and must not duplicate entries, aliases, routes, or metadata arrays.

## Route integration by load type

- `always_startup`: update canonical startup sources and source map through the startup-maintenance protocol, then regenerate and check startup delivery.
- `routed`: update the current routing owner and exact addressability metadata.
- `on_request`: ensure prompt ID/path discovery and companions are correct; do not force startup loading.
- `maintenance_only`: restrict selection to the governed maintenance trigger and keep it out of normal startup.

Class 02 owns routing architecture and response schemas. This protocol only applies the approved registration through current public contracts.

## Metadata implementation

Use the current Prompt Library metadata schema. Source and metadata must agree on:

- prompt code, when assigned;
- prompt ID;
- display name;
- filename and category;
- version;
- status and load type;
- owner box;
- canonical path;
- aliases;
- triggers and companions;
- source stage and update reason.

Do not create a competing metadata schema.

## Validation by mutation type

At minimum verify:

- source/metadata identity and version alignment;
- unique prompt code and aliases when applicable;
- exact folder and canonical path;
- no duplicate semantic owner introduced;
- current folder/group/navigation registration;
- no stale or orphaned route;
- no generated artifact used as source;
- changed-file-to-validator coverage;
- module-size and encoding rules for touched code or prompt files;
- startup dry run, sync, and post-sync check when startup delivery is affected;
- exact final patch ZIP contract when an installable release is produced.

Validators must enforce durable behavior and minimum compatibility, not incidental prose, exact phrase counts, invented JSON keys, or permanent equality to one release version.

## Implementation result record

Return:

- operation and feature IDs;
- primary box and supporting touches;
- mutation type and load type;
- upstream decision IDs;
- source snapshot and pre-write freshness result;
- exact changed files;
- generated artifacts;
- validation map and current results;
- rollback status;
- unresolved blockers;
- may build patch: `YES/NO`;
- may claim validation: `YES/NO`;
- may freeze: `YES/NO`.

## Downstream handoff

- Patch packaging and terminal delivery: current Class 05 and Pre-Output owners.
- Freeze intake and freeze form: current freeze owners after local validation.
- Preview remains read-only; Confirm and Write requires explicit human confirmation.
- Project-specific frozen memory remains under the selected project support root, never `project_freeze_ledger`.

## Non-authorization rule

Loading this prompt does not authorize a Prompt Library mutation. Only a current Brick Wall authorization bound to the exact source snapshot and operation permits writes.
