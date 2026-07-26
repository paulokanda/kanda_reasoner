# P1 - Pilot Boundary Design v1

`pilot_boundary_design.py` defines the immutable design-only boundary for what a future Pilot may become after P0 freeze.

P1 is not Pilot implementation. It does not create projection logic, route comparison, input/output contracts, live validation, prompt loading, runtime integration, persistence, training-data use, batch mode, Copilot behavior, limited shadow runtime, or authority.

## Protected boundary

P1 records that Pilot remains:

- not active;
- not runtime;
- not Copilot;
- not router authority;
- not prompt loader;
- not a state writer;
- not a training-data source;
- not a batch engine;
- not a human decision recorder.

## Future Pilot roles allowed only after later gates

Future Pilot may only be described as a non-authoritative, opt-in, ephemeral, in-memory, human-review support subsystem after later P-series gates allow the exact behavior.

P1 allows only boundary descriptions for possible later roles:

- descriptive projection analysis after contracts, taxonomy, skeleton, and implementation gate are frozen;
- frozen-router/canon reproduction comparison after the reproduction harness and implementation milestones exist;
- boundary-flag explanation for human review after contract design;
- passive in-memory human-review note preparation after evidence-record design.

## Required ordering preserved

- P2 must define contract and validator design before any field use.
- P3 must define divergence taxonomy before implementation.
- P6 must define the implementation gate before any callable projection.
- P8 must prove reproduction before divergence evidence is trusted.

## Next allowed milestone

After P1 validation and freeze, the next safe milestone is:

P2 - Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1.
