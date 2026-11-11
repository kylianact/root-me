import os, json, time, collections, requests
c = {"api_key": os.environ["ROOTME_API_KEY"].strip()}
h = {"User-Agent": "rootme-score-badge"}
d = requests.get("https://api.www.root-me.org/auteurs/815776", cookies=c, headers=h, timeout=30).json()
d = d[0] if isinstance(d, list) else d
v = collections.Counter(x["id_rubrique"] for x in d["validations"])
print("VALID BY RUB", dict(v))
for x in d["validations"]:
    print("V", x["id_rubrique"], x["titre"])
r = requests.get("https://api.www.root-me.org/challenges", cookies=c, headers=h, timeout=30).json()
print("PAGE STRUCT", type(r), len(r), [type(e).__name__ for e in r], json.dumps(r[1:], ensure_ascii=False)[:400])
allc = {}; start = 0; langs = collections.Counter()
while True:
    r = requests.get("https://api.www.root-me.org/challenges", params={"debut_challenges": start}, cookies=c, headers=h, timeout=30)
    if r.status_code != 200: print("STOP", r.status_code, r.text[:200]); break
    j = r.json(); items = list(j[0].values()) if j and isinstance(j[0], dict) else []
    if not items: break
    for it in items: allc[it["id_challenge"]] = it; langs[it.get("lang")] += 1
    start += len(items); time.sleep(0.5)
    if start > 3000: break
print("TOTAL", len(allc), "LANGS", dict(langs))
print("BY RUB", dict(collections.Counter(x["id_rubrique"] for x in allc.values())))
r = requests.get("https://api.www.root-me.org/challenges", params={"debut_challenges": 0, "lang": "fr"}, cookies=c, headers=h, timeout=30)
print("FR", r.status_code, r.text[:200])
