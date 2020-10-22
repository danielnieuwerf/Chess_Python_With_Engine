# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['chesspython.py'],
             pathex=['C:\\Users\\danie\\OneDrive\\Documents\\GitHub\\ChessPython\\chess_python_with_engine'],
             binaries=[],
             datas=[("C:\\Users\\danie\\OneDrive\\Documents\\GitHub\\ChessPython\\chess_python_with_engine\\files", "files"), ("C:\\Users\\danie\\OneDrive\\Documents\\GitHub\\ChessPython\\chess_python_with_engine\\saved_games", "saved_games")],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='chesspython',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
