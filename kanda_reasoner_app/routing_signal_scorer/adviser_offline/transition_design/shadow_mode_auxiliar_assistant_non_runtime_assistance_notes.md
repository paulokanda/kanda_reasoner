# M31 - Non Runtime Auxiliar/Assistant Assistance Implementation v1

M31 is the first narrow implementation milestone after the M26-M30 Auxiliar/Assistant design chain.

It adds a pure in-memory helper that accepts only caller-supplied JSON-safe primitive strings matching the M27 Auxiliar/Assistant input contract and returns one non-authoritative assistance record for human review.

M31 does not activate Assistant behavior. M31 does not start Auxiliar behavior. M31 does not activate shadow mode. M31 does not integrate runtime routing. M31 does not compare or select routes. M31 does not select or load prompts. M31 does not read or write files. M31 does not persist records. M31 does not write reports, review queues, registries, gold sets, or freeze entries. M31 does not record human decisions. M31 does not call providers or models. M31 does not use embeddings. M31 does not promote candidates. M31 grants no runtime authority.

The helper fails closed on unknown input fields, forbidden authority fields, missing required fields, blank required fields, non-string values, and unsupported non-authoritative support labels.

Allowed support labels are:

- `boundary_review`
- `evidence_summary`
- `safety_question_generation`
- `missing_information_review`

The output is an in-memory human-review support envelope only. It carries fixed no-effect markers for routing, prompt loading, Assistant activation, persistence, human decision recording, candidate promotion, shadow activation, and runtime authority.

The next allowed milestone is M32: Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1, after M31 validation, freeze, startup freeze-context refresh, and separate human scope review.
