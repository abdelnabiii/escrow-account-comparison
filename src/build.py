import json, re, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research")
B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
static = json.load(open(f"{B}/static.json", encoding="utf-8"))
ORDER = ["nbe","bm","cib","qnb","aaib","hsbc","enbd","fab","adib","hdb","bdc","alex","arab","mashreq","attijari"]
manual = json.load(open(f"{B}/manual.json", encoding="utf-8")) if os.path.exists(f"{B}/manual.json") else {"ratings":{}, "flags":{}}

banks = {}
for g in ("group1","group2","group3"):
    p = f"{R}/{g}.json"
    if os.path.exists(p):
        for b in json.load(open(p, encoding="utf-8"))["banks"]:
            banks[b["id"]] = b
legal = json.load(open(f"{R}/legal.json", encoding="utf-8")) if os.path.exists(f"{R}/legal.json") else {"legal_items":[], "legal_summary_en":"", "legal_summary_ar":"", "sabbour_shareholders":[], "mostakbal_shareholders":[], "bank_links":[]}

def blank():
    return {"value_en":"","value_ar":"","status":"unknown","source_url":"","source_title":"","accessed":"","note_en":"","note_ar":""}
def norm(d):
    d = dict(blank(), **(d or {}))
    if d["status"] not in ("verified","bank_to_confirm","unknown"): d["status"]="unknown"
    if d["status"]=="verified" and not d["source_url"]: d["status"]="bank_to_confirm"; d["note_en"]=(d["note_en"]+" No source URL recorded.").strip()
    if d["status"]=="unknown": d["source_url"]=""; d["source_title"]=""
    return d
def rate(f, d, bid):
    k = f"{bid}|{f['id']}"
    if k in manual["ratings"]: return manual["ratings"][k]
    s = d["status"]
    if s=="unknown": return 5
    if s=="bank_to_confirm" and not d["value_en"].strip(): return 5
    if f["kind"]=="cap": return 8 if s=="verified" else 6
    if f["kind"]=="branches":
        if s!="verified": return 5
        m = re.search(r"(\d[\d,]{1,5})", d["value_en"].replace(" "," "))
        if not m: return 5
        n = int(m.group(1).replace(",",""))
        return 10 if n>=500 else 8 if n>=200 else 7 if n>=100 else 6 if n>=50 else 4 if n>=20 else 3
    if f["kind"]=="cost": return 7 if s=="verified" else 5
    return 5  # timeline: neutral unless rated manually

out_banks = []
for bid in ORDER:
    src = banks.get(bid, {"id":bid,"name_en":bid,"name_ar":bid,"type":"","website":"","fields":{}})
    sf = src.get("fields",{})
    fields = {}
    for f in static["fields"]:
        fid = f["id"]
        if fid in ("s_auditor","s_sabbourview"): d = norm(sf.get("s_view"))
        else: d = norm(sf.get(fid))
        if fid=="s_sabbourview" and d["status"]=="verified":
            d["status"]="bank_to_confirm"; d["note_en"]=(d["note_en"]+" View access for a non-account-holder needs the bank's confirmation.").strip(); d["note_ar"]=(d["note_ar"]+" صلاحية اطلاع لغير صاحب الحساب تحتاج تأكيد البنك.").strip()
        d["rating"] = rate(f, d, bid)
        fields[fid] = d
    extra = {k: norm(sf.get(k)) for k in ("n_sabbour","n_conflict")}
    out_banks.append({"id":bid,"name_en":src.get("name_en",bid),"name_ar":src.get("name_ar",""),"type":src.get("type",""),"website":src.get("website",""),
                      "flags":manual["flags"].get(bid,{}),"links":extra,"fields":fields})

data = dict(static)
data["banks"] = out_banks
data["legal"] = legal
js = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
html = open(f"{B}/template.html", encoding="utf-8").read().replace("/*__DATA__*/", js)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
tot = {"verified":0,"bank_to_confirm":0,"unknown":0}
for b in out_banks:
    c = {"verified":0,"bank_to_confirm":0,"unknown":0}
    for d in b["fields"].values(): c[d["status"]]+=1; tot[d["status"]]+=1
    print(b["id"], c)
print("TOTAL", tot, "size", len(html))
