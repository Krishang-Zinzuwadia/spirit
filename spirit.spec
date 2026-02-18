# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all hidden imports for sarvamai, sounddevice, soundfile, pywinauto
hidden_imports = [
    'pyaudio',
    'pynput',
    'keyboard',
    'win32api',
    'win32con',
    'win32gui',
    'ctypes',
    'winsound',
    'dotenv',
    'sarvamai',
    'sounddevice',
    'soundfile',
    'pywinauto',
    'speech_recognition',
    'PIL',
]

# Include data files - check if assets exists
import os
assets_data = [('assets', 'assets')] if os.path.exists('assets') else []
datas = [('.env', '.')] + assets_data

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy.distutils'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Spirit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no console window — pure background process
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # add icon path here if you have one, e.g. 'assets/icon.ico'
    version=None,
)
