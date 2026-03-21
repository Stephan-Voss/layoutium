# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainLayoutium.py'],
    pathex=[],
    binaries=[],
    datas=[('Assets\\Add Box Icon.png', 'Assets\\.'), ('Assets\\Apply Color Icon.png', 'Assets\\.'), ('Assets\\Bleed Off Icon.png', 'Assets\\.'), ('Assets\\Bleed On Icon.png', 'Assets\\.'), ('Assets\\Create Group Icon.png', 'Assets\\.'), ('Assets\\Destroy Group Icon.png', 'Assets\\.'), ('Assets\\Embed Image Icon.png', 'Assets\\.'), ('Assets\\Eyecon - Hidden.png', 'Assets\\.'), ('Assets\\Eyecon - Shown.png', 'Assets\\.'), ('Assets\\Load Layout Icon.png', 'Assets\\.'), ('Assets\\Lock Box Icon.png', 'Assets\\.'), ('Assets\\Reset Zoom Icon.png', 'Assets\\.'), ('Assets\\Save Layout Icon.png', 'Assets\\.'), ('Assets\\Select Font Icon.png', 'Assets\\.'), ('Assets\\Zoom In Icon.png', 'Assets\\.'), ('Assets\\Zoom Out Icon.png', 'Assets\\.')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='Layoutium',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
