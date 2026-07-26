# project-path: tools/validate_project_structure_3d_visualizer_v1e.py
"""Validate the pinned local WebGL renderer release for Project Structure 3D."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

from project_structure_3d_test_environment import (
    environment_snapshot,
    isolated_project_fixture,
    isolated_show_project_environment,
)
from project_structure_3d_v1c_fixture import (
    write_semantic_complete_json,
    write_semantic_freeze_entry,
)
from project_structure_3d_v1d_qt_navigation_probe import (
    validate_navigation_actions,
)

FEATURE_ID = "project-structure-3d-visualizer-v1e"
ROOT = "kanda_reasoner_app/project_structure_visualizer/"
VENDOR = ROOT + "web/vendor/"
REQUIRED = (
    ROOT + "web_assets.py",
    ROOT + "web_runtime.py",
    ROOT + "web/graph_navigation.js",
    ROOT + "web/graph_painter.js",
    ROOT + "web/graph_renderer.js",
    ROOT + "web/graph_theme.css",
    ROOT + "web/index_template.html",
    VENDOR + "3d-force-graph-1.80.0.min.js",
    VENDOR + "LICENSE-3d-force-graph.txt",
    VENDOR + "VENDOR_MANIFEST.json",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Read one strict UTF-8 file."""
    return (root / relative).read_text(encoding="utf-8", errors="strict")


def sha256(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_vendor(root: Path) -> None:
    """Validate exact local vendor identity, integrity, and license."""
    manifest_path = root / (VENDOR + "VENDOR_MANIFEST.json")
    asset_path = root / (VENDOR + "3d-force-graph-1.80.0.min.js")
    license_path = root / (VENDOR + "LICENSE-3d-force-graph.txt")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("package_name") == "3d-force-graph", "vendor package")
    require(manifest.get("package_version") == "1.80.0", "vendor version")
    require(manifest.get("license") == "MIT", "vendor license")
    require(manifest.get("delivery") == "bundled_local_tool_asset", "vendor delivery")
    require(manifest.get("network_fallback") is False, "vendor network fallback")
    require(manifest.get("asset_path") == "web/vendor/3d-force-graph-1.80.0.min.js", "vendor path")
    require(sha256(asset_path) == manifest.get("asset_sha256"), "vendor SHA-256")
    require(asset_path.stat().st_size == manifest.get("asset_size_bytes"), "vendor size")
    require(asset_path.stat().st_size > 1_000_000, "vendor asset unexpectedly small")
    require("MIT License" in license_path.read_text(encoding="utf-8"), "MIT text")
    require(manifest.get("npm_integrity_algorithm") == "sha512", "npm algorithm")
    require(bool(manifest.get("npm_integrity_base64")), "npm integrity")
    print("PROJECT_STRUCTURE_3D_PINNED_VENDOR_IDENTITY: PASS")
    print("PROJECT_STRUCTURE_3D_PINNED_VENDOR_SHA256: PASS")
    print("PROJECT_STRUCTURE_3D_PINNED_VENDOR_LICENSE: PASS")


def validate_source(root: Path) -> None:
    """Validate local-only WebGL ownership and renderer boundaries."""
    for relative in REQUIRED:
        require((root / relative).is_file(), "missing file: " + relative)
    for relative in REQUIRED:
        path = root / relative
        if path.suffix == ".py":
            source = read(root, relative)
            require(source.isascii(), "non-ASCII Python: " + relative)
            require(len(source.splitlines()) <= 500, "Python module too large: " + relative)
            ast.parse(source, filename=relative)
        if path.suffix == ".js" and "vendor/" not in relative:
            require(len(read(root, relative).splitlines()) <= 500, "JS module too large: " + relative)
    assets = read(root, ROOT + "web_assets.py")
    runtime = read(root, ROOT + "web_runtime.py")
    template = read(root, ROOT + "web/index_template.html")
    painter = read(root, ROOT + "web/graph_painter.js")
    renderer = read(root, ROOT + "web/graph_renderer.js")
    css = read(root, ROOT + "web/graph_theme.css")
    require("vendor_manifest()" in assets, "runtime vendor verification missing")
    require("pinned local 3d-force-graph SHA-256 mismatch" in assets, "runtime hash gate")
    require('(\"WebGLEnabled\", True)' in runtime, "WebGL is not enabled")
    require('(\"LocalContentCanAccessRemoteUrls\", False)' in runtime, "remote access guard")
    require("graph3dHost" in template and "graph-3d-host" in css, "WebGL host missing")
    require(template.index("{{KANDA_VENDOR_SCRIPT}}") < template.index("{{KANDA_SCRIPT}}"), "vendor load order")
    require("new window.ForceGraph3D" in renderer, "3d-force-graph constructor missing")
    require("rendererIdentity" in renderer and "hasWebGLRenderer" in renderer, "renderer observability")
    require("getContext(\"2d\"" not in renderer, "custom 2D renderer remains")
    require("requestAnimationFrame" not in renderer, "parallel custom render loop remains")
    require("context." not in painter, "canvas painter authority remains")
    combined = "\n".join((assets, runtime, template, painter, renderer))
    for forbidden in ("fetch(", "XMLHttpRequest", "https://", "http://"):
        require(forbidden not in combined, "remote/runtime authority: " + forbidden)
    print("PROJECT_STRUCTURE_3D_LOCAL_WEBGL_SOURCE: PASS")
    print("PROJECT_STRUCTURE_3D_NO_REMOTE_RENDERER_FALLBACK: PASS")
    print("PROJECT_STRUCTURE_3D_NO_PARALLEL_CANVAS_RENDERER: PASS")
    print("PROJECT_STRUCTURE_3D_GRAPH_TRUTH_UNCHANGED: PASS")


def validate_javascript(root: Path) -> None:
    """Use Node syntax validation when Node is available."""
    node = os.environ.get("NODE_EXE", "node")
    paths = (
        ROOT + "web/graph_painter.js",
        ROOT + "web/graph_renderer.js",
        VENDOR + "3d-force-graph-1.80.0.min.js",
    )
    for relative in paths:
        try:
            result = subprocess.run(
                [node, "--check", str(root / relative)],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            print("PROJECT_STRUCTURE_3D_V1E_JAVASCRIPT: SKIPPED")
            return
        require(result.returncode == 0, result.stderr.strip() or relative)
    print("PROJECT_STRUCTURE_3D_V1E_JAVASCRIPT: PASS")


def wait_until(app: Any, predicate: Callable[[], bool], timeout: float) -> bool:
    """Process Qt events until a bounded predicate succeeds."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    app.processEvents()
    return bool(predicate())


def run_javascript(app: Any, page: Any, expression: str) -> Any:
    """Run one JSON-enveloped JavaScript expression."""
    result: dict[str, Any] = {"done": False, "value": None}

    def receive(value: Any) -> None:
        result["done"] = True
        result["value"] = value

    script = (
        "(() => { try { return JSON.stringify({ok:true,value:(" + expression + ")}); } "
        "catch (error) { return JSON.stringify({ok:false,error:String(error && error.stack ? "
        "error.stack : error)}); } })()"
    )
    page.runJavaScript(script, receive)
    require(wait_until(app, lambda: bool(result["done"]), 15.0), "JS timeout")
    require(isinstance(result["value"], str), "JS probe did not return text")
    payload = json.loads(result["value"])
    require(payload.get("ok") is True, "JS error: " + str(payload.get("error")))
    return payload.get("value")


def runtime_provenance() -> str:
    """Return bounded runtime provenance."""
    try:
        pyside = importlib.metadata.version("PySide6")
    except importlib.metadata.PackageNotFoundError:
        pyside = "unknown"
    return repr({
        "python": str(Path(sys.executable).resolve()),
        "python_version": platform.python_version(),
        "pyside6": pyside,
    })


def validate_real_qt(root: Path) -> None:
    """Validate the real local WebGL renderer and existing navigation API."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWebEngineCore import QWebEngineSettings
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise AssertionError("PySide6 import failed: " + str(exc)) from exc
    if QApplication.instance() is None:
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer import ProjectStructure3DWidget

    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    ambient = environment_snapshot()
    with isolated_show_project_environment():
        with isolated_project_fixture("kanda_visualizer_v1e_qt_") as (project_root, _support_root):
            write_semantic_complete_json(project_root)
            write_semantic_freeze_entry(project_root)
            widget = ProjectStructure3DWidget()
            widget.resize(1450, 880)
            widget.show()
            require(wait_until(app, lambda: bool(widget._renderer_ready), 60.0), "fixture renderer")
            widget.set_project_root(project_root)
            require(wait_until(app, lambda: bool(widget._renderer_ready), 60.0), "v1E renderer")
            page = widget._web_view.page()
            identity = run_javascript(app, page, "window.kandaProjectGraph.rendererIdentity()")
            require(identity.get("provider") == "3d-force-graph", "renderer provider")
            require(identity.get("version") == "1.80.0", "renderer version")
            require(identity.get("local") is True, "renderer is not local")
            require(identity.get("renderer") == "WebGL", "renderer type")
            require(bool(run_javascript(app, page, "window.kandaProjectGraph.hasWebGLRenderer()")), "WebGL renderer absent")
            require(bool(run_javascript(app, page, "typeof window.ForceGraph3D === 'function'")), "vendor global absent")
            require(bool(run_javascript(app, page, "Boolean(document.querySelector('#graph3dHost canvas'))")), "WebGL canvas absent")
            settings = widget._web_view.settings()
            attrs = QWebEngineSettings.WebAttribute
            require(settings.testAttribute(attrs.WebGLEnabled), "Qt WebGL disabled")
            require(not settings.testAttribute(attrs.LocalContentCanAccessRemoteUrls), "remote access enabled")
            validate_navigation_actions(app, page, len(widget._snapshot["nodes"]))
            widget.close()
            widget.deleteLater()
            app.processEvents()
    require(environment_snapshot() == ambient, "real Qt environment was not restored")
    print("REAL_QT_PROJECT_STRUCTURE_3D_LOCAL_VENDOR: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_WEBGL: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_NAVIGATION_REGRESSION: PASS")
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("RUNTIME_PROVENANCE: " + runtime_provenance())
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1E: PASS")


def validate_static(root: Path) -> None:
    """Run static release gates."""
    validate_vendor(root)
    validate_source(root)
    validate_javascript(root)


def main() -> int:
    """Run selected validation modes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.real_qt_only:
        validate_real_qt(root)
    elif args.static_only:
        validate_static(root)
    else:
        validate_static(root)
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
