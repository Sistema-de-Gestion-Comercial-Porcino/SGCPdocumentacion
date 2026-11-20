"""Lista asociaciones cuyas líneas atraviesan una clase ajena o se superponen con otra línea."""
import json, sys
P = json.load(open(sys.argv[1], encoding="utf-8"))
ids = {}
def w(o):
    if isinstance(o, dict):
        if "_id" in o: ids[o["_id"]] = o
        for v in o.values(): w(v)
    elif isinstance(o, list):
        for x in o: w(x)
w(P)
d = next(o for o in ids.values() if o.get("_type") == "UMLClassDiagram")
cajas = {v["_id"]: (v["left"], v["top"], v["left"] + v["width"], v["top"] + v["height"], ids[v["model"]["$ref"]]["name"])
         for v in d["ownedViews"] if v["_type"] in ("UMLClassView", "UMLEnumerationView")}
def nom(e): return ids[e["model"]["$ref"]].get("name") or "%s-%s" % (cajas[e["tail"]["$ref"]][4], cajas[e["head"]["$ref"]][4])
segs = []
malos = 0
for e in d["ownedViews"]:
    if e["_type"] != "UMLAssociationView": continue
    pts = [tuple(map(float, p.split(":"))) for p in e["points"].split(";")]
    par = cajas[e["tail"]["$ref"]][4] + "-" + cajas[e["head"]["$ref"]][4]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        segs.append((par, x1, y1, x2, y2))
        for cid, (l, t, r, b, n) in cajas.items():
            if cid in (e["tail"]["$ref"], e["head"]["$ref"]): continue
            if max(x1, x2) > l + 1 and min(x1, x2) < r - 1 and max(y1, y2) > t + 1 and min(y1, y2) < b - 1:
                print("CRUZA", par, "atraviesa", n); malos += 1
# superposición: segmentos colineales que se solapan de distintas asociaciones
for i, a in enumerate(segs):
    for b in segs[i + 1:]:
        if a[0] == b[0]: continue
        if a[1] == a[3] == b[1] == b[3] and min(max(a[2], a[4]), max(b[2], b[4])) - max(min(a[2], a[4]), min(b[2], b[4])) > 2:
            print("SOLAPA vertical", a[0], b[0], a[1]); malos += 1
        if a[2] == a[4] == b[2] == b[4] and min(max(a[1], a[3]), max(b[1], b[3])) - max(min(a[1], a[3]), min(b[1], b[3])) > 2:
            print("SOLAPA horizontal", a[0], b[0], a[2]); malos += 1
print("problemas:", malos)
