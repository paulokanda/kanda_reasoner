# FOLDER ASSIMILATION CARD

Folder: `06_refactor_and_architecture_hardening`
Card type: routing metadata
Status: active metadata card

## Purpose

This folder owns bounded structural-risk triage and behavior-preserving
refactor guidance. It does not own feature implementation, patch delivery,
validation evidence, terminal behavior, or freeze writes.

## Core owners

- `KPR-06-005 architecture_hardening_triage_protocol`: classify a verified
  architecture risk, discover the current owner and protection gap, and select
  the smallest justified hardening response.
- `KPR-06-007 large_module_refactor_protocol`: enforce generic module-size,
  cohesion, public-contract, behavior-preservation, dependency-direction, and
  touched-family validation law.

## Draft-only records

- `KPR-06-006 architecture_hardening_triage_template`: optional triage record.
- `KPR-06-008 large_module_refactor_template`: optional refactor planning
  record.

Draft templates are explicit on-request aids. They are not active governing
protocols and do not authorize mutation.

## Existing specialist routes

- `KPR-06-001`: bounded external Planner architecture reasoning.
- `KPR-06-002`: Imported Web AI payload and bundle profile.
- `KPR-06-003`: exact target-specific AST source repair under current evidence.
- `KPR-06-004 safe_refactor_how_to`: user-facing Safe Refactor How To refresher and bounded specialist dispatcher.

## Use when

Use this folder for:

- a verified architecture ownership or protection gap;
- a module above the 500-line hard maximum;
- a requested change that would exceed the hard maximum;
- mixed module responsibilities;
- behavior-preserving decomposition;
- target-specific AST or architecture refactor evidence.

## Companion owners

- Class 03 Brick Wall for implementation authorization;
- Class 04 for Box, shielding, boundary, and state law;
- Class 05 for patch, validation evidence, terminal, and freeze preparation;
- Class 08 or 09 specialists for implementation-quality or risk domains.

## Not responsible for

Do not use this folder as a second owner of:

- source mutation authorization;
- application-specific Planner or Workbench internals;
- patch ZIP construction or installation;
- validation-pass claims;
- Preview, Confirm and Write, or frozen memory.

## Load rule

Load the smallest exact owner required by the verified problem. Do not load a
draft template instead of its governing protocol.

## Wave 6B retired historical prompts

The following identities have no active route and must not be recreated as new
engines:

- `problem_set_roadmap_solver`: its useful owner/dependency/risk/validation
  sequencing fields are already covered by current roadmap and Brick Wall
  records;
- `refactor_fragmentation_audit_runner`: current AST, public-contract,
  architecture, runtime, and module-quality owners cover demonstrated checks;
- `tab1_tab2_audit_taxonomy`: detector categories route through current
  architecture/workflow owners and the KPR-06-005 detector coverage record.

## Wave 6C Web-AI specialist boundary

The three Web-AI prompts remain active routed specialists, not new core folder
owners:

- KPR-06-001 owns planning reasoning only;
- KPR-06-002 owns payload and bundle profile only;
- KPR-06-003 owns exact target-specific AST repair reasoning only.

Current KPR-06-007 remains generic large-module authority. Current Class 05 and
freeze owners remain authoritative for package mechanics, terminal behavior,
validation evidence, Preview, and explicit Confirm and Write.
