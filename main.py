# police Inter

import customtkinter
import os

from system_utils import ensure_admin, launch_oculus_client
from ui import Application



os.system('cls' if os.name == 'nt' else 'clear') # Clear console
ensure_admin()

launch_oculus_client()


root_path = os.path.dirname(os.path.abspath(__file__))
icons_path = os.path.join(root_path, "imgs", "icons")

customtkinter.set_appearance_mode("dark")

app = Application()
app.mainloop()