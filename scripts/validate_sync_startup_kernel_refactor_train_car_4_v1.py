"""Validate Sync Startup Kernel Refactor Train Car 4 v1.

This validation keeps the refactor focused on ZIP delivery contract extraction.
It proves that zip_delivery remains the public compatibility surface while the
contract helpers live in zip_contract.
"""

from __future__ import annotations

import importlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "sync-startup-kernel-refactor-train-car-4-v1"
MAX_MODULE_LINES = 500
IDEAL_MODULE_LINES = 400


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read_text(path).splitlines())


def validate_files() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    startup_kernel = prompt_tools / "startup_kernel"
    zip_delivery = startup_kernel / "zip_delivery.py"
    zip_contract = startup_kernel / "zip_contract.py"
    entrypoint = prompt_tools / "sync_startup_routing_kernel_pack.py"

    for path in (zip_delivery, zip_contract, entrypoint):
        _assert(path.exists(), "missing expected file: " + str(path))
        _assert(_line_count(path) <= MAX_MODULE_LINES, "module exceeds max line count: " + str(path))

    _assert(_line_count(zip_delivery) <= IDEAL_MODULE_LINES, "zip_delivery.py should remain under ideal line count")
    _assert(_line_count(zip_contract) <= IDEAL_MODULE_LINES, "zip_contract.py should remain under ideal line count")

    delivery_text = _read_text(zip_delivery)
    contract_text = _read_text(zip_contract)
    entrypoint_text = _read_text(entrypoint)

    _assert("from startup_kernel.zip_contract import" in delivery_text,
            "zip_delivery.py must import public contract helpers from zip_contract.py")
    _assert("def read_manifest_from_zip(" not in delivery_text,
            "read_manifest_from_zip must not be redefined in zip_delivery.py")
    _assert("def validate_generated_zip_contract(" not in delivery_text,
            "validate_generated_zip_contract must not be redefined in zip_delivery.py")
    _assert("def find_delivery_zip(" in delivery_text, "zip_delivery.py must keep find_delivery_zip")
    _assert("def make_zip(" in delivery_text, "zip_delivery.py must keep make_zip")

    _assert("def read_manifest_from_zip(" in contract_text,
            "zip_contract.py must own read_manifest_from_zip")
    _assert("def validate_generated_zip_contract(" in contract_text,
            "zip_contract.py must own validate_generated_zip_contract")
    _assert("ACTIVE_FREEZE_CONTEXT_FILENAME" in contract_text,
            "zip_contract.py must validate active freeze context contract")

    _assert("from startup_kernel.zip_delivery import (" in entrypoint_text,
            "entrypoint must keep zip_delivery compatibility import surface")
    _assert('"read_manifest_from_zip"' in entrypoint_text,
            "entrypoint __all__ must keep read_manifest_from_zip")
    _assert('"validate_generated_zip_contract"' in entrypoint_text,
            "entrypoint __all__ must keep validate_generated_zip_contract")


def validate_public_import_surface() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    sys.path.insert(0, str(prompt_tools))

    zip_delivery = importlib.import_module("startup_kernel.zip_delivery")
    zip_contract = importlib.import_module("startup_kernel.zip_contract")
    entrypoint = importlib.import_module("sync_startup_routing_kernel_pack")

    _assert(zip_delivery.read_manifest_from_zip is zip_contract.read_manifest_from_zip,
            "zip_delivery must re-export read_manifest_from_zip from zip_contract")
    _assert(zip_delivery.validate_generated_zip_contract is zip_contract.validate_generated_zip_contract,
            "zip_delivery must re-export validate_generated_zip_contract from zip_contract")
    _assert(entrypoint.read_manifest_from_zip is zip_contract.read_manifest_from_zip,
            "entrypoint public surface must preserve read_manifest_from_zip")
    _assert(entrypoint.validate_generated_zip_contract is zip_contract.validate_generated_zip_contract,
            "entrypoint public surface must preserve validate_generated_zip_contract")


def validate_contract_helper_behavior() -> None:
    root = _repo_root()
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    sys.path.insert(0, str(prompt_tools))

    from startup_freeze_context import ACTIVE_FREEZE_CONTEXT_FILENAME
    from startup_kernel.constants import MANIFEST_FILENAME, READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME
    from startup_kernel.zip_delivery import read_manifest_from_zip, validate_generated_zip_contract

    with tempfile.TemporaryDirectory(prefix="kanda_train_car_4_validation_") as temp_name:
        temp_dir = Path(temp_name)
        zip_path = temp_dir / "sample.zip"
        manifest = {"manifest_version": "test", "files": []}
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr(MANIFEST_FILENAME, json.dumps(manifest))
            z.writestr("00_START_HERE_FOR_AI.md", "Anti-bypass rule\nDo not implement anything\nDo not create a patch\nzz_read_only_if_modifying_startup_delivery.md\nRouted Work Path\n07_daily_patch_delivery_guardrails.md\n01_ai_prompt_request_canon.md\n")
            z.writestr("README_STARTUP_PROMPT_REQUEST_KERNEL.md", "readme")
            z.writestr("01_ai_prompt_request_canon.md", "canon")
            z.writestr(ACTIVE_FREEZE_CONTEXT_FILENAME, "\n".join([
                "ACTIVE PROJECT FREEZE CONTEXT",
                "Post-validation freeze awareness rule",
                "Freeze Feature After Update tab",
                "generated exposure copy",
                "First-prompt delivery certification",
                "Create First Prompt Files must insert this file into first_prompts_to_ai.zip",
                "<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory/",
                "Runtime source is completely correct",
            ]))
            z.writestr(READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME, "STARTUP DELIVERY READ ORDER - READ tell_AI_read_before_all.md FIRST")

        parsed_manifest = read_manifest_from_zip(zip_path)
        _assert(parsed_manifest == manifest, "read_manifest_from_zip did not return manifest")
        validate_generated_zip_contract(zip_path, expected_generated_filenames=["01_ai_prompt_request_canon.md"])


def main() -> int:
    validate_files()
    validate_public_import_surface()
    validate_contract_helper_behavior()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
