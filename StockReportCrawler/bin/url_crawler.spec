# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['url_crawler.py'],
             pathex=[
	     	'D:\\dekr0\\self-libs\\Python\\urlextractor\\bin',
		    'D:\\derk0\\self-libs\\Python\\urlextractor\\',
		]
             binaries=[],
             datas=[
	     	('D:/Dekr0/Python/appdata/database', 'appdata'),
	     	('D:/Dekr0/Python/appdata/pattern_lib.json', 'appdata'
	     ],
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
          name='url_crawler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
