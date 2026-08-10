# KANDA Error-Reduction Roadmap

## Reconcile First, Repair Second, Shield Third, Then Extract the Smallest Proven Reusable Contract

# 1. Governing implementation rule

Every roadmap step must follow this order:

```text
RECONCILE
    ↓
REUSE existing canonical owner where possible
    ↓
REPAIR the proven defect
    ↓
VALIDATE the repair
    ↓
SHIELD the repaired Box
    ↓
FREEZE the accepted behavior
    ↓
EXTRACT only the smallest proven reusable contract
    ↓
ADOPT gradually in other Boxes
```

The roadmap must not create:

* Another Project registry.
* Another Tool-versus-Project authority.
* Another universal MCard system.
* Another ZIP engine.
* Another transactional write engine.
* Another Freeze engine.
* Another Error Memory engine.
* Another global execution framework.
* Another broad safety prompt duplicating the existing canons.

Every new capability must be placed inside an existing canonical owner or exposed through a narrow public contract owned by the correct Box.

---

# 2. Delivery and download rules

Each source-changing delivery must contain:

1. One self-contained feature or update ZIP.
2. One owner-pure declared write set.
3. One explicit active Box.
4. Exact-source preconditions.
5. Brick Wall authorization.
6. Tool-versus-Project classification.
7. Anti-leak validation.
8. MCard linkage where the existing MCard lifecycle applies.
9. Transactional rollback.
10. Four separate PowerShell phases:

    * INSTALL
    * VALIDATE
    * FREEZE
    * ERROR MEMORY

No phase may execute a later phase.

A package may be eliminated from the roadmap when reconciliation proves that the required capability already exists and only needs to be reused.

---

# 3. Approximate number of downloads

## Recommended estimate

```text
Mandatory governed ZIP downloads: approximately 10
Likely range after reconciliation: 8–12
Optional adoption downloads: 1–3
Likely complete program total: approximately 10–13
```

## Why the number is approximate

The Reconciliation phase may reveal that:

* Some capabilities already exist and only need adapters.
* Two apparently separate changes belong to the same canonical owner and may safely share one ZIP.
* One proposed delivery touches two different canonical owners and must be divided into separate owner-pure ZIPs.
* A feature requires no source modification and therefore no download.

The goal is not to minimize ZIP count at any cost.

The goal is:

> The smallest number of downloads that preserves canonical ownership, rollback independence, exact validation, and Brick Wall clarity.

---

# 4. Phase 0 — Canonical reconciliation

## Download count

```text
0 mandatory source ZIP downloads
```

A written reconciliation report may be produced, but it is not a source patch.

## Objective

Determine what already exists, where it is owned, and what is genuinely missing.

## Step 0.1 — Load the current canons

Inspect the exact current versions of:

1. Brick Wall.
2. Box Architecture.
3. Tool-versus-Project canon.
4. NO_LEAK_LOGIC_V1.
5. MCard canon.
6. Governed implementation bridge.
7. Patch delivery protocol.
8. Installation protocol.
9. Validation protocol.
10. Freeze protocol.
11. Error Memory protocol.
12. Module-size and architecture rules.

## Step 0.2 — Inspect the exact Wave 2U source

Inspect:

* Patch Preview public facade.
* Preview service.
* Source reader.
* Diff generator.
* Rollback ZIP builder.
* Preview manifest.
* Preview ID generation.
* Workspace creation.
* Workspace cleanup.
* Tests and fixtures.
* Package validator.
* GUI integration.

## Step 0.3 — Identify current canonical owners

Create an owner table:

| Responsibility             | Current canonical owner  | Public contract             | Status                  |
| -------------------------- | ------------------------ | --------------------------- | ----------------------- |
| Project selection          | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Project stable ID          | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Operation identity         | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Source hashing             | Existing owner           | Existing public API         | REUSE / EXTEND          |
| ZIP safety                 | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Package validation         | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Transactional installation | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Rollback                   | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Validation evidence        | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Freeze evidence            | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Error Memory               | Existing owner           | Existing public API         | REUSE / EXTEND          |
| Test workspace isolation   | Existing owner or absent | Existing public API or none | REUSE / EXTEND / CREATE |

## Step 0.4 — Classify every proposed roadmap capability

Every capability receives one classification:

```text
REUSE
EXTEND EXISTING OWNER
REPAIR EXISTING OWNER
MISSING — CREATE UNDER NAMED OWNER
FORBIDDEN DUPLICATE
```

## Step 0.5 — Produce the authoritative download map

For each future ZIP, define:

* Feature ID.
* Canonical owner.
* Active Box.
* Allowed write set.
* Forbidden paths.
* Public contracts used.
* External Boxes touched.
* Required validation.
* Rollback boundary.
* Freeze eligibility.
* Error Memory eligibility.

## Brick Wall exit gate

Implementation remains blocked until:

```text
CANONICAL OWNER MAP: PASS
DUPLICATE OWNER CHECK: PASS
TOOL VERSUS PROJECT CLASSIFICATION: PASS
BOX WRITE SETS: PASS
ANTI-LEAK ROUTES: PASS
CURRENT SOURCE HASHES: PASS
```

---

# 5. Download 1 — Wave 2U surgical repair

## Canonical purpose

Repair only the two proven Wave 2U failure families:

1. BOM/text-decoding contract failure.
2. Preview identity or test-isolation collision.

## Active Box

Engineering Diagnostics Patch Preview Box.

## Allowed changes

* Exact source-reading path.
* Diff rendering path.
* Rollback-byte handling.
* Preview identity logic if proven defective.
* Test-fixture isolation.
* Cleanup.
* Focused validator expectations.

## Forbidden changes

* Other Engineering Diagnostics Boxes.
* Global Project registry.
* Freeze engine.
* Error Memory engine.
* Transactional installer.
* Unrelated GUI architecture.
* New generic governance framework.

## Step 1.1 — Prove the BOM root cause

Trace:

```text
source bytes
→ encoding detection
→ Unicode decode
→ diff generation
→ diff serialization
→ rollback packaging
```

Classify every boundary as:

```text
BYTES
UNICODE TEXT
SERIALIZED UTF-8
```

## Step 1.2 — Repair BOM handling

Requirements:

* Source authority begins with raw bytes.
* Original raw hash is preserved.
* Python encoding detection is explicit.
* Host-default text encoding is forbidden.
* The diff contains `U+FEFF`, not mojibake.
* Rollback restores the exact original bytes.
* Unrelated newline changes are forbidden.

## Step 1.3 — Prove the collision root cause

Inspect:

* Current Preview ID inputs.
* Storage directory selection.
* Test source roots.
* Test Project Support roots.
* Test daily-work roots.
* Cleanup registration.
* Repeated identical Preview behavior.

Do not assume that the collision is solely an identity defect before exact-source confirmation.

## Step 1.4 — Repair only the proven cause

Possible repairs:

* Unique test roots.
* Guaranteed cleanup.
* New attempt identity.
* Correct idempotent reuse.
* Integrity failure for mismatched content under the same identity.

## Step 1.5 — Preserve all 11 previously passing contracts

The corrected package must rerun the complete 14-test suite.

## Required validation

```text
BOM EXACT DIFF: PASS
BOM ROLLBACK BYTE IDENTITY: PASS
PREVIEW ATTEMPT ISOLATION: PASS
PREVIEW CONTENT INTEGRITY: PASS
NO WORKSPACE LEAK: PASS
ALL 14 TESTS: PASS
EXACT FINAL ZIP VALIDATION: PASS
```

## Freeze

Freeze only after installation and installed validation.

## Error Memory

Create draft candidates only after root cause is proven.

Likely candidates:

* Byte-decoding contract.
* Preview identity/test-isolation contract.

Do not activate them until the corrected feature is installed and validated.

---

# 6. Download 2 — Patch Preview Box Shield

## Objective

Protect the repaired Box before extracting reusable logic.

## Why Shield comes before extraction

Without a Shield, refactoring the corrected implementation into a reusable contract could reintroduce the same defects.

The Shield freezes the Box’s externally observable invariants.

## Active Box

Patch Preview Box.

## Shield invariants

### Source-byte invariants

* Original raw bytes remain authoritative.
* Original hash remains stable.
* BOM classification remains stable.
* Candidate bytes are explicit.
* Rollback is byte-exact.

### Preview invariants

* Preview is non-installable.
* Preview cannot directly mutate Project source.
* Frozen paths remain blocked.
* Approval tokens remain issue-bound.
* Active source changes invalidate Preview.
* Repeated attempts cannot collide improperly.

### Box invariants

* No SQLite owner introduced.
* No private cross-Box imports.
* No Project-specific state stored in Tool source.
* No Tool implementation stored in Project Support.
* No daily-work artifact promoted to source truth.

### GUI invariants

* Patch Preview remains a separate control.
* It requires the correct lifecycle state.
* Stale attempts cannot update the current GUI.
* Cancellation settles before restart.

## Required validation

* Focused Box tests.
* Public facade import.
* Known consumer imports.
* GUI lifecycle test.
* Anti-leak scan.
* Architecture scan.
* Module-size scan.

## Freeze

Freeze the repaired and shielded Patch Preview Box before generalizing its internals.

---

# 7. Download 3 — Extract the minimal source-byte contract

## Objective

Extract only the proven byte-handling contract from the repaired and shielded Preview implementation.

## Important limitation

This is not a project-wide file-I/O rewrite.

## Canonical owner

The existing Tool owner responsible for source inspection/transformation.

If reconciliation identifies an existing source-artifact or byte-preservation owner, extend it.

Create a new module only if no canonical owner exists.

## Minimal public contract

Possible public object:

```text
SourceTextArtifact
```

Minimum responsibilities:

* Read Python source as bytes.
* Compute original byte hash.
* Detect encoding and BOM.
* Record newline style.
* Expose decoded Unicode text.
* Build candidate bytes explicitly.
* Compute candidate byte hash.
* Verify round trip.
* Restore exact original bytes.

## Not included yet

* Generic binary-file support.
* Automatic encoding guessing.
* Project-wide migration.
* New transaction engine.
* New diff engine for every file type.
* New cache framework.

## Integration

Patch Preview becomes the first consumer of the extracted public contract.

## Required validation

1. Existing Patch Preview Shield remains fully green.
2. No public contract regression.
3. No duplicate byte-handling implementation remains inside the Preview Box.
4. Public facade remains stable.
5. No module exceeds 500 physical lines.

## Freeze

Freeze the reusable contract and its Patch Preview integration as one accepted feature only if canonical ownership remains pure.

---

# 8. Download 4 — Extend existing operation identity

## Objective

Add the smallest missing identity capability without creating another identity system.

## Canonical owner

Existing Project Selection, operation, request, or transaction identity owner identified during reconciliation.

## Reuse requirements

Reuse:

* Selected Project stable ID.
* Project root fingerprint.
* Project epoch if already canonical.
* Existing generation or operation identity.
* Existing stale-result rejection.

## New capability only if missing

Introduce the Preview-specific distinction:

```text
preview_content_id
preview_attempt_id
```

## Content identity

Represents:

* Selected Project identity.
* Target relative path.
* Original source hash.
* Issue fingerprint.
* Correction-plan hash.
* Transformer version.

## Attempt identity

Represents:

* One execution.
* One temporary workspace.
* One progress stream.
* One cancellation lifecycle.
* One GUI generation.
* One cleanup responsibility.

## Anti-leak requirements

* An attempt cannot write outside its declared roots.
* Late attempt results cannot update a newer operation.
* Changing selected Project invalidates the attempt.
* Changing target invalidates the attempt.
* Content identity cannot authorize source installation.

## Required validation

* Same content, multiple attempts.
* Different content, multiple attempts.
* Project switch.
* Target switch.
* Cancellation and restart.
* Late-result discard.
* Content integrity violation.

---

# 9. Download 5 — Governed test-workspace isolation

## Objective

Provide reusable test isolation without creating another execution framework.

## Canonical owner

Existing Tool testing or validation infrastructure owner.

Create a small test utility only if no suitable owner exists.

## Responsibilities

* Unique temporary Tool execution root.
* Unique selected-Project fixture root.
* Unique Project Support fixture root.
* Unique daily-work fixture root.
* Cleanup registered before test execution.
* Post-test leak detection.
* Bounded Windows locked-file diagnostics.
* No access to real Project Support during isolated tests.

## Required tests

* Cleanup after success.
* Cleanup after assertion failure.
* Cleanup after setup failure.
* Cleanup after worker exception.
* Cleanup after cancellation.
* No real Project Support mutation.
* No daily-work leakage.
* Repeated suite execution.
* Randomized test order when available.

## Integration

Patch Preview tests migrate first.

No other Box migrates in this ZIP.

---

# 10. Download 6 — Extend the existing package validator with exact-final-ZIP replay

## Objective

Validate the literal final ZIP that will be delivered.

## Canonical owner

Existing package-validation owner.

## Forbidden action

Do not create another ZIP engine or package authority.

## Replay sequence

1. Recalculate final ZIP SHA-256.
2. Validate exact member set.
3. Validate path safety.
4. Validate payload hashes.
5. Extract to governed test workspace.
6. Compile exact packaged Python files.
7. Enforce module-size limits.
8. Install into a disposable selected-Project copy or overlay.
9. Run focused tests.
10. Import public facades.
11. Import known consumers.
12. Run GUI lifecycle tests where applicable.
13. Prepare Freeze evidence without writing it.
14. Parse Error Memory candidates.
15. Verify no support or daily-work leakage.
16. Destroy the environment.
17. Emit structured validation evidence.

## MCard relationship

Where the workflow already uses MCard:

* MCard retains selected Project/target lifecycle authority.
* Exact-final-ZIP replay becomes evidence consumed by Brick Wall.
* It does not replace MCard.

## Exit condition

No patch ZIP is user-deliverable without exact-final-ZIP replay evidence.

---

# 11. Download 7 — Structured validation evidence

## Objective

Replace terminal-text authority with typed evidence under the existing validation owner.

## Canonical owner

Current validation/evidence owner.

## Minimal evidence model

```text
schema_version
gate_id
feature_id
generation_id
operation_id
content_id
attempt_id
selected_project_stable_id
input_hashes
output_hashes
environment_fingerprint
exit_code
structured_result
evidence_file_hashes
parent_evidence_ids
```

## Rules

* Human-readable PASS output is rendered from structured evidence.
* PASS text cannot create lifecycle authority.
* Evidence from an older generation is stale.
* Changed candidate bytes invalidate downstream evidence.
* Evidence belongs to its owning Project.
* Evidence cannot be transferred between Projects.
* Generated summaries remain non-authoritative.

## Brick Wall integration

Brick Wall consumes evidence records and decides whether the next phase is permitted.

No new Brick Wall engine is created.

---

# 12. Download 8 — Link existing installation receipts to validation evidence

## Objective

Strengthen the existing installer/transaction owner without creating another write engine.

## Reconciliation prerequisite

Identify and reuse the current:

* Transaction owner.
* Backup owner.
* Receipt owner.
* Rollback owner.

## Required additions only

* Link installation receipt to exact final ZIP hash.
* Link it to the validated generation.
* Record pre-install source hashes.
* Record installed source hashes.
* Record rollback verification.
* Record selected Project stable ID and root fingerprint.

## Installation rules

1. M4-equivalent package evidence must exist.
2. Current source must still match inspected hashes.
3. Writes remain within declared Project Source paths.
4. Backups remain under daily-work or existing canonical backup owner.
5. Installed hashes must match candidates.
6. Rollback is not successful until restored hashes match originals.

## Anti-leak rules

* Installer implementation: Tool Source.
* Installed files: selected Project Source.
* Receipt: selected Project Support.
* Temporary backup: daily-work.
* No Project-specific receipt in reusable Tool state.

---

# 13. Download 9 — Freeze evidence lineage adapter

## Objective

Extend the existing Freeze system so its evidence is linked to the exact validated installation.

## Canonical owner

Existing Project Freeze owner.

## No new Freeze engine

Reuse:

* Freeze Hint Intake.
* Freeze evidence merge.
* Preview Freeze Entry.
* Confirm and Write.
* Current Project-specific Freeze storage.

## Required lineage

```text
final ZIP hash
→ package validation evidence
→ installation receipt
→ installed validation evidence
→ Freeze hint
```

## Freeze readiness checks

* Same feature generation.
* Same selected Project stable ID.
* Same installed file hashes.
* No stale validation.
* No pending-validation wording.
* Correct protected paths.
* Correct Project-relative paths.
* No reused consumed feature identity.
* Correct public owner imports.
* No Tool/Project leakage.

## Human-only boundary

The adapter may prepare evidence.

It may not execute:

* Preview confirmation.
* Confirm and Write.

---

# 14. Download 10 — Error Memory evidence linkage

## Objective

Extend the existing Error Memory system so lesson drafts are linked to proven failure and validated correction evidence.

## Canonical owner

Existing Project Error Memory owner.

## No new memory engine

Reuse:

* Pending intake.
* Marker-wrapped transport.
* Draft model.
* Active-ready validation.
* Duplicate-family logic.
* Memorize Error GUI action.

## Automatic draft capture

Capture:

* Failure phase.
* Feature generation.
* Failed ZIP hash.
* Failing test.
* Exception.
* Evidence classification.
* Source hashes.
* Environment fingerprint.
* Installation status.
* Rollback status.
* Existing matching lessons.

## Active-ready requirements

1. Root cause proven.
2. Reusable wrong assumption identified.
3. Corrected ZIP identified.
4. Corrected ZIP installed.
5. Relevant regression passes.
6. Full applicable validation passes.
7. Duplicate-family search passes.
8. Final serialized lesson validates.
9. Human selects Memorize Error.

## Regression linkage

Active lessons may declare:

* Owning Box.
* Trigger paths.
* Trigger symbols.
* Required focused tests.
* Required architecture checks.
* Required environment checks.

Brick Wall may then add those obligations to future validation.

Error Memory itself does not become a test runner.

---

# 15. Optional Download 11 — Small governed implementation bridge update

## Status

Optional.

Implement only after the executable contracts exist.

## Objective

Teach the AI to request and interpret the new evidence without creating another long canon.

## Small bridge addition

Before coding, require:

* Exact source evidence.
* Canonical owner.
* Active Box.
* Selected Project identity.
* Allowed write set.
* Relevant lessons.
* Required regression.
* Unresolved inference.

Before claiming completion, require:

* Exact-final-ZIP evidence.
* Installation receipt.
* Installed validation evidence.
* Freeze eligibility.
* Error Memory status.

## Important rule

The prompt does not create authority.

It only routes the AI toward the existing executable authorities.

---

# 16. Optional Downloads 12–13 — Controlled adoption in other Boxes

## Objective

Prove that the extracted contracts generalize beyond Patch Preview.

## Candidate order

Choose only one additional source-mutating Box first.

Possible candidate:

* Large File Refactor Workbench.
* Architecture correction Preview.
* Another Engineering Diagnostics correction Box.

## Adoption procedure

1. Reconcile the target Box.
2. Confirm its owner.
3. Identify duplicate local byte/identity logic.
4. Add an adapter to the existing reusable contract.
5. Preserve its public facade.
6. Run Box-focused tests.
7. Run consumer imports.
8. Run GUI lifecycle.
9. Run architecture checks.
10. Remove duplicate private logic only after validation.
11. Shield.
12. Freeze.

Each new Box adoption should normally be its own download.

---

# 17. Summary of downloads

## Minimum likely safe program

| Download | Purpose                            |
| -------: | ---------------------------------- |
|        1 | Wave 2U surgical repair            |
|        2 | Patch Preview Shield               |
|        3 | Minimal source-byte contract       |
|        4 | Extend existing operation identity |
|        5 | Governed test workspace            |
|        6 | Exact-final-ZIP replay             |
|        7 | Structured validation evidence     |
|        8 | Installation receipt linkage       |
|        9 | Freeze evidence lineage            |
|       10 | Error Memory evidence linkage      |

```text
Recommended mandatory total: approximately 10 ZIP downloads
```

## Possible reductions

The total may fall to approximately 8 if reconciliation proves that:

* Operation identity and test-workspace changes belong to one existing owner.
* Validation evidence and installation receipts already share one canonical owner.
* Freeze or Error Memory already accepts the required lineage fields without source modification.

## Possible increases

The total may rise to approximately 12 if:

* Identity-owner and Patch Preview consumer changes must be owner-pure separate ZIPs.
* Package validator and cleanroom runner belong to different owners.
* Freeze evidence and Freeze GUI changes require separate owner deliveries.

## Optional adoption

```text
Small bridge update: +1
First additional Box adoption: +1
Second additional Box adoption: +1
```

## Expected complete range

```text
Core safety implementation: 8–12 downloads
Recommended planning estimate: 10 downloads
With prompt bridge and two additional Box migrations: 11–13 downloads
```

---

# 18. Completion milestone

The first major milestone is reached when:

```text
WAVE2U ALL TESTS: PASS
PATCH PREVIEW BOX SHIELD: PASS
SOURCE BYTE CONTRACT: PASS
PREVIEW ATTEMPT ISOLATION: PASS
TEST WORKSPACE LEAK CHECK: PASS
EXACT FINAL ZIP REPLAY: PASS
INSTALL RECEIPT LINEAGE: PASS
INSTALLED VALIDATION: PASS
FREEZE EVIDENCE LINEAGE: PASS
ERROR MEMORY ACTIVE-READY GATE: PASS
DUPLICATE OWNER CHECK: PASS
TOOL VERSUS PROJECT: PASS
NO_LEAK_LOGIC_V1: PASS
BRICK WALL: AUTHORIZED
```

The implementation principle throughout remains:

> Reconcile before creating.
> Repair before generalizing.
> Shield before extracting.
> Extract only what has been proven.
> Extend existing owners instead of creating competing owners.
