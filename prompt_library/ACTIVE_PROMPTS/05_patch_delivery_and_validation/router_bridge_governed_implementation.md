---
prompt_id: router_bridge_governed_implementation
title: Router Bridge Governed Implementation Gate
version: 1.3
status: active_candidate
load_type: routed
owner_group: 05_patch_delivery_and_validation
created_by_patch: startup-second-upload-hard-gate-v1
---

# Router Bridge Governed Implementation Gate

## Purpose

Use this routed bridge before any governed implementation work. This bridge closes the memory-based coding failure mode by requiring a visible implementation gate before code, prompt, startup, validation, GUI, Error Memory, freeze, or patch-source edits begin.

The bridge does not replace the existing router. It makes the router produce a compliance artifact before implementation.

## Trigger conditions

Route here when the user request or the AI plan includes any of the following:

```text
implement code
repair code
refactor code
modify source files
create a validation script
edit prompt library files
update router or prompt bridge logic
update startup delivery logic
modify generated startup behavior
modify GUI behavior
create a patch payload
change Error Memory workflow
change freeze workflow
handle a real project task after only the first startup upload group
```

Do not route here for simple explanation-only work that will not edit source, prompts, validation files, startup files, or patch artifacts.

## Required companion prompts

Load or apply the smallest complete set:

```text
prompt_router
implementation_and_delivery_protocol
box_architecture_canon, when boundary risk exists
project_tool_boundary_canon, when project/tool identity can be confused
pre_output_contract_gates, when terminal, ZIP, freeze, or validation artifacts will be emitted
python_clean_code or relevant Python engineering prompt, when Python files are changed
```

Do not load the entire prompt library. Do not code from memory.

## Mandatory Implementation Gate

Before implementation begins, emit this visible gate with truthful values:

```text
IMPLEMENTATION GATE
Task domain:
Router bridge selected:
Required prompt path:
Target box:
Forbidden box:
Source files inspected:
Generated-vs-canonical status:
Project/tool disambiguation needed:
Second-upload readiness:
Line-count risk:
GUI-resolution risk, if GUI:
May implement: YES / NO
```

Hard rule:

```text
No governed implementation may begin unless May implement is YES.
```

If any field is unknown, missing, not inspected, or unsafe, May implement must be NO and the AI must inspect the needed source, request the needed project files, or route to the required prompt before proceeding.

## Source audit requirement

## SECOND_UPLOAD_PROJECT_READY_GATE

Before any governed implementation begins, the bridge must verify the project
readiness state.

Hard rule:

```text
STARTUP PACK LOAD CHECK complete + second_prompt_files not loaded = May implement: NO
PROJECT READY CHECK returned with Next action: WAIT_FOR_TASK = May implement may be YES if all other gates pass
```

If the second upload group is missing, the AI must not continue with the user's
project request. It must ask for the second set of files from `second_prompt_files`
and keep asking on later project-task attempts until the required files are
loaded and the `PROJECT READY CHECK` is complete.

The Implementation Gate `Second-upload readiness` field must use one of:

```text
loaded - PROJECT READY CHECK complete
waiting - first startup complete, second_prompt_files not loaded
missing - no second upload evidence available
unknown - state cannot be verified from the chat
```

Only `loaded - PROJECT READY CHECK complete` can support `May implement: YES`.
All other states force `May implement: NO`.


The gate must list actual inspected files. It may not say "from memory" or rely on the previous conversation alone. If exact source files are unavailable, the AI must stop before editing and request or inspect the source archive or handoff manifest.

## Generated-vs-canonical requirement

If the target appears to be generated output, the gate must identify the canonical generator/source file to edit instead. Generated files may be regenerated after validation, but they should not be the only edited files unless the project explicitly defines them as canonical.

## Box boundary requirement

The gate must identify the active box and forbidden boxes. Typical boxes include:

```text
prompt-library
startup-delivery
patch-delivery
validation
Error Memory
freeze-memory
GUI
domain logic
source-project
tool-infrastructure
```

If the active project is `kanda_reasoner`, the AI must still distinguish the active target project from the reusable KANDA Reasoner tool role. Shared physical root does not remove the need for logical separation.

## Line-count and GUI requirements

When Python files are changed, line-count risk must enforce the code module-size law, not merely mention risk.

Code/source module-size law:

```text
Ideal module size: <= 400 lines.
Maximum module size: <= 500 lines.
```

Hard routing rule:

```text
If a new Python code module is expected to exceed 500 lines, do not create it as one file.
Route to Large Module Creation and Refactor Protocol v7.2 before implementation, split by responsibility, and define the target helper/module structure first.
```

For existing Python modules:

```text
If a touched Python module is already over 500 lines, or the planned change would push it over 500 lines, the implementation gate must route to large_module_refactor_protocol v7.2 and state whether AST Split Audit handoff is available.
If a touched Python module is near the ideal limit, around 400 lines or more, the implementation gate must state line-count risk and whether the change should be split into a smaller helper/module before delivery.
No governed patch may silently create or enlarge a Python code module above 500 lines without an explicit v7.2 staged refactor exception and validation plan.

Additional v7.2 granularity gate:

If a refactor would create several tiny Python helper files, require a practical-granularity check before delivery. Cohesive helper files near the 400-line ideal are acceptable. Do not create tiny helper crumbs, 5-line modules, or extra train cars merely to reduce line count when a responsibility helper can remain cohesive. Runtime/source logic must live in ordinary importable `.py` files; ZIP `payload/` structure is delivery packaging only, not application logic.
```

The Implementation Gate `Line-count risk` field must include current and projected line-count status when Python code is created or modified:

```text
Line-count risk: current N lines; projected M lines; ideal <=400; maximum <=500; v7.2 routing needed YES/NO.
```

When GUI files are changed, GUI-resolution risk must mention laptop-to-4K usability and avoid fixed-size-only assumptions when possible.

## Sequential double-refactor delivery train rule

When a large-module refactor roadmap can produce several independent or dependency-ordered refactor patches, route to Large Module Creation and Refactor Protocol v7.2. The allowed delivery-train shape is:

```text
Patch ZIP 1: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 2: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 3: up to two related refactor slices -> install -> validate -> freeze
Patch ZIP 4: up to two related refactor slices -> install -> validate -> freeze
```

Hard rules:

```text
Maximum per response: 4 ordered patch ZIPs.
Default maximum per ZIP: 2 related refactor slices.
Each ZIP must have its own feature id, install, validation, ZIP contract check, freeze code, KANDA_FREEZE_HINT.json, rollback boundary, and freeze entry.
Do not install the next ZIP until the current ZIP has passed validation and has been frozen.
Stop the train if any ZIP fails install, validation, ZIP contract, freeze-prep, preview, or freeze.
Do not freeze the outer train as one vague entry.
```


## Failure behavior

If the implementation gate cannot pass, do not implement. Output the missing source, missing prompt, unsafe box boundary, or generated-file conflict that must be resolved first.
