# 🎛️ Tooltip, Button, Core / Lane Logic
**Version:** 2025‑10‑01 • **Author:** KANDA Docs • **Purpose:** Unified, practical guide to header *menus* (Core/Pro), lane *comboboxes*, SIMPLE tooltips, and GORGEOUS hover‑cards — with wiring patterns, diagrams, and code snippets.

---

## 0) TL;DR
- **Headers (Core/Pro)** = **Dual buttons with QMenus** → attach **SIMPLE tooltips** to actions/buttons.  
- **Lane entries** = **real QComboBox** (`KandaDropdown`) → attach **GORGEOUS hover‑cards** via `HoverTipAdapter`.  
- JSON (`core/pro`) drives **both** the header menus *and* the lane comboboxes to keep UX in lockstep.

---

## 1) Architecture at a Glance
```mermaid
flowchart LR
  subgraph Config
    C1[core.json]:::json
    C2[pro.json]:::json
    C3[tooltips.json]:::json
  end
  subgraph Loader
    L1[cmbbx_lane_json_loader.py<br/>load_all / load_lane_config]:::code
  end
  subgraph Middle Tab Controller
    M1[ComboFiltersTemplate]:::code
    M2[_rebuild_core/_pro_menus]:::code
    M3[update_dropdowns()]:::code
  end
  subgraph UI
    U1[DualArrowButton<br/>(Main/Pro)]:::ui
    U2[QMenu/QAction]:::ui
    U3[KandaDropdown<br/>(lane comboboxes)]:::ui
  end
  subgraph Tips
    T1[SIMPLE Qt tooltip<br/>on menus/actions]:::tips
    T2[GORGEOUS HoverCard<br/>via HoverTipAdapter]:::tips
  end

  C1 --> L1
  C2 --> L1
  C3 --> M1
  L1 --> M1
  M1 --> M2 --> U2
  M1 --> M3 --> U3
  U2 --> T1
  U3 --> T2

  classDef code fill:#0f172a,stroke:#67e8f9,color:#e2e8f0;
  classDef json fill:#111827,stroke:#93c5fd,color:#e5e7eb;
  classDef ui fill:#1f2937,stroke:#fca5a5,color:#fef3c7;
  classDef tips fill:#052e1d,stroke:#86efac,color:#dcfce7;
```
The **tooltip wire** uses a label/option mapping (e.g., `"Montage" → { "bipolar": "...", "average": "..." }`) to deliver instant hints and learning moments on hover. fileciteturn1file0L6-L12

---

## 2) Menus vs Comboboxes (Know the Difference)
| UI Area | Widget | What It Shows | How It’s Built | Tooltip Type |
|---|---|---|---|---|
| **Header: Core/Pro** | `DualArrowButton` + `QMenu/QAction` | Groups, sections, and commands | `_rebuild_core/_pro_menus` | **SIMPLE** Qt tooltip on `QAction` / buttons |
| **Lane (filters)** | `KandaDropdown` (`QComboBox`) | Actual filter values (e.g., Montage, Speed, Gain) | `update_dropdowns()` using loader maps | **GORGEOUS** HoverCard on combobox header |

### Why both come from JSON
- JSON entries `[label, [items]]` (or record objects) power **lane dropdowns**, while the same keys populate **header menus** for navigation and grouping. fileciteturn1file1L24-L39

---

## 3) Tooltip Wire (SIMPLE, for menus/actions)
**Concept:** map label/option to short strings, surfaced as native Qt tooltips on menu actions or header buttons.
```jsonc
{
  "Montage": {
    "bipolar": "Used for clinical EEGs.",
    "average": "Average of all channels as reference."
  }
}
```
On hover, lookups resolve by label/selected option:  
`tooltip = tooltip_manager.get_tooltip("Montage", selected_option)` fileciteturn1file0L8-L18

**Attach point:** when building menus:
```python
for action in menu.actions():
    tip = simple_tip_for(action.text())
    if tip:
        action.setToolTip(tip)
```
Use this for **Core/Pro header menus** (fast, native, non-intrusive).

---

## 4) Lane Combobox Logic (From JSON → KandaDropdown)
**Loader contract** (simplified):
```jsonc
{
  "direct": {
    "Sensitivity Settings": [
      { "label": "Speed", "items": ["5 mm/s","10 mm/s"] },
      { "label": "Gain",  "items": ["10 µV","20 µV"] }
    ]
  }
}
```
- Parsed by `cmbbx_lane_json_loader.py` into `direct_map`/`nested_map`, then rendered horizontally as **real `QComboBox` widgets** in the lane. fileciteturn1file1L24-L39

**Widget build sketch:**
```python
for label, items in section_entries:   # from direct_map["Sensitivity Settings"]
    dd = KandaDropdown()
    dd.addItems(items)
    lane_layout.addWidget(dd)
```
**Why lanes rock:** clear **param mappings** (e.g., Channel×Action, Sensor×Gain) and streamlined user flow across multiple related selectors. fileciteturn1file0L21-L37

---

## 5) GORGEOUS Hover‑Cards (for combobox headers)
**Design goal:** teach users *in place* (title, description, icon, examples) while they explore advanced options.
```python
HoverCard(
    title="Bandpass Filter",
    description="Removes slow drifts and high-frequency noise.",
    icon="filter_wave.svg",
    use_case="Best for cognitive EEG analysis."
)
```
**Attach to dropdown option:**
```python
dropdown.add_hover_card(option="Bandpass", hover_card=HoverCard(...))
```
This creates that *luxury, educational* feel on hover. fileciteturn1file0L53-L64

**Where the content comes from:**  
`tooltip_cmbbx_1_neurotooltips.json` (primary) with optional template fallbacks; value‑specific entries can override defaults. fileciteturn1file4L1-L8

---

## 6) HoverTipAdapter — Event Flow (step‑by‑step)
```mermaid
sequenceDiagram
  participant DD as KandaDropdown
  participant HA as HoverTipAdapter
  participant HC as HoverCard
  DD->>HA: installEventFilter(self)
  Note over HA: keeps cfg, label; prepares QTimer
  DD-->>HA: QEvent.Enter
  HA->>HA: start timer (≈350ms)
  HA->>HC: set_data(cfg[label]); move(x+offset,y); show()
  DD-->>HA: QEvent.Leave / MousePress / Wheel
  HA->>HC: hide(); stop timer
```
- **Attach:** `attach_core_filter_hover(combo, cfg, label="...")` → internally `HoverTipAdapter(widget=combo, config=cfg, label=label)`.  
- **Core:** installs `eventFilter`, starts delay on `Enter`, shows card, hides on `Leave/Click/Wheel`.  
- **Card fields:** title, description, formula, range, units, warning; CSS‑styled; themeable. fileciteturn1file4L9-L57

**Summary diagram (alternate view):**  
`KandaDropdown → attach_core_filter_hover → HoverTipAdapter: installEventFilter → start_timer → show HoverCard → hide on exit` fileciteturn1file2L3-L11

**Key features:** configurable delay, light/dark themes, safe teardown, smart formatting. fileciteturn1file2L13-L21

---

## 7) Practical Wiring Checklist
**Menus (SIMPLE):**
- Build Core/Pro menus; for each `QAction` → `setToolTip(...)` from your tip registry.  
- Optional: put a brief tooltip on the **DualArrowButton** itself (header hint).

**Lane (GORGEOUS):**
- After each `KandaDropdown` is created, call:  
  `attach_core_filter_hover(dropdown, tipcfg_for(label_or_key))`  
- If headers swap (Core↔Pro), re‑apply cards in place when lane is rebuilt.

---

## 8) Testing Matrix (what to verify)
- **JSON→lane:** each `[label, items]` becomes a `QComboBox` in expected order. fileciteturn1file1L24-L39  
- **Menus:** actions exist; tooltips appear on hover.  
- **Hover‑cards:** appear after delay; dismiss on leave/click; content matches label/option. fileciteturn1file4L33-L64  
- **UX polish:** lanes support clear param mapping (e.g., Channel×Action, Sensor×Gain). fileciteturn1file0L25-L37

---

## 9) Reference Snippets
**Lane mapping pattern:**
```python
LaneComboBox(
    label="Map Channel",
    lanes=[
        Dropdown("Input Channel", options=channel_names),
        Dropdown("Target Gain", options=[0.5, 1.0, 2.0])
    ]
)
```
Great for multi‑param flows; keeps user mental model intact. fileciteturn1file0L29-L37

**Menu tip attach (1‑liner):**
```python
for act in menu.actions():
    if (tip := tips.get(act.text())):
        act.setToolTip(tip)
```

---

## 10) What’s Next
- Auto‑generate hover‑card entries from domain docs (reduce drift).  
- Add image/mini‑graph support in cards for signal shapes.  
- Build a toggle to enable/disable hover‑cards per user preference. fileciteturn1file2L23-L30

