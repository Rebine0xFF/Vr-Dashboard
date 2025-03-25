import ctypes
import sys

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def ensure_admin():
    if not is_admin():
        print("Relaunching as admin...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()