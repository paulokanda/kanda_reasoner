"""Regression tests for per-tab output clearing before new GUI runs."""

from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read_text(relative_path: str) -> str:
    """Return UTF-8 text for a project-relative file."""
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _decode_backend_payload(key: str) -> str:
    """Decode a backend payload source by payload key."""
    namespace: dict[str, object] = {}
    path = ROOT / 'ask_' 'ai_project_reasoner' / "backend_payloads" / f"payload_{key}.py"
    exec(path.read_text(encoding="utf-8"), namespace)
    symbol = "PAYLOAD_PARTS_" + key.upper()
    parts = namespace[symbol]
    assert isinstance(parts, tuple)
    encoded = "".join(str(part) for part in parts)
    return base64.b64decode(encoded.encode("ascii")).decode("utf-8")


def _decode_json_splitter_8_source() -> str:
    """Decode the source-preserving JSON splitter source."""
    namespace: dict[str, object] = {}
    base = ROOT / 'ask_' 'ai_project_reasoner' / "json_splitter" / "json_splitter_8_help"
    exec((base / "source_part_1_private_impl.py").read_text(encoding="utf-8"), namespace)
    exec((base / "source_part_2_private_impl.py").read_text(encoding="utf-8"), namespace)
    encoded = str(namespace["SOURCE_PART_1"]) + str(namespace["SOURCE_PART_2"])
    return base64.b64decode(encoded.encode("ascii")).decode("utf-8")


def test_tab1_architecture_run_clears_own_output_before_append() -> None:
    """Verify Tab 1 clears only its output pane before adding new run output."""
    source = _read_text('ask_' 'ai_project_reasoner' '/manage_architecture/manage_architecture_gui.py')
    clear_index = source.index("self._output.clear()")
    append_index = source.index("self._output.appendPlainText(", clear_index)
    assert clear_index < append_index


def test_tab2_workflow_run_clears_own_output_before_append() -> None:
    """Verify Tab 2 clears its decoded output pane before a new worker run."""
    source = _decode_backend_payload("w")
    clear_index = source.index("self._output.clear()")
    append_index = source.index("self._output.appendPlainText(", clear_index)
    assert clear_index < append_index


def test_tab3_docstring_run_clears_own_output_before_routes() -> None:
    """Verify Tab 3 clears its output before normal and Tab 1-audit write routes."""
    source = _decode_backend_payload("s")
    clear_index = source.index("self._output.clear()")
    route_index = source.index("_run_tab1_audit_write_route_from_run_controls", clear_index)
    append_index = source.index("self._output.appendPlainText(", clear_index)
    assert clear_index < route_index
    assert clear_index < append_index


def test_tab4_collector_run_resets_status_and_log_before_new_messages() -> None:
    """Verify Tab 4 resets status and log before collector startup output."""
    source = _read_text(
        'ask_' 'ai_project_reasoner' '/reasoner_tools_shell/runner_help/'
        "window_process_private_impl.py"
    )
    status_index = source.index('self.status_label.setText("Idle")')
    clear_index = source.index("self.log_box.clear()")
    create_index = source.index("self._create_json_file_if_missing(output_json)")
    append_index = source.index('self._append_log("Starting runtime trace generation...")')
    assert status_index < create_index
    assert clear_index < create_index
    assert clear_index < append_index


def test_tab5_split_json_clears_log_before_worker_start() -> None:
    """Verify Tab 5 clears the visible log before starting a split run."""
    source = _decode_json_splitter_8_source()
    clear_index = source.index("self.log_box.clear()")
    worker_index = source.index('self._start_worker("split"', clear_index)
    assert clear_index < worker_index


def test_tab5_public_splitter_entrypoint_keeps_same_clear_contract() -> None:
    """Verify the public splitter entrypoint mirrors the embedded Tab 5 clear behavior."""
    source = _read_text('ask_' 'ai_project_reasoner' '/json_splitter/__init__.py')
    clear_index = source.index("self.log_box.clear()")
    worker_index = source.index('self._start_worker("split"', clear_index)
    assert clear_index < worker_index


def test_tab5_split_wrapper_forces_canonical_paths_before_split() -> None:
    """Verify shell Tab 5 split uses the selected project evidence paths."""
    source = _read_text(
        'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/main_window_help/'
        "window_tool_patches.py"
    )
    bind_index = source.index("widget._original_start_split = widget._start_split")
    wrapper_index = source.index("def _start_split_via_wrapper")
    input_index = source.index("input_file = self._collector_complete_file(project_root)", wrapper_index)
    output_index = source.index("output_folder = self._json_splitted_dir(project_root)", wrapper_index)
    call_index = source.index("widget._original_start_split()", output_index)
    assert bind_index < wrapper_index
    assert input_index < call_index
    assert output_index < call_index


def test_tab5_split_wrapper_clears_split_output_directory_before_split() -> None:
    """Verify shell Tab 5 removes stale split artifacts before a new split."""
    source = _read_text(
        'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/main_window_help/'
        "window_tool_patches.py"
    )
    wrapper_index = source.index("def _start_split_via_wrapper")
    clear_index = source.index("self._clear_directory_contents(output_folder)", wrapper_index)
    call_index = source.index("widget._original_start_split()", clear_index)
    assert clear_index < call_index
