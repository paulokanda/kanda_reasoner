"""
| Feature                 | `raw.plot_sensors()` | Custom Diagnostic GUI |
| ----------------------- | -------------------- | --------------------- |
| Visual layout           | ✅ Yes                | ✅ Yes                 |
| Editable labels         | ❌ No                 | ✅ Yes (via UI logic)  |
| Auto suggestions        | ❌ No                 | ✅ Yes (we provide)    |
| Integration into loader | ❌ Manual only        | ✅ Seamless option     |


Detects montage issues

Lets user fix names interactively

Re-renders updated sensor map


🎯 GOAL

Create a diagnostic + corrective GUI that:

    Validates montage and channel names after file load

    Lets clinicians manually correct bad labels

    Updates EEG object + saves to .fif

    Prevents accidental corruption via undo/cancel

    Integrates into existing Qt GUI flow


🔄 WORKFLOW
🧠 Step 1: Auto-trigger if EEG has channel problems

    On _load_eeg_data(), we check for:

        Unknown channel names

        Duplicates (e.g. Fp1, Fp1)

        Missing standard channels (from full_ordered_channels)

    If issues detected → GUI pops up automatically

    If clean → user can open it manually from a menu

🧩 Step 2: GUI Features

| Feature                     | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| ✅ **Channel Table**         | Shows original + editable channel names                        |
| 🔍 **Problem Highlighting** | Color rows with problems (e.g., red for unknowns)              |
| ✏️ **Editable Fields**      | User can type or select correct label                          |
| 🔄 **Auto-suggest Fixes**   | Optional button to auto-fill standard names                    |
| 💾 **Save to .fif**         | Saves fixed EEG file with corrected montage                    |
| 🕘 **Undo**                 | Revert changes made during current session                     |
| ❌ **Cancel**                | Close GUI, discard edits                                       |
| 🚪 **Close**                | Close window, keep edits if applied                            |
| 📊 **Live Preview**         | Show updated `raw.plot_sensors(show_names=True)` after changes |


🛡️ Safety Design

    On open, EEG state is deep-copied

    Undo → reloads the copy

    Save → updates both raw and writes a _corrected_raw.fif file

    No changes apply unless saved


✨ Suggested Extra Features

    Dropdown Suggestions:

        Autocomplete box for each editable field from standard list

    Mismatch Counter:

        Status bar: 3 unknown labels, 2 duplicates

    Reference Scheme Selector:

        Optionally show + let user adjust referencing (CAR, A1/A2...)

    Log Corrections:

        Keep a .log or .json file per file listing changes made

    Auto-Accept Mode:

        Headless version (for batch) that applies corrections automatically


| Feature Idea                                       | Benefit                                 |
| -------------------------------------------------- | --------------------------------------- |
| Montage template selector                          | Handle neonatal, epilepsy, ICU variants |
| Sync with electrode caps (via photos or templates) | For accuracy                            |
| Upload to patient record                           | Seamless clinical archiving             |


Let’s break this into modular, testable, and PyQt6/PySide6-friendly steps with 💡smart sequencing. Here's a step-by-step master plan for implementing the MontageDiagnosticEditor GUI and its integration.

 Folder Structure
Kanda_Montage_Diag_Editor_03/
├── __init__.py
└── montage_diag_editor_03_2.py  ← will contain MontageDiagnosticEditor


📋 Implementation Plan: Step-by-Step
✅ Phase 1: Setup & Wiring

    [1] Create folder & module

        Create Kanda_Montage_Diag_Editor_03/

        Add montage_diag_editor_03_2.py

        Add class MontageDiagnosticEditor(QWidget)

    [2] Wire GUI into EEGVisualizerCore (top toolbar menu)

        Add menu item under Tools in top menubar

        Label: "🧠 Run Montage Diagnostic"

        Connect click to open_montage_diagnostic_gui()

    [3] Freeze Main GUI while open

        Use .setEnabled(False) on main window during GUI open

        Restore .setEnabled(True) on close or cancel

🧪 Phase 2: Diagnostic Core

    [4] Implement minimal GUI layout

        QTableView for channels (original name + editable field)

        Buttons: Save, Undo, Cancel, Auto-Fix

        Show mismatch count

    [5] Load EEG channels into table

        Populate from visualizer.raw_referential.ch_names

    [6] Highlight invalid/missing channels

        Compare to full_ordered_channels

        Color cells red for unknowns or duplicates

    [7] Editable column with suggestions

        Use QComboBox delegates or QLineEdit with validation

        Autocomplete from full_ordered_channels

💾 Phase 3: Apply & Save

    [8] Apply changes to raw

        Rename channels using raw.rename_channels()

        Check for integrity after update

    [9] Save corrected .fif file

        Write _corrected_raw.fif

        Also allow overwriting .fif if confirmed

    [10] Emit signal to refresh main app

        e.g., montage_updated_signal → reconnect downstream UI

🧪 Phase 4: PyTests

    [11] Pytest: GUI opens correctly

        Test presence of fields, labels, buttons

    [12] Pytest: Apply + Save logic

        Load mock raw → fix channel → save → re-check channels

    [13] Pytest: Auto-fix suggestions

        Validate that ‘T7’ maps to ‘T3’, ‘p8’ to ‘T6’ etc

🚀 Phase 5: Polishing

    [14] Status bar or label: 3 invalid channels

    [15] Log corrections to .log or .json

    [16] Button to visualize raw.plot_sensors()

    [17] Optionally: Reference Selector UI

🧩 Summary Timeline

| Step  | Task                         | ETA           |
| ----- | ---------------------------- | ------------- |
| 1-3   | Folder + Menu bar hookup     | ✅ today       |
| 4-7   | Table logic & interactivity  | ✅ soon        |
| 8-10  | Channel application + saving | ✅ soon        |
| 11-13 | PyTests                      | ⏳ in parallel |
| 14-17 | Extra UX polish              | 👌 optional   |


Here’s a step-by-step development blueprint of your Montage Diagnostic GUI with fine-grained task sequencing — at the level of: "now create window", "now create save button" etc. It’s divided by workflow sections, with suggested checkpoints and test milestones. This gives you full control 🔬
🔄 WORKFLOW DEFINITION: Full Breakdown


🧠 STEP 1: Trigger + Diagnostics (Auto or Manual)
🧩 [1.1] Add Auto-check on EEG Load

    ⏲️ Where: EegVisualizerLoaderLogic._load_eeg_data()

    🧪 Check:

        Unknown channels → not in full_ordered_channels

        Duplicates → use collections.Counter

        Missing core channels → check missing from full_ordered_channels

    ✅ If issues found:

        call: self._open_montage_diagnostic_gui(auto=True)

    🚫 If clean:

        user can manually open later from menu

🧩 [1.2] Add "🧠 Run Montage Diagnostic" to Tools menu

    ⏲️ Where: in EEG main window UI code (QMainWindow)

    Action: opens GUI manually

    Use: self._open_montage_diagnostic_gui(auto=False)

🪟 STEP 2: GUI Scaffold
🧩 [2.1] Now: Create MontageDiagnosticEditor(QWidget)

    📂 File:Kanda_Montage_Diag_Editor_03/montage_diag_editor_03_2.py

    Fields:

        original_channels, editable_model, visualizer, raw_copy

    🧪 PyTest: Can instantiate and display

🧩 [2.2] Create Main Layout

    QVBoxLayout or QGridLayout

    Add: title label + channel table

    Block other GUI (disable main app during open)

🗂️ STEP 3: Channel Table & Editing
🧩 [3.1] Create QTableWidget

    Columns: [Original] [Edited] [Status]

    Rows: from visualizer.raw.ch_names

    Store editable values in model

🧩 [3.2] Highlight Problems

    Color cell background:

        🔴 Red = unknown

        🟠 Orange = duplicate

        ⚠️ Add "Missing Channels" row for reference

    Use helper: analyze_montage_issues()

🧩 [3.3] Add Editing Logic

    Use QLineEdit or QComboBox per row

    Autocomplete suggestions from full_ordered_channels

    🧪 PyTest: update cell and reflect in model

💾 STEP 4: Actions and Workflow Buttons
🧩 [4.1] Add "Auto-Fix" Button

    Suggest canonical names from normalize_sensor_names()

    Update edited field if match found

    🧪 PyTest: auto-fix works on known messy labels

🧩 [4.2] Add "Save" Button

    Apply changes to raw:

        call raw.rename_channels(mapping)

    Save to: *_corrected_raw.fif

    Emit signal to refresh main app

    🧪 PyTest: load mock raw → rename → save → reload

🧩 [4.3] Add "Undo" Button

    Restore from deep copy (copy.deepcopy(raw))

    Re-populate table

🧩 [4.4] Add "Cancel" + "Close" Buttons

    Cancel: discard edits, close window

    Close: retain edits (if applied), close window

    App is unblocked (main_window.setEnabled(True))

🧪 STEP 5: Diagnostics + Extras
🧩 [5.1] Add Live Preview Button

    Calls raw.plot_sensors(show_names=True)

    Optional on layout (debug/audit only)

🧩 [5.2] Add Status Bar

    "3 unknown labels, 2 duplicates"

    Update on edits

🧩 [5.3] Optional: Reference Selector

    Show detected scheme (CAR, A1, etc)

    Allow change via dropdown + reproject

🧩 [5.4] Log Corrections

    Save .json or .log listing:

    {"Fp1_1": "Fp1", "T7": "T3", ...}

🧠 BONUS: Future Ideas
🧩 [6.1] Batch CLI Auto-Fixer

    Use headless version of GUI logic

    CLI tool to apply and save to _corrected_raw.fif if invalid montage

🧩 [6.2] Template Selector

    Allow switching to ICU, pediatric, neonatal layouts

🧩 [6.3] Patient Record Export

    Upload corrected montage into EMR or hospital file

✅ DEVELOPMENT SEQUENCE

| Phase | Component                    | Task ID    | Status   |
| ----- | ---------------------------- | ---------- | -------- |
| 1     | Trigger on load              | \[1.1]     | 🚧       |
| 1     | Menu action for manual run   | \[1.2]     | 🚧       |
| 2     | Editor class scaffold        | \[2.1]     | 🟢 Ready |
| 2     | GUI layout + freeze main app | \[2.2]     | 🔜       |
| 3     | Table creation and mapping   | \[3.1-3.3] | 🔜       |
| 4     | Button bar: save/undo/cancel | \[4.1–4.4] | 🔜       |
| 5     | Status + live view + logging | \[5.1–5.4] | 🔜       |


             ╭────────────────────────────────────────────────╮
             │        EEG File is Loaded (_load_eeg_data)     │
             ╰────────────────────────────────────────────────╯
                            │
                            ▼
       ┌────────────────────────────────────────────┐
       │ Analyze Channels for:                      │
       │  • Unknown names                           │
       │  • Duplicates                              │
       │  • Missing from full_ordered_channels      │
       └────────────────────────────────────────────┘
              │                         │
              │ if issues found         │
              ▼                         ▼
     ┌──────────────────────┐   ┌─────────────────────────┐
     │ Auto-launch GUI [1.1]│   │ Do nothing (clean)      │
     └──────────────────────┘   └─────────────────────────┘
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│     [2.1] Launch GUI: MontageDiagnosticEditor              │
│     └── Block Main App (disable EEG UI)                   │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [2.2] Create Main Layout (title + table + button bar)     │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [3.1] Create QTableWidget:                                 │
│   Original | Editable | Status (color)                    │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [3.2] Color-code issues:                                   │
│   🔴 Unknown   🟠 Duplicates   ⚠️ Missing Rows              │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [3.3] Make editable: Autocomplete using standard channels  │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [4.1] Auto-Fix button → normalize and rename suggestions   │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [4.2] Save → apply renaming, write _corrected_raw.fif      │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [4.3] Undo → reload deep-copied original raw               │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [4.4] Cancel / Close → discard or keep edits               │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [5.1] Live Preview → raw.plot_sensors(show_names=True)     │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [5.2] Status bar: “2 unknowns, 1 duplicate”                │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [5.3] Reference Scheme Dropdown (optional)                 │
╰────────────────────────────────────────────────────────────╯
              │
              ▼
╭────────────────────────────────────────────────────────────╮
│ [5.4] Save change log as JSON (.log or .json)              │
╰────────────────────────────────────────────────────────────╯


Here's a numbered step-by-step checklist of the full Montage Diagnostic GUI pipeline,
 broken down for implementation and testing 🧪📋:

🔢 STEP-BY-STEP CHECKLIST
[1] EEG LOADING + CHANNEL CHECKS

1.1 In _load_eeg_data(), add a check for:

    Unknown channels (not in standard list)

    Duplicate channels

    Missing channels from full_ordered_channels

1.2 If any of the above are true → trigger GUI:

self._launch_montage_diagnostic_gui()

1.3 Else → user can access it manually from Tools menu:

    Add a menu item 🛠 Montage Diagnostic under top bar → Tools

[2] GUI INIT: MontageDiagnosticEditor Window

2.1 Create new folder:Kanda_Montage_Diag_Editor_03/
2.2 New file: montage_diag_editor_03_2.py
2.3 Define class MontageDiagnosticEditor(QDialog)
2.4 Setup window with:

    Title: Montage Diagnostic & Correction

    Modal (freezes rest of app)

    Fixed size


[3] GUI TABLE UI

3.1 Add QTableWidget (3 columns):

    Original Name

    Editable Name (QLineEdit or ComboBox with autocomplete)

    Status (label + background color)

3.2 Detect and color code rows:

    🔴 Red for unknown names

    🟠 Orange for duplicates

    ⚠️ Yellow for missing expected channels (shown as disabled rows)


3.3 Add tooltip/status per row:

    "Not in 10-20 system"

    "Duplicated label"

[4] USER ACTIONS

4.1 Auto-Fix Button:

    Suggests fixes using normalize_sensor_names()

4.2 Save Button:

    Applies renaming to current raw

    Saves _corrected_raw.fif

    Updates visualizer state

4.3 Undo Button:

    Reverts changes using deep-copied original raw

4.4 Cancel Button:

    Discards edits

    Closes GUI (restores original)

4.5 Close Button:

    Accepts current GUI state (if valid)

    Keeps edits but does not save

[5] ADVANCED UI EXTRAS

5.1 Live Preview Button:

    Calls raw.plot_sensors(show_names=True) on current edits

5.2 Status Bar / Label:

    Shows count: “3 unknown, 2 duplicate”

5.3 Reference Selector (Optional):

    Dropdown for CAR, A1/A2, REST

5.4 Log Save (Optional):

    Save renaming actions to JSON .log file beside EDF

[6] TESTING

6.1 Unit test for:

    Unknown labels

    Missing channels

    Correct renaming

    Duplicate correction

6.2 GUI test (Pytest-qt or manual trigger):

    Open GUI on bad file

    User edits

    Save and verify changes applied to .fif


┌────────────────────────────────────────────────────────────────────┐
│                   🧠 Montage Diagnostic GUI Flow                  │
└────────────────────────────────────────────────────────────────────┘

  █ STEP 1 – Channel Validation in Load
  1.1 ─ After loading EEG in _load_eeg_data(),
        check:
        • unknown channels (not in standard list)
        • duplicate channels
        • missing standard channels
  1.2 ─ If any issues found → auto‑launch GUI via _launch_montage_diagnostic_gui()
  1.3 ─ Else → user can open GUI manually from Tools menu

  ↓

  █ STEP 2 – Tools Menu Integration
  2.1 ─ Add “🛠 Montage Diagnostic” menu item to top nav bar (right of app title)
  2.2 ─ Connect menu action to _launch_montage_diagnostic_gui()

  ↓

  █ STEP 3 – GUI Window Init
  3.1 ─ Folder:Kanda_Montage_Diag_Editor_03/
  3.2 ─ File:montage_diag_editor_03_2.py
  3.3 ─ Class:MontageDiagnosticEditor(QDialog)
  3.4 ─ Setup window:
        • Title: “Montage Diagnostic & Correction”
        • Modal (blocks main app)
        • Fixed size/layout container

  ↓

  █ STEP 4 – Populate Channel Table
  4.1 ─ QTableWidget with columns:
        • Original Name | Editable Name | Status
  4.2 ─ Fill rows with current channels:
        • highlight invalids in red/orange/yellow
  4.3 ─ Provide tooltips for issues (duplicates, unknown)

  ↓

  █ STEP 5 – GUI pro_filters
  5.1 ─ Auto‑Fix button (uses normalize_sensor_names())
  5.2 ─ Live Preview button → calls raw.plot_sensors(show_names=True)
  5.3 ─ Save → apply renaming to raw, save _corrected_raw.fif, update visualizer
  5.4 ─ Undo → revert to session‑start copy
  5.5 ─ Cancel → close GUI without saving
  5.6 ─ Close → accept changes and close window

  ↓

  █ STEP 6 – Safety Mechanisms
  6.1 ─ Deep‑copy raw on open to preserve original
  6.2 ─ Any changes only applied if Save clicked
  6.3 ─ Undo reloads from deep‑copy
  6.4 ─ Save writes out both modified raw & corrected .fif

  ↓

  █ STEP 7 – Visual Updates
  7.1 ─ After edits, raw.plot_sensors(sync current montage)
  7.2 ─ Refresh table highlight status
  7.3 ─ If Save → update visualizer.current_raw and refresh main plot

  ↓

  █ STEP 8 – Logging & Batch Support
  8.1 ─ Log corrections (e.g., JSON alongside file)
  8.2 ─ (Optional) Headless “Auto‑Accept” mode for CLI batching

  ↓

  █ STEP 9 – Unit & GUI Testing
  9.1 ─ Unit tests:
        • unknown/duplicate/missing detection
        • auto‑fix suggestions
        • save → correct .fif file
  9.2 ─ GUI tests (pytest‑qt or manual):
        • opens with bad channels
        • editing works
        • Undo reverts
        • Save persists












"""



