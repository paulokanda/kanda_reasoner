# tooltip_help_center — Hover‑Card Orchestrator for the Middle‑Tab Combobox Lane

> You have **two tooltip systems**:
> 1) **Simple** native tips on the **button system** (Core/Pro menus & actions).
> 2) **Gorgeous** hover‑cards attached **directly to each combobox header** in the lane.
>
> This module is the **orchestrator** for the gorgeous path — it builds/attaches cards, installs safe mediators, suppresses conflicts with popups, and provides diagnostics. It does **not** build Core/Pro menus (where simple tips belong). fileciteturn11file0

---

## What this module provides at a glance

- **attach_hover_help(widget, tipcfg, ...)** — the **entry point** that attaches a Gorgeous hover‑card to a widget (combobox header or header control). It idempotently enables hover prerequisites, **disables/clears native Qt tooltips** on that widget so the card “wins”, wires refresh on value‑change, and stores controller/mediator on the widget for teardown. fileciteturn11file0
- **_SafeHoverMediator** — a robust event‑filter that drives **show/hide** using timers (show/hide delays), installed on both the **target widget** and the **card** so entering the card cancels hides and leaving schedules them. fileciteturn11file0
- **_PopupGuard** — suppresses the hover‑card when popups/menus appear (e.g., when the combobox drops down), with a small hide delay to keep UX smooth. Test hook included. fileciteturn11file0
- **validate_all_comboboxes_hover_ready()** & **HoverDebuggerWindow** — runtime checks to highlight missing hover prerequisites across all QComboBoxes (WA_Hover, mouseTracking, provider/controller presence). fileciteturn11file0
- **Per‑value content** helpers — `_summary_for_card(...)` and `_detail_html(...)` read `tipcfg["tooltip"]["docs"][currentValue]` to render **value‑aware** summaries/details (falls back gracefully if absent). fileciteturn11file0
- **Environment knobs** — `HOVERCARD_THEME` (“light”/“dark”), `HOVERCARD_SHOW_DELAY_MS`, `HOVERCARD_HIDE_DELAY_MS`, `HOVER_POPUP_GUARD_HIDE_MS` to tune theme/timing. fileciteturn11file0

---

## How it maps to your two tooltip systems

### 1) Simple native tooltips — Core/Pro **menus & actions**
- **Where**: `QAction`s in the Core/Pro menus (created by your template/menu helpers).
- **How**: `action.setToolTip("Short hint…")` — instant, concise, shown **before** the lane exists.
- **This module’s role**: none here **except** that when you attach a **gorgeous** card to a header widget, `attach_hover_help(...)` clears native tips on that widget to avoid double tips. Keep menu action tips in the template. fileciteturn11file0

### 2) Gorgeous hover‑cards — **lane combobox headers** (and headers if you choose)
- **Where**: After the lane is (re)built, for every `KandaDropdown` (QComboBox) in the row.
- **How**: Call `attach_hover_help(combo, tipcfg, label="FilterOption: Low‑cut", theme_mode, show_delay_ms, hide_delay_ms)`. The function:
  - Enables hover (`WA_Hover`, mouse tracking), disables the native Qt tooltip (`WA_AlwaysShowToolTips=False`, clears `setToolTip("")`).  
  - Creates (or reuses) a themed **GorgeousHoverCard** + **HoverTipController**.  
  - Installs **_SafeHoverMediator** on widget/card to drive show/hide using delays.  
  - Wires an **index‑changed** callback so card content updates when the selection changes.  
  - Installs **_PopupGuard** so dropdown/menus automatically hide the card.  
  - Stores `_hover_tip_adapter`, `_hover_tip_provider`, `_hover_tip_mediator`, `_hover_tip_guard` (and `_popup_guard`) on the widget so your **lane‑clear** can stop/hide/delete reliably. fileciteturn11file0

---

## Minimal wiring (copy/paste)

### A) Attach a gorgeous card to each combobox during lane rebuild

```python
from k06_templates.tooltip_lane_tmplt.tooltip_help_center import attach_hover_help


def _attach_cards_for_dropdown(self, dd, key, label):
    tipcfg = self._params_map.get(key, {}).get("tooltip", {})
    if tipcfg:
        # Theme & delays may come from env; you can override explicitly:
        attach_hover_help(
            dd,
            tipcfg,
            label=f"FilterOption: {label}",
            theme_mode=os.getenv("HOVERCARD_THEME", "light"),
            show_delay_ms=int(os.getenv("HOVERCARD_SHOW_DELAY_MS", "200")),
            hide_delay_ms=int(os.getenv("HOVERCARD_HIDE_DELAY_MS", "220")),
        )
```

### B) Upgrade a **header control** to a gorgeous card (optional)

```python
from k06_templates.tooltip_lane_tmplt.tooltip_help_center import attach_hover_help
from k06_templates.tooltip_lane_tmplt.tooltip_cmbbx_1_neurotooltips import tooltip_map

core_hdr = self.core_filters_button  # or a header combobox
hdr_tip = tooltip_map.get("Core Filters", {})
attach_hover_help(core_hdr, hdr_tip, label="Header: Core Filters", theme_mode=self.theme_mode())
```

> When you choose this, the header’s native `setToolTip(...)` is cleared so the card takes precedence. Keep **menu action** simple tips intact in the template. fileciteturn11file0

---

## Lifecycle & Teardown

- **Lane rebuild**: old cards/mediators must be removed **before** widgets are deleted. Because this module stores references on the widget (`_hover_tip_*`), your lane‑clear helper can find and stop/hide/delete them safely (controller.hide_card(force=True), card.deleteLater(), removeEventFilter). fileciteturn11file0
- **Popups**: `_PopupGuard` keeps the card from fighting with dropdowns or menus (auto‑hide with a small delay). Tune with `HOVER_POPUP_GUARD_HIDE_MS`. fileciteturn11file0
- **Diagnostics**: Call `validate_all_comboboxes_hover_ready()` or use `HoverDebuggerWindow` to highlight missing hover prerequisites. fileciteturn11file0

---

## Value‑aware content

- Card **summary** fields (`Name`, `Description`, `Units`, `Range`, `Default`, `Warning`) come from `tipcfg["tooltip"]`. fileciteturn11file0
- Card **details** can depend on the current selection, looked up via `tipcfg["tooltip"]["docs"][currentValue]` (HTML string or richer object). If missing, the module returns a neutral “No additional details” panel. fileciteturn11file0

---

## Env knobs (safe defaults)

```text
HOVERCARD_THEME=light|dark
HOVERCARD_SHOW_DELAY_MS=200
HOVERCARD_HIDE_DELAY_MS=220
HOVER_POPUP_GUARD_HIDE_MS=180
```
All are sanitized/clamped (e.g., delay range 0–5000 ms). fileciteturn11file0

---

## Quick checklist

- [ ] **Simple tips** set on Core/Pro **menu actions** (template/menu builders).  
- [ ] **Gorgeous cards** attached to every visible lane combobox with `attach_hover_help(...)`.  
- [ ] Header upgraded to a gorgeous card **only** if desired (native tip cleared on that widget).  
- [ ] Lane‑clear stops/hides/deletes `_hover_tip_*` artifacts.  
- [ ] Hover prerequisites validated (WA_Hover, mouseTracking, provider/controller present). fileciteturn11file0

