# File: E:/EEG_KANDA/test_docs/test_scaffold_component.py

import importlib.util
import pytest
from pathlib import Path

@pytest.fixture
def tmp_project(tmp_path, monkeypatch):
    # Create a fake project directory under tmp_path
    project_root = tmp_path / "EEG_KANDA"
    project_root.mkdir()
    # Change working dir so scaffold writes in the right place
    monkeypatch.chdir(project_root)
    return project_root

@pytest.fixture
def ProjectAnalyzer(tmp_project):
    """
    Dynamically load ProjectAnalyzer from project_analysis/project_analizer_2.py
    """
    analyzer_path = Path(__file__).parents[1] / "project_analysis" / "project_analizer_2.py"
    spec = importlib.util.spec_from_file_location("project_analizer_2", str(analyzer_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ProjectAnalyzer

def test_scaffold_dropdown_creates_files(tmp_project, ProjectAnalyzer):
    pa = ProjectAnalyzer(project_root=str(tmp_project))
    pa.scaffold_component("dropdown", "BandpassFilter")

    code_path = (
        tmp_project
        / "k05_eeg_filters"
        / "k05_2_drpdwn_widgts"
        / "bandpass_filter_drpdwn.py"
    )
    assert code_path.exists(), f"Expected code stub at {code_path}"
    content = code_path.read_text(encoding="utf-8")
    assert "class BandpassFilterDropdown" in content
    assert "Auto-generated dropdown scaffold for BandpassFilter" in content

    test_path = tmp_project / "tests" / "test_bandpass_filter_drpdwn.py"
    assert test_path.exists(), f"Expected test stub at {test_path}"
    test_content = test_path.read_text(encoding="utf-8")
    assert "BandpassFilterDropdown" in test_content
    # <-- corrected here: include the underscore between "filter" and "drpdwn"
    assert "def test_bandpass_filter_drpdwn_exists" in test_content.lower()


def test_invalid_component_type_raises(tmp_project, ProjectAnalyzer):
    pa = ProjectAnalyzer(project_root=str(tmp_project))
    with pytest.raises(ValueError):
        pa.scaffold_component("unknown_type", "Foo")

