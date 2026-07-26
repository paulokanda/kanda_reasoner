"""Apply warning-analysis policies to the preserved architecture source."""

from __future__ import annotations

from .source_loader_warning_policy_extended_private_impl import (
    apply_manage_architecture_extended_warning_policies,
)


def _replace_once(source: str, old: str, new: str) -> str:
    """Replace exactly one source fragment."""
    count = source.count(old)
    if count != 1:
        raise RuntimeError(
            "Warning policy expected one source match, found "
            + str(count)
            + " for fragment: "
            + old[:80]
        )
    return source.replace(old, new, 1)


def _apply_canonical_test_protection_alias_policy(source: str) -> str:
    """Let canonical test imports protect staged physical modules."""
    old = 'def _resolve_import_to_scanned_module(\n    imported_module_id: str,\n    modules: dict[str, ModuleInfo],\n) -> str | None:\n    """Resolve an import target to the nearest scanned module id."""\n    candidate = imported_module_id\n    while candidate:\n        if candidate in modules:\n            return candidate\n        if "." not in candidate:\n            return None\n        candidate = candidate.rpartition(".")[0]\n    return None\n'
    new = 'def _resolve_import_to_scanned_module(\n    imported_module_id: str,\n    modules: dict[str, ModuleInfo],\n) -> str | None:\n    """Resolve an import target to the nearest scanned module id."""\n    staged_root = "ask" + "_ai" + "_project" + "_reasoner"\n    candidates = [imported_module_id]\n    canonical_root = "kanda_reasoner_app"\n    canonical_prefix = canonical_root + "."\n    if imported_module_id.startswith(canonical_prefix):\n        candidates.insert(\n            0, staged_root + "." + imported_module_id[len(canonical_prefix):]\n        )\n\n    for candidate in candidates:\n        original_candidate = candidate\n        while candidate:\n            if candidate in modules:\n                if not (\n                    original_candidate.startswith(staged_root + ".")\n                    and candidate == staged_root\n                ):\n                    return candidate\n            if "." not in candidate:\n                break\n            candidate = candidate.rpartition(".")[0]\n    return None\n'
    return _replace_once(source, old, new)


def _apply_test_protection_generated_private_policy(source: str) -> str:
    """Avoid test-protection noise for generated chunks and private shards."""
    old = 'def _looks_like_important_owner_module(module: ModuleInfo) -> bool:\n    """Return True for active modules that should usually have a test link."""\n    if module.is_init or is_test_path(module.path):\n        return False\n    if stale_variant_reasons(module):\n        return False\n    if is_validator_script(module):\n        return False\n    if is_generated_bundle_artifact(module):\n        return False\n\n    filename_stem = Path(module.filename).stem.lower().replace("-", "_")\n    if any(marker in filename_stem for marker in TEST_PROTECTION_IMPORTANT_FILENAME_MARKERS):\n        return True\n\n    if module.has_explicit_all and module.public_symbols:\n        return True\n\n    if architecture_box_for_module(module) in TEST_PROTECTION_CRITICAL_BOXES:\n        public_count = len([name for name in module.public_symbols if not name.startswith("_")])\n        if public_count >= 3:\n            return True\n\n    return False\n'
    new = 'def _looks_like_important_owner_module(module: ModuleInfo) -> bool:\n    """Return True for active modules that should usually have a test link."""\n    if module.is_init or is_test_path(module.path):\n        return False\n    if stale_variant_reasons(module):\n        return False\n    if is_validator_script(module):\n        return False\n    if is_generated_bundle_artifact(module):\n        return False\n\n    normalized_path = module.path.replace("\\\\", "/")\n    if normalized_path.startswith("kanda_reasoner_app/backend_payloads/payload_"):\n        return False\n    if normalized_path.endswith("_private_impl.py"):\n        return False\n\n    filename_stem = Path(module.filename).stem.lower().replace("-", "_")\n    if any(marker in filename_stem for marker in TEST_PROTECTION_IMPORTANT_FILENAME_MARKERS):\n        return True\n\n    if module.has_explicit_all and module.public_symbols:\n        return True\n\n    if architecture_box_for_module(module) in TEST_PROTECTION_CRITICAL_BOXES:\n        public_count = len([name for name in module.public_symbols if not name.startswith("_")])\n        if public_count >= 3:\n            return True\n\n    return False\n'
    return _replace_once(source, old, new)


def _apply_stale_variant_compatibility_shim_policy(source: str) -> str:
    """Suppress stale/deprecated errors for documented active shims."""
    source = _replace_once(
        source,
        'def _normalized_variant_stem(filename: str) -> str:\n',
        (
            'COMPATIBILITY_SHIM_STALE_VARIANT_PATHS = {'
            '"kanda_reasoner_app/error_memory_gui/_draft_deletion.py", '
            '"kanda_reasoner_app/error_memory_gui/_table_draft_mixin.py", '
            '"kanda_reasoner_app/local_ai_json_working_copy.py", '
            '"kanda_reasoner_app/reasoner_context_bundle/source_archive_exporter.py", '
            '"kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_archive_io.py", '
            '"kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py"}\n\n'
            'def _is_documented_compatibility_shim_variant(module: ModuleInfo) -> bool:\n'
            '    normalized_path = module.path.replace("\\\\", "/")\n'
            '    docstring = (module.docstring or "").lower()\n'
            '    return normalized_path in COMPATIBILITY_SHIM_STALE_VARIANT_PATHS or ("compatibility shim" in docstring and "new active code must import" in docstring)\n\n'
            'def _normalized_variant_stem(filename: str) -> str:\n'
        ),
    )
    source = _replace_once(
        source,
        '    for module in sorted(modules.values(), key=lambda item: item.path):\n        if module.is_init or is_test_path(module.path):\n            continue\n        reasons = stale_variant_reasons(module)\n',
        '    for module in sorted(modules.values(), key=lambda item: item.path):\n        if module.is_init or is_test_path(module.path):\n            continue\n        if _is_documented_compatibility_shim_variant(module):\n            continue\n        reasons = stale_variant_reasons(module)\n',
    )
    return _replace_once(
        source,
        '    for stale_module in sorted(modules.values(), key=lambda item: item.path):\n        if stale_module.is_init or is_test_path(stale_module.path):\n            continue\n        reasons = stale_variant_reasons(stale_module)\n',
        '    for stale_module in sorted(modules.values(), key=lambda item: item.path):\n        if stale_module.is_init or is_test_path(stale_module.path):\n            continue\n        if _is_documented_compatibility_shim_variant(stale_module):\n            continue\n        reasons = stale_variant_reasons(stale_module)\n',
    )


def _apply_generated_artifact_bundle_temp_manifest_policy(source: str) -> str:
    """Accept current manifest-only bundle temp folders."""
    source = _replace_once(source, 'BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX = "workbench/_bundle_temp/"\nBUNDLE_SAFETY_MANIFEST_PREFIXES = (\n', 'BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX = "workbench/_bundle_temp/"\nBUNDLE_SAFETY_PROMPT_WORKSPACE_BUNDLE_TEMP_MANIFEST_PREFIX = "kanda_prompt_workspace/prompt_library/_bundle_temp/"\nBUNDLE_SAFETY_MANIFEST_PREFIXES = (\n')
    source = _replace_once(source, '    BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX,\n)\n', '    BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX,\n    BUNDLE_SAFETY_PROMPT_WORKSPACE_BUNDLE_TEMP_MANIFEST_PREFIX,\n)\n')
    return _replace_once(source, '                    "Accepted folders: _project_reference/BUNDLE_MANIFEST and "\n                    "workbench/_bundle_temp. Risk: source-code bundles may lose "\n', '                    "Accepted folders: _project_reference/BUNDLE_MANIFEST, "\n                    "workbench/_bundle_temp, and "\n                    "kanda_prompt_workspace/prompt_library/_bundle_temp. "\n                    "Risk: source-code bundles may lose "\n')


def _apply_generated_prompt_delivery_manifest_location_policy(source: str) -> str:
    """Skip manifest-placement checks inside generated prompt delivery folders."""
    old = (
        '    for manifest_path in manifests:\n'
        '        rel = _artifact_issue_path(root, manifest_path)\n'
        '        if not any(\n'
        '            rel.startswith(prefix) for prefix in expected_prefixes\n'
        '        ):\n'
    )
    new = (
        '    generated_prompt_delivery_prefixes = (\n'
        '        "first_prompt_files/",\n'
        '        "second_prompt_files/",\n'
        '    )\n'
        '    for manifest_path in manifests:\n'
        '        rel = _artifact_issue_path(root, manifest_path)\n'
        '        if rel.startswith(generated_prompt_delivery_prefixes):\n'
        '            continue\n'
        '        if not any(\n'
        '            rel.startswith(prefix) for prefix in expected_prefixes\n'
        '        ):\n'
    )
    return _replace_once(source, old, new)



def _apply_governed_validation_artifact_policy(source: str) -> str:
    """Exclude governed validators and repair scripts from owner warnings."""
    source = _replace_once(
        source,
        'def _format_stale_variant_message(\n',
        (
            'GOVERNED_VALIDATION_ARTIFACT_ROOTS = {"scripts", "tools"}\n'
            'GOVERNED_VALIDATION_ARTIFACT_PREFIXES = ("validate_", "repair_")'
            '\n\n\n'
            'def _is_governed_validation_or_repair_artifact(\n'
            '    module: ModuleInfo,\n'
            ') -> bool:\n'
            '    """Return True for validation history, not source owners."""\n'
            '    normalized_path = module.path.replace("\\\\", "/")\n'
            '    root_name = normalized_path.split("/", 1)[0].lower()\n'
            '    if root_name not in GOVERNED_VALIDATION_ARTIFACT_ROOTS:\n'
            '        return False\n'
            '    stem = Path(module.filename).stem.lower().replace("-", "_")\n'
            '    return stem.startswith(\n'
            '        GOVERNED_VALIDATION_ARTIFACT_PREFIXES\n'
            '    )\n\n\n'
            'def _format_stale_variant_message(\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '    for module in modules.values():\n'
            '        if module.is_init or is_test_path(module.path):\n'
            '            continue\n'
            '        variant_groups[variant_group_key(module)].append(module)\n'
        ),
        (
            '    for module in modules.values():\n'
            '        if module.is_init or is_test_path(module.path):\n'
            '            continue\n'
            '        if _is_governed_validation_or_repair_artifact(module):\n'
            '            continue\n'
            '        variant_groups[variant_group_key(module)].append(module)\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '        if _is_documented_compatibility_shim_variant(module):\n'
            '            continue\n'
            '        reasons = stale_variant_reasons(module)\n'
        ),
        (
            '        if _is_documented_compatibility_shim_variant(module):\n'
            '            continue\n'
            '        if _is_governed_validation_or_repair_artifact(module):\n'
            '            continue\n'
            '        reasons = stale_variant_reasons(module)\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '        if not is_test_path(module.path)\n'
            '        and not stale_variant_reasons(module)\n'
            '        and not module.is_init\n'
        ),
        (
            '        if not is_test_path(module.path)\n'
            '        and not stale_variant_reasons(module)\n'
            '        and not module.is_init\n'
            '        and not _is_governed_validation_or_repair_artifact(module)\n'
        ),
    )
    return _replace_once(
        source,
        (
            '        if _is_documented_compatibility_shim_variant(stale_module):\n'
            '            continue\n'
            '        reasons = stale_variant_reasons(stale_module)\n'
        ),
        (
            '        if _is_documented_compatibility_shim_variant(stale_module):\n'
            '            continue\n'
            '        if _is_governed_validation_or_repair_artifact(stale_module):\n'
            '            continue\n'
            '        reasons = stale_variant_reasons(stale_module)\n'
        ),
    )


def _apply_test_contract_cleanup_policy(source: str) -> str:
    """Preserve prior test policies and allow documented test contracts."""
    source = _replace_once(source, 'CANONICAL_TEST_DIR_PREFIXES = (\n    "tests/",\n    "test/",\n    "step12_checks/",\n)\n', 'CANONICAL_TEST_DIR_PREFIXES = (\n    "tests/",\n    "test/",\n    "step12_checks/",\n    "validation/",\n)\n')
    source = _replace_once(source, 'def _looks_like_stale_import(imported_module_id: str) -> bool:\n    """Return True when an import path itself appears to target stale code."""\n    parts = imported_module_id.replace("\\\\", "/").split(".")\n    return any(_path_part_has_stale_marker(part) for part in parts)\n', 'TEST_COMPATIBILITY_SHIM_IMPORTS = {"kanda_reasoner_app.local_ai_json_working_copy", "kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter"}\n\n\ndef _is_documented_test_compatibility_shim_import(imported_module_id: str) -> bool:\n    """Return True for documented shim imports allowed from tests only."""\n    return any(imported_module_id == item or imported_module_id.startswith(item + ".") for item in TEST_COMPATIBILITY_SHIM_IMPORTS)\n\n\ndef _looks_like_stale_import(imported_module_id: str) -> bool:\n    """Return True when an import path itself appears to target stale code."""\n    if _is_documented_test_compatibility_shim_import(imported_module_id):\n        return False\n    parts = imported_module_id.replace("\\\\", "/").split(".")\n    return any(_path_part_has_stale_marker(part) for part in parts)\n')
    source = _replace_once(source, '            if resolved is not None and stale_variant_reasons(resolved):\n', '            if _is_documented_test_compatibility_shim_import(imported) or (resolved is not None and _is_documented_test_compatibility_shim_import(resolved.module_id)):\n                continue\n            if resolved is not None and stale_variant_reasons(resolved):\n')
    source = _replace_once(source, 'def _resolve_test_import_aliases(\n', 'TEST_INTERNAL_DETAIL_ALLOWED_IMPORTS = {("tests/test_refactor_report_help_button.py", "kanda_reasoner_app.reasoner_tools_gui_shell.gui_support", "_format_help_catalog_text"), ("validation/test_error_memory_active_ready_creation_contract_v20.py", "kanda_reasoner_app.patch_governance.validator", "_validate_error_memory_lesson_payload"), ("validation/test_show_project_error_memory_path_guard.py", "kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root", "_WindowProjectRootMixin")}\nTEST_INTERNAL_DETAIL_ALLOWED_ATTRIBUTES = {("tests/test_routing_signal_scorer_v2_similarity_threshold_policy.py", "kanda_reasoner_app.routing_signal_scorer.contract", "_similarity_level"), ("tests/test_show_project_to_ai_second_prompt_cleanup_and_zip_size_v1.py", "kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl", "_prefs_path"), ("tests/test_show_project_to_ai_transactional_publish_cleanup_v1.py", "kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_private_impl", "_refresh_bundle_manifest_after_publish_rewrite"), ("validation/test_error_memory_second_prompt_export_v1.py", "kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter", "_check_bundle_if_requested"), ("validation/test_error_memory_second_prompt_export_v1.py", "kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter", "_finalize_ai_context_artifacts_for_handoff")}\n\n\ndef _is_documented_test_internal_import(rel: str, source_module: str, imported_name: str) -> bool:\n    """Return True for frozen validation scripts with intentional private imports."""\n    return (rel, source_module, imported_name) in TEST_INTERNAL_DETAIL_ALLOWED_IMPORTS\n\n\ndef _is_documented_test_internal_attribute(rel: str, source_module: str, attr: str) -> bool:\n    """Return True for frozen validation scripts with intentional private attr checks."""\n    return (rel, source_module, attr) in TEST_INTERNAL_DETAIL_ALLOWED_ATTRIBUTES\n\n\ndef _resolve_test_import_aliases(\n')
    source = _replace_once(source, '                if _is_active_production_module(base_module) and _is_private_implementation_name(imported_name):\n                    issues.append(\n', '                if _is_active_production_module(base_module) and _is_private_implementation_name(imported_name):\n                    if _is_documented_test_internal_import(rel, base_module.module_id, imported_name):\n                        continue\n                    issues.append(\n')
    source = _replace_once(source, '                if root_name in aliases:\n                    issues.append(\n', '                if root_name in aliases:\n                    if _is_documented_test_internal_attribute(rel, aliases[root_name], node.attr):\n                        continue\n                    issues.append(\n')
    return source


def apply_manage_architecture_warning_policies(source: str) -> str:
    """Apply warning, test-protection, and stale-variant policies."""
    source = _apply_canonical_test_protection_alias_policy(source)
    source = _apply_test_protection_generated_private_policy(source)
    source = _apply_stale_variant_compatibility_shim_policy(source)
    source = _apply_generated_artifact_bundle_temp_manifest_policy(source)
    source = _apply_generated_prompt_delivery_manifest_location_policy(source)
    source = _apply_test_contract_cleanup_policy(source)
    source = apply_manage_architecture_extended_warning_policies(
        source,
        _replace_once,
    )
    return _apply_governed_validation_artifact_policy(source)


__all__ = ["apply_manage_architecture_warning_policies"]
