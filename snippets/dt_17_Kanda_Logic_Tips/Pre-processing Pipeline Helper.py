"""
===========================================================================
Kanda EEG – Pre-processing Pipeline Helper
===========================================================================

This companion module **does not execute any signal processing**.
Instead, it documents – in one place – *exactly* what happens inside
`k02_eeg_input/eeg_visualizer_raw_preprocessor.py`, so new contributors
can grasp the flow without digging through the full code.

---------------------------------------------------------------------------
1. High-level purpose
---------------------------------------------------------------------------
* Accept an `mne.io.Raw` read from an EDF (or BrainVision, etc.).
* Sanitize channel names, drop unusable channels, apply the 10-20 montage,
  generate a bipolar (“double-banana”) version, and hand both back to the
  GUI loader.

---------------------------------------------------------------------------
2. Inputs  →  Where they come from
---------------------------------------------------------------------------
Variable | Source (caller)                             | Type
---------|---------------------------------------------|--------------------
`raw`    | `EegVisualizerLoaderLogic._load_eeg_data`   | `mne.io.BaseRaw`
`file_path` | same caller                             | `str`, full path
`full_ordered_channels` | constant (this package)     | `list[str]`
Qt **QApplication** | lazily created *only* if a warning pop-up is needed.

---------------------------------------------------------------------------
3. Outputs  →  Where they go
---------------------------------------------------------------------------
Object(s) returned to **Loader**:
    raw_ref        → visualizer.current_raw (referential)
    raw_bipolar    → visualizer.raw_bipolar
    final_chs      → visualizer.channel_names
    sfreq          → visualizer.sfreq
    ref_name       → visualizer.reference_display_name

Side-effects:
    • Warning pop-ups (`PySide6.QMessageBox`) for bad channels.
    • Log lines via `logging`.
    • Optional *.fif* copy written next to the EDF for fast reload.

---------------------------------------------------------------------------
4. Detailed step-by-step logic
---------------------------------------------------------------------------
A  `summarize_raw_metadata`       – Console dump: sfreq, filters, channels.
B  `detect_reference_scheme`      – Tries CAR, REST, A1/A2, CSD, etc.
C  (inline) integrity scan        – Lists duplicates / unknown / missing chs.
D  `fix_and_deduplicate_channels` – Normalise labels (T7→T3) and make
                                   duplicates unique (`T3-0`, `T3-1` …).
E  `get_rename_mapping` + `normalize_sensor_names`
                                   – Fuzzy map remaining weird labels onto
                                     canonical 10-20 names.
F  `clean_valid_eeg_channels`     – Drop all-zero/NaN signals; reorder by
                                   `full_ordered_channels`.
G  `finalize_and_save_montage`    – Attach MNE “standard_1020” montage,
                                   optionally save *_converted_raw.fif*.
H  `generate_bipolar_version`     – Uses `BipolarMontageBuilder` to create
                                   double-banana channels.
I  Return tuple                   – (`raw_ref`, `raw_bipolar`, `final_chs`,
                                   `sfreq`, `ref_name`).

---------------------------------------------------------------------------
5. ASCII pipeline
---------------------------------------------------------------------------

    raw  +  file_path
          │
          ▼
    ┌──────────────────┐  A  header printout
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  B  detect reference
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  C  integrity scan
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  D  fix & de-dup
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  E  fuzzy rename
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  F  prune / reorder
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  G  montage + save
    └──────────────────┘
          │
          ▼
    ┌──────────────────┐  H  bipolar build
    └──────────────────┘
          │
          ▼
    (raw_ref, raw_bipolar, final_chs, sfreq, ref_name)  →  GUI loader


---------------------------------------------------------------------------
6. Reading this help from Python
---------------------------------------------------------------------------
>>> import eeg_preprocessor_help as h
>>> help(h)
(or simply open the file in your editor)

---------------------------------------------------------------------------
Authorship & License
---------------------------------------------------------------------------
© Paulo A. M. Kanda, Rafael G. Kanda, Felipe G. Kanda
Released under **CC BY-ND 4.0** for academic / non-commercial use.




"""
                 ┌─────────────────────────────────────────────────────┐
                 │ raw (MNE Raw)  +  file_path (str, *.edf)            │
                 └───────────────┬─────────────────────────────────────┘
                                 │  load_and_preprocess_eeg
                                 ▼
┌──────────────────┐   A   ┌──────────────────────┐
│ Summarise header │──────►│  console printout    │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   B   ┌──────────────────────┐
│ Detect reference │──────►│  ref_name (str)      │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   C   ┌──────────────────────┐
│ Integrity scan   │──────►│  log + optional GUI  │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   D   ┌──────────────────────┐
│ Fix & dedup chs  │──────►│  raw (renamed)       │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   E   ┌──────────────────────┐
│ Fuzzy rename map │──────►│  raw (renamed)       │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   F   ┌──────────────────────┐
│ Prune + reorder  │──────►│  final_chs (list)    │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   G   ┌──────────────────────┐
│ Apply montage    │──────►│  raw_ref            │
│ Save *.fif       │       │  (optionally file)   │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
┌──────────────────┐   H   ┌──────────────────────┐
│ Build bipolar    │──────►│  raw_bipolar/None    │
└──────────────────┘       └──────────────────────┘
                                 │
                                 ▼
                 ┌───────────────┴────────────────────────┐
                 │ RETURN: (raw_ref, raw_bipolar,         │
                 │          final_chs, sfreq, ref_name)    │
                 └─────────────────────────────────────────┘

