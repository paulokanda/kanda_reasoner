
"""
🔁 ASCII Pipeline – Where This Module Fits
+-------------------------------+
|      EEGMainWindowBuilder    |
|  (Assembles main UI layout)  |
+---------------+---------------+
                |
                v
+-------------------------------+
|     📁 EEGTab (EEG Traces)     |
| - Custom middle/top/bottom   |
| - canvas + timeline          |
+---------------+---------------+
                |
                v
+-------------------------------+
|     🟧 middle_bar (EEG3DBar)    |
| - Exposed as layout target   |
|   for dropdown integration   |
+---------------+---------------+
                |
                v
+-------------------------------+
|  🔗 DropdownIntegrator |
| - Injects SensitivityDropdown|
|   into middle_bar layout     |
+---------------+---------------+
                |
                v
+-------------------------------+
|   SensitivityDropdown Module  |
| - Inherits reusable template  |
| - Auto-sizes to content       |
| - Emits `sensitivity_changed`|
+---------------+---------------+
                |
                v
+-------------------------------+
|     EEGVisualizerCore Controller  |
| - Listens to signal and       |
|   applies µV setting          |
+-------------------------------+

🎯 ASCII Diagram: Sensitivity Dropdown → Canvas Update Flow

+-----------------------------+
|    User selects µV value    |
|   from SensitivityDropdown |
+-------------+--------------+
              |
              v  emits
+-------------+--------------+
| Signal: sensitivity_changed(int)        |
|  → emitted by SensitivityDropdown       |
+-------------+--------------+
              |
              v  connected to
+-------------+--------------+
| EEGVisualizerCore.set_sensitivity(value)   |
| - Updates internal state:             |
|   self.sensitivity = value            |
| - Triggers update_plot_view()         |
+-------------+--------------+
              |
              v
+-------------+--------------+
| EEGVisualizerCore.update_plot_view()      |
| - Redraws EEG window with new scale  |
| - Updates matplotlib Axes, canvas    |
+-------------+--------------+
              |
              v
+-------------+--------------+
| Matplotlib Canvas Refresh              |
| - Axes rescaled                        |
| - Red line + guide markers updated    |
| - canvas.draw_idle() called           |
+----------------------------------------+

🧠 Summary of Flow

    Dropdown emits signal ➜ sensitivity_changed(value)

    Signal is connected to method ➜ visualizer.set_sensitivity(value)

    Method updates internal state ➜ modifies scaling

    Visualizer triggers redraw ➜ update_plot_view()

    Matplotlib plot updates ➜ axes, red line, and UI refreshed
"""

