# Routing Signal Scorer v3 Precomputed Semantic Evidence Artifact Design v1

Feature ID: `routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1`

## Scope

This is a design/contract-only phase for a future precomputed semantic evidence artifact. It defines what a future generated evidence artifact would have to prove before it could be reviewed, frozen, and displayed as advisory evidence.

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

## Non-goals

This design does not authorize artifact generation.

This design does not authorize artifact writing.

This design does not authorize embedding generation.

This design does not authorize storing embedding values.

This design does not authorize storing vector values.

This design does not authorize vector index generation.

This design does not authorize provider execution.

This design does not authorize evaluation execution.

This design does not authorize threshold changes.

This design does not authorize semantic runtime enablement.

This design does not authorize startup artifact loading.

This design does not authorize runtime artifact loading.

## Required source prerequisites

A future generated artifact must reference frozen source inputs only:

- frozen Metadata Vector Manifest schema and curated manifest records
- active manifest items only
- frozen offline evaluation gold-set schema
- synthetic or curated gold-set cases only
- declared metrics and thresholds before any evaluation run
- source structural hash and schema version

No raw prompt text, raw user-query text, private project text, prompt body text, terminal logs, or freeze-entry text may be copied into the artifact.

## Future artifact shape

A future artifact may contain identifiers, schema versions, source hashes, evidence-record summaries, validation summaries, review status, and no-authority notices.

The artifact must not contain embedding values, vector values, vector index payloads, provider configs, model configs, credentials, router decisions, required prompts, may-proceed decisions, or any prompt-loading instruction.

## Validation gates

Future artifact generation remains blocked unless a separate governed patch supplies:

- schema validation
- source manifest frozen check
- source gold-set frozen check
- no raw text check
- no vector values check
- no authority fields check
- no runtime enablement check
- review-evidence-only check
- freeze required before runtime visibility

The precomputed artifact can only produce review evidence.

It may never enable semantic runtime behavior.

It may never tune thresholds.

It may never decide final route, required prompts, or May proceed now.

## Dependency boundary

This phase adds no external dependency. It remains standard-library-only and must not import or create providers, vector indexes, model loaders, prompt-library readers, freeze-memory writers, or startup hooks.
