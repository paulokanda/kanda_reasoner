from __future__ import annotations

import argparse
import json
from pathlib import Path

FEATURE_ID = "large-module-refactor-protocol-canon-v6"

PROTOCOL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)
TEMPLATE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_template.md"
)
PROTOCOL_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "large_module_refactor_protocol.meta.json"
)
TEMPLATE_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "large_module_refactor_template.meta.json"
)
LEGACY_ACTIVE_REL = Path(
    "kanda_reasoner_app/prompt_library/active/"
    "0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL TEMPLATE v1.0.md"
)

PROTOCOL_NEEDLES = [
    "Version: 6.0",
    "Import analysis",
    "Public API inventory",
    "characterization tests",
    "Import compatibility matrix",
    "`__init__.py` re-export",
    "__all__",
    "circular import risk",
    "Ruff",
    "modguard",
    "pyrefact",
    "wily",
    "<drive>:\\<project>_delete_after_daily_work",
    "Do not refactor to look organized while changing behavior accidentally.",
]

TEMPLATE_NEEDLES = [
    "Version: 2.0.0",
    "import compatibility risks",
    "`__init__.py` re-export strategy",
    "`__all__` strategy",
    "characterization tests",
    "circular import risk",
    "<drive>:\\<project>_delete_after_daily_work",
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def assert_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    assert_true(not raw.startswith(b"\xef\xbb\xbf"), str(path) + " must be UTF-8 without BOM")


def assert_ascii(path: Path) -> None:
    text = read_text(path)
    try:
        text.encode("ascii")
    except UnicodeEncodeError as exc:
        raise AssertionError(str(path) + " must be ASCII-only: " + str(exc)) from exc


def assert_prompt(project_root: Path) -> None:
    protocol = project_root / PROTOCOL_REL
    template = project_root / TEMPLATE_REL
    assert_true(protocol.is_file(), "missing protocol prompt: " + str(PROTOCOL_REL))
    assert_true(template.is_file(), "missing template prompt: " + str(TEMPLATE_REL))

    for path in [protocol, template]:
        assert_no_bom(path)
        assert_ascii(path)

    protocol_text = read_text(protocol)
    template_text = read_text(template)

    for needle in PROTOCOL_NEEDLES:
        assert_true(needle in protocol_text, "protocol prompt missing required canon needle: " + needle)

    for needle in TEMPLATE_NEEDLES:
        assert_true(needle in template_text, "template prompt missing required canon needle: " + needle)

    assert_true(
        "Legacy prompt-library mirrors" in protocol_text,
        "protocol must document backup/read-only treatment for named legacy active prompt mirrors",
    )


def assert_metadata(project_root: Path) -> None:
    protocol_meta = json.loads(read_text(project_root / PROTOCOL_META_REL))
    template_meta = json.loads(read_text(project_root / TEMPLATE_META_REL))

    assert_true(protocol_meta.get("version") == "6.0", "protocol metadata version must be 6.0")
    assert_true(template_meta.get("version") == "2.0.0", "template metadata version must be 2.0.0")

    triggers = set(protocol_meta.get("trigger_phrases", []))
    assert_true("import compatibility matrix" in triggers, "protocol metadata must include import compatibility trigger")
    assert_true("__all__ enforcement" in triggers, "protocol metadata must include __all__ trigger")


def assert_legacy_backup(project_root: Path) -> None:
    legacy = project_root / LEGACY_ACTIVE_REL
    if not legacy.exists():
        return

    project_name = project_root.name
    drive_root = Path(project_root.anchor)
    backup_dir = drive_root / f"{project_name}_delete_after_daily_work" / "prompt_backups" / FEATURE_ID
    backups = list(backup_dir.glob("0000_5_5_PYARCHITECT_LARGE_MODULE_REFACTOR_PROTOCOL_TEMPLATE_v1_0*.md"))
    assert_true(
        bool(backups),
        "legacy active prompt backup missing from daily-work prompt_backups for " + FEATURE_ID,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    assert_prompt(project_root)
    assert_metadata(project_root)
    assert_legacy_backup(project_root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
