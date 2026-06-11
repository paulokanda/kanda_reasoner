# 🌈 `cmbbx_lane_json_loader.py` — What Is It For?
**Source‑of‑truth mapper** from **JSON ➜ in‑memory maps** used by the **Middle Tab** to build:
1) the **button‑system menus** (“Main/Pro Filters” — where your *simple Qt tooltips* live)  
2) the **lane’s combobox list** (each dropdown — where your *gorgeous hover‑card* attaches)

It resolves `$include` recursively, shapes the data for both consumers, and returns precisely what the UI expects — clean, predictable maps.

---

## 🗺️ Where It Sits in the Pipeline
```mermaid
flowchart LR
  J[JSON configs<br/>(core.json, pro.json, includes...)] --> R[$include Resolver<br/>(deep, recursive)]
  R --> S[Shaper<br/>(direct/nested sections)]
  S -->|load_lane_config| M1[direct_map]
  S -->|load_lane_config| M2[nested_map]
  J -->|load_all| A[(core_direct, core_nested,<br/>pro_direct, pro_nested)]
  M1 --> MEN[Header Buttons Menus<br/>(Main/Pro)]
  M2 --> MEN
  M1 --> LANE[Lane Builder<br/>(Combobox list)]
  M2 --> LANE
```
The loader **feeds both the menus and the lane** so they are always in sync.

---

## ⚙️ Core Mechanics (Contract)
### `$include` — deep & recursive
- Allowed **anywhere** in JSON (objects or arrays).  
- Lets you split **large configs** or **tooltip payloads** across files.  
- The loader returns a **fully materialized tree** *before* shaping.

### `load_lane_config(path)` ➜ two maps
- `direct_map: { "Section": [[label, [items]], ...] }`  
- `nested_map: { "Group": {"Subgroup": [[label, [items]], ...], ...} }`  
  - Each `items` list contains **combobox ids** used to instantiate dropdowns in the lane.

### `load_all(core_json, pro_json)` ➜ four maps
- `(core_direct, core_nested, pro_direct, pro_nested)`  
  - Designed to plug straight into your two **header buttons**: **Main** and **Pro**.

---

## 🧩 How It Ties to Your Two Tooltip Systems
### 1) Simple tooltip (button system: menus & actions)
- “Main Filters” & “Pro Filters” menus are built from the **core/pro direct/nested** maps.
- Each `[label, items]` pair becomes a **QAction** (or submenu entry).
- **Attach simple Qt tooltip here**: `action.setToolTip("…")` — users hover before spawning a lane.

> Today, the loader often **flattens** entries to `[label, [items]]` via `as_pairs(...)`.  
> Side‑effect: any extra fields (e.g., per‑menu tooltip) are **dropped**.

### 2) Gorgeous hover‑card (lane combobox header)
- Every string inside `items` is the **dropdown id** to render in the scroll lane.
- **Attach hover‑card here**: after the dropdown widget exists, e.g.  
  `attach_hover_card(dropdown, meta)`.
- Thanks to `$include`, you can keep **rich hover content** (title/body, md/HTML snippets, quick‑facts) in separate JSON files and **include by id** — *as long as the loader preserves that metadata*.

---

## 📦 Two Clean Ways to Carry Tooltip Metadata
### Option A — Minimal change (recommended)
**Add optional** `"tip"` / `"hover"` fields and keep backward‑compatibility.

#### JSON (example)
```jsonc
{
  "direct": {
    "Time": [
      { "label": "Window", "items": ["tw_5", "tw_10", "tw_20"], "tip": "Select time window", 
        "hover": { "$include": "tips/time_window_hover.json" } }
    ]
  }
}
```

#### Loader sketch (drop‑in)
```python
# inside load_lane_config(...)
def as_records(lst):
    out = []
    for entry in lst:
        lab   = entry["label"]
        items = list(entry["items"])
        tip   = entry.get("tip")      # simple tooltip for menu entry
        hover = entry.get("hover")    # default hover meta for each item
        out.append({"label": lab, "items": items, "tip": tip, "hover": hover})
    return out

direct_map = {k: as_records(v) for k, v in (base.get("direct") or {}).items()}
nested_map = {A: {B: as_records(L) for B, L in sub.items()}
              for A, sub in (base.get("nested") or {}).items()}
```

#### UI usage
```python
# Menu builder (SIMPLE tooltip)
for rec in direct_map["Time"]:
    action = menu.addAction(rec["label"])
    if rec.get("tip"):
        action.setToolTip(rec["tip"])

# Lane builder (GORGEOUS hover-card)
for item_id in rec["items"]:
    dd = make_dropdown(item_id)
    attach_hover_card(dd, rec.get("hover"), item_id)
```

**Why Option A is nicer**
- **Fewer lookups, no drift** — config that defines the lane also carries its tips.  
- **Backward‑compatible** — treat `"tip"` / `"hover"` as optional; old JSON remains valid.

---

### Option B — Zero API change, use a parallel `TooltipRegistry`
Keep loader untouched; maintain a `tooltips.json` keyed by **menu labels** and **item ids**.

#### tooltips.json (example)
```json
{
  "SimpleTips": {
    "Window": "Select time window"
  },
  "HoverCards": {
    "tw_5":   { "$include": "tips/time_5s.json" },
    "tw_10":  { "$include": "tips/time_10s.json" },
    "tw_20":  { "$include": "tips/time_20s.json" }
  }
}
```

#### UI join (concept)
```python
# Menu tips
action.setToolTip(SimpleTips.get(label))

# Lane cards
attach_hover_card(dd, HoverCards.get(item_id), item_id)
```

**Pros**: Works **today** using `$include`; no loader change.  
**Cons**: Extra join logic and risk of **drift** between config and tips.

---

## 🔒 Guardrails & Edge Cases (already handled)
- **Deep includes**: giant tooltip bodies live in dedicated files; the resolver returns a **fully expanded** tree before shaping.
- **Core vs Pro**: `load_all(...)` delivers clean **separation** for the two header buttons; you can keep different tone/complexity across tiers.
- **Strict shapes**: the direct/nested contract ensures menu and lane builders consume **predictable** structures.

---

## 🧪 Example: Minimal Core JSON
```jsonc
{
  "$include": ["includes/common_groups.json"],
  "direct": {
    "Time": [
      ["Window", ["tw_5", "tw_10", "tw_20"]]
    ],
    "Amplitude": [
      ["Scale", ["amp_1", "amp_2", "amp_5", "amp_10"]]
    ]
  },
  "nested": {
    "Frequency": {
      "Bands": [
        ["Delta-Theta", ["f_dt_overlay", "f_dt_power"]],
        ["Alpha-Beta", ["f_ab_overlay", "f_ab_power"]]
      ]
    }
  }
}
```
> With **Option A**, the list entries can be objects carrying `"tip"` and `"hover"` without breaking old configs.

---

## 🧰 Quick Mapping You Can Implement Immediately
SIMPLE tips — assign on **QActions** created from each `[label, items]` in **Main/Pro menus**.  
GORGEOUS tips — after each `KandaDropdown` is created for an `item_id`, call  
`attach_hover_card(dropdown, hover_meta_for(item_id))` and **store the guard/controller on the widget** (so lane‑clear teardown can stop & delete them safely).

**Teardown hint**: mirror your existing “safe cleanup” pattern: attach `_hover_tip_guard` / `_hover_tip_adapter` attributes and clear them during lane reset.

---

## 🧭 API Summary
- `load_lane_config(path) -> (direct_map, nested_map)`  
- `load_all(core_json, pro_json) -> (core_direct, core_nested, pro_direct, pro_nested)`

**Shapes**
- `direct_map: { Section: [[label, [items]], ...] }` *(or records if Option A)*  
- `nested_map: { Group: { Subgroup: [[label, [items]], ...] } }` *(or records if Option A)*

---

## ⚡ Performance Notes
- `$include` resolution is **linear in the number of nodes**; cache included fragments if your configs get very deep.  
- Prefer **Option A** for fewer lookups at runtime; Option B pushes work to UI join stage.

---

## 🧪 Testing Checklist
- **Includes**: nested `$include` in arrays and objects resolve correctly.  
- **Shapes**: both **direct** and **nested** maps match expected shapes.  
- **Menus**: all sections/subsections produce the right **QActions**.  
- **Lane**: every `item_id` spawns a dropdown; hover‑card attaches without leaks.  
- **Back‑compat**: legacy pair‑lists load; new objects with `"tip"`/`"hover"` load.  
- **Error Paths**: missing include file, unknown item id, invalid shape ➜ helpful exceptions.

---

## ✅ TL;DR
`cmbbx_lane_json_loader.py` is the **single source of truth** that turns JSON into the exact maps your **menus** and **lane comboboxes** need — with deep `$include` support and a clean path (Option A) to carry both **simple Qt tooltips** and **gorgeous hover‑cards** from the same configuration.

