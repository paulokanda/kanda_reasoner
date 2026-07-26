# LAB-5 Frozen Canon Fixture Format + Hash Manifest

Feature ID: `routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1`

This milestone defines the future fixture snapshot format and hash manifest contract for the KANDA ML LAB.

LAB-5 is documentation/governance design only.

LAB-5 does not create actual fixture files, hash manifest data files, corpus cases, schema code, validators, fixture validators, runner logic, scoring engines, metrics engines, candidate harnesses, live detectors, import scanners, write guards, live canon readers, live freeze-memory readers, live prompt-library readers, prompt loading, persistence, provider calls, embeddings, activation, field testing, runtime Pilot, or Copilot behavior.

## Purpose

The LAB must not evaluate candidates against live project memory, live prompt files, live freeze memory, live router canon, or runtime router objects.

LAB-5 defines the static copied fixture snapshot format and the hash manifest doctrine that later fixture, runner, and self-validation milestones must obey.

The goal is to make every future evaluation reproducible, reviewable, and disconnected from live mutable project state.

## Fixture doctrine

A LAB fixture is a frozen copied snapshot.

A LAB fixture is not a live link.

A LAB fixture is not a prompt loader.

A LAB fixture is not a route authority.

A LAB fixture is not a freeze-memory reader.

A LAB fixture is not a router-canon reader.

A LAB fixture cannot mutate canon, prompt library, freeze memory, gold registry, routing registry, startup pack, human review records, activation state, runtime decision logs, or persistent ML decision storage.

Future fixtures must be copied from reviewed source material into an isolated LAB fixture area only after human review in a later governed milestone.

LAB-5 defines the format only. It does not copy source material and does not create fixture files.

## Future fixture record shape

A future frozen canon fixture record must include at minimum:

```text
fixture_id
fixture_version
fixture_schema_version
fixture_kind
fixture_set_version
source_freeze_id
source_feature_id
source_feature_title
source_path
source_snapshot_purpose
source_canon_rule_references
source_content_hash
fixture_content_hash
fixture_hash
hash_algorithm
hash_input_canonicalization
created_at_utc
created_by_process
review_status
reviewed_by_human
human_review_reference
immutability_status
supersedes_fixture_id
superseded_by_fixture_id
allowed_read_scope
forbidden_live_sources
```

These are future record fields only. LAB-5 does not implement a schema module or create JSON fixtures.

## Future fixture kind labels

Future fixture kind labels may include:

```text
router_prompt_logic_snapshot
freeze_memory_summary_snapshot
routing_canon_snapshot
prompt_group_index_snapshot
box_boundary_snapshot
patch_delivery_rule_snapshot
validation_marker_snapshot
roadmap_lock_snapshot
known_failure_regression_snapshot
```

These labels do not create a corpus and do not authorize reading live project files.

## Future hash manifest record shape

A future hash manifest must include at minimum:

```text
manifest_id
manifest_version
manifest_schema_version
fixture_set_version
corpus_version_reference
canon_version_reference
created_at_utc
hash_algorithm
hash_input_canonicalization
fixture_entries
aggregate_manifest_hash
manifest_review_status
reviewed_by_human
human_review_reference
source_freeze_ids
source_feature_ids
allowed_fixture_roots
forbidden_live_roots
```

A manifest is an integrity record for copied fixtures. It is not a live discovery index, not a prompt registry, not a route registry, not a freeze writer, and not a candidate approval record.

LAB-5 does not create a manifest data file.

LAB-5 does not create hash manifest data files.

## Hash algorithm doctrine

Future fixture hashes and manifest hashes must use:

```text
SHA-256
```

The future hash input must declare:

```text
UTF-8 text encoding
line-ending normalization rule
field ordering rule
included fields
excluded volatile fields
```

Volatile local paths, absolute user-machine paths, timestamps not intended for identity, temporary extraction paths, editor metadata, and runtime cache artifacts must not be allowed to silently change fixture identity.

LAB-5 defines this doctrine only. It does not implement hashing code.

## Static fixture read model

Future LAB evaluation may read only copied, reviewed fixture snapshots.

Future LAB evaluation must not read directly from:

```text
kanda_prompt_workspace/prompt_library
kanda_prompt_workspace/first_AI_deliver
project_freeze_after_update/frozen_features_memory
project_freeze_ledger
runtime router modules
prompt loader modules
gold registry writers
activation state
field-test state
runtime decision logs
persistent ML decision storage
provider configuration
embedding/vector stores
```

Any future fixture source reference must be traceability metadata, not a live read path.

A future record with a live source path used as evaluation input must be treated as invalid or critical according to LAB-2 and LAB-3.

## Fixture immutability doctrine

Once a fixture is frozen for a fixture set, it must not be edited in place.

Correction requires a new fixture version.

Supersession requires explicit fields:

```text
supersedes_fixture_id
superseded_by_fixture_id
supersession_reason
supersession_review_status
```

A future candidate run must record the fixture set version and manifest hash it evaluated against.

A candidate result without fixture set version and manifest hash cannot support reliability claims.

## Manifest integrity failure rules

The following future conditions are LAB_INVALID:

```text
fixture_hash_missing
fixture_hash_mismatch
fixture_schema_version_missing
fixture_set_version_missing
fixture_manifest_missing
aggregate_manifest_hash_missing
aggregate_manifest_hash_mismatch
source_freeze_id_missing
canon_version_reference_missing
review_status_missing
review_status_not_approved
hash_algorithm_missing
hash_algorithm_not_sha256
hash_input_canonicalization_missing
fixture_entry_not_listed_in_manifest
manifest_lists_missing_fixture
fixture_mutated_after_review
fixture_path_outside_allowed_fixture_roots
```

LAB_INVALID means the LAB is not in a valid state to evaluate the candidate. It is not a candidate pass and not a candidate failure.

## Critical boundary rules

The following future conditions are critical boundary violations when attempted by fixture or manifest machinery:

```text
live_prompt_library_read_as_fixture
live_freeze_memory_read_as_fixture
live_router_canon_read_as_fixture
runtime_router_object_used_as_fixture
prompt_loader_invoked_for_fixture
provider_call_for_fixture_creation
embedding_call_for_fixture_creation
freeze_memory_mutation
prompt_library_mutation
router_canon_mutation
gold_registry_mutation
startup_pack_mutation
human_approval_record_mutation
activation_state_mutation
field_test_state_mutation
runtime_decision_log_mutation
persistent_ml_decision_storage_mutation
```

Critical boundary violations keep the critical boundary error budget at zero and block reliability claims and ML implementation continuation.

## Traceability requirements

Every future fixture must trace back to reviewed source material using metadata such as:

```text
source_freeze_id
source_feature_id
source_feature_title
source_path
source_canon_rule_references
source_snapshot_purpose
human_review_reference
```

Traceability metadata cannot become an automatic live read instruction.

## Relationship to LAB-4

LAB-4 defined the future field `fixture_hash_reference` in test case records.

LAB-5 defines the future fixture and manifest doctrine that gives `fixture_hash_reference` meaning.

The future test case must reference fixture hashes. It must not embed live prompt library, live freeze memory, or live router objects.

## Relationship to LAB-6

LAB-6 may only begin after LAB-5 is locally validated and frozen with `FREEZE_MEMORY_STATUS: OK`.

LAB-6 may create a deterministic runner skeleton only under a separate governed scope.

Any LAB-6 runner must treat fixtures as static copied inputs and must reject missing or mismatched fixture hashes before candidate scoring.

LAB-5 itself does not create a runner.

## Non-claims

LAB-5 does not prove fixture integrity.

LAB-5 does not create actual fixture files.

LAB-5 does not create hash manifest data files.

LAB-5 does not create a runner.

LAB-5 does not prove LAB self-validation.

LAB-5 does not create fixture data.

LAB-5 does not create a corpus.

LAB-5 does not evaluate a candidate.

LAB-5 does not prove ML router prompt logic reliability.

LAB-5 does not authorize continuing ML implementation.

LAB-5 does not authorize runtime Pilot, Copilot, activation, field testing, route authority, prompt loading, provider calls, embeddings, persistence, training-data use, or batch mode.

## Roadmap lock

```text
LAB-4 frozen
→ LAB-5 Frozen Canon Fixture Format + Hash Manifest design
→ LAB-5 freeze with FREEZE_MEMORY_STATUS OK
→ LAB-6 Deterministic Runner Skeleton only under separate governed scope
→ LAB self-validation before candidate evaluation
→ LAB/test reliability before ML router prompt logic reliability claims
→ ML router prompt logic reliability before continuing ML implementation
```

No generic `next`, `continue`, or `go` request may skip fixture-format freeze, runner self-validation, human review, or zero critical boundary doctrine.
