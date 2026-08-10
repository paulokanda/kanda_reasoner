# project-path: tools/validate_config_ai_uploaded_png_artwork_v1.py
"""Validate exact reuse of the five user-uploaded Config AI illustrations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

FEATURE_ID = "config-ai-uploaded-png-artwork-v1"
HELP_ROOT_REL = Path("kanda_reasoner_app/reasoner_tools_gui_shell/help_docs")
ASSETS = {
    "assets/drawings/config_ai_opener_control_desk.png": "ade6af9828f65cabc543d6b430bf30bf19886fa3b8289c9e291ca3127f6dd850",
    "assets/drawings/config_ai_gateway_key_counter.png": "3694ad80799658a4ac59c0f4d6b10c1e199a21239a3e5d62e5873cf0bee3ebe8",
    "assets/drawings/config_ai_direct_provider_keyring.png": "1dc47db0ef242ddc680c4f1945cbe22531101ff3f254b379246346da1de5fd06",
    "assets/drawings/config_ai_local_home_workshop.png": "3704450d3450ff1f3f121e7e57814b1f869d6fd556936c8c7c7ffb9f801c29b5",
    "assets/drawings/config_ai_use_and_safety_bridge.png": "a3978ce1d21b4fd97e2d4473c4ec22bc6c774153845b39e3623fe0faf183527a"
}
OLD_NAMES = {
    "config_ai_opener_control_desk.png": "config_ai_opener_control_desk.svg",
    "config_ai_gateway_key_counter.png": "config_ai_gateway_key_counter.svg",
    "config_ai_direct_provider_keyring.png": "config_ai_direct_provider_keyring.svg",
    "config_ai_local_home_workshop.png": "config_ai_local_home_workshop.svg",
    "config_ai_use_and_safety_bridge.png": "config_ai_use_and_safety_bridge.svg"
}
SOURCE_VISIBLE_HASH = "7aa67194ba2d1de125c97905908d39f84b5713bf03850c07d02d00e26845e839"
HTML_VISIBLE_HASH = "8d5f9b71d548c416063ff33332787ac2f746b76e1c7bcb866a8718d196bb2353"
CONFIG_AI_FALLBACK_HASH = "dd03790ccd6d2617852d387e6b71c7f2f33404d6e0e50e070352907399147f1d"


def require(condition: bool, marker: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(marker + (": " + detail if detail else ""))
    print(marker + ": PASS")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_source(text: str) -> bytes:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for new_name, old_name in OLD_NAMES.items():
        text = text.replace(new_name, old_name)
    return text.encode("utf-8")


def normalized_html(text: str) -> bytes:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for new_name, old_name in OLD_NAMES.items():
        text = text.replace(new_name, old_name)
    return text.encode("utf-8")


def validate(root: Path) -> None:
    help_root = root / HELP_ROOT_REL
    source_path = help_root / "source/config_ai.md"
    html_path = help_root / "rendered/config_ai.html"
    manifest_path = help_root / "manifest.json"
    fallback_path = root / "kanda_reasoner_app/reasoner_tools_gui_help/config_ai.json"
    source = source_path.read_text(encoding="utf-8")
    html = html_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    require(sha256_bytes(normalized_source(source)) == SOURCE_VISIBLE_HASH, "CONFIG_AI_UPLOADED_PNG_SOURCE_TEXT_UNCHANGED")
    require(sha256_bytes(normalized_html(html)) == HTML_VISIBLE_HASH, "CONFIG_AI_UPLOADED_PNG_LAYOUT_TEXT_UNCHANGED")
    require(sha256_bytes(fallback_path.read_bytes()) == CONFIG_AI_FALLBACK_HASH, "CONFIG_AI_UPLOADED_PNG_FALLBACK_UNCHANGED")

    page = next((item for item in manifest.get("pages", []) if item.get("id") == "config_ai"), None)
    require(page is not None, "CONFIG_AI_UPLOADED_PNG_MANIFEST_PAGE")
    require(tuple(page.get("assets", ())) == tuple(ASSETS), "CONFIG_AI_UPLOADED_PNG_MANIFEST_EXACT")

    for relative, expected_hash in ASSETS.items():
        path = help_root / relative
        require(path.is_file(), "CONFIG_AI_UPLOADED_PNG_PRESENT", relative)
        raw = path.read_bytes()
        require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "CONFIG_AI_UPLOADED_PNG_SIGNATURE", relative)
        width, height = struct.unpack(">II", raw[16:24])
        require((width, height) == (1448, 1086), "CONFIG_AI_UPLOADED_PNG_DIMENSIONS", relative)
        require(sha256_bytes(raw) == expected_hash, "CONFIG_AI_UPLOADED_PNG_EXACT_BYTES", relative)
        require(relative in source and ("../" + relative) in html, "CONFIG_AI_UPLOADED_PNG_REFERENCED", relative)

    require("config_ai_opener_control_desk.svg" not in source, "CONFIG_AI_UPLOADED_PNG_SOURCE_SVG_ABSENT")
    require("config_ai_opener_control_desk.svg" not in html, "CONFIG_AI_UPLOADED_PNG_HTML_SVG_ABSENT")
    refs = re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", html, flags=re.I)
    require(all(not value.lower().startswith(("http://", "https://", "//")) for value in refs), "CONFIG_AI_UPLOADED_PNG_LOCAL_ONLY")
    print("CONFIG_AI_UPLOADED_PNG_PRESENTATION_ONLY_BOUNDARY: PASS")
    print("MCARD APPLICABILITY: NOT_APPLICABLE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", "--project-root", dest="root", required=True)
    args = parser.parse_args()
    try:
        validate(Path(args.root).expanduser().resolve())
        print("VALIDATION OK: " + FEATURE_ID)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
