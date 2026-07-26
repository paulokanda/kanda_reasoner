"""Validate cancel-button font-only styling for architecture workflow controls."""

import re
from pathlib import Path

__all__: list[str] = []


ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / 'kanda_reasoner_app' / 'manage_architecture' / 'manage_architecture_gui.py'
WORK = ROOT / 'kanda_reasoner_app' / 'manage_workflows' / 'manage_workflows_gui_help' / 'workflow_gui_window.py'

FORBIDDEN_IN_CANCEL_STYLE = (
    'background:',
    'border:',
    'border-color:',
    'border-radius:',
    'padding:',
    'color: white',
)

REQUIRED_SNIPPETS = (
    "QPushButton('Cancel')",
    "setObjectName(",
    "setEnabled(False)",
    "clicked.connect(self.cancel_running_operation)",
    "color: #C2185B",
    "font-weight: bold",
)

BEHAVIOR_SNIPPETS = (
    "requestInterruption()",
    ".quit()",
    ".terminate()",
    "_cancel_requested",
    "_cancel_operation_button.setEnabled",
)


def _cancel_style_literals(text: str) -> str:
    match = re.search(
        r"self\._cancel_operation_button\.setStyleSheet\(\s*(?P<body>.*?)\n\s*\)",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError('Cancel setStyleSheet block not found')
    return match.group('body')


def _check_file(path: Path, label: str) -> None:
    text = path.read_text(encoding='utf-8')
    missing = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in text]
    if missing:
        raise AssertionError(f'{label} missing required cancel snippets: {missing}')

    style_body = _cancel_style_literals(text)
    if "QPushButton { color: #C2185B; font-weight: bold; }" not in style_body:
        raise AssertionError(f'{label} Cancel style must be font-only magenta with no background/border override')

    present = [token for token in FORBIDDEN_IN_CANCEL_STYLE if token in style_body and token != 'color:']
    if present:
        raise AssertionError(
            f'{label} Cancel style still overrides filled-button visuals instead of font-only: {present}'
        )

    if "QPushButton:disabled { color: #9A9A9A; }" not in style_body:
        raise AssertionError(f'{label} Cancel disabled style must keep only font color override')

    missing_behavior = [snippet for snippet in BEHAVIOR_SNIPPETS if snippet not in text]
    if missing_behavior:
        raise AssertionError(f'{label} lost protected cancel behavior snippets: {missing_behavior}')



def main() -> None:
    _check_file(ARCH, 'Architecture')
    _check_file(WORK, 'Workflow Review')
    print('VALIDATION OK: architecture-workflow-cancel-font-only-v1')


if __name__ == '__main__':
    main()
