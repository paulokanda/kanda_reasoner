# Wave 2B Legacy Routing Retirement Reconciliation

Feature: prompt-audit-wave2b-legacy-routing-retirement-v1

## Final lifecycle decisions

- `prompt_router` and `kanda_prompt_router`: deprecated compatibility identities with no active route.
- RG-PILOT-000: retired historical P0 phase-entry identity with no active route.
- RG-LAB-000: retired historical LAB phase-entry identity with no active route.
- Historical source files are retained as compact provenance records; they are not active semantic owners.

## Consumer migration

- Current route selection uses KPR-01-014, KPR-02-002, KPR-02-004, and KPR-02-006.
- Historical names resolve through KPR-02-005.
- Prompt metadata, active groups, machine routes, human indexes, coverage tables, application Prompt Library registrations, startup ZIP requirements, terminal validators, large-module validators, and patch-recovery validators no longer depend on prompt_router as a specialist owner.

## Non-expansion decision

No routing engine, registry, context service, ML layer, or coordination super-system was created. The change removes duplicate authority and preserves current owners.
