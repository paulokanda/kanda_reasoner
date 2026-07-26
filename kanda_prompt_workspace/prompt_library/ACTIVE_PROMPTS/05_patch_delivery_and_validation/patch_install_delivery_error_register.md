---
prompt_id: patch_install_delivery_error_register
prompt_code: KPR-05-001
title: Patch Install Delivery Active Regression Index
version: 2.0
status: active
load_type: conditional_required
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave3b-specialist-startup-bridges-v1
---

# Patch Install Delivery Active Regression Index

## Purpose

This is the compact Class 05 index of active patch-install and delivery
regression classes. It preserves the prompt identity while routing each risk to
its current behavioral owner, focused validator, and relevant Error Memory.

It is required before patch-related output. It is not an append-only traceback
log, installer implementation, terminal contract, freeze schema, or Error Memory
store.

## Activation

Load this prompt when a response will deliver or repair a patch ZIP, installer,
validator, freeze workflow, validation-evidence handoff, or Error Memory payload.
The always-startup `daily_patch_delivery_guardrails` bridge routes here.

## Registry contract

Each active record uses:

```text
PIR ID:
Title:
Status:
Regression category:
Blocking predicate:
Current owner prompt:
Focused validator:
Expected rejection marker:
Expected success marker:
Relevant Error Memory lesson IDs:
Supersedes:
Superseded by:
Last verified source fingerprint:
Last verified date:
```

Long tracebacks, full correction narratives, complete PowerShell, and complete
lesson schemas belong to durable validation evidence or Error Memory, not this
index.

## Active regression classes

### PIR-001 - Governed ZIP staging

- Status: active
- Regression category: GOVERNED_ZIP_STAGING
- Blocking predicate: A delivery bypasses the current root-drive staging and
  project-derived transient-root contract.
- Current owner prompt: `implementation_and_delivery_protocol`
- Focused validator: `scripts/validate_ai_response_patch_delivery_contract.py`
- Expected rejection marker: `PATCH_DELIVERY_BLOCKED`
- Expected success marker: `PATCH_DELIVERY_GATE: PASS`

### PIR-002 - Root ZIP cleanup

- Status: active
- Regression category: ROOT_ZIP_CLEANUP
- Blocking predicate: The delivery leaves an unintended root-drive duplicate
  after verified staging.
- Current owner prompt: `pre_output_contract_gates`
- Focused validator: `scripts/validate_ai_response_patch_delivery_contract.py`
- Expected rejection marker: `ROOT_ZIP_CLEANUP_MISSING`
- Expected success marker: `PATCH_DELIVERY_GATE: PASS`

### PIR-003 - Staged-only extraction

- Status: active
- Regression category: STAGED_ONLY_EXTRACTION
- Blocking predicate: Installation extracts from an unverified or non-staged ZIP.
- Current owner prompt: `bundle_gated_development_workflow`
- Focused validator: `scripts/validate_ai_response_patch_delivery_contract.py`
- Expected rejection marker: `STAGED_EXTRACTION_REQUIRED`
- Expected success marker: `PATCH_DELIVERY_GATE: PASS`

### PIR-004 - No Downloads or Desktop fallback

- Status: active
- Regression category: NO_DOWNLOADS_DESKTOP_FALLBACK
- Blocking predicate: A generic Downloads/Desktop search replaces the governed
  project-drive delivery contract.
- Current owner prompt: `implementation_and_delivery_protocol`
- Focused validator: `scripts/validate_ai_response_patch_delivery_contract.py`
- Expected rejection marker: `UNAPPROVED_DOWNLOAD_FALLBACK`
- Expected success marker: `PATCH_DELIVERY_GATE: PASS`

### PIR-005 - Critical path null guard

- Status: active
- Regression category: CRITICAL_PATH_NULL_GUARD
- Blocking predicate: A derived path reaches a filesystem operation before a
  non-empty existence or authority check.
- Current owner prompt: `implementation_and_delivery_protocol`
- Focused validator: `tools/validate_prompt_audit_wave3b_specialist_startup_bridges_v1.py`
- Expected rejection marker: `CRITICAL_PATH_GUARD_MISSING`
- Expected success marker: `WAVE3B_PATCH_REGRESSION_INDEX: PASS`

### PIR-006 - Terminal footer contract

- Status: active
- Regression category: TERMINAL_FOOTER_CONTRACT
- Blocking predicate: A user-facing terminal block diverges from the current
  install-success or non-install cleanup contract.
- Current owner prompt: `terminal_cleanup_contract`
- Focused validator: `tools/validate_terminal_cleanup_contract_startup_bridge_v1.py`
- Expected rejection marker: `TERMINAL_CLEANUP_CONTRACT_MISMATCH`
- Expected success marker: `VALIDATION OK: terminal-cleanup-contract-startup-bridge-v1`

### PIR-007 - No isolated ZIP delivery

- Status: active
- Regression category: NO_ISOLATED_ZIP_DELIVERY
- Blocking predicate: A ZIP link is shown without the same-response install,
  validation, and freeze or Error Memory handling required by the routed task.
- Current owner prompt: `pre_output_contract_gates`
- Focused validator: `scripts/validate_ai_response_patch_delivery_contract.py`
- Expected rejection marker: `ISOLATED_ZIP_DELIVERY_BLOCKED`
- Expected success marker: `PATCH_DELIVERY_GATE: PASS`

### PIR-008 - Exact final ZIP contract

- Status: active
- Regression category: EXACT_FINAL_ZIP_CONTRACT
- Blocking predicate: The exact final archive has not passed the canonical ZIP
  member and manifest contract.
- Current owner prompt: `bundle_gated_development_workflow`
- Focused validator: `scripts/validate_patch_zip.py`
- Expected rejection marker: `ZIP CONTRACT ERROR`
- Expected success marker: `ZIP CONTRACT: PASS`

### PIR-009 - Freeze sidecar is delivery metadata

- Status: active
- Regression category: FREEZE_SIDECAR_NOT_INSTALLED
- Blocking predicate: `KANDA_FREEZE_HINT.json` is installed as canonical project
  source or treated as a completed freeze.
- Current owner prompt: `freeze_code_intake_and_form_protocol`
- Focused validator: `tools/validate_prompt_audit_wave3b_specialist_startup_bridges_v1.py`
- Expected rejection marker: `FREEZE_SIDECAR_SOURCE_LEAK`
- Expected success marker: `WAVE3B_PATCH_REGRESSION_INDEX: PASS`

### PIR-010 - Validation evidence safe output

- Status: active
- Regression category: VALIDATION_EVIDENCE_SAFE_OUTPUT
- Blocking predicate: Validation evidence is truncated, misencoded, lacks current
  feature identity, or is claimed without local execution.
- Current owner prompt: `pre_output_contract_gates`
- Focused validator: `tools/validate_prompt_audit_wave3b_specialist_startup_bridges_v1.py`
- Expected rejection marker: `VALIDATION_EVIDENCE_UNSAFE`
- Expected success marker: `WAVE3B_PATCH_REGRESSION_INDEX: PASS`

### PIR-011 - Error Memory payload validity

- Status: active
- Regression category: ERROR_MEMORY_PAYLOAD_VALIDITY
- Blocking predicate: A corrected-error delivery includes duplicate, invalid,
  unredacted, or unsupported active lesson content.
- Current owner prompt: `error_memory_ai_formulary_startup_canon`
- Focused validator: `tools/validate_prompt_audit_wave3b_specialist_startup_bridges_v1.py`
- Expected rejection marker: `ERROR_MEMORY_INTAKE_BLOCKED`
- Expected success marker: `WAVE3B_ERROR_MEMORY_ADMISSION_CANON: PASS`

## Update rule

Do not append a narrative entry automatically. A new or changed PIR requires:

1. a verified recurring delivery risk;
2. one current behavioral owner;
3. a focused validator or explicit new-test obligation;
4. an Error Memory admission decision;
5. an exact source fingerprint and verification date before freeze;
6. replacement or supersession of conflicting records.

Duplicate IDs, missing IDs, and multiple meanings for one ID are invalid.

## Failure behavior

If a patch-related response cannot identify the active regression classes and
owners, return:

```text
PATCH REGRESSION INDEX BLOCKED
Unresolved PIR classes:
Missing owner or validator:
Relevant Error Memory needed:
Next safe action:
May release patch: NO
```

## Scope exclusions

This index does not contain:

- full tracebacks or long root-cause narratives;
- complete correct-fix narratives;
- complete terminal or PowerShell templates;
- Error Memory or freeze schemas;
- historical patch-by-patch append logs;
- a second patch delivery engine.

## Do-not-regress rules

- Keep the identity unique under Class 05.
- Keep load type conditional-required, not always-startup.
- Keep the daily Class 01 guardrail as the startup bridge.
- Keep one meaning per PIR ID.
- Route behavior to current owners and evidence to current validators.
- Unknown or ownerless regression classes fail closed.
