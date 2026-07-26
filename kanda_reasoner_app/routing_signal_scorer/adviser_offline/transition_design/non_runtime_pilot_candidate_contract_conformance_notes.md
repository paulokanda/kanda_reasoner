# P9 - Non-Runtime Pilot Candidate Contract Conformance v1

This milestone adds a static contract-conformance declaration for the inert P8
non-runtime Pilot candidate record.

This is a static conformance declaration only.

It is not a live validator. It does not process input, generate output, run a
candidate, compare routes, read gold, read freeze memory, read prompt libraries,
write records, call providers, use embeddings, train from output, run batch
mode, activate field testing, activate Pilot, activate Copilot, or grant route
authority.

## Purpose

P9 declares that a future non-runtime Pilot candidate must preserve the frozen
input/output contract boundary from P2:

- primitive caller-supplied input fields only;
- non-authoritative output field names only;
- fixed no-effect constants;
- `human_review_mandatory = True`;
- `storage_status = "in_memory_only"`;
- no prompt-loading terminology;
- no recommendation, confidence, score, probability, approval, runtime, or
  promotion fields.

## Boundary

P9 remains a transition-design data module. The conformance record is static
metadata only and is not a live conformance checker.

## Activation Gate note

Field-test activation and definitive enablement remain deferred to a later
Activation Gate Box after lab testing and maturity evidence. They are not
implemented by P9.

## Next milestone

The next safe milestone after local validation, freeze, startup context refresh,
and `FREEZE_MEMORY_STATUS: OK` is P10 - Non-Runtime Pilot Candidate Readiness
Gate v1.

Human governance and the real router remain authoritative.
