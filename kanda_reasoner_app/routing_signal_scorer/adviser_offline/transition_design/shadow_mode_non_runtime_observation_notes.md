# M23 Non Runtime Shadow Observation Implementation v1

M23 is the first implementation milestone after the M18-M22 design-only chain.
It remains deliberately narrow: one pure in-memory helper builds a single
non-runtime shadow observation dictionary from caller-supplied JSON-safe
primitive data.

M23 does not activate shadow mode. M23 does not start Auxiliar/Assistant behavior. M23 does not integrate with the runtime router, load prompts, read or
write files, persist observations, write reports, mutate gold sets, mutate
registries, call providers, use embeddings, promote candidates, or grant router
authority.

The implementation fails closed on unknown input fields, forbidden authority
field names, missing required fields, and non-primitive values. The observation
record is evidence only and always requires separate human review.

The next allowed milestone is M24: Shadow Observation Review Evidence Design v1.
