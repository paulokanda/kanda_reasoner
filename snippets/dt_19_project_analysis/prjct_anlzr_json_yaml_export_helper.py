# File: project_analysis/prjct_anlzr_json_yaml_export_helper.py

"""
Dump a ProjectAnalyzer’s in-memory model to JSON or YAML.
"""

import json
import yaml
from pathlib import Path
from typing import Any, Union
from collections import defaultdict

__all__ = ["export_model"]

def _make_serializable(obj: Any) -> Any:
    """
    Recursively convert sets/tuples/defaultdicts into
    lists/dicts so that the entire structure becomes JSON/YAML serializable.
    """
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_make_serializable(v) for v in obj]
    if isinstance(obj, defaultdict):
        return _make_serializable(dict(obj))
    return obj

def export_model(
    analyzer: Any,
    fmt: str = "json",
    out_path: Union[str, Path] = None
) -> None:
    """
    Serialize `analyzer`’s project model to disk in JSON or YAML.
    """
    # Build the raw model (deep‐convert any sets)
    model = {
        "files": list(analyzer.all_files),
        "resources": list(analyzer.resource_files),
        "tests": list(analyzer.test_files),
        "entry_points": list(analyzer.entry_points),
        "file_dependencies": {
            fp: {
                "imports": list(data.get("imports", [])),
                "classes": data.get("classes", {}),
                "functions": data.get("functions", {}),
                "docstring": data.get("docstring", ""),
                "signals": list(data.get("signals", [])),
                "method_calls": list(data.get("method_calls", [])),
            }
            for fp, data in analyzer.file_dependencies.items()
        },
        "class_roles": analyzer.class_roles,
        "class_methods": analyzer.class_methods,
        "function_details": analyzer.function_details,
        "import_graph": {k: list(v) for k, v in analyzer.import_graph.items()},
        "signals": analyzer.signals,
        "method_calls": analyzer.method_calls,
        "feature_index": {k: list(v) for k, v in analyzer.feature_index.items()},
    }

    # Determine output path
    out_path = Path(out_path) if out_path else Path(analyzer.output_dir) / f"project_model.{fmt}"

    # Make everything serializable
    serializable = _make_serializable(model)

    # Dump
    if fmt == "json":
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
    elif fmt == "yaml":
        # with open(out_path, "w", encoding="utf-8") as f:
        #     yaml.safe_dump(serializable)
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(serializable, f)    # ← pass the file handle!
    else:
        raise ValueError(f"Unknown format {fmt!r}")

    print(f"Exported project model to {out_path}")

