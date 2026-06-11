# hvr_card_widget — Gorgeous Hover‑Cards for Middle‑Tab Comboboxes

> This module powers your **gorgeous** tooltip system: interactive hover‑cards attached **directly to each combobox header** in the middle tab. Use it **together** with your **simple** native Qt tips on the Core/Pro button‑system menus.

---

## What this file provides

**ThemeManager**
Minimal light/dark palette and CSS snippets so cards/dialogs look modern and consistent.

**GorgeousHoverCard**
Top‑level, translucent widget (tooltip‑like) with fade‑in animation, a rich text body, and a bottom‑right help icon to open a detail dialog.

**GorgeousDetailDialog**
A modal, scrollable dialog for deep dives (opened from the hover‑card’s help icon).

**HoverTipController**
A tiny bridge that binds a target widget (e.g., a `QComboBox`) to a `GorgeousHoverCard` using a **provider()** function that returns the card payload at show‑time.

**Positioning & Safety**
Smart screen‑aware placement, fade‑in/out animations, and crisp SVG icon loading with multiple fallback paths via `HOVER_CARD_SVG` env var.

---

## How it fits your two tooltip systems

1) **Simple tooltips — Core/Pro button system**  
   Assign short, native tips on each **menu action** (`QAction.setToolTip(...)`) when you build the Core/Pro menus in your template. These appear **before** the lane exists and should be instant and concise.

2) **Gorgeous hover‑cards — Lane combobox headers**  
   Attach one `GorgeousHoverCard` **per combobox** after the lane is rebuilt. The card is interactive and value‑aware and should reflect the **current** state of that dropdown.

---

## Integration recipe (copy/paste)

### 1) A tiny hover guard
Route enter/leave to the controller. Store on the widget so the lane‑clear routine can remove it safely.

```python
from PySide6.QtCore import QObject, QEvent

class _SimpleHoverGuard(QObject):
    def __init__(self, controller):
        super().__init__()
        self._ctl = controller

    def eventFilter(self, obj, ev):
        et = ev.type()
        if et == QEvent.Enter:
            self._ctl.show()
        elif et in (QEvent.Leave, QEvent.Hide, QEvent.FocusOut):
            self._ctl.hide()
        elif et == QEvent.Destroyed:
            self._ctl.stop()
        return False
```

### 2) Provider for each dropdown
Generate the **title/summary** dynamically (e.g., using your caption affixes).

```python
def make_provider(template, key, label, dd):
    def _provider():
        value = template.current_value_str(dd)  # normalize value for display
        pre, suf = template.get_caption_affixes(key=key, label=label)  # optional
        title = f"{pre}{value}{suf}" if (pre or suf) else (label or "Details")
        return {
            "title": title,
            "summary": template.summary_for(key) or "Hover for quick help. Click the icon for details.",
            "subject": label or key,
            "html": template.detail_html_for(key)  # optional: rich HTML for the dialog
        }
    return _provider
```

### 3) Attach per combobox during lane rebuild
Call this right after each `KandaDropdown` is created.

```python
from hvr_card_widget import ThemeManager, GorgeousHoverCard, HoverTipController

def attach_hover_card(dropdown, key, label, template):
    theme = ThemeManager(mode=template.theme_mode())  # "dark" or "light"
    card  = GorgeousHoverCard(theme=theme)
    ctl   = HoverTipController(dropdown, card, make_provider(template, key, label, dropdown))

    guard = _SimpleHoverGuard(ctl)
    dropdown.installEventFilter(guard)

    # Register on the widget for symmetric teardown on lane clear
    dropdown._hover_tip_guard = guard
    dropdown._hover_tip_adapter = ctl
```

### 4) Teardown on lane clear
Your lane‑clear routine should look for these attributes and stop/hide/delete safely:

```python
def teardown_hover_card(dropdown):
    guard = getattr(dropdown, "_hover_tip_guard", None)
    ctl   = getattr(dropdown, "_hover_tip_adapter", None)
    if ctl: 
        try: ctl.stop()
        except Exception: pass
        delattr(dropdown, "_hover_tip_adapter")
    if guard:
        try: dropdown.removeEventFilter(guard)
        except Exception: pass
        delattr(dropdown, "_hover_tip_guard")
```

---

## Header‑area hover‑cards (optional)
You can attach a single `GorgeousHoverCard` to Core/Pro **header buttons** as well—use the same `HoverTipController` plus a provider keyed by the header name (e.g., “Core Filters”). If you prefer native tips on headers, keep them as `setToolTip(...)` and reserve hover‑cards for the combobox lane.

---

## Notes & best practices

- **One card per widget**. Reuse the same `GorgeousHoverCard` for a dropdown; don’t allocate on every Enter event.
- **Attach after layout settles**. Use a `QTimer.singleShot(0, ...)` from your lane rebuild to avoid geometry races; the controller computes a safe global position each time it shows.
- **Store guard & controller**. Always set `_hover_tip_guard` and `_hover_tip_adapter` so the lane‑clear routine can stop and detach cleanly.
- **Keep simple tips short**. Reserve hover‑cards for rich text; simple tips should be terse and instant.
- **Testing**. In CI or tests, set `PYTEST_CURRENT_TEST` to disable fade animations for deterministic UI timing.

---

## Minimal working demo

```python
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
    app = QApplication([])

    win = QWidget(); win.setWindowTitle("Hover Card Demo")
    lay = QVBoxLayout(win)

    combo = QComboBox(); combo.addItems(["Option 1", "Option 2", "Option 3"])
    lay.addWidget(combo)

    # Reuse the recipe above
    attach_hover_card(combo, key="viz.gain", label="Gain", template=YourTemplate())

    win.show()
    app.exec()
```

> Replace `YourTemplate()` helpers with your own (e.g., `current_value_str`, `get_caption_affixes`, `summary_for`, `detail_html_for`).

---

## Troubleshooting

- Card appears far from the widget → install the hover guard after the dropdown is added to the layout so geometry is final.
- No card on hover → ensure the event filter is installed and the provider returns at least a `title` or `summary`.
- Orphan windows after lane rebuild → verify you call `ctl.stop()` and remove the event filter in your lane‑clear.

---

## At a glance

- **Simple tips** → set on `QAction`s when building Core/Pro menus.  
- **Gorgeous hover‑cards** → attach to `KandaDropdown`s with `HoverTipController` + provider; teardown on lane clear.
- **Detail dialog** → click the card’s help icon to open rich, scrollable content.

