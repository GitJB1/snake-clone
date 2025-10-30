from cx_Freeze import setup, Executable # type: ignore
import sys

# Dependências extras
build_options = {'packages': ["pygame"], 'excludes': []}

# Base correta para Windows GUI
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('main.py', base=base, target_name='snake')
]

setup(
    name='Snake',
    version='1.0',
    description='Snake clone by Jonas Bernardino',
    options={'build_exe': build_options},
    executables=executables)
