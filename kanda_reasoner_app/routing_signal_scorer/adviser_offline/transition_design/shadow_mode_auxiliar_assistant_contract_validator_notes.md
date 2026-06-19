# M28 - Auxiliar/Assistant Contract Validator Design v1

M28 is design-only.

It defines static, fail-closed validation-rule boundaries for a possible later
Auxiliar/Assistant contract validator over the M27 input/output contract. It does
does not implement a live validator, does not process inputs, does not generate
outputs, does not transform observations, does not compare or select routes, does
not load prompts, does not persist evidence, does not write reports, does not
write review queues, does not record human decisions, does not mutate gold sets
or registries, does not call providers, does not use embeddings, does not promote
candidates, does not activate shadow mode, and does not start Auxiliar,
Assistant, Pilot, or Copilot behavior.

The future validator, if separately governed, must fail closed on unknown keys,
missing required fields, non-primitive values, live objects, authority fields,
activation/readiness fields, governed-write fields, persistence fields, human
decision recording fields, and candidate-promotion fields.

M28 keeps the Assistant role non-authoritative. Any future assistance output must
remain human-review support only and must have no routing effect, no prompt-
loading effect, no persistence effect, no human-decision effect, no Assistant
activation effect, and no runtime authority.

The next allowed milestone after M28 freeze is M29: Auxiliar/Assistant Assistance
Skeleton Design v1. M29 still requires separate governed validation and freeze.
