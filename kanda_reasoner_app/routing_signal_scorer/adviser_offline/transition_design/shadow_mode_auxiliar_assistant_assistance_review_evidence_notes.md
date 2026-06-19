# M32 - Auxiliar/Assistant Assistance Review Evidence Design v1

M32 defines the immutable design-only review-evidence envelope for possible later
human review of M31 non-runtime Auxiliar/Assistant assistance records.

This milestone is intentionally not a live review-evidence builder. It does not
transform assistance records, validate live payloads, write files, persist
records, write reports, write queues, record human decisions, select routes,
select or load prompts, activate Assistant behavior, activate shadow mode,
integrate runtime routing, call providers, use embeddings, mutate gold or
registry state, promote candidates, or grant runtime authority.

Allowed source records for a future builder are limited to the M31 in-memory
non-runtime assistance dictionary shape. Future review evidence remains
non-authoritative human-review support only and must preserve explicit `none`
effects for routing, prompt loading, Assistant activation, persistence, human
decision, candidate promotion, and runtime authority.

M33 requires a separate governed scope confirmation, validation, and freeze.
