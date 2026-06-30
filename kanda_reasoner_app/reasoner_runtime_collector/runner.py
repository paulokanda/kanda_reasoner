# project-path: kanda_reasoner_app/reasoner_runtime_collector/runner.py
"""Canonical runtime collector runner facade.

This module replaces the retired project_reasoner_v10_runtime_collector
package name. It keeps runtime collector imports stable while delegating
runtime execution to the canonical shell runner payload.
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any


_SHELL_RUNNER_MODULE = "kanda_reasoner_app.reasoner_tools_shell.runner"


def _load_shell_runner() -> ModuleType:
    """Load the canonical shell runner module."""
    return importlib.import_module(_SHELL_RUNNER_MODULE)


class Runner:
    """Small facade that delegates construction to the shell runner."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """Support new behavior.
        
        Parameters
        ----------
        *args : Any
            The positional arguments.
        **kwargs : Any
            The kwargs value.
        
        Returns
        -------
        Any
            The any result.
        """
        
        shell_runner = _load_shell_runner()

        for candidate_name in (
            "Runner",
            "ReasonerToolsShellRunner",
            "ShellRunner",
            "ToolRunner",
        ):
            candidate = getattr(shell_runner, candidate_name, None)
            if isinstance(candidate, type) and candidate is not cls:
                return candidate(*args, **kwargs)

        return shell_runner


def __getattr__(name: str) -> Any:
    """Delegate unknown attributes to the canonical shell runner."""
    return getattr(_load_shell_runner(), name)
