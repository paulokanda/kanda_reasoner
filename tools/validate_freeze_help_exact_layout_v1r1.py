"""Validate the corrected Freeze help renderer and exact layout contract."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXPECTED_IMAGES = {
    "freeze_help_01_opener.png": "12d1e29aa1575ff0901126b39c41a0444764cdcdee1391ff65a3d767869762d2",
    "freeze_help_02_validation.png": "6855de2533d62891b87cb45b5e69e152f99aef429f2257d259906c6c21fd96f8",
    "freeze_help_03_paths.png": "29de435c057ac2700fd55cfa37a7889aca0da3da2bc4b7b7615f78dd80b87a40",
    "freeze_help_04_preview.png": "cf16d844eda06267ec18b5b2affa5fcbf66388732ed37870a225de97c2e530a3",
    "freeze_help_05_confirm.png": "fff96632f6fdd20435ceb631e6f25f86bee4abbe6fddfbc919abb7c6d65f89c5",
    "freeze_help_06_reminders.png": "b29e33a50594d54f70b2b3fd3ed9a4c6ab179e370f070a28ce7a8fc7d95ecaa5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    gui = root / "kanda_reasoner_app" / "freeze_after_update_gui"
    html_path = gui / "freeze_feature_after_update_help.html"
    source_path = gui / "help_source" / "freeze_feature_after_update_help.md"
    runtime_path = gui / "_freeze_memory_exports.py"
    require(html_path.is_file(), f"Missing help HTML: {html_path}")
    require(source_path.is_file(), f"Missing canonical help source: {source_path}")
    require(runtime_path.is_file(), f"Missing help runtime: {runtime_path}")
    html = html_path.read_text(encoding="utf-8")
    runtime = runtime_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8")

    layout_markers = [
        'border-top: 8px solid #ea580c !important',
        'background: #0f3460 !important',
        'width: 7in !important',
        'margin: 24px auto !important',
        'padding: 0.62in 0.66in 0.54in !important',
        'line-height: 1.36 !important',
        '<header class="chapter-opener">',
        '<h1>Freeze Feature After Update</h1>',
    ]
    for marker in layout_markers:
        require(marker in html, f"Missing exact-layout marker: {marker}")
    require("{{IMG_" not in html, "Unresolved image token remains in help HTML")
    for image_name in EXPECTED_IMAGES:
        require(f'help_assets/{image_name}' in html, f"HTML does not use relative asset: {image_name}")

    runtime_markers = [
        "from PySide6.QtWebEngineWidgets import QWebEngineView",
        "view.setUrl(QUrl.fromLocalFile(str(help_path)))",
        "from PySide6.QtWidgets import QTextBrowser",
        "browser.setSource(QUrl.fromLocalFile(str(help_path)))",
        "help_view = self._create_help_document_view()",
    ]
    for marker in runtime_markers:
        require(marker in runtime, f"Missing rich-renderer marker: {marker}")
    require("help_view.setHtml" not in runtime, "Legacy QTextEdit.setHtml path is still active")
    require("First-Time User" in source or "first-time" in source.lower(), "Canonical source lacks first-time-user framing")

    asset_root = gui / "help_assets"
    for name, expected_hash in EXPECTED_IMAGES.items():
        path = asset_root / name
        require(path.is_file(), f"Required unchanged image is missing: {path}")
        require(sha256(path) == expected_hash, f"Unexpected image content change: {name}")

    print("FREEZE_HELP_RED_TOP_RULE: PASS")
    print("FREEZE_HELP_BLUE_CHAPTER_OPENER: PASS")
    print("FREEZE_HELP_BILATERAL_PAGE_MARGINS: PASS")
    print("FREEZE_HELP_LINE_SPACING: PASS")
    print("FREEZE_HELP_QWEBENGINE_PRIMARY_RENDERER: PASS")
    print("FREEZE_HELP_TEXT_BROWSER_FALLBACK: PASS")
    print("FREEZE_HELP_IMAGE_REUSE_UNCHANGED: PASS")
    print("VALIDATION OK: freeze-feature-after-update-first-time-help-v1r1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
