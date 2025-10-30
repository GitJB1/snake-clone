from cx_Freeze import setup, Executable # type: ignore

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["pygame"], 'excludes': []}

base = 'gui'

executables = [
    Executable('main.py', base=base, target_name = 'snake')
]

setup(name='Snake',
      version = '1',
      description = 'Snake clone by Jonas Bernardino',
      options = {'build_exe': build_options},
      executables = executables)
