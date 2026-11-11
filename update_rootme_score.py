import json
import os
import sys

import requests

# UID Root-Me
UID = "815776"

# API officielle Root-Me : https://api.www.root-me.org
# L'authentification se fait via un cookie "api_key" (clé visible dans
# Root-Me > Mon profil > Préférences).
URL = f"https://api.www.root-me.org/auteurs/{UID}"
OUTPUT = "rootme_score.json"

API_KEY = os.getenv("ROOTME_API_KEY")
if not API_KEY:
    sys.exit("❌ Clé API manquante : configure le secret GitHub ROOTME_API_KEY.")

response = requests.get(
    URL,
    cookies={"api_key": API_KEY.strip()},
    headers={"User-Agent": "rootme-score-badge"},
    timeout=30,
)
print("➡ Status Code:", response.status_code)

if response.status_code != 200:
    # On ne touche pas au badge : il garde la dernière valeur valide.
    print("➡ Réponse API:", response.text[:500])
    sys.exit(f"❌ Erreur API Root-Me ({response.status_code}). Vérifie la clé API et l'UID.")

data = response.json()
# Selon les versions, l'API renvoie un objet ou une liste contenant l'objet
if isinstance(data, list):
    data = data[0] if data else {}

score = data.get("score")
if score in (None, ""):
    print("➡ Réponse API:", json.dumps(data)[:500])
    sys.exit("❌ Champ 'score' introuvable dans la réponse.")

score_data = {
    "schemaVersion": 1,
    "label": "RootMe Score",
    "message": f"{score} pts",
    "color": "blue",
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(score_data, f)

print("✅ Score RootMe mis à jour :", score)
