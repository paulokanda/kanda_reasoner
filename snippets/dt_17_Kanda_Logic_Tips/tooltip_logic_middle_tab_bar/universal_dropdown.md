# universal_dropdown — Middle‑Tab Combobox + Tooltip Wiring

> Two tooltip styles live in your middle tab:
> 1) **Simple native tips** → lightweight, Qt Rich Text bubbles (great for Core/Pro **menus** and basic widgets).
> 2) **Gorgeous hover‑cards** → rich, animated cards attached **directly to each combobox header** in the lane.

This module supplies the **combobox widget** (`KandaComboBox`) and its **wrapper** (`UniversalDropdown`) used across lanes. It also knows how to attach a **simple tooltip** for a dropdown **when provided by spec**; the **gorgeous** hover‑cards are attached elsewhere (help center / controllers).

---

## What’s in here

### `KandaComboBox` (strict 28px + soft hover)
- Fixed 28 px height with an item delegate (`TransparentItemDelegate`) that draws a subtle on‑row hover.
- A small QSS for a crisp orange accent and consistent popup styling.
- Intended to be **the** dropdown used in the lane, so all tip systems have a single anchor.

### `UniversalDropdown(QWidget)`
- Wraps `KandaComboBox` and exposes **domain signals**: `sensitivity_changed`, `montage_changed`, `speed_changed`, `hp_changed`, `lp_changed`, `notch_changed`.
- `configure(spec: DropdownSpec)` populates items, sets default, **and (optionally) attaches a simple native tooltip** via `NeuroTooltipManager.apply_tooltip(...)`.
- Keeps width sane via `_ensure_width()` using the longest label.

### `DropdownSpec`
A normalized spec used by both JSON and Pro filters. Fields commonly consumed by tooltips:
- `name`
- `tooltip` (string or dict)
- `units`, `range`, `default`, `formula`, `warning`

These feed the **simple** tooltip builder so you don’t handcraft bubbles per control.

---

## Where the two tooltip systems plug in

### 1) Simple native tooltips (this file attaches them)
In `configure(...)`, if `spec.tooltip` is present, the wrapper calls:

```python
NeuroTooltipManager.apply_tooltip(self, {
    "name": spec.name,
    "tooltip": spec.tooltip,
    "units": spec.units,
    "range": getattr(spec, "range", None),
    "default": getattr(spec, "default", None),
    "formula": getattr(spec, "formula", None),
    "warning": getattr(spec, "warning", None),
})
```

That yields a **native Qt** bubble on the wrapper widget (sufficient for a basic hint). Use this when you want a **lightweight** tip and you are **not** attaching a hover‑card to the same control.

> For Core/Pro **menus**, keep simple tips on the **`QAction`s** that the template builds (short, instant: `action.setToolTip(html)`), not here.

### 2) Gorgeous hover‑cards (attached elsewhere, to the combobox header)
This module **does not** attach hover‑cards. To enable the rich, animated cards on the **lane dropdowns**, call the help‑center entry from your controller right after each dropdown is created:

```python
from k06_templates.tooltip_lane_tmplt.tooltip_help_center import attach_hover_help

# dd is universal_dropdown.combo  (or the wrapper if you prefer)
attach_hover_help(dd.combo, tipcfg, label=f"FilterOption: {spec.name}",
                  theme_mode="light", show_delay_ms=200, hide_delay_ms=220)
```

Those cards are **value‑aware** (content may change with `currentIndexChanged`), and the help center will also install mediators and popup guards, plus store references on the widget so lane‑clear can stop/hide/delete safely.

---

## Integration patterns

**A) “Simple only” dropdown** (no hover‑card)
- Provide `spec.tooltip` (string or dict) and call `configure(spec)` → you’ll get the native bubble from this file.

**B) “Gorgeous” dropdown**
- Omit `spec.tooltip` (or ignore it) and attach the hover‑card in your lane controller using `attach_hover_help(dd.combo, tipcfg, ...)` with the per‑value docs.
- If you keep both, favor the card: attach it to **`dd.combo`**; the mouse is over the combo most of the time, so users will see the card.

**C) Menus (Core/Pro button system)**
- Build the menus in the template and set **simple** tips on each **`QAction`** (using `NeuroTooltipManager.preview_html(...)` if you want styled HTML).

---

## Signals that help tooltips stay in sync
`UniversalDropdown` emits domain signals on selection changes (`hp_changed`, `lp_changed`, `notch_changed`, etc.). Your controller can subscribe to these to **refresh** hover‑card content (e.g., to update a computed caption in the card title), while the help center already handles the most common **value‑aware** updates.

---

## Sanity checklist
- [ ] For **simple** tips on a dropdown, pass `spec.tooltip` and let `configure()` attach the native bubble.
- [ ] For **gorgeous** cards on lane dropdowns, call `attach_hover_help(dd.combo, tipcfg, ...)` after creation.
- [ ] Keep **menu action** tips short and instant (set on `QAction` during menu build).
- [ ] On lane rebuild, ensure your controller tears down any existing adapters/mediators (help center stores them on the widget).


