# Routing Signal Scorer v3 Shadow Mode Input Output Contract Design Notes

## Scope

This document belongs to M19 - Shadow Mode Input Output Contract Design v1.

M19 is design-only. It defines future non-runtime shadow observation input and
output contract fields. It does not implement validators, observation logic,
report generation, persistence, prompt loading, runtime integration,
Auxiliar/Assistant behavior, or candidate promotion.

## Relationship to M18

M18 froze the immutable shadow-mode boundary. M19 must preserve that boundary.
M19 may define static contract shapes only.

## Input doctrine

Future inputs must be caller-supplied, serialized, JSON-safe primitives. They
must not contain live router objects, prompt objects, file handles, registry
objects, gold mutation objects, freeze writer objects, provider clients,
embedding indexes, callables, modules, or unknown keys.

## Output doctrine

Future outputs must remain in-memory non-authoritative evidence. They must not
be routes, prompt-loading commands, approval records, freeze actions, gold
mutations, registry writes, persistence records, or Auxiliar/Assistant behavior.

## Next milestone

The next allowed milestone is M20 - Shadow Mode Contract Validator Design v1.
M20 is still expected to be design-first and must not implement runtime shadow
mode or Auxiliar/Assistant behavior without separate governance.
