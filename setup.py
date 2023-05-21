from cx_Freeze import setup, Executable

setup(
    name='KRAQEN',
    version='1.0',
    description='Air Quality App',
    executables=[Executable('Main.py')],
)