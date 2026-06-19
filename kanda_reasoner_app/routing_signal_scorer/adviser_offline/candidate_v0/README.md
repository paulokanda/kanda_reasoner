# Adviser Candidate v0 Offline Lexical Scorer v1

Feature ID: `routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1`
Schema version: `3.52-adviser-candidate-v0-offline-lexical-scorer`

This is the first **implementation** milestone after the M10 design-only boundary.
It remains inside the offline Adviser box and has no runtime router authority.

Allowed behavior:

- standard-library-only lexical classification;
- pure operation over caller-supplied primitive text identifiers;
- contract-shaped candidate answer dictionaries;
- advisory evidence for future offline comparison only;
- validation by the existing M3/M4 guard/resource/severity modules outside the candidate.

Forbidden behavior:

- runtime router integration;
- prompt auto-loading;
- source scanning;
- file input/output from the candidate;
- candidate output persistence;
- scratch writer or registry writer;
- artifact reading, writing, or generation;
- embeddings, vector indexes, providers, models, network calls, or dependency installation;
- router authority or final-route decisions.

The candidate never emits unconditional `YES`, `YES_UNCONDITIONAL`, `PROCEED`, or
`AUTO_PROCEED`. Ambiguous commands such as `continue`, `go`, `ok`, and `next`
return `ABSTAIN` as advisory evidence only.
