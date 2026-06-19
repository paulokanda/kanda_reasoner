# M9 Seed Gold Set Gate

Feature: `routing_signal_scorer_v3_adviser_seed_gold_set_gate_v1`
Schema version: `3.48-adviser-seed-gold-set-gate`

This directory is a safety gate for the planned seed gold set. It intentionally does **not** create gold cases.

Why blocked:

- M8 teacher answers are draft evidence only.
- M8 human review records are pending only.
- No explicit human approval records were supplied for these cases.
- The Teacher answer must not be treated as ground truth until reviewed.

This milestone records that gold promotion is blocked pending explicit human review. It adds no candidate outputs, no candidate scorer, no ML execution, no scratch writer, no registry writer, no runtime behavior, no prompt auto-loading, no artifact IO, no embeddings, no providers, and no router authority.
