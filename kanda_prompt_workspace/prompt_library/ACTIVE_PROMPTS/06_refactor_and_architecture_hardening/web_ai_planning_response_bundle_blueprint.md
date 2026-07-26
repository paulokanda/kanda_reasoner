# Web AI Planning Response Bundle Blueprint

Prompt code: `KPR-06-002`
Prompt id: `web_ai_planning_response_bundle_blueprint`
Version: 2.0.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this blueprint to package one already-reasoned KPR-06-001 planning response
for Imported Web AI Version intake. It owns the reusable payload and bundle
profile, not architecture reasoning and not general patch governance.

The canonical default is a ZIP containing the exact marker-wrapped planning
payload. The identical payload must also be repeated in chat for direct
`Panel 4: Proposed split plan` paste fallback.

## Authority boundary

- KPR-06-001 decides the bounded planning response.
- KPR-06-002 defines the Imported Web AI payload and bundle profile.
- current Class 05 owners define package, Install, Validate, terminal, evidence,
  and rollback mechanics.
- current freeze owners define Preview and explicit Confirm and Write.

This blueprint may describe required artifacts but must not invent competing
implementation, delivery, or freeze doctrine.

## Required input

Require the exact current planning package and exact response identity:

```text
source_content_hash
base_plan_hash
current_plan
architecture_review
known_helper_modules
known_movable_symbols
improvement_objective
imported_web_ai_version_install_contract
KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN ... END
```

Fail closed when either hash, the current plan, or the exact payload is missing.

## Payload contract

The file `pending_imported_web_ai_plan.txt` must contain exactly one complete
block:

```text
KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN
{ "schema_version": "2.0", "source_content_hash": "...", "base_plan_hash": "..." }
KANDA_WEB_AI_PLANNING_RESPONSE_END
```

The full JSON must satisfy the KPR-06-001 schema. There must be exactly one
begin marker and exactly one end marker.

## Canonical bundle profile

```text
<bundle_name>.zip
├── INSTALL.ps1
├── VALIDATE.ps1
├── FREEZE.ps1
├── KANDA_FREEZE_HINT.json
├── bundle_manifest.json
└── pending_imported_web_ai_plan.txt
```

The required files are a profile for the existing imported-plan workflow. Their
execution contracts remain governed by current Class 05 and freeze owners.

## Stable bundle naming

Use lowercase snake case and a version suffix:

```text
kanda_web_ai_plan_<target_short_name>_<bounded_purpose>_v1.zip
```

Do not reuse a target-specific example name for another module.

## Installer profile

`INSTALL.ps1` must be limited to the external pending-plan artifact. It must:

1. accept mandatory `-ProjectRoot`;
2. normalize the project root and derive its drive and project name;
3. derive the external imported-plan destination supplied by the current
   contract;
4. create only that external destination directory;
5. read the packaged payload as UTF-8;
6. count literal markers with `Regex.Matches` and `Regex.Escape`;
7. require exactly one begin and one end marker;
8. write UTF-8 without BOM;
9. verify exact installed-copy equality;
10. print the installed path and next Planner steps.

It must not patch KANDA source, selected-project source, Workbench state, freeze
memory, or Error Memory Lessons.

Mandatory literal marker counting:

```powershell
$BeginCount = [regex]::Matches(
    $PayloadText,
    [regex]::Escape($BeginMarker)
).Count

$EndCount = [regex]::Matches(
    $PayloadText,
    [regex]::Escape($EndMarker)
).Count
```

Do not use `String.Split(markerString)` for literal marker counts.

## Validation profile

`VALIDATE.ps1` must fail closed and verify at least:

```text
BUNDLE_REQUIRED_FILES: PASS
PAYLOAD_SHA256: PASS
KANDA_FREEZE_HINT_KIND_CONTRACT: PASS
MARKER_AND_JSON_CONTRACT: PASS
SOURCE_AND_BASE_PLAN_IDENTITY: PASS
ACTION_LIST_TYPES: PASS
ARCHITECTURE_ANSWERS_COMPLETE: PASS
BOUNDED_ACTION_IDENTITY: PASS
INSTALLED_COPY_EQUALS_PACKAGED_PAYLOAD: PASS
IMPORTED_WEB_AI_PLAN_BUNDLE: PASS
STATUS: IN_SYNC
```

Validation must prove that the packaged and installed payloads are identical,
the two identity hashes are exact, every action list is a list, every required
architecture answer exists, and no action escapes the supplied known-object
contract.

## Freeze evidence profile

`FREEZE.ps1` is evidence preparation only. It may:

- require successful validation evidence;
- read the root-level `KANDA_FREEZE_HINT.json`;
- merge evidence through the current freeze-hint intake contract;
- print the next local Preview step.

It must not write canonical frozen memory directly. Final freeze remains:

```text
Freeze Feature After Update
-> Preview Freeze Entry
-> explicit human Confirm and Write
```

## Freeze hint profile

`KANDA_FREEZE_HINT.json` must use the canonical kind and current feature data:

```json
{
  "schema_version": "1.0",
  "kind": "kanda_freeze_hint",
  "feature_id": "<current imported-plan feature>",
  "feature_title": "<current imported-plan title>",
  "primary_box": "06_refactor_and_architecture_hardening",
  "validated_files": ["pending_imported_web_ai_plan.txt"],
  "validation_evidence_summary": "<local validation evidence>"
}
```

Do not put project-specific frozen memory inside `project_freeze_ledger`.

## Bundle manifest profile

`bundle_manifest.json` records exact payload identity, required member names,
source hash, base-plan hash, and current schema version. It is a delivery record,
not architecture authority.

## User-visible delivery order

Return in this order:

1. bounded planning-result summary;
2. ZIP artifact;
3. ZIP SHA-256;
4. exact expected location;
5. current Class 05 Install code;
6. current Class 05 Validate code;
7. freeze-evidence preparation only after validation passes;
8. exact marker-wrapped payload for Panel 4 paste fallback.

## Beginner-safe terminal rules

- start from a clean PowerShell prompt;
- avoid an unnecessary outer `& {}` wrapper;
- do not use `else` or `elseif` in generated KANDA terminal wrappers;
- preserve phase-specific error provenance;
- never close the user's terminal;
- do not proceed to freeze evidence after failed validation.

## Do not regress

- Keep ZIP as the canonical imported-plan path.
- Keep the chat payload byte-identical to the packaged payload.
- Keep installer scope limited to the external pending-plan artifact.
- Keep exact source and base-plan identity.
- Keep KPR-06-001 as reasoning owner.
- Keep Class 05 and freeze owners authoritative for mechanics and final writes.
