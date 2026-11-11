import os, json, requests
c = {"api_key": os.environ["ROOTME_API_KEY"].strip()}
h = {"User-Agent": "rootme-score-badge"}
r = requests.get("https://api.www.root-me.org/auteurs/815776", cookies=c, headers=h, timeout=30)
d = r.json(); d = d[0] if isinstance(d, list) else d
print("AUTEUR KEYS:", list(d.keys()))
for k, v in d.items():
    if isinstance(v, list):
        print(k, "len", len(v), "sample:", json.dumps(v[:2], ensure_ascii=False))
    else:
        print(k, "=", json.dumps(v, ensure_ascii=False)[:200])
r = requests.get("https://api.www.root-me.org/challenges", cookies=c, headers=h, timeout=30)
print("CHALL status", r.status_code, r.text[:800])
r = requests.get("https://api.www.root-me.org/challenges/1", cookies=c, headers=h, timeout=30)
print("CHALL1 status", r.status_code, r.text[:800])
