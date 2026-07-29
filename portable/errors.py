"""Portable workflow errors."""


class PortableBuildError(RuntimeError):
    """Raised when the governed Portable workflow must fail closed."""
