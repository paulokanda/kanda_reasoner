"""
How the dropdowns + Close-EEG button follow the EEG life-cycle

(show only after data has been loaded, disappear when you “✖ Close EEG”)

EEGVisualizerCore.display_in_pyside6()

└─ 1.  EEGMainWindowBuilder.build_and_show()             ← all layouts created
   └─ EEGTab._setup_ui_once()
      ├─ a)  middle_bar   (EEG3DBar)                     ← container for pro_filters
      ├─ b)  close_btn  = eeg_traces_tab_close_button()  ← starts hidden
      └─ c)  save middle_bar.layout  → visualizer.middle_in_tab_bar_layout
└─ 2.  DropdownIntegrator(...)                           ← builds dropdown widgets
   • reads JSON schema, instantiates widgets
   • widgets are **added to middle_bar.layout**
   • each widget is `.hide()`d right away
└─ 3.  GUI idle → waiting for user to *Load EEG* …

When the user loads an EEG file

EegVisualizerLoaderLogic → EEGVisualizerCore.emit_eeg_loaded_signal()
└─ EEGTab._on_data_ready()              (slot connected to eeg_loaded_signal)
   ├─ middle_bar.timeline_widget.show()
   ├─ close_btn.show()                  ← becomes visible now
   └─ for name in ("Sensitivity","Montage"):
         dd = drpdwn_integrator_eeg.widgets_by_name[name]
         dd.show()                      ← both dropdowns are revealed

Additionally: each dropdown was wired in DropdownIntegrator._wire_value_changed
so that changes end up in EEGVisualizerCore.on_sensitivity_changed /
on_montage_changed, which in turn call _recompute_amplitude_scale() or reload
the raw object and finally update_plot_view().
That is why selecting a new sensitivity immediately redraws the traces.

When the user clicks ✖ Close EEG (or closes the “EEG Traces” tab)
EEGTab.close_btn.clicked  →  reset_to_initial_eeg_state(visualizer)
└─ 1. cleanup_all_artists()            ← clears Matplotlib stuff
└─ 2. drpdwn_integrator_eeg loop:
     for w in widgets_by_name.values(): w.hide()
└─ 3. tab.eeg_traces_tab_close_btn.hide()
└─ 4. update_ui_state_based_on_context() (guarded)

Result ➜ all dropdowns and the close button disappear; timeline is hidden; the
canvas shows the splash again — ready for a fresh EEG load.

Quick mental map

MiddleTabBar (QHBoxLayout)
│
├── SensitivityDropdown  ← built by DropdownIntegrator, .hide() initially
├── MontagesDropdown     ← idem
├── … other dropdowns …
└── close_btn            ← created by EEGTab, .hide() initially


| Lifecycle phase       | Dropdowns | ✖ Close EEG |
| --------------------- | --------- | ----------- |
| App start-up          | hidden    | hidden      |
| After successful load | **shown** | **shown**   |
| When reset/EEG closed | hidden    | hidden      |

Everything is driven by two single places:

    EEGTab._on_data_ready() → show pro_filters once visualizer.data is ready.

    reset_to_initial_eeg_state() → hide them again during cleanup.

That’s the entire circuit—no extra state flags needed. If any step mis-behaves,
these are the two methods to inspect first.









"""

