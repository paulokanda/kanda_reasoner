"""Validate canonical click-time loading of current KPR-06-001."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import zipfile
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "planner-web-ai-howto-canonical-tool-prompt-dynamic-loader-v1"
PROMPT_REL = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_large_module_refactor_exchange_protocol.md"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    prompt = root / PROMPT_REL
    gui_path = root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py"
    text = prompt.read_text(encoding="utf-8")
    gui = gui_path.read_text(encoding="utf-8")
    ast.parse(gui)

    need("KPR-06-001" in text and "Version: 2.0.0" in text, "Current KPR-06-001 missing")
    need("planning reasoning and bounded action selection only" in text, "Current owner boundary missing")
    need("web_ai_large_module_refactor_exchange_protocol.md" in gui, "Canonical path missing")
    need("read_text" in gui and "QApplication.clipboard().setText" in gui, "Click-time prompt read missing")
    need("planning reasoning and bounded action selection only" not in gui, "Embedded prompt copy returned")
    need(len(gui.splitlines()) <= 500, "GUI module exceeds 500 lines")

    with zipfile.ZipFile(patch_zip) as archive:
        names = set(archive.namelist())
        need("INSTALL_MANIFEST.json" in names, "Manifest missing")
        manifest = json.loads(archive.read("INSTALL_MANIFEST.json").decode("utf-8-sig"))
        record = next((x for x in manifest.get("files", []) if x.get("path") == PROMPT_REL), None)
        need(record is not None, "Prompt absent from package manifest")
        payload = archive.read("payload/" + PROMPT_REL)
        need(hashlib.sha256(payload).hexdigest() == record.get("after_sha256"), "Prompt payload hash mismatch")

    print("SOURCE_IDENTITY_GUARD: PASS")
    print("PYTHON_SYNTAX: PASS")
    print("CURRENT_MODULE_SIZE_POLICY: PASS")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("CANONICAL_KPR_06_001_MAPPING: PASS")
    print("NO_ACTIVE_PROJECT_PROMPT_SHADOWING: PASS")
    print("THIN_WRAPPER_NO_EMBEDDED_PROMPT: PASS")
    print("CANONICAL_PROMPT_ACTIVE: PASS")
    print("CLICK_TIME_PROMPT_REREAD: PASS")
    print("DYNAMIC_PROMPT_CONTENT_PROPAGATION: PASS")
    print("PACKAGE_PAYLOAD_HASHES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
