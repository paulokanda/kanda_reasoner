from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
from PySide6.QtCore import Qt
# from EEGTemplates.eeg_style_templates import FramePresets
from EEGTemplates.threed_button_templates import ThreeDButtonPresets

class EEGHelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"🧩 {FULL_NAME}")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
            }
            QLabel#Title {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px 0;
            }
            QLabel#Body {
                font-size: 14px;
                color: #333;
                padding: 8px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)

        # Title
        self.title_label = QLabel("Measurement Description")
        self.title_label.setObjectName("Title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(self.title_label)

        # Body
        self.body_label = QLabel("")
        self.body_label.setWordWrap(True)
        self.body_label.setObjectName("Body")
        self.scroll_layout.addWidget(self.body_label)

        main_layout.addWidget(self.scroll_area)

        # OK Button
        ok_button = ThreeDButtonPresets.make_button("OK", callback=self.accept, style="scientific")
        main_layout.addWidget(ok_button, alignment=Qt.AlignCenter)

    def set_content(self, text):
        """Set the text inside the help window"""
        self.body_label.setText(text)

