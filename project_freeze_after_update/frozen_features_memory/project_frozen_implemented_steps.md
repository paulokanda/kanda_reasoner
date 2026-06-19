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
