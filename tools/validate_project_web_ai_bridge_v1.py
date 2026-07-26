# project-path: tools/validate_project_web_ai_bridge_v1.py
"""Focused validation for the Project Web AI bridge and shared provider runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

FEATURE_ID = "project-web-ai-bridge-v1"
TOUCHED_CODE = (
    "kanda_reasoner_app/project_support_boundary.py",
    "kanda_reasoner_app/reasoner_context_bundle/schema_models.py",
    "kanda_reasoner_app/reasoner_context_bundle/project_context.py",
    "kanda_reasoner_app/reasoner_context_bundle/ai_briefing_builder.py",
    "kanda_reasoner_app/reasoner_context_bundle/bundle_manifest_builder.py",
    "kanda_reasoner_app/web_ai_provider_contracts.py",
    "kanda_reasoner_app/web_ai_provider_runtime.py",
    "kanda_reasoner_app/web_ai_model_catalog.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_handoff_reader.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/ai_openai_compatible_provider_runtime.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    "tools/validate_project_web_ai_bridge_v1.py",
)

def _sha256(path: Path) -> str:
    """Return the SHA-256 of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def _fixture_members(project_identity) -> dict[str, bytes]:
    """Return a minimal valid handoff package for bridge validation."""
    project_slug = project_identity.active_project_slug
    project = {
        "project_slug": project_identity.active_project_slug,
        "project_root_marker": "<PROJECT_ROOT>",
        "active_project_id": project_identity.active_project_id,
        "active_project_root_fingerprint": (
            project_identity.active_project_root_fingerprint
        ),
    }
    payloads: dict[str, object] = {
        f"{project_slug}__ai_briefing.json": {
            "bundle_kind": "ai_briefing",
            "generated_at_utc": "2026-07-19T12:00:00Z",
            "project": project,
            "source_truth_policy": {
                "source_files_are_truth": True,
                "inspect_exact_source_before_editing": True,
            },
        },
        f"{project_slug}__routing_manifest.json": {
            "bundle_kind": "routing_manifest",
            "project": project,
            "task_routes": {"general_project_understanding": {"description": "demo"}},
        },
        f"{project_slug}__bundle_manifest.json": {
            "bundle_kind": "bundle_manifest",
            "project": project,
            "artifacts": [],
        },
        f"{project_slug}__patch_safety_routes.json": {
            "bundle_kind": "patch_safety_routes",
            "project": project,
            "subsystems": {"gui_shell": {"risk_level": "standard"}},
        },
        f"{project_slug}__validation_state.json": {
            "bundle_kind": "validation_state",
            "project": project,
            "overall": {"status": "not_run"},
        },
        f"{project_slug}__error_lessons_compact.json": {
            "artifact_type": "error_memory_ai_export",
            "derived_from": {"project_slug": project_slug},
            "lessons": [
                {
                    "lesson_id": "lesson-demo",
                    "status": "active",
                    "do_not_repeat_rule": "Do not mutate source during advisory review.",
                    "correct_fix": "Keep the bridge read-only.",
                }
            ],
        },
        f"{project_slug}__error_memory_manifest.json": {
            "artifact_type": "error_memory_manifest",
            "project_slug": project_slug,
            "included_lesson_ids": ["lesson-demo"],
        },
        f"{project_slug}__file_manifest.json": {
            "bundle_kind": "file_manifest",
            "project": project,
            "counts": {"active_files": 4, "text_files": 4},
            "files": [{"path": "secret/source.py", "content": "must not be forwarded"}],
        },
        f"{project_slug}__source_archive_manifest.json": {
            "bundle_kind": "source_archive_manifest",
            "project": project,
            "counts": {"archive_parts": 1, "included_files": 4},
            "included_files": ["secret/source.py"],
        },
    }
    members = {
        "UPLOAD_README.txt": b"Read AI briefing first.",
        f"{project_slug}__error_memory_ai_prompt.md": b"Error Memory is prevention evidence.",
    }
    for name, payload in payloads.items():
        members[name] = json.dumps(payload).encode("utf-8")
    return members


def _rewrite_member_name_in_zip_headers(
    archive_path: Path,
    safe_member: str,
    unsafe_member: str,
) -> int:
    """Rewrite local and central-directory names without writer normalization."""
    safe_bytes = safe_member.encode("utf-8")
    unsafe_bytes = unsafe_member.encode("utf-8")
    _assert(len(safe_bytes) == len(unsafe_bytes), "raw ZIP fixture name lengths differ")
    payload = archive_path.read_bytes()
    replacement_count = payload.count(safe_bytes)
    _assert(replacement_count == 2, f"expected two ZIP header names, found {replacement_count}")
    archive_path.write_bytes(payload.replace(safe_bytes, unsafe_bytes))
    return replacement_count


def _build_fixture(
    base: Path,
    *,
    unsafe_member: str = "",
) -> tuple[Path, Path, Path, int]:
    """Create one isolated selected-Project handoff fixture."""
    from kanda_reasoner_app.project_support_boundary import (
        resolve_project_tool_boundary_identity,
    )

    project_slug = base.name + "_project"
    project = base / project_slug
    project.mkdir(parents=True, exist_ok=False)
    identity = resolve_project_tool_boundary_identity(project)
    support_root = identity.active_project_support_root
    if support_root.exists() or support_root.is_symlink():
        raise AssertionError(
            "isolated fixture support root already exists: " + str(support_root)
        )
    second = support_root / "second_prompt_files"
    second.mkdir(parents=True, exist_ok=False)
    (second / "_RUN_COLLECTOR_STATUS.txt").write_text(
        "Status: complete\nPublished after ZIP: True\n",
        encoding="utf-8",
    )
    archive_path = second / (project_slug + "__ai_handoff_upload.zip")
    safe_member = unsafe_member.replace("\\", "/")
    archive_prefix = project_slug + "__ai_handoff_upload/"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in _fixture_members(identity).items():
            if name.endswith("__ai_briefing.json"):
                payload = json.loads(content.decode("utf-8"))
                payload["project"]["absolute_root"] = str(project)
                content = json.dumps(payload).encode("utf-8")
            archive.writestr(archive_prefix + name, content)
        if unsafe_member:
            archive.writestr(safe_member, b"unsafe")
    replacement_count = 0
    if unsafe_member:
        replacement_count = _rewrite_member_name_in_zip_headers(
            archive_path,
            safe_member,
            unsafe_member,
        )
    return project, support_root, archive_path, replacement_count


def _cleanup_fixture(base: Path, support_root: Path | None) -> None:
    """Remove both transient source and canonical external support fixtures."""
    if support_root is not None:
        shutil.rmtree(support_root, ignore_errors=True)
    shutil.rmtree(base, ignore_errors=True)


class _FakeResponse:
    """Minimal context-managed response for catalog and SSE tests."""

    def __init__(self, body: bytes = b"", lines: tuple[bytes, ...] = ()) -> None:
        self._body = body
        self._lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> bool:
        return False

    def read(self, limit: int = -1) -> bytes:
        return self._body if limit < 0 else self._body[:limit]

    def __iter__(self):
        return iter(self._lines)


def _validate_bridge() -> None:
    """Validate bounded context loading and isolated ZIP fixtures."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_bridge import (
        load_project_web_ai_context,
    )
    from kanda_reasoner_app.web_ai_provider_contracts import SupportContextError

    fixtures: list[tuple[Path, Path | None]] = []
    safe_base = Path(tempfile.mkdtemp(prefix="kanda_web_ai_bridge_safe_"))
    unsafe_base = Path(tempfile.mkdtemp(prefix="kanda_web_ai_bridge_unsafe_"))
    fixtures.extend(((safe_base, None), (unsafe_base, None)))
    try:
        project, support_root, _archive_path, replacement_count = _build_fixture(
            safe_base
        )
        fixtures[0] = (safe_base, support_root)
        _assert(replacement_count == 0, "safe fixture unexpectedly rewrote ZIP headers")
        _assert(project.name != "demo", "validator retained the global fixed demo slug")
        snapshot = load_project_web_ai_context(project)
        _assert(snapshot.collector_status == "CURRENT", "collector status not current")
        _assert(snapshot.project_slug == project.name, "project slug mismatch")
        _assert("UNTRUSTED PROJECT EVIDENCE" in snapshot.context_text, "trust boundary missing")
        _assert("must not be forwarded" not in snapshot.context_text, "raw file inventory leaked")
        _assert(str(project) not in snapshot.context_text, "absolute project root leaked")
        _assert("<PROJECT_ROOT>" in snapshot.context_text, "project root marker missing")
        _assert("exact source files" in snapshot.omitted_sections, "source omission missing")
        print("PROJECT_WEB_AI_CONTEXT_BRIDGE: PASS")
        print("UNTRUSTED_PROJECT_EVIDENCE_BOUNDARY: PASS")
        print("COMPACT_HANDOFF_EXCLUDES_RAW_SOURCE: PASS")
        print("UNIQUE_ACTIVE_PROJECT_FIXTURE_IDENTITY: PASS")

        project, support_root, archive_path, replacement_count = _build_fixture(
            unsafe_base,
            unsafe_member="bad\\member.txt",
        )
        fixtures[1] = (unsafe_base, support_root)
        _assert(replacement_count == 2, "raw backslash fixture did not patch both ZIP headers")
        print("RAW_BACKSLASH_FIXTURE_HEADER_COUNT: PASS - 2")
        with zipfile.ZipFile(archive_path, "r") as archive:
            raw_names = [
                str(getattr(info, "orig_filename", ""))
                for info in archive.infolist()
            ]
        _assert(any("\\" in name for name in raw_names), "raw backslash fixture was normalized")
        print("RAW_BACKSLASH_FIXTURE_ORIG_FILENAME: PASS")
        try:
            load_project_web_ai_context(project)
        except SupportContextError as exc:
            _assert("backslash" in str(exc).lower(), "wrong unsafe-member failure")
        else:
            raise AssertionError("raw backslash ZIP member was accepted")
        print("SAFE_HANDOFF_ZIP_MEMBER_ACCESS: PASS")
    finally:
        for base, support_root in reversed(fixtures):
            _cleanup_fixture(base, support_root)

    for base, support_root in fixtures:
        _assert(not base.exists(), "temporary Project source fixture was not removed")
        if support_root is not None:
            _assert(
                not support_root.exists(),
                "canonical Project Support fixture was not removed",
            )
    print("PROJECT_SUPPORT_FIXTURE_CLEANUP: PASS")
    print("VALIDATOR_RERUN_SAFE_FIXTURE_OWNERSHIP: PASS")


def _validate_provider_runtime() -> None:
    """Validate profiles, dynamic catalogs, streaming, and prompt boundaries."""
    from kanda_reasoner_app.web_ai_model_catalog import fetch_gateway_models
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProviderResponseError,
        gateway_profiles,
        get_gateway_profile,
    )
    from kanda_reasoner_app.web_ai_provider_runtime import (
        build_project_messages,
        stream_chat_completion,
    )

    profiles = tuple(gateway_profiles())
    _assert([item.gateway_id for item in profiles] == ["openrouter", "kilo"], "wrong gateways")
    _assert(all("local" not in item.gateway_id for item in profiles), "local model exposed")
    print("WEB_ONLY_GATEWAY_PROFILES: PASS")

    catalog_body = json.dumps(
        {
            "data": [
                {
                    "id": "example/free:free",
                    "name": "Example Free",
                    "context_length": 100000,
                    "pricing": {"prompt": "0", "completion": "0"},
                    "supported_parameters": ["tools", "stream"],
                },
                {
                    "id": "example/paid",
                    "name": "Example Paid",
                    "context_length": 200000,
                    "pricing": {"prompt": "0.000001", "completion": "0.000002"},
                },
            ]
        }
    ).encode("utf-8")
    models = fetch_gateway_models(
        get_gateway_profile("kilo"),
        opener=lambda *_args, **_kwargs: _FakeResponse(body=catalog_body),
    )
    _assert(models[0].free_status, "free model was not classified")
    _assert(models[0].supports_tools, "tool metadata was not normalized")
    _assert(not models[-1].free_status, "paid model was classified as free")
    print("DYNAMIC_MODEL_CATALOG: PASS")

    lines = (
        b'data: {"id":"r1","model":"example/free:free","choices":[{"delta":{"content":"Hello"},"finish_reason":null}]}\n',
        b'data: {"id":"r1","model":"example/free:free","choices":[{"delta":{"content":" world"},"finish_reason":"stop"}]}\n',
        b'data: {"usage":{"prompt_tokens":4,"completion_tokens":2,"total_tokens":6},"choices":[]}\n',
        b'data: [DONE]\n',
    )
    tokens: list[str] = []
    result = stream_chat_completion(
        get_gateway_profile("kilo"),
        "example/free:free",
        [{"role": "user", "content": "hello"}],
        request_id="fixture-request",
        on_token=tokens.append,
        opener=lambda *_args, **_kwargs: _FakeResponse(lines=lines),
    )
    _assert(result.content == "Hello world", "stream content mismatch")
    _assert(result.usage.total_tokens == 6, "stream usage mismatch")
    _assert(tokens == ["Hello", " world"], "token delivery mismatch")
    oversized_line = b"data: " + (b"x" * (2 * 1024 * 1024 + 1)) + b"\n"
    try:
        stream_chat_completion(
            get_gateway_profile("kilo"),
            "example/free:free",
            [{"role": "user", "content": "hello"}],
            opener=lambda *_args, **_kwargs: _FakeResponse(lines=(oversized_line,)),
        )
    except ProviderResponseError:
        pass
    else:
        raise AssertionError("oversized SSE line was accepted")
    print("OPENAI_COMPATIBLE_STREAMING_RUNTIME: PASS")

    messages = build_project_messages(
        "Question",
        "PROJECT EVIDENCE",
        trusted_boundary_text="Tool: kanda_reasoner\nActive Project: demo",
    )
    _assert(messages[0]["role"] == "system", "system boundary missing")
    _assert("no authority" in messages[0]["content"].lower(), "advisory authority missing")
    _assert("UNTRUSTED PROJECT EVIDENCE" in messages[-2]["content"], "evidence marker missing")
    _assert("Tool: kanda_reasoner" in messages[0]["content"], "Tool identity missing")
    _assert("Active Project: demo" in messages[0]["content"], "Project identity missing")
    print("ADVISORY_ONLY_PROMPT_CONTRACT: PASS")


def _validate_local_adapter_reuse() -> None:
    """Prove the existing Tab 3 adapter reuses the shared transport."""
    source = Path(
        "kanda_reasoner_app/tab3_manual_review_runtime/"
        "ai_openai_compatible_provider_runtime.py"
    ).read_text(encoding="utf-8")
    _assert("web_ai_provider_runtime import request_chat_completion" in source, "shared runtime not reused")
    _assert("urllib.request" not in source, "Tab 3 retained a duplicate HTTP client")
    print("EXISTING_OPENAI_COMPATIBLE_ADAPTER_REUSES_SHARED_RUNTIME: PASS")


def _validate_registry_and_source(root: Path) -> None:
    """Validate tab registration, module boundaries, size, and source immutability."""
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

    matches = [spec for spec in TOOLS if spec.tab_id == "project_web_ai"]
    _assert(len(matches) == 1, "Project Web AI tab registration missing or duplicated")
    _assert(matches[0].class_candidates == ("ProjectWebAITab",), "wrong tab class")
    print("PROJECT_WEB_AI_NEW_TAB_REGISTERED: PASS")

    tab_source = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py").read_text(
        encoding="utf-8"
    )
    _assert("urllib.request" not in tab_source, "GUI owns networking")
    _assert("write_text(" not in tab_source and "write_bytes(" not in tab_source, "GUI writes source")
    print("NO_SECOND_NETWORK_ENGINE_IN_GUI: PASS")
    print("PROJECT_SOURCE_READ_ONLY_CONTRACT: PASS")

    for relative in TOUCHED_CODE:
        path = root / relative
        _assert(path.is_file(), "missing touched source: " + relative)
        lines = len(path.read_text(encoding="utf-8").splitlines())
        _assert(0 < lines <= 500, f"module-size violation {relative}: {lines}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _validate_widget() -> None:
    """Instantiate the real tab offscreen when PySide6 is available."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name == "nt" and Path("C:/Windows/Fonts").is_dir():
        os.environ.setdefault("QT_QPA_FONTDIR", "C:/Windows/Fonts")
    from PySide6.QtWidgets import QApplication
    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import ProjectWebAITab
    from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
    from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration

    app = QApplication.instance() or QApplication([])
    config = ConfigWebAITab()
    widget = ProjectWebAITab()
    _assert(config._controller is application_web_ai_configuration(), "central config owner mismatch")
    _assert(config.gateway_combo.count() == 2, "central gateway count mismatch")
    _assert(config.free_only_checkbox.isChecked(), "central free-only default missing")
    _assert(hasattr(widget, "open_web_config_button"), "Project Web AI config shortcut missing")
    _assert(not widget.send_button.isEnabled(), "send must fail closed initially")
    _assert(hasattr(widget, "project_root_edit"), "shared project-root field missing")
    widget.close()
    config.close()
    app.processEvents()
    print("REAL_PROJECT_WEB_AI_WIDGET: PASS")


def main() -> int:
    """Run the focused validator."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))

    before = {
        relative: _sha256(root / relative)
        for relative in TOUCHED_CODE
        if (root / relative).is_file()
    }
    os.chdir(root)
    _validate_bridge()
    _validate_provider_runtime()
    _validate_local_adapter_reuse()
    _validate_registry_and_source(root)
    if not args.static_only:
        _validate_widget()
    after = {relative: _sha256(root / relative) for relative in before}
    _assert(before == after, "focused validation mutated source")
    print("LIVE_PROJECT_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
