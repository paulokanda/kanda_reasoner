"""PA028 tests for cleaning inactive reference paths during JSON creation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_json_scope_filter import (  # noqa: E402
    filter_project_analysis_json_payload,
)
from kanda_reasoner_app.reasoner_context_collector.collector_config import (  # noqa: E402
    CollectorConfig,
)
from kanda_reasoner_app.reasoner_context_collector.collector_utils import (  # noqa: E402
    safe_json_dump,
)
from kanda_reasoner_app.reasoner_context_collector.collector_walker import (  # noqa: E402
    walk_python_files_filtered,
)


def _write_text(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_payload() -> dict:
    return {
        "collector_info": {"project_root": ""},
        "project_summary": {"project_root": ""},
        "source_file_index": {
            'ask_' 'ai_project_reasoner' '/active.py': {
                "path": 'ask_' 'ai_project_reasoner' '/active.py',
            },
            "_project_reference/memo.py": {
                "path": "_project_reference/memo.py",
            },
            "project_freeze_ledger/memo.py": {
                "path": "project_freeze_ledger/memo.py",
            },
        },
        "symbol_index": {
            "active_symbol": {
                "file": 'ask_' 'ai_project_reasoner' '/active.py',
                "kind": "function",
            },
            "memo_symbol": {
                "file": "_project_reference/memo.py",
                "kind": "function",
            },
            "dot_memo_symbol": {
                "file": "project_freeze_ledger/memo.py",
                "kind": "function",
            },
        },
        "web_ai_symbol_index": {
            "active_symbol": {
                "source_file": 'ask_' 'ai_project_reasoner' '/active.py',
            },
            "memo_symbol": {
                "source_file": "_project_reference/memo.py",
            },
        },
        "primary_definition_index": {
            "active_symbol": 'ask_' 'ai_project_reasoner' '/active.py',
            "memo_symbol": "_project_reference/memo.py",
            "dot_memo_symbol": "project_freeze_ledger/memo.py",
        },
        "web_ai_file_responsibility_index": {
            'ask_' 'ai_project_reasoner' '/active.py': {"path": 'ask_' 'ai_project_reasoner' '/active.py'},
            "_project_reference/memo.py": {"path": "_project_reference/memo.py"},
        },
        "notes": [
            'ask_' 'ai_project_reasoner' '/active.py',
            "_project_reference/memo.py",
            "project_freeze_ledger/memo.py",
            "plain non-path note",
        ],
    }


def test_scope_filter_removes_reference_paths_from_project_analysis_payload() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        payload = _build_payload()
        payload["collector_info"]["project_root"] = str(project_root)
        payload["project_summary"]["project_root"] = str(project_root)

        filtered, summary = filter_project_analysis_json_payload(
            payload,
            project_root=project_root,
        )

        serialized = json.dumps(filtered, sort_keys=True)
        assert "_project_reference" not in serialized
        assert "project_freeze_ledger" not in serialized
        assert 'ask_' 'ai_project_reasoner' '/active.py' in serialized
        assert "plain non-path note" in serialized
        assert summary["applied"] is True
        assert summary["removed_count"] >= 6


def test_safe_json_dump_filters_reference_paths_before_writing_complete_json() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        output_path = (
            project_root
            / "project_analysis_evidence"
            / "json_complete"
            / "sample__complete.json"
        )
        payload = _build_payload()
        payload["collector_info"]["project_root"] = str(project_root)
        payload["project_summary"]["project_root"] = str(project_root)

        safe_json_dump(payload, output_path)

        text = output_path.read_text(encoding="utf-8")
        assert "_project_reference" not in text
        assert "project_freeze_ledger" not in text
        assert 'ask_' 'ai_project_reasoner' '/active.py' in text
        assert "plain non-path note" in text


def test_safe_json_dump_does_not_filter_non_project_analysis_payloads() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "plain.json"
        payload = {
            "note": "_project_reference/memo.py",
            "other": "project_freeze_ledger/memo.py",
        }

        safe_json_dump(payload, output_path)

        data = json.loads(output_path.read_text(encoding="utf-8"))
        assert data == payload


def test_collector_walker_excludes_reference_folders_from_json_creation_input() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write_text(project_root / 'ask_' 'ai_project_reasoner' / "active.py", "x = 1\n")
        _write_text(project_root / "_project_reference" / "memo.py", "x = 2\n")
        _write_text(project_root / "project_freeze_ledger" / "memo.py", "x = 3\n")

        files = walk_python_files_filtered(project_root, CollectorConfig())
        relative_files = sorted(
            path.relative_to(project_root).as_posix()
            for path in files
        )

        assert relative_files == ['ask_' 'ai_project_reasoner' '/active.py']


def main() -> int:
    test_scope_filter_removes_reference_paths_from_project_analysis_payload()
    test_safe_json_dump_filters_reference_paths_before_writing_complete_json()
    test_safe_json_dump_does_not_filter_non_project_analysis_payloads()
    test_collector_walker_excludes_reference_folders_from_json_creation_input()
    print("PA028 clean reference paths from JSON creation tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
