# ML Advisory Signal Phase 7 Web-and-Book-Informed Advisory Surface Wiring Research Flux v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 7 Web-and-Book-Informed Advisory Surface Wiring Research Flux v1
Feature ID: rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1

## Purpose

This feature supersedes the prior web-only Phase 7 research flux patch. It adds
a wider design audit using both specialized web sources and five specialized books
before any automatic router/app/UI use or visible advisory panel. It converts the
audit into local gates only. It does not activate runtime wiring.

## Five books used in the implementation audit

1. AI Engineering: Building Applications with Foundation Models — Chip Huyen.
   Gain: eval-first development, latency/cost budgeting, foundation-model app boundaries.

2. Designing Large Language Model Applications — Suhas Pai.
   Gain: LLM applications need structured product playbooks, typed interfaces, and careful transition from demo to product.

3. Designing Machine Learning Systems — Chip Huyen.
   Gain: ML systems should be reliable, scalable, maintainable, adaptive, and explicit about data/system boundaries.

4. Reliable Machine Learning — Cathy Chen, Niall Richard Murphy, Kranti Parisa, Todd Underwood, and D. Sculley.
   Gain: SRE-style reliability, monitoring, rollback, and error-budget thinking should exist before production behavior.

5. Human-Centered AI — Ben Shneiderman.
   Gain: safe AI should combine high human control with useful automation and should preserve user mastery, responsibility, and trust.

## Web sources used in the implementation audit

- NIST AI RMF and Generative AI Profile;
- OWASP Top 10 for LLM and GenAI Applications;
- Google People + AI Guidebook;
- Microsoft HAX Guidelines for Human-AI Interaction;
- OpenAI Evals and Guardrails documentation;
- UK NCSC prompt-injection/confusable-deputy guidance;
- Anthropic effective-agent guardrail/evals design notes.

## Real gains accepted into the logic flux

1. Authority separation and final-router invariant.
2. Confusable-deputy privilege denial.
3. Guardrail adjacency before side effects.
4. Structured typed payloads, no free-text route advice.
5. Explicit uncertainty, status, role, and scope labeling.
6. User control, disable/no-op behavior, and non-training feedback.
7. Eval-first gates for code, payload, model, and UI changes.
8. SLO/error-budget and regression-budget requirements for the advisory surface.
9. Monitoring readiness without persistence or privileged reads.
10. Latency, cost, and availability budgets before provider activation.
11. Rollback and kill-switch as first-class boundary requirements.
12. Modular typed interface; no hidden registry or global-state coupling.
13. Threat model for prompt injection, insecure output handling, disclosure, excessive agency, supply-chain, and DoS/cost risks.
14. Route influence limited to a future deterministic re-check request contract, not override.

## Audit decisions

Accepted now: only research-to-logic contract gates.

Deferred or rejected: direct ML route override, runtime Copilot decision authority,
provider-backed runtime adapter activation, free-text route recommendations,
persistent advisory logs, prompt-library reads, router-canon reads, and hidden
router modifications.

## Next safe implementation shape

Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract v1

The next contract may specify automatic use after canonical router selection and
a visible read-only telemetry panel. It must not wire route authority.
