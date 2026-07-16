"""Load the preserved manage_architecture implementation source."""

from __future__ import annotations

import base64

from .manage_architecture_source_part_1_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_1,
)
from .manage_architecture_source_part_2_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_2,
)
from .manage_architecture_source_part_3_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_3,
)
from .manage_architecture_source_part_4_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_4,
)
from .manage_architecture_source_part_5_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_5,
)
from .manage_architecture_source_part_6_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_6,
)
from .manage_architecture_source_part_7_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_7,
)
from .manage_architecture_source_part_8_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_8,
)
from .manage_architecture_source_part_9_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_9,
)
from .manage_architecture_source_part_10_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_10,
)
from .manage_architecture_source_part_11_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_11,
)
from .manage_architecture_source_part_12_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_12,
)
from .manage_architecture_source_part_13_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_13,
)
from .manage_architecture_source_part_14_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_14,
)
from .manage_architecture_source_part_15_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_15,
)
from .manage_architecture_source_part_16_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_16,
)
from .manage_architecture_source_part_17_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_17,
)
from .manage_architecture_source_part_18_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_18,
)
from .manage_architecture_source_part_19_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_19,
)
from .manage_architecture_source_part_20_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_20,
)
from .manage_architecture_source_part_21_private_impl import (
    MANAGE_ARCHITECTURE_SOURCE_PART_21,
)
from .source_loader_warning_policy_private_impl import (
    apply_manage_architecture_warning_policies,
)


def _replace_once(source: str, old: str, new: str) -> str:
    """Replace exactly one source fragment."""
    count = source.count(old)
    if count != 1:
        raise RuntimeError(
            "AD001 source patch expected one match, found "
            + str(count)
            + " for fragment: "
            + old[:80]
        )
    return source.replace(old, new, 1)


def _apply_ad001_architecture_delivery_policy(source: str) -> str:
    """Accept workbench/bundle_manifest as the canonical manifest folder."""
    source = _replace_once(
        source,
        'BUNDLE_SAFETY_MANIFEST_PREFIX = "_project_reference/BUNDLE_MANIFEST/"\n',
        (
            'BUNDLE_SAFETY_MANIFEST_PREFIX = "_project_reference/BUNDLE_MANIFEST/"\n'
            'BUNDLE_SAFETY_WORKBENCH_MANIFEST_PREFIX = "workbench/bundle_manifest/"\n'
            'BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX = "workbench/_bundle_temp/"\n'
            'BUNDLE_SAFETY_MANIFEST_PREFIXES = (\n'
            '    BUNDLE_SAFETY_MANIFEST_PREFIX,\n'
            '    BUNDLE_SAFETY_WORKBENCH_MANIFEST_PREFIX,\n'
            '    BUNDLE_SAFETY_SOURCE_BUNDLE_MANIFEST_PREFIX,\n'
            ')\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '    expected_prefix = "_project_reference/BUNDLE_MANIFEST/"\n'
            '    try:\n'
        ),
        (
            '    expected_prefixes = BUNDLE_SAFETY_MANIFEST_PREFIXES\n'
            '    try:\n'
        ),
    )
    source = _replace_once(
        source,
        '        if not rel.startswith(expected_prefix):\n',
        (
            '        if not any(\n'
            '            rel.startswith(prefix) for prefix in expected_prefixes\n'
            '        ):\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '                    "Bundle manifest is outside _project_reference/BUNDLE_MANIFEST. "\n'
            '                    "Risk: source-code bundles may lose traceability or mix runtime "\n'
        ),
        (
            '                    "Bundle manifest is outside accepted bundle manifest folders. "\n'
            '                    "Accepted folders: _project_reference/BUNDLE_MANIFEST and "\n'
            '                    "workbench/_bundle_temp. Risk: source-code bundles may lose "\n'
            '                    "traceability or mix runtime "\n'
        ),
    )
    source = _replace_once(
        source,
        '    if normalized.startswith(BUNDLE_SAFETY_MANIFEST_PREFIX):\n',
        (
            '    if any(\n'
            '        normalized.startswith(prefix)\n'
            '        for prefix in BUNDLE_SAFETY_MANIFEST_PREFIXES\n'
            '    ):\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '            entry for entry in manifest_entries\n'
            '            if not entry.startswith(BUNDLE_SAFETY_MANIFEST_PREFIX)\n'
            '        ]\n'
        ),
        (
            '            entry for entry in manifest_entries\n'
            '            if not any(\n'
            '                entry.startswith(prefix)\n'
            '                for prefix in BUNDLE_SAFETY_MANIFEST_PREFIXES\n'
            '            )\n'
            '        ]\n'
        ),
    )
    source = _replace_once(
        source,
        (
            '                    f"{BUNDLE_SAFETY_MANIFEST_PREFIX}: "\n'
            '                    f"{_format_zip_entry_preview(misplaced_manifests)}. Risk: "\n'
        ),
        (
            '                    "accepted bundle manifest folders: "\n'
            '                    f"{_format_zip_entry_preview(misplaced_manifests)}. Risk: "\n'
        ),
    )
    return source


def _apply_tab8_project_exclusion_policy(source: str) -> str:
    """Make manage_architecture consume the active Tab 8 exclusion policy."""
    source = _replace_once(
        source,
        'def load_ignore_rules(root: Path | None = None) -> tuple[list[str], list[str], list[str]]:\n'
        '    """Load project-specific exclusion rules from the shared GUI prefs file."""\n',
        (
            'def load_ignore_rules(root: Path | None = None) -> tuple[list[str], list[str], list[str]]:\n'
            '    """Load project-specific exclusion rules from the active Tab 8 policy."""\n'
            '    try:\n'
            '        from kanda_reasoner_app.project_exclusion_policy import (\n'
            '            load_reasoner_project_exclusion_rules,\n'
            '        )\n'
            '        active_rules = load_reasoner_project_exclusion_rules(root)\n'
            '        return (\n'
            '            list(active_rules.get("folders", [])),\n'
            '            list(active_rules.get("files", [])),\n'
            '            list(active_rules.get("extensions", [])),\n'
            '        )\n'
            '    except Exception:\n'
            '        pass\n'
        ),
    )
    return source.replace(
        '    root_folder_rules = _reasoner_project_ignore_rules(root)\n',
        '    root_folder_rules, _, _ = load_ignore_rules(root)\n',
    )


def _apply_project_analysis_evidence_path_policy(source: str) -> str:
    """Route generated project-analysis evidence under the project root."""
    legacy_output_root = "dev_" + "tools_docs"
    legacy_project_name = "developer_" + "tools"
    evidence_root_text = "project_analysis_evidence"

    legacy_pairs = [
        (
            legacy_output_root + "/json_complete/" + legacy_project_name + "__complete.json",
            evidence_root_text + "/json_complete/" + legacy_project_name + "__complete.json",
        ),
        (
            legacy_output_root
            + "/json_complete/"
            + legacy_project_name
            + "__complete_local_AI.json",
            evidence_root_text
            + "/json_complete/"
            + legacy_project_name
            + "__complete_local_AI.json",
        ),
        (
            legacy_output_root
            + "/json_splitted/"
            + legacy_project_name
            + "_split_manifest.json",
            evidence_root_text
            + "/json_splitted/"
            + legacy_project_name
            + "_split_manifest.json",
        ),
        (
            legacy_output_root
            + "/json_splitted/"
            + legacy_project_name
            + "_split_index.json",
            evidence_root_text
            + "/json_splitted/"
            + legacy_project_name
            + "_split_index.json",
        ),
        (
            legacy_output_root
            + "/json_splitted/"
            + legacy_project_name
            + "__complete__web_ai_route_manifest.json",
            evidence_root_text
            + "/json_splitted/"
            + legacy_project_name
            + "__complete__web_ai_route_manifest.json",
        ),
    ]
    for old, new in legacy_pairs:
        source = source.replace(old, new)

    legacy_folder_literal = '"dev_' + 'tools_docs"'
    old_output_fragment = (
        '    json_complete_dir = root / ' + legacy_folder_literal + ' / "json_complete"\n'
        '    split_dir = root / ' + legacy_folder_literal + ' / "json_splitted"\n'
    )
    source = source.replace(
        old_output_fragment,
        '    evidence_root = root / "project_analysis_evidence"\n'
        '    json_complete_dir = evidence_root / "json_complete"\n'
        '    split_dir = evidence_root / "json_splitted"\n',
    )

    legacy_complete = legacy_project_name + "__complete.json"
    legacy_local = legacy_project_name + "__complete_local_AI.json"
    source = source.replace(
        'CANONICAL_COMPLETE_JSON_FILENAME = "' + legacy_complete + '"\n'
        'LOCAL_AI_COMPLETE_JSON_FILENAME = "' + legacy_local + '"\n',
        'CANONICAL_COMPLETE_JSON_FILENAME = "project__complete.json"\n'
        'LOCAL_AI_COMPLETE_JSON_FILENAME = "project__complete_local_AI.json"\n',
    )

    legacy_split_manifest = legacy_project_name + "_split_manifest.json"
    legacy_split_index = legacy_project_name + "_split_index.json"
    legacy_route = legacy_project_name + "__complete__web_ai_route_manifest.json"
    source = source.replace(
        'GENERATED_ARTIFACT_SPLIT_MANIFEST_NAME = "' + legacy_split_manifest + '"\n'
        'GENERATED_ARTIFACT_SPLIT_INDEX_NAME = "' + legacy_split_index + '"\n'
        'GENERATED_ARTIFACT_ROUTE_MANIFEST_NAME = (\n'
        '    "' + legacy_route + '"\n'
        ')\n',
        'GENERATED_ARTIFACT_SPLIT_MANIFEST_NAME = "project_split_manifest.json"\n'
        'GENERATED_ARTIFACT_SPLIT_INDEX_NAME = "project_split_index.json"\n'
        'GENERATED_ARTIFACT_ROUTE_MANIFEST_NAME = (\n'
        '    "project__complete__web_ai_route_manifest.json"\n'
        ')\n',
    )

    legacy_suffix_block = (
        'BUNDLE_SAFETY_GENERATED_ARTIFACT_SUFFIXES = (\n'
        '    "' + evidence_root_text + '/json_complete/' + legacy_complete + '",\n'
        '    "' + evidence_root_text + '/json_complete/' + legacy_local + '",\n'
        '    "' + evidence_root_text + '/json_splitted/' + legacy_split_manifest + '",\n'
        '    "' + evidence_root_text + '/json_splitted/' + legacy_split_index + '",\n'
        '    "' + evidence_root_text + '/json_splitted/' + legacy_route + '",\n'
        '    ".chunk.json",\n'
        ')\n'
    )
    source = source.replace(
        legacy_suffix_block,
        'BUNDLE_SAFETY_GENERATED_ARTIFACT_SUFFIXES = (\n'
        '    "project_analysis_evidence/json_complete/",\n'
        '    "project_analysis_evidence/json_splitted/",\n'
        '    ".chunk.json",\n'
        ')\n',
    )

    source = source.replace(
        '    "tests", "test",\n}\n\nDEFAULT_EXCLUDE_DIR_PATTERNS',
        '    "tests", "test",\n    ".project_reference",\n    "_project_reference",\n}\n\nDEFAULT_EXCLUDE_DIR_PATTERNS',
    )
    source = source.replace(
        '    "dev_tools_docs",\n    "_project_reference",\n',
        '    "dev_tools_docs",\n    ".project_reference",\n    "_project_reference",\n',
    )
    source = source.replace(
        '    for zip_path in zip_paths:\n'
        '        rel = _artifact_issue_path(root, zip_path)\n',
        '    ignore_folders, _, _ = load_ignore_rules(root)\n'
        '    zip_paths = [\n'
        '        zip_path for zip_path in zip_paths\n'
        '        if not _path_has_ignored_folder(zip_path.parent, root, ignore_folders)\n'
        '    ]\n\n'
        '    for zip_path in zip_paths:\n'
        '        rel = _artifact_issue_path(root, zip_path)\n',
    )
    source = source.replace(
        '    canonical_path = json_complete_dir / CANONICAL_COMPLETE_JSON_FILENAME\n'
        '    local_ai_path = json_complete_dir / LOCAL_AI_COMPLETE_JSON_FILENAME\n',
        '    artifact_project_name = root.name.strip() or "project"\n'
        '    canonical_path = json_complete_dir / f"{artifact_project_name}__complete.json"\n'
        '    local_ai_path = json_complete_dir / f"{artifact_project_name}__complete_local_AI.json"\n',
    )
    source = source.replace(
        '    manifest_path = split_dir / GENERATED_ARTIFACT_SPLIT_MANIFEST_NAME\n'
        '    index_path = split_dir / GENERATED_ARTIFACT_SPLIT_INDEX_NAME\n'
        '    route_path = split_dir / GENERATED_ARTIFACT_ROUTE_MANIFEST_NAME\n',
        '    artifact_project_name = root.name.strip() or "project"\n'
        '    split_manifest_name = f"{artifact_project_name}_split_manifest.json"\n'
        '    split_index_name = f"{artifact_project_name}_split_index.json"\n'
        '    route_manifest_name = f"{artifact_project_name}__complete__web_ai_route_manifest.json"\n'
        '    manifest_path = split_dir / split_manifest_name\n'
        '    index_path = split_dir / split_index_name\n'
        '    route_path = split_dir / route_manifest_name\n',
    )
    source = source.replace(
        '                    f"is missing {GENERATED_ARTIFACT_SPLIT_MANIFEST_NAME}. "\n',
        '                    f"is missing {split_manifest_name}. "\n',
    )
    source = source.replace(
        '                    f"Split manifest exists but {GENERATED_ARTIFACT_SPLIT_INDEX_NAME} "\n',
        '                    f"Split manifest exists but {split_index_name} "\n',
    )
    source = source.replace(
        '                    f"Split manifest exists but {GENERATED_ARTIFACT_ROUTE_MANIFEST_NAME} "\n',
        '                    f"Split manifest exists but {route_manifest_name} "\n',
    )
    return source


def _apply_dynamic_root_cli_policy(source: str) -> str:
    """Make the architecture CLI root help prefer dynamic roots over stale history."""
    source = _replace_once(
        source,
        'def get_history_roots() -> list[str]:\n'
        '    return _load_history()["roots"]\n\n\n',
        'def get_history_roots() -> list[str]:\n'
        '    return _load_history()["roots"]\n\n\n'
        'def _existing_history_roots() -> list[str]:\n'
        '    """Return remembered project roots that still exist on disk."""\n'
        '    existing_roots: list[str] = []\n'
        '    for root_text in get_history_roots():\n'
        '        try:\n'
        '            root = Path(root_text).expanduser().resolve()\n'
        '        except Exception:\n'
        '            continue\n'
        '        if root.exists():\n'
        '            existing_roots.append(str(root))\n'
        '    return existing_roots\n\n\n'
        'def _project_root_from_environment() -> str | None:\n'
        '    """Return the first existing project root from supported environment names."""\n'
        '    env_names = (\n'
        '        "kanda_reasoner_project_root",\n'
        '        "PROJECT_ROOT",\n'
        '        "KANDA_REASONER_PROJECT_ROOT",\n'
        '        "KANDA_RUNTIME_PROJECT_ROOT",\n'
        '        "PROJECT_REASONER_PROJECT_ROOT",\n'
        '        "PROJECT_REASONER_SCAN_ROOT",\n'
        '        "KANDA_REASONER_SCAN_ROOT",\n'
        '    )\n'
        '    for env_name in env_names:\n'
        '        root_text = os.environ.get(env_name, "").strip()\n'
        '        if not root_text:\n'
        '            continue\n'
        '        try:\n'
        '            root = Path(root_text).expanduser().resolve()\n'
        '        except Exception:\n'
        '            continue\n'
        '        if root.exists():\n'
        '            return str(root)\n'
        '    return None\n\n\n'
        'def _source_tree_root_from_this_file() -> str | None:\n'
        '    """Return the source-tree root that contains this CLI module, if detectable."""\n'
        '    try:\n'
        '        root = Path(__file__).resolve().parents[2]\n'
        '    except Exception:\n'
        '        return None\n'
        '    source_package_dir = "ask" + "_ai" + "_project" + "_reasoner"\n'
        '    if (root / source_package_dir).exists():\n'
        '        return str(root)\n'
        '    return None\n\n\n'
        'def _select_default_root_for_help() -> str:\n'
        '    """Select the root displayed by --help without reviving stale old paths."""\n'
        '    env_root = _project_root_from_environment()\n'
        '    if env_root is not None:\n'
        '        return env_root\n\n'
        '    existing_roots = _existing_history_roots()\n'
        '    if existing_roots:\n'
        '        return existing_roots[0]\n\n'
        '    source_root = _source_tree_root_from_this_file()\n'
        '    if source_root is not None:\n'
        '        return source_root\n\n'
        '    return r"."\n\n\n',
    )
    source = _replace_once(
        source,
        '    # Resolve the default root: prefer the most recently used root from history,\n'
        '    # then fall back to the hard-coded path.\n'
        '    history_roots = get_history_roots()\n'
        '    default_root = history_roots[0] if history_roots else r"."\n',
        '    # Resolve the displayed/default root dynamically. Prefer an explicit\n'
        '    # environment root, then existing remembered roots, then this source tree.\n'
        '    default_root = _select_default_root_for_help()\n',
    )
    source = _replace_once(
        source,
        '            f"Project root path (default: last used root or hard-coded fallback).\\n"\n'
        '            f"Currently defaults to: {default_root}"\n',
        '            f"Project root path (default: environment root, existing history, or source tree).\\n"\n'
        '            f"Currently defaults to: {default_root}"\n',
    )
    source = _replace_once(
        source,
        '        history_roots = get_history_roots()\n'
        '        idx = args.use_root - 1\n',
        '        history_roots = _existing_history_roots()\n'
        '        idx = args.use_root - 1\n',
    )
    return source



def load_manage_architecture_source() -> str:
    """Return the original manage_architecture implementation source."""
    encoded_source = "".join([
        MANAGE_ARCHITECTURE_SOURCE_PART_1,
        MANAGE_ARCHITECTURE_SOURCE_PART_2,
        MANAGE_ARCHITECTURE_SOURCE_PART_3,
        MANAGE_ARCHITECTURE_SOURCE_PART_4,
        MANAGE_ARCHITECTURE_SOURCE_PART_5,
        MANAGE_ARCHITECTURE_SOURCE_PART_6,
        MANAGE_ARCHITECTURE_SOURCE_PART_7,
        MANAGE_ARCHITECTURE_SOURCE_PART_8,
        MANAGE_ARCHITECTURE_SOURCE_PART_9,
        MANAGE_ARCHITECTURE_SOURCE_PART_10,
        MANAGE_ARCHITECTURE_SOURCE_PART_11,
        MANAGE_ARCHITECTURE_SOURCE_PART_12,
        MANAGE_ARCHITECTURE_SOURCE_PART_13,
        MANAGE_ARCHITECTURE_SOURCE_PART_14,
        MANAGE_ARCHITECTURE_SOURCE_PART_15,
        MANAGE_ARCHITECTURE_SOURCE_PART_16,
        MANAGE_ARCHITECTURE_SOURCE_PART_17,
        MANAGE_ARCHITECTURE_SOURCE_PART_18,
        MANAGE_ARCHITECTURE_SOURCE_PART_19,
        MANAGE_ARCHITECTURE_SOURCE_PART_20,
        MANAGE_ARCHITECTURE_SOURCE_PART_21,
    ])
    source = base64.b64decode(encoded_source.encode("ascii")).decode("utf-8")
    source = _apply_ad001_architecture_delivery_policy(source)
    source = _apply_project_analysis_evidence_path_policy(source)
    source = _apply_dynamic_root_cli_policy(source)
    source = apply_manage_architecture_warning_policies(source)
    return _apply_tab8_project_exclusion_policy(source)


__all__ = ["load_manage_architecture_source"]
