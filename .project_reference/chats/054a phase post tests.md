HANDOFF — ML Advisory Signal Integration / Router Logic
Project

Project root: E:\kanda_reasoner

Current workstream: ML integration into the prompt/router logic.

Important status: ML integration is paused, not abandoned. The last safe implemented ML-related patch was only a router-canon / advisory-signal preparation patch. It did not add runtime ML behavior, did not train a model, and did not let ML override governed routing.

What we were trying to do

The goal was to integrate ML into the router/prompt logic as an advisory signal, not as an autonomous decision-maker.

The intended design direction:

ML can help classify routing signals.
ML can suggest advisory confidence, overlap, similarity, or likely prompt groups.
ML must not bypass governed routing.
ML must not override project freeze rules.
ML must not write directly to protected prompt or freeze files.
ML must remain subordinate to deterministic router, prompt governance, and validation gates.
ML output should be explainable and auditable.
If ML disagrees with canonical router logic, canonical router logic wins.
ML should be introduced gradually, behind explicit gates and tests.
User’s conceptual understanding from this chat

We clarified that complete ML integration logic is probably shorter than previous governance phases, because most of the hard governance infrastructure already exists.

The ML work is not expected to be a huge rewrite. It should likely be layered into the existing router flow as a small advisory component:

deterministic router receives task;
canonical routing rules classify task;
ML advisory layer may produce optional suggested signals;
deterministic router checks ML signals against canon;
final routing remains governed, explainable, and testable.

We also discussed that the chance of positive results is reasonable because the previous ML/router tests and experiments were encouraging, but this does not justify skipping governance. Positive tests support continuing carefully, not merging ML directly into authority paths.

We also clarified that discussions with other AI, web, and books were useful for the complete logic flow, not just one isolated part. They informed the overall architecture idea: ML as a bounded advisory signal inside a governed deterministic router.

Patch already created for ML work

Patch created earlier:

ml_adv000_router_canon_v1_patch.zip

Purpose:

Add canonical documentation / router framing for ML Advisory Signal Integration.
Establish ML as advisory-only.
Preserve deterministic router authority.
Avoid runtime ML behavior.
Avoid unsafe direct ML integration.
Keep the project on a governed path.

Important caveat:

That patch exposed weaknesses in ZIP/freeze delivery rules. After that, the session shifted into fixing ZIP delivery, freeze hints, validation runners, stale pending cleanup, freeze-form gates, and terminal cleanup. Those are separate infrastructure problems and should not be confused with the ML feature itself.

ML work intentionally paused

The user explicitly paused ML integration while we fixed the recurring patch delivery and freeze issues.

Do not continue ML implementation until the user asks to resume.

When resuming ML, start from:

existing router canon;
startup prompt pack;
frozen memory context;
ml_adv000_router_canon_v1_patch concept;
current project governance rules;
all newer delivery/freeze guardrails now in place.
What not to do when resuming

Do not jump straight to runtime ML.

Do not add model inference into production router paths immediately.

Do not create automatic ML overrides.

Do not let ML decide required prompts/groups alone.

Do not store ML-derived routing as frozen memory unless it passed validation and freeze workflow.

Do not weaken validation gates.

Do not bypass prompt canon, freeze canon, or release guard.

Do not reopen the terminal-cleanup issue unless the user explicitly asks; it is separate from this ML handoff.

Recommended next ML step

The next safe step should be a small governed patch, probably something like:

ml_adv001_advisory_signal_schema_v1_patch.zip

Suggested scope:

Define a project-local ML advisory signal schema.
Add tests proving advisory signals cannot override deterministic router decisions.
Add examples of advisory signal payloads.
Add a router contract saying ML signal is optional, bounded, and ignored when missing/invalid.
Add validation that ML cannot change:
required prompts/groups,
freeze gates,
protected paths,
patch delivery rules,
startup sync rules.
Keep implementation non-runtime or mock-only at first.

Possible schema fields:

task_text
candidate_route
confidence
suggested_prompt_groups
similarity_matches
risk_flags
advisory_notes
must_not_override
router_final_decision
router_decision_source

Core invariant:

router_final_decision must be produced by deterministic router logic, not by ML.

Suggested implementation sequence

Phase 1 — Advisory schema only
Create schema, docs, and tests. No runtime ML.

Phase 2 — Mock advisory provider
Add a fake/test provider that simulates ML suggestions. Prove router remains deterministic.

Phase 3 — Router intake hook
Allow router to accept advisory signal input, but only as optional metadata.

Phase 4 — Conflict handling
When ML advisory and canonical router disagree, log/report disagreement and follow canon.

Phase 5 — Local evaluation harness
Run controlled tests comparing ML suggestions against existing routing scenarios.

Phase 6 — Optional real ML provider
Only after all gates pass, consider real model-backed advisory generation.

Key phrase to preserve

ML is not the router. ML is an advisory signal consumed by the governed router.

Suggested next prompt to user

“Do you want to resume ML from the safe next step: ml_adv001_advisory_signal_schema_v1, with schema + tests only and no runtime ML yet?”