# Routing Signal Scorer v3 Adviser Offline Box Boundary

Feature ID: routing_signal_scorer_v3_adviser_foundations_reference_and_box_boundary_design_v1
Schema version: 3.39-adviser-foundations-reference-and-box-boundary-design
Status: design-only box boundary, no candidate scorer, no runtime behavior change.

## 1. Box placement

The Adviser foundations belong under the Routing Signal Scorer box.

Preferred future root:

```text
kanda_reasoner_app/routing_signal_scorer/adviser_offline/
```

This is a sub-box for offline Adviser evaluation foundations.

It is not a runtime router module.

## 2. Authority boundary

The Adviser offline sub-box may eventually produce advisory evidence.

It must never produce final routing authority.

It must never decide:

- final route;
- May proceed now;
- required prompts as binding authority;
- prompt auto-loading;
- freeze write approval;
- box-boundary override;
- runtime semantic scoring;
- startup behavior.

## 3. Import boundary

Runtime router code must not import adviser_offline.

adviser_offline must not import runtime router code.

The future offline Adviser may accept primitive strings or serialized case dictionaries only.

It must not accept live runtime objects, file handles, router state, GUI state, freeze-engine state, prompt-library objects, or startup state.

## 4. File ownership boundary

This milestone may add only design documents under:

```text
kanda_reasoner_app/routing_signal_scorer/adviser_offline/design/
```

and a validation test under:

```text
tests/
```

It may update the Routing Signal Scorer box manifest with design-only markers.

It must not create candidate, core, harness, contracts, test_data, gold, registry, or scratch implementation folders yet.

## 5. Forbidden neighboring boxes

This milestone must not touch:

- prompt-library source of truth;
- startup delivery logic;
- freeze engine logic;
- freeze memory writer logic;
- project freeze ledger logic;
- GUI tabs;
- runtime router contract;
- public prompt-loading behavior;
- provider or dependency configuration;
- source scanning logic.

## 6. Forbidden runtime effects

This milestone adds no:

- candidate scorer;
- ML execution;
- embeddings;
- vectors;
- providers;
- artifacts;
- source scanning;
- report writer;
- gold-set writer;
- prompt loader;
- router integration;
- startup hook;
- background process;
- file watcher;
- runtime semantic signal;
- public runtime export.

## 7. Future allowed evolution

Future governed milestones may add, in order:

1. system card, bug bar, threat model, and pattern library;
2. schema family;
3. contract validator and output guard;
4. severity evaluator and resource limits;
5. pure comparison harness;
6. gold manifest and run registry;
7. seed case corpus;
8. reviewed gold set;
9. candidate v0 design;
10. candidate v0 offline scorer.

Each future step requires its own patch, validation, and freeze.

## 8. Current effect statement

This patch is reference-only and boundary-only.

No candidate exists yet.

No Adviser output exists yet.

No router behavior changes.

No prompt-routing authority changes.

No runtime contract changes.

No public export changes.
