I will treat this as canonical for the JSON bundle roadmap and for future Project Reasoner work:

Closed-box implementation
A feature must be implemented inside its own owning box.
It may communicate with other boxes only through explicit interfaces, adapters, contracts, or generated evidence.
It must not directly change another box’s code unless there is a declared cross-box reason, such as boundary repair or a required handoff.
Project-agnostic implementation
Nothing is specific to E:\developer_tools.
No hardcoded drive, root, project name, or absolute path.
The same mechanism must work for any project root on C:\, D:\, E:\, external drives, or future project folders.
Project-local generated files
JSON files must belong to the project being analyzed.
The output location must be dynamically resolved from the active project context.
Example only, not hardcoded:
<PROJECT_ROOT>\PROJECT_ANALYSIS_EVIDENCE\json_complete\
    <project_name>__complete.json
    <project_name>__active_snapshot.json
    <project_name>__file_manifest.json
    <project_name>__exclusion_rules.json
    <project_name>__validation_state.json
    <project_name>__bundle_manifest.json
Multiproject Kanda Reasoner rule
The generator must support many projects.
Each project owns its own evidence files.
Evidence from one project must not leak into another project.
Project identity should come from active GUI/project context, CLI --root, or a project registry, not from fixed paths.
Roadmap correction
The JSON context bundle should be designed as a project-agnostic closed-box feature, probably something like:
kanda_reasoner_app/project_context_bundle/
It should expose clean outputs to other boxes, but not mutate Tab 1, Tab 2, Tab 3, Tab 8, Tab 9, or governance code unless explicitly scoped.

The revised principle is:

Build a closed-box, project-agnostic AI context bundle generator that reads the active project context dynamically, respects that project’s exclusion rules, and writes only that project’s own generated evidence files into that project’s own evidence folder.

That is the foundation before any code implementation.