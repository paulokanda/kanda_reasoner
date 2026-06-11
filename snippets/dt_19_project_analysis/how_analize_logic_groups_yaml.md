How to Analyze Logic via File Groups

A practical guide to make focused relationship reports (ASCII + PNG/HTML) for any subset of your repo.

TL;DR

Define a named group in dev_tools/project_analysis/file_groups.yaml.

Run from PyCharm: Parameters â†’ group-report <group_name> (or --no-png).

Open results in dev_tools/results_report/:

group_<group_name>.txt (ASCII relationships)

group_<group_name>.png + group_<group_name>.html (optional)

Whatâ€™s a â€œGroupâ€?

A group is a named set of files you care about (e.g., dropdown_tooltip).
The analyzer expands those files/patterns, analyzes only that subset, and produces a clean relationship map (imports within the subset) so you can understand logic and connections without the noise of the whole project.

Where Groups Live

Create/edit:

dev_tools/project_analysis/file_groups.yaml


Keys are group names

Values are lists of entries (file paths, folders, or glob patterns)

YAML is whitespace-sensitiveâ€”use spaces, not tabs

Example: your â€œdropdown + tooltipâ€ slice

dropdown_tooltip:
  - k06_templates/tooltip_lane_tmplt/tooltip_help_center.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/combobox_template.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_lane_json_loader.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/dropdown_caption_formatter.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/filters_controller.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_template_helpers/update_dropdown_cmbbx_template_helper.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_template_helpers/class_option_loading_cmbbx_template_helper.py
  - k03_tabs/k03_3_content/k03_3_eeg_traces_tab.py
  - k01_core_eeg/k01_3_eeg_visualizer/visualizer_core_helpers/display_pyside6_eeg_visualizer.py
  - k01_core_eeg/k01_3_eeg_visualizer/eeg_visualizer_core.py

ou can also put folders (will recurse *.py) or globs, e.g.
k05_combobox_forge/**/cmbbx_*helper*.py

How to Run (PyCharm)

You donâ€™t need terminal/PowerShell. Use PyCharmâ€™s Run/Debug:

Open dev_tools/project_analysis/project_analizer_2_runner.py.

Create a Run Configuration:

Script path: this file

Parameters:

For a YAML-defined group:

group-report dropdown_tooltip

Add --no-png if you want ASCII only.

For ad-hoc (no YAML), pass explicit files or globs:

ad-hoc-report k05_combobox_forge/**/*.py --no-png

Run.

Open results in dev_tools/results_report/:

group_dropdown_tooltip.txt

group_dropdown_tooltip.png

group_dropdown_tooltip.html

What Youâ€™ll Get
ASCII (always)

Group: dropdown_tooltip â€” 2025-09-20 22:37
Files (10):
  â€¢ k06_templates/tooltip_lane_tmplt/tooltip_help_center.py
  â€¢ k05_combobox_forge/k05_4_cmbbx_constructor/combobox_template.py
  ...
Relationships (file â†’ file):
  - k05_combobox_forge/.../filters_controller.py  â†’  k05_combobox_forge/.../combobox_template.py
  - k03_tabs/k03_3_content/k03_3_eeg_traces_tab.py â†’ k01_core_eeg/k01_3_eeg_visualizer/eeg_visualizer_core.py
  ...

PNG/HTML (optional)

One node per file, color-coded by top folder

Edges for internal imports within the subset

HTML wrapper showing the PNG

How It Works (Under the Hood)
1) load_file_groups()

Reads file_groups.yaml â†’ returns a dict:

{
  "dropdown_tooltip": [
    "k06_templates/tooltip_lane_tmplt/tooltip_help_center.py",
    "k05_combobox_forge/k05_4_cmbbx_constructor/combobox_template.py",
    ...
  ],
  ...
}

Troubleshooting

â€œNo edges in reportâ€

Files may not import each other directly, or imports reference tokens that donâ€™t match any file stem/top module in the subset.
â†’ Add more provider files or broaden with folder/glob entries.

BOM or weird characters

Analyzer reads with utf-8-sig and errors="replace".
If parse still fails, remove or escape non-ASCII characters in code (OK in strings/comments).

Duplicates in YAML

Harmlessâ€”de-duplicated automatically.

Tests missing

By design. If you want tests included, tweak resolve_group_files() filter (remove _is_test_path checks).

Quick Recipes
Create a new group

Edit dev_tools/project_analysis/file_groups.yaml:

my_new_flow:
  - path/to/file_a.py
  - path/to/folder_b/
  - some/module/**/pattern_*.py

Run in PyCharm:
group-report my_new_flow

Open results in dev_tools/results_report/:

group_my_new_flow.txt

group_my_new_flow.png

group_my_new_flow.html

One-off analysis without YAML

Run:
ad-hoc-report k05_combobox_forge/**/*.py --no-png

FAQ

Q: Will this teach the AI the projectâ€™s logic?
A: It gives a clear, minimal map of how chosen files depend on each other. When you share the ASCII/PNG outputs, itâ€™s much easier for an AI (and humans) to understand intent, boundaries, and call paths within that slice.

Q: Can I include third-party/stdlib edges?
A: The report intentionally focuses on internal relationships in your chosen subset. External deps show up as no internal target, which keeps the graph clean.

Q: Can I version control these outputs?
A: Yesâ€”dev_tools/results_report/ is deterministic and CI-friendly. Commit the ASCII and PNG/HTML if you want historical diffs.

Appendix: Example Starter file_groups.yaml

# Focused UI slice for dropdown + tooltip UX
dropdown_tooltip:
  - k06_templates/tooltip_lane_tmplt/tooltip_help_center.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/combobox_template.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_lane_json_loader.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/dropdown_caption_formatter.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/filters_controller.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_template_helpers/update_dropdown_cmbbx_template_helper.py
  - k05_combobox_forge/k05_4_cmbbx_constructor/cmbbx_template_helpers/class_option_loading_cmbbx_template_helper.py
  - k03_tabs/k03_3_content/k03_3_eeg_traces_tab.py
  - k01_core_eeg/k01_3_eeg_visualizer/visualizer_core_helpers/display_pyside6_eeg_visualizer.py
  - k01_core_eeg/k01_3_eeg_visualizer/eeg_visualizer_core.py

# Broader combobox helpers
combobox_helpers:
  - k05_combobox_forge/**/cmbbx_*helper*.py

# Core visualization
viz_core:
  - k01_core_eeg/k01_3_eeg_visualizer/**/*.py

# Broader combobox helpers
combobox_helpers:
  - k05_combobox_forge/**/cmbbx_*helper*.py

# Core visualization
viz_core:
  - k01_core_eeg/k01_3_eeg_visualizer/**/*.py

