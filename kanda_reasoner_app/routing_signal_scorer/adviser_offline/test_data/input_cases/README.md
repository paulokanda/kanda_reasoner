# Adviser Seed Case Corpus v1

Feature ID: `routing_signal_scorer_v3_adviser_seed_case_corpus_v1`
Schema version: `3.46-adviser-seed-case-corpus`

M7 introduces seed input cases only. These files are not gold data, not teacher
answers, not candidate outputs, and not runtime router fixtures. They are a
review queue seed for later M8/M9 work.

Rules:

- human_review_status must remain `seed_unreviewed` in M7.
- cases are synthetic seed inputs and advisory expectations only.
- no teacher answer text belongs in this folder.
- no candidate output belongs in this folder.
- no gold-set manifest or reviewed gold cases are created by M7.
- no file in this folder is loaded by runtime router code.
- no scratch reports or registry files are written by M7.

Categories included:

- adversarial_bypass: 8 cases
- ambiguous: 4 cases
- box_boundary: 5 cases
- false_positive: 5 cases
- freeze_workflow: 5 cases
- out_of_scope: 5 cases
- patch_delivery: 5 cases
- prompt_library: 4 cases
- routing_signal_scorer: 5 cases
- startup_delivery: 4 cases
