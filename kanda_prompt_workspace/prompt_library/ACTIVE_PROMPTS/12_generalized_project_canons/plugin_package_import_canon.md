# Plugin Package Import Canon

Version: 1.0
Status: Active prompt-library candidate
Use: Load when designing user-importable packages, plugin bundles, extension formats, import/export workflows, package validation, or app-specific portable artifacts.


## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


## Generalization Rule

This prompt was generalized from EEG/KANDA project materials. Do not copy EEG-specific nouns, paths, labels, channel names, montage rules, electrode coordinates, or clinical assumptions into KANDA Reasoner unless the current project explicitly needs them. Preserve only the transferable engineering pattern.


## Core Rule

A plugin package is an application-owned portable container with a manifest, payload, optional assets, optional docs, and optional code. The container format must be simple, inspectable, validate-before-install, and project-agnostic.

## Recommended Container Pattern

Use ZIP as the underlying container unless a project-wide decision replaces it. The outside extension may be app-specific, but the inside should remain standard ZIP.

Generic naming pattern:

```text
<name>.<plugin_type>.<app_extension>
```

Examples:

```text
custom_theme.theme.kanda
analysis_template.report.kanda
workflow_gate.validation.kanda
visual_palette.palette.kanda
```

## Internal Structure

Minimum:

```text
manifest.json
payload/
```

Optional:

```text
assets/
docs/
code/
tests/
examples/
```

## Manifest Requirements

The manifest must declare:

- package name;
- plugin type;
- package version;
- schema version;
- target app family;
- compatibility constraints;
- payload files;
- optional assets;
- validation rules;
- permissions requested;
- whether code execution is required;
- checksum or integrity metadata.

## Import Safety

Import must be staged:

1. open package read-only;
2. validate ZIP/container;
3. parse manifest;
4. validate schema;
5. validate payload files;
6. check compatibility;
7. quarantine unsafe or unknown code;
8. preview import plan;
9. apply only after user approval;
10. record import evidence.

## Code Plugin Rule

If a plugin contains executable code, treat it as high-risk. Require explicit permission, sandboxing if possible, dependency scan, and rollback path.

## Freeze Rule

A new plugin type is not frozen until at least one valid package and one invalid package are both tested.
