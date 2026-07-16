review "Project Q&A" tab logic an  make tab update to read correct data from dinamic drive_where_project_is:\<project_name>_show_project_to_AI folder , instead from inside  kanda_reasoner code
Ran 6 commands, viewed 2 files

Good, "show_project_to_AI" is a real established concept in this codebase. Let me look at index_loader.py — where the JsonProjectIndex reads its files from — since that's the likely place feeding Project Q&A its data.
Viewed 11 files, ran 6 commands

Confirmed the bug precisely. Here's the review, then the fix.
What's actually happening

The "Project Q&A" tab's Create Local-AI Copy / Refresh Local-AI Copy buttons sit directly next to the "Project root:" field in the GUI (ui_builder.py, _build_project_json_group), visually implying they act on whatever project is currently selected there.

But runtime_controller.py::_tool_project_root() ignores that field entirely:
python

def _tool_project_root(self) -> Path:
    """Return the developer_tools root that owns Reasoner assets."""
    return Path(__file__).resolve().parents[3]

This walks up from the kanda_reasoner source file itself and is passed straight into ensure_local_ai_copy() / refresh_local_ai_copy(), which derive <project_drive>:/<project_name>_show_project_to_AI/second_prompt_files/... from whatever root they're given (project_analysis_evidence_paths.py, confirmed correct/mature scheme). So today those two buttons always resolve to kanda_reasoner analyzing itself — matching what _RUN_COLLECTOR_STATUS.txt shows (E:\kanda_reasoner_show_project_to_AI\...) — instead of the actively selected project's dynamic show_project_to_AI folder.

Good news: window.project_root_edit is already one of the shell-synced field names (main_window.py::_project_root_field_names), so it correctly tracks whatever project is active elsewhere in the app. The fix is just to make these two actions use it instead of _tool_project_root().
Identified hardcoded filenames requiring dynamic path resolution updates

The confirm dialog text also names static/generic filenames that don't match the real dynamic naming scheme ({project_name}__complete_local_AI.json). Fixing that too so the prompt reflects the actual behavior:
Ran 5 commands, edited a file, viewed a file

Good — no remaining calls to _tool_project_root() anywhere in the file (it's kept only as a documented fallback, unused for now). Let me produce a diff and package the file.
Ran 2 commands, read a file
What I found and fixed

File: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py

The Create Local-AI Copy / Refresh Local-AI Copy buttons in Project Q&A (right next to the "Project root:" field) called _tool_project_root(), which returns Path(__file__).resolve().parents[3] — the kanda_reasoner tool's own source location — instead of the actively selected project. Since ensure_local_ai_copy()/refresh_local_ai_copy() derive <project_drive>:/<project_name>_show_project_to_AI/... from whatever root they're given, both buttons were always operating on kanda_reasoner analyzing itself, matching what _RUN_COLLECTOR_STATUS.txt shows (E:\kanda_reasoner_show_project_to_AI\...).

Fix: added _active_project_root(window), which reads window.project_root_edit (already shell-synced to whatever project is active app-wide, per main_window_help/window_project_root.py), falls back to the loaded JSON's own recorded project_root if that field is empty, and raises a clear user-facing error if neither is available — rather than silently defaulting to the tool's own folder. Both actions now use it. I also corrected the refresh confirmation dialog, which hardcoded generic filenames (developer_tools__complete_local_AI.json) that don't match the real dynamic per-project naming scheme.

Compiles clean, 258 lines (well under the 500 cap), _tool_project_root() kept only as a documented fallback, no longer called anywhere.
Two more things I found while tracing this — didn't touch, want your call

    analysis_controller.py::build_analysis_command launches python -m kanda_reasoner_app.reasoner_engine_data_collector.collector_main — but that package doesn't exist anywhere in the source tree. The real collector lives at kanda_reasoner_app.reasoner_context_collector.collector_main. As written, clicking Run Analysis would fail with ModuleNotFoundError immediately. This looks like a stale rename that never got propagated (reasoner_engine_data_collector also shows up broken in run_real_project_static_context_smoke.py and run_static_context_test_suite.py).
    AnalysisController.expected_generated_json_path writes project_structure_index.json directly inside the selected project_root itself — not into <project_root>_show_project_to_AI/second_prompt_files/. That's a third location (neither kanda_reasoner's own folder, nor the dynamic show-project-to-AI scheme), which is inconsistent with the mature path scheme in project_analysis_evidence_paths.py that everything else in the app now follows.

Want me to fix #1 (the broken module path — likely a one-line rename, high confidence) and/or investigate #2 further before touching it, since it may be intentional legacy behavior for the collector's own bootstrap step?
Runtime controller
PY 
Runtime controller
DIFF 

nvestigate #2 further before touching it, since it may be intentional legacy behavior for the collector's own bootstrap step?
Deliberated cautious investigation before modifying potentially intentional legacy code

Now I can read the actual collector logic (decoded, not executed) to see what it really does with output paths.
Investigated workflow divergence and verified collector implementation details

This confirms it. Here's what I found.
Investigation result: this is NOT intentional bootstrap behavior — it's a broken duplicate implementation

There is already a correct, mature, fully-working "Run Collector" system elsewhere in the app: kanda_reasoner_app/reasoner_tools_shell/runner_help/. I traced it end to end:

    It resolves output location with analysis_json_complete_dir(project_root) — the same dynamic <project_root>_show_project_to_AI/second_prompt_files/ scheme everything else correctly uses.
    It launches the real collector as a standalone script file (reasoner_tools_shell/runner.py) with positional args: [runner.py, child_mode_flag, project_root, output_json, runtime_trace_json].
    Separately, it calls -m kanda_reasoner_app.reasoner_context_collector.complete_json_web_ai_enrichment --root ... --complete-json ... --compact for enrichment.

Then I decoded (without executing — it's base64-encoded source assembled via exec(compile(...)), so I extracted and decoded the string parts only) the actual run_collector() function inside reasoner_context_collector/collector_main.py. Its real signature is:
python

def run_collector(project_root: str, output_json: str, runtime_trace_json: str | None = None) -> dict:

It's a plain library function that takes an explicit output path from its caller — it has no argparse, no if __name__ == "__main__": block, and doesn't decide its own output location at all.

Compare that to what Project Q&A's "Run Analysis" actually does (analysis_controller.py::build_analysis_command):
python

module_name = 'kanda_reasoner_app.reasoner_engine_data_collector.collector_main'   # doesn't exist
args = ['-m', module_name, '--project-root', project_root]                          # not a valid CLI contract either

So this button is broken on three independent counts, not one legacy-tradeoff:

    Wrong module path (reasoner_engine_data_collector vs. the real reasoner_context_collector).
    Even the real module has no CLI entry point matching -m module --project-root X — it's not invokable as a script at all, so fixing #1 alone still wouldn't work.
    expected_generated_json_path() assumes the output lands at <project_root>/project_structure_index.json, which matches neither the real collector's output-path contract (caller-supplied) nor the dynamic show_project_to_AI scheme the rest of the app (including the working Run Collector window and my earlier fix) correctly follows.

This reads like an earlier/abandoned attempt at a simplified in-tab "Run Analysis" shortcut that was never reconciled with the canonical collector runner, rather than a deliberate bootstrap exception.
Recommendation

Don't patch analysis_controller.py in place — the cleanest fix is to make Project Q&A's "Run Analysis" delegate to the same proven runner path the working collector window already uses (same subprocess invocation of runner.py with positional args, same analysis_json_complete_dir(project_root) for the expected output path), rather than maintaining a second, divergent invocation of the collector. That also automatically fixes the "reads from the wrong folder" pattern for this button too, consistently with the fix I already made.

Want me to implement that (wire analysis_controller.py to reuse reasoner_tools_shell/runner_help's invocation pattern), or would you rather see the two options (delegate vs. standalone fix) laid out in more detail first?

gimme update to tab get information from correct place to allow local aI answer questions correctly. use this structure, send me zip, install code freeze code
Architected JSON schema, PowerShell scripts, and validation framework comprehensively

Now I have exact ground truth for the freeze hint intake schema and mechanism (not guessing) — pulled directly from models.py and scanner.py. Let me build the full patch.
Ran 3 commands, created a file

Validator confirmed to discriminate correctly (fails against the original bug, passes against the fix). Now the install/validate/freeze scripts and manifests.
Orchestrated configuration setup and documentation for code deployment package

Now the README and the ZIP-contract validator I'll actually run before claiming pass/fail.
Ran a command, created a file

Now the ZIP-contract validator I'll run myself before claiming pass, then package and validate the exact final ZIP.
Ran 2 commands, created a file

Stray __pycache__ artifacts got picked up from my earlier compile check. Cleaning and rebuilding.
Remove pycache and rebuild the clean ZIP

Clean now. Running the exact final ZIP through the contract validator before claiming anything.
Orchestrated workflow simulation to validate installation, freezing, and delivery mechanisms

End-to-end install→validate flow confirmed working. Now the SHA-256 of the final ZIP and packaging for delivery.
Ran a command, read a file
Delivered

patch_project_qa_active_project_local_ai_json_copy_fix_v1.zip
SHA-256: 0cd07949c1c1397358945634a5a660b6764fee9d60593cfb45e3787782cdd76f
ZIP CONTRACT: PASS (checked against the exact final downloadable ZIP, not a draft)

Validation markers actually observed (run by me before delivery, not invented):

VALIDATION OK: project_qa_active_project_local_ai_json_copy_fix_v1
STATUS: IN_SYNC

— confirmed to correctly fail against the original file and correctly pass after install, in a real end-to-end simulated install→validate run.

What changed: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py — Project Q&A's Create/Refresh Local-AI Copy buttons now resolve the active selected project (window.project_root_edit, shell-synced) instead of always resolving to kanda_reasoner's own tool folder.

Changed files: 1 (see PATCH_README.txt for full detail, SHA-256, line count)
Install

Run from the extracted daily-work folder, after staging the ZIP per your normal contract (place at project drive root → stage into <drive>:\<project_name>_delete_after_daily_work\ → delete the drive-root copy → extract):
powershell

powershell -File INSTALL.ps1 -ProjectRoot "<path to kanda_reasoner tool root>"

Backs up the previous file automatically before overwriting.
Validate
powershell

powershell -File VALIDATE.ps1 -ProjectRoot "<path to kanda_reasoner tool root>"

Expected:

VALIDATION OK: project_qa_active_project_local_ai_json_copy_fix_v1
STATUS: IN_SYNC

Freeze

Only after the markers above appear:
Patch project qa active project local ai json copy fix v1
ZIP 


