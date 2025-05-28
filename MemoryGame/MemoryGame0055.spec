# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['MemoryGame0055.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('background.jpg', '.'),
        ('cards/card_1.png', 'cards'),        
        ('cards/card_2.png', 'cards'),
        ('cards/card_3.png', 'cards'),
        ('cards/card_4.png', 'cards'),
        ('cards/card_5.png', 'cards'),
        ('cards/card_6.png', 'cards'),
        ('cards/card_7.png', 'cards'),
        ('cards/card_8.png', 'cards'),
        ('cards/card_9.png', 'cards'),
        ('cards/card_back.png', 'cards'),
		('fonts/NotoSansJP-Regular.ttf', 'fonts'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,    
)

pyz = PYZ(a.pure, a.zipped_data, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,    
    a.datas,
    [],
    name='MemoryGame005',
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
    icon='app_icon.ico',
    onefile=True,  
)
