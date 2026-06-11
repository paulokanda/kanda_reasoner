# File: E:/EEG_KANDA/test_docs/test_feature_index.py

import sys
import os
# Insert the dev_tools folder onto PYTHONPATH so we can import project_analysis
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from temp.dt_19_project_analysis.project_analizer_2 import ProjectAnalyzer
from collections import defaultdict

def make_dummy_file_deps():
    return {
        'dir1/foo_bar.py': {
            'docstring': 'This handles foo bar logic.',
            'classes': {'FooBar': {}},
            'functions': {'baz_qux': {}}
        },
        'dir2/another_file.py': {
            'docstring': 'Some other description.',
            'classes': {},
            'functions': {}
        }
    }

def test_build_feature_index_and_find_exact():
    analyzer = ProjectAnalyzer(project_root=".", output_dir="./dev_tools")
    analyzer.file_dependencies = make_dummy_file_deps()
    analyzer.feature_index = defaultdict(set)

    analyzer.build_feature_index()

    # Exact lookups
    assert 'dir1/foo_bar.py' in analyzer.find_feature_location('FooBar')
    assert 'dir1/foo_bar.py' in analyzer.find_feature_location('logic')
    assert 'dir1/foo_bar.py' in analyzer.find_feature_location('baz_qux')

def test_find_feature_location_fuzzy():
    analyzer = ProjectAnalyzer(project_root=".", output_dir="./dev_tools")
    analyzer.file_dependencies = {
        'filters/bandpass_filter.py': {
            'docstring': 'Dropdown for bandpass filtering.',
            'classes': {'BandFilterDropdown': {}},
            'functions': {}
        }
    }
    analyzer.feature_index = defaultdict(set)

    analyzer.build_feature_index()
    results = analyzer.find_feature_location('bandflt')
    assert 'filters/bandpass_filter.py' in results

def test_find_feature_location_no_match():
    analyzer = ProjectAnalyzer(project_root=".", output_dir="./dev_tools")
    analyzer.file_dependencies = {
        'some_module.py': {'docstring': '', 'classes': {}, 'functions': {}}
    }
    analyzer.feature_index = defaultdict(set)
    analyzer.build_feature_index()
    assert analyzer.find_feature_location('nonexistent') == []

