# Group: combobox_template

- Modules: **24**  |  Functions: **119**  |  Methods: **73**
- Module edges: **23**  |  Function edges: **47**

## Group Logic (Heuristic Summary)

Group **combobox_template** logic overview:

- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_lane_json_loader.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.caption_format_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\caption_format_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_caption_adapter_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_debug_helpers_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_dependency_engine_iface_cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **should_enable_dropdown** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_dependency_engine_iface_cmbbx_template_helper.py:47 sig=(ctx, label: str) — Decide enable/disable for a dependent dropdown identified by its label.
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_dependency_helpers_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **on_any_dropdown_changed** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py:33 sig=(ctx, changed_key: Optional[str]=None) — Generic change handler to recompute dependent dropdown states
    • **emit_filter_change** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py:48 sig=(ctx, label: str, combo) — Emit the filterChanged signal for a given combobox, then kick dependency updates.
    • **get_dropdown_values** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py:75 sig=(ctx) — Return the *raw* values for all dropdowns (keyed by 'logical_key::label').
  - Other data receivers (dict/list-like):
    • **emit_initial_snapshot** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py:25 sig=(ctx, built: List[Tuple[str, object]])
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_key_index_and_values_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_menus_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_option_loading_cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **_process_filter_config** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_option_loading_cmbbx_template_helper.py:124 sig=(ctx, filter_config: dict) (receives dict/list-like data) — Process a single filter configuration and extract tooltip data.
    • **coerce_valid_selection** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_option_loading_cmbbx_template_helper.py:155 sig=(ctx) — Ensure core/pro main and caret selections are valid, rebuild caret menus if needed.
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_sizing_headers_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_style_helpers_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **set_dropdown_width_scale** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py:49 sig=(ctx, scale: float) — Adjust how aggressively dropdown widths are clamped and rebuild the lane
    • **setup_dropdown_area** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py:109 sig=(ctx) [insertion calls: ctx.dropdown_scroll.setWidget] — Construct the scrollable row that will hold the dropdowns
    • **clear_dropdown_lane** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py:141 sig=(ctx) — Remove all widgets/spacers from the dropdown lane and clear the registry
  - Widget insertion points:
    • **setup_ui** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py:58 calls [ctx.addWidget, main_layout.addWidget]
    • **setup_dropdown_area** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py:109 calls [ctx.dropdown_scroll.setWidget]
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py`)
  - Dropdown builder(s):
    • **should_enable_dropdown** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:226 sig=(label: str, *, label_to_tipcfg: Mapping[str, dict], get_raw_value_for_key: Callable[[str], str], check_condition: Callable[[str, Mapping[str, Any]], bool]=check_condition) (receives dict/list-like data) — Decide whether a dropdown should be enabled based on its tipcfg
  - Widget insertion points:
    • **rebuild_main_menu** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:348 calls [menu.addAction]
    • **rebuild_caret_menu** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:379 calls [menu.addAction]
  - Other data receivers (dict/list-like):
    • **apply_fast_sizing** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:42 sig=(combo: QComboBox, *, items: Iterable[Any], display_value: Callable[[Any], str]=lambda x: str(x), char_buffer: int=3, width_scale: float=0.6)
    • **apply_precise_sizing** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:77 sig=(combo: QComboBox, *, items: Iterable[Any], display_value: Callable[[Any], str]=lambda x: str(x), px_padding: int=32, width_scale: float=0.6, min_px: int=64)
    • **check_condition** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:171 sig=(current_value: str, condition: Mapping[str, Any])
    • **update_dependencies_engine** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:261 sig=(dropdowns: Mapping[str, QComboBox], *, label_to_tipcfg: Mapping[str, dict], controller_key: Optional[str], get_raw_value_for_key: Callable[[str], str], apply_enabled_style: Callable[[QComboBox], None], apply_disabled_style: Callable[[QComboBox], None], canon_bool_token: Callable[[Any], str], logger: Optional[logging.Logger]=None)
    • **rebuild_caret_menu** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:379 sig=(menu: QMenu, *, main_key: Optional[str], nested_map: Mapping[str, Mapping[str, Any]], on_caret_selected: Callable[[str], None])
    • **find_items_for_label** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py:516 sig=(*, label: str, core_direct_map: Mapping[str, Pairs], core_nested_map: Mapping[str, Mapping[str, Pairs]], pro_direct_map: Mapping[str, Pairs], pro_nested_map: Mapping[str, Mapping[str, Pairs]])
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.delegate_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\delegate_cmbbx_template_helper.py`)
  - Other data receivers (dict/list-like):
    • **TransparentItemDelegate.paint** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\delegate_cmbbx_template_helper.py:84 sig=(self, painter: QPainter, option: QStyleOptionViewItem, index)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\dependency_eval_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.lane_items_lookup_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\lane_items_lookup_cmbbx_template_helper.py`)
  - Other data receivers (dict/list-like):
    • **_items_from_listdef** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\lane_items_lookup_cmbbx_template_helper.py:15 sig=(lst: Sequence[dict])
    • **find_items_for_label** @ k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\lane_items_lookup_cmbbx_template_helper.py:30 sig=(label: str, *, core_direct_map: Mapping[str, Sequence[dict]], core_nested_map: Mapping[str, Mapping[str, Sequence[dict]]], pro_direct_map: Mapping[str, Sequence[dict]], pro_nested_map: Mapping[str, Mapping[str, Sequence[dict]]])
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\updat_wavlt_on_off_cmbbx_template_helper.py`)
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
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\value_text_utils_cmbbx_template_helper.py`)
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper** (`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\widgets_cmbbx_template_helper.py`)
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
- Module **k05_combobox_forge.k05_4_cmbbx_constructor.filters_controller** (`k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py`)
  - Other data receivers (dict/list-like):
    • **_check_atomic** @ k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py:34 sig=(key: str, spec: Any, params: Dict[str, Any])
    • **_check_condition** @ k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py:61 sig=(cond: Dict[str, Any], params: Dict[str, Any])
    • **_apply_dependencies** @ k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py:64 sig=(params: Dict[str, Any], deps: List[Dict[str, Any]])
    • **_apply_dependency_ui** @ k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py:82 sig=(self, params_after_deps: Dict[str, Any])

Module connections (imports within group):
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper

Cross-module function calls:
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:maybe_attach_caption → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:_extract_tooltip_configurations → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:setup_option_data → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:set_initial_content_width → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper:setup_dropdown_area → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_disabled_style → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_enabled_style → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_header → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_scale_sizes → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._canon_scalar → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._check_condition → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._coerce_valid_selection → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_label_to_tipcfg → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_wavelet_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_wavelet_state → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._emit_filter_change → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._emit_initial_snapshot → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._find_items_for_label → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._get_raw_value_for_key → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._harvest_label_keys → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._harvest_label_tooltips → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._header_label → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._maybe_attach_caption → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._on_any_dropdown_changed → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_core_caret_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_core_menus → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_key_index → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_pro_caret_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_pro_menus → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_caret_highlight → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_headers → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_lane_layout → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._safe_compute_params_after_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._set_initial_content_width → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._setup_dropdown_area → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._setup_option_data → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._should_enable_dropdown → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._style_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._sync_chrome_heights → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._update_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.get_dropdown_values → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.reload_from_json → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.resizeEvent → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
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

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.caption_format_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\caption_format_cmbbx_template_helper.py`
- **Imports**:
  - External: __future__, typing, value_text_utils_cmbbx_template_helper
  - Aliases: annotations→__future__, Any→typing, Optional→typing, looks_numeric→value_text_utils_cmbbx_template_helper, ends_with_known_unit→value_text_utils_cmbbx_template_helper
- **Functions**
  - `format_display_value(value: Any, *, prefix: str='', suffix: str='', tipcfg: Optional[dict]=None, key: Optional[str]=None, label: Optional[str]=None)` (line 32) — Build the user-visible caption for a dropdown item
    - Calls (inter): str, tipcfg.get, tipcfg.get, str, tipcfg.get, value_text_utils_cmbbx_template_helper, value_text_utils_cmbbx_template_helper

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_caption_adapter_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, k05_combobox_forge.k05_5_utils.combo_caption_adapter
  - External: PySide6.QtCore, __future__, logging
  - Aliases: annotations→__future__, logging→logging, QTimer→PySide6.QtCore, ComboCaptionAdapter→k05_combobox_forge.k05_5_utils.combo_caption_adapter, find_caption_rule→k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, get_caption_affixes→k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- **Functions**
  - `maybe_attach_caption(ctx, combo, label: str)` (line 14) — Attach a ComboCaptionAdapter when prefix/suffix applies (explicit or rule-based)
    - Calls (intra): refresh_lane_layout
    - Calls (inter): str, combo.property, str, tipcfg.get, tipcfg.get, k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, k05_combobox_forge.k05_5_utils.combo_caption_adapter.attach, adapter.widthChanged.connect
  - `refresh_lane_layout(ctx)` (line 37) — Refresh lane geometry after caption width changes
    - Calls (inter): hasattr, ctx.dropdown_container.adjustSize, ctx.dropdown_scroll.updateGeometry, getattr, ctx._sync_chrome_heights, PySide6.QtCore.singleShot

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_debug_helpers_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
  - External: __future__, logging
  - Aliases: annotations→__future__, logging→logging, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- **Functions**
  - `debug_wavelet_state(ctx)` (line 23) — Diagnostic: log wavelet state and whether dependents are enabled
    - Calls (inter): log.debug, hasattr, wavelet_combo.raw_current_text, wavelet_combo.currentText, log.debug, log.debug, combo.property, str, tipcfg.get, enabled_if.get, log.debug, combo.setEnabled, combo.setStyleSheet, log.debug
  - `debug_wavelet_dependencies(ctx)` (line 55) — Diagnostic: enumerate labels gated by wavelet.enable and report current state.
    - Calls (inter): log.debug, tipcfg.get, enabled_if.get, wavelet_dependent.append, log.debug, ctx._get_raw_value_for_key, str, log.debug, log.debug, combo.isEnabled, log.debug
  - `debug_label_to_tipcfg(ctx)` (line 83) — Diagnostic: dump labels with/without enabled_if configs.
    - Calls (inter): log.debug, log.debug, log.debug

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_dependency_engine_iface_cmbbx_template_helper.py`
- **Imports**:
  - External: __future__, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, logging, typing
  - Aliases: annotations→__future__, Optional→typing, Callable→typing, logging→logging, _eval_condition_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, _should_enable_dropdown_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, _update_dependencies_engine_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
- **Functions**
  - `canon_scalar(v: object, canon_bool_token: Callable[[object], str])` (line 30) — Canonicalize a scalar-ish value using the provided token mapper (typically ComboFiltersTemplate._canon_bool_token).
    - Calls (inter): canon_bool_token
  - `check_condition(ctx, current_value: str, condition: dict)` (line 40) — Delegate to the single-source-of-truth evaluator (unchanged logic).
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
  - `should_enable_dropdown(ctx, label: str)` (line 47) — Decide enable/disable for a dependent dropdown identified by its label. [dropdown builder]
    - Calls (intra): check_condition
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, str
  - `update_dependencies(ctx, controller_key: Optional[str]=None)` (line 59) — Re-evaluate dependent dropdowns via the extracted engine
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, ctx._canon_bool_token

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_dependency_helpers_cmbbx_template_helper.py`
- **Imports**:
  - External: __future__, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, logging, sys, typing
  - Aliases: annotations→__future__, logging→logging, sys→sys, Dict→typing, Sequence→typing, Tuple→typing, List→typing, Optional→typing, _find_items_for_label_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
- **Functions**
  - `safe_compute_params_after_dependencies(ctx)` (line 16) — Mirrors the in-class behavior, but made more robust: 1) Try module-level shim in the owning module of ctx (if present)
    - Calls (inter): sys.modules.get, hasattr, getattr, fn, getattr, callable, fn2
  - `find_items_for_label(ctx, label: str)` (line 46) — Delegate to the canonical helper with the current maps on `ctx`
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, str

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_emission_and_change_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_5_utils.combo_caption_adapter
  - External: __future__, logging, typing
  - Aliases: annotations→__future__, Dict→typing, List→typing, Tuple→typing, Optional→typing, logging→logging, ComboCaptionAdapter→k05_combobox_forge.k05_5_utils.combo_caption_adapter
- **Functions**
  - `emit_initial_snapshot(ctx, built: List[Tuple[str, object]])` (line 25) — Loop the newly-built dropdowns and emit a snapshot via ctx._emit_filter_change. [receives data]
    - Calls (inter): ctx._emit_filter_change
  - `on_any_dropdown_changed(ctx, changed_key: Optional[str]=None)` (line 33) — Generic change handler to recompute dependent dropdown states [dropdown builder]
    - Calls (inter): ctx._get_raw_value_for_key, log.debug, ctx._canon_bool_token, ctx._get_raw_value_for_key, log.debug, ctx._canon_bool_token, ctx._update_dependencies
  - `emit_filter_change(ctx, label: str, combo)` (line 48) — Emit the filterChanged signal for a given combobox, then kick dependency updates. [dropdown builder]
    - Calls (inter): getattr, combo.property, getattr, isinstance, adapter.get_raw_current_text, combo.currentText, combo.currentText, ctx.filterChanged.emit, str, str, str, isinstance, ctx._update_dependencies
  - `get_dropdown_values(ctx)` (line 75) — Return the *raw* values for all dropdowns (keyed by 'logical_key::label'). [dropdown builder]
    - Calls (inter): getattr, isinstance, adapter.get_raw_current_text, dropdown.currentText, dropdown.currentText

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_key_index_and_values_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_5_utils.combo_caption_adapter
  - External: PySide6.QtWidgets, __future__, typing
  - Aliases: annotations→__future__, Dict→typing, QComboBox→PySide6.QtWidgets, ComboCaptionAdapter→k05_combobox_forge.k05_5_utils.combo_caption_adapter
- **Functions**
  - `rebuild_key_index(ctx)` (line 8) — Build logical_key → QComboBox mapping for quick dependency checks
    - Calls (inter): klabel.split, combo.property, str
  - `get_raw_value_for_key(ctx, logical_key: str)` (line 20) — Return raw value (not caption) for the dropdown by its logical key
    - Calls (inter): str, dropdown_key.startswith, getattr, getattr, isinstance, str, adapter.get_raw_current_text, combo.currentIndex, combo.itemData, str, combo.currentText

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_menus_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper
  - External: PySide6.QtWidgets, __future__, logging
  - Aliases: annotations→__future__, logging→logging, QMenu→PySide6.QtWidgets, _style_menu_helper→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, _rebuild_main_menu→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, _rebuild_caret_menu→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper
- **Functions**
  - `rebuild_core_menus(ctx)` (line 28) — Rebuild Core main menu, then its caret menu.
    - Calls (intra): rebuild_core_caret_menu
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, ctx.core_direct_map.keys, ctx.core_nested_map.keys, ctx._on_core_main_selected
  - `rebuild_core_caret_menu(ctx)` (line 39) — Rebuild Core caret menu and toggle caret button enabled state.
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, ctx._on_core_caret_selected, ctx.core_filters_button.caret_button.setEnabled, bool, log.debug
  - `rebuild_pro_menus(ctx)` (line 53) — Rebuild Pro main menu, then its caret menu.
    - Calls (intra): rebuild_pro_caret_menu
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, ctx.pro_direct_map.keys, ctx.pro_nested_map.keys, ctx._on_pro_main_selected
  - `rebuild_pro_caret_menu(ctx)` (line 64) — Rebuild Pro caret menu and toggle caret button enabled state.
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper, ctx._on_pro_caret_selected, ctx.pro_filters_button.caret_button.setEnabled, bool, log.debug
  - `style_qmenu(_ctx, menu: QMenu)` (line 78) — Apply canonical lane styling to a QMenu (kept for API symmetry).
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.menu_build_cmbbx_template_helper

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_option_loading_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader
  - External: __future__, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, logging, os, typing
  - Aliases: annotations→__future__, os→os, logging→logging, Dict→typing, load_all→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader, _harvest_label_keys_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers, _harvest_label_tooltips_impl→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
- **Functions**
  - `reload_from_json(ctx, core_json: str | None=None, pro_json: str | None=None)` (line 36) — Update JSON paths (if provided), rebuild option data, menus, and lane
    - Calls (intra): setup_option_data
    - Calls (inter): ctx._rebuild_core_menus, ctx._coerce_valid_selection, ctx._rebuild_pro_menus, ctx.update_dropdowns
  - `setup_option_data(ctx)` (line 59) — Reset maps and (if both JSON files exist) load maps + harvest metadata
    - Calls (intra): harvest_label_keys, harvest_label_tooltips, _extract_tooltip_configurations, _extract_tooltip_configurations
    - Calls (inter): os.path.exists, os.path.exists, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader, ctx._label_to_key.update, ctx._label_to_tipcfg.update, log.info, log.warning, log.warning
  - `_extract_tooltip_configurations(ctx, json_path: str)` (line 97) — Extract detailed tooltip configurations from JSON for hover cards
    - Calls (intra): _process_filter_config, _process_filter_config
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader, subcategories.items, log.warning
  - `_process_filter_config(ctx, filter_config: dict)` (line 124) — Process a single filter configuration and extract tooltip data. [receives data; dropdown builder]
    - Calls (inter): filter_config.get, filter_config.get, filter_config.get, isinstance
  - `harvest_label_keys(ctx, json_path: str)` (line 144) — Wrapper to keep the old class method behavior/signature.
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
  - `harvest_label_tooltips(ctx, json_path: str)` (line 148) — Wrapper to keep the old class method behavior/signature.
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers
  - `_first_key(d: dict | None)` (line 159) — Implements `_first_key` logic.
    - Calls (inter): isinstance, next, iter, d.keys
  - `coerce_valid_selection(ctx)` (line 155) — Ensure core/pro main and caret selections are valid, rebuild caret menus if needed. [dropdown builder]
    - Calls (inter): _first_key, _first_key, _first_key, _first_key, _first_key, _first_key, ctx._rebuild_core_caret_menu, ctx._rebuild_pro_caret_menu

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_sizing_headers_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, qss_styles_cmbbx_template_helper, typing
  - Aliases: annotations→__future__, Optional→typing, Qt→PySide6.QtCore, QSizePolicy→PySide6.QtWidgets, QPushButton→PySide6.QtWidgets, QComboBox→PySide6.QtWidgets, get_caption_affixes→k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, get_caret_qss→qss_styles_cmbbx_template_helper
- **Functions**
  - `apply_scale_sizes(ctx)` (line 37) — Apply scaled sizes to the lane height and header buttons, then sync heights
    - Calls (intra): sync_chrome_heights
    - Calls (inter): max, int, round, max, int, round, max, int, round, ctx.dropdown_scroll.setFixedHeight, b.setMinimumWidth, b.setFixedHeight, c.setFixedWidth, c.setFixedHeight
  - `set_initial_content_width(ctx, combo: QComboBox, key: str, label: str, tipcfg: dict)` (line 63) — Compute and set a min width that fits the widest 'closed' caption (prefix+value+suffix)
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter, combo.fontMetrics, range, combo.count, combo.itemText, max, fm.horizontalAdvance, combo.setMinimumWidth, combo.setSizePolicy
  - `sync_chrome_heights(ctx)` (line 80) — Synchronize header/button heights with the lane height, call external chrome sync, and refresh header captions (elided)
    - Calls (intra): refresh_headers
    - Calls (inter): hasattr, int, ctx.dropdown_scroll.viewport, max, int, getattr, getattr, getattr, hasattr, pair.set_row_height, pair.setFixedHeight, pair.main_button.setFixedHeight, pair.caret_button.setFixedHeight, ctx._sync_external_chrome_heights
  - `header_label(ctx, main: Optional[str], caret: Optional[str], *, is_core: bool)` (line 112) — Compose the visible header caption: "main • caret" when nested, else main, else default ("Main Filters"/"Pro Filters")
    - Calls (inter): str
  - `apply_header(button: QPushButton, full_text: str)` (line 127) — Apply elided text to a header QPushButton and set tooltip to full text
    - Calls (inter): max, button.width, button.fontMetrics, metrics.elidedText, button.setText, button.setToolTip
  - `refresh_headers(ctx)` (line 140) — Recompute and apply both header captions
    - Calls (intra): apply_header, header_label, apply_header, header_label
  - `refresh_caret_highlight(ctx)` (line 155) — Tint caret buttons depending on whether nested menus are available
    - Calls (inter): ctx.core_filters_button.caret_button.setStyleSheet, qss_styles_cmbbx_template_helper, ctx.pro_filters_button.caret_button.setStyleSheet, qss_styles_cmbbx_template_helper
  - `on_resize(ctx)` (line 168) — Small hook used by resizeEvent to keep heights in sync.
    - Calls (intra): sync_chrome_heights

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_style_helpers_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
  - External: __future__
  - Aliases: annotations→__future__, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- **Functions**
  - `apply_enabled_style(ctx, combo)` (line 6) — Set enabled CSS; keeps a try/except in caller if desired.
    - Calls (inter): combo.setStyleSheet
  - `apply_disabled_style(ctx, combo)` (line 10) — Set disabled CSS; keeps a try/except in caller if desired.
    - Calls (inter): combo.setStyleSheet

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\class_ui_layout_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dual_arrow_button_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, typing
  - Aliases: annotations→__future__, Optional→typing, Qt→PySide6.QtCore, QTimer→PySide6.QtCore, QPropertyAnimation→PySide6.QtCore, QWidget→PySide6.QtWidgets, QHBoxLayout→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, QScrollArea→PySide6.QtWidgets, QFrame→PySide6.QtWidgets, QMenu→PySide6.QtWidgets, QSpacerItem→PySide6.QtWidgets, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, DualArrowButton→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dual_arrow_button_cmbbx_template_helper
- **Functions**
  - `canon_bool_token(v: object)` (line 37) — Map common truthy/falsy tokens to 'on'/'off' buckets; else pass-through lowercased string.
    - Calls (inter): str
  - `set_dropdown_width_scale(ctx, scale: float)` (line 49) — Adjust how aggressively dropdown widths are clamped and rebuild the lane [dropdown builder]
    - Calls (inter): float, max, min, ctx.update_dropdowns
  - `setup_ui(ctx)` (line 58) — Build toolbar chrome, main layout, header buttons + menus, dropdown area, then apply sizes and sync heights [insertion: ctx.addWidget, main_layout.addWidget]
    - Calls (intra): setup_dropdown_area
    - Calls (inter): ctx.setStyleSheet, PySide6.QtWidgets, ctx.main_widget.setSizePolicy, PySide6.QtWidgets, main_layout.setContentsMargins, main_layout.setSpacing, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dual_arrow_button_cmbbx_template_helper, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dual_arrow_button_cmbbx_template_helper, main_layout.addWidget, main_layout.addWidget, PySide6.QtWidgets, PySide6.QtWidgets, PySide6.QtWidgets, PySide6.QtWidgets, ctx.core_filters_button.main_button.setMenu, ctx.core_filters_button.caret_button.setMenu, ctx.pro_filters_button.main_button.setMenu, ctx.pro_filters_button.caret_button.setMenu, main_layout.addWidget, ctx._after_dropdown_area_built, ctx.addWidget, ctx._apply_scale_sizes, PySide6.QtCore.singleShot
  - `setup_dropdown_area(ctx)` (line 109) — Construct the scrollable row that will hold the dropdowns [dropdown builder; insertion: ctx.dropdown_scroll.setWidget]
    - Calls (inter): k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper, probe.addItem, probe.sizeHint, probe.deleteLater, PySide6.QtWidgets, ctx.dropdown_scroll.setWidgetResizable, ctx.dropdown_scroll.setHorizontalScrollBarPolicy, ctx.dropdown_scroll.setSizePolicy, ctx.dropdown_scroll.setFrameShape, ctx.dropdown_scroll.setFixedHeight, PySide6.QtWidgets, ctx.dropdown_container.setSizePolicy, PySide6.QtWidgets, ctx.dropdown_layout.setAlignment, ctx.dropdown_layout.setContentsMargins, ctx.dropdown_layout.setSpacing, ctx.dropdown_scroll.setWidget
  - `clear_dropdown_lane(ctx)` (line 141) — Remove all widgets/spacers from the dropdown lane and clear the registry [dropdown builder]
    - Calls (inter): getattr, ctx.dropdown_container.setUpdatesEnabled, range, lay.count, lay.itemAt, item.widget, getattr, hasattr, guard.teardown, getattr, hasattr, ctrl.stop, hasattr, card.hide, hasattr, card.deleteLater, hasattr, delattr, hasattr, delattr, lay.count, lay.takeAt, item.widget, w.deleteLater, ctx.dropdown_container.setUpdatesEnabled, ctx._dropdowns.clear
  - `setup_animations(ctx)` (line 235) — Initialize property animations for smoother lane moves
    - Calls (inter): PySide6.QtCore, ctx.dropdown_animation.setDuration

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\cmbbx_template_helper.py`
- **Imports**:
  - External: PySide6.QtWidgets, __future__, json, logging, os, re, typing
  - Aliases: annotations→__future__, Callable→typing, Dict→typing, Iterable→typing, Mapping→typing, Optional→typing, Sequence→typing, Tuple→typing, Any→typing, List→typing, json→json, re→re, os→os, logging→logging, QComboBox→PySide6.QtWidgets, QMenu→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets
- **Functions**
  - `apply_fast_sizing(combo: QComboBox, *, items: Iterable[Any], display_value: Callable[[Any], str]=lambda x: str(x), char_buffer: int=3, width_scale: float=0.6)` (line 42) — Cheap pre-populate sizing using character count (fast path) [receives data]
    - Calls (inter): str, max, len, display_value, int, max, int, float, combo.setMinimumContentsLength, combo.setSizeAdjustPolicy
  - `apply_precise_sizing(combo: QComboBox, *, items: Iterable[Any], display_value: Callable[[Any], str]=lambda x: str(x), px_padding: int=32, width_scale: float=0.6, min_px: int=64)` (line 77) — Pixel-accurate pre-populate sizing using font metrics (precise path) [receives data]
    - Calls (inter): str, combo.fontMetrics, max, fm.horizontalAdvance, display_value, int, max, int, int, float, combo.setMinimumWidth, combo.setSizePolicy, combo.setSizeAdjustPolicy
  - `looks_numeric(val: str)` (line 124) — Return True if the string looks like a scalar number.
    - Calls (inter): bool, _NUM_RE.fullmatch, str
  - `ends_with_known_unit(val: str)` (line 128) — Return True if value ends with a known unit suffix to avoid duplication.
    - Calls (inter): bool, _UNIT_RE.search, str
  - `format_display_value(x: Any, *, key: str='', label: str='', tipcfg: Optional[dict]=None)` (line 132) — Format a value for display inside the dropdown list
    - Calls (intra): looks_numeric, ends_with_known_unit
    - Calls (inter): str, str, t.get, suf.startswith, s.endswith, str, t.get
  - `_canon(s: Any)` (line 168) — Implements `_canon` logic.
    - Calls (inter): str
  - `check_condition(current_value: str, condition: Mapping[str, Any])` (line 171) — Evaluate a single JSON condition against the current controller value [receives data]
    - Calls (intra): _canon, _canon, _canon, _canon, _canon
    - Calls (inter): condition.get, condition.get, any, condition.get, all, condition.get, condition.get, float, any, float, float, float, float
  - `should_enable_dropdown(label: str, *, label_to_tipcfg: Mapping[str, dict], get_raw_value_for_key: Callable[[str], str], check_condition: Callable[[str, Mapping[str, Any]], bool]=check_condition)` (line 226) — Decide whether a dropdown should be enabled based on its tipcfg [receives data; dropdown builder]
    - Calls (intra): check_condition, check_condition
    - Calls (inter): dict, label_to_tipcfg.get, tipcfg.get, tipcfg.get, isinstance, en_if.get, str, get_raw_value_for_key, isinstance, dis_if.get, str, get_raw_value_for_key, bool
  - `update_dependencies_engine(dropdowns: Mapping[str, QComboBox], *, label_to_tipcfg: Mapping[str, dict], controller_key: Optional[str], get_raw_value_for_key: Callable[[str], str], apply_enabled_style: Callable[[QComboBox], None], apply_disabled_style: Callable[[QComboBox], None], canon_bool_token: Callable[[Any], str], logger: Optional[logging.Logger]=None)` (line 261) — Re-evaluate enabled/disabled on dependent combos [receives data]
    - Calls (intra): should_enable_dropdown
    - Calls (inter): get_raw_value_for_key, logger.debug, canon_bool_token, klabel.split, label_to_tipcfg.get, tipcfg.get, tipcfg.get, d.get, isinstance, d.get, combo.isEnabled, combo.setEnabled, apply_enabled_style, apply_disabled_style
  - `style_menu(menu: QMenu)` (line 328) — Apply a consistent, unobtrusive style to lane menus.
    - Calls (inter): menu.setStyleSheet
  - `rebuild_main_menu(menu: QMenu, *, direct_keys: Iterable[str], nested_keys: Iterable[str], on_main_selected: Callable[[str], None])` (line 348) — Populate the 'main' (root) menu with direct and nested roots [insertion: menu.addAction]
    - Calls (intra): style_menu
    - Calls (inter): menu.clear, list, list, menu.addAction, str, act.triggered.connect, on_main_selected, menu.addSeparator, menu.addAction, str, act.triggered.connect, on_main_selected
  - `rebuild_caret_menu(menu: QMenu, *, main_key: Optional[str], nested_map: Mapping[str, Mapping[str, Any]], on_caret_selected: Callable[[str], None])` (line 379) — Populate the caret (nested) menu for the selected main root [receives data; insertion: menu.addAction]
    - Calls (intra): style_menu
    - Calls (inter): menu.clear, nested_map.get, list, submap.keys, menu.addAction, str, act.triggered.connect, on_caret_selected, bool
  - `_scan_label_nodes(obj: Any)` (line 410) — Yield dict nodes that (appear to) represent a label item
    - Calls (intra): _scan_label_nodes, _scan_label_nodes
    - Calls (inter): isinstance, obj.values, isinstance, isinstance, len, isinstance
  - `harvest_label_keys(json_path: str)` (line 435) — Build a {label -> logical_key} mapping by scanning a lane JSON file
    - Calls (intra): _scan_label_nodes
    - Calls (inter): os.path.exists, open, json.load, log.debug, str, node.get, node.get, node.get, node.get, isinstance, key.strip, str
  - `_merge_tip(a: dict, b: dict)` (line 465) — Shallow merge with 'b' winning (good enough for the template tests).
    - Calls (inter): dict, x.update
  - `harvest_label_tooltips(json_path: str)` (line 472) — Build a {label -> tipcfg} mapping by scanning the same JSON
    - Calls (intra): _scan_label_nodes, _merge_tip
    - Calls (inter): os.path.exists, open, json.load, log.debug, str, node.get, node.get, out.get
  - `find_items_for_label(*, label: str, core_direct_map: Mapping[str, Pairs], core_nested_map: Mapping[str, Mapping[str, Pairs]], pro_direct_map: Mapping[str, Pairs], pro_nested_map: Mapping[str, Mapping[str, Pairs]])` (line 516) — Return items for a label by scanning maps in canonical order:   1) core_direct_map   2) pro_direct_map   3) core_nested_map   4) pro_nested_map [receives data]
    - Calls (inter): isinstance, p.get, p.get, isinstance, len, isinstance, p.get, p.get, isinstance, len, isinstance, p.get, p.get, isinstance, len, isinstance, p.get, p.get, isinstance, len
  - `rebuild_core_menus(*_a, **_k)` (line 576) — Implements `rebuild_core_menus` logic.
  - `rebuild_core_caret_menu(*_a, **_k)` (line 579) — Implements `rebuild_core_caret_menu` logic.
  - `rebuild_pro_menus(*_a, **_k)` (line 582) — Implements `rebuild_pro_menus` logic.
  - `rebuild_pro_caret_menu(*_a, **_k)` (line 585) — Implements `rebuild_pro_caret_menu` logic.

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.delegate_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\delegate_cmbbx_template_helper.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtGui, PySide6.QtWidgets, __future__
  - Aliases: annotations→__future__, Qt→PySide6.QtCore, QColor→PySide6.QtGui, QPainter→PySide6.QtGui, QStyledItemDelegate→PySide6.QtWidgets, QStyleOptionViewItem→PySide6.QtWidgets, QStyle→PySide6.QtWidgets
- **Classes**
  - `TransparentItemDelegate` (QStyledItemDelegate) (line 29) — Lightweight delegate that draws hover/selection/focus rings without obscuring item text
    - `__init__(self, parent=None)` (line 61) — Implements `__init__` logic.
      - Calls (inter): super
    - `setDrawFocusRing(self, enabled: bool)` (line 67) — Implements `setDrawFocusRing` logic.
      - Calls (inter): bool
    - `drawFocusRing(self)` (line 71) — Implements `drawFocusRing` logic.
    - `_dim_alpha(color: QColor, factor: float)` (line 76) — Implements `_dim_alpha` logic.
      - Decorators: staticmethod
      - Calls (inter): PySide6.QtGui, c.setAlpha, int, c.alpha, max, min
    - `paint(self, painter: QPainter, option: QStyleOptionViewItem, index)` (line 84) — Implements `paint` logic. [receives data]
      - Calls (inter): super, bool, bool, bool, bool, painter.save, painter.pen, self._dim_alpha, pen.setColor, pen.setWidth, painter.setPen, painter.setBrush, option.rect.adjusted, painter.drawRoundedRect, painter.restore, painter.save, painter.pen, self._dim_alpha, pen.setColor, pen.setWidth, pen.setStyle, painter.setPen, painter.setBrush, option.rect.adjusted, painter.drawRoundedRect, painter.restore

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\dependency_eval_cmbbx_template_helper.py`
- **Functions**
  - `check_condition(current_value: str, condition: dict)` (line 11) — Evaluate a single JSON condition object against the current value
    - Calls (inter): str, str, condition.get, condition.get, any, str, str, condition.get, all, str, condition.get, condition.get, float, float, float, float, float

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.lane_items_lookup_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\lane_items_lookup_cmbbx_template_helper.py`
- **Imports**:
  - External: __future__, typing
  - Aliases: annotations→__future__, Mapping→typing, Sequence→typing, Any→typing, List→typing
- **Functions**
  - `_items_from_listdef(lst: Sequence[dict])` (line 15) — Normalize one lane list: [{"label": ..., "items": [...]}, ...] → items for exact label. [receives data]
    - Calls (inter): str, entry.get, str, entry.get
  - `find_items_for_label(label: str, *, core_direct_map: Mapping[str, Sequence[dict]], core_nested_map: Mapping[str, Mapping[str, Sequence[dict]]], pro_direct_map: Mapping[str, Sequence[dict]], pro_nested_map: Mapping[str, Mapping[str, Sequence[dict]]])` (line 30) — Resolve `items` for a human label preserving the original search order:    1) core_direct_map   2) pro_direct_map   3) core_nested_map   4) pro_nested_map  Returns ------- list[str] [receives data]
    - Calls (intra): _items_from_listdef, _items_from_listdef, _items_from_listdef, _items_from_listdef
    - Calls (inter): str

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\updat_wavlt_on_off_cmbbx_template_helper.py`
- **Imports**:
  - Internal: k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
  - External: __future__, logging, typing
  - Aliases: annotations→__future__, Any→typing, Optional→typing, logging→logging, KandaDropdown→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- **Functions**
  - `update_wavelet_on_off(host: Any, *, logger: Optional[logging.Logger]=None)` (line 22) — Update the enabled/disabled state of all dropdowns that depend on wavelet.enable
    - Calls (inter): logging.getLogger, host._get_raw_value_for_key, log.debug, str, log.debug, getattr, getattr, dropdowns.items, dropdown_key.split, label_to_tipcfg.get, tipcfg.get, tipcfg.get, enabled_if.get, disabled_if.get, host._should_enable_dropdown, combo.isEnabled, combo.setEnabled, combo.setStyleSheet, log.debug, log.debug

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

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\value_text_utils_cmbbx_template_helper.py`
- **Imports**:
  - External: re
  - Aliases: re→re
- **Functions**
  - `looks_numeric(val: str)` (line 20) — Implements `looks_numeric` logic.
    - Calls (inter): str, bool, _NUM_RE.fullmatch
  - `ends_with_known_unit(val: str)` (line 24) — Implements `ends_with_known_unit` logic.
    - Calls (inter): str, bool, _UNIT_RE.search

### k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper  
`k05_combobox_forge\k05_4_cmbbx_constructor\cmbbx_template_helpers\widgets_cmbbx_template_helper.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, delegate_cmbbx_template_helper, qss_styles_cmbbx_template_helper, typing
  - Aliases: annotations→__future__, Optional→typing, Qt→PySide6.QtCore, QComboBox→PySide6.QtWidgets, QSizePolicy→PySide6.QtWidgets, QWidget→PySide6.QtWidgets, TransparentItemDelegate→delegate_cmbbx_template_helper, get_enabled_combo_qss→qss_styles_cmbbx_template_helper, get_disabled_combo_qss→qss_styles_cmbbx_template_helper
- **Classes**
  - `KandaDropdown` (QComboBox) (line 25) — Compact dropdown used in lanes with clear focus/hover affordances
    - `__init__(self, parent: Optional[Widget]=None, row_h: int=16)` (line 47) — Initialize the dropdown with a compact, accessible style
      - Calls (inter): super, self.setMouseTracking, self.setAttribute, self.setFocusPolicy, self.setItemDelegate, delegate_cmbbx_template_helper, self.setStyleSheet, self.view, v.setMouseTracking, v.viewport, v.setAttribute, v.viewport, v.setFocusPolicy, v.viewport, self.setSizePolicy, self.setSizeAdjustPolicy, self.setMouseTracking, self.setAttribute
    - `raw_current_text(self)` (line 94) — Return the *raw* current text (without caption prefixes/suffixes)
      - Calls (inter): self.currentIndex, self.currentText
    - `set_focus_ring_enabled(self, enabled: bool)` (line 103) — Toggle the dashed focus ring drawn by the item delegate
      - Calls (inter): self.itemDelegate, isinstance, d.setDrawFocusRing, self.view, self.view
    - `_apply_enabled_style(self, combo: QComboBox)` (line 122) — Apply the enabled stylesheet to `combo`.
      - Calls (inter): combo.setStyleSheet
    - `_apply_disabled_style(self, combo: QComboBox)` (line 126) — Apply the disabled stylesheet to `combo`.
      - Calls (inter): combo.setStyleSheet

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

### k05_combobox_forge.k05_4_cmbbx_constructor.filters_controller  
`k05_combobox_forge\k05_4_cmbbx_constructor\filters_controller.py`
- **Imports**:
  - External: __future__, json, pathlib, typing
  - Aliases: annotations→__future__, Path→pathlib, Any→typing, Dict→typing, List→typing, Tuple→typing, json→json
- **Functions**
  - `_load_json(p: Path)` (line 13) — Implements `_load_json` logic.
    - Calls (inter): json.loads, p.read_text
  - `_is_not_null(val: Any)` (line 31) — Implements `_is_not_null` logic.
  - `_check_atomic(key: str, spec: Any, params: Dict[str, Any])` (line 34) — Match a single key against a spec (supports not null, ranges, sets). [receives data]
    - Calls (intra): _is_not_null
    - Calls (inter): params.get, isinstance, spec.strip, isinstance, isinstance
  - `_check_condition(cond: Dict[str, Any], params: Dict[str, Any])` (line 61) — Implements `_check_condition` logic. [receives data]
    - Calls (intra): _check_atomic
    - Calls (inter): all, cond.items
  - `_apply_dependencies(params: Dict[str, Any], deps: List[Dict[str, Any]])` (line 64) — Returns a new params dict with dependent params cleared (set to None) plus human-readable notes about what was disabled. [receives data]
    - Calls (intra): _check_condition
    - Calls (inter): dict, dep.get, dep.get, newp.get, notes.append, dep.get
  - `_apply_dependency_ui(self, params_after_deps: Dict[str, Any])` (line 82) — Hide or grey-out widgets whose params were disabled by dependencies [receives data]
    - Calls (inter): filtering_config.get, ui_cfg.get, ui_cfg.get, filtering_config.get, isinstance, getattr, hasattr, getattr, key_to_combo.get, params_after_deps.get, combo.setVisible, key_to_label.get, lbl.setVisible, combo.setEnabled
  - `compute_params_after_dependencies(self)` (line 125) — Pull current selections, inject controller default if missing, apply dependency rules, return (params_after_deps, notes).
    - Calls (intra): _apply_dependencies
    - Calls (inter): hasattr, callable, self._collect_current_params, getattr, hasattr, callable, combo.currentData, hasattr, callable, combo.currentText, params.setdefault, filtering_config.get

## Module Dependencies
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.updat_wavlt_on_off_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.dependency_eval_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.value_text_utils_cmbbx_template_helper
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper

## Cross-Module Function Calls
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:maybe_attach_caption → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:_extract_tooltip_configurations → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:setup_option_data → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_lane_json_loader:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:set_initial_content_width → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_ui_layout_cmbbx_template_helper:setup_dropdown_area → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_build_one_combo → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:_refresh_header → k05_combobox_forge.k05_4_cmbbx_constructor.dropdown_caption_formatter:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_disabled_style → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_enabled_style → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_style_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_header → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._apply_scale_sizes → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._canon_scalar → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._check_condition → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._coerce_valid_selection → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_label_to_tipcfg → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_wavelet_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._debug_wavelet_state → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_debug_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._emit_filter_change → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._emit_initial_snapshot → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._find_items_for_label → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._get_raw_value_for_key → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._harvest_label_keys → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._harvest_label_tooltips → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._header_label → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._maybe_attach_caption → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._on_any_dropdown_changed → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_core_caret_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_core_menus → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_key_index → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_key_index_and_values_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_pro_caret_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._rebuild_pro_menus → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_caret_highlight → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_headers → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._refresh_lane_layout → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_caption_adapter_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._safe_compute_params_after_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_helpers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._set_initial_content_width → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._setup_dropdown_area → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.widgets_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._setup_option_data → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._should_enable_dropdown → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._style_menu → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_menus_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._sync_chrome_heights → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate._update_dependencies → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_dependency_engine_iface_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.get_dropdown_values → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_emission_and_change_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.reload_from_json → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_option_loading_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.resizeEvent → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.class_sizing_headers_cmbbx_template_helper:<module>
- k05_combobox_forge.k05_4_cmbbx_constructor.combobox_template:ComboFiltersTemplate.update_dropdowns → k05_combobox_forge.k05_4_cmbbx_constructor.cmbbx_template_helpers.update_dropdown_cmbbx_template_helper:<module>

