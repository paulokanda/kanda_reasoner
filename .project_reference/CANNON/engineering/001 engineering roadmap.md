# KANDA Reasoner Engineering Diagnostics

## Consolidated Architecture Decision and Detailed Implementation Roadmap

## 1. Executive decision

The proposed sibling tab should be implemented.

The final separation of responsibilities will be:

```text
Validate Project
→ Enforces established architecture and governance contracts.

Full Audit
→ Provides a broad engineering-health summary.

Engineering Diagnostics
→ Investigates individual findings, their origin, evidence, scope, ownership,
  history and recommended next action.

Patch Preview
→ Later converts an approved remediation intent into a governed patch.
```

The new tab must initially remain completely read-only.

It must not:

* edit source files;
* execute Ruff fixes;
* remove BOMs;
* write suppression decisions without human confirmation;
* modify frozen files;
* generate or apply patches;
* silently accept a degraded baseline;
* treat AI-generated explanations as authoritative facts.

The implementation should not begin with all collectors, root-cause analysis, reachability, AI remediation and patch generation simultaneously.

The safe strategy is a series of thin vertical slices.

The first complete slice should prove:

```text
collect
→ normalize
→ fingerprint
→ persist
→ compare with baseline
→ display
→ inspect evidence
```

using one simple collector before expanding to Ruff, Architecture, Shadow and Symbol Atlas.

---

# 2. Audit of the three expert answers

## 2.1 Strong consensus

All three responses correctly support the following decisions:

### KEEP — sibling tab

Full Audit should remain a summary and orchestration surface.

Engineering Diagnostics should be a dedicated investigation workspace.

This prevents Full Audit from becoming an enormous and unusable log.

### KEEP — read-only diagnostics

The diagnostic pipeline must not mutate source code.

Patch creation and application must remain separate and governed.

### KEEP — separate facts from inference

The original monolithic `EngineeringIssue` model should not be used.

Tool facts, normalized identities, enrichment, decisions and remediation plans must be separate records.

### KEEP — stable baseline tracking

The system should track findings across runs rather than treating every run as a completely new report.

### KEEP — deterministic evidence first

Tool output, exact locations and rule-based explanations should appear before any AI interpretation.

### KEEP — defer deep reachability

Python import and call reachability cannot be represented as a certain boolean.

Dynamic imports, PySide6 signals, plugins, `getattr`, runtime dispatch and conditional imports prevent reliable static certainty.

### KEEP — deterministic grouping first

Do not begin with generic graph clustering or AI clustering.

Group findings using explicit, auditable rules.

### KEEP — frozen-path enforcement

Any proposed correction touching a frozen path must become:

```text
PLAN_GOVERNED_WAVE
```

The Diagnostics UI must not provide an override.

### KEEP — multidimensional priority

Do not calculate priority by multiplying categorical scores.

The user must be able to understand why an issue received its priority.

---

## 2.2 Recommendations that should be modified

### MODIFY — Wave 2N and Diagnostics sequencing

One response suggested developing Wave 2N and Wave 2O in parallel.

That is acceptable only at the source-development level.

Engineering Diagnostics must not rely on Symbol Atlas ownership until Wave 2N has been:

```text
installed
validated
regression-tested
reviewed
frozen
```

Diagnostics can exist before this with:

```text
owner_status: NOT_EVALUATED
owner_confidence: NONE
```

It must not consume known-degraded owner data as authoritative.

### MODIFY — SARIF usage

SARIF should not be the internal storage model.

Collectors should use their most reliable machine-readable native output:

```text
Ruff → JSON
Architecture Review → canonical project JSON
BOM → canonical project JSON
Shadow → canonical project JSON
Symbol Atlas → canonical project JSON
```

These are normalized into the KANDA model.

SARIF should later be an import/export adapter.

Reasons:

* KANDA requires governance-specific fields not naturally represented by SARIF.
* SARIF is verbose.
* SARIF should not determine KANDA’s internal schema.
* converting every tool to SARIF before normalization adds unnecessary work.

### MODIFY — fingerprinting

No single fingerprint can reliably survive:

* line movement;
* formatting;
* function rename;
* file rename;
* symbol extraction;
* façade relocation.

The system should use multiple fingerprints and a matching algorithm, not one universal hash.

### MODIFY — persistent storage location

Several responses suggested storing governed diagnostic state inside:

```text
kanda_reasoner_app
```

or a generic project-memory folder.

That would mix application source with project-specific diagnostic memory.

The preferred ownership model is:

```text
Temporary and reproducible data:
E:\kanda_reasoner_delete_after_daily_work\
engineering_diagnostics\

Persistent project-specific diagnostic decisions:
E:\kanda_reasoner_show_project_to_AI\
engineering_diagnostics_memory\
```

This follows the existing project-specific support-root convention.

It must not use:

```text
project_freeze_ledger
```

### MODIFY — baseline resolution

A missing finding should not immediately become permanently `RESOLVED`.

The default should be:

```text
First complete clean run:
RESOLUTION_CANDIDATE

Second consecutive complete clean run:
RESOLVED
```

A dedicated regression test can resolve an issue immediately if that validation contract explicitly covers it.

### MODIFY — GUI data model

SQLite should be used for large temporary run data.

However, the UI does not need to depend specifically on `QSqlTableModel`.

A custom virtualized `QAbstractTableModel` backed by paginated SQLite queries provides more control over:

* grouping;
* computed columns;
* partial collector state;
* baseline badges;
* root-cause rows;
* lazy loading.

---

## 2.3 Recommendations that should be rejected or deferred

### REMOVE — one giant `EngineeringIssue` record

Facts, inference and decisions must not be persisted as one object.

### REMOVE — scalar multiplicative priority

It is opaque and can hide a severe issue when another factor has a low value.

### DEFER — static startup reachability

It is not part of the MVP.

Early scope classification should rely on deterministic path rules and explicit markers.

### DEFER — AI-generated remediation

AI suggestions should not appear until deterministic diagnostic explanations, ownership, baselines and validation plans have proven reliable.

### DEFER — automatic fixes

Even apparently simple operations such as BOM removal should not be implemented in the first Diagnostics waves.

### DEFER — generic graph clustering

Graph grouping should initially be limited to Shadow findings whose data is inherently relational.

### REJECT — Full Audit rewrite during initial implementation

Wave 2M protects the Full Audit implementation.

Engineering Diagnostics should initially be added as an independent sibling.

A later corrective wave can add drill-through buttons to Full Audit after Diagnostics is stable.

---

# 3. Final target architecture

```text
┌─────────────────────────────┐
│ Validate Project            │
│ Architecture/governance gate│
└─────────────────────────────┘

┌─────────────────────────────┐
│ Full Audit                  │
│ Broad engineering summary   │
└──────────────┬──────────────┘
               │ later drill-through
               ▼
┌──────────────────────────────────────────┐
│ Engineering Diagnostics                  │
│ Investigation and evidence workspace     │
└─────────────────┬────────────────────────┘
                  ▼
┌──────────────────────────────────────────┐
│ Diagnostic Run Engine                    │
├──────────────────────────────────────────┤
│ Collectors                               │
│ Normalizers                              │
│ Fingerprint matcher                      │
│ Baseline comparator                      │
│ Enrichers                                │
│ Deterministic grouping                   │
│ Decision and lifecycle engine            │
│ Remediation-intent planner               │
└─────────────────┬────────────────────────┘
                  ▼
┌──────────────────────────────────────────┐
│ Storage                                  │
├──────────────────────────────────────────┤
│ Temporary SQLite run database            │
│ Raw collector artifacts                  │
│ Persistent governed decisions            │
│ Accepted baseline                        │
└──────────────────────────────────────────┘
```

---

# 4. Domain model

The system should use linked records instead of one monolithic dataclass.

## 4.1 DiagnosticRule

Represents a rule definition, not an occurrence.

```python
DiagnosticRule:
    tool
    rule_id
    rule_version
    title
    deterministic_explanation
    category
    default_impacts
    default_action_class
    tool_fix_capability
    documentation_reference
```

Examples:

```text
ruff:F821
bom:UTF8_BOM_DETECTED
architecture:PUBLIC_SURFACE_VIOLATION
shadow:DUPLICATE_PUBLIC_SYMBOL
```

---

## 4.2 RawFinding

Immutable representation of exactly what a collector returned.

```python
RawFinding:
    raw_finding_id
    run_id
    collector_id
    tool
    tool_version
    ruleset_version
    rule_id
    message
    raw_severity
    raw_payload_reference
    primary_location
    related_locations
    captured_at
```

The raw payload should not be rewritten after collection.

---

## 4.3 CanonicalIssue

Deterministic normalized identity.

```python
CanonicalIssue:
    issue_id
    strict_fingerprint
    semantic_fingerprint
    location_fingerprint
    tool
    rule_id
    normalized_message_key
    structural_context
    normalized_context_hash
    first_seen_run_id
    last_seen_run_id
    schema_version
```

This record must contain no ownership, reachability, priority or remediation opinion.

---

## 4.4 RunOccurrence

Represents the appearance of an issue in one diagnostic run.

```python
RunOccurrence:
    run_id
    issue_id
    raw_finding_ids
    occurrence_count
    current_location
    source_excerpt_reference
    baseline_state
    match_method
    match_confidence
```

Possible match methods:

```text
STRICT
SEMANTIC
RENAME_AWARE
CONTEXTUAL
LOCATION_FALLBACK
MANUAL
```

---

## 4.5 IssueEnrichment

Regenerable contextual information.

```python
IssueEnrichment:
    run_id
    issue_id

    scope_classification
    scope_confidence
    scope_evidence

    canonical_owner
    owner_candidates
    owner_confidence
    owner_evidence

    frozen_status
    governing_freeze_ids

    reachability_classification
    reachability_confidence
    reachability_method
    reachability_caveat

    impact_vector
    overall_priority
    priority_reason

    root_cause_group_id
    grouping_confidence
    grouping_method

    enrichment_version
    generated_at
```

---

## 4.6 DiagnosticDecision

Persistent human-governed state.

```python
DiagnosticDecision:
    decision_id
    issue_id

    lifecycle_state
    decision_type
    reason_code
    rationale

    created_by
    created_at
    reviewed_by
    reviewed_at

    expiration_policy
    revisit_after_run_count
    related_ticket
    related_wave
```

Decision types:

```text
CONFIRM
SUPPRESS
ACCEPT_RISK
FALSE_POSITIVE
DEFER
REOPEN
RESOLVE
```

---

## 4.7 RootCauseGroup

Introduced only after deterministic grouping is implemented.

```python
RootCauseGroup:
    group_id
    title
    grouping_method
    grouping_rule_version
    confidence
    representative_issue_id
    member_issue_ids
    affected_file_count
    affected_symbol_count
    action_class
```

---

## 4.8 RemediationIntent

Not an executable patch.

```python
RemediationIntent:
    intent_id
    issue_id_or_group_id
    source_type

    action_class
    summary
    rationale

    expected_affected_files
    frozen_impact
    required_wave

    fix_applicability
    semantic_review_required

    validation_plan
    rollback_expectation

    ai_generated
    confidence
    human_reviewed
```

---

# 5. Storage architecture

## 5.1 Temporary run storage

```text
E:\kanda_reasoner_delete_after_daily_work\
engineering_diagnostics\
    runs\
        <run_id>\
            active_run.db
            collector_status.json
            raw\
                bom.json
                ruff.json
                architecture.json
                shadow.json
            logs\
            exports\
```

The SQLite database contains:

```text
diagnostic_runs
collector_runs
raw_findings
canonical_issues
run_occurrences
issue_enrichments
root_cause_groups
root_cause_members
```

This database is reproducible and may be deleted.

---

## 5.2 Persistent governed state

```text
E:\kanda_reasoner_show_project_to_AI\
engineering_diagnostics_memory\
    schema.json
    accepted_baseline.json
    issue_decisions.jsonl
    accepted_risks.jsonl
    suppressions.jsonl
    lifecycle_history.jsonl
    remediation_intents.jsonl
    index.json
```

Properties:

* project-specific;
* human-readable;
* append-friendly;
* reviewable;
* independent from temporary run databases;
* not stored in `project_freeze_ledger`;
* protected by future project Freeze entries.

---

## 5.3 Schema versioning

Every persistent record must contain:

```text
schema_version
record_version
created_at
updated_at
```

Schema migration must be explicit.

No migration should silently discard a field or decision.

---

# 6. Fingerprinting and matching strategy

## 6.1 Strict fingerprint

Used for exact matching.

```text
SHA256(
    tool
    + rule_id
    + normalized project-relative path
    + structural anchor
    + normalized message key
    + normalized context token hash
)
```

---

## 6.2 Semantic fingerprint

Used to detect movement or rename.

```text
SHA256(
    tool
    + rule_id
    + structural AST shape
    + normalized message key
    + normalized context token hash
)
```

The path is intentionally excluded.

---

## 6.3 Location fingerprint

Used for findings without a symbol or structural parent.

```text
SHA256(
    tool
    + rule_id
    + normalized relative path
    + normalized line text
    + location bucket
)
```

Examples:

* BOM findings;
* formatting findings at module scope;
* file-wide architecture findings.

---

## 6.4 Matching order

```text
1. Strict fingerprint exact match
2. Semantic fingerprint in same file
3. Semantic fingerprint in renamed-file candidates
4. Context similarity within same rule
5. Location fallback
6. No safe match → NEW
```

A weak match must not automatically merge issues.

It should become:

```text
POSSIBLE_MOVE
POSSIBLE_RENAME
POSSIBLE_RELOCATION
```

requiring human review.

False merging is more dangerous than creating a duplicate issue.

---

## 6.5 Rename detection

Use, in order:

```text
Git rename information, when available
Whole-file content similarity
AST declaration similarity
Manual identity confirmation
```

Do not strip arbitrary numeric path suffixes from fingerprints. That could merge unrelated files.

---

## 6.6 Tool-version changes

A diagnostic run must record:

```text
tool_version
ruleset_version
collector_schema_version
```

If a version changes:

```text
BASELINE_COMPATIBILITY: REVIEW_REQUIRED
```

The system should perform a bridge comparison before declaring thousands of findings new or resolved.

---

# 7. Baseline and lifecycle rules

## 7.1 Baseline acceptance

The baseline must never be accepted automatically.

A human must explicitly choose:

```text
Accept completed run as diagnostic baseline
```

The dialog must show:

```text
collector completeness
collector failures
invalid coverage
issue counts
new issues
resolution candidates
tool-version changes
```

A partial run cannot become the baseline.

---

## 7.2 Baseline states

```text
NEW
EXISTING
CHANGED
POSSIBLE_MOVE
POSSIBLE_RENAME
RESOLUTION_CANDIDATE
RESOLVED
REGRESSED
SUPPRESSED
ACCEPTED_RISK
FALSE_POSITIVE
```

---

## 7.3 Resolution rules

An issue becomes `RESOLUTION_CANDIDATE` when it is absent from one complete run.

It becomes `RESOLVED` when:

```text
it is absent from two consecutive complete compatible runs
```

or:

```text
a dedicated regression validation explicitly proves resolution
```

---

## 7.4 Regression

An issue becomes `REGRESSED` when:

* a resolved fingerprint returns;
* a semantically equivalent fingerprint returns;
* a dedicated regression contract fails again.

---

## 7.5 Accepted risk versus suppression

`ACCEPTED_RISK`:

```text
The issue is understood and intentionally retained.
It does not expire automatically.
```

`SUPPRESSED`:

```text
The issue is temporarily hidden from the default active queue.
It should have an expiration or review condition.
```

Both remain visible in history.

---

# 8. Scope classification

Initial scope classification must be deterministic.

## 8.1 Path classifications

```text
ACTIVE
TEST
FIXTURE
PROTOTYPE
GENERATED
REFERENCE
DEPRECATED
WORKBENCH
SNIPPET
TEMPORARY
UNKNOWN
```

## 8.2 Evidence order

```text
1. Explicit project exclusion policy
2. Explicit scope marker
3. Canonical path pattern
4. Manifest classification
5. Import-graph inference
6. UNKNOWN
```

Potential explicit marker:

```python
# kanda:scope=prototype
```

or a sidecar manifest.

---

## 8.3 Reachability

Reachability is deferred from the MVP.

Later classifications may be:

```text
VERIFIED_ACTIVE
LIKELY_ACTIVE
POSSIBLY_ACTIVE
NOT_OBSERVED
UNKNOWN
```

Every non-verified result must display:

```text
Static evidence only. Runtime behavior may differ.
```

---

# 9. Priority model

Priority must be a transparent vector.

```python
ImpactVector:
    runtime_impact
    architecture_impact
    reliability_impact
    security_impact
    governance_impact
    maintainability_impact
```

Each dimension:

```text
NONE
LOW
MEDIUM
HIGH
CRITICAL
```

Context dimensions:

```text
scope
finding_confidence
owner_confidence
reachability_confidence
baseline_state
frozen_impact
```

Overall priority is derived by explicit rules.

Example:

```text
If security_impact = CRITICAL
→ BLOCKER

If runtime_impact = HIGH
and scope = ACTIVE
and finding_confidence = HIGH
→ HIGH

If governance_impact = HIGH
and frozen_impact = BLOCKING
→ HIGH + PLAN_GOVERNED_WAVE

If maintainability_impact = LOW
and rule = E501
→ LOW

If evidence is missing
→ INFORMATION + EVIDENCE_REQUIRED
```

Every issue must show:

```text
Priority: HIGH
Reason:
Active source + undefined name + high-confidence Ruff rule.
```

No unexplained score should be displayed.

---

# 10. Collector contract

Every collector must implement a common contract.

```python
CollectorResult:
    collector_id
    collector_version
    tool_version
    execution_status
    assessment
    assessment_reason
    coverage
    raw_output_reference
    findings
    started_at
    completed_at
```

Execution statuses:

```text
PASS
FAILED
CANCELLED
```

Assessments should reuse Wave 2M semantics:

```text
CLEAN
PASS_WITH_FINDINGS
DEGRADED
INVALID_COVERAGE
MISSING_EVIDENCE
NOT_RUN
FAILED
```

One collector failure must not abort the whole run.

---

# 11. GUI design

## 11.1 Tab structure

```text
Engineering Diagnostics
├── Run controls
├── Summary
├── Filters
├── Issue/group table
└── Detail panel
```

---

## 11.2 Run controls

```text
Run Diagnostics
Cancel
Compare with Baseline
Accept as Baseline
Export Report
```

No fix button during early waves.

---

## 11.3 Summary

```text
Run status
Collectors complete
Collectors failed
Coverage invalid
Raw findings
Canonical issues
New issues
Existing issues
Resolution candidates
Regressions
Suppressed
Accepted risks
```

---

## 11.4 Filters

MVP filters:

```text
Collector
Rule
Path prefix
Scope
Baseline state
Lifecycle state
Frozen status
```

Later:

```text
Owner
Owner confidence
Priority
Root-cause group
Action class
```

---

## 11.5 Issue table

MVP columns:

```text
State
Tool
Rule
Message
Scope
Path
Line
Frozen
First seen
Last seen
```

The table must:

* use paginated SQLite queries;
* support virtual scrolling;
* avoid loading all source excerpts;
* avoid loading all raw payloads;
* perform filtering outside the GUI thread.

---

## 11.6 Detail panel

MVP sections:

```text
Finding
Exact source location
Source excerpt
Deterministic rule explanation
Raw tool evidence
Baseline history
Scope evidence
Frozen-path status
```

Later sections:

```text
Owner
Root-cause group
Impact vector
Remediation intent
Validation plan
Decision history
```

AI explanations, when eventually added, must appear under:

```text
AI-assisted hypothesis
```

not under deterministic evidence.

---

# 12. Detailed governed implementation roadmap

## Wave 2N — Symbol Atlas active-owner filtering

### Objective

Prevent inactive historical candidates from entering canonical owner ranking.

### Scope

Investigate and modify the Symbol Atlas owner-selection pipeline.

Filtering must happen before ranking.

### Required behavior

```text
.project_reference
_project_reference
reference archives
deprecated ownership sources
```

must not compete as active owners.

Historical candidates may remain available in a separate historical-results field.

### Deliverables

* owner candidate scope classification;
* pre-ranking active-candidate filter;
* historical candidate reporting;
* owner confidence behavior;
* exact regression fixtures;
* focused validator;
* Full Audit verification.

### Required tests

```text
active owner versus historical owner
only historical owner exists
multiple active candidates
facade candidate versus implementation owner
generated candidate
test-only candidate
reference path containing an otherwise identical symbol
```

### Acceptance gate

```text
Known historical owner leakage: eliminated
Active owner ranking tests: PASS
Wave 2M protected files: unchanged
Validate Project: 0 issues
Full Audit Symbol Atlas result: no inactive-reference leakage
STATUS: IN_SYNC
```

### Freeze

Freeze Wave 2N separately before Diagnostics consumes owner enrichment.

---

## Wave 2O-A — Diagnostics contract and BOM vertical slice

### Objective

Prove the complete diagnostic pipeline with the smallest collector.

### Collector

BOM only.

### Deliverables

Domain:

```text
kanda_reasoner_app/engineering_diagnostics/
    enums.py
    schema_version.py
    records.py
    collector_contract.py
    run_engine.py
    fingerprints.py
    matcher.py
    baseline.py
    scope_policy.py
```

Storage:

```text
storage/
    sqlite_run_store.py
    governed_state_store.py
    schema.py
    migrations.py
```

Collector:

```text
collectors/
    bom_collector.py
    bom_normalizer.py
```

CLI or internal runner:

```text
run BOM diagnostic
persist run
compare baseline
print deterministic summary
```

### No GUI requirement yet

This wave proves backend correctness first.

### Required tests

```text
BOM collector returns four known findings
raw payload remains unchanged
normalization is deterministic
line movement does not affect BOM identity
path change creates POSSIBLE_RENAME, not automatic merge
baseline NEW/EXISTING behavior
resolution candidate behavior
partial run cannot become baseline
SQLite schema migration smoke
persistent state never writes to project_freeze_ledger
```

### Acceptance gate

```text
Two identical runs:
NEW on run 1
EXISTING on run 2
0 false NEW
0 false RESOLVED

Remove one BOM in test fixture:
RESOLUTION_CANDIDATE after first complete run
RESOLVED after second complete run

Validate Project: 0 issues
```

### Freeze

Freeze backend contract and storage schema.

---

## Wave 2O-B — Engineering Diagnostics GUI vertical slice

### Objective

Create the sibling tab using the proven BOM pipeline.

### Deliverables

```text
kanda_reasoner_app/engineering_diagnostics_gui/
    engineering_diagnostics_tab.py
    diagnostic_run_worker.py
    diagnostic_table_model.py
    diagnostic_filter_model.py
    diagnostic_summary_panel.py
    diagnostic_detail_panel.py
    source_excerpt_view.py
```

### UI behavior

* run BOM diagnostics;
* stream run state;
* cancel cooperatively;
* display issue table;
* filter by rule/path/state;
* display source excerpt;
* compare with baseline;
* accept baseline after explicit confirmation;
* show persistent decision history read-only.

### Performance gate

```text
25,000 synthetic rows:
initial table visible under 2 seconds
filter update under 500 ms
detail panel under 200 ms
GUI remains responsive
```

These are target thresholds and should be measured on the deployment machine.

### Safety gate

```text
Source files modified: 0
Freeze memory modified: 0
Baseline write requires explicit confirmation
Partial run baseline acceptance: blocked
```

### Freeze

Freeze the GUI and baseline-confirmation contracts.

---

## Wave 2O-C — Ruff structured collector and scale validation

### Objective

Add the first high-volume collector.

### Collector behavior

Execute Ruff with machine-readable JSON.

Do not parse the human-readable log.

Capture:

```text
rule
message
location
fix availability
fix applicability
tool version
```

Do not execute fixes.

### Deliverables

```text
collectors/ruff_collector.py
collectors/ruff_normalizer.py
rules/ruff_rule_registry.py
```

### Initial priority defaults

```text
F821, F822, F601 → HIGH candidate
F811, E402, F403 → MEDIUM/HIGH depending on scope
F401, F841 → MEDIUM/LOW
E501, formatting → LOW
```

These are defaults, not final truth.

### Required tests

```text
malformed Ruff JSON
Ruff executable missing
Ruff version change
line insertion above issue
whitespace formatting
function rename
file rename
duplicate findings
safe-fix metadata capture
unsafe-fix metadata capture
```

### Real-project acceptance

The expected scale is approximately 20,000 findings.

The test must verify:

```text
all rows persisted
no GUI freeze
no duplicate canonical issues caused by pagination
baseline diff remains stable
tool version recorded
collector failure does not erase BOM results
```

### Freeze

Freeze Ruff collection, normalization and high-volume storage behavior.

---

## Wave 2O-D — Architecture collector

### Objective

Represent Validate Project findings inside Diagnostics without changing Validate Project.

### Deliverables

```text
collectors/architecture_collector.py
collectors/architecture_normalizer.py
rules/architecture_rule_registry.py
```

### Behavior

Architecture issues should retain:

```text
severity
rule
owner
boundary
path
symbol
evidence
validation source
```

Architecture findings normally receive higher governance impact.

### Acceptance gate

Current project:

```text
Architecture canonical issues: 0
Collector assessment: CLEAN
Coverage: valid
```

Synthetic fixtures must generate known architecture violations.

### Freeze

Freeze architecture collector behavior.

---

## Wave 2P-A — Scope and frozen-path enrichment

### Objective

Add reliable project context without owner or reachability speculation.

### Deliverables

```text
enrichers/scope_enricher.py
enrichers/frozen_path_enricher.py
scope_manifest.py
```

### Scope evidence

Use:

* current exclusion policy;
* active-source policy;
* exact path classifications;
* explicit markers;
* generated-file manifests.

### Frozen enrichment

For every issue:

```text
UNFROZEN
FROZEN
TOUCHES_FROZEN
HISTORICAL_FROZEN
UNKNOWN
```

Include governing Freeze IDs.

### Hard rule

If a future remediation intent touches any active frozen path:

```text
action_class = PLAN_GOVERNED_WAVE
```

### Required tests

Include all protected paths from Waves 2L, 2M and 2N.

### Freeze

Freeze scope and frozen-path classification.

---

## Wave 2P-B — Symbol Atlas owner enrichment

### Objective

Consume the frozen Wave 2N owner contract.

### Deliverables

```text
enrichers/owner_enricher.py
owner_evidence.py
```

### Output

```text
canonical owner
owner candidates
active candidates
historical candidates
owner confidence
owner decision reason
```

### Confidence levels

```text
HIGH
MEDIUM
LOW
NONE
```

### Failure behavior

If Symbol Atlas is degraded:

```text
owner_confidence = LOW or NONE
owner_status = DEGRADED
```

The issue remains usable without an owner.

### Acceptance gate

Known Wave 2N fixtures must remain correct.

### Freeze

Freeze owner enrichment independently.

---

## Wave 2Q-A — Deterministic grouping

### Objective

Reduce noise without claiming generic root-cause intelligence.

### Initial grouping recipes

BOM:

```text
rule + file
```

Ruff:

```text
rule + canonical file
rule + structural parent
rule + package
```

Architecture:

```text
rule + owner box
rule + violated boundary
```

### Important distinction

The UI should label these:

```text
Diagnostic group
```

not necessarily:

```text
Confirmed root cause
```

### Group confidence

Deterministic same-rule groups:

```text
HIGH
```

Cross-location inferred groups:

```text
MEDIUM
```

No low-confidence automatic grouping.

### Manual controls

```text
Ungroup
Create manual group
Move issue to group
Mark group as reviewed
```

Manual changes must be recorded.

### Freeze

Freeze deterministic grouping rules and manual override history.

---

## Wave 2Q-B — Shadow collector and relational grouping

### Objective

Add Shadow findings after the grouping infrastructure has proven reliable.

### Deliverables

```text
collectors/shadow_collector.py
collectors/shadow_normalizer.py
grouping/shadow_graph_builder.py
grouping/shadow_group_rules.py
```

### Graph nodes

```text
file
symbol
public surface
facade
implementation owner
export
```

### Graph edges

```text
duplicate_of
reexports
facade_of
implements
unbound_export
```

Connected components may become groups only when edge evidence is deterministic.

### No generic clustering

Do not use semantic embedding or unsupervised clustering at this stage.

### Acceptance gate

Manually review a statistically meaningful sample:

```text
all HIGH-confidence groups
random sample of MEDIUM-confidence groups
all groups touching frozen files
```

### Freeze

Freeze Shadow collection and grouping contracts.

---

## Wave 2R — Lifecycle, suppression and accepted-risk governance

### Objective

Allow human triage decisions without changing code.

### Deliverables

```text
decision_engine.py
decision_validation.py
decision_history.py
```

### UI actions

```text
Confirm issue
Suppress with reason
Accept risk
Mark false positive
Defer to wave
Reopen
```

### Required confirmation

Every persistent decision must show:

```text
issue/group
reason
effect
expiration
related wave/ticket
persistent storage path
```

### Hard rules

* no silent deletion;
* suppression reason required;
* accepted risk requires explicit confirmation;
* false-positive decisions remain searchable;
* baseline acceptance does not automatically accept risk;
* decisions do not modify source.

### Freeze

Freeze decision semantics and storage ownership.

---

## Wave 2S — Remediation intents and validation plans

### Objective

Provide actionable advice without producing patches.

### Sources of guidance

Trust order:

```text
1. Tool-provided deterministic metadata
2. KANDA deterministic rule template
3. Project-governance rule
4. AI-assisted hypothesis
```

### Output

```text
What should probably change
Why
Expected owner
Expected files
Frozen impact
Required wave
Validation commands
Uncertainty
```

### Examples

F821:

```text
Potential missing import or invalid symbol reference.
Inspect exact scope and annotation behavior.
Run targeted Ruff F821 and py_compile validation.
```

BOM:

```text
Convert file encoding to UTF-8 without BOM.
Verify consumer compatibility.
Compare file content hash excluding BOM.
```

Historical owner leakage:

```text
Requires governed Symbol Atlas correction.
Do not patch the historical reference file.
```

### AI rules

AI-generated advice must:

* be visually labeled;
* show confidence;
* cite deterministic evidence;
* never be auto-applied;
* never override frozen-path rules.

### Freeze

Freeze remediation-intent semantics.

---

## Wave 2T — Full Audit drill-through integration

### Objective

Connect Full Audit summary rows to Engineering Diagnostics.

Because Wave 2M protects Full Audit files, this requires a separately governed corrective integration wave.

### Behavior

Example:

```text
Ruff Quality
Raw findings: 19,882
Canonical issues: 17,450
Diagnostic groups: 312
New high-priority issues: 4

[Open in Engineering Diagnostics]
```

The button passes filters:

```text
collector=ruff
run_id=<latest compatible run>
```

### Restrictions

Do not change Wave 2M assessment semantics.

### Gate

Existing Wave 2M validator must remain fully green.

### Freeze

Create a corrective Freeze that explicitly supersedes only the affected integration surface, not the whole Wave 2M contract.

---

## Wave 2U — Patch Preview integration

### Objective

Convert reviewed remediation intents into isolated patch proposals.

### Workflow

```text
Select reviewed remediation intent
→ Generate patch plan
→ Identify frozen impact
→ Build isolated workspace
→ Preview diff
→ Run focused validation
→ Run Validate Project
→ Human confirms installation
```

### Initial mechanical candidates

Only after explicit approval:

```text
single-file BOM removal
single unused import where Ruff marks fix as safe
simple deterministic formatting in an unfrozen file
```

### Required safety

* original file hash captured;
* exact diff preview;
* isolated workspace;
* rollback package;
* frozen-path hard block;
* no global Ruff fix;
* no global formatter;
* targeted validation;
* project validation;
* source patch governance.

### Freeze

Patch Preview must have its own extensive governance Freeze.

---

## Wave 2V — Advanced and optional diagnostics

### Deferred capabilities

```text
probabilistic import reachability
GUI startup reachability
dynamic runtime traces
AI root-cause hypotheses
cross-rule correlation
SARIF export/import
IDE integrations
trend analytics
```

Each should be evaluated independently.

They must not be required for the reliable deterministic core.

---

# 13. Failure isolation

Each collector runs in an isolated process or protected worker boundary.

Possible collector states:

```text
COMPLETE
COMPLETE_WITH_FINDINGS
DEGRADED
INVALID_COVERAGE
MISSING_EVIDENCE
FAILED
CANCELLED
NOT_RUN
```

Rules:

* one collector failure does not abort others;
* completed partial results are retained;
* a partial run cannot become baseline;
* cancellation persists completed collector results;
* malformed output is stored for diagnosis;
* tool-version incompatibility is explicit;
* collector stderr is captured;
* exact exit code is retained.

---

# 14. Performance plan

## Collection

* run independent collectors concurrently when safe;
* limit concurrency to prevent disk saturation;
* allow cooperative cancellation;
* stream collector completion events.

## Persistence

* SQLite WAL mode for temporary run data;
* batched inserts;
* indexes on rule, tool, path, baseline state and issue ID;
* avoid storing large raw payloads repeatedly;
* use references to raw output files.

## GUI

* query only visible pages;
* lazy-load details;
* lazy-load source excerpts;
* debounce filter changes;
* execute queries outside the GUI thread;
* cap log display while preserving full log on disk.

## Incremental analysis

Later optimization:

```text
file content hash
+ collector version
+ ruleset version
+ configuration hash
```

Unchanged compatible files may reuse normalized results where valid.

---

# 15. Validation architecture for Diagnostics itself

Engineering Diagnostics must be treated as a governed analysis product.

Required validation families:

```text
Collector contract tests
Golden output fixtures
Fingerprint stability tests
Baseline transition tests
Schema migration tests
SQLite integrity tests
Collector failure-isolation tests
Cancellation tests
Frozen-path enforcement tests
GUI performance tests
Scope-classification tests
Owner-enrichment tests
Grouping accuracy tests
Decision persistence tests
Remediation-intent safety tests
```

A dedicated validator should eventually produce:

```text
DIAGNOSTIC SCHEMA CONTRACT: PASS
COLLECTOR ISOLATION: PASS
FINGERPRINT STABILITY: PASS
BASELINE TRANSITIONS: PASS
FROZEN PATH ENFORCEMENT: PASS
PERSISTENT STATE OWNERSHIP: PASS
GUI PERFORMANCE BASELINE: PASS
ARCHITECTURE VALIDATION: 0 ISSUES
STATUS: IN_SYNC
```

---

# 16. Minimum viable useful product

The smallest genuinely useful version consists of Waves:

```text
2O-A
2O-B
2O-C
2O-D
```

It provides:

* BOM, Ruff and Architecture collectors;
* structured findings;
* stable issue identities;
* SQLite run storage;
* manual baseline acceptance;
* NEW, EXISTING and RESOLUTION_CANDIDATE states;
* performant sibling GUI;
* filters;
* exact locations;
* source excerpts;
* deterministic rule explanations;
* frozen-path visibility;
* no source mutation.

It explicitly excludes:

* Shadow;
* owner enrichment;
* root-cause grouping;
* remediation advice;
* AI;
* reachability;
* patch generation;
* automatic fixing.

---

# 17. Final implementation order

```text
1. Wave 2N
   Fix and freeze Symbol Atlas active-owner filtering.

2. Wave 2O-A
   Build domain contracts, SQLite storage, fingerprinting and BOM backend.

3. Wave 2O-B
   Build the BOM Diagnostics GUI vertical slice.

4. Wave 2O-C
   Add Ruff and validate high-volume behavior.

5. Wave 2O-D
   Add Architecture Review findings.

6. Wave 2P-A
   Add scope and frozen-path enrichment.

7. Wave 2P-B
   Add owner enrichment from frozen Wave 2N.

8. Wave 2Q-A
   Add deterministic diagnostic grouping.

9. Wave 2Q-B
   Add Shadow and relational grouping.

10. Wave 2R
    Add lifecycle, suppressions and accepted-risk governance.

11. Wave 2S
    Add non-mutating remediation intents and validation plans.

12. Wave 2T
    Add Full Audit drill-through through a corrective governed wave.

13. Wave 2U
    Add isolated Patch Preview and targeted mechanical corrections.

14. Wave 2V
    Consider reachability, AI, SARIF and advanced analysis.
```

---

# 18. Final architecture verdict

The three external reviews validate the central product idea.

The strongest combined decision is:

```text
KEEP:
Sibling Engineering Diagnostics tab
Read-only pipeline
Baseline tracking
Frozen-path enforcement
Deterministic evidence
Human-confirmed decisions

MODIFY:
Split data model
Use SQLite for run data
Use native structured collector output
Use multi-tier fingerprints
Use multidimensional priority
Implement one vertical slice at a time

DEFER:
Reachability
AI remediation
Graph clustering
Automatic fixes
Patch application
Full Audit integration

REMOVE:
Monolithic issue schema
Multiplicative priority score
Generic automatic root-cause clustering
SARIF as internal source of truth
```

The next implementation work should begin with Wave 2N, followed by Wave 2O-A.

No Engineering Diagnostics source should be created before the Wave 2O-A owner map, storage ownership, schema version and exact validation contract are defined.
