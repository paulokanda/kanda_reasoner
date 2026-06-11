"""Screen-aware startup sizing helpers for the main tools window."""

from __future__ import annotations

__all__ = [
    "calculate_safe_startup_size",
    "calculate_screen_fraction_size",
    "resize_window_for_primary_screen",
    "set_widget_size_pressure_limit",
    "release_widget_size_pressure_limit",
    "resize_window_to_screen_fraction_unlocked",
    "shrink_window_to_screen_fraction",
]


def calculate_safe_startup_size(
    available_width: int,
    available_height: int,
    preferred_width: int = 1900,
    preferred_height: int = 1100,
    width_ratio: float = 0.80,
    height_ratio: float = 0.80,
    minimum_width: int = 1100,
    minimum_height: int = 720,
) -> tuple[int, int]:
    """Return a startup size that fits inside one monitor.

    Parameters
    ----------
    available_width : int
        Width available on the selected screen.
    available_height : int
        Height available on the selected screen.
    preferred_width : int, optional
        Desired width before screen clamping.
    preferred_height : int, optional
        Desired height before screen clamping.
    width_ratio : float, optional
        Maximum fraction of available screen width to use.
    height_ratio : float, optional
        Maximum fraction of available screen height to use.
    minimum_width : int, optional
        Preferred minimum width, clamped to available width if necessary.
    minimum_height : int, optional
        Preferred minimum height, clamped to available height if necessary.

    Returns
    -------
    tuple[int, int]
        Width and height that do not exceed one monitor's available geometry.
    """
    safe_available_width = max(1, int(available_width))
    safe_available_height = max(1, int(available_height))

    ratio_width = max(1, int(safe_available_width * width_ratio))
    ratio_height = max(1, int(safe_available_height * height_ratio))

    max_width = min(preferred_width, ratio_width, safe_available_width)
    max_height = min(preferred_height, ratio_height, safe_available_height)

    width = max(minimum_width, max_width)
    height = max(minimum_height, max_height)

    width = min(width, safe_available_width)
    height = min(height, safe_available_height)

    return width, height


def calculate_screen_fraction_size(
    available_width: int,
    available_height: int,
    width_ratio: float = 2.0 / 3.0,
    height_ratio: float = 2.0 / 3.0,
    minimum_width: int = 900,
    minimum_height: int = 620,
) -> tuple[int, int]:
    """Return a target window size based on one monitor fraction.

    The returned size is always clamped to the available screen geometry.
    On small displays, the preferred minimum is also clamped so the window
    never spans more than one monitor.
    """
    safe_available_width = max(1, int(available_width))
    safe_available_height = max(1, int(available_height))

    target_width = max(1, int(safe_available_width * width_ratio))
    target_height = max(1, int(safe_available_height * height_ratio))

    width = max(minimum_width, target_width)
    height = max(minimum_height, target_height)

    width = min(width, safe_available_width)
    height = min(height, safe_available_height)

    return width, height


def resize_window_for_primary_screen(
    window,
    preferred_width: int = 1900,
    preferred_height: int = 1100,
) -> tuple[int, int]:
    """Resize a Qt window so initial size fits on one monitor.

    The function prefers the window's current screen, falls back to the
    application's primary screen, and finally falls back to a conservative
    static size if screen geometry is unavailable.
    """
    fallback_size = (1400, 900)

    try:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance()
        screen = None
        if hasattr(window, "screen"):
            screen = window.screen()
        if screen is None and app is not None:
            screen = app.primaryScreen()
        if screen is None:
            width, height = fallback_size
        else:
            available = screen.availableGeometry()
            width, height = calculate_safe_startup_size(
                available.width(),
                available.height(),
                preferred_width=preferred_width,
                preferred_height=preferred_height,
            )
    except Exception:
        width, height = fallback_size

    window.resize(width, height)
    return width, height


def _screen_available_geometry(window):
    """Return the best available geometry object for a Qt window."""
    try:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance()
        screen = None
        if hasattr(window, "screen"):
            screen = window.screen()
        if screen is None and app is not None:
            screen = app.primaryScreen()
        if screen is None:
            return None
        return screen.availableGeometry()
    except Exception:
        return None


def set_widget_size_pressure_limit(widget, width: int, height: int) -> None:
    """Reduce child size pressure without blocking user resizing.

    The widget is allowed to grow when the user resizes the main window. The
    important part is to remove large minimum-size pressure during the initial
    Tab 3 layout pass.
    """
    if widget is None:
        return

    try:
        from PySide6.QtWidgets import QSizePolicy

        widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    except Exception:
        pass

    method = getattr(widget, "setMinimumSize", None)
    if callable(method):
        try:
            method(0, 0)
        except Exception:
            pass


def release_widget_size_pressure_limit(widget) -> None:
    """Release size-pressure limits previously applied to a child widget."""
    if widget is None:
        return

    try:
        from PySide6.QtWidgets import QSizePolicy

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    except Exception:
        pass

    method = getattr(widget, "setMaximumSize", None)
    if callable(method):
        try:
            method(16777215, 16777215)
        except Exception:
            pass


def resize_window_to_screen_fraction_unlocked(
    window,
    width_ratio: float = 0.80,
    height_ratio: float = 0.80,
) -> tuple[int, int]:
    """Resize a top-level window inside one monitor without locking it.

    This helper is intentionally different from a geometry lock. It moves and
    resizes the window to a safe fraction of the current monitor, then releases
    maximum-size limits so the user can still maximize, minimize, and manually
    resize the window by dragging its borders.
    """
    fallback_size = (1400, 850)
    available = _screen_available_geometry(window)

    if available is None:
        target_width, target_height = fallback_size
        available_x = 0
        available_y = 0
        available_width = target_width
        available_height = target_height
    else:
        available_x = int(available.x())
        available_y = int(available.y())
        available_width = int(available.width())
        available_height = int(available.height())
        target_width, target_height = calculate_screen_fraction_size(
            available_width,
            available_height,
            width_ratio=width_ratio,
            height_ratio=height_ratio,
            minimum_width=1100,
            minimum_height=720,
        )

    try:
        if callable(getattr(window, "isMaximized", None)) and window.isMaximized():
            return target_width, target_height
    except Exception:
        pass

    for method_name, args in (
        ("setMinimumSize", (0, 0)),
        ("setMaximumSize", (16777215, 16777215)),
    ):
        method = getattr(window, method_name, None)
        if callable(method):
            try:
                method(*args)
            except Exception:
                pass

    try:
        window.resize(target_width, target_height)
    except Exception:
        pass

    try:
        x_pos = available_x + max(0, (available_width - target_width) // 2)
        y_pos = available_y + max(0, (available_height - target_height) // 2)
        window.move(x_pos, y_pos)
    except Exception:
        pass

    return target_width, target_height

def shrink_window_to_screen_fraction(
    window,
    width_ratio: float = 2.0 / 3.0,
    height_ratio: float = 2.0 / 3.0,
    only_shrink: bool = True,
) -> tuple[int, int]:
    """Shrink a Qt window to a fraction of one monitor when needed.

    Parameters
    ----------
    window
        Qt window to resize.
    width_ratio : float, optional
        Fraction of available monitor width to use.
    height_ratio : float, optional
        Fraction of available monitor height to use.
    only_shrink : bool, optional
        When true, do not enlarge smaller windows.

    Returns
    -------
    tuple[int, int]
        Final requested window width and height.
    """
    fallback_size = (1200, 760)

    try:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance()
        screen = None
        if hasattr(window, "screen"):
            screen = window.screen()
        if screen is None and app is not None:
            screen = app.primaryScreen()

        if screen is None:
            target_width, target_height = fallback_size
        else:
            available = screen.availableGeometry()
            target_width, target_height = calculate_screen_fraction_size(
                available.width(),
                available.height(),
                width_ratio=width_ratio,
                height_ratio=height_ratio,
            )
    except Exception:
        target_width, target_height = fallback_size

    current_width = 0
    current_height = 0
    try:
        current_width = int(window.width())
        current_height = int(window.height())
    except Exception:
        current_width = 0
        current_height = 0

    if only_shrink and current_width and current_height:
        final_width = min(current_width, target_width)
        final_height = min(current_height, target_height)
    else:
        final_width = target_width
        final_height = target_height

    window.resize(final_width, final_height)
    return final_width, final_height
