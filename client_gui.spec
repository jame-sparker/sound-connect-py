# -*- mode: python -*-

block_cipher = None



a = Analysis(['client_gui.py'],
             pathex=['/home/james/Documents/5th_Semester/COMP3530/tutorial_facilitation/soundconnectpy'],
             binaries=[],
             datas=[('assets','assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='client_gui',
          debug=False,
          strip=False,
          upx=True,
          console=False )
