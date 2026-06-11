# dt_17_Kanda_Logic_Tips/font_test.py
"""
Font test utility — safe for imports, only runs GUI if executed directly.

Usage:
    python dt_17_Kanda_Logic_Tips/font_test.py
"""

import os
import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import QCoreApplication, Qt


def main():
    """Main entry for manual GUI testing."""
    app = QApplication(sys.argv)

    # Force software OpenGL for environments without GPU
    QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

    font_path = os.path.join("fonts", "Roboto-Bold.ttf")
    fid = QFontDatabase.addApplicationFont(font_path)
    families = QFontDatabase.applicationFontFamilies(fid)
    print(f"Loaded families: {families}")

    if families:
        font = QFont(families[0], 14)
        app.setFont(font)

    label = QLabel("Testing Roboto Bold\n0123456789")
    label.resize(300, 100)
    label.show()

    sys.exit(app.exec())


# ✅ Only launch GUI if executed directly, not when imported (e.g., by pytest)
if __name__ == "__main__":
    main()
