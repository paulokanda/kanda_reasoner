"""Validate the Local AI symbol-shadowing correction for wave 2C."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-local-ai-symbol-shadowing-wave2c-v1"
TARGET = Path("kanda_reasoner_app/local_ai_configuration.py")
CONFIG_AI_GLOBAL_VALIDATOR = Path(
    "tools/validate_config_ai_global_local_v1.py"
)
CONFIG_WEB_AI_TAB = Path(
    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py"
)
EXPECTED_CONFIG_WEB_AI_TAB_SHA256 = (
    "882956d59d3cc6de1090c6447ba43c7c603ec07124d8ec26d22edec97fcd4843"
)
EXPECTED_CONFIG_AI_SUBTAB_LABELS = (
    "Config Web AI",
    "Direct API Providers",
    "Config Local AI",
)
EXPECTED_LOCAL_AI_CONFIGURATION_SHA256 = (
    "9f66737307b4c59f018dcf0e9d02b1313478db1bb022abc06ac40cbcf7030d67"
)
OBSOLETE_LOCAL_AI_CONFIGURATION_SHA256 = (
    "d0bbca141d2f374754fc8bbe1e72daca4472ee06d68904d44703e2ca57b4aa59"
)
LOCAL_AI_HASH_PIN_VALIDATORS = (
    Path("tools/validate_integrated_free_api_web_ai_v1.py"),
    Path("tools/validate_project_web_ai_smart_complete_json_context_v1.py"),
)

PORTABLE_MANIFESTS = (
    Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json"),
    Path("portable/PORTABLE_BUILDER_MANIFEST.json"),
    Path("portable/PORTABLE_EXTERNAL_BUILD_CONTROLS.json"),
)


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error when condition is false."""
    if not condition:
        raise RuntimeError(code)


def read_source(root: Path, relative: Path) -> str:
    """Read one governed source file as strict UTF-8."""
    return (root / relative).read_text(encoding="utf-8-sig")


def class_node(tree: ast.Module, name: str) -> ast.ClassDef:
    """Return one top-level class by exact name."""
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise RuntimeError("CLASS_NOT_FOUND:" + name)


def method_node(owner: ast.ClassDef, name: str) -> ast.FunctionDef:
    """Return one class method by exact name."""
    for node in owner.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError("METHOD_NOT_FOUND:" + name)


def imported_aliases(tree: ast.Module) -> dict[str, str]:
    """Return imported source-name to alias-name bindings."""
    bindings: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module != "kanda_reasoner_app.local_ai_runtime_state":
            continue
        for alias in node.names:
            bindings[alias.name] = alias.asname or alias.name
    return bindings


def module_string_constant(tree: ast.Module, name: str) -> str:
    """Return one exact top-level string constant."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id != name:
            continue
        if not isinstance(node.value, ast.Constant):
            break
        if not isinstance(node.value.value, str):
            break
        return node.value.value
    raise RuntimeError("MODULE_STRING_CONSTANT_NOT_FOUND:" + name)


def module_string_tuple_constant(
    tree: ast.Module,
    name: str,
) -> tuple[str, ...]:
    """Return one exact top-level tuple of string constants."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id != name:
            continue
        if not isinstance(node.value, ast.Tuple):
            break
        values: list[str] = []
        for item in node.value.elts:
            if not isinstance(item, ast.Constant):
                break
            if not isinstance(item.value, str):
                break
            values.append(item.value)
        else:
            return tuple(values)
        break
    raise RuntimeError("MODULE_STRING_TUPLE_CONSTANT_NOT_FOUND:" + name)


def module_literal_dict_constant(
    tree: ast.Module,
    name: str,
) -> dict[str, object]:
    """Return one exact top-level literal dictionary."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id != name:
            continue
        value = ast.literal_eval(node.value)
        if not isinstance(value, dict):
            break
        return {
            str(key): item
            for key, item in value.items()
        }
    raise RuntimeError("MODULE_LITERAL_DICT_CONSTANT_NOT_FOUND:" + name)


def validate_inherited_source_baseline(root: Path) -> None:
    """Require inherited validator pins and UI contracts to be current."""
    web_tab = root / CONFIG_WEB_AI_TAB
    actual_hash = hashlib.sha256(web_tab.read_bytes()).hexdigest()
    require(
        actual_hash == EXPECTED_CONFIG_WEB_AI_TAB_SHA256,
        "CONFIG_WEB_AI_SOURCE_HASH_CHANGED",
    )

    validator_source = read_source(root, CONFIG_AI_GLOBAL_VALIDATOR)
    validator_tree = ast.parse(
        validator_source,
        filename=str(root / CONFIG_AI_GLOBAL_VALIDATOR),
    )
    pinned_hash = module_string_constant(
        validator_tree,
        "WEB_TAB_SHA256",
    )
    require(
        pinned_hash == actual_hash,
        "CONFIG_AI_GLOBAL_VALIDATOR_BASELINE_STALE",
    )

    subtab_labels = module_string_tuple_constant(
        validator_tree,
        "CONFIG_AI_SUBTAB_LABELS",
    )
    require(
        subtab_labels == EXPECTED_CONFIG_AI_SUBTAB_LABELS,
        "CONFIG_AI_GLOBAL_VALIDATOR_SUBTAB_CONTRACT_STALE",
    )

    required_contract_tokens = (
        "ConfigDirectWebAITab",
        'addTab(self.direct_web_ai_tab, "Direct API Providers")',
        "composite.direct_web_ai_tab.__class__.__name__",
        "labels != CONFIG_AI_SUBTAB_LABELS",
    )
    for token in required_contract_tokens:
        require(
            token in validator_source,
            "CONFIG_AI_GLOBAL_VALIDATOR_SEMANTIC_CONTRACT_MISSING:"
            + token,
        )

    print("CONFIG WEB AI SOURCE HASH: PASS")
    print("CONFIG AI GLOBAL VALIDATOR BASELINE CURRENT: PASS")
    print("CONFIG AI THREE-SUBTAB CONTRACT CURRENT: PASS")

    local_ai_path = root / TARGET
    local_ai_hash = hashlib.sha256(local_ai_path.read_bytes()).hexdigest()
    require(
        local_ai_hash == EXPECTED_LOCAL_AI_CONFIGURATION_SHA256,
        "LOCAL_AI_CONFIGURATION_SOURCE_HASH_CHANGED",
    )

    for relative in LOCAL_AI_HASH_PIN_VALIDATORS:
        source = read_source(root, relative)
        tree = ast.parse(source, filename=str(root / relative))
        protected = module_literal_dict_constant(
            tree,
            "PROTECTED_HASHES",
        )
        require(
            protected.get(TARGET.as_posix()) == local_ai_hash,
            "LOCAL_AI_PROTECTED_HASH_PIN_STALE:"
            + relative.as_posix(),
        )

    stale_pin_owners: list[str] = []
    current_validator = Path(__file__).resolve()
    for search_root in (root / "tools", root / "scripts"):
        for path in search_root.rglob("*.py"):
            if path.resolve() == current_validator:
                continue
            source = path.read_text(encoding="utf-8-sig")
            if OBSOLETE_LOCAL_AI_CONFIGURATION_SHA256 in source:
                stale_pin_owners.append(
                    path.relative_to(root).as_posix()
                )
    require(
        not stale_pin_owners,
        "OBSOLETE_LOCAL_AI_HASH_PIN_REMAINS:"
        + ",".join(stale_pin_owners),
    )

    print("LOCAL AI PROTECTED HASH PIN OWNERS CURRENT: PASS")
    print("OBSOLETE LOCAL AI HASH PINS ABSENT: PASS")


def validate_static_contract(root: Path) -> None:
    """Require distinct imported and method names with preserved behavior."""
    source = read_source(root, TARGET)
    tree = ast.parse(source, filename=str(root / TARGET))
    aliases = imported_aliases(tree)

    require(
        aliases.get("publish_runtime_local_ai_configuration_snapshot")
        == "_publish_runtime_configuration_snapshot",
        "LOCAL_AI_RUNTIME_PUBLISHER_ALIAS_INVALID",
    )
    require(
        "_publish_runtime_snapshot" not in aliases.values(),
        "LOCAL_AI_RUNTIME_PUBLISHER_STILL_SHADOWS_METHOD",
    )

    owner = class_node(tree, "LocalAIConfigurationController")
    method = method_node(owner, "_publish_runtime_snapshot")

    calls = [
        node
        for node in ast.walk(method)
        if isinstance(node, ast.Call)
    ]
    require(
        len(calls) == 2,
        "LOCAL_AI_RUNTIME_PUBLISH_METHOD_CALL_COUNT_INVALID",
    )

    publisher_calls = [
        call
        for call in calls
        if isinstance(call.func, ast.Name)
        and call.func.id == "_publish_runtime_configuration_snapshot"
    ]
    require(
        len(publisher_calls) == 1,
        "LOCAL_AI_RUNTIME_PUBLISHER_CALL_MISSING",
    )

    snapshot_calls = [
        call
        for call in calls
        if isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "self"
        and call.func.attr == "snapshot"
    ]
    require(
        len(snapshot_calls) == 1,
        "LOCAL_AI_RUNTIME_SNAPSHOT_CALL_MISSING",
    )

    source_calls = source.count("self._publish_runtime_snapshot()")
    require(
        source_calls >= 2,
        "LOCAL_AI_CONTROLLER_PUBLISH_METHOD_CALLS_NOT_PRESERVED",
    )

    require(
        len(source.splitlines()) <= 500,
        "LOCAL_AI_CONFIGURATION_EXCEEDS_500_LINES",
    )

    current_validator = Path(__file__).resolve()
    require(
        len(
            current_validator.read_text(encoding="utf-8-sig").splitlines()
        )
        <= 500,
        "WAVE2C_VALIDATOR_EXCEEDS_500_LINES",
    )

    print("LOCAL AI RUNTIME PUBLISHER DISTINCT ALIAS: PASS")
    print("LOCAL AI CONTROLLER METHOD NAME PRESERVED: PASS")
    print("LOCAL AI RUNTIME SNAPSHOT PUBLICATION CALL: PASS")
    print("WAVE2C PYTHON COMPILE AND SIZE: PASS")


def validate_portable_non_membership(root: Path) -> None:
    """Prove this source file is not governed by Portable manifests."""
    target_text = TARGET.as_posix()
    validator_text = Path(__file__).resolve().relative_to(root).as_posix()
    for relative in PORTABLE_MANIFESTS:
        content = read_source(root, relative)
        require(
            target_text not in content,
            "TARGET_UNEXPECTEDLY_IN_PORTABLE_MANIFEST:"
            + relative.as_posix(),
        )
        require(
            validator_text not in content,
            "VALIDATOR_UNEXPECTEDLY_IN_PORTABLE_MANIFEST:"
            + relative.as_posix(),
        )

    print("PORTABLE RUNTIME ALLOWLIST MODIFIED: NO")
    print("PORTABLE BUILDER MANIFEST MODIFIED: NO")
    print("PORTABLE EXTERNAL BUILD CONTROLS MODIFIED: NO")


def run_command(
    root: Path,
    command: list[str],
    marker: str,
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one owned command and require its exact success marker."""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(root)

    completed = subprocess.run(
        command,
        cwd=str(root),
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, code + "_NONZERO_EXIT")
    require(marker in output, code + "_MARKER_MISSING")
    return output


def validate_live_architecture(root: Path) -> None:
    """Require zero errors and absence of the one target warning."""
    output = run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "kanda_reasoner_app"
                / "manage_architecture"
                / "manage_architecture.py"
            ),
            "--root",
            str(root),
            "--validate",
        ],
        "ARCHITECTURE VALIDATION SUMMARY",
        "ARCHITECTURE_VALIDATION",
    )

    require(
        "Errors: 0" in output,
        "ARCHITECTURE_ERRORS_REMAIN",
    )

    target_warning = (
        "WARNING SYMBOL_SHADOWING             "
        "kanda_reasoner_app/local_ai_configuration.py"
    )
    require(
        target_warning not in output,
        "LOCAL_AI_SYMBOL_SHADOWING_WARNING_REMAINS",
    )

    print("WAVE2C TARGET SYMBOL SHADOWING ABSENT: PASS")


def validate_inherited_contracts(root: Path) -> None:
    """Run the main Local AI owner and call-site validators."""
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools" / "validate_config_ai_global_local_v1.py"),
            str(root),
        ],
        "VALIDATION OK: config-ai-global-local-controller-v1r2",
        "CONFIG_AI_GLOBAL_LOCAL_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools" / "validate_config_web_ai_central_v1.py"),
            "--root",
            str(root),
            "--static-only",
        ],
        "VALIDATION OK: config-web-ai-central-v1r2",
        "CONFIG_WEB_AI_CENTRAL_STATIC_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "tools"
                / "validate_ai_global_consumer_callsite_audit_v1.py"
            ),
            "--root",
            str(root),
        ],
        "VALIDATION OK: ai-global-consumer-callsite-audit-v1r1",
        "AI_GLOBAL_CONSUMER_CALLSITE_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "tools"
                / "validate_local_ai_redundant_model_projection_removal_v1.py"
            ),
            "--root",
            str(root),
        ],
        "VALIDATION OK: local-ai-redundant-model-projection-removal-v1",
        "LOCAL_AI_REDUNDANT_PROJECTION_VALIDATOR",
    )


def main() -> int:
    """Run static and live validation for wave 2C."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_static_contract(root)
    validate_inherited_source_baseline(root)
    validate_portable_non_membership(root)

    if not args.static_only:
        validate_live_architecture(root)
        validate_inherited_contracts(root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
