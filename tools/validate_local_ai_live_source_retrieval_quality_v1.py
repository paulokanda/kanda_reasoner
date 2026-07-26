#!/usr/bin/env python3
"""Validate Local AI live-source query extraction and production ranking."""
from __future__ import annotations
import argparse
import importlib
import json
import sys
import tempfile
from pathlib import Path
FEATURE_ID = "local-ai-selected-project-source-access-v1r3"
QUERY_MODULE = (
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "_live_source_query.py"
)
FALLBACK_MODULE = (
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "live_source_fallback.py"
)
HELP_MANIFEST = (
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json"
)
LONG_QUESTION = """Use the selected Project source to trace how Local AI obtains
live source evidence when the loaded JSON is incomplete.
Find the implementation responsible for:
1. Accepting the explicitly selected Project root.
2. Detecting that the loaded JSON does not contain complete Project evidence.
3. Searching the selected Project folder for relevant Python source.
4. Blocking Project Support, secret files, symlinks, junctions, binaries,
   virtual environments, build folders, shell access, and writes.
5. Returning bounded source evidence to the Local AI model.
6. Preserving complete Project JSON as the preferred evidence source when it
   is available.
"""
EXPECTED_FIXTURE_PATHS = {
    "app/retriever/live_source_fallback.py",
    "app/retriever/retriever_core_mixin.py",
    "app/ui/runtime_controller.py",
    "app/ui/session_service.py",
    "app/ui/project_json_path_resolver.py",
    "app/index_loader.py",
}

def _marker(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print(name + ": PASS")

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def _validate_source_contract(root: Path) -> None:
    for relative in (QUERY_MODULE, FALLBACK_MODULE):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        _marker("ASCII_ONLY_" + path.stem.upper(), text.isascii())
        _marker(
            "MODULE_MAX_500_LINES_" + path.stem.upper(),
            len(text.splitlines()) <= 500,
        )

    query_text = (root / QUERY_MODULE).read_text(encoding="utf-8")
    fallback_text = (root / FALLBACK_MODULE).read_text(encoding="utf-8")
    manifest = json.loads((root / HELP_MANIFEST).read_text(encoding="utf-8"))

    _marker(
        "QUERY_EXTRACTOR_REJECTS_GENERIC_AI_AND_JSON",
        '"ai", "json", "local"' in query_text,
    )
    _marker(
        "QUERY_EXTRACTOR_HAS_IMPLEMENTATION_ALIASES",
        "selected_project_root" in query_text
        and "ensure_project_json_loaded_for_question" in query_text
        and "augment_bundle_with_live_source_fallback" in query_text,
    )
    _marker(
        "PYTHON_STRING_AND_COMMENT_NOISE_REMOVED",
        "tokenize.generate_tokens" in query_text
        and "tokenize.STRING" not in query_text,
    )
    _marker(
        "REFERENCE_AND_OLDIES_DEPRIORITIZED",
        '".project_reference"' in query_text
        and '"oldies"' in query_text
        and "adjustment -= 2400" in query_text,
    )
    _marker(
        "REFERENCE_ARCHIVE_SCAN_SURFACE_EXCLUDED",
        '".project_reference"' in fallback_text
        and '"legacy_physical_package_archive"' in fallback_text
        and '"oldies"' in fallback_text,
    )
    _marker(
        "PRODUCTION_DIRECTORY_PRIORITY_PRESENT",
        "def _directory_sort_key" in fallback_text
        and 'lowered.endswith("_app")' in fallback_text
        and "kept_dirs.sort(key=_directory_sort_key)" in fallback_text,
    )
    _marker(
        "LOCAL_AI_QUERY_DEPRIORITIZES_WEB_AI_OWNER",
        '"project_web_ai" in relative.lower()' in query_text,
    )
    _marker(
        "MULTI_TERM_COVERAGE_RANKING_PRESENT",
        "distinct = len(matched)" in query_text
        and "score += min(distinct, 8)" in query_text,
    )
    _marker(
        "FALLBACK_USES_PRIVATE_QUERY_RANKER",
        "from ._live_source_query import" in fallback_text
        and "score_live_source_candidate" in fallback_text,
    )
    _marker(
        "FALLBACK_CANDIDATE_LIMIT_REMAINS_BOUNDED",
        "limit=min(max_files, 6)" in fallback_text,
    )
    helper = manifest.get("helpers", {}).get("_live_source_query.py", {})
    fallback = manifest.get("helpers", {}).get("live_source_fallback.py", {})
    _marker(
        "HELP_MANIFEST_PRIVATE_QUERY_HELPER_REGISTERED",
        helper.get("stability") == "internal"
        and helper.get("consumed_by") == ["live_source_fallback.py"],
    )
    _marker(
        "HELP_MANIFEST_FALLBACK_DEPENDENCY_REGISTERED",
        fallback.get("depends_on") == ["_live_source_query.py"],
    )

def _fixture_source(project: Path) -> None:
    _write(
        project / "app/retriever/live_source_fallback.py",
        "_EXCLUDED_DIRS = {'.venv', 'venv', 'build', 'dist'}\n"
        "_SOURCE_EXTENSIONS = {'.py'}\n"
        "_MAX_SOURCE_FILES = 3000\n"
        "_MAX_SOURCE_FILE_BYTES = 98304\n\n"
        "def _is_reparse_point(path):\n    return False\n\n"
        "def _is_excluded_path(path):\n    return False\n\n"
        "def find_live_source_candidates(project_root, terms):\n"
        "    return []\n\n"
        "def augment_bundle_with_live_source_fallback(bundle):\n"
        "    return bundle\n",
    )
    _write(
        project / "app/retriever/retriever_core_mixin.py",
        "def retrieve(question, project_root_override=''):\n"
        "    return augment_bundle_with_live_source_fallback(question)\n",
    )
    _write(
        project / "app/ui/runtime_controller.py",
        "def ensure_project_json_loaded_for_question(window):\n"
        "    window.project_index.initialize_live_project(\n"
        "        window.selected_project_root\n"
        "    )\n",
    )
    _write(
        project / "app/ui/session_service.py",
        "class SessionService:\n"
        "    def execute(self, selected_project_root):\n"
        "        bundle = self.retriever.retrieve(\n"
        "            project_root_override=selected_project_root\n"
        "        )\n"
        "        return bundle\n",
    )
    _write(
        project / "app/ui/project_json_path_resolver.py",
        "def resolve_project_json_path(project_root):\n"
        "    canonical_json = project_root / 'complete.json'\n"
        "    local_ai_json = project_root / 'complete_local_AI.json'\n"
        "    selected_json = (\n"
        "        local_ai_json if local_ai_json.exists() else canonical_json\n"
        "    )\n"
        "    return selected_json\n",
    )
    _write(
        project / "app/index_loader.py",
        "class JsonProjectIndex:\n"
        "    def initialize_live_project(self, project_root):\n"
        "        self.index_data = {\n"
        "            'artifact_type': 'local_ai_live_project_source'\n"
        "        }\n",
    )
    _write(
        project
        / ".project_reference/legacy_physical_package_archive/"
        "T10P082/reasoner_retriever_help/live_source_fallback.py",
        "_EXCLUDED_DIRS = {'.venv', 'venv', 'build', 'dist'}\n"
        "_SOURCE_EXTENSIONS = {'.py'}\n"
        "_MAX_SOURCE_FILES = 3000\n"
        "_MAX_SOURCE_FILE_BYTES = 98304\n\n"
        "def _is_reparse_point(path):\n    return False\n\n"
        "def _is_excluded_path(path):\n    return False\n\n"
        "def find_live_source_candidates(project_root, terms):\n"
        "    return []\n\n"
        "def augment_bundle_with_live_source_fallback(bundle):\n"
        "    return bundle\n",
    )
    _write(
        project
        / ".project_reference/legacy_physical_package_archive/"
        "T10P082/main_window_help/session_service.py",
        "class SessionService:\n"
        "    def execute(self, selected_project_root):\n"
        "        bundle = self.retriever.retrieve(\n"
        "            project_root_override=selected_project_root\n"
        "        )\n"
        "        return bundle\n",
    )
    _write(
        project / "oldies/legacy_ai.py",
        "AI = 'old unrelated implementation'\n",
    )

def _validate_runtime(root: Path) -> None:
    sys.path.insert(0, str(root))
    try:
        from kanda_reasoner_app.reasoner_engine.index_loader import (
            JsonProjectIndex,
        )
        from kanda_reasoner_app.reasoner_engine.reasoner_retriever import (
            ProjectRetriever,
        )
        fallback_module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help."
            "live_source_fallback"
        )
        query_module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help."
            "_live_source_query"
        )
        extract_live_identifier_terms = (
            fallback_module.extract_live_identifier_terms
        )
        find_live_source_candidates = (
            fallback_module.find_live_source_candidates
        )
        iter_candidate_source_files = (
            fallback_module._iter_candidate_source_files
        )
        score_live_source_candidate = query_module.score_live_source_candidate

        terms = extract_live_identifier_terms(LONG_QUESTION)
        normalized_terms = {term.lower() for term in terms}
        _marker("GENERIC_AI_TERM_NOT_SELECTED", "ai" not in normalized_terms)
        _marker("GENERIC_JSON_TERM_NOT_SELECTED", "json" not in normalized_terms)
        _marker(
            "SPECIFIC_IMPLEMENTATION_TERMS_SELECTED",
            {
                "project_root_override",
                "ensure_project_json_loaded_for_question",
                "augment_bundle_with_live_source_fallback",
                "initialize_live_project",
                "resolve_project_json_path",
            }.issubset(normalized_terms),
        )

        alias_score, _anchor = score_live_source_candidate(
            "app/alias_table.py",
            'ALIASES = ("_is_excluded_path", "project_root_override")\n',
            terms,
            LONG_QUESTION,
        )
        _marker("QUOTED_ALIAS_TABLE_DOES_NOT_SELF_RANK", alias_score == 0)

        with tempfile.TemporaryDirectory() as temp_text:
            temp_root = Path(temp_text)
            project = temp_root / "sample_project"
            project.mkdir()
            _fixture_source(project)

            candidates = find_live_source_candidates(
                project,
                terms,
                limit=6,
                question=LONG_QUESTION,
            )
            candidate_paths = {
                str(item["path"]).replace("\\", "/") for item in candidates
            }
            _marker(
                "LONG_QUERY_TOP_SIX_ARE_CANONICAL_OWNERS",
                candidate_paths == EXPECTED_FIXTURE_PATHS,
            )
            _marker(
                "PROJECT_REFERENCE_NOISE_NOT_SELECTED",
                all(".project_reference" not in path for path in candidate_paths),
            )
            _marker(
                "OLDIES_NOISE_NOT_SELECTED",
                all("oldies" not in path for path in candidate_paths),
            )
            scanned_paths = {
                str(path.relative_to(project)).replace("\\", "/")
                for path in iter_candidate_source_files(project)
            }
            _marker(
                "PROJECT_REFERENCE_ARCHIVE_NOT_SCANNED",
                all(
                    not path.lower().startswith(".project_reference/")
                    for path in scanned_paths
                ),
            )
            _marker(
                "OLDIES_DIRECTORY_NOT_SCANNED",
                all("/oldies/" not in "/" + path.lower() for path in scanned_paths),
            )

            auxiliary = temp_root / "error_lessons_compact.json"
            auxiliary.write_text(
                json.dumps(
                    {
                        "artifact_type": "error_memory_ai_export",
                        "lessons": [],
                    }
                ),
                encoding="utf-8",
            )
            index = JsonProjectIndex()
            index.load_json(str(auxiliary))
            bundle = ProjectRetriever(index).retrieve(
                LONG_QUESTION,
                file_limit=10,
                symbol_limit=10,
                snippet_limit=6,
                project_root_override=str(project),
            )
            paths = {
                item.path.replace("\\", "/")
                for item in bundle.file_evidence
                if item.reason == "live_source_fallback"
            }
            _marker(
                "AUXILIARY_JSON_LONG_QUERY_RETRIEVES_CANONICAL_OWNERS",
                EXPECTED_FIXTURE_PATHS.issubset(paths),
            )
            _marker(
                "LONG_QUERY_RETURNS_SIX_LIVE_SNIPPETS",
                len(bundle.snippet_evidence) == 6
                and all(
                    str(item.get("anchor", "")).startswith("LIVE_SOURCE:")
                    for item in bundle.snippet_evidence
                ),
            )
            _marker(
                "NO_GENERIC_AI_MATCH_PROVENANCE",
                all(
                    "Matched identifier: AI" not in item.detail
                    for item in bundle.file_evidence
                ),
            )

            provider = project / "provider_errors.py"
            provider.write_text(
                "class ProviderResponseError(RuntimeError):\n"
                "    pass\n\n"
                "def raise_provider_error():\n"
                "    raise ProviderResponseError('failed')\n",
                encoding="utf-8",
            )
            exact = ProjectRetriever(index).retrieve(
                "Find where ProviderResponseError is defined and raised.",
                file_limit=10,
                symbol_limit=10,
                snippet_limit=6,
                project_root_override=str(project),
            )
            _marker(
                "EXACT_IDENTIFIER_RETRIEVAL_PRESERVED",
                any(item.path == "provider_errors.py" for item in exact.file_evidence),
            )
            _marker(
                "EXACT_IDENTIFIER_SNIPPET_PRESERVED",
                any(
                    item.get("anchor") == "LIVE_SOURCE:ProviderResponseError"
                    for item in exact.snippet_evidence
                ),
            )

        installed_terms = extract_live_identifier_terms(LONG_QUESTION)
        installed_top_ten = find_live_source_candidates(
            root,
            installed_terms,
            limit=10,
            question=LONG_QUESTION,
        )
        installed_top_six = installed_top_ten[:6]
        for position, item in enumerate(installed_top_ten, start=1):
            print(
                "INSTALLED_KANDA_CANDIDATE "
                + str(position)
                + ": "
                + str(item["path"]).replace("\\", "/")
                + " | anchor="
                + str(item["term"])
                + " | score="
                + str(item["score"])
            )

        top_six_paths = {
            str(item["path"]).replace("\\", "/")
            for item in installed_top_six
        }
        top_ten_paths = {
            str(item["path"]).replace("\\", "/")
            for item in installed_top_ten
        }
        expected_installed = {
            "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
            "live_source_fallback.py",
            "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
            "retriever_core_mixin.py",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
            "runtime_controller.py",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
            "session_service.py",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
            "project_json_path_resolver.py",
            "kanda_reasoner_app/reasoner_engine/index_loader.py",
        }
        production_only = all(
            path.startswith("kanda_reasoner_app/")
            and path.endswith(".py")
            and ".project_reference" not in path.lower()
            and "/oldies/" not in path.lower()
            and "/tests/" not in path.lower()
            and "/tools/" not in path.lower()
            and "project_web_ai" not in path.lower()
            for path in top_six_paths
        )
        _marker(
            "INSTALLED_KANDA_TOP_SIX_PRODUCTION_ONLY",
            len(top_six_paths) == 6 and production_only,
        )
        _marker(
            "INSTALLED_KANDA_REFERENCE_ARCHIVE_NOT_RANKED",
            all(
                not path.lower().startswith(".project_reference/")
                and "legacy_physical_package_archive" not in path.lower()
                for path in top_ten_paths
            ),
        )

        categories = {
            "fallback": any(
                path.endswith("reasoner_retriever_help/live_source_fallback.py")
                for path in top_six_paths
            ),
            "selected_root": any(
                path.endswith("reasoner_retriever_help/retriever_core_mixin.py")
                or path.endswith("ai_reasoner_main_window_help/session_service.py")
                for path in top_six_paths
            ),
            "json_preference": any(
                path.endswith("ai_reasoner_main_window_help/project_json_path_resolver.py")
                or path.endswith("local_ai_json_contract.py")
                for path in top_six_paths
            ),
            "live_initialization": any(
                path.endswith("reasoner_engine/index_loader.py")
                or path.endswith("ai_reasoner_main_window_help/runtime_controller.py")
                for path in top_six_paths
            ),
            "orchestration": any(
                path.endswith("ai_reasoner_main_window_help/runtime_controller.py")
                or path.endswith("ai_reasoner_main_window_help/session_service.py")
                for path in top_six_paths
            ),
            "safety": any(
                path.endswith("reasoner_retriever_help/live_source_fallback.py")
                or path.endswith("live_source_verification/verifier.py")
                for path in top_six_paths
            ),
        }
        _marker(
            "INSTALLED_KANDA_SEMANTIC_OWNER_COVERAGE",
            all(categories.values()),
        )
        _marker(
            "INSTALLED_KANDA_EXPECTED_OWNERS_DISCOVERABLE",
            expected_installed.issubset(top_ten_paths),
        )
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    _validate_source_contract(root)
    _validate_runtime(root)
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
