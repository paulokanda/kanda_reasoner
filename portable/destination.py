"""Native destination-folder selection for Portable publication."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from portable.constants import FINAL_ZIP_NAME
from portable.errors import PortableBuildError
from portable.models import RegistryBoundary
from portable.registry_boundary import (
    assert_registry_unchanged,
    validate_publication_directory,
)


def _windows_folder_picker(initial_directory: Path) -> Path:
    """Open a native folder picker and return the selected directory."""

    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:
        raise PortableBuildError(
            "Python tkinter is unavailable; the destination folder picker "
            "cannot open."
        ) from exc

    root = tk.Tk()
    root.withdraw()
    root.update_idletasks()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    try:
        selected = filedialog.askdirectory(
            parent=root,
            title=(
                "Select folder for "
                "KandaReasoner-Windows-Portable.zip"
            ),
            initialdir=str(initial_directory),
            mustexist=True,
        )
    finally:
        root.destroy()

    if not selected:
        raise PortableBuildError(
            "Portable destination-folder selection was cancelled."
        )
    return Path(selected).resolve()


def _verify_writable(directory: Path) -> None:
    """Probe writability only after registry-boundary validation passes."""

    probe: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=".kanda_portable_write_probe_",
            dir=directory,
            delete=False,
        ) as handle:
            probe = Path(handle.name)
            handle.write(b"KANDA_PORTABLE_DESTINATION_PROBE")
        probe.unlink()
    except OSError as exc:
        if probe is not None:
            probe.unlink(missing_ok=True)
        raise PortableBuildError(
            f"Selected Portable destination is not writable: {directory}"
        ) from exc


def select_output_directory(
    project_root: Path,
    requested_directory: Path | None,
    boundary: RegistryBoundary,
) -> Path:
    """Select and boundary-validate the final destination before probing it."""

    project = project_root.resolve()
    default_directory = Path(project.anchor).resolve()
    selected = (
        requested_directory.resolve()
        if requested_directory is not None
        else _windows_folder_picker(default_directory)
    )

    if not selected.is_dir():
        raise PortableBuildError(
            f"Selected Portable destination folder does not exist: {selected}"
        )
    if os.name != "nt":
        raise PortableBuildError(
            "The native Portable destination picker is supported on Windows."
        )

    validated = validate_publication_directory(
        selected,
        boundary,
        final_zip_name=FINAL_ZIP_NAME,
    )
    print("PORTABLE DESTINATION REGISTRY BOUNDARY: PASS")
    assert_registry_unchanged(boundary)
    _verify_writable(validated)
    print(f"PORTABLE DESTINATION FOLDER SELECTED: {validated}")
    print("PORTABLE DESTINATION FOLDER WRITABLE: PASS")
    return validated
