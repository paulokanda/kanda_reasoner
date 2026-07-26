# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py
"""Select AST-grounded source and test evidence for Local AI test protection review."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import re

__all__ = [
    "SemanticSourceEvidence",
    "SemanticTestEvidence",
    "build_semantic_source_evidence",
    "build_semantic_test_evidence",
]

_ROLE_TOKENS = {
    "action",
    "adapter",
    "builder",
    "contract",
    "controller",
    "dialog",
    "engine",
    "formatting",
    "gui",
    "intake",
    "layout",
    "manifest",
    "models",
    "orchestration",
    "orchestrator",
    "policy",
    "qt",
    "runtime",
    "service",
    "spec",
    "store",
    "worker",
}
_NOISE_TOKENS = {"py", "test", "tests", "validation", "validate"}
_MAX_SOURCE_CHARS = 9000
_MAX_TEST_CHARS = 5200


@dataclass(frozen=True, slots=True)
class SemanticSourceEvidence:
    """Hold focused public-contract and dependency evidence from one source module."""

    excerpt: str
    imports: tuple[str, ...]
    public_signatures: tuple[str, ...]
    referenced_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SemanticTestEvidence:
    """Hold focused behavioral evidence extracted from one test module."""

    excerpt: str
    imported_modules: tuple[str, ...]
    test_functions: tuple[str, ...]
    fixtures: tuple[str, ...]
    mock_targets: tuple[str, ...]
    assertion_symbols: tuple[str, ...]
    symbol_hits: tuple[str, ...]
    token_overlap: tuple[str, ...]


def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _tokens(value: str) -> set[str]:
    raw = re.findall(r"[a-z0-9]+", value.lower().replace("\\", "/"))
    return {
        token
        for token in raw
        if token not in _NOISE_TOKENS
        and token not in _ROLE_TOKENS
        and not re.fullmatch(r"v\d+", token)
        and not token.isdigit()
    }


def _node_text(lines: list[str], node: ast.AST) -> str:
    start = max(0, int(getattr(node, "lineno", 1)) - 1)
    end = int(getattr(node, "end_lineno", start + 1))
    return "".join(lines[start:end]).rstrip()


def _signature(node: ast.AST) -> str:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return ""
    if isinstance(node, ast.ClassDef):
        bases = [ast.unparse(base) for base in node.bases]
        return "class " + node.name + ("(" + ", ".join(bases) + ")" if bases else "")
    prefix = "async def " if isinstance(node, ast.AsyncFunctionDef) else "def "
    return prefix + node.name + ast.unparse(node.args)


def _module_import_lines(tree: ast.Module, lines: list[str]) -> tuple[str, ...]:
    result: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            text = _node_text(lines, node)
            if text:
                result.append(text)
    return tuple(result)


def _module_import_names(tree: ast.Module) -> tuple[str, ...]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return tuple(sorted(names))


def _referenced_names(nodes: list[ast.AST]) -> tuple[str, ...]:
    names = {
        child.id
        for node in nodes
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
    }
    return tuple(sorted(names))


def build_semantic_source_evidence(
    path: Path,
    public_symbols: tuple[str, ...],
) -> SemanticSourceEvidence:
    """Build an AST-focused source excerpt instead of a raw file prefix."""
    text = _read_utf8(path)
    tree = ast.parse(text, filename=str(path))
    lines = text.splitlines(keepends=True)
    imports = _module_import_lines(tree, lines)
    public_set = set(public_symbols)
    selected_nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name in public_set
    ]
    if not selected_nodes:
        selected_nodes = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not node.name.startswith("_")
        ][:8]
    signatures = tuple(filter(None, (_signature(node) for node in selected_nodes)))
    chunks: list[str] = []
    if imports:
        chunks.append("# IMPORTS\n" + "\n".join(imports))
    if signatures:
        chunks.append("# PUBLIC SIGNATURES\n" + "\n".join(signatures))
    for node in selected_nodes:
        rendered = _node_text(lines, node)
        if rendered:
            chunks.append("# PUBLIC CONTRACT BODY\n" + rendered)
    excerpt = "\n\n".join(chunks)
    if len(excerpt) > _MAX_SOURCE_CHARS:
        excerpt = excerpt[:_MAX_SOURCE_CHARS]
    return SemanticSourceEvidence(
        excerpt=excerpt,
        imports=_module_import_names(tree),
        public_signatures=signatures,
        referenced_names=_referenced_names(selected_nodes),
    )


def _call_target_name(node: ast.Call) -> str:
    try:
        return ast.unparse(node.func)
    except Exception:
        return ""


def _mock_targets(tree: ast.Module) -> tuple[str, ...]:
    targets: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_target_name(node)
        if not any(marker in name for marker in ("patch", "monkeypatch", "mocker")):
            continue
        for arg in node.args[:2]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                targets.add(arg.value)
    return tuple(sorted(targets))


def _assertion_symbols(tree: ast.Module) -> tuple[str, ...]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            names.update(
                child.id
                for child in ast.walk(node.test)
                if isinstance(child, ast.Name)
            )
        elif isinstance(node, ast.With):
            for item in node.items:
                text = ast.unparse(item.context_expr)
                if "pytest.raises" in text:
                    names.add("pytest.raises")
    return tuple(sorted(names))


def _fixture_names(node: ast.AST) -> tuple[str, ...]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return ()
    positional = [arg.arg for arg in node.args.posonlyargs + node.args.args]
    keyword_only = [arg.arg for arg in node.args.kwonlyargs]
    return tuple(positional + keyword_only)


def _relevance_score(
    node: ast.AST,
    *,
    source_tokens: set[str],
    public_symbols: tuple[str, ...],
) -> int:
    text = ast.unparse(node)
    node_tokens = _tokens(text)
    score = 3 * len(source_tokens & node_tokens)
    score += 4 * sum(1 for symbol in public_symbols if re.search(rf"\b{re.escape(symbol)}\b", text))
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        score += 2 * len(source_tokens & _tokens(node.name))
    return score


def build_semantic_test_evidence(
    path: Path,
    *,
    source_stem: str,
    public_symbols: tuple[str, ...],
) -> SemanticTestEvidence:
    """Build focused test evidence around relevant functions, fixtures, mocks, and asserts."""
    text = _read_utf8(path)
    tree = ast.parse(text, filename=str(path))
    lines = text.splitlines(keepends=True)
    source_tokens = _tokens(source_stem)
    test_nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]
    ranked = sorted(
        test_nodes,
        key=lambda node: (-_relevance_score(node, source_tokens=source_tokens, public_symbols=public_symbols), node.lineno),
    )
    selected = ranked[:6]
    imports = _module_import_lines(tree, lines)
    chunks: list[str] = []
    if imports:
        chunks.append("# TEST IMPORTS\n" + "\n".join(imports))
    for node in selected:
        rendered = _node_text(lines, node)
        if rendered:
            chunks.append("# RELEVANT TEST\n" + rendered)
    excerpt = "\n\n".join(chunks)
    if not excerpt:
        excerpt = text[:_MAX_TEST_CHARS]
    elif len(excerpt) > _MAX_TEST_CHARS:
        excerpt = excerpt[:_MAX_TEST_CHARS]
    symbol_hits = tuple(
        symbol
        for symbol in public_symbols
        if re.search(rf"\b{re.escape(symbol)}\b", text)
    )
    fixtures = sorted({name for node in selected for name in _fixture_names(node)})
    relative_name = path.as_posix()
    return SemanticTestEvidence(
        excerpt=excerpt,
        imported_modules=_module_import_names(tree),
        test_functions=tuple(node.name for node in selected),
        fixtures=tuple(fixtures),
        mock_targets=_mock_targets(tree),
        assertion_symbols=_assertion_symbols(tree),
        symbol_hits=symbol_hits,
        token_overlap=tuple(sorted(source_tokens & _tokens(relative_name))),
    )
