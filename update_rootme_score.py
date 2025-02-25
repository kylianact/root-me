import requests
import json
import os

# UID Root-Me
UID = "TON_UID"

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("ROOTME_API_KEY")

if not API_KEY:
    print("❌ Erreur : Clé API manquante. Vérifie ton secret GitHub.")
    exit(1)

# URL de l'API Root-Me
URL = f"https://www.root-me.org/API/private/user/{UID}"

# Headers d'authentification
headers = {"Authorization": f"Bearer {API_KEY}"}

# Requête API
response = requests.get(URL, headers=headers)

# Debug : Afficher le statut et la réponse complète
print("➡ Status Code:", response.status_code)
print("➡ Réponse API:", response.text)

if response.status_code == 200:
    data = response.json()
    score = data.get("score", "N/A")
elif response.status_code == 403:
    print("❌ Erreur 403 : Accès refusé. Vérifie ta clé API Root-Me.")
    score = "Erreur 403"
elif response.status_code == 404:
    print("❌ Erreur 404 : UID invalide. Vérifie ton identifiant Root-Me.")
    score = "Erreur 404"
else:
    print(f"❌ Erreur {response.status_code} : {response.text}")
    score = "Erreur"

# Générer un fichier JSON pour Shields.io
score_data = {"label": "RootMe Score", "message": str(score), "color": "blue"}

with open("rootme_score.json", "w") as json_file:
    json.dump(score_data, json_file)

print("✅ Score RootMe mis à jour :", score)
