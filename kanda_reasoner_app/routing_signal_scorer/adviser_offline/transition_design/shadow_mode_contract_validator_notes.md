# M20 Shadow Mode Contract Validator Design v1

M20 is design-only.

M20 defines future contract validator behavior for the M19 shadow-mode input and
output contracts. It does not implement a callable validator, process live input,
generate output, execute observations, compare routes, load prompts, persist
records, mutate project state, or start Auxiliar/Assistant behavior.

Future validator design rules:

- Future validation must fail closed on unknown input keys.
- Future validation must reject non-JSON-safe primitive data.
- Future validation must reject live router, prompt, file, module, callable,
  registry, freeze-writer, provider, embedding, and vector-index objects.
- Future output validation must block route, prompt-loading, approval, freeze,
  gold, registry, patch-execution, confidence, score, probability, readiness,
  activation, promotion, and Assistant-authority fields.
- Future validated outputs must remain in-memory non-authoritative evidence.
- Future validation cannot grant runtime router authority.

The next allowed milestone is M21: Shadow Mode Observation Skeleton Design v1.
M21 may design a future observation skeleton, but must still avoid observation
execution unless a later governed milestone explicitly allows it.
