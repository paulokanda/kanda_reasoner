# Dev Portal Overview

Generated: 2025-10-04 16:33:32.884575

<|im_sep|>
"""
Assistant module for analysis and documentation of PySide6-based applications.

This module is designed to help with analysis and documentation of PySide6 applications, including:
- Enhanced dependency graph with imports, class/method relationships, and signal/slot connections
- Detailed class and method documentation
- Testing overview
- Complete file listing
- Directory structure visualization
- ASCII diagrams of signal/slot connections

Requires Python 3.8+ and PySide6.

Usage:
    python -m pyside_analyzer project_directory [output_directory]

<|im_sep|>This script uses the ast and graphviz libraries, which can be installed with pip:
    pip install pyside-analyzer astroid graphviz

To generate an ASCII-only diagram, run the script with the --ascii option:
    python -m pyside_analyzer --ascii project_directory [output_directory]

To skip certain files or directories, add them to the exclude_paths list in the project_analizer.py file.
To exclude certain directories from the directory structure, add them to the exclude_dirs list in the project_analizer.py file.
"""

import ast
import graphviz
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .project_analizer import ProjectAnalyzer


def main():
    project_root = None
    output_dir = None
    ascii_only = False
    if "--ascii" in sys.argv:
        ascii_only = True
        sys.argv.remove("--ascii")

    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    analyzer = ProjectAnalyzer(project_root=project_root, output_dir=output_dir)
    analyzer.analyze_project()
    if not ascii_only:
        analyzer.create_dependency_graph()
        analyzer.create_signal_flow_diagram()
        analyzer.create_class_method_report()
    analyzer.create_ascii_diagrams()


if __name__ == "__main__":
    main()
<|im_sep|> 