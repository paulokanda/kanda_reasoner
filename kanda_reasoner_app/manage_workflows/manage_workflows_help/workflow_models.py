"""Own workflow validation result data structures."""

from __future__ import annotations

import argparse
import contextlib
import difflib
import fnmatch
import importlib.util
import io
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

__all__ = [
    "CheckResult",
]

@dataclass(slots=True)
class CheckResult:
    category: str
    name: str
    status: str
    message: str
    duration_seconds: float = 0.0
    command: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "duration_seconds": self.duration_seconds,
            "command": self.command,
            "details": self.details,
        }
