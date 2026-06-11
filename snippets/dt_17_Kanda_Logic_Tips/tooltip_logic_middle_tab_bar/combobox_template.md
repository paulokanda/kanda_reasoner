# combobox_template — Middle Tab Comboboxes & Tooltip Systems

## Purpose in the architecture
`combobox_template.py` is the glue layer for the **middle tab** filter lane:
it builds Core/Pro **button‑system menus**,
renders a **scrollable combobox lane**,
loads tooltip metadata from JSON,
and exposes the right hook points to attach the two tooltip systems you use.

Simple tooltips live on the **button system** (Core/Pro menus and actions).
Gorgeous hover‑card tooltips attach **directly to each combobox header** in the lane.

---

## Where the two tooltip systems plug in

### 1) Simple tooltips — Core/Pro button system (menus & actions)
When the template rebuilds menus:
- `_rebuild_core_menus_helper(...)`
- `_rebuild_core_caret_menu_helper(...)`
- `_rebuild_pro_menus_helper(...)`
- `_rebuild_pro_caret_menu_helper(...)`

this is your place to set **lightweight Qt tips** on each `QAction`, e.g.:
```python
for action in core_menu.actions():
    label = action.text()
    tipcfg = self._label_to_tipcfg.get(label, {})
    simple_tip = (tipcfg.get("tooltip") or {}).get("description")
    if simple_tip:
        action.setToolTip(simple_tip)
```
These tips show **before the lane renders** and should be concise and instant (no animations).

Data source
- The template keeps a `self._label_to_tipcfg` mapping (populated by the option‑loading helpers).
- During header changes you can rebuild menus (already done here) and keep tips in sync.

### 2) Gorgeous hover‑card tooltips — per combobox in the lane
When the lane is rebuilt by `update_dropdowns()` → `_update_dropdowns_impl(self)`,
each `KandaDropdown` widget is created.
Right there (or in `_after_dropdowns_rebuilt`), attach your **hover‑card**:
```python
# After creating each dropdown 'dd' with logical key 'key' and human label 'label'
params = self._params_map.get(key, {})
tipcfg = params.get("tooltip", {})
if tipcfg:
    NeuroTooltipManager.apply_tooltip(dd, tipcfg)   # rich, animated hover-card
```
The template keeps `_params_map: key -> {label, tooltip}` built by `_rebuild_params_map()` so you can fetch the right payload per dropdown.

Lifecycle considerations
- On lane rebuilds, attached hover‑cards must be **stopped/hidden/deleted** before the widgets are removed.
- The template delegates teardown to the lane‑clearing helper (called via `_clear_dropdown_lane_helper(self)`),
  so store your guard/controller on the widget (e.g., `_hover_tip_guard`, `_hover_tip_adapter`) for symmetric cleanup.

---

## How tooltip metadata flows from JSON to UI

1) **Option loading** (JSON)  
The template calls the option‑loading helpers, which among other things harvest **per‑label tooltip configs** and store them in `self._label_to_tipcfg`.

2) **Key/label map**  
After building visible dropdowns, `_rebuild_key_index()` ensures the template can find widgets by logical key.

3) **Params map**  
`_rebuild_params_map()` consolidates the data into:
```python
self._params_map[key] = {
    "label": label,
    "tooltip": tipcfg.get("tooltip", {})
}
```
Use this in both systems:
- **Simple tips**: show `tooltip.description` on `QAction`s.
- **Gorgeous cards**: pass the whole dict to `NeuroTooltipManager.apply_tooltip(...)` so the card can render title/body/links/shortcuts.

---

## Header changes and tooltip refresh
`headerFilterSetChanged` is emitted when “Core Filters” ↔ “Pro Filters” changes.
Wire a slot to **refresh visible hover‑cards** in place:
```python
def _update_tooltips_for_header(self, header_name: str) -> None:
    # look up the active map for that header and re-apply cards to the visible dropdowns
    for key, dd in self.dropdowns_by_key.items():
        tipcfg = self._params_map.get(key, {}).get("tooltip")
        if tipcfg:
            NeuroTooltipManager.apply_tooltip(dd, tipcfg)
```

---

## Optional: header‑area hover‑cards
`_attach_hover_to_headers()` shows how to define **example** tip payloads for the header areas themselves (Core/Pro).
If you prefer **simple** native tips on the header buttons, keep hover‑cards off and just set `setToolTip(...)` on the button widgets.

---

## Minimal checklist

Simple tips (menus/actions)
- Build/rebuild menus (already done by the template).
- For each `QAction`, set `action.setToolTip(...)` using `self._label_to_tipcfg[label]`.

Gorgeous hover‑cards (combobox headers)
- After each dropdown is created, call `NeuroTooltipManager.apply_tooltip(dd, tipcfg)` using `self._params_map[key]["tooltip"]`.
- Ensure your lane‑clear routine tears them down (store guard/controller on the widget).

Header flip Core↔Pro
- On `headerFilterSetChanged`, call `_update_tooltips_for_header(...)` to refresh visible cards.

---

## Example JSON snippet (backward‑compatible)
```json
{
  "label": "Low-cut",
  "items": ["filter.lowcut.hz"],
  "tooltip": {
    "title": "Low-cut",
    "description": "High‑pass cutoff frequency (Hz).",
    "shortcuts": ["↑/↓ to change", "Enter to apply"]
  }
}
```
This gives the simple tip text for the menu action (`description`) and a richer payload for the hover‑card on the dropdown itself.

---

## Hotspots you’ll likely touch
- Menu rebuild helpers: add `QAction.setToolTip(...)` at creation time.
- Lane rebuild helper: after each `KandaDropdown` is instantiated, call the hover‑card manager.
- `_rebuild_params_map()`: ensures `{key → tooltip}` is always in sync with the current header and visible lane.


