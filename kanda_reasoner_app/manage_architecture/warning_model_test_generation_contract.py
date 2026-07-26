# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py
"""Validate bounded Local AI proposals that extend or create focused Python tests."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from typing import Any

__all__ = [
    "ACTION_CREATE_FOCUSED_TEST",
    "ACTION_EXTEND_EXISTING_TEST",
    "ACTION_MODEL_TEST_CHANGE",
    "ModelTestMutationProposal",
    "apply_mutation_to_text",
    "build_mutation_proposal",
    "normalize_test_path",
]

ACTION_EXTEND_EXISTING_TEST = "extend_existing_test"
ACTION_CREATE_FOCUSED_TEST = "create_focused_test"
ACTION_MODEL_TEST_CHANGE = "model_test_change"
_MIN_MUTATION_CONFIDENCE = 0.85
_MAX_GENERATED_TEST_CHARS = 16000
_TEST_ROOTS = {"test", "tests", "validation"}
_BANNED_IMPORT_ROOTS = {
    "requests",
    "socket",
    "subprocess",
    "urllib",
    "httpx",
    "ftplib",
    "telnetlib",
}
_BANNED_CALL_NAMES = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.call",
    "subprocess.Popen",
}


@dataclass(frozen=True, slots=True)
class ModelTestMutationProposal:
    """Describe one AI-authored test-only change that passed static contract gates."""

    source_path: str
    module_name: str
    action: str
    target_test_path: str
    generated_test_code: str
    rendered_test_text: str
    test_sha256_before: str
    confidence: float
    reason: str
    model_name: str


def normalize_test_path(value: str) -> str:
    """Normalize a project-relative test path without allowing traversal."""
    normalized = str(value or "").replace("\\", "/").strip().strip("/")
    if not normalized or normalized.startswith("../") or "/../" in normalized:
        return ""
    return normalized


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _test_path_allowed(relative: str) -> bool:
    path = Path(relative)
    if path.suffix.lower() != ".py":
        return False
    parts = {part.lower() for part in path.parts[:-1]}
    name = path.name.lower()
    return bool(parts & _TEST_ROOTS) and (
        name.startswith("test_") or name.endswith("_test.py")
    )


def _call_name(node: ast.Call) -> str:
    try:
        return ast.unparse(node.func)
    except Exception:
        return ""


def _has_assertion_evidence(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            if isinstance(node.test, ast.Constant) and bool(node.test.value) is True:
                continue
            return True
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name == "pytest.raises" or re.search(r"\.assert[A-Z_a-z]", name):
            return True
    return False


def _directly_imports_module(tree: ast.Module, module_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == module_name for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom) and node.module == module_name:
            return True
    return False


def _references_public_contract(
    tree: ast.Module,
    public_symbols: tuple[str, ...],
) -> bool:
    if not public_symbols:
        return True
    names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }
    attrs = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    }
    return bool(set(public_symbols) & (names | attrs))


def _validate_top_level_shape(tree: ast.Module) -> None:
    allowed = (
        ast.Expr,
        ast.Import,
        ast.ImportFrom,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
    )
    for node in tree.body:
        if not isinstance(node, allowed):
            raise ValueError(
                "Generated test code may contain only imports, a module docstring, and test functions."
            )
        if isinstance(node, ast.Expr):
            if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
                raise ValueError("Generated test code has executable top-level expressions.")


def _validate_dangerous_operations(tree: ast.Module) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots = {alias.name.partition(".")[0] for alias in node.names}
            if roots & _BANNED_IMPORT_ROOTS:
                raise ValueError("Generated test imports a blocked external/process module.")
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.partition(".")[0] in _BANNED_IMPORT_ROOTS:
                raise ValueError("Generated test imports a blocked external/process module.")
        elif isinstance(node, ast.Call):
            if _call_name(node) in _BANNED_CALL_NAMES:
                raise ValueError("Generated test calls a blocked dynamic/process execution API.")


def _validate_test_functions(tree: ast.Module) -> None:
    test_functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]
    if not test_functions:
        raise ValueError("Generated test code must define at least one test_ function.")
    if not _has_assertion_evidence(tree):
        raise ValueError("Generated test code must contain assertion or expected-exception evidence.")


def _validate_generated_code(
    code: str,
    *,
    module_name: str,
    public_symbols: tuple[str, ...],
) -> ast.Module:
    if not code.strip():
        raise ValueError("Generated test code is empty.")
    if len(code) > _MAX_GENERATED_TEST_CHARS:
        raise ValueError("Generated test code exceeds the bounded size contract.")
    tree = ast.parse(code)
    _validate_top_level_shape(tree)
    _validate_dangerous_operations(tree)
    _validate_test_functions(tree)
    if not _directly_imports_module(tree, module_name):
        raise ValueError("Generated test code must directly import the exact source module.")
    if not _references_public_contract(tree, public_symbols):
        raise ValueError("Generated test code does not reference the supplied public contract.")
    return tree


def apply_mutation_to_text(
    existing_text: str,
    *,
    action: str,
    generated_code: str,
) -> str:
    """Render one validated test mutation without touching the filesystem."""
    if action == ACTION_CREATE_FOCUSED_TEST:
        rendered = generated_code.rstrip() + "\n"
    elif action == ACTION_EXTEND_EXISTING_TEST:
        prefix = existing_text.rstrip()
        rendered = prefix + "\n\n" + generated_code.strip() + "\n"
    else:
        raise ValueError("Unsupported test mutation action: " + action)
    ast.parse(rendered)
    return rendered


def _candidate_paths(context: Any) -> set[str]:
    return {
        normalize_test_path(str(item.test_path))
        for item in getattr(context, "candidates", ())
    }


def build_mutation_proposal(
    project_root: Path,
    context: Any,
    payload: dict[str, Any],
    model_name: str,
) -> ModelTestMutationProposal:
    """Convert one model payload into a statically validated test-only proposal."""
    action = str(payload.get("action", "")).strip()
    if action not in {ACTION_EXTEND_EXISTING_TEST, ACTION_CREATE_FOCUSED_TEST}:
        raise ValueError("Payload does not request a supported test mutation action.")
    try:
        confidence = float(payload.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    if confidence < _MIN_MUTATION_CONFIDENCE:
        raise ValueError("Test mutation confidence is below the fail-closed threshold.")
    target = normalize_test_path(str(payload.get("target_test_path", "")))
    if not _test_path_allowed(target):
        raise ValueError("Target test path is not an allowed project-relative test path.")
    suggested_new = normalize_test_path(str(getattr(context, "suggested_new_test_path", "")))
    candidates = _candidate_paths(context)
    target_path = project_root / Path(target)
    if action == ACTION_EXTEND_EXISTING_TEST:
        if target not in candidates or not target_path.is_file():
            raise ValueError("Local AI may extend only an exact supplied existing test candidate.")
        existing_text = target_path.read_text(encoding="utf-8-sig")
        before_hash = _sha256_text(existing_text)
    else:
        if not suggested_new or target != suggested_new:
            raise ValueError("Local AI may create only the exact deterministic suggested test path.")
        if target_path.exists():
            raise ValueError("Suggested new test path already exists.")
        existing_text = ""
        before_hash = ""
    code = str(payload.get("test_code", ""))
    _validate_generated_code(
        code,
        module_name=str(context.module_name),
        public_symbols=tuple(context.public_symbols),
    )
    rendered = apply_mutation_to_text(
        existing_text,
        action=action,
        generated_code=code,
    )
    reason = str(payload.get("reason", "")).strip()[:500]
    return ModelTestMutationProposal(
        source_path=str(context.source_path),
        module_name=str(context.module_name),
        action=action,
        target_test_path=target,
        generated_test_code=code,
        rendered_test_text=rendered,
        test_sha256_before=before_hash,
        confidence=confidence,
        reason=reason or "Local AI proposed a bounded focused test change.",
        model_name=model_name,
    )
