"""Focused validator for the Freeze Feature After Update first-time help."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

FEATURE_ID = "freeze-feature-after-update-first-time-help-v1"
SOURCE_REL = Path("kanda_reasoner_app/freeze_after_update_gui/help_source/freeze_feature_after_update_help.md")
HTML_REL = Path("kanda_reasoner_app/freeze_after_update_gui/freeze_feature_after_update_help.html")
ASSET_ROOT = Path("kanda_reasoner_app/freeze_after_update_gui/help_assets")
ASSETS = {
    "freeze_help_01_opener.png": "12d1e29aa1575ff0901126b39c41a0444764cdcdee1391ff65a3d767869762d2",
    "freeze_help_02_validation.png": "6855de2533d62891b87cb45b5e69e152f99aef429f2257d259906c6c21fd96f8",
    "freeze_help_03_paths.png": "29de435c057ac2700fd55cfa37a7889aca0da3da2bc4b7b7615f78dd80b87a40",
    "freeze_help_04_preview.png": "cf16d844eda06267ec18b5b2affa5fcbf66388732ed37870a225de97c2e530a3",
    "freeze_help_05_confirm.png": "fff96632f6fdd20435ceb631e6f25f86bee4abbe6fddfbc919abb7c6d65f89c5",
    "freeze_help_06_reminders.png": "b29e33a50594d54f70b2b3fd3ed9a4c6ab179e370f070a28ce7a8fc7d95ecaa5",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(text: str, phrases: list[str], label: str) -> None:
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        raise RuntimeError(f"{label} missing required content: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source_path = root / SOURCE_REL
    html_path = root / HTML_REL
    if not source_path.is_file() or not html_path.is_file():
        raise RuntimeError("Canonical Markdown source or rendered HTML is missing.")
    source = source_path.read_text(encoding="utf-8", errors="replace")
    html = html_path.read_text(encoding="utf-8", errors="replace")
    require(source, [
        "# Freeze Feature After Update",
        "## Recommended First-Time Workflow",
        "## Every Freeze Field Explained",
        "Preview does not write",
        "Confirm and Write Freeze Entry",
        "freeze_hint_intake",
        "frozen_features_memory",
        "must not be stored inside `project_freeze_ledger`",
    ], "SOURCE")
    require(html, [
        'class="chapter-opener"',
        'border-top:8px solid var(--orange)',
        'grid-template-columns:minmax(0,1fr) 2in',
        'font-family:"Minion Pro"',
        'font-family:"Myriad Pro Cond"',
        "Recommended First-Time Workflow",
        "Every Freeze Field Explained",
        "Preview Freeze Entry Is Read-Only",
        "Confirm and Write Is Final Human Authority",
        "{{IMG_OPENER}}",
        "{{IMG_VALIDATION}}",
        "{{IMG_PATHS}}",
        "{{IMG_PREVIEW}}",
        "{{IMG_CONFIRM}}",
        "{{IMG_REMINDERS}}",
    ], "HTML")
    for name, expected in ASSETS.items():
        path = root / ASSET_ROOT / name
        if not path.is_file():
            raise RuntimeError(f"Required unchanged help image is missing: {path}")
        actual = digest(path)
        if actual != expected:
            raise RuntimeError(f"Help image changed unexpectedly: {name}: {actual}")
    print("FREEZE_HELP_SOURCE: PASS")
    print("FREEZE_HELP_RENDERED_LAYOUT: PASS")
    print("FREEZE_HELP_FIRST_TIME_CONTENT: PASS")
    print("FREEZE_HELP_IMAGE_REUSE_UNCHANGED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
