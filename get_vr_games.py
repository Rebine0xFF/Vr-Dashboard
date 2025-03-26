import requests


def get_installed_vr_games():

    in_apps = False
    vr_games_list = []

    with open("C:/Program Files (x86)/Steam/steamapps/libraryfolders.vdf", "r") as file:

        for line in file:
            line = line.strip()  # Retirer les espaces et les tabulations inutiles
            
            if line == '"apps"':
                in_apps = True
                continue  # Passer à la ligne suivante sans l'afficher
            
            if line == "}":
                in_apps = False

            if in_apps and line and '"' in line:  # On s'assure qu'on est dans "apps" et que la ligne contient des données
                
                app_id = line.split()[0].strip('"')  # On supprime les guillemets autour de la clé
                
                result = check_vr_support(app_id)
                if result == "Game supports VR":  # Si le jeu supporte la VR, on l'ajoute à la liste
                    vr_games_list.append(app_id)

    return vr_games_list


def check_vr_support(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Check if app_id is in the response (if the request was successful)
        if str(app_id) in data and data[str(app_id)]["success"]:
            # Fetch categories
            categories = data[str(app_id)]["data"].get("categories", [])
            
            # Check vr support (id 53 or 54)
            for category in categories:
                if category["id"] == 53 or category["id"] == 54:
                    return "Game supports VR"
            return "Game does NOT support VR"
        else:
            return "No info available for this app_id"
    else:
        return "ERROR when fetching data"
    


vr_games = get_installed_vr_games()
print("Jeux installés qui supportent la VR:", vr_games)