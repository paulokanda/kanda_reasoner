"""
You can absolutely scatter your tests alongside each sub-package rather than lumping everything in one “tests/” folder. Here’s a recipe:
1. Directory layout

E:/EEG_KANDA
├── k01_core_eeg/
│   ├── Kanda_Amplitude_0_1/
│   │   ├── __init__.py
│   │   ├── k01_core_eeg/
│   │   ├── controller/
│   │   ├── renderer/
│   │   ├── utils/
│   │   └── tests_amplitude/
│   │       ├── __init__.py
│   │       ├── test_core_amplitude.py
│   │       ├── test_renderer.py
│   │       └── test_amplitude_map.py
│   └── tests_kandaModules/
│       └── test_open_eeg_dialog.py
├── pytest.ini
└── …

Each tests_…/ folder has its own __init__.py (so imports like from
Kanda_Amplitude_0_1.k01_core_eeg.amplitude import AmplitudeComputer work).




"""

Now whenever you run pytest from E:/EEG_KANDA, pytest will:

    Look only in those two test folders.

    Automatically add E:/EEG_KANDA/Core to sys.path, so

from Kanda_Amplitude_0_1.core_mv.amplitude import AmplitudeComputer

Just Works™.


Summary

    Give each module its own tests_…/ subfolder with an __init__.py.

    List all your test-folders under testpaths in a single pytest.ini at the top.

    Set pythonpath = Core so imports resolve cleanly.

With that, you can have:

    k01_core_eeg/Kanda_Amplitude_0_1/tests_amplitude/...

    k01_core_eeg/tests_kandaModules/...

    k01_core_eeg/another_module/tests_another/...

…all discovered and runnable from one pytest command.



"""

"""

