# Copy Message Floating Window Blueprint

## Purpose

Use this template when a long diagnostic message should be preserved by the user before the window closes.

The window has one action button:

```text
Copy
```

Pressing Copy writes the complete configured message to the clipboard and then closes the window.

## Current scope

This patch only creates the reusable template. The template is not inserted into Error Memory, Freeze Feature After Update, or any other existing caller.

## When to use

Use this pattern for long, copy-worthy messages such as:

- active-ready lesson validation failures;
- import or freeze diagnostics;
- generated-intake validation errors;
- any message the user may need to paste back into AI as raw evidence.

## When not to use

Do not use this pattern as a confirmation gate.

Do not use it for destructive actions, governed write confirmation, deletion confirmation, or any prompt where the user must explicitly approve a change before it happens.

## Behavior contract

1. The action row must contain Copy, not OK and not Close.
2. Pressing Copy must copy the complete configured message text to the clipboard.
3. Pressing Copy must close the window after the clipboard action.
4. The template must not use native message-box widgets, native alert icons, application beep calls, or operating-system notification sounds.
5. The displayed message must remain selectable by mouse.
6. The template must be reusable for multiple features without embedding Error Memory-specific text.
7. The template must not be inserted into existing workflows until a separate explicit caller patch is requested.
8. The caller owns whether the window is modal and what exact text is copied.

## Import path

```python
from kanda_reasoner_app.templates.floating_windows.clipboard_message_window import (
    CopyMessageFloatingWindow,
    show_copy_message_window,
)
```

## Example only - not installed by this template patch

```python
show_copy_message_window(
    self,
    title="Formatted lesson is not active-ready",
    message=active_ready_diagnostic_text,
    clipboard_text=active_ready_diagnostic_text,
)
```

## Implementation file

```text
kanda_reasoner_app/templates/floating_windows/clipboard_message_window.py
```
