# Prompt Intake Boundary

This package defines Phase 1a contracts for future governed prompt intake.

It is a boundary contract only. It does not create prompts, write a prompt
registry, bind the router, or mutate freeze memory.

Prompt Intake is the only safe door for future new prompts. Manual prompt
codes are classification hints only. A prompt code is a reference, not a
command. A code can be added, removed, replaced, or cleared.
