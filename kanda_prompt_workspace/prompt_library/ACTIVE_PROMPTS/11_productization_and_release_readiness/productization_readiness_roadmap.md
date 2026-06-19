# Productization Readiness Roadmap

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.0
Status: Strategic product-readiness roadmap
Prompt ID: kanda_productization_readiness_roadmap
Prompt type: professionalization / release readiness protocol
Scope: Move Kanda Reasoner from internal tool toward polished developer product and, later, commercial SaaS/product readiness.

## Honesty rule

Do not promise literal 100% certainty. Interpret "100% professional readiness" as
a release-grade target with defined gates, documentation, tests, packaging, CI,
support workflow, security, and user-facing polish.

## Track A comes first: polished product for other developers

A developer who is not the original author must be able to install, run,
validate, understand, and safely use Kanda Reasoner on a new project without
chat history.

### Gates

1. Stable installation.
2. Single command validation.
3. Warning cleanup phase.
4. Critical API test protection.
5. Public API stabilization.
6. Documentation: README, INSTALL, QUICKSTART, ARCHITECTURE, VALIDATION,
   CONTRIBUTING, TROUBLESHOOTING, RELEASE_NOTES, and GOVERNANCE pointer.
7. UX polish: first-run flow, project root selector, validation buttons, help
   buttons, visible safe baseline, copyable commands, and clear error summaries.
8. Packaging: source distribution, portable ZIP, pip package, or later Windows executable.
9. Example project with expected validation output.
10. Release discipline: semver, changelog, release checklist, checksum.

## Track B comes second: commercial SaaS/product readiness

Do not start serious SaaS before Track A is credible.

Required gates:

1. Product positioning.
2. User journey.
3. Security and privacy: no training on user code unless opt-in, encryption,
   access controls, audit logs, secrets detection, data retention, deletion.
4. Deployment architecture: frontend, API, queue, worker sandbox, storage,
   database, auth, billing, observability.
5. Sandboxed execution for customer code.
6. Billing and licensing.
7. Support model.
8. Reliability metrics.
9. Legal/compliance review including LGPD/GDPR concerns.
10. Enterprise/local/on-prem path.

## Recommended implementation order

1. Stabilize current local product.
2. Low-risk warning cleanup.
3. Test protection.
4. Developer documentation.
5. Packaging and release.
6. Product UX polish.
7. SaaS feasibility prototype.
8. Commercial launch readiness.

## Non-negotiable baseline

Every professionalization change still follows Kanda Bundle-Gated Development:

```text
Task 0 audit -> Task 1 roadmap -> Task 2 implementation runner -> dry run -> apply -> rollback on failure -> Tab 1 validation -> Tab 2 validation -> freeze only if clean
```

Do not add product features while Tab 1 Errors or Tab 2 failures are unresolved.

---

## Professional workflow infrastructure productization update

### Professional infrastructure required before product readiness

Before Kanda Reasoner can be considered a polished developer product, the
engineering workflow itself must be productized.

Required infrastructure modules:

1. Evidence Freshness Gate with hash and timestamp checks.
2. Patch Registry with created, installed, validated, frozen, failed, restored,
   and abandoned states.
3. Unified Validation Runner with raw log plus structured JSON result sidecar.
4. GUI Smoke Checklist System for visual/manual validation.
5. Freeze Governance Workflow with explicit user freeze.
6. Git Checkpoint Gate for recommended pre-patch checkpoints.
7. Patch Install Manifest Indexer for backup/install discovery.
8. Failure Triage Classifier.
9. Prompt and Protocol Enforcement through Tab 9 routing.
10. End-of-Session Handoff Generator.
11. State-Based Testing Sandbox for persistent-state-sensitive patches.
12. Human Override Log for rare, justified gate overrides.

Productization gates should include:

```text
fresh evidence
patch state known
validation result saved
manual GUI checklist recorded when visual
no unresolved workflow failure
no unresolved architecture failure
no hidden terminal-log clearing
no freeze without explicit human command
```

Track A product readiness must come before SaaS readiness. A SaaS or public
product should not start until the local product has a stable installation path,
single-command validation, documentation, clean release packaging, test
protection, and visible validation state.
