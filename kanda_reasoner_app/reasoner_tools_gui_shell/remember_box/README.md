# Remember Box

Status: scaffold only.

The Remember Box is the future explanation-card display used by the Brain
Navigator first tab. In this patch it is a display-state contract only: it does
not render widgets, does not add a tab, and does not change the visible GUI.

## Owns

- Placeholder Remember Box display state.
- Display state built from a brain-region target-like object.
- Safe unmapped display state when a target is unknown.
- Box Architecture metadata for this display box.

## Does not own

- It does not render the brain.
- It does not open tabs.
- It does not import PySide6.
- It does not import MainWindow.
- It does not import the Tab Navigation Controller Box.
- It does not own Brain Region Mapping logic.
- It does not own registry metadata.

## Future wiring

A later GUI patch may convert `RememberBoxState` into a visible card widget.
That future widget should receive state through this public contract and should
request tab opening through the Tab Navigation Controller Box, not directly from
this Remember Box.
