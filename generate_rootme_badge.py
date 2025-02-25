import requests
from PIL import Image, ImageDraw, ImageFont

USERNAME = "kylian_act"
URL = f"https://www.root-me.org/API/public/user?login={USERNAME}"

# Récupérer le score
response = requests.get(URL)
if response.status_code == 200:
    data = response.json()
    score = data.get("score", "N/A")
else:
    score = "N/A"

# Créer une image
img = Image.new("RGB", (300, 100), color=(30, 30, 30))
draw = ImageDraw.Draw(img)

# Charger une police (sinon utiliser une police par défaut)
try:
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()

# Ajouter du texte
draw.text((30, 30), f"RootMe: {score}", font=font, fill=(255, 255, 255))

# Sauvegarder l'image
img.save("rootme_score.png")
