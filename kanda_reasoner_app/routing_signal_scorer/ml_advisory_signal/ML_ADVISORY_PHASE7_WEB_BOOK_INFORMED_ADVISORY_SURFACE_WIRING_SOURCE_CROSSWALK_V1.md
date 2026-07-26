# Phase 7 Web-and-Book-Informed Source Crosswalk v1

This crosswalk records source families used to improve the next implementation
logic. It stores principles, not vendor dependencies or provider calls.

## Web guidance to project gates

- NIST AI RMF / GenAI Profile -> risk gates, eval evidence, no hidden authority expansion.
- OWASP LLM Top 10 -> prompt injection, insecure output handling, sensitive disclosure, excessive agency, supply-chain, and DoS/cost gates.
- Google PAIR -> role, uncertainty, user expectation, and trust labels in any future panel.
- Microsoft HAX -> user control, graceful failure, feedback slots, and clear AI behavior.
- OpenAI Evals/Guardrails -> evals for every future wiring step and guardrails near side-effect boundaries.
- UK NCSC -> treat model output as confusable deputy; deny privileges and minimize blast radius.
- Anthropic effective agents -> separate guard checks/evals from core behavior; keep systems simple and bounded.

## Book audit to project gates

- AI Engineering -> provider-backed activation must wait for eval, latency, cost, fallback, and availability budgets.
- Designing Large Language Model Applications -> visible advisory surfaces need typed interfaces and product-grade transition gates.
- Designing Machine Learning Systems -> keep boundaries explicit and modular; avoid hidden global state coupling.
- Reliable Machine Learning -> require SLO/error budget, rollback, monitoring readiness, and regression gates.
- Human-Centered AI -> favor high human control plus useful automation; advisory surface must not reduce user responsibility or router accountability.

## Resulting next-step rule

Automatic use and visible panel can be designed next only as read-only,
bounded, fail-open telemetry after canonical router final selection. Direct
route effect remains blocked.
