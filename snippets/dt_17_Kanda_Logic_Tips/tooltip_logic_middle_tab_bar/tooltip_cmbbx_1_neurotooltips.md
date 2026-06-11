# tooltip_cmbbx_1_neurotooltips — Header Hover‑Card Map for the Middle Tab

## Purpose
This JSON file defines the **header‑level hover‑cards** (the “gorgeous” tooltips shown on header controls like **Core/Pro** buttons or a **header combobox**).  
It does **not** define the simple native tips used in the Core/Pro **menus**; those belong to your template/menu builders (`QAction.setToolTip(...)`).

## What’s inside
Top‑level entries correspond to **header groups** you expose in the UI. Each entry provides:
- `description`: one‑line help (shown in the hover‑card body).
- `icon`: an emoji/icon hint used by your card UI (optional).
- `note`: a short operational guidance line.

Example groups shipped:
- **Core Filters** — essential visualization and reference settings.
- **FIR Filters** — zero/linear‑phase finite impulse response options.
- **IIR Filters** — low‑latency infinite impulse response families.
- **Wavelet Filters** — time–frequency denoising/decomposition.
- **Normalizations** — scale and contrast normalization strategies.
- **Visualization** — non‑signal modifiers (overlays, aesthetics).

> These groups fuel the **gorgeous** hover‑cards for header controls; they are **category‑level**. Per‑dropdown, **value‑aware** tooltips come from each dropdown’s `tipcfg` (separate JSON/maps) and are attached in the lane.

## Where it plugs into your two tooltip systems

### 1) Simple native tooltips — Core/Pro menus (button system)
- **Where**: On each `QAction` created while building Core/Pro menus.
- **How**: `action.setToolTip("Short hint…")`
- **Source**: Your template/menu helpers (not this JSON). Keep them **short** and **instant**.

### 2) Gorgeous hover‑cards — Header controls
- **Where**: On **Core/Pro header buttons** (e.g., `DualArrowButton`) or a **header combobox**.
- **How**: Use the helpers that consume this JSON to attach a card:
  ```python
  from tooltip_cmbbx_1 import register_header_button_hover, register_combobox1_tooltips
  from tooltip_cmbbx_1_neurotooltips import tooltip_map  # the JSON as dict

  # Buttons get upgraded to hover-cards (clears any native tip on the widget)
  register_header_button_hover(self.core_filters_button, tooltip_map, theme=self.theme_mode())
  register_header_button_hover(self.pro_filters_button,  tooltip_map, theme=self.theme_mode())

  # Or, if you use a header combobox in dev/tests:
  register_combobox1_tooltips(self.header_combobox)
  ```
- **Behavior**: When a header gets a hover‑card, any plain `setToolTip(...)` on that widget is cleared so the rich card takes precedence.

## File interactions & flow
1) **Load** the JSON into a Python `dict` (`tooltip_map`).  
2) **Alias match** header labels (e.g., “Main Filters” → “Core Filters”).  
3) **Attach** the hover‑card to the target header widget using the matched entry’s `description / icon / note`.  
4) **Teardown** is automatic when the header widget is deleted; if you re‑attach dynamically, ensure you remove old adapters first.

## Extending the map
Add a new header section by inserting a new top‑level key with the same fields:
```json
{
  "My Custom Group": {
    "description": "One‑line purpose users see on hover.",
    "icon": "🧩",
    "note": "Short operational hint."
  }
}
```
Keep `description` concise; reserve deep dives for the detail dialog launched from your hover‑card.

## Best practices
- Use **header cards** for **conceptual guidance** (what the group controls do).
- Use **menu simple tips** for **action hints** (what menu selection will perform).
- Keep **per‑dropdown** rich, value‑aware cards in the **lane**, not at the header level.
- When adopting new groups, verify alias mapping so the right entry is applied even if button text differs (“Main Filters” vs “Core Filters”).

## Quick checklist
- [ ] Core/Pro menu actions have short native tips (template builds).
- [ ] Core/Pro header buttons are upgraded to gorgeous cards using this map.
- [ ] Header combobox (if present) also registered for cards in dev/tests.
- [ ] Lane comboboxes use their **own** per‑dropdown tipcfg for value‑aware cards.

