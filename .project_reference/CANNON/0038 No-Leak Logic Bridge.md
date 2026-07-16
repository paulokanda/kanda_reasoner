## No-Leak Logic Bridge

NO_LEAK_LOGIC_V1: No-Leak Logic is a named boundary-protection object inside Box Logic and Box Shielding.

It prevents ownership, path, state, contract, evidence, and responsibility from leaking across boxes.

No-Leak Logic is not a separate architecture system. It is a specific enforcement object inside the existing Box Logic and Shielding discipline.

### Core rule

Before implementation, refactor, prompt update, validation, freeze, patch delivery, GUI work, or artifact generation, classify every touched item as one of:

1. tool-owned logic;
2. active-project source;
3. project-specific support state;
4. generated evidence or handoff artifact;
5. temporary daily-work artifact;
6. external box dependency;
7. out-of-scope file.

If classification is unclear, stop before writing and inspect the source, manifest, prompt, or validation context.

### No-Leak checklist

The AI must block or flag all of the following:

1. Tool/project leakage
   Reusable KANDA Reasoner tool logic must not be written into active-project output paths. Active-project generated/refactored files must not be written into reusable tool-source paths.

2. Wrong-root leakage
   Project-specific support files must use the selected active project root and its external support folders, not a hardcoded KANDA Reasoner root.

3. Cross-box logic leakage
   Code, imports, mutable state, UI logic, domain logic, prompt logic, validation logic, governance logic, freeze logic, or delivery logic must not move from one box into another without an explicit governed cross-box touch.

4. Private reach-in leakage
   A box must not import, call, edit, or depend on another box's private internals. Use public contracts only.

5. Public API ownership leakage
   Helper modules must not accidentally become public owners of facade symbols. Facades own public compatibility surfaces unless a separate architecture change approves another owner.

6. Mutable-state leakage
   Hidden mutable globals, registries, caches, singletons, or shared runtime state must not become silent communication channels between boxes.

7. Generated-artifact leakage
   Generated handoff files, startup ZIP contents, reports, manifests, validation output, and preview artifacts are not source truth unless explicitly promoted through the governed source path.

8. Validation/freeze leakage
   Validation evidence, freeze hints, freeze memory, and error-memory intake must stay in their governed locations and must not be mixed into unrelated tool, project, or generated-output paths.

9. Prompt/canon leakage
   Prompt-library canon updates must be made in canonical prompt files, not only in generated startup artifacts or copied ZIP contents.

10. Refactor-output leakage
    Refactor engines, analyzers, planners, and validators are tool-owned. The concrete split/refactored files produced for a selected project are project-owned.

### Required output when risk exists

When a task has no-leak risk, output this before implementation:

NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:

### Routing rule

If any no-leak answer is uncertain, route to:

* box_architecture_canon.md;
* kanda_box_shielding_canon.md;
* project_tool_boundary_canon.md when tool/project ownership is involved;
* startup delivery maintenance rules when generated startup delivery is involved.

Do not proceed from memory when ownership, root, box, public contract, generated/source status, or freeze/validation location is unclear.
