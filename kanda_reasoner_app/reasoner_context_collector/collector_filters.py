# project-path: kanda_reasoner_app/reasoner_context_collector/collector_filters.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import Path

from .collector_config import CollectorConfig

def should_exclude_dir(dirname: str, config: CollectorConfig) -> bool:
    """Support should exclude dir behavior.
    
    Parameters
    ----------
    dirname : str
        The dirname value.
    config : CollectorConfig
        The configuration data.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = dirname.strip().lower()
    return lowered in {item.lower() for item in config.excluded_dirs}


def should_exclude_file(path: Path, config: CollectorConfig) -> bool:
    """Support should exclude file behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    config : CollectorConfig
        The configuration data.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = path.name.lower()

    if lowered.endswith(".pyc"):
        return True

    if lowered.startswith("."):
        return True

    if not config.include_tests and "test" in lowered:
        return True

    return False
