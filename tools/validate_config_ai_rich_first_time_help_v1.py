# project-path: tools/validate_config_ai_rich_first_time_help_v1.py
"""Validate the rich, local-only first-time Config AI help page."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import hashlib
import struct
from pathlib import Path

FEATURE_ID = "config-ai-rich-first-time-help-v1"
HELP_ROOT_REL = Path("kanda_reasoner_app/reasoner_tools_gui_shell/help_docs")
ASSETS = (
    "assets/drawings/config_ai_opener_control_desk.png",
    "assets/drawings/config_ai_gateway_key_counter.png",
    "assets/drawings/config_ai_direct_provider_keyring.png",
    "assets/drawings/config_ai_local_home_workshop.png",
    "assets/drawings/config_ai_use_and_safety_bridge.png",
)


def require(condition: bool, marker: str, detail: str = "") -> None:
    """Raise one focused assertion or print one PASS marker."""
    if not condition:
        raise AssertionError(marker + (": " + detail if detail else ""))
    print(marker + ": PASS")


def read(path: Path) -> str:
    """Read one UTF-8 file."""
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate help content, assets, manifest, and runtime boundary."""
    help_root = root / HELP_ROOT_REL
    source_path = help_root / "source/config_ai.md"
    html_path = help_root / "rendered/config_ai.html"
    manifest_path = help_root / "manifest.json"
    css_path = help_root / "css/book_help.css"
    fallback_path = root / "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json"

    for path in (source_path, html_path, manifest_path, css_path, fallback_path):
        require(path.is_file(), "CONFIG_AI_HELP_FILE_PRESENT", str(path))

    source = read(source_path)
    html = read(html_path)
    manifest = json.loads(read(manifest_path))
    fallback = json.loads(read(fallback_path))

    require(len(source) >= 20_000, "CONFIG_AI_HELP_SOURCE_DETAILED")
    require(len(html) >= 24_000, "CONFIG_AI_HELP_RENDERED_DETAILED")
    fallback_text = "\n".join(str(item) for item in fallback.get("display_lines", []))
    require(len(fallback.get("display_lines", [])) >= 12, "CONFIG_AI_HELP_FALLBACK_DETAILED")
    require("Use Key / Load Environment" in fallback_text and "Web Advisory Config" in fallback_text, "CONFIG_AI_HELP_FALLBACK_ALIGNED")

    source_tokens = (
        "How To Use This",
        "Config Web AI: OpenRouter and Kilo",
        "OpenRouter setup",
        "Kilo AI Gateway setup",
        "Direct API Providers: the shared setup pattern",
        "Google Gemini API",
        "Mistral API Free Mode",
        "Qwen API Free Quota",
        "Groq API Free Plan",
        "Config Local AI",
        "Use Key / Load Environment",
        "Free access guard",
        "Refresh Approved Models",
        "Refresh Local AI Models",
        "Web Advisory Config",
        "Project Conversation",
        "429 RESOURCE_EXHAUSTED",
        "Tool-versus-Project boundary",
        "Further reading",
        "Validation rule",
    )
    for token in source_tokens:
        require(token in source, "CONFIG_AI_HELP_SOURCE_TOKEN", token)

    env_tokens = (
        "OPENROUTER_API_KEY",
        "KILO_API_KEY",
        "GEMINI_API_KEY",
        "MISTRAL_API_KEY",
        "DASHSCOPE_API_KEY",
        "GROQ_API_KEY",
    )
    for token in env_tokens:
        require(token in source and token in html, "CONFIG_AI_HELP_ENVIRONMENT_KEY", token)

    parity_tokens = (
        "OpenRouter",
        "Kilo AI Gateway",
        "Google Gemini API",
        "Mistral API Free Mode",
        "Qwen API Free Quota",
        "Groq API Free Plan",
        "OpenAI-compatible base URL",
        "Free models only",
        "Catalog status",
        "Capabilities",
        "Privacy",
        "Active Project",
        "API keys are secrets",
    )
    for token in parity_tokens:
        require(token in source and token in html, "CONFIG_AI_HELP_SOURCE_RENDERED_PARITY", token)

    config_page = None
    for page in manifest.get("pages", []):
        if isinstance(page, dict) and page.get("id") == "config_ai":
            config_page = page
            break
    require(config_page is not None, "CONFIG_AI_HELP_MANIFEST_PAGE")
    require(config_page.get("source") == "source/config_ai.md", "CONFIG_AI_HELP_MANIFEST_SOURCE")
    require(config_page.get("rendered") == "rendered/config_ai.html", "CONFIG_AI_HELP_MANIFEST_RENDERED")
    require(config_page.get("css") == "css/book_help.css", "CONFIG_AI_HELP_MANIFEST_CSS")
    require(tuple(config_page.get("assets", ())) == ASSETS, "CONFIG_AI_HELP_MANIFEST_ASSETS")

    expected_hashes = {
        "assets/drawings/config_ai_opener_control_desk.png": "ade6af9828f65cabc543d6b430bf30bf19886fa3b8289c9e291ca3127f6dd850",
        "assets/drawings/config_ai_gateway_key_counter.png": "3694ad80799658a4ac59c0f4d6b10c1e199a21239a3e5d62e5873cf0bee3ebe8",
        "assets/drawings/config_ai_direct_provider_keyring.png": "1dc47db0ef242ddc680c4f1945cbe22531101ff3f254b379246346da1de5fd06",
        "assets/drawings/config_ai_local_home_workshop.png": "3704450d3450ff1f3f121e7e57814b1f869d6fd556936c8c7c7ffb9f801c29b5",
        "assets/drawings/config_ai_use_and_safety_bridge.png": "a3978ce1d21b4fd97e2d4473c4ec22bc6c774153845b39e3623fe0faf183527a",
    }
    for relative in ASSETS:
        asset = help_root / relative
        require(asset.is_file(), "CONFIG_AI_HELP_ASSET_PRESENT", relative)
        raw = asset.read_bytes()
        require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "CONFIG_AI_HELP_ASSET_PNG", relative)
        width, height = struct.unpack(">II", raw[16:24])
        require((width, height) == (1448, 1086), "CONFIG_AI_HELP_ASSET_DIMENSIONS", relative)
        require(hashlib.sha256(raw).hexdigest() == expected_hashes[relative], "CONFIG_AI_HELP_ASSET_EXACT_UPLOAD", relative)
        require(relative in source, "CONFIG_AI_HELP_ARTWORK_METADATA", relative)
        require(("../" + relative) in html, "CONFIG_AI_HELP_RENDERED_ARTWORK", relative)
    require("config_ai_opener_control_desk.svg" not in source and "config_ai_opener_control_desk.svg" not in html, "CONFIG_AI_HELP_OLD_SVG_REFERENCES_ABSENT")

    require("../css/book_help.css" in html, "CONFIG_AI_HELP_BOOK_CSS")
    require("chapter-opener" in html and "chapter-drawing" in html and "section-drawing" in html, "CONFIG_AI_HELP_CANONICAL_LAYOUT")
    require("callout-note" in html and "callout-warning" in html, "CONFIG_AI_HELP_CALLOUTS")
    require("<script" not in html.lower(), "CONFIG_AI_HELP_NO_SCRIPT")
    external_attr = re.findall(r'''(?:src|href)=["']([^"']+)["']''', html, flags=re.I)
    require(all(not value.lower().startswith(("http://", "https://", "//")) for value in external_attr), "CONFIG_AI_HELP_LOCAL_ONLY_RESOURCES")
    require("fonts.googleapis" not in html.lower() and "cdn." not in html.lower(), "CONFIG_AI_HELP_NO_REMOTE_FONT_OR_CDN")

    runtime_paths = {
        "config_ai_tab": root / "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",
        "config_web_ai_tab": root / "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",
        "config_direct_web_ai_tab": root / "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",
        "config_local_ai_tab": root / "kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py",
    }
    runtime = {name: read(path) for name, path in runtime_paths.items()}
    require('addTab(self.web_ai_tab, "Config Web AI")' in runtime["config_ai_tab"], "CONFIG_AI_RUNTIME_GATEWAY_TAB_PRESERVED")
    require('addTab(self.direct_web_ai_tab, "Direct API Providers")' in runtime["config_ai_tab"], "CONFIG_AI_RUNTIME_DIRECT_TAB_PRESERVED")
    require('addTab(self.local_ai_tab, "Config Local AI")' in runtime["config_ai_tab"], "CONFIG_AI_RUNTIME_LOCAL_TAB_PRESERVED")
    require("Use Key / Load Environment" in runtime["config_web_ai_tab"] and "Refresh Models" in runtime["config_web_ai_tab"], "CONFIG_AI_RUNTIME_GATEWAY_CONTROLS_PRESERVED")
    require("Use Key / Load Environment" in runtime["config_direct_web_ai_tab"] and "Refresh Approved Models" in runtime["config_direct_web_ai_tab"], "CONFIG_AI_RUNTIME_DIRECT_CONTROLS_PRESERVED")
    require("Refresh Local AI Models" in runtime["config_local_ai_tab"], "CONFIG_AI_RUNTIME_LOCAL_CONTROLS_PRESERVED")
    require("open_configuration_requested" in runtime["config_ai_tab"], "CONFIG_AI_RUNTIME_SHARED_OWNER_PRESERVED")
    print("CONFIG_AI_HELP_PRESENTATION_ONLY_BOUNDARY: PASS")
    print("MCARD APPLICABILITY: NOT_APPLICABLE")


def _is_missing_pyside6_dependency(exc: ImportError) -> bool:
    """Return True only for an unavailable PySide6 or shiboken6 dependency."""
    module_name = str(getattr(exc, "name", "") or "")
    message = str(exc)
    return (
        module_name == "PySide6"
        or module_name.startswith("PySide6.")
        or module_name == "shiboken6"
        or module_name.startswith("shiboken6.")
        or "PySide6" in message
        or "shiboken6" in message
    )


def validate_real_qt(root: Path) -> bool:
    """Resolve the page and confirm Config AI's existing tab composition in Qt."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        if not _is_missing_pyside6_dependency(exc):
            raise
        print("CONFIG_AI_HELP_REAL_QT: SKIP (" + exc.__class__.__name__ + ")")
        return False

    from kanda_reasoner_app.reasoner_engine.config_ai_tab import ConfigAITab
    from kanda_reasoner_app.reasoner_tools_gui_shell.help_docs.path_resolver import (
        find_page_by_legacy_catalog,
    )

    app = QApplication.instance() or QApplication([])
    widget = ConfigAITab()
    labels = tuple(widget.subtabs.tabText(index) for index in range(widget.subtabs.count()))
    require(labels == ("Config Web AI", "Direct API Providers", "Config Local AI"), "CONFIG_AI_HELP_REAL_QT_THREE_SUBTABS")
    page = find_page_by_legacy_catalog("config_ai.json")
    require(page is not None, "CONFIG_AI_HELP_REAL_QT_PAGE_RESOLVED")
    require(page.rendered_path.is_file() and page.css_path.is_file(), "CONFIG_AI_HELP_REAL_QT_RENDERED_READY")
    require(len(page.asset_paths) == 5 and all(path.is_file() for path in page.asset_paths), "CONFIG_AI_HELP_REAL_QT_ASSETS_READY")
    widget.close()
    widget.deleteLater()
    app.processEvents()
    print("CONFIG_AI_HELP_REAL_QT: PASS")
    return True


def main() -> int:
    """Run the focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", "--project-root", dest="root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        validate_static(root)
        validate_real_qt(root)
        print("VALIDATION OK: " + FEATURE_ID)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
