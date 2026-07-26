# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/real_preview_structural_validator.py
"""Structural validation for real moved-code Workbench previews."""
from __future__ import annotations

import ast
import copy
import inspect
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from graphlib import CycleError, TopologicalSorter
from typing import Any

from .cst_real_preview_writer import RealPreviewWriteResult
from .import_migration_preview import build_import_migration_preview
from .models import RefactorPlan, SCHEMA_VERSION
from .module_size_policy import check_resulting_module_size
from .preview_static_quality import inspect_preview_static_quality
from .preview_writer import resolve_preview_root
from .workbench_project_support_paths import preview_root_blockers

__all__ = [
    "REAL_PREVIEW_VALIDATION_FEATURE_ID",
    "RealPreviewStructuralValidationResult",
    "validate_real_preview_structure",
]

REAL_PREVIEW_VALIDATION_FEATURE_ID = "architecture-review-large-file-refactor-structural-preview-validation-v1"
_PREVIEW_HEADER = "KANDA PREVIEW ARTIFACT"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_ai",
    "_show_project_to_ai",
}


@dataclass(frozen=True)
class PreviewFileValidation:
    """Validation evidence for one generated preview file."""

    path: str
    role: str
    physical_lines: int
    ast_parse_ok: bool
    compile_ok: bool
    symbols: list[str]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready record."""
        return asdict(self)


@dataclass(frozen=True)
class RealPreviewStructuralValidationResult:
    """Structural validation report for a real preview bundle."""

    schema_version: str
    feature_id: str
    status: str
    structural_status: str
    behavior_status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    source_hash_verified: bool
    source_mutation_enabled: bool
    import_migration_preview_status: str
    checked_files: list[str]
    report_files: list[str]
    file_results: list[PreviewFileValidation]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready report."""
        data = asdict(self)
        data["file_results"] = [item.to_dict() for item in self.file_results]
        return data


def validate_real_preview_structure(
    *,
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    active_project_root: str,
) -> RealPreviewStructuralValidationResult:
    """Validate generated real preview files without applying source changes."""
    blockers: list[str] = []
    warnings: list[str] = ["BEHAVIOR_VALIDATION_NOT_RUN", "STRUCTURAL_VALIDATION_ONLY"]
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    if preview_result is None:
        blockers.append("REAL_PREVIEW_RESULT_MISSING")
    if blockers or plan is None or preview_result is None:
        return _result(plan, preview_result, active_project_root, blockers, warnings, [], [], "not_generated")

    project_root = Path(active_project_root).resolve()
    preview_root = Path(preview_result.preview_root).resolve()
    checked: list[str] = []
    file_results: list[PreviewFileValidation] = []
    blockers.extend(_preview_root_blockers(project_root, preview_root))
    if preview_result.status != "real_preview_written":
        blockers.append("REAL_PREVIEW_NOT_WRITTEN")
    if preview_result.source_mutation_enabled:
        blockers.append("SOURCE_MUTATION_ENABLED_DURING_PREVIEW")
    source_hash_verified = _hash_file(Path(plan.target_file)) == plan.source_content_hash
    if not source_hash_verified:
        blockers.append("STALE_SOURCE")

    original_symbols = _symbol_map(Path(plan.target_file), blockers)
    allowed_local_imports = _allowed_facade_local_imports(preview_result)
    generated_symbols: dict[str, str] = {}
    generated_graph: dict[str, set[str]] = {}
    for item in preview_result.files:
        path = (preview_root / item.relative_path).resolve()
        result = _validate_one_file(path, item.role, project_root, preview_root)
        file_results.append(result)
        checked.append(str(path))
        blockers.extend(result.blockers)
        warnings.extend(result.warnings)
        if result.ast_parse_ok:
            generated_symbols.update(
                _symbol_map(
                    path,
                    blockers=[],
                    allowed_local_imports=allowed_local_imports,
                )
            )
            generated_graph[path.stem] = _relative_import_dependencies(path)

    blockers.extend(_validate_moved_symbols(plan, original_symbols, generated_symbols))
    blockers.extend(_validate_public_facade(plan, preview_root))
    blockers.extend(_validate_generated_import_graph(generated_graph))
    import_preview = build_import_migration_preview(plan, active_project_root=str(project_root))
    blockers.extend(import_preview.blockers)
    warnings.extend(import_preview.warnings)
    report_files = _write_reports(preview_root, plan, import_preview.to_dict(), blockers, warnings, file_results)
    return _final_result(
        plan=plan,
        preview_result=preview_result,
        source_hash_verified=source_hash_verified,
        checked=checked,
        report_files=report_files,
        file_results=file_results,
        import_status=import_preview.status,
        blockers=blockers,
        warnings=warnings,
    )


def _validate_one_file(path: Path, role: str, project_root: Path, preview_root: Path) -> PreviewFileValidation:
    """Validate one generated preview Python file."""
    blockers: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return PreviewFileValidation(str(path), role, 0, False, False, [], ["PREVIEW_FILE_MISSING"], [])
    blockers.extend(_destination_blockers(path, preview_root, project_root))
    text = path.read_text(encoding="utf-8", errors="replace")
    if _PREVIEW_HEADER not in text:
        blockers.append("PREVIEW_WATERMARK_MISSING")
    lines = text.splitlines()
    size_check = check_resulting_module_size(text, relative_path=path.name)
    blockers.extend(size_check.blockers)
    quality = inspect_preview_static_quality(path, text)
    blockers.extend(quality.blockers)
    warnings.extend(quality.warnings)
    compile_ok = True
    ast_ok = True
    symbols: list[str] = []
    try:
        compile(text, str(path), "exec")
    except SyntaxError:
        compile_ok = False
        blockers.append("PREVIEW_COMPILE_FAILED")
    try:
        tree = ast.parse(text)
        symbols = sorted(_top_level_defs(tree))
    except SyntaxError:
        ast_ok = False
        blockers.append("PREVIEW_AST_PARSE_FAILED")
    return PreviewFileValidation(str(path), role, len(lines), ast_ok, compile_ok, symbols, blockers, warnings)


def _validate_moved_symbols(
    plan: RefactorPlan,
    original_symbols: dict[str, str],
    generated_symbols: dict[str, str],
) -> list[str]:
    """Validate moved symbol bodies are structurally preserved."""
    blockers: list[str] = []
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            continue
        for symbol in module.symbols:
            original = original_symbols.get(symbol)
            generated = generated_symbols.get(symbol)
            if original is None:
                blockers.append(f"ORIGINAL_SYMBOL_NOT_FOUND:{symbol}")
            elif generated is None:
                blockers.append(f"MOVED_SYMBOL_NOT_FOUND_IN_PREVIEW:{symbol}")
            elif original != generated:
                blockers.append(f"MOVED_SYMBOL_BODY_MISMATCH:{symbol}")
    return blockers


def _validate_public_facade(plan: RefactorPlan, preview_root: Path) -> list[str]:
    """Validate public API names remain present in the facade preview."""
    facade = next((item for item in plan.proposed_modules if item.role == "public_facade"), None)
    if facade is None:
        return ["PUBLIC_FACADE_MISSING"]
    path = (preview_root / facade.filename).resolve()
    if not path.exists():
        return ["PUBLIC_FACADE_FILE_MISSING"]
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ["PUBLIC_FACADE_AST_PARSE_FAILED"]
    facade_names = set(_top_level_defs(tree)) | set(_imported_names(tree)) | set(_all_names(tree))
    missing = sorted(name for name in plan.public_api_after_expected if name.isidentifier() and name not in facade_names)
    return [f"PUBLIC_API_SYMBOL_MISSING_FROM_FACADE:{name}" for name in missing]


def _validate_generated_import_graph(graph: dict[str, set[str]]) -> list[str]:
    """Validate relative imports among generated preview modules are acyclic."""
    try:
        TopologicalSorter(graph).static_order()
    except CycleError:
        return ["GENERATED_PREVIEW_IMPORT_GRAPH_CYCLE"]
    return []


def _write_reports(
    preview_root: Path,
    plan: RefactorPlan,
    import_preview: dict[str, Any],
    blockers: list[str],
    warnings: list[str],
    file_results: list[PreviewFileValidation],
) -> list[str]:
    """Write validation and import Preview reports under project support."""
    preview_root.mkdir(parents=True, exist_ok=True)
    report_files: list[str] = []
    targets = {
        "IMPORT_MIGRATION_PLAN.json": import_preview,
        "REAL_PREVIEW_VALIDATION_REPORT.json": {
            "schema_version": SCHEMA_VERSION,
            "feature_id": REAL_PREVIEW_VALIDATION_FEATURE_ID,
            "target_file": plan.target_file,
            "source_content_hash": plan.source_content_hash,
            "structural_status": "STRUCTURAL_FAIL" if blockers else "STRUCTURAL_PASS_WITH_WARNINGS",
            "behavior_status": "BEHAVIOR_VALIDATION_NOT_RUN",
            "file_results": [item.to_dict() for item in file_results],
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        },
    }
    for name, payload in targets.items():
        target = (preview_root / name).resolve()
        if not _is_relative_to(target, preview_root):
            continue
        target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        report_files.append(str(target))
    return report_files


def _symbol_map(
    path: Path,
    blockers: list[str],
    allowed_local_imports: dict[str, tuple[str, tuple[str, ...]]] | None = None,
) -> dict[str, str]:
    """Return normalized AST dumps for top-level functions/classes in a file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        blockers.append(f"SYMBOL_MAP_PARSE_FAILED:{path}")
        return {}
    result: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result[node.name] = _normalized_symbol_dump(
                node,
                allowed_local_import=(allowed_local_imports or {}).get(node.name),
            )
    return result


def _normalized_symbol_dump(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    allowed_local_import: tuple[str, tuple[str, ...]] | None = None,
) -> str:
    """Return AST evidence with documented preview-only normalization."""
    normalized = copy.deepcopy(node)
    if normalized.body and isinstance(normalized.body[0], ast.Expr):
        value = normalized.body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            value.value = inspect.cleandoc(value.value)
    if allowed_local_import and isinstance(normalized, (ast.FunctionDef, ast.AsyncFunctionDef)):
        _remove_expected_local_import(normalized, allowed_local_import)
    return ast.dump(normalized, include_attributes=False)


def _allowed_facade_local_imports(
    preview_result: RealPreviewWriteResult,
) -> dict[str, tuple[str, tuple[str, ...]]]:
    """Return exact synthesized local imports allowed by preview evidence."""
    result: dict[str, tuple[str, tuple[str, ...]]] = {}
    report = preview_result.facade_global_import_insertion or {}
    for item in report.get("insertions", []):
        symbol = str(item.get("symbol_name", ""))
        module = str(item.get("facade_module", ""))
        names = tuple(sorted(str(name) for name in item.get("imported_names", [])))
        if symbol and module and names:
            result[symbol] = (module, names)
    return result


def _remove_expected_local_import(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    expected: tuple[str, tuple[str, ...]],
) -> None:
    """Remove only the exact recorded function-local facade import."""
    module, names = expected
    for index, statement in enumerate(node.body):
        if not isinstance(statement, ast.ImportFrom):
            continue
        actual_names = tuple(sorted(alias.asname or alias.name for alias in statement.names))
        if statement.level == 1 and statement.module == module and actual_names == names:
            del node.body[index]
            return


def _top_level_defs(tree: ast.Module) -> list[str]:
    """Return top-level function and class names."""
    return [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]


def _imported_names(tree: ast.Module) -> list[str]:
    """Return top-level imported names and aliases."""
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            names.extend(alias.asname or alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            names.extend(alias.asname or alias.name for alias in node.names)
    return names


def _all_names(tree: ast.Module) -> list[str]:
    """Return static string names assigned to __all__."""
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            if isinstance(node.value, (ast.List, ast.Tuple)):
                return [item.value for item in node.value.elts if isinstance(item, ast.Constant) and isinstance(item.value, str)]
    return []


def _relative_import_dependencies(path: Path) -> set[str]:
    """Return generated module stems imported relatively by one preview file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return set()
    deps: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
            deps.add(node.module.rsplit(".", 1)[-1])
    return deps


def _preview_root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return blockers for Preview roots outside selected project support."""
    return preview_root_blockers(project_root, preview_root)


def _destination_blockers(path: Path, preview_root: Path, project_root: Path) -> list[str]:
    """Return destination no-leak blockers."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append("PREVIEW_FILE_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append("PREVIEW_FILE_INSIDE_PROJECT_SOURCE")
    if {part.lower() for part in path.parts} & _PROTECTED_PARTS:
        blockers.append("PREVIEW_FILE_INSIDE_PROTECTED_ROOT")
    return blockers


def _hash_file(path: Path) -> str:
    """Return SHA-256 for a file, or empty string on failure."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _final_result(
    *,
    plan: RefactorPlan,
    preview_result: RealPreviewWriteResult,
    source_hash_verified: bool,
    checked: list[str],
    report_files: list[str],
    file_results: list[PreviewFileValidation],
    import_status: str,
    blockers: list[str],
    warnings: list[str],
) -> RealPreviewStructuralValidationResult:
    """Build a final validation result."""
    structural = "STRUCTURAL_FAIL" if blockers else "STRUCTURAL_PASS_WITH_WARNINGS"
    return RealPreviewStructuralValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_VALIDATION_FEATURE_ID,
        status="blocked" if blockers else "passed_with_warnings",
        structural_status=structural,
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        preview_root=preview_result.preview_root,
        source_hash_verified=source_hash_verified,
        source_mutation_enabled=False,
        import_migration_preview_status=import_status,
        checked_files=sorted(set(checked)),
        report_files=sorted(set(report_files)),
        file_results=file_results,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def _result(
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    active_project_root: str,
    blockers: list[str],
    warnings: list[str],
    checked: list[str],
    report_files: list[str],
    import_status: str,
) -> RealPreviewStructuralValidationResult:
    """Build an early blocked validation result."""
    target = plan.target_file if plan else ""
    source_hash = plan.source_content_hash if plan else ""
    preview_root = preview_result.preview_root if preview_result else resolve_preview_root(active_project_root)
    return RealPreviewStructuralValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_VALIDATION_FEATURE_ID,
        status="blocked",
        structural_status="STRUCTURAL_FAIL",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        target_file=target,
        source_content_hash=source_hash,
        preview_root=preview_root,
        source_hash_verified=False,
        source_mutation_enabled=False,
        import_migration_preview_status=import_status,
        checked_files=checked,
        report_files=report_files,
        file_results=[],
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base after resolution."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
