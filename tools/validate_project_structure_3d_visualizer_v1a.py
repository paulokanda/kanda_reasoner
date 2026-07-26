# project-path: tools/validate_project_structure_3d_visualizer_v1a.py
"""Focused validator for Project Structure 3D v1A revision 2."""

from __future__ import annotations

import argparse
import ast
import importlib.metadata
import importlib.util
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

FEATURE_ID = "project-structure-3d-visualizer-v1a-r2"
REQUIRED_FILES = (
    "kanda_reasoner_app/project_structure_visualizer/__init__.py",
    "kanda_reasoner_app/project_structure_visualizer/fixture_graph.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_schema.py",
    "kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py",
    "kanda_reasoner_app/project_structure_visualizer/safe_web_page.py",
    "kanda_reasoner_app/project_structure_visualizer/web_assets.py",
    "kanda_reasoner_app/project_structure_visualizer/web_bridge.py",
    "kanda_reasoner_app/project_structure_visualizer/web_runtime.py",
    "kanda_reasoner_app/project_structure_visualizer/web/browser_details.js",
    "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js",
    "kanda_reasoner_app/project_structure_visualizer/web/graph_theme.css",
    "kanda_reasoner_app/project_structure_visualizer/web/index_template.html",
    "kanda_reasoner_app/project_structure_visualizer/web/qt_bridge_bootstrap.js",
)


def _require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def _read(root: Path, relative_path: str) -> str:
    """Read one UTF-8 project file explicitly."""
    return (root / relative_path).read_text(
        encoding="utf-8",
        errors="strict",
    )


def _load_fixture_module(root: Path) -> Any:
    """Import fixture support without importing PySide6 GUI owners."""
    package_root = root / "kanda_reasoner_app/project_structure_visualizer"
    package_name = "kanda_reasoner_app.project_structure_visualizer"
    package_spec = importlib.util.spec_from_file_location(
        package_name,
        package_root / "__init__.py",
        submodule_search_locations=[str(package_root)],
    )
    _require(
        package_spec is not None and package_spec.loader is not None,
        "package spec",
    )
    package = importlib.util.module_from_spec(package_spec)
    sys.modules[package_name] = package
    package_spec.loader.exec_module(package)
    module_name = package_name + ".fixture_graph"
    module_spec = importlib.util.spec_from_file_location(
        module_name,
        package_root / "fixture_graph.py",
    )
    _require(
        module_spec is not None and module_spec.loader is not None,
        "fixture spec",
    )
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    module_spec.loader.exec_module(module)
    return module


def validate_registry(root: Path) -> None:
    """Validate the public lazy-tab and Project-scope registrations."""
    specs = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    )
    scope = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py",
    )
    _require(specs.count('tab_id="project_structure_3d"') == 1, "tab ID count")
    _require(
        'class_candidates=("ProjectStructure3DWidget",)' in specs,
        "public widget registration",
    )
    _require(scope.count('"project_structure_3d"') == 1, "Project-scope registration")
    print("PROJECT_STRUCTURE_3D_TAB_REGISTRY: PASS")


def validate_source_modules(root: Path) -> None:
    """Validate syntax, size, ASCII Python, and runtime authority."""
    forbidden_imports = {"shutil", "socket", "subprocess"}
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        _require(path.is_file(), "missing required file: " + relative_path)
        source = path.read_text(encoding="utf-8", errors="strict")
        if path.suffix in {".js", ".py"}:
            _require(
                len(source.splitlines()) <= 500,
                "module exceeds 500 lines: " + relative_path,
            )
        if path.suffix != ".py":
            continue
        _require(source.isascii(), "non-ASCII Python source: " + relative_path)
        tree = ast.parse(source, filename=relative_path)
        imports = {
            alias.name.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            str(node.module or "").split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        )
        if not relative_path.startswith("tools/"):
            _require(
                not imports.intersection(forbidden_imports),
                "forbidden runtime authority import: " + relative_path,
            )
    print("PROJECT_STRUCTURE_3D_SOURCE_MODULE_CONTRACT: PASS")


def validate_graph_contract(root: Path) -> None:
    """Build and validate the canonical deterministic fixture."""
    module = _load_fixture_module(root)
    snapshot = module.build_fixture_graph(Path("E:/kanda_reasoner"))
    _require(
        snapshot["statistics"]["node_count"] == len(snapshot["nodes"]),
        "node count",
    )
    _require(
        snapshot["statistics"]["edge_count"] == len(snapshot["edges"]),
        "edge count",
    )
    _require(
        snapshot["source_provenance"]["authoritative"] is False,
        "fixture authority",
    )
    for node in snapshot["nodes"]:
        _require("E:/" not in node["relative_path"], "absolute path leaked")
    print("PROJECT_STRUCTURE_3D_GRAPH_SCHEMA: PASS")


def validate_web_contract(root: Path) -> None:
    """Validate local-only renderer and the revised runtime loader."""
    html = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/web/index_template.html",
    )
    renderer = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js",
    )
    bootstrap = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/web/qt_bridge_bootstrap.js",
    )
    tab = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py",
    )
    assets = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/web_assets.py",
    )
    runtime = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/web_runtime.py",
    )
    safe_page = _read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/safe_web_page.py",
    )
    combined = "\n".join((html, renderer, bootstrap, assets, runtime))
    _require("http://" not in combined and "https://" not in combined, "external URL")
    _require("fetch(" not in combined, "renderer fetch authority")
    _require("XMLHttpRequest" not in combined, "renderer network authority")
    _require(
        "qrc:///qtwebchannel/qwebchannel.js" in assets,
        "static QWebChannel bootstrap",
    )
    _require("Date.now() + 30000" in bootstrap, "bounded bridge retry deadline")
    _require("ensureBridge" in renderer, "renderer handshake facade")
    _require("write_embedded" in runtime, "local embedded document owner")
    _require("web_view.setUrl(document_url)" in tab, "file URL loading")
    _require("web_view.setHtml(" not in tab, "embedded setHtml regression")
    _require("renderProcessTerminated.connect" in tab, "process diagnostics")
    _require("WebGLEnabled" in runtime, "software-friendly renderer setting")
    _require("_allowed_roots" in safe_page, "local root allowlist")
    _require("_is_live_generation" in tab, "Python stale-generation guard")
    _require("isValid(self)" in tab, "QObject validity guard")
    _require("Open in browser" in tab, "browser preview action")
    print("PROJECT_STRUCTURE_3D_LOCAL_WEB_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_LOCAL_FILE_LOAD_RECOVERY: PASS")
    print("PROJECT_STRUCTURE_3D_QWEBCHANNEL_HANDSHAKE_RECOVERY: PASS")
    print("PROJECT_STRUCTURE_3D_STALE_EVENT_GUARD: PASS")


def validate_javascript(root: Path) -> None:
    """Use Node syntax validation for every JavaScript module when available."""
    relative_paths = (
        "kanda_reasoner_app/project_structure_visualizer/web/browser_details.js",
        "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js",
        "kanda_reasoner_app/project_structure_visualizer/web/qt_bridge_bootstrap.js",
    )
    node = os.environ.get("NODE_EXE", "node")
    for relative_path in relative_paths:
        try:
            result = subprocess.run(
                [node, "--check", str(root / relative_path)],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            print("PROJECT_STRUCTURE_3D_JAVASCRIPT_SYNTAX: SKIPPED")
            return
        _require(
            result.returncode == 0,
            result.stderr.strip() or "JavaScript syntax: " + relative_path,
        )
    print("PROJECT_STRUCTURE_3D_JAVASCRIPT_SYNTAX: PASS")


def _wait_until(
    app: Any,
    predicate: Callable[[], bool],
    timeout_seconds: float,
) -> bool:
    """Process Qt events until one predicate succeeds or times out."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    app.processEvents()
    return bool(predicate())


def _run_javascript(
    app: Any,
    page: Any,
    script: str,
    timeout_seconds: float = 8.0,
) -> Any:
    """Run one bounded JavaScript probe and return its callback value."""
    result: dict[str, Any] = {"done": False, "value": None}

    def receive(value: Any) -> None:
        result["value"] = value
        result["done"] = True

    page.runJavaScript(script, receive)
    _require(
        _wait_until(app, lambda: bool(result["done"]), timeout_seconds),
        "JavaScript probe callback timed out",
    )
    return result["value"]


def _runtime_provenance() -> dict[str, str]:
    """Return bounded interpreter and PySide6 provenance."""
    try:
        pyside_version = importlib.metadata.version("PySide6")
    except importlib.metadata.PackageNotFoundError:
        pyside_version = "unknown"
    return {
        "python": str(Path(sys.executable).resolve()),
        "python_version": platform.python_version(),
        "pyside6": pyside_version,
    }


def _qt_diagnostic(widget: Any, app: Any) -> str:
    """Return bounded page, process, bridge, and runtime evidence."""
    probe: Any = None
    try:
        probe = _run_javascript(
            app,
            widget._web_view.page(),
            "({"
            "documentState: document.readyState,"
            "location: String(window.location.href),"
            "graphFacade: Boolean(window.kandaProjectGraph),"
            "bridgeFacade: Boolean(window.kandaQtBridge),"
            "bridgeConnected: Boolean(window.kandaQtBridge && "
            "window.kandaQtBridge.isConnected()),"
            "qtTransport: Boolean(window.qt && window.qt.webChannelTransport),"
            "qwebchannelLibrary: typeof window.QWebChannel === 'function'"
            "})",
        )
    except Exception as exc:
        probe = {"probe_error": type(exc).__name__ + ": " + str(exc)}
    diagnostics = list(getattr(widget, "_renderer_diagnostics", []))
    return (
        "runtime=" + repr(_runtime_provenance())
        + "; page_load_ok=" + repr(getattr(widget, "_page_load_ok", None))
        + "; page_url=" + repr(widget._web_view.url().toString())
        + "; render_termination=" + repr(getattr(widget, "_render_termination", None))
        + "; js_probe=" + repr(probe)
        + "; console=" + repr(diagnostics[-8:])
    )


def _validate_qwebengine_control(app: Any) -> None:
    """Prove one default local-file QWebEngine page can load."""
    from PySide6.QtCore import QUrl
    from PySide6.QtWebEngineWidgets import QWebEngineView

    events: dict[str, Any] = {"loaded": None, "terminated": None}
    with tempfile.TemporaryDirectory(prefix="kanda_qwebengine_control_") as folder:
        path = Path(folder) / "control.html"
        path.write_text(
            "<!doctype html><html><body><div id='ok'>ready</div></body></html>",
            encoding="utf-8",
            newline="\n",
        )
        view = QWebEngineView()
        view.resize(320, 180)
        view.loadFinished.connect(
            lambda success: events.__setitem__("loaded", bool(success))
        )
        view.page().renderProcessTerminated.connect(
            lambda status, code: events.__setitem__(
                "terminated",
                (getattr(status, "name", str(status)), int(code)),
            )
        )
        view.show()
        view.setUrl(QUrl.fromLocalFile(str(path)))
        completed = _wait_until(
            app,
            lambda: events["loaded"] is not None or events["terminated"] is not None,
            25.0,
        )
        _require(
            completed and events["loaded"] is True,
            "QWebEngine local-file control page failed; runtime="
            + repr(_runtime_provenance())
            + "; events="
            + repr(events),
        )
        value = _run_javascript(
            app,
            view.page(),
            "document.getElementById('ok').textContent",
        )
        _require(value == "ready", "QWebEngine control JavaScript failed")
        view.close()
        view.deleteLater()
        app.processEvents()
    print("QWEBENGINE_LOCAL_FILE_CONTROL: PASS")


def validate_real_qt(root: Path) -> None:
    """Run a bounded real-QWebEngine handshake and lifecycle test."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWidgets import QApplication, QPushButton
    except ImportError as exc:
        raise AssertionError("PySide6 QtWebEngine import failed: " + str(exc)) from exc
    del QWebEngineView
    if QApplication.instance() is None:
        QCoreApplication.setAttribute(
            Qt.ApplicationAttribute.AA_ShareOpenGLContexts,
            True,
        )
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer import (
        ProjectStructure3DWidget,
    )

    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    _validate_qwebengine_control(app)
    widget = ProjectStructure3DWidget()
    browser_button = widget.findChild(
        QPushButton,
        "projectStructure3DOpenBrowser",
    )
    if browser_button is not None:
        browser_button.setEnabled(False)
    widget.resize(1100, 720)
    widget.show()

    ready = _wait_until(app, lambda: bool(widget._renderer_ready), 45.0)
    _require(
        ready,
        "real QWebEngine renderer did not become ready; "
        + _qt_diagnostic(widget, app),
    )
    _require(widget._page_load_ok is True, "real QWebEngine page did not load")

    old_generation = widget._generation_id
    widget.set_project_root(Path("E:/kanda_reasoner_validation_fixture"))
    _require(
        _wait_until(app, lambda: bool(widget._renderer_ready), 45.0),
        "renderer did not reconnect after Project switch; "
        + _qt_diagnostic(widget, app),
    )
    widget._on_node_selected(old_generation, "module:tool_specs")
    _require(
        "tool_specs.py" not in widget.details.toPlainText(),
        "stale generation changed current details",
    )
    found = _run_javascript(
        app,
        widget._web_view.page(),
        "window.kandaProjectGraph.focusByQuery('tool_specs.py')",
    )
    _require(bool(found), "real renderer search did not find tool_specs.py")
    _require(
        _wait_until(
            app,
            lambda: "tool_specs.py" in widget.details.toPlainText(),
            8.0,
        ),
        "real QWebChannel selection did not reach Python details",
    )
    bridge = widget._bridge_bundle.bridge
    current_generation = widget._generation_id
    widget.close()
    bridge.node_selected.emit(current_generation, "module:tool_specs")
    app.processEvents()
    widget.deleteLater()
    app.processEvents()
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("REAL_QT_PROJECT_STRUCTURE_3D: PASS")


def validate_static(root: Path) -> None:
    """Run all source-only gates."""
    validate_registry(root)
    validate_source_modules(root)
    validate_graph_contract(root)
    validate_web_contract(root)
    validate_javascript(root)


def main() -> int:
    """Run selected v1A revision 2 validation gates."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    _require(
        not (args.static_only and args.real_qt_only),
        "validation modes are mutually exclusive",
    )
    root = Path(args.root).expanduser().resolve()
    if not args.real_qt_only:
        validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
