# KANDA REASONER TOOL VERSUS PROJECT

## Complete-source audit and updated pre-implementation roadmap

Date: 2026-07-31

Project in use: KANDA REASONER

External validation Project: EEG_KANDA

Supersedes as implementation plan:

`0058 COMPLETE SEPARATION TOOL VERSUS PROJECT 30.07.26.MD`

---

# 1. Purpose

This document updates the Tool-versus-Project roadmap after auditing:

1. The complete uploaded KANDA Reasoner project ZIP.
2. The complete 0058 Tool/Project separation discussion and roadmap.
3. Current source-level boundary, memory, archive, Project Web AI, shell-session, patch-governance, Workbench, and validation owners.
4. Current focused validators that could be executed safely against the extracted source tree.
5. Current compact Error Memory lessons already loaded for KANDA Reasoner.

This is a pre-implementation artifact.

No KANDA Reasoner source was modified during this audit.

No EEG_KANDA source or Project Support data was modified.

---

# 2. Audit scope and evidence limits

## 2.1 Complete project inspected

The uploaded project ZIP contained:

- 8,719 archive members.
- Approximately 403 MB uncompressed.
- KANDA Reasoner source.
- Tool validators.
- Prompt workspace and active canons.
- Generated and historical evidence.
- Build and cache material.
- Workbench outputs and supporting implementation.

The complete ZIP is a working-tree capture, not the same thing as a governed Tool source archive. Build products, caches, and generated evidence physically present in the working tree may still be correctly excluded by the governed source-archive policy.

## 2.2 Evidence classifications used

### VERIFIED IN SOURCE AND FOCUSED VALIDATOR PASSED

The implementation exists in current exact source, and an applicable focused validator passed against the extracted source.

### VERIFIED IN SOURCE; FULL INSTALLED VALIDATION NOT PROVEN

The implementation exists, but the authoritative installed Windows validation, receipt-backed validation, or real Qt runtime gate was not completed during this audit.

### PARTIAL

A strong implementation exists for part of the system, but it is not yet the common contract for all Boxes.

### NOT FOUND

No current implementation of the requested contract was found through direct source inspection and search.

### VALIDATOR DRIFT

The current source or canon has changed, but a validator still expects stale text, a retired contract, or an obsolete caller.

## 2.3 Runtime limitation

PySide6 was not available in the audit environment.

Therefore, source-level and non-Qt functional checks could be run, but real Qt GUI runtime conclusions remain pending.

This roadmap must not treat source-level success as proof of installed Windows GUI success.

---

# 3. Executive verdict

The central architecture in 0058 remains correct:

- KANDA Reasoner is an independent reusable Tool Box.
- A selected Project is an independent Project Box.
- The Project is inserted operationally through a controlled boundary.
- Operational insertion does not transfer ownership.
- External Project work must not silently modify KANDA Reasoner.
- A Tool defect discovered during external Project work becomes a separate Tool work order.
- Tool and Project memory, validation, support, package, and Freeze ownership remain separate.

However, the complete-source audit changes the implementation plan materially.

## 3.1 Capabilities that already exist

The roadmap must not rebuild these:

1. Explicit Project selection.
2. Explicit self-hosting.
3. Tool-owned Project selection registry.
4. Stable registry Project IDs.
5. No implicit Tool-root-to-Project fallback.
6. Owner-scoped Error Memory.
7. Owner-scoped Freeze behavior.
8. Foreign-owner canonical memory rejection.
9. Read-only cross-owner lesson references.
10. Tool source classification.
11. External Project capture exclusion.
12. Allowlist-driven Tool source archives.
13. Safe ZIP member validation.
14. Post-extraction physical containment.
15. Show Project versus Portable Distribution separation.
16. A mature Project Web AI governed-apply vertical slice.
17. Project Web AI request identity, epoch, snapshot, source hash, authorization, backup, receipt, and rollback protection.

## 3.2 Highest-priority remaining architecture problem

Current source contains a strict explicit Project registry, but multiple runtime and durable-state consumers still call the compatibility resolver:

`resolve_project_tool_boundary_identity(...)`

That facade explicitly states that it is for compatibility-only read paths and that new mutation-capable callers must use explicit selection.

The audit found:

- 28 total compatibility-resolver call sites.
- 16 call sites inside `kanda_reasoner_app`.
- At least one direct mutation authority:
  - `reasoner_engine/project_web_ai_write_broker.py`
- Durable owner derivation:
  - `memory_ownership/context.py`
- Freeze and Error Memory GUI contracts.
- General handoff generation.
- Architecture Review and documentation workflows.

This is the main authority gap.

The next boundary release must migrate mutation-capable and durable-owner consumers to the Tool-owned registry-backed identity. It must not create another identity engine.

## 3.3 Highest-priority pre-implementation quality problem

The project contains widespread contradictory module-size rules.

The 0058 discussion correctly rejects an artificial minimum and states that a cohesive 45-line module is better than a padded 110-line module. Later in the same roadmap, section 18 requires every new or modified Python module to be strictly more than 100 lines.

Current source also contains obsolete 101-499 policies across validators and runtime refactoring planners.

The audit found 63 files containing relevant minimum-size language or enforcement patterns, including:

- 38 files under `tools`.
- Active Tool/Project validators.
- AST-safe refactor validators.
- Workbench planning and feasibility logic.
- Workbench Freeze and Shadow validation.
- Refactor tutorials and orchestration code.

The active startup canon is correct:

- Ideal maximum: 400 code lines when cohesion permits.
- Hard maximum: 500 physical lines.
- Minimum: none.
- Never pad, compress, or duplicate logic to satisfy a line rule.

This contradiction must be reconciled before adding new boundary modules.

## 3.4 Highest-priority validation problem

Several current validators are stale relative to current source or current prompt canon.

Examples:

- Shell Project synchronization validator expects:
  - `self._remember_project_root(project_root)`
- Current shell source uses:
  - `self._remember_project_boundary(next_boundary)`

The validator fails before completing its current-source audit.

Several Brick Wall validators also fail because they search for obsolete exact phrases rather than validating the current semantic contract.

This is validator drift, not evidence that every corresponding runtime capability is absent.

A pre-implementation canon/validator reconciliation release is mandatory.

---

# 4. Canonical Box model

## 4.1 KANDA Reasoner Tool Box

Owns:

- Tool source.
- Tool runtime.
- Tool governance.
- Tool prompt infrastructure.
- Tool validators.
- Tool Error Memory.
- Tool Freeze evidence.
- Tool release.
- Tool Portable Distribution.
- Tool-side Project selection registry.
- Tool-specific durable support evidence.

Does not own:

- External Project source.
- External Project implementation.
- External Project validation truth.
- External Project Error Memory.
- External Project Freeze Memory.

## 4.2 Active Project Box

Owns:

- Project source.
- Project configuration.
- Project tests.
- Project runtime behavior.
- Project-specific implementation.
- Project-specific validators.
- Project-specific generated source.

Does not own:

- KANDA Reasoner source.
- KANDA Reasoner governance.
- KANDA Reasoner runtime.
- KANDA Reasoner release.

## 4.3 Project Support Box

Canonical pattern:

`<project_drive>\<project_slug>_show_project_to_AI`

Owns durable Project-specific evidence:

- AI handoffs.
- Project Error Memory.
- Project Freeze Memory.
- Project validation evidence.
- Audit reports.
- Migration receipts.
- Project support metadata.

Project Support is not Project source.

Project Support is not Tool governance.

Project Support cannot authorize itself.

## 4.4 Tool Support Box

Canonical KANDA Reasoner location:

`E:\kanda_reasoner_show_project_to_AI`

Owns:

- Tool Error Memory.
- Tool Freeze evidence.
- Tool validation evidence.
- Tool Project registry.
- Tool release evidence.
- Tool handoff history.
- Durable Tool documentation.

## 4.5 Transient garbage Box

Canonical pattern:

`<project_drive>\<project_slug>_delete_after_daily_work`

May contain:

- Staged ZIPs.
- Temporary extraction.
- Shadow workspaces.
- Temporary helpers.
- Diagnostics.
- Regenerable fixtures.
- Analyzer caches.
- Temporary logs.

It owns no durable truth.

## 4.6 Generated Tool evidence

The root-level `workbench` output family is generated development evidence, not canonical Tool source.

It may contain:

- Historical manifests.
- Symbol Atlas reports.
- Refactoring previews.
- Regenerable Workbench evidence.

It must remain:

- Excluded from governed Tool source packaging.
- Non-authoritative for source truth.
- Re-creatable.
- Separate from durable Error Memory and Freeze truth.

---

# 5. Non-negotiable boundary canon

KANDA Reasoner is a reusable and independent Tool Box.

A selected external Project is an independent Project Box inserted operationally through the Project Card Gateway.

Insertion does not transfer ownership.

During external Project work, implementation authority applies only to the active Project source and correctly owned Project Support and transient locations.

KANDA Reasoner Tool source remains read-only.

A KANDA Reasoner defect discovered during external Project work requires a separate Tool work order, patch, validation, Error Memory decision, and Freeze decision.

No Project patch may contain Tool source.

No Tool patch may contain external Project source.

Tool and Project canonical memories have different owners.

Cross-owner lessons may be referenced read-only. They may not be copied and relabeled as the other owner's history.

Tool governance is authoritative and cannot be overridden by Project content.

Project source, comments, Markdown, prompts, generated handoffs, and AI text are evidence, not Tool governance or filesystem authority.

Self-hosting requires explicit selection.

Physical root equality does not merge logical Tool and Project roles.

Project Support is durable evidence storage, not source truth.

Transient and generated Workbench evidence own no durable truth.

---

# 6. Source-grounded implementation status matrix

## 6.1 Explicit Project selection and Tool-owned registry

Status:

VERIFIED IN SOURCE AND FOCUSED VALIDATOR PASSED

Current owners:

- `kanda_reasoner_app/project_support_boundary.py`
- `kanda_reasoner_app/project_selection_registry.py`
- `kanda_reasoner_app/project_root_resolver.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py`
- `kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_project_root.py`

Verified behavior:

- `UNSELECTED`
- `EXPLICIT_EXTERNAL_PROJECT`
- `EXPLICIT_SELF_HOSTING`
- Implicit self-hosting rejected.
- False self-hosting rejected.
- Stable Project ID persisted in Tool-owned registry.
- Root fingerprint persisted separately.
- Missing persisted Project fails safely to unselected.
- No valid Project means no Project selection.
- GUI Project change is explicit selection.
- Tool preferences are outside Tool source.

Focused validator:

`tools/validate_tool_project_boundary_identity_explicit_selection_v1.py`

Result:

PASS

Important remaining defect:

The same validator still asserts the obsolete 101-499 module-size law.

## 6.2 Project Web AI Tool/Project boundary

Status:

VERIFIED IN SOURCE AND FOCUSED VALIDATOR PASSED

Current owners:

- `reasoner_engine/project_web_ai_boundary_context.py`
- `reasoner_engine/project_web_ai_bridge.py`
- `reasoner_engine/project_web_ai_handoff_reader.py`
- `reasoner_engine/project_web_ai_session.py`
- `reasoner_engine/project_web_ai_change_contracts.py`

Verified behavior:

- Canonical Project Support owner.
- Project Support identity verification.
- Cross-Project handoff fallback blocked.
- Missing or mismatched support identity blocked.
- Self-hosting logical separation.
- Full request identity.
- Project epoch.
- Snapshot identity.
- Protected Tool and Project export roots.
- Exact selected Project source treated as untrusted data.
- Remote AI has proposal authority only.

Focused validator:

`tools/validate_project_web_ai_tool_project_boundary_v1.py`

Result:

PASS

Remaining defect:

The boundary and handoff contexts still derive identity through the compatibility resolver instead of consuming the registry-backed explicit current boundary.

## 6.3 Project Web AI governed apply

Status:

VERIFIED IN SOURCE; REAL QT RUNTIME NOT PROVEN

Current owners:

- `reasoner_engine/project_web_ai_apply_contracts.py`
- `reasoner_engine/project_web_ai_write_broker.py`
- `reasoner_engine/project_web_ai_write_storage.py`
- `reasoner_engine/project_web_ai_session.py`

Current strengths:

- One-use human authorization.
- Exact operation identity.
- Project ID, root fingerprint, epoch, and snapshot checks.
- Exact selected target set.
- Immediate source freshness.
- Shadow payload hash verification.
- Bounded Project source writes.
- Backups.
- Durable receipt.
- Rollback.
- Unresolved transaction blocks Project switching.
- Symlink component rejection.
- Windows junction guard.
- Remote AI has no write capability.
- Post-write handoff refresh required.
- 500-line hard maximum.

Focused validator:

`tools/validate_project_web_ai_governed_apply_v1.py`

Result:

PASS for source-level and non-Qt behavior.

Qt result:

`REAL_QT_GOVERNED_APPLY_DIALOG: NOT_APPLICABLE`

Critical remaining defect:

`project_web_ai_write_broker.py` calls the compatibility identity resolver during mutation authorization.

## 6.4 Owner-scoped Error Memory and Freeze

Status:

VERIFIED IN SOURCE; REGISTRY AUTHORITY MIGRATION INCOMPLETE

Current owners:

- `memory_ownership/context.py`
- `error_memory/backend.py`
- `error_memory/cross_owner_reference.py`
- `error_memory/importer.py`
- `freeze_after_update/ownership.py`

Current strengths:

- Tool and Project backends are separate.
- Owner metadata is assigned by the store.
- Form or AI content cannot grant canonical owner authority.
- Tool lessons are rejected from Project canonical storage.
- Project lessons are rejected from Tool canonical storage.
- Foreign canonical imports fail closed.
- Cross-owner references are read-only.
- Cross-owner references are excluded from canonical counts.
- Self-hosting preserves logical ownership separation.
- Wrong-owner Freeze writes are rejected.

Remaining defect:

`project_owner_context()` uses the compatibility resolver and therefore path-derived legacy Project identity.

Historical EEG_KANDA memory migration remains pending.

## 6.5 Tool source and archive hygiene

Status:

VERIFIED IN SOURCE; RECEIPT-BACKED INSTALLED VALIDATION NOT RUN

Current owners:

- `archive_safety.py`
- `source_hygiene/`
- `reasoner_context_bundle/source_archive_routing.py`
- `reasoner_context_bundle/source_tree_exporter_inventory.py`
- `portable/archive.py`
- `portable/build.py`
- `portable/policy.py`
- `patch_governance/zip_member_contract.py`

Current strengths:

- Fail-closed Tool source classification.
- Unclassified paths rejected.
- External Project captures excluded.
- Tool source archive allowlist.
- PyInstaller data allowlist.
- Package-wide data collection rejected.
- Generated dependency workspaces excluded.
- Directory pruning avoids repeated recursive rescans.
- Source exporter compatibility facade preserved.
- Show Project and Portable Distribution remain separate Boxes.
- ZIP absolute, drive, UNC, traversal, duplicate, case-collision, file-directory collision, symlink, undeclared payload, and missing-manifest cases rejected.
- Physical post-extraction containment exists.

Brick Wall Q26 validator:

PASS

Remaining work:

- Remove obsolete minimum module-size enforcement from Release 3 validator.
- Run the authoritative installed Windows validation with current receipts.
- Continue reusing the current archive safety implementation instead of introducing a second archive engine.

## 6.6 General shell Project synchronization

Status:

PARTIAL AND VALIDATOR DRIFT

Current owners:

- `reasoner_tools_gui_shell/project_scope_sync.py`
- `reasoner_tools_gui_shell/main_window_help/window_tool_patches.py`

Current strengths:

- Canonical active Project root.
- Project switch epoch.
- Propagation to Project-scoped tabs.
- Old Project transient state cleared.
- Global configuration preserved.
- Known active work can block switching.

Current weaknesses:

- Multiple private worker/process attributes are inspected.
- No universal public Project-session component protocol.
- No common cooperative cancellation and bounded settlement contract.
- No `close_active_project()` safe-eject owner found.
- No complete `RECOVERY_REQUIRED` lifecycle found.
- No owner-root interprocess durable-write lock found.

Focused validator:

`tools/validate_shell_active_project_sync_v1.py`

Result:

FAIL due validator drift.

The validator expects an obsolete call:

`self._remember_project_root(project_root)`

Current source uses:

`self._remember_project_boundary(next_boundary)`

This validator must be reconciled before runtime changes.

## 6.7 General handoff trust

Status:

PARTIAL

Current strengths:

- Project Web AI system prompts explicitly treat selected source, comments, logs, and handoff evidence as untrusted data.
- Generated artifacts are labeled as evidence rather than source truth.
- Project identity, epoch, support root, root fingerprint, snapshot, and context hash are checked in Project Web AI.
- Cross-Project fallback is blocked.

Missing general contracts:

- No structural general `content_trust` envelope was found.
- General handoff generation still uses compatibility identity.
- No separate `PROJECT_SUPPORT_OWNER.json` two-sided trust artifact was found.
- No package-owned Tool governance loader using `importlib.resources` was found.

## 6.8 Patch ownership and provenance

Status:

PARTIAL

Current strengths:

- Existing patch-governance module.
- Exact ZIP member contract.
- Manifest-declared payload.
- Containment and collision rejection.
- Freeze payload contracts.
- Strong Brick Wall ZIP protection.

Missing general contracts:

- No universal one-owner patch manifest using Tool or stable Project ID.
- No universal materials/subjects provenance with boundary digest.
- No universal mixed Tool/Project payload rejection based on stable owner identity.
- No common operation authority passed from the active Project boundary into every patch builder.

## 6.9 Workbench mutation safety

Status:

PARTIAL BUT MATURE

Current owners include:

- `engineering_safety/project_mutation_lane.py`
- `manage_architecture/large_file_refactor_planner/workbench_refactor_transaction.py`
- Workbench transaction stores and journaled apply owners.

Current strengths:

- Dedicated mutation lane.
- Journaled application.
- Rollback support.
- Source and transaction evidence.
- Strong refactoring-specific validation.

Remaining identity problem:

Workbench uses a physical Project ID derived from the resolved path.

That may remain a physical-location fingerprint, but it must not serve as the stable logical Project identity.

The final model should retain:

- Stable Project ID from Tool registry.
- Current physical root fingerprint.
- Workbench transaction ID.
- Existing Workbench transaction implementation.

Do not replace the Workbench transaction engine.

## 6.10 Tool governance resource ownership

Status:

NOT FOUND

No current governance loading implementation based on `importlib.resources` was found.

Before implementing it, the project must identify:

- Canonical governance source.
- Generated packaged resource.
- Generator/synchronization owner.
- Portable and source-install behavior.
- Validation of source-to-package synchronization.

Do not treat generated prompt workspace copies as canonical source without reconciliation.

---

# 7. Validator evidence from this audit

## 7.1 Passed

### Explicit Project boundary and registry

`VALIDATION OK: tool-project-boundary-identity-explicit-selection-v1`

`STATUS: IN_SYNC`

### Project Web AI Tool/Project boundary

`VALIDATION OK: project-web-ai-tool-project-boundary-v1`

`STATUS: IN_SYNC`

### Project Web AI governed apply

`VALIDATION OK: project-web-ai-governed-apply-v1`

`STATUS: IN_SYNC`

Qt dialog gate:

NOT APPLICABLE in this environment.

### Brick Wall Q21 negative boundary matrix

`VALIDATION OK: brick-wall-q21-parametrized-negative-boundary-matrix-enforcement-v1`

`STATUS: IN_SYNC`

### Brick Wall Q26 ZIP containment and collision hardening

`VALIDATION OK: brick-wall-q26-zip-containment-collision-hardening-enforcement-v1`

`STATUS: IN_SYNC`

## 7.2 Failed because of validator/canon drift

### Shell active Project synchronization

Fails while searching for an obsolete method call.

### Brick Wall Q06 Tool/Project identity

Fails while expecting an old exact record field:

`Tool task or Project operation: TOOL_CHANGE / PROJECT_OPERATION / MIXED_GOVERNED / BLOCKED`

### Brick Wall Q07 ownership and no-leak classification

Fails while expecting the exact phrase:

`NO_LEAK_LOGIC_V1`

inside a current owner document that no longer contains that exact marker.

### Brick Wall Q37 canonical ownership reconciliation

Its regression set passes, then it fails while searching for old exact phrases:

- `Public Contract, Private Internals`
- `No Private Reach-In`

These failures demonstrate validator-to-canon drift.

They do not authorize bypassing the validators.

They require a governed reconciliation of the current canonical owner and current validation contract.

---

# 8. Internal contradictions in the previous 0058 roadmap

## 8.1 Module size

Earlier analysis in 0058:

- Rejects the artificial 101-line minimum.
- States minimum is none.
- Rejects padding.

Later final roadmap:

- Requires every new or modified Python module to be strictly more than 100 lines.

Decision:

The later requirement is rejected.

Canonical rule:

- Ideal at most 400 code lines when cohesive.
- Hard maximum 500 physical lines.
- Minimum none.
- No padding.
- No code compression.
- No duplication to fit.

## 8.2 Release status

The previous roadmap presents Releases 1-3 as future implementation.

Complete-source audit shows that the core functions of Releases 1-3 already exist.

Decision:

Treat them as implemented baseline capabilities with targeted reconciliation work.

Do not rebuild them.

## 8.3 Operation scope design

The previous roadmap proposes a new generic OperationScope from first principles.

Current Project Web AI already implements a strong operation-specific vertical slice with:

- Operation ID.
- Project ID.
- Root fingerprint.
- Epoch.
- Snapshot.
- Selected source hashes.
- One-use human authorization.
- Freshness checks.
- Backups.
- Receipt.
- Rollback.
- Unresolved transaction state.

Decision:

Extract the smallest shared authority contract from the proven vertical slice.

Do not create a new oversized execution framework.

## 8.4 Session design

The previous roadmap proposes ProjectSessionController as a new concept.

Current source already has:

- General shell Project synchronization.
- Project Web AI session lifecycle.
- Project epoch.
- Pending root.
- Worker settlement.
- Transaction switch blocking.

Decision:

Reconcile and elevate existing owners.

Do not create a third session system.

## 8.5 Archive design

The previous roadmap proposes archive validation as future work.

Current source already has mature archive and ZIP safety.

Decision:

Extend current patch provenance and owner contracts.

Do not create another archive builder or extractor.

---

# 9. Architecture decisions retained

1. Tool and Project remain separate bounded contexts.
2. Project Card Gateway functions as an Anti-Corruption Layer.
3. Operational hosting is not ownership.
4. Consequential operations require least authority.
5. Project Support cannot authorize itself.
6. Tool registry is the trusted identity authority.
7. Project content is untrusted as Tool instructions.
8. Tool governance must remain Tool-owned.
9. Every patch has one owner.
10. Mixed Tool/Project patches fail closed.
11. Stale Project results fail closed.
12. Project switching uses cooperative cancellation and bounded settlement.
13. Durable support writes require interprocess exclusion.
14. Historical memory migration is Preview-first and human-confirmed.
15. Architecture readiness uses independent mandatory dimensions, not one weighted score.
16. Existing transaction, rollback, archive, and memory owners are reused.

---

# 10. Architecture proposals rejected or deferred

## 10.1 Rejected

- Global Execution Arbiter.
- New universal write engine.
- Distributed two-phase commit.
- Large machine-card state engine.
- Duplicate Project Support resolver.
- Duplicate patch builder.
- Duplicate archive extractor.
- Duplicate memory engine.
- Path-derived stable Project identity.
- Artificial 101-line minimum.
- Generic no-argument behavior probes.
- Runtime full-tree leak scans.
- Direct automatic Freeze writes.
- Automatic Error Memory memorization.
- Mixed Tool/Project delivery.

## 10.2 Deferred

- Persistent AST cache.
- Parallel AST validation.
- Incremental dependency-cone validation.
- Refactoring dashboard.
- Digital signatures.
- User-editable governance policy language.

These may be reconsidered only after deterministic correctness and complete Tool/Project readiness are proven.

---

# 11. Updated implementation sequence

The implementation now begins with reconciliation, not with a new boundary engine.

---

# Release 0A - Canon, validator, and module-size reconciliation

## 11.1 Objective

Restore agreement among:

- Current source.
- Current active canons.
- Current startup bridges.
- Current validators.
- Current roadmap.

No Tool/Project runtime behavior should change in this release.

## 11.2 Required work

1. Inventory every active 101-499 or minimum-helper-size rule.
2. Classify each as:
   - Obsolete universal rule.
   - Feature-specific justified limit.
   - Unrelated numeric use.
3. Remove the obsolete universal minimum from:
   - Tool/Project boundary validators.
   - Tool archive validators.
   - AST-safe refactor orchestration.
   - Workbench planning.
   - Workbench Shadow validation.
   - Workbench Freeze checks.
   - Tutorials and prompts.
4. Preserve the hard 500-line maximum.
5. Add a small cohesive-module acceptance fixture.
6. Add a no-padding requirement.
7. Reconcile stale Shell Project synchronization validator with current public source contract.
8. Reconcile Brick Wall Q06, Q07, Q12, Q13, Q37 and any dependent validators with current canonical owners.
9. Replace brittle obsolete exact-string checks with current exact public-contract checks where appropriate.
10. Preserve canonical source ownership and generated artifact synchronization.

## 11.3 Required output

A reconciliation matrix containing:

- Validator.
- Current canonical owner.
- Expected current contract.
- Obsolete expectation.
- Required disposition.
- Changed files.
- Validation result.

## 11.4 Required markers

`NO_ARTIFICIAL_MINIMUM_MODULE_SIZE: PASS`

`SMALL_COHESIVE_MODULE_ACCEPTED: PASS`

`TOUCHED_SOURCE_MODULES_MAX_500: PASS`

`NO_PADDING_OR_COMPRESSION_REQUIRED: PASS`

`SHELL_ACTIVE_PROJECT_SYNC_VALIDATOR_CURRENT: PASS`

`BRICK_WALL_VALIDATOR_CANON_ALIGNMENT: PASS`

`NO_RUNTIME_BEHAVIOR_CHANGE: PASS`

`VALIDATION OK: tool-project-canon-validator-reconciliation-v1`

`STATUS: IN_SYNC`

## 11.5 Freeze rule

Freeze Release 0A separately before changing boundary authority.

---

# Release 0B - Exact authority and consumer inventory

## 11.6 Objective

Identify every runtime and durable-state consumer that currently derives identity, support ownership, or write authority.

This is characterization and implementation planning.

## 11.7 Required inventory

For every compatibility-resolver caller, record:

- File.
- Symbol.
- Read-only or mutation-capable.
- Source owner.
- Support owner.
- Current identity source.
- Required stable identity source.
- Current validator.
- Required negative test.
- Migration release.

At minimum include:

- Project Web AI write broker.
- Project Web AI boundary and bridge.
- Project handoff generation.
- Memory owner context.
- Error Memory GUI.
- Freeze GUI.
- Architecture Review AI contracts.
- Documentation insertion workflows.
- Manual review runtime.
- Project structure visualizer.
- Workbench physical Project ID.
- Patch builders and installers.
- Shell Project session propagation.

## 11.8 Classify write systems

Identify current separate transaction owners:

1. Project Web AI governed apply.
2. Workbench journaled apply.
3. Documentation insertion.
4. Architecture Review apply.
5. Error Memory write.
6. Freeze write.
7. Handoff publication.
8. Patch installation.
9. Tool source corrections.

The result must distinguish:

- Shared authority preconditions.
- Box-specific transaction logic.
- Box-specific rollback logic.
- Durable evidence owner.

## 11.9 Required markers

`COMPATIBILITY_RESOLVER_CONSUMERS_COMPLETE: PASS`

`MUTATION_CAPABLE_CALLERS_CLASSIFIED: PASS`

`DURABLE_OWNER_CALLERS_CLASSIFIED: PASS`

`CURRENT_WRITE_OWNERS_COMPLETE: PASS`

`NO_DUPLICATE_EXECUTION_ENGINE_PROPOSED: PASS`

`CHANGED_FILE_VALIDATOR_MAP_READY: PASS`

`NO_SOURCE_MODIFICATION: PASS`

---

# Release 1R2 - Registry-backed stable identity authority

## 11.10 Objective

Make the Tool-owned Project selection registry the stable identity authority for every mutation-capable and durable-owner operation.

## 11.11 Reuse current owners

Reuse:

- `project_selection_registry.py`
- `project_support_boundary.py`
- Current shell selected Project boundary.
- Current Project Web AI request/session identity.
- Current owner-scoped memory types.

Do not add another Project registry.

## 11.12 Required changes

1. Mutation-capable callers receive the explicit current boundary.
2. Durable memory and Freeze callers receive the explicit current boundary.
3. General handoff generation receives the explicit current boundary.
4. Compatibility resolver remains read-only only.
5. Add a validator that fails if a mutation-capable module imports or calls the compatibility resolver.
6. Keep stable Project ID separate from root fingerprint.
7. Convert Workbench path-derived Project ID into:
   - Physical root fingerprint.
   - Stable registry Project ID.
8. Preserve approved Project move/rename reconciliation.
9. Preserve explicit self-hosting.
10. Preserve logical Tool/Project owner separation during self-hosting.

## 11.13 Two-sided Project Support trust

Add one Project Support identity artifact, conceptually:

`PROJECT_SUPPORT_OWNER.json`

It records evidence matching the Tool registry:

- Stable Project ID.
- Project slug.
- Root fingerprint.
- Approved Project Support root.
- Schema version.
- Creation and reconciliation provenance.

Authority requires:

1. Explicit human selection.
2. Current Tool registry record.
3. Canonical root validation.
4. Project Support owner evidence match.
5. No conflicting owner.
6. Current operation authority.

The Project Support artifact is evidence.

It cannot authorize itself.

## 11.14 Required markers

`STABLE_PROJECT_ID_REGISTRY_AUTHORITY: PASS`

`MUTATION_CALLER_COMPATIBILITY_RESOLVER_REJECTED: PASS`

`DURABLE_MEMORY_REGISTRY_IDENTITY: PASS`

`FREEZE_REGISTRY_IDENTITY: PASS`

`HANDOFF_REGISTRY_IDENTITY: PASS`

`WORKBENCH_STABLE_AND_PHYSICAL_IDENTITY_SEPARATE: PASS`

`PROJECT_SUPPORT_OWNER_EVIDENCE_PRESENT: PASS`

`PROJECT_CANNOT_SELF_AUTHORIZE: PASS`

`TOOL_REGISTRY_SUPPORT_EVIDENCE_CROSSCHECK: PASS`

`EXPLICIT_SELF_HOSTING_PRESERVED: PASS`

`VALIDATION OK: registry-backed-project-authority-v1`

`STATUS: IN_SYNC`

---

# Release 2R2 - Shared minimal operation authority

## 11.15 Objective

Generalize the smallest proven authority contract from Project Web AI without replacing existing Box-specific transaction engines.

## 11.16 Proven source to reuse

Project Web AI already provides:

- Operation ID.
- Stable Project identity fields.
- Root fingerprint.
- Project epoch.
- Snapshot identity.
- Selected source hashes.
- One-use human authorization.
- Target-set binding.
- Immediate prewrite freshness.
- Backup.
- Receipt.
- Rollback.
- Unresolved transaction blocking.

This is the reference implementation.

## 11.17 Shared immutable authority value

Create one small contract containing only fields required for enforcement:

- Owner scope.
- Stable owner ID.
- Allowed root.
- Allowed operation kinds.
- Project root fingerprint.
- Project switch epoch.
- Operation ID.
- Source snapshot identity when applicable.
- Selection mode.
- Expiration or invalidation condition.

Do not create many scope subclasses unless they reduce invalid states.

## 11.18 Shared authority guard

One public guard should verify:

1. Scope is current.
2. Stable owner still matches.
3. Root fingerprint still matches.
4. Epoch still matches.
5. Operation kind is allowed.
6. Target resolves inside the permitted root.
7. Target is outside protected subroots.
8. Required source snapshot remains current.
9. Self-hosting role is explicit.
10. Ownership is resolved.

## 11.19 Integration strategy

Integrate incrementally into existing writers.

Do not replace:

- Project Web AI write broker.
- Workbench transaction engine.
- Error Memory backend.
- Freeze backend.
- Existing archive safety.
- Existing patch installation transaction.

The shared contract supplies authority.

Each Box retains transaction and rollback ownership.

## 11.20 Required Windows path matrix

- Exact root.
- Child path.
- Shared text-prefix sibling.
- Different case.
- Different drive.
- Relative path.
- Parent traversal.
- Symbolic link into Tool source.
- Junction into Tool source.
- Junction out of Project source.
- Broken link.
- Unsupported reparse point.
- Same physical root alias.
- Explicit self-hosting.

## 11.21 Required markers

`OPERATION_AUTHORITY_EXPLICIT: PASS`

`PROJECT_WRITE_SCOPE_TOOL_SOURCE_REJECTED: PASS`

`TOOL_WRITE_SCOPE_EXTERNAL_PROJECT_REJECTED: PASS`

`PROJECT_SUPPORT_SCOPE_TOOL_SUPPORT_REJECTED: PASS`

`STALE_SCOPE_AFTER_PROJECT_SWITCH_REJECTED: PASS`

`STALE_SCOPE_AFTER_ROOT_CHANGE_REJECTED: PASS`

`STALE_SCOPE_AFTER_SOURCE_CHANGE_REJECTED: PASS`

`EXPLICIT_SELF_HOSTING_SCOPE_REQUIRED: PASS`

`WINDOWS_REPARSE_POINT_BOUNDARY_MATRIX: PASS`

`EXISTING_BOX_TRANSACTION_OWNERS_PRESERVED: PASS`

`NO_GLOBAL_EXECUTION_ARBITER: PASS`

`VALIDATION OK: shared-tool-project-operation-authority-v1`

`STATUS: IN_SYNC`

---

# Release 3R2 - General Project session lifecycle and safe eject

## 11.22 Objective

Reconcile the general shell session with the proven Project Web AI lifecycle and remove private thread/process reach-in as the canonical API.

## 11.23 Reuse current owners

Reuse:

- General shell Project synchronization.
- Current Project switch epoch.
- Project Web AI session lifecycle.
- Existing transaction switch blockers.
- Current Qt ownership and cleanup conventions.

Do not create a third unrelated session system.

## 11.24 Public component protocol

Project-scoped components expose the equivalent of:

- `has_active_project_work()`
- `request_project_work_cancel()`
- `await_project_work_settlement(timeout)`
- `can_accept_project_context(context)`
- `apply_project_context(context)`
- `clear_project_context()`

Temporary compatibility adapters may inspect old private attributes during migration, but validators must identify and retire them.

## 11.25 Switch sequence

1. Block new Project operations.
2. Detect active Project work.
3. Request cooperative cancellation.
4. Await bounded settlement.
5. Keep current Project active if settlement fails.
6. Build registry-backed new boundary.
7. Validate Project Support owner evidence.
8. Ask components to accept the new context.
9. Clear old transient Project state.
10. Apply the new context.
11. Persist after full success only.
12. Advance epoch after full success only.
13. Restore old context when safe.
14. Enter `RECOVERY_REQUIRED` only if safe restoration is impossible.

## 11.26 Safe eject

Implement one public action:

`close_active_project()`

It must:

- Block new work.
- Settle active work.
- Reject unresolved mutations.
- Clear Project-scoped UI state.
- Disconnect Project callbacks.
- Invalidate authority.
- Release locks.
- Transition to unselected.
- Preserve Project source.
- Preserve durable Project Support.
- Write an owner-correct receipt.

## 11.27 Durable-write interprocess locks

Use a standard interprocess lock facility.

Preferred when the Qt runtime contract supports it:

`QLockFile`

Required lock owners:

- Project Support durable write.
- Tool Support durable write.
- Project source apply.

The current per-operation transient exclusive-create lock may remain inside Project Web AI, but it is not a substitute for owner-root multi-instance exclusion.

## 11.28 Required markers

`PUBLIC_PROJECT_SESSION_PROTOCOL: PASS`

`PROJECT_SWITCH_IDLE_FAST_PATH: PASS`

`ACTIVE_WORK_CANCEL_AND_SETTLE: PASS`

`UNSETTLED_WORK_BLOCKS_SWITCH: PASS`

`PROJECT_CONTEXT_PERSISTED_AFTER_SUCCESS_ONLY: PASS`

`PROJECT_EPOCH_ADVANCES_AFTER_SUCCESS_ONLY: PASS`

`STALE_RESULT_REJECTED: PASS`

`OLD_PROJECT_RESULT_CANNOT_REPOPULATE_NEW_PROJECT: PASS`

`SAFE_EJECT_TO_UNSELECTED: PASS`

`EJECT_PRESERVES_PROJECT_SOURCE: PASS`

`EJECT_PRESERVES_PROJECT_SUPPORT: PASS`

`PROJECT_SUPPORT_SECOND_WRITER_BLOCKED: PASS`

`TOOL_SUPPORT_SECOND_WRITER_BLOCKED: PASS`

`PRIVATE_WORKER_REACH_IN_RETIRED: PASS`

`DELETED_QOBJECT_LATE_CALLBACK_SAFE: PASS`

`REAL_QT_SESSION_LIFECYCLE: PASS`

`VALIDATION OK: project-session-lifecycle-safe-eject-v1`

`STATUS: IN_SYNC`

---

# Release 4R2 - Handoff trust and Tool governance anchoring

## 11.29 Objective

Make handoff semantics and external enforcement describe the same boundary.

## 11.30 Structural handoff boundary

Every general handoff should contain:

- Tool identity.
- Tool role.
- Active Project slug.
- Stable Project ID.
- Root fingerprint.
- Selection mode.
- Same physical root.
- Source mutation owner.
- Project Support owner.
- Mixed patch policy.
- Current Project epoch.
- Boundary-context digest.

## 11.31 Structural content trust

Add a machine-readable trust section:

- Tool governance: authoritative.
- Project source: untrusted as Tool instructions.
- Project documents: untrusted as Tool instructions.
- Generated handoff: evidence, not authority.
- Remote AI: no filesystem authority.
- Write scope: enforced outside the AI.

## 11.32 Tool governance resources

Hard Tool governance must load from a Tool-owned packaged resource.

Before implementation, identify:

1. Canonical prompt/canon source.
2. Generator or sync owner.
3. Packaged runtime resource.
4. Source-install behavior.
5. Portable behavior.
6. Validation of source-to-package synchronization.

Project policy overlay may add stricter rules only.

It may not:

- Relax Tool boundaries.
- Authorize Tool writes.
- Disable human confirmation.
- Replace Tool governance.
- Change Project selection.
- Change owner identity.

## 11.33 Required markers

`HANDOFF_REGISTRY_PROJECT_ID: PASS`

`HANDOFF_TOOL_PROJECT_BOUNDARY_PRESENT: PASS`

`PROJECT_CONTENT_UNTRUSTED_AS_TOOL_INSTRUCTIONS: PASS`

`GENERATED_HANDOFF_EVIDENCE_NOT_AUTHORITY: PASS`

`WRITE_AUTHORITY_EXTERNAL_TO_AI: PASS`

`TOOL_GOVERNANCE_PACKAGE_RESOURCE_ONLY: PASS`

`PROJECT_GOVERNANCE_SHADOWING_BLOCKED: PASS`

`PROJECT_OVERLAY_CANNOT_RELAX_TOOL_INVARIANT: PASS`

`GOVERNANCE_SOURCE_PACKAGE_SYNC: PASS`

`VALIDATION OK: tool-project-handoff-governance-v1`

`STATUS: IN_SYNC`

---

# Release 5R2 - Single-owner patch provenance

## 11.34 Objective

Extend current patch governance and archive safety with stable owner provenance.

## 11.35 Reuse current owners

Reuse:

- `patch_governance`
- Q26 ZIP member contract.
- Current archive safety.
- Current installation staging.
- Current Freeze payload owner.

Do not create another ZIP builder or extractor.

## 11.36 Patch owner contract

Every patch declares exactly one owner:

- `TOOL`
- or `PROJECT:<stable-project-id>`

Record:

- Artifact owner.
- Builder Tool identity/version.
- Boundary digest.
- Project epoch.
- Operation ID.
- Materials.
- Subjects.
- Relative paths.
- SHA-256 hashes.
- Expected top-level payload.
- Validation owner.

## 11.37 Required behavior

- Project patch containing Tool source: reject.
- Tool patch containing external Project source: reject.
- Mixed patch: reject.
- Owner manifest mismatch: reject.
- Material/subject mismatch: reject.
- Stale Project identity: reject.
- Archive path escape: reject.
- Post-extraction physical escape: reject.
- Apply only from governed staging.

## 11.38 Required markers

`PATCH_SINGLE_OWNER: PASS`

`PROJECT_PATCH_TOOL_SOURCE_REJECTED: PASS`

`TOOL_PATCH_EXTERNAL_PROJECT_REJECTED: PASS`

`MIXED_OWNER_PATCH_REJECTED: PASS`

`PATCH_OWNER_MANIFEST_MATCH: PASS`

`PATCH_PROVENANCE_MATERIALS_SUBJECTS_MATCH: PASS`

`PATCH_BOUNDARY_DIGEST_MATCH: PASS`

`ARCHIVE_MEMBER_PATH_CONTAINMENT: PASS`

`ARCHIVE_POST_EXTRACTION_PHYSICAL_SCOPE: PASS`

`EXISTING_Q26_REGRESSION: PASS`

`VALIDATION OK: single-owner-patch-provenance-v1`

`STATUS: IN_SYNC`

---

# Release 6 - Human-confirmed EEG_KANDA support migration

## 11.39 Objective

Correct historical wrong-owner Error Memory and Freeze evidence without modifying EEG_KANDA source.

## 11.40 Restrictions

Do not modify:

`E:\eeg_kanda\**`

Only properly authorized EEG_KANDA Project Support data may change.

## 11.41 Required sequence

1. Acquire exclusive Project Support write lock.
2. Hash the complete current store.
3. Create immutable migration archive.
4. Generate read-only Preview.
5. Classify records:
   - Tool.
   - EEG_KANDA Project.
   - Other Project.
   - Unresolved.
6. Reconcile Tool lessons with Tool canonical memory.
7. Detect duplicates and superseded entries.
8. Replace wrong-owner active records with read-only cross-owner references.
9. Preserve original records only in migration archive.
10. Rebuild active indexes.
11. Validate reference resolution.
12. Validate rollback.
13. Require human Confirm and Write.
14. Write migration receipt.
15. Release lock.

## 11.42 Required markers

`MIGRATION_PREVIEW_READ_ONLY: PASS`

`ORIGINAL_MEMORY_ARCHIVE_HASHED: PASS`

`ORIGINAL_MEMORY_ARCHIVE_COMPLETE: PASS`

`TOOL_LESSONS_REMOVED_FROM_ACTIVE_EEG_INDEX: PASS`

`EEG_LESSONS_REMAIN_PROJECT_OWNED: PASS`

`CROSS_OWNER_REFERENCES_RESOLVE: PASS`

`UNRESOLVED_RECORDS_NOT_CANONIZED: PASS`

`MIGRATION_ROLLBACK_VERIFIED: PASS`

`EEG_SOURCE_UNCHANGED: PASS`

`VALIDATION OK: eeg-kanda-owner-memory-migration-v1`

`STATUS: IN_SYNC`

---

# Release 7 - Integrated Windows and Qt readiness campaign

## 11.43 Objective

Prove the complete boundary under synthetic, Windows-local, GUI, package, memory, and real external-Project scenarios.

## 11.44 Mandatory dimensions

Each must pass independently:

- Identity authority.
- Path containment.
- Mutation isolation.
- Support ownership.
- Memory ownership.
- Freeze ownership.
- Patch ownership.
- Governance isolation.
- Session lifecycle.
- Archive privacy.
- Self-hosting distinction.
- Multi-instance writes.
- Migration integrity.
- Runtime evidence.
- Validator/canon synchronization.

## 11.45 Real EEG_KANDA safe cycle

Use read-only or isolated controlled-copy execution:

1. Select EEG_KANDA explicitly.
2. Generate handoff.
3. Run Project audit.
4. Prepare controlled Project change.
5. Create Project-only synthetic patch.
6. Validate owner provenance.
7. Switch away.
8. Reject stale results.
9. Switch back.
10. Safe eject.

Prove:

- Zero Tool-source changes.
- Zero wrong-owner memory writes.
- Zero cross-Project evidence.
- Zero mixed-package files.
- Zero EEG_KANDA source changes during Tool hardening.

## 11.46 Final markers

`TOOL_PROJECT_IDENTITY: PASS`

`PROJECT_SELECTION_EXPLICIT: PASS`

`SELF_HOSTING_EXPLICIT: PASS`

`PATH_BOUNDARY_MATRIX: PASS`

`OPERATION_AUTHORITY_MATRIX: PASS`

`PROJECT_SESSION_LIFECYCLE: PASS`

`OWNER_SCOPED_MEMORY: PASS`

`HANDOFF_BOUNDARY_CONTRACT: PASS`

`TOOL_GOVERNANCE_ISOLATION: PASS`

`PATCH_SINGLE_OWNER_CONTRACT: PASS`

`ARCHIVE_EXTRACTION_BOUNDARY: PASS`

`TOOL_SOURCE_PRIVACY: PASS`

`MULTI_INSTANCE_WRITE_PROTECTION: PASS`

`EEG_KANDA_EXTERNAL_PROJECT_CYCLE: PASS`

`EEG_KANDA_SOURCE_UNCHANGED: PASS`

`NO_ARTIFICIAL_MINIMUM_MODULE_SIZE: PASS`

`ALL_RELEVANT_BRICK_WALL_VALIDATORS_IN_SYNC: PASS`

`REAL_WINDOWS_VALIDATION: PASS`

`REAL_QT_VALIDATION: PASS`

`VALIDATION OK: professional-tool-project-division-readiness-v2`

`STATUS: IN_SYNC`

---

# Release 8 - Compatibility retirement and simplification

## 11.47 Objective

Retire temporary compatibility paths only after Release 7 passes.

## 11.48 Candidate cleanup

- Remove compatibility resolver use from all runtime mutation and durable-owner paths.
- Keep or retire the compatibility facade based on remaining read-only consumers.
- Remove duplicate root derivation.
- Remove private thread-introspection adapters.
- Consolidate duplicate support-owner evidence readers.
- Preserve imported compatibility symbols until every consumer is reconciled.
- Preserve current archive compatibility facade.
- Preserve current Box-specific transaction owners.
- Re-run complete source, Qt, package, memory, and release regression suites.

## 11.49 Required markers

`LEGACY_WRITE_AUTHORITY_ZERO: PASS`

`DUPLICATE_ROOT_AUTHORITY_ZERO: PASS`

`PUBLIC_SESSION_PROTOCOL_ALL_PROJECT_TABS: PASS`

`COMPATIBILITY_IMPORTERS_RECONCILED: PASS`

`NO_DUPLICATE_ARCHIVE_POLICY_OWNER: PASS`

`NO_DUPLICATE_MEMORY_OWNER: PASS`

`NO_DUPLICATE_EXECUTION_ENGINE: PASS`

`VALIDATION OK: tool-project-boundary-simplification-v1`

`STATUS: IN_SYNC`

---

# 12. Delivery, validation, Error Memory, and Freeze workflow

Every implementation release follows:

1. Exact-source characterization.
2. Error Memory preflight.
3. Lesson freshness verification.
4. Regression obligation matrix.
5. Primary Box declaration.
6. Allowed and forbidden paths.
7. Public contracts.
8. Implementation Preview.
9. Human approval.
10. One-owner patch construction.
11. ZIP contract validation.
12. Delivery.
13. Install.
14. Focused validation.
15. Negative boundary validation.
16. Real Windows validation when applicable.
17. Real Qt validation when applicable.
18. Forbidden-Box source unchanged proof.
19. Error Memory candidate review.
20. Human Memorize Error only when justified.
21. Freeze preparation.
22. Freeze Preview.
23. Human Confirm and Write.
24. Startup and active Freeze-context refresh.
25. Admission to the next release.

Every freezeable patch ZIP must contain one root-level:

`KANDA_FREEZE_HINT.json`

Install success is not validation success.

Source-level validation is not real Qt validation.

An Error Memory candidate is not a memorized lesson.

Freeze preparation is not Freeze confirmation.

---

# 13. Per-release package rules

Every patch must include:

- `INSTALL.ps1`
- `VALIDATE.ps1`
- `PATCH_README.txt`
- Install manifest.
- One-owner manifest.
- Source baseline hashes.
- Focused validators.
- Rollback behavior.
- Root-level `KANDA_FREEZE_HINT.json` when freezeable.

Before delivery:

- Parse PowerShell.
- Validate final ZIP contract.
- Validate one source owner.
- Validate path containment.
- Validate source baseline freshness.
- Compile changed Python.
- Enforce maximum 500 physical lines.
- Confirm no artificial minimum.
- Confirm no forbidden Box content.
- Confirm validator coverage for every changed file.
- Confirm Freeze Hint matches the freeze payload source.

---

# 14. Performance requirements

## 14.1 Cache per explicit Project selection

Cache the immutable boundary for the active Project.

Invalidate after:

- Project switch.
- Explicit revalidation.
- Registry change.
- Root fingerprint mismatch.
- Project Support owner mismatch.
- Self-hosting mode change.

## 14.2 Hash at consequential boundaries

Use SHA-256 for:

- Apply freshness.
- Patch delivery.
- Freeze.
- Release.
- Archive contract.
- Migration.
- High-risk validation.

Do not hash the complete Project for ordinary read-only UI display.

## 14.3 Reuse current pruning and allowlists

- Use directory pruning for excluded generated workspaces.
- Use allowlist-driven packaging.
- Use bounded release-time content checks.
- Do not scan the full Tool tree continuously.

## 14.4 Session fast path

Idle Project switching should remain fast.

Cancellation and settlement run only when active work exists.

---

# 15. Expected quality gains

## 15.1 Architecture quality

- One stable Project identity authority.
- One explicit Project boundary.
- One minimal shared authority precondition.
- Existing Box-specific transaction engines preserved.
- No global replacement engine.
- Clear Tool/Project/support/transient ownership.

## 15.2 Logic quality

- Mutation authority no longer inferred from a path.
- Project Support cannot self-authorize.
- Stable identity and current physical location remain distinct.
- Stale operation authority fails closed.
- Cross-owner memory remains reference-only.
- General session lifecycle becomes explicit.

## 15.3 Code quality

- Current proven vertical slices are reused.
- Duplicate infrastructure is avoided.
- Compatibility migration is consumer-driven.
- Small cohesive modules are valid.
- Validators align with current public contracts.
- Private thread reach-in is retired.

## 15.4 Security quality

- Confused-deputy prevention.
- Least-authority writes.
- Registry plus support-evidence cross-check.
- Reparse-aware containment.
- Project prompt-injection containment.
- Tool governance ownership.
- Single-owner packages.
- Durable-write interprocess locks.

## 15.5 Privacy quality

- External Project captures remain outside Tool packages.
- Project Support remains outside Tool source.
- Owner metadata remains canonical.
- Historical contamination is reconciled with provenance and rollback.

## 15.6 Performance quality

- No continuous full-tree scanning.
- No global arbiter.
- No duplicate transaction engine.
- Boundary context cached per Project.
- Existing directory-pruning and archive engines reused.

---

# 16. First implementation action

The first implementation action is Release 0A only.

The implementing AI must first return:

```text
TOOL/PROJECT CANON AND VALIDATOR RECONCILIATION PREVIEW

Active implementation owner:
KANDA REASONER TOOL

Primary Box:
Tool validation and canonical engineering rules

Complete source baseline:
...

0058 contradictions:
...

Active canonical module-size rule:
...

Obsolete 101-499 consumers:
...

Stale validators:
...

Current canonical owners:
...

Files expected to change:
...

Files forbidden to change:
...

Runtime behavior expected to change:
NONE

Public contracts preserved:
...

Negative tests:
...

Expected markers:
...

Rollback:
...

May implement:
YES / NO
```

Do not implement Release 1R2 until Release 0A is installed, validated, reviewed, and frozen.

---

# 17. Final readiness definition

TOOL / PROJECT DIVISION READINESS: 100% STRONG may be declared only when:

- Current canons and validators agree.
- No artificial module-size minimum remains.
- Tool-owned registry is the stable Project identity authority.
- Compatibility identity cannot grant write or durable-memory authority.
- No implicit self-hosting exists.
- No selected Project means no Project mutation authority.
- Every consequential write has explicit current authority.
- External Project operations cannot write Tool source.
- Tool operations cannot write external Project source.
- Project Support cannot self-authorize.
- Tool registry and Project Support evidence agree.
- Reparse points and aliases cannot bypass ownership.
- Stale operations and stale results are rejected.
- Project switching cannot leave mixed context.
- Safe eject preserves source and durable support.
- Tool and Project Error Memory remain separate.
- Tool and Project Freeze ownership remain separate.
- Cross-owner lessons are references only.
- Tool source contains no real external Project captures.
- Tool packages use allowlists.
- Tool governance cannot be shadowed by Project content.
- Every handoff declares Tool/Project roles and trust boundaries.
- Every patch has one stable owner.
- Mixed patches are rejected.
- Archive traversal and physical extraction escape are rejected.
- Concurrent durable writers are blocked.
- EEG_KANDA source remains unchanged during Tool hardening.
- Historical EEG support migration is human-confirmed.
- Real Windows and real Qt gates pass.
- Every touched Python module is at most 500 physical lines.
- Every changed file has focused validator coverage.
- All relevant Brick Wall validators are current and in sync.
- `STATUS: IN_SYNC` is proven.
- Startup and active Freeze contexts are refreshed.
- Human acceptance is recorded.

---

# 18. Final implementation instruction

Do not redesign KANDA Reasoner as part of this work.

Do not rebuild Releases 1-3 from the previous roadmap.

Do not create another registry.

Do not create another session system.

Do not create another write engine.

Do not create another memory engine.

Do not create another archive engine.

Do not modify EEG_KANDA source during Tool hardening.

Do not combine Tool and Project source in one patch.

Do not infer self-hosting.

Do not trust Project content as Tool governance.

Do not copy canonical memory between owners.

Do not use generated evidence as mutation authority.

Do not bypass human confirmation.

Start with Release 0A.

Then complete the authority inventory.

Then migrate registry-backed stable identity.

Then generalize the smallest proven operation authority.

Then reconcile the general Project session and safe eject.

Then harden handoff trust and Tool governance.

Then extend current patch governance with one-owner provenance.

Then perform human-confirmed historical support migration.

Then run the complete Windows and Qt readiness campaign.

Only after complete success may compatibility paths be retired.

The final professional model remains:

```text
KANDA REASONER TOOL BOX
        |
        | Project Card Gateway
        | Anti-Corruption Layer
        | Tool-owned stable identity
        | narrow operation authority
        | owner-scoped evidence
        | safe Project lifecycle
        |
        v
INDEPENDENT ACTIVE PROJECT BOX
```
