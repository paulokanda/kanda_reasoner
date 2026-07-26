# Large File Refactor Workbench Tutorial

## Button behavior

Preparation and validation actions remain clickable. If a prerequisite is missing,
the action fails closed and its output explains the exact blocker. Disabled buttons
are reserved for true mutation or recovery authorization gates, including
Refactor Large Module and journaled rollback. Legacy direct-apply token, apply,
and rollback controls are intentionally absent from the sequential Workbench GUI.

## Purpose

The Large File Refactor Workbench executes one explicitly selected Large File Refactor Planner architecture with maximum source-integrity, behavior, and recovery evidence. The Planner owns architecture. The Workbench owns execution feasibility and deterministic realization. The journaled transaction executor owns physical mutation and recovery.

## Human and AI roles

The human sets direction, selects or approves the Planner version, reviews semantic and text diffs, acknowledges warnings, confirms the transaction summary, tests delivered behavior, and approves freeze decisions. The human does not write or manually copy source code.

The AI audits current source, proposes before implementation, performs deterministic transformation, prepares governed patch delivery, validates, reports blockers, and stages freeze/error-memory evidence through the governed receivers. The AI must not silently redesign a selected Planner architecture during Workbench execution.

## Module-size law

Every resulting Python source module, including helpers and facades, must satisfy:

```text
100 < physical_lines < 500
```

Therefore 101–499 physical lines are valid. A result at 100 or 500 lines is blocked. There are no facade, constants, adapter, or structural-role exceptions in this Workbench workflow. Do not add padding. When a cohesive architecture cannot satisfy the rule, return `PLAN_CORRECTION_REQUIRED` with structured Compliance Veto evidence to the Planner.

## Page Code snapshot

`Get Page Code` is a read-only top-level button placed outside and above the numbered Workbench stage containers. It opens one text window that aggregates every current Workbench text output, grouped by stages 1 through 7. Each stage includes an `Origin:` explanation describing the owning handoff, validator, analyzer service, evidence builder, or authorization source. The snapshot does not execute a stage, change a gate, write source, or mutate Project Support evidence.

## Exact visible tab sequence

The user-facing tab sequence is:

```text
1. Plan Intake from Large File Refactor Planner
   -> Load Latest Planner Plan
   -> optional Recheck Source Hash

2. Dependency and Scope Readiness
   -> Analyze Dependency Readiness

3. Real Moved-Code Preview Generation
   -> Generate Real Preview

4. Structural Validation
   -> Validate Real Preview

5. Advanced Quality Review
   -> Run Advanced Quality Review
   -> Visible nine-stage progress and Cancel

6. Preflight Backup and Source Payload
   -> Prepare Preflight Backup Readiness
   -> Build Source Apply Payload

7. Completion Review and Refactor Authorization
   -> Prepare Completion Evidence
      (Execution Basis, Feasibility, Baseline, Contract, Recipe, Seal,
       Shadow Apply, Provenance, Structural/API/Topology/Runtime/Behavior evidence)
   -> review Semantic Diff first
   -> review Text Diff second
   -> optional assisted review: Heuristic, Local AI, Web AI, or Receive From Web AI
      (review evidence only; never source mutation or automatic human confirmation)
   -> acknowledge listed warnings
   -> Prepare Transaction Summary
   -> confirm the exact transaction summary
   -> Refactor Large Module
   -> post-apply validation and RefactorReceipt
   -> rollback/recovery only when the durable transaction state allows it
```

`Generate Real Preview` does not itself run Structural Validation. When Preview succeeds with status `real_preview_written`, the `Validate Real Preview` button becomes available. If Preview is blocked, Structural Validation stays disabled and the Structural Validation panel must show the Preview status and blockers instead of silently appearing stuck.

The deprecated legacy optional behavior-validation GUI has been removed. Behavior evidence for the current workflow is produced through the governed Shadow and journaled transaction validation chain, not through a parallel legacy command field or button.

## Internal execution flow behind the visible steps

```text
PlannerSnapshot
RefactorBaseline
Execution Basis Set
Execution Feasibility
    -> EXECUTABLE
    or PLAN_CORRECTION_REQUIRED
WorkbenchExecutionContract
TransformationRecipe
LibCST deterministic transformation
Exact artifact set
Sealed payload
Preflight
Shadow backend selection
Shadow Apply of the exact sealed payload
Shadow provenance proof
Structural/API/topology/runtime/behavior validation
Semantic Diff review
Text Diff review
Warning acknowledgment
Transaction summary confirmation
Final source-basis recheck
Refactor Large Module
Journaled exact-byte apply
Post-apply validation
RefactorReceipt
Completion or rollback/recovery
```

## Why the button is last

`Refactor Large Module` is not a planning action. It must not call AI, regenerate a plan, rename responsibilities, merge modules, split modules, run a formatter, or produce different bytes from Preview/Shadow. The button may proceed only after the same sealed payload was reviewed and validated, the canonical Patch 5 executor proof is available, the human confirmed the transaction summary, and the final execution basis still matches.

The Stage 7 executor-proof text window reports live read-only status instead of a historical placeholder. It shows `AVAILABLE`, `UNAVAILABLE`, or `NOT_CHECKED`, includes the matched canonical frozen entry when proof is available, and lists blockers when proof is unavailable. This status satisfies only the executor-proof prerequisite; it never force-enables the final button or replaces immutable evidence, human review, warning acknowledgment, transaction-summary confirmation, freshness, or transaction safety gates.

## Review order

Review Semantic Diff first. It summarizes symbol movements, responsibility modules, actual size map, import changes, public API before/after, topology before/after, consumer rewrites, and dynamic/runtime warnings. Review raw Text Diff second for exact line changes.

The Assisted Diff Review row provides four optional review routes:

```text
Heuristic
Local AI
Web AI
Receive From Web AI
```

Heuristic performs a deterministic evidence review. Local AI reviews the same bounded evidence asynchronously and discards stale results when the current evidence identity changes. Web AI copies a bounded, contextualized review package. Receive From Web AI accepts exactly one marker-wrapped structured response, validates its schema, and appends the semantic and text review sections to their matching panels.

The `Use Version` choice remembers the last stable selection (`Heuristic`, `Local AI`, or `Imported Web AI Version`) through the application settings store and restores it when the Planner is opened again. Missing or invalid saved values fall back safely to `Local AI`.

Assisted review is advisory evidence only. It must not mutate source, replace Preview or transaction evidence, set human-review checkboxes, acknowledge warnings, confirm a transaction summary, or enable a mutation gate. Human review remains explicit.

Warnings that require human judgment must be acknowledged explicitly. Widget state is projection only; durable transaction state is the source of truth.

## Preview static quality gate

Before Semantic Diff or Text Diff reaches human review, Structural Validation must reject transform artifacts that compile but are still structurally wrong or noisy. The deterministic in-process gate currently blocks:

```text
duplicate __all__ assignments
pointless top-level string expressions after the real module docstring
multiple top-level imports from the same relative helper module
duplicate # project-path headers
```

The facade renderer must preserve the original module docstring as the first executable statement, preserve a single public API declaration, and group re-export imports by helper module. Compile success alone is not sufficient.

Optional deeper external checks may complement, but never replace, the deterministic gate when the tools are available in the validation environment:

```text
Ruff: F811, F401, B018, I001
Griffe: public API snapshot/breaking-change comparison
Grimp: import graph and cycle policy checks
Vulture: dead-code candidates
Pyright or mypy: type-level regression checks
```

These optional tools must not mutate Preview automatically. Any formatter or autofix output must be regenerated through a governed Preview path and revalidated before human review.

## Shadow validation

Use either `ControlledMirrorBackend` or `GitWorktreeBackend` when eligible. Backend identity alone is not proof. Runtime provenance must record the Python executable, cwd, `sys.path`, `PYTHONPATH`, package installation mode, `module.__file__`, `module.__spec__.origin`, and pytest collection root. Wrong-origin imports fail validation.

Behavior validation distinguishes baseline pass/shadow pass, baseline pass/shadow fail, no tests collected, and insufficient evidence. No tests is never equivalent to behavior preservation.

## Serial project mutation lane

Each source-mutating tab remains independently boxed behind a data-only Mutation Port. Real mutations for one physical project use one serial project lane. Only one request may own that lane. `RECOVERY_PENDING` keeps it closed to later queued writers. Planning, analysis, Preview, and eligible Shadow work may run independently; live source mutation is serial.

## Journaled apply protocol

For every physical operation:

```text
PENDING
-> INTENT_RECORDED
-> physical exact-byte operation
-> APPLIED
-> result hash verification
-> VERIFIED
```

SQLite stores durable transaction evidence but does not make filesystem writes part of one atomic SQLite transaction. After crash or restart, reconcile durable state with actual filesystem hashes before resume or rollback.

## Rollback rules

Rollback is available from rollback-eligible applied/recovery states. Verify current hashes before restoration. Restore modified/deleted files from verified backups and remove transaction-created files. If external drift is detected, enter `ROLLBACK_CONFLICT`; never overwrite unrelated edits or attempt an automatic Python three-way merge.

A terminal completed transaction releases its serial lane. The controlled Patch 6 proof demonstrates rollback before terminal finalization, then creates a fresh transaction for the final second successful application.

## Controlled real-module proof

The final proof uses the approved plan for:

```text
kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py
```

Baseline: 786 physical lines and SHA-256 `6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55`.

Approved planned sizes:

```text
public facade:      197
path resolution:    145
helper selection:   429
```

The controlled proof runs on a full disposable project copy. It proves baseline characterization, decorator preservation, cycle-safe function-local imports for facade-owned globals, structural validation, Shadow provenance and behavior, first journaled apply, post-apply behavior pass, exact rollback restoration, fresh second transaction, `COMPLETED_VALIDATED`, RefactorReceipt integrity, final 101–499 module sizes, and unchanged live-project source hash.

## Transformation correctness rules discovered by the controlled proof

LibCST extraction must preserve decorators as part of the symbol source span. Structural comparison may normalize docstring whitespace only and may ignore only exact function-local facade imports recorded in the transformation evidence. Moved functions that depend on facade-owned globals use explicit function-local relative imports, preventing import-time facade/helper cycles without duplicating constants or changing Planner ownership.

## Freeze and Error Memory boundaries

The Workbench and transaction executor never write canonical frozen memory directly. Validation writes UTF-8 evidence with exact machine-recognizable markers, then uses the canonical freeze evidence merge helper. Freeze remains `Preview -> Confirm and Write` after explicit human confirmation.

Correction lessons are staged under the project Error Memory pending AI-assisted intake receiver for human review. Do not write canonical Lessons directly.

## Completion states

Use explicit states such as:

```text
COMPLETED_VALIDATED
COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED
APPLIED_VALIDATION_FAILED
RECOVERY_PENDING
ROLLBACK_CONFLICT
ROLLBACK_VERIFIED
ROLLBACK_FAILED
```

Do not present behavior-not-run as equivalent to validated completion.

## Advanced Quality Review correction recovery

If Advanced Quality Review reaches a terminal non-authorizing result such as `BLOCKED`, `INDETERMINATE`, `FAILED`, `TIMED_OUT`, or a review-required decision, Stage 5 exposes the governed Correction Routes. The correction context includes analyzer stage statuses, execution status, quality decision, typed rule results, diagnostics, and the current AQR text output.

Heuristic, Local AI, and Web AI correction routes may propose a new Planner generation, but none of them opens Preflight directly. Any accepted correction invalidates downstream AQR evidence and requires a fresh deterministic sequence: Dependency Readiness -> Real Preview -> Structural Validation -> Advanced Quality Review.

The Stage 5 `Local AI Correction` route uses one Qt-native QThread/Signal worker and a bounded single-track staged correction. The recovery lane does not run the three-candidate Planner tournament. It exposes progress phases, provides `Cancel Local AI Wait`, times out the accepted result after 120 seconds, rejects late results, and leaves Heuristic/Web AI alternatives available after timeout or cancellation. A canceled or timed-out underlying model request may finish later, but its result is stale and cannot replace Workbench ownership or open a gate.

While Local AI Correction is active, the Workbench shows the reusable green sonar monitor. The sonar text follows real worker phases, including source analysis, responsibility analysis, bounded repair attempts, corrected-plan validation, and candidate readiness. The sonar is started, updated, and settled by the same Qt-native correction lifecycle, so success, error, timeout, or cancellation cannot leave an orphaned activity animation.

After a materially changed Local AI correction candidate reloads Workbench ownership, control projection is recomputed immediately and once again on the next Qt event-loop turn. The accepted reload returns the sequential workflow to Dependency and Scope Readiness, so Analyze Dependency Readiness becomes the next available action while Preview, Structural Validation, AQR, Preflight, payload, and completion stages remain closed until rerun evidence is rebuilt. The unresolved AQR correction session remains available across candidate generations so Heuristic, Local AI, and Web AI alternatives can be tried repeatedly until a fresh AQR PASS or PASS_WITH_WARNINGS retires the blocker. A zero-change candidate never retires the blocker or replaces Workbench ownership.
Correction buttons do not remain as workflow authority: they remain optional recovery alternatives for the unresolved AQR session, while sequential next-action and Preflight authority continue to derive only from the canonical progression model and fresh AQR evidence.

While AQR is still running, correction routes remain closed. The preflight text must show the actual AQR gate state instead of stale structural-only availability.



## Correction route reuse and AQR sonar

When a Workbench stage has terminal correctable evidence, the Heuristic, Local AI,
and Web AI correction routes remain reusable alternatives for that blocker. A failed,
cancelled, or timed-out attempt does not consume another route. Switching from one
worker route to the other abandons the previous accepted-result authority and late
results are discarded. Copy Web AI Correction Package remains read-only and usable
while a worker route is active. Receive Web AI Correction abandons active worker
results before the imported candidate enters the public Planner-to-Workbench handoff.

Correction routes remain closed for PASS stages and stages not yet reached. During an unresolved AQR correction session, the routes remain available across materially changed candidate generations and deterministic reruns; they are temporarily closed only while the fresh AQR worker itself is actively running. A terminal AQR FAILED, BLOCKED, INDETERMINATE, TIMED_OUT,
CONFIGURATION_ERROR, REVIEW_REQUIRED, or ADVISORY_REVIEW_REQUIRED result exposes the
Stage 5 correction routes with exact blocker context. Technical AQR failure remains
correctable even when no outcome object exists, because terminal status and diagnostic
evidence are authoritative.

The Advanced Quality Review uses the reusable green sonar monitor as presentation-only
feedback. The sonar starts only after the Qt review controller accepts the run, updates
from real worker progress stages, and settles on authorizing success, blocked outcome,
failure, or cancellation. The sonar never controls gates or stores evidence.
