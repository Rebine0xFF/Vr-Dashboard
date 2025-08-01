import customtkinter
from PIL import Image
import os

from system_utils import change_overlay, get_service, manage_service

class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("VR Dashboard by Rebine")
        self.geometry("1000x500")

        self.options_frame = OptionsFrame(self)
        self.options_frame.pack(side="left",
                                pady=20,
                                padx=20,
                                fill="y")
        
        self.games_frame = GamesFrame(self)
        self.games_frame.pack(side="right",
                                pady=20,
                                padx=20,
                                fill="y")


class OptionsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        root_path = os.path.dirname(os.path.abspath(__file__))
        icons_path = os.path.join(root_path, "imgs", "icons")


        def oculus_service_action_button_callback(action):

            self.top_progrees_bar.configure(mode="indeterminate")
            self.top_progrees_bar.start()

            def on_service_complete():
                self.top_progrees_bar.stop()
                self.top_progrees_bar.configure(mode="determinate")
                
            manage_service(action, on_complete=on_service_complete)


        def HUD_selection_segmented_button_callback(value):
            print(value, "was selected and has the index of", self.HUD_actions_dictionnary[value])

            if value != "None":
                self.HUD_selection_segmented_button.configure(selected_color="#2E7E09") # green
                self.HUD_selection_segmented_button.configure(selected_hover_color="#27640A")
            else:
                self.HUD_selection_segmented_button.configure(selected_color="#1f6aa5") # default blue color
                self.HUD_selection_segmented_button.configure(selected_hover_color="#144870")

            change_overlay(self.HUD_actions_dictionnary[value][0], self.HUD_actions_dictionnary[value][1])


        # Dictionnaire associant chaque valeur à une action
        self.HUD_actions_dictionnary = {
            "None": ["perfhud", 0],
            "Performance": ["perfhud", 1],
            "Stereo Debug": ["stereohud", 1],
            "Layer": ["layerhud", 1]
        }

        self.top_progrees_bar = customtkinter.CTkProgressBar(self, height=3)
        self.top_progrees_bar.pack(fill="x")
        self.top_progrees_bar.set(1)

        self.HUD_label = customtkinter.CTkLabel(self,
                                             text="Visible HUD",
                                             text_color="white",
                                             font=("Inter", 15, "bold"))
        self.HUD_label.pack(pady=(5, 10), fill="x")

        self.HUD_selection_segmented_button = customtkinter.CTkSegmentedButton(self,
                                                             values=["None", "Performance", "Stereo Debug", "Layer"],
                                                             command=HUD_selection_segmented_button_callback,
                                                             font=("Inter Regular", 14))
        self.HUD_selection_segmented_button.set("None")
        self.HUD_selection_segmented_button.pack(padx=40, pady=(5, 1))
        HUD_selection_segmented_button_callback("None") # Reset overlays in CLI at app launch

        self.HUD_status_label = customtkinter.CTkLabel(self,
                                                       text=f"Current overlay index: {self.HUD_actions_dictionnary[self.HUD_selection_segmented_button._current_value]}",
                                                       font=("Inter Extra Light", 13),
                                                       text_color="#A7A7A7")
        self.HUD_status_label.pack(anchor="w", padx=40, pady=1)


        self.separator_line1 = customtkinter.CTkProgressBar(self, height=3, width=330, progress_color="#3D3C3C", fg_color="#3D3C3C")
        self.separator_line1.pack(pady=10)


        self.oculus_service_label = customtkinter.CTkLabel(self,
                                             text="Oculus Service",
                                             text_color="white",
                                             font=("Inter", 15, "bold"))
        self.oculus_service_label.pack(pady=5, fill="x")

        self.oculus_service_button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.oculus_service_button_frame.pack()

        self.start_icon = customtkinter.CTkImage(Image.open(icons_path + "/start_icon.png"), size=(40, 40))
        self.stop_icon = customtkinter.CTkImage(Image.open(icons_path + "/stop_icon.png"), size=(40, 40))
        self.restart_icon = customtkinter.CTkImage(Image.open(icons_path + "/restart_icon.png"), size=(40, 40))

        self.oculus_start_service_button = customtkinter.CTkButton(self.oculus_service_button_frame,
                                                                   text="Start     \nService",
                                                                   width=1,
                                                                   height=52,
                                                                   fg_color="#353E28",
                                                                   hover_color=("blue"),
                                                                   text_color="white",
                                                                   image=self.start_icon,
                                                                   font=("Inter Medium", 14),
                                                                   command=lambda: oculus_service_action_button_callback(action="start"))
        self.oculus_start_service_button.pack(side="left", padx=5, pady=5)

        self.oculus_stop_service_button = customtkinter.CTkButton(self.oculus_service_button_frame,
                                                                   text="Stop      \nService",
                                                                   width=1,
                                                                   height=52,
                                                                   fg_color="#483333",
                                                                   hover_color=("blue"),
                                                                   text_color="white",
                                                                   image=self.stop_icon,
                                                                   font=("Inter Medium", 14),
                                                                   command=lambda: oculus_service_action_button_callback(action="stop"))
        self.oculus_stop_service_button.pack(side="left", padx=5, pady=5)

        self.oculus_restart_service_button = customtkinter.CTkButton(self.oculus_service_button_frame,
                                                                   text="Restart \nService",
                                                                   width=1,
                                                                   height=52,
                                                                   fg_color="#5C4634",
                                                                   hover_color=("blue"),
                                                                   text_color="white",
                                                                   image=self.restart_icon,
                                                                   font=("Inter Medium", 14),
                                                                   command=lambda: oculus_service_action_button_callback(action="restart"))
        self.oculus_restart_service_button.pack(side="left", padx=5, pady=5)


        self.service_status_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.service_status_frame.pack()

        self.service_fixed_label = customtkinter.CTkLabel(self.service_status_frame,
                                                       text="Service status: ",
                                                       font=("Inter Extra Light", 13),
                                                       text_color="#A7A7A7")
        self.service_fixed_label.pack(side="left", padx=0, pady=1)

        self.service_dynamic_label = customtkinter.CTkLabel(self.service_status_frame,
                                                       text="Running",
                                                       font=("Inter Extra Light", 13),
                                                       text_color="#5C8D18")
        self.service_dynamic_label.pack(side="left", padx=0, pady=1)


        self.separator_line2 = customtkinter.CTkProgressBar(self, height=3, width=330, progress_color="#3D3C3C", fg_color="#3D3C3C")
        self.separator_line2.pack(pady=10)


        self.shortcut_label = customtkinter.CTkLabel(self,
                                             text="Shortcuts",
                                             text_color="white",
                                             font=("Inter", 15, "bold"))
        self.shortcut_label.pack(pady=5, fill="x")



class GamesFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.top_progrees_bar = customtkinter.CTkProgressBar(self, height=3)
        self.top_progrees_bar.pack(fill="x")
        self.top_progrees_bar.set(1)