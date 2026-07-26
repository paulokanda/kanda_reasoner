# project-path: tools/validate_stale_variant_governed_validation_artifact_policy_v1.py
"""Validate governed validation artifact stale-variant classification."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Sequence

__all__ = [
    "main",
]

FEATURE_ID = "stale-variant-governed-validation-artifact-policy-v1"
SOURCE_LOADER_PATH = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_private_impl.py"
)
WARNING_POLICY_PATH = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_warning_policy_private_impl.py"
)
VALIDATOR_PATH = Path(
    "tools/validate_stale_variant_governed_validation_artifact_policy_v1.py"
)
FREEZE_HINT_NAME = "KANDA_FREEZE_HINT.json"
MAX_MODULE_LINES = 500

REQUIRED_PROJECT_ARTIFACTS = (
    Path("scripts/repair_ai_response_patch_delivery_public_ownership_batch18_v1.py"),
    Path("scripts/validate_large_module_refactor_protocol_v71.py"),
    Path("tools/validate_error_memory_duplicate_cleanup_v13.py"),
    Path("tools/validate_project_aa_boxed_dynamic_local_ai_run_analysis_v8.py"),
)


def _assert(condition: bool, message: str) -> None:
    """Raise a deterministic validation error when a condition fails."""
    if not condition:
        raise AssertionError(message)


def _normalized_member_names(path: Path) -> list[str]:
    """Return normalized file members from a ZIP archive."""
    with zipfile.ZipFile(path, "r") as archive:
        return sorted(
            name.replace("\\", "/")
            for name in archive.namelist()
            if name and not name.endswith("/")
        )


def _validate_patch_zip(path: Path) -> None:
    """Validate exact required members when a patch ZIP is supplied."""
    _assert(path.is_file(), f"PATCH_ZIP_MISSING: {path}")
    members = _normalized_member_names(path)
    required = {
        SOURCE_LOADER_PATH.as_posix(),
        WARNING_POLICY_PATH.as_posix(),
        VALIDATOR_PATH.as_posix(),
        FREEZE_HINT_NAME,
    }
    missing = sorted(required.difference(members))
    _assert(not missing, "PATCH_ZIP_REQUIRED_MEMBERS_MISSING: " + repr(missing))
    _assert(
        members.count(FREEZE_HINT_NAME) == 1,
        "PATCH_ZIP_FREEZE_HINT_COUNT_CHANGED",
    )
    print("PATCH_ZIP_REQUIRED_MEMBERS: PASS")


def _validate_source_files(project_root: Path) -> None:
    """Validate syntax, ASCII text, and module-size limits."""
    for relative_path in (
        SOURCE_LOADER_PATH,
        WARNING_POLICY_PATH,
        VALIDATOR_PATH,
    ):
        path = project_root / relative_path
        _assert(path.is_file(), f"REQUIRED_FILE_MISSING: {relative_path}")
        raw = path.read_bytes()
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise AssertionError(
                f"NON_ASCII_SOURCE: {relative_path}: {exc}"
            ) from exc
        compile(text, str(path), "exec")
        line_count = len(text.splitlines())
        _assert(
            line_count <= MAX_MODULE_LINES,
            f"MODULE_TOO_LARGE: {relative_path}: {line_count}",
        )
    print("PYTHON_SYNTAX_ASCII_MODULE_SIZE: PASS")


def _import_architecture_module(project_root: Path):
    """Import the architecture module from the selected project root."""
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    importlib.invalidate_caches()
    return importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )


def _write_fixture(root: Path, relative_path: str, text: str) -> None:
    """Write one UTF-8 fixture source file."""
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _stale_paths(issues) -> set[str]:
    """Return stale-variant issue paths."""
    return {
        issue.path
        for issue in issues
        if issue.code == "STALE_VARIANT_SOURCE_OF_TRUTH"
    }


def _deprecated_paths(issues) -> set[str]:
    """Return deprecated-reference issue paths."""
    return {
        issue.path
        for issue in issues
        if issue.code == "DEPRECATED_VARIANT_STILL_REFERENCED"
    }


def _validate_characterization(module) -> None:
    """Validate exclusion and retained-warning behavior on a small project."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        fixtures = {
            "scripts/repair_alpha_batch18_v1.py": '"""Repair helper."""\n',
            "scripts/validate_alpha_v1.py": '"""Validator v1."""\n',
            "scripts/validate_alpha_v2.py": '"""Validator v2."""\n',
            "tools/validate_beta_repair_v1.py": '"""Validator repair."""\n',
            "kanda_reasoner_app/feature_old.py": '"""Old production variant."""\n',
            "tools/old_helper.py": '"""Old tool helper."""\n',
            "scripts/copy_worker.py": '"""Suspicious copy script."""\n',
        }
        for relative_path, text in fixtures.items():
            _write_fixture(root, relative_path, text)

        _, issues, _, _ = module.scan_project(root)
        stale_paths = _stale_paths(issues)
        excluded_paths = {
            "scripts/repair_alpha_batch18_v1.py",
            "scripts/validate_alpha_v1.py",
            "scripts/validate_alpha_v2.py",
            "tools/validate_beta_repair_v1.py",
        }
        retained_paths = {
            "kanda_reasoner_app/feature_old.py",
            "tools/old_helper.py",
            "scripts/copy_worker.py",
        }
        _assert(
            not stale_paths.intersection(excluded_paths),
            "GOVERNED_ARTIFACT_FALSE_POSITIVE_REMAINS: "
            + repr(sorted(stale_paths.intersection(excluded_paths))),
        )
        _assert(
            retained_paths.issubset(stale_paths),
            "REAL_STALE_VARIANT_SIGNAL_LOST: "
            + repr(sorted(retained_paths.difference(stale_paths))),
        )

    print("GOVERNED_VALIDATION_ARTIFACT_EXCLUSION: PASS")
    print("NON_GOVERNED_STALE_VARIANT_RETENTION: PASS")


def _validate_reference_scope(module) -> None:
    """Prove validators are not treated as active runtime referrers."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_fixture(
            root,
            "kanda_reasoner_app/old_service.py",
            '"""Old service."""\nVALUE = 1\n',
        )
        _write_fixture(
            root,
            "tools/validate_old_service_repair_v1.py",
            "import kanda_reasoner_app.old_service\n",
        )
        _, issues, _, _ = module.scan_project(root)
        _assert(
            "kanda_reasoner_app/old_service.py" not in _deprecated_paths(issues),
            "VALIDATOR_COUNTED_AS_ACTIVE_RUNTIME_REFERRER",
        )

        _write_fixture(
            root,
            "kanda_reasoner_app/consumer.py",
            "import kanda_reasoner_app.old_service\n",
        )
        _, issues, _, _ = module.scan_project(root)
        _assert(
            "kanda_reasoner_app/old_service.py" in _deprecated_paths(issues),
            "ACTIVE_RUNTIME_DEPRECATED_REFERENCE_NOT_DETECTED",
        )

    print("DEPRECATED_REFERENCE_ACTIVE_OWNER_SCOPE: PASS")


def _validate_current_project(module, project_root: Path) -> None:
    """Validate representative current project artifacts and all candidates."""
    for relative_path in REQUIRED_PROJECT_ARTIFACTS:
        _assert(
            (project_root / relative_path).is_file(),
            f"REPRESENTATIVE_ARTIFACT_MISSING: {relative_path}",
        )

    top_names = module.project_top_level_names(project_root)
    candidate_modules = {}
    for root_name in ("scripts", "tools"):
        root = project_root / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            stem = path.stem.lower().replace("-", "_")
            if not stem.startswith(("validate_", "repair_")):
                continue
            info, _ = module.scan_module(project_root, path, top_names)
            candidate_modules[info.module_id] = info

    _assert(candidate_modules, "NO_GOVERNED_VALIDATION_CANDIDATES_FOUND")
    module.build_reverse_dependencies(candidate_modules)
    stale_issues = module.detect_stale_variant_issues(candidate_modules)
    deprecated_issues = module.detect_deprecated_variant_reference_issues(
        candidate_modules
    )
    _assert(
        not stale_issues,
        "CURRENT_PROJECT_GOVERNED_ARTIFACT_WARNINGS_REMAIN: "
        + repr([issue.path for issue in stale_issues[:10]]),
    )
    _assert(
        not deprecated_issues,
        "CURRENT_PROJECT_GOVERNED_REFERENCE_ERRORS_REMAIN: "
        + repr([issue.path for issue in deprecated_issues[:10]]),
    )
    print(
        "CURRENT_PROJECT_GOVERNED_ARTIFACT_SET: PASS "
        f"({len(candidate_modules)} artifacts)"
    )


def _validate_freeze_hint(project_root: Path) -> None:
    """Validate a staged root-level freeze hint when present beside the ZIP."""
    hint_path = project_root / FREEZE_HINT_NAME
    if not hint_path.is_file():
        return
    payload = json.loads(hint_path.read_text(encoding="utf-8"))
    _assert(payload.get("feature_id") == FEATURE_ID, "FREEZE_HINT_FEATURE_ID_CHANGED")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        required=True,
        help="Installed project root to validate.",
    )
    parser.add_argument(
        "--patch-zip",
        help="Optional staged patch ZIP to validate.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run focused validation and print deterministic markers."""
    args = build_parser().parse_args(argv)
    project_root = Path(args.project_root).expanduser().resolve()
    _assert(project_root.is_dir(), f"PROJECT_ROOT_MISSING: {project_root}")

    _validate_source_files(project_root)
    if args.patch_zip:
        _validate_patch_zip(Path(args.patch_zip).expanduser().resolve())

    module = _import_architecture_module(project_root)
    _validate_characterization(module)
    _validate_reference_scope(module)
    _validate_current_project(module, project_root)
    _validate_freeze_hint(project_root)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
