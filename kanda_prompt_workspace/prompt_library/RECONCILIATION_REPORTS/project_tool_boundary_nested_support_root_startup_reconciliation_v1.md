# Project Tool Boundary Nested Support Root Startup Reconciliation v1

Owner canon: `project_tool_boundary_canon` (KPR-12-001)

## Source evidence

- User-uploaded Project Tool Boundary Canon v1.2.
- Existing active Project Tool Boundary Canon v1.3.
- Current startup source map where KPR-12-001 was absent and therefore routed only.
- Current production path helpers and Workbench support-root constructors.
- Release 9 outbound validator source that created `_release9_exchange_validation_fixture` inside the Project source root.

## Decision matrix

| Idea | Decision | Owner |
|---|---|---|
| Keep Tool and selected Project identities separate | ALREADY_PRESENT | KPR-12-001 |
| Support root must be external sibling/drive-root | ALREADY_PRESENT, strengthened | KPR-12-001 plus public path contract |
| Nested `<active_project_root>/<slug>_show_project_to_AI` can never exist | UPDATE_EXISTING_PROMPT | KPR-12-001 v1.4 |
| AI must not forget this boundary at session start | UPDATE_STARTUP_REGISTRATION | startup source map load order 14 |
| Duplicate path derivation should be eliminated | UPDATE_EXISTING_RUNTIME_OWNER | public `project_support_boundary.py` contract |
| Existing nested folder must be removed without data loss | REPAIR_UTILITY | conflict-safe migration tool |
| Release 9 fixture must never be recreated in Project source | UPDATE_VALIDATOR_OWNER | transient garbage root plus guaranteed cleanup |

## Why no new prompt was created

KPR-12-001 already owns Tool-versus-Project identity and path ownership. A new prompt would duplicate the canon and increase routing ambiguity. The correct action is to update the existing prompt and promote its load mode from routed to always_startup.

## Do not regress

- Do not downgrade v1.3 content while importing the uploaded v1.2 file.
- Do not edit generated startup artifacts as canonical source.
- Do not silently overwrite differing files during nested-root repair.
- Do not permit production modules to independently construct Project support roots.
- Do not create validation fixtures inside the Tool or active Project source root.
