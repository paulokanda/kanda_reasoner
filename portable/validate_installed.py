"""Static and focused functional validator for Portable builder v1r12."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
__all__ = [
    "main",
]

EXPECTED_FEATURE_ID = 'kanda-reasoner-portable-builder-install-v1r12'
EXPECTED_VERSION = 'v1r12'
EXPECTED_HARDENING_FEATURES = ('registry-boundary-gate', 'packaged-gui-smoke-isolation', 'governed-root-exact-rollback', 'runtime-path-hash-allowlist', 'exact-builder-member-governance', 'external-build-control-hash-binding')
EXPECTED_HARDENING_STAGE = 'registry-boundary-plus-smoke-isolation-plus-governed-root-rollback-plus-runtime-path-hash-allowlist-plus-exact-builder-member-governance-plus-external-build-control-hash-binding'
FORBIDDEN_IMPORT_PREFIXES = ('kanda_reasoner_app.reasoner_context_bundle', 'reasoner_context_bundle', 'handoff_zip_exporter', 'collector_main')

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

def _imported_modules(tree: ast.AST) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update((alias.name for alias in node.names))
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules

def _is_forbidden_import(module: str) -> bool:
    normalized = module.casefold()
    return any((normalized == prefix or normalized.startswith(prefix + '.') for prefix in FORBIDDEN_IMPORT_PREFIXES))

def _validate_python(path: Path) -> None:
    source = path.read_text(encoding='utf-8')
    source.encode('ascii')
    tree = ast.parse(source, filename=str(path))
    if len(source.splitlines()) > 500:
        raise RuntimeError(f'Python module exceeds 500 lines: {path.name}')
    forbidden = sorted((module for module in _imported_modules(tree) if _is_forbidden_import(module)))
    if forbidden:
        raise RuntimeError(f"Show Project implementation import in {path.name}: {', '.join(forbidden)}")

def _validate_policy_and_cleanup(root: Path) -> None:
    sys.path.insert(0, str(root.parent))
    from portable.build import stage_application
    from portable.errors import PortableBuildError
    from portable.models import BuildPaths, BuiltApplication
    from portable.physical_runtime_validation import assert_fixture_stage, populate_fixture_project
    from portable.policy import is_generated_handoff_or_release_path, is_non_runtime_debris_path, is_runtime_package_path
    runtime_relative = 'kanda_reasoner_app/reasoner_tools_shell/runner_help/first_prompt_files_private_impl.py'
    backup_relative = runtime_relative + '.bak_startup_creator_canonical_zz_v11'
    runtime_freeze_package = 'kanda_reasoner/_internal/kanda_reasoner_app/freeze_hint_intake/runtime_contract.json'
    external_freeze_intake = 'kanda_reasoner_show_project_to_AI/project_freeze_after_update/freeze_hint_intake/generated_hint.json'
    if is_generated_handoff_or_release_path(runtime_relative):
        raise RuntimeError('Runtime module name triggered generated policy.')
    if is_generated_handoff_or_release_path(backup_relative):
        raise RuntimeError('Backup filename triggered generated policy.')
    if not is_non_runtime_debris_path(backup_relative):
        raise RuntimeError('Known backup is not classified as debris.')
    if not is_runtime_package_path(runtime_freeze_package):
        raise RuntimeError('Runtime freeze_hint_intake package was not recognized.')
    if is_generated_handoff_or_release_path(runtime_freeze_package):
        raise RuntimeError('Runtime freeze_hint_intake package triggered generated policy.')
    if not is_generated_handoff_or_release_path(external_freeze_intake):
        raise RuntimeError('External generated freeze-intake path was not rejected.')
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        app_root = temp_root / 'source_app'
        runtime = app_root / runtime_relative
        backup = app_root / backup_relative
        runtime_freeze = app_root / '_internal' / 'kanda_reasoner_app' / 'freeze_hint_intake' / 'runtime_contract.json'
        runtime.parent.mkdir(parents=True)
        runtime.write_text('RUNTIME = True\n', encoding='ascii')
        backup.write_text('BACKUP = True\n', encoding='ascii')
        runtime_freeze.parent.mkdir(parents=True)
        runtime_freeze.write_text('{"runtime":true}\n', encoding='ascii')
        executable = app_root / 'kanda_reasoner.exe'
        executable.write_bytes(b'MZ')
        (app_root / '_internal').mkdir(exist_ok=True)
        stage_parent = temp_root / 'release_stage'
        dummy = temp_root / 'dummy'
        populate_fixture_project(dummy, reference_project_root=root.parent)
        paths = BuildPaths(project_root=dummy, drive_root=dummy, project_support_root=dummy, transient_root=dummy, run_root=dummy, pyinstaller_work=dummy, pyinstaller_dist=dummy, pyinstaller_config=dummy, temporary_root=dummy, stage_parent=stage_parent, candidate_zip=dummy, clean_extract_root=dummy, final_zip=dummy, spec_path=dummy, governed_python=dummy, zip_helper=dummy)
        staged = stage_application(paths, BuiltApplication(app_root=app_root, executable=executable))
        if not (staged / runtime_relative).is_file():
            raise RuntimeError('Runtime module was removed by staging cleanup.')
        if (staged / backup_relative).exists():
            raise RuntimeError('Backup debris survived staging cleanup.')
        staged_runtime_freeze = staged / '_internal' / 'kanda_reasoner_app' / 'freeze_hint_intake' / 'runtime_contract.json'
        if not staged_runtime_freeze.is_file():
            raise RuntimeError('Runtime freeze_hint_intake package was removed.')
        assert_fixture_stage(staged)
        invalid_app = temp_root / 'invalid_app'
        invalid_executable = invalid_app / 'kanda_reasoner.exe'
        invalid_generated = invalid_app / 'project_freeze_after_update' / 'freeze_hint_intake' / 'generated_hint.json'
        invalid_generated.parent.mkdir(parents=True)
        invalid_generated.write_text('{"generated":true}\n', encoding='ascii')
        invalid_executable.write_bytes(b'MZ')
        (invalid_app / '_internal').mkdir()
        invalid_paths = BuildPaths(project_root=dummy, drive_root=dummy, project_support_root=dummy, transient_root=dummy, run_root=dummy, pyinstaller_work=dummy, pyinstaller_dist=dummy, pyinstaller_config=dummy, temporary_root=dummy, stage_parent=temp_root / 'invalid_stage', candidate_zip=dummy, clean_extract_root=dummy, final_zip=dummy, spec_path=dummy, governed_python=dummy, zip_helper=dummy)
        try:
            stage_application(invalid_paths, BuiltApplication(app_root=invalid_app, executable=invalid_executable))
        except PortableBuildError as exc:
            if 'freeze_hint_intake' not in str(exc):
                raise RuntimeError('Generated intake rejection reported the wrong path.') from exc
        else:
            raise RuntimeError('Generated external freeze-intake fixture was accepted.')

def _validate_identity_json(root: Path) -> None:
    facade = root / 'create_kanda_reasoner_portable.py'
    environment = os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, str(facade), '--identity-json'], cwd=str(root.parent), env=environment, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f'Identity JSON command failed with exit code {result.returncode}.')
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f'Identity JSON must be one line; found {len(lines)}.')
    identity = json.loads(lines[0])
    if identity != {'schema_version': '1.0', 'builder_member_feature_id': 'kanda-reasoner-portable-exact-builder-member-governance-v1', 'builder_version': EXPECTED_VERSION, 'external_control_feature_id': 'kanda-reasoner-portable-external-build-control-hash-binding-v1r1', 'feature_id': EXPECTED_FEATURE_ID, 'hardening_features': list(EXPECTED_HARDENING_FEATURES), 'hardening_stage': EXPECTED_HARDENING_STAGE, 'production_portable_enabled': False}:
        raise RuntimeError(f'Identity JSON mismatch: {identity}')

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--portable-root', required=True)
    args = parser.parse_args()
    root = Path(args.portable_root).resolve()
    if root.name.casefold() != 'portable':
        raise RuntimeError(f'Portable validator requires a package root named portable: {root}')
    manifest_path = root / 'PORTABLE_BUILDER_MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('feature_id') != EXPECTED_FEATURE_ID or manifest.get('builder_version') != EXPECTED_VERSION or manifest.get('hardening_features') != list(EXPECTED_HARDENING_FEATURES) or (manifest.get('hardening_stage') != EXPECTED_HARDENING_STAGE):
        raise RuntimeError('Portable builder identity contract mismatch.')
    if manifest.get('exact_physical_runtime_allowlist_pending') is not False:
        raise RuntimeError('Exact physical runtime allowlist is still pending.')
    if manifest.get('exact_physical_runtime_path_hash_allowlist') is not True:
        raise RuntimeError('Exact physical runtime allowlist contract is missing.')
    if manifest.get('exact_builder_member_contract_pending') is not False:
        raise RuntimeError('Exact builder member contract is still pending.')
    if manifest.get('exact_builder_member_governance') is not True:
        raise RuntimeError('Exact builder member governance is missing.')
    if manifest.get('external_control_hash_binding_pending') is not False:
        raise RuntimeError('External build-control binding is still pending.')
    if manifest.get('external_control_hash_binding') is not True:
        raise RuntimeError('External build-control hash binding is missing.')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root.parent))
    from portable.builder_members import validate_exact_builder_members
    member_inventory = validate_exact_builder_members(root, manifest)
    from portable.external_controls import validate_external_build_controls
    external_controls = validate_external_build_controls(root.parent, root)
    for path in sorted(root.glob('*.py')):
        _validate_python(path)
    _validate_policy_and_cleanup(root)
    _validate_identity_json(root)
    from portable.constants import BUILDER_MEMBER_FEATURE_ID, BUILDER_VERSION, EXTERNAL_CONTROL_FEATURE_ID, FEATURE_ID, FIRST_SMOKE_CONFIRMATION, PORTABLE_HARDENING_FEATURES, PORTABLE_HARDENING_STAGE, PRODUCTION_PORTABLE_ENABLED, SMOKE_CONFIRMATION
    if BUILDER_MEMBER_FEATURE_ID != 'kanda-reasoner-portable-exact-builder-member-governance-v1' or EXTERNAL_CONTROL_FEATURE_ID != 'kanda-reasoner-portable-external-build-control-hash-binding-v1r1' or BUILDER_VERSION != EXPECTED_VERSION or (FEATURE_ID != EXPECTED_FEATURE_ID) or (tuple(PORTABLE_HARDENING_FEATURES) != EXPECTED_HARDENING_FEATURES) or (PORTABLE_HARDENING_STAGE != EXPECTED_HARDENING_STAGE):
        raise RuntimeError('Runtime builder identity contract mismatch.')
    if PRODUCTION_PORTABLE_ENABLED is not False:
        raise RuntimeError('Production Portable gate must remain closed.')
    if FIRST_SMOKE_CONFIRMATION != 'FIRST PASS CLOSED':
        raise RuntimeError('First natural-close confirmation mismatch.')
    if SMOKE_CONFIRMATION != 'PORTABLE TESTS PASS CLOSED':
        raise RuntimeError('Final natural-close confirmation mismatch.')
    required_text = {'cli.py': ('"--identity-json"', '"--result-json"', 'json.dumps'), 'workflow.py': ('_write_result', '"status": "portable_ready"', 'project_snapshot_after_publication', 'support_snapshot_after_publication', 'PRODUCTION_PORTABLE_ENABLED', 'load_registry_boundary', 'prepare_governed_root_rollback', 'PORTABLE FAILURE GOVERNED ROOT EXACT ROLLBACK'), 'environment.py': ('PORTABLE CANONICAL SPECIFICATION: PASS', 'PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT', 'validate_external_build_controls', 'PORTABLE EXTERNAL BUILD CONTROL PREFLIGHT: PASS'), 'build.py': ('validate_external_build_controls', 'PORTABLE EXTERNAL CONTROLS UNCHANGED THROUGH PYINSTALLER: PASS', '_remove_non_runtime_debris', 'hydrate_physical_runtime', 'validate_physical_runtime', 'PORTABLE QT WEBENGINE PROCESS: PASS', 'PORTABLE QT WINDOWS PLATFORM PLUGIN: PASS'), 'physical_runtime.py': ('PORTABLE_RUNTIME_ALLOWLIST.json', 'load_runtime_allowlist', 'validate_runtime_allowlist_sources', 'committed_exact_source_archive_path_sha256_allowlist', 'Runtime allowlist source SHA-256 mismatch', 'physical_runtime_manifest.json'), 'archive.py': ('_launch_and_require_natural_close', 'PORTABLE CLEAN SHUTDOWN: PASS'), 'destination.py': ('askdirectory', 'mustexist=True', 'validate_publication_directory', 'assert_registry_unchanged'), 'publish.py': ('shutil.copyfile', 'os.replace'), 'paths.py': ('%Y%m%d_%H%M%S_%f', 'uuid4().hex[:8]', 'registry_boundary'), 'registry_boundary.py': ('EXPLICIT_SELF_HOSTING', 'protected_roots', 'assert_registry_unchanged', 'validate_result_path'), 'snapshots.py': ('_update_file_content', 'content_snapshot'), 'governed_root_rollback.py': ('prepare_governed_root_rollback', 'registered_projects_snapshot', 'restore_if_changed', 'PORTABLE GOVERNED ROOT EXACT ROLLBACK: PASS', 'PORTABLE FAILURE-PATH GOVERNED ROOT ROLLBACK: PASS'), 'external_controls.py': ('validate_external_build_controls', 'EXTERNAL_CONTROL_ORDER_OR_PATH_MISMATCH', 'EXTERNAL_CONTROL_SHA256_MISMATCH'), 'builder_members.py': ('validate_exact_builder_members', 'BUILDER_FILE_SET_MISMATCH', 'BUILDER_DIRECTORY_SET_MISMATCH', 'BUILDER_LINK_OR_REPARSE_MEMBER')}
    for name, tokens in required_text.items():
        source = (root / name).read_text(encoding='utf-8')
        missing = [token for token in tokens if token not in source]
        if missing:
            raise RuntimeError(f'{name} is missing contracts: {missing}')
    print('PORTABLE BUILDER PAYLOAD HASHES: PASS')
    print('PORTABLE BUILDER MANIFESTED SOURCE SET: PASS')
    print('PORTABLE BUILDER EXACT MEMBER CONTRACT: PASS')
    print(f"PORTABLE BUILDER EXACT MEMBER FILE COUNT: {len(member_inventory['files'])}")
    print(f"PORTABLE BUILDER EXACT MEMBER DIRECTORY COUNT: {len(member_inventory['directories'])}")
    print('PORTABLE BUILDER MANIFEST SELF MEMBER: PASS')
    print('PORTABLE BUILDER PYTHON AST: PASS')
    print('PORTABLE BUILDER ASCII SOURCE: PASS')
    print('PORTABLE SHOW PROJECT IMPLEMENTATION IMPORTS: ABSENT')
    print('PORTABLE IDENTITY JSON RUNTIME: PASS')
    print('PORTABLE RESULT JSON CONTRACT: PASS')
    print('PORTABLE STAGING CLEANUP FUNCTIONAL FIXTURE: PASS')
    print('PORTABLE RUNTIME MODULE PRESERVATION: PASS')
    print('PORTABLE BACKUP DEBRIS REMOVAL: PASS')
    print('PORTABLE RUNTIME FREEZE HINT PACKAGE CLASSIFIER: PASS')
    print('PORTABLE RUNTIME FREEZE HINT PACKAGE PRESERVATION: PASS')
    print('PORTABLE EXTERNAL FREEZE HINT INTAKE EXCLUSION: PASS')
    print('PORTABLE LOOSE PYTHON RUNTIME DEPENDENCY FIXTURE: PASS')
    print('PORTABLE PHYSICAL WORKER AND HELPER MANIFEST FIXTURE: PASS')
    print('PORTABLE RUNTIME EXACT PATH-HASH ALLOWLIST: PASS')
    print('PORTABLE RUNTIME RECURSIVE DISCOVERY: ABSENT')
    print('PORTABLE NATURAL CLOSE CONTRACT: PASS')
    print('PORTABLE CONTENT HASH IMMUTABILITY CONTRACT: PASS')
    print('PORTABLE UNIQUE RUN ID CONTRACT: PASS')
    print('PORTABLE REGISTRY BOUNDARY MODULE: PASS')
    print('PORTABLE GOVERNED ROOT ROLLBACK MODULE: PASS')
    print('PORTABLE EXACT BUILDER MEMBER GOVERNANCE CAPABILITY: PASS')
    print('PORTABLE EXTERNAL BUILD CONTROL MANIFEST: PASS')
    print(f"PORTABLE EXTERNAL BUILD CONTROL ITEM COUNT: {external_controls['item_count']}")
    print('PORTABLE EXTERNAL BUILD CONTROL EXACT SHA-256: PASS')
    print('PORTABLE EXTERNAL BUILD CONTROL HASH BINDING CAPABILITY: PASS')
    print('PORTABLE PRODUCTION BUILD GATE CLOSED: PASS')
    print(f'VALIDATION OK: {EXPECTED_FEATURE_ID}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
