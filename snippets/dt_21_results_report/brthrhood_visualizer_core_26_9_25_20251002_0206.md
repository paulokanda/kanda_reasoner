# Group: visualizer_core_26_9_25

- Modules: **51**  |  Functions: **79**  |  Methods: **130**
- Module edges: **39**  |  Function edges: **52**

## Group Logic (Heuristic Summary)

Group **visualizer_core_26_9_25** logic overview:

- Module **k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core** (`k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py`)
  - Dropdown builder(s):
    • **EEGVisualizerCore.create_hp_filter** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:260 sig=(self, *, cutoff_hz: float) — Deprecated during dropdown clean-sweep (no-op).
    • **EEGVisualizerCore._handle_graph_selection** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:514 sig=(self, graph_name) — Handles the selection of different graph types to display on the plot panel
    • **EEGVisualizerCore.create_lp_filter** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:577 sig=(self, cutoff_hz: float) — Deprecated during dropdown clean-sweep (no-op).
    • **EEGVisualizerCore.create_notch_filter** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:585 sig=(self, freqs: list[float] | None) (receives dict/list-like data) — Deprecated during dropdown clean-sweep (no-op).
    • **EEGVisualizerCore.on_notchfilter_changed** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:655 sig=(self, freqs: list[float] | None) (receives dict/list-like data) — Deprecated during dropdown clean-sweep (no-op).
  - Other data receivers (dict/list-like):
    • **EEGVisualizerCore.update_eeg_data** @ k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py:402 sig=(self, new_data)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_channel_manager_0_5_7.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_data_extraction.py`)
  - Other data receivers (dict/list-like):
    • **DummyWindowMgr.__init__** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_data_extraction.py:12 sig=(self, view_data, view_times)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_data_state.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_dataframe_utils.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_display_pyside6_eeg_visualizer.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_eeg_session_initializer.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_filter_pipeline.py`)
  - Dropdown builder(s):
    • **test_filter_stack_order** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_filter_pipeline.py:53 sig=(viz) — Filter stages arrive in the expected order: montage → speed → hp.
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_graph_selection_handler.py`)
  - Dropdown builder(s):
    • **test_handle_graph_selection_success** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_graph_selection_handler.py:28 sig=(mock_core, capsys) — Implements `test_handle_graph_selection_success` logic.
    • **test_handle_graph_selection_nograph** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_graph_selection_handler.py:36 sig=(monkeypatch, capsys) — Implements `test_handle_graph_selection_nograph` logic.
    • **test_handle_graph_selection_noplot** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_graph_selection_handler.py:50 sig=(monkeypatch, capsys) — Implements `test_handle_graph_selection_noplot` logic.
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_mcrvlt_snapshot_map_initializer.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_memory_manager_0_5_6** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_memory_manager_0_5_6.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_montage_handler.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_pipeline_reset.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_manager_0_5_4.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_timer_manager_0_5_10.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_view_updater.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_sensitivity_handler.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_signal_manager_0_5_8.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_splash_manager_0_5_5.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_ui_helpers.py`)
  - Canvas class: **DummyCanvas** at k01_core_eeg\k01_3_eeg_visualizer\tests\test_ui_helpers.py:4
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_visualizer_reseter.py`)
  - Canvas class: **DummyCanvas** at k01_core_eeg\k01_3_eeg_visualizer\tests\test_visualizer_reseter.py:22
- Module **k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11** (`k01_core_eeg\k01_3_eeg_visualizer\tests\test_window_manager_0_5_11.py`)
  - Other data receivers (dict/list-like):
    • **fake_slice_window** @ k01_core_eeg\k01_3_eeg_visualizer\tests\test_window_manager_0_5_11.py:4 sig=(data, sfreq, start, window)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\channel_core_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_data_bootstrapper.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_input_manager.py`)
  - Dropdown builder(s):
    • **InputManager._install_event_filter** @ k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_input_manager.py:52 sig=(self) — Implements `_install_event_filter` logic.
    • **InputManager.eventFilter** @ k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_input_manager.py:63 sig=(self, obj, event) — Implements `eventFilter` logic.
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_memory_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_plot_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\create_montage_stage_help.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\data_extraction.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\data_state.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\dataframe_utils.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.diagnostics_utils** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\diagnostics_utils.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\display_pyside6_eeg_visualizer.py`)
  - Dropdown builder(s):
    • **_find_filters_toolbar** @ k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\display_pyside6_eeg_visualizer.py:27 sig=(core) — Prefer the middle lane toolbar (DrpdwnPanelMiddleBar) if present
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\eeg_session_initializer.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_state** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\eeg_state.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\graph_selection_handler.py`)
  - Dropdown builder(s):
    • **handle_graph_selection** @ k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\graph_selection_handler.py:20 sig=(core, graph_name: str) — Handles selection of a graph from dropdown and renders it on the canvas
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\mcrvlt_snapshot_map_initializer.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.null_signal_pipeline** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\null_signal_pipeline.py`)
  - Other data receivers (dict/list-like):
    • **NullSignalPipeline.set_order** @ k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\null_signal_pipeline.py:29 sig=(self, stages: list[str])
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\pipeline_reset.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\plot_core_timer_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\plot_view_updater.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\sensitivity_handler.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\signal_core_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\splash_core_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\start_snapshot.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\timeline_manager_core.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\ui_core_manager.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\ui_helpers.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\visualizer_reset_snpsht.py`)
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\window_core_manager.py`)
  - Canvas class: **_View** at k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\window_core_manager.py:10
- Module **k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_setup** (`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\window_core_setup.py`)

Module connections (imports within group):
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot

Cross-module function calls:
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore._delayed_plot → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.current_view → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.current_window → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_close_clicked → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_timeline_clicked → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_timeline_moved → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_window_moved → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7:test_init_channel_state_sets_attributes → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_current_raw_assigned → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_current_raw_assigned → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_with_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_with_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_without_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_without_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state:test_init_data_state_sets_defaults → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state:test_init_data_state_sets_defaults → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_missing_channels → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_missing_data → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer:test_display_pyside6_gui_installs_everything → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer:test_initialize_eeg_session_sets_up_fields → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline:viz → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_nograph → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_noplot → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer:test_initialize_mcrvlt_snapshot_map_creates_and_wires → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer:test_initialize_mcrvlt_snapshot_map_no_raw_returns_false → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler:test_create_montage_stage_does_nothing_if_pipeline_missing → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler:test_create_montage_stage_sets_pipeline_and_triggers_refresh → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset:test_reset_pipeline_state_sets_pipeline_and_window → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4:test_init_matplotlib_state_sets_attributes → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10:test_delayed_plot_invokes_helper → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater:test_update_plot_view_runs_render_and_helpers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler:test_handle_sensitivity_change → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8:test_init_signals_connects_handlers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5:test_show_splash_creates_and_configures → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5:test_show_splash_idempotent → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_failure → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_no_canvas → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter:test_handle_close_clicked_all_steps → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11:test_current_window_delegates_to_slice → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager:MemoryManager.init_memory_monitor → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer:display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:eeg_visu_reset_snpsht → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot:<module>

## Modules
### k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core  
`k01_core_eeg\k01_3_eeg_visualizer\eeg_visualizer_core.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, k01_core_eeg.k01_2_visualizer.visualizer_data.amplitude_scale_utils, k01_core_eeg.k01_2_visualizer.visualizer_data.input_rate, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager, k01_core_eeg.k01_4_visualizer_render.visualizer_render_core, k01_core_eeg.k01_4_visualizer_render.visualizer_render_helpers.visu_renderer, k02_eeg_input.eeg_visualizer_loader_logic, k11_graph_stat.hdf5.hdf5_folder_file_creator
  - External: PySide6.QtCore, dipy.viz.horizon, faulthandler, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers, logging, matplotlib, matplotlib.pyplot, mne, visualizer_core_helpers, visualizer_core_helpers.diagnostics_utils, visualizer_core_helpers.eeg_session_initializer
  - Aliases: logging→logging, visualizer→dipy.viz.horizon, faulthandler→faulthandler, matplotlib→matplotlib, mne→mne, plt→matplotlib.pyplot, Qt→PySide6.QtCore, Signal→PySide6.QtCore, QObject→PySide6.QtCore, QCoreApplication→PySide6.QtCore, ensure_eeg_folders→k11_graph_stat.hdf5.hdf5_folder_file_creator, initialize_main_plot→k01_core_eeg.k01_4_visualizer_render.visualizer_render_core, EegVisualizerLoaderLogic→k02_eeg_input.eeg_visualizer_loader_logic, recompute_amplitude_scale→k01_core_eeg.k01_2_visualizer.visualizer_data.amplitude_scale_utils, help03_show_input_warning→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, EEGRenderer→k01_core_eeg.k01_4_visualizer_render.visualizer_render_helpers.visu_renderer, Slot→PySide6.QtCore, DataManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper, init_data_state→visualizer_core_helpers, extract_and_store_eeg_data→visualizer_core_helpers, build_dataframe_from_data→visualizer_core_helpers, force_canvas_focus→visualizer_core_helpers, eeg_visu_reset_snpsht→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht, initialize_mcrvlt_snapshot_map→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers, handle_sensitivity_change→visualizer_core_helpers, create_montage_stage_helper→visualizer_core_helpers, hash_raw_data→visualizer_core_helpers.diagnostics_utils, SignalManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager, MemoryManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager, PlotManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager, UIManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager, SplashManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager, ChannelManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager, initialize_eeg_session→visualizer_core_helpers.eeg_session_initializer, reset_pipeline_state→visualizer_core_helpers, init_eeg_state→visualizer_core_helpers, WindowManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager, TimelineManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core, PlotTimerManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager, update_plot_view_safely→visualizer_core_helpers, display_pyside6_eeg_visualizer→visualizer_core_helpers, handle_graph_selection→visualizer_core_helpers, should_accept_input→k01_core_eeg.k01_2_visualizer.visualizer_data.input_rate
- **Classes**
  - `EEGVisualizerCore` (QObject) (line 72) — 
    - `__init__(self, file_path=None)` (line 78) — Implements `__init__` logic.
      - Calls (inter): super, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper, self.data_mgr.init_data_state, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager, k11_graph_stat.hdf5.hdf5_folder_file_creator, matplotlib.pyplot.close, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager, k01_core_eeg.k01_4_visualizer_render.visualizer_render_core, k01_core_eeg.k01_4_visualizer_render.visualizer_render_helpers.visu_renderer, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager, k02_eeg_input.eeg_visualizer_loader_logic, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager, self._init_eeg_state, k01_core_eeg.k01_4_visualizer_render.visualizer_render_helpers.visu_renderer
    - `install_key_handler(self)` (line 176) — Backward‐compat stub for InterfaceManager: delegate to the new InputManager’s event‐filter installer.
      - Calls (inter): hasattr, self.input_mgr._install_event_filter
    - `_extract_and_store_eeg_data(self, raw: 'mne.io.BaseRaw')` (line 188) — Copy the channels-of-interest from *raw* into NumPy arrays and build the window-limited views consumed by the renderer
      - Calls (inter): visualizer_core_helpers
    - `load_eeg(self, raw: mne.io.BaseRaw)` (line 207) — Called once by EegVisualizerLoaderLogic.
      - Calls (inter): visualizer_core_helpers.eeg_session_initializer
    - `window_size(self)` (line 218) — Always return **something** meaningful:  • If WindowManager is ready → its authoritative value • Else → the pending value stored during early startup
      - Decorators: property
      - Calls (inter): getattr
    - `window_size(self, sec: float)` (line 231) — Accept writes at any stage of startup
      - Decorators: window_size.setter
      - Calls (inter): float, getattr, setattr
    - `reset_processing_pipeline(self)` (line 246) — Clear every stage and start again from pristine recording
      - Calls (inter): visualizer_core_helpers
    - `create_hp_filter(self, *, cutoff_hz: float)` (line 260) — Deprecated during dropdown clean-sweep (no-op). [dropdown builder]
    - `create_speed_scaler(self, *, speed_mm_s: int)` (line 271) — Deprecated during dropdown clean-sweep (no-op).
    - `create_montage_stage(self, *, montage: str)` (line 288) — create logic for `create_montage_stage`.
      - Calls (inter): visualizer_core_helpers
    - `on_close_clicked(self)` (line 294) — Called by the Close-EEG button; reset state, clear axes, hide UI elements
      - Decorators: Slot()
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht, PySide6.QtCore
    - `_init_data_state(self)` (line 304) — Delegate initialization of raw/data/timing attributes to the helper in visualizer_core_helpers.
      - Calls (inter): visualizer_core_helpers
    - `_init_eeg_state(self)` (line 314) — Delegate EEG-state initialization to the helper.
      - Calls (inter): visualizer_core_helpers
    - `current_window(self)` (line 324) — Return the data slice for the active time-window
      - Calls (inter): getattr, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager, mgr.current_window, getattr
    - `current_view(self)` (line 341) — Back-compat helper for callers that want (window, times) directly.
      - Calls (inter): getattr, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager, mgr.current_view, getattr
    - `verify_amplitude_map_state(self)` (line 349) — Debug method to check amplitude map state
      - Calls (inter): hasattr, print
    - `_complete_amplitude_map_setup(self)` (line 355) — Final setup after amplitude map is created
      - Calls (inter): self.eeg_loaded_signal.connect, print
    - `initialize_mcrvlt_snapshot_map(self)` (line 361) — Signal handler: create the amplitude‐map façade once raw data is available.
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers
    - `emit_eeg_loaded_signal(self)` (line 367) — Implements `emit_eeg_loaded_signal` logic.
      - Calls (inter): print, self.eeg_loaded_signal.emit, print
    - `set_vertical_gain(self, gain: float)` (line 374) — Shrinks or enlarges all traces vertically without changing channel spacing or the numeric sensitivity shown in the ruler
      - Calls (inter): max, self._recompute_amplitude_scale
    - `_recompute_amplitude_scale(self)` (line 385) — Legacy wrapper kept so existing callers inside EEGVisualizerCore keep working
      - Calls (inter): k01_core_eeg.k01_2_visualizer.visualizer_data.amplitude_scale_utils
    - `on_sensitivity_changed(self, μV: int)` (line 394) — Called when the Sensitivity dropdown changes (in µV)
      - Decorators: Slot(int)
      - Calls (inter): visualizer_core_helpers, PySide6.QtCore
    - `update_eeg_data(self, new_data)` (line 402) — Updates the EEG data and sets a flag indicating that the data has changed [receives data]
      - Calls (inter): print
    - `build_dataframe_from_data(self)` (line 412) — Converts loaded EEG numpy array and channel names into a pandas DataFrame
      - Calls (inter): visualizer_core_helpers
    - `on_window_moved(self, start: float, end: float)` (line 420) — Delegate window‐moved → TimelineManager.
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core
    - `on_timeline_moved(self, start_time: float, end_time: float)` (line 426) — Delegate viz.timeline_moved → TimelineManager.
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core
    - `_delayed_plot(self)` (line 432) — Slot connected to self.plot_timer.timeout
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
    - `update_plot_view(self)` (line 443) — Redraw the EEG canvas for the **current** time-window
      - Calls (inter): visualizer_core_helpers
    - `force_canvas_focus(self)` (line 453) — Ensures the Matplotlib canvas widget receives and retains keyboard focus
      - Calls (inter): visualizer_core_helpers, print, print
    - `display_in_pyside6(self)` (line 468) — Build main window + wire up every GUI helper (Phase-2 version)
      - Calls (inter): visualizer_core_helpers
    - `_toggle_max_restore(self)` (line 477) — Alternates between maximizing and restoring the main window.
      - Calls (inter): self.main_window.isMaximized, self.main_window.showNormal, self.main_window.showMaximized
    - `on_timeline_clicked(self, clicked_time: float)` (line 484) — Delegate timeline click → TimelineManager.
      - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core
    - `update_amplitude_scale(self, new_scale: float)` (line 490) — Updates the vertical amplitude scale of EEG traces and refreshes the plot
      - Calls (inter): print, self.mcrvlt_snapshot_map.reset_red_line_to_same_position, self.plot_timer.start
    - `_show_input_warning(self, message='Too many inputs! Slow down.')` (line 506) — Displays a temporary warning message to the user, typically for input flood protection
      - Calls (inter): k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers
    - `_handle_graph_selection(self, graph_name)` (line 514) — Handles the selection of different graph types to display on the plot panel [dropdown builder]
      - Calls (inter): visualizer_core_helpers
    - `_register_input_event(self, event_type: str)` (line 525) — Thin wrapper kept only so older helper classes (drop-downs, etc.) that still call `viz._register_input_event()` don’t break
      - Calls (inter): k01_core_eeg.k01_2_visualizer.visualizer_data.input_rate
    - `_refresh_view(self)` (line 551) — Re-compute NumPy caches + redraw using new core helpers.
      - Calls (inter): getattr, getattr, print, self.pipeline.fingerprint, self.pipeline.build, print, visualizer_core_helpers.diagnostics_utils, self._extract_and_store_eeg_data, self.update_plot_view, print, self.pipeline.fingerprint
    - `on_lowpass_changed(self, hz: int)` (line 569) — Deprecated during dropdown clean-sweep (no-op).
      - Decorators: Slot(int)
      - Calls (inter): PySide6.QtCore
    - `create_lp_filter(self, cutoff_hz: float)` (line 577) — Deprecated during dropdown clean-sweep (no-op). [dropdown builder]
    - `create_notch_filter(self, freqs: list[float] | None)` (line 585) — Deprecated during dropdown clean-sweep (no-op). [receives data; dropdown builder]
    - `on_notchfilter_changed(self, freqs: list[float] | None)` (line 655) — Deprecated during dropdown clean-sweep (no-op). [receives data; dropdown builder]
      - Decorators: Slot(object)
      - Calls (inter): PySide6.QtCore

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_channel_manager_0_5_7.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
  - External: pytest
  - Aliases: pytest→pytest, ChannelManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
- **Functions**
  - `patch_channel_tools(monkeypatch)` (line 10) — Implements `patch_channel_tools` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, monkeypatch.setattr, pytest.fixture
  - `test_init_channel_state_sets_attributes()` (line 25) — Implements `test_init_channel_state_sets_attributes` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager, mgr.init_channel_state, isinstance
- **Classes**
  - `DummyCloser`  (line 5) — 
    - `__init__(self, viz)` (line 6) — Implements `__init__` logic.
  - `DummyViz`  (line 22) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_data_extraction.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction
  - External: mne, numpy, pytest
  - Aliases: np→numpy, pytest→pytest, mne→mne, extract_and_store_eeg_data→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction, EEGVisualizerCore→k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- **Functions**
  - `raw_simple()` (line 20) — Implements `raw_simple` logic.
    - Decorators: pytest.fixture
    - Calls (inter): numpy.arange, mne.create_info, mne.io.RawArray
  - `test_extract_without_window_mgr(raw_simple)` (line 28) — Implements `test_extract_without_window_mgr` logic.
    - Calls (intra): raw_simple.get_data
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core.__new__, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction, numpy.array_equal, numpy.array_equal, pytest.approx, pytest.approx, numpy.array_equal
  - `test_extract_with_window_mgr(raw_simple)` (line 50) — Implements `test_extract_with_window_mgr` logic.
    - Calls (intra): DummyWindowMgr
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core.__new__, numpy.array, numpy.array, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction, numpy.array_equal, numpy.array, numpy.array_equal, numpy.array
  - `test_current_raw_assigned(raw_simple)` (line 77) — Implements `test_current_raw_assigned` logic.
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core.__new__, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction
- **Classes**
  - `DummyWindowMgr`  (line 11) — 
    - `__init__(self, view_data, view_times)` (line 12) — Implements `__init__` logic. [receives data]
    - `current_view(self, start)` (line 15) — Implements `current_view` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_data_state.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state
  - External: pytest
  - Aliases: pytest→pytest, init_data_state→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state, EEGVisualizerCore→k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- **Functions**
  - `test_init_data_state_sets_defaults()` (line 5) — Implements `test_init_data_state_sets_defaults` logic.
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core.__new__, hasattr, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_dataframe_utils.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils
  - External: numpy, pandas, pytest
  - Aliases: pytest→pytest, np→numpy, pd→pandas, build_dataframe_from_data→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils
- **Functions**
  - `test_build_dataframe_success()` (line 12) — Implements `test_build_dataframe_success` logic.
    - Calls (intra): DummyViz
    - Calls (inter): numpy.arange, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils, isinstance, list
  - `test_build_dataframe_missing_data()` (line 26) — Implements `test_build_dataframe_missing_data` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils, hasattr
  - `test_build_dataframe_missing_channels()` (line 33) — Implements `test_build_dataframe_missing_channels` logic.
    - Calls (intra): DummyViz
    - Calls (inter): numpy.zeros, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils, hasattr
- **Classes**
  - `DummyViz`  (line 9) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_display_pyside6_eeg_visualizer.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer
  - External: PySide6.QtCore, importlib, pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, importlib→importlib, display_pyside6_eeg_visualizer→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer, QTimer→PySide6.QtCore
- **Functions**
  - `mock_core(monkeypatch)` (line 12) — Implements `mock_core` logic.
    - Decorators: pytest.fixture
    - Calls (inter): types, types, setattr, setattr, setattr, types, types, setattr, types, types, setattr, types, types, setattr, types, setattr, monkeypatch.setattr, fn, monkeypatch.setattr, types, setattr, monkeypatch.setattr, monkeypatch.setattr, types, setattr, DummySignal, DummySignal
  - `test_display_pyside6_gui_installs_everything(mock_core)` (line 54) — Implements `test_display_pyside6_gui_installs_everything` logic.
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer, getattr, getattr, getattr, getattr, getattr, getattr, getattr, getattr, getattr, isinstance
- **Classes**
  - `DummySignal`  (line 44) — 
    - `__init__(self, label)` (line 45) — Implements `__init__` logic.
    - `connect(self, fn)` (line 46) — Implements `connect` logic.
      - Calls (inter): setattr

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_eeg_session_initializer.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer
  - External: pytest, sys, types
  - Aliases: pytest→pytest, SimpleNamespace→types, sys→sys, initialize_eeg_session→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer
- **Functions**
  - `patch_deps(monkeypatch)` (line 28) — Implements `patch_deps` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, monkeypatch.setattr, monkeypatch.setattr, monkeypatch.setattr, pytest.fixture
  - `make_core()` (line 58) — Implements `make_core` logic.
    - Calls (inter): types
  - `test_initialize_eeg_session_sets_up_fields()` (line 64) — Implements `test_initialize_eeg_session_sets_up_fields` logic.
    - Calls (intra): DummyRaw, make_core
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer, isinstance, isinstance
- **Classes**
  - `DummyRaw`  (line 7) — 
    - `__init__(self, ch_names)` (line 8) — Implements `__init__` logic.
    - `copy(self)` (line 11) — Implements `copy` logic.
      - Calls (intra): DummyRaw
  - `DummyPipeline`  (line 15) — 
    - `__init__(self, raw)` (line 16) — Implements `__init__` logic.
  - `DummyWindowMgr`  (line 20) — 
    - `__init__(self, pipeline)` (line 21) — Implements `__init__` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_filter_pipeline.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
  - External: pytest, types
  - Aliases: MethodType→types, pytest→pytest, EEGVisualizerCore→k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- **Functions**
  - `_minimal_init(self)` (line 35) — Implements `_minimal_init` logic.
    - Calls (inter): types
  - `viz(monkeypatch)` (line 29) — Provide a *light-weight* EEGVisualizerCore whose __init__ does **not** spin up Qt or MNE
    - Decorators: pytest.fixture
    - Calls (inter): monkeypatch.setattr, k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
  - `test_filter_stack_order(viz)` (line 53) — Filter stages arrive in the expected order: montage → speed → hp. [dropdown builder]
    - Calls (intra): viz.create_montage_stage, viz.create_speed_scaler, viz.create_hp_filter
    - Calls (inter): any

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_graph_selection_handler.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, handle_graph_selection→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler, NoGraphDataError→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, NoPlotFunctionError→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection
- **Functions**
  - `mock_core(monkeypatch)` (line 6) — Implements `mock_core` logic.
    - Decorators: pytest.fixture
    - Calls (inter): types, monkeypatch.setattr, monkeypatch.setattr, setattr, monkeypatch.setattr, plot_func, monkeypatch.setattr, setattr
  - `test_handle_graph_selection_success(mock_core, capsys)` (line 28) — Implements `test_handle_graph_selection_success` logic. [dropdown builder]
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler, capsys.readouterr
  - `test_handle_graph_selection_nograph(monkeypatch, capsys)` (line 36) — Implements `test_handle_graph_selection_nograph` logic. [dropdown builder]
    - Calls (inter): monkeypatch.setattr, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, types, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler, capsys.readouterr
  - `test_handle_graph_selection_noplot(monkeypatch, capsys)` (line 50) — Implements `test_handle_graph_selection_noplot` logic. [dropdown builder]
    - Calls (inter): monkeypatch.setattr, monkeypatch.setattr, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, types, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler, capsys.readouterr

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_mcrvlt_snapshot_map_initializer.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, initialize_mcrvlt_snapshot_map→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer
- **Functions**
  - `patch_deps(monkeypatch)` (line 10) — Implements `patch_deps` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, types, monkeypatch.setattr, types, pytest.fixture
  - `make_core()` (line 21) — Implements `make_core` logic.
    - Calls (inter): types, object, DummySignal
  - `test_initialize_mcrvlt_snapshot_map_creates_and_wires()` (line 33) — Implements `test_initialize_mcrvlt_snapshot_map_creates_and_wires` logic.
    - Calls (intra): make_core
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer, hasattr
  - `test_initialize_mcrvlt_snapshot_map_no_raw_returns_false()` (line 41) — Implements `test_initialize_mcrvlt_snapshot_map_no_raw_returns_false` logic.
    - Calls (intra): make_core
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer
- **Classes**
  - `DummySignal`  (line 27) — 
    - `__init__(self)` (line 28) — Implements `__init__` logic.
    - `connect(self, cb)` (line 29) — Implements `connect` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_memory_manager_0_5_6  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_memory_manager_0_5_6.py`
- **Imports**:
  - External: K01_Core.k01_3_eeg_visualizer.core_memory_manager, pytest
  - Aliases: pytest→pytest, MemoryManager→K01_Core.k01_3_eeg_visualizer.core_memory_manager
- **Functions**
  - `dummy_capture_initial_eeg_state(viz)` (line 23) — Implements `dummy_capture_initial_eeg_state` logic.
  - `patch_memory_tools(monkeypatch)` (line 16) — Implements `patch_memory_tools` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, monkeypatch.setattr, pytest.fixture
  - `test_init_memory_monitor(monkeypatch)` (line 33) — Implements `test_init_memory_monitor` logic.
    - Calls (intra): DummyViz
    - Calls (inter): K01_Core.k01_3_eeg_visualizer.core_memory_manager, mgr.init_memory_monitor, isinstance, getattr
- **Classes**
  - `DummyMem`  (line 4) — 
    - `__init__(self, viz)` (line 5) — Implements `__init__` logic.
    - `capture_snapshot(self, label)` (line 9) — Implements `capture_snapshot` logic.
      - Calls (inter): self.snapshots.append
    - `get_current_memory(self)` (line 12) — Implements `get_current_memory` logic.
  - `DummyViz`  (line 30) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_montage_handler.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, create_montage_stage→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help
- **Functions**
  - `test_create_montage_stage_sets_pipeline_and_triggers_refresh()` (line 5) — Implements `test_create_montage_stage_sets_pipeline_and_triggers_refresh` logic.
    - Calls (inter): types, types, setattr, setattr, setattr, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help
  - `test_create_montage_stage_does_nothing_if_pipeline_missing()` (line 25) — Implements `test_create_montage_stage_does_nothing_if_pipeline_missing` logic.
    - Calls (inter): types, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_pipeline_reset.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, reset_pipeline_state→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset
- **Functions**
  - `mock_core(monkeypatch)` (line 13) — Implements `mock_core` logic.
    - Decorators: pytest.fixture
    - Calls (inter): types, setattr, monkeypatch.setattr, monkeypatch.setattr
  - `test_reset_pipeline_state_sets_pipeline_and_window(mock_core)` (line 25) — Implements `test_reset_pipeline_state_sets_pipeline_and_window` logic.
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset, isinstance, isinstance
- **Classes**
  - `DummyPipeline`  (line 5) — 
    - `__init__(self, raw)` (line 6) — Implements `__init__` logic.
  - `DummyWindowManager`  (line 8) — 
    - `__init__(self, pipeline)` (line 9) — Implements `__init__` logic.
    - `set_speed(self, speed)` (line 10) — Implements `set_speed` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_manager_0_5_4.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
  - Aliases: PlotManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
- **Functions**
  - `test_init_matplotlib_state_sets_attributes()` (line 6) — Implements `test_init_matplotlib_state_sets_attributes` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager, hasattr, hasattr, hasattr, isinstance, hasattr, isinstance, hasattr, isinstance
- **Classes**
  - `DummyViz`  (line 3) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_timer_manager_0_5_10.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
  - External: pytest
  - Aliases: pytest→pytest, PlotTimerManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
- **Functions**
  - `dummy_help(viz)` (line 5) — Implements `dummy_help` logic.
  - `patch_helper(monkeypatch)` (line 10) — Implements `patch_helper` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, pytest.fixture
  - `test_delayed_plot_invokes_helper()` (line 19) — Implements `test_delayed_plot_invokes_helper` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager, mgr.delayed_plot, getattr
- **Classes**
  - `DummyViz`  (line 16) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_plot_view_updater.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater
  - External: numpy, pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, update_plot_view_safely→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater, np→numpy
- **Functions**
  - `dummy_render(mode)` (line 22) — Implements `dummy_render` logic.
  - `mock_core(monkeypatch)` (line 11) — Implements `mock_core` logic.
    - Decorators: pytest.fixture
    - Calls (intra): FakeAxes
    - Calls (inter): types, numpy.array, types, numpy.array, types, monkeypatch.setattr, core.helpers_run.append, monkeypatch.setattr, core.helpers_run.append, monkeypatch.setattr, core.helpers_run.append, monkeypatch.setattr, core.helpers_run.append
  - `test_update_plot_view_runs_render_and_helpers(mock_core)` (line 37) — Implements `test_update_plot_view_runs_render_and_helpers` logic.
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater, numpy.array_equal, numpy.array, set
- **Classes**
  - `FakeAxes`  (line 6) — 
    - `__init__(self)` (line 7) — Implements `__init__` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_sensitivity_handler.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, handle_sensitivity_change→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler
- **Functions**
  - `test_handle_sensitivity_change(uv, expect_changed, expect_scale)` (line 24) — Implements `test_handle_sensitivity_change` logic.
    - Decorators: pytest.mark.parametrize('uv, expect_changed, expect_scale', [(50, False, 0.002), (25, True, pytest.approx(0.004)), (0, False, 0.002), (-5, False, 0.002)])
    - Calls (intra): DummyCore
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler, pytest.mark.parametrize, pytest.approx
- **Classes**
  - `DummyCore` (SimpleNamespace) (line 8) — 
    - `__init__(self)` (line 9) — Implements `__init__` logic.
      - Calls (inter): super
    - `update_plot_view(self)` (line 15) — update logic for `update_plot_view`.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_signal_manager_0_5_8.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
  - Aliases: SignalManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
- **Functions**
  - `test_init_signals_connects_handlers(capsys)` (line 16) — Implements `test_init_signals_connects_handlers` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager, mgr.init_signals, len, callable, capsys.readouterr
- **Classes**
  - `DummySignal`  (line 3) — 
    - `__init__(self)` (line 4) — Implements `__init__` logic.
    - `connect(self, slot)` (line 6) — Implements `connect` logic.
      - Calls (inter): self.connected.append
  - `DummyViz`  (line 9) — 
    - `__init__(self)` (line 10) — Implements `__init__` logic.
      - Calls (intra): DummySignal

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_splash_manager_0_5_5.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
  - External: pytest
  - Aliases: pytest→pytest, SplashManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
- **Functions**
  - `patch_kandasplash(monkeypatch)` (line 18) — Implements `patch_kandasplash` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, pytest.fixture
  - `test_show_splash_creates_and_configures(monkeypatch)` (line 34) — Implements `test_show_splash_creates_and_configures` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager, mgr.show_splash, isinstance
  - `test_show_splash_idempotent(monkeypatch)` (line 51) — Implements `test_show_splash_idempotent` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager, mgr.show_splash, mgr.show_splash
- **Classes**
  - `DummySplash`  (line 4) — 
    - `__init__(self, canvas, path)` (line 5) — Implements `__init__` logic.
    - `setSizePolicy(self, h, v)` (line 11) — Implements `setSizePolicy` logic.
    - `adjustSize(self)` (line 14) — Implements `adjustSize` logic.
  - `DummyViz`  (line 25) — 
    - `__init__(self)` (line 26) — Implements `__init__` logic.
      - Calls (inter): object
    - `force_canvas_focus(self)` (line 31) — Implements `force_canvas_focus` logic.

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_ui_helpers.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
  - External: pytest
  - Aliases: pytest→pytest, force_canvas_focus→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
- **Functions**
  - `test_force_canvas_focus_success(monkeypatch)` (line 20) — Implements `test_force_canvas_focus_success` logic.
    - Calls (intra): DummyViz, DummyCanvas
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
  - `test_force_canvas_focus_failure(monkeypatch)` (line 28) — Implements `test_force_canvas_focus_failure` logic.
    - Calls (intra): DummyViz, DummyCanvas
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
  - `test_force_canvas_focus_no_canvas()` (line 36) — Implements `test_force_canvas_focus_no_canvas` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
- **Classes**
  - `DummyCanvas`  (line 4) [canvas] — 
    - `__init__(self, will_focus=True)` (line 5) — Implements `__init__` logic.
    - `setFocus(self, reason)` (line 8) — Implements `setFocus` logic.
    - `raise_(self)` (line 10) — Implements `raise_` logic.
    - `repaint(self)` (line 12) — Implements `repaint` logic.
    - `hasFocus(self)` (line 14) — Implements `hasFocus` logic.
  - `DummyViz`  (line 17) — 

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_visualizer_reseter.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht
  - External: pytest, types
  - Aliases: pytest→pytest, SimpleNamespace→types, eeg_visu_reset_snpsht→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht, ss→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- **Functions**
  - `viz_core(tmp_path, monkeypatch)` (line 35) — Implements `viz_core` logic.
    - Decorators: pytest.fixture
    - Calls (intra): DummyIntegrator, DummyWidget, DummyWidget, DummyAxes, DummyCanvas
    - Calls (inter): types, monkeypatch.setattr, setattr
  - `test_handle_close_clicked_all_steps(viz_core)` (line 52) — Implements `test_handle_close_clicked_all_steps` logic.
    - Calls (intra): viz_core.dropdown_integrator.dropdown_widgets.values
    - Calls (inter): hasattr, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht, all, getattr, getattr
- **Classes**
  - `DummyWidget`  (line 8) — 
    - `__init__(self)` (line 9) — Implements `__init__` logic.
    - `hide(self)` (line 11) — Implements `hide` logic.
  - `DummyAxes`  (line 14) — 
    - `__init__(self)` (line 15) — Implements `__init__` logic.
      - Calls (inter): types, types, setattr
    - `clear(self)` (line 19) — Implements `clear` logic.
  - `DummyCanvas`  (line 22) [canvas] — 
    - `__init__(self)` (line 23) — Implements `__init__` logic.
    - `draw_idle(self)` (line 25) — Implements `draw_idle` logic.
  - `DummyIntegrator`  (line 28) — 
    - `__init__(self)` (line 29) — Implements `__init__` logic.
      - Calls (inter): types, setattr, setattr

### k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11  
`k01_core_eeg\k01_3_eeg_visualizer\tests\test_window_manager_0_5_11.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
  - External: pytest
  - Aliases: pytest→pytest, WindowManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
- **Functions**
  - `fake_slice_window(data, sfreq, start, window)` (line 4) — Implements `fake_slice_window` logic. [receives data]
  - `patch_slice(monkeypatch)` (line 9) — Implements `patch_slice` logic.
    - Decorators: pytest.fixture(autouse=True)
    - Calls (inter): monkeypatch.setattr, pytest.fixture
  - `test_current_window_delegates_to_slice(monkeypatch)` (line 22) — Implements `test_current_window_delegates_to_slice` logic.
    - Calls (intra): DummyViz
    - Calls (inter): k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager, wm.current_window
- **Classes**
  - `DummyViz`  (line 15) — 
    - `__init__(self)` (line 16) — Implements `__init__` logic.

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\channel_core_manager.py`
- **Imports**:
  - Internal: k02_eeg_input.eeg_visualizer_raw_preprocessor, k09_tools.matplotlib_cleanup_tools
  - Aliases: full_ordered_channels→k02_eeg_input.eeg_visualizer_raw_preprocessor, CloseEEGEvents→k09_tools.matplotlib_cleanup_tools
- **Classes**
  - `ChannelManager`  (line 6) — Version 0.5.7 – Responsible solely for initializing channel ordering, labels, and cleanup hooks on an EEGVisualizerCore.
    - `__init__(self, viz)` (line 12) — Implements `__init__` logic.
    - `init_channel_state(self)` (line 15) — Set up channel metadata and close‐event handler, plus placeholders/flags for Matplotlib‐drawn decorations.
      - Calls (inter): k09_tools.matplotlib_cleanup_tools

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_data_bootstrapper.py`
- **Imports**:
  - External: __future__, typing
  - Aliases: annotations→__future__, Any→typing
- **Classes**
  - `DataManager`  (line 66) — Bootstrap all EEG‑related attributes on a ``visualiser`` instance
    - `__init__(self, viz: Any)` (line 81) — Implements `__init__` logic.
    - `init_data_state(self)` (line 87) — Zero‑out all raw/data/timing attributes in **ten** steps

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_input_manager.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
  - External: PySide6.QtCore, PySide6.QtGui, __future__, os, sys, typing
  - Aliases: annotations→__future__, TYPE_CHECKING→typing, QObject→PySide6.QtCore, QTimer→PySide6.QtCore, Qt→PySide6.QtCore, QEvent→PySide6.QtCore, QKeyEvent→PySide6.QtGui, QWheelEvent→PySide6.QtGui, help01_on_key_event→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, help02_wheel_event→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, os→os, sys→sys, EEGVisualizerCore→k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- **Functions**
  - `_dbg(msg: str)` (line 19) — Print only when KANDA_DEBUG is set (any value).
    - Calls (inter): os.getenv, print
- **Classes**
  - `InputManager` (QObject) (line 25) — Single‐responsibility: installs the Qt event filter on your main_window & canvas, sets up flood‐protection & debounce timer, and delegates key/wheel events back to the visualizer.
    - `__init__(self, viz: EEGVisualizerCore)` (line 31) — Implements `__init__` logic.
      - Calls (inter): super, self._setup_timer, self._install_event_filter
    - `_setup_timer(self)` (line 37) — Implements `_setup_timer` logic.
      - Calls (inter): PySide6.QtCore, v.plot_timer.setSingleShot, v.plot_timer.timeout.connect, v._delayed_plot
    - `_install_event_filter(self)` (line 52) — Implements `_install_event_filter` logic. [dropdown builder]
      - Calls (intra): _dbg
      - Calls (inter): v.main_window.installEventFilter, v.canvas.setFocusPolicy, v.canvas.installEventFilter, v.canvas.setFocus
    - `eventFilter(self, obj, event)` (line 63) — Implements `eventFilter` logic. [dropdown builder]
      - Calls (inter): event.type, isinstance, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers, event.type, isinstance, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_input_handlers

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_memory_manager.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot, k09_tools.memory_leak_performance
  - Aliases: MemoryLeakDetector→k09_tools.memory_leak_performance, capture_initial_eeg_state→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- **Classes**
  - `MemoryManager`  (line 6) — Version 0.5.6 – Responsible solely for setting up the MemoryLeakDetector on an EEGVisualizerCore and capturing its initial memory snapshot.
    - `__init__(self, viz)` (line 13) — Implements `__init__` logic.
    - `init_memory_monitor(self)` (line 16) — Instantiate MemoryLeakDetector on viz, capture an 'init' snapshot, then record the initial EEG state.
      - Calls (inter): k09_tools.memory_leak_performance, v.memory_monitor.capture_snapshot, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot, print, v.memory_monitor.get_current_memory

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\core_plot_manager.py`
- **Classes**
  - `PlotManager`  (line 3) — Version 0.5.4 – Responsible solely for initializing Matplotlib placeholders and visual parameters on an EEGVisualizerCore.
    - `__init__(self, viz)` (line 9) — Implements `__init__` logic.
    - `init_matplotlib_state(self)` (line 12) — Set up placeholders for Matplotlib figure, axes, and canvas, and establish default plot parameters.

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\create_montage_stage_help.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
  - External: __future__, typing
  - Aliases: annotations→__future__, TYPE_CHECKING→typing, EEGVisualizerCore→k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- **Functions**
  - `create_mntg_stge(viz: 'EEGVisualizerCore', *, montage: str)` (line 9) — Montage dropdown → SignalPipeline
    - Calls (inter): getattr, pipeline.set_param, list, getattr, order.insert, pipeline.set_order, viz._refresh_view

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\data_extraction.py`
- **Imports**:
  - External: numpy
  - Aliases: np→numpy
- **Functions**
  - `extract_and_store_eeg_data(viz_core, raw)` (line 11) — Copy channels-of-interest from `raw` into viz_core’s data/times, then build the window-limited view
    - Calls (inter): list, raw.ch_names.index, raw.get_data, float, float, getattr, viz_core.window_mgr.current_view, numpy.searchsorted, numpy.searchsorted

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\data_state.py`
- **Functions**
  - `init_data_state(viz_core)` (line 8) — Initialize raw/data/timing attributes on an EEGVisualizerCore instance

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\dataframe_utils.py`
- **Imports**:
  - External: pandas
  - Aliases: pd→pandas
- **Functions**
  - `build_dataframe_from_data(viz_core)` (line 11) — Build or update `viz_core.dataframe` from `viz_core.data` and `viz_core.channel_names`
    - Calls (inter): pandas.DataFrame

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.diagnostics_utils  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\diagnostics_utils.py`
- **Imports**:
  - External: hashlib
  - Aliases: hashlib→hashlib
- **Functions**
  - `hash_raw_data(raw)` (line 5) — Generate a SHA256 fingerprint from EEG raw data to check integrity or changes.
    - Calls (inter): hashlib.sha256, raw.get_data

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\display_pyside6_eeg_visualizer.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_1_main_win_builder.main_win_builder, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager, k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_middle_bar
  - External: PySide6.QtCore, PySide6.QtWidgets, __future__, inspect, k05_combobox_forge.k05_4_cmbbx_constructor, k05_combobox_forge.k05_4_cmbbx_constructor.cmbbox_forge, logging, os
  - Aliases: annotations→__future__, inspect→inspect, os→os, logging→logging, QTimer→PySide6.QtCore, QToolBar→PySide6.QtWidgets, EEGMainWindowBuilder→k01_core_eeg.k01_1_main_win_builder.main_win_builder, InputManager→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager, DrpdwnPanelMiddleBar→k05_combobox_forge.k05_8_eeg_middle_tab_bar_cmbbx_lane.cmbbx_lane_middle_bar, cmbbx_ctor→k05_combobox_forge.k05_4_cmbbx_constructor, FilterToolbar→k05_combobox_forge.k05_4_cmbbx_constructor.cmbbox_forge
- **Functions**
  - `_find_filters_toolbar(core)` (line 27) — Prefer the middle lane toolbar (DrpdwnPanelMiddleBar) if present [dropdown builder]
    - Calls (inter): getattr, isinstance, isinstance, getattr, mw.findChildren, mw.findChildren, hasattr, hasattr, mw.findChildren
  - `_wire_close_button(core)` (line 57) — Attach the Close-EEG behavior to the toolbar close button
    - Calls (intra): _find_filters_toolbar
    - Calls (inter): logger.warning, hasattr, tb.set_close_action, logger.debug, logger.exception, hasattr, tb.close_eeg_requested.disconnect, tb.close_eeg_requested.connect, logger.debug, logger.exception, logger.warning
  - `_wire_unified_params(core)` (line 94) — No-k05, duck-typed wiring: - If a filters toolbar exists, optionally share a param manager and lane provider   without importing any k05 modules
    - Calls (intra): _find_filters_toolbar
    - Calls (inter): hasattr, tb.hide_dropdowns, logger.exception, getattr, hasattr, tb.set_param_manager, logger.exception, hasattr, callable, getattr, hasattr, hasattr, hasattr, tb.set_lane_provider, logger.exception
  - `_show_and_poke()` (line 169) — Implements `_show_and_poke` logic.
    - Calls (inter): tb.show, tb.findChildren, hasattr, ft._debug_state, hasattr, ft._coerce_valid_selection, ft.update_dropdowns, hasattr, ft._debug_state, hasattr, tb.show_all_dropdowns, hasattr, tb.show_dropdowns, logger.exception
  - `display_pyside6_eeg_visualizer(core)` (line 137) — Implements `display_pyside6_eeg_visualizer` logic.
    - Calls (intra): _wire_close_button, _find_filters_toolbar, _wire_unified_params, _wire_unified_params
    - Calls (inter): k01_core_eeg.k01_1_main_win_builder.main_win_builder, getattr, os.path.abspath, inspect.getfile, getattr, getattr, logging.getLogger, logging.getLogger, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager, hasattr, core.input_mgr.install, core.install_key_handler, PySide6.QtCore.singleShot, PySide6.QtCore.singleShot, tb.hide, core.eeg_loaded_signal.connect, logger.exception, PySide6.QtCore.singleShot

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\eeg_session_initializer.py`
- **Imports**:
  - External: __future__, logging, null_signal_pipeline, typing, window_core_manager
  - Aliases: annotations→__future__, logging→logging, Any→typing, Dict→typing, WindowManager→window_core_manager, NullSignalPipeline→null_signal_pipeline
- **Functions**
  - `initialize_eeg_session(core, raw)` (line 95) — initialize logic for `initialize_eeg_session`.
    - Calls (inter): logger.debug, raw.copy, null_signal_pipeline, window_core_manager, float, getattr, list, getattr, callable, refresh, logger.info
- **Classes**
  - `_NullSignalPipeline`  (line 69) — Minimal, no-op pipeline compatible with EEGVisualizerCore expectations
    - `__init__(self, raw)` (line 77) — Implements `__init__` logic.
    - `set_param(self, _name: str, _value: Any)` (line 81) — Implements `set_param` logic.
      - Calls (inter): self._cache.pop
    - `build(self)` (line 84) — build logic for `build`.
    - `fingerprint(self)` (line 87) — Implements `fingerprint` logic.
      - Calls (inter): float, self._raw.info.get, len, getattr

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_state  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\eeg_state.py`
- **Imports**:
  - External: PySide6.QtCore, time
  - Aliases: QTimer→PySide6.QtCore, Qt→PySide6.QtCore, time→time
- **Functions**
  - `init_eeg_state(viz_core)` (line 13) — Initialize EEG-specific flags and UI hooks on an EEGVisualizerCore instance
    - Calls (inter): float, PySide6.QtCore.singleShot, viz_core.eeg_loaded_signal.connect, print, time.time

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\graph_selection_handler.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection
  - External: logging
  - Aliases: logging→logging, help01_get_graph_data_source→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, help02_find_plot_function→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, help03_execute_plot→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, help04_restore_focus→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, NoGraphDataError→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, NoPlotFunctionError→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection
- **Functions**
  - `handle_graph_selection(core, graph_name: str)` (line 20) — Handles selection of a graph from dropdown and renders it on the canvas [dropdown builder]
    - Calls (inter): print, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_graph_selection, print, print

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\mcrvlt_snapshot_map_initializer.py`
- **Imports**:
  - Internal: k06_templates.eeg_table_templates, k07_mcrvlt_snapshot_map.mcrvlt_snapshot_map
  - External: logging
  - Aliases: logging→logging, EEGAmplitudeMap→k07_mcrvlt_snapshot_map.mcrvlt_snapshot_map, EEGAmplitudeMapTable→k06_templates.eeg_table_templates
- **Functions**
  - `initialize_mcrvlt_snapshot_map(core)` (line 14) — Signal handler: create the amplitude-map façade once raw data is available
    - Calls (inter): getattr, k06_templates.eeg_table_templates, k07_mcrvlt_snapshot_map.mcrvlt_snapshot_map, core.eeg_loaded_signal.connect, logger.error

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.null_signal_pipeline  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\null_signal_pipeline.py`
- **Imports**:
  - External: __future__, hashlib, logging, mne
  - Aliases: annotations→__future__, hashlib→hashlib, mne→mne, logging→logging
- **Classes**
  - `NullSignalPipeline`  (line 10) — k05-free pipeline stub: - Accepts set_param / set_order / fingerprint / build - Exposes a dict-like _cache so `.clear()` calls won’t fail - Always returns the source Raw unchanged
    - `__init__(self, source_raw: mne.io.BaseRaw)` (line 17) — Implements `__init__` logic.
      - Calls (inter): isinstance, TypeError
    - `set_param(self, stage: str, params: dict | object)` (line 26) — Implements `set_param` logic.
      - Calls (inter): str
    - `set_order(self, stages: list[str])` (line 29) — Implements `set_order` logic. [receives data]
      - Calls (inter): str
    - `fingerprint(self)` (line 32) — Implements `fingerprint` logic.
      - Calls (inter): hashlib.sha256, self._src.get_data, min, id, sorted, self._params.keys
    - `build(self)` (line 39) — build logic for `build`.
    - `clear_cache(self)` (line 44) — Implements `clear_cache` logic.
      - Calls (inter): self._cache.clear

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\pipeline_reset.py`
- **Imports**:
  - External: eeg_session_initializer, hashlib, logging, null_signal_pipeline, typing, window_core_manager
  - Aliases: logging→logging, NullSignalPipeline→null_signal_pipeline, WindowManager→window_core_manager, hashlib→hashlib, Any→typing, Dict→typing, _NullSignalPipeline→eeg_session_initializer, CoreWindowManager→window_core_manager
- **Functions**
  - `reset_pipeline_state(core)` (line 212) — Implements `reset_pipeline_state` logic.
    - Calls (intra): _safe_refresh
    - Calls (inter): getattr, null_signal_pipeline, window_core_manager, float, getattr, logger.error
  - `_safe_refresh(core)` (line 250) — Implements `_safe_refresh` logic.
    - Calls (inter): core.pipeline.build, core._extract_and_store_eeg_data, core.update_plot_view, logger.info, logger.error
  - `hash_raw_data(raw)` (line 259) — Deterministic fingerprint of the underlying samples for quick sanity checks.
    - Calls (inter): hashlib.sha256, raw.get_data
- **Classes**
  - `_NullSignalPipeline`  (line 118) — Minimal, no-op pipeline compatible with EEGVisualizerCore expectations
    - `__init__(self, raw)` (line 126) — Implements `__init__` logic.
    - `set_param(self, _name: str, _value: Any)` (line 130) — Implements `set_param` logic.
      - Calls (inter): self._cache.pop
    - `build(self)` (line 133) — build logic for `build`.
    - `fingerprint(self)` (line 136) — Implements `fingerprint` logic.
      - Calls (inter): float, self._raw.info.get, len, getattr

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\plot_core_timer_manager.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_plot_timer
  - Aliases: help01_delayed_plot→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_plot_timer
- **Classes**
  - `PlotTimerManager`  (line 5) — Version 0.5.10 – Responsible for handling the debounced redraw trigger via QTimer.
    - `__init__(self, viz)` (line 11) — Implements `__init__` logic.
    - `delayed_plot(self)` (line 14) — Slot connected to self.viz.plot_timer.timeout
      - Calls (inter): k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_plot_timer

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\plot_view_updater.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_update_plot_view
  - External: logging
  - Aliases: logging→logging, help03_update_plot_view_postplot→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_update_plot_view, help04_update_plot_view_canvas→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_update_plot_view, help05_update_plot_view_ui_state→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_update_plot_view, help06_update_plot_view_timeline→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_update_plot_view
- **Functions**
  - `update_plot_view_safely(core)` (line 26) — Central EEG view redraw function
    - Calls (inter): hasattr, core.profiler.before_render, getattr, core.ax.__class__.__name__.startswith, logger.debug, logger.error, core.current_window, logger.warning, core.renderer.render, logger.debug, hasattr, hasattr, core.timeline_widget.timeline_bar.set_show_labels, logger.debug, logger.exception, hasattr, hasattr, core.timeline_widget.update_bracket_position, hasattr, hasattr, core.timeline_widget.timeline_bar.set_window, core.timeline_widget.timeline_bar.update, logger.debug, logger.warning, logger.debug, fn, logger.warning, hasattr, core.profiler.after_render, logger.info, logger.debug

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\sensitivity_handler.py`
- **Imports**:
  - External: logging
  - Aliases: logging→logging
- **Functions**
  - `handle_sensitivity_change(core, μV: int)` (line 12) — Called when the Sensitivity dropdown changes (in µV)
    - Calls (inter): logger.debug, float, abs, getattr, logger.debug, logger.info, core.update_plot_view

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\signal_core_manager.py`
- **Classes**
  - `SignalManager`  (line 3) — Version 0.5.8 – Responsible solely for wiring up Qt signals used by the EEGVisualizerCore.
    - `__init__(self, viz)` (line 9) — Implements `__init__` logic.
    - `init_signals(self)` (line 12) — Connects EEGVisualizerCore.Qt signals to their handlers.
      - Calls (inter): print, v.eeg_loaded_signal.connect, v.eeg_loaded_signal.connect, print, print

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\splash_core_manager.py`
- **Imports**:
  - Internal: Kanda_Splash.kanda_splash_roboto
  - External: PySide6.QtCore, PySide6.QtWidgets
  - Aliases: KandaSplashImageText→Kanda_Splash.kanda_splash_roboto, QSizePolicy→PySide6.QtWidgets, QTimer→PySide6.QtCore
- **Classes**
  - `SplashManager`  (line 7) — Version 0.5.5 – Responsible solely for showing the Kanda splash screen on an EEGVisualizerCore.
    - `__init__(self, viz)` (line 13) — Implements `__init__` logic.
    - `show_splash(self, path: str='k12_images/cocteau2.png')` (line 16) — Displays the splash screen using KandaSplashImageText, wires up size policy, and schedules canvas focus.
      - Calls (inter): getattr, Kanda_Splash.kanda_splash_roboto, splash.setSizePolicy, splash.adjustSize, PySide6.QtCore.singleShot

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\start_snapshot.py`
- **Imports**:
  - Internal: k09_tools.matplotlib_cleanup_tools, k09_tools.ui_state_controller
  - External: logging, numpy
  - Aliases: update_ui_state_based_on_context→k09_tools.ui_state_controller, cleanup_all_artists→k09_tools.matplotlib_cleanup_tools, log_tick_labels→k09_tools.matplotlib_cleanup_tools, np→numpy, logging→logging
- **Functions**
  - `capture_initial_eeg_state(visualizer)` (line 11) — Captures the clean EEG-related state of the app (before EEG is loaded)
    - Calls (inter): getattr, getattr, getattr, getattr, logging.info
  - `reset_to_initial_eeg_state(visualizer)` (line 34) — Implements `reset_to_initial_eeg_state` logic.
    - Calls (inter): hasattr, logging.warning, logging.info, hasattr, visualizer.mcrvlt_snapshot_map.hide_amplitude_map_elements, logging.error, k09_tools.matplotlib_cleanup_tools, hasattr, visualizer.ruler_ax.remove, hasattr, hasattr, logging.info, logging.error, hasattr, visualizer.ax.set_yticks, visualizer.ax.set_yticklabels, visualizer.ax.tick_params, logging.debug, hasattr, visualizer.label_ax.set_yticks, visualizer.label_ax.set_yticklabels, visualizer.label_ax.tick_params, logging.debug, hasattr, k09_tools.matplotlib_cleanup_tools, hasattr, k09_tools.matplotlib_cleanup_tools, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, snapshot.get, numpy.array_equal, hasattr, visualizer.timeline_bar.set_duration, visualizer.timeline_bar.hide, visualizer.timeline_bar.update, hasattr, visualizer.show_placeholder_image, hasattr, isinstance, visualizer.tabs.get, hasattr, hasattr, tab.update_duration_label, getattr, hasattr, ft.hide_close_button, hasattr, ft.hide_dropdowns, ft.hide, logging.debug, logging.error, getattr, getattr, btn.hide, logging.debug, logging.error, k09_tools.ui_state_controller, logging.info

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\timeline_manager_core.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_timeline
  - External: logging
  - Aliases: logging→logging, help01_compute_safe_start→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_timeline, help02_emit_timeline_signal→k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_timeline
- **Classes**
  - `TimelineManager`  (line 17) — EEGVisualizer timeline manager
    - `__init__(self, viz)` (line 27) — Implements `__init__` logic.
    - `handle_window_moved(self, start: float, end: float)` (line 34) — Triggered when the bracket is dragged
      - Calls (inter): logger.debug, v.update_plot_view
    - `handle_timeline_moved(self, start_time: float, end_time: float)` (line 50) — Called when some other widget (like a heatmap tab) moves the timeline
      - Calls (inter): logger.debug, v.update_plot_view
    - `handle_timeline_clicked(self, clicked_time: float)` (line 66) — User clicked the timeline bar
      - Calls (inter): k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_timeline, logger.debug, v.update_plot_view, getattr, v.timeline_widget.manager.window_moved.emit, logger.debug, logger.warning, k01_core_eeg.k01_2_visualizer.plotting_pipeline.help_timeline, logger.debug, logger.warning

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\ui_core_manager.py`
- **Imports**:
  - External: PySide6.QtCore, __future__, logging
  - Aliases: annotations→__future__, logging→logging, QObject→PySide6.QtCore, Signal→PySide6.QtCore
- **Classes**
  - `NullLowPassDropdown` (QObject) (line 41) — Minimal stub to preserve attribute presence and signal wiring without k05
    - `__init__(self, parent=None)` (line 49) — Implements `__init__` logic.
      - Calls (inter): super
    - `set_value(self, _val: int)` (line 53) — Implements `set_value` logic.
    - `show(self)` (line 54) — Implements `show` logic.
    - `hide(self)` (line 55) — Implements `hide` logic.
    - `setParent(self, _p)` (line 56) — Implements `setParent` logic.
  - `UIManager`  (line 59) — 
    - `__init__(self, viz)` (line 60) — Implements `__init__` logic.
    - `init_ui_placeholders(self)` (line 63) — initialize logic for `init_ui_placeholders`.
      - Calls (intra): NullLowPassDropdown
      - Calls (inter): hasattr, v.lowpass_dropdown.lp_changed.connect, logger.debug

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\ui_helpers.py`
- **Imports**:
  - External: PySide6.QtCore
  - Aliases: Qt→PySide6.QtCore
- **Functions**
  - `force_canvas_focus(viz_core)` (line 11) — Ensure the Matplotlib canvas widget receives keyboard focus
    - Calls (inter): getattr, canvas.setFocus, canvas.raise_, canvas.repaint, canvas.hasFocus

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\visualizer_reset_snpsht.py`
- **Imports**:
  - Internal: k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
  - External: __future__, gc, logging
  - Aliases: annotations→__future__, logging→logging, gc→gc, reset_to_initial_eeg_state→k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- **Functions**
  - `eeg_visu_reset_snpsht(viz_core)` (line 6) — Reset everything back to the initial snapshot, clear axes, hide UI elements, and drop heavy references so memory can be reclaimed
    - Calls (inter): hasattr, hasattr, viz_core.plot_timer.stop, logger.debug, hasattr, viz_core.timeline_moved.disconnect, k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot, logger.debug, getattr, viz_core.tabs.get, getattr, hasattr, panel.snapshot_controls_state, hasattr, getattr, getattr, viz_core.dropdown_integrator.dropdown_widgets.values, w.hide, getattr, hasattr, hasattr, tw.timeline_bar.set_show_labels, tw.hide, getattr, viz_core.ax.clear, viz_core.ax.xaxis.set_tick_params, getattr, viz_core.canvas.draw_idle, getattr, hasattr, amp.deleteLater, logger.debug, getattr, hasattr, viz_core.pipeline._cache.clear, logger.debug, getattr, hasattr, setattr, hasattr, setattr, getattr, viz_core.dropdown_integrator.widgets_by_name.get, hp_dd.set_cutoff, setattr, gc.collect, logger.info

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\window_core_manager.py`
- **Imports**:
  - External: __future__, dataclasses, mne, numpy, typing
  - Aliases: annotations→__future__, dataclass→dataclasses, np→numpy, mne→mne, Tuple→typing
- **Classes**
  - `_View`  (line 10) [canvas] — 
  - `WindowManager`  (line 17) — k05-free window slicer for Raw objects + NumPy cache builder
    - `__init__(self, source: mne.io.BaseRaw | object, window_sec: float=9.0)` (line 24) — Implements `__init__` logic.
      - Calls (inter): hasattr, isinstance, hasattr, isinstance, isinstance, ValueError, float, float
    - `current_view(self, start_time: float | None=None)` (line 40) — Implements `current_view` logic.
      - Calls (inter): self.current_window
    - `current_window(self, start_time: float | None=None)` (line 46) — Implements `current_window` logic.
      - Calls (intra): _View
      - Calls (inter): float, max, min, float, int, round, int, round, self._raw.get_data
    - `set_speed(self, speed_mm_s: int)` (line 54) — Implements `set_speed` logic.
      - Calls (inter): int
    - `set_window(self, seconds: float)` (line 57) — Implements `set_window` logic.
      - Calls (inter): float, max

### k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_setup  
`k01_core_eeg\k01_3_eeg_visualizer\visualizer_core_helpers\window_core_setup.py`
- **Imports**:
  - External: PySide6.QtCore, PySide6.QtWidgets
  - Aliases: QMainWindow→PySide6.QtWidgets, QWidget→PySide6.QtWidgets, QVBoxLayout→PySide6.QtWidgets, Qt→PySide6.QtCore
- **Functions**
  - `create_main_window()` (line 6) — create logic for `create_main_window`.
    - Calls (inter): PySide6.QtWidgets, window.setWindowFlags, window.setWindowTitle
  - `create_main_widget()` (line 12) — create logic for `create_main_widget`.
    - Calls (inter): PySide6.QtWidgets, PySide6.QtWidgets, main_layout.setContentsMargins, main_layout.setSpacing

## Module Dependencies
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11 → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot

## Cross-Module Function Calls
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_data_bootstrapper:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.__init__ → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore._delayed_plot → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.current_view → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.current_window → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_close_clicked → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_timeline_clicked → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_timeline_moved → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:EEGVisualizerCore.on_window_moved → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.timeline_manager_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_channel_manager_0_5_7:test_init_channel_state_sets_attributes → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.channel_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_current_raw_assigned → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_current_raw_assigned → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_with_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_with_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_without_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_extraction:test_extract_without_window_mgr → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_extraction:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state:test_init_data_state_sets_defaults → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:__new__
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_data_state:test_init_data_state_sets_defaults → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.data_state:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_missing_channels → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_missing_data → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_dataframe_utils:test_build_dataframe_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.dataframe_utils:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_display_pyside6_eeg_visualizer:test_display_pyside6_gui_installs_everything → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_eeg_session_initializer:test_initialize_eeg_session_sets_up_fields → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.eeg_session_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_filter_pipeline:viz → k01_core_eeg.k01_3_eeg_visualizer.eeg_visualizer_core:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_nograph → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_noplot → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_graph_selection_handler:test_handle_graph_selection_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.graph_selection_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer:test_initialize_mcrvlt_snapshot_map_creates_and_wires → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_mcrvlt_snapshot_map_initializer:test_initialize_mcrvlt_snapshot_map_no_raw_returns_false → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.mcrvlt_snapshot_map_initializer:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler:test_create_montage_stage_does_nothing_if_pipeline_missing → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_montage_handler:test_create_montage_stage_sets_pipeline_and_triggers_refresh → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.create_montage_stage_help:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_pipeline_reset:test_reset_pipeline_state_sets_pipeline_and_window → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.pipeline_reset:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_manager_0_5_4:test_init_matplotlib_state_sets_attributes → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_plot_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_timer_manager_0_5_10:test_delayed_plot_invokes_helper → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_core_timer_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_plot_view_updater:test_update_plot_view_runs_render_and_helpers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.plot_view_updater:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_sensitivity_handler:test_handle_sensitivity_change → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.sensitivity_handler:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_signal_manager_0_5_8:test_init_signals_connects_handlers → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.signal_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5:test_show_splash_creates_and_configures → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_splash_manager_0_5_5:test_show_splash_idempotent → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.splash_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_failure → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_no_canvas → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_ui_helpers:test_force_canvas_focus_success → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.ui_helpers:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_visualizer_reseter:test_handle_close_clicked_all_steps → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:<module>
- k01_core_eeg.k01_3_eeg_visualizer.tests.test_window_manager_0_5_11:test_current_window_delegates_to_slice → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.window_core_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_memory_manager:MemoryManager.init_memory_monitor → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.display_pyside6_eeg_visualizer:display_pyside6_eeg_visualizer → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.core_input_manager:<module>
- k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.visualizer_reset_snpsht:eeg_visu_reset_snpsht → k01_core_eeg.k01_3_eeg_visualizer.visualizer_core_helpers.start_snapshot:<module>

