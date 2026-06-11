# help_eeg_visualizer_loader_logic.py
"""
Help & Documentation Module: EegVisualizerLoaderLogic

This module provides a comprehensive breakdown of the EegVisualizerLoaderLogic class,
showing its responsibilities, interactions with other modules, and a detailed ASCII
pipeline of data flow.

✅ Core Responsibility:
    - Orchestrates EEG file selection, loading, preprocessing, and UI integration.

🟨 Steps & Interactions:
1. open() → Workflow coordinator
2. _select_file(): opens QFileDialog for .edf
3. _reset_visualizer(): calls reset_to_initial_eeg_state()
4. _load_eeg_data()
    a. _load_raw_file(): MNE raw file loading
    b. load_and_preprocess_eeg(): preprocess, montage
    c. _update_visualizer_state(): sets .current_raw/.sfreq/.channel_names
    d. _extract_and_store_final_data(): extracts numpy data, sets .data/.times/.total_duration
    e. _notify_components(): emits eeg_loaded_signal, calls mcrvlt_snapshot_map
5. _build_dataframe(): builds labeled pandas DataFrame
6. _update_ui_context(): updates UI via update_ui_state_based_on_context()
7. _update_timeline(): updates timeline widget
8. _finalize_plot(): calls update_plot_view(); sets QTimer for focus
9. _switch_to_eeg_tab(): activates EEG Traces tab
10. Error path: _handle_loading_error(): QMessageBox; hide timeline

🔁 Module Flux Table:

| Module / Method                                      | Role                         | Inbound | Outbound |
|------------------------------------------------------|------------------------------|---------|----------|
| mne.io.read_raw_*                                   | Load EEG formats             | ✔️       |          |
| load_and_preprocess_eeg()                           | Filters & preprocessing      | ✔️       | ✔️        |
| reset_to_initial_eeg_state()                        | Visualizer reset             | ✔️       |          |
| full_ordered_channels                               | Ordered channel reference    | ✔️       |          |
| EegVisualizerHeader(raw).print_all_header_info()    | Logs raw metadata            | ✔️       | 🖨️ Log    |
| update_ui_state_based_on_context()                  | Sync UI state                | ✔️       | 🖼️ UI     |
| mcrvlt_snapshot_map.on_eeg_loaded()                       | Trigger amplitude UI update  | ✔️       |          |
| QTimer.singleShot(...)                              | Delayed canvas focus         | ✔️       |          |
| QMessageBox()                                       | Display error message        | ✔️       | 🖼️ Dialog |

📊 ASCII Pipeline:

[Start: open()]
      |
      V
+----------------------+             +------------------------+
| _select_file()       |--[.edf]--> | _load_raw_file()       |
| QFileDialog          |            | mne.io.read_raw_*()    |
+----------------------+             +------------------------+
      |                                          |
      V                                          V
+------------------------+        +-------------------------------+
| _reset_visualizer()    |        | load_and_preprocess_eeg()     |
| reset_to_initial_*     |        | filters, montages, reorder    |
+------------------------+        +-------------------------------+
      |                                          |
      V                                          V
+----------------------------+     +-----------------------------+
| _update_visualizer_state() | --> | _extract_and_store_data()   |
| Set .raw, .sfreq, .names   |     | → .data, .times, .duration  |
+----------------------------+     +-----------------------------+
              |
              V
+----------------------------+
| _notify_components()       | --→ eeg_loaded_signal.emit(), mcrvlt_snapshot_map()
+----------------------------+
              |
              V
+----------------------------+
| _build_dataframe()         | → pandas DataFrame with attributes
+----------------------------+
              |
              V
+----------------------------+
| _update_ui_context()       | → updates UI labels/views
+----------------------------+
              |
              V
+----------------------------+
| _update_timeline()         | → set timeline duration & window
+----------------------------+
              |
              V
+----------------------------+
| _finalize_plot()           | → update_plot_view(), focus canvas
+----------------------------+
              |
              V
+----------------------------+
| _switch_to_eeg_tab()       | → activates EEG Traces tab in UI
+----------------------------+

If ❌ Error at any step:
 → _handle_loading_error() → QMessageBox, hide Timeline

🔧 Extension Notes:
- This doc string can aid future devs or AIs to modify or hook into the EEG loading pipeline.
- Use this helper module for reference or code reviews.

"""
# End of help_eeg_visualizer_loader_logic.py
"""
#### - INTERACTION modules:
KandaModules/eeg_visualizer_loader_logic.py AND
k02_eeg_input/eeg_visualizer_raw_preprocessor.py - ####

Module `eeg_visualizer_loader_logic.py` houses class `EegVisualizerLoaderLogic`, the entry-point that ties GUI events to data ingestion in the visualizer
When the user clicks “Load EEG”, `EegVisualizerLoaderLogic.open()` executes, hiding the splash screen, invoking a Qt file dialog, and falling back to a default EDF path if nothing is chosen
`open()` then calls `_reset_visualizer`, which invokes `reset_to_initial_eeg_state` to clear any pre-existing traces, timers, or widgets so that the application is in a pristine state

Next `_load_eeg_data` is called; here the loader delegates the heavy lifting to `load_and_preprocess_eeg` found in `eeg_visualizer_raw_preprocessor.py`
`load_and_preprocess_eeg` uses MNE to read the EDF, normalises and renames messy sensor labels via `get_rename_mapping`, filters out non-EEG or bad channels, enforces a canonical 10-20 ordering (`full_ordered_channels`), attaches the standard\_1020 montage, and saves an intermediate \*.fif snapshot; the function returns the cleaned `Raw` object, the final ordered channel list, and the sampling rate
`_load_eeg_data` stores these outputs inside the visualiser (`self.visualizer.raw_referential`, `.data`, `.sfreq`, `.times`, `.total_duration`, `.channel_names`) and emits `eeg_loaded_signal`, enabling downstream widgets to subscribe to readiness

Control returns to `open()` which proceeds through `_build_dataframe` (converts the NumPy data matrix into a pandas DataFrame for tabular views), `_update_ui_context` (enables or disables buttons, updates labels, synchronises tab state), `_update_timeline` (feeds total duration and current view window into the interactive TimelineBar and reveals it), `_finalize_plot` (calls `update_plot_view` so that the Matplotlib or PyQtGraph canvas renders the first frame and schedules `force_canvas_focus` after 100 ms to ensure keyboard shortcuts work), and finally `_switch_to_eeg_tab` (raises the “EEG Traces” tab in the notebook so the user immediately sees the signal)

Throughout these steps the loader performs memory-leak snapshots if a `memory_monitor` is attached, and every critical action logs a debug line for traceability
If any exception arises—file corruption, no valid channels, missing sampling frequency—`_handle_loading_error` catches it, hides the TimelineBar, and shows a modal `QMessageBox` with details

Thus the logic flux is
GUI click → `EegVisualizerLoaderLogic.open()` → splash hide → file path selection → visualiser reset → `load_and_preprocess_eeg` pipeline → visualiser attributes populated → DataFrame creation → UI state refresh → timeline synchronisation → first plot render → tab activation
This tight coupling means `eeg_visualizer_raw_preprocessor.py` is purely a data-cleaning utility with no UI knowledge, while `eeg_visualizer_loader_logic.py` orchestrates user workflow, lifecycle management, and visual feedback, ensuring a clean separation between preprocessing logic and interface control


┌─────────────────────────────  GUI EVENT  ──────────────────────────────┐
│           User clicks “Load EEG / Open File” button in UI             │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │ Qt signal
                                  ▼
┌─────────────────────────── EegVisualizerLoaderLogic.open() ───────────────────────┐
│ 1) _hide_splash_screen()       ──┐                                     │
│ 2) _select_file()                 │  ⟶  QFileDialog (or default path)  │
│ 3) _reset_visualizer()            │  ⟶  reset_to_initial_eeg_state()   │
│ 4) _load_eeg_data(file_path)  ────┴─┐                                  │
│                                    │                                  │
│   ┌────────── load_and_preprocess_eeg()  (eeg_visualizer_raw_preprocessor) ┐
│   │  [a] mne.io.read_raw_edf()                                             │
│   │  [b] get_rename_mapping() ─┐                                           │
│   │  [c] normalize_sensor_names() │ String aliases & canonical map         │
│   │  [d] Filter bad / non-EEG ch. │ NaN / zero data                        │
│   │  [e] Sort by 10-20 order       │                                         │
│   │  [f] raw.set_montage()         │ Adds 3-D positions                    │
│   │  [g] raw.save(...fif)          │ Optional snapshot                     │
│   │  [h] Integrity checks & pop-ups                                        │
│   └───────────────┬───────────────────────────────────────────────────────┘
│                   │ returns: Raw, channel_list, sfreq                     │
│                   ▼                                                       │
│   Set visualizer attributes .raw / .data / .times / .sfreq / .total_duration│
│   Emit visualizer.eeg_loaded_signal()                                     │
│   (optional) memory_monitor.capture_snapshot("pre_load")                  │
│                                                                        │
│ 5) _build_dataframe()               → visualizer.build_dataframe_from_data│
│ 6) _update_ui_context()             → ui_state_controller.update_state    │
│                                      ↳ Enable buttons / tabs, update labels│
│ 7) _update_timeline()               → timeline_widget.manager.update()    │
│                                      ↳ set_duration() & emit window_moved │
│ 8) _finalize_plot()                 → visualizer.update_plot_view()       │
│                                      ↳ QTimer(100 ms) force_canvas_focus  │
│ 9) _switch_to_eeg_tab()             → notebook.setCurrentIndex("EEG Traces")│
│10) print “[✅] EEG loading complete.”                                     │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │
                     ┌────────────▼─────────────┐
                     │  EEG fully displayed:    │
                     │  • Traces painted        │
                     │  • Timeline visible      │
                     │  • Widgets active        │
                     └──────────────────────────┘
                                  │
                ┌─────────────────┴──────────────────┐
                │          Error branch              │
                │  (any Exception inside try-block)  │
                └───────▼────────────────────────────┘
                  _handle_loading_error(e)
                  ├─ Hide TimelineBar (if shown)
                  ├─ QMessageBox(Critical) with details
                  └─ Log “[CRITICAL ERROR] …”

Legend
──────
□  Solid boxes  = functions/methods
→  Arrow        = call/return or signal/slot
┬/┴/├/┤/┘       = flow connectors


High-level logic

    UI trigger starts EegVisualizerLoaderLogic.open()

    Splash hide → file selection → visualiser reset

    Data pipeline (load_and_preprocess_eeg) normalises, cleans, orders, montages, and returns a ready Raw object

    Visualizer fields are populated, signalling that data are ready

    UI widgets (DataFrame, buttons, timeline, canvas) are refreshed in sequence

    Plot appears & tab is focused; any exception diverts to _handle_loading_error

This ASCII diagram captures every major call and the data/control flux between the file-loader logic and
 the preprocessing module, from user click to rendered EEG traces
(or graceful error dialog).




#### - RECRIATING REFERENTIAL FROM BIPOLAR - ###
Run code to list all channel names.

Detect if auricular references (A1, A2) or others exist.

Examine metadata to see if a reference is specified.

Summarize everything clearly in a report.

Load it using MNE.

Extract and list all channel names (e.g., Fp1, F7, etc.).

Detect any reference channels (like A1/A2 for auricular references).

Share a clear summary of the channel layout and reference configuration.

Load the file using MNE.

List all EEG channel names (e.g. Fp1, F7, etc.).

Identify any reference channels (like auricular A1/A2 or others).

Provide a clear summary of your setup and reference scheme.
Load the file using MNE

List all EEG channels (e.g., Fp1, F7, etc.)

Highlight any reference channels (like A1/A2 or mastoid references)

Provide details on the reference scheme in use

MNE loading result
File successfully read as raw EDF; 20 channels detected, all typed as EEG.

Channel list (shown in the table above)
EEG FP1-R_Fp1-F7
EEG F7-R_F7-T3[F
EEG T3-R_T3-T5[T
EEG T5-R_T5-O1[T
EEG 19-R_Fp1-F3[
EEG F3-R_F3-C3[F
EEG C3-R_C3-P3[C
EEG P3-R_P3-O1[P
EEG FZ-R_Fz-Cz[F
EEG CZ-R_Cz-Pz[C
EEG FP2-R_Fp2-F8
EEG F8-R_F8-T4[F
EEG T4-R_T4-T6[T
EEG T6-R_T6-O2[T
EEG 20-R_Fp2-F4[
EEG F4-R_F4-C4[F
EEG C4-R_C4-P4[C
EEG P4-R_P4-O2[P
EEG 3-R_EKG[3]
EEG 21-R_PHOTIC[


Reference detection
No dedicated reference-only channels (A1, A2, M1, M2, or “REF”) were found.
All 18 scalp-EEG traces are labelled as bipolar derivations (each name contains “Fp1-F7”, “F7-T3”, etc.), indicating the data were recorded or re-exported in a bipolar montage. In such files each signal is already the difference between two scalp electrodes; a separate reference electrode is therefore not present in the file header.

Reference scheme summary
Layout: classic 10-20 pairs, anterior-to-posterior and left-to-right chains (e.g. Fp1-F7-T3-T5-O1; Fp2-F8-T4-T6-O2; midline Fz-Cz-Pz).
Auxiliary channels: one ECG lead (“EEG 3-R_EKG[3]”) and one photic-stim trigger (“EEG 21-R_PHOTIC[”).
Recording reference: implicit—each channel already stores a voltage difference between two scalp sites; no mastoid or common reference saved. Any re-referencing (average, linked-ears, REST, etc.) would have to be performed offline.

In short: the file uses a fully bipolar montage with no standalone auricular or mastoid reference channels.


yes, very helpful. Using information in file is that possible recriate or simulate reference A1, A2 or AA to recriate referential channels?



Below is what you can—and cannot—do with a purely bipolar export such as the one in ben_p_s_v2.edf.

────────────────────────────────────────────────────────────────────────
1 Information that is lost forever
────────────────────────────────────────────────────────────────────────
• The file contains only voltage differences (Fp1 – F7, F7 – T3, …).
• Absolute potentials of each electrode with respect to the true recording reference (A1, A2, Cz-ref, ground, etc.) were never stored.
• Therefore the genuine “Fp1 vs A1”, “F7 vs A1”, … signals are irretrievable; the ear-electrode trace itself was not sampled, so there is nothing to subtract.

In other words, you cannot reconstruct the exact “referential” channels that would have existed during acquisition.

────────────────────────────────────────────────────────────────────────
2 What is mathematically recoverable
────────────────────────────────────────────────────────────────────────
Because the bipolar chain forms a connected graph, you can solve for one consistent set of scalp potentials up to an arbitrary constant. A simple way is to:

 a Create an incidence (edge-node) matrix B where each row is a bipolar pair (e.g. Fp1 – F7 = +1 · Fp1 – 1 · F7).
 b Solve B v = g by least squares with one constraint such as “v(Cz)=0” or “Σ v = 0”.
 c You now have estimated voltages v(electrode) relative to the chosen anchor.

That gives you single-ended signals that are consistent with every bipolar trace, but the common offset is arbitrary.

────────────────────────────────────────────────────────────────────────
3 How to create a new reference in practice
────────────────────────────────────────────────────────────────────────
You can pick any surrogate reference channel (average, Cz, virtual mastoids, REST, etc.) and re-reference inside MNE:

import mne, numpy as np
raw = mne.io.read_raw_edf("ben_p_s_v2.edf", preload=True)

# Step 1 – convert the whole set to a temporary average reference
# (works even for bipolar labels)
raw.set_eeg_reference('average', projection=False)

# Step 2 – create two virtual “mastoids” as the mean of the T5 and T6 voltages
mastoid_left  = raw.copy().pick('T5')[0]      # get data array
mastoid_right = raw.copy().pick('T6')[0]

raw.add_reference_channels(ch_name=['A1','A2'],
                           ref_data=np.vstack([mastoid_left,
                                               mastoid_right]))
raw.set_eeg_reference(ref_channels=['A1','A2'])   # linked-ears

Key points:

• set_eeg_reference('average') first converts bipolar traces into pseudo-monopolar voltages using the inversion method mentioned above (MNE does it internally).
• add_reference_channels inserts synthetic channels (here an average of T5/T6 as a proxy for real mastoids).
• set_eeg_reference(...) rereferences everything to those proxies.

Feel free to substitute any other strategy (e.g. use only T5 as A1, Laplacian CSD, common-average, etc.).

────────────────────────────────────────────────────────────────────────
4 Limitations you must accept
────────────────────────────────────────────────────────────────────────
• All reconstructed signals share an unknown constant offset versus the real A1/A2 potentials recorded in the lab; spectral content and morphology are preserved, but absolute DC values are meaningless.
• Because the auricular electrodes were not actually measured, artefacts unique to A1/A2 (e.g. cable noise, high impedance) cannot be reproduced—your “virtual” ears are mathematically clean.
• Clinical rules that rely on true ear references (classic spike localisation, amplitude criteria) should be interpreted cautiously; always document that a reconstructed reference was used.

────────────────────────────────────────────────────────────────────────
Take-home summary
────────────────────────────────────────────────────────────────────────
You cannot get the original “Fp1 vs A1” traces back, but you can:

    Invert the bipolar montage to obtain monopolar voltages relative to an arbitrary baseline.

    Create synthetic A1/A2 (or any other) channels from existing electrodes.

    Rereference the entire data set to those channels inside MNE.

This yields a practical linked-ears or average-ears montage that behaves like a referential recording for further analysis, while acknowledging the small loss of authenticity inherent to any reconstruction.


"""

