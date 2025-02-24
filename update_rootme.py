import requests

USERNAME = "TON_USERNAME"
URL = f"https://www.root-me.org/API/public/user?login={USERNAME}"

response = requests.get(URL)
if response.status_code == 200:
    data = response.json()
    score = data.get("score", "N/A")

    with open("README.md", "r") as file:
        content = file.readlines()

    with open("README.md", "w") as file:
        for line in content:
            if line.startswith("<!-- ROOTME-SCORE -->"):
                file.write(f"<!-- ROOTME-SCORE -->\n**Score Root-Me :** {score} 🏆\n")
            else:
                file.write(line)
