# Routing Signal Scorer v2 Similarity Threshold Policy v1

Feature ID: `routing_signal_scorer_v2_similarity_threshold_policy_v1`

## Purpose

This document freezes the threshold policy for Routing Signal Scorer v2
Similarity Runtime Lite before any stronger machine-learning behavior is
considered.

The policy is design and calibration only. It does not add embeddings, TF-IDF,
vector stores, model training, self-learning, automatic prompt loading, route
override authority, or May proceed now authority.

## Authority boundary

Runtime-lite similarity remains advisory only.

The runtime may surface similar frozen corpus cases, suggested route-family
anchors, recommended hooks, and caution flags. It must not decide the final
route, final required prompts, missing context, or whether the user may proceed.
The KANDA routing canon decides those outcomes.

## Threshold ladder

The frozen threshold ladder is:

1. Noise / hidden floor: score below `0.18`
   - Default runtime-lite calls do not expose corpus matches below this floor.
   - The floor exists to avoid noisy accidental lexical overlap.

2. Visible low similarity: `0.18 <= score < 0.30`
   - A corpus case may appear in `similar_cases` for transparency.
   - It must not promote similarity-derived route families.
   - It must not promote similarity-derived hooks.
   - It must not promote similarity-derived caution flags.

3. Medium similarity: `0.30 <= score < 0.55`
   - A corpus case may contribute advisory route-family anchors.
   - A corpus case may contribute expected hooks or caution flags.
   - The contribution remains advisory and non-authoritative.

4. High similarity: `score >= 0.55`
   - A corpus case may be labelled high similarity.
   - High similarity still does not override the router.
   - High similarity still does not auto-load prompts.
   - High similarity still does not decide May proceed now.

## Promotion policy

Similarity-derived route families, hooks, and caution flags require a score of
at least `0.30`.

Low similarity matches are allowed to be visible, but low similarity must stay
non-promotional. This protects Fast Path and prevents weak lexical overlap from
creating false route pressure.

Rule-based diagnostic and advisory signals remain independent from the
similarity match threshold. Raising `min_similarity` must not mute rule-based
patch, freeze, terminal, validation, or project-root safety hooks.

## Fast Path protection

Fast Path explanation requests can mention words like patch, code, routing, or
validation conceptually. Similarity must not turn those requests into governed
patch work unless the deterministic rules and canon agree.

A low or medium similarity case is never permission to bypass the normal routing
response, missing-context checks, or pre-output contract gates.

## High-risk hook protection

Patch delivery, terminal install output, terminal validation output, freeze hint
sidecars, freeze memory writes, and selected-project-root sensitive changes must
continue to recommend the pre-output contract gate through deterministic signals
or through medium-or-higher similarity anchors.

Similarity must not suppress high-risk hooks that deterministic signals already
recommend.

## Forbidden behavior

This policy does not permit:

- embeddings
- TF-IDF dependency
- vector store
- self-learning
- cross-project memory learning
- automatic prompt loading
- route override
- May proceed now decision
- final required prompts decision
- replacing the routing canon

## Required regression tests

The threshold policy is protected by tests that verify:

- the policy document keeps the numeric threshold ladder explicit;
- runtime `_similarity_level` boundaries match the policy;
- low similarity matches remain visible but non-promotional;
- changing `min_similarity` filters only similarity matches, not deterministic
  rule-based hooks;
- high similarity remains advisory-only;
- forbidden stronger-ML runtime files are absent.

## Do-not-regress rules

- Keep the default similarity visibility floor at `0.18` unless a governed
  threshold-policy update is validated and frozen.
- Keep the similarity promotion floor at `0.30` unless a governed
  threshold-policy update is validated and frozen.
- Keep the high similarity label threshold at `0.55` unless a governed
  threshold-policy update is validated and frozen.
- Do not allow visible low similarity matches to promote route families, hooks,
  or caution flags.
- Do not let similarity override deterministic high-risk hook recommendations.
- Do not expand runtime-lite authority beyond advisory-only behavior.
