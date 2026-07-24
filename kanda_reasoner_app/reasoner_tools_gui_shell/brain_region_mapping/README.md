# Brain Region Mapping Box

Status: active pure mapping box.

This box maps stable brain-region identifiers to stable Kanda Reasoner tab IDs
and analogy text for the future Brain Navigator and Remember Box.

It deliberately contains no GUI behavior. It does not render the brain, does not open tabs, does not import the tab registry, does not import the main window, and does not import PySide6 or QWebEngine.

## Owns

- Brain structure IDs.
- Brain structure display names.
- Target tab IDs.
- Target tab labels.
- Tooltip text.
- Remember Box analogy text.
- Safe fallback behavior for unknown regions.

## Does not own

- Brain rendering.
- Hover/click event bridge.
- Tab switching.
- Tab registry creation.
- Remember Box widget display.
- Other tab internals.

## Public contract

Use only `contract.py` or package-level exports.

Public functions:

- `list_brain_region_targets()`
- `list_brain_region_ids()`
- `is_known_brain_region(region_id)`
- `resolve_brain_region(region_id)`
- `get_brain_region_mapping_summary()`

## Box Architecture rule

Other boxes may ask this box to resolve a `region_id`, but they may not mutate
its private mapping data. Unknown region IDs return a safe fallback target rather
than raising or switching tabs.

## Current shell synchronization

The mapping covers every visible top-level KANDA tab except Brain Navigator
itself. Target labels use the current shell labels, while references to Audit
Project child areas remain explanatory only. Hidden or deprecated standalone
tabs are not navigation targets.

Cross-box synchronization is validated by
`tools/validate_brain_navigator_tab_catalog_sync_v1.py`; the mapping box itself
remains data-only and does not import `tool_specs`.
