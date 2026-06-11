
"""
# Copyright (c) Paulo Afonso Medeiros Kanda
# Neurologist, Neurophysiologist, PhD - Hospital das Clínicas da Universidade de São Paulo (FMUSP)
#
# Rafael Guimarães Kanda
# Neurologist, Neurophysiologist
# Faculdade de Medicina de Botucatu, Universidade Estadual Paulista "Júlio de Mesquita Filho" (UNESP-Botucatu)
# Universidade Estadual de Campinas (UNICAMP)
#
# Felipe Guimarães Kanda
# Faculdade de Medicina da Universidade de Taubaté (UNITAU)
#
# License: Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)
# This software is free to use for academic and non-commercial purposes, provided that all original authors are properly credited.
# Modification and distribution of modified versions are NOT allowed without prior written authorization from the authors.
# Any use or redistribution must include this copyright notice.
#
# This application/script uses code and incorporates components from the MNE-Python EEG processing library (BSD-3-Clause License).
#
# For more information, contact the corresponding author.
# pkanda@alumni.usp.br    paulokanda@gmail.com  kanda@unicamp.br

+--------------------------------------------------------------+
|                🧠 EEGVisualizerCore (QObject)                    |
|      Main EEG handler: load, navigate, and display EEG       |
+------------------------------+-------------------------------+
                               |
            +------------------+------------------+
            |                                     |
  +---------v---------+               +-----------v-----------+
  |  🖼️ Canvas Init     |               |  📂 EegVisualizerLoaderLogic        |
  |  - fig, ax, canvas |               |  - Loads .raw, .data     |
  |  - Matplotlib + Qt |               |  - Sets .eeg_loaded      |
  +-------------------+               +--------------------------+
            |                                     |
            +------------------+------------------+
                               |
                      +--------v--------+
                      |  📊 Plot View     |
                      |  update_plot_view() |
                      +------------------+
                               |
         +---------------------+----------------------+
         |                                            |
+--------v--------+                        +----------v----------+
| prepare_plot_   |                        | plot_default(self)  |
| window(self)     |                        | - Draw EEG signals  |
+------------------+                        | - Add red line etc.|
                                            +---------------------+

EEGVisualizerCore handles:
 ├── ⚙️ EEG state (window_size, current_start, etc.)
 ├── ⏱️ TimelineBar clicks → on_timeline_clicked()
 ├── 📢 show_kanda_splash() during startup
 ├── 🧼 force_canvas_focus() and canvas.repaint()
 └── 🧹 cleanup by EEGMainWindowBuilder

User Interaction:
-----------------
+---------------------------+
| ⌨️ Keyboard Input (on_key) |
|  ↑↓→← + - keys            |
+---------------------------+
| 🖱️ Scroll Input (wheel_event) |
|  - 1s forward/back        |
+---------------------------+
| Both inputs use QTimer    |
| (150ms debounce)          |
+---------------------------+

Input Flood Protection:
-----------------------
- _register_input_event()
   - Limits excessive key or scroll activity
   - Shows warning via warning_label (if present)

Amplitude Map Overlay (optional):
---------------------------------
- self.mcrvlt_snapshot_map
  ├─ table.df → alternate data source
  ├─ red_line_visible → visual control
  └─ reset_red_line_to_middle()

Graph Selector Support:
-----------------------
- _handle_graph_selection(name)
  ├─ If mcrvlt_snapshot_map.table exists → use its data
  └─ Else use rawself.current_raw (if loaded)
  └─ Calls self.plot_panel.<graph_name>(data)

Canvas Management:
------------------
- All EEG traces are drawn on:
  ├─ self.canvas ← FigureCanvasQTAgg
  ├─ self.fig ← matplotlib Figure
  └─ self.ax ← matplotlib Axes

🔍 Breakdown by Functional Area

1. 🧠 Initialization & Splash

    Ensures folders (ensure_eeg_folders())

    Creates figure, canvas, splash screen (show_kanda_splash())

2. 🖼️ Canvas Setup

    initialize_main_plot() provides:

        self.fig, self.ax, self.canvas

    Canvas is embedded in Qt layout and attached to EEGTab

3. 📂 EEG File Loading

    EegVisualizerLoaderLogic(self) allows file selection

    Sets self.current_raw, self.data, self.eeg_loaded = True

4. 📊 EEG Plot View

    update_plot_view() drives plotting:

        Prepares the window

        Calls plot_default(self)

        Updates red line

        Draws canvas

5. ⌨️ / 🖱️ User Input

    on_key(event) handles keys: zoom in/out, nav left/right

    wheel_event(event) scrolls time window ±1s

    QTimer(150ms) debounces updates

    Flood protection via _register_input_event(type)

6. ⏱️ Timeline Bar

    on_timeline_clicked(time) updates current_start

    Refreshes plot + red line position

7. 📈 Amplitude Map

    If self.mcrvlt_snapshot_map is active:

        Uses table.df for graphs

        Adjusts red line position and overlay

8. 🧼 Cleanup & Canvas Focus

    force_canvas_focus() ensures canvas receives input

    display_in_pyside6() invokes builder + input install

"""
################################
"""
Absolutely! Here's a fully detailed pipeline summary and functionality interaction map of the EEGVisualizerCore class, written as if it's intended to help another AI understand the complete internal logic and external interactions for intelligent code enhancement:
🧠 EEGVisualizerCore - Architecture & Functional Summary for AI Integration

This class is the k01_core_eeg GUI-integrated EEG data visualizer. It uses PySide6 for UI, Matplotlib for signal rendering, and several custom modules for managing EEG state, UI events, memory profiling, splash screens, and input regulation.
+----------------------+
| EEGVisualizerCore        |
+----------------------+
       |
       ▼
[1] Initialization
    ├── Memory profiling (MemoryLeakDetector)
    ├── Folder check (ensure_eeg_folders)
    ├── Canvas & Axes (initialize_main_plot)
    ├── Splash (KandaSplashImageText)
    ├── EEG loader (EegVisualizerLoaderLogic)
    ├── Timeline + RedLine + UI elements prep
       |
       ▼
[2] EEG File Loading
    ├── EEG data populated via EegVisualizerLoaderLogic
    └── Channel ordering (full_ordered_channels)
       |
       ▼
[3] EEG Plotting Engine
    ├── update_plot_view()
    │   ├─ prepare_plot_window()
    │   ├─ plot_default()
    │   ├─ red line logic
    │   ├─ canvas.draw()
    │   └─ update_ui_state_based_on_context()
       |
       ▼
[4] UI Interaction
    ├── Keyboard (on_key)
    ├── Scroll (wheel_event)
    ├── Click timeline (on_timeline_clicked)
    └── Debounce + flood protection (_register_input_event)
       |
       ▼
[5] Display Management
    ├── display_in_pyside6()
    ├── install_key_handler()
    └── force_canvas_focus()

🔗 Key Interactions with Other Modules

| External Module/Class                    | Purpose / Interaction Point                               |
| ---------------------------------------- | --------------------------------------------------------- |
| `EegVisualizerLoaderLogic(self)`                    | UI-based file dialog; sets `.raw`, `.data`, `.eeg_loaded` |
| `initialize_main_plot()`                 | Sets up `self.fig`, `self.ax`, `self.canvas`              |
| `plot_default(self)`                     | Core EEG rendering logic using Matplotlib                 |
| `prepare_plot_window(self)`              | Prepares view window (clears axes, aligns channels)       |
| `CloseEEGEvents(self)`                   | Hook to safely close or clean memory                      |
| `KandaSplashImageText`                   | Splash screen until EEG file is loaded                    |
| `update_ui_state_based_on_context(self)` | Dynamically updates dropdowns, config states              |
| `SensitivityDropdown`                    | Dropdown to update EEG amplitude scaling                  |



🧠 Detailed Summary of Major Functions
✅ Initialization

    Ensures necessary folders exist (ensure_eeg_folders)

    Sets default plot properties, state flags, splash screen

    Prepares plot window via initialize_main_plot

    Loads EEG data using EegVisualizerLoaderLogic

    Captures memory snapshot with MemoryLeakDetector

📊 update_plot_view()

The master EEG rendering controller:

    Defines time window and indexes (_start_idx, _end_idx)

    Invokes prepare_plot_window() and plot_default(self)

    Updates red line from amplitude map

    Re-renders Matplotlib canvas

    Refreshes UI via update_ui_state_based_on_context()

🧭 User Interaction Handlers

    Keyboard: on_key(event) for zoom/pan/amplitude

    Mouse Wheel: wheel_event(event) for ±1s time scroll

    Timeline Click: on_timeline_clicked(t) for jump-to-time

🛡️ Input Protection

    _register_input_event() rate-limits scrolls/keys (max 20/sec)

    Uses QTimer for debounce, prevents UI overload

🎚️ Amplitude Scale Logic

    _update_amplitude_scale(µV)

    Updates self.amplitude_scale

    Redraws plot using new sensitivity

🧪 test_signal_connection()

Verifies Qt signal-slot for amplitude sensitivity dropdowns
📁 Data Management

    update_eeg_data(new_data) to replace EEG matrix

    build_dataframe_from_data() to create labeled pandas.DataFrame

🔎 Graph Selection

    _handle_graph_selection(name)

        Triggers plot methods from self.plot_panel

        Source: mcrvlt_snapshot_map.table.df or self.current_raw

📦 Pipeline Canvas Hierarchy

self.canvas     ← matplotlib.backends.backend_qtagg.FigureCanvasQTAgg
  ├─ self.fig   ← matplotlib.figure.Figure
  └─ self.ax    ← fig.add_subplot(1,1,1)
       ├─ EEG Traces
       ├─ Red Line (vline)
       └─ Channel Labels & Guides

⚠️ Internal Flags & Performance Enhancers
Flag	Purpose
self._key_handler_installed	Prevents duplicate event filter setup
self._update_texts	Forces refresh of labels/text overlays
self.eeg_data_changed	Used to refresh data pipeline
self.plot_timer	150ms debounce to throttle redraws
self._scroll/_keypress_count	Prevents user interaction spam

🔧 Notable Expansion Points for AI Enhancements

    🧠 Graph Recommendation Engine: Analyze self.current_raw or .table.df for plotting suggestions

    ⚙️ UI Action Optimizer: Automate optimal zoom, sensitivity based on user behavior

    📈 Real-Time Metrics: Use MemoryLeakDetector trends to adapt rendering speed

    🧪 Smart Testing Agent: Expand test_signal_connection() with dynamic scenarios

                         +--------------------------+
                         |     EEGVisualizerCore        |
                         |    (Main Controller)     |
                         +------------+-------------+
                                      |
     +--------------------------------+--------------------------------+
     |                                |                                |
+----v-----+                 +--------v--------+               +-------v--------+
| Init     |                 | EEG File Loader |               | Matplotlib UI  |
| (State,  |                 | EegVisualizerLoaderLogic   |               | initialize_*   |
| Memory)  |                 | → raw, data     |               | → fig, ax, canvas
+----+-----+                 +--------+--------+               +--------+--------+
     |                               |                                  |
     |              +----------------v----------------+                 |
     |              | Channel Order & EEG Snapshots   |                 |
     |              | full_ordered_channels           |                 |
     |              +----------------+----------------+                 |
     |                               |                                  |
     +-------------------+           |                                  |
                         |           |                                  |
              +----------v-----------v---------+                        |
              |      update_plot_view()        |                        |
              |  (Plot Manager & Controller)   |                        |
              +------+--------+----------------+                        |
                     |        |                                         |
     +---------------v--+  +--v-----------------+             +---------v--------+
     | prepare_plot_()  |  |  plot_default()    |             | Amplitude Map    |
     | Layout + Grid    |  | EEG Signals Render |             | (table.df)       |
     +------------------+  +--------------------+             +---------+--------+
                                                                          |
                                                                  +-------v-------+
                                                                  | Red Line Ctrl |
                                                                  | Reset/Midline |
                                                                  +---------------+

USER INTERACTION PIPELINE:
==========================
+-----------------------+
|  ⌨️  on_key(event)     |
|  ← → + - ↑ ↓          |
+-----------+-----------+
            |
    +-------v-------+
    | Adjust Window |
    | Zoom/Sensitivity |
    +-------+-------+
            |
        +---v---+
        | Plot  |
        +-------+

+------------------------+
| 🖱️  wheel_event(event) |
| Scroll ↕ (±1s)         |
+-----------+------------+
            |
        +---v---+
        | Debounced Plot |
        +---------------+

+---------------------------+
| 🕒  on_timeline_clicked()  |
| Jump to clicked time      |
+-----------+---------------+
            |
        +---v---+
        | update_plot_view |
        +------------------+

UTILITIES & HELPERS:
====================
+--------------------------+
| MemoryLeakDetector       |
+--------------------------+
| force_canvas_focus()     |
| show_kanda_splash()      |
| display_in_pyside6()     |
| update_ui_state_*        |
+--------------------------+
| _register_input_event()  | (Flood Protection)
+--------------------------+

EXTENSION ZONES:
================
+-----------------------------+
| plot_panel.graph_X(df)     |  <- dynamic graph callbacks
+-----------------------------+
| update_amplitude_scale()   |  <- sensitivity logic
+-----------------------------+


"""


