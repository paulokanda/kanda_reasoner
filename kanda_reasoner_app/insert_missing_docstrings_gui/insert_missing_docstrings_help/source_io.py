# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/source_io.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Source text IO and parsing helpers
# EXPORTS       : UTF8_BOM, read_source_text, write_source_text, parse_source
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Source text IO and parsing helpers."""

from __future__ import annotations

import ast
import warnings
from pathlib import Path

__all__ = [
    "UTF8_BOM",
    "read_source_text",
    "write_source_text",
    "parse_source",
]


UTF8_BOM = b"\xef\xbb\xbf"

def read_source_text(path: Path) -> tuple[str, bool]:
    """Handle read source text.
    
    Parameters
    ----------
    path : Path
        TODO: describe path.
    
    Returns
    -------
    tuple[str, bool]
        TODO: describe the return value.
    """
    
    raw = path.read_bytes()
    had_bom = raw.startswith(UTF8_BOM)
    return raw.decode("utf-8-sig"), had_bom

def write_source_text(path: Path, text: str, had_bom: bool) -> None:
    """Handle write source text.
    
    Parameters
    ----------
    path : Path
        TODO: describe path.
    text : str
        TODO: describe text.
    had_bom : bool
        TODO: describe had_bom.
    """
    
    encoding = "utf-8-sig" if had_bom else "utf-8"
    path.write_text(text, encoding=encoding, newline="\n")

def parse_source(text: str, path: Path) -> ast.Module:
    """Handle parse source.
    
    Parameters
    ----------
    text : str
        TODO: describe text.
    path : Path
        TODO: describe path.
    
    Returns
    -------
    ast.Module
        TODO: describe the return value.
    """
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(text, filename=str(path))
