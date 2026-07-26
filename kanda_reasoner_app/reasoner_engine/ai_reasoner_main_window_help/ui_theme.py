# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_theme.py
"""Professional dark theme for the Local AI project-reasoner surface."""

from __future__ import annotations

__all__ = ["LOCAL_AI_THEME"]


LOCAL_AI_THEME = """
QMainWindow#localAITab, QWidget#localAIScrollableBody {
    background: #0d0d0d;
    color: #eef1f5;
    font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;
    font-size: 13px;
}
QFrame#localAISidebar {
    background: #111318;
    border-right: 1px solid #252932;
}
QFrame#localAIChatCanvas {
    background: #0d0d0d;
}
QFrame#localAIHeader {
    background: #0f1115;
    border-bottom: 1px solid #252932;
}
QFrame#localAISection {
    background: #171a20;
    border: 1px solid #292e38;
    border-radius: 12px;
}
QFrame#localAIComposerFrame {
    background: #1a1e25;
    border: 1px solid #343b47;
    border-radius: 20px;
}
QFrame#localAIDivider {
    background: #252932;
    min-height: 1px;
    max-height: 1px;
}
QLabel {
    color: #eef1f5;
    background: transparent;
}
QLabel#localAITitle {
    color: #f8fafc;
    font-size: 20px;
    font-weight: 700;
}
QLabel#localAISubtitle {
    color: #8f98a6;
    font-size: 12px;
}
QLabel#localAISectionTitle {
    color: #dce2ea;
    font-size: 12px;
    font-weight: 650;
}
QLabel#localAIMuted {
    color: #929baa;
    font-size: 12px;
}
QLabel#localAIStatus {
    color: #aeb6c2;
    padding: 2px 0;
    font-size: 12px;
}
QLabel#localAIBadge {
    color: #9fe3d0;
    background: #17372f;
    border: 1px solid #245447;
    border-radius: 9px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 700;
}
QLineEdit, QPlainTextEdit#localAISideText {
    background-color: #20242b;
    color: #f4f6f8;
    border: 1px solid #343a45;
    border-radius: 8px;
    padding: 8px;
    selection-background-color: #355e55;
}
QLineEdit:focus, QPlainTextEdit#localAISideText:focus {
    border: 1px solid #5e8f82;
    background-color: #232831;
}
QComboBox {
    background-color: #20242b;
    color: #f4f6f8;
    border: 1px solid #343a45;
    border-radius: 8px;
    padding: 8px 30px 8px 10px;
    min-height: 18px;
    selection-background-color: #355e55;
}
QComboBox:hover, QComboBox:on {
    background-color: #272c35;
    border-color: #4b5361;
}
QComboBox:focus {
    background-color: #272c35;
    border: 1px solid #5e8f82;
}
QComboBox::drop-down {
    background-color: #20242b;
    border: 0;
    border-left: 1px solid #343a45;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    width: 27px;
}
QComboBox QAbstractItemView {
    background-color: #1d2128;
    color: #f4f6f8;
    border: 1px solid #3d4552;
    outline: 0;
    padding: 5px;
    selection-background-color: #2f4f48;
    selection-color: #ffffff;
}
QComboBox QAbstractItemView::item {
    background-color: #1d2128;
    color: #f4f6f8;
    min-height: 30px;
    padding: 5px 10px;
}
QComboBox QAbstractItemView::item:hover,
QComboBox QAbstractItemView::item:selected {
    background-color: #2f4f48;
    color: #ffffff;
}
QPushButton {
    background: #222730;
    color: #e8edf3;
    border: 1px solid #383f4b;
    border-radius: 8px;
    padding: 8px 11px;
    font-weight: 550;
}
QPushButton:hover {
    background: #2b313c;
    border-color: #4d5665;
}
QPushButton:pressed {
    background: #343b47;
}
QPushButton:disabled {
    color: #68717e;
    background: #191c22;
    border-color: #282d35;
}
QPushButton#localAINewSessionButton {
    background: #1c4f43;
    border: 1px solid #2f7565;
    color: #effff9;
    text-align: left;
    padding: 10px 13px;
    font-weight: 650;
}
QPushButton#localAINewSessionButton:hover {
    background: #246253;
}
QPushButton#localAISendButton {
    background: #10a37f;
    color: #ffffff;
    border: 0;
    border-radius: 22px;
    padding: 0;
}
QPushButton#localAISendButton:hover {
    background: #16b58e;
}
QPushButton#localAISendButton:pressed {
    background: #0c8e6e;
}
QPushButton#localAISendButton:disabled {
    background: #38413f;
    color: #818b88;
}
QListWidget {
    background: #111318;
    color: #dfe4ea;
    border: 1px solid #292e38;
    border-radius: 8px;
    outline: 0;
    padding: 2px;
}
QListWidget::item {
    background: transparent;
    color: #cfd5dd;
    border-radius: 7px;
    margin: 1px;
    padding: 8px 9px;
}
QListWidget::item:hover {
    background: #1c2027;
    color: #ffffff;
}
QListWidget::item:selected {
    background: #272d36;
    color: #ffffff;
}
QPlainTextEdit#localAIConversation {
    background: #0d0d0d;
    color: #eef1f5;
    border: 0;
    padding: 16px 28px;
    selection-background-color: #355e55;
    font-size: 14px;
}
QLineEdit#localAIComposer {
    background: transparent;
    color: #f5f7fa;
    border: 0;
    padding: 10px 8px;
    font-size: 14px;
    selection-background-color: #355e55;
}
QLineEdit#localAIComposer:focus {
    border: 0;
}
QTabWidget#localAIInspectorTabs::pane {
    background: #111318;
    border: 1px solid #252932;
    border-radius: 10px;
    top: -1px;
}
QTabBar::tab {
    background: #171a20;
    color: #aeb6c2;
    border: 1px solid #292e38;
    border-bottom: 0;
    padding: 7px 12px;
    margin-right: 2px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
}
QTabBar::tab:selected {
    background: #222730;
    color: #ffffff;
}
QRadioButton, QCheckBox {
    color: #cfd5dd;
    spacing: 7px;
}
QScrollArea {
    border: 0;
    background: #111318;
}
QScrollBar:vertical {
    background: transparent;
    width: 9px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #414854;
    border-radius: 4px;
    min-height: 26px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QSplitter::handle {
    background: #252932;
    width: 1px;
    height: 1px;
}
"""
