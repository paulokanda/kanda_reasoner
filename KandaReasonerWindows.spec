# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = [('kanda_reasoner_app\\reasoner_context_collector\\collector_main_help', 'kanda_reasoner_app\\reasoner_context_collector\\collector_main_help')]
hiddenimports = ['PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtWebChannel', 'reasoner_tools_gui_engineering_safety_panel', '_reasoner_tools_gui_engineering_safety_panel_catalog', '_reasoner_tools_gui_engineering_safety_panel_commands', '_reasoner_tools_gui_engineering_safety_full_audit', '_reasoner_tools_gui_engineering_safety_sonar', '_reasoner_tools_gui_ruff_correction_dialog']
datas += collect_data_files('kanda_reasoner_app')
hiddenimports += collect_submodules('kanda_reasoner_app')


a = Analysis(
    ['reasoner_tools_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='KandaReasoner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KandaReasoner',
)
