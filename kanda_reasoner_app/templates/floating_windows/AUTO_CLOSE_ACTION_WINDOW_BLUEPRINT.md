# Silent Auto-Close Action Floating Window Blueprint

## Purpose

Use this template for small post-action floating windows that only inform the user that an action finished. The window appears, stays visible for about 3 seconds by default, then closes automatically.

If a follow-up command is linked to the window close, that command runs automatically when the window closes. The command also runs if the user clicks the optional OK button before the timer ends.

## Sound policy

This template is silent by default.

It must not use `QMessageBox`, `QApplication.beep`, native message-box icons, operating-system notification sounds, or dialog patterns that create a Windows alert sound when the message closes.

The OK button is not a default dialog button. Timer close, OK click, Escape close, and programmatic close all use the same silent close path.

## When to use

Use this pattern for success or low-risk status messages such as:

- Local freeze written.
- Settings saved.
- Export finished.
- Temporary helper completed.

## When not to use

Do not use this pattern as a human confirmation gate.

For governed writes, destructive actions, freeze confirmation, deletion, replacement, irreversible changes, or any action that needs deliberate human approval, keep a normal confirmation dialog before the action happens.

The auto-close window belongs after the action has already completed successfully.

## Behavior contract

1. Default timeout is 3000 ms.
2. The user can click OK to close earlier.
3. The linked close command runs exactly once.
4. The linked close command runs on timer close, OK click, Escape close, window-manager close, or programmatic close.
5. Closing is silent and must not play the Windows alert sound.
6. The template must not bypass Preview, Confirm and Write, or any other confirmation gate.
7. The template should be stored under `kanda_reasoner_app/templates/floating_windows/`.
8. The caller owns the decision about which close command is safe to run.

## Example: Local freeze written

The Confirm local freeze write dialog remains a normal confirmation gate. After the freeze is written and AI startup context is refreshed, replace the final information dialog with a silent auto-close action window:

```python
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window

show_auto_close_action_window(
    self,
    title="Local freeze written",
    message="Freeze entry written successfully and AI startup freeze context was refreshed.",
    detail_text="This message will close automatically.",
    timeout_ms=3000,
    button_text="OK",
    on_close=dialog.close,
)
```

In this example, closing the small "Local freeze written" window automatically closes the parent "New Local Freeze Entry" window through the linked `dialog.close` command.

## Import path

```python
from kanda_reasoner_app.templates.floating_windows import (
    AutoCloseActionFloatingWindow,
    show_auto_close_action_window,
)
```

## Implementation file

```text
kanda_reasoner_app/templates/floating_windows/auto_close_action_window.py
```
