# Public-contract checks for the AST split-audit runner.
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit


def test_ast_split_audit_detects_islands_and_writes_reports(tmp_path: Path) -> None:
    project = tmp_path / "demo_project"
    project.mkdir()
    target = project / "sample_gui.py"
    source = (
        "from pathlib import Path\n"
        "from PySide6.QtWidgets import QMessageBox\n"
        "\n"
        "class Demo:\n"
        "    def _load_pending_file(self):\n"
        "        text = Path('x').read_text()\n"
        "        self.pending_edit.setPlainText(text)\n"
        "        return text\n"
        "\n"
        "    def _delete_draft_file(self):\n"
        "        self.draft_path.unlink()\n"
        "        QMessageBox.warning(self, 'x', 'y')\n"
        "\n"
        "    def _copy_clipboard(self):\n"
        "        self.clipboard_button.setEnabled(True)\n"
    )
    target.write_text(source, encoding="utf-8")
    result = run_large_module_split_audit(project, "sample_gui.py")
    assert result.markdown_path.exists()
    assert result.json_path.exists()
    assert "Large Module AST Split Audit" in result.markdown
    assert "pending_intake" in result.markdown
    assert "draft_cleanup" in result.markdown
    assert "file_delete" in result.markdown
    assert result.data["kind"] == "large_module_ast_split_audit"
    assert result.data["recommendation"]["mode"] in {"single_island", "two_island_batch_candidate", "manual_audit_required"}
