# widgets_cmbbx_template_helper — Middle‑Tab Combobox & Tooltip Readiness

> Two tooltip styles in your middle tab:
> 1) **Simple native tips** — short Qt bubbles for **Core/Pro menu actions** (button system).
> 2) **Gorgeous hover‑cards** — rich, animated tooltips attached **directly to each combobox header** in the lane.

This helper supplies the compact lane widget **`KandaDropdown`** and prepares it so both systems “just work,” while keeping the actual attachment logic elsewhere (menus/templates for **simple tips**, help‑center/adapter for **gorgeous cards**).

---

## What `KandaDropdown` does for tooltips

**Enables precise hover/focus semantics**
- `setMouseTracking(True)` and `setAttribute(Qt.WA_Hover, True)` so **enter/leave/move** events fire reliably for hover‑cards.
- `setFocusPolicy(Qt.StrongFocus)` so keyboard navigation doesn’t lose the card connection.
- `setAttribute(Qt.WA_AlwaysShowToolTips, False)` to **suppress native balloons** when a hover‑card is present (prevents double tips).

**Prepares the popup view, too**
- Enables mouse tracking and `WA_Hover` on the **popup view** and its **viewport**; this avoids flicker or stuck cards when users open the dropdown then move across items.

**Draws a clean focus/hover affordance**
- Uses `TransparentItemDelegate` and themeable QSS (enabled/disabled) so focus/hover visuals don’t fight with the hover‑card chrome.

**Provides attachment placeholders**
- Stubs `_hover_tip_adapter`, `_hover_tip_provider`, and `_hover_tip_guard` right on the widget.
- Your hover‑card adapter can set these so the **lane‑clear** routine can **stop/hide/delete** safely on rebuild.

**Keeps sizing/UI compact**
- `QSizePolicy.Minimum` × `Fixed` with `AdjustToContents` → stable header metrics for positioning the hover‑card anchor.

---

## Where the two tooltip systems plug in

### 1) Simple native tips (menus, not here)
Attach to **menu actions** when building Core/Pro menus:
```python
# template/menu-builder
html = NeuroTooltipManager.preview_html({"tooltip": {"name": "Low‑cut", "description": "High‑pass cutoff (Hz)."}})
action = core_menu.addAction("Low‑cut")
action.setToolTip(html)  # instant native tip
```
This file doesn’t attach simple tips itself; it just provides a dropdown that won’t conflict if you later add hover‑cards.

### 2) Gorgeous hover‑cards (direct on the combobox header)
Attach **after** the dropdown is created and placed in the lane:

```python
from k06_templates.tooltip_lane_tmplt.tooltip_help_center import attach_hover_help

tipcfg = {...}  # includes "tooltip": {...}
attach_hover_help(dd, tipcfg, label=f"FilterOption: {label}", theme_mode="light", show_delay_ms=200, hide_delay_ms=220)

# inside your adapter, remember to set:
dd._hover_tip_guard = guard
dd._hover_tip_adapter = controller
dd._hover_tip_provider = provider
```
Because `KandaDropdown` already enables hover, disables native balloons, and makes the popup view hover‑aware, your card appears in the right place and doesn’t clash with native tips.

---

## Teardown & safety pattern

On lane rebuild:
```python
def teardown_hover_card(dd):
    ctl   = getattr(dd, "_hover_tip_adapter", None)
    guard = getattr(dd, "_hover_tip_guard", None)
    if ctl:
        try: ctl.stop()
        except Exception: pass
        delattr(dd, "_hover_tip_adapter")
    if guard:
        try: dd.removeEventFilter(guard)
        except Exception: pass
        delattr(dd, "_hover_tip_guard")
    if hasattr(dd, "_hover_tip_provider"):
        delattr(dd, "_hover_tip_provider")
```
This keeps the UI free of orphan windows/timers.

---

## Quick checklist

- [ ] Menus: simple tips on **QAction** (short, instant).
- [ ] Lane: attach a hover‑card per combobox **after creation**.
- [ ] Do not re‑enable native `setToolTip` on a combobox that has a hover‑card.
- [ ] On rebuild: stop/hide/delete through the stored `_hover_tip_*` handles.
- [ ] Popup view has mouse tracking & hover enabled (already done here).


