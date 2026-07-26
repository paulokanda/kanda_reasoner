# Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1

Feature ID: rss_ml_adv_phase3_offline_fixture_catalog_contract_v1

## purpose

Create an offline fixture catalog contract after the frozen Phase 2 offline
evaluation harness result review gate.

This phase adds synthetic, caller-supplied-shape, in-memory fixtures that can be
passed into the Phase 2 offline harness. It is still a governed implementation
step, not runtime ML and not router integration, with no runtime integration.

## accepted scope

- Adds `fixture_catalog_contract.py` immutable catalog contracts.
- Adds `offline_fixture_catalog.py` synthetic fixture builder.
- Exports fixture catalog contracts through the ML advisory package boundary.
- Adds documentation and validation tests.
- Uses only standard-library Python and local Phase 1a/Phase 2 contracts.

## hard boundaries

- No real ML.
- No provider calls.
- No embeddings.
- No vector store.
- No persistence or report persistence.
- No prompt loading.
- No prompt registry mutation.
- No prompt library read.
- No freeze-memory read or write.
- No router-canon read.
- No runtime shadow mode.
- No router prompt logic modification.
- No router final selection modification.
- No route authority.
- No advisory rankings.
- No free-text advisory explanations.
- No training, calibration, or model improvement.
- No runtime Pilot or runtime Copilot behavior.
- No MLRT-113.

## catalog policy

The catalog may contain only synthetic fixtures. The fixture IDs, candidate
group IDs, and governed decision strings must not be harvested from real prompt
library assets, real user prompt text, freeze entries, router canon, telemetry,
or provider outputs.

The catalog adds 0 real prompt-selection cases. It exists only to test boundary
behavior for offline evaluation.

## route-invariance rule

Each fixture carries caller-supplied governed decision strings before and after
advisory. The offline harness may compare those strings but must not compute,
select, override, rank, or bind the final route.

## next safe step

Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Result Review Gate v1

The next step must review this catalog as documentation, synthetic contract, and
validation evidence only. It must not treat this phase as reliability,
production-readiness, runtime ML, or route-authority evidence.

## critical boundary error budget

critical boundary error budget zero.
