# project-path: tools/validate_project_structure_3d_ui_chrome_white_v1r1.py
"""Validate the Project Structure 3D UI-chrome white-text r1 correction."""

from __future__ import annotations

import argparse
import ast
import hashlib
import sys
from pathlib import Path

FEATURE_ID = "project-structure-3d-visualizer-v1b-ui-chrome-white-v1r1"
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
    CSS_PATH: "408d52a9eedded81f1e287b486335a52e56421a38cd787bfcccc40a7ccf78193",
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


def version_tuple(value: str) -> tuple[int, ...]:
    """Convert one dotted version into a comparable integer tuple."""
    parts: list[int] = []
    for token in value.split("."):
        digits = "".join(character for character in token if character.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def validate_static_contract(root: Path) -> None:
    """Validate direct QSS ownership and preserved visual boundaries."""
    tab = read_text(root, TAB_PATH)
    ast.parse(tab, filename=TAB_PATH)
    require(tab.isascii(), "tab source must remain ASCII")
    require(len(tab.splitlines()) <= 500, "tab module exceeds 500 lines")
    required_tokens = (
        '"#projectStructure3DToolbar QPushButton {color: #ffffff;}"',
        '"#projectStructure3DSearch {color: #ffffff; "',
        '"placeholder-text-color: #ffffff;}"',
        '"#projectStructure3DStatus {color: #ffffff; padding: 2px 6px;}"',
        '"#projectStructure3DDetails {"',
        '"background: #0b1420; color: #e8f1fa; border: 1px solid #273b4e;"',
    )
    for token in required_tokens:
        require(token in tab, "missing scoped UI contract: " + token)
    require(
        "#projectStructure3DWidget {color: #ffffff;}" not in tab,
        "root-wide white text would affect node/detail surfaces",
    )
    for relative_path, expected_hash in EXPECTED_UNCHANGED_HASHES.items():
        require(
            sha256(root, relative_path) == expected_hash,
            "out-of-scope presentation file changed: " + relative_path,
        )
    print("PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_R1_STATIC: PASS")
    print("PROJECT_STRUCTURE_3D_NODE_AND_DETAILS_STYLING_UNCHANGED: PASS")


def validate_real_qt(root: Path) -> None:
    """Validate the durable QSS contract on the real PySide6 widget."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt, qVersion
        from PySide6.QtWidgets import QApplication, QComboBox, QLineEdit
    except ImportError as exc:
        raise AssertionError("PySide6 import failed: " + str(exc)) from exc

    require(
        version_tuple(qVersion()) >= (6, 5),
        "Qt 6.5 or newer is required for placeholder-text-color",
    )
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

    style = widget.styleSheet().lower().replace("\n", "")
    require(
        "#projectstructure3dsearch {color: #ffffff; "
        "placeholder-text-color: #ffffff;}" in style,
        "search placeholder direct QSS contract is missing",
    )
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
        "details pane styling changed outside approved scope",
    )
    search = widget.findChild(QLineEdit, "projectStructure3DSearch")
    require(search is not None, "search control missing")
    require(bool(search.placeholderText()), "search placeholder text missing")
    combo = widget.findChild(QComboBox, "projectStructure3DViewMode")
    require(combo is not None, "view mode combo missing")
    require("qcombobox qabstractitemview" in style, "combo popup style missing")

    widget.close()
    widget.deleteLater()
    app.processEvents()
    print("QT_PLACEHOLDER_DIRECT_QSS_CONTRACT: PASS")
    print("QT_PLACEHOLDER_PALETTE_RIGIDITY_AVOIDED: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_R1: PASS")


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
        validate_static_contract(root)
    else:
        validate_static_contract(root)
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
