# filters_controller — Middle‑Tab Comboboxes & Tooltip Systems

> Two tooltip styles, one controller: **simple native tips** on the Core/Pro button system, and **gorgeous hover‑cards** attached directly to every combobox header in the lane.

---

## 1) What this controller owns

**Hover‑card lifecycle (gorgeous)**
- Attaches hover‑cards to **each lane combobox** after the lane is rebuilt.
- Attaches hover‑cards to **header controls** (Core/Pro) when available (buttons or the legacy header combobox).
- Validates that all expected comboboxes are “hover‑ready” at the end of an update.

**Dependency → UI sync**
- Computes parameter dependencies from JSON and **hides/disables** affected comboboxes and labels, so users don’t see irrelevant controls or tooltips.

**Indexing**
- Rebuilds the internal `key → combobox` index so tooltip attachment is always performed on the correct widgets.

**Configuration sources**
- Loads: `filtering_config.json` (dependencies, UI flags), optional `filtering_support.json` (rules/help), and the header hover map `tooltip_cmbbx_1_neurotooltips.json`.

> In practice: **gorgeous** tooltips are wired here; **simple** tooltips (native Qt `setToolTip`) for the Core/Pro menus are set where the menus/actions are created (typically the template/menu helpers).

---

## 2) The update flow (where to hook your tooltips)

### `update_dropdowns(controller)`
Called after the lane has been (re)built. It performs the following, in order:

1. **Index rebuild**
   ```python
   rebuild_key_index(controller)  # populates controller._key_to_combo
   ```

2. **Attach hover‑cards to lane comboboxes**
   ```python
   attach_hover_cards_to_dropdowns(controller)
   ```

3. **Dependencies → UI**
   ```python
   updated_params, notes = compute_params_after_dependencies(controller)
   _apply_dependency_ui(controller, updated_params)  # hide/grey combos & labels
   ```

4. **Attach header hover‑cards**
   ```python
   attach_header_button_tooltips_if_available(controller)  # Core/Pro buttons
   attach_header_tooltip_if_available(controller)          # legacy header combobox
   ```

5. **Sanity check**
   ```python
   validate_all_comboboxes_hover_ready()
   ```

> **Tip:** If you also want **simple native tips** on Core/Pro **menus/actions**, apply them during the **menu build** in your template (not here).

---

## 3) Gorgeous hover‑cards — lane comboboxes

### `attach_hover_cards_to_dropdowns(controller)`
- Iterates `controller._key_to_combo.items()` (rebuilt in step #1).
- For each `key, combo`, it looks up `cfg = controller._params_map.get(key, {})`.
- Calls the hover‑center adapter:
  ```python
  tooltip_help_center.attach_hover_help(
      combo,
      cfg,                              # contains label/tooltip payload
      label=f"FilterOption: {label}",
      theme_mode="light",
      show_delay_ms=200,
      hide_delay_ms=200
  )
  ```
- Store guard/controller on the widget in your adapter so lane‑clear can stop/hide/delete them cleanly on rebuild.

**What to put in `cfg`**
- At minimum: `{"label": "...", "tooltip": {"title": "...", "description": "...", ...}}`
- If you use a caption formatter, compute `title` as `<prefix><value><suffix>` for a consistent, value‑aware header (e.g., “Low‑cut 1.0 Hz”, “Gain 50 µV”).

---

## 4) Gorgeous hover‑cards — header controls

### Buttons (preferred in production)
`attach_header_button_tooltips_if_available(controller)`:
- **Discovers** likely header buttons (named attrs, `findChildren(QAbstractButton)`, or app‑wide scan).
- Maps the runtime button text to a JSON key (e.g., **“Main Filters” → “Core Filters”**).
- Clears any plain Qt tooltip so the hover‑card “wins”.  
- Attaches the hover‑card using the header tooltip map (theme/delay can be set via env).

### Legacy header combobox (dev/tests)
`attach_header_tooltip_if_available(controller)`:
- If a `header_combobox` exists, registers its hover‑map via `NeuroTooltipManager.register_combobox_header_tooltips(...)` after validating the JSON map.

---

## 5) Dependencies → UI behavior (so tooltips don’t lie)

1) **Collect current params** (from the controller’s helper or from each combobox currentData/currentText).
2) **Apply rules** from `filtering_config.json`:
   - Condition operators: `not null`, ranges (`gte`/`lte`), set membership (`in`, `not_in`).
   - When a parameter is disabled by a rule, it is set to `None` in the computed params.
3) **Update the UI**:
   - If `hide_when_disabled` is true, **hide** the combo and its label.
   - Else, **grey** the combo out (disabled).

Result: disabled/hidden controls won’t distract users with inappropriate hover‑cards.

---

## 6) How this fits with the simple tooltips (Core/Pro menus)

- **Simple native tips** belong to **menu actions** (QAction) on the Core/Pro buttons.  
- They should be assigned **during menu construction** (in the template/menu helpers), e.g.:
  ```python
  action.setToolTip(simple_tip_text)  # short, instant, no animation
  ```
- This controller **does not build menus**; it focuses on hover‑cards and dependency/UI state.

---

## 7) Quick checklist

- [ ] Lane rebuilt and `_key_to_combo` refreshed
- [ ] Hover‑cards attached to **every visible** lane combobox
- [ ] Dependencies applied and disabled widgets hidden/greyed
- [ ] Core/Pro header hover‑cards attached (buttons or header combobox)
- [ ] Simple tips set on menu **actions** (done in template)
- [ ] Final `validate_all_comboboxes_hover_ready()` passes

---

## 8) Minimal snippet you can paste

```python
def update_dropdowns(self):
    rebuild_key_index(self)
    attach_hover_cards_to_dropdowns(self)         # per‑dropdown gorgeous cards
    params_after, _ = compute_params_after_dependencies(self)
    _apply_dependency_ui(self, params_after)      # hide/disable as needed
    attach_header_button_tooltips_if_available(self)
    attach_header_tooltip_if_available(self)      # legacy header combo, if present
    validate_all_comboboxes_hover_ready()         # end‑state assertion
```

> For **simple** tooltips on Core/Pro menus, set `QAction.setToolTip(...)` during menu build in your template.

