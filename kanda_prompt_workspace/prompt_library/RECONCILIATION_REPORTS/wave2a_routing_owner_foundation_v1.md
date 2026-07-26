# Wave 2A Routing Owner Foundation Reconciliation

Feature: prompt-audit-wave2a-routing-owner-foundation-v1

## Decisions

- KPR-01-014 owns request admission and missing-context classification.
- KPR-02-001 retains advisory route-choice output identity.
- KPR-02-002 owns routing-system architecture.
- KPR-02-003 is a true read-only Project overlay selector.
- KPR-02-004 is the human-readable route locator.
- KPR-02-005 resolves historical identities.
- KPR-02-006 is the semantic and ML adoption safety boundary.
- The duplicate root-level routing-system source is a deprecated redirect.
- prompt_router, RG-PILOT-000, and RG-LAB-000 remain transitional until Wave 2B migrates their remaining consumers.

## Non-decisions

This release does not delete the legacy router, phase prompts, application registrations, or validators that still consume them. It creates no new routing engine, prompt registry, context engine, or automatic loader.
