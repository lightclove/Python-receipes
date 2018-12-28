from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("my first prog.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Snmp_Handler",
    options = options,
    version = "0.1_beta",
    description = 'Snmp handler modem interactor',
    executables = executables
)