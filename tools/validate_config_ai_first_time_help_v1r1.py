"""Focused validator for the Config AI first-time Help feature."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "config-ai-first-time-help-v1r1"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a required UTF-8 file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate Config AI Help routing, content, layout, and images."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app = root / "kanda_reasoner_app"
    shell = app / "reasoner_tools_gui_shell"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    host = read_text(app / "reasoner_engine" / "config_ai_tab.py")
    web = read_text(app / "reasoner_engine" / "config_web_ai_tab.py")
    local = read_text(app / "reasoner_engine" / "config_local_ai_tab.py")
    source = read_text(help_root / "source" / "config_ai.md")
    html = read_text(help_root / "rendered" / "config_ai.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))
    fallback = json.loads(
        read_text(app / "reasoner_tools_gui_help" / "config_ai.json")
    )

    title_index = tool_specs.index('step_title="Config AI"')
    spec_start = tool_specs.rfind("ToolSpec(", 0, title_index)
    next_spec = tool_specs.find("\n    ToolSpec(", title_index)
    require(spec_start >= 0 and next_spec >= 0, "Config AI ToolSpec missing.")
    spec = tool_specs[spec_start:next_spec]
    require('help_catalog="config_ai.json"' in spec, "Config AI Help route missing.")
    require('tab_id="config_web_ai"' in spec, "Config AI tab ID changed.")
    print("CONFIG_AI_STANDARD_HELP_BUTTON: PASS")

    require('addTab(self.web_ai_tab, "Config Web AI")' in host, "Web sub-tab missing.")
    require('addTab(self.local_ai_tab, "Config Local AI")' in host, "Local sub-tab missing.")
    print("CONFIG_AI_REAL_SUBTABS: PASS")

    for marker in [
        'form.addRow("Gateway", self.gateway_combo)',
        'form.addRow("API key", key_row)',
        'form.addRow("Credential", self.credential_status)',
        'form.addRow("Model", self.model_combo)',
        'form.addRow("Catalog", catalog_row)',
        'form.addRow("Catalog status", self.catalog_status)',
        'form.addRow("Capabilities", self.capability_status)',
        'form.addRow("Privacy", self.privacy_status)',
    ]:
        require(marker in web, f"Web control missing: {marker}")
    print("CONFIG_AI_WEB_CONTROLS_GROUNDED: PASS")

    for marker in [
        'form.addRow("OpenAI-compatible base URL:", self.base_url_edit)',
        'form.addRow("Global Local AI model:", model_row)',
        'QPushButton("Refresh Local AI Models")',
        "Tool-versus-Project boundary:",
    ]:
        require(marker in local, f"Local control missing: {marker}")
    print("CONFIG_AI_LOCAL_CONTROLS_GROUNDED: PASS")

    page = next(
        (item for item in manifest.get("pages", []) if item.get("id") == "config_ai"),
        None,
    )
    require(page is not None, "Config AI manifest page missing.")
    require(page.get("tab_id") == "config_web_ai", "Manifest tab ID mismatch.")
    require(
        page.get("legacy_help_catalog") == "config_ai.json",
        "Fallback catalog mapping mismatch.",
    )
    print("CONFIG_AI_HELP_MANIFEST_REGISTRATION: PASS")

    for marker in [
        "First-Time User Tutorial",
        "What Config AI Means",
        "The Safest First-Time Workflow",
        "Config Web AI",
        "Config Local AI",
        "Tool-versus-Project Boundary",
        "Session Keys and Environment Keys",
        "First-Time Checklist",
        "Important Safety Boundary",
    ]:
        require(marker in source, f"Source marker missing: {marker}")
    print("CONFIG_AI_HELP_CANONICAL_SOURCE: PASS")

    for marker in [
        'class="book-page"',
        'class="chapter-opener"',
        "Config Web AI",
        "Config Local AI",
        "Tool-versus-Project Boundary",
        "Important Safety Boundary",
    ]:
        require(marker in html, f"HTML marker missing: {marker}")
    print("CONFIG_AI_HELP_FIRST_TIME_CONTENT: PASS")

    require(
        "border-top: 8px solid var(--orange-rule)" in css,
        "Orange top rule missing.",
    )
    require(
        "background: var(--blue-chapter)" in css,
        "Blue opener missing.",
    )
    require(
        "width: min(100%, 7in)" in css,
        "Centered page width missing.",
    )
    require("margin: 24px auto" in css, "Bilateral margin contract missing.")
    require("line-height: 1.36" in css, "Body line spacing missing.")
    print("CONFIG_AI_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local-file URL loading missing.")
    require("view.setUrl" in renderer, "QWebEngineView.setUrl missing.")
    require("QTextBrowser" in renderer, "QTextBrowser fallback missing.")
    print("CONFIG_AI_HELP_QWEBENGINE_PRIMARY: PASS")

    expected_assets = [
        "assets/drawings/config_ai_opener_global_controls.png",
        "assets/drawings/config_ai_web_configuration.png",
        "assets/drawings/config_ai_local_configuration.png",
        "assets/drawings/config_ai_tool_project_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        asset = help_root / relative
        require(asset.is_file(), f"Asset missing: {relative}")
        require(asset.stat().st_size > 100000, f"Asset too small: {relative}")
        filename = Path(relative).name
        require(filename in source, f"Source does not use asset: {filename}")
        require(filename in html, f"HTML does not use asset: {filename}")
    print("CONFIG_AI_CONTEXTUAL_CARTOON_IMAGES: PASS")

    require(fallback.get("tab") == "Config AI", "Fallback title mismatch.")

    lowered_html = html.lower()
    remote_resource_markers = (
        'src="http://',
        "src='http://",
        'src="https://',
        "src='https://",
        'href="http://',
        "href='http://",
        'href="https://',
        "href='https://",
    )
    for marker in remote_resource_markers:
        require(marker not in lowered_html, f"Remote resource found: {marker}")

    require(
        "http://127.0.0.1:11434/v1" in html,
        "Expected local base URL example is missing.",
    )
    print("CONFIG_AI_HELP_LOCAL_ONLY: PASS")
    print("CONFIG_AI_LOCAL_URL_EXAMPLE_ALLOWED: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
