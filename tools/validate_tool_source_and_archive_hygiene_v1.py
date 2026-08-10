"""Focused Release 3 validation for Tool-source and archive hygiene."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from zipfile import ZipInfo
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from kanda_reasoner_app.archive_safety import (  # noqa: E402
    ArchiveSafetyError,
    safe_extract_zip,
)
from kanda_reasoner_app import project_root_resolver as _project_roots  # noqa: E402
from kanda_reasoner_app.project_support_boundary import (  # noqa: E402
    canonical_project_support_root,
    canonical_transient_garbage_root,
)
from kanda_reasoner_app.reasoner_context_bundle import source_tree_exporter_inventory as _source_inventory  # noqa: E402
from kanda_reasoner_app.reasoner_context_bundle.exclusion_provider import (  # noqa: E402
    load_bundle_exclusion_rules,
)
from kanda_reasoner_app.reasoner_context_bundle.project_context import (  # noqa: E402
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.source_archive_routing import (  # noqa: E402
    SourceArchiveRouteKind,
    route_source_archive_entry,
)
from kanda_reasoner_app.source_hygiene.external_capture_preview import (  # noqa: E402
    CAPTURE_FEATURE_ID,
    capture_quarantine_root,
)
from kanda_reasoner_app.source_hygiene.freeze_blueprint_validation import (  # noqa: E402
    seed_freeze_blueprint_fixture,
    validate_freeze_blueprint_policy,
    validate_freeze_blueprint_show_project_exclusion,
)
from kanda_reasoner_app.source_hygiene import kilo_workspace_validation as _kilo_validation  # noqa: E402
from kanda_reasoner_app.source_hygiene.reference_archive_validation import (  # noqa: E402
    copy_hygiene_contract as _copy_hygiene_contract,
    validate_local_development_metadata_classification,
    validate_project_reference_archive_policy,
)
from kanda_reasoner_app.source_hygiene.workspace_routing_validation import (  # noqa: E402
    validate_workspace_archive_routing,
)
from kanda_reasoner_app.source_hygiene.tool_archive_policy import (  # noqa: E402
    ToolPathClassification,
    is_project_capture_forbidden_relative,
    iter_known_capture_records,
    iter_packaged_resource_files,
    validate_registered_synthetic_fixtures,
)
FEATURE_ID = "tool-source-and-archive-hygiene-v1"
_CACHE_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    ".venv",
    "venv",
    "node_modules",
}
def gate(marker: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(marker + (":" + detail if detail else ""))
    print(marker + ": PASS")
def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
def _path_inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False
def _validate_all_current_paths(project_root: Path) -> None:
    validate_workspace_archive_routing(project_root, gate)

def _validate_source_archive_allowlist(project_root: Path, temp_root: Path) -> None:
    fixture_root = temp_root / "tool_fixture"
    (fixture_root / "kanda_reasoner_app" / "outputs").mkdir(parents=True)
    (fixture_root / "reasoner_tools_gui.py").write_text("# fixture\n", encoding="utf-8")
    (fixture_root / "KandaReasonerWindows.spec").write_text("# fixture\n", encoding="utf-8")
    (fixture_root / "kanda_reasoner_app" / "__init__.py").write_text(
        "# fixture\n", encoding="utf-8"
    )
    (fixture_root / "kanda_reasoner_app" / "approved.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    (fixture_root / "kanda_reasoner_app" / "outputs" / "capture.json").write_text(
        '{"project_root":"E:/external_project"}\n', encoding="utf-8"
    )
    _copy_hygiene_contract(project_root, fixture_root)
    seed_freeze_blueprint_fixture(fixture_root)
    inventory = _source_inventory.gather_source_archive_inventory(
        fixture_root,
        temp_root / "output",
    )
    included = {str(item["path"]) for item in inventory["included_files"]}
    excluded = {str(item["path"]) for item in inventory["excluded_paths"]}
    validate_freeze_blueprint_show_project_exclusion(included, excluded)
    gate(
        "TOOL_ARCHIVE_ALLOWLIST_ONLY",
        "kanda_reasoner_app/approved.py" in included
        and "kanda_reasoner_app/outputs" in excluded,
    )
    gate(
        "UNREGISTERED_TOOL_OUTPUT_BLOCKED",
        not any(path.startswith("kanda_reasoner_app/outputs/") for path in included),
    )
    unregistered = fixture_root / "unregistered-root-artifact.bin"
    unregistered.write_bytes(b"unregistered")
    try:
        _source_inventory.gather_source_archive_inventory(fixture_root, temp_root / "output2")
    except RuntimeError as exc:
        gate(
            "UNCLASSIFIED_TOOL_PATH_REJECTED",
            "UNCLASSIFIED_TOOL_SOURCE_PATH" in str(exc),
        )
    else:
        raise AssertionError("UNCLASSIFIED_TOOL_PATH_REJECTED")
def _validate_capture_absence(project_root: Path, receipt_path: Path) -> None:
    records = iter_known_capture_records(project_root)
    gate("KNOWN_PROJECT_CAPTURE_RECORD_PRESENT", bool(records))
    destination_count = 0
    for record in records:
        relative = str(record["path"])
        source = project_root / relative
        gate("TOOL_CAPTURE_REMOVED_FROM_SOURCE", not source.exists(), relative)
        destination = (
            capture_quarantine_root(project_root)
            / "quarantined_foreign_project_captures"
            / str(record["sha256"])
            / Path(relative).name
        )
        gate("TOOL_CAPTURE_QUARANTINE_FILE_PRESENT", destination.is_file())
        gate(
            "TOOL_CAPTURE_QUARANTINE_HASH_EXACT",
            destination.stat().st_size == int(record["size_bytes"])
            and _sha256_file(destination) == str(record["sha256"]),
        )
        destination_count += 1
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    gate(
        "TOOL_CAPTURE_QUARANTINE_RECEIPT",
        receipt.get("feature_id") == CAPTURE_FEATURE_ID
        and receipt.get("external_project_mutation_performed") is False,
    )
    gate("TOOL_CAPTURE_QUARANTINE_RECORDS_VERIFIED", destination_count > 0)
    remaining_capture_files = 0
    pruned_non_archived_roots = 0
    context = resolve_project_context(project_root)
    rules = load_bundle_exclusion_rules(context)
    output_dir = (
        project_root.parent
        / (project_root.name + "_show_project_to_AI")
        / "second_prompt_files"
    )
    for current, directory_names, file_names in os.walk(project_root):
        current_path = Path(current)
        retained: list[str] = []
        for name in directory_names:
            candidate = current_path / name
            route = route_source_archive_entry(
                candidate,
                context,
                output_dir,
                rules,
                tool_hygiene_active=True,
            )
            if route.route is SourceArchiveRouteKind.BLOCK:
                raise AssertionError(
                    "CAPTURE_SCAN_ROUTE_BLOCKED:"
                    + route.relative_path
                    + ":"
                    + route.error
                )
            if route.route is SourceArchiveRouteKind.EXCLUDE:
                if (
                    route.tool_decision is not None
                    and route.tool_decision.classification
                    is ToolPathClassification.PROJECT_CAPTURE_FORBIDDEN
                ):
                    remaining_capture_files += sum(
                        1 for item in candidate.rglob("*") if item.is_file()
                    )
                pruned_non_archived_roots += 1
                continue
            retained.append(name)
        directory_names[:] = retained
        for name in file_names:
            route = route_source_archive_entry(
                current_path / name,
                context,
                output_dir,
                rules,
                tool_hygiene_active=True,
            )
            if route.route is SourceArchiveRouteKind.BLOCK:
                raise AssertionError(
                    "CAPTURE_FILE_ROUTE_BLOCKED:"
                    + route.relative_path
                    + ":"
                    + route.error
                )
            if (
                route.tool_decision is not None
                and route.tool_decision.classification
                is ToolPathClassification.PROJECT_CAPTURE_FORBIDDEN
            ):
                remaining_capture_files += 1
    gate("NON_ARCHIVED_ROOT_RESCAN_PRUNED", pruned_non_archived_roots > 0)
    gate("TOOL_ARCHIVE_EXTERNAL_PROJECT_CAPTURE_COUNT_ZERO", remaining_capture_files == 0)
    print("TOOL_ARCHIVE_EXTERNAL_PROJECT_CAPTURE_COUNT: 0")
def _validate_synthetic_fixture(project_root: Path) -> None:
    fixtures = validate_registered_synthetic_fixtures(project_root)
    gate(
        "SYNTHETIC_FIXTURE_PROVENANCE",
        all(
            item["synthetic"] is True
            and item["source_owner"] == "TOOL"
            and item["contains_real_project_data"] is False
            for item in fixtures
        ),
    )
def _validate_pyinstaller_allowlist(project_root: Path) -> None:
    spec = (project_root / "KandaReasonerWindows.spec").read_text(
        encoding="utf-8"
    )
    active_lines = [
        line.strip()
        for line in spec.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    gate(
        "PACKAGE_WIDE_DATA_COLLECTION_REJECTED",
        not any(
            line.startswith("from PyInstaller.utils.hooks import collect_data_files")
            or line.startswith("datas += collect_data_files(")
            or line.startswith("datas = collect_data_files(")
            for line in active_lines
        ),
    )
    resources = iter_packaged_resource_files(project_root)
    gate(
        "PYINSTALLER_DATA_ALLOWLIST_ONLY",
        bool(resources)
        and not any(
            is_project_capture_forbidden_relative(
                Path(source).relative_to(project_root).as_posix()
            )
            for source, _ in resources
        ),
    )
def _validate_smoke_output(project_root: Path) -> None:
    output = _project_roots.default_smoke_output_json_path(project_root)
    transient = canonical_transient_garbage_root(project_root)
    support = canonical_project_support_root(project_root)
    gate(
        "STATIC_CONTEXT_SMOKE_OUTPUT_TRANSIENT",
        _path_inside(transient, output)
        and not _path_inside(project_root, output)
        and not _path_inside(support, output),
    )
def _write_zip(path: Path, records: list[tuple[str, bytes, int | None]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content, external_attr in records:
            info = ZipInfo(name)
            if external_attr is not None:
                info.create_system = 3
                info.external_attr = external_attr
            archive.writestr(info, content)
def _expect_archive_rejection(
    path: Path,
    destination: Path,
    expected: str,
    marker: str,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    try:
        safe_extract_zip(path, destination)
    except ArchiveSafetyError as exc:
        gate(marker, expected in str(exc), str(exc))
    else:
        raise AssertionError(marker)
def _validate_archive_safety(temp_root: Path) -> None:
    temp_root.mkdir(parents=True, exist_ok=True)
    normal = temp_root / "normal.zip"
    _write_zip(normal, [("app/file.txt", b"ok", None)])
    destination = temp_root / "normal_extract"
    report = safe_extract_zip(normal, destination, expected_top_level="app")
    gate(
        "ARCHIVE_MEMBER_PATH_CONTAINMENT",
        report.member_count == 1 and (destination / "app/file.txt").is_file(),
    )
    gate("ARCHIVE_POST_EXTRACTION_SCOPE", report.file_count == 1)
    cases = (
        ("absolute.zip", [("/evil.txt", b"x", None)], "ARCHIVE_ABSOLUTE_MEMBER_REJECTED", "ARCHIVE_ABSOLUTE_MEMBER_REJECTION"),
        ("drive.zip", [("C:/evil.txt", b"x", None)], "ARCHIVE_DRIVE_QUALIFIED_MEMBER_REJECTED", "ARCHIVE_DRIVE_QUALIFIED_MEMBER_REJECTION"),
        ("parent.zip", [("app/../evil.txt", b"x", None)], "ARCHIVE_PARENT_TRAVERSAL_REJECTED", "ARCHIVE_PARENT_TRAVERSAL_REJECTION"),
    )
    for filename, records, expected, marker in cases:
        archive_path = temp_root / filename
        _write_zip(archive_path, list(records))
        _expect_archive_rejection(
            archive_path,
            temp_root / (filename + ".out"),
            expected,
            marker,
        )
    collision = temp_root / "collision.zip"
    _write_zip(
        collision,
        [("app/File.txt", b"a", None), ("app/file.txt", b"b", None)],
    )
    _expect_archive_rejection(
        collision,
        temp_root / "collision.out",
        "ARCHIVE_CASE_COLLISION_REJECTED",
        "ARCHIVE_CASE_COLLISION_REJECTION",
    )
    symlink_mode = (0o120777 << 16)
    symlink = temp_root / "symlink.zip"
    _write_zip(symlink, [("app/link", b"../outside", symlink_mode)])
    _expect_archive_rejection(
        symlink,
        temp_root / "symlink.out",
        "ARCHIVE_SYMLINK_MEMBER_REJECTED",
        "ARCHIVE_REPARSE_POINT_ESCAPE_REJECTION",
    )
def _run_validator(
    project_root: Path,
    relative: str,
    expected_marker: str,
    success_marker: str,
    extra: list[str] | None = None,
) -> None:
    command = [sys.executable, str(project_root / relative)]
    if extra:
        command.extend(extra)
    environment = dict(os.environ)
    existing_pythonpath = environment.get("PYTHONPATH", "").strip()
    environment["PYTHONPATH"] = (
        str(project_root)
        if not existing_pythonpath
        else str(project_root) + os.pathsep + existing_pythonpath
    )
    result = subprocess.run(
        command,
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    if result.returncode != 0 or expected_marker not in result.stdout:
        raise AssertionError(
            success_marker + "\n" + result.stdout + result.stderr
        )
    print(success_marker + ": PASS")
def _validate_regressions(project_root: Path, install_receipt: Path) -> None:
    _run_validator(
        project_root,
        "tools/validate_show_project_generated_portable_archive_exclusion_v1.py",
        "SHOW_PROJECT_PORTABLE_BOX_NO_MIXTURE: PASS",
        "SHOW_PROJECT_PORTABLE_BOX_SEPARATION",
        ["--project-root", str(project_root)],
    )
    _run_validator(
        project_root,
        "portable/validate_installed.py",
        "VALIDATION OK: kanda-reasoner-portable-builder-install-v1r11",
        "PORTABLE_RELEASE_PIPELINE_REGRESSION",
        ["--portable-root", str(project_root / "portable")],
    )
    _run_validator(
        project_root,
        "tools/validate_tool_project_boundary_identity_explicit_selection_v1.py",
        "VALIDATION OK: tool-project-boundary-identity-explicit-selection-v1",
        "RELEASE1_FROZEN_BOUNDARY_REGRESSION",
    )
    _run_validator(
        project_root,
        "tools/validate_owner_scoped_error_memory_and_freeze_memory_v1.py",
        "VALIDATION OK: owner-scoped-error-memory-and-freeze-memory-v1",
        "RELEASE2_MEMORY_OWNERSHIP_REGRESSION",
        [
            "--project-root",
            str(project_root),
            "--install-receipt",
            str(install_receipt),
        ],
    )
def _validate_module_sizes(project_root: Path) -> None:
    modules = (
        "KandaReasonerWindows.spec",
        "kanda_reasoner_app/project_root_resolver.py",
        "kanda_reasoner_app/archive_safety.py",
        "kanda_reasoner_app/source_hygiene/tool_archive_policy.py",
        "kanda_reasoner_app/source_hygiene/freeze_blueprint_validation.py",
        "kanda_reasoner_app/source_hygiene/kilo_workspace_policy.py",
        "kanda_reasoner_app/source_hygiene/kilo_workspace_validation.py",
        "kanda_reasoner_app/source_hygiene/reference_archive_validation.py",
        "kanda_reasoner_app/source_hygiene/workspace_routing_validation.py",
        "kanda_reasoner_app/source_hygiene/external_capture_preview.py",
        "kanda_reasoner_app/reasoner_context_bundle/source_archive_routing.py",
        "kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_inventory.py",
        "portable/policy.py",
        "portable/build.py",
        "portable/archive.py",
        "tools/validate_tool_source_and_archive_hygiene_v1.py",
    )
    for relative in modules:
        count = len((project_root / relative).read_text(encoding="utf-8").splitlines())
        gate(
            "MODULE_SIZE_" + Path(relative).name.upper().replace(".", "_"),
            100 < count < 500,
            f"{relative}:{count}",
        )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--install-receipt", required=True)
    parser.add_argument("--capture-receipt", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=False)
    install_receipt = Path(args.install_receipt).expanduser().resolve(strict=False)
    capture_receipt = Path(args.capture_receipt).expanduser().resolve(strict=False)
    _validate_all_current_paths(project_root)
    validate_local_development_metadata_classification(project_root, gate)
    validate_project_reference_archive_policy(project_root, gate)
    _kilo_validation.validate_kilo_workspace_policy(project_root)
    validate_freeze_blueprint_policy(project_root)
    with tempfile.TemporaryDirectory(prefix="kanda_release3_") as raw:
        temp_root = Path(raw)
        _validate_source_archive_allowlist(project_root, temp_root / "source")
        _validate_archive_safety(temp_root / "archive")
    _validate_capture_absence(project_root, capture_receipt)
    _validate_synthetic_fixture(project_root)
    _validate_pyinstaller_allowlist(project_root)
    _validate_smoke_output(project_root)
    _validate_regressions(project_root, install_receipt)
    _validate_module_sizes(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
