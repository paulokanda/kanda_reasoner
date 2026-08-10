"""Validate the Kanda Phrasebook help page and Prompt Library button."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


FEATURE_ID = "kanda-phrasebook-help-and-prompt-library-button-v1"
EXPECTED_PROMPT_COUNT = 310
EXPECTED_ASSETS = (
    "assets/drawings/kanda_phrasebook_opener.png",
    "assets/drawings/kanda_phrasebook_choose_prompt.png",
    "assets/drawings/kanda_phrasebook_tool_project_boundary.png",
    "assets/drawings/kanda_phrasebook_box_logic_repair.png",
    "assets/drawings/kanda_phrasebook_validation.png",
    "assets/drawings/kanda_phrasebook_freeze.png",
)


class StrictHTMLParser(HTMLParser):
    """Track basic HTML document structure without external dependencies."""

    def __init__(self) -> None:
        """Initialize document counters."""
        super().__init__()
        self.html_count = 0
        self.body_count = 0
        self.details_count = 0
        self.summary_count = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        """Count required structural elements."""
        del attrs
        if tag == "html":
            self.html_count += 1
        elif tag == "body":
            self.body_count += 1
        elif tag == "details":
            self.details_count += 1
        elif tag == "summary":
            self.summary_count += 1


def require(condition: bool, message: str) -> None:
    """Raise a focused validation error when a contract is missing."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read one required UTF-8 text file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def validate_button(tab_text: str) -> None:
    """Validate the far-right Prompt Library Phrasebook button contract."""
    button_marker = 'self.kanda_phrasebook_button = QPushButton("Kanda Phrasebook")'
    stretch_marker = "button_row.addStretch(1)"
    add_marker = "button_row.addWidget(self.kanda_phrasebook_button)"
    require(button_marker in tab_text, "Kanda Phrasebook button is missing.")
    require(stretch_marker in tab_text, "Button-row stretch is missing.")
    require(add_marker in tab_text, "Kanda Phrasebook button is not added.")
    require(
        tab_text.index(stretch_marker) < tab_text.index(add_marker),
        "Kanda Phrasebook button is not positioned after the stretch.",
    )
    for marker in (
        "self._open_kanda_phrasebook",
        '"kanda_phrasebook.json"',
        'window_title="Help - Kanda Phrasebook"',
        "open_help_document_for_legacy_catalog",
    ):
        require(marker in tab_text, f"Button route is missing: {marker}")
    print("KANDA_PHRASEBOOK_FAR_RIGHT_BUTTON: PASS")
    print("KANDA_PHRASEBOOK_CANONICAL_HELP_ROUTE: PASS")


def validate_manifest(help_root: Path, manifest: dict) -> None:
    """Validate manifest registration and local asset ownership."""
    page = next(
        (
            item
            for item in manifest.get("pages", [])
            if item.get("id") == "kanda_phrasebook"
        ),
        None,
    )
    require(page is not None, "Kanda Phrasebook manifest page is missing.")
    require(page.get("tab_id") == "prompt_library", "Manifest tab mismatch.")
    require(
        page.get("legacy_help_catalog") == "kanda_phrasebook.json",
        "Manifest catalog mapping mismatch.",
    )
    require(
        tuple(page.get("assets", [])) == EXPECTED_ASSETS,
        "Manifest asset inventory mismatch.",
    )
    for relative in EXPECTED_ASSETS:
        asset = help_root / relative
        require(asset.is_file(), f"Missing Phrasebook image: {relative}")
        require(asset.stat().st_size > 100000, f"Phrasebook image too small: {relative}")
        require(asset.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"Not a PNG: {relative}")
    print("KANDA_PHRASEBOOK_HELP_MANIFEST: PASS")
    print("KANDA_PHRASEBOOK_LOCAL_IMAGE_INVENTORY: PASS")


def validate_content(source: str, rendered: str, css: str) -> None:
    """Validate full explained Phrasebook content and exact layout markers."""
    for marker in (
        "Kanda Phrasebook",
        "Mini-Prompts for Safer AI Coding",
        "What This Help File Is",
        "How to Use the Phrasebook",
        "Important Placeholders",
        "Quick Section Map",
        "A. Universal Prefixes",
        "E. Tool Versus Active Project Boundary",
        "F. Box Architecture And Public Contracts",
        "L. Testing And Validation",
        "N. Freeze And Error Memory",
        "T. One-Line Command Deck",
        'id="a3"',
        "Surgical repair prefix",
        "Plain-English explanation",
    ):
        require(marker in source, f"Source marker missing: {marker}")

    prompt_ids = re.findall(
        r'<details class="prompt-card" id="([a-t]\d+)">',
        rendered,
    )
    require(
        len(prompt_ids) == EXPECTED_PROMPT_COUNT,
        f"Expected {EXPECTED_PROMPT_COUNT} prompt cards, found {len(prompt_ids)}.",
    )
    require(len(set(prompt_ids)) == EXPECTED_PROMPT_COUNT, "Duplicate prompt card IDs.")
    for required_id in ("a1", "a5", "b1", "e18", "n18", "t1", "t40"):
        require(required_id in prompt_ids, f"Prompt card missing: {required_id}")

    parser = StrictHTMLParser()
    parser.feed(rendered)
    require(parser.html_count == 1, "HTML root count mismatch.")
    require(parser.body_count == 1, "Body count mismatch.")
    require(
        parser.details_count == EXPECTED_PROMPT_COUNT,
        "Rendered details count mismatch.",
    )
    require(
        parser.summary_count == EXPECTED_PROMPT_COUNT,
        "Rendered summary count mismatch.",
    )

    for marker in (
        'class="book-page phrasebook-page"',
        'class="chapter-opener"',
        'class="phrasebook-index"',
        'class="phrasebook-card-list"',
        "Plain-English explanation",
        "310 Explained Mini-Prompts",
    ):
        require(marker in rendered, f"Rendered marker missing: {marker}")

    for marker in (
        ".phrasebook-index",
        ".prompt-card",
        ".prompt-card[open]",
        ".prompt-card summary",
        ".prompt-code",
        ".back-to-map",
    ):
        require(marker in css, f"Phrasebook CSS marker missing: {marker}")

    lowered = rendered.lower()
    for remote_marker in (
        'src="http://',
        "src='http://",
        'src="https://',
        "src='https://",
        'href="http://',
        "href='http://",
        'href="https://',
        "href='https://",
    ):
        require(remote_marker not in lowered, f"Remote dependency found: {remote_marker}")
    print("KANDA_PHRASEBOOK_310_EXPLAINED_MINI_PROMPTS: PASS")
    print("KANDA_PHRASEBOOK_BOOK_LAYOUT: PASS")
    print("KANDA_PHRASEBOOK_LOCAL_ONLY: PASS")


def validate_runtime_import(root: Path, *, require_qt_smoke: bool) -> None:
    """Validate manifest resolution and offscreen Prompt Library construction."""
    sys.path.insert(0, str(root))
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    from kanda_reasoner_app.reasoner_tools_gui_shell.help_docs.path_resolver import (
        find_page_by_legacy_catalog,
    )

    page = find_page_by_legacy_catalog("kanda_phrasebook.json")
    require(page is not None, "Runtime help-page resolution failed.")
    require(page.rendered_path.is_file(), "Runtime rendered page is missing.")
    require(page.source_path.is_file(), "Runtime source page is missing.")

    print("KANDA_PHRASEBOOK_RUNTIME_MANIFEST_RESOLUTION: PASS")

    try:
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.prompt_library_gui.prompt_library_tab import (
            PromptLibraryTab,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "PySide6":
            if require_qt_smoke:
                raise AssertionError(
                    "PySide6 is required for the target-environment button smoke."
                ) from exc
            print(
                "KANDA_PHRASEBOOK_OFFSCREEN_BUTTON_SMOKE: NOT_RUN "
                "(PySide6 unavailable in this environment)"
            )
            return
        raise
    except Exception as exc:
        raise AssertionError(f"Prompt Library runtime import failed: {exc}") from exc

    app = QApplication.instance() or QApplication([])
    widget = PromptLibraryTab()
    widget.resize(1200, 800)
    widget.show()
    app.processEvents()
    require(
        widget.kanda_phrasebook_button.text() == "Kanda Phrasebook",
        "Runtime Phrasebook button text mismatch.",
    )
    require(
        widget.kanda_phrasebook_button.x() > widget.prompt_library_help_button.x(),
        "Runtime Phrasebook button is not to the right of Help.",
    )
    widget.close()
    app.processEvents()
    print("KANDA_PHRASEBOOK_OFFSCREEN_BUTTON_SMOKE: PASS")


def main() -> int:
    """Run focused Phrasebook validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--require-qt-smoke", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app_root = root / "kanda_reasoner_app"
    help_root = app_root / "reasoner_tools_gui_shell/help_docs"

    tab_text = read_text(app_root / "prompt_library_gui/prompt_library_tab.py")
    source = read_text(help_root / "source/kanda_phrasebook.md")
    rendered = read_text(help_root / "rendered/kanda_phrasebook.html")
    css = read_text(help_root / "css/book_help.css")
    manifest = json.loads(read_text(help_root / "manifest.json"))
    catalog = json.loads(
        read_text(app_root / "reasoner_tools_gui_help/kanda_phrasebook.json")
    )

    validate_button(tab_text)
    validate_manifest(help_root, manifest)
    validate_content(source, rendered, css)
    require(catalog.get("tab") == "Kanda Phrasebook", "Fallback catalog mismatch.")
    print("KANDA_PHRASEBOOK_TEXT_FALLBACK: PASS")
    validate_runtime_import(root, require_qt_smoke=args.require_qt_smoke)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
