
# 🧠 TOOLTIP SYSTEMS IN YOUR EEG GUI

There are **two distinct architectures**:

---

## 🟨 1. Simple Qt Tooltips — for Buttons, Toolbar, Basic ComboBoxes

### ✅ Purpose
- Provides **basic text** help bubbles when you hover over:
  - Buttons
  - Middle tab bar widgets
  - Core/pro dropdowns that don’t use hover-cards

### ✅ Core File
- [`tooltip_templates.py`](#) — `NeuroTooltipManager` is the manager for these tooltips.

### ✅ How it works
- Uses `.setToolTip(str or rich-text)` on Qt widgets
- Can auto-detect **dark/light mode**
- Accepts tooltip configs from JSON:
  ```json
  { "label": "µV Gain", "tooltip": { "description": "Vertical scale." } }
  ```
- Registered defaults under semantic keys like `"HighPass"`, `"Montage"`

### ✅ Key Methods
- `NeuroTooltipManager.apply_tooltip(widget, config)`  
- Applies description, warning, and extras like range, units, etc.
- Used in:
  - `universal_dropdown.py` — applies tooltip in `configure(...)`:
    ```python
    self.setToolTip(spec.tooltip)  # string or dict
    ```

### ✅ Used in:
- Buttons (e.g. middle bar, EEG toolbar)
- Standard dropdowns if HoverCard unavailable
- Visualizer controls

---

## 💎 2. Gorgeous HoverCard Tooltips — for Lane Dropdowns (Core/Pro)

### ✅ Purpose
- Provides **rich, interactive hover-cards** for EEG config dropdowns
  - Contextual notes per value
  - Color themes, headers, links, math
  - Documentation blocks per selection

### ✅ Core File
- [`tooltip_help_center.py`](#)  
  - Imports: `GorgeousHoverCard`, `HoverTipController`, `ThemeManager`

### ✅ How it works
- Attaches hover logic to widgets dynamically
- Tracks current value in the dropdown
- Caches rendered HTML using LRU
- Can attach hover card and Qt tooltip in fallback mode

### ✅ Key Functions
- `apply_rich_tooltip(widget, tipcfg)`  
  - Applies **Qt tooltip** as fallback  
- `attach_hover_help(widget, label, tipcfg)`  
  - Creates & connects the **HoverCard** tooltip

### ✅ Used in:
- `update_dropdown_cmbbx_template_helper.py`:
  - Inside `_build_all_combos()`
    ```python
    attach_hover_help(combo, label, tipcfg)
    ```
  - Dropdowns are constructed dynamically from core/pro filter maps
  - Hover tooltips are enriched with label, current value, etc.

---

# 🧱 Tooltip Architecture Summary

## 🔧 Tooltip Application Points:

| Component                     | Tooltip Type     | Where Applied                                 | Connected Function                      |
|------------------------------|------------------|------------------------------------------------|------------------------------------------|
| Buttons (middle tab bar)     | Simple Qt        | `setToolTip(...)` via `NeuroTooltipManager`   | `apply_tooltip(...)` in `tooltip_templates.py` |
| UniversalDropdown (basic UI) | Simple Qt        | `configure(...)` → `setToolTip(...)`          | `universal_dropdown.py`                 |
| Core/Pro Dropdowns (lane)     | HoverCard + Fallback | `_build_all_combos(...)` in `update_dropdown_cmbbx_template_helper.py` | `attach_hover_help(...)` from `tooltip_help_center.py` |
| Fallback Tooltip             | Simple Qt        | `apply_rich_tooltip(...)`                     | Always sets a basic `.setToolTip(...)`  |

---

# 📊 Architectural Chart

```
                     [ JSON Tooltip Configs ]
                              ↓
 ┌────────────────────────────────────────────────────────────────┐
 │                         Tooltip Engine                         │
 └────────────────────────────────────────────────────────────────┘
              ↓                                ↓
     [Simple Qt Tooltip]                [HoverCard Tooltip]
              ↓                                ↓
   NeuroTooltipManager             attach_hover_help(widget, label, cfg)
  (tooltip_templates.py)           GorgeousHoverCard + HoverTipController
              ↓                                ↓
        Buttons, Tabs         Lane Dropdowns (core/pro: rebuilt dynamically)
        UniversalDropdowns    (_build_all_combos → attach_hover_help)

                  ↘                      ↙
               fallback to rich Qt tooltip if HoverCard is missing
```

---

# 📋 Architecture Table: Tooltip Systems

| Aspect                        | Simple Tooltip                      | Gorgeous HoverCard Tooltip               |
|------------------------------|-------------------------------------|------------------------------------------|
| Visual Style                 | Native Qt bubble                    | Custom rich HoverCard with HTML/css      |
| Used In                      | Buttons, tab bar, fallback combos   | Lane dropdowns in core/pro               |
| Manager                      | `NeuroTooltipManager`               | `GorgeousHoverCard`, `HoverTipController`|
| Applies To                   | All QWidget                         | QComboBox (in lanes)                     |
| Fallback Support             | Yes (always sets Qt tooltip)        | Yes (sets fallback Qt tooltip too)       |
| Source File                  | `tooltip_templates.py`              | `tooltip_help_center.py`                 |
| Attach Function              | `apply_tooltip(...)`                | `attach_hover_help(...)`                 |
| Connected Module             | `universal_dropdown.py`             | `update_dropdown_cmbbx_template_helper.py` |
| Data Source                  | JSON (e.g. `core_filters.json`)     | Same                                     |
| Dynamic Value Notes          | No                                  | Yes (contextual per item)                |
| Dependencies                 | None                                | Optional: `shiboken6`, HoverCard classes |

