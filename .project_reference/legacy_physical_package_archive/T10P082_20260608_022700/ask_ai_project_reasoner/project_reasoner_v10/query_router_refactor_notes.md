# query_router refactor notes

Structural changes:
- extracted repeated phrase lists into module-level constants
- centralized "which calls + code/snippet request" logic into `_which_calls_needs_code_answer()`
- kept public names unchanged:
  - `QueryRouteDecision`
  - `route_query_intent`
- kept route names, intent names, reasons, and debug print keys unchanged
- preserved decision order in `route_query_intent()`

Validation commands:
- `python -m py_compile E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\query_router.py`
- `python check_query_router_routes.py`
