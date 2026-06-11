# tooltip_cmbbx_1 — Hover‑Card Tooltips for Core/Middle‑Tab Comboboxes

## Quick mental model
Two tooltip styles live side‑by‑side in the middle tab:
1) **Simple native tips** on the **button system** (Core/Pro menus & actions)
2) **Gorgeous hover‑cards** attached **directly to each combobox header** in the lane

This module is the *attachment layer* for the **gorgeous** path and also provides helpers for header widgets. It does **not** build the Core/Pro menus (where simple tips belong). fileciteturn9file0

---

## What this file exposes

### `attach_core_filter_hover(combo, tipcfg, label="")`
Attach a **GorgeousHoverCard** to a lane `QComboBox` (your per‑dropdown “gorgeous” tooltip). Key details:
- Enables hover prerequisites, disables native Qt balloon tips, and clears any existing simple tooltip on the combo. fileciteturn9file0
- Builds an **effective payload** from `tipcfg` and the **current value**:  
  • if `tipcfg['tooltip']['docs'][value]` is a **dict**, it merges onto the base tooltip;  
  • if it’s a **string**, it’s treated as HTML and turned into a header‑like `{title, summary, subject, html}` payload;  
  • otherwise it falls back to the original `tipcfg`. fileciteturn9file0
- Calls `tooltip_help_center.attach_hover_help(...)` with theme and delays read from env (`HOVERCARD_SHOW_DELAY_MS`, `HOVERCARD_HIDE_DELAY_MS`) via sanitizers. fileciteturn9file0
- **Rewires on value change** idempotently: disconnects any previous callback, then reconnects to rebuild the payload whenever the index changes. fileciteturn9file0

> In short: you get a **value‑aware** hover‑card that follows the dropdown’s current selection and can render either rich HTML per value or structured tooltips.

### `register_header_button_hover(widget, tooltip_map, theme="light")`
Attach a **GorgeousHoverCard** to a **header button** (e.g., `DualArrowButton`). It also clears any simple tooltip on that widget so the hover‑card “wins.” It respects label aliases (e.g., "Main Filters" → "Core Filters"). fileciteturn9file0

### `register_combobox1_tooltips(cmbbx_1)`
Register a **header‑combobox** (left panel / Combobox1) with a predefined `tooltip_map` (Core Filters, FIR/IIR, Wavelet, Normalizations, Visualization). Theme may be overridden with `HOVERCARD_THEME`. fileciteturn9file0

### `debug_check_hovercard_health(combo, label="")`
Quick diagnostics: checks `WA_Hover`, `mouseTracking`, and whether guard/adapter/provider attributes are present on the combo. Helpful when cards don’t show. fileciteturn9file0

---

## How it complements the **two tooltip systems**

### 1) Simple native tips (button system)
- **Where**: On `QAction`s inside the Core/Pro **menus** created by your template/menu builders.  
- **How**: `action.setToolTip("…")` — short, instant hints *before* the lane exists.  
- **This file’s role**: none, except that when you **upgrade** a header to a hover‑card via `register_header_button_hover(...)`, it **clears** any simple tip on that header widget to avoid clashes. fileciteturn9file0

### 2) Gorgeous hover‑cards (lane combobox headers)
- **Where**: On each `QComboBox` instantiated in the lane after `update_dropdowns()`.  
- **How**: `attach_core_filter_hover(combo, tipcfg, label)` — reads per‑value docs, merges or builds HTML payloads, and re‑attaches on every value change. Use with your lane rebuild and teardown (store guard/adapter on the widget so clear‑lane can stop/hide/delete safely). fileciteturn9file0

---

## Minimal wiring (copy/paste)

### A) Per‑dropdown attach during lane rebuild

```python
from k06_templates.tooltip_lane_tmplt.tooltip_cmbbx_1.tooltip_cmbbx_1 import attach_core_filter_hover


def _attach_cards_for_row(self, dd, key, label):
  tipcfg = self._params_map.get(key, {}).get("tooltip", {})
  if tipcfg:
    attach_core_filter_hover(dd, tipcfg, label=label)
```

### B) Header buttons upgraded to hover‑cards

```python
from k06_templates.tooltip_lane_tmplt.tooltip_cmbbx_1.tooltip_cmbbx_1 import register_header_button_hover, tooltip_map

register_header_button_hover(self.core_filters_button, tooltip_map, theme=self.theme_mode())
register_header_button_hover(self.pro_filters_button, tooltip_map, theme=self.theme_mode())
```

### C) Keep simple tips on menu **actions**
```python
# When building menus (template/menu helpers)
action = core_menu.addAction("Time Window")
action.setToolTip("Choose the visible EEG time span (seconds).")  # simple native tip
```

---

## Notes & best practices
Attach **after** the dropdown is in the layout (geometry stable).  
Keep **one** controller/card per widget; reuse on show/hide.  
If a value has no doc entry, the module logs it and falls back to a generic description. Add docs later for richer cards. fileciteturn9file0

---

## Frequently seen pitfalls
Hover doesn’t trigger → ensure `WA_Hover` and `mouseTracking` are enabled (the function does it, but verify in custom combos). Use `debug_check_hovercard_health(...)`. fileciteturn9file0  
Card re‑shows wrong content after change → confirm the value‑change callback is connected and not shadowed by another disconnect. fileciteturn9file0  
Header shows both native tip and card → you likely didn’t route the header through `register_header_button_hover(...)` (which clears the simple tip). fileciteturn9file0

---

## TL;DR
- **Simple tips** live on Core/Pro **menu actions** (template code), short and instant.  
- **Gorgeous hover‑cards** live on **lane combobox headers** (this module).  
- This file also upgrades header widgets to hover‑cards and gives you a ready tooltip map for common groups.

