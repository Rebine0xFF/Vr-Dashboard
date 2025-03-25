# police Inter

import customtkinter

import subprocess
import psutil # pour vérifier si le processus est déjà en cours d'exécution (à faire)
import os

from admin_check import ensure_admin
from ui import Application



os.system('cls' if os.name == 'nt' else 'clear') # Clear console
ensure_admin()

print("App running as admin ✅")
processus = subprocess.Popen([r"C:\Program Files\Oculus\Support\oculus-client\OculusClient.exe"],
                                text=True)



root_path = os.path.dirname(os.path.abspath(__file__))
icons_path = os.path.join(root_path, "imgs", "icons")

customtkinter.set_appearance_mode("dark")

app = Application()
app.mainloop()