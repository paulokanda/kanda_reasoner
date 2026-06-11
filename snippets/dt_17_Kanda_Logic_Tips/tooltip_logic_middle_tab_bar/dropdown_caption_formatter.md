# dropdown_caption_formatter — Captions for Simple & Gorgeous Tooltips

## Why this file matters
You have **two tooltip systems** in the middle tab:
1) **Simple tooltips** on the **button system** (Core/Pro menus & actions)
2) **Gorgeous hover‑cards** attached **directly to each combobox header** in the lane

`dropdown_caption_formatter.py` gives you a single way to build **clean, consistent headers** for both systems by returning a **(prefix, suffix)** pair you concatenate with the current option/value (e.g., `"Low‑cut 1.0 Hz"`, `"Gain 50 µV"`). fileciteturn6file0L73-L84

---

## What the module provides

### Normalization helper
A tiny normalizer `_norm(s)` removes non‑word chars and lowercases strings so **keys or labels** can be matched robustly. fileciteturn6file0L6-L9

### CaptionRule + Registry
A `CaptionRule` is just `{prefix, suffix}`. The singleton `_registry` stores rules **by key** and **by label** with sensible EEG defaults (viz/filter/FIR/IIR). fileciteturn6file0L19-L21 fileciteturn6file0L23-L27 fileciteturn6file0L55-L62

**Key‑based defaults (samples)**  
- `viz.time_window` → `"Time Window ", " s"`  
- `viz.gain` / `viz.sensitivity` → `"Gain ", " µV"`  
- `filter.lowcut.hz` → `"Low‑cut ", " Hz"`  
- `filter.highcut.hz` → `"High cut ", " Hz"`  
- `filter.notch.hz` → `"Notch ", ""` *(suffix purposely empty so labels like “50 Hz + Hs” render verbatim)* fileciteturn6file0L31-L53

**Label fallbacks (samples)**  
- `Time Window`, `Gain`, `Sensitivity`, `Montage`  
- Low‑cut family: `Low‑cut`, `High‑pass (Low‑cut)`, `Slope (dB/oct)`  
- High‑cut family: `High‑cut`, `Low‑pass`, `HCut Slope`  
- Notch family: `Notch`, `Line Filter`  
- FIR/IIR groups: `Window`, `Phase`, `TBW`, `Order`, `Ripple (dB)`, `Stop Atten` fileciteturn6file0L64-L108

### Public API (you’ll actually call)
- `get_caption_affixes(key=..., label=..., tipcfg=...) -> (prefix, suffix)` — main helper used by both tooltip systems. fileciteturn6file0L90-L108  
- `register_caption_rule(key=..., label=..., prefix=..., suffix=...)` — extend rules at runtime (future filters). fileciteturn6file0L84-L89  
- `find_caption_rule(label, key)` — query the registry directly if you need. fileciteturn6file0L11-L12  
- **Compat shims**:  
  - `get_caption_affixes_compat(...)` — same as main helper for old call‑sites. fileciteturn6file0L9-L11  
  - `apply_caption_if_any(...)` — **deprecated**: no longer mutates the combo; now returns a rule for callers to apply. fileciteturn6file0L89-L100

### Affix priority
When you call `get_caption_affixes(...)`, the module resolves the best (prefix, suffix) in this order:  
1. `tipcfg["tooltip_header_prefix" | "tooltip_header_suffix"]`  
2. `tipcfg["caption_prefix" | "caption_suffix"]`  
3. Registry match by **key** or **label**  
4. Default: `("", "")`  
This guarantees JSON can override defaults cleanly. fileciteturn6file0L100-L108

---

## Wiring it into the two tooltip systems

### A) Simple tooltips (Core/Pro menus & actions)
Attach short native tips **when building menus**. If an action represents a filter with a current value, compose the heading with affixes:

```python
# Inside your menu-building loop
value_str = current_value_for(label)   # e.g., "1.0" for Low-cut (Hz)
tipcfg = self._label_to_tipcfg.get(label, {})     # harvested from JSON
pre, suf = get_caption_affixes(key=key_for(label), label=label, tipcfg=tipcfg)
header = f"{pre}{value_str}{suf}" if (pre or suf) else label

desc = (tipcfg.get("tooltip") or {}).get("description") or ""
action.setToolTip(header if header != label else (desc or label))
```

**Why here?** Users hover these items **before** the lane exists; they need **instant hints** with minimal chrome.

### B) Gorgeous hover‑card (per combobox header)
Right after each `KandaDropdown` is created during lane rebuild, compute the card title and attach:

```python
# After creating dropdown 'dd' for logical key 'key' / human 'label'
tipcfg = self._params_map.get(key, {}).get("tooltip", {})
pre, suf = get_caption_affixes(key=key, label=label, tipcfg=tipcfg)
title = f"{pre}{current_value(dd)}{suf}" if (pre or suf) else (tipcfg.get("title") or label)

NeuroTooltipManager.apply_tooltip(dd, {"title": title, **tipcfg})
# Store guard/controller on widget so lane-clear can stop/hide/delete safely
dd._hover_tip_guard, dd._hover_tip_adapter = guard, adapter
```

**Why here?** Hover‑cards are **rich & contextual**; they belong to a real widget and can reflect **live values**.

---

## Extending at runtime (new filters)
You can add a rule on the fly so both systems get the same caption semantics:

```python
register_caption_rule(key="filter.bandpower.low.hz", prefix="Band Low ", suffix=" Hz")
register_caption_rule(label="Band High",               prefix="Band High ", suffix=" Hz")
```
This avoids scattering string concatenation logic across the UI. fileciteturn6file0L80-L89

---

## Migration & pitfalls
- Prefer `get_caption_affixes(...)`; keep `get_caption_affixes_compat(...)` only for old call‑sites. fileciteturn6file0L9-L11
- Avoid the deprecated `apply_caption_if_any` mutating patterns; the function now **returns** a rule and will be removed in the future. fileciteturn6file0L89-L100
- Be aware the **Notch** suffix is intentionally empty so labels like `"50 Hz + Hs"` render verbatim. Don’t append units twice. fileciteturn6file0L43-L53
- Always pass the **key** when available (more specific), but labels will still work due to normalization. fileciteturn6file0L108-L115

---

## Quick tests (suggested)
- Unit test priority: tipcfg headers > tipcfg captions > registry > empty.
- Snapshot a menu build and assert `QAction.toolTip()` contains `<prefix><value><suffix>` when value is known.
- UI test: build lane → hover a dropdown header → hover‑card title equals the same composed header.


