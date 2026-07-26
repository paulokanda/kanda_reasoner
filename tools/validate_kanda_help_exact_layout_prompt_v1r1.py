"""Validate the KANDA help exact-layout renderer-contract prompt revision."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FEATURE_ID = "kanda-help-exact-layout-renderer-contract-v1r1"
PID = "kanda_desktop_help_exact_layout_blueprint"
CODE = "KPR-12-015"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    library = root / "kanda_prompt_workspace/prompt_library"

    prompt_path = library / f"ACTIVE_PROMPTS/12_generalized_project_canons/{PID}.md"
    meta_path = library / f"METADATA/{PID}.meta.json"
    require(prompt_path.is_file(), "exact-layout prompt missing")
    require(meta_path.is_file(), "exact-layout metadata missing")

    text = prompt_path.read_text(encoding="utf-8")
    required_tokens = (
        CODE,
        "version: 1.1.0",
        "Non-negotiable rendering-path contract",
        "QWebEngineView",
        "QUrl.fromLocalFile",
        "setUrl",
        "QTextBrowser",
        "QTextEdit.setHtml()",
        "Visual failure diagnosis",
        "orange top rule",
        "dark-blue chapter opener",
        "bilateral page margins",
        "restarted application",
    )
    for token in required_tokens:
        require(token in text, "renderer contract missing: " + token)

    require(
        "Primary renderer must use `QWebEngineView`" in text,
        "primary-renderer requirement missing",
    )
    require(
        "A patch that changes only Markdown or HTML" in text,
        "renderer-boundary correction rule missing",
    )

    meta = load_json(meta_path)
    require(meta["prompt_code"] == CODE, "prompt code mismatch")
    require(meta["version"] == "1.1.0", "metadata version mismatch")
    require(
        meta["required_companion_prompts"] == ["desktop_help_document_layout_canon"],
        "companion mismatch",
    )
    regressions = " ".join(meta.get("do_not_regress", []))
    require("QWebEngineView" in regressions, "metadata renderer guard missing")
    require("setHtml" in regressions, "metadata rich-text guard missing")

    owner_path = library / "ACTIVE_PROMPTS/12_generalized_project_canons/desktop_help_document_layout_canon.md"
    owner = owner_path.read_text(encoding="utf-8")
    require("version: 2.2.0" in owner, "owner version bridge missing")
    require(PID in owner and CODE in owner, "owner companion bridge missing")
    require("browser-grade local-file rendering" in owner, "owner renderer bridge missing")

    owner_meta = load_json(library / "METADATA/desktop_help_document_layout_canon.meta.json")
    require(owner_meta["version"] == "2.2.0", "owner metadata version mismatch")
    require(PID in owner_meta.get("required_companion_prompts", []), "owner metadata bridge missing")

    groups = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in groups["groups"] if item["group_id"] == "12_generalized_project_canons")
    require(PID in group["prompt_ids"], "canonical group registration missing")
    require(group["prompt_count"] == len(group["prompt_ids"]), "group count mismatch")

    mirror = load_json(root / "kanda_reasoner_app/prompt_library/groups/PROMPT_GROUPS.json")
    mirrored = next(item for item in mirror["groups"] if item["group_id"] == "12_generalized_project_canons")
    require(group == mirrored, "group mirror mismatch")

    nav = load_json(library / "ROUTING/prompt_navigation_index.json")
    matches = [entry for entry in nav["entries"] if entry.get("prompt_id") == PID]
    require(len(matches) == 1, "navigation registration must be unique")
    require(nav["prompt_count"] == len(nav["entries"]), "navigation count mismatch")

    folder = (library / "ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md").read_text(encoding="utf-8")
    require(CODE in folder and PID in folder, "folder-card registration missing")

    substitution = (library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md").read_text(encoding="utf-8")
    require(CODE in substitution and PID in substitution, "routing bridge missing")

    print("HELP_EXACT_LAYOUT_PROMPT_SOURCE: PASS")
    print("HELP_RENDERER_PRIMARY_QWEBENGINE: PASS")
    print("HELP_LOCAL_FILE_URL_LOADING: PASS")
    print("HELP_RICH_TEXT_PRIMARY_REJECTED: PASS")
    print("HELP_RENDERER_FIRST_DIAGNOSIS: PASS")
    print("HELP_EXACT_LAYOUT_COMPANION_BRIDGE: PASS")
    print("PROMPT_LIBRARY_REGISTRATION: PASS")
    print("PROMPT_GROUP_MIRROR: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
