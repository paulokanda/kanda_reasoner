# Reasoner Professional Engineering Governance

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.7
Status: Optional professional engineering governance layer
Use: Load for high-risk Reasoner work.

This layer is subordinate to:
1. Current source files and runtime logs.
2. Active Reasoner governance files.
3. Reasoner startup canon.
4. Daily startup loader.
5. Universal delivery protocol.

Project Reasoner is an evidence-grounded AI developer tool. It must preserve:
- evidence integrity;
- source-truth hierarchy;
- dynamic PROJECT_ROOT;
- GUI-first workflow;
- static/runtime/reader separation;
- schema compatibility;
- retrieval correctness;
- prompt grounding;
- AI bridge reliability;
- traceability;
- controlled evolution.

Before implementation, define:
- user-visible requirement;
- evidence-safety requirement;
- functional requirement;
- non-functional requirement;
- out-of-scope behavior;
- testable validation condition.

If the requirement is not testable, decompose it before coding.

Risk classification:
- LOW: local helper, docstring, isolated test, no runtime effect.
- MEDIUM: bounded GUI rendering, retrieval scoring, project profile metadata.
- HIGH: schema, index loader, prompt contract, AI bridge, threading, persistence.
- CRITICAL: startup, main GUI event loop, global root logic, broad owner refactor.

High-risk and critical tasks require:
- explicit current box;
- blast radius;
- regression guard;
- validation plan;
- user-visible manual validation when relevant;
- one focused bundle per concern.

Evidence-first rule:
Do not let the app silently guess code ownership or architecture.
AI answers must distinguish:
- source truth;
- runtime truth;
- generated evidence;
- declared documentation intent;
- inference;
- uncertainty.

Testing rule:
A bundle that changes retrieval, prompt, schema, runtime trace, or AI bridge
behavior is not validated by py_compile alone. It needs a focused fixture,
ranking check, prompt build check, mocked bridge check, schema compatibility
check, or documented GUI/manual evidence validation.

Delivery rule:
- Deliver final files in one project-relative ZIP.
- Runtime/source bundle manifest goes in _bundle_temp.
- No install script is required.
- No normal delivery depends on a separate backup-script folder.
- Governance-only updates use _project_reference\ACTIVE_PROJECT_ GOVERNANCE.

Configuration management:
Every bundle must record:
- changed box;
- files changed;
- what changed;
- what did not change;
- safety boundaries;
- validation performed;
- user validation commands;
- next safe step.

Final rule:
Do not optimize for quick AI output at the expense of evidence correctness,
architecture integrity, schema safety, or future maintainability.
