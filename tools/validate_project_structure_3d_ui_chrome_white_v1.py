# project-path: tools/validate_project_structure_3d_ui_chrome_white_v1.py
"""Validate the scoped Project Structure 3D UI-chrome contrast patch."""

from __future__ import annotations

import argparse
import ast
import hashlib
import sys
from pathlib import Path

FEATURE_ID = "project-structure-3d-visualizer-v1b-ui-chrome-white-v1"
TAB_PATH = (
    "kanda_reasoner_app/project_structure_visualizer/"
    "project_structure_3d_tab.py"
)
CSS_PATH = (
    "kanda_reasoner_app/project_structure_visualizer/web/graph_theme.css"
)
DETAILS_PATH = (
    "kanda_reasoner_app/project_structure_visualizer/details_presenter.py"
)
RENDERER_PATH = (
    "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js"
)
EXPECTED_UNCHANGED_HASHES = {
    DETAILS_PATH: "fc77d2364cb95c0e81328318a2f1c3b2efd174af09fc4c91190916e57ba2a861",
    RENDERER_PATH: "582c4e68d97af8f299fa72456b2e5e25251b11439810cfcf72b656433f8b805a",
}


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def read_bytes(root: Path, relative_path: str) -> bytes:
    """Read one required source file as bytes."""
    path = root / relative_path
    require(path.is_file(), "missing required file: " + relative_path)
    return path.read_bytes()


def read_text(root: Path, relative_path: str) -> str:
    """Read one required UTF-8 source file."""
    return read_bytes(root, relative_path).decode("utf-8", errors="strict")


def sha256(root: Path, relative_path: str) -> str:
    """Return the SHA-256 of one required source file."""
    return hashlib.sha256(read_bytes(root, relative_path)).hexdigest()


def validate_scoped_python_contract(root: Path) -> None:
    """Validate white text only on PySide6 controls and external labels."""
    tab = read_text(root, TAB_PATH)
    ast.parse(tab, filename=TAB_PATH)
    require(tab.isascii(), "tab source must remain ASCII")
    require(len(tab.splitlines()) <= 500, "tab module exceeds 500 lines")
    required_tokens = (
        'from PySide6.QtGui import QColor, QPalette',
        'search_palette.setColor(QPalette.PlaceholderText, QColor("#ffffff"))',
        '"#projectStructure3DToolbar QLabel, "',
        '"#projectStructure3DToolbar QCheckBox, "',
        '"#projectStructure3DToolbar QComboBox, "',
        '"#projectStructure3DToolbar QLineEdit, "',
        '"#projectStructure3DToolbar QPushButton {color: #ffffff;}"',
        '"background: #0b1420; color: #ffffff;"',
        '"selection-background-color: #1f6fb2; selection-color: #ffffff;}"',
        '"#projectStructure3DBadge {color: #ffffff; font-weight: 700;}"',
        '"#projectStructure3DStatus {color: #ffffff; padding: 2px 6px;}"',
    )
    for token in required_tokens:
        require(token in tab, "missing UI-chrome white-text contract: " + token)
    require(
        '"background: #0b1420; color: #e8f1fa; border: 1px solid #273b4e;"'
        in tab,
        "details pane color was changed outside the approved scope",
    )
    require(
        "#projectStructure3DWidget {color: #ffffff;}" not in tab,
        "root-wide white text would affect node/detail surfaces",
    )
    print("PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_PYTHON: PASS")


def validate_scoped_web_contract(root: Path) -> None:
    """Validate only scene badge/help labels changed in browser styling."""
    css = read_text(root, CSS_PATH)
    require(
        ".scene-badge strong {\n  color: #ffffff;" in css,
        "scene badge title is not white",
    )
    require(
        ".scene-badge span,\n.scene-help {\n  color: #ffffff;" in css,
        "scene badge/help labels are not white",
    )
    unchanged_tokens = (
        ":root {\n  color-scheme: dark;\n  font-family: Inter, \"Segoe UI\", Arial, sans-serif;\n  background: #07101c;\n  color: #eef4ff;",
        ".tooltip {",
        "  color: #f5f8ff;",
        ".eyebrow {\n  color: #56d6ff;",
        ".muted {\n  color: #91a9c3;",
        ".details-card dt {\n  color: #7e98b4;",
        "  color: #b8c9dc;",
    )
    for token in unchanged_tokens:
        require(token in css, "out-of-scope browser styling changed: " + token)
    print("PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_WEB: PASS")


def validate_node_and_details_unchanged(root: Path) -> None:
    """Prove node labels and details presenters remain byte-identical."""
    for relative_path, expected_hash in EXPECTED_UNCHANGED_HASHES.items():
        actual_hash = sha256(root, relative_path)
        require(
            actual_hash == expected_hash,
            "out-of-scope file changed: " + relative_path,
        )
    print("PROJECT_STRUCTURE_3D_NODE_AND_DETAILS_STYLING_UNCHANGED: PASS")


def validate_real_qt(root: Path) -> None:
    """Validate the scoped palette on the real PySide6 widget."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtGui import QColor, QPalette
        from PySide6.QtWidgets import QApplication, QComboBox, QLineEdit
    except ImportError as exc:
        raise AssertionError("PySide6 import failed: " + str(exc)) from exc
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
    widget = ProjectStructure3DWidget()
    widget.resize(1200, 760)
    widget.show()
    app.processEvents()
    style = widget.styleSheet().lower()
    require(
        "#projectstructure3dtoolbar qpushbutton {color: #ffffff;}" in style,
        "toolbar button text is not white",
    )
    require(
        "#projectstructure3dstatus {color: #ffffff;" in style,
        "status label text is not white",
    )
    require(
        "#projectstructure3ddetails {background: #0b1420; color: #e8f1fa;"
        in style,
        "details pane styling changed outside the approved scope",
    )
    search = widget.findChild(QLineEdit, "projectStructure3DSearch")
    require(search is not None, "search control missing")
    placeholder = search.palette().color(QPalette.PlaceholderText)
    require(placeholder == QColor("#ffffff"), "search placeholder is not white")
    combo = widget.findChild(QComboBox, "projectStructure3DViewMode")
    require(combo is not None, "view mode combo missing")
    require("qcombobox qabstractitemview" in style, "combo popup style missing")
    widget.close()
    widget.deleteLater()
    app.processEvents()
    print("REAL_QT_PROJECT_STRUCTURE_3D_UI_CHROME_WHITE: PASS")


def main() -> int:
    """Run static and optional real-Qt validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.real_qt_only:
        validate_real_qt(root)
    elif args.static_only:
        validate_scoped_python_contract(root)
        validate_scoped_web_contract(root)
        validate_node_and_details_unchanged(root)
    else:
        validate_scoped_python_contract(root)
        validate_scoped_web_contract(root)
        validate_node_and_details_unchanged(root)
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
