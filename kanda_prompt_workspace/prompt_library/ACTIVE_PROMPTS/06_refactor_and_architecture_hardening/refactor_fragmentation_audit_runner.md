# Refactor Fragmentation Audit Runner

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
Status: Post-refactor audit runner roadmap
Prompt ID: kanda_refactor_fragmentation_audit_runner
Prompt type: large-module/refactor safety companion
Scope: Design a read-only Task 0 audit runner after large-module splits or source-preserving facades.

## Purpose

Detect helper-shard fragmentation problems after refactors: unresolved names,
missing imports, runtime API leaks, GUI imports in non-GUI helpers, facade binding
gaps, and smoke failures.

## Architecture

The audit runner operates in five phases:

1. Discover helper modules.
2. Build AST-based name-resolution sets.
3. Detect missing imports, runtime trace API gaps, GUI leaks, and split-wrapper binding gaps.
4. Run non-destructive import/headless smoke checks where safe.
5. Generate Markdown and JSON reports.

## Core static sets

For each helper module, compute:

```text
USED: loaded Name/Attribute references
DEFINED: local assignments, imports, definitions, parameters
EXPORTED: facade/sibling public exports when applicable
UNRESOLVED: USED - DEFINED - EXPORTED - BUILTINS
```

## Detection targets

- missing standard imports;
- missing runtime trace API imports;
- Qt symbols in non-GUI helpers;
- wrapper binding gaps;
- missing implementation symbols;
- import smoke failures;
- facade-only helper false positives.

## Safety rules

- Do not modify project source.
- Use `ast.parse` for static analysis.
- Use subprocess for import/headless smoke when necessary.
- Place temp files outside project source.
- Catch per-module exceptions and record them as findings.
- The audit runner itself should exit cleanly unless its own setup fails.

## Report schema

A finding should include:

```text
module
root_facade
unresolved_names
binding_gaps
missing_std_imports
missing_runtime_api
qt_leaks
smoke_import status
smoke_headless status
risk_level
recommended_repair
```

## Critical question before implementation

Clarify whether helper shards are intended to be standalone importable or only
imported through the facade. This changes import-smoke expectations and prevents
false positives.
