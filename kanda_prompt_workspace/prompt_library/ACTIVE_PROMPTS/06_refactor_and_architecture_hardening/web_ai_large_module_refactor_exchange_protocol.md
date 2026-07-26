# Web AI Large Module Refactor Exchange Protocol

Prompt code: `KPR-06-001`
Prompt id: `web_ai_large_module_refactor_exchange_protocol`
Version: 2.0.0
Status: `active`
Load type: `routed`
Owner box: `06_refactor_and_architecture_hardening`

## Purpose

Use this protocol when a current Large File Refactor Planner package is sent to
an external Web AI for bounded architecture review. The purpose is not to redo
the whole refactor from scratch. The purpose is to compare the native plan with
the exact source and deterministic evidence, then return the smallest defensible
planning correction.

This prompt owns external planning reasoning and bounded action selection only.
It does not own source implementation, installer mechanics, validation
infrastructure, terminal behavior, freeze writes, or Error Memory writes.

## Distinct ownership

- `KPR-06-001` owns bounded external architecture reasoning for an existing
  Planner plan.
- `KPR-06-002` owns the reusable Imported Web AI planning-response bundle
  profile and exact payload identity rules.
- `KPR-06-003` owns exact target-specific source repair after AST Split Audit
  evidence.
- `KPR-06-007` owns the current generic large-module and cohesion law.
- current Class 05 owners govern patch construction, Install, Validate,
  terminal completion, evidence preparation, and freeze handoff.

Do not duplicate those authorities here.

## When to use

Use when the supplied package contains:

```text
KANDA_COMPREHENSIVE_PLANNING_PACKAGE
source_content_hash
base_plan_hash
source_code
analysis
current_plan
architecture_review
known_helper_modules
known_movable_symbols
improvement_objective
imported_web_ai_version_install_contract
```

Typical user triggers include:

- `Copy Comprehensive Planning for Web AI`;
- `AI Refactor Version How To`;
- `Imported Web AI Version`;
- `Receive Planning from Web AI`;
- a request to improve a native Planner split without implementing it.

## When not to use

Do not use this protocol to:

- edit selected-project source;
- create arbitrary helpers or public API changes;
- repair target-specific AST blockers;
- replace the native Planner or Workbench;
- weaken module-size, cohesion, dependency, or public-contract gates;
- invent install, validation, terminal, or freeze governance;
- write canonical frozen memory directly.

## Required identity checks

Fail closed unless all are present and exact:

```text
source_content_hash
base_plan_hash
current_plan
known_helper_modules
known_movable_symbols
allowed bounded action schema
```

Treat source and base-plan hashes as immutable exchange identity. Never guess or
recompute them from an incomplete excerpt.

## Architecture reasoning workflow

Use this order:

1. Read the complete source, deterministic analysis, and current native plan.
2. Separate hard blockers, warnings, and optional improvements.
3. Answer every supplied `architecture_review` question.
4. Compare the current plan with the smallest plausible bounded alternatives.
5. Preserve public-facade ownership, atomic clusters, decorators, annotations,
   public import paths, and one-way dependency direction.
6. Apply the current supplied module-size policy. When no workflow-specific
   policy is supplied, defer to KPR-06-007: 400 lines or fewer is ideal, 500 is
   the hard maximum, and there is no universal minimum.
7. Prefer truthful no-change output when no bounded improvement is supported.
8. Return only actions permitted by the supplied schema.
9. Hand exact payload packaging to KPR-06-002 and current Class 05 owners.

## Allowed bounded actions

Use only action lists explicitly allowed by the supplied Planner contract:

```text
module_merges
reassignments
module_renames
docstring_updates
```

Constraints:

- merge only known helpers into known helpers;
- reassign only known movable symbols to known helpers;
- rename only surviving known private helper modules;
- update only supplied docstring proposal targets;
- preserve public-facade-owned symbols and atomic clusters;
- do not create dependency cycles or helper-to-facade back references;
- do not add a new action kind.

## Required planning response

Return exactly one marker-wrapped JSON payload:

```text
KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN
{
  "schema_version": "2.0",
  "exchange_feature_id": "large-file-refactor-planner-web-ai-exchange-v2",
  "source_content_hash": "<exact supplied hash>",
  "base_plan_hash": "<exact supplied hash>",
  "verdict": "valid_or_refine",
  "module_merges": [],
  "reassignments": [],
  "module_renames": [],
  "docstring_updates": [],
  "architecture_answers": {
    "tiny_helpers": "<evidence-backed answer>",
    "module_count": "<evidence-backed answer>",
    "cohesion": "<evidence-backed answer>",
    "dependency_safety": "<evidence-backed answer>",
    "atomic_clusters": "<evidence-backed answer>",
    "semantic_names": "<evidence-backed answer>",
    "public_facade": "<evidence-backed answer>",
    "final_gate": "<evidence-backed answer>"
  },
  "analysis_observations": [],
  "rationale": "<bounded evidence-backed rationale>",
  "warnings": []
}
KANDA_WEB_AI_PLANNING_RESPONSE_END
```

There must be exactly one begin marker and exactly one end marker.

## Bundle handoff

Load `KPR-06-002 web_ai_planning_response_bundle_blueprint` when a governed ZIP
or Panel 4 fallback is requested. The payload packaged in
`pending_imported_web_ai_plan.txt` and the payload printed in chat must be byte
identical.

The bundle profile may include `INSTALL.ps1`, `VALIDATE.ps1`, `FREEZE.ps1`,
`KANDA_FREEZE_HINT.json`, and `bundle_manifest.json`, but their mechanics remain
subject to current Class 05 and freeze contracts. This protocol does not author
those governance rules.

## Planner receive and review

After current delivery validation:

1. load the installed pending plan as `Imported Web AI Version`, or paste the
   exact marker-wrapped payload into `Panel 4: Proposed split plan`;
2. verify source and base-plan identity;
3. compare the imported plan with the native plan;
4. keep implementation blocked until current Brick Wall and Workbench gates
   authorize the next phase.

## Required output to the human

Return:

1. concise architecture diagnosis;
2. exact bounded action result;
3. exact marker-wrapped planning payload;
4. when requested, the KPR-06-002 bundle artifact;
5. current Class 05 Install and Validate instructions;
6. freeze-evidence preparation only after validation passes.

## Freeze boundary

Imported-plan evidence may be prepared after local validation. Preview remains
read-only. Final frozen-memory writing requires explicit human
`Preview Freeze Entry` followed by `Confirm and Write`.

## Do not regress

- Keep planning actions bounded to known modules, symbols, renames, and
  docstring targets.
- Keep source and base-plan hashes exact.
- Keep the import installer outside KANDA source and selected-project source.
- Keep KPR-06-002 as the bundle profile rather than duplicating it here.
- Keep implementation, terminal, evidence, and freeze authority delegated.
