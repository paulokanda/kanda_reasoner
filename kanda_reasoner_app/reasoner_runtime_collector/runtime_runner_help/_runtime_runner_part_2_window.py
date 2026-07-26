# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_2_window.py
"""Qt window behavior for runtime runner part 2."""

from __future__ import annotations

from ._runtime_runner_part_2_bindings import RuntimeRunnerPart2Bindings

__all__: list[str] = []

_SPINNER_FRAMES = ("-", "\\", "|", "/")

def _no_op_slot(*types: object):
    """Provide an import-safe no-op slot decorator when Qt is absent."""
    del types

    def decorate(function):
        return function

    return decorate


def _load_qt_bindings() -> tuple[object, ...]:
    """Load one supported Qt family without rebinding imported symbols."""
    try:
        import PySide6.QtCore as pyside_core
        import PySide6.QtWidgets as pyside_widgets
    except ImportError:
        try:
            import PyQt6.QtCore as pyqt_core
            import PyQt6.QtWidgets as pyqt_widgets
        except ImportError:
            return (None, _no_op_slot, None, None, None, None, None, object)
        return (
            pyqt_core.QMetaObject,
            pyqt_core.pyqtSlot,
            pyqt_widgets.QFileDialog,
            pyqt_widgets.QGridLayout,
            pyqt_widgets.QHBoxLayout,
            pyqt_widgets.QLabel,
            pyqt_widgets.QVBoxLayout,
            pyqt_widgets.QWidget,
        )
    return (
        pyside_core.QMetaObject,
        pyside_core.Slot,
        pyside_widgets.QFileDialog,
        pyside_widgets.QGridLayout,
        pyside_widgets.QHBoxLayout,
        pyside_widgets.QLabel,
        pyside_widgets.QVBoxLayout,
        pyside_widgets.QWidget,
    )


(
    QMetaObject,
    Slot,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
) = _load_qt_bindings()


class _RuntimeCollectorCentralWidget(QWidget):
    """Central widget whose named slots preserve the control wiring contract."""

    def __init__(self, owner) -> None:
        super().__init__()
        self._owner = owner

    @Slot()
    def on_browse_project_button_clicked(self) -> None:
        """Dispatch project-root browsing to the public window owner."""
        self._owner._browse_project_root()

    @Slot()
    def on_browse_output_button_clicked(self) -> None:
        """Dispatch output browsing to the public window owner."""
        self._owner._browse_output_json()

    @Slot()
    def on_browse_entry_button_clicked(self) -> None:
        """Dispatch entry-script browsing to the public window owner."""
        self._owner._browse_entry_script()

    @Slot()
    def on_configure_button_clicked(self) -> None:
        """Dispatch trace configuration to the public window owner."""
        self._owner._configure_trace()

    @Slot()
    def on_save_button_clicked(self) -> None:
        """Dispatch trace saving to the public window owner."""
        self._owner._save_trace()

    @Slot()
    def on_close_button_clicked(self) -> None:
        """Close the public runtime collector window."""
        self._owner.close()


def build_ui(bindings: RuntimeRunnerPart2Bindings, owner) -> None:
    """Build the runtime collector central widget and layouts."""
    del bindings
    central = _RuntimeCollectorCentralWidget(owner)
    owner.setCentralWidget(central)
    owner._runtime_runner_part2_button_names = [
        (owner.browse_project_button, owner.browse_project_button.objectName()),
        (owner.browse_output_button, owner.browse_output_button.objectName()),
        (owner.browse_entry_button, owner.browse_entry_button.objectName()),
        (owner.configure_button, owner.configure_button.objectName()),
        (owner.save_button, owner.save_button.objectName()),
        (owner.close_button, owner.close_button.objectName()),
    ]
    owner.browse_project_button.setObjectName("browse_project_button")
    owner.browse_output_button.setObjectName("browse_output_button")
    owner.browse_entry_button.setObjectName("browse_entry_button")
    owner.configure_button.setObjectName("configure_button")
    owner.save_button.setObjectName("save_button")
    owner.close_button.setObjectName("close_button")
    main_layout = QVBoxLayout(central)
    grid = QGridLayout()
    grid.addWidget(QLabel("Project root:"), 0, 0)
    grid.addWidget(owner.project_root_edit, 0, 1)
    grid.addWidget(owner.browse_project_button, 0, 2)
    grid.addWidget(QLabel("Output JSON:"), 1, 0)
    grid.addWidget(owner.output_json_edit, 1, 1)
    grid.addWidget(owner.browse_output_button, 1, 2)
    grid.addWidget(QLabel("Entry script:"), 2, 0)
    grid.addWidget(owner.entry_script_edit, 2, 1)
    grid.addWidget(owner.browse_entry_button, 2, 2)
    button_row = QHBoxLayout()
    button_row.addStretch()
    button_row.addWidget(owner.configure_button)
    button_row.addWidget(owner.save_button)
    button_row.addWidget(owner.close_button)
    main_layout.addLayout(grid)
    main_layout.addLayout(button_row)
    main_layout.addWidget(QLabel("Log:"))
    main_layout.addWidget(owner.log_box)


def connect_signals(bindings: RuntimeRunnerPart2Bindings, owner) -> None:
    """Connect named child controls through Qt auto-connect semantics."""
    del bindings
    central = owner.centralWidget()
    if QMetaObject is None:
        raise RuntimeError("Qt bindings are required for runtime window wiring.")
    QMetaObject.connectSlotsByName(central)
    for button, prior_name in owner._runtime_runner_part2_button_names:
        button.setObjectName(prior_name)
    owner._runtime_runner_part2_button_names = []


def append_log(owner, text: str) -> None:
    """Append text and keep the log view scrolled to its maximum."""
    owner.log_box.appendPlainText(str(text))
    scroll_bar = owner.log_box.verticalScrollBar()
    scroll_bar.setValue(scroll_bar.maximum())


def start_spinner(owner) -> None:
    """Start spinner state and reserve its output line."""
    owner._append_log("")
    document = owner.log_box.document()
    owner._spinner_line = document.blockCount() - 1
    owner._spinner_frame = 0
    owner._spinner_timer.start()


def tick_spinner(owner) -> None:
    """Advance the spinner and update its display line."""
    frame = _SPINNER_FRAMES[owner._spinner_frame % len(_SPINNER_FRAMES)]
    owner._spinner_frame += 1
    owner._update_spinner_line(f"{frame}  Saving trace...")


def update_spinner_line(owner, text: str) -> None:
    """Replace the current spinner line with text."""
    document = owner.log_box.document()
    block = document.findBlockByNumber(owner._spinner_line)
    cursor = owner.log_box.textCursor()
    cursor.setPosition(block.position())
    cursor.movePosition(
        cursor.MoveOperation.EndOfBlock,
        cursor.MoveMode.KeepAnchor,
    )
    cursor.insertText(text)


def stop_spinner(owner) -> None:
    """Stop spinner state and replace its line with success evidence."""
    owner._spinner_timer.stop()
    if owner._spinner_line >= 0:
        owner._update_spinner_line("[OK] Trace saved.")
        owner._spinner_line = -1


def browse_project_root(
    bindings: RuntimeRunnerPart2Bindings,
    owner,
) -> None:
    """Choose a project root and persist the resulting preferences."""
    folder = QFileDialog.getExistingDirectory(
        owner,
        "Select project root",
        owner.project_root_edit.text().strip()
        or str(bindings.default_project_root),
    )
    if folder:
        owner.project_root_edit.setText(folder)
        bindings.save_prefs(
            folder,
            owner.output_json_edit.text().strip(),
            owner.entry_script_edit.text().strip(),
        )


def browse_output_json(
    bindings: RuntimeRunnerPart2Bindings,
    owner,
) -> None:
    """Choose an output JSON file and persist the resulting preferences."""
    file_path, _selected_filter = QFileDialog.getSaveFileName(
        owner,
        "Select output JSON",
        owner.output_json_edit.text().strip()
        or str(bindings.default_output_json),
        "JSON Files (*.json)",
    )
    if file_path:
        owner.output_json_edit.setText(file_path)
        bindings.save_prefs(
            owner.project_root_edit.text().strip(),
            file_path,
            owner.entry_script_edit.text().strip(),
        )
