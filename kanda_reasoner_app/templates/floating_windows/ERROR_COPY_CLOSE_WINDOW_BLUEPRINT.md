# Error Copy-Close Floating Window Blueprint

## Purpose

Use this template for error floating windows that show a problem and need a simple Copy Close button.

The Copy Close button must do two things in this exact order:

1. Copy the complete error text from the window to the clipboard.
2. Close the window silently.

This removes the extra manual copy step when the user needs to paste an error into chat, Error Memory, a bug report, or a validation log.

## Sound policy

This template avoids native message boxes and system alert behavior.

Do not use `QMessageBox.critical`, `QMessageBox.warning`, `QApplication.beep`, or native message-box icons inside this template. The button must close through the template close path, not through a native message-box accept path.

## When to use

Use this pattern for error windows where the next likely action is to copy the error text somewhere else, for example:

- A validation command failed.
- A patch install failed.
- A source file could not be read.
- A GUI operation raised an exception.
- A local write failed and the user may need to paste the error into chat.

## When not to use

Do not use this pattern for success/completion messages. Use `show_auto_close_action_window` for those.

Do not use this pattern as a confirmation gate. Confirmation gates must remain explicit and must not copy text as a side effect.

Do not use this template to write Error Memory automatically. It only copies text to the clipboard.

## Behavior contract

1. The window is not auto-closing.
2. The Copy Close button copies the complete diagnostic text to the clipboard.
3. After the copy attempt, the Copy Close button closes the window.
4. The Copy Close button is not a default native dialog button.
5. The template must not trigger Windows message-box sounds.
6. The full clipboard text must include the title, message, details, context, traceback, and visible note when those fields are provided.
7. Window-manager close and Escape close may close without copying, because the user did not click OK.
8. Optional `on_close` runs exactly once after the window closes.
9. The template is stored under `kanda_reasoner_app/templates/floating_windows/`.

## Import path

```python
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
```

## Example

```python
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

show_error_copy_close_window(
    self,
    title="Validation error",
    message="The validation command failed.",
    detail_text="Expected marker was not found.",
    traceback_text=traceback_text,
    context_text="Feature: freeze-local-entry-action-buttons-v1",
    button_text="Copy Close",
)
```

When the user clicks Copy Close, the complete text is copied to the clipboard and the window closes.

## Implementation file

```text
kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py
```
