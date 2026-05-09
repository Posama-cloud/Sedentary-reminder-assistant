# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['maincharacter.py'],
    pathex=[],
    binaries=[],
    datas=[('image_0.png', '.')],
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
    [],
    exclude_binaries=True,
    name='久坐提醒助手',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='久坐提醒助手',
)
app = BUNDLE(
    coll,
    name='久坐提醒助手.app',
    icon=None,
    bundle_identifier='com.sedentary.reminder',
    info_plist={
        'NSCameraUsageDescription': '本应用需要访问摄像头来检测您是否在电脑前，以便准确提醒您休息。摄像头仅用于本地检测，不会上传或保存任何图像。',
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.1.0',
        'CFBundleVersion': '1.1.0',
        'LSMinimumSystemVersion': '10.13.0',
        'LSUIElement': True,  # 菜单栏应用，不在 Dock 显示
    },
)
