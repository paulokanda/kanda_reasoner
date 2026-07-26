# Project Tool Boundary Startup Bridge Split Reconciliation v1

Primary owner: `project_tool_boundary_canon` (`KPR-12-001`)
Startup bridge: `project_tool_boundary_startup_bridge` (`KPR-12-006`)
Decision: `SPLIT_NON_AUTHORITATIVE_STARTUP_BRIDGE`

## Verified problem

The full KPR-12-001 canon was always-startup and carried detailed Q06, Workbench, migration, and path-policy text. This consumed startup context and mixed a compact invariant with routed specialist reasoning.

## Ownership decision

- KPR-12-001 retains the full Tool/Project identity and root-ownership responsibility.
- KPR-12-006 is a compact startup bridge only.
- The bridge has no source-write, validation-claim, delivery, or freeze authority.
- Consequential work routes to KPR-12-001.
- No second boundary canon or coordination system is created.

## Compatibility

The generated startup filename remains `14_project_tool_boundary_canon.md` so the startup read order and external upload contract remain stable. Its canonical source changes to the compact bridge. KPR-12-001 remains available by prompt code, prompt ID, path, navigation, and machine routing.
