# project-path: tools/project_structure_3d_v1d_qt_navigation_probe.py
"""Platform-stable real-Qt navigation probes for Project Structure 3D v1D."""

from __future__ import annotations

import json
import time
from typing import Any, Callable

__all__ = ["validate_navigation_actions"]


def _require(condition: bool, message: str) -> None:
    """Raise one deterministic navigation validation error."""
    if not condition:
        raise AssertionError(message)


def _wait_until(app: Any, predicate: Callable[[], bool], timeout: float) -> bool:
    """Process Qt events until one bounded predicate succeeds."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    app.processEvents()
    return bool(predicate())


def _run_javascript(app: Any, page: Any, script: str) -> Any:
    """Run one bounded JavaScript probe."""
    result: dict[str, Any] = {"done": False, "value": None}

    def receive(value: Any) -> None:
        result["done"] = True
        result["value"] = value

    page.runJavaScript(script, receive)
    _require(_wait_until(app, lambda: bool(result["done"]), 12.0), "JS timeout")
    return result["value"]


def _run_json_expression(app: Any, page: Any, expression: str) -> Any:
    """Return one expression through a deterministic JSON text envelope."""
    script = (
        "(() => { try { return JSON.stringify({probeOk:true,value:("
        + expression
        + ")}); } catch (error) { return JSON.stringify({probeOk:false,error:"
        "String(error && error.stack ? error.stack : error)}); } })()"
    )
    raw = _run_javascript(app, page, script)
    _require(isinstance(raw, str), "JavaScript JSON probe did not return text")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "JavaScript JSON probe was invalid: " + raw[:400]
        ) from exc
    _require(isinstance(payload, dict), "JavaScript JSON probe root was not an object")
    _require(
        bool(payload.get("probeOk")),
        "JavaScript probe failed: "
        + str(payload.get("error") or "unknown error")[:500],
    )
    return payload.get("value")


def _mapping(value: Any, label: str) -> dict[str, Any]:
    """Require one decoded JavaScript object with useful diagnostics."""
    _require(
        isinstance(value, dict),
        label + " result was not an object: " + repr(value),
    )
    return value


def _action(app: Any, page: Any, expression: str, label: str) -> dict[str, Any]:
    """Run one action and require its JSON-decoded success object."""
    result = _mapping(_run_json_expression(app, page, expression), label)
    _require(bool(result.get("ok")), label + " failed: " + repr(result))
    return result


def _state(app: Any, page: Any, label: str) -> dict[str, Any]:
    """Read the durable navigation state through JSON text."""
    return _mapping(
        _run_json_expression(
            app,
            page,
            "window.kandaProjectGraph.navigationState()",
        ),
        label,
    )


def _focus(app: Any, page: Any, query: str, label: str) -> dict[str, Any]:
    """Focus one node and prove that selection state was committed."""
    quoted = json.dumps(query, ensure_ascii=True)
    focused = _run_javascript(
        app,
        page,
        "window.kandaProjectGraph.focusByQuery(" + quoted + ")",
    )
    _require(bool(focused), label + " query did not match a node")
    state = _state(app, page, label + " state")
    _require(
        bool(state.get("selectedId")),
        label + " did not create a selected node: " + repr(state),
    )
    return state


def validate_navigation_actions(app: Any, page: Any, total_nodes: int) -> None:
    """Validate actions by durable state rather than QVariant container shape."""
    _focus(app, page, "Child", "focus Child")
    _action(
        app,
        page,
        "window.kandaProjectGraph.isolateSelected()",
        "isolate selected",
    )
    isolated = _state(app, page, "isolated navigation state")
    _require(
        isolated.get("focusMode") == "neighborhood",
        "isolation mode was not applied: " + repr(isolated),
    )
    _require(
        int(isolated.get("visibleNodeCount") or 0) < int(total_nodes),
        "isolation did not reduce visible nodes: " + repr(isolated),
    )

    _action(app, page, "window.kandaProjectGraph.showOverview()", "show overview")
    _focus(app, page, "Child", "refocus Child")
    _action(
        app,
        page,
        "window.kandaProjectGraph.tracePathToQuery('helper')",
        "dependency path",
    )
    path_state = _state(app, page, "path navigation state")
    _require(path_state.get("focusMode") == "path", "path mode was not applied")
    _require(
        int(path_state.get("pathEdgeCount") or 0) >= 1,
        "path edge highlight was not applied: " + repr(path_state),
    )

    _action(app, page, "window.kandaProjectGraph.goBack()", "go back")
    _action(app, page, "window.kandaProjectGraph.goForward()", "go forward")

    _action(
        app,
        page,
        "window.kandaProjectGraph.showOverview()",
        "show overview before expansion",
    )
    _focus(app, page, "Child", "expansion focus")
    _action(
        app,
        page,
        "window.kandaProjectGraph.toggleSelectedExpansion()",
        "collapse selected",
    )
    collapsed = _state(app, page, "collapsed navigation state")
    _require(
        int(collapsed.get("collapsedCount") or 0) == 1,
        "collapse state was not committed: " + repr(collapsed),
    )
    _action(
        app,
        page,
        "window.kandaProjectGraph.toggleSelectedExpansion()",
        "expand selected",
    )
