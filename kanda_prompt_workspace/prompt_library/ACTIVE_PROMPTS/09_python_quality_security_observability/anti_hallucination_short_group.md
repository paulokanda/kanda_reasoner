---
prompt_id: anti_hallucination_short_group
prompt_code: KPR-09-002
title: Evidence Verification Train - Short
version: 2.0.0
status: active
load_type: routed
owner_box: 09_python_quality_security_observability
classification: evidence_verification_group_router
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Evidence Verification Train - Short

## Purpose

Route one sealed operation through the compact evidence-verification train.
This group is an orchestrator, not a substitute for the stage prompts.

## Admission

Use this group when routine governed work needs a bounded evidence review and no full-train admission factor is present. Record the operation ID, plan or artifact hash,
current source fingerprints, risk class, privacy constraints, and required
truthful outcome before starting.

## Stage sequence

1. `KPR-09-007`
2. `KPR-09-008 when current external facts matter`
3. `KPR-09-009 when verified literature matters`
4. `KPR-09-010`

Each stage receives the same operation identity plus the previous stage record
hash. A blocked or critical stage stops the train unless the record explicitly
states why a later read-only stage remains useful.

## Routing rules

- Agreement between AIs is not proof.
- Search for disconfirming evidence.
- Literature is conditional and requires inspected-source provenance.
- Skip an inapplicable stage with a reason instead of fabricating output.
- Escalate from the short group to the full group when risk or uncertainty rises.
- The final synthesis reports status; it does not authorize implementation.

## Required group record

Return stage versions, input/output hashes, skipped or blocked stages, conflicts,
limitations, final truthful status, and the exact next evidence owner.

## Version history

- 2.0.0: added risk admission, operation identity, stage handoffs, stop
  conditions, and version compatibility.
