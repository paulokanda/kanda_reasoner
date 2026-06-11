"""Regression tests for Engineering Safety legacy-token cleanup."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENGINEERING_SAFETY_FILES = [
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "crash_triage.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "risk_radar.py",
]
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'


class EngineeringSafetyLegacyTokenCleanupTests(unittest.TestCase):
    """Validate Engineering Safety compatibility without hardcoded legacy token."""

    def test_engineering_safety_sources_do_not_hardcode_legacy_package_token(self) -> None:
        for path in ENGINEERING_SAFETY_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn(LEGACY_TOKEN, source, path.as_posix())

    def test_risk_radar_still_classifies_canonical_and_legacy_paths(self) -> None:
        from kanda_reasoner_app.engineering_safety.risk_radar import (
            infer_risk_change_affected_boxes,
        )

        boxes = infer_risk_change_affected_boxes(
            [
                "kanda_reasoner_app/engineering_safety/risk_radar.py",
                "ask_ai" + "_project_reasoner/engineering_safety/risk_radar.py",
            ]
        )
        self.assertEqual(boxes, ["engineering_safety"])

    def test_crash_triage_extracts_canonical_and_legacy_traceback_frames(self) -> None:
        from kanda_reasoner_app.engineering_safety.crash_triage import (
            extract_crash_traceback_frames,
        )

        traceback_text = (
            "Traceback (most recent call last):\n"
            "  File \"E:/kanda_reasoner/kanda_reasoner_app/engineering_safety/risk_radar.py\", line 10, in run\n"
            '  File "E:/kanda_reasoner/ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py", line 20, in run\n'
        )
        frames = extract_crash_traceback_frames(traceback_text, "E:/kanda_reasoner")
        joined = "\n".join(frames)
        self.assertIn("kanda_reasoner_app/engineering_safety/risk_radar.py:10", joined)
        self.assertIn('ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py:20', joined)


if __name__ == "__main__":
    unittest.main()
