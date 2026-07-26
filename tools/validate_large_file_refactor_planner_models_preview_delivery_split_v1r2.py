# project-path: tools/validate_large_file_refactor_planner_models_preview_delivery_split_v1r2.py
"""Validate the behavior-preserving planner models preview/delivery split."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
import dataclasses
import hashlib
import inspect
import json
import os
import pickle
import shutil
from pathlib import Path
import subprocess
import tempfile
import sys
from typing import Any

FEATURE_ID = "large-file-refactor-planner-models-preview-delivery-split-v1r2"
PUBLIC_MODULE = (
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models"
)
TARGET_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "_preview_delivery_models.py"
)
SUPPORT_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "_model_payload_support.py"
)
EXPECTED_HASHES = {
    TARGET_REL.as_posix(): "a6e721448b9cc473dee4c70a50d61e017b60c1fa701fa5d1369d670ae2952ae7",
    HELPER_REL.as_posix(): "5a18a420e53958de5b37d54568f81190b3111a791cac2a82cb269d346b18c097",
}
EXPECTED_SUPPORT_HASH = (
    "76105f550251437e22ffeb69e326857e26327e976589633ba6b7a0a9960936dc"
)
EXPECTED_CONTRACT_HASH = (
    "96f183971f54a45a3e9bd373f40b92739c810c654ee08dc5d2bb1db864acd77c"
)
EXPECTED_LINES = {TARGET_REL.as_posix(): 381, HELPER_REL.as_posix(): 172}
MOVED_NAMES = (
    "ImportMigrationPreview",
    "ImportMigrationRecord",
    "PreviewArtifactValidationResult",
    "PreviewBundle",
    "PreviewFileDraft",
    "PreviewValidationResult",
    "PreviewWriteResult",
    "ProjectPatchPayloadResult",
)
FORBIDDEN_TARGET_CODES = (
    "MODULE_TOO_LARGE",
    "DUPLICATE_PUBLIC_SYMBOL",
    "PRIVATE_SYMBOL_EXPORTED",
    "MISSING_PUBLIC_SURFACE_CONTROL",
    "PUBLIC_API_INSTABILITY",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_modules() -> None:
    prefix = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    for name in list(sys.modules):
        if name == prefix or name.startswith(prefix + "."):
            sys.modules.pop(name, None)


def contract_hash(models: Any) -> str:
    payload: dict[str, Any] = {
        "all": list(models.__all__),
        "constants": {},
        "classes": {},
    }
    for name in (
        "FEATURE_ID",
        "SCHEMA_VERSION",
        "IDEAL_PHYSICAL_LINES",
        "MAX_PHYSICAL_LINES",
        "MIN_HELPER_PHYSICAL_LINES",
        "PATCH_ALLOWED_STATE",
    ):
        value = getattr(models, name)
        payload["constants"][name] = getattr(value, "value", value)
    for name in models.__all__:
        value = getattr(models, name)
        if not inspect.isclass(value):
            continue
        item: dict[str, Any] = {
            "name": value.__name__,
            "qualname": value.__qualname__,
            "module": value.__module__,
            "doc": value.__doc__,
            "signature": str(inspect.signature(value)),
        }
        if dataclasses.is_dataclass(value):
            params = value.__dataclass_params__
            item["params"] = [
                getattr(params, key)
                for key in ("init", "repr", "eq", "order", "unsafe_hash", "frozen")
            ]
            item["fields"] = []
            for field in dataclasses.fields(value):
                item["fields"].append(
                    {
                        "name": field.name,
                        "type": str(field.type),
                        "default": (
                            None
                            if field.default is dataclasses.MISSING
                            else repr(field.default)
                        ),
                        "factory": (
                            None
                            if field.default_factory is dataclasses.MISSING
                            else getattr(
                                field.default_factory,
                                "__qualname__",
                                repr(field.default_factory),
                            )
                        ),
                    }
                )
            for method_name in ("to_dict", "blocked"):
                if hasattr(value, method_name):
                    method = getattr(value, method_name)
                    item[method_name] = {
                        "sig": str(inspect.signature(method)),
                        "doc": method.__doc__,
                    }
        payload["classes"][name] = item
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_source_identity(root: Path) -> None:
    for relative, expected in EXPECTED_HASHES.items():
        path = root / relative
        if not path.is_file() or sha256_file(path) != expected:
            fail("SOURCE_IDENTITY_MISMATCH: " + relative)
    if sha256_file(root / SUPPORT_REL) != EXPECTED_SUPPORT_HASH:
        fail("MODEL_PAYLOAD_SUPPORT_OWNER_CHANGED")
    print("SOURCE_IDENTITY_GUARD: PASS")
    print("MODEL_PAYLOAD_SUPPORT_OWNER_UNCHANGED: PASS")


def validate_line_law(root: Path) -> None:
    for relative, expected in EXPECTED_LINES.items():
        path = root / relative
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count != expected or not 100 < count < 500:
            fail("LINE_LAW_VIOLATION: " + relative + ":" + str(count))
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("MODULE_TOO_LARGE_PLANNER_MODELS_RESOLVED: PASS")


def validate_dependency_direction(root: Path) -> None:
    helper_text = (root / HELPER_REL).read_text(encoding="utf-8")
    helper_tree = ast.parse(helper_text, filename=HELPER_REL.as_posix())
    if "from .models" in helper_text or PUBLIC_MODULE in helper_text:
        fail("HELPER_TO_FACADE_BACK_REFERENCE")
    public_defs = [
        node.name
        for node in helper_tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]
    if public_defs:
        fail("PRIVATE_HELPER_PUBLIC_OWNER: " + repr(public_defs))
    if "__all__: list[str] = []" not in helper_text:
        fail("PRIVATE_HELPER_SURFACE_CONTROL_MISSING")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("PRIVATE_BACKING_MODEL_OWNERSHIP: PASS")
    print("NO_HELPER_TO_FACADE_BACK_REFERENCE: PASS")


def validate_public_contract(root: Path) -> Any:
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    purge_modules()
    models = __import__(PUBLIC_MODULE, fromlist=["*"])
    if contract_hash(models) != EXPECTED_CONTRACT_HASH:
        fail("PUBLIC_MODEL_CONTRACT_HASH_CHANGED")
    for name in MOVED_NAMES:
        cls = getattr(models, name)
        if cls.__name__ != name or cls.__qualname__ != name:
            fail("PUBLIC_MODEL_NAME_CHANGED: " + name)
        if cls.__module__ != PUBLIC_MODULE:
            fail("PUBLIC_MODEL_MODULE_OWNER_CHANGED: " + name)
    print("PUBLIC_MODELS_FACADE_PRESERVATION: PASS")
    print("DATACLASS_SIGNATURE_FIELD_DEFAULT_IDENTITY: PASS")
    print("ANNOTATION_RUNTIME_IDENTITY: PASS")
    return models


def validate_behavior(models: Any) -> None:
    draft = models.PreviewFileDraft(
        "1.0", "feature", "helper.py", "helper", ["symbol"], "hash", 120
    )
    bundle = models.PreviewBundle(
        "1.0", "feature", "target.py", "hash", "preview", "no_write", True,
        ["symbol"], ["symbol"], [draft], [], [], "ready",
    )
    expected_bundle = {
        "schema_version": "1.0",
        "feature_id": "feature",
        "target_file": "target.py",
        "source_content_hash": "hash",
        "preview_root": "preview",
        "write_mode": "no_write",
        "libcst_available": True,
        "public_api_before": ["symbol"],
        "public_api_after_expected": ["symbol"],
        "files": [draft.to_dict()],
        "validation_blockers": [],
        "risk_flags": [],
        "status": "ready",
    }
    if bundle.to_dict() != expected_bundle:
        fail("PREVIEW_BUNDLE_PAYLOAD_CHANGED")
    record = models.ImportMigrationRecord(
        "1.0", "feature", "consumer.py", "old", "new", "replace", "move"
    )
    migration = models.ImportMigrationPreview(
        "1.0", "feature", "target.py", "hash", False, [record]
    )
    expected_migration = {
        "schema_version": "1.0",
        "feature_id": "feature",
        "target_file": "target.py",
        "source_content_hash": "hash",
        "rewrite_enabled": False,
        "records": [record.to_dict()],
        "blockers": [],
        "warnings": [],
        "status": "preview_only",
    }
    if migration.to_dict() != expected_migration:
        fail("IMPORT_MIGRATION_PAYLOAD_CHANGED")
    for instance in (
        draft,
        bundle,
        record,
        migration,
        models.PreviewValidationResult("1.0", "feature", "passed", []),
        models.PreviewWriteResult("1.0", "feature", "written", "preview", []),
        models.PreviewArtifactValidationResult(
            "1.0", "feature", "passed", "preview", [], True, True, True, "ready"
        ),
        models.ProjectPatchPayloadResult(
            "1.0", "feature", "created", "patch.zip", "manifest.json",
            "preview", [], True, True,
        ),
    ):
        restored = pickle.loads(pickle.dumps(instance))
        if restored != instance or type(restored) is not type(instance):
            fail("PICKLE_ROUNDTRIP_CHANGED: " + type(instance).__name__)
        json.dumps(instance.to_dict(), sort_keys=True)
    print("PREVIEW_DELIVERY_PAYLOAD_BEHAVIOR: PASS")
    print("PICKLE_PUBLIC_IMPORT_PATH_PRESERVATION: PASS")
    print("JSON_SERIALIZATION_CONTRACT: PASS")


def validate_consumers(root: Path, models: Any) -> None:
    count = 0
    target_parent = TARGET_REL.parent
    for path in root.rglob("*.py"):
        if set(path.parts).intersection({".git", ".venv", "venv", "__pycache__"}):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        relative_parent = path.relative_to(root).parent
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            direct = node.module == PUBLIC_MODULE
            sibling = node.level > 0 and node.module == "models" and relative_parent == target_parent
            if not direct and not sibling:
                continue
            count += 1
            for alias in node.names:
                if alias.name != "*" and not hasattr(models, alias.name):
                    fail("CONSUMER_IMPORT_MISSING: " + str(path) + ":" + alias.name)
    if count < 10:
        fail("MODEL_CONSUMER_COVERAGE_TOO_LOW: " + str(count))
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("MODEL_CONSUMER_IMPORT_RECORDS_CHECKED: " + str(count))


def run_command(root: Path, relative: str, markers: tuple[str, ...], label: str) -> None:
    path = root / relative
    if not path.is_file():
        fail(label + "_VALIDATOR_MISSING")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(root),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if output:
        print(output.rstrip())
    if result.returncode != 0:
        fail(label + "_EXIT: " + str(result.returncode))
    for marker in markers:
        if marker not in output:
            fail(label + "_MARKER_MISSING: " + marker)
    print(label + "_REGRESSION: PASS")


def validate_preflight_boundary_regression(root: Path, models: Any) -> None:
    from kanda_reasoner_app.project_support_boundary import (
        canonical_project_support_root,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator import (
        SourceApplyDryRunValidationResult,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract import (
        build_source_apply_preflight_backup_contract,
        write_source_apply_preflight_backup_contract_manifest,
    )

    with tempfile.TemporaryDirectory(
        prefix="kanda_models_preflight_",
        dir=str(root.parent),
    ) as temporary:
        fixture_root = Path(temporary).resolve()
        project_root = fixture_root / (fixture_root.name + "_project")
        target = project_root / "pkg" / "large_module.py"
        target.parent.mkdir(parents=True)
        target.write_text('"""source fixture."""\nVALUE = 1\n', encoding="utf-8")
        source_hash = sha256_file(target)
        support_root = canonical_project_support_root(project_root)
        if support_root.exists():
            fail("PREFLIGHT_FIXTURE_SUPPORT_ROOT_COLLISION")
        preview_root = (
            support_root
            / "large_file_refactor_workbench"
            / "preview"
            / fixture_root.name
        )
        try:
            preview_root.mkdir(parents=True)
            dry_run_manifest = preview_root / "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
            dry_run_manifest.write_text(
                json.dumps({"status": "validated"}) + "\n",
                encoding="utf-8",
            )
            dry_run = SourceApplyDryRunValidationResult(
                schema_version=models.SCHEMA_VERSION,
                feature_id="models-split-preflight-fixture",
                status="source_apply_dry_run_validated",
                target_file=str(target),
                source_content_hash=source_hash,
                preview_root=str(preview_root),
                payload_zip_path=str(preview_root / "payload.zip"),
                final_plan_manifest_path=str(preview_root / "final-plan.json"),
                dry_run_manifest_path=str(dry_run_manifest),
                confirmation_token_required="fixture",
                dry_run_confirmation_present=True,
                dry_run_confirmation_valid=True,
                source_hash_verified=True,
            )
            result = build_source_apply_preflight_backup_contract(
                dry_run,
                active_project_root=str(project_root),
            )
            if result.status != "source_apply_preflight_backup_ready":
                fail("PREFLIGHT_CONTRACT_BLOCKED: " + repr(result.blockers))
            if not result.backup_snapshot_verified or not result.rollback_ready:
                fail("PREFLIGHT_BACKUP_READINESS_CHANGED")
            manifest = write_source_apply_preflight_backup_contract_manifest(result)
            if not manifest.is_file() or sha256_file(target) != source_hash:
                fail("PREFLIGHT_MANIFEST_OR_SOURCE_IDENTITY_CHANGED")
        finally:
            shutil.rmtree(support_root, ignore_errors=True)

    print("PREVIEW_DELIVERY_PREFLIGHT_WINDOWS_CANONICAL_SUPPORT: PASS")
    print("PREVIEW_DELIVERY_PREFLIGHT_REGRESSION: PASS")


def validate_inherited_regressions(root: Path) -> None:
    run_command(
        root,
        "tools/validate_large_file_refactor_workbench_owned_plan_snapshot_v1.py",
        ("BOX_SHIELD: PASS", "NO_LEAK_LOGIC: PASS", "STATUS: IN_SYNC"),
        "MCARD_BOX_SHIELD",
    )
    run_command(
        root,
        "tools/validate_large_file_refactor_workbench_patch2_transaction_core_v1.py",
        ("SERIAL_LANE: PASS", "NO_SOURCE_MUTATION: PASS", "STATUS: IN_SYNC"),
        "WORKBENCH_TRANSACTION",
    )


def validate_architecture(root: Path) -> None:
    script = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--validate"],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if result.returncode != 0 or "Errors: 0" not in output:
        if output:
            print(output.rstrip())
        fail("FULL_ARCHITECTURE_SCAN_ERRORS_NOT_ZERO")
    for line in output.splitlines():
        if not any(rel.as_posix() in line for rel in (TARGET_REL, HELPER_REL)):
            continue
        if any(code in line for code in FORBIDDEN_TARGET_CODES):
            fail("TARGET_ARCHITECTURE_FINDING: " + line.strip())
    print("FULL_PROJECT_ARCHITECTURE_SCAN_ERRORS_ZERO: PASS")
    print("TARGET_PUBLIC_OWNERSHIP_FINDINGS_ZERO: PASS")
    print("BRICK_WALL_ARCHITECTURE_GATES_PRESERVED: PASS")


def validate_ast_audit(root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )
    labels: list[str] = []
    for relative in (TARGET_REL, HELPER_REL):
        result = run_large_module_split_audit(
            root, root / relative, classifier_mode="heuristic"
        )
        classification = result.data["refactor_safety_classification"]
        blockers = list(classification.get("hard_blockers") or [])
        label = str(classification.get("label") or "")
        if blockers:
            fail("AST_SPLIT_HARD_BLOCKERS: " + relative.as_posix() + ":" + repr(blockers))
        if label not in {"SAFE REFACTORING", "RISK REFACTORING"}:
            fail("AST_SPLIT_UNEXPECTED_LABEL: " + relative.as_posix() + ":" + label)
        labels.append(label)
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("AST_DECORATOR_ANNOTATION_RISK_MITIGATED: PASS")
    print("AST_SPLIT_LABELS: " + " | ".join(labels))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--full-project-scan", action="store_true")
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    validate_source_identity(root)
    validate_line_law(root)
    validate_dependency_direction(root)
    models = validate_public_contract(root)
    validate_behavior(models)
    validate_consumers(root, models)
    validate_preflight_boundary_regression(root, models)
    validate_inherited_regressions(root)
    if args.full_project_scan:
        validate_architecture(root)
    validate_ast_audit(root)
    print("LARGE_FILE_REFACTOR_PLANNER_MODELS_PREVIEW_DELIVERY_SPLIT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
