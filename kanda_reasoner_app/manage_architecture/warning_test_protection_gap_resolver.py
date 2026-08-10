# project-path: kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py
"""Plan and apply conservative TEST_PROTECTION_GAP corrections."""
from __future__ import annotations
import ast
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path

from kanda_reasoner_app.project_fire_shield import (
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    assert_fire_shield_write_allowed,
    build_current_fire_shield_context,
    verify_tool_snapshot_unchanged,
)

from kanda_reasoner_app.project_support_boundary import (
    canonical_transient_garbage_root,
)
import re
from collections.abc import Callable, Iterable
from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    WarningFinding,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_family_evidence import (
    score_test_family_evidence,
)
__all__ = [
    "ACTION_ALREADY_PROTECTED",
    "ACTION_LINK_EXISTING_TEST",
    "ACTION_WEB_AI",
    "TestProtectionApplyResult",
    "TestProtectionGapDecision",
    "TestProtectionGapPlan",
    "apply_test_protection_gap_plan",
    "build_test_protection_gap_plan",
    "render_test_protection_link_text",
]
ACTION_ALREADY_PROTECTED = "already_protected"
ACTION_LINK_EXISTING_TEST = "link_existing_test"
ACTION_WEB_AI = "web_ai"
_TEST_PATH_PARTS = {"test", "tests", "validation"}
_AUTO_LINK_MIN_SCORE = 8
ProgressCallback = Callable[[int, int, int, int, str, str], None]
@dataclass(frozen=True, slots=True)
class TestProtectionGapDecision:
    """Describe one conservative resolution decision for a test gap."""
    source_path: str
    module_name: str
    action: str
    candidate_test_path: str
    candidate_score: int
    candidate_reasons: tuple[str, ...]
    source_public_symbols: tuple[str, ...]
    test_sha256_before: str
    reason: str
@dataclass(frozen=True, slots=True)
class TestProtectionGapPlan:
    """Hold all TEST_PROTECTION_GAP specialist decisions."""
    project_root: str
    decisions: tuple[TestProtectionGapDecision, ...]
    @property
    def safe_link_count(self) -> int:
        """Return the number of safe existing-test links that can be applied."""
        return sum(
            1 for item in self.decisions if item.action == ACTION_LINK_EXISTING_TEST
        )
    @property
    def web_ai_count(self) -> int:
        """Return the number of unresolved findings that require Web AI review."""
        return sum(1 for item in self.decisions if item.action == ACTION_WEB_AI)
    @property
    def already_protected_count(self) -> int:
        """Return stale findings already protected by a direct import."""
        return sum(
            1 for item in self.decisions if item.action == ACTION_ALREADY_PROTECTED
        )
@dataclass(frozen=True, slots=True)
class TestProtectionApplyResult:
    """Report the result of applying safe test-protection links."""
    applied_count: int
    changed_files: tuple[str, ...]
    backup_root: str
def _normalize_relative_path(value: str) -> str:
    return str(value).replace("\\", "/").strip().strip("/")
def _module_name_from_path(path: str) -> str:
    normalized = _normalize_relative_path(path)
    if normalized.endswith(".py"):
        normalized = normalized[:-3]
    if normalized.endswith("/__init__"):
        normalized = normalized[: -len("/__init__")]
    return normalized.replace("/", ".")
def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")
def _literal_dunder_all(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            return ()
        if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
            return tuple(value)
        return ()
    return ()
def _public_symbols_from_source(path: Path) -> tuple[str, ...]:
    tree = ast.parse(_read_utf8(path), filename=str(path))
    explicit = _literal_dunder_all(tree)
    if explicit:
        return explicit
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
    return tuple(sorted(set(names)))
def _is_test_path(relative_path: Path) -> bool:
    parts = {part.lower() for part in relative_path.parts[:-1]}
    name = relative_path.name.lower()
    return (
        bool(parts & _TEST_PATH_PARTS)
        or name.startswith("test_")
        or name.endswith("_test.py")
    ) and relative_path.suffix.lower() == ".py"
def _iter_test_files(project_root: Path) -> tuple[Path, ...]:
    candidates: list[Path] = []
    for path in project_root.rglob("*.py"):
        if not path.is_file():
            continue
        relative = path.relative_to(project_root)
        if _is_test_path(relative):
            candidates.append(path)
    return tuple(sorted(candidates))
def _import_evidence(tree: ast.Module) -> tuple[set[str], set[tuple[str, str]]]:
    modules: set[str] = set()
    imported_symbols: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
            for alias in node.names:
                imported_symbols.add((node.module, alias.name))
    return modules, imported_symbols
def _ancestor_modules(module_name: str) -> tuple[str, ...]:
    parts = module_name.split(".")
    return tuple(".".join(parts[:index]) for index in range(1, len(parts)))
def _candidate_score(
    *,
    source_module: str,
    source_symbols: tuple[str, ...],
    source_stem: str,
    test_path: Path,
    test_text: str,
    test_tree: ast.Module,
) -> tuple[int, tuple[str, ...], bool]:
    imported_modules, imported_symbols = _import_evidence(test_tree)
    if source_module in imported_modules:
        return 100, ("direct_module_import",), True
    score = 0
    reasons: list[str] = []
    ancestors = set(_ancestor_modules(source_module))
    public_symbol_set = set(source_symbols)
    facade_hits = sorted(
        symbol
        for module, symbol in imported_symbols
        if module in ancestors and symbol in public_symbol_set
    )
    if facade_hits:
        score += min(12, 8 + (len(facade_hits) - 1) * 2)
        reasons.append("imports_public_symbol_from_ancestor_facade")
    lower_text = test_text.lower()
    if source_module.lower() in lower_text:
        score += 6
        reasons.append("references_source_module")
    symbol_hits = [
        symbol for symbol in source_symbols if re.search(rf"\b{re.escape(symbol)}\b", test_text)
    ]
    if symbol_hits:
        score += min(4, len(symbol_hits))
        reasons.append("references_public_symbol")
    test_stem = test_path.stem.lower()
    if source_stem and source_stem in test_stem:
        score += 4
        reasons.append("test_filename_matches_source_stem")
    family = score_test_family_evidence(
        source_module=source_module,
        source_stem=source_stem,
        test_path=test_path,
        imported_modules=imported_modules,
        source_public_symbols=source_symbols,
        test_text=test_text,
    )
    score += family.score_bonus
    reasons.extend(family.reasons)
    return score, tuple(sorted(set(reasons))), False
def _decision_for_finding(
    project_root: Path,
    finding: WarningFinding,
    test_files: tuple[Path, ...],
) -> TestProtectionGapDecision:
    source_relative = _normalize_relative_path(finding.path)
    source_path = project_root / Path(source_relative)
    module_name = _module_name_from_path(source_relative)
    if not source_path.is_file():
        return TestProtectionGapDecision(
            source_path=source_relative,
            module_name=module_name,
            action=ACTION_WEB_AI,
            candidate_test_path="",
            candidate_score=0,
            candidate_reasons=(),
            source_public_symbols=(),
            test_sha256_before="",
            reason="Source file is missing from the selected project root.",
        )
    try:
        public_symbols = _public_symbols_from_source(source_path)
    except (OSError, SyntaxError, UnicodeError) as exc:
        return TestProtectionGapDecision(
            source_path=source_relative,
            module_name=module_name,
            action=ACTION_WEB_AI,
            candidate_test_path="",
            candidate_score=0,
            candidate_reasons=(),
            source_public_symbols=(),
            test_sha256_before="",
            reason=f"Source contract could not be parsed safely: {type(exc).__name__}.",
        )
    scored: list[tuple[int, str, tuple[str, ...], bool, str]] = []
    for test_path in test_files:
        try:
            test_text = _read_utf8(test_path)
            test_tree = ast.parse(test_text, filename=str(test_path))
        except (OSError, SyntaxError, UnicodeError):
            continue
        score, reasons, direct = _candidate_score(
            source_module=module_name,
            source_symbols=public_symbols,
            source_stem=source_path.stem.lower(),
            test_path=test_path,
            test_text=test_text,
            test_tree=test_tree,
        )
        if score <= 0:
            continue
        relative_test = test_path.relative_to(project_root).as_posix()
        scored.append((score, relative_test, reasons, direct, _sha256_text(test_text)))
    scored.sort(key=lambda item: (-item[0], item[1]))
    if not scored:
        return TestProtectionGapDecision(
            source_path=source_relative,
            module_name=module_name,
            action=ACTION_WEB_AI,
            candidate_test_path="",
            candidate_score=0,
            candidate_reasons=(),
            source_public_symbols=public_symbols,
            test_sha256_before="",
            reason="No existing test has strong structural relationship evidence.",
        )
    score, test_relative, reasons, direct, test_hash = scored[0]
    if direct:
        return TestProtectionGapDecision(
            source_path=source_relative,
            module_name=module_name,
            action=ACTION_ALREADY_PROTECTED,
            candidate_test_path=test_relative,
            candidate_score=score,
            candidate_reasons=reasons,
            source_public_symbols=public_symbols,
            test_sha256_before=test_hash,
            reason="A direct module import already exists; rerun the architecture audit.",
        )
    has_contract_evidence = (
        "imports_public_symbol_from_ancestor_facade" in reasons
        or (
            "strong_existing_test_family" in reasons
            and "references_source_public_symbol" in reasons
        )
        or (
            "test_filename_matches_source_stem" in reasons
            and "imports_source_package_sibling" in reasons
        )
        or (
            "references_source_module" in reasons
            and "references_public_symbol" in reasons
        )
    )
    if score >= _AUTO_LINK_MIN_SCORE and has_contract_evidence:
        return TestProtectionGapDecision(
            source_path=source_relative,
            module_name=module_name,
            action=ACTION_LINK_EXISTING_TEST,
            candidate_test_path=test_relative,
            candidate_score=score,
            candidate_reasons=reasons,
            source_public_symbols=public_symbols,
            test_sha256_before=test_hash,
            reason=(
                "Existing test already exercises or imports the public contract; "
                "a TYPE_CHECKING direct module link is a bounded metadata correction."
            ),
        )
    return TestProtectionGapDecision(
        source_path=source_relative,
        module_name=module_name,
        action=ACTION_WEB_AI,
        candidate_test_path=test_relative,
        candidate_score=score,
        candidate_reasons=reasons,
        source_public_symbols=public_symbols,
        test_sha256_before=test_hash,
        reason="Relationship evidence is insufficient for an automatic test-protection link.",
    )
def build_test_protection_gap_plan(
    project_root: str | Path,
    findings: Iterable[WarningFinding],
    *,
    progress_callback: ProgressCallback | None = None,
) -> TestProtectionGapPlan:
    """Build a conservative plan and optionally report real item progress."""
    root = Path(project_root).expanduser().resolve()
    test_files = _iter_test_files(root)
    eligible = tuple(
        finding
        for finding in findings
        if finding.code == "TEST_PROTECTION_GAP" and finding.path != "."
    )
    total = len(eligible)
    decisions: list[TestProtectionGapDecision] = []
    done = 0
    web_ai = 0
    for finding in eligible:
        decision = _decision_for_finding(root, finding, test_files)
        decisions.append(decision)
        if decision.action == ACTION_WEB_AI:
            web_ai += 1
        else:
            done += 1
        if progress_callback is not None:
            progress_callback(
                total,
                total - len(decisions),
                done,
                web_ai,
                decision.source_path,
                decision.action,
            )
    return TestProtectionGapPlan(project_root=str(root), decisions=tuple(decisions))
def _safe_alias(module_name: str) -> str:
    stem = module_name.rsplit(".", 1)[-1]
    safe = re.sub(r"[^a-zA-Z0-9_]", "_", stem)
    return "_test_protection_" + safe
def _future_import_end_line(tree: ast.Module) -> int:
    line = 0
    body = list(tree.body)
    index = 0
    if body and isinstance(body[0], ast.Expr):
        value = body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            line = body[0].end_lineno or body[0].lineno
            index = 1
    while index < len(body):
        node = body[index]
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            line = node.end_lineno or node.lineno
            index += 1
            continue
        break
    return line
def _has_type_checking_import(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            if any(alias.name == "TYPE_CHECKING" for alias in node.names):
                return True
    return False
def _render_linked_test_text(test_text: str, module_name: str) -> str:
    tree = ast.parse(test_text)
    imported_modules, _ = _import_evidence(tree)
    if module_name in imported_modules:
        return test_text
    lines = test_text.splitlines(keepends=True)
    insert_after = _future_import_end_line(tree)
    block_lines: list[str] = []
    if not _has_type_checking_import(tree):
        block_lines.append("from typing import TYPE_CHECKING\n")
    block_lines.extend(
        [
            "\n",
            "if TYPE_CHECKING:\n",
            f"    import {module_name} as {_safe_alias(module_name)}\n",
            "\n",
        ]
    )
    lines[insert_after:insert_after] = block_lines
    rendered = "".join(lines)
    ast.parse(rendered)
    return rendered
def render_test_protection_link_text(test_text: str, module_name: str) -> str:
    """Render one guarded direct test-protection link without filesystem mutation."""
    return _render_linked_test_text(test_text, module_name)
def _backup_root(project_root: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    daily_work = canonical_transient_garbage_root(project_root)
    return daily_work / "warning_heuristic_resolver" / "test_protection_gap" / timestamp
def apply_test_protection_gap_plan(
    plan: TestProtectionGapPlan,
) -> TestProtectionApplyResult:
    """Apply only source-fresh safe existing-test links from one plan."""
    root = Path(plan.project_root).resolve()
    selected = [
        item for item in plan.decisions if item.action == ACTION_LINK_EXISTING_TEST
    ]
    if not selected:
        return TestProtectionApplyResult(0, (), "")
    rendered_by_path: dict[Path, str] = {}
    original_by_path: dict[Path, str] = {}
    for decision in selected:
        test_path = root / Path(decision.candidate_test_path)
        current = _read_utf8(test_path)
        current_hash = _sha256_text(current)
        if current_hash != decision.test_sha256_before:
            raise RuntimeError(
                "TEST SOURCE FRESHNESS CONFLICT: " + decision.candidate_test_path
            )
        original_by_path.setdefault(test_path, current)
        base_text = rendered_by_path.get(test_path, current)
        rendered_by_path[test_path] = _render_linked_test_text(
            base_text,
            decision.module_name,
        )
    backup_root = _backup_root(root)
    for test_path, original in original_by_path.items():
        relative = test_path.relative_to(root)
        backup_path = backup_root / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_text(original, encoding="utf-8", newline="")
    changed: list[str] = []
    fire_shield = build_current_fire_shield_context(
        project_root=root,
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="test-protection-gap-apply",
    )
    for test_path, rendered in sorted(rendered_by_path.items(), key=lambda item: str(item[0])):
        original = original_by_path[test_path]
        if rendered == original:
            continue
        payload = rendered.encode("utf-8")
        assert_fire_shield_write_allowed(fire_shield, test_path, operation="REPLACE")
        assert_fire_shield_payload_bytes_allowed(fire_shield, test_path, payload)
        temporary = test_path.with_name(test_path.name + ".warning_resolver_tmp")
        temporary.write_bytes(payload)
        os.replace(temporary, test_path)
        changed.append(test_path.relative_to(root).as_posix())
    verify_tool_snapshot_unchanged(fire_shield)
    return TestProtectionApplyResult(
        applied_count=len(selected),
        changed_files=tuple(changed),
        backup_root=str(backup_root),
    )
