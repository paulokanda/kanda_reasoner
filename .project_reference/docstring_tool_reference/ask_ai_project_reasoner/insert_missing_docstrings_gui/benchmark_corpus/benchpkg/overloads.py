"""Support missing-docstring insertion workflows."""

from typing import overload

@overload
def coerce(value: int) -> int: ...
@overload
def coerce(value: str) -> str: ...

def coerce(value):
    if isinstance(value, str):
        return value.strip()
    return int(value)
