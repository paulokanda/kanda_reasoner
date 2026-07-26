# Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract v1

## Role

This is a contract-only Phase 7 wiring gate. It translates the frozen
web-and-book-informed research flux into explicit rules for future
automatic router/app/UI use and future visible advisory surfaces.

It does not activate runtime wiring, create an advisory panel, mutate UI,
call providers, execute adapters, persist advisory reports, read privileged
stores, modify router prompt logic, modify final route selection, grant route
authority, or create MLRT-113.

## Accepted source-backed gains now enforced as contract gates

- Final-router authority separation.
- Confusable-deputy privilege denial.
- Guardrails adjacent to any future side-effect boundary.
- Structured typed payloads; no free-text route advice.
- Explicit uncertainty, status, role, and scope labels.
- Disable/no-op behavior and non-training feedback only.
- Eval-first gates for code, payload, model, and UI changes.
- SLO/error-budget and regression-budget requirements.
- Monitoring readiness without persistence or privileged reads.
- Latency, cost, availability, privacy, and fallback budgets before providers.
- Rollback and kill-switch requirements.
- Modular typed interface with no hidden registry/global-state coupling.
- LLM threat model for injection, insecure output, disclosure, agency, supply-chain, and DoS/cost risks.
- Route influence limited to a future deterministic re-check request contract, never override.

## Future automatic use rule

Future implementation may call advisory display logic only after the
canonical router has finalized its route. The route result must be copied
unchanged into any response envelope and must remain final-selection-invisible
to advisory code.

## Future visible panel rule

Any future visible panel must be read-only telemetry with bounded fields,
uncertainty/status/role/scope labels, disable/no-op controls, and non-training
feedback slots. It must not contain route recommendations, prompt rankings,
executable instructions, or free-text route advice.

## Direct route authority

Direct route authority remains blocked. A later separate contract may study a
deterministic re-check request, but not ML route choice or router override.
