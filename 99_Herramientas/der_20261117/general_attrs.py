# Vista general CON atributos: misma topología que la vista general, grilla ampliada,
# lado de los atributos elegido por entidad para minimizar choques.
import sys, os, json, itertools
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import gen_der
from gen_der import Page, build, shape_bbox, shape_id, seg_rect, rect_ov, check, EW, EH, AD, TRI_W, TRI_H
from render_general import build_general, MOD
import general as G

OLD_CW, OLD_CH = 470, 300
SX = float(os.environ.get("SX", 1050)); SY = float(os.environ.get("SY", 660))

def attrs_by_entity():
    g = {}; sys.argv = ["paginas.py"]
    exec(open(os.path.join(here, "paginas.py")).read(), g)
    out = {}
    for p in g["pages"]:
        for a in p.attrs:
            if p.ents[a["ent"]]["ref"]: continue
            out.setdefault(a["ent"], [])
            if (a["name"], a["kind"]) not in out[a["ent"]]:
                out[a["ent"]].append((a["name"], a["kind"]))
    return out

def candidates(n):
    h = n // 2; c = []
    for s in "TBLR":
        c.append([(s, n)])
        c.append([(s, n, 170 if s in "TB" else 80)])
    for off in (-260, 260, -480, 480):
        c.append([("T", n, 0, off)]); c.append([("B", n, 0, off)])
    for off in (-140, 140, -240, 240):
        c.append([("L", n, 0, off)]); c.append([("R", n, 0, off)])
    if n >= 3:
        k = n - h
        for a, b in (("T", "B"), ("L", "R"), ("T", "L"), ("T", "R"), ("B", "L"), ("B", "R"), ("L", "T"), ("R", "T"), ("L", "B"), ("R", "B")):
            c.append([(a, k), (b, h)])
            c.append([(a, k, 170 if a in "TB" else 80), (b, h, 170 if b in "TB" else 80)])
    return c

def place_tmp(e, attrs, sides):
    t = Page("t", "t"); t.ents[e["key"]] = e; t.place_attrs(e["key"], attrs, sides)
    return t.attrs

def attr_geom(a):
    w = gen_der.tw(a["name"]) + 6
    if a["side"] == "T":   box = (a["x"] - w / 2, a["y"] - AD / 2 - 18, w, 16)
    elif a["side"] == "B": box = (a["x"] - w / 2, a["y"] + AD / 2 + 2, w, 16)
    elif a["side"] == "L": box = (a["x"] - AD / 2 - 4 - w, a["y"] - 8, w, 16)
    else:                  box = (a["x"] + AD / 2 + 4, a["y"] - 8, w, 16)
    circ = (a["x"] - AD / 2, a["y"] - AD / 2, a["x"] + AD / 2, a["y"] + AD / 2)
    lab = (box[0], box[1], box[0] + box[2], box[1] + box[3])
    return circ, lab

def segx(a, b, c, d):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)

def score(p, key, cand_attrs, env):
    shapes, lines, texts = env
    e = p.ents[key]; s = 0
    for a in cand_attrs:
        circ, lab = attr_geom(a)
        line = ((a["x"], a["y"]), (e["x"], e["y"]))
        for bb, sid in shapes:
            if sid == ("ent", key):
                if rect_ov(circ, bb, 6) or rect_ov(lab, bb, 2): s += 200
                continue
            if rect_ov(circ, bb, 6) or rect_ov(lab, bb, 4): s += 200
            if seg_rect(line[0], line[1], bb): s += 120
        for tb in texts:
            if rect_ov(circ, tb, 4) or rect_ov(lab, tb, 4): s += 150
            if seg_rect(line[0], line[1], tb, shrink=1): s += 60
        for p1, p2, own in lines:
            if seg_rect(p1, p2, circ, shrink=0): s += 120
            if seg_rect(p1, p2, lab, shrink=0): s += 90
            if not own and segx(line[0], line[1], p1, p2): s += 4
        dist = abs(a["x"] - e["x"]) + abs(a["y"] - e["y"]); s += dist * 0.01
    return s

def environment(p, skip_key):
    shapes, lines, texts = build(p)
    sh = []
    for s_ in shapes:
        if s_["kind"] == "attr" and s_["a"]["ent"] == skip_key: continue
        sh.append((shape_bbox(s_), shape_id(s_)))
    ln = []
    for l in lines:
        if l["src"][0] == "attr":
            a = next(x for x in p.attrs if id(x) == l["src"][1])
            if a["ent"] == skip_key: continue
        ln.append((l["p1"], l["p2"], skip_key in (l["src"][1], l["dst"][1])))
    tx = []
    for t in texts:
        b = t["box"]
        if any(t["text"] == a["name"] and a["ent"] == skip_key and abs(attr_geom(a)[1][0] - b[0]) < 0.5 for a in p.attrs): continue
        tx.append((b[0], b[1], b[0] + b[2], b[1] + b[3]))
    return sh, ln, tx

def main():
    data = json.load(open(os.path.join(here, "gen_32.json")))
    ov = {}; exec(open(os.path.join(here, "ov.py")).read(), ov)
    # posiciones: celdas * nuevo paso
    G.CW, G.CH = SX, SY
    import render_general as RG
    RG.CW, RG.CH = SX, SY
    cells = {k: tuple(v) for k, v in data["cells"].items()}
    relpos = {k: (x / OLD_CW * SX, y / OLD_CH * SY) for k, (x, y) in ov["REL_POS"].items()}
    extra = json.load(open(os.path.join(here, "attr_overrides.json"))) if os.path.exists(os.path.join(here, "attr_overrides.json")) else {}
    relpos.update({k: tuple(v) for k, v in extra.get("REL_POS", {}).items()})
    shift = {k: tuple(v) for k, v in extra.get("SHIFT", {}).items()}
    cot = (cells["COT"][0] * SX, cells["COT"][1] * SY)
    rpos = tuple(extra.get("REFLEX_POS", (cot[0], cot[1] - 300)))
    reflex = (rpos, [((0.25, 0), (0, 0.5)), ((0.75, 0), (1, 0.5))], (0, -1))
    card = {**ov.get("CARD", {}), **{k: tuple(v) for k, v in extra.get("CARD", {}).items()}}
    p = build_general(cells, relpos, None, reflex, card, shift)
    p.title = "DER SGCC · Vista general completa · 41 entidades, 59 relaciones y sus atributos"
    AT = attrs_by_entity()
    assert set(AT) == set(p.ents), set(p.ents) ^ set(AT)
    order = sorted(p.ents, key=lambda k: -len(AT[k]))
    choice = {}
    forced = {k: [tuple(x) for x in v] for k, v in extra.get("SIDES", {}).items()}
    for rnd in range(3):
        for key in order:
            p.attrs = [a for a in p.attrs if a["ent"] != key]
            env = environment(p, key)
            best = None
            cands = [forced[key]] if key in forced else candidates(len(AT[key]))
            for cand in cands:
                ca = place_tmp(p.ents[key], AT[key], cand)
                sc = score(p, key, ca, env)
                if best is None or sc < best[0]: best = (sc, cand, ca)
            p.attrs += best[2]; choice[key] = (best[1], round(best[0]))
        print("pasada", rnd, "suma", sum(v[1] for v in choice.values()))
    for k in order:
        if choice[k][1] >= 60: print("  ", k, choice[k])
    pr = check(p)
    print("problemas:", len(pr)); [print("   ", x) for x in pr[:80]]
    json.dump({k: v[0] for k, v in choice.items()}, open(os.path.join(here, "attr_choice.json"), "w"))
    return p

if __name__ == "__main__":
    p = main()
    gen_der.png_page(p, os.path.join(here, "out", "DER_SGCC_0_Vista_general.png"), scale=1.0)
    import pickle
    pickle.dump(p, open(os.path.join(here, "p0.pkl"), "wb"))
