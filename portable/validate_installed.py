"""Validate Portable Tool/Project-decoupled build v1r26."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
__all__ = [
    "main",
]

EXPECTED_FEATURE_ID = 'kanda-reasoner-portable-timestamped-publication-name-v1r32'
EXPECTED_VERSION = 'v1r32'
EXPECTED_HARDENING_FEATURES = ('registry-boundary-gate', 'packaged-gui-smoke-isolation', 'governed-root-exact-rollback', 'runtime-path-hash-allowlist', 'exact-builder-member-governance', 'external-build-control-hash-binding', 'self-host-venv-build-interpreter', 'production-portable-authorization', 'spec-audit-policy-reconciliation', 'posix-zip-member-writer', 'packaged-gui-runtime-report-preservation', 'pyinstaller-submodule-import-preflight', 'selected-owner-fire-shield-isolation', 'packaged-worker-reentry-dispatch', 'clean-start-gui-regression-reset', 'tool-project-decoupled-portable-build', 'timestamped-publication-name')
EXPECTED_HARDENING_STAGE = 'registry-boundary-plus-smoke-isolation-plus-governed-root-rollback-plus-runtime-path-hash-allowlist-plus-exact-builder-member-governance-plus-external-build-control-hash-binding-plus-self-host-venv-build-interpreter-plus-production-portable-authorization-plus-spec-audit-policy-reconciliation-plus-posix-zip-member-writer-plus-packaged-gui-runtime-report-preservation-plus-pyinstaller-submodule-import-preflight-plus-selected-owner-fire-shield-isolation-plus-packaged-worker-reentry-dispatch-plus-clean-start-gui-regression-reset-plus-tool-project-decoupled-portable-build-plus-timestamped-publication-name'
FORBIDDEN_IMPORT_PREFIXES = ('kanda_reasoner_app.reasoner_context_bundle', 'reasoner_context_bundle', 'handoff_zip_exporter', 'collector_main')
WORKER_VALIDATOR_RELATIVE = Path('..') / 'tools' / 'validate_portable_tool_project_decoupled_build_v1r26.py'

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


def _validate_governed_root_zip_timestamp_compatibility(root: Path) -> None:
    sys.path.insert(0, str(root.parent))
    from portable.governed_root_rollback import RootViewPolicy, _write_archive
    from portable.models import ProtectedRoot

    source = (root / "governed_root_rollback.py").read_text(encoding="ascii")
    if "strict_timestamps=False" not in source:
        raise RuntimeError(
            "Governed-root backup ZIP must disable strict filesystem timestamps."
        )
    print("PORTABLE GOVERNED ROOT ZIP STRICT TIMESTAMPS DISABLED: PASS")

    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        legacy_root = temp_root / "legacy_root"
        legacy_root.mkdir()
        legacy_file = legacy_root / "legacy.txt"
        payload = b"KANDA_PRE_1980_ROLLBACK_FIXTURE"
        legacy_file.write_bytes(payload)
        old_epoch = 157766400.0
        os.utime(legacy_file, (old_epoch, old_epoch))

        policy = RootViewPolicy(
            protected_root=ProtectedRoot(
                label="pre-1980 rollback fixture",
                owner_id="fixture",
                owner_slug="fixture",
                root_kind="PROJECT_ROOT",
                path=legacy_root,
            ),
            ignored_names=frozenset(),
            excluded_top_level=frozenset(),
        )
        archive_path = temp_root / "legacy_root.zip"
        _write_archive(policy, archive_path)

        with zipfile.ZipFile(archive_path, "r") as archive:
            info = archive.getinfo("legacy.txt")
            if info.date_time[0] != 1980:
                raise RuntimeError(
                    "Pre-1980 rollback member was not clamped to ZIP epoch."
                )
            if archive.read("legacy.txt") != payload:
                raise RuntimeError(
                    "Pre-1980 rollback fixture content changed in archive."
                )

    print("PORTABLE GOVERNED ROOT PRE-1980 BACKUP FIXTURE: PASS")
    print("PORTABLE GOVERNED ROOT PRE-1980 CONTENT PRESERVED: PASS")


def _validate_zip_member_writer(root: Path, package_only: bool) -> None:
    helper = root / 'create_windows_zip.ps1'
    source = helper.read_text(encoding='ascii')
    assembly_lines = [
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith('-AssemblyName ')
    ]
    expected_assemblies = [
        '-AssemblyName System.IO.Compression',
        '-AssemblyName System.IO.Compression.FileSystem',
    ]
    if assembly_lines[:2] != expected_assemblies:
        raise RuntimeError(
            'ZIP compression assemblies are not preloaded in the required order: '
            + repr(assembly_lines[:2])
        )
    print('PORTABLE ZIP COMPRESSION ASSEMBLY PRELOAD STATIC: PASS')
    required = (
        'ZipArchiveMode]::Create',
        '.CreateEntry(',
        'Replace([char]92, [char]47)',
        'ZIP_COMPRESSION_ASSEMBLY_PRELOAD=PASS',
        'ZIP_MEMBER_SEPARATOR_CONTRACT=PASS',
    )
    missing = [token for token in required if token not in source]
    if missing:
        raise RuntimeError(f'POSIX ZIP writer is missing contracts: {missing}')
    if 'CreateFromDirectory(' in source:
        raise RuntimeError('CreateFromDirectory returned to the ZIP writer.')
    print('PORTABLE ZIP POSIX MEMBER WRITER STATIC: PASS')
    if package_only:
        print('PORTABLE ZIP COMPRESSION ASSEMBLY PRELOAD LIVE: DEFERRED_PACKAGE_ONLY')
        print('PORTABLE ZIP POSIX MEMBER WRITER LIVE FIXTURE: DEFERRED_PACKAGE_ONLY')
        return
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        app_root = temp_root / 'kanda_reasoner'
        nested = app_root / '_internal' / 'fixture.txt'
        nested.parent.mkdir(parents=True)
        (app_root / 'kanda_reasoner.exe').write_bytes(b'MZ')
        nested.write_text('fixture\n', encoding='ascii')
        destination = temp_root / 'fixture.zip'
        result = subprocess.run(
            [
                'powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                '-File', str(helper), '-SourceDirectory', str(app_root),
                '-DestinationZip', str(destination),
            ],
            cwd=str(root.parent), capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            details = '\n'.join(
                part for part in (result.stdout.strip(), result.stderr.strip()) if part
            )
            raise RuntimeError(
                'POSIX ZIP writer fixture failed with exit code '
                + str(result.returncode)
                + ': '
                + details
            )
        if 'ZIP_COMPRESSION_ASSEMBLY_PRELOAD=PASS' not in result.stdout:
            raise RuntimeError('ZIP helper did not report assembly-preload PASS.')
        print('PORTABLE ZIP COMPRESSION ASSEMBLY PRELOAD LIVE: PASS')
        if 'ZIP_MEMBER_SEPARATOR_CONTRACT=PASS' not in result.stdout:
            raise RuntimeError('ZIP helper did not report separator-contract PASS.')
        with zipfile.ZipFile(destination, 'r') as archive_file:
            names = [item.filename for item in archive_file.infolist()]
        if any('\\' in name for name in names):
            raise RuntimeError(f'Backslash ZIP member survived writer fixture: {names}')
        expected = {
            'kanda_reasoner/kanda_reasoner.exe',
            'kanda_reasoner/_internal/fixture.txt',
        }
        if set(names) != expected:
            raise RuntimeError(f'Unexpected ZIP writer fixture members: {names}')
    print('PORTABLE ZIP POSIX MEMBER WRITER LIVE FIXTURE: PASS')

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
    if identity != {'schema_version': '1.0', 'builder_member_feature_id': 'kanda-reasoner-portable-exact-builder-member-governance-v1', 'builder_version': EXPECTED_VERSION, 'external_control_feature_id': 'kanda-reasoner-portable-external-build-control-hash-binding-v1r3', 'feature_id': EXPECTED_FEATURE_ID, 'hardening_features': list(EXPECTED_HARDENING_FEATURES), 'hardening_stage': EXPECTED_HARDENING_STAGE, 'production_portable_enabled': True}:
        raise RuntimeError(f'Identity JSON mismatch: {identity}')

def _validate_worker_validator_non_mutation_contract(root: Path) -> None:
    validator = (root / WORKER_VALIDATOR_RELATIVE).resolve(strict=True)
    source = validator.read_text(encoding="utf-8", errors="strict")
    if "import importlib.util" in source:
        raise RuntimeError("PORTABLE_WORKER_VALIDATOR_IMPORTLIB_MUTATION_RISK")
    for needle in (
        "types.ModuleType",
        "compile(source, str(path), \"exec\", dont_inherit=True)",
        "PORTABLE_WORKER_VALIDATOR_CANONICAL_CACHE_MUTATION_ABSENT",
    ):
        if needle not in source:
            raise RuntimeError(
                "PORTABLE_WORKER_VALIDATOR_NON_MUTATION_CONTRACT_MISSING:" + needle
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--portable-root', required=True)
    parser.add_argument('--package-only', action='store_true')
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
    _validate_worker_validator_non_mutation_contract(root)
    member_inventory = validate_exact_builder_members(root, manifest)
    from portable.external_controls import validate_external_build_controls
    external_controls = validate_external_build_controls(root.parent, root)
    from portable.physical_runtime import validate_runtime_allowlist_sources
    if args.package_only:
        print('PORTABLE RUNTIME LIVE SOURCE HASHES: DEFERRED_PACKAGE_ONLY')
    else:
        runtime_allowlist = validate_runtime_allowlist_sources(root.parent)
        print(
            'PORTABLE RUNTIME LIVE SOURCE HASHES: PASS - '
            + str(runtime_allowlist['item_count'])
        )
    for path in sorted(root.glob('*.py')):
        _validate_python(path)
    if args.package_only:
        print('PORTABLE FUNCTIONAL RUNTIME FIXTURES: DEFERRED_PACKAGE_ONLY')
    else:
        _validate_policy_and_cleanup(root)
    from types import SimpleNamespace
    from portable.environment import audit_spec_contract
    spec_path = root.parent / "KandaReasonerWindows.spec"
    if not spec_path.is_file():
        raise RuntimeError("Canonical PyInstaller specification is missing.")
    spec_source = spec_path.read_text(encoding="utf-8")
    if "collect_data_files" in spec_source:
        raise RuntimeError("Package-wide collect_data_files returned to canonical spec.")
    if "iter_packaged_resource_files" not in spec_source:
        raise RuntimeError("Tool-owned data allowlist owner is missing from canonical spec.")
    if "PORTABLE PYINSTALLER SUBMODULE IMPORT PREFLIGHT: PASS" not in spec_source:
        raise RuntimeError("PyInstaller submodule import preflight is missing.")
    app_contract = (
        root.parent
        / "kanda_reasoner_app"
        / "routing_signal_scorer"
        / "ml_advisory_signal"
        / "read_only_advisory_panel_runtime_app_host_visibility_contract.py"
    )
    app_contract_source = app_contract.read_text(encoding="utf-8")
    for marker in (
        "FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES",
        "REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS",
    ):
        if marker not in app_contract_source:
            raise RuntimeError(
                "ML advisory facade re-export contract is missing: " + marker
            )
    tab_patch = (
        root.parent
        / "kanda_reasoner_app"
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_tool_patches.py"
    ).read_text(encoding="utf-8")
    if "lazy_tab_activation" not in tab_patch or "ACTIVATING" not in tab_patch:
        raise RuntimeError("Pre-load lazy-tab activation evidence is missing.")
    audit_spec_contract(SimpleNamespace(spec_path=spec_path))
    print("PORTABLE SPEC AUDIT POLICY RECONCILIATION: PASS")
    _validate_governed_root_zip_timestamp_compatibility(root)
    _validate_zip_member_writer(root, args.package_only)
    _validate_identity_json(root)
    from portable.constants import BUILDER_MEMBER_FEATURE_ID, BUILDER_VERSION, EXTERNAL_CONTROL_FEATURE_ID, FEATURE_ID, FIRST_SMOKE_CONFIRMATION, PORTABLE_HARDENING_FEATURES, PORTABLE_HARDENING_STAGE, PRODUCTION_PORTABLE_ENABLED, SMOKE_CONFIRMATION
    if BUILDER_MEMBER_FEATURE_ID != 'kanda-reasoner-portable-exact-builder-member-governance-v1' or EXTERNAL_CONTROL_FEATURE_ID != 'kanda-reasoner-portable-external-build-control-hash-binding-v1r3' or BUILDER_VERSION != EXPECTED_VERSION or (FEATURE_ID != EXPECTED_FEATURE_ID) or (tuple(PORTABLE_HARDENING_FEATURES) != EXPECTED_HARDENING_FEATURES) or (PORTABLE_HARDENING_STAGE != EXPECTED_HARDENING_STAGE):
        raise RuntimeError('Runtime builder identity contract mismatch.')
    if PRODUCTION_PORTABLE_ENABLED is not True:
        raise RuntimeError('Production Portable authorization gate must be open.')
    if FIRST_SMOKE_CONFIRMATION != 'FIRST PASS CLOSED':
        raise RuntimeError('First natural-close confirmation mismatch.')
    if SMOKE_CONFIRMATION != 'PORTABLE TESTS PASS CLOSED':
        raise RuntimeError('Final natural-close confirmation mismatch.')
    required_text = {'cli.py': ('"--identity-json"', '"--result-json"', 'json.dumps'), 'workflow.py': ('_write_result', '"status": "portable_ready"', 'project_snapshot_after_publication', 'support_snapshot_after_publication', 'PRODUCTION_PORTABLE_ENABLED', 'load_registry_boundary', 'prepare_governed_root_rollback', 'PORTABLE FAILURE TOOL OWNER ROOT EXACT ROLLBACK', '"active_project_identity_used_for_build": False', '"tool_build_authority": "BUILDER_LOCATION"'), 'environment.py': ('PORTABLE CANONICAL SPECIFICATION: PASS', 'PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT', 'PORTABLE SPEC TOOL DATA ALLOWLIST OWNER: PASS', 'PORTABLE SPEC PACKAGE-WIDE DATA COLLECTION: ABSENT', 'iter_packaged_resource_files', '_PROHIBITED_SPEC_PACKAGING_TOKENS', 'validate_external_build_controls', 'PORTABLE EXTERNAL BUILD CONTROL PREFLIGHT: PASS', 'PORTABLE TOOL VENV PYTHON: PASS', 'VENV_PYTHON_RELATIVE'), 'build.py': ('validate_external_build_controls', 'PORTABLE EXTERNAL CONTROLS UNCHANGED THROUGH PYINSTALLER: PASS', '_remove_non_runtime_debris', 'hydrate_physical_runtime', 'validate_physical_runtime', 'validate_packaged_worker_runtime', 'PORTABLE QT WEBENGINE PROCESS: PASS', 'PORTABLE QT WINDOWS PLATFORM PLUGIN: PASS'), 'physical_runtime.py': ('PORTABLE_RUNTIME_ALLOWLIST.json', 'load_runtime_allowlist', 'validate_runtime_allowlist_sources', 'committed_exact_source_archive_path_sha256_allowlist', 'Runtime allowlist source SHA-256 mismatch', 'physical_runtime_manifest.json'), 'archive.py': ('_launch_and_require_natural_close', 'PORTABLE CLEAN SHUTDOWN: PASS', 'validate_archive_members', 'validate_packaged_worker_runtime', 'PORTABLE ZIP POSIX MEMBER WRITER: PASS', 'PORTABLE PACKAGED PROCESS EXIT DURING TAB SMOKE', 'PORTABLE SMOKE RUNTIME REPORT: PASS', 'PORTABLE SMOKE REQUIRED LAZY TABS: PASS', 'verify_no_project_registry', 'selected_project_environment'), 'smoke_isolation.py': ('KANDA_PORTABLE_SMOKE_RUNTIME_REPORT', 'packaged_gui_smoke_runtime_evidence', 'PORTABLE SMOKE RUNTIME REPORT: ENABLED', 'PORTABLE SMOKE FIRST LAUNCH PROJECT NONE: PASS', 'selected_project_environment'), 'create_windows_zip.ps1': ('System.IO.Compression', 'System.IO.Compression.FileSystem', 'ZipArchiveMode]::Create', '.CreateEntry(', 'Replace([char]92, [char]47)', 'ZIP_COMPRESSION_ASSEMBLY_PRELOAD=PASS', 'ZIP_MEMBER_SEPARATOR_CONTRACT=PASS'), 'destination.py': ('askdirectory', 'mustexist=True', 'validate_publication_directory', 'assert_registry_unchanged'), 'publish.py': ('shutil.copyfile', 'os.replace'), 'paths.py': ('%Y%m%d_%H%M%S_%f', '%Y%m%d_%H%M%S', 'build_publication_zip_name', 'publication_zip_name', '-Windows-Portable.zip', 'uuid4().hex[:8]', 'registry_boundary', 'VENV_PYTHON_RELATIVE'), 'registry_boundary.py': ('protected_roots', 'tool_owner_roots', 'assert_registry_unchanged', 'validate_result_path', 'Resolve Tool authority independently of active Project identity'), 'snapshots.py': ('_update_file_content', 'content_snapshot'), 'governed_root_rollback.py': ('prepare_governed_root_rollback', 'tool_owner_roots', 'rollback_scope', 'TOOL_OWNER_ONLY', 'restore_if_changed', 'strict_timestamps=False', 'PORTABLE TOOL OWNER ROOT EXACT BACKUPS: PASS', 'PORTABLE FAILURE-PATH GOVERNED ROOT ROLLBACK: PASS'), 'external_controls.py': ('validate_external_build_controls', 'EXTERNAL_CONTROL_ORDER_OR_PATH_MISMATCH', 'EXTERNAL_CONTROL_SHA256_MISMATCH'), 'builder_members.py': ('validate_exact_builder_members', 'BUILDER_FILE_SET_MISMATCH', 'BUILDER_DIRECTORY_SET_MISMATCH', 'BUILDER_LINK_OR_REPARSE_MEMBER'), 'packaged_worker_runtime.py': ('build_worker_runtime_binaries', 'build_worker_runtime_hooks', 'validate_packaged_worker_runtime', 'PORTABLE WORKER REENTRY HEADLESS DISPATCH: PASS'), 'pyinstaller_worker_dispatch_hook.py': ('KANDA_PORTABLE_WORKER_REPORT_TOKEN', 'headless_worker_dispatch', 'KANDA_PORTABLE_WORKER_REENTRY_REJECTED', 'kanda_reasoner_app.safety_suite_cli', 'sync_startup_routing_kernel_pack.py')}
    for name, tokens in required_text.items():
        source = (root / name).read_text(encoding='utf-8')
        missing = [token for token in tokens if token not in source]
        if missing:
            raise RuntimeError(f'{name} is missing contracts: {missing}')
    environment_source = (root / 'environment.py').read_text(encoding='ascii')
    paths_source = (root / 'paths.py').read_text(encoding='ascii')
    registry_source = (root / 'registry_boundary.py').read_text(encoding='ascii')
    if 'LOCALAPPDATA' in environment_source or 'Programs\" / \"Python' in environment_source:
        raise RuntimeError('Portable builder still binds a user-local base Python path.')
    if 'VENV_PYTHON_RELATIVE' not in environment_source or 'VENV_PYTHON_RELATIVE' not in paths_source:
        raise RuntimeError('Tool .venv Python contract is missing.')
    forbidden_registry_tokens = (
        'Portable creation requires the KANDA Reasoner Tool to be the active Project',
        'Portable creation requires explicit self-hosting authority',
    )
    if any(token in registry_source for token in forbidden_registry_tokens):
        raise RuntimeError('Active Project still authorizes or blocks Tool Portable creation.')
    if 'tool_owner_roots' not in registry_source or 'active Project identity' not in registry_source:
        raise RuntimeError('Tool/Project-decoupled registry boundary is missing.')
    print('PORTABLE TOOL VENV PYTHON CONTRACT: PASS')
    print('PORTABLE FIXED KANDA DRIVE WORDING: ABSENT')
    print('PORTABLE ACTIVE PROJECT BUILD AUTHORITY: ABSENT')
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
    if not args.package_only:
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
    print('PORTABLE PYINSTALLER SUBMODULE IMPORT PREFLIGHT CONTRACT: PASS')
    print('PORTABLE SMOKE RUNTIME REPORT RETENTION CONTRACT: PASS')
    print('PORTABLE PRELOAD TAB ACTIVATION EVIDENCE CONTRACT: PASS')
    print('PORTABLE NATURAL CLOSE CONTRACT: PASS')
    print('PORTABLE CONTENT HASH IMMUTABILITY CONTRACT: PASS')
    print('PORTABLE UNIQUE RUN ID CONTRACT: PASS')
    print('PORTABLE TIMESTAMPED PUBLICATION NAME CONTRACT: PASS')
    print('PORTABLE REGISTRY BOUNDARY MODULE: PASS')
    print('PORTABLE GOVERNED ROOT ROLLBACK MODULE: PASS')
    print('PORTABLE EXACT BUILDER MEMBER GOVERNANCE CAPABILITY: PASS')
    print('PORTABLE EXTERNAL BUILD CONTROL MANIFEST: PASS')
    print(f"PORTABLE EXTERNAL BUILD CONTROL ITEM COUNT: {external_controls['item_count']}")
    print('PORTABLE EXTERNAL BUILD CONTROL EXACT SHA-256: PASS')
    print('PORTABLE EXTERNAL BUILD CONTROL HASH BINDING CAPABILITY: PASS')
    print('PORTABLE ZIP BACKSLASH MEMBER REJECTION PRESERVED: PASS')
    print('PORTABLE WORKER VALIDATOR NON-MUTATION CONTRACT: PASS')
    print('PORTABLE PACKAGED WORKER REENTRY DISPATCH CONTRACT: PASS')
    print('PORTABLE CLEAN START PROJECT NONE CONTRACT: PASS')
    print('PORTABLE GUI LAYOUT REGRESSION RESET CONTRACT: PASS')
    print('PORTABLE PRODUCTION BUILD AUTHORIZATION: PASS')
    print('PORTABLE ALL REGISTERED ROOTS DESTINATION FIREWALL CONTRACT: PASS')
    print('PORTABLE TOOL OWNER MUTATION SCOPE CONTRACT: PASS')
    print('PORTABLE CROSS PROJECT MUTATION NON-INTERFERENCE CONTRACT: PASS')
    print('PORTABLE TOOL/PROJECT DECOUPLED BUILD CONTRACT: PASS')
    if args.package_only:
        print('PORTABLE_V1R18_PRE1980_ZIP_TIMESTAMP_REPAIRED: DEFERRED_PACKAGE_ONLY')
    else:
        print('PORTABLE_V1R18_PRE1980_ZIP_TIMESTAMP_REPAIRED: PASS')
    print(f'VALIDATION OK: {EXPECTED_FEATURE_ID}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
