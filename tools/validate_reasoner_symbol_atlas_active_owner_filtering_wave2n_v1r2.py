"""Validate Symbol Atlas active-owner filtering wave 2N corrective revision v1r5."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

from reasoner_symbol_atlas_wave2n_architecture_gate import (
    validate_architecture_non_regression,
)
from reasoner_symbol_atlas_wave2n_public_boundary_gate import (
    validate_wave2n_public_boundary,
)

FEATURE_ID = "reasoner-symbol-atlas-active-owner-filtering-wave2n-v1"
VALIDATION_MARKER = "VALIDATION OK: " + FEATURE_ID

TARGET_HASHES = {
    "tests/test_reasoner_symbol_atlas_active_owner_filtering_wave2n.py": (
        "7800212649d556fb3906847193282ec92c85201c9e42bd7ae420a74d86e97727"
    ),
    "tools/reasoner_symbol_atlas_wave2n_architecture_gate.py": (
        "bca752d82f087b3135261d143205edd5d0bf0674aaba62af48e9fe372901cddb"
    ),
    "tools/reasoner_symbol_atlas_wave2n_public_boundary_gate.py": (
        "1c66d947763631614834a0f97b409c053b621926ee650c411c2d9b754f238dca"
    ),
}

PACKAGE_REVISION = "v1r5"


WAVE2M_PROTECTED_HASHES = {
    "_reasoner_tools_gui_engineering_safety_full_audit.py": (
        "3406df90ce51fa0df349ded3a19ce864c5407c950b71b9e935a48bfeaf18b44f"
    ),
    "_reasoner_tools_gui_engineering_safety_review_signals.py": (
        "6d2ae82b16d38aaab6a57b0d7ece8cd25bea9111dcef390b1f4e791a42dec8f1"
    ),
    "kanda_reasoner_app/source_hygiene/_active_scope.py": (
        "ecc7017f6f7607f34fb5bb7e513d1fe2a59fea50878c5bc1ac1efa5a92087c44"
    ),
    "kanda_reasoner_app/source_hygiene/bom_scanner.py": (
        "80b8d544690fedfc75fd0558b29537ddd02a3c57dbb1141d8e90c07fbc1e5c60"
    ),
    "kanda_reasoner_app/source_hygiene/shadow_audit.py": (
        "cdf5efc3717c0a29365467f65eda914ad86df93d7c9feb6f25f3a251835fa91f"
    ),
    "kanda_reasoner_app/source_hygiene/shadow_fixer.py": (
        "7dc5ec64b370648e2c39a4f787de0eca2839f9c0b9886255a548fd6927f9aead"
    ),
    "tests/test_engineering_review_signal_semantics.py": (
        "88da301be4b10507742b29514cc88b759b80c349eb6ad8fe3c5aa59951152fc8"
    ),
    "tools/validate_engineering_review_signal_semantics_wave2m_v1.py": (
        "d31f850425d99b18a9e774f2637d49dba59b9d1349974e86a22f5fa7e08f9916"
    ),
}

TARGET_MODULES = (
    "kanda_reasoner_app.reasoner_symbol_atlas.output_policy",
    "kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder",
    "kanda_reasoner_app.reasoner_symbol_atlas.facade_owner_resolver",
)

TARGET_SOURCE_PATHS = (
    "kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder_matching_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver_helpers_private.py",
    "tests/test_reasoner_symbol_atlas_active_owner_filtering_wave2n.py",
    "tools/reasoner_symbol_atlas_wave2n_architecture_gate.py",
    "tools/reasoner_symbol_atlas_wave2n_public_boundary_gate.py",
    "tools/validate_reasoner_symbol_atlas_active_owner_filtering_wave2n_v1r2.py",
)

ARCHITECTURE_TOUCHED_PATHS = frozenset(TARGET_SOURCE_PATHS)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _run(
    command: list[str],
    root: Path,
    expected_markers: tuple[str, ...],
) -> str:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = completed.stdout
    if completed.stderr:
        output = output + ("\n" if output else "") + completed.stderr
    print(output.rstrip())
    _require(
        completed.returncode == 0,
        "VALIDATION_COMMAND_FAILED: " + " ".join(command),
    )
    for marker in expected_markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING: " + marker)
    return output


def _check_target_hashes(root: Path) -> None:
    _require(bool(TARGET_HASHES), "TARGET_HASH_CONTRACT_EMPTY")
    for relative_path, expected_hash in TARGET_HASHES.items():
        path = root / relative_path
        _require(path.is_file(), "TARGET_FILE_MISSING: " + relative_path)
        _require(
            _sha256(path) == expected_hash,
            "TARGET_HASH_MISMATCH: " + relative_path,
        )
    print("WAVE2N CORRECTIVE TEST HASH: PASS")



def _check_adaptive_source_contract(root: Path) -> None:
    contracts = {
        "kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py": (
            "def is_active_owner_candidate(",
            "not is_active_project_source_path(normalized)",
        ),
        "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py": (
            "inactive_symbol_matches",
            "inactive_owner_paths",
            "inactive_matches = _matching_inactive_symbols(",
        ),
        "kanda_reasoner_app/reasoner_symbol_atlas/"
        "existing_code_finder_matching_private.py": (
            "def _matching_symbol_candidates(",
            "def _matching_inactive_symbols(",
            "def _inactive_owner_paths(",
        ),
        "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py": (
            "inactive_owner_candidates: tuple[str, ...]",
            "inactive_owner_candidates = _inactive_candidate_owner_paths(",
        ),
        "kanda_reasoner_app/reasoner_symbol_atlas/"
        "facade_owner_resolver_helpers_private.py": (
            "def _all_candidate_owner_paths(",
            "def _inactive_candidate_owner_paths(",
            "def _record_is_active_owner_candidate(",
        ),
    }
    for relative_path, required_markers in contracts.items():
        path = root / relative_path
        _require(path.is_file(), "ADAPTIVE_SOURCE_MISSING: " + relative_path)
        source = path.read_text(encoding="utf-8")
        for marker in required_markers:
            _require(
                marker in source,
                "ADAPTIVE_SOURCE_CONTRACT_MISSING: "
                + relative_path
                + ":"
                + marker,
            )
        compile(source, str(path), "exec")
        _require(source.isascii(), "ADAPTIVE_SOURCE_NON_ASCII: " + relative_path)
        _require(
            len(source.splitlines()) <= 500,
            "ADAPTIVE_SOURCE_MODULE_SIZE_LIMIT_EXCEEDED: " + relative_path,
        )
    print("WAVE2N ADAPTIVE SOURCE CONTRACTS: 5/5 PASS")

def _check_protected_hashes(root: Path, allow_handoff_omissions: bool) -> None:
    omitted: list[str] = []
    for relative_path, expected_hash in WAVE2M_PROTECTED_HASHES.items():
        path = root / relative_path
        if not path.is_file() and allow_handoff_omissions:
            omitted.append(relative_path)
            continue
        _require(path.is_file(), "WAVE2M_PROTECTED_FILE_MISSING: " + relative_path)
        _require(
            _sha256(path) == expected_hash,
            "WAVE2M_PROTECTED_HASH_MISMATCH: " + relative_path,
        )
    if omitted:
        print("WAVE2M HANDOFF-OMITTED PROTECTED PATHS: " + str(len(omitted)))
    print("WAVE2M FROZEN PROTECTED PATHS UNCHANGED: PASS")


def _check_source_contract(root: Path) -> None:
    for relative_path in TARGET_SOURCE_PATHS:
        path = root / relative_path
        _require(path.is_file(), "SOURCE_PATH_MISSING: " + relative_path)
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        line_count = len(source.splitlines())
        _require(line_count <= 500, "MODULE_SIZE_LIMIT_EXCEEDED: " + relative_path)
        _require(source.isascii(), "NON_ASCII_SOURCE_DETECTED: " + relative_path)
    print("WAVE2N PYTHON SOURCE CONTRACT: PASS")
    print("WAVE2N MODULE SIZE MAXIMUM 500: PASS")


def _check_import_contract(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    for module_name in TARGET_MODULES:
        __import__(module_name)
    from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
        is_active_owner_candidate,
    )

    _require(
        is_active_owner_candidate(
            "kanda_reasoner_app/domain/service.py",
            "canonical_owner",
        ),
        "ACTIVE_OWNER_POLICY_REJECTED_ACTIVE_SOURCE",
    )
    _require(
        not is_active_owner_candidate(
            ".project_reference/domain/service.py",
            "canonical_owner",
        ),
        "ACTIVE_OWNER_POLICY_ACCEPTED_REFERENCE_SOURCE",
    )
    _require(
        not is_active_owner_candidate(
            "tests/test_service.py",
            "test_only",
            True,
        ),
        "ACTIVE_OWNER_POLICY_ACCEPTED_TEST_SOURCE",
    )
    _require(
        not is_active_owner_candidate(
            "generated/service.py",
            "generated_or_stale",
        ),
        "ACTIVE_OWNER_POLICY_ACCEPTED_GENERATED_SOURCE",
    )
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")
    print("ACTIVE OWNER POLICY CONTRACT: PASS")


def _run_focused_tests(root: Path) -> None:
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_reasoner_symbol_atlas_active_owner_filtering_wave2n",
        ],
        root,
        ("Ran 7 tests", "OK"),
    )
    print("WAVE2N ACTIVE OWNER REGRESSION FIXTURES: PASS")
    print("EXISTING CODE FINDER PRE-RANK FILTER: PASS")
    print("FACADE OWNER PRE-RANK FILTER: PASS")
    print("INACTIVE OWNER EVIDENCE PRESERVED SEPARATELY: PASS")


def _run_previous_symbol_atlas_regression(root: Path) -> None:
    validator = (
        root
        / "tools"
        / "validate_reasoner_symbol_atlas_main_helper_mapper_source_ready_refactor_v1.py"
    )
    _require(validator.is_file(), "PREVIOUS_SYMBOL_ATLAS_VALIDATOR_MISSING")
    _run(
        [sys.executable, str(validator), "--root", str(root)],
        root,
        (
            "VALIDATION OK: reasoner-symbol-atlas-main-helper-mapper-source-ready-refactor-v1",
            "STATUS: IN_SYNC",
        ),
    )
    print("PREVIOUS SYMBOL ATLAS CONTRACT PRESERVED: PASS")


def _run_architecture_validation(root: Path) -> None:
    validator = root / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
    _require(validator.is_file(), "ARCHITECTURE_VALIDATOR_MISSING")
    output = _run(
        [
            sys.executable,
            str(validator),
            "--root",
            str(root),
            "--validate",
        ],
        root,
        ("ARCHITECTURE VALIDATION SUMMARY",),
    )
    validate_architecture_non_regression(output)


def _write_evidence(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--evidence-path", default="")
    parser.add_argument("--skip-architecture", action="store_true")
    parser.add_argument("--allow-handoff-omissions", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = Path(args.root).expanduser().resolve(strict=False)
    _require(root.is_dir(), "PROJECT_ROOT_INVALID: " + str(root))
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    _check_target_hashes(root)
    _check_adaptive_source_contract(root)
    _check_protected_hashes(root, args.allow_handoff_omissions)
    _check_source_contract(root)
    _check_import_contract(root)
    validate_wave2n_public_boundary(root)
    _run_focused_tests(root)
    _run_previous_symbol_atlas_regression(root)

    architecture_status = "LIVE_PROJECT_REQUIRED"
    if not args.skip_architecture:
        _run_architecture_validation(root)
        architecture_status = "PASS"
    if args.skip_architecture:
        print("WAVE2N ARCHITECTURE VALIDATION: DEFERRED TO LIVE PROJECT")

    evidence_lines = [
        "KANDA Reasoner Wave 2N validation evidence",
        "Feature ID: " + FEATURE_ID,
        "WAVE2N CORRECTIVE TEST HASH: PASS",
        "WAVE2N ADAPTIVE SOURCE CONTRACTS: 5/5 PASS",
        "WAVE2M FROZEN PROTECTED PATHS UNCHANGED: PASS",
        "WAVE2N PYTHON SOURCE CONTRACT: PASS",
        "VALIDATOR PROJECT ROOT IMPORT PATH: PASS",
        "ACTIVE OWNER POLICY CONTRACT: PASS",
        "WAVE2N PRIVATE MODULE STRUCTURAL CONTRACT: PASS",
        "WAVE2N EXTERNAL PRIVATE REACH-IN: 0",
        "WAVE2N SINGLE VALIDATOR STATE OWNER: PASS",
        "WAVE2N PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "WAVE2N ACTIVE OWNER REGRESSION FIXTURES: PASS",
        "EXISTING CODE FINDER PRE-RANK FILTER: PASS",
        "FACADE OWNER PRE-RANK FILTER: PASS",
        "INACTIVE OWNER EVIDENCE PRESERVED SEPARATELY: PASS",
        "PREVIOUS SYMBOL ATLAS CONTRACT PRESERVED: PASS",
        "ARCHITECTURE VALIDATION: " + architecture_status,
    ]
    if architecture_status == "PASS":
        evidence_lines.extend(
            (
                "WAVE2N ARCHITECTURE PREEXISTING BASELINE: 20",
                "WAVE2N NEW ARCHITECTURE ISSUES: 0",
                "WAVE2N TOUCHED PATH ARCHITECTURE ISSUES: 0",
                "WAVE2N ARCHITECTURE NON-REGRESSION: PASS",
                VALIDATION_MARKER,
                "STATUS: IN_SYNC",
            )
        )
    if args.evidence_path:
        _write_evidence(Path(args.evidence_path), evidence_lines)
        print("VALIDATION EVIDENCE WRITTEN: " + str(Path(args.evidence_path)))

    if architecture_status == "PASS":
        print(VALIDATION_MARKER)
        print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
