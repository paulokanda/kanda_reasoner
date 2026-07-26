# project-path: tools/validate_brick_wall_q30_human_confirmation_freeze_protection_v1.py
"""Focused Q30 human-confirmation and freeze-protection validation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

from brick_wall_q30_human_confirmation_freeze_protection_contract import (
    mutated_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRICK_META = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRIDGE_META = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
MANIFEST = Path("kanda_reasoner_app/freeze_after_update/box_manifest.json")
CONTRACT = Path("kanda_reasoner_app/freeze_after_update/contract.py")
TAB = Path("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")
BINDING = Path("kanda_reasoner_app/freeze_after_update_gui/local_freeze_confirmation_binding.py")
Q29 = Path("tools/validate_brick_wall_q29_no_leak_runtime_trace_pilot_decision_v1.py")
SELF = Path("tools/validate_brick_wall_q30_human_confirmation_freeze_protection_v1.py")
REAL_QT = Path("tools/validate_brick_wall_q30_human_confirmation_freeze_protection_real_qt_v1.py")
FEATURE = "brick-wall-q30-human-confirmation-freeze-protection-enforcement-v1"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load " + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    brick_meta = json.loads(_read(root / BRICK_META))
    bridge_meta = json.loads(_read(root / BRIDGE_META))
    manifest = json.loads(_read(root / MANIFEST))
    contract = _read(root / CONTRACT)
    tab = _read(root / TAB)
    binding = _read(root / BINDING)
    q29 = _read(root / Q29)
    required_brick = (
        "Human confirmation and freeze protection (Q30)",
        "HUMAN CONFIRMATION AND FREEZE PROTECTION RECORD",
        "read-only Preview",
        "explicit Confirm and Write",
        "proceed Q31",
        "may begin coding NO",
        "may write source NO",
    )
    for marker in required_brick:
        _gate("Q30_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Human confirmation and freeze protection gate (Q30)",
        "exact reviewed-form and selected-project binding",
        "no automatic Error Memory promotion or frozen-memory write",
        "May proceed to Q31",
    ):
        _gate("Q30_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate("Q30_BRICK_VERSION", tuple(map(int, brick_meta["version"].split("."))) >= (3, 12))
    _gate("Q30_BRIDGE_VERSION", tuple(map(int, bridge_meta["version"].split("."))) >= (4, 6))
    _gate("Q30_BRICK_HEADER_METADATA_VERSION_ALIGNMENT", f"version: {brick_meta['version']}" in brick)
    _gate("Q30_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT", f"version: {bridge_meta['version']}" in bridge)
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        source_stage = str(meta.get("source_stage", "")).strip()
        updated_for = str(meta.get("updated_for", "")).strip()
        _gate(
            "Q30_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
    _gate(
        "Q30_FORWARD_COMPATIBLE_Q31_PROGRESSION",
        "CHANGED-FILE-TO-VALIDATOR COVERAGE MAP" in brick
        and "Changed-file-to-validator coverage bridge (Q31)" in bridge,
    )
    _gate("Q30_Q29_FROZEN_BASELINE_PRESENT", "Q29_FORWARD_COMPATIBLE_Q30_PROGRESSION" in q29)
    protection = manifest.get("confirmation_protection") or {}
    _gate("Q30_BOX_OWNER_REUSED", manifest.get("box_id") == "freeze_feature_after_update")
    _gate("Q30_BOX_CONTRACT_VERSION", manifest.get("contract_version") == "1.5.0")
    _gate("Q30_PREVIEW_READ_ONLY_MANIFEST", protection.get("preview") == "read_only")
    _gate("Q30_NO_AUTOMATIC_FREEZE_WRITE", protection.get("automatic_freeze_write") is False)
    _gate("Q30_NO_AUTOMATIC_ERROR_MEMORY_PROMOTION", protection.get("automatic_error_memory_promotion") is False)
    _gate("Q30_PUBLIC_CONFIRMATION_CHECK", "confirmation is not True" in contract)
    _gate("Q30_PUBLIC_ROOT_BINDING_CHECK", "_preview_root_binding_error" in contract)
    _gate("Q30_GUI_EXACT_FORM_BINDING", "build_freeze_confirmation_binding" in tab and "freeze_confirmation_binding_matches" in tab)
    _gate("Q30_GUI_CHANGE_INVALIDATION", "bind_freeze_confirmation_invalidation" in tab and "invalidate_current_confirmation" in tab)
    _gate("Q30_GUI_EXPLICIT_CONFIRMED_WRITE", "write_confirmed_freeze_entry(project_root, preview, confirmation=True)" in tab)
    _gate("Q30_GUI_READ_ONLY_PREVIEW", "preview_text_edit" in tab and "setReadOnly(True)" in _read(root / Path("kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py")))
    _gate("Q30_BINDING_FIELD_INVENTORY", all(name in binding for name in ("validation_evidence_summary", "protected_paths", "planned_next_step", "project_root_edit")))
    for rel in (BRICK, BRIDGE, CONTRACT, TAB, BINDING, Q29, SELF, REAL_QT):
        _gate("Q30_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, str(rel))


def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_record_contract() -> None:
    validate_record(valid_complete_record())
    _gate("Q30_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q30_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q30_NEGATIVE_Q29_BASELINE", lambda r: r.update(q29_decision_complete=False)),
        ("Q30_NEGATIVE_PREVIEW_WRITABLE", lambda r: r.update(preview_read_only=False)),
        ("Q30_NEGATIVE_IMPLICIT_CONFIRMATION", lambda r: r.update(explicit_confirm_and_write=False)),
        ("Q30_NEGATIVE_FORM_BINDING", lambda r: r.update(exact_form_binding=False)),
        ("Q30_NEGATIVE_PROJECT_BINDING", lambda r: r.update(selected_project_binding=False)),
        ("Q30_NEGATIVE_FORM_CHANGE", lambda r: r.update(form_change_invalidates=False)),
        ("Q30_NEGATIVE_SOURCE_EVIDENCE_CHANGE", lambda r: r.update(source_evidence_change_invalidates=False)),
        ("Q30_NEGATIVE_TARGET_CHANGE", lambda r: r.update(target_change_invalidates=False)),
        ("Q30_NEGATIVE_PROJECT_ROOT_CHANGE", lambda r: r.update(project_root_change_invalidates=False)),
        ("Q30_NEGATIVE_PUBLIC_CONFIRMATION_CHECK", lambda r: r.update(public_contract_confirmation_check=False)),
        ("Q30_NEGATIVE_PUBLIC_ROOT_CHECK", lambda r: r.update(public_contract_root_binding_check=False)),
        ("Q30_NEGATIVE_AUTO_ERROR_MEMORY", lambda r: r.update(automatic_error_memory_promotion=True)),
        ("Q30_NEGATIVE_AUTO_FREEZE_WRITE", lambda r: r.update(automatic_freeze_memory_write=True)),
        ("Q30_NEGATIVE_Q31_PROGRESSION", lambda r: r.update(may_proceed_to_q31=False)),
        ("Q30_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q30_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_protection_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q30_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q30_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q30_HUMAN_CONFIRMATION_FREEZE_PROTECTION_REGRESSION_SET: PASS")


class Signal:
    def __init__(self): self.callbacks=[]
    def connect(self, callback): self.callbacks.append(callback)
    def emit(self):
        for callback in tuple(self.callbacks): callback()


class Editor:
    def __init__(self, text=""):
        self.value=text; self.textChanged=Signal()
    def text(self): return self.value
    def toPlainText(self): return self.value
    def setText(self, value): self.value=str(value); self.textChanged.emit()
    def setPlainText(self, value): self.value=str(value); self.textChanged.emit()


class Button:
    def __init__(self): self.enabled=None; self.style=""; self.tip=""
    def setEnabled(self, value): self.enabled=bool(value)
    def setStyleSheet(self, value): self.style=value
    def setToolTip(self, value): self.tip=value


def validate_binding_runtime(root: Path) -> None:
    module = _load_module(root / BINDING, "q30_binding")
    names=("feature_title","primary_box","box_type","validated_files","generated_files","protected_paths","do_not_regress","validation_evidence","known_warnings","planned_next_step","notes")
    widgets=SimpleNamespace(**{name+"_edit":Editor(name) for name in names})
    project=Editor(str(root))
    inputs=module.collect_freeze_form_inputs(widgets)
    binding=module.build_freeze_confirmation_binding(project.text(), inputs)
    ok, reason=module.freeze_confirmation_binding_matches(binding, project.text(), inputs)
    _gate("Q30_EXACT_FORM_PROJECT_BINDING", ok, reason)
    changed=dict(inputs); changed["validation_evidence_summary"] += " changed"
    _gate("Q30_SOURCE_EVIDENCE_CHANGE_REJECTED", not module.freeze_confirmation_binding_matches(binding, project.text(), changed)[0])
    changed=dict(inputs); changed["protected_paths"] += " changed"
    _gate("Q30_TARGET_CHANGE_REJECTED", not module.freeze_confirmation_binding_matches(binding, project.text(), changed)[0])
    _gate("Q30_PROJECT_ROOT_CHANGE_REJECTED", not module.freeze_confirmation_binding_matches(binding, root / "other", inputs)[0])
    calls=[]
    count=module.bind_freeze_confirmation_invalidation(widgets, project, lambda *args: calls.append("invalidated"))
    widgets.feature_title_edit.setText("new")
    widgets.validation_evidence_edit.setPlainText("new evidence")
    project.setText(str(root / "new-project"))
    _gate("Q30_ALL_REVIEWED_INPUTS_BOUND", count == 12)
    _gate("Q30_SIGNAL_INVALIDATION_RUNTIME", len(calls) == 3)
    confirm=Button(); ignore=Button()
    state=module.FreezeActionStateController(confirm_button=confirm,ignore_button=ignore,confirm_enabled_style="on",ignore_enabled_style="ignore",disabled_style="off")
    state.set_state(True, True)
    _gate("Q30_CONFIRM_BUTTON_ENABLED_ONLY_BY_VALID_STATE", confirm.enabled is True and ignore.enabled is True)
    state.disable("stale")
    _gate("Q30_STALE_CONFIRMATION_DISABLED", confirm.enabled is False and ignore.enabled is False and "stale" in confirm.tip)
    print("Q30_RUNTIME_CONFIRMATION_BINDING: PASS")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args=parser.parse_args()
    root=args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_record_contract()
    validate_binding_runtime(root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
