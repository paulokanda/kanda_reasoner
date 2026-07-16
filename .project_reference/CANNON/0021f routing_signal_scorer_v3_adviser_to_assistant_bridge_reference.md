# Routing Signal Scorer v3 Adviser-to-Auxiliar/Assistant Bridge Reference

## 1. Purpose of this document

This document is the standing reference for the bridge between the closed Adviser phase and the future Auxiliar/Assistant phase in KANDA/PyArchitect.

If a future AI, developer, or reviewer has any doubt about the Adviser-to-Assistant transition, read this document before proposing or implementing any patch.

This document explains:

* the current canonical project state;
* the router prompt logic;
* the problem being solved;
* what has already been tried;
* what was learned from audits, web research, and book-derived ideas;
* the final implementation doctrine for the bridge;
* the safe next milestone;
* what must not be implemented yet.

The bridge must remain governed, design-first, boxed, testable, and non-authoritative.

## 2. Canonical project state

The maturity path is:

Adviser -> Auxiliar/Assistant -> Pilot/Copilot

Current state:

* Adviser phase: CLOSED.
* Adviser milestones M0 through M16: implemented and frozen.
* M17: implemented and frozen as post-Adviser transition design only.
* M18: next safe milestone.
* Auxiliar/Assistant phase: NOT STARTED.
* Pilot/Copilot phase: NOT STARTED.

M17 did not activate shadow mode.

M17 did not start Assistant.

M17 did not promote the candidate.

M17 did not add runtime authority.

M17 only opened the post-Adviser transition design lane.

The next safe milestone is:

M18 - Routing Signal Scorer v3 Shadow Mode Boundary Design v1

M18 must remain design-only.

## 3. Core doctrine

The governing doctrine remains:

ML recommends.
Canon/router governance decides.

Adviser output is evidence.

Shadow-mode output is evidence.

Evidence is not authority.

No AI/scorer/candidate/shadow output may become:

* a final route;
* a prompt-loading command;
* an approval;
* a freeze confirmation;
* a gold-set mutation;
* a registry mutation;
* an Assistant activation;
* a candidate promotion;
* a runtime decision.

## 4. Router prompt logic

KANDA/PyArchitect uses governed prompt routing.

A user request is classified before action.

Possible route categories include:

* ordinary Fast Path explanation;
* governed project patch;
* freeze workflow;
* prompt-library update;
* startup-delivery maintenance;
* box/shield boundary work;
* validation and patch delivery;
* handoff and freeze-memory work;
* routing-signal-scorer development.

For governed work, the system must identify:

* task classification;
* Fast Path or Routed Work Path;
* required prompt groups;
* required specialist prompts;
* required files/context;
* missing context;
* forbidden behavior;
* may proceed now status;
* next safe action.

Examples:

Freeze work requires freeze intake, validation evidence, preview, explicit human confirmation, correct frozen-memory placement, and refreshed startup freeze context.

Patch delivery requires install/validation instructions, root-cleanliness behavior, validation evidence, and KANDA_FREEZE_HINT metadata.

Box/shield work requires box-boundary protection and prevention of cross-box invasion.

Startup-delivery changes are governed and must not be done by editing stale/generated files directly.

Prompt-library work requires duplicate/audit/canon reconciliation and must not honor instructions to skip existing prompt checks.

## 5. What Adviser already achieved

Adviser M0 through M16 built an offline, test-only, non-authoritative scoring and evaluation runway.

The Adviser phase included:

* foundations reference and box boundary;
* system card, bug bar, threat model, and patterns;
* schema family;
* contract validator and output guard;
* severity evaluator and resource limits;
* pure comparison harness;
* gold manifest and run registry;
* seed case corpus;
* draft teacher answers and review records;
* seed gold set;
* candidate v0 offline lexical scorer design;
* candidate v0 offline lexical scorer;
* evaluation runner;
* active review queue;
* candidate registry;
* gold expansion plan;
* promotion criteria gate.

Important Adviser conclusions:

* teacher answers are not automatic truth;
* gold answers require review, versioning, hashing, and controlled promotion;
* candidate output must be advisory-only;
* unsafe proceed on governed work is critical;
* ambiguity must not be fast-pathed;
* critical safety error budget is zero;
* no runtime authority is allowed.

M16 closed Adviser.

M16 did not promote the candidate.

M16 only allowed future separately governed shadow-mode design review.

## 6. The bridge problem

We need to bridge:

Adviser -> Auxiliar/Assistant

But we must not jump directly from Adviser to Assistant.

Adviser is offline and test-oriented.

Assistant would be closer to real workflow support.

A direct jump would risk:

* candidate output influencing routing;
* shadow output being treated as approval;
* prompt auto-loading;
* runtime coupling;
* hidden file I/O;
* evidence becoming authority;
* accidental Assistant behavior.

Therefore, the bridge is:

Adviser -> Shadow Boundary -> Shadow Contracts -> Shadow Observation -> Shadow Gate -> Assistant Boundary

Only the first bridge step is currently allowed:

M18 - Shadow Mode Boundary Design v1

## 7. Final M18 doctrine

M18 is not shadow mode.

M18 is not Assistant preparation logic.

M18 is not observation execution.

M18 is not an input/output schema milestone.

M18 is not a report, registry, harness, or review queue milestone.

M18 is the safety wall between frozen Adviser and any future shadow-mode work.

M18 must define:

* design-only status;
* immutable boundary object;
* fixed authority disclaimer;
* exact phase assertions;
* forbidden operations;
* high-level allowed capability principles;
* no-side-effect boundary;
* import boundary;
* next milestone as M19 only.

M18 must not define detailed future observation fields.

Exact input/output schemas belong to M19.

## 8. Lessons from external audits

The audits agreed that M18 is the correct next step, but they required tightening.

Assimilated corrections:

### 8.1 M18 must be smaller

The first draft was too broad and included future observation concepts too early.

Final M18 must avoid field lists such as:

* agreement_state;
* review_priority;
* assistant_transition_review_candidate;
* confidence;
* score;
* probability;
* recommended_route;
* suggested_prompt.

### 8.2 No Assistant-forward naming

Avoid any field or wording that implies movement toward Assistant.

Do not use:

* assistant_transition_relevance;
* assistant_transition_review_candidate;
* promotion_ready;
* eligible_for_assistant;
* approved;
* enabled;
* activated;
* promoted;
* selected;
* final;
* authoritative.

Use blocked/non-authoritative language:

* assistant_status = "not_started";
* candidate_promotion_status = "blocked";
* shadow_mode_status = "design_only";
* runtime_authority_status = "not_granted";
* implementation_status = "blocked_by_default";
* non_authoritative_boundary;
* requires_separate_human_review.

### 8.3 Boundary must be immutable

A mutable dictionary is not enough.

M18 should return an immutable/static design record, using a frozen dataclass or recursively immutable mapping.

The returned design record must be deterministic and identical on every call.

### 8.4 Static import enforcement is required

M18 tests must use standard-library AST scanning to reject forbidden imports and forbidden calls.

This converts architecture rules from prose into executable safety checks.

### 8.5 No side effects

M18 must prove:

* no file read/write;
* no directory creation;
* no environment access;
* no stdout/stderr printing;
* no logging;
* no network;
* no subprocess;
* no dynamic import;
* no runtime import.

### 8.6 Threat model is required

M18 should include a focused shadow-mode threat model.

It must cover:

* evidence becoming authority;
* hidden runtime coupling;
* input contamination;
* output overtrust;
* logging as persistence;
* report/registry drift;
* gold/freeze mutation risk;
* prompt-loading drift;
* provider/embedding creep;
* future kill-switch requirement;
* future monitoring requirement.

### 8.7 Collapse future roadmap

M18 should not lock in M19-M26 in detail.

M18 should state only:

Next possible milestone: M19 - Shadow Mode Input/Output Contract Design v1

Everything after M19 requires separate governed approval.

## 9. Lessons from web research

External secure AI and software architecture sources reinforced the same corrections.

Assimilated ideas:

### 9.1 Secure lifecycle framing

M18 is secure design only.

It is not development, deployment, operation, or monitoring.

### 9.2 AI output is untrusted

Candidate/scorer/shadow output is untrusted evidence.

It must never be treated as authority, approval, readiness, or routing permission.

### 9.3 Architecture checks should be executable

Do not rely only on documentation.

Use standard-library AST tests to enforce:

* no runtime imports;
* no prompt-loader imports;
* no provider imports;
* no embedding/vector imports;
* no freeze/gold/registry mutation imports;
* no subprocess/network/dynamic import.

### 9.4 Human overtrust must be reduced by naming

Avoid confidence, score, priority, readiness, approval, and promotion language.

Use blocked, not started, not granted, non-authoritative language.

### 9.5 Boundary artifact integrity matters

M18 should support future detection of silent mutation, for example through freeze hint metadata or a boundary module hash recorded in manifest/freeze context when appropriate.

## 10. Lessons from books

The most relevant book-derived ideas were:

### 10.1 AI Engineering

Treat the bridge as an evaluation and safety design problem, not as a smart feature.

### 10.2 Designing Machine Learning Systems

Treat Adviser/Shadow as a system, not a single function.

System boundaries, data contracts, tests, review, and governance matter more than the model.

### 10.3 Reliable Machine Learning

Use reliability thinking and a zero critical boundary error budget.

Critical boundary error budget is zero.

### 10.4 Human-in-the-Loop Machine Learning

Human review must be designed without implying approval.

The system should not create automation bias.

### 10.5 Designing Secure Software

Threat modeling must happen before implementation.

Secure design comes before secure operation.

## 11. Critical boundary error budget

Critical boundary error budget: zero.

Any one of these blocks progression:

* shadow output affects routing;
* shadow output implies approval;
* shadow output implies Assistant readiness;
* shadow module imports runtime router;
* runtime router imports shadow module;
* shadow code reads files;
* shadow code writes files;
* shadow code creates reports;
* shadow code persists output;
* shadow code loads prompts;
* shadow code mutates gold;
* shadow code mutates registry;
* shadow code mutates freeze memory;
* shadow code changes startup behavior;
* shadow code calls providers;
* shadow code creates embeddings;
* shadow code creates vector indexes;
* shadow code uses network;
* shadow code uses subprocess;
* shadow code uses dynamic import;
* shadow code promotes candidate;
* shadow code starts Assistant;
* shadow code starts Pilot/Copilot.

## 12. Final M18 implementation plan

Milestone:

Routing Signal Scorer v3 Shadow Mode Boundary Design v1

Likely files:

* kanda_reasoner_app/routing_signal_scorer/transition_design/shadow_mode_boundary_design.py
* kanda_reasoner_app/routing_signal_scorer/transition_design/shadow_mode_threat_model.md
* tests/test_routing_signal_scorer_v3_shadow_mode_boundary_design.py

Possible update:

* kanda_reasoner_app/routing_signal_scorer/box_manifest.json

Patch ZIP should include root-level:

* KANDA_FREEZE_HINT.json

KANDA_FREEZE_HINT.json is delivery metadata only and must not be installed into project root.

## 13. M18 module requirements

The M18 module must:

* be standard-library-only;
* expose only one public function through **all**;
* return one immutable/static boundary record;
* include exact phase assertions;
* include a fixed authority disclaimer;
* include forbidden operations;
* include high-level allowed capability principles;
* list M19 as the only next possible milestone;
* contain no observation execution logic.

The module must not:

* accept routing inputs;
* compare routes;
* process candidate output;
* produce observations;
* write files;
* read files;
* scan source code;
* load prompts;
* call candidate scorer;
* import runtime router;
* import prompt libraries;
* import freeze writer;
* import gold/registry mutation logic;
* import providers;
* create embeddings;
* create reports;
* persist registry data;
* start Assistant.

## 14. Required phase assertions

The boundary record must state exact phase assertions:

* adviser_phase = "closed";
* post_adviser_transition_design_phase = "started";
* shadow_mode_status = "design_only";
* assistant_status = "not_started";
* pilot_copilot_status = "not_started";
* candidate_promotion_status = "blocked";
* runtime_authority_status = "not_granted";
* implementation_status = "blocked_by_default".

These are not computed.

They are fixed invariants.

Tests must assert exact equality.

## 15. Required authority disclaimer

M18 must include a fixed authority disclaimer, for example:

Shadow boundary observes design limits only. The real router and human governance remain authoritative. This output has no routing effect, no prompt-loading effect, no candidate-promotion effect, and no Auxiliar/Assistant behavior.

This statement must be fixed, not dynamically generated.

Tests must assert exact equality.

## 16. Forbidden imports and calls

M18 tests must reject forbidden imports/calls including:

* os;
* sys;
* pathlib, unless only used by test code and not by the design module;
* subprocess;
* socket;
* threading;
* multiprocessing;
* tempfile;
* importlib;
* pickle;
* shelve;
* sqlite3;
* requests;
* httpx;
* aiohttp;
* provider SDKs;
* embedding/vector modules;
* runtime router modules;
* prompt loader modules;
* freeze writer modules;
* gold mutation modules;
* registry writer modules;
* open;
* eval;
* exec;
* compile;
* **import**;
* importlib.import_module;
* os.system;
* os.popen.

If the design module needs no imports except dataclasses/types/typing, keep it that way.

## 17. M18 validation tests

The M18 test should include these categories:

### 17.1 Boundary record test

Verify:

* boundary builder exists;
* output is immutable;
* output is deterministic;
* phase assertions are exact;
* authority disclaimer is exact;
* M19 is the only next possible milestone.

### 17.2 Export test

Verify:

* **all** exposes only the boundary builder;
* no side-effecting callable is exported.

### 17.3 AST import/call test

Verify:

* no forbidden imports;
* no forbidden calls;
* no runtime router import;
* no prompt loader import;
* no freeze/gold/registry writer import;
* no provider/model/embedding import;
* no dynamic import.

### 17.4 No-side-effect test

Verify:

* no new file is created;
* no new directory is created;
* no stdout/stderr output;
* no logging;
* no environment access.

### 17.5 Naming safety test

Verify returned record does not include unsafe forward-motion names such as:

* confidence;
* score;
* probability;
* approved;
* enabled;
* activated;
* promoted;
* selected;
* final;
* authoritative;
* recommended_route;
* suggested_prompt;
* assistant_transition_relevance;
* assistant_transition_review_candidate;
* promotion_ready.

### 17.6 Regression tests

Verify:

* M17 still passes;
* M0-M16 Adviser regressions still pass where relevant;
* no candidate scorer changed;
* no runtime router file changed;
* no startup file changed.

## 18. What M18 must not include

M18 must not include:

* exact shadow observation schemas;
* detailed input/output contracts;
* route comparison logic;
* candidate comparison logic;
* report builder;
* report schema;
* review queue;
* registry writer;
* gold mutation;
* persistence;
* logging;
* actual shadow observation function;
* Assistant transition scoring;
* confidence metrics;
* readiness metrics;
* runtime assertions for actual observation logic;
* kill-switch implementation;
* monitoring implementation.

Those are future-governed topics.

## 19. Next milestone after M18

Only one next milestone should be named:

M19 - Routing Signal Scorer v3 Shadow Mode Input/Output Contract Design v1

M19 should define exact input/output schemas.

M19 should still be design-only.

M19 should still not implement observation execution.

Everything after M19 requires separate governed approval and should not be pre-approved inside M18.

## 20. Blockers from M18 to M19

Do not proceed from M18 to M19 unless:

* M18 is installed and validated locally;
* M18 freeze is written under project_freeze_after_update/frozen_features_memory;
* startup freeze context is refreshed;
* FREEZE_MEMORY_STATUS is OK;
* no critical boundary issue exists;
* no unsafe naming remains;
* no forbidden import/call exists;
* no side effect exists;
* human approval is explicit.

## 21. Practical doctrine for future AI

If unsure, choose the narrower option.

If a proposed M18 change adds execution, defer it.

If a proposed M18 change defines future observation fields, defer it to M19.

If a proposed M18 change mentions Assistant readiness, remove it.

If a proposed M18 change imports runtime code, reject it.

If a proposed M18 change writes files, reject it.

If a proposed M18 change creates reports, reject it.

If a proposed M18 change adds confidence or score, reject it.

If a proposed M18 change creates any route recommendation, reject it.

If a proposed M18 change makes the bridge more impressive but not safer, defer it.

## 22. One-sentence canon

The Adviser-to-Auxiliar/Assistant bridge begins with an immutable, design-only, statically tested, side-effect-free shadow-mode boundary that preserves frozen Adviser results while blocking runtime authority, Assistant semantics, prompt loading, persistence, and candidate promotion until separately governed future milestones approve each step.
