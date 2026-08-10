# project-path: tools/validate_architecture_reported_error_cleanup_v1.py
"""Validate cleanup of the reported architecture error set."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import sys
import tempfile
from pathlib import Path
from typing import Sequence

__all__ = ["main"]

FEATURE_ID = "kanda-reasoner-architecture-reported-error-cleanup-v1"
MAX_MODULE_LINES = 500

TOUCHED_SOURCE_PATHS = (
    Path("kanda_reasoner_app/_project_support_path_contracts.py"),
    Path("kanda_reasoner_app/project_root_resolver.py"),
    Path("kanda_reasoner_app/project_support_boundary.py"),
    Path(
        "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
        "source_loader_warning_policy_extended_private_impl.py"
    ),
    Path(
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_write_storage.py"
    ),
    Path(
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_write_broker.py"
    ),
    Path("tools/validate_architecture_reported_error_cleanup_v1.py"),
)

TARGET_ERROR_CODES = {
    "CIRCULAR_IMPORT",
    "CROSS_BOX_PUBLIC_SYMBOL_COLLISION",
    "DEPRECATED_VARIANT_STILL_REFERENCED",
}

REPORTED_DEPRECATED_PATHS = {
    "kanda_reasoner_app/freeze_after_update_gui/"
    "_ai_formulary_transport_repair.py",
    "kanda_reasoner_app/reasoner_context_bundle/generated_archive_policy.py",
    "kanda_reasoner_app/reasoner_context_bundle/source_archive_routing.py",
    "kanda_reasoner_app/reasoner_engine/chat_clipboard_actions.py",
    "kanda_reasoner_app/source_hygiene/reference_archive_validation.py",
    "kanda_reasoner_app/source_hygiene/tool_archive_policy.py",
    "portable/archive.py",
}

PORTABLE_MANIFEST_HASHES = {
    Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json"):
        "3edc2dc542d24b222384267a4d52f6e19b7cc959dc332bc36a259c7ce8a7a2a7",
    Path("portable/PORTABLE_BUILDER_MANIFEST.json"):
        "c1c0013e9925039bb688e13532a6f279a2ee00053bb0d55047813b3a82022eaa",
}


def require(condition: bool, message: str) -> None:
    """Raise a deterministic validation error when a condition fails."""
    if not condition:
        raise AssertionError(message)


def bootstrap_project_root(project_root: Path) -> None:
    """Make the selected Project package root explicit for all imports."""
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    importlib.invalidate_caches()


def validate_source_contracts(project_root: Path) -> None:
    """Validate syntax, ASCII text, and module-size limits."""
    for relative_path in TOUCHED_SOURCE_PATHS:
        path = project_root / relative_path
        require(path.is_file(), f"REQUIRED_FILE_MISSING:{relative_path}")
        raw = path.read_bytes()
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise AssertionError(
                f"NON_ASCII_SOURCE:{relative_path}:{exc}"
            ) from exc
        compile(text, str(path), "exec")
        line_count = len(text.splitlines())
        require(
            line_count <= MAX_MODULE_LINES,
            f"MODULE_TOO_LARGE:{relative_path}:{line_count}",
        )
    print("TOUCHED_SOURCE_SYNTAX_ASCII_MODULE_SIZE: PASS")


def load_architecture_module():
    """Import the architecture scanner after explicit root bootstrap."""
    return importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )


def validate_current_architecture(module, project_root: Path) -> None:
    """Require the reported architecture errors to be absent."""
    _, issues, _, _ = module.scan_project(project_root)
    target_errors = [
        issue
        for issue in issues
        if issue.level == "error" and issue.code in TARGET_ERROR_CODES
    ]
    require(
        not target_errors,
        "REPORTED_ARCHITECTURE_ERRORS_REMAIN:"
        + repr([issue.as_dict() for issue in target_errors]),
    )

    deprecated_paths = {
        issue.path
        for issue in issues
        if issue.code == "DEPRECATED_VARIANT_STILL_REFERENCED"
    }
    remaining_paths = sorted(REPORTED_DEPRECATED_PATHS & deprecated_paths)
    require(
        not remaining_paths,
        "REPORTED_DEPRECATED_FALSE_POSITIVES_REMAIN:" + repr(remaining_paths),
    )

    cycle_messages = [
        issue.message
        for issue in issues
        if issue.code == "CIRCULAR_IMPORT"
    ]
    require(
        not any(
            "project_root_resolver" in message
            and "project_support_boundary" in message
            for message in cycle_messages
        ),
        "PROJECT_ROOT_SUPPORT_BOUNDARY_CYCLE_REMAINS",
    )

    collision_messages = [
        issue.message
        for issue in issues
        if issue.code == "CROSS_BOX_PUBLIC_SYMBOL_COLLISION"
    ]
    require(
        not any("sha256_bytes" in message for message in collision_messages),
        "SHA256_PUBLIC_SYMBOL_COLLISION_REMAINS",
    )

    print("REPORTED_ARCHITECTURE_ERROR_SET_ABSENT: PASS")
    print("PROJECT_ROOT_SUPPORT_BOUNDARY_CYCLE_ABSENT: PASS")
    print("PROJECT_WEB_AI_SHA256_OWNER_UNIQUE: PASS")
    print("ACTIVE_DOMAIN_FILENAME_FALSE_POSITIVES_ABSENT: PASS")


def write_fixture(root: Path, relative_path: str, text: str) -> None:
    """Write one deterministic fixture module."""
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def validate_stale_variant_characterization(module) -> None:
    """Preserve real stale detection while accepting domain terminology."""
    active_paths = sorted(REPORTED_DEPRECATED_PATHS)
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        imports = []
        for index, relative_path in enumerate(active_paths):
            write_fixture(root, relative_path, f'"""Active fixture {index}."""\n')
            module_name = relative_path[:-3].replace("/", ".")
            imports.append(f"import {module_name}")
        write_fixture(
            root,
            "kanda_reasoner_app/active_consumer.py",
            "\n".join(imports) + "\n",
        )
        write_fixture(
            root,
            "kanda_reasoner_app/old_archive_policy.py",
            '"""Intentionally stale fixture."""\n',
        )

        _, issues, _, _ = module.scan_project(root)
        stale_or_deprecated = {
            issue.path
            for issue in issues
            if issue.code in {
                "STALE_VARIANT_SOURCE_OF_TRUTH",
                "DEPRECATED_VARIANT_STILL_REFERENCED",
            }
        }
        active_false_positives = sorted(
            set(active_paths) & stale_or_deprecated
        )
        require(
            not active_false_positives,
            "ACTIVE_DOMAIN_FILENAME_FALSE_POSITIVE:"
            + repr(active_false_positives),
        )
        require(
            "kanda_reasoner_app/old_archive_policy.py"
            in stale_or_deprecated,
            "REAL_STALE_ARCHIVE_VARIANT_SIGNAL_LOST",
        )

    print("ACTIVE_DOMAIN_FILENAME_CHARACTERIZATION: PASS")
    print("REAL_STALE_VARIANT_SIGNAL_RETAINED: PASS")


def validate_path_contract() -> None:
    """Require both public owners to resolve one transient path contract."""
    from kanda_reasoner_app.project_root_resolver import (
        default_smoke_output_json_path,
    )
    from kanda_reasoner_app.project_support_boundary import (
        canonical_transient_garbage_root,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "fixture_project"
        project_root.mkdir()
        transient_root = canonical_transient_garbage_root(project_root)
        smoke_path = default_smoke_output_json_path(project_root)
        require(
            smoke_path.parent.parent == transient_root,
            "TRANSIENT_PATH_CONTRACT_DIVERGED",
        )
        require(
            project_root not in smoke_path.parents,
            "TRANSIENT_OUTPUT_LEAKED_INSIDE_PROJECT_SOURCE",
        )

    print("NEUTRAL_PROJECT_SUPPORT_PATH_CONTRACT: PASS")


def validate_hash_owner() -> None:
    """Require the scoped public digest helper to remain behaviorally exact."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_write_storage import (
        project_web_ai_sha256_bytes,
    )

    raw = b"kanda-reasoner-architecture-cleanup"
    expected = hashlib.sha256(raw).hexdigest()
    require(
        project_web_ai_sha256_bytes(raw) == expected,
        "PROJECT_WEB_AI_SHA256_BEHAVIOR_CHANGED",
    )
    print("PROJECT_WEB_AI_SHA256_BEHAVIOR: PASS")


def validate_portable_manifests_unchanged(project_root: Path) -> None:
    """Prove this source repair did not alter Portable manifest authority."""
    for relative_path, expected_hash in PORTABLE_MANIFEST_HASHES.items():
        path = project_root / relative_path
        require(path.is_file(), f"PORTABLE_MANIFEST_MISSING:{relative_path}")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual_hash == expected_hash,
            f"PORTABLE_MANIFEST_CHANGED:{relative_path}:{actual_hash}",
        )
    print("PORTABLE_RUNTIME_ALLOWLIST_MODIFIED: NO")
    print("PORTABLE_BUILDER_MANIFEST_MODIFIED: NO")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the focused regression validator."""
    args = build_parser().parse_args(argv)
    project_root = Path(args.project_root).expanduser().resolve()
    require(project_root.is_dir(), f"PROJECT_ROOT_MISSING:{project_root}")
    bootstrap_project_root(project_root)
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")

    validate_source_contracts(project_root)
    module = load_architecture_module()
    validate_current_architecture(module, project_root)
    validate_stale_variant_characterization(module)
    validate_path_contract()
    validate_hash_owner()
    validate_portable_manifests_unchanged(project_root)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
