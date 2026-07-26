# ML Advisory and Prompt Intake Boundary Model v1

Phase 1a defines separate systems:

1. Governed Router
   Final authority. Not modified by this patch.

2. ML Advisory Signal
   Emits non-authoritative telemetry flags and canned reason codes only.
   It cannot select routes, load prompts, or register prompts.

3. Governed Prompt Intake Gate
   The only safe door for future new prompts. It handles proposal,
   classification, duplicate checks, boundary review, testing, validation,
   router binding, and freeze.

4. Interactive Manual Prompt Code Resolver
   Lets a human add, remove, replace, or clear a namespaced prompt-code
   hint. The code is a classification hint, not a command.

Boundary flow:

- Router classifies normally.
- Advisory signal may emit flags only.
- Manual code may be attached to the request envelope only as a hint.
- Prompt gaps go to Governed Prompt Intake.
- New prompts are validated and frozen before router binding.
- Final route remains governed.
