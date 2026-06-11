import sys
import json
import yaml
import pytest
from pathlib import Path

# Put  onto PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from temp.dt_19_project_analysis import export_model, ProjectAnalyzer

@pytest.fixture
def minimal_analyzer(tmp_path):
    pa = ProjectAnalyzer(project_root=str(tmp_path), output_dir=str(tmp_path))
    # fake minimal state
    pa.all_files = {"foo.py"}
    pa.resource_files = {"bar.txt"}
    pa.test_files = {"test_foo.py"}
    pa.entry_points = {"main.py"}
    pa.file_dependencies = {
        "foo.py": {
            "imports": set(),
            "classes": {},
            "functions": {},
            "docstring": "No doc",
            "signals": set(),
            "method_calls": set(),
        }
    }
    pa.class_roles = {}
    pa.class_methods = {}
    pa.function_details = {}
    pa.import_graph = {}
    pa.signals = {}
    pa.method_calls = {}
    pa.feature_index = {}
    return pa

def test_export_json(minimal_analyzer, tmp_path):
    out = tmp_path / "m.json"
    export_model(minimal_analyzer, fmt="json", out_path=out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["files"] == ["foo.py"]

def test_export_yaml(minimal_analyzer, tmp_path):
    out = tmp_path / "m.yaml"
    export_model(minimal_analyzer, fmt="yaml", out_path=out)
    assert out.exists()
    data = yaml.safe_load(out.read_text())
    assert data["files"] == ["foo.py"]

def test_export_invalid(minimal_analyzer):
    with pytest.raises(ValueError):
        export_model(minimal_analyzer, fmt="xml")

