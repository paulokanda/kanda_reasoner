"""Tests for the report-only storage policy secret scan gate."""

from __future__ import annotations

from pathlib import Path
import inspect
import unittest

from kanda_reasoner_app.storage_policy.secret_scan_gate import (
    SECRET_SCAN_ACTION,
    SECRET_SCAN_SEVERITY_HIGH,
    SECRET_SCAN_SEVERITY_HINT,
    SECRET_SCAN_SEVERITY_MEDIUM,
    SecretScanFinding,
    SecretScanReport,
    scan_path_for_secrets,
    scan_text_for_secrets,
    summarize_secret_scan,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECRET_SCAN_SOURCE = (
    PROJECT_ROOT / "kanda_reasoner_app" / "storage_policy" / "secret_scan_gate.py"
)


class StoragePolicySecretScanGateTests(unittest.TestCase):
    """Validate the report-only sensitive value scan gate."""

    def test_clean_tree_has_no_findings(self) -> None:
        root = self._make_root("clean_tree")
        (root / "main.py").write_text("print('hello')\n", encoding="utf-8")

        report = scan_path_for_secrets(root)

        self.assertTrue(report.is_clean())
        self.assertEqual(report.total_findings, 0)
        self.assertEqual(report.action, SECRET_SCAN_ACTION)

    def test_detects_private_key_block_without_revealing_value(self) -> None:
        secret_text = "-----BEGIN " + "PRIVATE KEY-----"
        content = "header\n" + secret_text + "\nfooter\n"

        findings = scan_text_for_secrets("secret.txt", content)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].pattern_name, "private_key_block")
        self.assertEqual(findings[0].severity, SECRET_SCAN_SEVERITY_HIGH)
        self.assertNotIn(secret_text, findings[0].redacted_preview)
        self.assertIn("<redacted>", findings[0].redacted_preview)

    def test_detects_github_style_token(self) -> None:
        token = "ghp_" + ("A" * 30)
        findings = scan_text_for_secrets("token.txt", "value = '" + token + "'\n")

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].pattern_name, "github_token")
        self.assertEqual(findings[0].severity, SECRET_SCAN_SEVERITY_HIGH)
        self.assertNotIn(token, findings[0].redacted_preview)

    def test_detects_credential_assignment(self) -> None:
        value = "x" * 20
        findings = scan_text_for_secrets("config.py", "api_key = '" + value + "'\n")

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].pattern_name, "credential_assignment")
        self.assertEqual(findings[0].severity, SECRET_SCAN_SEVERITY_MEDIUM)
        self.assertNotIn(value, findings[0].redacted_preview)

    def test_detects_sensitive_filename_hint(self) -> None:
        root = self._make_root("filename_hint")
        (root / ".env").write_text("NOT_A_SECRET=placeholder\n", encoding="utf-8")

        report = scan_path_for_secrets(root)

        self.assertEqual(report.total_findings, 1)
        self.assertEqual(report.findings[0].pattern_name, "sensitive_filename_hint")
        self.assertEqual(report.findings[0].severity, SECRET_SCAN_SEVERITY_HINT)

    def test_summary_is_redacted(self) -> None:
        token = "ghp_" + ("B" * 30)
        report = SecretScanReport(
            source_root="demo",
            findings=scan_text_for_secrets("token.txt", token),
        )

        summary = summarize_secret_scan(report)

        self.assertIn("Kanda Reasoner secret scan report", summary)
        self.assertIn("<redacted>", summary)
        self.assertNotIn(token, summary)

    def test_missing_source_root_raises(self) -> None:
        with self.assertRaises(ValueError):
            scan_path_for_secrets(PROJECT_ROOT / "missing_secret_scan_root_xyz")

    def test_finding_dataclass_is_immutable_data(self) -> None:
        finding = SecretScanFinding(
            relative_path="file.py",
            line_number=1,
            pattern_name="demo",
            severity="hint",
            redacted_preview="<redacted>",
            recommended_action="review",
        )

        with self.assertRaises(Exception):
            finding.relative_path = "changed.py"  # type: ignore[misc]

    def test_report_counts_findings_by_severity(self) -> None:
        findings = (
            SecretScanFinding("a", 1, "x", SECRET_SCAN_SEVERITY_HIGH, "r", "a"),
            SecretScanFinding("b", 1, "x", SECRET_SCAN_SEVERITY_MEDIUM, "r", "a"),
            SecretScanFinding("c", 1, "x", SECRET_SCAN_SEVERITY_HINT, "r", "a"),
        )
        report = SecretScanReport(source_root="demo", findings=findings)

        self.assertEqual(report.total_findings, 3)
        self.assertEqual(report.high_confidence_findings, 1)
        self.assertEqual(report.medium_confidence_findings, 1)
        self.assertEqual(report.hint_findings, 1)

    def test_public_surface_is_declared(self) -> None:
        import kanda_reasoner_app.storage_policy.secret_scan_gate as module

        expected = {
            "SECRET_SCAN_ACTION",
            "SECRET_SCAN_EXCLUDED_DIR_NAMES",
            "SECRET_SCAN_PATTERNS",
            "SECRET_SCAN_SEVERITY_HIGH",
            "SECRET_SCAN_SEVERITY_HINT",
            "SECRET_SCAN_SEVERITY_MEDIUM",
            "SECRET_SCAN_TEXT_SUFFIXES",
            "SENSITIVE_FILENAME_HINTS",
            "SecretPattern",
            "SecretScanFinding",
            "SecretScanReport",
            "scan_path_for_secrets",
            "scan_text_for_secrets",
            "summarize_secret_scan",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = SECRET_SCAN_SOURCE.read_text(encoding="utf-8")

        forbidden_fragments = [
            "E:\\",
            "E:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
            "project_analysis_evidence",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)

    def test_import_does_not_scan_live_tree(self) -> None:
        import kanda_reasoner_app.storage_policy.secret_scan_gate as module

        source = inspect.getsource(module)
        self.assertIn("report-only", source)
        self.assertNotIn("scan_path_for_secrets(get_app_root", source)

    def _make_root(self, name: str) -> Path:
        root = PROJECT_ROOT / "workbench" / "bundle_manifest" / "test_tmp" / name
        if root.exists():
            for item in sorted(root.rglob("*"), reverse=True):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    item.rmdir()
            root.rmdir()
        root.mkdir(parents=True)
        return root


if __name__ == "__main__":
    unittest.main()
