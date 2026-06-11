# tooltip_templates — Simple vs Gorgeous Tooltips for the Middle Tab

> Two systems work side‑by‑side:
> 1) **Simple native tips** (Qt Rich Text) — ideal for **Core/Pro menu actions** and lightweight widgets.
> 2) **Gorgeous hover‑cards** — rich, animated help attached **directly to headers** (buttons or header combobox) and, elsewhere, to lane comboboxes via the help center.

This module gives you the **builders and managers** for simple tips and the **registration hooks** to attach gorgeous cards to header widgets.


---

## 1) Where this file fits

- **Simple tips API** (native tooltip bubble)
  - `NeuroTooltipManager.apply_tooltip(widget, config)`
  - `NeuroTooltipManager.apply_many({widget: config, ...})`
  - `NeuroTooltipManager.preview_html(config)`
  - A **defaults registry** and robust matching so you can set `tooltip={"description": ...}` or just a semantic `key` and let the manager format the bubble.

- **Gorgeous header cards** (hover‑card for header widgets)
  - `NeuroTooltipManager.register_header_widget_tooltips(widget, tooltip_map, theme="light", label_aliases=None)` upgrades a header **button/label** to a hover‑card by delegating to the help center.
  - `NeuroTooltipManager.register_combobox_header_tooltips(combobox, tooltip_map, theme="light")` does the same for a **header combobox** (dev/tests pattern).

- **Theming** and **palette following**
  - `set_theme(True|False)`, `theme()`
  - `set_theme_auto()` (detect from `QApplication.palette()`), `follow_app_palette(True)`

- **ToolTipBinder mixin**
  - One‑liners to bind simple tips by `objectName`, either explicitly or heuristically from a registry.


---

## 2) Simple native tips (Core/Pro menus & lightweight widgets)

`NeuroTooltipManager` builds a polished **Qt Rich Text** bubble and attaches it to any `QWidget` with `setToolTip(...)`.

**How to feed it**
- **Direct content** via `config["tooltip"]`:
  - If it’s a **dict**, it’s treated as a **structured** payload with fields like `name`, `description`, `range`, `units`, `default`, `options`, `formula`, `warning`.
  - If it’s a **string**, it becomes a basic body with optional header (`name`).
- **Semantic key** via `config["key"]`:
  - The manager resolves a **default** from its registry (by key or normalized name) and builds a nice, consistent bubble.

**Helpers**
- `apply_tooltip(widget, config)` → attaches the bubble to the widget.
- `preview_html(config)` → returns the HTML string (useful to feed `QAction.setToolTip(...)` since `QAction` isn’t a `QWidget`).
- `register_defaults(mapping, replace=False)` / `clear_defaults()` → maintain your semantic library.

**Example**
```python
# Building Core/Pro menus (template code)
html_tip = NeuroTooltipManager.preview_html({
    "key": "HighPass",
    "tooltip": {"name": "Low‑cut", "description": "High‑pass cutoff (Hz).", "units": "Hz", "range": [0.1, 10]}
})
action = core_menu.addAction("Low‑cut")
action.setToolTip(html_tip)  # simple native tip (Qt Rich Text)
```


---

## 3) Gorgeous hover‑cards on **header widgets**

These are **rich, animated** and orchestrated by the help center; this module provides the registration **hooks**.

### A) Header buttons / labels

```python
from k06_templates.tooltip_templates import NeuroTooltipManager
from k06_templates.tooltip_lane_tmplt.tooltip_cmbbx_1_neurotooltips import tooltip_map

NeuroTooltipManager.register_header_widget_tooltips(
    self.core_filters_button,
    tooltip_map,
    theme=self.theme_mode(),  # "light"|"dark"
    label_aliases={"Main Filters": "Core Filters"}
)
```
- Resolves label (e.g., `QAbstractButton.text()`), applies alias (“Main Filters” → “Core Filters”).
- Clears any **plain** tooltip on that widget so the hover‑card wins.
- Delegates to the help center with theme and delays read from env.

### B) Header combobox
```python
NeuroTooltipManager.register_combobox_header_tooltips(
    self.header_combobox,
    tooltip_map,
    theme="dark"
)
```
- Hooks selection change → re‑attaches the card for the current header value.
- Runs a small **hover‑readiness diagnostic** in the console to catch missing flags.


---

## 4) Theming & palette

- `set_theme_auto()` detects dark/light using `QApplication.palette()` (luminance heuristic).
- `follow_app_palette(True)` tries to re‑apply theme when the palette changes at runtime.
- All HTML builders read the resolved theme so colors/icons adapt automatically.


---

## 5) ToolTipBinder — fast binding by `objectName`

When your widgets already exist in a panel, you can **bind simple tips** quickly:

```python
class MyPanel(QWidget, ToolTipBinder):
    def __init__(self):
        defaults = {
            "HighPass": {"name": "Low‑cut", "description": "Hz cutoff"},
            "Notch"   : {"name": "Notch",   "description": "Line filter"}
        }
        self.register_and_bind_tooltips(
            self,
            defaults,
            mapping={"comboHighPass": "HighPass"},  # objectName → key
            auto=True                               # also try heuristic matches
        )
```

- `bind_by_object_map(root, {"objName": "Key" | dict})` → explicit mapping
- `auto_bind_registered(root, exact_only=False)` → uses normalized names and strips common prefixes (`cmb/combo/btn/spin/...`).


---

## 6) How this pairs with the **two systems** in your app

- **Simple tips** → best for **Core/Pro menu actions** and small widgets. Build with `preview_html(...)` and attach to `QAction` or use `apply_tooltip(...)` for real widgets.
- **Gorgeous hover‑cards** → attach to **header** widgets here; for **lane comboboxes** use your help‑center entry point (`attach_hover_help(...)`) in the lane rebuild flow.
- When a header widget is upgraded to a hover‑card, any plain tooltip on that widget is cleared so users only see the rich card.


---

## 7) Sanity checklist

- [ ] Core/Pro **menu actions** have simple tips (short, instant).
- [ ] Header widgets (buttons or header combobox) registered for hover‑cards with your `tooltip_map`.
- [ ] Lane comboboxes attach gorgeous cards via the help center during lane rebuild.
- [ ] Theme auto‑detect or explicit `theme` set; palette following enabled if needed.
- [ ] Defaults registry kept up‑to‑date for consistent simple tips.


