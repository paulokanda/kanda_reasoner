### Helper expansion rule

When a new or touched code/source module would exceed the 500-physical-line hard maximum, the implementation must split the work into as many cohesive helper, auxiliary, derived, adapter, or complementary modules as needed to preserve behavior, ownership, readability, and validation safety.

Creating additional helper modules is allowed and expected when needed to keep the main module and every helper module within the size limit.

Every helper or auxiliary code/source module must obey the same size law:

* ideal size: 400 physical lines or fewer;
* hard maximum: 500 physical lines or fewer;
* practical minimum: 100 physical lines or more unless a documented exception applies.

Do not create tiny helper files merely to satisfy a line-count target. A helper below 100 physical lines is allowed only when it is justified as a facade/re-export shim, package marker, constants module, validation helper, optional dependency adapter, cycle breaker, stable seam, or another explicitly documented cohesive boundary.

Prefer cohesive responsibility modules over catch-all helpers or project hyperpopulation. Split by responsibility, dependency direction, public API boundary, side-effect isolation, validation boundary, or no-leak ownership boundary, not by arbitrary line ranges.

Where this belongs

Insert it in three places:

Canonical large-module prompt
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md
Best location: under Module-size and complexity law, after the existing “Practical granularity rule for helper files.”
Large-module refactor template
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_template.md
Best location: under the target structure/helper-file planning section.
Startup bridge source
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md
Best location: inside BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_START.

Do not edit generated startup ZIP contents directly. Generated startup artifacts are not source truth; prompt/canon updates must happen in canonical prompt files and then be regenerated through the governed startup delivery path. The No-Leak Bridge explicitly blocks prompt/canon leakage and generated-artifact-as-source leakage.

BOX CHECK
BOX CHECK

Task type:
Governed prompt/canon and startup bridge clarification before tool-feature implementation.

Active box:
KANDA/Canda Reasoner prompt/canon layer, with later tool-owned implementation.

Owner path:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/

Allowed files:
large_module_refactor_protocol.md
large_module_refactor_template.md
start_of_day_master_stack.md
startup generated artifacts only through regeneration, not direct manual edit

Out-of-scope files:
Concrete project refactor outputs
Generated split files
Freeze memory
Prompt ZIP contents edited directly
Unrelated GUI/source modules

Cross-box touches:
Yes, prompt/canon affects future tool implementation behavior.

Public contracts:
Code Module Size Bridge
Large Module Refactor Protocol
No-Leak Logic Bridge
Tool/project ownership boundary

Validation scope:
Prompt text scan
Startup regeneration check if startup bridge changes
Obsolete reference scan
Startup pack inspection if generated artifacts are regenerated

Boundary risks:
Generated-artifact-as-source leakage
Tool/project leakage
Over-fragmentation into tiny helper files
Facade/helper public API ownership leakage

Tool/project ownership risk:
Moderate, because the future Large File Refactor Planner is tool-owned but will produce project-owned outputs.

No-leak risk:
Moderate to high unless the bridge explicitly states helper expansion must stay inside owner paths and allowed roots.

May proceed:
YES, but as governed prompt/canon update before implementation.

Next safe action:
Patch canonical prompt files first, regenerate startup delivery only through the generator, then implement the Large File Refactor Planner.
NO-LEAK CHECK
NO-LEAK CHECK

Active box:
Prompt/canon update now; KANDA/Canda Reasoner tool implementation later.

Tool-owned files:
Large File Refactor Planner GUI, controller, analyzer, planner, docstring engine, LLM arbitration, preview writer, validation runner, patch creator, no-leak gate.

Project-owned files:
Selected source file being refactored, generated split modules, generated project helper files, project-specific docstrings, project preview outputs, project-specific validation evidence.

Project-specific support files:
Refactor plan JSON, preview folder, patch payload, project freeze hint if applicable.

Generated/evidence files:
Startup ZIPs, validation output, freeze hints, handoff artifacts, preview reports.

Temporary daily-work files:
Only under the selected active project daily-work/delete-after-daily-work area.

External boxes touched:
Startup delivery only if the bridge is regenerated.

Out-of-scope files:
Direct ZIP-content edits, freeze memory writes, unrelated project source, unrelated prompt canons.

Leak risks:
Tool logic leaking into project-generated output.
Project split files leaking into tool source.
Helper modules accidentally owning facade public API.
Generated startup artifacts being treated as canonical source.
Tiny helper-file hyperpopulation.

Blocked writes:
Any write outside canonical prompt files for this rule update.
Any direct edit to generated startup ZIP contents.
Any project refactor output during tool-feature implementation.

Safe next action:
Add the helper expansion rule to the canonical large-module prompt and startup bridge source, then regenerate/validate startup delivery before coding the planner.
Implementation consequence

For the Large File Refactor Planner, I will apply this rule like this:

- No new/touched Python module may exceed 500 physical lines.
- Target size remains around 400 lines.
- The planner may create as many helper modules as needed.
- Every helper must be cohesive and justified.
- Helpers should generally be >=100 lines unless they match an allowed exception.
- Helpers must not become dumping grounds.
- Helpers must not accidentally own facade public API.
- The original facade remains the public owner unless a governed architecture change says otherwise.

This also aligns with Error Memory: previous large-module splits failed when helper modules accidentally exported the same public symbol as the facade, so the helper expansion rule must be paired with facade/public API ownership protection