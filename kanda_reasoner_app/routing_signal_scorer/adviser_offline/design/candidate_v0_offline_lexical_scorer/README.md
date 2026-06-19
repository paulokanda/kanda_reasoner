# Adviser Candidate v0 Offline Lexical Scorer Design v1

Feature ID: `routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design_v1`

This folder contains **design-only** materials for a future Adviser Candidate v0 offline lexical scorer.

M10 does not implement or run the candidate. It does not create candidate outputs. It does not read the seed gold set at runtime. It does not integrate with the router.

The design records the future allowed boundary for M11:

- deterministic lexical baseline only;
- standard library only;
- pure function over caller-supplied primitive inputs;
- no files, directories, network, providers, embeddings, vectors, source scanning, prompt auto-loading, or runtime route authority;
- output must be guarded by existing Adviser contract, output guard, resource limits, and severity gates before use in any future harness.

This design exists because the next milestone after a reviewed seed gold set is to define a small baseline candidate safely before implementing it.


No router authority is allowed.
