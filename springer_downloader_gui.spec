# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['springer_downloader_gui.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='springer_downloader_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='springer_downloader_gui')
app = BUNDLE(coll,
             name='springer_downloader_gui.app',
             icon=None,
             bundle_identifier=None,
            info_plist={
                'NSHighResolutionCapable': 'True'
                },
        )
