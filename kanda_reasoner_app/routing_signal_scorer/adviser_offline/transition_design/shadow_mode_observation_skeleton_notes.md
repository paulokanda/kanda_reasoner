# M21 Shadow Mode Observation Skeleton Design v1

M21 is design-only.

M21 defines the future non-runtime observation skeleton boundary that may be
implemented only after a later gate. It does not implement a callable observation
builder and it does not accept, validate, process, compare, or generate any live
shadow observation data.

The skeleton design depends on the frozen prior bridge milestones:

- M18 shadow-mode boundary design.
- M19 input/output contract design.
- M20 contract validator design.

Future implementation, if separately governed later, must use only
M20-validated caller-supplied JSON-safe primitive input and may return only one
in-memory non-authoritative observation. Future output must not select a route,
load a prompt, approve a freeze, write gold, write a registry, execute a patch,
promote a candidate, activate shadow mode, or start Auxiliar/Assistant behavior.

M21 does not implement observation execution.

The next allowed milestone is M22: Shadow Mode Implementation Gate Design v1.
