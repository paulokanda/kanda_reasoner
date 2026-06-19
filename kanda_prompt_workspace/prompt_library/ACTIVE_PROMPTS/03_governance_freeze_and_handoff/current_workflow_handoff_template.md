# Current Workflow Handoff Template

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.1
Status: Daily engineering handoff template
Use: End of workday, break, unfinished task, or before switching chats.

This is not an official governance update.
Use 0000 4.11 only after a validated, user-approved freeze.

Handoff output format:

===============================================================================
REASONER CURRENT ACTIVE WORKFLOW HANDOFF
===============================================================================

Date:
- <YYYY-MM-DD>

Project:
- Project Reasoner / developer_tools

Project root:
- <PROJECT_ROOT>

Handoff type:
- daily_engineering_handoff
- not_official_canon_update

Current active box:
- <box name>

Owning paths:
- <project-relative paths or NONE>

Boxes explicitly out of scope:
- <box/path>
- <box/path>

Current task:
- <summary>

User target outcome:
- <target>

What was completed:
1. <item>

What was validated by the user:
1. <gate/result>

What was delivered but still needs validation:
1. <bundle/gate>

What was discussed but not implemented:
1. <proposal>

Open bugs or unresolved observations:
1. <bug>

Known risks:
1. <risk>

Frozen or do-not-regress behavior:
1. <behavior>

Important prior canon:
1. PROJECT_ROOT is dynamic and user-selected.
2. GUI-first workflow remains primary.
3. Static collector, runtime collector, V10 reader/GUI, retriever, prompt builder, and AI bridge are separate boxes.
4. Runtime/source bundle manifests go in _bundle_temp.
5. Governance-only bundles go in _project_reference\ACTIVE_PROJECT_ GOVERNANCE.
6. No normal delivery requires a separate backup-script folder or a install script.
7. No exhaustive runtime testing claim without full project and runnable environment.

Files recently modified or delivered:
1. <path>

Bundles delivered:
1. <bundle>
   - status: <validated | pending | failed | superseded>
   - validation: <result>

Terminal validation status:
- py_compile: <passed | failed | not run | targeted only>
- focused checker: <passed | failed | not run | targeted only>
- pytest: <passed | failed | not run | targeted only>
- full runtime test: <not performed unless complete project was available>

Manual GUI validation status:
- <passed | pending | failed | not applicable>

Testing honesty:
- <targeted only | full runtime performed with evidence>

Next safe step:
- <one precise next action>

Prompt files the next AI should request before implementation:
1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
2. universal_delivery_protocol.md
3. reasoner_startup_canon.md
4. daily_reasoner_startup_loader.md
5. Current active governance files or active governance ZIP
6. Latest 0000 6.0 handoff
7. Current task description
8. Relevant source ZIP, logs, and validation output

Additional prompts needed:
- <0000 3.6 if high risk>
- <0000 5.7 if large module/refactor>
- <0000 7.1 if problem set roadmap>
- <0000 4.11 only if governance update is requested>

Do not touch next:
- <box/path>

If contradiction appears:
- Stop.
- State the contradiction.
- Compare source files, runtime logs, active governance, and this handoff.
- Ask the user before changing frozen behavior.

End-of-handoff instruction:
- Continue with a focused audit of the next active box.
- Do not implement until required prompt files and current source files are available.
- Do not update canon from this handoff alone.

===============================================================================
END OF REASONER CURRENT ACTIVE WORKFLOW HANDOFF
===============================================================================
