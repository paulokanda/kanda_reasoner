import re
import pytest
from pathlib import Path
from temp.dt_19_project_analysis.project_analizer_2 import ProjectAnalyzer

@pytest.fixture
def tmp_project(tmp_path):
    # Create a dummy Python file with TODO and FIXME
    src = tmp_path / "example.py"
    src.write_text(
        """
# This is a test module
def foo():
    pass  # TODO: implement foo

# FIXME - fix bar behavior
"""
    )

    return tmp_path

def test_scan_debt(tmp_project):
    pa = ProjectAnalyzer(project_root=str(tmp_project), output_dir=str(tmp_project))
    # 1) discover the file
    pa.scan_project_structure()
    assert "example.py" in pa.all_files

    # 2) no AST info needed for debt scan, but run analyze_file once
    pa.analyze_file(Path(pa.project_root) / "example.py")
    # 3) scan debt
    pa.scan_debt()
    # Should have picked up two items
    types = {item["type"] for item in pa.debt_items}
    msgs  = [item["msg"] for item in pa.debt_items]
    assert types == {"TODO", "FIXME"}
    assert any("implement foo" in m for m in msgs)
    assert any("fix bar behavior" in m for m in msgs)

def test_generate_debt_report(tmp_project, capsys):
    pa = ProjectAnalyzer(project_root=str(tmp_project), output_dir=str(tmp_project))
    pa.scan_project_structure()
    pa.analyze_file(Path(pa.project_root) / "example.py")
    pa.scan_debt()
    # Generate the markdown
    pa.generate_debt_report()

    # Locate the generated file
    out = next(tmp_project.glob("technical_debt_*.md"))
    text = out.read_text(encoding="utf-8")

    # The header and summary must be present
    assert re.search(r"# Technical Debt Report — \d{4}-\d{2}-\d{2}", text)

    # Dynamically check TODO and FIXME entries by line numbers
    todo = next(item for item in pa.debt_items if item["type"] == "TODO")
    fixm = next(item for item in pa.debt_items if item["type"] == "FIXME")

    expected_todo_line = todo["line"]
    expected_fixm_line = fixm["line"]

    assert f"- **Line {expected_todo_line}** [TODO] {todo['msg']}" in text
    assert f"- **Line {expected_fixm_line}** [FIXME] {fixm['msg']}" in text

    # Summary counts
    assert "- Total TODOs: 1" in text
    assert "- Total FIXMEs: 1" in text

    # And it should print the console message
    captured = capsys.readouterr()
    assert "📋 Generated debt report" in captured.out

