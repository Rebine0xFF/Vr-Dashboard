import subprocess
import threading
import psutil
import ctypes
import sys
import time

service_name = "OVRService"


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
                                         stdin=subprocess.PIPE,                                          # Set it's mode to the dictionnary value
                                         text=True)                                                                    # |     |
            processus.communicate(input=f"perfhud set-mode 0\nstereohud set-mode 0\nlayerhud set-mode 0\n{name} set-mode {index}\nexit\n")
                                                               # Reset all huds                          |    |
                                                                                       # Get selected hud name from dictionnary




def get_service():

    service = None
    try:
        service = psutil.win_service_get(service_name)
        service = service.as_dict()
    except Exception as ex:
        print(str(ex))
    return service




def run_subprocess(command, shell=False):
    """
    Utility function to run a subprocess with default parameters.
    """
    return subprocess.Popen(
        command,
        shell=shell,
        creationflags=0x00000008,  # Independent process
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )

def manage_service(action, on_complete=None):
    if action not in ["start", "stop", "restart"]:
        print("❌ Invalid action! Use 'start', 'stop' or 'restart'.")
        return

    def service_task():
        try:
            if action == "restart":
                run_subprocess(["net", "stop", service_name], shell=True)
                time.sleep(3)
                run_subprocess(["net", "start", service_name], shell=True)
                print(f"🔄 {service_name} successfully restarted.")
            else:
                run_subprocess(["net", action, service_name], shell=True)
                time.sleep(1)
                print(f"✅ {service_name} {action}ed with success.")
        except Exception as e:
            print(f"❌ Error when executing '{action}': {e}")
        finally:
            if on_complete:
                on_complete()

    # Exécuter la tâche dans un thread séparé
    threading.Thread(target=service_task, daemon=True).start()