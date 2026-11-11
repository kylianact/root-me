"""Met à jour le badge et le README à partir de l'API Root-Me.

Un seul appel API par exécution (l'API est limitée à 20 requêtes/minute).
"""
import html
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests

UID = "815776"
URL = f"https://api.www.root-me.org/auteurs/{UID}"

# id_rubrique -> (nom, emoji, nombre total de challenges)
# Totaux relevés via https://api.www.root-me.org/challenges (novembre 2026).
CATEGORIES = {
    "68": ("Web - Serveur", "🌐", 97),
    "182": ("Réseau", "📡", 35),
    "18": ("Cryptanalyse", "🔐", 75),
    "16": ("Web - Client", "🖥️", 42),
    "67": ("Stéganographie", "🖼️", 24),
    "189": ("App - Script", "📜", 33),
    "69": ("Cracking", "🧩", 70),
    "208": ("Forensic", "🔎", 48),
    "17": ("Programmation", "💻", 29),
    "203": ("App - Système", "⚙️", 93),
    "70": ("Réaliste", "🎯", 62),
}


def fetch_profile(api_key):
    response = requests.get(
        URL,
        cookies={"api_key": api_key.strip()},
        headers={"User-Agent": "rootme-score-badge"},
        timeout=30,
    )
    print("➡ Status Code:", response.status_code)
    if response.status_code != 200:
        print("➡ Réponse API:", response.text[:500])
        sys.exit(f"❌ Erreur API Root-Me ({response.status_code}).")
    data = response.json()
    if isinstance(data, list):
        data = data[0] if data else {}
    if data.get("score") in (None, ""):
        sys.exit("❌ Champ 'score' introuvable dans la réponse.")
    return data


def bar(done, total, width=20):
    filled = round(width * done / total) if total else 0
    return "█" * filled + "░" * (width - filled)


def pct(done, total):
    return round(100 * done / total) if total else 0


def clean(title):
    title = html.unescape(title).strip()
    for ch in ("\\", "*", "_", "`", "<", ">", "|", "[", "]"):
        title = title.replace(ch, "\\" + ch)
    return title


def badge(label, value, color):
    def esc(s):
        s = str(s).replace("-", "--").replace("_", "__").replace(" ", "_")
        return quote(s, safe="")
    return f"https://img.shields.io/badge/{esc(label)}-{esc(value)}-{color}?style=for-the-badge"


def render(data, now):
    nom = data.get("nom", "")
    score = int(data["score"])
    position = data.get("position")
    rang = str(data.get("rang", "")).capitalize()
    validations = data.get("validations", [])

    by_cat = defaultdict(list)
    for v in validations:
        by_cat[str(v.get("id_rubrique"))].append(v)

    total_done = len(validations)
    total_all = sum(c[2] for c in CATEGORIES.values())
    rank_txt = f"#{position:,}".replace(",", " ") if isinstance(position, int) else "—"
    profile = f"https://www.root-me.org/{nom}"

    out = []
    w = out.append
    w("<!-- Fichier généré automatiquement par update_rootme_score.py : ne pas modifier à la main. -->")
    w('<div align="center">')
    w("")
    w("# 🛡️ Root-Me — " + nom)
    w("")
    w("*Mon parcours sur [Root-Me](https://www.root-me.org), plateforme d'apprentissage du hacking éthique.*")
    w("")
    w(f'<a href="{profile}"><img src="{badge("Score", f"{score} pts", "1f6feb")}" alt="Score"></a>')
    w(f'<a href="{profile}"><img src="{badge("Classement", rank_txt, "8957e5")}" alt="Classement"></a>')
    w(f'<a href="{profile}"><img src="{badge("Rang", rang, "2ea043")}" alt="Rang"></a>')
    w(f'<a href="{profile}"><img src="{badge("Challenges", f"{total_done} / {total_all}", "d29922")}" alt="Challenges"></a>')
    w("")
    w("</div>")
    w("")
    w("## 📊 En bref")
    w("")
    w("| Score | Classement | Rang | Challenges validés | Progression globale |")
    w("|:---:|:---:|:---:|:---:|:---:|")
    w(f"| **{score} pts** | **{rank_txt}** | **{rang}** | **{total_done} / {total_all}** "
      f"| `{bar(total_done, total_all, 15)}` {pct(total_done, total_all)} % |")
    w("")

    w("## 🗂️ Progression par catégorie")
    w("")
    w("| Catégorie | Validés | Progression | % |")
    w("|:---|:---:|:---|---:|")
    rows = sorted(
        CATEGORIES.items(),
        key=lambda kv: (-len(by_cat[kv[0]]), -pct(len(by_cat[kv[0]]), kv[1][2])),
    )
    for rid, (name, emoji, total) in rows:
        done = len(by_cat[rid])
        w(f"| {emoji} **{name}** | {done} / {total} | `{bar(done, total)}` | {pct(done, total)} % |")
    w("")

    recent = sorted(validations, key=lambda v: v.get("date", ""), reverse=True)[:5]
    if recent:
        w("## 🕒 Dernières validations")
        w("")
        w("| Date | Challenge | Catégorie |")
        w("|:---:|:---|:---|")
        for v in recent:
            name, emoji, _ = CATEGORIES.get(str(v.get("id_rubrique")), ("Autre", "❔", 0))
            date = v.get("date", "")[:10]
            date = "/".join(reversed(date.split("-"))) if date else "—"
            w(f"| {date} | {clean(v.get('titre', ''))} | {emoji} {name} |")
        w("")

    w("## ✅ Challenges validés")
    w("")
    w("<sub>Clique sur une catégorie pour afficher le détail.</sub>")
    w("")
    for rid, (name, emoji, total) in rows:
        items = by_cat[rid]
        if not items:
            continue
        w("<details>")
        w(f"<summary><b>{emoji} {name}</b> — {len(items)} / {total}</summary>")
        w("")
        for v in sorted(items, key=lambda v: html.unescape(v.get("titre", "")).strip().lower()):
            w(f"- {clean(v.get('titre', ''))}")
        w("")
        w("</details>")
        w("")

    unknown = [r for r in by_cat if r not in CATEGORIES]
    if unknown:
        print("⚠ Catégories inconnues (à ajouter dans CATEGORIES) :", unknown)

    w("---")
    w("")
    w('<div align="center">')
    w("")
    w(f"<sub>🔄 Mis à jour automatiquement via GitHub Actions et l'API Root-Me — dernière mise à jour le {now:%d/%m/%Y}.</sub>")
    w("")
    w("</div>")
    w("")
    return "\n".join(out)


def main():
    api_key = os.getenv("ROOTME_API_KEY")
    if not api_key:
        sys.exit("❌ Clé API manquante : configure le secret GitHub ROOTME_API_KEY.")

    data = fetch_profile(api_key)
    now = datetime.now(ZoneInfo("Europe/Paris"))

    with open("rootme_score.json", "w", encoding="utf-8") as f:
        json.dump({"schemaVersion": 1, "label": "RootMe Score",
                   "message": f"{data['score']} pts", "color": "blue"}, f)

    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(render(data, now))

    print("✅ Score RootMe mis à jour :", data["score"], "| validations :", len(data.get("validations", [])))


if __name__ == "__main__":
    main()
