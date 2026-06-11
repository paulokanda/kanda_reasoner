from pathlib import Path
import subprocess

def test_portal_report_generation():
    root = Path(__file__).resolve().parents[2]  # Points to EEG_KANDA/
    script_path = root / "dev_portal_updater_08/portal_updater_08.py"
    output_path = script_path.parent / "dev_portal_report.md"

    result = subprocess.run(["python", str(script_path)],
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                            errors="replace")

    print(result.stdout)
    print(result.stderr)

    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert output_path.exists(), "Markdown report was not generated"
    assert output_path.stat().st_size > 20, "Markdown file seems empty"


# pytest test_test_portal_updater.py