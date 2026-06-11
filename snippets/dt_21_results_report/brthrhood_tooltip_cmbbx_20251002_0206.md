# Group: tooltip_cmbbx

- Modules: **9**  |  Functions: **70**  |  Methods: **142**
- Module edges: **4**  |  Function edges: **7**

## Group Logic (Heuristic Summary)

Group **tooltip_cmbbx** logic overview:

- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_lane_json_loader.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **update_dropdowns** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:105 sig=(ctx) — Rebuild the dropdown lane (Core/Pro) from the current maps/selection
    • **_coerce_valid_selection_if_needed** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:169 sig=(ctx, core_pairs: Pairs, pro_pairs: Pairs) — Implements `_coerce_valid_selection_if_needed` logic.
    • **_build_all_combos** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:217 sig=(ctx, combined: Pairs) [insertion calls: ctx.dropdown_layout.addWidget] — Implements `_build_all_combos` logic.
    • **_build_one_combo** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:245 sig=(*, ctx, label: str, items: Sequence[str], use_fast_default: bool, char_buf: int, precise_keys: set, width_scale: float) (receives dict/list-like data) — Build, size, populate, connect, and decorate one QComboBox.
  - Widget insertion points:
    • **_build_all_combos** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:217 calls [ctx.dropdown_layout.addWidget]
  - Other data receivers (dict/list-like):
    • **_disp** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:454 sig=(x: object, key: str, label: str, tipcfg: Dict)
    • **_install_dynamic_tooltip** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py:471 sig=(combo: QComboBox, logical_key: str, label: str, pre: str, suf: str, tipcfg: Dict)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template** (`k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py`)
  - Canvas class: **ComboFiltersTemplate** at k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:296 bases=['QToolBar'] — JSON/maps-driven combobox toolbar
  - Dropdown builder(s):
    • **ComboFiltersTemplate.set_dropdown_width_scale** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:408 sig=(self, scale: float) — Implements `set_dropdown_width_scale` logic.
    • **ComboFiltersTemplate._after_dropdown_area_built** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:415 sig=(self, _main_layout) — Subclass hook to append extra chrome (arrows/presets/etc.) after the lane is built.
    • **ComboFiltersTemplate._setup_dropdown_area** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:420 sig=(self) [insertion calls: self.dropdown_scroll.setWidget] — Construct the scrollable lane that will hold the dropdowns
    • **ComboFiltersTemplate._setup_dropdown_area** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:458 sig=(self) — Implements `_setup_dropdown_area` logic.
    • **ComboFiltersTemplate._clear_dropdown_lane** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:461 sig=(self) — Implements `_clear_dropdown_lane` logic.
    • **ComboFiltersTemplate._on_core_main_selected** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:487 sig=(self, opt: str) — Implements `_on_core_main_selected` logic.
    • **ComboFiltersTemplate._on_core_caret_selected** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:490 sig=(self, sub: str) — Implements `_on_core_caret_selected` logic.
    • **ComboFiltersTemplate._on_pro_main_selected** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:493 sig=(self, opt: str) — Implements `_on_pro_main_selected` logic.
    • **ComboFiltersTemplate._on_pro_caret_selected** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:496 sig=(self, sub: str) — Implements `_on_pro_caret_selected` logic.
    • **ComboFiltersTemplate.update_dropdowns** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:513 sig=(self) — update logic for `update_dropdowns`.
    • **ComboFiltersTemplate._after_dropdowns_rebuilt** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:516 sig=(self) — Subclass hook invoked after dropdowns are fully rebuilt.
    • **ComboFiltersTemplate._on_any_dropdown_changed** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:525 sig=(self, changed_key: Optional[str]=None) — Implements `_on_any_dropdown_changed` logic.
    • **ComboFiltersTemplate._emit_filter_change** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:528 sig=(self, label: str, combo) — Implements `_emit_filter_change` logic.
    • **ComboFiltersTemplate.get_dropdown_values** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:531 sig=(self) — Implements `get_dropdown_values` logic.
    • **ComboFiltersTemplate._coerce_valid_selection** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:582 sig=(self) — Implements `_coerce_valid_selection` logic.
    • **ComboFiltersTemplate._update_wavelet_dependent_dropdowns** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:622 sig=(self) — Implements `_update_wavelet_dependent_dropdowns` logic.
    • **ComboFiltersTemplate._should_enable_dropdown** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:664 sig=(self, label: str) — Implements `_should_enable_dropdown` logic.
  - Widget insertion points:
    • **ComboFiltersTemplate._setup_dropdown_area** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:420 calls [self.dropdown_scroll.setWidget]
  - Other data receivers (dict/list-like):
    • **ComboFiltersTemplate._emit_initial_snapshot** @ k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py:522 sig=(self, built: list[tuple[str, object]])
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter** (`k05_combobox_forge\k05_4_cmbbx_constructor\dropdown_caption_formatter.py`)
  - Other data receivers (dict/list-like):
    • **CaptionRegistry.bulk_register** @ k05_combobox_forge\k05_4_cmbbx_constructor\dropdown_caption_formatter.py:143 sig=(self, *, keys: Mapping[str, CaptionRule] | None=None, labels: Mapping[str, CaptionRule] | None=None)
    • **get_caption_affixes** @ k05_combobox_forge\k05_4_cmbbx_constructor\dropdown_caption_formatter.py:177 sig=(*, key: Optional[str]=None, label: Optional[str]=None, tipcfg: Optional[Mapping]=None)
- Module **k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_middle_bar** (`k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py`)
  - Canvas class: **DrpdwnPanelMiddleBar** at k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:10 bases=['QToolBar'] — Middle lane for dropdown widgets with support for right-aligned widgets
  - Dropdown builder(s):
    • **DrpdwnPanelMiddleBar.add_dropdown** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:62 sig=(self, name: str, widget: QWidget) [insertion calls: self.dropdown_layout.addWidget] — Implements `add_dropdown` logic.
    • **DrpdwnPanelMiddleBar.remove_dropdown** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:77 sig=(self, name: str) — remove logic for `remove_dropdown`.
    • **DrpdwnPanelMiddleBar.clear_all_dropdowns** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:91 sig=(self) — Implements `clear_all_dropdowns` logic.
    • **DrpdwnPanelMiddleBar.show_dropdown** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:99 sig=(self, name: str) — Implements `show_dropdown` logic.
    • **DrpdwnPanelMiddleBar.hide_dropdown** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:103 sig=(self, name: str) — Implements `hide_dropdown` logic.
    • **DrpdwnPanelMiddleBar.show_all_dropdowns** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:115 sig=(self) — Implements `show_all_dropdowns` logic.
    • **DrpdwnPanelMiddleBar.hide_all_dropdowns** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:119 sig=(self) — Implements `hide_all_dropdowns` logic.
    • **DrpdwnPanelMiddleBar.show_dropdowns** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:132 sig=(self) — Implements `show_dropdowns` logic.
    • **DrpdwnPanelMiddleBar.hide_dropdowns** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:136 sig=(self) — Implements `hide_dropdowns` logic.
  - Widget insertion points:
    • **DrpdwnPanelMiddleBar._init_ui** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:28 calls [layout.addWidget, self.addWidget, self.dropdown_scroll.setWidget]
    • **DrpdwnPanelMiddleBar.add_dropdown** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:62 calls [self.dropdown_layout.addWidget]
    • **DrpdwnPanelMiddleBar.add_right_widget** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py:69 calls [self.right_layout.addWidget]
- Module **k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_tooltips** (`k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_tooltips.py`)
  - Other data receivers (dict/list-like):
    • **apply_eeg_tooltips_bulk** @ k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_tooltips.py:58 sig=(mapping: Dict[QWidget, str], *, dark_mode: Optional[bool]=None)
- Module **k06_templates.dropdown_templates** (`k06_templates\dropdown_templates.py`)
  - Canvas class: **KandaDropdownTemplates** at k06_templates\dropdown_templates.py:17 bases=['QWidget'] — Re-usable dropdown template with transparent hover effects
  - Dropdown builder(s):
    • **KandaDropdownTemplates._on_selection_change** @ k06_templates\dropdown_templates.py:90 sig=(self, index: int) — Implements `_on_selection_change` logic.
  - Widget insertion points:
    • **KandaDropdownTemplates._build_ui** @ k06_templates\dropdown_templates.py:77 calls [layout.addWidget]
  - Other data receivers (dict/list-like):
    • **KandaDropdownTemplates.set_items** @ k06_templates\dropdown_templates.py:118 sig=(self, label_value_pairs: list[tuple[str, object]], default_index: int=0)
    • **KandaDropdownTemplates.update_graph_options** @ k06_templates\dropdown_templates.py:157 sig=(self, graph_keys: list[str])
    • **TransparentItemDelegate.paint** @ k06_templates\dropdown_templates.py:167 sig=(self, painter, option, index)
    • **TransparentItemDelegate.sizeHint** @ k06_templates\dropdown_templates.py:184 sig=(self, option, index)
- Module **k06_templates.tooltip_lane_tmplt.hvr_card_widget** (`k06_templates\tooltip_lane_tmplt\hvr_card_widget.py`)
  - Canvas class: **GorgeousDetailDialog** at k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:223 bases=['QDialog'] — A modern, rich-content dialog for deep dives.
  - Canvas class: **GorgeousHoverCard** at k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:280 bases=['QWidget'] — Interactive, tooltip-like popup with link to detail dialog.
  - Canvas class: **DemoWindow** at k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:630 bases=['QWidget']
  - Widget insertion points:
    • **GorgeousDetailDialog.__init__** @ k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:226 calls [footer_layout.addWidget, layout.addWidget, scroll.setWidget]
    • **GorgeousHoverCard._setup_ui** @ k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:309 calls [btn_row.addWidget, layout.addWidget]
    • **DemoWindow.__init__** @ k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:631 calls [layout.addWidget]
  - Other data receivers (dict/list-like):
    • **GorgeousHoverCard.set_content** @ k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:353 sig=(self, data: Dict[str, str])
    • **HoverTipController.__init__** @ k06_templates\tooltip_lane_tmplt\hvr_card_widget.py:585 sig=(self, target: QWidget, card: GorgeousHoverCard, provider: Callable[[], Dict[str, str]])
- Module **k06_templates.tooltip_lane_tmplt.tooltip_help_center** (`k06_templates\tooltip_lane_tmplt\tooltip_help_center.py`)
  - Dropdown builder(s):
    • **_SafeHoverMediator.eventFilter** @ k06_templates\tooltip_lane_tmplt\tooltip_help_center.py:437 sig=(self, obj, ev) — Implements `eventFilter` logic.
    • **_PopupGuard.eventFilter** @ k06_templates\tooltip_lane_tmplt\tooltip_help_center.py:611 sig=(self, obj, ev) — Implements `eventFilter` logic.

Module connections (imports within group):
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k06_templates.tooltip_lane_tmplt.tooltip_help_center
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k06_templates.tooltip_lane_tmplt.tooltip_help_center

Cross-module function calls:
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_attach_hover_delayed → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._attach_hover_to_headers → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.update_dropdowns → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:<module>

## Modules
### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_lane_json_loader.py`
- **Imports**:
  - External: json, os
  - Aliases: json→json, os→os
- **Functions**
  - `_load_json(path)` (line 4) — Implements `_load_json` logic.
    - Calls (inter): open, json.load
  - `_resolve_includes(base_dir, node)` (line 8) — Implements `_resolve_includes` logic.
    - Calls (intra): _load_json, _resolve_includes, _resolve_includes, _resolve_includes
    - Calls (inter): isinstance, os.path.join, os.path.dirname, node.items, isinstance
  - `as_pairs(lst)` (line 27) — Implements `as_pairs` logic.
    - Calls (inter): list
  - `load_lane_config(json_path)` (line 19) — Returns (direct_map, nested_map) shaped exactly for FilterToolbar:   direct_map: { "X": [[label, [items]], ...], ..
    - Calls (intra): _resolve_includes, _load_json
    - Calls (inter): os.path.dirname, as_pairs, base.get, base.get, as_pairs, sub.items
  - `load_all(core_json, pro_json)` (line 37) — load logic for `load_all`.
    - Calls (intra): load_lane_config, load_lane_config

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\update_dropdown_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_forge_helpers.lane_pairs, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, k05_combobox_forge.k05_5_utils.combo_caption_adapter, k06_templates.tooltip_lane_tmplt.tooltip_help_center
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, logging, os, traceback, typing
  - Aliases: annotations→__future__, logging→logging, os→os, Dict→typing, List→typing, Sequence→typing, Tuple→typing, QTimer→PySide6.QtCore, QCoreApplication→PySide6.QtCore, QComboBox→PySide6.QtWidgets, QSpacerItem→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, pairs_for_lane→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_forge_helpers.lane_pairs, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, ComboCaptionAdapter→k05_combobox_forge.k05_5_utils.combo_caption_adapter, get_caption_affixes→k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, apply_fast_sizing→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, apply_precise_sizing→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, format_display_value→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, _looks_numeric→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, _ends_with_known_unit→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, apply_rich_tooltip→k06_templates.tooltip_lane_tmplt.tooltip_help_center, attach_hover_help→k06_templates.tooltip_lane_tmplt.tooltip_help_center, traceback→traceback
- **Functions**
  - `apply_rich_tooltip(widget, cfg: dict, *, dark_mode=None)` (line 70) — Implements `apply_rich_tooltip` logic.
    - Calls (inter): str, widget.setToolTip
  - `attach_hover_help(*_a, **_k)` (line 79) — Implements `attach_hover_help` logic.
  - `_force_layout_recalculation(ctx)` (line 88) — Force complete layout recalculation after hover cards are attached.
    - Calls (inter): ctx.dropdown_container.updateGeometry, ctx.dropdown_container.adjustSize, ctx.dropdown_scroll.updateGeometry, ctx._sync_chrome_heights, hasattr, hasattr, ctx.dropdown_layout.setStretch, ctx.dropdown_layout.setStretch, ctx.dropdown_layout.count, PySide6.QtCore.processEvents, print
  - `update_dropdowns(ctx)` (line 105) — Rebuild the dropdown lane (Core/Pro) from the current maps/selection [dropdown builder]
    - Calls (intra): _lifecycle_begin, _compute_lane_pairs, _coerce_valid_selection_if_needed, _prep_lane, _choose_active_pairs, _build_all_combos, _finalize_lane_visuals, _post_build_dependencies_and_debug, _lifecycle_end_and_emit, _force_layout_recalculation
    - Calls (inter): log.debug, PySide6.QtCore.singleShot, log.debug
  - `_lifecycle_begin(ctx)` (line 152) — Implements `_lifecycle_begin` logic.
    - Calls (inter): ctx._safe_compute_params_after_dependencies
  - `_pairs_for(main_key, caret_key, direct_map, nested_map)` (line 160) — Implements `_pairs_for` logic.
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_forge_helpers.lane_pairs
  - `_compute_lane_pairs(ctx)` (line 159) — Implements `_compute_lane_pairs` logic.
    - Calls (inter): _pairs_for, _pairs_for, log.debug, len, len
  - `_coerce_valid_selection_if_needed(ctx, core_pairs: Pairs, pro_pairs: Pairs)` (line 169) — Implements `_coerce_valid_selection_if_needed` logic. [dropdown builder]
    - Calls (intra): _compute_lane_pairs
    - Calls (inter): next, iter, next, iter, next, iter, next, iter, ctx._rebuild_core_caret_menu, ctx._rebuild_pro_caret_menu
  - `_prep_lane(ctx)` (line 197) — Implements `_prep_lane` logic.
    - Calls (inter): ctx._clear_dropdown_lane, ctx.dropdown_container.setUpdatesEnabled, PySide6.QtWidgets, PySide6.QtWidgets, ctx.dropdown_layout.addItem
  - `_choose_active_pairs(ctx, core_pairs: Pairs, pro_pairs: Pairs)` (line 205) — Implements `_choose_active_pairs` logic.
    - Calls (inter): getattr, combined.extend, combined.extend, log.debug, len, enumerate, log.debug, list
  - `_build_all_combos(ctx, combined: Pairs)` (line 217) — Implements `_build_all_combos` logic. [dropdown builder; insertion: ctx.dropdown_layout.addWidget]
    - Calls (intra): _build_one_combo
    - Calls (inter): bool, getattr, int, getattr, set, getattr, set, float, getattr, str, list, ctx.dropdown_layout.addWidget, built.append, str, ctx.dropdown_layout.addItem
  - `_build_one_combo(*, ctx, label: str, items: Sequence[str], use_fast_default: bool, char_buf: int, precise_keys: set, width_scale: float)` (line 245) — Build, size, populate, connect, and decorate one QComboBox. [receives data; dropdown builder]
    - Calls (intra): _resolve_tipcfg, _disp, _canon, _attach_hover_delayed
    - Calls (inter): print, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, combo.setFixedHeight, ctx._label_to_key.get, print, bool, print, list, tipcfg.keys, k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, combo.setSizePolicy, combo.clear, combo.addItem, tipcfg.get, combo.findData, combo.setCurrentIndex, combo.currentIndexChanged.connect, ctx._emit_filter_change, combo.currentIndexChanged.connect, ctx._on_any_dropdown_changed, cmb.property, ctx._maybe_attach_caption, getattr, getattr, isinstance, _adapter.set_fast_mode, _adapter.set_debounce_ms, _adapter.recompute_now, PySide6.QtCore.singleShot, a.set_debounce_ms, combo.setProperty, combo.setProperty, combo.setProperty, id, PySide6.QtCore.singleShot
  - `_attach_hover_delayed(combo, tipcfg, label)` (line 346) — Attach hover help after layout is complete.
    - Calls (inter): print, hasattr, str, int, os.getenv, int, os.getenv, os.getenv, k06_templates.tooltip_lane_tmplt.tooltip_help_center, print, print, print, traceback.print_exc
  - `_finalize_lane_visuals(ctx)` (line 376) — Implements `_finalize_lane_visuals` logic.
    - Calls (inter): ctx.dropdown_container.setUpdatesEnabled, ctx.dropdown_container.adjustSize, ctx.dropdown_scroll.updateGeometry, ctx._sync_chrome_heights, ctx._refresh_headers, ctx.dropdown_layout.activate, ctx.dropdown_container.updateGeometry, ctx.dropdown_layout.setStretch, ctx.dropdown_layout.setStretch, ctx.dropdown_layout.count, PySide6.QtCore.processEvents, ctx.dropdown_container.repaint
  - `_post_build_dependencies_and_debug(ctx)` (line 400) — Implements `_post_build_dependencies_and_debug` logic.
    - Calls (inter): ctx._rebuild_key_index, ctx._update_dependencies, PySide6.QtCore.singleShot, getattr, log.debug, ctx._debug_wavelet_state, ctx._debug_wavelet_dependencies, ctx._debug_label_to_tipcfg
  - `_lifecycle_end_and_emit(ctx, built)` (line 413) — Implements `_lifecycle_end_and_emit` logic.
    - Calls (inter): PySide6.QtCore.singleShot, ctx._emit_initial_snapshot, ctx._after_dropdowns_rebuilt
  - `_canon(v)` (line 421) — Coerce textual defaults to int/float when unambiguous; otherwise pass through.
    - Calls (inter): int, str, str, float
  - `_resolve_tipcfg(ctx, logical_key: str, label: str)` (line 435) — Resolve tooltip configuration for a specific dropdown.
    - Calls (inter): hasattr, dict, ctx._key_to_tipcfg.get, hasattr, dict, ctx._label_to_tipcfg.get, str
  - `_disp(x: object, key: str, label: str, tipcfg: Dict)` (line 454) — Display string formatter routed to canonical helper to keep rules in one place. [receives data]
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, str
  - `_curr_text(cmb: QComboBox)` (line 459) — Raw current value from ComboCaptionAdapter (if any) else combo text.
    - Calls (inter): getattr, getattr, isinstance, adapter.get_raw_current_text, cmb.currentText
  - `_refresh_header(_ix=None, cmb=combo, k=logical_key, lbl=str(label), base=base_cfg, tp=tipcfg)` (line 493) — Implements `_refresh_header` logic.
    - Calls (intra): _curr_text
    - Calls (inter): str, k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, tp.get, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, dict, k06_templates.tooltip_lane_tmplt.tooltip_help_center
  - `_install_dynamic_tooltip(combo: QComboBox, logical_key: str, label: str, pre: str, suf: str, tipcfg: Dict)` (line 471) — Keep the base Qt tooltip (small, immediate) updated to reflect the combo's current value, while the HoverCard shows richer delayed help. [receives data]
    - Calls (intra): _curr_text
    - Calls (inter): tipcfg.get, str, tipcfg.get, tipcfg.get, tipcfg.get, tipcfg.get, combo.currentIndexChanged.connect, _refresh_header

### k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template  
`k05_combobox_forge\k05_4_cmbbx_constructor\combobox_template.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_depend_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, k06_templates.tooltip_lane_tmplt.tooltip_help_center
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, cmbbx_template_helpers.reload_frm_maps_cmbbx_template_helper, cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper, logging, os, re, traceback, typing
  - Aliases: annotations→__future__, attach_hover_help→k06_templates.tooltip_lane_tmplt.tooltip_help_center, os→os, logging→logging, re→re, Dict→typing, List→typing, Optional→typing, Sequence→typing, Tuple→typing, Qt→PySide6.QtCore, QTimer→PySide6.QtCore, Signal→PySide6.QtCore, QToolBar→PySide6.QtWidgets, QPushButton→PySide6.QtWidgets, QComboBox→PySide6.QtWidgets, QHBoxLayout→PySide6.QtWidgets, QWidget→PySide6.QtWidgets, QMenu→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, QScrollArea→PySide6.QtWidgets, QFrame→PySide6.QtWidgets, QStyle→PySide6.QtWidgets, _upd_wavlt_deps→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_depend_cmbbx_template_helper, _update_dropdowns_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, _canon_bool_token_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _set_dropdown_width_scale_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _setup_ui_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _setup_dropdown_area_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _clear_dropdown_lane_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _setup_animations_helper→cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper, _rebuild_core_menus_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, _rebuild_core_caret_menu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, _rebuild_pro_menus_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, _rebuild_pro_caret_menu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, _style_qmenu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper, _reload_from_maps_helper→cmbbx_template_helpers.reload_frm_maps_cmbbx_template_helper, _update_wavlt_on_off→cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper, _apply_scale_sizes_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _set_initial_content_width_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _sync_chrome_heights_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _header_label_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _apply_header_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _refresh_headers_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _refresh_caret_highlight_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _on_resize_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper, _reload_from_json_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, _setup_option_data_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, _harvest_label_keys_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, _harvest_label_tooltips_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, _coerce_valid_selection_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper, _on_core_main_selected_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _on_core_caret_selected_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _on_pro_main_selected_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _on_pro_caret_selected_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _open_core_caret_menu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _open_pro_caret_menu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper, _canon_scalar_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, _check_condition_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, _should_enable_dropdown_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, _update_dependencies_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, _emit_initial_snapshot_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper, _on_any_dropdown_changed_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper, _emit_filter_change_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper, _get_dropdown_values_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper, _debug_wavelet_state_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper, _debug_wavelet_dependencies_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper, _debug_label_to_tipcfg_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper, _safe_compute_params_after_dependencies_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper, _find_items_for_label_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper, _maybe_attach_caption_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper, _refresh_lane_layout_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper, _apply_enabled_style_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper, _apply_disabled_style_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper, _rebuild_key_index_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper, _get_raw_value_for_key_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper, _looks_numeric→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper, _ends_with_known_unit→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper, _dep_check_condition→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper, _re→re, traceback→traceback
- **Functions**
  - `_looks_numeric(val: str)` (line 178) — Fallback: Return True if the string looks like a scalar number.
    - Calls (inter): str, bool, re.fullmatch
  - `_ends_with_known_unit(val: str)` (line 187) — Fallback: Guard against double-units in captions (Hz, dB, uV/ÂµV).
    - Calls (inter): str, bool, re.search
  - `_dep_check_condition(current_value: str, condition: dict)` (line 202) — Fallback: Evaluate condition (equals/in/not/truthy/numeric).
    - Calls (inter): str, str, condition.get, condition.get, any, str, str, condition.get, all, str, condition.get, condition.get, float, float, float, float, float
  - `_looks_numeric(val: str)` (line 247) — Return True if the string looks like a scalar number
    - Calls (inter): str, bool, re.fullmatch
  - `_ends_with_known_unit(val: str)` (line 262) — Guard against double-units in captions (Hz, dB, uV/ÂµV, optional suffix additions)
    - Calls (inter): str, bool, re.search
- **Classes**
  - `ComboFiltersTemplate` (QToolBar) (line 296) [canvas] — JSON/maps-driven combobox toolbar
    - `__init__(self, parent: Optional[QWidget]=None, *, scale: float=1.0, core_json: Optional[str]=None, pro_json: Optional[str]=None)` (line 313) — Construct a toolbar capable of showing a dynamic combobox lane
      - Calls (inter): super, float, self.setMovable, self.setSizePolicy, self._setup_ui, self._setup_animations, self._setup_option_data, self._rebuild_core_menus, self._rebuild_pro_menus, self._coerce_valid_selection, self.update_dropdowns, self._refresh_caret_highlight, self._refresh_headers, set, PySide6.QtCore.singleShot, PySide6.QtCore.singleShot, self._attach_hover_to_headers
    - `_canon_bool_token(v: object)` (line 404) — Implements `_canon_bool_token` logic.
      - Decorators: staticmethod
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `set_dropdown_width_scale(self, scale: float)` (line 408) — Implements `set_dropdown_width_scale` logic. [dropdown builder]
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `_setup_ui(self)` (line 412) — Implements `_setup_ui` logic.
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `_after_dropdown_area_built(self, _main_layout)` (line 415) — Subclass hook to append extra chrome (arrows/presets/etc.) after the lane is built. [dropdown builder]
    - `_setup_dropdown_area(self)` (line 420) — Construct the scrollable lane that will hold the dropdowns [dropdown builder; insertion: self.dropdown_scroll.setWidget]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, probe.addItem, probe.sizeHint, probe.deleteLater, PySide6.QtWidgets, self.dropdown_scroll.setWidgetResizable, self.dropdown_scroll.setHorizontalScrollBarPolicy, self.dropdown_scroll.setSizePolicy, self.dropdown_scroll.setFrameShape, self.dropdown_scroll.setFixedHeight, PySide6.QtWidgets, self.dropdown_container.setSizePolicy, PySide6.QtWidgets, self.dropdown_layout.setAlignment, self.dropdown_layout.setContentsMargins, self.dropdown_layout.setSpacing, self.dropdown_scroll.setWidget
    - `_setup_dropdown_area(self)` (line 458) — Implements `_setup_dropdown_area` logic. [dropdown builder]
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `_clear_dropdown_lane(self)` (line 461) — Implements `_clear_dropdown_lane` logic. [dropdown builder]
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `_setup_animations(self)` (line 465) — Implements `_setup_animations` logic.
      - Calls (inter): cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper
    - `_rebuild_core_menus(self)` (line 470) — Implements `_rebuild_core_menus` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
    - `_rebuild_core_caret_menu(self)` (line 473) — Implements `_rebuild_core_caret_menu` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
    - `_rebuild_pro_menus(self)` (line 476) — Implements `_rebuild_pro_menus` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
    - `_rebuild_pro_caret_menu(self)` (line 479) — Implements `_rebuild_pro_caret_menu` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
    - `_style_menu(self, menu: QMenu)` (line 482) — Implements `_style_menu` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
    - `_on_core_main_selected(self, opt: str)` (line 487) — Implements `_on_core_main_selected` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_on_core_caret_selected(self, sub: str)` (line 490) — Implements `_on_core_caret_selected` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_on_pro_main_selected(self, opt: str)` (line 493) — Implements `_on_pro_main_selected` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_on_pro_caret_selected(self, sub: str)` (line 496) — Implements `_on_pro_caret_selected` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_open_core_caret_menu(self)` (line 499) — Implements `_open_core_caret_menu` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_open_pro_caret_menu(self)` (line 502) — Implements `_open_pro_caret_menu` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_selection_handlers_cmbbx_template_helper
    - `_safe_compute_params_after_dependencies(self)` (line 506) — Implements `_safe_compute_params_after_dependencies` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper
    - `_find_items_for_label(self, label: str)` (line 509) — Implements `_find_items_for_label` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper
    - `update_dropdowns(self)` (line 513) — update logic for `update_dropdowns`. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper
    - `_after_dropdowns_rebuilt(self)` (line 516) — Subclass hook invoked after dropdowns are fully rebuilt. [dropdown builder]
    - `_emit_initial_snapshot(self, built: list[tuple[str, object]])` (line 522) — Implements `_emit_initial_snapshot` logic. [receives data]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
    - `_on_any_dropdown_changed(self, changed_key: Optional[str]=None)` (line 525) — Implements `_on_any_dropdown_changed` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
    - `_emit_filter_change(self, label: str, combo)` (line 528) — Implements `_emit_filter_change` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
    - `get_dropdown_values(self)` (line 531) — Implements `get_dropdown_values` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
    - `_apply_scale_sizes(self)` (line 535) — Implements `_apply_scale_sizes` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_set_initial_content_width(self, combo: QComboBox, key: str, label: str, tipcfg: dict)` (line 538) — Implements `_set_initial_content_width` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_sync_chrome_heights(self)` (line 541) — Implements `_sync_chrome_heights` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_sync_external_chrome_heights(self, _lane_h: int)` (line 544) — Subclass hook for arrows/presets sizing outside of this template
    - `resizeEvent(self, ev)` (line 550) — Implements `resizeEvent` logic.
      - Calls (inter): super, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_header_label(self, main: Optional[str], caret: Optional[str], *, is_core: bool)` (line 554) — Implements `_header_label` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_apply_header(self, button: QPushButton, full_text: str)` (line 557) — Implements `_apply_header` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_refresh_headers(self)` (line 560) — Implements `_refresh_headers` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `_refresh_caret_highlight(self)` (line 563) — Implements `_refresh_caret_highlight` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
    - `reload_from_json(self, core_json: Optional[str]=None, pro_json: Optional[str]=None)` (line 568) — Implements `reload_from_json` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
    - `_setup_option_data(self)` (line 571) — Implements `_setup_option_data` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
    - `_harvest_label_keys(self, json_path: str)` (line 574) — Implements `_harvest_label_keys` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
    - `_harvest_label_tooltips(self, json_path: str)` (line 578) — Implements `_harvest_label_tooltips` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
    - `_coerce_valid_selection(self)` (line 582) — Implements `_coerce_valid_selection` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
    - `reload_from_maps(self, *, core_direct: dict | None=None, core_nested: dict | None=None, pro_direct: dict | None=None, pro_nested: dict | None=None, core_main: str | None=None, pro_main: str | None=None, core_caret: str | None=None, pro_caret: str | None=None, maps_version: str | None=None)` (line 586) — Delegates to reload_frm_maps_cmbbx_template_helper.reload_from_maps
      - Calls (inter): cmbbx_template_helpers.reload_frm_maps_cmbbx_template_helper
    - `_maybe_attach_caption(self, combo, label: str)` (line 614) — Implements `_maybe_attach_caption` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper
    - `_refresh_lane_layout(self)` (line 617) — Implements `_refresh_lane_layout` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper
    - `_update_wavelet_dependent_dropdowns(self)` (line 622) — Implements `_update_wavelet_dependent_dropdowns` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_depend_cmbbx_template_helper
    - `_debug_wavelet_state(self)` (line 626) — Implements `_debug_wavelet_state` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper
    - `_debug_wavelet_dependencies(self)` (line 629) — Implements `_debug_wavelet_dependencies` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper
    - `_debug_label_to_tipcfg(self)` (line 632) — Implements `_debug_label_to_tipcfg` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper
    - `_apply_enabled_style(self, combo)` (line 636) — Implements `_apply_enabled_style` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper
    - `_apply_disabled_style(self, combo)` (line 642) — Implements `_apply_disabled_style` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper
    - `_rebuild_key_index(self)` (line 649) — Implements `_rebuild_key_index` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper
    - `_get_raw_value_for_key(self, logical_key: str)` (line 652) — Implements `_get_raw_value_for_key` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper
    - `_canon_scalar(v: object)` (line 657) — Implements `_canon_scalar` logic.
      - Decorators: staticmethod
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper
    - `_check_condition(self, current_value: str, condition: dict)` (line 661) — Implements `_check_condition` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper
    - `_should_enable_dropdown(self, label: str)` (line 664) — Implements `_should_enable_dropdown` logic. [dropdown builder]
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper
    - `_update_dependencies(self, controller_key: Optional[str]=None)` (line 667) — Implements `_update_dependencies` logic.
      - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper, log.debug
    - `_update_wavelet_on_off(self)` (line 674) — Implements `_update_wavelet_on_off` logic.
      - Calls (inter): cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper
    - `_attach_hover_to_headers(self)` (line 677) — Attach hover cards to both core and pro dropdown headers
      - Calls (inter): int, os.getenv, int, os.getenv, os.getenv, hasattr, k06_templates.tooltip_lane_tmplt.tooltip_help_center, print, print, hasattr, k06_templates.tooltip_lane_tmplt.tooltip_help_center, print, print, print, traceback.print_exc

### k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter  
`k05_combobox_forge\k05_4_cmbbx_constructor\dropdown_caption_formatter.py`
- **Imports**:
  - External: __future__, dataclasses, re, typing
  - Aliases: annotations→__future__, dataclass→dataclasses, re→re, Optional→typing, Mapping→typing, Tuple→typing
- **Functions**
  - `_norm(s: Optional[str])` (line 9) — Implements `_norm` logic.
    - Calls (inter): re.sub
  - `get_caption_affixes_compat(*, key: str, label: str, tipcfg: dict)` (line 13) — Implements `get_caption_affixes_compat` logic.
    - Calls (intra): get_caption_affixes
  - `find_caption_rule(label: Optional[str], key: Optional[str])` (line 16) — Implements `find_caption_rule` logic.
    - Calls (inter): _registry.match
  - `register_caption_rule(*, key: Optional[str]=None, label: Optional[str]=None, prefix: str='', suffix: str='')` (line 162) — Public helper to add rules at runtime (future dropdowns).
    - Calls (inter): _registry.register
  - `apply_caption_if_any(label: Optional[str], key: Optional[str], combo: object | None=None)` (line 167) — DEPRECATED behavior: previously mutated `combo`
    - Calls (inter): _registry.match
  - `get_caption_affixes(*, key: Optional[str]=None, label: Optional[str]=None, tipcfg: Optional[Mapping]=None)` (line 177) — Returns (prefix, suffix) to build a tooltip header like:  <prefix><option><suffix> [receives data]
    - Calls (inter): str, tipcfg.get, tipcfg.get, str, tipcfg.get, tipcfg.get, _registry.match
- **Classes**
  - `CaptionRule`  (line 20) — 
  - `CaptionRegistry`  (line 24) — 
    - `__init__(self)` (line 25) — Implements `__init__` logic.
      - Calls (intra): _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, _norm, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule, CaptionRule
      - Calls (inter): self._by_key.update, self._by_label.update
    - `register(self, *, key: Optional[str]=None, label: Optional[str]=None, prefix: str='', suffix: str='')` (line 135) — Implements `register` logic.
      - Calls (intra): CaptionRule, _norm, _norm
    - `bulk_register(self, *, keys: Mapping[str, CaptionRule] | None=None, labels: Mapping[str, CaptionRule] | None=None)` (line 143) — Implements `bulk_register` logic. [receives data]
      - Calls (intra): _norm, _norm
    - `match(self, *, key: Optional[str], label: Optional[str])` (line 150) — Implements `match` logic.
      - Calls (intra): _norm, _norm
      - Calls (inter): self._by_key.get, self._by_label.get

### k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_middle_bar  
`k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_middle_bar.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, typing
  - Aliases: annotations→__future__, Dict→typing, Qt→PySide6.QtCore, QPropertyAnimation→PySide6.QtCore, QPoint→PySide6.QtCore, Signal→PySide6.QtCore, QToolBar→PySide6.QtWidgets, QWidget→PySide6.QtWidgets, QHBoxLayout→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, QScrollArea→PySide6.QtWidgets, QPushButton→PySide6.QtWidgets
- **Classes**
  - `DrpdwnPanelMiddleBar` (QToolBar) (line 10) [canvas] — Middle lane for dropdown widgets with support for right-aligned widgets
    - `__init__(self, parent=None)` (line 17) — Implements `__init__` logic.
      - Calls (inter): super, self.setMovable, self._init_ui, self._init_state
    - `_init_state(self)` (line 25) — Implements `_init_state` logic.
    - `_init_ui(self)` (line 28) — Implements `_init_ui` logic. [insertion: layout.addWidget, self.addWidget, self.dropdown_scroll.setWidget]
      - Calls (inter): PySide6.QtWidgets, PySide6.QtWidgets, layout.setContentsMargins, layout.setSpacing, PySide6.QtWidgets, self.dropdown_scroll.setWidgetResizable, self.dropdown_scroll.setHorizontalScrollBarPolicy, self.dropdown_scroll.setFixedHeight, PySide6.QtWidgets, PySide6.QtWidgets, self.dropdown_layout.setContentsMargins, self.dropdown_layout.setSpacing, self.dropdown_scroll.setWidget, PySide6.QtWidgets, PySide6.QtWidgets, self.right_layout.setContentsMargins, self.right_layout.setSpacing, self.right_layout.addStretch, container.setSizePolicy, layout.addWidget, layout.addWidget, self.addWidget, self.hide_dropdowns
    - `add_dropdown(self, name: str, widget: QWidget)` (line 62) — Implements `add_dropdown` logic. [dropdown builder; insertion: self.dropdown_layout.addWidget]
      - Calls (inter): KeyError, widget.setVisible, self.dropdown_layout.addWidget
    - `add_right_widget(self, name: str, widget: QWidget)` (line 69) — Add a widget to the right side of the middle bar [insertion: self.right_layout.addWidget]
      - Calls (inter): KeyError, widget.setVisible, self.right_layout.addWidget
    - `remove_dropdown(self, name: str)` (line 77) — remove logic for `remove_dropdown`. [dropdown builder]
      - Calls (inter): self._dropdowns.pop, self.dropdown_layout.removeWidget, dd.setParent, dd.deleteLater
    - `remove_right_widget(self, name: str)` (line 84) — remove logic for `remove_right_widget`.
      - Calls (inter): self._right_widgets.pop, self.right_layout.removeWidget, widget.setParent, widget.deleteLater
    - `clear_all_dropdowns(self)` (line 91) — Implements `clear_all_dropdowns` logic. [dropdown builder]
      - Calls (inter): list, self._dropdowns.keys, self.remove_dropdown
    - `clear_all_right_widgets(self)` (line 95) — Implements `clear_all_right_widgets` logic.
      - Calls (inter): list, self._right_widgets.keys, self.remove_right_widget
    - `show_dropdown(self, name: str)` (line 99) — Implements `show_dropdown` logic. [dropdown builder]
    - `hide_dropdown(self, name: str)` (line 103) — Implements `hide_dropdown` logic. [dropdown builder]
    - `show_right_widget(self, name: str)` (line 107) — Implements `show_right_widget` logic.
    - `hide_right_widget(self, name: str)` (line 111) — Implements `hide_right_widget` logic.
    - `show_all_dropdowns(self)` (line 115) — Implements `show_all_dropdowns` logic. [dropdown builder]
      - Calls (inter): self._dropdowns.values, w.show
    - `hide_all_dropdowns(self)` (line 119) — Implements `hide_all_dropdowns` logic. [dropdown builder]
      - Calls (inter): self._dropdowns.values, w.hide
    - `show_all_right_widgets(self)` (line 123) — Implements `show_all_right_widgets` logic.
      - Calls (inter): self._right_widgets.values, w.show
    - `hide_all_right_widgets(self)` (line 127) — Implements `hide_all_right_widgets` logic.
      - Calls (inter): self._right_widgets.values, w.hide
    - `show_dropdowns(self)` (line 132) — Implements `show_dropdowns` logic. [dropdown builder]
      - Calls (inter): self.dropdown_scroll.show
    - `hide_dropdowns(self)` (line 136) — Implements `hide_dropdowns` logic. [dropdown builder]
      - Calls (inter): self.dropdown_scroll.hide

### k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_tooltips  
`k05_combobox_forge\k05_8_eeg_middle_tab_bar_cmbbx_lane\cmbbx_lane_tooltips.py`
- **Imports**:
  - Internal: k06_templates.tooltip_templates
  - External: PySide6.QtWidgets, __future__, typing
  - Aliases: annotations→__future__, Dict→typing, Any→typing, Optional→typing, QWidget→PySide6.QtWidgets, NeuroTooltipManager→k06_templates.tooltip_templates, ToolTipBinder→k06_templates.tooltip_templates
- **Functions**
  - `register_eeg_tooltips(*, replace: bool=False)` (line 43) — Implements `register_eeg_tooltips` logic.
    - Calls (inter): k06_templates.tooltip_templates.register_defaults
  - `set_eeg_tooltip_theme(dark_mode: bool)` (line 47) — Implements `set_eeg_tooltip_theme` logic.
    - Calls (inter): k06_templates.tooltip_templates.set_theme
  - `apply_eeg_tooltip(widget: QWidget, key: str, *, dark_mode: Optional[bool]=None, **overrides)` (line 51) — Implements `apply_eeg_tooltip` logic.
    - Calls (inter): cfg.update, k06_templates.tooltip_templates.apply_tooltip
  - `apply_eeg_tooltips_bulk(mapping: Dict[QWidget, str], *, dark_mode: Optional[bool]=None)` (line 58) — Implements `apply_eeg_tooltips_bulk` logic. [receives data]
    - Calls (inter): isinstance, isinstance, k06_templates.tooltip_templates.apply_tooltip
- **Classes**
  - `EEGLaneToolTipBinder` (ToolTipBinder) (line 67) — Drop-in helper for lanes/toolbars that want painless tooltip wiring

### k06_templates.dropdown_templates  
`k06_templates\dropdown_templates.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtGui, PySide6.QtWidgets, __future__, logging
  - Aliases: annotations→__future__, Qt→PySide6.QtCore, Signal→PySide6.QtCore, QTimer→PySide6.QtCore, QWidget→PySide6.QtWidgets, QComboBox→PySide6.QtWidgets, QVBoxLayout→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, QStyledItemDelegate→PySide6.QtWidgets, QStyle→PySide6.QtWidgets, QColor→PySide6.QtGui, QLinearGradient→PySide6.QtGui, QPainter→PySide6.QtGui, logging→logging
- **Classes**
  - `KandaDropdownTemplates` (QWidget) (line 17) [canvas] — Re-usable dropdown template with transparent hover effects
    - `__init__(self, parent: QWidget | None=None)` (line 68) — Implements `__init__` logic.
      - Calls (inter): super, self._build_ui
    - `_build_ui(self)` (line 77) — Implements `_build_ui` logic. [insertion: layout.addWidget]
      - Calls (intra): TransparentItemDelegate
      - Calls (inter): PySide6.QtWidgets, layout.setContentsMargins, PySide6.QtWidgets, self.dropdown.setEnabled, self.dropdown.setSizePolicy, self.dropdown.setSizeAdjustPolicy, self.dropdown.setStyleSheet, self.dropdown.currentIndexChanged.connect, self.dropdown.setItemDelegate, layout.addWidget
    - `_on_selection_change(self, index: int)` (line 90) — Implements `_on_selection_change` logic. [dropdown builder]
      - Calls (inter): self.dropdown.itemData, logging.debug, type, self.value_selected.emit, isinstance, logging.warning, tuple, hasattr, getattr, callable, self.on_selection_callback
    - `set_items(self, label_value_pairs: list[tuple[str, object]], default_index: int=0)` (line 118) — Implements `set_items` logic. [receives data]
      - Calls (inter): self.dropdown.clear, self.dropdown.setEnabled, max, self.dropdown.addItem, max, min, self.dropdown.count, self.dropdown.setCurrentIndex, self.dropdown.setEnabled, self._ensure_min_width, self.isVisible, PySide6.QtCore.singleShot
    - `_ensure_min_width(self)` (line 136) — Implements `_ensure_min_width` logic.
      - Calls (inter): self.dropdown.fontMetrics, fm.horizontalAdvance, self.dropdown.minimumWidth, self.dropdown.setMinimumWidth
    - `current_value(self)` (line 143) — Implements `current_value` logic.
      - Calls (inter): self.dropdown.currentData
    - `set_value(self, value)` (line 146) — Implements `set_value` logic.
      - Calls (inter): self.dropdown.findData, self.dropdown.setCurrentIndex
    - `enable(self)` (line 151) — Implements `enable` logic.
      - Calls (inter): self.dropdown.setEnabled
    - `disable(self)` (line 154) — Implements `disable` logic.
      - Calls (inter): self.dropdown.setEnabled
    - `update_graph_options(self, graph_keys: list[str])` (line 157) — update logic for `update_graph_options`. [receives data]
      - Calls (inter): self.set_items, key.replace
  - `TransparentItemDelegate` (QStyledItemDelegate) (line 164) — Delegate for transparent hover effect while maintaining all functionality
    - `paint(self, painter, option, index)` (line 167) — Implements `paint` logic. [receives data]
      - Calls (inter): super, painter.save, painter.setCompositionMode, painter.setBrush, PySide6.QtGui, painter.setPen, painter.drawRoundedRect, option.rect.adjusted, painter.restore, painter.setPen, PySide6.QtGui, painter.drawLine, option.rect.bottomLeft, option.rect.bottomRight
    - `sizeHint(self, option, index)` (line 184) — Implements `sizeHint` logic. [receives data]
      - Calls (inter): super, size.setHeight, size.height

### k06_templates.tooltip_lane_tmplt.hvr_card_widget  
`k06_templates\tooltip_lane_tmplt\hvr_card_widget.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtGui, PySide6.QtSvg, PySide6.QtWidgets, __future__, os, typing
  - Aliases: annotations→__future__, os→os, Callable→typing, Dict→typing, Optional→typing, Qt→PySide6.QtCore, QEvent→PySide6.QtCore, QTimer→PySide6.QtCore, QPoint→PySide6.QtCore, QEasingCurve→PySide6.QtCore, QPropertyAnimation→PySide6.QtCore, QRect→PySide6.QtCore, QObject→PySide6.QtCore, QSize→PySide6.QtCore, QRectF→PySide6.QtCore, QGuiApplication→PySide6.QtGui, QColor→PySide6.QtGui, QPalette→PySide6.QtGui, QIcon→PySide6.QtGui, QPixmap→PySide6.QtGui, QMouseEvent→PySide6.QtGui, QEnterEvent→PySide6.QtGui, QPainter→PySide6.QtGui, QWidget→PySide6.QtWidgets, QDialog→PySide6.QtWidgets, QVBoxLayout→PySide6.QtWidgets, QTextBrowser→PySide6.QtWidgets, QLabel→PySide6.QtWidgets, QPushButton→PySide6.QtWidgets, QHBoxLayout→PySide6.QtWidgets, QScrollArea→PySide6.QtWidgets, QGraphicsDropShadowEffect→PySide6.QtWidgets, QApplication→PySide6.QtWidgets, QToolButton→PySide6.QtWidgets, QStyle→PySide6.QtWidgets, QSvgRenderer→PySide6.QtSvg, QComboBox→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets
- **Classes**
  - `ThemeManager`  (line 98) — Manage light/dark themes for consistent gorgeous appearance
    - `__init__(self, mode: str='light')` (line 104) — Implements `__init__` logic.
      - Calls (inter): self.set_mode
    - `set_mode(self, mode: str)` (line 107) — Implements `set_mode` logic.
      - Calls (inter): PySide6.QtGui, PySide6.QtGui
    - `card_stylesheet(self)` (line 137) — Implements `card_stylesheet` logic.
      - Decorators: property
    - `detail_stylesheet(self)` (line 175) — Implements `detail_stylesheet` logic.
      - Decorators: property
  - `GorgeousDetailDialog` (QDialog) (line 223) [canvas] — A modern, rich-content dialog for deep dives.
    - `__init__(self, subject: str, parent: Optional[QWidget]=None, *, theme: Optional[ThemeManager]=None)` (line 226) — Implements `__init__` logic. [insertion: footer_layout.addWidget, layout.addWidget, scroll.setWidget]
      - Calls (intra): ThemeManager
      - Calls (inter): super, self.setWindowTitle, self.setMinimumSize, self.setWindowModality, PySide6.QtWidgets, layout.setSpacing, layout.setContentsMargins, PySide6.QtWidgets, header.setObjectName, layout.addWidget, PySide6.QtWidgets, self._browser.setOpenExternalLinks, PySide6.QtWidgets, scroll.setWidgetResizable, scroll.setWidget, layout.addWidget, PySide6.QtWidgets, PySide6.QtWidgets, footer_layout.addStretch, PySide6.QtWidgets, close_btn.setObjectName, close_btn.clicked.connect, footer_layout.addWidget, layout.addWidget, self.setStyleSheet, self._apply_shadow, self._theme.shadow.alpha
    - `setHtml(self, html: str)` (line 267) — Implements `setHtml` logic.
      - Calls (inter): self._browser.setHtml
    - `_apply_shadow(self, blur: int, dy: int, alpha: int)` (line 270) — Implements `_apply_shadow` logic.
      - Calls (inter): PySide6.QtWidgets, eff.setBlurRadius, eff.setColor, PySide6.QtGui, eff.setOffset, self.setGraphicsEffect
  - `GorgeousHoverCard` (QWidget) (line 280) [canvas] — Interactive, tooltip-like popup with link to detail dialog.
    - `__init__(self, parent: Optional[QWidget]=None, *, theme: Optional[ThemeManager]=None, detail_factory: Optional[Callable[[str, QWidget, ThemeManager], QDialog]]=None)` (line 283) — Implements `__init__` logic.
      - Calls (intra): ThemeManager, GorgeousDetailDialog
      - Calls (inter): super, self.setAttribute, self.setAttribute, self.setAttribute, self.setMouseTracking, self.setObjectName, self._setup_ui, self._setup_animations, self.setStyleSheet, self._apply_shadow, self._theme.shadow.alpha, os.environ.get, self._browser.anchorClicked.connect
    - `_setup_ui(self)` (line 309) — Implements `_setup_ui` logic. [insertion: btn_row.addWidget, layout.addWidget]
      - Calls (inter): PySide6.QtWidgets, layout.setContentsMargins, PySide6.QtWidgets, self._browser.setOpenExternalLinks, self._browser.setContextMenuPolicy, self._browser.setVerticalScrollBarPolicy, self._browser.setHorizontalScrollBarPolicy, self._browser.setAttribute, self._browser.setMouseTracking, layout.addWidget, PySide6.QtWidgets, btn_row.setContentsMargins, btn_row.addStretch, PySide6.QtWidgets, self._help_btn.setObjectName, self._help_btn.setAutoRaise, self._help_btn.setToolTip, self._help_btn.setIcon, self._load_help_icon, self._help_btn.setIconSize, PySide6.QtCore, self._help_btn.setSizePolicy, self._help_btn.clicked.connect, btn_row.addWidget, layout.addLayout
    - `_on_finish()` (line 348) — Implements `_on_finish` logic.
      - Calls (inter): self._fade_anim.direction, self.hide_immediate
    - `_setup_animations(self)` (line 341) — Implements `_setup_animations` logic.
      - Calls (inter): PySide6.QtCore, self._fade_anim.setDuration, self._fade_anim.setStartValue, self._fade_anim.setEndValue, self._fade_anim.setEasingCurve, self._fade_anim.finished.connect
    - `set_content(self, data: Dict[str, str])` (line 353) — Populate the card with new data from the provider. [receives data]
      - Calls (inter): data.get, data.get, data.get, data.get, getattr, self._browser.setHtml, self.adjustSize
    - `_load_help_icon(self)` (line 373) — Load doubt01.svg robustly
      - Calls (inter): os.path.dirname, os.path.abspath, os.environ.get, candidates.append, os.path.normpath, os.path.join, candidates.append, os.path.normpath, os.path.join, range, os.path.join, candidates.append, os.path.dirname, set, seen.add, os.path.exists, self._icon_from_svg, PySide6.QtGui, icon.isNull, self.style
    - `_icon_from_svg(self, path: str, *, target_px: int=54)` (line 426) — Render an SVG file to a pixmap at target size (accounts for devicePixelRatio), with caching and crisp scaling
      - Calls (inter): PySide6.QtGui, icon.isNull, self.style, getattr, setattr, hasattr, self.devicePixelRatioF, max, int, round, round, cache.get, isinstance, PySide6.QtSvg, rdr.isValid, RuntimeError, PySide6.QtGui, pm.fill, PySide6.QtGui, painter.setRenderHints, rdr.render, PySide6.QtCore, rdr.render, painter.end, pm.setDevicePixelRatio, PySide6.QtGui, PySide6.QtGui, icon.isNull, self.style
    - `_open_details_dialog(self)` (line 492) — Open the detail dialog; used by the bottom-right icon button.
      - Calls (inter): self.parent, PySide6.QtWidgets.activeWindow, self._detail_factory, dialog.setHtml, dialog.exec, print
    - `_on_link_clicked(self, url)` (line 502) — Open the detail dialog when link is clicked.
      - Calls (inter): url.toString, self.hide_immediate, self._open_details_dialog, print
    - `show_at(self, global_pos: QPoint)` (line 511) — Show the card near the given global position, with fade-in.
      - Calls (inter): self.isVisible, self.adjustSize, self._calculate_smart_position, self.move, target_rect.topLeft, self.setWindowOpacity, super, self.raise_, self._fade_anim.setDirection, self._fade_anim.start, self.setWindowOpacity, print
    - `hide_animated(self)` (line 530) — Fade out, then hide.
      - Calls (inter): self.isVisible, self.hide_immediate, self._fade_anim.setDirection, self._fade_anim.start, self.hide_immediate
    - `hide(self)` (line 543) — Implements `hide` logic.
      - Calls (inter): self.hide_animated
    - `hide_immediate(self)` (line 546) — Implements `hide_immediate` logic.
      - Calls (inter): self._fade_anim.stop, super
    - `enterEvent(self, event: QEnterEvent)` (line 553) — Implements `enterEvent` logic.
      - Calls (inter): super
    - `leaveEvent(self, event: QEvent)` (line 556) — Implements `leaveEvent` logic.
      - Calls (inter): super
    - `_apply_shadow(self, blur: int, dy: int, alpha: int)` (line 559) — Implements `_apply_shadow` logic.
      - Calls (inter): PySide6.QtWidgets, eff.setBlurRadius, eff.setColor, PySide6.QtGui, eff.setOffset, self.setGraphicsEffect
    - `_calculate_smart_position(self, pos: QPoint)` (line 566) — Stay within screen bounds.
      - Calls (inter): PySide6.QtGui.primaryScreen, self.sizeHint, pos.x, pos.y, card_size.width, screen_geo.right, pos.x, card_size.width, card_size.height, screen_geo.bottom, pos.y, card_size.height, PySide6.QtCore, PySide6.QtCore
  - `HoverTipController` (QObject) (line 580) — Passive bridge between a target widget, a GorgeousHoverCard, and a provider()
    - `__init__(self, target: QWidget, card: GorgeousHoverCard, provider: Callable[[], Dict[str, str]])` (line 585) — Implements `__init__` logic. [receives data]
      - Calls (inter): super, self._card.parent, self._card.setParent, target.window
    - `_calc_pos(self)` (line 593) — Implements `_calc_pos` logic.
      - Calls (inter): PySide6.QtCore, self._target.rect, self._target.mapToGlobal, rect.bottomLeft, PySide6.QtCore
    - `refresh(self)` (line 600) — Implements `refresh` logic.
      - Calls (inter): self._provider, self._card.set_content, print
    - `show(self)` (line 609) — Implements `show` logic.
      - Calls (inter): self.refresh, self._card.show_at, self._calc_pos
    - `hide(self)` (line 615) — Implements `hide` logic.
      - Calls (inter): self._card.hide
    - `stop(self)` (line 619) — Implements `stop` logic.
      - Calls (inter): self.hide
  - `DemoWindow` (QWidget) (line 630) [canvas] — 
    - `make_provider(t=title, s=summary)` (line 651) — Implements `make_provider` logic.
    - `__init__(self)` (line 631) — Implements `__init__` logic. [insertion: layout.addWidget]
      - Calls (intra): ThemeManager, GorgeousHoverCard, HoverTipController
      - Calls (inter): super, self.setWindowTitle, self.setGeometry, PySide6.QtWidgets, PySide6.QtWidgets, combo.addItems, make_provider, layout.addWidget

### k06_templates.tooltip_lane_tmplt.tooltip_help_center  
`k06_templates\tooltip_lane_tmplt\tooltip_help_center.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtGui, __future__, collections, hvr_card_widget, os, shiboken6, traceback, typing, weakref
  - Aliases: annotations→__future__, Any→typing, Dict→typing, Optional→typing, Callable→typing, weakref→weakref, Qt→PySide6.QtCore, QObject→PySide6.QtCore, QEvent→PySide6.QtCore, QTimer→PySide6.QtCore, QCoreApplication→PySide6.QtCore, QPoint→PySide6.QtCore, QRect→PySide6.QtCore, QCursor→PySide6.QtGui, shiboken6→shiboken6, ThemeManager→hvr_card_widget, GorgeousHoverCard→hvr_card_widget, HoverTipController→hvr_card_widget, OrderedDict→collections, os→os, traceback→traceback
- **Functions**
  - `_cache_get(key)` (line 41) — Implements `_cache_get` logic.
    - Calls (inter): _DETAIL_CACHE.get, hasattr, _DETAIL_CACHE.move_to_end
  - `_cache_put(key, value)` (line 49) — Implements `_cache_put` logic.
    - Calls (inter): hasattr, _DETAIL_CACHE.move_to_end, len, _DETAIL_CACHE.popitem
  - `_invalidate_detail_cache_for_widget(widget)` (line 57) — Remove all cached detail HTML entries for this widget.
    - Calls (inter): id, list, _DETAIL_CACHE.keys, isinstance, _DETAIL_CACHE.pop
  - `_hover_set_active(widget, controller, card)` (line 69) — Ensure only the given widget's hover is visible; hide the previous one.
    - Calls (inter): _active_hover.get, _active_hover.get, hasattr, prev_ctrl.hide
  - `_hover_clear_if(widget)` (line 85) — Clear active registry if it belongs to this widget.
    - Calls (inter): _active_hover.get
  - `_extract_tipdict(tipcfg: Any)` (line 96) — Implements `_extract_tipdict` logic.
    - Calls (inter): isinstance, isinstance, tipcfg.get, isinstance
  - `_plain_tooltip_text(tipcfg: Any, *, label: Optional[str])` (line 102) — Implements `_plain_tooltip_text` logic.
    - Calls (intra): _extract_tipdict
    - Calls (inter): t.get, str, isinstance, t.get
  - `apply_rich_tooltip(widget, tipcfg: Any, *, label: Optional[str]=None, dark_mode: Optional[bool]=None)` (line 111) — Always set a basic Qt tooltip from JSON so users get help even without HoverCard.
    - Calls (intra): _plain_tooltip_text
    - Calls (inter): widget.setToolTip
  - `_esc(s: Any)` (line 122) — Implements `_esc` logic.
    - Calls (inter): str, _HTML_ESCAPE.items, s.replace
  - `_current_item_text(widget)` (line 129) — Implements `_current_item_text` logic.
    - Calls (inter): widget.currentText
  - `_coerce_float(s: str)` (line 136) — Implements `_coerce_float` logic.
    - Calls (inter): float
  - `_note_for_value(tipcfg: Any, value_txt: str)` (line 143) — Implements `_note_for_value` logic.
    - Calls (intra): _extract_tipdict, _coerce_float
    - Calls (inter): value_txt.strip, t.get, isinstance, isinstance, str, str, rule.get, rule.get, rule.get, float, float, str, rule.get
  - `_summary_for_card(label: str, tipcfg: Any, widget)` (line 169) — Implements `_summary_for_card` logic.
    - Calls (intra): _plain_tooltip_text, _note_for_value, _current_item_text, _esc, _esc, _esc, _esc
  - `_detail_html(label: str, tipcfg: Any, widget)` (line 178) — Cached facade; HTML bytes are identical to _build_detail_html
    - Calls (intra): _current_item_text, _cache_get, _build_detail_html, _cache_put, _build_detail_html
    - Calls (inter): id, str
  - `_kv_list(d: dict)` (line 228) — Implements `_kv_list` logic.
    - Calls (intra): _esc, _esc, _esc, _esc
    - Calls (inter): d.items, isinstance, items.append, items.append
  - `_maybe_section(heading: str, html_body: str)` (line 238) — Implements `_maybe_section` logic.
    - Calls (intra): _esc
  - `_render_links(lnks)` (line 248) — Implements `_render_links` logic.
    - Calls (intra): _esc, _esc, _esc, _esc
    - Calls (inter): isinstance, isinstance, entry.get, out.append, entry.get, str, out.append
  - `_build_detail_html(label: str, tipcfg: Any, widget)` (line 197) — Build rich HTML for the detail dialog/hover content (non-cached)
    - Calls (intra): _extract_tipdict, _esc, _esc, _current_item_text, _esc, _note_for_value, _current_item_text, _current_item_text, _esc, _esc, _esc, _esc, _esc, _esc, _esc, _esc, _esc, _esc, _esc, _esc
    - Calls (inter): t.get, str, t.get, t.get, t.get, isinstance, t.get, t.get, isinstance, t.get, t.get, t.get, t.get, t.get, t.get, t.get, isinstance, docs.get, isinstance, block.items, isinstance, subrows.append, isinstance, _kv_list, subrows.append, subrows.append, list, docs.keys, rng.items, _kv_list, _kv_list, isinstance, isinstance, isinstance, isinstance, str, _render_links, table_rows.append, _maybe_section, table_rows.append, _maybe_section, table_rows.append, _maybe_section, table_rows.append, _maybe_section, table_rows.append, _maybe_section, table_rows.append, _maybe_section
  - `_is_valid_qobject(obj)` (line 362) — Check if a QObject is still valid and not destroyed.
    - Calls (inter): bool, shiboken6.isValid, obj.metaObject
  - `_app_closing()` (line 378) — Implements `_app_closing` logic.
    - Calls (inter): PySide6.QtCore.instance, bool, app.closingDown
  - `_install_popup_guards(widget, mediator: _SafeHoverMediator, controller, card)` (line 625) — Install guards on the combo's popup view to freeze hover while open.
    - Calls (intra): _PopupGuard
    - Calls (inter): hasattr, widget.view, view.installEventFilter
  - `provider()` (line 690) — Implements `provider` logic.
    - Calls (intra): _summary_for_card, _detail_html
    - Calls (inter): print, print, print, print, len
  - `_teardown(*_a)` (line 733) — Implements `_teardown` logic.
    - Calls (intra): _hover_clear_if, _invalidate_detail_cache_for_widget
    - Calls (inter): mediator.teardown, getattr, callable, fn, card.hide, card.deleteLater, hasattr, delattr
  - `attach_hover_help(widget, tipcfg: Any, *, label: Optional[str]=None, subject: Optional[str]=None, theme_mode: str='light', show_delay_ms: int=2000, hide_delay_ms: int=220, **_kwargs)` (line 644) — Attach a GorgeousHoverCard to `widget` with robust, deduped show/hide.
    - Calls (intra): apply_rich_tooltip, _wire_index_change_updates, _SafeHoverMediator, _safe_refresh, _install_popup_guards, _safe_refresh, _wire_index_change_updates, apply_rich_tooltip
    - Calls (inter): widget.setMouseTracking, widget.setAttribute, widget.setAttribute, getattr, hvr_card_widget, hvr_card_widget, hasattr, widget.window, card.setParent, card.setWindowFlags, card.setAttribute, card.setFocusPolicy, hvr_card_widget, max, widget.destroyed.connect, print, print, traceback.print_exc
  - `_safe_refresh(widget)` (line 787) — Implements `_safe_refresh` logic.
    - Calls (intra): _do_refresh
    - Calls (inter): PySide6.QtCore.singleShot
  - `_do_refresh(widget)` (line 794) — Implements `_do_refresh` logic.
    - Calls (inter): getattr, hasattr, controller.refresh
  - `_on_change(*_a, **_k)` (line 817) — Implements `_on_change` logic.
    - Calls (intra): _is_valid_qobject, _invalidate_detail_cache_for_widget, apply_rich_tooltip, _safe_refresh
    - Calls (inter): wref
  - `_wire_index_change_updates(widget, tipcfg: Any, label: Optional[str])` (line 803) — Keep the base Qt tooltip and HoverCard content in sync with combo selection
    - Calls (inter): getattr, callable, getattr, weakref.ref, sig.disconnect, sig.connect
- **Classes**
  - `_SafeHoverMediator` (QObject) (line 386) — Coalesces show/hide and dedupes calls
    - `__init__(self, widget, controller: QObject, card, *, show_delay_ms: int, hide_delay_ms: int, on_refresh: Optional[Callable[[], None]]=None)` (line 392) — Implements `__init__` logic.
      - Calls (inter): super, weakref.ref, weakref.ref, max, int, max, int, int, os.getenv, widget.installEventFilter, card.installEventFilter
    - `_alive(self)` (line 429) — Implements `_alive` logic.
      - Calls (intra): _is_valid_qobject
      - Calls (inter): self._wref
    - `_card(self)` (line 433) — Implements `_card` logic.
      - Calls (intra): _is_valid_qobject
      - Calls (inter): self._cref
    - `eventFilter(self, obj, ev)` (line 437) — Implements `eventFilter` logic. [dropdown builder]
      - Calls (inter): self._alive, self._card, ev.type, self._queue, setattr, self._do_show, self._check_and_hide, self._check_and_hide
    - `_check_and_hide(self)` (line 476) — Implements `_check_and_hide` logic.
      - Calls (inter): self._is_cursor_in_safe_zone, self._queue, max, int, self._queue, setattr, self._do_hide
    - `guarded()` (line 489) — Implements `guarded` logic.
      - Calls (inter): fn
    - `_queue(self, fn: Callable, ms: int)` (line 486) — Implements `_queue` logic.
      - Calls (inter): PySide6.QtCore.singleShot
    - `_global_rect(self, obj)` (line 495) — Implements `_global_rect` logic.
      - Calls (inter): obj.mapToGlobal, PySide6.QtCore, PySide6.QtCore, obj.size, PySide6.QtCore
    - `_is_cursor_in_safe_zone(self)` (line 503) — Implements `_is_cursor_in_safe_zone` logic.
      - Calls (inter): self._alive, self._card, card.isVisible, self._global_rect, self._global_rect, wr.isValid, cr.isValid, wr.united, union.adjust, union.contains, PySide6.QtGui.pos
    - `_do_show(self)` (line 519) — Implements `_do_show` logic.
      - Calls (intra): _app_closing, _hover_set_active
      - Calls (inter): self._alive, self._card, widget.isVisible, widget.isEnabled, widget.underMouse, card.isVisible, card.underMouse, getattr, hasattr, self._ctrl.show, hasattr, self._ctrl.start, callable, self._on_refresh
    - `_do_hide(self)` (line 552) — Implements `_do_hide` logic.
      - Calls (intra): _hover_clear_if, _app_closing
      - Calls (inter): self._alive, self._card, hasattr, self._ctrl.hide, hasattr, self._ctrl.stop
    - `set_frozen(self, frozen: bool)` (line 571) — Implements `set_frozen` logic.
      - Calls (inter): bool
    - `teardown(self)` (line 574) — Implements `teardown` logic.
      - Calls (inter): self._alive, widget.removeEventFilter, self._card, card.removeEventFilter, self._do_hide
  - `_PopupGuard` (QObject) (line 592) — Freezes the mediator while the QComboBox popup is open
    - `__init__(self, widget, mediator: _SafeHoverMediator, controller, card)` (line 597) — Implements `__init__` logic.
      - Calls (inter): super, weakref.ref, weakref.ref, weakref.ref
    - `_freeze(self, yes: bool)` (line 605) — Implements `_freeze` logic.
      - Calls (inter): self._mref, m.set_frozen
    - `eventFilter(self, obj, ev)` (line 611) — Implements `eventFilter` logic. [dropdown builder]
      - Calls (inter): ev.type, getattr, getattr, self._freeze, hasattr, self._ctrl.hide, getattr, PySide6.QtCore.singleShot, self._freeze

## Module Dependencies
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k06_templates.tooltip_lane_tmplt.tooltip_help_center
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k06_templates.tooltip_lane_tmplt.tooltip_help_center

## Cross-Module Function Calls
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_attach_hover_delayed → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._attach_hover_to_headers → k06_templates.tooltip_lane_tmplt.tooltip_help_center:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.update_dropdowns → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:<module>

