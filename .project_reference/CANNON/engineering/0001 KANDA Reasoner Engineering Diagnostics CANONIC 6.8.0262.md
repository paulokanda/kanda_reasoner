# KANDA Reasoner Engineering Diagnostics

## Updated Complete Engineering Roadmap

### 1. Program objective

The Engineering Diagnostics program transforms KANDA Reasoner’s engineering-review output from a broad collection of warnings into a governed investigation and remediation system.

The final separation of responsibilities is:

Validate Project
Enforces existing architecture, ownership, boundary, and governance contracts.

Full Audit
Provides the broad engineering-health overview and reports clean checks, findings, degraded coverage, missing evidence, draft work, and manual-review requirements.

Engineering Diagnostics
Investigates individual findings and provides structured evidence, history, ownership context, scope classification, grouping, lifecycle state, and recommended next action.

Patch Preview
Later converts an explicitly reviewed remediation intent into an isolated, validated, human-approved patch proposal.

Engineering Diagnostics must remain read-only until the later Patch Preview phase.

It must not directly:

* modify source code;
* execute Ruff fixes;
* remove BOMs;
* alter Architecture Review or Validate Project;
* modify frozen files;
* accept baselines automatically;
* suppress findings silently;
* apply AI-generated remediation;
* generate or install patches without explicit governance.

---

# 2. Current authoritative status

## 2.1 Completed prerequisite

### Wave 2N — Symbol Atlas active-owner filtering

Status: COMPLETED AND PROTECTED

Purpose:

* remove inactive historical and reference candidates before canonical-owner ranking;
* prevent `.project_reference`, `_project_reference`, deprecated, and archival sources from competing as active owners;
* preserve historical candidates separately;
* provide a reliable future owner-enrichment contract.

Later Engineering Diagnostics waves rely on this protected contract.

---

## 2.2 Engineering Diagnostics MVP

### Wave 2O-A — Backend foundation and BOM vertical slice

Status: FROZEN

Implemented:

* Engineering Diagnostics public backend;
* immutable diagnostic records;
* project boundary and support-root contracts;
* deterministic issue and scan fingerprints;
* project-owned SQLite persistence;
* atomic completed-run storage;
* baseline creation and explicit activation;
* new, persistent, and resolved comparison;
* BOM public adapter;
* stale project, source, scope, configuration, and generation rejection;
* single persistent mutation owner through `EngineeringDiagnosticsStore`.

Canonical persistence location:

`<selected-project-support-root>\project_engineering_diagnostics\engineering_diagnostics.sqlite3`

Important frozen rules:

* `EngineeringDiagnosticsStore` remains the only persistent mutation owner.
* Project diagnostic state must remain outside canonical source.
* Engineering Diagnostics must not reuse another subsystem’s database.
* Collectors and GUI consumers must communicate through public contracts.
* Tool and selected Project remain logically separate during self-hosting.

---

### Wave 2O-B — Engineering Diagnostics GUI vertical slice

Status: FROZEN

Implemented:

* Engineering Diagnostics sibling tab under Audit Project;
* BOM diagnostic execution;
* background worker and cooperative cancellation;
* diagnostic run history;
* issue table;
* severity, lifecycle, path, and text filtering;
* exact evidence and source excerpt display;
* active-baseline comparison;
* explicit human-confirmed baseline activation;
* stale generation, changed Project, changed source, and cancelled-result rejection;
* transient GUI filtering, selection, and worker state.

Corrective validation entry also frozen:

* token-bound Portable Smoke support-root fixtures;
* exact `--project-root` invocation for the Wave 2O-A validator;
* original Wave 2O-B production GUI and backend preserved.

---

### Wave 2O-C — Ruff structured ingestion and high-volume behavior

Status: FROZEN

Final package revision: `v1r2`

Implemented:

* Ruff native machine-readable JSON ingestion;
* Ruff version and configuration capture;
* no parsing of human-readable Ruff output;
* no execution of Ruff fixes;
* no Project-source mutation;
* deterministic Ruff normalization;
* exact duplicate suppression;
* stable identity across line insertion and whitespace changes;
* explicit identity changes for file or function rename;
* safe and unsafe fix metadata retained only as evidence;
* Ruff collector in the Engineering Diagnostics GUI;
* high-volume persistence for at least 25,000 findings;
* deterministic streaming run digest above 10,000 findings;
* backward-compatible original digest at or below 10,000 findings;
* Ruff failure isolation that preserves existing BOM history;
* direct indexed `QAbstractTableModel`;
* removal of `QSortFilterProxyModel`;
* removal of Python `filterAcceptsRow` high-volume callbacks;
* transient filtering and sorting in one table-model owner.

Validated live performance:

* 25,000-row initialization: passed;
* filter update: passed;
* panel creation: passed;
* GUI responsiveness: passed.

---

### Wave 2O-D — Architecture diagnostic ingestion

Status: FROZEN

Final package revision: `v1r1`

Implemented:

* Architecture Review findings as an Engineering Diagnostics collector;
* collection only through the public `scan_project` facade;
* no Architecture Review private imports;
* no parsing of human-readable terminal output;
* no Architecture Review write execution;
* no modification of Validate Project or Architecture Review;
* preservation of severity, rule, owner, boundary, path, symbol, evidence, and validation source;
* architecture option in the Engineering Diagnostics GUI;
* zero architecture errors represented as `CLEAN`;
* architecture warnings retained as diagnostic evidence;
* canonical POSIX source-map keys;
* Windows-safe `Path.as_posix()` lookup normalization;
* persistence through the existing Engineering Diagnostics store.

The complete Engineering Diagnostics MVP is now frozen.

---

# 3. Current product capability

Engineering Diagnostics currently supports:

| Capability                                   | Status   |
| -------------------------------------------- | -------- |
| BOM structured diagnostics                   | Complete |
| Ruff structured diagnostics                  | Complete |
| Architecture structured diagnostics          | Complete |
| Project-owned SQLite run history             | Complete |
| Stable issue fingerprints                    | Complete |
| Run identity separated from attempt identity | Complete |
| Active-baseline comparison                   | Complete |
| Explicit baseline activation                 | Complete |
| Cooperative cancellation                     | Complete |
| Changed-source rejection                     | Complete |
| Changed-Project rejection                    | Complete |
| Stale-generation rejection                   | Complete |
| Exact source evidence                        | Complete |
| High-volume GUI                              | Complete |
| 25,000-finding persistence                   | Complete |
| Direct indexed table model                   | Complete |
| Read-only collector execution                | Complete |
| Architecture contract preservation           | Complete |

The MVP intentionally does not yet include:

* scope enrichment;
* frozen-path enrichment;
* Symbol Atlas owner enrichment;
* Shadow collection;
* deterministic diagnostic groups;
* lifecycle decisions;
* suppressions;
* accepted risks;
* remediation intents;
* Full Audit drill-through;
* Patch Preview;
* automatic correction;
* AI remediation;
* reachability inference;
* SARIF import/export.

---

# 4. Next governed phase

## Wave 2P-A — Scope and frozen-path enrichment

Status: NEXT

### Objective

Add reliable Project context to each diagnostic issue without introducing speculative ownership or reachability claims.

### New enrichment fields

Each issue should receive:

Scope classification:

* ACTIVE
* TEST
* FIXTURE
* PROTOTYPE
* GENERATED
* REFERENCE
* DEPRECATED
* WORKBENCH
* SNIPPET
* TEMPORARY
* UNKNOWN

Frozen classification:

* UNFROZEN
* FROZEN
* TOUCHES_FROZEN
* HISTORICAL_FROZEN
* UNKNOWN

Supporting evidence:

* classification method;
* matching policy or manifest;
* confidence;
* governing Freeze IDs;
* protected paths involved.

### Evidence precedence

1. Explicit Project exclusion policy
2. Explicit scope marker
3. Canonical path classification
4. Generated-file or source manifest
5. Public import-graph evidence
6. UNKNOWN

### Hard governance rule

Any future remediation intent touching an active frozen path must become:

`PLAN_GOVERNED_WAVE`

Diagnostics must not offer a direct fix or bypass action.

### Required validation

* deterministic classification;
* exact Project-relative paths;
* current frozen-memory lookup;
* no writes to frozen memory;
* no writes to `project_freeze_ledger`;
* no private Freeze imports;
* all Wave 2O contracts preserved;
* Tool versus selected Project separation preserved;
* architecture non-regression;
* `STATUS: IN_SYNC`.

---

# 5. Remaining implementation roadmap

## Wave 2P-B — Symbol Atlas owner enrichment

### Objective

Consume the protected Wave 2N owner-resolution contract.

### Output

* canonical owner;
* active owner candidates;
* historical owner candidates;
* competing owners;
* owner confidence;
* owner evidence;
* degraded-owner state;
* owner decision reason.

Confidence levels:

* HIGH
* MEDIUM
* LOW
* NONE

Failure behavior:

If Symbol Atlas is degraded or insufficient:

* the diagnostic issue remains usable;
* owner information is not presented as authoritative;
* owner status becomes `DEGRADED` or `NOT_EVALUATED`;
* confidence becomes `LOW` or `NONE`.

No private Symbol Atlas reach-in is permitted.

---

## Wave 2Q-A — Deterministic diagnostic grouping

### Objective

Reduce noise without claiming unproven root-cause intelligence.

### Initial grouping recipes

BOM:

* rule plus file.

Ruff:

* rule plus canonical file;
* rule plus structural parent;
* rule plus package.

Architecture:

* rule plus owner Box;
* rule plus violated boundary.

### Terminology

Automatically created collections must initially be called:

`Diagnostic groups`

They must not automatically be called:

`Confirmed root causes`

### Confidence

* deterministic same-rule group: HIGH;
* cross-location inferred group: MEDIUM;
* low-confidence grouping: not performed automatically.

### Manual governance

Support:

* ungroup;
* create manual group;
* move issue to group;
* mark group reviewed.

Every manual grouping change must be recorded in persistent decision history.

---

## Wave 2Q-B — Shadow collector and relational grouping

### Objective

Add Shadow findings after deterministic grouping is proven.

### Structured Shadow findings

Examples:

* `RUNTIME_LOGIC_IN_FACADE`
* `BEHAVIOR_DEFINED_IN_FACADE`
* `DUPLICATE_PUBLIC_SYMBOL`
* `UNBOUND_ALL_EXPORT`

### Deterministic relational graph

Nodes:

* file;
* symbol;
* public surface;
* facade;
* implementation owner;
* export.

Edges:

* duplicate_of;
* reexports;
* facade_of;
* implements;
* unbound_export.

Connected components may become diagnostic groups only when every edge is supported by deterministic evidence.

No semantic embeddings, unsupervised clustering, or AI grouping should be included at this stage.

---

## Wave 2R — Lifecycle, suppression, and accepted-risk governance

### Objective

Allow human diagnostic decisions without modifying source.

### Lifecycle states

* OPEN
* INVESTIGATING
* CONFIRMED
* FIX_PLANNED
* PATCH_PREPARED
* VALIDATING
* RESOLUTION_CANDIDATE
* RESOLVED
* ACCEPTED_RISK
* FALSE_POSITIVE
* SUPPRESSED
* DEFERRED
* REOPENED

### Persistent actions

* confirm issue;
* suppress with reason;
* accept risk;
* mark false positive;
* defer to governed wave;
* reopen.

### Required decision metadata

* issue or group;
* action;
* reason code;
* rationale;
* author;
* date;
* expiration or revisit condition;
* related ticket;
* related governed wave.

### Hard rules

* findings are never silently deleted;
* suppression requires a reason;
* accepted risk requires explicit confirmation;
* false positives remain searchable;
* baseline acceptance does not imply risk acceptance;
* lifecycle decisions do not modify source.

---

## Wave 2S — Remediation intents and validation plans

### Objective

Provide useful, non-mutating engineering advice.

### Trust order

1. Tool-provided deterministic metadata
2. KANDA deterministic rule template
3. Project-governance rule
4. AI-assisted hypothesis

### Remediation intent content

* likely correction;
* reason;
* canonical owner;
* expected affected files;
* frozen-path impact;
* required governed wave;
* fix applicability;
* mechanical safety;
* semantic-review requirement;
* focused tests;
* validation commands;
* rollback expectation;
* uncertainty.

### Action classes

* FIX_NOW
* PLAN_GOVERNED_WAVE
* HUMAN_DECISION_REQUIRED
* EVIDENCE_REQUIRED
* SAFE_MECHANICAL_FIX_AVAILABLE
* DEFERRED_TECHNICAL_DEBT
* SUPPRESS_WITH_JUSTIFICATION
* DO_NOT_TOUCH

A remediation intent is not an executable patch.

AI-generated advice must be visibly labeled:

`AI-assisted hypothesis`

It must cite deterministic evidence and must never override frozen-path rules.

---

## Wave 2T — Full Audit drill-through integration

### Objective

Connect Full Audit summary rows to Engineering Diagnostics.

Example:

```text
Ruff Quality
Assessment: PASS_WITH_FINDINGS
Raw findings: 19,882
Canonical issues: 17,450
Diagnostic groups: 312
New high-priority issues: 4

Open in Engineering Diagnostics
```

The action should pass filters such as:

* collector;
* compatible run ID;
* baseline state;
* rule family;
* severity.

### Governance requirement

Wave 2M Full Audit files are frozen.

Therefore, this must be a separately governed integration wave.

It must:

* preserve Wave 2M assessment semantics;
* avoid duplicating diagnostic content inside Full Audit;
* use a narrow public navigation contract;
* create a corrective Freeze only for the affected integration surface.

---

## Wave 2U — Patch Preview integration

### Objective

Convert reviewed remediation intents into isolated patch proposals.

### Workflow

Reviewed remediation intent
→ generate patch plan
→ calculate frozen impact
→ create isolated workspace
→ preview exact diff
→ run focused validation
→ run Validate Project
→ require human confirmation
→ install through normal governed delivery

### Initial eligible corrections

Only explicitly approved, narrowly mechanical changes such as:

* single-file UTF-8 BOM removal;
* single unused import where Ruff marks the fix safe;
* deterministic formatting in one unfrozen file.

### Hard safety requirements

* original hash captured;
* exact-source precondition;
* exact diff preview;
* isolated workspace;
* rollback package;
* frozen-path hard block;
* no global Ruff fix;
* no global formatter;
* focused tests;
* architecture validation;
* explicit human application.

Patch Preview must be a separate governed Box.

---

## Wave 2V — Advanced optional diagnostics

### Status

OPTIONAL AND DEFERRED

Potential independent capabilities:

* probabilistic import reachability;
* GUI-startup reachability;
* runtime trace collection;
* AI root-cause hypotheses;
* cross-rule correlation;
* SARIF import and export;
* IDE integration;
* trend analytics;
* collector caching;
* incremental diagnostics.

Wave 2V should not be treated as one mandatory monolithic feature.

Each capability should be evaluated and governed independently.

None is required for the deterministic core.

---

# 6. Storage roadmap

## Current persistent diagnostic state

Current project-owned SQLite state:

`<selected-project-support-root>\project_engineering_diagnostics\engineering_diagnostics.sqlite3`

This remains owned by:

`EngineeringDiagnosticsStore`

No later wave may create a competing persistent mutation owner.

## Future persistent human decisions

Lifecycle decisions, suppressions, accepted risks, manual groups, and remediation intents should use a governed Project-specific support location.

They must not be written to:

* canonical source directories;
* reusable Tool-private storage;
* `project_freeze_ledger`;
* temporary daily-work storage as their only authoritative copy.

Any new persistent decision store requires:

* one canonical owner;
* explicit schema version;
* atomic writes;
* rollback;
* migration tests;
* Project identity binding;
* human confirmation where applicable;
* separate Freeze protection.

---

# 7. Baseline roadmap

Current baseline behavior is explicit and human-controlled.

Future lifecycle comparison should support:

* NEW
* EXISTING
* CHANGED
* POSSIBLE_MOVE
* POSSIBLE_RENAME
* RESOLUTION_CANDIDATE
* RESOLVED
* REGRESSED
* SUPPRESSED
* ACCEPTED_RISK
* FALSE_POSITIVE

A finding should become `RESOLUTION_CANDIDATE` after one complete compatible run in which it is absent.

It should become `RESOLVED` after:

* two consecutive complete compatible clean runs; or
* an exact dedicated regression contract proves resolution.

A partial, cancelled, degraded, incompatible, or invalid-coverage run must not resolve findings or become the accepted baseline.

---

# 8. Failure-isolation roadmap

Every collector should retain an independent state:

* COMPLETE
* COMPLETE_WITH_FINDINGS
* DEGRADED
* INVALID_COVERAGE
* MISSING_EVIDENCE
* FAILED
* CANCELLED
* NOT_RUN

Required behavior:

* one collector failure does not erase other results;
* malformed output is retained as diagnostic evidence;
* collector stderr and exit code remain available;
* partial runs cannot become baselines;
* cancellation prevents unfinished result persistence;
* completed collector results may remain inspectable;
* collector-version drift is explicit;
* schema incompatibility fails closed.

---

# 9. Validation strategy for every remaining wave

Every feature must continue the KANDA routine:

INSTALL
→ VALIDATE
→ FREEZE
→ ERROR MEMORY, when applicable

Every delivery requires:

* one self-contained feature ZIP;
* independent PowerShell blocks;
* transactional installation;
* exact-source validation;
* idempotence;
* unknown-source rejection;
* rollback testing;
* public-boundary tests;
* focused functional tests;
* prior frozen-contract regression tests;
* architecture non-regression;
* Project Selection Registry immutability;
* Tool versus selected Project separation;
* `VALIDATION OK`;
* `STATUS: IN_SYNC`;
* human-reviewed Freeze Preview;
* explicit Confirm and Write.

Freeze and Error Memory remain independent.

A prepared Freeze intake is not the same as a frozen feature.

A feature is frozen only after the persistent Project-specific frozen-memory entry exists.

---

# 10. Updated downloads remaining

## Engineering Diagnostics MVP

Downloads remaining: **0**

Completed and frozen:

* Wave 2N prerequisite;
* Wave 2O-A;
* Wave 2O-B;
* Wave 2O-B validation corrective entry;
* Wave 2O-C;
* Wave 2O-D.

## Core post-MVP roadmap

Assuming one governed feature package per listed wave, downloads remaining through Patch Preview:

1. Wave 2P-A — Scope and frozen-path enrichment
2. Wave 2P-B — Symbol Atlas owner enrichment
3. Wave 2Q-A — Deterministic grouping
4. Wave 2Q-B — Shadow collector and relational grouping
5. Wave 2R — Lifecycle, suppression, and accepted-risk governance
6. Wave 2S — Remediation intents and validation plans
7. Wave 2T — Full Audit drill-through
8. Wave 2U — Patch Preview integration

Core planned downloads remaining: **8**

## Optional advanced roadmap

Wave 2V remains optional.

Because Wave 2V contains several independent capabilities, it should not be assumed to equal exactly one download.

For simple roadmap counting:

* minimum optional umbrella count: **1**
* realistic implementation count: multiple separately governed packages

## Current total

Mandatory planned downloads remaining: **8**

Mandatory plus Wave 2V counted as one optional umbrella download: **9**

Corrective revisions discovered during live validation are not included in this planned count.

Error Memory reviews and Freeze confirmation steps are procedural phases and are not counted as new feature downloads unless a separate governed intake package is explicitly required.

---

# 11. Immediate next action

The next implementation should be:

## Wave 2P-A — Scope and frozen-path enrichment

Before implementation, its handoff should load and preserve the exact frozen contracts from:

* Wave 2N;
* Wave 2O-A;
* Wave 2O-B;
* Wave 2O-B corrective validation entry;
* Wave 2O-C;
* Wave 2O-D.

Wave 2P-A must remain owner-pure.

It should add deterministic enrichment through public contracts without:

* changing collector meaning;
* changing baseline meaning;
* changing diagnostic fingerprints;
* introducing remediation;
* introducing lifecycle decisions;
* introducing owner enrichment;
* introducing reachability inference;
* creating another database;
* modifying Freeze memory;
* modifying Full Audit;
* modifying Architecture Review;
* modifying Symbol Atlas private logic.

The acceptance target is:

```text
SCOPE CLASSIFICATION: PASS
FROZEN PATH CLASSIFICATION: PASS
GOVERNING FREEZE IDS: PASS
FROZEN MEMORY MUTATED: NO
PROJECT_FREEZE_LEDGER USED: NO
ENGINEERING DIAGNOSTICS STORE OWNER: PRESERVED
WAVE2OA THROUGH WAVE2OD REGRESSION: PASS
NEW ARCHITECTURE ISSUES: 0
TOUCHED PATH ARCHITECTURE ISSUES: 0
VALIDATION OK: <wave-2p-a-feature-id>
STATUS: IN_SYNC
```

---

# 12. Final program position

The Engineering Diagnostics MVP is complete.

KANDA Reasoner can now:

* collect BOM, Ruff, and Architecture findings;
* normalize them into one diagnostic domain;
* persist Project-owned run history;
* maintain stable finding identity;
* compare runs with an explicitly accepted baseline;
* retain exact evidence;
* reject stale or changed-source completions;
* process at least 25,000 findings;
* display large result sets responsively;
* execute diagnostics without modifying source;
* preserve architecture and Box boundaries.

The next phase changes the product from a structured finding viewer into a governed investigation system.

The development order from this point is:

```text
2P-A Scope and frozen paths
→ 2P-B Owner enrichment
→ 2Q-A Deterministic grouping
→ 2Q-B Shadow relational diagnostics
→ 2R Human lifecycle decisions
→ 2S Remediation intents
→ 2T Full Audit drill-through
→ 2U Governed Patch Preview
→ 2V Optional advanced capabilities
```

The immediate planned download is Wave 2P-A.

After it is delivered, validated, and frozen, the mandatory core download count will fall from eight to seven.
