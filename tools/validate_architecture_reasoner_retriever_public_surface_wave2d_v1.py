"""Validate reasoner retriever public-surface ownership for wave 2D."""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-reasoner-retriever-public-surface-wave2d-v1"
QUERY_MODULE = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "_live_source_query.py"
)
FACADE_MODULE = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "live_source_fallback.py"
)
HELP_MANIFEST = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json"
)
INHERITED_VALIDATOR = Path(
    "tools/validate_local_ai_live_source_retrieval_quality_v1.py"
)


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def read_text(root: Path, relative: Path) -> str:
    """Read one governed UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8-sig")


def literal_all(tree: ast.Module) -> list[str] | None:
    """Return one literal module __all__, or None when absent."""
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.target if isinstance(node, ast.AnnAssign) else None
        value = node.value
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                continue
            target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id != "__all__":
            continue
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        result: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant):
                return None
            if not isinstance(item.value, str):
                return None
            result.append(item.value)
        return result
    return None


def top_level_functions(tree: ast.Module) -> set[str]:
    """Return top-level function names."""
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def validate_static_contract(root: Path) -> None:
    """Validate private implementation and stable facade ownership."""
    query_text = read_text(root, QUERY_MODULE)
    facade_text = read_text(root, FACADE_MODULE)
    query_tree = ast.parse(query_text, filename=str(root / QUERY_MODULE))
    facade_tree = ast.parse(facade_text, filename=str(root / FACADE_MODULE))

    require(
        literal_all(query_tree) == [],
        "PRIVATE_QUERY_MODULE_PUBLIC_SURFACE_NOT_EMPTY",
    )
    require(
        {
            "extract_live_identifier_terms",
            "score_live_source_candidate",
        }.issubset(top_level_functions(query_tree)),
        "PRIVATE_QUERY_IMPLEMENTATION_FUNCTIONS_MISSING",
    )

    facade_all = literal_all(facade_tree)
    require(
        facade_all is not None
        and "extract_live_identifier_terms" in facade_all,
        "STABLE_FACADE_EXTRACTOR_EXPORT_MISSING",
    )
    require(
        "extract_live_identifier_terms" in top_level_functions(facade_tree),
        "STABLE_FACADE_EXTRACTOR_WRAPPER_MISSING",
    )

    alias_found = False
    scorer_found = False
    for node in facade_tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level != 1 or node.module != "_live_source_query":
            continue
        for alias in node.names:
            if (
                alias.name == "extract_live_identifier_terms"
                and alias.asname == "_extract_live_identifier_terms"
            ):
                alias_found = True
            if (
                alias.name == "score_live_source_candidate"
                and alias.asname is None
            ):
                scorer_found = True

    require(alias_found, "PRIVATE_EXTRACTOR_IMPORT_ALIAS_MISSING")
    require(scorer_found, "PRIVATE_SCORER_IMPORT_MISSING")
    require(
        "return _extract_live_identifier_terms(question)" in facade_text,
        "STABLE_FACADE_WRAPPER_DELEGATION_MISSING",
    )
    require(
        "score_live_source_candidate" not in (facade_all or []),
        "PRIVATE_SCORER_EXPOSED_BY_FACADE",
    )

    manifest = json.loads(read_text(root, HELP_MANIFEST))
    private_record = manifest.get("helpers", {}).get(
        "_live_source_query.py",
        {},
    )
    facade_record = manifest.get("helpers", {}).get(
        "live_source_fallback.py",
        {},
    )
    require(
        private_record.get("stability") == "internal"
        and private_record.get("exports") == []
        and private_record.get("consumed_by") == ["live_source_fallback.py"],
        "PRIVATE_QUERY_HELPER_MANIFEST_CONTRACT_INVALID",
    )
    require(
        facade_record.get("stability") == "stable"
        and "extract_live_identifier_terms"
        in facade_record.get("exports", []),
        "STABLE_FACADE_HELPER_MANIFEST_CONTRACT_INVALID",
    )

    for relative in (QUERY_MODULE, FACADE_MODULE, Path(__file__).resolve()):
        path = relative if relative.is_absolute() else root / relative
        require(
            len(path.read_text(encoding="utf-8-sig").splitlines()) <= 500,
            "TOUCHED_MODULE_EXCEEDS_500_LINES:" + str(path),
        )

    print("PRIVATE QUERY MODULE EXPLICIT EMPTY PUBLIC SURFACE: PASS")
    print("STABLE FACADE OWNS IDENTIFIER EXTRACTOR: PASS")
    print("PRIVATE QUERY SCORER REMAINS INTERNAL: PASS")
    print("RETRIEVER HELPER MANIFEST CONTRACT PRESERVED: PASS")
    print("WAVE2D PYTHON COMPILE AND SIZE: PASS")


def validate_behavior(root: Path) -> None:
    """Validate stable facade output and internal scorer behavior."""
    sys.path.insert(0, str(root))
    try:
        facade = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help."
            "live_source_fallback"
        )
        query = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help."
            "_live_source_query"
        )

        question = "Find where ProviderResponseError is defined and raised."
        terms = facade.extract_live_identifier_terms(question)
        require(
            "ProviderResponseError" in terms,
            "FACADE_IDENTIFIER_EXTRACTION_BEHAVIOR_CHANGED",
        )
        score, anchor = query.score_live_source_candidate(
            "provider_errors.py",
            "class ProviderResponseError(RuntimeError):\n    pass\n",
            terms,
            question,
        )
        require(
            score > 0 and anchor == "ProviderResponseError",
            "PRIVATE_QUERY_SCORING_BEHAVIOR_CHANGED",
        )
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)

    print("STABLE FACADE IDENTIFIER BEHAVIOR: PASS")
    print("PRIVATE QUERY SCORING BEHAVIOR: PASS")


def run_command(
    root: Path,
    command: list[str],
    marker: str,
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one owned command and require its exact marker."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, code + "_NONZERO_EXIT")
    require(marker in output, code + "_MARKER_MISSING")
    return output


def validate_live_architecture(root: Path) -> None:
    """Require zero errors and absence of both target warnings."""
    output = run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "kanda_reasoner_app"
                / "manage_architecture"
                / "manage_architecture.py"
            ),
            "--root",
            str(root),
            "--validate",
        ],
        "ARCHITECTURE VALIDATION SUMMARY",
        "ARCHITECTURE_VALIDATION",
    )
    require("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    require(
        (
            "HELPER_MANIFEST_CONTRACT     "
            "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help"
        )
        not in output,
        "RETRIEVER_HELPER_MANIFEST_WARNING_REMAINS",
    )
    require(
        (
            "PUBLIC_API_INSTABILITY       "
            "kanda_reasoner_app/reasoner_engine/"
            "reasoner_retriever_help/live_source_fallback.py"
        )
        not in output,
        "RETRIEVER_PUBLIC_API_INSTABILITY_REMAINS",
    )
    require(
        "DUPLICATE_PUBLIC_SYMBOL" not in output
        or "extract_live_identifier_terms" not in output,
        "RETRIEVER_PUBLIC_SYMBOL_DUPLICATED",
    )
    print("WAVE2D RETRIEVER HELPER WARNING ABSENT: PASS")
    print("WAVE2D RETRIEVER PUBLIC API INSTABILITY ABSENT: PASS")


def validate_inherited(root: Path) -> None:
    """Run the full live-source quality contract."""
    run_command(
        root,
        [
            sys.executable,
            str(root / INHERITED_VALIDATOR),
            "--root",
            str(root),
        ],
        "VALIDATION OK: local-ai-selected-project-source-access-v1r3",
        "LOCAL_AI_LIVE_SOURCE_RETRIEVAL_VALIDATOR",
    )


def main() -> int:
    """Run Wave 2D static and live validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve(strict=True)
    validate_static_contract(root)
    validate_behavior(root)

    if not args.static_only:
        validate_live_architecture(root)
        validate_inherited(root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
