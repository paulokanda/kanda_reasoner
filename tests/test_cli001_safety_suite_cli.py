from __future__ import annotations

import io
import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.safety_suite_cli.commands import (  # noqa: E402
    available_cli_commands,
    build_safety_suite_parser,
    run_cli,
)


def test_cli001_command_catalog_and_parser() -> None:
    commands = available_cli_commands()
    assert "risk-radar" in commands
    assert "crash-triage" in commands
    assert "refactor-playbook" in commands
    assert "bom-scan" in commands
    assert "shadow-audit" in commands
    assert "api-contract" in commands
    assert build_safety_suite_parser().prog == "kanda-safety-suite"


def test_cli001_list_tools_outputs_known_commands() -> None:
    stdout = io.StringIO()
    status = run_cli(["list-tools"], stdout=stdout)
    assert status == 0
    output = stdout.getvalue()
    assert "risk-radar" in output
    assert "property-test" in output


def test_cli001_risk_radar_command_outputs_markdown(tmp_path: pathlib.Path) -> None:
    stdout = io.StringIO()
    status = run_cli(
        [
            "risk-radar",
            "--root",
            str(tmp_path),
            "--changed-file",
            'ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py',
        ],
        stdout=stdout,
    )
    assert status == 0
    text = stdout.getvalue()
    assert "Risk Change Radar" in text or "risk_change_radar" in text
    assert 'ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py' in text


def test_cli001_push_plan_json_command(tmp_path: pathlib.Path) -> None:
    stdout = io.StringIO()
    status = run_cli(["push-plan", "--root", str(tmp_path), "--format", "json"], stdout=stdout)
    assert status == 0
    text = stdout.getvalue()
    assert '"report_type"' in text
    assert "on_every_push" in text


def test_cli001_api_and_property_draft_commands() -> None:
    api_stdout = io.StringIO()
    api_status = run_cli(
        [
            "api-contract",
            "--module",
            "pkg.mod",
            "--function",
            "load_data",
            "--param",
            "path",
        ],
        stdout=api_stdout,
    )
    assert api_status == 0
    assert "API Contract Guard Draft" in api_stdout.getvalue()

    prop_stdout = io.StringIO()
    prop_status = run_cli(
        [
            "property-test",
            "--module",
            "pkg.mod",
            "--function",
            "normalize_name",
            "--property",
            "Output is stable for repeated input.",
        ],
        stdout=prop_stdout,
    )
    assert prop_status == 0
    assert "Property Test Draft" in prop_stdout.getvalue()


if __name__ == "__main__":
    test_cli001_command_catalog_and_parser()
    test_cli001_list_tools_outputs_known_commands()
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        test_cli001_risk_radar_command_outputs_markdown(pathlib.Path(temp_dir))
        test_cli001_push_plan_json_command(pathlib.Path(temp_dir))
    test_cli001_api_and_property_draft_commands()
    print("CLI001 Safety Suite CLI tests passed.")
