"""
PHASE 4 WIRING PATCH
====================

Three targeted changes spread across two files.

══════════════════════════════════════════════════════════════════════════════
FILE 1: insert_missing_docstrings.py
══════════════════════════════════════════════════════════════════════════════

CHANGE A — Add --private CLI flag and --min-confidence flag to build_parser()
──────────────────────────────────────────────────────────────────────────────
Inside build_parser(), add after the existing --workers argument:

    parser.add_argument(
        "--private",
        action="store_true",
        default=True,
        help=(
            "Document private (_name, __name) symbols.  "
            "Default: on.  Use --no-private to skip them."
        ),
    )
    parser.add_argument(
        "--no-private",
        dest="private",
        action="store_false",
        help="Skip private (_name, __name) symbols.",
    )
    parser.add_argument(
        "--min-confidence",
        choices=["high", "medium", "low"],
        default="low",
        help=(
            "Minimum validator confidence required to accept an AI docstring. "
            "Rejected docstrings fall back to heuristic.  Default: low."
        ),
    )
    parser.add_argument(
        "--no-uncertain",
        action="store_true",
        help="Suppress # AI-UNCERTAIN comments on low-confidence docstrings.",
    )


CHANGE B — Forward new flags into AIConfig in run()
────────────────────────────────────────────────────
In run(), after building `cfg = AIConfig.from_json(...) / AIConfig.default()`,
add the following overrides if the caller passes them:

    # Phase 4: override config from CLI flags when explicitly set.
    if include_private is not None:
        cfg.include_private = include_private
    if min_confidence is not None:
        cfg.min_confidence = min_confidence
    if no_uncertain:
        cfg.uncertain_annotation = False

Update run()'s signature to accept these:

    def run(
        root: Path,
        mode: str,
        *,
        include_module: bool = True,
        include_classes: bool = True,
        include_functions: bool = True,
        include_init: bool = False,
        include_relaxed_paths: bool = False,
        include_tests: bool = False,
        ai_config_path: str | None = None,
        workers: int = 1,
        include_private: bool = True,          # Phase 4 new
        min_confidence: str = "low",           # Phase 4 new
        no_uncertain: bool = False,            # Phase 4 new
        on_file_progress: Callable | None = None,
        on_file_complete: Callable | None = None,
    ) -> int:

And update main() to pass them through:

    return run(
        root, mode,
        include_module=not args.no_module,
        include_classes=not args.no_classes,
        include_functions=not args.no_functions,
        include_init=args.include_init,
        include_relaxed_paths=args.include_relaxed_paths,
        include_tests=args.include_tests,
        ai_config_path=args.ai,
        workers=args.workers or 1,
        include_private=args.private,          # Phase 4
        min_confidence=args.min_confidence,    # Phase 4
        no_uncertain=args.no_uncertain,        # Phase 4
    )


CHANGE C — Print GenerationStats after collect_changes() in run()
─────────────────────────────────────────────────────────────────
After the `if generator is not None and _AI_AVAILABLE: generator.flush_cache()` block,
add:

    if generator is not None and _AI_AVAILABLE:
        print(f"\nAI generation stats: {generator.stats.summary_line()}")


CHANGE D — Pass on_low_confidence to AIDocstringGenerator in run()
───────────────────────────────────────────────────────────────────
Replace:

    generator = AIDocstringGenerator(
        config=cfg,
        project_root=root,
        on_fallback=_on_fallback,
    )

With:

    def _on_low_confidence(symbol_name: str, issues: list[str]) -> None:
        print(f"LOW-CONFIDENCE {symbol_name}: {'; '.join(issues)}")

    generator = AIDocstringGenerator(
        config=cfg,
        project_root=root,
        on_fallback=_on_fallback,
        on_low_confidence=_on_low_confidence,
    )


══════════════════════════════════════════════════════════════════════════════
FILE 2: insert_missing_docstrings_gui.py
══════════════════════════════════════════════════════════════════════════════

CHANGE E — Add min-confidence selector and include-private checkbox to AISettingsPanel
──────────────────────────────────────────────────────────────────────────────────────
Inside AISettingsPanel.__init__(), after the fallback_checkbox row, add:

    self._confidence_combo = QComboBox()
    self._confidence_combo.addItems(["low", "medium", "high"])
    self._confidence_combo.setCurrentText("low")
    self._confidence_combo.setToolTip(
        "Minimum confidence required to accept an AI docstring.\n"
        "Rejected docstrings fall back to heuristic.\n"
        "• low   — accept everything that passes fatal checks\n"
        "• medium — also require no high TODO density or invented names\n"
        "• high  — also require correct line length and section ordering"
    )
    form.addRow("Min confidence", self._confidence_combo)

    self._private_checkbox = QCheckBox("Document private (_name, __name) symbols")
    self._private_checkbox.setChecked(True)
    form.addRow("", self._private_checkbox)

    self._uncertain_checkbox = QCheckBox("Append # AI-UNCERTAIN comments")
    self._uncertain_checkbox.setChecked(True)
    form.addRow("", self._uncertain_checkbox)

Add properties for the new widgets:

    @property
    def min_confidence(self) -> str:
        return self._confidence_combo.currentText()

    @property
    def include_private(self) -> bool:
        return self._private_checkbox.isChecked()

    @property
    def uncertain_annotation(self) -> bool:
        return self._uncertain_checkbox.isChecked()


CHANGE F — Forward new panel values to DocstringRunWorker
──────────────────────────────────────────────────────────
In MissingDocstringsWindow.run_mode(), update the DocstringRunWorker construction:

    self._worker = DocstringRunWorker(
        worker_script_path=str(worker_path),
        project_root=str(root_path),
        mode=mode,
        include_module=self._module_checkbox.isChecked(),
        include_classes=self._class_checkbox.isChecked(),
        include_functions=self._function_checkbox.isChecked(),
        ai_enabled=self._ai_panel.ai_enabled,
        ai_config_path=self._ai_panel.ai_config_path,
        workers=self._ai_panel.workers,
        include_private=self._ai_panel.include_private,     # Phase 4
        min_confidence=self._ai_panel.min_confidence,       # Phase 4
        uncertain_annotation=self._ai_panel.uncertain_annotation,  # Phase 4
    )

Add these to DocstringRunWorker.__init__() and forward them in the
module.run(...) call:

    run_kwargs["include_private"] = self._include_private
    run_kwargs["min_confidence"] = self._min_confidence
    run_kwargs["no_uncertain"] = not self._uncertain_annotation


CHANGE G — Display confidence counts in the output panel
─────────────────────────────────────────────────────────
In MissingDocstringsWindow._handle_worker_success(), change the info box to:

    # The worker prints stats to stdout which arrives via output_ready.
    # Just refresh the status bar with a summary.
    self.statusBar().showMessage(
        f"Finished {mode} — check output panel for AI generation stats"
    )


══════════════════════════════════════════════════════════════════════════════
FINAL FILE LAYOUT (all 7 files in the same directory)
══════════════════════════════════════════════════════════════════════════════

    insert_missing_docstrings.py        ← patched (Changes A-D)
    insert_missing_docstrings_gui.py    ← patched (Changes E-G)
    ai_config.py                        ← Phase 4 replacement
    context_builder.py                  ← Phase 3, unchanged
    ai_docstring_generator.py           ← Phase 4 replacement
    docstring_validator.py              ← Phase 4 new file
    parallel_runner.py                  ← Phase 2, unchanged
    module_summarizer.py                ← Phase 3, unchanged

══════════════════════════════════════════════════════════════════════════════
EXAMPLE ai_config.json with Phase 4 fields
══════════════════════════════════════════════════════════════════════════════
{
  "base_url": "http://localhost:11434/v1",
  "model": "qwen2.5-coder:14b",
  "timeout_seconds": 25.0,
  "max_tokens": 512,
  "temperature": 0.05,
  "fallback_to_heuristic": true,
  "workers": 4,
  "cache_enabled": true,
  "cache_path": ".docstring_cache.json",
  "docstring_style": "numpy",
  "include_private": true,
  "min_confidence": "medium",
  "max_line_length": 88,
  "max_todo_ratio": 0.4,
  "allow_invented_params": false,
  "allow_invented_raises": false,
  "uncertain_annotation": true
}

══════════════════════════════════════════════════════════════════════════════
EXAMPLE CLI invocations with Phase 4 flags
══════════════════════════════════════════════════════════════════════════════

# Default: document everything including private, accept low confidence
python insert_missing_docstrings.py --root . --diff --ai

# Skip private symbols, require medium confidence, suppress uncertainty comments
python insert_missing_docstrings.py --root . --diff --ai \\
    --no-private --min-confidence medium --no-uncertain

# Strictest: only accept high-confidence output, use custom model config
python insert_missing_docstrings.py --root . --write --ai my_config.json \\
    --min-confidence high --workers 6
"""
