# project-path: tools/validate_engineering_diagnostics_wave2oa_v1.py
"""Live validator for Engineering Diagnostics backend foundation Wave 2O-A."""

from __future__ import annotations

import argparse
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import warnings
from contextlib import redirect_stdout

from tools.engineering_diagnostics_wave2oa_architecture_gate import (
    validate_engineering_diagnostics_wave2oa_architecture_non_regression,
)
from tools.engineering_diagnostics_wave2oa_public_boundary_gate import (
    validate_engineering_diagnostics_wave2oa_public_boundary,
)

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-backend-foundation-wave2oa-v1"
PACKAGE_REVISION = "v1r2"
VALIDATION_MARKER = "VALIDATION OK: " + FEATURE_ID

TARGET_HASHES = {
    "kanda_reasoner_app/engineering_diagnostics/__init__.py": "4a29f3ba39fff1e9357189f5185d27ff0efe071e7a7c48bf881d167de5a06b62",
    "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py": "18d038f8302906b291f70de3fa89c5a2148dd0b971271457776963e98012e1e1",
    "kanda_reasoner_app/engineering_diagnostics/_store_database.py": "bbf6a57ef1d65bf05f4cd173ab34a91fd6f5eb4ec33ea90c3df931f44cfb75b8",
    "kanda_reasoner_app/engineering_diagnostics/baseline.py": "5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e",
    "kanda_reasoner_app/engineering_diagnostics/bom_adapter.py": "ceeb930aa9713c63205d1d6c60aad286abc60dfa246e11492ce88846190fef25",
    "kanda_reasoner_app/engineering_diagnostics/fingerprinting.py": "7e262b06c167ea315fe8e26258428090a4271400a62c77cf7ec616bebcade69b",
    "kanda_reasoner_app/engineering_diagnostics/models.py": "2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184",
    "kanda_reasoner_app/engineering_diagnostics/paths.py": "95640db89ef725b160cbbe6784599f9ab9f5c1cf01814602b1121c924d48c48d",
    "kanda_reasoner_app/engineering_diagnostics/store.py": "b40d07897501051b4318ad50577769c1df86481a8cd88f08f8374cd3e766272e",
    "tests/test_engineering_diagnostics_wave2oa.py": "4cefd958d53df34acd8b53b4b9a3f8fdbb1e2afd806e01dc19806b551c26bbbd",
    "tools/engineering_diagnostics_wave2oa_architecture_gate.py": "35affe7f13821f9ba7d530ff1dd0b5f4fdcfa21141bbb878380621a0ca29c249",
    "tools/engineering_diagnostics_wave2oa_public_boundary_gate.py": "8eecb38a9630b84ce34089017cc8139600a869aaa9349ab76d3f778914fbdd15",
}

WAVE2N_ANCHOR_HASHES = {
    "kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py": "63eb29a659782ae56c57be513ea69987bbd2321fb0edc3c6b6bc1bf7ddfeb14c",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py": "77387d6c6b8d3fca0aa067fe6a456d3f567c32f07bf4b1d8cb71e8c05a22ed5a",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder_matching_private.py": "fb8d6d6c5f697ba87afd265be41d5330e0860f1a34ea653afe5ca62b58b47040",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py": "6212a2d1958a212f438e0f5f1b46510a9b7dd92606839605e304c8bc98863a48",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver_helpers_private.py": "5341abd47cb0afbf14f426f165cf62650194e7d57995c7de663caaf011753a70",
    "tools/reasoner_symbol_atlas_wave2n_architecture_gate.py": "bca752d82f087b3135261d143205edd5d0bf0674aaba62af48e9fe372901cddb",
    "tools/reasoner_symbol_atlas_wave2n_public_boundary_gate.py": "1c66d947763631614834a0f97b409c053b621926ee650c411c2d9b754f238dca",
    "tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py": "3636ab0616a5ac4112a137e6d7f167584859cb9f9ce1f8e5e7c6643fa6251e2a",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_hashes(root: Path, expected: dict[str, str], marker: str) -> None:
    for relative, digest in expected.items():
        path = root / relative
        _require(path.is_file(), "VALIDATION_TARGET_MISSING:" + relative)
        actual = _sha256(path)
        _require(actual == digest, "VALIDATION_TARGET_HASH_MISMATCH:" + relative)
    print(marker)


def _run(command: list[str], cwd: Path, markers: tuple[str, ...]) -> str:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(cwd)},
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0:
        raise RuntimeError("VALIDATION_COMMAND_FAILED:\n" + output)
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def _check_registry_unchanged(root: Path) -> tuple[str, str]:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    registry = ProjectSelectionRegistry(tool_source_root=root)
    path = registry.registry_path
    before = _sha256(path) if path.is_file() else "ABSENT"
    boundary = registry.resolve_boundary_for_root(root)
    after = _sha256(path) if path.is_file() else "ABSENT"
    _require(before == after, "PROJECT_SELECTION_REGISTRY_MUTATED")
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    return str(boundary.active_project_support_root), before



def _check_invalid_escape_warning_guard(root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="wave2oa_warning_guard_") as raw_temp:
        fixture_root = Path(raw_temp) / "fixture_project"
        package_source = root / "kanda_reasoner_app/engineering_diagnostics"
        package_target = fixture_root / "kanda_reasoner_app/engineering_diagnostics"
        package_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package_source, package_target)

        test_source = root / "tests/test_engineering_diagnostics_wave2oa.py"
        test_target = fixture_root / "tests/test_engineering_diagnostics_wave2oa.py"
        test_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(test_source, test_target)

        slash = chr(92)
        snippet = fixture_root / "snippets/reference_invalid_escape.py"
        snippet.parent.mkdir(parents=True, exist_ok=True)
        snippet.write_text(
            'VALUE = "' + slash + '_"\n',
            encoding="utf-8",
            newline="\n",
        )

        unrelated = fixture_root / "misc/reference_invalid_escape.py"
        unrelated.parent.mkdir(parents=True, exist_ok=True)
        unrelated.write_text(
            'VALUE = "' + slash + '["\n',
            encoding="utf-8",
            newline="\n",
        )

        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            with redirect_stdout(io.StringIO()):
                validate_engineering_diagnostics_wave2oa_public_boundary(
                    fixture_root
                )

        leaked = [item for item in captured if item.category is SyntaxWarning]
        _require(not leaked, "INVALID_ESCAPE_SYNTAXWARNING_LEAKED_TO_STDERR")

    print("BROAD STATIC SCAN SNIPPET EXCLUSION: PASS")
    print("INVALID ESCAPE SYNTAXWARNING STDERR LEAK: 0")
    print(
        "EXISTING ERROR MEMORY LESSON APPLIED: "
        "lesson-batch20-invalid-escape-sequence-warning-stderr-v1"
    )

def _run_tests(root: Path) -> None:
    _run(
        [sys.executable, "-m", "unittest", "-v", "tests.test_engineering_diagnostics_wave2oa"],
        root,
        ("Ran 13 tests", "OK"),
    )
    print("FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WINDOWS CANONICAL SUPPORT TEST ISOLATION: PASS")
    print("VALIDATION DOES NOT CREATE DRIVE ROOT SUPPORT FIXTURE: PASS")
    print("PORTABLE SMOKE ISOLATION PUBLIC CONTRACT REUSED: PASS")
    print("SQLITE DETERMINISTIC CONNECTION CLOSE: PASS")
    print("DIAGNOSTIC RUN ATOMICITY AND IDEMPOTENCY: PASS")
    print("BASELINE COMPARE-AND-SWAP LIFECYCLE: PASS")
    print("STALE RESULT REJECTION: PASS")
    print("BOM PUBLIC DATA ADAPTER: PASS")


def _run_previous_wave(root: Path) -> None:
    validator = root / "tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py"
    _run(
        [sys.executable, str(validator), "--root", str(root), "--skip-architecture"],
        root,
        (
            "WAVE2N EXTERNAL PRIVATE REACH-IN: 0",
            "WAVE2N SINGLE VALIDATOR STATE OWNER: PASS",
            "WAVE2N PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
            "PREVIOUS SYMBOL ATLAS CONTRACT PRESERVED: PASS",
        ),
    )
    print("WAVE2N FROZEN CONTRACT PRESERVED: PASS")


def _run_architecture(root: Path) -> None:
    command = [
        sys.executable,
        str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
        "--root",
        str(root),
        "--validate",
    ]
    output = _run(command, root, ("ARCHITECTURE VALIDATION SUMMARY",))
    validate_engineering_diagnostics_wave2oa_architecture_non_regression(output)


def _write_evidence(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-path", default="")
    parser.add_argument("--skip-live-boundary", action="store_true")
    parser.add_argument("--skip-previous-wave", action="store_true")
    parser.add_argument("--skip-architecture", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=False)
    _require(root.is_dir(), "PROJECT_ROOT_INVALID:" + str(root))
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")
    _check_hashes(root, TARGET_HASHES, "ENGINEERING DIAGNOSTICS INSTALLED HASHES: PASS")
    _check_hashes(root, WAVE2N_ANCHOR_HASHES, "WAVE2N PROTECTED ANCHOR HASHES: PASS")
    validate_engineering_diagnostics_wave2oa_public_boundary(root)
    _check_invalid_escape_warning_guard(root)
    _run_tests(root)

    support_root = "LOCAL_PREFLIGHT"
    if not args.skip_live_boundary:
        support_root, _ = _check_registry_unchanged(root)
    else:
        print("PROJECT SELECTION REGISTRY VALIDATION: DEFERRED TO LIVE PROJECT")

    if not args.skip_previous_wave:
        _run_previous_wave(root)
    else:
        print("WAVE2N LIVE REGRESSION: DEFERRED TO LIVE PROJECT")

    architecture_status = "DEFERRED_TO_LIVE_PROJECT"
    if not args.skip_architecture:
        _run_architecture(root)
        architecture_status = "PASS"
    else:
        print("WAVE2OA ARCHITECTURE VALIDATION: DEFERRED TO LIVE PROJECT")

    evidence_lines = [
        "KANDA Reasoner Engineering Diagnostics Wave 2O-A validation evidence",
        "Feature ID: " + FEATURE_ID,
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "ENGINEERING DIAGNOSTICS INSTALLED HASHES: PASS",
        "WAVE2N PROTECTED ANCHOR HASHES: PASS",
        "ENGINEERING DIAGNOSTICS PUBLIC FACADE: PASS",
        "ENGINEERING DIAGNOSTICS EXTERNAL PRIVATE REACH-IN: 0",
        "ENGINEERING DIAGNOSTICS PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "BROAD STATIC SCAN SNIPPET EXCLUSION: PASS",
        "INVALID ESCAPE SYNTAXWARNING STDERR LEAK: 0",
        "EXISTING ERROR MEMORY LESSON APPLIED: lesson-batch20-invalid-escape-sequence-warning-stderr-v1",
        "FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS",
        "WINDOWS CANONICAL SUPPORT TEST ISOLATION: PASS",
        "VALIDATION DOES NOT CREATE DRIVE ROOT SUPPORT FIXTURE: PASS",
        "PORTABLE SMOKE ISOLATION PUBLIC CONTRACT REUSED: PASS",
        "SQLITE DETERMINISTIC CONNECTION CLOSE: PASS",
        "DIAGNOSTIC RUN ATOMICITY AND IDEMPOTENCY: PASS",
        "BASELINE COMPARE-AND-SWAP LIFECYCLE: PASS",
        "STALE RESULT REJECTION: PASS",
        "BOM PUBLIC DATA ADAPTER: PASS",
        "ARCHITECTURE VALIDATION: " + architecture_status,
        "PROJECT SUPPORT ROOT: " + support_root,
    ]
    if architecture_status == "PASS" and not args.skip_previous_wave and not args.skip_live_boundary:
        evidence_lines.extend(
            [
                "WAVE2N FROZEN CONTRACT PRESERVED: PASS",
                "PROJECT SELECTION REGISTRY MUTATED: NO",
                "WAVE2OA NEW ARCHITECTURE ISSUES: 0",
                "WAVE2OA TOUCHED PATH ARCHITECTURE ISSUES: 0",
                VALIDATION_MARKER,
                "STATUS: IN_SYNC",
            ]
        )
    if args.evidence_path:
        _write_evidence(Path(args.evidence_path), evidence_lines)
        print("VALIDATION EVIDENCE WRITTEN: " + str(Path(args.evidence_path)))

    if architecture_status == "PASS" and not args.skip_previous_wave and not args.skip_live_boundary:
        print(VALIDATION_MARKER)
        print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
