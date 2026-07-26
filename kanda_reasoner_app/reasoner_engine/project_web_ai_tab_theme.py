# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_tab_theme.py
"""Professional Qt stylesheet for the Project Web AI tab."""

from __future__ import annotations

__all__ = ["PROJECT_WEB_AI_THEME"]


PROJECT_WEB_AI_THEME = """
QWidget#projectWebAITab {
    background: #0d0d0d;
    color: #eef1f5;
    font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;
    font-size: 13px;
}
QFrame#projectWebAISidebar {
    background: #111318;
    border-right: 1px solid #252932;
}
QFrame#projectWebAIChatCanvas {
    background: #0d0d0d;
}
QFrame#projectWebAIHeader {
    background: #0f1115;
    border-bottom: 1px solid #252932;
}
QFrame#projectWebAISection {
    background: #171a20;
    border: 1px solid #292e38;
    border-radius: 12px;
}
QFrame#projectWebAIComposerFrame {
    background: #1a1e25;
    border: 1px solid #343b47;
    border-radius: 20px;
}
QFrame#projectWebAIDivider {
    background: #252932;
    min-height: 1px;
    max-height: 1px;
}
QLabel {
    color: #eef1f5;
    background: transparent;
}
QLabel#projectWebAITitle {
    color: #f8fafc;
    font-size: 20px;
    font-weight: 700;
}
QLabel#projectWebAISubtitle {
    color: #8f98a6;
    font-size: 12px;
}
QLabel#projectWebAISectionTitle {
    color: #dce2ea;
    font-size: 12px;
    font-weight: 650;
}
QLabel#projectWebAIMuted {
    color: #929baa;
    font-size: 12px;
}
QLabel#projectWebAIStatus {
    color: #aeb6c2;
    padding: 2px 0;
    font-size: 12px;
}
QLabel#projectWebAIBadge {
    color: #9fe3d0;
    background: #17372f;
    border: 1px solid #245447;
    border-radius: 9px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 700;
}
QLineEdit, QPlainTextEdit#projectWebAISideText {
    background-color: #20242b;
    color: #f4f6f8;
    border: 1px solid #343a45;
    border-radius: 8px;
    padding: 8px;
    selection-background-color: #355e55;
}
QLineEdit:focus, QPlainTextEdit#projectWebAISideText:focus {
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
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
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
QPushButton#projectWebAINewChatButton {
    background: #1c4f43;
    border: 1px solid #2f7565;
    color: #effff9;
    text-align: left;
    padding: 10px 13px;
    font-weight: 650;
}
QPushButton#projectWebAINewChatButton:hover {
    background: #246253;
}
QPushButton#projectWebAIHistoryAction {
    padding: 6px 8px;
    font-size: 11px;
}
QPushButton#projectWebAISendButton {
    background: #10a37f;
    color: #ffffff;
    border: 0;
    border-radius: 22px;
    padding: 0;
}
QPushButton#projectWebAISendButton:hover {
    background: #16b58e;
}
QPushButton#projectWebAISendButton:pressed {
    background: #0c8e6e;
}
QPushButton#projectWebAISendButton:disabled {
    background: #38413f;
    color: #818b88;
}
QPushButton#projectWebAIStopButton {
    border-radius: 14px;
    padding: 4px 10px;
    font-size: 11px;
}
QListWidget#projectWebAIChatList {
    background: #111318;
    color: #dfe4ea;
    border: 0;
    outline: 0;
    padding: 1px;
}
QListWidget#projectWebAIChatList::item {
    background: transparent;
    color: #cfd5dd;
    border-radius: 8px;
    margin: 1px 0;
    padding: 9px 10px;
}
QListWidget#projectWebAIChatList::item:hover {
    background: #1c2027;
    color: #ffffff;
}
QListWidget#projectWebAIChatList::item:selected {
    background: #272d36;
    color: #ffffff;
}
QTextBrowser#projectWebAIConversation {
    background: #0d0d0d;
    color: #eef1f5;
    border: 0;
    padding: 12px 24px;
    selection-background-color: #355e55;
}
QPlainTextEdit#projectWebAIComposer {
    background: transparent;
    color: #f5f7fa;
    border: 0;
    padding: 10px 8px;
    font-size: 14px;
    selection-background-color: #355e55;
}
QPlainTextEdit#projectWebAIComposer:focus {
    border: 0;
}
QCheckBox {
    color: #cfd5dd;
    spacing: 8px;
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
}
"""
