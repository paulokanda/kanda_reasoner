# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py
"""Semantic source/test context and strict response contract for Warning Local AI Resolver."""
from __future__ import annotations
import ast
from collections.abc import Callable
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from kanda_reasoner_app.manage_architecture.ai_review.adapter import (
    AUTO_MODEL_LABEL,
    Tab1AIReviewAdapter,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_semantic_evidence import (
    build_semantic_source_evidence,
    build_semantic_test_evidence,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_LINK_EXISTING_TEST,
    ACTION_WEB_AI,
    TestProtectionGapDecision,
)
__all__ = [
    "ModelResolverError",
    "ModelTestCandidateEvidence",
    "ModelTestSourceContext",
    "build_model_source_context",
    "build_model_test_messages",
    "decision_from_model_payload",
    "iter_test_files",
    "parse_model_test_response",
    "resolve_selected_model",
]
_MAX_CANDIDATES_PER_SOURCE = 8
_MIN_AI_LINK_CONFIDENCE = 0.90
_TEST_PATH_PARTS = {"test", "tests", "validation"}
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
ModelLister = Callable[[], list[str]]
class ModelResolverError(RuntimeError):
    """Raised when the selected model route cannot run safely."""
@dataclass(frozen=True, slots=True)
class ModelTestCandidateEvidence:
    """Describe one semantically ranked existing test candidate supplied to Local AI."""
    test_path: str
    test_sha256: str
    score: int
    sibling_import: bool
    token_overlap: tuple[str, ...]
    symbol_hits: tuple[str, ...]
    imported_modules: tuple[str, ...]
    test_functions: tuple[str, ...]
    fixtures: tuple[str, ...]
    mock_targets: tuple[str, ...]
    assertion_symbols: tuple[str, ...]
    excerpt: str
@dataclass(frozen=True, slots=True)
class ModelTestSourceContext:
    """AST-focused source and candidate-test context for one unresolved gap."""
    source_path: str
    module_name: str
    public_symbols: tuple[str, ...]
    source_excerpt: str
    source_imports: tuple[str, ...]
    public_signatures: tuple[str, ...]
    suggested_new_test_path: str
    candidates: tuple[ModelTestCandidateEvidence, ...]
def normalize_relative_path(value: str) -> str:
    return str(value).replace("\\", "/").strip().strip("/")
def module_name_from_path(path: str) -> str:
    normalized = normalize_relative_path(path)
    if normalized.endswith(".py"):
        normalized = normalized[:-3]
    if normalized.endswith("/__init__"):
        normalized = normalized[: -len("/__init__")]
    return normalized.replace("/", ".")
def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
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
def is_test_path(relative_path: Path) -> bool:
    parts = {part.lower() for part in relative_path.parts[:-1]}
    name = relative_path.name.lower()
    return (
        bool(parts & _TEST_PATH_PARTS)
        or name.startswith("test_")
        or name.endswith("_test.py")
    ) and relative_path.suffix.lower() == ".py"
def iter_test_files(project_root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in project_root.rglob("*.py")
            if path.is_file() and is_test_path(path.relative_to(project_root))
        )
    )
def _package_sibling_import(source_module: str, imported: set[str]) -> bool:
    package, separator, _ = source_module.rpartition(".")
    if not separator:
        return False
    prefix = package + "."
    return any(item != source_module and item.startswith(prefix) for item in imported)
def _public_symbols(path: Path) -> tuple[str, ...]:
    tree = ast.parse(_read_utf8(path), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (TypeError, ValueError):
            break
        if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
            return tuple(value)
    names = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]
    return tuple(sorted(set(names)))
def _suggested_new_test_path(root: Path, source_stem: str) -> str:
    safe_stem = re.sub(r"[^a-zA-Z0-9_]+", "_", source_stem).strip("_").lower()
    candidates = (
        f"tests/test_{safe_stem}.py",
        f"validation/test_{safe_stem}_protection_v1.py",
    )
    for relative in candidates:
        if not (root / relative).exists():
            return relative
    index = 2
    while True:
        relative = f"validation/test_{safe_stem}_protection_v{index}.py"
        if not (root / relative).exists():
            return relative
        index += 1
def _candidate_evidence(
    root: Path,
    source_module: str,
    source_stem: str,
    public_symbols: tuple[str, ...],
    test_path: Path,
    preferred_test_path: str,
) -> ModelTestCandidateEvidence | None:
    try:
        text = _read_utf8(test_path)
        semantic = build_semantic_test_evidence(
            test_path,
            source_stem=source_stem,
            public_symbols=public_symbols,
        )
    except (OSError, SyntaxError, UnicodeError):
        return None
    imported = set(semantic.imported_modules)
    relative = test_path.relative_to(root).as_posix()
    sibling = _package_sibling_import(source_module, imported)
    overlap = tuple(sorted(_tokens(source_stem) & _tokens(relative)))
    symbol_hits = semantic.symbol_hits
    direct_mock_hits = tuple(
        target
        for target in semantic.mock_targets
        if target == source_module or target.startswith(source_module + ".")
    )
    score = 5 if sibling else 0
    score += min(12, 3 * len(overlap))
    score += min(12, 3 * len(symbol_hits))
    score += min(12, 6 * len(direct_mock_hits))
    score += min(6, len(semantic.assertion_symbols))
    score += min(6, 2 * len(_tokens(source_stem) & _tokens(" ".join(semantic.test_functions))))
    if relative == preferred_test_path:
        score += 4
    if score <= 0:
        return None
    return ModelTestCandidateEvidence(
        test_path=relative,
        test_sha256=_sha256_text(text),
        score=score,
        sibling_import=sibling,
        token_overlap=overlap,
        symbol_hits=symbol_hits,
        imported_modules=semantic.imported_modules[:32],
        test_functions=semantic.test_functions,
        fixtures=semantic.fixtures,
        mock_targets=semantic.mock_targets,
        assertion_symbols=semantic.assertion_symbols,
        excerpt=semantic.excerpt,
    )
def build_model_source_context(
    root: Path,
    decision: TestProtectionGapDecision,
    test_files: tuple[Path, ...],
) -> ModelTestSourceContext | None:
    """Build AST-selected context from exact source and semantically ranked tests."""
    source_path = root / Path(decision.source_path)
    if not source_path.is_file():
        return None
    try:
        public_symbols = _public_symbols(source_path)
        semantic_source = build_semantic_source_evidence(source_path, public_symbols)
    except (OSError, SyntaxError, UnicodeError):
        return None
    module_name = module_name_from_path(decision.source_path)
    candidates = [
        item
        for test_path in test_files
        if (
            item := _candidate_evidence(
                root,
                module_name,
                source_path.stem,
                public_symbols,
                test_path,
                decision.candidate_test_path,
            )
        )
        is not None
    ]
    candidates.sort(key=lambda item: (-item.score, item.test_path))
    return ModelTestSourceContext(
        source_path=decision.source_path,
        module_name=module_name,
        public_symbols=public_symbols,
        source_excerpt=semantic_source.excerpt,
        source_imports=semantic_source.imports,
        public_signatures=semantic_source.public_signatures,
        suggested_new_test_path=_suggested_new_test_path(root, source_path.stem),
        candidates=tuple(candidates[:_MAX_CANDIDATES_PER_SOURCE]),
    )
def list_available_models() -> list[str]:
    return Tab1AIReviewAdapter().list_models()
def resolve_selected_model(
    selection: str,
    *,
    model_lister: ModelLister = list_available_models,
) -> str:
    """Resolve the top selector model without silently falling back to another."""
    models = [str(item).strip() for item in model_lister() if str(item).strip()]
    if not models:
        raise ModelResolverError("No local Ollama model is available.")
    selected = str(selection or "").strip()
    if not selected or selected == AUTO_MODEL_LABEL:
        return models[0]
    if selected in models:
        return selected
    casefolded = {item.casefold(): item for item in models}
    matched = casefolded.get(selected.casefold())
    if matched:
        return matched
    raise ModelResolverError(
        "Selected Ollama model is not available: " + selected + ". Refresh AI Models first."
    )
def _context_payload(context: ModelTestSourceContext) -> dict[str, Any]:
    return {
        "source_path": context.source_path,
        "module_name": context.module_name,
        "public_symbols": list(context.public_symbols[:32]),
        "public_signatures": list(context.public_signatures[:24]),
        "source_imports": list(context.source_imports[:32]),
        "source_semantic_excerpt": context.source_excerpt,
        "suggested_new_test_path": context.suggested_new_test_path,
        "candidate_tests": [
            {
                "path": item.test_path,
                "score": item.score,
                "sibling_import": item.sibling_import,
                "token_overlap": list(item.token_overlap),
                "symbol_hits": list(item.symbol_hits),
                "imported_modules": list(item.imported_modules),
                "test_functions": list(item.test_functions),
                "fixtures": list(item.fixtures),
                "mock_targets": list(item.mock_targets),
                "assertion_symbols": list(item.assertion_symbols),
                "semantic_test_excerpt": item.excerpt,
            }
            for item in context.candidates
        ],
    }
def build_model_test_messages(
    contexts: tuple[ModelTestSourceContext, ...],
) -> list[dict[str, str]]:
    """Build strict JSON-only messages for semantic linking or focused test proposals."""
    contract = {
        "decisions": [
            {
                "source_path": "exact supplied source path",
                "action": (
                    "link_existing_test, extend_existing_test, create_focused_test, or web_ai"
                ),
                "candidate_test_path": "exact supplied existing candidate path or empty",
                "target_test_path": (
                    "exact existing candidate for extend, exact suggested_new_test_path for create, or empty"
                ),
                "confidence": 0.0,
                "reason": "short factual reason",
                "evidence_symbols": ["optional exact public symbols"],
                "test_code": "required only for extend/create; imports exact source module and defines meaningful tests",
            }
        ]
    }
    user_payload = {
        "task": (
            "For each TEST_PROTECTION_GAP source, first decide whether a supplied existing test "
            "really protects the same public behavior. If yes use link_existing_test. If no, you may "
            "propose a meaningful focused test change using extend_existing_test or create_focused_test. "
            "Never invent a path: extend only a supplied candidate and create only at suggested_new_test_path. "
            "Generated test_code must directly import the exact source module, exercise a supplied public "
            "contract, and contain real assertions or expected-exception evidence. Never use assert True or "
            "an import-only smoke test. Use web_ai when behavior cannot be tested safely from supplied evidence."
        ),
        "sources": [_context_payload(item) for item in contexts],
        "response_contract": contract,
    }
    return [
        {
            "role": "system",
            "content": (
                "You are a conservative Python test-protection engineer. Return strict JSON only. "
                "Prefer existing tests when they truly exercise the contract. Otherwise propose a small, "
                "deterministic behavioral test only when the supplied source context is sufficient. "
                "Uncertainty must be action web_ai. Do not modify production source."
            ),
        },
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=True)},
    ]
def _extract_json(text: str) -> Any:
    raw = str(text or "").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    return json.loads(raw)
def parse_model_test_response(
    text: str,
    expected_sources: set[str],
) -> dict[str, dict[str, Any]]:
    """Validate strict source identity and response completeness."""
    payload = _extract_json(text)
    if not isinstance(payload, dict) or not isinstance(payload.get("decisions"), list):
        raise ValueError("Local AI response must contain a decisions list.")
    by_source: dict[str, dict[str, Any]] = {}
    for item in payload["decisions"]:
        if not isinstance(item, dict):
            raise ValueError("Every Local AI decision must be an object.")
        source_path = normalize_relative_path(str(item.get("source_path", "")))
        if source_path not in expected_sources or source_path in by_source:
            raise ValueError("Unexpected or duplicate source_path: " + source_path)
        by_source[source_path] = item
    if set(by_source) != expected_sources:
        missing = sorted(expected_sources - set(by_source))
        raise ValueError("Local AI response omitted source(s): " + ", ".join(missing))
    return by_source
def _relationship_gate(candidate: ModelTestCandidateEvidence) -> bool:
    has_behavior_signal = bool(candidate.symbol_hits) or bool(candidate.mock_targets)
    has_structure = candidate.sibling_import or bool(candidate.token_overlap)
    has_assertion_signal = bool(candidate.assertion_symbols)
    return (has_behavior_signal and has_structure and has_assertion_signal) or (
        candidate.sibling_import and len(candidate.token_overlap) >= 2 and has_assertion_signal
    )
def decision_from_model_payload(
    context: ModelTestSourceContext,
    payload: dict[str, Any],
    model_name: str,
) -> TestProtectionGapDecision:
    """Convert link/web-ai model output to a fail-closed deterministic decision."""
    action = str(payload.get("action", "")).strip()
    candidate_path = normalize_relative_path(str(payload.get("candidate_test_path", "")))
    try:
        confidence = float(payload.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    reason = str(payload.get("reason", "")).strip()[:400]
    candidates = {item.test_path: item for item in context.candidates}
    candidate = candidates.get(candidate_path)
    if (
        action != ACTION_LINK_EXISTING_TEST
        or confidence < _MIN_AI_LINK_CONFIDENCE
        or candidate is None
        or not _relationship_gate(candidate)
    ):
        return TestProtectionGapDecision(
            source_path=context.source_path,
            module_name=context.module_name,
            action=ACTION_WEB_AI,
            candidate_test_path=candidate_path if candidate is not None else "",
            candidate_score=int(round(confidence * 100)),
            candidate_reasons=("model_reviewed",),
            source_public_symbols=context.public_symbols,
            test_sha256_before=candidate.test_sha256 if candidate is not None else "",
            reason=reason or "Local AI did not produce a sufficiently grounded existing-test link.",
        )
    reasons = [
        "model_semantic_review",
        "model_confidence_" + str(int(round(confidence * 100))),
        "ast_semantic_retrieval",
    ]
    if candidate.sibling_import:
        reasons.append("imports_source_package_sibling")
    if candidate.token_overlap:
        reasons.append("test_name_matches_feature_family")
    if candidate.symbol_hits:
        reasons.append("references_source_public_symbol")
    if candidate.mock_targets:
        reasons.append("mock_target_evidence")
    if candidate.assertion_symbols:
        reasons.append("assertion_evidence")
    return TestProtectionGapDecision(
        source_path=context.source_path,
        module_name=context.module_name,
        action=ACTION_LINK_EXISTING_TEST,
        candidate_test_path=candidate.test_path,
        candidate_score=int(round(confidence * 100)),
        candidate_reasons=tuple(sorted(set(reasons))),
        source_public_symbols=context.public_symbols,
        test_sha256_before=candidate.test_sha256,
        reason=(reason or "Local AI selected an existing test with semantic and assertion evidence.")
        + " Model: "
        + model_name,
    )
