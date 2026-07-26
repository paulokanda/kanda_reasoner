# project-path: scripts/validate_sync_startup_kernel_refactor_train_car_6_v1.py
"""Validate Sync Startup Routing Kernel Refactor Train Car 6 v1."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

FEATURE_ID = "sync-startup-kernel-refactor-train-car-6-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
STARTUP_KERNEL = PROMPT_TOOLS / "startup_kernel"


def _line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(path.read_text(encoding="utf-8").splitlines())


def _require(condition: bool, message: str) -> None:
    """Support require behavior.
    
    Parameters
    ----------
    condition : bool
        The condition value.
    message : str
        The message text.
    """
    
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    if str(PROMPT_TOOLS) not in sys.path:
        sys.path.insert(0, str(PROMPT_TOOLS))

    maintenance_text_path = STARTUP_KERNEL / "maintenance_text.py"
    maintenance_body_path = STARTUP_KERNEL / "maintenance_body.py"
    _require(maintenance_text_path.exists(), "maintenance_text.py is missing")
    _require(maintenance_body_path.exists(), "maintenance_body.py is missing")

    maintenance_text_lines = _line_count(maintenance_text_path)
    maintenance_body_lines = _line_count(maintenance_body_path)
    _require(maintenance_text_lines <= 80, f"maintenance_text.py is too large: {maintenance_text_lines}")
    _require(maintenance_body_lines <= 400, f"maintenance_body.py is too large: {maintenance_body_lines}")

    for path in sorted(STARTUP_KERNEL.glob("*.py")):
        count = _line_count(path)
        _require(count <= 500, f"startup_kernel helper exceeds 500-line law: {path.name} has {count} lines")

    text_source = maintenance_text_path.read_text(encoding="utf-8")
    body_source = maintenance_body_path.read_text(encoding="utf-8")
    _require("make_modify_startup_delivery_protocol_body" in text_source, "public wrapper does not delegate to body helper")
    _require("def make_modify_startup_delivery_protocol(" in text_source, "public maintenance function missing")
    _require("def make_modify_startup_delivery_protocol_body(" in body_source, "body helper function missing")
    _require("Required validation evidence" in body_source, "maintenance protocol validation evidence section missing")
    _require("Final rule" in body_source, "maintenance protocol final rule section missing")

    maintenance_text = importlib.import_module("startup_kernel.maintenance_text")
    maintenance_body = importlib.import_module("startup_kernel.maintenance_body")
    sync_module = importlib.import_module("sync_startup_routing_kernel_pack")

    generated_at = "2026-06-29T00:00:00Z"
    zip_filename = "first_prompts_to_ai.zip"
    public_output = maintenance_text.make_modify_startup_delivery_protocol(generated_at, zip_filename)
    body_output = maintenance_body.make_modify_startup_delivery_protocol_body(generated_at, zip_filename)
    sync_output = sync_module.make_modify_startup_delivery_protocol(generated_at, zip_filename)

    _require(public_output == body_output, "public wrapper output differs from maintenance body output")
    _require(sync_output == public_output, "sync public import surface does not expose the same maintenance output")

    required_fragments = [
        "# PASTE IF MODIFYING STARTUP DELIVERY",
        "prompt_tools/",
        "first_prompt_files/",
        "STARTUP_ROUTING_KERNEL_SOURCES.json",
        "sync_startup_routing_kernel_pack.py",
        "tell_AI_read_before_all.md",
        "zz_read_only_if_modifying_startup_delivery.md",
        "Required validation evidence",
        "STARTUP DELIVERY MODIFICATION RESULT",
        "This file is for startup delivery maintenance only.",
    ]
    for fragment in required_fragments:
        _require(fragment in public_output, "maintenance output missing fragment: " + fragment)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
