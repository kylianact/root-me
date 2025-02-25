import requests
import json
import os

# UID et clé API (la clé API sera stockée dans GitHub Secrets)
UID = "TON_UID"
API_KEY = os.getenv("ROOTME_API_KEY")  # Récupère la clé API depuis GitHub Actions
URL = f"https://www.root-me.org/API/private/user/{UID}"

# Headers d'authentification
headers = {"Authorization": f"Bearer {API_KEY}"}

# Récupérer le score Root-Me
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    score = data.get("score", "N/A")
elif response.status_code == 403:
    print("❌ Erreur 403 : Accès interdit. Vérifie ta clé API.")
    score = "Erreur 403"
else:
    print(f"❌ Erreur {response.status_code} : {response.text}")
    score = "Erreur"

# Sauvegarde du score dans un fichier JSON
score_data = {"label": "RootMe Score", "message": str(score), "color": "blue"}

with open("rootme_score.json", "w") as json_file:
    json.dump(score_data, json_file)

print("✅ Score mis à jour :", score)
