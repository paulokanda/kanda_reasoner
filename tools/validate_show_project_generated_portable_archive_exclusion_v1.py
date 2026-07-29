# project-path: tools/validate_show_project_generated_portable_archive_exclusion_v1.py
"""Validate generated portable archive exclusion for Show Project to AI."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import zipfile
from contextlib import contextmanager
from unittest.mock import patch
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle import (
    file_manifest_builder as file_manifest_builder_module,
)
from kanda_reasoner_app.reasoner_context_bundle import (
    source_tree_exporter_inventory as source_inventory_module,
)
from kanda_reasoner_app.reasoner_context_bundle.file_manifest_builder import (
    build_file_manifest_payload,
)
from kanda_reasoner_app.reasoner_context_bundle.generated_archive_policy import (
    PORTABLE_DISTRIBUTION_CREATION_POLICY,
    PORTABLE_DISTRIBUTION_NAME_TEMPLATE,
    SUSPICIOUS_LARGE_ROOT_ARCHIVE_BYTES,
    classify_generated_project_archive,
)
from kanda_reasoner_app.reasoner_context_bundle.project_context import (
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ExclusionRules
from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter import (
    gather_source_archive_inventory,
    write_source_archive_parts,
)

FEATURE_ID = "show-project-generated-portable-archive-exclusion-v1r4"



_FIXTURE_RULE_ENV = {
    "PROJECT_REASONER_TAB8_IGNORE_RULES_JSON": json.dumps(
        {
            "folders": ["tests"],
            "files": ["*.zip"],
            "extensions": [],
        }
    ),
    "PROJECT_REASONER_IGNORE_RULES_JSON": json.dumps(
        {
            "folders": ["fixtures"],
            "files": [],
            "extensions": [".zip"],
        }
    ),
}


@contextmanager
def _isolated_fixture_exclusion_rules():
    """Keep deterministic fixtures independent from user/project preferences."""
    rules = ExclusionRules(
        folders=(),
        files=(),
        extensions=(),
        source="validator_fixture_isolated_rules",
    )
    with patch.dict(os.environ, _FIXTURE_RULE_ENV, clear=False):
        with patch.object(
            file_manifest_builder_module,
            "load_bundle_exclusion_rules",
            return_value=rules,
        ):
            with patch.object(
                source_inventory_module,
                "load_bundle_exclusion_rules",
                return_value=rules,
            ):
                yield


def _write_zip(path: Path, member_name: str, payload: bytes) -> None:
    """Write one small deterministic ZIP fixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr(member_name, payload)


def _source_archive_members(result: dict[str, object]) -> set[str]:
    """Return all member names from generated source archive parts."""
    names: set[str] = set()
    source_filenames = {
        str(item.get("filename", ""))
        for item in result.get("source_zip_parts", [])
        if isinstance(item, dict)
    }
    for item in result.get("created_paths", []):
        path = Path(str(item))
        if path.name not in source_filenames:
            continue
        with zipfile.ZipFile(path, "r") as archive:
            names.update(archive.namelist())
    return names


def _reason_codes(rows: list[dict[str, object]]) -> dict[str, str]:
    """Map excluded paths to reason codes."""
    return {
        str(item.get("path", "")): str(item.get("reason_code", ""))
        for item in rows
        if isinstance(item, dict)
    }


def _validate_portable_exclusion_isolated(temp_root: Path) -> None:
    """Validate manifest and source archive exclusion alignment."""
    project = temp_root / "ExampleProject"
    output = temp_root / "second_prompt_files"
    scratch = temp_root / "scratch"
    project.mkdir()
    (project / "main.py").write_text("print('ok')\n", encoding="utf-8")

    portable = project / "ExampleProject-Windows-Portable.zip"
    _write_zip(portable, "ExampleProject/main.py", b"print('portable')\n")

    nested_portable = (
        project / "tests" / "fixtures" / "ExampleProject-Windows-Portable.zip"
    )
    _write_zip(nested_portable, "fixture.txt", b"portable fixture\n")

    nested_source_fixture = (
        project / "tests" / "fixtures" / "ExampleProject-ArchiveFixture.zip"
    )
    _write_zip(nested_source_fixture, "fixture.txt", b"source fixture\n")

    ordinary_archive = project / "assets" / "sample_data.zip"
    _write_zip(ordinary_archive, "sample.txt", b"sample\n")

    file_manifest = build_file_manifest_payload(project)
    manifest_files = {str(item.get("path", "")) for item in file_manifest["files"]}
    manifest_excluded = _reason_codes(file_manifest["excluded_path_samples"])

    assert portable.name not in manifest_files
    assert manifest_excluded.get(portable.name) == "generated_portable_distribution"
    nested_portable_path = "tests/fixtures/ExampleProject-Windows-Portable.zip"
    assert nested_portable_path not in manifest_files
    assert manifest_excluded.get(nested_portable_path) == (
        "generated_portable_distribution"
    )
    nested_source_path = "tests/fixtures/ExampleProject-ArchiveFixture.zip"
    assert nested_source_path in manifest_files
    assert "assets/sample_data.zip" in manifest_files
    print("FILE_MANIFEST_PORTABLE_EXCLUSION: PASS")
    print("NESTED_PORTABLE_DISTRIBUTION_EXCLUDED: PASS")

    inventory = gather_source_archive_inventory(project, output)
    included_paths = {str(item.get("path", "")) for item in inventory["included_files"]}
    excluded_codes = _reason_codes(inventory["excluded_paths"])

    assert portable.name not in included_paths
    assert excluded_codes.get(portable.name) == "generated_portable_distribution"
    nested_portable_path = "tests/fixtures/ExampleProject-Windows-Portable.zip"
    assert nested_portable_path not in included_paths
    assert excluded_codes.get(nested_portable_path) == (
        "generated_portable_distribution"
    )
    nested_source_path = "tests/fixtures/ExampleProject-ArchiveFixture.zip"
    assert nested_source_path in included_paths
    assert "assets/sample_data.zip" in included_paths
    print("SOURCE_ARCHIVE_PORTABLE_EXCLUSION: PASS")

    result = write_source_archive_parts(
        project,
        output,
        scratch,
        part_size_mb=50,
        part_size_bytes=50 * 1024 * 1024,
    )
    members = _source_archive_members(result)
    assert portable.name not in members
    assert "tests/fixtures/ExampleProject-Windows-Portable.zip" not in members
    assert "tests/fixtures/ExampleProject-ArchiveFixture.zip" in members
    assert "assets/sample_data.zip" in members
    print("PORTABLE_ARCHIVE_NOT_IN_SOURCE_PARTS: PASS")
    print("LEGITIMATE_NESTED_SOURCE_ZIP_PRESERVED: PASS")

    manifest_path = Path(str(result["manifest_path"]))
    manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_codes = _reason_codes(manifest_payload["excluded_paths"])
    assert manifest_codes.get(portable.name) == "generated_portable_distribution"
    assert manifest_codes.get(
        "tests/fixtures/ExampleProject-Windows-Portable.zip"
    ) == "generated_portable_distribution"
    print("PORTABLE_EXCLUSION_RECORDED_IN_MANIFEST: PASS")


def _validate_portable_exclusion(temp_root: Path) -> None:
    """Run portable fixtures with explicit isolation from ambient rule state."""
    with _isolated_fixture_exclusion_rules():
        _validate_portable_exclusion_isolated(temp_root)
    print("AMBIENT_PROJECT_EXCLUSION_RULE_ISOLATION: PASS")


def _validate_large_archive_fail_closed(temp_root: Path) -> None:
    """Validate fast failure for unknown large project-prefixed root ZIPs."""
    project = temp_root / "LargeProject"
    output = temp_root / "large_output"
    project.mkdir()
    (project / "main.py").write_text("print('ok')\n", encoding="utf-8")
    suspicious = project / "LargeProject-CapturedData.zip"
    with suspicious.open("wb") as stream:
        stream.truncate(SUSPICIOUS_LARGE_ROOT_ARCHIVE_BYTES + 1)

    expected = "Suspicious large project-prefixed ZIP at project root"
    try:
        gather_source_archive_inventory(project, output)
    except ValueError as exc:
        assert expected in str(exc)
    else:
        raise AssertionError("Large project-prefixed root ZIP was not blocked.")

    try:
        build_file_manifest_payload(project)
    except ValueError as exc:
        assert expected in str(exc)
    else:
        raise AssertionError("File manifest did not block suspicious large ZIP.")
    print("SUSPICIOUS_LARGE_ROOT_ARCHIVE_FAIL_CLOSED: PASS")


def _validate_kanda_filename(temp_root: Path) -> None:
    """Validate the exact demonstrated KANDA portable filename."""
    project = temp_root / "kanda_reasoner"
    output = temp_root / "kanda_output"
    project.mkdir()
    portable = project / "KandaReasoner-Windows-Portable.zip"
    _write_zip(portable, "KandaReasonerWindows.exe", b"portable")
    inventory = gather_source_archive_inventory(project, output)
    excluded_codes = _reason_codes(inventory["excluded_paths"])
    assert excluded_codes.get(portable.name) == "generated_portable_distribution"
    print("KANDA_PORTABLE_FILENAME_REGRESSION: PASS")



def _validate_live_project_classification(project_root: Path | None) -> None:
    """Validate the demonstrated portable archive against the live project."""
    if project_root is None:
        print("LIVE_PROJECT_PORTABLE_CLASSIFICATION: NOT_REQUESTED")
        return
    context = resolve_project_context(project_root)
    candidate = project_root / "KandaReasoner-Windows-Portable.zip"
    if not candidate.is_file():
        print("LIVE_PROJECT_PORTABLE_CLASSIFICATION: PASS (NOT_PRESENT)")
        return
    classification = classify_generated_project_archive(candidate, context)
    assert classification is not None
    assert classification.reason_code == "generated_portable_distribution"
    print("LIVE_PROJECT_PORTABLE_CLASSIFICATION: PASS")



def _validate_portable_creation_canon(project_root: Path) -> None:
    """Validate that portable builds are external and explicit-user-only."""
    assert PORTABLE_DISTRIBUTION_NAME_TEMPLATE == "<project>-Windows-Portable.zip"
    required_policy = (
        "Show Project to AI never creates a portable distribution"
    )
    assert required_policy in PORTABLE_DISTRIBUTION_CREATION_POLICY
    assert "explicit user request" in PORTABLE_DISTRIBUTION_CREATION_POLICY
    assert "outside the selected Project Support root" in (
        PORTABLE_DISTRIBUTION_CREATION_POLICY
    )

    support_path = project_root / (
        "kanda_reasoner_app/reasoner_context_bundle/"
        "handoff_zip_exporter_support.py"
    )
    support_text = support_path.read_text(encoding="utf-8-sig")
    assert (
        "Show Project to AI never creates <project>-Windows-Portable.zip"
        in support_text
    )
    assert "only by an independent workflow after an explicit user request" in (
        support_text
    )
    assert "outside the _show_project_to_AI support root" in support_text
    assert (
        "Show Project to AI and Portable Distribution are different Boxes"
        in support_text
    )

    bridge_path = project_root / (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "12_generalized_project_canons/project_tool_boundary_startup_bridge.md"
    )
    bridge_text = bridge_path.read_text(encoding="utf-8-sig")
    assert "version: 2.2" in bridge_text
    assert "Show Project to AI must never create, refresh, publish" in bridge_text
    assert "Portable build trigger = explicit user request only" in bridge_text

    canon_path = project_root / (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "12_generalized_project_canons/project_tool_boundary_canon.md"
    )
    canon_text = canon_path.read_text(encoding="utf-8-sig")
    assert "Version: 2.2" in canon_text
    assert "is not a Show Project to AI artifact" in canon_text
    normalized_canon = " ".join(canon_text.split())
    assert "independently routed productization/release workflow" in normalized_canon
    assert "different Box" in normalized_canon
    assert "must never share an output owner" in normalized_canon
    assert "must not be silently regenerated" in normalized_canon

    metadata_expectations = {
        "project_tool_boundary_startup_bridge.meta.json": "2.2",
        "project_tool_boundary_canon.meta.json": "2.2",
    }
    metadata_root = project_root / (
        "kanda_prompt_workspace/prompt_library/METADATA"
    )
    for filename, version in metadata_expectations.items():
        payload = json.loads(
            (metadata_root / filename).read_text(encoding="utf-8-sig")
        )
        assert str(payload.get("version")) == version
        assert payload.get("source_stage") == (
            "show-project-generated-portable-archive-exclusion-v1r2"
        )
        assert payload.get("updated_for") == payload.get("source_stage")

    forbidden_creation_tokens = (
        "KandaReasonerWindows.spec",
        "PyInstaller.__main__",
        "pyinstaller ",
        "build_portable_distribution",
        "create_portable_distribution",
    )
    scan_roots = [
        project_root / "kanda_reasoner_app/reasoner_context_bundle",
        project_root / "kanda_reasoner_app/reasoner_tools_shell/runner_help",
    ]
    allowed = {
        support_path.resolve(),
        (project_root / (
            "kanda_reasoner_app/reasoner_context_bundle/"
            "generated_archive_policy.py"
        )).resolve(),
    }
    offenders: list[str] = []
    for scan_root in scan_roots:
        for path in scan_root.rglob("*.py"):
            if path.resolve() in allowed:
                continue
            body = path.read_text(encoding="utf-8-sig", errors="replace")
            if any(token.lower() in body.lower() for token in forbidden_creation_tokens):
                offenders.append(path.relative_to(project_root).as_posix())
    assert not offenders, "Show Project portable creation owner leaked: " + ", ".join(offenders)
    print("SHOW_PROJECT_NEVER_CREATES_PORTABLE: PASS")
    print("PORTABLE_BUILD_EXPLICIT_USER_ONLY: PASS")
    print("PORTABLE_BUILD_OUTSIDE_PROJECT_SUPPORT: PASS")
    print("PORTABLE_CREATION_OWNER_SEPARATION: PASS")
    print("SHOW_PROJECT_PORTABLE_BOX_NO_MIXTURE: PASS")

def main() -> int:
    """Run focused regression validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="")
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve() if args.project_root else None
    with tempfile.TemporaryDirectory(prefix="kanda_portable_archive_") as temp_dir:
        temp_root = Path(temp_dir)
        _validate_portable_exclusion(temp_root)
        _validate_large_archive_fail_closed(temp_root)
        _validate_kanda_filename(temp_root)
    _validate_live_project_classification(project_root)
    _validate_portable_creation_canon(PROJECT_ROOT)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
