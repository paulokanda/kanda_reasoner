# project_analysis/project_analizer_2.py
# -*- coding: utf-8 -*-

"""
Project Analyzer (clean, deduplicated)

Key fixes
- Removed duplicate methods (e.g., export_model, analyze_complexity, dependency graph, etc.).
- Harmonized method names with the runner (run_* analysis methods + report_metrics).
- Single source of truth for flow builders, web server, and export helpers.
- Consistent output_dir: results_report by default.
"""

from __future__ import annotations

import ast
import os
import re
import json
import textwrap
import inspect
import subprocess
import unicodedata
import difflib
import webbrowser
import http.server
import socketserver
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Any, Dict, List, Set, DefaultDict, Optional, Union, Tuple

import graphviz
from radon.complexity import cc_visit

from temp.dt_19_project_analysis.prjct_anlzr_json_yaml_export_helper import export_model as _export_model

def serve_web_explorer(directory: Path, port: int = 8000):
    """Serve `directory` via a simple HTTP server."""
    old_cwd = os.getcwd()
    try:
        os.chdir(directory)

        class _ThreadingHTTPServer(socketserver.ThreadingTCPServer):
            allow_reuse_address = True

        httpd = _ThreadingHTTPServer(("", port), http.server.SimpleHTTPRequestHandler)
        url = f"http://localhost:{port}"
        print(f"ðŸŒ Serving at {url} (dir: {directory}) â€” Ctrl+C to stop")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nðŸ›‘ Stopping serverâ€¦")
        finally:
            httpd.shutdown()
            httpd.server_close()
    finally:
        os.chdir(old_cwd)


class ProjectAnalyzer:

    SCAFFOLD_TEMPLATES = {
        "dropdown": {
            "dir": "k05_eeg_filters_deprecated/k05_2_drpdwn_widgts",
            "file_tpl": "{{ snake_name }}_drpdwn.py",
            "test_dir": "tests",
            "test_tpl": "test_{{ snake_name }}_drpdwn.py",
            "template": r'''
"""Autoâ€generated {{ feature_name }} dropdown scaffold."""

from PySide6.QtWidgets import QComboBox
from k05_eeg_filters_deprecated.k05_1_drpdwn_integrator.drpdwn_integrator_eeg import DropdownIntegrator

class {{ class_name }}(QComboBox):
    """
    Dropdown stub for {{ feature_name }}.
    Emits '{{ snake_name }}_changed' when selection changes.
    """
    def __init__(self, visualizer, parent):
        super().__init__(parent)
        self.visualizer = visualizer
        DropdownIntegrator.register("{{ feature_name }}", self)
        self.addItems(["Option1", "Option2", "Option3"])
        self.currentIndexChanged[str].connect(self.on_change)

    def on_change(self, text: str):
        # Example: self.visualizer.create_{{ snake_name }}(param=text)
        print(f"[DEBUG] {{ feature_name }} selected â†’", text)
'''
        },
        "manager": {
            "dir": "k01_core_eeg/k01_3_eeg_visualizer",
            "file_tpl": "{{ snake_name }}_manager.py",
            "test_dir": "tests",
            "test_tpl": "test_{{ snake_name }}_manager.py",
            "template": r'''
"""Autoâ€generated manager scaffold for {{ feature_name }}Manager."""

class {{ class_name }}:
    """Manager stub for {{ feature_name }}."""
    def __init__(self, core):
        self.core = core

    def do_something(self, *args, **kwargs):
        pass
'''
        },
        "helper": {
            "dir": "k01_core_eeg/k01_3_eeg_visualizer/visualizer_core_helpers",
            "file_tpl": "{{ snake_name }}.py",
            "test_dir": "tests",
            "test_tpl": "test_{{ snake_name }}.py",
            "template": r'''
"""Autoâ€generated helper scaffold for {{ feature_name }}."""

def {{ snake_name }}(core):
    """Helper stub for {{ feature_name }}."""
    return None
'''
        },
    }

    def __init__(self,
                 project_root: str | None = None,
                 output_dir: str | None = None,
                 *,
                 exclude_dirs: Optional[List[str]] = None,
                 skip_complexity_errors: bool = True,
                 generate_media_artifacts: bool = True,
                 enable_complexity_analysis: bool = True,
                 enable_git_history_analysis: bool = True,
                 enable_dependency_check: bool = True,
                 enable_similarity_check: bool = True,
                 enable_architecture_check: bool = True,
                 enable_performance_metrics: bool = True):
        self.module_dir = Path(__file__).parent
        default_root = self.module_dir.parent.parent.parent
        self.project_root = Path(project_root) if project_root else default_root

        # default output dir: results_report
        default_output = self.project_root / "dev_tools" / "results_report"
        self.output_dir = Path(output_dir) if output_dir else default_output
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[Analyzer] Output dir â†’ {self.output_dir}")

        # Options
        self.exclude_dirs = set(exclude_dirs or [])
        self.skip_complexity_errors = skip_complexity_errors
        self.generate_media_artifacts = generate_media_artifacts

        # Core stores
        self.file_dependencies: DefaultDict[str, dict] = defaultdict(dict)
        self.all_files: Set[str] = set()
        self.module_purposes: Dict[str, str] = {}
        self.class_roles: Dict[str, dict] = {}
        self.class_methods: DefaultDict[str, Dict[str, dict]] = defaultdict(dict)
        self.function_details: DefaultDict[str, dict] = defaultdict(dict)
        self.entry_points: Set[str] = set()
        self.test_files: Set[str] = set()
        self.resource_files: Set[str] = set()
        self.signal_chains: DefaultDict[str, list] = defaultdict(list)
        self.import_graph: DefaultDict[str, Set[str]] = defaultdict(set)
        self.atlas_data: Dict[str, Any] = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.signals: DefaultDict[str, list] = defaultdict(list)
        self.method_calls: DefaultDict[str, list] = defaultdict(list)
        self.skipped_files: DefaultDict[str, list] = defaultdict(list)

        # Search index
        self.feature_index: DefaultDict[str, Set[str]] = defaultdict(set)

        # Debt
        self.debt_items: List[Dict[str, Any]] = []

        # Feature toggles
        self.enable_complexity_analysis = enable_complexity_analysis
        self.enable_git_history_analysis = enable_git_history_analysis
        self.enable_dependency_check = enable_dependency_check
        self.enable_similarity_check = enable_similarity_check
        self.enable_architecture_check = enable_architecture_check
        self.enable_performance_metrics = enable_performance_metrics

        # Analysis results
        self.complexity_results: Dict[str, List[Tuple[str, int]]] = {}
        self.commit_history: List[dict] = []
        self.dependency_warnings: List[str] = []
        self.similar_code: List[dict] = []
        self.architecture_violations: List[dict] = []
        self.performance_metrics_results: Dict[str, dict] = {}

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  SCAN  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def scan_project_structure(self):
        print(f"\nScanning project at: {self.project_root}")
        for root, dirs, files in os.walk(self.project_root):
            if any(ex in Path(root).as_posix() for ex in self.exclude_dirs):
                continue

            dirs[:] = [
                d for d in dirs
                if not (d.startswith('.') or d in ('__pycache__', 'build', 'dist'))
            ]

            for file in files:
                file_path = Path(root) / file
                try:
                    rel = str(file_path.relative_to(self.project_root))

                    if self._is_test_file(file) or 'test' in Path(rel).parent.as_posix().lower():
                        self.test_files.add(rel)
                        continue

                    if file.endswith('.py'):
                        self.all_files.add(rel)
                        if self._is_entry_point(file):
                            self.entry_points.add(rel)
                    elif any(file.endswith(ext) for ext in ('.json', '.csv', '.edf', '.txt', '.md')):
                        self.resource_files.add(rel)

                except Exception as e:
                    self.skipped_files[str(file_path)] = str(e)

        print(f"Found {len(self.all_files)} Python files, "
              f"{len(self.resource_files)} resources, "
              f"{len(self.test_files)} tests")

    def analyze_file(self, file_path: Path):
        """Analyze a single .py file and populate structures."""
        try:
            relative_path = str(file_path.relative_to(self.project_root))
            content = file_path.read_text(encoding='utf-8', errors='replace')

            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                self.skipped_files[relative_path] = f"Syntax error: {e}"
                return

            self.file_dependencies[relative_path] = {
                'imports': set(),
                'classes': {},
                'functions': {},
                'docstring': self._clean_docstring(ast.get_docstring(tree)),
                'signals': set(),
                'method_calls': set()
            }

            for node in ast.walk(tree):
                try:
                    if isinstance(node, ast.ClassDef):
                        self._process_class(node, relative_path)
                    elif isinstance(node, ast.FunctionDef):
                        self._process_function(node, relative_path)
                    elif isinstance(node, (ast.ImportFrom, ast.Import)):
                        self._process_import(node, relative_path)
                    elif isinstance(node, ast.Call):
                        self._process_method_call(node, relative_path)
                    elif isinstance(node, ast.Assign):
                        self._process_signal_assignment(node, relative_path)
                except Exception as e:
                    print(f"Error processing node in {file_path}: {e}")
                    continue

        except Exception as e:
            msg = f"Error analyzing {file_path}: {e}"
            print(msg)
            self.skipped_files[str(file_path)] = msg

    def _sanitize_code_for_complexity(self, raw: str) -> str:
        """
        Make source safe for radon/ast parsing without touching files on disk.
        - strips BOM if present
        - normalizes newlines
        - removes ASCII control chars (except \n, \t)
        - replaces a few common non-ASCII symbols that sometimes sneak into code
        """
        # normalize BOM
        if raw.startswith("\ufeff"):
            raw = raw.lstrip("\ufeff")

        # normalize newlines
        raw = raw.replace("\r\n", "\n").replace("\r", "\n")

        # remove non-printable control chars (keep tab/newline)
        import re
        raw = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", raw)

        # common fancy symbols occasionally used in code instead of ascii
        replacements = {
            "â†’": "->",
            "â†": "<-",
            "â€”": "-",
            "â€“": "-",
            "â€œ": '"',
            "â€": '"',
            "â€˜": "'",
            "â€™": "'",
            "â€¦": "...",
        }
        for bad, good in replacements.items():
            raw = raw.replace(bad, good)

        return raw

    def _is_entry_point(self, filename: str) -> bool:
        entry_patterns = ['main', 'app', 'start', 'run', 'manage']
        return (any(p in filename.lower() for p in entry_patterns) and
                not filename.startswith('test_'))

    def _is_test_file(self, filename: str) -> bool:
        return any(p in filename.lower() for p in ['test_', '_test', 'tests'])

    def _is_test_path(self, rel: str) -> bool:
        p = rel.replace("\\", "/").lower()
        return ("/tests/" in p or p.endswith("/tests")
                or re.search(r'(^|/)test_', p) is not None
                or p.endswith("_test.py") or "/test_" in p)

    def _clean_docstring(self, docstring: Optional[str]) -> str:
        if not docstring:
            return "No docstring"
        return inspect.cleandoc(docstring).replace('\n', ' ').strip()

    def _process_class(self, node: ast.ClassDef, file_path: str):
        try:
            class_info = {
                'methods': {},
                'bases': [self._get_base_name(base) for base in node.bases],
                'docstring': self._clean_docstring(ast.get_docstring(node)) or "No class docstring",
                'signals': set(),
                'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
            }
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_info = self._create_method_info(item)
                    class_info['methods'][item.name] = method_info
                    self.class_methods[node.name][item.name] = method_info

            self.file_dependencies[file_path]['classes'][node.name] = class_info
            self.class_roles[node.name] = {
                'file': file_path,
                'purpose': class_info['docstring'],
                'is_abstract': any(d == 'abstractmethod' for d in class_info['decorators']),
                'bases': class_info['bases'],
            }
        except Exception as e:
            print(f"Error processing class {node.name} in {file_path}: {e}")

    def _get_base_name(self, base_node: ast.AST) -> str:
        try:
            if isinstance(base_node, ast.Name):
                return base_node.id
            if isinstance(base_node, ast.Attribute):
                return base_node.attr
            if isinstance(base_node, ast.Subscript):
                return self._get_base_name(base_node.value)
            return "UnknownBase"
        except Exception:
            return "UnknownBase"

    def _create_method_info(self, node: ast.FunctionDef) -> dict:
        try:
            return {
                'docstring': self._clean_docstring(ast.get_docstring(node)) or "No method docstring",
                'args': [arg.arg for arg in node.args.args],
                'returns': self._get_return_annotation(node),
                'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)],
                'is_async': isinstance(node, ast.AsyncFunctionDef)
            }
        except Exception as e:
            print(f"Error creating method info: {e}")
            return {'docstring': "Error", 'args': [], 'returns': "Unknown", 'decorators': [], 'is_async': False}

    def _get_return_annotation(self, node: ast.FunctionDef) -> str:
        try:
            if node.returns:
                if isinstance(node.returns, ast.Name):
                    return node.returns.id
                if isinstance(node.returns, ast.Subscript):
                    return getattr(node.returns.value, "id", "Unknown")
                if isinstance(node.returns, ast.Str):
                    return node.returns.s
            return "None"
        except Exception:
            return "Unknown"

    def _process_function(self, node: ast.FunctionDef, file_path: str):
        func_info = self._create_method_info(node)
        self.file_dependencies[file_path]['functions'][node.name] = func_info
        self.function_details[node.name] = {'file': file_path, 'info': func_info}
        if node.name.startswith('test_'):
            self.test_files.add(file_path)

    def _process_import(self, node: ast.AST, file_path: str):
        try:
            imports = set()
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    base = node.module.split('.')[0]
                    imports.add(base)
                    for alias in node.names:
                        self.import_graph[file_path].add(f"{base}.{alias.name}")
            self.import_graph[file_path].update(imports)
            self.file_dependencies[file_path].setdefault('imports', set()).update(imports)
        except Exception as e:
            print(f"Error processing import in {file_path}: {e}")

    def _process_method_call(self, node: ast.Call, file_path: str):
        try:
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                if isinstance(node.func.value, ast.Name):
                    class_name = node.func.value.id
                    self.method_calls[file_path].append(f"{class_name}.{method_name}")
            elif isinstance(node.func, ast.Name):
                self.method_calls[file_path].append(node.func.id)
        except Exception as e:
            print(f"Error processing method call in {file_path}: {e}")

    def _process_signal_assignment(self, node: ast.Assign, file_path: str):
        try:
            if (isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Attribute)
                    and node.value.func.attr in ('Signal', 'pyqtSignal')):
                if node.targets and isinstance(node.targets[0], ast.Name):
                    signal_name = node.targets[0].id
                    self.signals[file_path].append(signal_name)
                    self.file_dependencies[file_path]['signals'].add(signal_name)
        except Exception as e:
            print(f"Error processing signal assignment in {file_path}: {e}")

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  Feature index + search  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def build_feature_index(self):
        self.feature_index.clear()
        for file_path, data in self.file_dependencies.items():
            tokens: Set[str] = set()
            stem = Path(file_path).stem
            tokens.update(re.split(r'[\W_]+', stem))
            for part in Path(file_path).parent.as_posix().split('/'):
                tokens.update(re.split(r'[\W_]+', part))
            tokens.update(re.split(r'[\W_]+', data.get('docstring', '')))
            tokens.update(data.get('classes', {}).keys())
            tokens.update(data.get('functions', {}).keys())

            for tok in tokens:
                norm = unicodedata.normalize('NFKD', tok).encode('ascii', 'ignore').decode()
                norm = re.sub(r'\W+', '', norm).lower()
                if len(norm) < 3:
                    continue
                self.feature_index[norm].add(file_path)

    def find_feature_location(self, feature_name: str, max_results: int = 5) -> List[str]:
        q = unicodedata.normalize('NFKD', feature_name).encode('ascii', 'ignore').decode()
        q = re.sub(r'\W+', '', q).lower()
        if q in self.feature_index:
            return sorted(self.feature_index[q])
        keys = list(self.feature_index.keys())
        close = difflib.get_close_matches(q, keys, n=max_results, cutoff=0.5)
        results: Set[str] = set()
        for key in close:
            results.update(self.feature_index[key])
        return sorted(results)

    def _generate_class_method_report(self) -> Path:
        """
        Emit a detailed, human-readable report of all discovered classes,
        their methods (with args/returns/decorators/dev_tools), plus standalone
        functions. Returns the path to the generated file.

        Safe to call anytime; it will scan/analyze missing pieces as needed.
        """
        # Ensure the model is populated
        try:
            if not getattr(self, "all_files", None):
                self.scan_project_structure()
            # Parse any files we haven't analyzed yet
            for rel in list(self.all_files):
                if rel not in self.file_dependencies:
                    self.analyze_file(Path(self.project_root) / rel)
            # Build reverse method index if missing
            if not hasattr(self, "method_index"):
                self._build_method_index()
        except Exception as e:
            print(f"[class-method-report] preflight failed: {e}")

        lines: list[str] = []
        sep = "=" * 80
        ts = getattr(self, "timestamp", datetime.now().strftime("%Y%m%d_%H%M"))

        lines.append(sep)
        lines.append(" CLASS & METHOD DETAILS")
        lines.append(sep)
        lines.append(f"Generated: {datetime.now():%Y-%m-%d %H:%M}")
        lines.append(f"Project  : {Path(self.project_root).name}")
        lines.append("")

        # ---------- Classes ----------
        if not getattr(self, "class_methods", None):
            lines.append("No classes discovered.")
        else:
            for cls_name in sorted(self.class_methods):
                class_info = self.class_roles.get(cls_name, {})
                file_path = class_info.get("file", "unknown")
                purpose = class_info.get("purpose", "No description")
                bases = class_info.get("bases", [])
                is_abs = class_info.get("is_abstract", False)

                lines.append(f"\nðŸ”¹ {cls_name}")
                lines.append(f"   Location : {file_path}")
                if bases:
                    lines.append(f"   Bases    : {', '.join(bases)}")
                if is_abs:
                    lines.append("   Flags    : abstract")
                # keep purpose short
                try:
                    short_purpose = textwrap.shorten(str(purpose), width=100, placeholder="â€¦")
                except Exception:
                    short_purpose = str(purpose)
                lines.append(f"   Purpose  : {short_purpose}")

                # Each method
                methods = self.class_methods.get(cls_name, {}) or {}
                for m_name in sorted(methods.keys()):
                    info = methods[m_name] or {}
                    args = info.get("args", [])
                    retn = info.get("returns", "None")
                    decs = info.get("decorators", [])
                    doc = info.get("docstring", "No docstring")

                    # format signature (skip 'self' if present)
                    sig_args = [a for a in args if a != "self"]
                    sig = f"{m_name}({', '.join(sig_args)})"

                    try:
                        short_doc = textwrap.shorten(str(doc), width=120, placeholder="â€¦")
                    except Exception:
                        short_doc = str(doc)

                    lines.append(f"\n   â–ª {sig}")
                    lines.append(f"     - Returns   : {retn}")
                    if decs:
                        lines.append(f"     - Decorators: {', '.join(decs)}")
                    lines.append(f"     - Doc       : {short_doc}")

        # ---------- Standalone functions ----------
        lines.append("\n\n" + sep)
        lines.append(" STANDALONE FUNCTIONS")
        lines.append(sep)

        if not getattr(self, "function_details", None):
            lines.append("No standalone functions discovered.")
        else:
            for func_name in sorted(self.function_details.keys()):
                fd = self.function_details.get(func_name, {}) or {}
                file = fd.get("file", "unknown")
                info = fd.get("info", {}) or {}
                doc = info.get("docstring", "No docstring")
                args = info.get("args", [])
                try:
                    short_doc = textwrap.shorten(str(doc), width=120, placeholder="â€¦")
                except Exception:
                    short_doc = str(doc)
                sig = f"{func_name}({', '.join(args)})"

                lines.append(f"\nðŸ”¹ {sig}")
                lines.append(f"   Location : {file}")
                lines.append(f"   Doc      : {short_doc}")

        # Write file
        try:
            out_name = f"method_details_{ts}.txt"
            out_path = Path(self.output_dir) / out_name
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"Created class/method report: {out_path}")
            return out_path
        except Exception as e:
            print(f"[class-method-report] failed to write report: {e}")
            return Path(self.output_dir) / f"method_details_{ts}_ERROR.txt"

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  High-level pipeline  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def generate_architecture_docs(self,
                                   *,
                                   onboarding: bool = False,
                                   clean_flows: bool = False,
                                   dep_hotspots: bool = False,
                                   tech_debt: bool = False,
                                   enable_complexity_analysis: bool | None = None,
                                   enable_git_history_analysis: bool | None = None,
                                   enable_dependency_check: bool | None = None,
                                   enable_similarity_check: bool | None = None,
                                   enable_architecture_check: bool | None = None,
                                   enable_performance_metrics: bool | None = None):
        # resolve toggles
        if enable_complexity_analysis is None:
            enable_complexity_analysis = self.enable_complexity_analysis
        if enable_git_history_analysis is None:
            enable_git_history_analysis = self.enable_git_history_analysis
        if enable_dependency_check is None:
            enable_dependency_check = self.enable_dependency_check
        if enable_similarity_check is None:
            enable_similarity_check = self.enable_similarity_check
        if enable_architecture_check is None:
            enable_architecture_check = self.enable_architecture_check
        if enable_performance_metrics is None:
            enable_performance_metrics = self.enable_performance_metrics

        # 1) scan & analyze
        self.scan_project_structure()
        for f in self.all_files:
            self.analyze_file(Path(self.project_root) / f)

        # 2) indexes
        self.build_feature_index()
        self._build_method_index()

        # 3) debt & git
        self.scan_debt()
        self.analyze_git_metadata()
        self.generate_recent_changes(since="7 days ago")

        # 4) optional analyses
        if enable_complexity_analysis:
            self.run_complexity_analysis()
        if enable_git_history_analysis:
            self.run_git_history_analysis()
        if enable_dependency_check:
            self.run_dependency_check()
        if enable_similarity_check:
            self.run_similarity_check()
        if enable_architecture_check:
            self.run_architecture_check()
        if enable_performance_metrics:
            self.run_performance_analysis()

        # 5) dev_tools
        self._generate_text_atlas()
        self._generate_ascii_diagrams()
        if self.generate_media_artifacts:
            self._generate_dependency_graph()  # PNG + cmapx + HTML
        self._generate_class_method_report()
        self._generate_enriched_ascii_flows()

        # 6) extras
        if onboarding:
            self.generate_onboarding_readme()
        if clean_flows and self.generate_media_artifacts:
            self.generate_clean_flow_diagrams()
        if dep_hotspots:
            self.generate_dependency_hotspots_report()
        if tech_debt:
            self.generate_debt_report()

        print(f"\nDocumentation generated at: {self.output_dir}")

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  debt + git  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def scan_debt(self):
        self.debt_items.clear()
        for rel in sorted(self.all_files):
            if not rel.endswith('.py') or any(ex in rel for ex in self.exclude_dirs):
                continue
            abs_path = Path(self.project_root) / rel
            try:
                for lineno, line in enumerate(abs_path.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
                    m = re.search(r'#\s*(TODO|FIXME)\s*[:\-]?\s*(.*)', line, flags=re.IGNORECASE)
                    if m:
                        self.debt_items.append({
                            "file": rel, "line": lineno,
                            "type": m.group(1).upper(), "msg": m.group(2).strip()
                        })
            except Exception:
                continue

    def generate_debt_report(self):
        if not self.debt_items:
            print("No TODO/FIXME found.")
            return
        md: List[str] = [f"# Technical Debt Report â€” {datetime.now():%Y-%m-%d}\n"]
        by_file: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for item in self.debt_items:
            by_file[item["file"]].append(item)
        for file, items in sorted(by_file.items()):
            md.append(f"## {file}")
            for it in items:
                md.append(f"- **Line {it['line']}** [{it['type']}] {it['msg']}")
            md.append("")
        total_todo = sum(1 for i in self.debt_items if i['type'] == 'TODO')
        total_fix = sum(1 for i in self.debt_items if i['type'] == 'FIXME')
        md.extend(["---", f"- Total TODOs: {total_todo}", f"- Total FIXMEs: {total_fix}"])
        out = self.output_dir / f"technical_debt_{self.timestamp}.md"
        out.write_text("\n".join(md), encoding="utf-8")
        print(f"ðŸ“‹ Generated debt report: {out}")

    def analyze_git_metadata(self):
        if not (Path(self.project_root) / ".git").exists():
            return
        self.git_metadata: Dict[str, Dict[str, str]] = {}
        for rel in self.all_files:
            full = Path(self.project_root) / rel
            try:
                out = subprocess.check_output(
                    ["git", "log", "-1", "--format=%an|%ad", "--", str(full)],
                    cwd=self.project_root, stderr=subprocess.DEVNULL
                ).decode().strip()
                if '|' in out:
                    author, date = out.split("|", 1)
                    self.git_metadata[rel] = {"author": author, "date": date}
            except Exception:
                continue

    def generate_recent_changes(self, since: str = "7 days ago"):
        if not (Path(self.project_root) / ".git").exists():
            return
        try:
            out = subprocess.check_output(
                ["git", "log", f"--since={since}", "--pretty=format:%h|%an|%ad|%s"],
                cwd=self.project_root
            ).decode().strip()
        except Exception:
            return
        self.recent_changes = []
        for line in out.splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                h, author, date, msg = parts
                self.recent_changes.append({"hash": h, "author": author, "date": date, "msg": msg})

    def _generate_dependency_warnings_section(self) -> str:
        if not getattr(self, "dependency_warnings", None):
            return "\n[DEPENDENCY WARNINGS]\n" + "=" * 80 + "\nNo dependency warnings found."
        lines = ["\n[DEPENDENCY WARNINGS]", "=" * 80, "\nPotential dependency issues found:"]
        for w in self.dependency_warnings:
            lines.append(f"- {w}")
        lines.extend([
            "\nRecommendations:",
            "- Pin dependencies in requirements.txt",
            "- Use a vulnerability scanner (e.g. `safety`)",
            "- Update regularly to patch CVEs",
        ])
        return "\n".join(lines)

    def _generate_similar_code_section(self) -> str:
        if not getattr(self, "similar_code", None):
            return "\n[CODE SIMILARITY ANALYSIS]\n" + "=" * 80 + "\nNo significant code similarities found."
        lines = ["\n[CODE SIMILARITY ANALYSIS]", "=" * 80,
                 f"\nFound {len(self.similar_code)} pairs of files with high code similarity:"]
        high = [s for s in self.similar_code if s['similarity'] > 0.9][:5]
        med = [s for s in self.similar_code if 0.7 < s['similarity'] <= 0.9][:5]
        if high:
            lines.append("\nHigh similarity (potential duplication):")
            for it in high:
                a, b = it['files']
                lines.append(f"- {a} â†” {b} ({it['similarity'] * 100:.1f}%)")
        if med:
            lines.append("\nMedium similarity (possible refactors):")
            for it in med:
                a, b = it['files']
                lines.append(f"- {a} â†” {b} ({it['similarity'] * 100:.1f}%)")
        lines.extend([
            "\nRecommendations:",
            "- Extract common code into shared modules",
            "- Prefer composition/inheritance to reduce duplication",
        ])
        return "\n".join(lines)

    def _generate_architecture_violations_section(self) -> str:
        if not getattr(self, "architecture_violations", None):
            return "\n[ARCHITECTURE RULES CHECK]\n" + "=" * 80 + "\nNo architecture violations found."
        if not self.architecture_violations:
            return "\n[ARCHITECTURE RULES CHECK]\n" + "=" * 80 + "\nNo architecture violations found."
        lines = ["\n[ARCHITECTURE RULES CHECK]", "=" * 80,
                 f"\nFound {len(self.architecture_violations)} architecture violations:"]
        # group by type
        by_type = {}
        for v in self.architecture_violations:
            by_type.setdefault(v.get("type", "other"), []).append(v)
        for t, items in by_type.items():
            lines.append(f"\n{t.upper()} violations:")
            for v in items:
                det = v.get("details")
                if isinstance(det, (list, tuple)):
                    lines.append(f"- {' â†’ '.join(det)}")
                else:
                    lines.append(f"- {det}")
        lines.extend([
            "\nRecommendations:",
            "- Break cycles using interfaces/DI",
            "- Keep dependencies one-way (layered)",
            "- Shrink surface of core modules",
        ])
        return "\n".join(lines)

    def _generate_performance_metrics_section(self) -> str:
        if not getattr(self, "performance_metrics_results", None):
            return "\n[PERFORMANCE METRICS]\n" + "=" * 80 + "\nNo performance metrics collected."
        if not self.performance_metrics_results:
            return "\n[PERFORMANCE METRICS]\n" + "=" * 80 + "\nNo performance metrics collected."
        lines = ["\n[PERFORMANCE METRICS]", "=" * 80, "\nPotential performance issues found:"]
        nested = []
        large = []
        for f, m in self.performance_metrics_results.items():
            if m.get('nested_loops', 0) > 2:
                nested.append((f, m['nested_loops']))
            if m.get('large_structures'):
                large.append((f, m['large_structures']))
        if nested:
            lines.append("\nDeeply nested loops (possible bottlenecks):")
            for f, depth in sorted(nested, key=lambda x: x[1], reverse=True)[:5]:
                lines.append(f"- {f}: {depth} levels")
        if large:
            lines.append("\nLarge data structure initializations:")
            for f, structs in large[:5]:
                lines.append(f"- {f}:")
                for s in structs[:3]:
                    lines.append(f"  â€¢ {s}")
                if len(structs) > 3:
                    lines.append(f"  â€¢ ... and {len(structs) - 3} more")
        if not nested and not large:
            lines.append("\nNo significant performance issues detected.")
        lines.extend([
            "\nRecommendations:",
            "- Flatten loops or use vectorization/algorithms",
            "- Consider lazy loading / pagination for big data",
            "- Profile to target real bottlenecks",
        ])
        return "\n".join(lines)

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  dev_tools  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _generate_text_atlas(self):
        try:
            integrated = self._generate_integrated_architecture_overview()
            ascii_deps = self._generate_ascii_dependency_graph()
            ascii_flow = self._generate_ascii_interaction_graph()

            sections = [
                "=" * 80,
                " KANDA PROJECT ARCHITECTURE",
                "=" * 80,
                f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n",
                "\n".join([integrated, ascii_deps, ascii_flow]),
                self._generate_structure_section(),
                self._generate_skipped_files_section(),
                self._generate_component_section(),
                self._generate_signal_flow_section(),
                self._generate_method_call_section(),
                self._generate_testing_section(),
                self._generate_file_listing(),
            ]

            # extra analysis sections
            if self.complexity_results:
                sections.append(self._generate_complexity_section())
            if self.commit_history:
                sections.append(self._generate_git_history_section())
            if self.dependency_warnings:
                sections.append(self._generate_dependency_warnings_section())
            if self.similar_code:
                sections.append(self._generate_similar_code_section())
            if self.architecture_violations:
                sections.append(self._generate_architecture_violations_section())
            if self.performance_metrics_results:
                sections.append(self._generate_performance_metrics_section())
            if getattr(self, "git_metadata", None):
                sections.append("\n[GIT METADATA]\n" + "=" * 80 + "\n" +
                                "\n".join(f"{f}: {md['author']} @ {md['date']}"
                                          for f, md in sorted(self.git_metadata.items())))
            if getattr(self, "recent_changes", None):
                sections.append("\n[RECENT CHANGES]\n" + "=" * 80 + "\n" +
                                "\n".join(f"{c['hash']} | {c['author']} | {c['date']} | {c['msg']}"
                                          for c in self.recent_changes[:10]))

            atlas_path = self.output_dir / f"project_architecture_{self.timestamp}.txt"
            atlas_path.write_text("\n".join(sections), encoding="utf-8")
            print(f"Created architecture file: {atlas_path.name}")
        except Exception as e:
            print(f"Error generating text atlas: {e}")
            raise

    def _generate_complexity_section(self) -> str:
        if not self.complexity_results:
            return ""
        section = ["\n[COMPLEXITY ANALYSIS]", "=" * 80,
                   "\nCyclomatic complexity of functions/methods:"]
        flat = []
        for file, entries in self.complexity_results.items():
            for name, cx in entries:
                flat.append((cx, name, file))
        flat.sort(reverse=True)
        section.append("\nTop 10 most complex functions:")
        for i, (cx, name, file) in enumerate(flat[:10], 1):
            section.append(f"{i:2d}. {name} (complexity: {cx}) in {file}")
        return "\n".join(section)

    def _generate_git_history_section(self) -> str:
        if not self.commit_history:
            return ""
        section = ["\n[GIT HISTORY ANALYSIS]", "=" * 80,
                   f"\nCommit history for the last 30 days ({len(self.commit_history)} commits):"]
        for commit in self.commit_history[:10]:
            section.append(f"\nCommit: {commit['hash']}")
            section.append(f"Author: {commit['author']}")
            section.append(f"Date: {commit['date']}")
            section.append(f"Message: {commit['msg']}")
            if commit.get('changes'):
                section.append("Changes:")
                for file, ch in commit['changes'].items():
                    section.append(f"  {file}: +{ch['additions']}/-{ch['deletions']}")
        return "\n".join(section)

    def _generate_structure_section(self) -> str:
        try:
            structure = ["[PROJECT STRUCTURE]", "=" * 80]
            dir_tree = defaultdict(lambda: defaultdict(list))
            for file in sorted(self.all_files.union(self.resource_files)):
                dir_path = str(Path(file).parent)
                file_type = self._get_file_type(file)
                if file_type == 'test' or 'test' in Path(file).parts:
                    continue
                dir_tree[dir_path][file_type].append(Path(file).name)
            for dir_path in sorted(dir_tree.keys()):
                if any(p.lower() in ('test', 'tests') or 'test' in p.lower() for p in Path(dir_path).parts):
                    continue
                structure.append(f"\nðŸ“‚ {dir_path}/")
                for file_type in sorted(dir_tree[dir_path].keys()):
                    for file in sorted(dir_tree[dir_path][file_type]):
                        structure.append(f" â”œâ”€ {self._get_file_icon(file, file_type)} {file}")
            return '\n'.join(structure)
        except Exception as e:
            print(f"Error generating structure section: {e}")
            return "[Error generating project structure]"

    def _get_file_type(self, filepath: str) -> str:
        filename = Path(filepath).name
        if filename in [Path(f).name for f in self.entry_points]:
            return 'entry_point'
        if 'test' in filename.lower() or 'test' in Path(filepath).parent.name.lower():
            return 'test'
        if any(filename.endswith(ext) for ext in ('.json', '.csv', '.edf')):
            return 'data'
        return 'code'

    def _get_file_icon(self, filename: str, file_type: str) -> str:
        return {'entry_point': 'ðŸš€', 'test': 'ðŸ§ª', 'data': 'ðŸ“Š', 'code': 'ðŸ“„'}.get(file_type, 'ðŸ“„')

    def _generate_skipped_files_section(self) -> str:
        if not self.skipped_files:
            return ""
        skipped = ["\n[SKIPPED FILES]", "=" * 80, "\nThe following files were skipped during analysis:"]
        for file, reason in sorted(self.skipped_files.items()):
            skipped.append(f"\n- {file}: {reason}")
        return '\n'.join(skipped)

    def _generate_component_section(self) -> str:
        try:
            components = ["[KEY COMPONENTS]", "=" * 80]
            important = sorted(
                self.class_roles.items(),
                key=lambda x: (len(self.class_methods.get(x[0], {})),
                               len(self._get_class_dependencies(x[0]))),
                reverse=True
            )[:15]
            for cls, info in important:
                components.append(f"\n{cls}:")
                components.append(f"  - Location: {info.get('file', 'unknown')}")
                components.append(f"  - Purpose: {textwrap.shorten(info.get('purpose', 'No description'), width=80)}")
                methods = list(self.class_methods.get(cls, {}).keys())
                components.append(f"  - Methods: {len(methods)}")
                if methods:
                    components.append("  - Key Methods: " + ", ".join(methods[:5]) + ("..." if len(methods) > 5 else ""))
            return '\n'.join(components)
        except Exception as e:
            print(f"Error generating component section: {e}")
            return "[Error generating component documentation]"

    def _get_class_dependencies(self, class_name: str) -> Set[str]:
        deps = set()
        for file, data in self.file_dependencies.items():
            if class_name in data.get('classes', {}):
                deps.update(data['imports'])
        return deps

    # Signal flows
    def _find_signal_connections(self, file_path: str, signals: Set[str]) -> Dict[str, List[str]]:
        connections: DefaultDict[str, List[str]] = defaultdict(list)
        try:
            content = (self.project_root / file_path).read_text(encoding='utf-8', errors='ignore')
            for signal in signals:
                connect_pattern = re.compile(rf"{signal}\.connect\(([^\)]+)\)")
                matches = connect_pattern.findall(content)
                for m in matches:
                    connections[signal].append(m.strip())
            slot_pattern = re.compile(r"@pyqtSlot\(.*?\)\s*def\s+([^\(]+)")
            slots = slot_pattern.findall(content)
            for s in slots:
                # we don't know which signal, but record under a generic key
                connections["<decorated_slots>"].append(s)
        except Exception:
            pass
        return connections

    def _generate_signal_flow_section(self) -> str:
        try:
            lines = ["[SIGNAL FLOW ANALYSIS]", "=" * 80]
            signal_data = defaultdict(dict)
            for file, data in self.file_dependencies.items():
                if data.get('signals'):
                    signal_data[file]['signals'] = data['signals']
                    signal_data[file]['connections'] = self._find_signal_connections(file, data['signals'])
            if not signal_data:
                return "\n".join(lines + ["\nNo PyQt/PySide signals detected in the project"])
            lines.append("\nSIGNAL DEFINITIONS:")
            for file in sorted(signal_data.keys()):
                lines.append(f"\nðŸ“„ {file}:")
                for sig in sorted(signal_data[file]['signals']):
                    lines.append(f"  - {sig}")
                    if sig in signal_data[file]['connections']:
                        conns = signal_data[file]['connections'][sig]
                        if conns:
                            lines.append(f"    â†³ Connected to: {', '.join(conns)}")
            lines.append("\n\nSIGNAL FLOW DIAGRAM:")
            lines.append("=" * 40)
            lines.append(self._generate_signal_flow_diagram(signal_data))
            return "\n".join(lines)
        except Exception as e:
            print(f"Error generating signal flow section: {e}")
            return "[Error generating signal flow documentation]"

    def _generate_signal_flow_diagram(self, signal_data: Dict) -> str:
        diagram = []
        for file in sorted(signal_data.keys()):
            diagram.append(f"\n[{Path(file).name}]")
            for signal in sorted(signal_data[file]['signals']):
                diagram.append(f"  {signal}")
                if signal in signal_data[file]['connections']:
                    for connection in signal_data[file]['connections'][signal]:
                        diagram.append(f"    â†’ {connection}")
                else:
                    diagram.append("    â†’ (no connections found)")
        return "\n".join(diagram)

    def _generate_method_call_section(self) -> str:
        if not self.method_calls:
            return "[METHOD CALLS]\n" + "=" * 80 + "\nNo method call data collected"
        lines = ["[METHOD CALLS]", "=" * 80, "\nMost frequently called methods:"]
        counter = Counter()
        for calls in self.method_calls.values():
            for c in calls:
                counter[c] += 1
        for method, count in sorted(counter.items(), key=lambda x: x[1], reverse=True)[:20]:
            lines.append(f"  - {method} (called {count} times)")
        return "\n".join(lines)

    def _generate_testing_section(self) -> str:
        lines = ["[TESTING]", "=" * 80]
        if not self.test_files:
            return "\n".join(lines + ["No test files detected"])
        lines.append("\nTest Files Structure:")
        cats = defaultdict(list)
        for t in sorted(self.test_files):
            cats[Path(t).parent.name].append(Path(t).name)
        for cat, files in sorted(cats.items()):
            lines.append(f"\n{cat}/")
            for f in sorted(files):
                lines.append(f"  - {f}")
        lines.append(f"\nTest Coverage Summary:\n  - Total test files: {len(self.test_files)}")
        return "\n".join(lines)

    def _generate_file_listing(self) -> str:
        lines = ["\n[COMPLETE FILE LISTING]", "=" * 80]
        for file in sorted(self.all_files):
            if 'test' in file.lower():
                continue
            fd = self.file_dependencies.get(file, {})
            purpose = fd.get('docstring', "No description available")
            classes = list(fd.get('classes', {}).keys())
            functions = list(fd.get('functions', {}).keys())
            lines.append(f"\n{file}:")
            lines.append(f"  - Purpose: {textwrap.shorten(purpose, width=100)}")
            if classes:
                lines.append(f"  - Classes: {', '.join(classes)}")
            if functions:
                lines.append(f"  - Functions: {', '.join(functions[:5])}" +
                             ("..." if len(functions) > 5 else ""))
            if fd.get('signals'):
                lines.append(f"  - Signals: {', '.join(fd['signals'])}")
        return "\n".join(lines)

    def _generate_dependency_graph(self):
        if not self.generate_media_artifacts:
            print("â†ª Skipping dependency graph media artifacts (generate_media_artifacts=False)")
            return
        try:
            dot = graphviz.Digraph(engine='fdp', name='Project Dependencies',
                                   graph_attr={'rankdir': 'LR', 'splines': 'ortho'})
            TYPE_COLORS = {
                "k05_eeg_filters_deprecated": ("Filters", "lightgreen"),
                "k01_core_eeg": ("Core", "lightblue"),
                "k01_2_visualizer": ("CoreViz", "lightcyan"),
                "k01_3_eeg_visualizer": ("UI", "khaki"),
                "visualizer_core_helpers": ("Helpers", "orange"),
            }
            for file in self.all_files:
                top = file.split(os.sep)[0]
                tag, color = TYPE_COLORS.get(top, ("Code", "white"))
                dot.node(file, label=f"{Path(file).name}\n[{tag}]",
                         shape="box", style="filled", fillcolor=color)
            for src, targets in self.import_graph.items():
                for tgt in targets:
                    for f in self.all_files:
                        if tgt in f:
                            dot.edge(src, f)

            base = os.path.join(self.output_dir, f"dependency_graph_{self.timestamp}")
            dot.format = 'png'
            png_path = dot.render(base, cleanup=False)
            print(f"Created graph image: {png_path}")

            dot.format = 'cmapx'
            cmapx_path = dot.render(base, cleanup=False)
            html_file = f"{base}.html"
            cmapx_text = Path(cmapx_path).read_text(encoding='utf-8')
            html = f"""<html>
  <head><title>Dependency Graph</title></head>
  <body>
    <h2>Dependency Graph ({self.timestamp})</h2>
    <img src="{os.path.basename(png_path)}" usemap="#Project_Dependencies" />
    {cmapx_text}
  </body>
</html>"""
            Path(html_file).write_text(html, encoding='utf-8')
            print(f"Created HTML wrapper: {html_file}")
        except Exception as e:
            print(f"Error generating annotated dependency graph: {e}")

    def _create_ascii_diagram(self, title: str, elements: List[str]) -> str:
        border = "=" * 60
        header = f" {title.center(58)} "
        diagram = [border, header, border]
        for element in elements:
            if "-->" in element:
                left, right = element.split("-->")
                diagram.append(f" {left.strip():<20} â†’ {right.strip():>20}")
            else:
                diagram.append(f" {element}")
        diagram.append(border)
        return "\n".join(diagram)

    def _generate_ascii_diagrams(self):
        try:
            diagrams = [
                self._create_ascii_diagram(
                    "HighPass Filter Flow",
                    ["[UI] --> [Dropdown]",
                     "[Dropdown] --> [FilterEngine]",
                     "[FilterEngine] --> [Visualizer]",
                     "[Visualizer] --> [Display]"]
                ),
                self._create_ascii_diagram(
                    "k01_core_eeg Data Flow",
                    ["[File Loader] --> [Preprocessor]",
                     "[Preprocessor] --> [Signal Processor]",
                     "[Signal Processor] --> [Visualizer]",
                     "[Visualizer] --> [UI Components]"]
                )
            ]
            path = self.output_dir / f"component_diagrams_{self.timestamp}.txt"
            path.write_text("\n\n".join(diagrams), encoding='utf-8')
            print(f"Created diagram file: {path.name}")
        except Exception as e:
            print(f"Error generating ASCII diagrams: {e}")

    def _build_method_index(self) -> None:
        self.method_index: DefaultDict[str, List[Tuple[str, Optional[str]]]] = defaultdict(list)
        for cls, methods in self.class_methods.items():
            cls_file = self.class_roles.get(cls, {}).get("file")
            if not cls_file:
                continue
            for m in methods.keys():
                self.method_index[m].append((cls_file, cls))
        for func_name, func_data in self.function_details.items():
            f = func_data.get("file")
            if f:
                self.method_index[func_name].append((f, None))

    def _generate_ascii_dependency_graph(self) -> str:
        dependency_tree = defaultdict(set)
        for src, targets in self.import_graph.items():
            src_top = src.split(os.sep)[0]
            for t in targets:
                for f in self.all_files:
                    if t in f:
                        tgt_top = f.split(os.sep)[0]
                        if tgt_top != src_top:
                            dependency_tree[src_top].add(tgt_top)
        lines = ["\n" + "=" * 60, " ASCII DEPENDENCY GRAPH", "=" * 60]
        for module, deps in sorted(dependency_tree.items()):
            lines.append(f"\n[{module}]")
            for dep in sorted(deps):
                lines.append(f"  â””â”€â”€ depends on â†’ {dep}")
        return "\n".join(lines)

    def _generate_ascii_interaction_graph(self) -> str:
        lines = [
            "\n" + "=" * 60,
            " SYSTEM INTERACTION FLOW (Conceptual)",
            "=" * 60,
            "",
            " +-----------------------+",
            " |    UI Dropdowns       |  ðŸŽ›ï¸",
            " +-----------------------+",
            "             â”‚",
            "             â–¼",
            " +-----------------------+",
            " | Signal Integrator ðŸ§©  |",
            " +-----------------------+",
            "             â”‚",
            "             â–¼",
            " +-----------------------+",
            " |   EEG Core Manager ðŸ§  |",
            " +-----------------------+",
            "             â”‚",
            "             â–¼",
            " +-----------------------+",
            " |   Filter Pipeline âš™ï¸   |",
            " +-----------------------+",
            "             â”‚",
            "             â–¼",
            " +-----------------------+",
            " |   Renderer Engine ðŸ–¼ï¸   |",
            " +-----------------------+",
            ""
        ]
        return "\n".join(lines)

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Web export â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def export_for_web(self, output_path: Path):
        data = {
            "filesystem": self._build_tree_dict(self.project_root),
            "dependencies": self._build_dependency_graph_elements()
        }
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / "project_data.json"
        output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Exported web visualization data â†’ {output_file}")

    def _build_dependency_graph_elements(self) -> dict:
        nodes = set()
        edges = []
        for src, targets in self.import_graph.items():
            src_id = src.replace(os.sep, "/")
            nodes.add(src_id)
            for tgt in targets:
                tgt_matches = [f for f in self.all_files if tgt in f]
                for tgt_file in tgt_matches:
                    tgt_id = tgt_file.replace(os.sep, "/")
                    nodes.add(tgt_id)
                    edges.append({"data": {"source": src_id, "target": tgt_id}})

        def determine_role(path: str) -> str:
            if "k01_core_eeg" in path:
                return "Core"
            if "k03_tabs" in path:
                return "UI"
            if "k05_eeg_filters_deprecated" in path:
                return "Filters"
            if "k02_eeg_input" in path:
                return "IO"
            if "k07_mcrvlt_snapshot_map" in path:
                return "Visualization"
            return "Other"

        enriched_nodes = []
        for n in nodes:
            role = determine_role(n)
            enriched_nodes.append({"data": {"id": n, "label": Path(n).name, "role": role, "doc": ""}})
        return {"nodes": enriched_nodes, "edges": edges}

    def _build_tree_dict(self, root: Path) -> list:
        def recurse(path: Path) -> Optional[dict]:
            name_lower = path.name.lower()
            if 'test' in name_lower or name_lower in ('test', 'tests'):
                return None
            node = {"id": str(path.relative_to(self.project_root)), "text": path.name}
            if path.is_dir():
                children = []
                for p in sorted(path.iterdir()):
                    if p.name.startswith('.'):
                        continue
                    if 'test' in p.name.lower():
                        continue
                    child = recurse(p)
                    if child:
                        children.append(child)
                node["children"] = children
            return node
        root_node = recurse(root)
        return [root_node] if root_node else []

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Flows â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _parse_slot_expr(self, expr: str) -> str:
        expr = expr.strip()
        expr = re.sub(r"\(.*\)$", "", expr)
        if "." in expr:
            expr = expr.split(".")[-1]
        return expr

    def _best_node_label(self, rel_file: str, cls: Optional[str]) -> str:
        base = Path(rel_file).name
        return f"{cls} ({base})" if cls else base

    def _top_container(self, rel: str) -> str:
        return rel.split("/", 1)[0] if "/" in rel else rel

    def _rel_in_module(self, rel: str, module: str) -> str:
        p = Path(rel)
        parts = p.parts
        return str(Path(*parts[1:])) if parts and parts[0] == module else rel

    def _build_flow_edges(self) -> List[Dict[str, Any]]:
        edges: List[Dict[str, Any]] = []
        seen: Set[Tuple[str, str, str, str]] = set()

        # 1) Signals
        for file, data in self.file_dependencies.items():
            if self._is_test_path(file):
                continue
            sigs: Set[str] = data.get("signals", set()) or set()
            if not sigs:
                continue
            connections = self._find_signal_connections(file, sigs)
            for signal, targets in connections.items():
                for expr in targets:
                    method = self._parse_slot_expr(expr)
                    owners = self.method_index.get(method, [])
                    if not owners:
                        key = (file, "?", f"{signal} â†’ {method}", "signal")
                        if key not in seen:
                            edges.append({"kind": "signal", "label": f"{signal} â†’ {method}",
                                          "src_file": file, "src_class": None,
                                          "dst_file": "?", "dst_class": None})
                            seen.add(key)
                        continue
                    for dst_file, dst_cls in owners:
                        if self._is_test_path(dst_file):
                            continue
                        key = (file, dst_file, f"{signal} â†’ {method}", "signal")
                        if key in seen:
                            continue
                        edges.append({"kind": "signal", "label": f"{signal} â†’ {method}",
                                      "src_file": file, "src_class": None,
                                      "dst_file": dst_file, "dst_class": dst_cls})
                        seen.add(key)

        # 2) Calls
        for src_file, calls in self.method_calls.items():
            if self._is_test_path(src_file):
                continue
            for call in calls:
                label = call + "()"
                dst_file = None
                dst_cls = None
                if "." in call:
                    cls, meth = call.split(".", 1)
                    if cls in self.class_roles:
                        dst_file = self.class_roles[cls]["file"]
                        dst_cls = cls
                    else:
                        owners = self.method_index.get(meth, [])
                        for f, c in owners:
                            if not self._is_test_path(f):
                                dst_file, dst_cls = f, c
                                break
                else:
                    owners = self.method_index.get(call, [])
                    for f, c in owners:
                        if not self._is_test_path(f):
                            dst_file, dst_cls = f, c
                            break
                if not dst_file:
                    key = (src_file, "?", label, "call")
                    if key not in seen:
                        edges.append({"kind": "call", "label": label, "src_file": src_file,
                                      "src_class": None, "dst_file": "?", "dst_class": None})
                        seen.add(key)
                    continue
                key = (src_file, dst_file, label, "call")
                if key in seen or self._is_test_path(dst_file):
                    continue
                edges.append({"kind": "call", "label": label, "src_file": src_file,
                              "src_class": None, "dst_file": dst_file, "dst_class": dst_cls})
                seen.add(key)
        return edges

    def _generate_enriched_ascii_flows(self) -> None:
        try:
            out_file = self.output_dir / f"flows_enriched_{self.timestamp}.txt"
            edges = self._build_flow_edges()
            grouped: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
            for e in edges:
                grouped[self._top_container(e["src_file"].replace("\\", "/"))].append(e)

            lines: List[str] = []
            lines.append("=" * 72)
            lines.append(" ENRICHED ASCII FLOWS â€” annotated with signals/calls")
            lines.append("=" * 72 + "\n")

            for container in sorted(grouped.keys()):
                lines.append("\n" + "=" * 60)
                lines.append(f" {container}")
                lines.append("=" * 60)
                for e in grouped[container]:
                    src_lbl = self._best_node_label(e["src_file"], e.get("src_class"))
                    dst_lbl = "UNRESOLVED" if e["dst_file"] == "?" else self._best_node_label(
                        e["dst_file"], e.get("dst_class"))
                    kind = "SIGNAL" if e["kind"] == "signal" else "CALL"
                    lines.append(f"[{src_lbl}]  --{e['label']}-->  [{dst_lbl}]  ({kind})")

            out_file.write_text("\n".join(lines), encoding="utf-8")
            print(f"ðŸ§­ Enriched flows written â†’ {out_file}")
        except Exception as ex:
            print(f"[flows] Failed: {ex}")

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Onboarding / extras â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def generate_onboarding_readme(self, out_path: Optional[Path] = None) -> Path:
        if not self.all_files:
            self.scan_project_structure()
            for f in self.all_files:
                self.analyze_file(Path(self.project_root) / f)

        entry_points = sorted(self.entry_points)
        tests_total = len(self.test_files)
        reqs_exists = (self.project_root / "requirements.txt").exists()

        lines: List[str] = []
        lines.append("# EEG_KANDA â€” Developer Onboarding (One-Page)\n")
        lines.append("> Run, test, and contribute quickly.\n")
        lines.append("---\n")
        lines.append("## Setup")
        lines.append("```bash")
        lines.append("python -m venv .venv && (. .venv/bin/activate || .venv\\Scripts\\activate)")
        lines.append("pip install -r requirements.txt" if reqs_exists
                     else "pip install -U pip pytest graphviz radon jinja2 pyyaml")
        lines.append("```")
        lines.append("")
        lines.append("## Run")
        if entry_points:
            lines.append("Detected entry points:")
            for ep in entry_points:
                lines.append(f"- `{ep}`")
            lines.append("\n```bash")
            lines.append(f"python {entry_points[0]}")
            lines.append("```")
        else:
            lines.append("```bash\npython k00_main/kanda_runner.py\n```")
        lines.append("")
        lines.append("## Analyzer CLI")
        lines.append("```bash")
        lines.append("python project_analysis/project_analizer_2_runner.py generate-dev_tools")
        lines.append("python project_analysis/project_analizer_2_runner.py onboarding-readme")
        lines.append("python project_analysis/project_analizer_2_runner.py flow-diagrams")
        lines.append("python project_analysis/project_analizer_2_runner.py dep-hotspots")
        lines.append("python dev_tools/project_analysis/project_analizer_2_runner.py debt-report")
        lines.append("```")
        lines.append("")
        lines.append("## Tests")
        lines.append(f"- Discovered **{tests_total}** test files.\n")
        lines.append("```bash\npytest -q\n```")
        lines.append("")
        lines.append("## Contributing")
        lines.append("- Keep dropdown â†’ integrator â†’ visualizer APIs small.")
        lines.append("- Include tests with changes. Prefer small PRs.\n")

        target_file = (out_path or self.project_root) / "README_ONBOARDING.md"
        (self.output_dir / "README_ONBOARDING.md").write_text("\n".join(lines), encoding="utf-8")
        target_file.write_text("\n".join(lines), encoding="utf-8")
        print(f"ðŸ“˜ Onboarding README â†’ {target_file}")
        return target_file

    def generate_clean_flow_diagrams(self) -> List[Path]:
        if not self.generate_media_artifacts:
            print("â†ª Skipping clean flow PNGs/MD (generate_media_artifacts=False)")
            return []
        out_dir = self.output_dir

        def draw(name: str, nodes: List[str]) -> Path:
            g = graphviz.Digraph(name=name, format="png", engine="dot")
            g.attr(rankdir="LR", concentrate="true", nodesep="0.45", ranksep="0.6")
            for n in nodes:
                g.node(n, shape="box", style="rounded,filled", color="#2B6CB0", fillcolor="#E6F0FF")
            for a, b in zip(nodes, nodes[1:]):
                g.edge(a, b, color="#1A202C")
            base = out_dir / f"{name}_{self.timestamp}"
            return Path(g.render(str(base), cleanup=True))

        flow1 = ["UI", "Dropdown", "FilterEngine", "Visualizer", "Display"]
        flow2 = ["File Loader", "Preprocessor", "Signal Processor", "Visualizer", "UI Components"]
        p1 = draw("flow_dropdown_to_visualizer", flow1)
        p2 = draw("flow_data_pipeline", flow2)

        md = out_dir / f"flows_clean_{self.timestamp}.md"
        md.write_text("# Clean Flow Diagrams\n\n" f"![Flow 1]({p1.name})\n\n" f"![Flow 2]({p2.name})\n",
                      encoding="utf-8")
        print(f"ðŸ–¼ï¸  Flow diagrams â†’ {p1}, {p2}")
        return [p1, p2]

    def generate_dependency_hotspots_report(self, top_n: int = 20) -> Path:
        if not self.all_files:
            self.scan_project_structure()
            for f in self.all_files:
                self.analyze_file(Path(self.project_root) / f)

        token_to_files: Dict[str, Set[str]] = defaultdict(set)
        for f in self.all_files:
            tok = Path(f).stem
            token_to_files[tok].add(f)
            token_to_files[self._top_module(f)].add(f)

        fan_out: Dict[str, int] = {}
        fan_in: Counter = Counter()
        for src, imports in self.import_graph.items():
            targets: Set[str] = set()
            for imp in imports:
                first = imp.split(".", 1)[0]
                for tok in (imp, first, Path(imp).stem):
                    targets |= token_to_files.get(tok, set())
            targets &= set(self.all_files)
            fan_out[src] = len(targets)
            for t in targets:
                fan_in[t] += 1

        if not self.complexity_results:
            self.run_complexity_analysis()
        comp_scores: Dict[str, int] = {}
        for f, entries in self.complexity_results.items():
            comp_scores[f] = max([c for _, c in entries], default=0)

        def instability(fi: int, fo: int) -> float:
            denom = fi + fo
            return (fo / denom) if denom else 0.0

        rows = []
        for f in self.all_files:
            fi, fo = fan_in[f], fan_out.get(f, 0)
            I = instability(fi, fo)
            cx = comp_scores.get(f, 0)
            score = 2 * fi + fo + (cx / 10.0)
            rows.append((score, f, fi, fo, I, cx))
        rows.sort(reverse=True)

        mod_agg: Dict[str, Dict[str, float]] = defaultdict(lambda: {"fi": 0, "fo": 0, "cx": 0, "count": 0})
        for _, f, fi, fo, _, cx in rows:
            m = self._top_module(f)
            mod_agg[m]["fi"] += fi
            mod_agg[m]["fo"] += fo
            mod_agg[m]["cx"] += cx
            mod_agg[m]["count"] += 1

        lines = [f"# Dependency Hotspots â€” {datetime.now():%Y-%m-%d}\n"]
        lines.append("## Top Files")
        lines.append("| Rank | File | Fan-In | Fan-Out | Instability | Max Cyclomatic | Score |")
        lines.append("|---:|---|---:|---:|---:|---:|---:|")
        for i, (score, f, fi, fo, I, cx) in enumerate(rows[:top_n], 1):
            lines.append(f"| {i} | `{f}` | {fi} | {fo} | {I:.2f} | {cx} | {score:.1f} |")

        lines.append("\n## Modules (Aggregated)")
        lines.append("| Module | Files | Fan-In | Fan-Out |")
        lines.append("|---|---:|---:|---:|")
        for m, d in sorted(mod_agg.items(), key=lambda kv: (kv[1]["fi"] + kv[1]["fo"]), reverse=True):
            lines.append(f"| {m} | {int(d['count'])} | {int(d['fi'])} | {int(d['fo'])} |")

        out = self.output_dir / f"dependency_hotspots_{self.timestamp}.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        print(f"ðŸ”¥ Hotspots report â†’ {out}")
        return out

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  Advanced analysis  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def run_complexity_analysis(self):
        """Calculate cyclomatic complexity for all functions/methods (robust to BOM/Unicode)."""
        if not self.enable_complexity_analysis:
            return


        self.complexity_results = {}
        for rel_path in sorted(self.all_files):
            full_path = Path(self.project_root) / rel_path
            if not full_path.suffix == ".py":
                continue
            try:
                # read with utf-8-sig to auto-strip BOM; then extra sanitize
                raw = full_path.read_text(encoding="utf-8-sig", errors="ignore")
                safe = self._sanitize_code_for_complexity(raw)

                # quick gate: if the code still has syntax errors, skip gracefully
                try:
                    ast.parse(safe)
                except SyntaxError as e:
                    print(f"Complexity analysis skipped for {rel_path}: {e}")
                    continue

                blocks = cc_visit(safe)
                self.complexity_results[rel_path] = [(b.name, b.complexity) for b in blocks]

            except Exception as e:
                # never crash; just report and continue
                print(f"Complexity analysis failed for {rel_path}: {e}")

    def report_metrics(self, top_n: int = 10):
        # Complexity
        flat = []
        for f, entries in self.complexity_results.items():
            for name, comp in entries:
                flat.append((comp, f, name))
        flat.sort(reverse=True, key=lambda x: x[0])
        print("\n=== Top Cyclomatic Complexity ===")
        for comp, f, name in flat[:top_n]:
            print(f"  {comp:>3} | {f:<40} :: {name}")

        # Fan in/out
        fan_out = {}
        fan_in = Counter()
        for src, imports in self.import_graph.items():
            targets = set()
            for imp in imports:
                for cand in self.all_files:
                    if imp in cand:
                        targets.add(cand)
            fan_out[src] = len(targets)
            for t in targets:
                fan_in[t] += 1
        print("\n=== Top Fan-Out (imports) ===")
        for f, cnt in sorted(fan_out.items(), key=lambda x: x[1], reverse=True)[:top_n]:
            print(f"  {cnt:>3} | {f}")
        print("\n=== Top Fan-In (imported by) ===")
        for f, cnt in fan_in.most_common(top_n):
            print(f"  {cnt:>3} | {f}")

    def run_git_history_analysis(self, since_days=30):
        if not self.enable_git_history_analysis:
            return
        if not (Path(self.project_root) / ".git").exists():
            return
        try:
            result = subprocess.run([
                'git', 'log', f'--since="{since_days} days ago"',
                '--pretty=format:%h|%an|%ad|%s', '--numstat'
            ], cwd=self.project_root, capture_output=True, text=True)
            self.commit_history = []
            current_commit = {}
            for line in result.stdout.split('\n'):
                if '|' in line:
                    if current_commit:
                        self.commit_history.append(current_commit)
                    h, author, date, msg = line.split('|', 3)
                    current_commit = {'hash': h, 'author': author, 'date': date, 'msg': msg, 'changes': {}}
                elif line and '\t' in line:
                    additions, deletions, file = line.split('\t')
                    current_commit['changes'][file] = {
                        'additions': int(additions) if additions != '-' else 0,
                        'deletions': int(deletions) if deletions != '-' else 0
                    }
            if current_commit:
                self.commit_history.append(current_commit)
        except Exception as e:
            print(f"Git history analysis failed: {e}")

    def run_dependency_check(self):
        if not self.enable_dependency_check:
            return
        try:
            req_file = self.project_root / 'requirements.txt'
            self.dependency_warnings = []
            if req_file.exists():
                for req in req_file.read_text().splitlines():
                    r = req.strip()
                    if r and not r.startswith('#'):
                        if '==' not in r and '>=' not in r:
                            self.dependency_warnings.append(f"Unpinned dependency: {r}")
        except Exception as e:
            print(f"Dependency check failed: {e}")

    def run_similarity_check(self, threshold=0.8):
        if not self.enable_similarity_check:
            return
        from difflib import SequenceMatcher
        self.similar_code = []
        files = list(self.all_files)
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                f1 = Path(self.project_root) / files[i]
                f2 = Path(self.project_root) / files[j]
                try:
                    c1 = f1.read_text(encoding='utf-8')
                    c2 = f2.read_text(encoding='utf-8')
                    sim = SequenceMatcher(None, c1, c2).ratio()
                    if sim > threshold:
                        self.similar_code.append({'files': (files[i], files[j]), 'similarity': sim})
                except Exception:
                    continue

    def run_architecture_check(self):
        if not self.enable_architecture_check:
            return
        self.architecture_violations = []
        graph = self._build_import_file_graph()
        cycles = self._find_cycles(graph)
        for cyc in cycles:
            self.architecture_violations.append({'type': 'circular_import', 'details': cyc})
        self._check_layer_violations()

    def _build_import_file_graph(self) -> Dict[str, Set[str]]:
        graph = defaultdict(set)
        for src, imports in self.import_graph.items():
            for imp in imports:
                for target in self.all_files:
                    if imp in target:
                        graph[src].add(target)
        return graph

    def _find_cycles(self, graph: Dict[str, Set[str]]) -> List[List[str]]:
        visited, stack, cycles = set(), [], []

        def dfs(node: str):
            if node in stack:
                idx = stack.index(node)
                cycles.append(stack[idx:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            stack.append(node)
            for nbr in graph.get(node, []):
                dfs(nbr)
            stack.pop()

        for n in list(graph.keys()):
            if n not in visited:
                dfs(n)
        return cycles

    def _check_layer_violations(self):
        layers = {
            'ui': ['k03_tabs', 'k05_eeg_filters_deprecated', 'k05_combobox_forge'],
            'core': ['k01_core_eeg', 'k02_eeg_input'],
            'data': ['k04_eeg_data_management'],
            'utils': ['k06_templates', 'k07_mcrvlt_snapshot_map'],
        }
        for src_file, imports in self.import_graph.items():
            src_layer = None
            for lname, dirs in layers.items():
                if any(d in src_file for d in dirs):
                    src_layer = lname
                    break
            if not src_layer:
                continue
            for imp in imports:
                for lname, dirs in layers.items():
                    if any(d in imp for d in dirs):
                        if (src_layer == 'ui' and lname == 'data') or \
                           (src_layer == 'ui' and lname == 'utils') or \
                           (src_layer == 'core' and lname == 'data'):
                            self.architecture_violations.append({
                                'type': 'layer_violation',
                                'details': f"{src_file} ({src_layer}) imports {imp} ({lname})"
                            })
                        break

    def run_performance_analysis(self):
        if not self.enable_performance_metrics:
            return
        self.performance_metrics_results = {}
        for file_path in self.all_files:
            full_path = Path(self.project_root) / file_path
            try:
                content = full_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                content = ""
            nested = self._count_nested_loops(content)
            large = self._find_large_data_structures(content)
            self.performance_metrics_results[file_path] = {'nested_loops': nested, 'large_structures': large}

    def _count_nested_loops(self, content: str) -> int:
        try:
            tree = ast.parse(content)
        except Exception:
            return 0
        class V(ast.NodeVisitor):
            def __init__(self): self.depth = 0; self.max_depth = 0
            def visit_For(self, node): self.depth+=1; self.max_depth=max(self.max_depth,self.depth); self.generic_visit(node); self.depth-=1
            def visit_While(self, node): self.depth+=1; self.max_depth=max(self.max_depth,self.depth); self.generic_visit(node); self.depth-=1
        v = V(); v.visit(tree); return v.max_depth

    def _find_large_data_structures(self, content: str) -> List[str]:
        try:
            tree = ast.parse(content)
        except Exception:
            return []
        large: List[str] = []
        class V(ast.NodeVisitor):
            def visit_List(self, node):
                if len(node.elts) > 10: large.append(f"List with {len(node.elts)} elements")
                self.generic_visit(node)
            def visit_Dict(self, node):
                if len(node.keys) > 10: large.append(f"Dict with {len(node.keys)} elements")
                self.generic_visit(node)
        V().visit(tree)
        return large

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Export model (single definition) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def export_model(self, fmt: str = "json", out_path: Union[str, Path, None] = None) -> None:
        if not self.all_files:
            self.scan_project_structure()
        for f in self.all_files:
            self.analyze_file(Path(self.project_root) / f)
        if not self.feature_index:
            self.build_feature_index()
        _export_model(self, fmt=fmt, out_path=out_path)

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Module flows (public wrapper) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def generate_module_ascii_relationships(self, *module_roots: str):
        # For now, unfilteredâ€”project-wide
        return self._generate_enriched_ascii_flows()

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Integrated overview (pretty tree) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _generate_integrated_architecture_overview(self) -> str:
        ICONS = {"dir": "ðŸ“‚", ".py": "ðŸ“„", ".json": "ðŸ§¾", ".md": "ðŸ“˜", ".csv": "ðŸ“Š", ".edf": "ðŸ§ "}
        def icon_for(file: str) -> str:
            for k, v in ((".py","ðŸ“„"),(".json","ðŸ§¾"),(".md","ðŸ“˜"),(".csv","ðŸ“Š"),(".edf","ðŸ§ ")):
                if file.endswith(k): return v
            return "ðŸ“„"
        lines: List[str] = []
        lines.append("=" * 95)
        lines.append("KANDA EEG VISUALIZATION PLATFORM - INTEGRATED ARCHITECTURE")
        lines.append(f"Generated on: {datetime.now():%Y-%m-%d %H:%M}")
        lines.append("=" * 95 + "\n")
        lines.append("ðŸ“¦ Project Root: " + self.project_root.name + "\n")
        for root, dirs, files in os.walk(self.project_root):
            rel_path = Path(root).relative_to(self.project_root)
            if any(part.startswith(".") or part == "__pycache__" for part in rel_path.parts):
                continue
            if any("test" in part.lower() for part in rel_path.parts):
                continue
            depth = len(rel_path.parts)
            if depth == 0:
                continue
            indent = "â”‚   " * (depth - 1)
            folder_name = rel_path.name
            lines.append(f"{indent}{ICONS['dir']} {folder_name}/")
            for file in sorted(files):
                if file.startswith('.') or file.endswith(('.pyc', '.pyo')):
                    continue
                rel = (rel_path / file).as_posix()
                if self._is_test_path(rel):
                    continue
                lines.append(f"{indent}â”‚   {icon_for(file)} {file}")
        return "\n".join(lines)

    # helpers
    def _top_module(self, rel: str) -> str:
        return Path(rel).parts[0] if rel else ""

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    # File-groups: load, resolve, and report relationships for a subset
    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _groups_file(self) -> Path:
        """Default location for the groups YAML."""
        return Path(self.project_root) / "dev_tools" / "project_analysis" / "file_groups.yaml"

    def load_file_groups(self) -> Dict[str, List[str]]:
        """
        Load YAML mapping {group_name: [paths|globs|folders]}.
        Example YAML:
          core-ui:
            - k01_core_eeg/**/*.py
            - k03_tabs/**/*.py
          combobox-helpers:
            - k05_combobox_forge/**/cmbbx_*helper*.py
        """
        yml = self._groups_file()
        if not yml.exists():
            return {}
        try:
            import yaml  # already imported in your file
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
            return data or {}
        except Exception as e:
            print(f"[groups] Failed to read {yml}: {e}")
            return {}

        # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # Internals used by both
        # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def _normalize_rel_paths(self, rels: List[str]) -> List[str]:
        """
        - Normalizes slashes
        - Keeps only files that exist and are .py
        - Returns repo-relative POSIX paths
        """
        normed = []
        for r in rels:
            p = (self.project_root / r).resolve()
            try:
                rp = p.relative_to(self.project_root)
            except Exception:
                # if user passed absolute path, try to detect it inside project
                if p.exists():
                    # best effort: turn absolute to relative if under project
                    try:
                        rp = p.relative_to(self.project_root)
                    except Exception:
                        continue
                else:
                    continue
            if rp.suffix == ".py" and (self.project_root / rp).exists():
                normed.append(rp.as_posix())
        return normed

    def _scan_subset(self, files: List[str]) -> None:
        """
        Re-scan just the subset to ensure AST, imports, calls and signals exist for them.
        This DOES NOT clear global state; it keeps whole-project info available for resolution.
        """
        for rel in files:
            self.analyze_file(self.project_root / rel)

        # method index might need refresh to resolve calls/slots properly
        self._build_method_index()

    def _subset_import_graph(self, files: List[str]) -> Dict[str, Set[str]]:
        """
        Return a pruned import graph containing only edges where both ends are inside 'files'.
        """
        set(files)
        sub = defaultdict(set)
        for src in files:
            for token in self.import_graph.get(src, set()):
                # token may be top-level or submodule; resolve to actual files we know
                for cand in files:
                    if token in cand:
                        sub[src].add(cand)
        return sub

    def _subset_call_edges(self, files: List[str]) -> List[Tuple[str, str, str]]:
        """
        Returns [(src_file, dst_file, label)] for method/function calls where both ends resolve within files.
        """
        files_set = set(files)
        edges = []
        for src, calls in self.method_calls.items():
            if src not in files_set:
                continue
            for call in calls:
                method = call.split(".")[-1]
                owners = self.method_index.get(method, [])
                # pick first owner inside subset
                for dst_file, dst_cls in owners:
                    if dst_file in files_set:
                        label = call + "()" if not call.endswith(")") else call
                        edges.append((src, dst_file, label))
                        break
        return edges

    def _subset_signal_edges(self, files: List[str]) -> List[Tuple[str, str, str]]:
        """
        Returns [(src_file, dst_file| '?', 'signal â†’ method')] for Qt signal connections in subset files.
        """
        files_set = set(files)
        edges = []
        for f in files:
            conns = self._find_signal_connections(f)
            for signal, targets in conns.items():
                for expr in targets:
                    method = self._parse_slot_expr(expr)
                    owners = self.method_index.get(method, [])
                    if not owners:
                        edges.append((f, "?", f"{signal} â†’ {method}"))
                        continue
                    # prefer first owner in subset
                    dst = next((df for (df, cls) in owners if df in files_set), None)
                    edges.append((f, dst if dst else "?", f"{signal} â†’ {method}"))
        return edges

    def _relationship_report(self, files: List[str], *, tag: str, render_png: bool) -> Path:
        """
        Central routine: builds subset graph (imports + calls + signals),
        writes TXT + JSON (and optional PNG/HTML).
        """
        if not files:
            raise ValueError("No files provided for subset report.")

        # ensure analysis for these files is available
        self._scan_subset(files)

        # assemble edges
        import_edges = []
        sub_imports = self._subset_import_graph(files)
        for src, tgts in sub_imports.items():
            for t in sorted(tgts):
                import_edges.append((src, t, "import"))

        call_edges = [(a, b, "call: " + lbl) for (a, b, lbl) in self._subset_call_edges(files)]
        signal_edges = [(a, b, "signal: " + lbl) for (a, b, lbl) in self._subset_signal_edges(files)]

        # collect minimal per-file metadata (first docstring line + classes + functions)
        file_meta = {}
        for f in files:
            d = self.file_dependencies.get(f, {})
            doc = d.get("docstring", "") or ""
            if "\n" in doc:
                doc = doc.split("\n", 1)[0]
            file_meta[f] = {
                "doc": doc,
                "classes": sorted((d.get("classes") or {}).keys()),
                "functions": sorted((d.get("functions") or {}).keys()),
            }

        # JSON (AI-friendly)
        json_data = {
            "tag": tag,
            "generated": self.timestamp,
            "files": files,
            "meta": file_meta,
            "edges": [
                         {"src": a, "dst": b, "kind": "import"} for (a, b, _) in import_edges
                     ] + [
                         {"src": a, "dst": b, "kind": "call", "label": _.replace("call: ", "", 1)}
                         for (a, b, _) in call_edges
                     ] + [
                         {"src": a, "dst": b, "kind": "signal", "label": _.replace("signal: ", "", 1)}
                         for (a, b, _) in signal_edges
                     ]
        }

        base = self.output_dir / f"{tag}_rel_{self.timestamp}"
        json_path = base.with_suffix(".json")
        json_path.write_text(json.dumps(json_data, indent=2), encoding="utf-8")

        # TXT (human quick-read)
        lines = [
            f"SUBSET RELATIONSHIP REPORT â€” {tag}",
            f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
            f"Files ({len(files)}):",
        ]
        for f in files:
            lines.append(f"  - {f} :: {file_meta[f]['doc'] or 'No doc'}")
        lines.append("\n[IMPORT EDGES]")
        for a, b, _ in import_edges:
            lines.append(f"  {a}  â†’  {b}")
        lines.append("\n[CALL EDGES]")
        for a, b, lbl in call_edges:
            lines.append(f"  {a}  -- {lbl} -->  {b}")
        lines.append("\n[SIGNAL EDGES]")
        for a, b, lbl in signal_edges:
            dst = b if b != "?" else "UNRESOLVED"
            lines.append(f"  {a}  -- {lbl} -->  {dst}")

        txt_path = base.with_suffix(".txt")
        txt_path.write_text("\n".join(lines), encoding="utf-8")

        # Optional tiny Graphviz PNG + HTML (subset only)
        if render_png and self.generate_media_artifacts:
            try:
                g = graphviz.Digraph(name=f"Subset_{tag}", engine="dot", format="png")
                g.attr(rankdir="LR", concentrate="true", nodesep="0.4", ranksep="0.6")
                for f in files:
                    g.node(f, label=Path(f).name, shape="box", style="rounded,filled",
                           color="#2B6CB0", fillcolor="#E6F0FF")
                # imports in grey, calls in blue, signals in green (unresolved signals go to a diamond)
                for a, b, _ in import_edges:
                    g.edge(a, b, color="#666666", penwidth="1.2")
                for a, b, lbl in call_edges:
                    g.edge(a, b, label=lbl, color="#1A73E8")
                unresolved_added = False
                for a, b, lbl in signal_edges:
                    if b == "?":
                        # add one shared unresolved node
                        if not unresolved_added:
                            g.node("UNRESOLVED", shape="diamond", style="filled", fillcolor="#FFE8E8", color="#C53030")
                            unresolved_added = True
                        g.edge(a, "UNRESOLVED", label=lbl, color="#16A34A")
                    else:
                        g.edge(a, b, label=lbl, color="#16A34A")
                png = Path(g.render(str(base), cleanup=True))
                # small HTML wrapper (no cmapx to stay minimal)
                html = base.with_suffix(".html")
                html.write_text(
                    f"<!doctype html><meta charset='utf-8'>"
                    f"<h3>Subset graph: {tag} ({self.timestamp})</h3>"
                    f"<img src='{png.name}'/>",
                    encoding="utf-8"
                )
            except Exception as e:
                print(f"[subset-graph] skipped PNG/HTML: {e}")

        print(f"ðŸ“¦ Wrote: {txt_path.name}, {json_path.name}" + ("" if not render_png else " (+ graph)"))
        return txt_path

