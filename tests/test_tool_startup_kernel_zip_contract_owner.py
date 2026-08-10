"""Focused public-contract tests for startup-kernel ZIP ownership."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

from startup_kernel.constants import MANIFEST_FILENAME

ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = ROOT / "kanda_prompt_workspace/prompt_tools"
if str(PROMPT_TOOLS) not in sys.path:
    sys.path.insert(0, str(PROMPT_TOOLS))

CONTRACT_MODULE = "startup_kernel.zip_contract"
DELIVERY_MODULE = "startup_kernel.zip_delivery"
CONTRACT_NAMES = {
    "read_manifest_from_zip",
    "validate_generated_zip_contract",
}


def _module_text(node: ast.ImportFrom) -> str:
    return "." * node.level + (node.module or "")


def _imported_names(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and _module_text(node) == module:
            names.update(alias.name for alias in node.names)
    return names


class StartupKernelZipContractOwnerTests(unittest.TestCase):
    def test_contract_helpers_have_one_definition_owner(self) -> None:
        kernel = PROMPT_TOOLS / "startup_kernel"
        owners = {name: [] for name in CONTRACT_NAMES}
        for path in kernel.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name in owners:
                        owners[node.name].append(path.name)
        self.assertEqual(
            owners,
            {
                "read_manifest_from_zip": ["zip_contract.py"],
                "validate_generated_zip_contract": ["zip_contract.py"],
            },
        )

    def test_consumers_import_contract_helpers_from_owner(self) -> None:
        paths = (
            PROMPT_TOOLS / "startup_kernel/cli_check.py",
            PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py",
        )
        for path in paths:
            self.assertEqual(
                _imported_names(path, CONTRACT_MODULE) & CONTRACT_NAMES,
                CONTRACT_NAMES,
            )
            self.assertFalse(
                _imported_names(path, DELIVERY_MODULE) & CONTRACT_NAMES,
            )

    def test_manifest_reader_is_importable_from_contract_owner(self) -> None:
        contract = importlib.import_module(CONTRACT_MODULE)
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "sample.zip"
            expected = {"schema_version": "1.0", "kind": "fixture"}
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(MANIFEST_FILENAME, json.dumps(expected))
            self.assertEqual(contract.read_manifest_from_zip(archive_path), expected)


if __name__ == "__main__":
    unittest.main()
