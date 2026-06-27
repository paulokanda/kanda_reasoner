# Routing Signal Scorer v3 Adviser System Card Bug Bar Threat Model Design v1

Feature ID: `routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design_v1`

Schema version: `3.40-adviser-system-card-bug-bar-threat-model-design`

Status: design-only, standard-library-only governance reference. No candidate scorer, no machine-learning execution, no runtime router integration, no prompt auto-loading, no artifact I/O, no embeddings, no providers, and no router authority are introduced by this milestone.


## Purpose

This threat model records the highest-risk ways a future Adviser could degrade prompt-router safety.

## Assets to protect

- deterministic prompt-router authority;
- freeze confirmation gate;
- project-specific frozen memory under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory;
- box boundaries;
- startup delivery behavior;
- prompt-library audit and duplicate checks;
- human decision recording boundaries;
- generator-candidate boundaries;
- no-runtime-import boundary for adviser_offline.

## Trust boundaries

No AI output is a security boundary.

No teacher answer is ground truth until reviewed and frozen.

No candidate output is authority.

No scratch report is source-of-truth.

Runtime router code must not import adviser_offline.

adviser_offline must not import runtime router code.

## Main threats

### Teacher contamination

A wrong teacher answer could become false gold. Mitigation: draft-only teacher answers, human review, teacher version, input hash, supersedes record, append-only gold.

### Gold-set poisoning

A careless or malicious record could train the system toward unsafe behavior. Mitigation: reviewed gold, manifest hashes, provenance, no automatic gold promotion.

### Schema drift

Old cases could be silently misread after schema changes. Mitigation: schema_version on all records and strict contract validation in a later milestone.

### Lexical negation failure

A future weak scorer may misread "do not freeze" as a freeze command. Mitigation: negative pattern tests, ABSTAIN/NO default, red-path cases.

### Bypass attempt

User text may request skipping confirmation or anti-audit checks. Mitigation: bypass flags, critical severity, output guard.

### Authority promotion

User text may say "you decide routing from now on." Mitigation: authority flags, critical severity, no router authority.

### Candidate output mistaken as authority

A scratch or report file could be consumed by runtime code. Mitigation: scratch-only outputs, no runtime imports, no public export.

### Resource exhaustion

Long, malformed, nested, or adversarial input could hang a future scorer. Mitigation: future resource_limits module, max input size, no threads, no recursion, no network.

### Cross-box leakage

Adviser could read or recommend changes outside its box. Mitigation: box boundary, no source scanning, primitive input only in future candidate.

## Current milestone guarantees

This milestone adds only design documents and manifest declarations. It does not create scorer code, harness code, contracts, test_data, gold, registry, or scratch implementation folders.

## Future required mitigations

Before candidate trust, implement:

- schema family;
- contract validator;
- output guard;
- severity-as-code;
- resource limits;
- pure comparison harness;
- reviewed seed gold set;
- active review queue;
- promotion gate.
