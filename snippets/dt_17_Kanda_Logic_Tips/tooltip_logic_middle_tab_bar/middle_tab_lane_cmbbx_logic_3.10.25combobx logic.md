# middle_tab_lane_cmbbx_logic_3.10.25.md

This document summarizes how Core, Pro, Carets, and Dropdown Lanes logic works in your EEG filtering GUI system.

---

## 🧠 1. **Core/Pro Filters & Carets – Selection Model**

These are the **main axes** of your dropdown logic:

### ✅ **Core / Pro Filter Maps**
- **`core_filters.json`** and **`pro_filters.json`** define:
  - `direct_map`: simple flat key-value pairs (e.g., “Lowpass”: [options])
  - `nested_map`: a mapping of main keys to nested caret options
    ```json
    {
      "FilterBank": {
        "Delta": [...],
        "Theta": [...]
      }
    }
    ```

### ✅ **Active Selection Keys**
- Stored in the `ComboFiltersTemplate` base class:
  ```python
  self.core_main
  self.core_caret
  self.pro_main
  self.pro_caret
  ```
- These represent:
  - Which dropdown category is selected
  - And if nested, which subcategory (caret)

---

## 🔄 2. **Dropdown Lane – Rebuilding on Selection**

### ✅ Trigger: `update_dropdowns()`
- This triggers full rebuild of the active dropdown lane (Core or Pro).
- Logic moved to:  
  `update_dropdown_cmbbx_template_helper.py → update_dropdowns(ctx)`

### ✅ Steps it follows:
1. **Determine if Core or Pro lane is active** (`ctx._active_lane`)
2. **Pull matching filter options from:**
   - `core_direct_map` / `core_nested_map`
   - `pro_direct_map` / `pro_nested_map`
3. **Build "Pairs"** of dropdown label and option list:
   ```python
   pairs = [
       ("Lowpass Cutoff", ["None", "30Hz", "40Hz"]),
       ("Highpass Cutoff", ["0.1Hz", "1Hz"]),
   ]
   ```

4. **Create widgets (`KandaDropdown`)** with:
   - Tooltip from `label_to_tipcfg`
   - Signals for emitting changes
   - Optional caption

5. **Insert into `dropdown_layout`** with:
   - Left & right spacers
   - Optional filler to ensure layout stretch

6. **Emit `filterChanged` signal** after building to notify listeners.

---

## 🧩 3. **Carets – Nested Group Selection**

- When a key exists in `*_nested_map`, it’s a *group*.
- `*_caret` tells us which sub-group to use.
- Used by `pairs_for_lane(...)` to generate correct dropdowns.

🔁 Switching caret updates:
```python
self.core_caret = "Theta"
self.update_dropdowns()
```

---

## 🎛️ 4. **Dropdown Widget – KandaDropdown**

### From:
`widgets_cmbbx_template_helper.py`

### Features:
- Custom styling (hover, focus ring)
- Tooltip logic via `attach_hover_help`
- Captions via `ComboCaptionAdapter`
- Auto-sizing via `apply_caption_aware_precise_sizing`

Connected during `update_dropdowns()` inside `_build_one_combo()`.

---

## 📡 5. **Signal Emission Logic**

### Triggered on:
```python
combo.currentIndexChanged.connect(...)
```

### Emission Handlers:
Defined in `class_emission_and_change_cmbbx_template_helper.py`:
```python
ctx._emit_filter_change(label, combo)
ctx._on_any_dropdown_changed(key)
```

Purpose:
- 🔄 Update dependent dropdowns (e.g., wavelet).
- 💾 Save active state (for persistence).
- 🔔 Notify listeners (e.g., `EEGTab` components).

---

## 🛠️ 6. **Dropdown Lane Data Flow (High-level)**

```plaintext
JSON File → Filter Maps → Selection Keys
     ↓             ↓         ↓
  map_harvest → ComboFiltersTemplate → update_dropdowns()
     ↓                             ↓
   pairs_for_lane()       _build_one_combo()  → KandaDropdown
     ↓                             ↓
   Label + Options     Caption + Tooltip + Emission
```

---

## ✅ Summary of Module Responsibilities

| File | Role |
|------|------|
| `core_filters.json` / `pro_filters.json` | Define available dropdowns |
| `ComboFiltersTemplate` | Holds state & triggers UI updates |
| `update_dropdowns` | Rebuilds all active dropdowns |
| `KandaDropdown` | Custom dropdown with hover, styling |
| `ComboCaptionAdapter` | Adds label + caption logic |
| `TooltipHoverHelp` | Adds rich delayed hovercards |
| `map_harvest` | Parses the JSON maps |
| `pairs_for_lane` | Builds (label, options) for current selection |
| `class_emission_and_change_cmbbx_template_helper` | Handles change signals |

---

## 🟢 Next Step

You mentioned:  
> "Now we implement logic to show dropdown options and make nested logic implemented."

✅ That is all implemented and **wired correctly** in `update_dropdowns(ctx)`.  
If dropdowns are **not showing** options:

### Likely Causes:
1. `core_main` / `pro_main` / carets are not correctly set
2. JSON is not loaded into `core_direct_map` / `core_nested_map`
3. `_active_lane` is misconfigured
4. UI isn't calling `update_dropdowns()` at the right time
5. Widget is hidden by mistake
