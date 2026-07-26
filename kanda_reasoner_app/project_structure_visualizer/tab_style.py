# project-path: kanda_reasoner_app/project_structure_visualizer/tab_style.py
"""Local stylesheet for the Project Structure 3D tab."""

from __future__ import annotations


def project_structure_3d_style() -> str:
    """Return the scoped visualizer stylesheet."""
    return (
        "#projectStructure3DJsonControls, "
        "#projectStructure3DToolbar, #projectStructure3DNavigation {"
        "background: #111d2a; border: 1px solid #273b4e;"
        "border-radius: 8px;}"
        "#projectStructure3DJsonControls QLabel, "
        "#projectStructure3DJsonControls QPushButton, "
        "#projectStructure3DToolbar QLabel, "
        "#projectStructure3DToolbar QCheckBox, "
        "#projectStructure3DToolbar QComboBox, "
        "#projectStructure3DToolbar QLineEdit, "
        "#projectStructure3DToolbar QPushButton, "
        "#projectStructure3DNavigation QLabel, "
        "#projectStructure3DNavigation QPushButton {color: #ffffff;}"
        "#projectStructure3DSearch {color: #ffffff; "
        "placeholder-text-color: #ffffff;}"
        "#projectStructure3DToolbar QComboBox QAbstractItemView {"
        "background: #0b1420; color: #ffffff;"
        "selection-background-color: #1f6fb2; "
        "selection-color: #ffffff;}"
        "#projectStructure3DJsonRequiredLabel {color: #f4a261; font-weight: 700;}"
        "#projectStructure3DJsonStatus {color: #d9e7f4;}"
        "#projectStructure3DBadge {color: #ffffff; font-weight: 700;}"
        "#projectStructure3DDetails {"
        "background: #0b1420; color: #e8f1fa; "
        "border: 1px solid #273b4e;"
        "border-radius: 8px; padding: 8px;}"
        "#projectStructure3DStatus {color: #ffffff; padding: 2px 6px;}"
    )
