# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_decorators.py
"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from runtime_trace_api import get_runtime_trace_writer


def trace_runtime_event(
    event_type: str,
    source_file: str,
    source_symbol: str,
) -> Callable:
    """Support trace runtime event behavior.
    
    Parameters
    ----------
    event_type : str
        The event type value.
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    
    Returns
    -------
    Callable
        The callable result.
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            writer = get_runtime_trace_writer()
            if writer is not None:
                writer.trace_event(
                    event_type=event_type,
                    source_file=source_file,
                    source_symbol=source_symbol,
                    message="entered",
                )

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                writer = get_runtime_trace_writer()
                if writer is not None:
                    writer.trace_error(
                        source_file=source_file,
                        source_symbol=source_symbol,
                        message=str(exc),
                    )
                raise

            writer = get_runtime_trace_writer()
            if writer is not None:
                writer.trace_event(
                    event_type=event_type,
                    source_file=source_file,
                    source_symbol=source_symbol,
                    message="completed",
                )

            return result

        return wrapper

    return decorator
