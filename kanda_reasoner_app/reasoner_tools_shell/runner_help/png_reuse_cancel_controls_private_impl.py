"""Show Project to AI PNG reuse prompt and cancellation controls."""

from __future__ import annotations

from typing import Any

PNG_REUSE_PROMPT = (
    "Inspect and preserve the canonical Show Project to AI PNG reuse behavior. "
    "When the selected Project's current PNG content signature - path, byte size, "
    "and SHA-256 - matches the previously published source archive manifest, and "
    "every previous png_assets ZIP part validates by filename, size, SHA-256, and "
    "ZIP integrity, reuse those already published PNG ZIP parts from the same "
    "Project's final second_prompt_files folder. Do not rebuild unchanged PNG "
    "archives. Do not treat mtime or ZIP timestamp differences as image-content "
    "changes. Preserve project-independent paths, do not create empty PNG ZIPs, "
    "and do not duplicate PNG files in the source_archive family. If any PNG "
    "content or the archive contract changed, rebuild normally. Validate both "
    "reuse-when-unchanged and rebuild-when-changed behavior."
)


def install_controls(window: Any, row: Any) -> None:
    """Add the Cancel and Reuse PNG buttons to the combined-run row."""
    from PySide6.QtGui import QColor, QPalette
    from PySide6.QtWidgets import QApplication, QPushButton

    window.cancel_prompt_files_button = QPushButton("Cancel")
    cancel_palette = window.cancel_prompt_files_button.palette()
    cancel_palette.setColor(QPalette.ButtonText, QColor("#008000"))
    window.cancel_prompt_files_button.setPalette(cancel_palette)
    cancel_font = window.cancel_prompt_files_button.font()
    cancel_font.setBold(True)
    window.cancel_prompt_files_button.setFont(cancel_font)
    row.addWidget(window.cancel_prompt_files_button)

    window.copy_png_reuse_prompt_button = QPushButton("Reuse PNG")
    reuse_palette = window.copy_png_reuse_prompt_button.palette()
    reuse_palette.setColor(QPalette.ButtonText, QColor("#ff4d00"))
    window.copy_png_reuse_prompt_button.setPalette(reuse_palette)
    reuse_font = window.copy_png_reuse_prompt_button.font()
    reuse_font.setBold(True)
    window.copy_png_reuse_prompt_button.setFont(reuse_font)
    row.addWidget(window.copy_png_reuse_prompt_button)

    def copy_prompt() -> None:
        QApplication.clipboard().setText(PNG_REUSE_PROMPT)
        try:
            window._append_log("Copied canonical PNG reuse prompt to clipboard.")
        except Exception:
            pass

    window.copy_png_reuse_prompt_button.clicked.connect(copy_prompt)
    window.cancel_prompt_files_button.clicked.connect(lambda: cancel_run(window))


def update_cancel_enabled(window: Any) -> None:
    """Enable Cancel only while a child process is active."""
    try:
        window.cancel_prompt_files_button.setEnabled(
            getattr(window, "_process", None) is not None
        )
    except Exception:
        pass


def cancel_run(window: Any) -> None:
    """Cancel the active prompt-file child process without publishing partial output."""
    process = getattr(window, "_process", None)
    if process is None:
        try:
            window._append_log("No Create Prompt Files process is active.")
        except Exception:
            pass
        update_cancel_enabled(window)
        return

    window._cancel_prompt_files_requested = True
    try:
        window._append_log("Cancel requested. Stopping Create Prompt Files...")
    except Exception:
        pass
    try:
        process.terminate()
        if not process.waitForFinished(3000):
            process.kill()
            process.waitForFinished(3000)
    except Exception:
        try:
            process.kill()
        except Exception:
            pass


def consume_cancel_on_finish(window: Any, finish_status) -> bool:
    """Finalize a requested cancellation before normal process handling."""
    if not bool(getattr(window, "_cancel_prompt_files_requested", False)):
        return False
    window._cancel_prompt_files_requested = False
    try:
        finish_status("Canceled")
    except Exception:
        pass
    try:
        window._append_log(
            "[OK] Create Prompt Files canceled. Previous published delivery was preserved."
        )
    except Exception:
        pass
    window._process = None
    update_cancel_enabled(window)
    return True
