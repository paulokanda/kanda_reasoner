# update_dropdown_cmbbx_template_helper — Tooltip Wiring for the Middle‑Tab Combobox Lane

> You run **two tooltip systems**:
> 1) **Simple native tips** for the **button system** (Core/Pro menus & their actions).
> 2) **Gorgeous hover‑cards** attached **directly to each combobox header** in the lane.
>
> This helper extracts the *procedure* of rebuilding the lane (update‑dropdowns pipeline) while leaving *policy* (tooltips, debug hooks, dependency engine) in the template. It operates on a minimal `ctx` (the toolbar instance). fileciteturn14file0L1-L22

---

## What this module is responsible for

- Defines `update_dropdowns(ctx)` — a phased pipeline that clears the lane, builds every dropdown, sizes them, connects signals, refreshes headers, updates dependency state, and emits an initial snapshot. fileciteturn14file0L48-L80  
- Works only through the **context contract** (no direct template import): maps, active header selection, sizing flags, lane widgets/layout, and a set of hooks such as `_maybe_attach_caption`, `_emit_filter_change`, and `_after_dropdowns_rebuilt`. fileciteturn14file0L12-L45

**Why this matters for tooltips**  
- **Simple tips** (on Core/Pro menu actions) are **not** created here; menus live in the template/menu builders. This helper may **trigger menu rebuilds** when it coerces a valid selection (so your simple tips stay aligned), but it doesn’t attach them. fileciteturn14file0L108-L125  
- **Gorgeous hover‑cards** for **lane comboboxes** *are* wired here, centrally, during dropdown construction. fileciteturn14file0L167-L198

---

## Where each tooltip system plugs in

### 1) Simple native tips — Core/Pro menus (button system)
- Your simple tips are attached to **`QAction`s** when building Core/Pro menus in the template.  
- This helper only **coerces** a valid header/caret selection and then asks the template to **rebuild caret menus** (`_rebuild_core_caret_menu`, `_rebuild_pro_caret_menu`) if needed. That ensures the menu content (and your simple tips) match the active header, but the actual `action.setToolTip(...)` happens elsewhere. fileciteturn14file0L108-L124

### 2) Gorgeous hover‑cards — lane combobox headers (direct attach)
- In `_build_one_combo(...)`, after resolving `tipcfg`, if the config contains `"tooltip"`, the helper **enables hover prerequisites**, **disables the native Qt tooltip** (`setToolTip("")`), and **attaches the hover‑card** via `attach_core_filter_hover(combo, tipcfg, label)`. This is the central hook for your rich, animated cards. fileciteturn14file0L167-L198  
- The attachment is **universal** — any dropdown with tooltip data gets a card. The help‑center adapter (called here) stores guard/controller on the widget so your lane‑clear can stop/hide/delete safely. (The storing happens inside the adapter; this helper ensures the widget is prepared.) fileciteturn14file0L167-L198

---

## How tooltip data is found and normalized

- `_resolve_tipcfg(ctx, logical_key, label)` looks up tooltip config **first by key** (`ctx._key_to_tipcfg`) then **by label** (`ctx._label_to_tipcfg`). If an older flat format is detected (`description`/`docs` at the top level), it **upconverts** to `{"tooltip": ...}` so the attach logic stays consistent. fileciteturn14file0L271-L296  
- Each combo also gets a unique `tooltip_uid` (`<key>:<id(widget)>`) for debugging/tracing. fileciteturn14file0L244-L252

---

## Build pipeline (where hover‑cards are attached)

1) **Lifecycle begin** — primes dependency inputs. fileciteturn14file0L82-L92  
2) **Pairs** — computes Core & Pro label→items pairs, coercing a valid selection and **rebuilding caret menus** if necessary. fileciteturn14file0L94-L125  
3) **Prep lane** — clears the lane, freezes updates, inserts a left spacer. fileciteturn14file0L127-L137  
4) **Build** — for each `(label, items)` pair:  
   - create `KandaDropdown`, resolve `tipcfg`, and **attach hover‑card** if `"tooltip"` exists, disabling the native bubble first. fileciteturn14file0L147-L198  
   - size via `apply_fast_sizing`/`apply_precise_sizing` using `get_caption_affixes(...)`, populate items via `format_display_value(...)`, connect change signals, and attach the **ComboCaptionAdapter**. fileciteturn14file0L198-L244  
5) **Finalize lane visuals** — unfreeze updates, refresh headers, balance spacers, and force a repaint. fileciteturn14file0L212-L236  
6) **Dependencies & debug** — rebuild key index, apply dependency UI, schedule a wavelet on/off pass, and print debug. fileciteturn14file0L238-L269  
7) **Lifecycle end** — emit an initial snapshot and run the post‑hook. fileciteturn14file0L258-L269  
8) **Deferred layout recalculation** — a `QTimer.singleShot(200, ...)` that **re‑measures the lane** after all hover‑cards are attached; this prevents mis‑positioned cards on the first frame. fileciteturn14file0L59-L80

---

## Signal flow that keeps tooltips in sync

- Each combo connects to `ctx._emit_filter_change(label, combo)` and to `_on_any_dropdown_changed(...)`, so your template/controller can respond to value changes (e.g., **recompute a card title** or caption). The hover‑card adapter also listens to `currentIndexChanged` internally for **value‑aware** content. fileciteturn14file0L232-L244

---

## Interplay with simple tips (menus)

- When selection coercion happens, the helper calls `_rebuild_core_caret_menu()` and `_rebuild_pro_caret_menu()` so your **menu structure** and any **simple menu tooltips** (attached in the template) reflect the new active header. This helper **does not** attach simple tips itself. fileciteturn14file0L108-L125

---

## Practical checklist

- [ ] Keep `tipcfg` per dropdown (key‑ or label‑indexed); legacy shapes are auto‑upconverted. fileciteturn14file0L271-L296  
- [ ] Let this helper attach **gorgeous** hover‑cards automatically for any dropdown with `"tooltip"` in its `tipcfg`. fileciteturn14file0L167-L198  
- [ ] Attach **simple** tips to Core/Pro **menu actions** in the template/menu builders; rely on this helper’s caret‑menu rebuilds to keep them aligned. fileciteturn14file0L108-L125  
- [ ] Do not fight the native bubble: the helper disables `setToolTip` on combos when a hover‑card is attached. fileciteturn14file0L173-L182  
- [ ] Let the deferred layout recalc settle the lane before measuring/placing cards. fileciteturn14file0L59-L80


