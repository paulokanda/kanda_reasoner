"""
 KandaDropDowns – what lives where?

 KandaDropDowns/
├── manager/                    # “brains” of the system
│   ├── __init__.py             # re-exports public API
│   ├── schema_loader.py        # lazy-loads & caches JSON schemas
│   ├── parameter_manager_04_1_2    # EEGParameterManager (value store + dependency rules)
│   ├── drpdwn_integrator_eeg.py  # builds widgets, wires signals
│   └── tests/                  # pytest specs for the manager
│       └── test_…py
└── widgets/                    # one file per concrete widget
    ├── __init__.py             # WIDGET_REGISTRY = { "Name": Class, … }
    ├── sensitivity_drpdwn.py # emits `sensitivity_changed(int µV)`
    ├── montages_drpdwn.py    # emits `montage_changed(str)`
    └── …                       # new widgets drop in here

How the pieces talk to each other
flowchart LR
    subgraph Widgets
        SD(SensitivityDropdown)
        MD(MontagesDropdown)
        New(..your next widget..)
    end

    JSON[core_filters_json_schema.json] --(parse)--> Integrator
    Widgets -. registered in . -> Integrator
    Integrator -- create / show --> Layouts
    Integrator -- value-changed --> ParamMgr
    ParamMgr -- emits parameter_changed --> Visualizer
    MD -- montage_changed --> Visualizer  <!-- direct pass-through -->

    core_filters_json_schema.json
    Declarative recipe – defines which dropdowns exist, their group (“middle”), default values, tooltips, dependencies, …

    widgets/__init__.py
    Central WIDGET_REGISTRY → maps the name in the JSON to the actual Python class.
    When you drop a new widget file into widgets/, just add it to the registry – no other file changes.

    drpdwn_integrator_eeg.py
    Orchestrator

        reads the schema once

        instantiates each widget class

        plugs it into the correct Qt layout (layout_map = {"middle": …})

        wires the widget’s “value changed” signal either

            directly to the EEGVisualizerCore (special cases like Montage), or

            through EEGParameterManager for dependency validation.

    parameter_manager_04_1_2
    Lightweight store: .set_parameter(name, value)

        Keeps current values

        Validates requires / depends_on rules from the JSON

        Emits parameter_changed(name, value) when safe.

    Tests (manager/tests/…)
    Tiny PySide-6/pytest‐qt specs check that:

        Integrator builds all widgets from the JSON

        Dependencies block illegal combinations

        Widgets hide/show correctly when EEG loads/unloads.

Typical workflow for a new dropdown

    Create widget in widgets/your_dropdown.py

        subclass QComboBox/QWidget

        emit a dedicated Qt Signal (e.g. value_changed(float))

    Add to registry

    # widgets/__init__.py
from .your_dropdown import YourDropdown
WIDGET_REGISTRY["YourNewOption"] = YourDropdown

{
  "name": "YourNewOption",
  "group": "middle",
  "stage": "visualization",
  "options": [/* … */],
  "default": 42,
  "tooltip": "Explain what this does"
}

(Optional) handle it in EEGVisualizerCore

def on_yournewoption_changed(self, value):
    # react to selection

Done – no change needed in drpdwn_integrator_eeg.py.

Lifecycle in the GUI

    Start-up – Integrator builds widgets but hides them.

    EEG file loaded – EEGTab._on_data_ready() shows the widgets
    (dd = drpdwn_integrator_eeg.widgets_by_name["Sensitivity"]; dd.show()).

    Close EEG – reset_to_initial_eeg_state() iterates over
    widgets_by_name.values() and hides them again.

Same logic, same code-path, no special cases – both Sensitivity and Montage dropdowns obey the “only visible when EEG is present” rule.

"""

