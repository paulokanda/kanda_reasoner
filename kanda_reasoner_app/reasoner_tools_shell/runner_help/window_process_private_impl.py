"""Private window process private impl helpers for reasoner_tools_shell.runner."""

from __future__ import annotations

from PySide6.QtCore import QProcess, QProcessEnvironment

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    analysis_json_building_dir,
    analysis_json_complete_dir,
    primary_evidence_json_path,
    secondary_evidence_json_path,
)

import json
import os
from pathlib import Path
__all__ = ()
CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"
LEGACY_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))
def _has_reasoner_package(root: Path) -> bool: return any((root / name).is_dir() for name in (LEGACY_PACKAGE_NAME, CANONICAL_PACKAGE_NAME))
def _installed_package_dir(root: Path) -> Path: return next((root / name for name in (LEGACY_PACKAGE_NAME, CANONICAL_PACKAGE_NAME) if (root / name).is_dir()), root / LEGACY_PACKAGE_NAME)

def _bind_globals(namespace):
    """Bind runner.py globals for moved method bodies."""
    globals().update(namespace)

# PASS_067G_TAB4_SCOPE_HELPERS_START
def _tab4_tool_root() -> Path:
    """Return the installed tool root without assuming a fixed drive path."""
    try:
        default_root = globals().get("_DEFAULT_PROJECT_ROOT")
        if isinstance(default_root, Path) and _has_reasoner_package(default_root):
            return default_root.resolve()
    except Exception:
        pass
    here = Path(__file__).resolve()
    for parent in here.parents:
        if _has_reasoner_package(parent) and (parent / "reasoner_tools_gui.py").is_file():
            return parent
    for parent in here.parents:
        if _has_reasoner_package(parent):
            return parent
    return here.parent


def _tab4_is_drive_root(path: Path) -> bool:
    try:
        resolved = path.resolve()
    except Exception:
        resolved = path.absolute()
    anchor = Path(resolved.anchor) if resolved.anchor else None
    return bool(anchor and resolved == anchor)


def _tab4_resolve_project_root(raw_root: object) -> Path:
    """Resolve a Tab 4 scan root and prevent broad drive-root scans."""
    raw = str(raw_root or "").strip()
    if not raw:
        return _tab4_tool_root()
    try:
        candidate = Path(raw).expanduser().resolve()
    except Exception:
        candidate = Path(raw).expanduser().absolute()
    if _tab4_is_drive_root(candidate):
        tool_root = project_root if _has_reasoner_package(project_root) else _tab4_tool_root()
        try:
            if tool_root.drive.lower() == candidate.drive.lower():
                return tool_root
        except Exception:
            return tool_root
        raise ValueError("Project root must be a project folder, not a drive root: " + str(candidate))
    return candidate


def _tab4_project_key_candidates(project_root: Path) -> list[str]:
    keys = []
    try:
        resolved = str(project_root.expanduser().resolve())
        keys.append(resolved)
        keys.append(resolved.replace("\\", "/"))
    except Exception:
        raw = str(project_root.expanduser())
        keys.append(raw)
        keys.append(raw.replace("\\", "/"))
    keys.append(str(project_root))
    keys.append(str(project_root).replace("\\", "/"))
    return list(dict.fromkeys(keys))


def _tab4_rules_dict(payload: object) -> dict:
    if not isinstance(payload, dict):
        return {"folders": [], "files": [], "extensions": []}
    return {
        "folders": [str(x) for x in payload.get("folders", []) if str(x).strip()],
        "files": [str(x) for x in payload.get("files", []) if str(x).strip()],
        "extensions": [str(x) for x in payload.get("extensions", []) if str(x).strip()],
    }


def _tab4_load_ignore_rules(project_root: Path) -> dict:
    """Load Tab 8 non-project rules from shared GUI prefs, if available."""
    candidates = []
    for base in (project_root, _tab4_tool_root()):
        try:
            current = base.resolve()
        except Exception:
            current = base
        for _ in range(10):
            candidate = current / ".reasoner_tools_gui_prefs.json"
            if candidate not in candidates:
                candidates.append(candidate)
            if current.parent == current:
                break
            current = current.parent
    for prefs_path in candidates:
        if not prefs_path.exists():
            continue
        try:
            data = json.loads(prefs_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        project_rules = data.get("project_ignore_rules", {})
        if isinstance(project_rules, dict):
            for key in _tab4_project_key_candidates(project_root):
                if key in project_rules:
                    return _tab4_rules_dict(project_rules.get(key))
        legacy_rules = data.get("ignore_rules", {})
        if isinstance(legacy_rules, dict):
            return _tab4_rules_dict(legacy_rules)
    return {"folders": [], "files": [], "extensions": []}


def _tab4_build_child_env(project_root: Path) -> dict:
    env = os.environ.copy()
    tool_root = project_root if _has_reasoner_package(project_root) else _tab4_tool_root()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(tool_root) + (os.pathsep + existing if existing else "")
    env["PROJECT_REASONER_PROJECT_ROOT"] = str(project_root)
    env["PROJECT_REASONER_SCAN_ROOT"] = str(project_root)
    env["KANDA_RUNTIME_PROJECT_ROOT"] = str(project_root)
    env["KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT"] = str(project_root)
    env["PROJECT_REASONER_TAB8_IGNORE_RULES_JSON"] = json.dumps(_tab4_load_ignore_rules(project_root), ensure_ascii=True)
    return env


def _tab4_apply_second_prompt_build_env(self, env: dict) -> None:
    """Route child-process JSON bundle writes into the temporary build folder."""
    build_dir = str(getattr(self, "_pending_second_prompt_build_dir", "") or "").strip()
    if build_dir:
        env[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = build_dir


def _tab4_apply_qprocess_env(process, env: dict, working_dir: Path) -> None:
    try:
        process.setWorkingDirectory(str(working_dir))
    except Exception:
        pass
    process_env = QProcessEnvironment.systemEnvironment()
    for key, value in env.items():
        process_env.insert(str(key), str(value))
    process.setProcessEnvironment(process_env)
# PASS_067G_TAB4_SCOPE_HELPERS_END


def _start_runtime_trace_process(self) -> None:
    self._process = QProcess(self)
    self._process.finished.connect(self._on_process_finished)
    self._process.errorOccurred.connect(self._on_process_error)

    project_root = _tab4_resolve_project_root(self._pending_project_root)
    self._pending_project_root = str(project_root)

    env = _tab4_build_child_env(project_root)
    _tab4_apply_second_prompt_build_env(self, env)
    env["PROJECT_REASONER_RUNTIME_TRACE_JSON"] = self._pending_runtime_trace_json
    env["PROJECT_REASONER_RUNTIME_TRACE_OVERWRITE"] = "1"
    env["KANDA_RUNTIME_TRACE_JSON"] = self._pending_runtime_trace_json
    env["KANDA_RUNTIME_TRACE_OVERWRITE"] = "1"
    env["KANDA_RUNTIME_EXECUTE_ENTRY_SCRIPT"] = "0"

    tool_root = _tab4_tool_root()
    _tab4_apply_qprocess_env(self._process, env, project_root)
    process_args = [
        str((tool_root / CANONICAL_PACKAGE_NAME / "reasoner_runtime_collector" / "runtime_runner.py").resolve())
    ]

    self._start_busy_animation("Running runtime runner")
    self._process.start(sys.executable, process_args)

def _on_process_finished_without_web_ai_enrichment(self, exit_code: int, _exit_status) -> None:
    stdout_text = ""
    stderr_text = ""

    if self._process is not None:
        stdout_text = bytes(self._process.readAllStandardOutput()).decode(
            "utf-8",
            errors="replace",
        ).strip()
        stderr_text = bytes(self._process.readAllStandardError()).decode(
            "utf-8",
            errors="replace",
        ).strip()

    if exit_code != 0:
        failed_stage = self._active_stage or "Process"
        self._stop_busy_animation("Failed")
        self._append_log(f"[ERROR] {failed_stage} failed:")
        self._append_log(stderr_text or stdout_text or "Unknown child-process error")

        _safe_log_runtime_error(
            source_symbol="CollectorRunnerWindow._on_process_finished",
            message=f"{failed_stage} failed",
            payload={
                "traceback": stderr_text or stdout_text or "Unknown child-process error",
                "stage": failed_stage,
                "exit_code": exit_code,
            },
        )

        QMessageBox.critical(
            self,
            "Collector error",
            stderr_text or stdout_text or "Unknown child-process error",
        )
        self._process = None
        return

    try:
        result = json.loads(stdout_text) if stdout_text else {}
    except Exception:
        result = {}

    if self._active_stage == "Enriching complete JSON":
        missing_after = result.get("missing_after", [])
        changed = bool(result.get("changed", False))
        target = str(result.get("target", "") or "").strip()

        self._append_log("[OK] Complete JSON deterministic evidence sections verified.")
        self._append_log("  changed: " + str(changed))
        if target:
            self._append_log("  complete_json: " + target)

        _safe_log_runtime_event(
            event_type="complete_json_enriched",
            source_symbol="CollectorRunnerWindow._on_process_finished",
            message="Complete JSON deterministic AI-readable sections verified",
            tags=["collector", "complete_json", "enrichment"],
            payload={
                "target": target,
                "changed": changed,
                "missing_after": missing_after,
            },
        )

        self._process = None
        _start_ai_context_bundle_process(self)
        return

    if self._active_stage == "Generating AI context bundle":
        project_slug = str(result.get("project_slug", "") or "").strip()
        written_artifacts = result.get("written_artifacts", [])
        artifact_count = len(written_artifacts) if isinstance(written_artifacts, list) else 0

        self._append_log("[OK] AI context bundle generated.")
        if project_slug:
            self._append_log("  project_slug: " + project_slug)
        self._append_log("  companion_artifacts: " + str(artifact_count))

        _safe_log_runtime_event(
            event_type="ai_context_bundle_generated",
            source_symbol="CollectorRunnerWindow._on_process_finished",
            message="AI context bundle companion files generated successfully",
            tags=["collector", "ai_context_bundle", "finish"],
            payload={
                "project_slug": project_slug,
                "artifact_count": artifact_count,
            },
        )

        self._process = None
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
            zip_json_files_private_impl as _zip_json_impl,
        )
        try:
            project_root_path = _tab4_resolve_project_root(self._pending_project_root)
            final_dir = analysis_json_complete_dir(project_root_path).expanduser().resolve(strict=False)
            build_dir = Path(str(getattr(self, "_pending_second_prompt_build_dir", "") or "")).expanduser().resolve(strict=False)
            _zip_json_impl.write_second_prompt_status(
                build_dir,
                status="running",
                step="zipping generated files before final publish",
                project_root=project_root_path,
                final_output_dir=final_dir,
                details=[
                    "The final second_prompt_files folder remains untouched until ZIP export succeeds.",
                    "ZIP files are created inside the temporary build folder first.",
                ],
            )
            self._pending_second_prompt_final_dir = str(final_dir)
            self._append_log("Preparing ZIP export inside temporary build folder before final publish...")
            self._append_log("  build folder: " + str(build_dir))
            self._append_log("  final folder: " + str(final_dir))
        except Exception as exc:
            self._stop_busy_animation("Failed")
            self._append_log("[ERROR] Preparing second_prompt_files ZIP export failed:")
            self._append_log(str(exc))
            QMessageBox.critical(self, "Collector ZIP preparation error", str(exc))
            return
        _zip_json_impl.auto_zip_json_complete(self, self._pending_project_root)
        return

    if self._active_stage == "Running runtime runner":
        runtime_trace_path = str(result.get("runtime_trace_json", "") or "").strip()
        overwrote_existing = bool(result.get("overwrote_existing", False))
        trace_size = int(result.get("size", 0))

        if runtime_trace_path:
            self._pending_runtime_trace_json = runtime_trace_path
            self.runtime_trace_json_edit.setText(runtime_trace_path)

        self._append_log(
            "[OK] Runtime trace generated - "
            f"overwrote_existing={overwrote_existing}, size={trace_size}"
        )
        self._append_log(f"  runtime_trace: {self._pending_runtime_trace_json}")

        _save_prefs(
            self._pending_project_root,
            self._pending_output_json,
            self._pending_runtime_trace_json,
        )

        _safe_log_runtime_event(
            event_type="runtime_trace_generated",
            source_symbol="CollectorRunnerWindow._on_process_finished",
            message="Runtime trace generated successfully",
            tags=["runtime", "trace", "collector"],
            payload={
                "runtime_trace_json": self._pending_runtime_trace_json,
                "overwrote_existing": overwrote_existing,
                "size": trace_size,
            },
        )

        self._process = None
        self._start_collector_process()
        return

    file_count = int(result.get("file_count", 0))
    error_count = int(result.get("error_count", 0))

    self._append_log(f"[OK] Done - {file_count} files indexed, {error_count} errors.")
    self._append_log(f"  Saved to: {self._current_output_json}")

    _safe_log_runtime_event(
        event_type="collector_run_finished",
        source_symbol="CollectorRunnerWindow._on_process_finished",
        message="Collector child process finished successfully",
        tags=["collector", "finish"],
        payload={
            "file_count": file_count,
            "error_count": error_count,
            "output_json": self._current_output_json,
        },
    )

    self._process = None
    _start_complete_json_enrichment_process(self)

# PASS_070A_DISABLE_GUI_ENRICHMENT_START
def _on_process_finished(self, exit_code: int, _exit_status) -> None:
    """Use the official process-finished handler only.

    Complete JSON enrichment must not run inside the GUI parent process. The
    collector child owns collection and output writing; running enrichment here
    can block or crash the Qt process while the child is still active.
    """
    return _on_process_finished_without_web_ai_enrichment(self, exit_code, _exit_status)
# PASS_070A_DISABLE_GUI_ENRICHMENT_END

def _on_process_error(self, _process_error) -> None:
    failed_stage = self._active_stage or "Process"
    self._stop_busy_animation("Failed")
    self._append_log(f"[ERROR] {failed_stage} process could not start.")
    QMessageBox.critical(
        self,
        "Collector error",
        f"{failed_stage} process could not start.",
    )

    _safe_log_runtime_error(
        source_symbol="CollectorRunnerWindow._on_process_error",
        message=f"{failed_stage} process could not start.",
        payload={
            "stage": failed_stage,
        },
    )

    self._process = None

def _start_collector_process(self) -> None:
    self._process = QProcess(self)
    self._process.finished.connect(self._on_process_finished)
    self._process.errorOccurred.connect(self._on_process_error)

    project_root = _tab4_resolve_project_root(self._pending_project_root)
    self._pending_project_root = str(project_root)

    env = _tab4_build_child_env(project_root)
    _tab4_apply_second_prompt_build_env(self, env)
    env["PROJECT_REASONER_RUNTIME_TRACE_JSON"] = self._pending_runtime_trace_json
    env["PROJECT_REASONER_RUNTIME_TRACE_OVERWRITE"] = "1"
    tool_root = _tab4_tool_root()
    _tab4_apply_qprocess_env(self._process, env, project_root)

    process_args = [
        str(tool_root / CANONICAL_PACKAGE_NAME / "reasoner_tools_shell" / "runner.py"),
        _CHILD_MODE_ARG,
        self._pending_project_root,
        self._pending_output_json,
        self._pending_runtime_trace_json,
    ]

    self._start_busy_animation("Running collector")
    self._process.start(sys.executable, process_args)


def _start_complete_json_enrichment_process(self) -> None:
    self._process = QProcess(self)
    self._process.finished.connect(self._on_process_finished)
    self._process.errorOccurred.connect(self._on_process_error)

    project_root = _tab4_resolve_project_root(self._pending_project_root)
    self._pending_project_root = str(project_root)

    env = _tab4_build_child_env(project_root)
    _tab4_apply_second_prompt_build_env(self, env)
    _tab4_apply_qprocess_env(self._process, env, project_root)

    process_args = [
        "-m",
        CANONICAL_PACKAGE_NAME + ".reasoner_context_collector.complete_json_web_ai_enrichment",
        "--root",
        self._pending_project_root,
        "--complete-json",
        self._pending_output_json,
        "--compact",
    ]

    self._start_busy_animation("Enriching complete JSON")
    self._append_log("Verifying complete JSON deterministic evidence sections...")
    self._process.start(sys.executable, process_args)


def _start_ai_context_bundle_process(self) -> None:
    self._process = QProcess(self)
    self._process.finished.connect(self._on_process_finished)
    self._process.errorOccurred.connect(self._on_process_error)

    project_root = _tab4_resolve_project_root(self._pending_project_root)
    self._pending_project_root = str(project_root)

    env = _tab4_build_child_env(project_root)
    _tab4_apply_second_prompt_build_env(self, env)
    _tab4_apply_qprocess_env(self._process, env, project_root)

    process_args = [
        "-m",
        CANONICAL_PACKAGE_NAME + ".reasoner_context_bundle",
        "--root",
        self._pending_project_root,
        "--write",
        "--compact",
        "--skip-validation",
    ]

    self._start_busy_animation("Generating AI context bundle")
    self._append_log("Generating AI context bundle companion files...")
    self._process.start(sys.executable, process_args)




def _run_collector(self) -> None:
    project_root_raw = self.project_root_edit.text().strip()

    try:
        project_root_path = _tab4_resolve_project_root(project_root_raw)
    except Exception as exc:
        QMessageBox.warning(
            self,
            "Invalid path",
            "Project root must be a project folder, not a broad drive root.\n" + str(exc),
        )
        return

    if not project_root_path.is_dir():
        QMessageBox.warning(
            self,
            "Invalid path",
            "Project root does not exist:\n" + str(project_root_path),
        )
        return

    project_root = str(project_root_path)
    if self.project_root_edit.text().strip() != project_root:
        self.project_root_edit.setText(project_root)

    from kanda_reasoner_app.generated_artifact_hygiene import cleanup_project_generated_zip_noise

    cleanup_result = cleanup_project_generated_zip_noise(project_root_path)
    if cleanup_result.get("removed"):
        self._append_log("Cleaned deprecated in-project ZIP delivery artifacts before source archive:")
        for item in cleanup_result.get("removed", []):
            self._append_log("  " + str(item.get("path", "")) + " (" + str(item.get("reason_code", "")) + ")")
    if cleanup_result.get("errors"):
        QMessageBox.warning(
            self,
            "Cleanup failed",
            "Generated ZIP artifact cleanup failed before source archive:\n" + str(cleanup_result.get("errors")),
        )
        return

    # Hybrid Source Archive mode: the selected project root is the scan target,
    # but Second Prompt Files no longer generates the old heavy complete.json or
    # active_snapshot.json payloads.  Exact reconstruction is a source archive
    # manifest plus standalone source_archive_part ZIPs; AI-readable JSONs are
    # lightweight maps only.
    final_output_dir = analysis_json_complete_dir(project_root_path).expanduser().resolve(strict=False)
    build_output_dir = analysis_json_building_dir(project_root_path).expanduser().resolve(strict=False)
    project_slug = project_root_path.name
    output_json = build_output_dir / (project_slug + "__source_archive_manifest.json")
    runtime_trace_path = build_output_dir / (project_slug + "__validation_state.json")
    self.output_json_edit.setText(str(output_json))
    self.runtime_trace_json_edit.setText(str(runtime_trace_path))

    self.status_label.setText("Idle")
    self.log_box.clear()

    from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
        zip_json_files_private_impl as _zip_json_impl,
    )
    removed_count = _zip_json_impl.clear_second_prompt_files_building_dir(build_output_dir)
    self._pending_second_prompt_build_dir = str(build_output_dir)
    self._pending_second_prompt_final_dir = str(final_output_dir)
    _zip_json_impl.write_second_prompt_status(
        build_output_dir,
        status="running",
        step="starting lightweight map generation",
        project_root=project_root_path,
        final_output_dir=final_output_dir,
        details=[
            "Temporary build folder was cleared before this run.",
            "Removed old build-folder items: " + str(removed_count),
            "Previous final delivery remains available until publish succeeds.",
            "Hybrid mode skips old heavy complete.json and active_snapshot.json generation.",
        ],
    )
    self._append_log(
        "Prepared second_prompt_files_building output folder; removed existing items: "
        + str(removed_count)
    )
    self._append_log("  build folder: " + str(build_output_dir))
    self._append_log("  final folder: " + str(final_output_dir))

    build_output_dir.mkdir(parents=True, exist_ok=True)

    self._current_output_json = str(output_json)
    self._pending_project_root = project_root
    self._pending_output_json = str(output_json)
    self._pending_runtime_trace_json = str(runtime_trace_path)

    _save_prefs(
        self._pending_project_root,
        self._pending_output_json,
        self._pending_runtime_trace_json,
    )

    self._append_log("Starting lightweight map generation for hybrid source archive export...")
    self._append_log(f"  root : {self._pending_project_root}")
    self._append_log(f"  source_archive_manifest: {self._pending_output_json}")
    self._append_log("  skipped: old complete.json and active_snapshot.json generation")

    _safe_log_runtime_event(
        event_type="collector_run_started",
        source_symbol="CollectorRunnerWindow._run_collector",
        message="Collector run requested from GUI",
        tags=["collector", "start", "gui"],
        payload={
            "project_root": self._pending_project_root,
            "output_json": self._pending_output_json,
            "runtime_trace_json": self._pending_runtime_trace_json,
        },
    )

    _start_ai_context_bundle_process(self)
