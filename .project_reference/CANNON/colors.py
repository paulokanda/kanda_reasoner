import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QScrollArea)
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QFont
from PySide6.QtCore import Qt, QTimer

# A selection of popular vivid palettes from Coolors
VIVID_PALETTES = [
    ["#ffbe0b", "#fb5607", "#ff006e", "#8338ec", "#3a86ff"],
    ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"],
    ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"],
    ["#f94144", "#f3722c", "#f8961e", "#90be6d", "#577590"],
    ["#d9ed92", "#b5e48c", "#99d98c", "#76c893", "#52b69a"],
    ["#e63946", "#f1faee", "#a8dadc", "#457b9d", "#1d3557"],
    ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
    ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff"],
    ["#00b4d8", "#0077b6", "#023e8a", "#03045e", "#90e0ef"],
    ["#d00000", "#ffba08", "#3f88c5", "#032b43", "#136f63"]
]

class ColorBlock(QWidget):
    def __init__(self, color_hex, is_first=False, is_last=False):
        super().__init__()
        self.color_hex = color_hex.upper()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(120)
        
        # Setup Layout and Label (hidden by default)
        layout = QVBoxLayout(self)
        self.label = QLabel(self.color_hex)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Determine text color based on background brightness for readability
        bg_color = QColor(self.color_hex)
        brightness = (bg_color.red() * 299 + bg_color.green() * 587 + bg_color.blue() * 114) / 1000
        text_color = "black" if brightness > 125 else "white"
        
        font = QFont("Arial", 12, QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet(f"color: {text_color}; background: transparent;")
        self.label.setGraphicsEffect(None)
        self.label.hide()
        
        # Apply rounded corners only to the outer edges of the palette
        radius = 12
        style = f"background-color: {self.color_hex};"
        if is_first:
            style += f"border-top-left-radius: {radius}px; border-bottom-left-radius: {radius}px;"
        if is_last:
            style += f"border-top-right-radius: {radius}px; border-bottom-right-radius: {radius}px;"
            
        self.setStyleSheet(style)

    def enterEvent(self, event):
        self.label.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.label.text() == "COPIED!":
            self.label.setText(self.color_hex)
        self.label.hide()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Copy to clipboard
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(self.color_hex)
            
            # Show feedback
            self.label.setText("COPIED!")
            QTimer.singleShot(1200, self.reset_text)

    def reset_text(self):
        self.label.setText(self.color_hex)


class PaletteRow(QWidget):
    def __init__(self, colors):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) # Remove spacing so colors touch seamlessly

        for i, hex_code in enumerate(colors):
            block = ColorBlock(
                color_hex=hex_code, 
                is_first=(i == 0), 
                is_last=(i == len(colors) - 1)
            )
            layout.addWidget(block)
            
        # Add a subtle shadow effect (Optional but adds to the Coolors aesthetic)
        self.setStyleSheet("""
            PaletteRow {
                background-color: white;
                border-radius: 12px;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popular Vivid Palettes")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #f8f9fa;") # Light gray background

        # Main Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        # Container for the palettes
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(30)
        
        # Title
        title_label = QLabel("Popular Vivid Palettes")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #333333; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # Add all palettes to the layout
        for colors in VIVID_PALETTES:
            palette_widget = PaletteRow(colors)
            container_layout.addWidget(palette_widget)
            
        # Add stretch to push everything to the top
        container_layout.addStretch()

        scroll_area.setWidget(container_widget)
        self.setCentralWidget(scroll_area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())