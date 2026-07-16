"""Support missing-docstring insertion workflows."""

def require_positive(value: int) -> int:
    if value <= 0:
        raise ValueError("value must be positive")
    return value

def read_flag(mapping: dict[str, bool], key: str) -> bool:
    if key not in mapping:
        raise KeyError(key)
    return mapping[key]
