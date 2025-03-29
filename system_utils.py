import subprocess
import psutil
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





def is_process_running(process_name):

    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def launch_oculus_client():

    try:
        if not is_process_running("OculusClient.exe"):
            subprocess.Popen(
                [r"C:\Program Files\Oculus\Support\oculus-client\OculusClient.exe"],
                creationflags=0x00000008,   # Independent process
                stdout=subprocess.DEVNULL,  #
                stderr=subprocess.DEVNULL,  #
                text=True)
            print("Oculus Client launched.")
        else:
            print("Oculus Client is already running.")
    except Exception as e:
        print(f"Errore launching Oculus Client : {e}")





def change_overlay(name, index):
    
            processus = subprocess.Popen("C:/Program Files/Oculus/Support/oculus-diagnostics/OculusDebugToolCLI.exe",
                                         stdin=subprocess.PIPE,
                                         text=True)
            processus.communicate(input=f"perfhud set-mode 0\nstereohud set-mode 0\nlayerhud set-mode 0\n{name} set-mode {index}\nexit\n")
                                        # |                     Reset all huds                          | Get selected hud name from dictionnary |        | Set it's mode to the dictionnary value |