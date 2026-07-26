---
prompt_id: anti_hallucination_protocol_short
prompt_code: KPR-09-010
title: Evidence Synthesis Protocol - Short
version: 2.0.0
status: active
load_type: on_request
owner_box: 09_python_quality_security_observability
classification: derived_short_profile
derived_from: KPR-09-006
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Evidence Synthesis Protocol - Short

## Purpose

Provide a compact profile for routine evidence synthesis. This file is derived from `KPR-09-006`
and does not own an independent canon.

## Binding rule

- The parent prompt owns semantics and version history.
- This short profile may omit detail but must not contradict the parent.
- Escalate to `KPR-09-006` when risk, uncertainty, conflict, or scope exceeds a
  bounded routine review.
- Do not force a finding count.
- Do not authorize source mutation or claim unexecuted validation.

## Compact procedure

1. Record operation identity and current evidence freshness.
2. Separate facts from assumptions and unsupported claims.
3. Apply the parent prompt's core safety and provenance rules.
4. Search for disconfirming or conflicting evidence where applicable.
5. Return: inputs, conflicts, truthful status, escalation decision.
6. State `ESCALATE_TO_KPR-09-006` when the compact profile is insufficient.

## Version history

- 2.0.0: converted to a version-bound derived profile with explicit escalation.
