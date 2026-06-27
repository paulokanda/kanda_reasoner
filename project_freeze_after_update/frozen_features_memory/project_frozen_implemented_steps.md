# project frozen implemented steps

Project: `kanda_reasoner`

Ledger version: `1.9-structured-entries`

Canonical source: this Markdown ledger plus structured detailed files in `entries/`.

JSON mirror: deferred until a validation/generation script exists.

## current frozen baselines

| freeze id | date | project box | status | detailed entry |
|---|---:|---|---|---|
| `freeze-20260612-phase7a-v24` | 2026-06-12 | `kanda_prompt_workspace/startup_delivery_system` | frozen operational baseline | `entries/freeze-20260612-phase7a-v24.md` |
| `freeze-20260612-project-freeze-ledger-v1` | 2026-06-12 | `project_freeze_ledger` | superseded historical baseline | `entries/freeze-20260612-project-freeze-ledger-v1.md` |
| `freeze-20260612-project-freeze-ledger-v18` | 2026-06-12 | `project_freeze_ledger` | current frozen dynamic-path baseline | `entries/freeze-20260612-project-freeze-ledger-v18.md` |
| `freeze-20260614-t9t013-prompt-authoring-lifecycle-routing-v1` | 2026-06-14 | `kanda_prompt_workspace/prompt_authoring_routing_kernel` | frozen prompt-authoring lifecycle and RG-015 exact routing override | `entries/freeze-20260614-t9t013-prompt-authoring-lifecycle-routing-v1.md` |
| `freeze-20260614-freeze-memory-exposure-cli-v1` | 2026-06-14 | `project_freeze_ledger/freeze_memory_dynamic_exposure_bridge` | frozen read-only freeze-memory exposure CLI v1 | `entries/freeze-20260614-freeze-memory-exposure-cli-v1.md` |

## structured entry requirement

Every file in:

```text
project_freeze_ledger/entries/
```

must start with strict YAML-like frontmatter containing:

```text
freeze_id
box
status
date
entry
protected_paths
do_not_touch_summary
superseded_by
```

Run the validator after any freeze ledger change:

```text
project_freeze_ledger/freeze_tools/validate_freeze_entry_frontmatter.py
```

## active do-not-touch summary

### startup delivery system

Frozen baseline:

```text
freeze-20260612-phase7a-v24
```

Protected paths are declared in the entry frontmatter:

```text
project_freeze_ledger/entries/freeze-20260612-phase7a-v24.md
```

Core invariant:

```text
maps first, not all prompts
```

Startup delivery invariant:

```text
first_prompts_to_ai.zip contains stable 00_START_HERE_FOR_AI.md
certificate data stays in file content and manifest
send_ai_just_if_modify_startup_delivery.md stays outside the normal startup ZIP
governed startup-delivery changes require the maintenance file before implementation
```

### project freeze ledger

Current frozen baseline:

```text
freeze-20260612-project-freeze-ledger-v18
```

Historical baseline:

```text
freeze-20260612-project-freeze-ledger-v1
```

Protected paths are declared in the entry frontmatter:

```text
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v18.md
```

Freeze ledger invariant:

```text
one master dashboard + one detailed entry per meaningful frozen baseline
Markdown is canonical in v1.x
entries use strict structured frontmatter
no manually maintained JSON mirror until a validator/generator exists
human guide and AI helper are separate files
freeze docs and scripts must use dynamic <project_root> or project-root-relative paths
project_freeze_ledger stays at <project_root>/project_freeze_ledger
project_freeze_ledger is not inside kanda_prompt_workspace
```

## next allowed project step

After this structured-entry implementation is installed and validated, the next allowed step may be:

```text
freeze this v1.9 structured-entries upgrade as a new baseline
```

Do not implement `freeze_index.json`, `check_protected_paths.py`, or AI-send path filtering until this frontmatter format is validated and accepted.

## how AI decides what is frozen

Use this sequence:

```text
1. read project_frozen_implemented_steps.md
2. identify candidate frozen boxes
3. read relevant entries/freeze-....md files
4. inspect protected_paths in frontmatter
5. read the full entry body before modifying protected files
```

If relevance is unclear, read all entries.

## freeze-20260612-project-freeze-ledger-v19-structured-entries

Summary:

```text
The project_freeze_ledger entries were upgraded with structured frontmatter and validated with validate_freeze_entry_frontmatter.py.
```

Detailed entry:

```text
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v19-structured-entries.md
```

Protected structured-entry layer:

```text
project_freeze_ledger/entries/
project_freeze_ledger/freeze_tools/repair_v19_structured_entries.py
project_freeze_ledger/freeze_tools/validate_freeze_entry_frontmatter.py
```

Next allowed step:

```text
v20 freeze_index.json generator, only after explicit user approval.
```

## freeze-20260612-project-freeze-ledger-v20-freeze-index

Summary:

```text
The project_freeze_ledger now has a generated freeze_index.json produced from structured Markdown freeze entries.
```

Detailed entry:

```text
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v20-freeze-index.md
```

Generated index:

```text
project_freeze_ledger/freeze_index.json
```

Generator:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py
```

Next allowed step:

```text
v21 protected path checker, only after explicit user approval.
```

## freeze-20260612-project-freeze-ledger-v22-final-clean-ai-send-tools

```text
status: frozen
date: 2026-06-12
box: project_freeze_ledger/final_clean_ai_send_tools
entry: project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v22-final-clean-ai-send-tools.md
```

Frozen final clean state:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py
project_freeze_ledger/freeze_tools/check_protected_paths.py
project_freeze_ledger/freeze_tools/files_needed_for_freezing.py
```

Permanent rule:

```text
freeze_tools should not keep validate_*.py, cleanup_validators_after_validation.py, repair_v19_structured_entries.py, or apply_freeze_*.py as permanent files.
```

Generated AI-send packs are convenience outputs. The canonical history remains in `entries/*.md` and this master ledger.


## freeze-after-update-tab-help-layout-v1

Validated and frozen: Freeze Feature After Update tab GUI helpers, symmetrical two-column layout, read-only what_to_say viewer, and top-right practical Help window.


## freeze-20260613-startup-patch-request-routing-logic-v4

Summary:

```text
Startup patch request routing logic v4 is frozen. Patch and bypass-patch requests must explicitly name 05_patch_delivery_and_validation, relevant source files, validation command or manual validation steps, relevant folder card or specialist prompt, conditional 04_box_architecture_and_boundaries, 08_python_engineering_core, 09_python_quality_security_observability, and box_architecture_canon when ownership or boundary decisions are involved.
```

Detailed entry:

```text
project_freeze_after_update/frozen_features_memory/entries/freeze-20260613-startup-patch-request-routing-logic-v4.md
```

Validated evidence:

```text
STATUS: IN_SYNC
VALIDATION OK - Patch request routing logic v4 is installed and coherent.
RG-011 live behavior PASS: Routed Work Path, May proceed now: NO, explicit prompt naming present.
```

Protected startup routing layer:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
```

Next allowed step:

```text
Continue focused routing gatekeeper tests or proceed to the next prompt-system roadmap step without weakening v4 patch-request specificity.
```

<!-- freeze-20260613-freeze-after-update-bom-index-tolerance-v1_START -->
## freeze-20260613-freeze-after-update-bom-index-tolerance-v1 - Freeze After Update BOM index tolerance v1

Status: frozen after validation evidence.

Validated behavior:
- Existing `freeze_index.json` is read with BOM-tolerant decoding.
- BOM and non-BOM freeze indexes both parse.
- Regenerated `freeze_index.json` is written as normal UTF-8 without BOM.
- `files_to_send_ai` generation recovered and included current frozen feature memory.
- Active project freeze memory remains under `project_freeze_after_update/frozen_features_memory/`.

Validation evidence pasted by human:

```text
VALIDATION OK - Freeze After Update BOM index patch v2 validation repair is installed and coherent.
```

<!-- freeze-20260613-freeze-after-update-bom-index-tolerance-v1_END -->


| `freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1` | 2026-06-14 | `kanda_prompt_workspace/startup_kernel_auditor_and_dynamic_delivery` | frozen startup-kernel auditor, dynamic delivery, and paste-file rename | `entries/freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1.md` |

## freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1

Summary:

```text
The startup kernel now has a validated auditor for explicit .meta.json startup candidates, a dynamic source-map-driven startup delivery generator, and the human startup paste file has been renamed to paste_after_first_prompts_to_ai.md.
```

Detailed entry:

```text
project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-startup-kernel-auditor-dynamic-delivery-v1.md
```

Protected startup-kernel layer:

```text
kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md
kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md
```

Frozen behavior:

```text
The auditor explains candidate startup prompts, requires human YES before updating STARTUP_ROUTING_KERNEL_SOURCES.json, and then regenerates startup delivery through sync_startup_routing_kernel_pack.py --ensure-sync --yes.
The generator must dynamically include all approved source-map entries in the ZIP, boot file, paste file, README, and manifest.
The old paste_after_uploading_startup_zip.md filename must not be reintroduced in active delivery.
```

## freeze-20260614-freeze-memory-exposure-cli-v1

Summary:

```text
The project now has a validated read-only CLI exposure tool for project-specific frozen memory.
```

Detailed entry:

```text
project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-freeze-memory-exposure-cli-v1.md
```

Protected implementation:

```text
project_freeze_ledger/freeze_tools/expose_freeze_memory.py
```

Validated result:

```text
freeze_memory_exposure_cli_v1 installed and validated.
The tool correctly reported FREEZE_MEMORY_STATUS: STALE_EXPOSURE on the real project, proving stale files_to_send_ai detection while preserving read-only behavior.
```

Permanent rules:

```text
Keep active freeze memory project-specific under <project_root>/project_freeze_after_update/frozen_features_memory.
Keep project_freeze_ledger as reusable freeze engine / blueprint logic only.
Keep expose_freeze_memory.py read-only in v1.
Do not add publish, ZIP, GUI, startup, app-contract, or index-repair behavior to v1.
```

Next allowed step:

```text
freeze_memory_context_publish_v1_1 may be designed only as a separate governed patch after this freeze is validated.
```
- 2026-06-15 | freeze-20260615-freeze-feature-after-update-local-freeze-workflow-v1 | Freeze Feature After Update Local Freeze Workflow v1 | frozen
- 2026-06-15 | freeze-20260615-cooperative-implementation-methodology-v1 | Cooperative Implementation Methodology v1 | frozen
- 2026-06-15 | freeze-20260615-routing-index-escalation-and-staleness-v1 | Routing Index Escalation and Startup Staleness v1 | frozen
- 2026-06-15 | freeze-20260615-phase2-conditional-context-rubric-v1 | Phase 2 Conditional Context Rubric v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-feature-after-update-local-freeze-workflow-v1 | Freeze Feature After Update Local Freeze Workflow v1 | frozen
- 2026-06-16 | freeze-20260616-rg-029-startup-stale-filename-override-v1 | RG-029 Startup Stale Filename Override v1 | frozen
- 2026-06-16 | freeze-20260616-rg-028-exact-context-expansion-v2 | RG-028 Exact Context Expansion v2 | frozen
- 2026-06-16 | freeze-20260616-freeze-hint-intake-box-v1 | Freeze Hint Intake Box v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-hint-preserve-local-validation-v1 | Freeze Hint Preserve Local Validation v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-hint-validation-evidence-merge-v1 | Freeze Hint Validation Evidence Merge v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-code-intake-prompt-routing-v1 | Freeze Code Intake Prompt Routing v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-hint-sidecar-delivery-contract-v1 | Freeze Hint Sidecar Delivery Contract v1 | frozen
- 2026-06-16 | freeze-20260616-phase-2-prompt-call-accuracy-routing-matrix-v1 | Phase 2 Prompt-Call Accuracy Routing Matrix v1 | frozen
- 2026-06-16 | freeze-20260616-pre-output-contract-gates-v1 | Pre-Output Contract Gates v1 | frozen
- 2026-06-16 | freeze-20260616-freeze-hint-windows-temp-cleanup-tolerance-v1 | Freeze Hint Windows Temp Cleanup Tolerance v1 | frozen
- 2026-06-16 | freeze-20260616-routing-signal-scorer-v1-diagnostic | Routing Signal Scorer v1 Diagnostic | frozen
- 2026-06-16 | freeze-20260616-routing-signal-scorer-manual-pilots-v1 | Routing Signal Scorer Manual Pilots v1 | frozen
- 2026-06-16 | freeze-20260616-routing-signal-scorer-v1-advisory | Routing Signal Scorer v1 Advisory | frozen
- 2026-06-16 | freeze-20260616-routing-signal-scorer-v2-similarity-design | Routing Signal Scorer v2 Similarity Design | frozen
- 2026-06-16 | freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus | Routing Signal Scorer v2 Similarity Test Corpus | frozen
- 2026-06-16 | freeze-20260616-freeze-form-autofill-stale-sidecar-selection-repair-v1 | Freeze Form Autofill Stale Sidecar Selection Repair v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-autofill-state-machine-tests-v1 | Freeze Hint Autofill State Machine Tests v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1 | Freeze Hint Consumed Newer Scan Continuation v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-frozen-entry-body-mention-guard-v1 | Freeze Hint Frozen Entry Body Mention Guard v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-false-consumed-retry-guard-v1 | Freeze Hint False Consumed Retry Guard v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite | Routing Signal Scorer v2 Similarity Runtime Lite | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-metadata-alias-autofill-v1 | Freeze Hint Metadata Alias Autofill v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite-calibration-tests-v1 | Routing Signal Scorer v2 Similarity Runtime Lite Calibration Tests v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-threshold-policy-v1 | Routing Signal Scorer v2 Similarity Threshold Policy v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-policy-runtime-alignment-v1 | Routing Signal Scorer v2 Similarity Policy Runtime Alignment v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-explainability-v1 | Routing Signal Scorer v2 Similarity Explainability v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-decision-report-v1 | Routing Signal Scorer v2 Similarity Decision Report v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-ui-preview-adapter-v1 | Routing Signal Scorer v2 Similarity UI Preview Adapter v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-prompt-context-preview-v1 | Routing Signal Scorer v2 Similarity Prompt Context Preview v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-hint-nested-patch-boundary-formulary-autofill-v1 | Freeze Hint Nested Patch-Boundary Formulary Autofill v1 | frozen
- 2026-06-17 | freeze-20260617-kanda-box-shielding-canon-routing-registration-v1 | KANDA Box Shielding Canon Routing Registration v1 | frozen
- 2026-06-17 | freeze-20260617-kanda-routing-system-canon-registration-v1 | KANDA Routing System Canon Registration v1 | frozen
- 2026-06-17 | freeze-20260617-freeze-tab-local-preview-visible-log-v1 | Freeze Tab Local Preview Visible Log v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v2-similarity-box-shield-v1 | Routing Signal Scorer v2 Similarity Box Shield v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-semantic-readiness-canon-registration-v1 | Routing Signal Scorer v3 Semantic Readiness Canon Registration v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-structural-contract-and-semantic-readiness-design-v1 | Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-mock-semantic-evidence-contract-v1 | Routing Signal Scorer v3 Mock Semantic Evidence Contract v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-metadata-vector-manifest-schema-v1 | Routing Signal Scorer v3 Metadata Vector Manifest Schema v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-offline-corpus-governance-design-v1 | Routing Signal Scorer v3 Offline Corpus Governance Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-offline-evaluation-corpus-design-v1 | Routing Signal Scorer v3 Offline Evaluation Corpus Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-offline-evaluation-gold-set-schema-v1 | Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-disabled-evaluation-runner-design-v1 | Routing Signal Scorer v3 Disabled Evaluation Runner Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-provider-boundary-design-v1 | Routing Signal Scorer v3 Provider Boundary Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-precomputed-semantic-evidence-artifact-design-v1 | Routing Signal Scorer v3 Precomputed Semantic Evidence Artifact Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-disabled-artifact-reader-boundary-design-v1 | Routing Signal Scorer v3 Disabled Artifact Reader Boundary Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-advisory-precomputed-artifact-ui-preview-design-v1 | Routing Signal Scorer v3 Advisory Precomputed Artifact UI Preview Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-schema-only-precomputed-artifact-example-v1 | Routing Signal Scorer v3 Schema-Only Precomputed Artifact Example v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-closure-shield-v1 | Routing Signal Scorer v3 Closure Shield v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-disabled-generation-boundary-design-v1 | Routing Signal Scorer v3 Disabled Generation Boundary Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-dry-run-artifact-generation-plan-design-v1 | Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-local-generator-candidate-review-gate-design-v1 | Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-human-architectural-review-record-design-v1 | Routing Signal Scorer v3 Human Architectural Review Record Design v1 | frozen
- 2026-06-17 | freeze-20260617-routing-signal-scorer-v3-human-decision-intake-design-v1 | Routing Signal Scorer v3 Human Decision Intake Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-actual-human-decision-record-design-v1 | Routing Signal Scorer v3 Actual Human Decision Record Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-actual-human-decision-recording-boundary-design-v1 | Routing Signal Scorer v3 Actual Human Decision Recording Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-proposal-schema-design-v1 | Routing Signal Scorer v3 Generator Candidate Proposal Schema Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-proposal-review-design-v1 | Routing Signal Scorer v3 Generator Candidate Proposal Review Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-patch-preflight-design-v1 | Routing Signal Scorer v3 Generator Candidate Patch Preflight Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-patch-envelope-design-v1 | Routing Signal Scorer v3 Generator Candidate Patch Envelope Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-patch-skeleton-design-v1 | Routing Signal Scorer v3 Generator Candidate Patch Skeleton Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-patch-file-set-design-v1 | Routing Signal Scorer v3 Generator Candidate Patch File-Set Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-dependency-boundary-design-v1 | Routing Signal Scorer v3 Generator Candidate Dependency Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-side-effect-boundary-design-v1 | Routing Signal Scorer v3 Generator Candidate Side-Effect Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-review-bundle-design-v1 | Routing Signal Scorer v3 Generator Candidate Review Bundle Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-preparation-closure-shield-v1 | Routing Signal Scorer v3 Generator Candidate Preparation Closure Shield v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-gate-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Gate Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-record-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Record Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-boundary-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-candidate-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Candidate Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-implementation-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Implementation Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-commit-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Commit Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-finalization-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Finalization Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-finalization-closure-shield-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Finalization Closure Shield v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-patch-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Patch Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-generator-candidate-human-decision-recording-patch-boundary-design-v1 | Routing Signal Scorer v3 Generator Candidate Human Decision Recording Patch Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-foundations-reference-and-box-boundary-design-v1 | Routing Signal Scorer v3 Adviser Foundations Reference and Box Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-system-card-bug-bar-threat-model-design-v1 | Routing Signal Scorer v3 Adviser System Card Bug Bar Threat Model Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-schema-family-design-v1 | Routing Signal Scorer v3 Adviser Schema Family Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-contract-validator-output-guard-v1 | Routing Signal Scorer v3 Adviser Contract Validator Output Guard v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-severity-resource-limits-v1 | Routing Signal Scorer v3 Adviser Severity Resource Limits v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-pure-comparison-harness-v1 | Routing Signal Scorer v3 Adviser Pure Comparison Harness v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-gold-manifest-run-registry-v1 | Routing Signal Scorer v3 Adviser Gold Manifest Run Registry v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-seed-case-corpus-v1 | Routing Signal Scorer v3 Adviser Seed Case Corpus v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-human-review-draft-teacher-answers-v1 | Routing Signal Scorer v3 Adviser Human Review Draft Teacher Answers v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-gate-v1 | Routing Signal Scorer v3 Adviser Seed Gold Set Gate v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-human-reviewed-approval-records-v1 | Routing Signal Scorer v3 Adviser Human Reviewed Approval Records v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-seed-gold-set-assembly-v1 | Routing Signal Scorer v3 Adviser Seed Gold Set Assembly v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-design-v1 | Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-offline-lexical-scorer-v1 | Routing Signal Scorer v3 Adviser Candidate v0 Offline Lexical Scorer v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-candidate-v0-evaluation-runner-v1 | Routing Signal Scorer v3 Adviser Candidate v0 Evaluation Runner v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-active-review-queue-v1 | Routing Signal Scorer v3 Adviser Active Review Queue v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-candidate-registry-v1 | Routing Signal Scorer v3 Adviser Candidate Registry v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-gold-set-expansion-plan-v1 | Routing Signal Scorer v3 Adviser Gold Set Expansion Plan v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-adviser-promotion-criteria-gate-v1 | Routing Signal Scorer v3 Adviser Promotion Criteria Gate v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-assistant-transition-design-v1 | Routing Signal Scorer v3 Shadow Mode / Assistant Transition Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-boundary-design-v1 | Routing Signal Scorer v3 Shadow Mode Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-input-output-contract-design-v1 | Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-contract-validator-design-v1 | Routing Signal Scorer v3 Shadow Mode Contract Validator Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-observation-skeleton-design-v1 | Routing Signal Scorer v3 Shadow Mode Observation Skeleton Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-implementation-gate-design-v1 | Routing Signal Scorer v3 Shadow Mode Implementation Gate Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-non-runtime-shadow-observation-implementation-v1 | Routing Signal Scorer v3 Non Runtime Shadow Observation Implementation v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-observation-review-evidence-design-v1 | Routing Signal Scorer v3 Shadow Observation Review Evidence Design v1 | frozen
- 2026-06-18 | freeze-20260618-architecture-review-rich-desktop-help-layout-v1 | Architecture Review Rich Desktop Help Layout v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-shadow-mode-readiness-gate-for-assistant-boundary-review-v1 | Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-boundary-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-input-output-contract-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Input Output Contract Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-contract-validator-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Contract Validator Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-assistance-skeleton-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Assistance Skeleton Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-implementation-gate-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1 | frozen
- 2026-06-18 | freeze-20260618-architecture-review-blue-orange-dual-layer-help-layout-v2 | Architecture Review Blue-Orange Dual-Layer Help Layout v2 | frozen
- 2026-06-18 | freeze-20260618-architecture-review-blue-orange-dual-layer-help-source-parity-v3 | Architecture Review Blue-Orange Dual-Layer Help Source Parity v3 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-non-runtime-auxiliar-assistant-assistance-implementation-v1 | Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-assistance-review-evidence-design-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1 | frozen
- 2026-06-18 | freeze-20260618-help-layout-image-generation-style-rule-v4 | Help Layout Image Generation Style Rule v4 | frozen
- 2026-06-18 | freeze-20260618-help-layout-colorful-daily-life-image-style-v5 | Help Layout Colorful Daily-Life Image Style v5 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-auxiliar-assistant-assistance-readiness-gate-for-pilot-boundary-review-v1 | Routing Signal Scorer v3 Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review v1 | frozen
- 2026-06-18 | freeze-20260618-architecture-review-help-colorful-daily-life-drawings-v6 | Architecture Review Help Colorful Daily-Life Drawings v6 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-pilot-copilot-boundary-design-v1 | Routing Signal Scorer v3 Pilot/Copilot Boundary Design v1 | frozen
- 2026-06-18 | freeze-20260618-routing-signal-scorer-v3-post-adviser-to-pilot-copilot-handoff-closure-design-v1 | Routing Signal Scorer v3 Post-Adviser to Pilot/Copilot Handoff Closure Design v1 | frozen
- 2026-06-18 | freeze-20260618-help-hand-lettered-daily-life-drawings-v7 | Help Hand-Lettered Daily-Life Drawings v7 | frozen
- 2026-06-19 | freeze-20260619-rg-pilot-000-pilot-copilot-phase-0-router-canon-v1 | RG-PILOT-000 Pilot/Copilot Phase 0 Router Canon v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-copilot-scope-charter-and-entry-gate-design-v1 | Routing Signal Scorer v3 Pilot/Copilot Scope Charter and Entry Gate Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-boundary-design-v1 | Routing Signal Scorer v3 Pilot Boundary Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-input-output-contract-and-validator-design-v1 | Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-disagreement-taxonomy-design-v1 | Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1 | frozen
- 2026-06-19 | freeze-20260619-kanda-patch-delivery-root-drive-zip-staging-canon-v1 | KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-gold-frozen-router-reproduction-harness-design-v1 | Routing Signal Scorer v3 Pilot Gold Frozen Router Reproduction Harness Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-simulation-skeleton-design-v1 | Routing Signal Scorer v3 Pilot Simulation Skeleton Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-review-evidence-design-v1 | Routing Signal Scorer v3 Pilot Review Evidence Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-pilot-implementation-gate-design-v1 | Routing Signal Scorer v3 Pilot Implementation Gate Design v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-candidate-implementation-v1 | Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-candidate-contract-conformance-v1 | Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-candidate-readiness-gate-v1 | Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness Gate v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-candidate-review-evidence-packet-v1 | Routing Signal Scorer v3 Non-Runtime Pilot Candidate Review Evidence Packet v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-phase-closure-copilot-boundary-entry-gate-v1 | Routing Signal Scorer v3 Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1 | frozen
- 2026-06-19 | freeze-20260619-rg-lab-000-ml-lab-phase-entry-router-canon-v1 | RG-LAB-000 ML LAB Phase Entry Router Canon v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-phase-boundary-charter-entry-gate-v1 | Routing Signal Scorer v3 ML LAB Phase Boundary / Charter Entry Gate v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-success-criteria-matrix-v1 | Routing Signal Scorer v3 ML LAB Success Criteria Matrix v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-risk-control-matrix-v1 | Routing Signal Scorer v3 ML LAB Risk-Control Matrix v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-slo-critical-error-budget-declaration-v1 | Routing Signal Scorer v3 ML LAB SLO / Critical Error Budget Declaration v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-box-boundary-shielding-manifest-v1 | Routing Signal Scorer v3 ML LAB Box Boundary + Shielding Manifest v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-failure-taxonomy-critical-violation-model-v1 | Routing Signal Scorer v3 ML LAB Failure Taxonomy + Critical Violation Model v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-scoring-model-hard-gates-v1 | Routing Signal Scorer v3 ML LAB Scoring Model + Hard Gates v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-test-case-schema-candidate-output-contract-v1 | Routing Signal Scorer v3 ML LAB Test Case Schema + Candidate Output Contract v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-frozen-canon-fixture-format-hash-manifest-v1 | Routing Signal Scorer v3 ML LAB Frozen Canon Fixture Format + Hash Manifest v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-deterministic-runner-skeleton-v1 | Routing Signal Scorer v3 ML LAB Deterministic Runner Skeleton v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-self-validation-gate-v1 | Routing Signal Scorer v3 ML LAB Self-Validation Gate v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-alpha-corpus-seed-v1 | Routing Signal Scorer v3 ML LAB Alpha Corpus Seed v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-offline-observability-experiment-report-v1 | Routing Signal Scorer v3 ML LAB Offline Observability + Experiment Report v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-candidate-evaluation-harness-interface-v1 | Routing Signal Scorer v3 ML LAB Candidate Evaluation Harness Interface v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-corpus-v1-expansion-v1 | Routing Signal Scorer v3 ML LAB Corpus V1 Expansion v1 | frozen
- 2026-06-19 | freeze-20260619-routing-signal-scorer-v3-ml-lab-error-canonization-intake-spec-v1 | Routing Signal Scorer v3 ML LAB Error Canonization Intake Spec v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-ml-lab-closure-next-phase-readiness-review-v1 | Routing Signal Scorer v3 ML LAB Closure / Next-Phase Readiness Review v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-0-controlled-non-runtime-ml-router-candidate-reliability-test-plan-v1 | Routing Signal Scorer v3 MLRT-0 Controlled Non-Runtime ML/Router Candidate Reliability Test Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-1-candidate-reliability-input-output-contract-plan-v1 | Routing Signal Scorer v3 MLRT-1 Candidate Reliability Input/Output Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-2-candidate-package-intake-contract-plan-v1 | Routing Signal Scorer v3 MLRT-2 Candidate Package Intake Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-3-candidate-static-review-checklist-plan-v1 | Routing Signal Scorer v3 MLRT-3 Candidate Static Review Checklist Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-4-candidate-static-review-evidence-envelope-plan-v1 | Routing Signal Scorer v3 MLRT-4 Candidate Static Review Evidence Envelope Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-5-candidate-static-review-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-5 Candidate Static Review Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-6-candidate-non-runtime-dry-run-readiness-gate-plan-v1 | Routing Signal Scorer v3 MLRT-6 Candidate Non-Runtime Dry-Run Readiness Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-7-candidate-non-runtime-dry-run-protocol-plan-v1 | Routing Signal Scorer v3 MLRT-7 Candidate Non-Runtime Dry-Run Protocol Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-8-candidate-non-runtime-dry-run-input-set-plan-v1 | Routing Signal Scorer v3 MLRT-8 Candidate Non-Runtime Dry-Run Input Set Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-9-candidate-non-runtime-dry-run-output-capture-plan-v1 | Routing Signal Scorer v3 MLRT-9 Candidate Non-Runtime Dry-Run Output Capture Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-10-candidate-non-runtime-dry-run-output-capture-rejection-gate-plan-v1 | Routing Signal Scorer v3 MLRT-10 Candidate Non-Runtime Dry-Run Output Capture Rejection Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-11-candidate-non-runtime-dry-run-output-capture-contract-conformance-plan-v1 | Routing Signal Scorer v3 MLRT-11 Candidate Non-Runtime Dry-Run Output Capture Contract-Conformance Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-12-candidate-non-runtime-dry-run-contract-conformance-rejection-gate-plan-v1 | Routing Signal Scorer v3 MLRT-12 Candidate Non-Runtime Dry-Run Contract-Conformance Rejection Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-13-candidate-first-non-runtime-dry-run-execution-plan-v1 | Routing Signal Scorer v3 MLRT-13 Candidate First Non-Runtime Dry-Run Execution Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-14-candidate-first-non-runtime-dry-run-harness-skeleton-plan-v1 | Routing Signal Scorer v3 MLRT-14 Candidate First Non-Runtime Dry-Run Harness Skeleton Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-15-candidate-first-non-runtime-dry-run-harness-contract-plan-v1 | Routing Signal Scorer v3 MLRT-15 Candidate First Non-Runtime Dry-Run Harness Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-16-candidate-first-non-runtime-dry-run-harness-implementation-boundary-plan-v1 | Routing Signal Scorer v3 MLRT-16 Candidate First Non-Runtime Dry-Run Harness Implementation Boundary Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-17-candidate-first-non-runtime-dry-run-harness-stub-implementation-plan-v1 | Routing Signal Scorer v3 MLRT-17 Candidate First Non-Runtime Dry-Run Harness Stub Implementation Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-18-candidate-first-non-runtime-dry-run-harness-stub-source-surface-plan-v1 | Routing Signal Scorer v3 MLRT-18 Candidate First Non-Runtime Dry-Run Harness Stub Source Surface Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-19-candidate-first-non-runtime-dry-run-harness-stub-static-interface-contract-plan-v1 | Routing Signal Scorer v3 MLRT-19 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-20-candidate-first-non-runtime-dry-run-harness-stub-static-interface-abort-contract-plan-v1 | Routing Signal Scorer v3 MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-21-candidate-first-non-runtime-dry-run-harness-stub-static-interface-rejection-contract-plan-v1 | Routing Signal Scorer v3 MLRT-21 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Rejection Contract Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-22-candidate-first-non-runtime-dry-run-harness-stub-static-interface-test-start-readiness-gate-plan-v1 | Routing Signal Scorer v3 MLRT-22 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Test-Start Readiness Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-23-candidate-first-non-runtime-dry-run-harness-stub-static-interface-source-implementation-boundary-confirmation-plan-v1 | Routing Signal Scorer v3 MLRT-23 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Source/Implementation Boundary Confirmation Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-24-candidate-first-non-runtime-dry-run-harness-stub-static-interface-source-file-authorization-plan-v1 | Routing Signal Scorer v3 MLRT-24 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Source File Authorization Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-25-candidate-first-non-runtime-dry-run-harness-stub-static-interface-stub-source-creation-gate-plan-v1 | Routing Signal Scorer v3 MLRT-25 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Stub Source Creation Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-26-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-plan-v1 | Routing Signal Scorer v3 MLRT-26 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-27-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-authorization-gate-plan-v1 | Routing Signal Scorer v3 MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-28-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-plan-v1 | Routing Signal Scorer v3 MLRT-28 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-29-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-safety-review-plan-v1 | Routing Signal Scorer v3 MLRT-29 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Safety Review Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-30-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-safety-review-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-30 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Safety Review Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-31-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-final-human-review-gate-plan-v1 | Routing Signal Scorer v3 MLRT-31 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-32-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-final-human-review-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-32 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-33-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-final-source-creation-authorization-gate-plan-v1 | Routing Signal Scorer v3 MLRT-33 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Source Creation Authorization Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-34-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-final-source-creation-authorization-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-34 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Source Creation Authorization Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-35-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-plan-v1 | Routing Signal Scorer v3 MLRT-35 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-36-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-safety-review-plan-v1 | Routing Signal Scorer v3 MLRT-36 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Safety Review Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-37-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-safety-review-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-37 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Safety Review Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-38-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-final-human-review-gate-plan-v1 | Routing Signal Scorer v3 MLRT-38 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Final Human Review Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-39-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-final-human-review-outcome-gate-plan-v1 | Routing Signal Scorer v3 MLRT-39 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Final Human Review Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-v3-mlrt-40-candidate-first-non-runtime-dry-run-harness-stub-static-interface-minimal-stub-source-file-creation-patch-controlled-minimal-source-file-creation-patch-execution-readiness-plan-v1 | Routing Signal Scorer v3 MLRT-40 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Execution Readiness Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-41-execution-readiness-outcome-gate-plan-v1 | Routing Signal Scorer MLRT-41 Execution Readiness Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-42-execution-gate-plan-v1 | Routing Signal Scorer MLRT-42 Execution Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-43-execution-gate-outcome-plan-v1 | Routing Signal Scorer MLRT-43 Execution Gate Outcome Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-44-source-creation-authorization-plan-v1 | Routing Signal Scorer MLRT-44 Source Creation Authorization Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-45-source-creation-authorization-outcome-plan-v1 | Routing Signal Scorer MLRT-45 Source Creation Authorization Outcome Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-46-source-creation-authorization-outcome-gate-plan-v1 | Routing Signal Scorer MLRT-46 Source Creation Authorization Outcome Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-47-source-creation-final-human-review-plan-v1 | Routing Signal Scorer MLRT-47 Source Creation Final Human Review Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-48-controlled-minimal-source-creation-v1 | Routing Signal Scorer MLRT-48 Controlled Minimal Source Creation v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-49-static-boundary-test-v1 | Routing Signal Scorer MLRT-49 Static Boundary Test v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-50-non-runtime-harness-smoke-test-v1 | Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-51-candidate-evaluation-harness-self-test-v1 | Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-52-lab-reliability-test-against-fixed-cases-v1 | Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-53-training-learning-governance-plan-v1 | Routing Signal Scorer MLRT-53 Training Learning Governance Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-54-training-data-boundary-plan-v1 | Routing Signal Scorer MLRT-54 Training Data Boundary Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-55-gold-registry-mutation-gate-plan-v1 | Routing Signal Scorer MLRT-55 Gold Registry Mutation Gate Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-56-offline-evaluation-protocol-plan-v1 | Routing Signal Scorer MLRT-56 Offline Evaluation Protocol Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-57-calibration-only-dry-run-plan-v1 | Routing Signal Scorer MLRT-57 Calibration-Only Dry-Run Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-58-learning-sandbox-plan-v1 | Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-59-first-controlled-learning-experiment-plan-v1 | Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-60-gold-registry-schema-proposal-plan-v1 | Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-61-router-prompt-selection-offline-evaluation-case-schema-plan-v1 | Routing Signal Scorer MLRT-61 Router Prompt Selection Offline Evaluation Case Schema Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-62-router-prompt-selection-fixed-case-set-format-plan-v1 | Routing Signal Scorer MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-63-router-prompt-selection-fixed-case-set-static-validation-plan-v1 | Routing Signal Scorer MLRT-63 Router Prompt Selection Fixed Case Set Static Validation Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-64-router-prompt-selection-non-runtime-offline-evaluation-harness-plan-v1 | Routing Signal Scorer MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-65-first-controlled-offline-ml-prompt-selection-test-v1 | Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-66-controlled-offline-ml-prompt-selection-test-result-review-gate-v1 | Routing Signal Scorer MLRT-66 Controlled Offline ML Prompt-Selection Test Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-67-second-controlled-offline-ml-prompt-selection-test-v1 | Routing Signal Scorer MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-68-second-controlled-offline-ml-prompt-selection-test-result-review-gate-v1 | Routing Signal Scorer MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-69-expanded-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-69 Expanded Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-70-expanded-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-70 Expanded Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-71-boundary-negative-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-72-boundary-negative-controlled-offline-ml-prompt-selection-test-result-review-gate-v1 | Routing Signal Scorer MLRT-72 Boundary-Negative Controlled Offline ML Prompt-Selection Test Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-73-increased-volume-mixed-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-73 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-74-increased-volume-mixed-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-74 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-75-maximum-optimized-adversarial-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-75 Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-76-maximum-optimized-adversarial-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-76 Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-20 | freeze-20260620-routing-signal-scorer-mlrt-77-maximum-optimized-near-miss-counterfactual-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-77 Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-78-maximum-optimized-near-miss-counterfactual-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-78 Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-79-maximum-optimized-differential-drift-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-79 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-80-maximum-optimized-differential-drift-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-80 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-81-maximum-optimized-regression-metamorphic-consistency-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-81 Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-82-maximum-optimized-regression-metamorphic-consistency-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-82 Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-83-maximum-optimized-semantic-collision-disambiguation-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-83 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-84-maximum-optimized-semantic-collision-disambiguation-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-84 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-85-maximum-optimized-ambiguity-saturation-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-85 Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-86-maximum-optimized-ambiguity-saturation-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-86 Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-87-maximum-optimized-state-transition-evidence-recognition-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-87 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-88-maximum-optimized-state-transition-evidence-recognition-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-88 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-89-maximum-optimized-temporal-recency-arbitration-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-89 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-90-maximum-optimized-temporal-recency-arbitration-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-90 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-91-maximum-optimized-user-correction-evidence-recovery-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-91 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-92-maximum-optimized-user-correction-evidence-recovery-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-92 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-93-maximum-optimized-current-feature-freeze-intake-precedence-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-93 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-94-maximum-optimized-current-feature-freeze-intake-precedence-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-94 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-95-maximum-optimized-freeze-exposure-status-recovery-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-95 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-96-maximum-optimized-freeze-exposure-status-recovery-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-96 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-97-maximum-optimized-preview-versus-write-boundary-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-97 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-98-maximum-optimized-preview-versus-write-boundary-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-98 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-99-maximum-optimized-human-confirmation-binding-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-99 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-100-maximum-optimized-human-confirmation-binding-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-100 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-101-maximum-optimized-written-path-integrity-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-101 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-102-maximum-optimized-written-path-integrity-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-102 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-103-maximum-optimized-freeze-index-consistency-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-103 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-104-maximum-optimized-freeze-index-consistency-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-104 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-105-maximum-optimized-ai-send-exposure-alignment-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-105 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-106-maximum-optimized-ai-send-exposure-alignment-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-106 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-107-maximum-optimized-startup-freeze-context-propagation-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-107 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-108-maximum-optimized-startup-freeze-context-propagation-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-108 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-109-maximum-optimized-startup-handoff-next-step-arbitration-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-109 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-110-maximum-optimized-startup-handoff-next-step-arbitration-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-110 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-111-maximum-optimized-freeze-hint-consumption-binding-controlled-offline-ml-prompt-selection-test-suite-v1 | Routing Signal Scorer MLRT-111 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-112-maximum-optimized-freeze-hint-consumption-binding-controlled-offline-ml-prompt-selection-test-suite-result-review-gate-v1 | Routing Signal Scorer MLRT-112 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-consolidation-audit-and-coverage-map-v1 | Routing Signal Scorer MLRT Consolidation Audit and Coverage Map v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-mlrt-final-closure-audit-and-reuse-policy-v1 | Routing Signal Scorer MLRT Final Closure Audit and Reuse Policy v1 | frozen
- 2026-06-21 | freeze-20260621-release-guard-zip-delivery-contract-v1 | Release Guard ZIP Delivery Contract v1 | frozen
- 2026-06-21 | freeze-20260621-release-guard-validation-runner-fix-v1 | Release Guard Validation Runner Fix v1 | frozen
- 2026-06-21 | freeze-20260621-freeze-hint-stale-pending-cleanup-v1 | Freeze Hint Stale Pending Cleanup v1 | frozen
- 2026-06-21 | freeze-20260621-terminal-cleanup-canon-v1 | Terminal Cleanup Canon v1 | frozen
- 2026-06-21 | freeze-20260621-freeze-form-pending-write-gate-v1 | Freeze Form Pending Write Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-and-governed-prompt-intake-boundary-contract-v1 | Routing Signal Scorer ML Advisory-Signal and Governed Prompt Intake Boundary Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-1a-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 1a Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-1b-non-runtime-design-audit-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-1b-non-runtime-design-audit-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-2-offline-evaluation-harness-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1 | frozen
- 2026-06-21 | freeze-20260621-patch-install-delivery-guard-prompt-and-startup-enforcement-v1 | Patch Install Delivery Guard Prompt and Startup Enforcement v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-2-offline-evaluation-harness-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-3-offline-fixture-catalog-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-3-offline-fixture-catalog-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-4-offline-advisor-comparison-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-4-offline-advisor-comparison-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-5-offline-real-adapter-boundary-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-5-offline-real-adapter-boundary-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-5-offline-real-adapter-candidate-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-5-offline-real-adapter-candidate-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Final Safety Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-6-guarded-runtime-advisory-display-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Completion Handoff v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-web-and-book-informed-advisory-surface-wiring-research-flux-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Web-and-Book-Informed Advisory Surface Wiring Research Flux v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-guarded-advisory-surface-wiring-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-guarded-advisory-surface-wiring-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-read-only-advisory-surface-wiring-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-read-only-advisory-surface-wiring-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-read-only-advisory-surface-wiring-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Final Safety Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-7-read-only-advisory-surface-wiring-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation Result Review Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Final Safety Gate v1 | frozen
- 2026-06-21 | freeze-20260621-routing-signal-scorer-ml-advisory-signal-phase-8-read-only-advisory-panel-ui-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Completion Handoff v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Implementation v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Implementation Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Final Safety Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-9-read-only-advisory-panel-runtime-activation-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Completion Handoff v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Contract v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Contract Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Implementation v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Implementation Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Final Safety Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-10-read-only-advisory-panel-renderer-mount-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Completion Handoff v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Contract v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Contract Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Implementation v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Implementation Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Final Safety Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-11-read-only-advisory-panel-host-binding-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Completion Handoff v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Contract v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Contract Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Implementation v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Implementation Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-final-safety-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Final Safety Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-12-read-only-advisory-panel-runtime-app-host-visibility-completion-handoff-v1 | Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Completion Handoff v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-13-read-only-advisory-panel-passive-visibility-activation-contract-v1 | Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-13-read-only-advisory-panel-passive-visibility-activation-contract-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-13-read-only-advisory-panel-passive-visibility-activation-implementation-v1 | Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation v1 | frozen
- 2026-06-22 | freeze-20260622-routing-signal-scorer-ml-advisory-signal-phase-13-read-only-advisory-panel-passive-visibility-activation-implementation-result-review-gate-v1 | Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation Result Review Gate v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-persistent-review-store-v1 | Prompt Router Reasoner Persistent Review Store v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-shadow-ml-bridge-v1 | Prompt Router Reasoner Shadow ML Bridge v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-router-mode-state-v1 | Prompt Router Reasoner Router Mode State v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-tab-skeleton-v1 | Prompt Router Reasoner Tab Skeleton v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-review-list-loading-v1 | Prompt Router Reasoner Review List Loading v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-heuristic-ml-detail-panels-v1 | Prompt Router Reasoner Heuristic ML Detail Panels v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-save-review-and-undo-v1 | Prompt Router Reasoner Save Review and Undo v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-vertical-bars-and-stats-panel-v1 | Prompt Router Reasoner Vertical Bars and Stats Panel v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-ask-ai-workflow-v1 | Prompt Router Reasoner Ask AI Workflow v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-ai-second-opinion-capture-v1 | Prompt Router Reasoner AI Second Opinion Capture v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-sessionservice-runtime-capture-wiring-v1 | Prompt Router Reasoner SessionService Runtime Capture Wiring v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-windows-temp-cleanup-validation-repair-v1 | Prompt Router Reasoner Windows Temp Cleanup Validation Repair v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-runtime-capture-visibility-refresh-v1 | Prompt Router Reasoner Runtime Capture Visibility Refresh v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-runtime-newest-selection-tie-repair-v1 | Prompt Router Reasoner Runtime Newest Selection Tie Repair v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-gui-polish-and-review-ergonomics-v1 | Prompt Router Reasoner GUI Polish and Review Ergonomics v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-full-prompt-lazy-display-v1 | Prompt Router Reasoner Full Prompt Lazy Display v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-export-review-dataset-v1 | Prompt Router Reasoner Export Review Dataset v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-import-loaded-ids-tuple-contract-repair-v1 | Prompt Router Reasoner Import Loaded IDs Tuple Contract Repair v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-import-no-store-side-effect-repair-v1 | Prompt Router Reasoner Import No-Store Side-Effect Repair v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-import-review-dataset-v1 | Prompt Router Reasoner Import Review Dataset v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-import-conflict-review-v1 | Prompt Router Reasoner Import Conflict Review v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-review-dataset-export-polish-v1 | Prompt Router Reasoner Review Dataset Export Polish v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-performance-large-review-list-v1 | Prompt Router Reasoner Performance Large Review List v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-final-closeout-undo-label-contract-repair-v1 | Prompt Router Reasoner Final Closeout Undo Label Contract Repair v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-final-gui-regression-and-closeout-v1 | Prompt Router Reasoner Final GUI Regression and Closeout v1 | frozen
- 2026-06-22 | freeze-20260622-prompt-router-reasoner-auto-ml-pilot-activation-repair-v1 | Prompt Router Reasoner Auto ML Pilot Activation Repair v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-router-reasoner-startup-check-delivery-v1 | Prompt Router Reasoner Startup Check Delivery v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-insertion-and-router-registration-protocol-v1 | Prompt Insertion and Router Registration Protocol v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-identity-code-registry-canon-v1 | Prompt Identity Code Registry Canon v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-router-reasoner-manual-router-choice-capture-v1 | Prompt Router Reasoner Manual Router Choice Capture v1 | frozen
- 2026-06-23 | freeze-20260623-chatgpt-kanda-routing-choice-output-protocol-v1 | ChatGPT KANDA Routing Choice Output Protocol v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-router-reasoner-manual-ui-simplification-v1 | Prompt Router Reasoner Manual UI Simplification v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-library-zip-direct-retrieval-v1 | Prompt Library ZIP Direct Retrieval v1 | frozen
- 2026-06-23 | freeze-20260623-startup-read-before-all-instruction-file-v1 | Startup Read Before All Instruction File v1 | frozen
- 2026-06-23 | freeze-20260623-startup-read-before-all-compliance-refresh-alignment-v1 | Startup Read-Before-All Compliance Refresh Alignment v1 | frozen
- 2026-06-23 | freeze-20260623-prompt-router-reasoner-auto-ml-pilot-activation-v1 | Prompt Router Reasoner Auto ML Pilot Activation v1 | frozen
- 2026-06-23 | freeze-20260623-project-structure-map-dynamic-ai-delivery-files-v1 | Project Structure Map Dynamic AI Delivery Files v1 | frozen
- 2026-06-23 | freeze-20260623-patch-freeze-delivery-sequence-canon-v1 | Patch Freeze Delivery Sequence Canon v1 | frozen
- 2026-06-23 | freeze-20260623-project-structure-map-auto-zip-json-complete-v1 | Project Structure Map Auto ZIP json_complete v1 | frozen
- 2026-06-23 | freeze-20260623-project-structure-map-show-project-to-ai-folder-v1 | Project Structure Map show_project_to_AI Folder v1 | frozen
- 2026-06-23 | freeze-20260623-handoff-zip-exporter-runpy-warning-fix-v1 | Handoff ZIP Exporter Runpy Warning Fix v1 | frozen
- 2026-06-23 | freeze-20260623-handoff-zip-exporter-show-project-to-ai-warning-fix-v1 | Handoff ZIP Exporter show_project_to_AI Warning Fix v1 | frozen
- 2026-06-23 | freeze-20260623-show-project-to-ai-second-prompt-files-output-v1 | Show Project to AI second_prompt_files Output v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-first-prompt-files-columns-v1 | Show Project to AI First Prompt Files Columns v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-startup-reference-cleanup-v1 | Show Project to AI Startup Reference Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-zip-part-size-split-v1 | Show Project to AI ZIP Part Size Split v1 | frozen
- 2026-06-24 | freeze-20260624-freeze-tab-first-prompt-files-import-hotfix-v1 | Freeze Tab first_prompt_files Import Hotfix v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-project-root-selector-v1 | Show Project to AI Project Root Selector v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-combined-actions-v1 | Show Project to AI Combined Actions v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-path-buttons-v1 | Show Project to AI Path Buttons v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-selected-project-override-v1 | Show Project to AI Selected Project Override v1 | frozen
- 2026-06-24 | freeze-20260624-legacy-project-name-reference-cleanup-v1 | Legacy Project Name Reference Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-startup-delivery-deep-reference-cleanup-v1 | Startup Delivery Deep Reference Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-publish-manifest-hash-refresh-v1 | Show Project to AI Publish Manifest Hash Refresh v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-hybrid-source-archive-export-v1 | Show Project to AI Hybrid Source Archive Export v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-transactional-publish-cleanup-v1 | Show Project to AI Transactional Publish Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-minimal-hybrid-map-output-v1 | Show Project to AI Minimal Hybrid Map Output v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-minimal-hybrid-gui-start-hotfix-v1 | Show Project to AI Minimal Hybrid GUI Start Hotfix v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-zip-build-folder-bundle-manifest-hotfix-v1 | Show Project to AI ZIP Build Folder Bundle Manifest Hotfix v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-project-zip-noise-cleanup-v1 | Show Project to AI Project ZIP Noise Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-final-artifact-consistency-cleanup-v1 | Show Project to AI Final Artifact Consistency Cleanup v1 | frozen
- 2026-06-24 | freeze-20260624-startup-second-upload-json-handoff-zip-contract-v1 | Startup Second Upload JSON Handoff ZIP Contract v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-build-override-hash-resolution-v1 | Show Project to AI Build Override Hash Resolution v1 | frozen
- 2026-06-24 | freeze-20260624-show-project-to-ai-ai-briefing-self-hash-contract-v1 | Show Project to AI AI Briefing Self-Hash Contract v1 | frozen
- 2026-06-25 | freeze-20260625-show-project-to-ai-second-prompt-cleanup-and-zip-size-v1 | Show Project to AI Second Prompt Cleanup and ZIP Size v1 | frozen
- 2026-06-25 | freeze-20260625-show-project-to-ai-remove-ai-import-builder-v1 | Show Project to AI Remove AI Import Builder v1 | frozen
- 2026-06-25 | freeze-20260625-show-project-to-ai-project-independent-png-assets-reuse-v1 | Show Project to AI Project-Independent PNG Assets Reuse v1 | frozen
- 2026-06-25 | freeze-20260625-project-tool-boundary-canon-routed-for-coding-tasks | Project/tool boundary canon routed for coding tasks | frozen
- 2026-06-25 | freeze-20260625-error-memory-core-gui-tab-and-ai-send-canon-v1 | Error Memory core, GUI tab, and AI-send canon v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-ai-formulary-startup-canon-v1 | Error Memory AI Formulary Startup Canon v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-zip-import-repair-v1 | Error Memory ZIP Import Repair v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-active-status-and-fingerprint-repair-v1 | Error Memory Active Status and Fingerprint Repair v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-plain-text-intake-repair-v1 | Error Memory Plain Text Intake Repair v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-zip-import-dependency-repair-v1 | Error Memory ZIP Import Dependency Repair v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-two-column-lesson-actions-v1 | Error Memory GUI Two Column Lesson Actions v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-zip-import-filter-v1 | Error Memory ZIP Import Filter v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-status-workflow-v1 | Error Memory GUI Status Workflow v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-repeat-error-guard-v1 | Error Memory Repeat Error Guard v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-second-prompt-export-v1 | Error Memory Second Prompt Export v1 | frozen
- 2026-06-25 | freeze-20260625-prompt-error-memory-two-track-closure-v2 | Prompt Error Memory Two-Track Closure v2 | frozen
- 2026-06-25 | freeze-20260625-error-memory-receive-formulary-freeze-intake-syntaxerror-guard-v2 | Error Memory Receive Formulary Freeze Intake SyntaxError Guard v2 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-memorize-formatted-import-flow-v1 | Error Memory GUI Memorize Formatted Import Flow v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-header-project-root-v3 | Error Memory GUI Header Project Root v3 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-loaded-row-project-root-v4 | Error Memory GUI Loaded Row Project Root v4 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-error-editor-memorize-active-v5 | Error Memory GUI Error Editor Memorize Active v5 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-ai-draft-zip-workflow-v6 | Error Memory GUI AI Draft ZIP Workflow v6 | frozen
- 2026-06-25 | freeze-20260625-prompt-error-lesson-zip-router-canon-v1 | Prompt Error Lesson ZIP Router Canon v1 | frozen
- 2026-06-25 | freeze-20260625-error-memory-gui-memorize-clean-editor-flow-v7 | Error Memory GUI Memorize Clean Editor Flow v7 | frozen
- 2026-06-26 | freeze-20260626-error-memory-gui-pending-intake-autoload-v9 | Error Memory GUI Pending Intake Autoload v9 | frozen
- 2026-06-26 | freeze-20260626-prompt-error-memory-default-insertion-autoload-v2 | Prompt Error Memory Default Insertion Autoload v2 | frozen
- 2026-06-26 | freeze-20260626-error-memory-gui-pending-intake-root-sync-v10 | Error Memory GUI Pending Intake Root Sync v10 | frozen
- 2026-06-26 | freeze-20260626-error-memory-gui-manifest-zip-import-v8 | Error Memory GUI Manifest ZIP Import v8 | frozen
- 2026-06-26 | freeze-20260626-show-project-and-error-memory-path-guard | Show Project and Error Memory path guard | frozen
- 2026-06-26 | freeze-20260626-startup-delivery-maintenance-filename-sorts-after-normal-upload-files | Startup delivery maintenance filename sorts after normal upload files | frozen
- 2026-06-26 | freeze-20260626-error-memory-memorize-error-clears-ai-assisted-intake-only | Error Memory Memorize Error clears AI-assisted intake only | frozen
- 2026-06-26 | freeze-20260626-error-memory-packaged-lesson-active-ready-schema-guard | Error Memory packaged lesson active-ready schema guard | frozen
- 2026-06-26 | freeze-20260626-error-memory-packaged-lesson-active-ready-schema-guard-v2 | Error Memory packaged lesson active-ready schema guard v2 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-v2 | Startup artifact read-order guard v2 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-v9 | Startup artifact read-order guard v9 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-v8 | Startup artifact read-order guard v8 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-v7 | Startup artifact read-order guard v7 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-replacing-stale-generated-notice-blocks-v6 | Startup artifact read-order guard replacing stale generated notice blocks v6 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-replacing-stale-generated-notice-blocks-v5 | Startup artifact read-order guard replacing stale generated notice blocks v5 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-with-tell-file-optional-maintenance-wording-v4 | Startup artifact read-order guard with tell-file optional maintenance wording v4 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard-with-optional-maintenance-file-v3 | Startup artifact read-order guard with optional maintenance file v3 | frozen
- 2026-06-26 | freeze-20260626-startup-artifact-read-order-guard | Startup artifact read order guard | frozen
- 2026-06-26 | freeze-20260626-freeze-gui-ignore-this-freeze-and-get-frozen-snippet-controls | Freeze GUI Ignore this Freeze and Get Frozen snippet controls | frozen
- 2026-06-26 | freeze-20260626-startup-code-module-size-bridge | Startup Code Module Size Bridge | frozen
- 2026-06-26 | freeze-20260626-freeze-validation-evidence-merge-by-patch-zip | Freeze Validation Evidence Merge By Patch ZIP | frozen
- 2026-06-26 | freeze-20260626-error-memory-lesson-block-schema-gate | Error Memory Lesson Block Schema Gate | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-clipboard-complete-json | Error Memory Export Clipboard Complete JSON | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-clipboard-complete-json-v2 | Error Memory Export Clipboard Complete JSON v2 | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-complete-json-windows-isolated-validation-v5 | Error Memory Export Complete JSON Windows-Isolated Validation v5 | frozen
- 2026-06-26 | freeze-20260626-startup-box-logic-bridge | Startup Box Logic Bridge | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-cursor-start-guard-v6 | Error Memory Export Cursor Start Guard v6 | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-complete-json-all-statuses-v4 | Error Memory Export Complete JSON All Statuses v4 | frozen
- 2026-06-26 | freeze-20260626-error-memory-export-clipboard-complete-json-v3 | Error Memory Export Clipboard Complete JSON v3 | frozen
- 2026-06-26 | freeze-20260626-error-memory-copy-error-draft-editor-only-v7 | Error Memory Copy Error Draft Editor Only v7 | frozen
- 2026-06-26 | freeze-20260626-error-memory-copy-error-draft-latest-editor-payload-v8 | Error Memory Copy Error Draft Latest Editor Payload v8 | frozen
- 2026-06-26 | freeze-20260626-error-memory-copy-error-editor-exact-json-v12 | Error Memory Copy Error Editor Exact JSON v12 | frozen
- 2026-06-26 | freeze-20260626-error-memory-copy-error-draft-button-recreated-v13 | Error Memory Copy Error Draft Button Recreated v13 | frozen
- 2026-06-26 | freeze-20260626-error-memory-memorize-auto-loads-next-pending-v14 | Error Memory Memorize Auto Loads Next Pending v14 | frozen
- 2026-06-26 | freeze-20260626-router-terminal-footer-contract-v15 | Router Terminal Footer Contract v15 | frozen
- 2026-06-26 | freeze-20260626-error-memory-memorize-next-syncs-editor-v17 | Error Memory Memorize Next Syncs Editor v17 | frozen
- 2026-06-26 | freeze-20260626-error-memory-ai-intake-copy-error-draft-button-v18 | Error Memory AI Intake Copy Error Draft Button v18 | frozen
- 2026-06-26 | freeze-20260626-error-memory-ai-intake-pending-format-v19 | Error Memory AI Intake Pending Format v19 | frozen
- 2026-06-26 | freeze-20260626-error-memory-pending-intake-del-draft | Error Memory Pending Intake Del Draft | frozen
- 2026-06-26 | freeze-20260626-error-memory-file-send-smoke-test-v1 | Error Memory file-send smoke test v1 | frozen
- 2026-06-26 | freeze-20260626-error-memory-heuristic-mark-draft-saveable-v25 | Error Memory heuristic Mark Draft saveable v25 | frozen
- 2026-06-26 | freeze-20260626-error-memory-state-machine-separates-draft-normalization-from-active-memorization | Error Memory state machine separates draft normalization from active memorization | frozen
- 2026-06-26 | freeze-20260626-error-memory-del-draft-complete-delete | Error Memory Del Draft Complete Delete | frozen
- 2026-06-26 | freeze-20260626-error-memory-active-ready-output-hard-gate-v21 | Error Memory Active-Ready Output Hard Gate v21 | frozen
- 2026-06-27 | freeze-20260627-error-memory-strict-heuristic-correction-active-ready-transition | Error Memory strict Heuristic Correction active-ready transition | frozen
- 2026-06-27 | freeze-20260627-stage-active-ready-replacement-lesson-for-ml-pilot-activation-state-draft | Stage active-ready replacement lesson for ml_pilot_activation_state draft | frozen
- 2026-06-27 | freeze-20260627-prompt-router-bridge-for-error-memory-active-ready-correction-blueprint | Prompt Router Bridge for Error Memory Active-Ready Correction Blueprint | frozen
- 2026-06-27 | freeze-20260627-no-isolated-zip-freeze-hint-readiness-repair-v1 | No Isolated ZIP Freeze Hint Readiness Repair v1 | frozen
- 2026-06-27 | freeze-20260627-governed-implementation-router-bridge-gate-v1 | Governed Implementation Router Bridge Gate v1 | frozen
- 2026-06-27 | freeze-20260627-user-detected-correction-router-bridge-gate-v1 | User-Detected Correction Router Bridge Gate v1 | frozen
- 2026-06-27 | freeze-20260627-startup-project-ready-check-after-second-upload-v1 | Startup Project Ready Check after second upload v1 | frozen
