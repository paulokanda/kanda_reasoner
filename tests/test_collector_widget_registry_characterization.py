from __future__ import annotations

from kanda_reasoner_app.reasoner_context_collector import collector_widget_registry
from kanda_reasoner_app.reasoner_context_collector.collector_widget_registry import (
    build_widget_registry,
)


def _record_by_variable(
    registry: dict[str, dict[str, object]],
    variable_name: str,
) -> dict[str, object]:
    matches = [
        record
        for record in registry.values()
        if record.get("variable_name") == variable_name
    ]
    assert len(matches) == 1
    return matches[0]


def _records_by_type(
    registry: dict[str, dict[str, object]],
    widget_type: str,
) -> list[dict[str, object]]:
    return [
        record
        for record in registry.values()
        if record.get("widget_type") == widget_type
    ]


def test_public_contract_exposes_build_widget_registry_only() -> None:
    assert collector_widget_registry.__all__ == ["build_widget_registry"]
    assert build_widget_registry([]) == {}


def test_widget_registry_captures_assignments_and_property_setters() -> None:
    source = """
class Demo:
    def build(self):
        self.button = QPushButton("Run", self)
        self.button.setText("Launch")
        self.button.setToolTip("Run now")
        self.edit = QLineEdit(parent=self)
        self.edit.setPlaceholderText("Name")
        self.edit.setObjectName("name_edit")
        self.combo = QComboBox()
        self.combo.addItems(["One", "Two"])
        self.table = QTableWidget()
        self.table.setHeaderLabels(["A", "B"])
"""

    registry = build_widget_registry([{"path": "demo.py", "source": source}])

    button = _record_by_variable(registry, "button")
    assert button["widget_type"] == "QPushButton"
    assert button["widget_ref"] == "self.button"
    assert button["display_text"] == "Launch"
    assert button["tooltip_text"] == "Run now"
    assert button["container_widget"] == "self"
    assert button["source_symbol"] == "Demo.build"
    assert button["class_name"] == "Demo"
    assert button["method_name"] == "build"

    edit = _record_by_variable(registry, "edit")
    assert edit["widget_type"] == "QLineEdit"
    assert edit["placeholder_text"] == "Name"
    assert edit["object_name"] == "name_edit"

    combo = _record_by_variable(registry, "combo")
    assert combo["items"] == ["One", "Two"]

    table = _record_by_variable(registry, "table")
    assert table["header_labels"] == ["A", "B"]


def test_widget_registry_captures_layout_positions_rows_and_tabs() -> None:
    source = """
class Demo:
    def build(self):
        self.button = QPushButton("Run")
        self.edit = QLineEdit()
        grid = QGridLayout()
        grid.addWidget(self.button, 1, 2, 3, 4)
        form = QFormLayout()
        form.addRow(QLabel("User"), self.edit)
        tabs = QTabWidget()
        tabs.addTab(QLabel("Page Body"), "Main")
"""

    registry = build_widget_registry([{"path": "layout_demo.py", "source": source}])

    button = _record_by_variable(registry, "button")
    assert button["parent_layout"] == "grid"
    assert button["layout_kind"] == "layout_add_widget"
    assert button["layout_position"] == {
        "row": 1,
        "col": 2,
        "row_span": 3,
        "col_span": 4,
    }
    assert button["layout_records"] == [
        {
            "parent_layout": "grid",
            "layout_kind": "layout_add_widget",
            "layout_position": {
                "row": 1,
                "col": 2,
                "row_span": 3,
                "col_span": 4,
            },
            "line": 6,
        }
    ]

    edit = _record_by_variable(registry, "edit")
    assert edit["parent_layout"] == "form"
    assert edit["layout_kind"] == "form_row_field"
    assert edit["layout_position"] == {"role": "field"}

    inline_labels = _records_by_type(registry, "QLabel")
    label_texts = {record["display_text"] for record in inline_labels}
    assert label_texts == {"User", "Page Body"}

    page_label = next(
        record for record in inline_labels if record["display_text"] == "Page Body"
    )
    assert page_label["parent_layout"] == "tabs"
    assert page_label["layout_kind"] == "tab_page"
    assert page_label["layout_position"] == {"tab_text": "Main"}
    assert page_label["tab_texts"] == [{"index": None, "text": "Main", "line": 10}]


def test_widget_registry_skips_invalid_or_empty_file_payloads() -> None:
    registry = build_widget_registry(
        [
            {"path": "", "source": "button = QPushButton('Ignored')"},
            {"path": "broken.py", "source": "def broken("},
            {"path": "valid.py", "source": "button = QPushButton('Run')"},
        ]
    )

    assert list(registry) == ["valid.py::<module>::button"]
    assert registry["valid.py::<module>::button"]["display_text"] == "Run"
