---
prompt_id: implementation_and_delivery_protocol
prompt_code: KPR-05-003
title: Implementation and Delivery Protocol
version: 2.1
status: active
load_type: routed
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave5a-patch-lifecycle-core-v1
---

# Implementation and Delivery Protocol

## Purpose

Define the surgical construction and installer-preparation contract for an
already authorized release. This prompt owns payload planning, exact baseline
admission, backup, controlled mutation, rollback, and installed-file
verification. It does not own implementation authorization, final response
rendering, receiver classification, terminal footers, freeze writes, or Error
Memory schemas.

## Activation gate

Load only after Brick Wall has admitted the verified problem and authorized the
bounded implementation, and `bundle_gated_development_workflow` has classified
an installable release as applicable.

Do not use for analysis-only work, speculative roadmap writing, or direct source
mutation without a governed release.

## Release-owner boundary

For `KANDA_TOOL_RELEASE`, this protocol may define the KANDA patch payload,
installer, rollback, and installed-hash checks. For `EXTERNAL_PROJECT_RELEASE`,
KANDA Reasoner is observer-only: the payload, installer, validator, release
contract, rollback, and interpreter belong to the Project or release itself. Do
not import KANDA Tool validators into the Project, do not request KANDA Tool
source archives, and do not make KANDA runtime availability a release condition.

## Required inputs

```text
SURGICAL DELIVERY INPUT
Feature ID:
Primary box:
Supporting touches:
Project root:
Project-linked transient root:
Exact current source fingerprints:
Changed files:
New files:
Governed deletions:
Public contracts affected:
Relevant Error Memory lessons:
Active PIR classes:
Required validators:
Receiver type:
Freezeable release: YES / NO
Write authorization evidence:
```

## Payload and release metadata

Separate installable project payload from root-level release metadata.

- Payload members map to project-relative destinations and appear exactly once
  in the install manifest.
- Root-level release controls may include installer, validator, readme, manifest,
  and freeze sidecar. They are not installed as canonical project source unless
  explicitly declared as payload.
- `KANDA_FREEZE_HINT.json` is release metadata, not a completed freeze and not an
  installable source member.
- Every changed file maps to at least one focused validator or an explicit
  evidence-based non-applicability record.

For a KANDA Tool release, the exact final ZIP must pass the KANDA canonical ZIP contract. For an external Project release, the exact final ZIP must pass the Project/release-owned contract; KANDA `scripts/validate_patch_zip.py` is not a fallback.

## Archive-member safety

Fail closed for:

- empty, absolute, drive-qualified, UNC, or traversal paths;
- raw backslash separators in archive metadata;
- duplicate, case-folded, file-directory, or destination collisions;
- links, reparse points, special files, or undeclared payload members;
- a freeze sidecar duplicated inside the payload namespace.

Use the least-normalized archive name available for lexical security checks.

## Baseline fingerprint policy

For every replacement or deletion declare:

- exact expected predecessor SHA-256 values;
- exact already-current SHA-256 value;
- whether absence is permitted;
- exact destination path and operation.

Accept only a manifest-declared predecessor, an already-current final state, or
an explicitly allowed absent state. Reject an unknown third hash before any
mutation. Never add a hash to an allowlist without source-level comparison and a
recorded compatibility decision.

## Governed staging

Resolve the project provider path first, derive the drive root from the resolved
project, and derive the transient work folder as
`<project_drive>/<project_name>_delete_after_daily_work`.

For user-delivered ZIP installation:

1. look first at the project drive root for the named ZIP;
2. verify its exact expected SHA-256;
3. copy or move it into the project-linked transient folder;
4. verify the staged ZIP before deleting the root-drive copy;
5. extract and install only from the staged ZIP;
6. reject Downloads/Desktop fallback searches.

Every critical path must be non-empty, authority-checked, and existence-checked
before a filesystem operation uses it.

## Transaction and backup

1. Complete preflight for every operation before changing any destination.
2. Create a surgical backup for each existing replacement or deletion.
3. Apply new files, replacements, and deletions as one bounded transaction.
4. Verify exact final hashes and required absence states.
5. Run declared compilation and focused validation.
6. Regenerate or check derived startup delivery only through its canonical
   generator when the release changes prompt sources or startup inputs.
7. On any failure, restore all changed and deleted files and verify rollback.

Do not report installation success until final installed-state verification
passes.

## Validation and output dispatch

- Package/disposable validation may prove package behavior but does not prove the
  user's live Windows installation.
- Windows-local validation evidence must identify the feature, ZIP, source
  state, validator revision, command, exit status, and success markers.
- `pre_output_contract_gates` decides whether the artifact may be emitted.
- `terminal_cleanup_contract` owns interactive PowerShell cleanup.
- The receiver owner decides intake, extraction, and destination behavior.
- Freeze and Error Memory owners decide conditional post-validation actions.

## Non-authorization statement

This protocol cannot authorize coding, artifact release, validation claims, or
freeze. It may construct a release only while current Brick Wall and specialist
evidence permit it.

## Version history

- 2.1: scoped KANDA patch construction to KANDA Tool releases and made external Project delivery Project-owned and KANDA-independent.
- 2.0: narrowed to surgical patch construction, exact baseline admission,
  archive safety, staging, transaction, and rollback; delegated all final gates.
- 1.x: historical end-to-end implementation and delivery mega-protocol.
