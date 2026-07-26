"""Validate Docstring Assistant and Project Q&A normal-source migration.

This validation intentionally checks only the migrated visible-tab source files.
Legacy placeholder folders under the Docstring Assistant tree are outside this
migration and may contain older text or non-ASCII comments. They must not make
this normal-source migration fail unless they are part of the migrated source
contract below.
"""

from __future__ import annotations

import py_compile
from pathlib import Path

FEATURE_ID = "docstring-projectqa-normal-source-v1"
ROOT = Path(__file__).resolve().parents[1]
MARKER = "VALIDATION OK: " + FEATURE_ID

DOCSTRING_MAIN = ROOT / "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py"
PROJECT_QA_MAIN = ROOT / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
WORKING_COPY = ROOT / "kanda_reasoner_app/local_ai_json_working_copy.py"
FILE_RETRIEVAL = ROOT / "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval.py"

MIGRATED_SOURCE_FILES = (
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/docstring_payloads.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/heuristics.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/response_parsing.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/docstring_validator.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/dialogs.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/ast_safety.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/cli.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/file_processing.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/heuristic_docstrings.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/insertion_collector.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/insertion_formatting.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/reporting.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/run_orchestrator.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/module_summarizer.py",
    "kanda_reasoner_app/local_ai_json_working_copy.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/profile_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/query_intents.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def migrated_paths() -> list[Path]:
    paths: list[Path] = []
    for relative in MIGRATED_SOURCE_FILES:
        path = ROOT / relative
        require(path.exists(), "missing migrated source file: " + relative)
        paths.append(path)
    return paths


def assert_ascii(path: Path) -> None:
    text = read(path)
    require(
        all(ord(char) < 128 for char in text),
        "non-ASCII character found in migrated file: " + path.relative_to(ROOT).as_posix(),
    )


def assert_migrated_files_compile_and_are_ascii() -> None:
    for path in migrated_paths():
        py_compile.compile(str(path), doraise=True)
        assert_ascii(path)


def assert_no_payload_loader_in_migrated_visible_tab_sources() -> None:
    for path in migrated_paths():
        text = read(path)
        relative = path.relative_to(ROOT).as_posix()
        require("load_payload" not in text, relative + " still calls load_payload")
        require("PAYLOAD_PARTS_" not in text, relative + " still exposes payload parts")


def assert_no_retired_runtime_imports() -> None:
    forbidden = (
        "from ask_ai_project_reasoner",
        "import ask_ai_project_reasoner",
    )
    for path in migrated_paths():
        text = read(path)
        relative = path.relative_to(ROOT).as_posix()
        for token in forbidden:
            require(token not in text, relative + " still contains retired import: " + token)


def assert_docstring_assistant_normal_source() -> None:
    text = read(DOCSTRING_MAIN)
    require(
        "class MissingDocstringsWindow(QMainWindow):" in text,
        "Docstring Assistant main window is not readable normal source",
    )
    require("load_payload" not in text, "Docstring Assistant main window still loads payload")


def assert_project_qa_normal_source() -> None:
    text = read(PROJECT_QA_MAIN)
    require(
        "class JsonProjectReasonerV10(QMainWindow):" in text,
        "Project Q&A main window is not readable normal source",
    )
    require(
        "encoded backend payload" in text and "deprecated" in text,
        "Project Q&A payload deprecation note is missing",
    )
    require("load_payload" not in text, "Project Q&A main window still loads payload")


def assert_project_qa_retriever_readable() -> None:
    text = read(FILE_RETRIEVAL)
    require(
        "Deprecated private base64 source shards are history only" in text,
        "Project Q&A file_retrieval.py does not mark base64 shards as deprecated",
    )
    require(
        "file_retrieval_impl_private_impl" not in text,
        "Project Q&A file_retrieval.py still imports the private base64 loader",
    )
    require("import base64" not in text, "Project Q&A file_retrieval.py still imports base64")
    require("b64decode" not in text, "Project Q&A file_retrieval.py still decodes base64")


def assert_working_copy_module() -> None:
    text = read(WORKING_COPY)
    require(
        "def build_default_paths" in text,
        "local_ai_json_working_copy.py is missing build_default_paths",
    )
    require(
        "def ensure_local_ai_copy" in text,
        "local_ai_json_working_copy.py is missing ensure_local_ai_copy",
    )
    require(
        "def refresh_local_ai_copy" in text,
        "local_ai_json_working_copy.py is missing refresh_local_ai_copy",
    )
    require(
        "never\nmodifies the canonical complete JSON" in text,
        "local_ai_json_working_copy.py is missing canonical-protection note",
    )


def assert_non_tab_payloads_not_touched_by_contract() -> None:
    collector_payload = ROOT / "kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios.py"
    if collector_payload.exists():
        require(
            "load_payload" in read(collector_payload),
            "non-tab collector payload was unexpectedly changed by this patch",
        )


def assert_external_freeze_hint_optional() -> None:
    drive = ROOT.anchor or str(ROOT.parent)
    project_name = ROOT.name
    if drive:
        expected = (
            Path(drive)
            / (project_name + "_show_project_to_AI")
            / "project_freeze_after_update"
            / "freeze_hint_intake"
            / (FEATURE_ID + "__KANDA_FREEZE_HINT.json")
        )
        if expected.exists():
            text = read(expected)
            require(FEATURE_ID in text, "external freeze hint belongs to another feature")


def main() -> int:
    assert_migrated_files_compile_and_are_ascii()
    assert_no_payload_loader_in_migrated_visible_tab_sources()
    assert_no_retired_runtime_imports()
    assert_docstring_assistant_normal_source()
    assert_project_qa_normal_source()
    assert_project_qa_retriever_readable()
    assert_working_copy_module()
    assert_non_tab_payloads_not_touched_by_contract()
    assert_external_freeze_hint_optional()
    print(MARKER)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
