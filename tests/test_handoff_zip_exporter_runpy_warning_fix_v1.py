"""Regression tests for executing the handoff ZIP exporter as a module.

The package ``reasoner_context_bundle`` must not eagerly import
``handoff_zip_exporter`` from ``__init__`` because the GUI starts the exporter
with ``python -m kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter``.
Eager import triggers the runpy warning about the module already being present
in ``sys.modules`` before execution.
"""

from __future__ import annotations

import subprocess
import sys


def test_handoff_zip_exporter_module_execution_has_no_runpy_warning() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "default",
            "-m",
            "kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter",
            "--help",
        ],
        cwd=".",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "found in sys.modules after import of package" not in combined
    assert "RuntimeWarning" not in combined


def test_handoff_zip_exporter_public_surface_remains_lazy_available() -> None:
    import kanda_reasoner_app.reasoner_context_bundle as bundle

    assert bundle.DEFAULT_PART_SIZE_MB == 40
    assert bundle.CONSERVATIVE_PART_SIZE_MB == 25
    assert callable(bundle.export_json_handoff_zip_parts)
    assert callable(bundle.is_destination_inside_project_root)


if __name__ == "__main__":
    test_handoff_zip_exporter_module_execution_has_no_runpy_warning()
    test_handoff_zip_exporter_public_surface_remains_lazy_available()
    print("VALIDATION OK: handoff zip exporter runpy warning fix")
