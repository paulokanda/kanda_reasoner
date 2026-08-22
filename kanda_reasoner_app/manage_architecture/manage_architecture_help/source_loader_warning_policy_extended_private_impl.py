"""Apply extended warning classification policies to architecture source."""

from __future__ import annotations

from collections.abc import Callable


ReplaceOnce = Callable[[str, str, str], str]


def _apply_governed_validator_classification_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Classify governed validate/repair CLIs as validator artifacts."""
    old = (
        'def is_validator_script(module: ModuleInfo) -> bool:\n'
        '    return module.filename.endswith("_validate_manifests.py")\n'
    )
    new = (
        'GOVERNED_VALIDATOR_ROOTS = {"scripts", "tools"}\n'
        'GOVERNED_VALIDATOR_PREFIXES = ("validate_", "repair_")\n\n\n'
        'def is_validator_script(module: ModuleInfo) -> bool:\n'
        '    """Return True for governed validator or repair command modules."""\n'
        '    if module.filename.endswith("_validate_manifests.py"):\n'
        '        return True\n'
        '    normalized_path = module.path.replace("\\\\", "/")\n'
        '    root_name = normalized_path.split("/", 1)[0].lower()\n'
        '    if root_name not in GOVERNED_VALIDATOR_ROOTS:\n'
        '        return False\n'
        '    stem = Path(module.filename).stem.lower().replace("-", "_")\n'
        '    return stem.startswith(GOVERNED_VALIDATOR_PREFIXES)\n'
    )
    return replace_once(source, old, new)


def _apply_boundary_error_contract_marker_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Avoid treating successful feature IDs containing error as failures."""
    old = (
        'def _stmt_prints_failure(stmt: ast.stmt) -> int | None:\n'
        '    """Return the line number when a statement prints failure/error text."""\n'
        '    if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):\n'
        '        return None\n'
        '    if _call_full_name(stmt.value.func) != "print":\n'
        '        return None\n'
        '    printable = " ".join(_string_literals_in_node(stmt.value)).upper()\n'
        '    if "FAIL" in printable or "ERROR" in printable:\n'
        '        return getattr(stmt, "lineno", 0)\n'
        '    return None\n'
    )
    new = (
        'def _stmt_prints_failure(stmt: ast.stmt) -> int | None:\n'
        '    """Return the line number when a statement prints actual failure text."""\n'
        '    if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):\n'
        '        return None\n'
        '    if _call_full_name(stmt.value.func) != "print":\n'
        '        return None\n'
        '    printable = " ".join(_string_literals_in_node(stmt.value)).upper()\n'
        '    failure_markers = (\n'
        '        "VALIDATION ERROR",\n'
        '        "VALIDATION FAIL",\n'
        '        "VALIDATION FAILED",\n'
        '        "ZIP CONTRACT: FAIL",\n'
        '        "FREEZE_HINT_EVIDENCE_MERGE: FAIL",\n'
        '        "FAIL -",\n'
        '        "FAIL:",\n'
        '        ": FAIL",\n'
        '        "FAILED",\n'
        '    )\n'
        '    if any(marker in printable for marker in failure_markers):\n'
        '        return getattr(stmt, "lineno", 0)\n'
        '    if printable.startswith("ERROR:"):\n'
        '        return getattr(stmt, "lineno", 0)\n'
        '    if printable.startswith("ERROR "):\n'
        '        if (\n'
        '            printable.startswith("ERROR MEMORY ")\n'
        '            and (": PASS" in printable or ": ABSENT" in printable)\n'
        '        ):\n'
        '            return None\n'
        '        return getattr(stmt, "lineno", 0)\n'
        '    return None\n'
    )
    return replace_once(source, old, new)


def _apply_stale_variant_active_domain_terms_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Do not flag active domain phrases that contain broad stale tokens."""
    old = (
        'def _filename_has_stale_marker(filename: str) -> bool:\n'
        '    """Return True when a filename looks like an old/copy/fixed variant."""\n'
        '    stem = Path(filename).stem.lower()\n'
        '    tokens = _tokenize_variant_text(stem)\n'
        '    if tokens.intersection(STALE_VARIANT_TOKEN_MARKERS):\n'
        '        return True\n'
        '    if any(marker in stem for marker in STALE_VARIANT_SUBSTRING_MARKERS):\n'
        '        return True\n'
        '    if any(stem.endswith(suffix) for suffix in STALE_VARIANT_SUFFIXES):\n'
        '        return True\n'
        '    return False\n'
    )
    new = (
        'ACTIVE_DOMAIN_STALE_TOKEN_PHRASES = (\n'
        '    "preflight_backup",\n'
        '    "copy_error",\n'
        '    "chat_service",\n'
        '    "transport_repair",\n'
        '    "archive_policy",\n'
        '    "archive_routing",\n'
        '    "archive_validation",\n'
        '    "archive_safety",\n'
        '    "chat_clipboard",\n'
        '    "show_project_backup",\n'
        ')\n'
        'ACTIVE_DOMAIN_STALE_EXACT_STEMS = {"archive", "legacy_bridge", "_draft_intake_lifecycle", "pre_backup_cleanup_dialog", "pre_backup_cleanup_service", "pre_backup_cleanup_support"}\n\n\n'
        'def _filename_has_stale_marker(filename: str) -> bool:\n'
        '    """Return True when a filename looks like an old/copy/fixed variant."""\n'
        '    stem = Path(filename).stem.lower()\n'
        '    if stem in ACTIVE_DOMAIN_STALE_EXACT_STEMS:\n'
        '        return False\n'
        '    candidate = stem\n'
        '    for phrase in ACTIVE_DOMAIN_STALE_TOKEN_PHRASES:\n'
        '        candidate = candidate.replace(phrase, "_")\n'
        '    tokens = _tokenize_variant_text(candidate)\n'
        '    if tokens.intersection(STALE_VARIANT_TOKEN_MARKERS):\n'
        '        return True\n'
        '    if any(marker in candidate for marker in STALE_VARIANT_SUBSTRING_MARKERS):\n'
        '        return True\n'
        '    if any(candidate.endswith(suffix) for suffix in STALE_VARIANT_SUFFIXES):\n'
        '        return True\n'
        '    return False\n'
    )
    return replace_once(source, old, new)

def _apply_generated_prompt_delivery_duplicate_owner_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Exclude generated artifacts and imported facade re-exports from package ownership."""
    old = (
        'def is_excluded_from_duplicate_checks(module: ModuleInfo) -> bool:\n'
        '    normalized_path = module.path.replace("\\\\", "/")\n'
        '    if is_validator_script(module):\n'
        '        return True\n'
        '    if is_generated_bundle_artifact(module):\n'
        '        return True\n'
        '    if is_test_path(normalized_path):\n'
        '        return True\n'
        '    if is_transitional_copy_filename(module.filename):\n'
        '        return True\n'
        '    if is_transitional_path(normalized_path):\n'
        '        return True\n'
        '    if not module.has_explicit_all:\n'
        '        return True\n'
        '    for prefix in EXCLUDED_DUPLICATE_DIR_PREFIXES:\n'
        '        if normalized_path.startswith(prefix):\n'
        '            return True\n'
        '    return False\n'
    )
    new = (
        'GENERATED_PROMPT_DELIVERY_DUPLICATE_PREFIXES = (\n'
        '    "first_prompt_files/",\n'
        '    "second_prompt_files/",\n'
        ')\n\n\n'
        'def _is_generated_prompt_delivery_artifact(module: ModuleInfo) -> bool:\n'
        '    """Return True for generated prompt handoff files, not API owners."""\n'
        '    normalized_path = module.path.replace("\\\\", "/")\n'
        '    return normalized_path.startswith(\n'
        '        GENERATED_PROMPT_DELIVERY_DUPLICATE_PREFIXES\n'
        '    )\n\n\n'
        'def is_excluded_from_duplicate_checks(module: ModuleInfo) -> bool:\n'
        '    normalized_path = module.path.replace("\\\\", "/")\n'
        '    if is_validator_script(module):\n'
        '        return True\n'
        '    if is_generated_bundle_artifact(module):\n'
        '        return True\n'
        '    if _is_generated_prompt_delivery_artifact(module):\n'
        '        return True\n'
        '    if is_test_path(normalized_path):\n'
        '        return True\n'
        '    if is_transitional_copy_filename(module.filename):\n'
        '        return True\n'
        '    if is_transitional_path(normalized_path):\n'
        '        return True\n'
        '    if not module.has_explicit_all:\n'
        '        return True\n'
        '    for prefix in EXCLUDED_DUPLICATE_DIR_PREFIXES:\n'
        '        if normalized_path.startswith(prefix):\n'
        '            return True\n'
        '    return False\n\n\n'
        'def _locally_owned_public_symbols(module: ModuleInfo) -> list[str]:\n'
        '    """Return public bindings defined locally rather than imported facades."""\n'
        '    locally_defined = set(module.all_symbols)\n'
        '    return [symbol for symbol in module.public_symbols if symbol in locally_defined]\n'
    )
    source = replace_once(source, old, new)

    old_duplicate_ownership = (
        '    public_symbol_owners: dict[str, list[ModuleInfo]] = defaultdict(list)\n'
        '    package_symbol_owners: dict[tuple[str, str], list[str]] = defaultdict(list)\n'
        '    for module in modules.values():\n'
        '        if module.is_init:\n'
        '            continue\n'
        '        if is_excluded_from_duplicate_checks(module):\n'
        '            continue\n'
        '        for sym in module.public_symbols:\n'
        '            if sym in EXCLUDED_DUPLICATE_SYMBOLS:\n'
        '                continue\n'
        '            public_symbol_owners[sym].append(module)\n'
        '            package_symbol_owners[(module.package, sym)].append(module.module_id)\n'
    )
    new_duplicate_ownership = (
        '    public_symbol_owners: dict[str, list[ModuleInfo]] = defaultdict(list)\n'
        '    package_symbol_owners: dict[tuple[str, str], list[str]] = defaultdict(list)\n'
        '    for module in modules.values():\n'
        '        if module.is_init:\n'
        '            continue\n'
        '        if is_excluded_from_duplicate_checks(module):\n'
        '            continue\n'
        '        locally_owned = set(_locally_owned_public_symbols(module))\n'
        '        for sym in module.public_symbols:\n'
        '            if sym in EXCLUDED_DUPLICATE_SYMBOLS:\n'
        '                continue\n'
        '            public_symbol_owners[sym].append(module)\n'
        '            if sym in locally_owned:\n'
        '                package_symbol_owners[(module.package, sym)].append(module.module_id)\n'
    )
    source = replace_once(source, old_duplicate_ownership, new_duplicate_ownership)

    old_manifest_ownership = (
        '        if not info.is_init:\n'
        '            for sym in info.public_symbols:\n'
        '                package_symbol_owners[(info.package, sym)].append(module_id)\n'
    )
    new_manifest_ownership = (
        '        if not info.is_init:\n'
        '            for sym in _locally_owned_public_symbols(info):\n'
        '                package_symbol_owners[(info.package, sym)].append(module_id)\n'
    )
    return replace_once(source, old_manifest_ownership, new_manifest_ownership)

def _apply_mixed_responsibility_boundary_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Accept documented UI/domain adapters and governed validators."""
    source = replace_once(
        source,
        'def _format_mixed_responsibility_message(\n',
        (
            'MIXED_RESPONSIBILITY_GOVERNED_ARTIFACT_ROOTS = {"scripts", "tools"}\n'
            'MIXED_RESPONSIBILITY_GOVERNED_ARTIFACT_PREFIXES = ("validate_", "repair_")\n'
            'MIXED_RESPONSIBILITY_ALLOWED_BOUNDARY_DOMAINS: tuple[\n'
            '    tuple[str, frozenset[str]], ...\n'
            '] = (\n'
            '    (\n'
            '        "kanda_reasoner_app/error_memory_gui/",\n'
            '        frozenset({"gui_ui", "ai_bridge", "prompt_building"}),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/freeze_after_update_gui/",\n'
            '        frozenset({"gui_ui", "ai_bridge"}),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/insert_missing_docstrings_gui/",\n'
            '        frozenset({"gui_ui", "docstring_tool", "ai_bridge"}),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/manage_architecture/",\n'
            '        frozenset({\n'
            '            "gui_ui",\n'
            '            "architecture_governance",\n'
            '            "ai_bridge",\n'
            '            "daily_refactor_report",\n'
            '        }),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/manage_workflows/",\n'
            '        frozenset({\n'
            '            "gui_ui",\n'
            '            "workflow_governance",\n'
            '            "daily_refactor_report",\n'
            '            "architecture_governance",\n'
            '            "ai_bridge",\n'
            '        }),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/reasoner_engine/",\n'
            '        frozenset({\n'
            '            "gui_ui",\n'
            '            "ai_bridge",\n'
            '            "prompt_building",\n'
            '            "retrieval",\n'
            '            "static_collection",\n'
            '            "runtime_collection",\n'
            '        }),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/reasoner_tools_gui_shell/",\n'
            '        frozenset({"gui_ui", "ai_bridge"}),\n'
            '    ),\n'
            '    (\n'
            '        "kanda_reasoner_app/local_ai_configuration.py",\n'
            '        frozenset({"gui_ui", "ai_bridge"}),\n'
            '    ),\n'
            ')\n\n\n'
            'def _is_mixed_responsibility_governed_artifact(module: ModuleInfo) -> bool:\n'
            '    """Return True for validator/repair artifacts, not app owners."""\n'
            '    normalized_path = module.path.replace("\\\\", "/")\n'
            '    root_name = normalized_path.split("/", 1)[0].lower()\n'
            '    if root_name not in MIXED_RESPONSIBILITY_GOVERNED_ARTIFACT_ROOTS:\n'
            '        return False\n'
            '    stem = Path(module.filename).stem.lower().replace("-", "_")\n'
            '    return stem.startswith(MIXED_RESPONSIBILITY_GOVERNED_ARTIFACT_PREFIXES)\n\n\n'
            'def _is_documented_mixed_responsibility_boundary(\n'
            '    module: ModuleInfo,\n'
            '    domains: dict[str, list[str]],\n'
            ') -> bool:\n'
            '    """Return True when mixed terms belong to an explicit adapter boundary."""\n'
            '    if _is_mixed_responsibility_governed_artifact(module):\n'
            '        return True\n'
            '    normalized_path = module.path.replace("\\\\", "/")\n'
            '    domain_names = set(domains)\n'
            '    for path_prefix, allowed_domains in MIXED_RESPONSIBILITY_ALLOWED_BOUNDARY_DOMAINS:\n'
            '        if normalized_path.startswith(path_prefix) and domain_names <= allowed_domains:\n'
            '            return True\n'
            '    return False\n\n\n'
            'def _format_mixed_responsibility_message(\n'
        ),
    )
    return replace_once(
        source,
        (
            '        domains = _mixed_responsibility_hits(module)\n'
            '        if len(domains) < 2:\n'
            '            continue\n\n'
            '        # Governance detector modules intentionally mention many boxes while\n'
        ),
        (
            '        domains = _mixed_responsibility_hits(module)\n'
            '        if len(domains) < 2:\n'
            '            continue\n'
            '        if _is_documented_mixed_responsibility_boundary(module, domains):\n'
            '            continue\n\n'
            '        # Governance detector modules intentionally mention many boxes while\n'
        ),
    )


def _apply_import_heaviness_gui_boundary_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Accept intentional Qt imports in GUI adapters and GUI validators."""
    old = (
        'def _is_intentional_gui_import_surface(module: ModuleInfo) -> bool:\n'
        '    """Return True for explicit GUI/profiling surfaces that own Qt imports."""\n'
        '    normalized = module.path.lower().replace(chr(92), "/")\n'
        '    return any(\n'
        '        normalized.endswith(suffix)\n'
        '        for suffix in INTENTIONAL_GUI_IMPORT_SURFACE_SUFFIXES\n'
        '    )\n'
    )
    new = (
        'GUI_VALIDATION_ARTIFACT_ROOTS = ("tools/validate_", "scripts/validate_")\n'
        'INTENTIONAL_KANDA_GUI_IMPORT_PREFIXES = (\n'
        '    "kanda_reasoner_app/manage_architecture/ai_review/",\n'
        '    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/",\n'
        '    "kanda_reasoner_app/reasoner_tools_shell/runner_help/",\n'
        '    "kanda_reasoner_app/tab3_manual_review_runtime/",\n'
        ')\n'
        'INTENTIONAL_KANDA_GUI_IMPORT_PATHS = {\n'
        '    "kanda_reasoner_app/external_ai_configuration.py",\n'
        '    "kanda_reasoner_app/external_ai_handoff.py",\n'
        '    "kanda_reasoner_app/local_ai_configuration.py",\n'
        '    "kanda_reasoner_app/manage_architecture/architecture_audit_external_ai.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/safe_web_page.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/tab_evidence_mixin.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/tab_json_controls_mixin.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/tab_navigation_mixin.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/tab_ui_builder.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/tab_viewport_activation_mixin.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/web_bridge.py",\n'
        '    "kanda_reasoner_app/project_structure_visualizer/web_runtime.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/chat_clipboard_actions.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/config_ai_tab.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/config_web_ai_ui_support.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preview.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_configuration_selector.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",\n'
        '    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",\n'
        '    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_2_scenarios.py",\n'
        '    "kanda_reasoner_app/web_ai_configuration.py",\n'
        '}\n\n\n'
        'def _is_intentional_gui_import_surface(module: ModuleInfo) -> bool:\n'
        '    """Return True for explicit GUI/profiling surfaces that own Qt imports."""\n'
        '    normalized = module.path.lower().replace(chr(92), "/")\n'
        '    if normalized.startswith(GUI_VALIDATION_ARTIFACT_ROOTS):\n'
        '        return True\n'
        '    if normalized in INTENTIONAL_KANDA_GUI_IMPORT_PATHS:\n'
        '        return True\n'
        '    if normalized.startswith(INTENTIONAL_KANDA_GUI_IMPORT_PREFIXES):\n'
        '        return True\n'
        '    return any(\n'
        '        normalized.endswith(suffix)\n'
        '        for suffix in INTENTIONAL_GUI_IMPORT_SURFACE_SUFFIXES\n'
        '    )\n'
    )
    return replace_once(source, old, new)


def _apply_side_effect_governed_validation_policy(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Exclude governed validation scripts from import-time side-effect warnings."""
    old = (
        'def detect_side_effect_on_import_issues(\n'
        '    root: Path,\n'
        '    modules: dict[str, ModuleInfo],\n'
        ') -> list[ValidationIssue]:\n'
        '    """Detect risky top-level calls that execute during module import."""\n'
        '    issues: list[ValidationIssue] = []\n'
        '    for module in sorted(modules.values(), key=lambda item: item.path):\n'
        '        if module.is_init or is_test_path(module.path) or stale_variant_reasons(module):\n'
        '            continue\n'
        '        path = root / module.path\n'
        '        try:\n'
        '            text = read_text(path)\n'
    )
    new = (
        'def detect_side_effect_on_import_issues(\n'
        '    root: Path,\n'
        '    modules: dict[str, ModuleInfo],\n'
        ') -> list[ValidationIssue]:\n'
        '    """Detect risky top-level calls that execute during module import."""\n'
        '    issues: list[ValidationIssue] = []\n'
        '    for module in sorted(modules.values(), key=lambda item: item.path):\n'
        '        if module.is_init or is_test_path(module.path) or stale_variant_reasons(module):\n'
        '            continue\n'
        '        if _is_governed_validation_or_repair_artifact(module):\n'
        '            continue\n'
        '        path = root / module.path\n'
        '        try:\n'
        '            text = read_text(path)\n'
    )
    return replace_once(source, old, new)


def apply_manage_architecture_extended_warning_policies(
    source: str,
    replace_once: ReplaceOnce,
) -> str:
    """Apply the extended warning-policy chain in its governed order."""
    source = _apply_governed_validator_classification_policy(
        source,
        replace_once,
    )
    source = _apply_boundary_error_contract_marker_policy(
        source,
        replace_once,
    )
    source = _apply_stale_variant_active_domain_terms_policy(
        source,
        replace_once,
    )
    source = _apply_generated_prompt_delivery_duplicate_owner_policy(
        source,
        replace_once,
    )
    source = _apply_mixed_responsibility_boundary_policy(
        source,
        replace_once,
    )
    source = _apply_import_heaviness_gui_boundary_policy(
        source,
        replace_once,
    )
    return _apply_side_effect_governed_validation_policy(
        source,
        replace_once,
    )


__all__ = ["apply_manage_architecture_extended_warning_policies"]
