# Generador del DER (notación Chen) del SGCC: .drawio multipágina + PNG por página.
import sys, math, html
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTBI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"
_mf = ImageFont.truetype(FONT, 11)
def tw(s, size=11, bold=False):
    f = ImageFont.truetype(FONTB if bold else FONT, size)
    return f.getlength(s)

EW, EH = 180, 60          # entidad
RW, RH = 128, 60          # relación (rombo)
AD = 26                   # atributo
TRI_W, TRI_H = 64, 50

# ---------------------------------------------------------------- modelo
def mult(m):
    return {"1": "(1,1)", "0..1": "(0,1)", "0..*": "(0,N)", "1..*": "(1,N)"}[m]
def card(ma, mb):
    na = ma in ("0..*", "1..*"); nb = mb in ("0..*", "1..*")
    if na and nb: return "N:M"
    if na or nb: return "1:N"
    return "1:1"

class Page:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.ents, self.rels, self.attrs, self.edges, self.texts, self.isa = {}, [], [], [], [], []

    def ent(self, key, label, x, y, weak=False, ref=False, attrs=None, sides=None, fill=None):
        self.ents[key] = dict(key=key, label=label, x=x, y=y, weak=weak, ref=ref, fill=fill)
        if attrs:
            self.place_attrs(key, attrs, sides)

    # attrs: lista de (nombre, tipo) tipo en k(clave) d(discriminador) n(normal) v(derivado)
    def place_attrs(self, key, attrs, sides):
        e = self.ents[key]
        groups = []; i = 0
        for s in sides:              # ("T", n, gap) ...
            side, n = s[0], s[1]; gap = s[2] if len(s) > 2 else 0
            off = s[3] if len(s) > 3 else 0
            groups.append((side, attrs[i:i + n], gap, off)); i += n
        assert i == len(attrs), (key, i, len(attrs))
        for side, lst, gap, off in groups:
            if side in "TB":
                ws = [max(tw(a[0]) + 16, 60) for a in lst]
                total = sum(ws) + gap
                half = len(lst) // 2 if gap else None
                x = e["x"] - total / 2 + off
                pos = []
                for j, w in enumerate(ws):
                    if gap and j == half: x += gap
                    pos.append(x + w / 2); x += w
                dist = max(105, min(190, total * 0.16))
                cy = e["y"] - EH / 2 - dist if side == "T" else e["y"] + EH / 2 + dist
                for (nm, kind), px in zip(lst, pos):
                    self.attrs.append(dict(ent=key, name=nm, kind=kind, x=px, y=cy, side=side))
            else:
                n = len(lst); sp = 40
                cx = e["x"] - EW / 2 - 110 if side == "L" else e["x"] + EW / 2 + 110
                y0 = e["y"] - (n - 1) * sp / 2 + off
                if gap: y0 -= gap / 2
                for j, (nm, kind) in enumerate(lst):
                    yy = y0 + j * sp + (gap if gap and j >= n // 2 else 0)
                    self.attrs.append(dict(ent=key, name=nm, kind=kind, x=cx, y=yy, side=side))

    def rel(self, name, a, ma, b, mb, pos=None, ident=False, card_off=(0, -46), anchors=None, roles=None):
        ea, eb = self.ents[a], self.ents[b]
        if pos is None: pos = ((ea["x"] + eb["x"]) / 2, (ea["y"] + eb["y"]) / 2)
        rw = max(RW, tw(name, 11, True) / 0.62 + 10)
        self.rels.append(dict(w=rw, name=name, a=a, b=b, ma=ma, mb=mb, x=pos[0], y=pos[1], ident=ident,
                              card=card(ma, mb), card_off=card_off, anchors=anchors, roles=roles))

    def isa_(self, sup, subs, pos, label="d"):
        self.isa.append(dict(sup=sup, subs=subs, x=pos[0], y=pos[1], label=label))

# ---------------------------------------------------------------- geometría
def clip_rect(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0: return cx, cy
    s = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * s, cy + dy * s
def clip_rhombus(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    s = 1 / (abs(dx) / (w / 2) + abs(dy) / (h / 2))
    return cx + dx * s, cy + dy * s

def rel_endpoints(p, r, which):
    """Devuelve (punto en entidad, punto en rombo) para el lado a/b."""
    e = p.ents[r[which]]
    if r["anchors"]:
        (fx, fy), (gx, gy) = r["anchors"][0 if which == "a" else 1]
        pe = (e["x"] - EW / 2 + fx * EW, e["y"] - EH / 2 + fy * EH)
        pr = (r["x"] - r["w"] / 2 + gx * r["w"], r["y"] - RH / 2 + gy * RH)
        return pe, pr
    pe = clip_rect(e["x"], e["y"], EW, EH, r["x"], r["y"])
    pr = clip_rhombus(r["x"], r["y"], r["w"], RH, e["x"], e["y"])
    return pe, pr

# ---------------------------------------------------------------- layout final
def build(p):
    """Calcula elementos dibujables con coordenadas absolutas."""
    shapes, lines, texts = [], [], []
    # líneas atributo -> entidad (centro a centro, quedan tapadas por los rellenos)
    for a in p.attrs:
        e = p.ents[a["ent"]]
        lines.append(dict(p1=(a["x"], a["y"]), p2=(e["x"], e["y"]), src=("attr", id(a)), dst=("ent", a["ent"])))
    for r in p.rels:
        for w in ("a", "b"):
            e = p.ents[r[w]]
            if r["anchors"]:
                pe, pr = rel_endpoints(p, r, w)
                lines.append(dict(p1=pe, p2=pr, src=("ent", r[w]), dst=("rel", id(r)), anchor=r["anchors"][0 if w == "a" else 1]))
            else:
                lines.append(dict(p1=(e["x"], e["y"]), p2=(r["x"], r["y"]), src=("ent", r[w]), dst=("rel", id(r))))
    for s in p.isa:
        sup = p.ents[s["sup"]]
        lines.append(dict(p1=(sup["x"], sup["y"]), p2=(s["x"], s["y"]), src=("ent", s["sup"]), dst=("isa", id(s))))
        for sb in s["subs"]:
            e = p.ents[sb]
            lines.append(dict(p1=(s["x"], s["y"]), p2=(e["x"], e["y"]), src=("isa", id(s)), dst=("ent", sb)))
    # formas
    for k, e in p.ents.items():
        shapes.append(dict(kind="ent", key=k, e=e))
    for r in p.rels:
        shapes.append(dict(kind="rel", r=r))
    for s in p.isa:
        shapes.append(dict(kind="isa", s=s))
    for a in p.attrs:
        shapes.append(dict(kind="attr", a=a))
    # textos
    for a in p.attrs:
        w = tw(a["name"]) + 6
        if a["side"] == "T":   box = (a["x"] - w / 2, a["y"] - AD / 2 - 18, w, 16, "center")
        elif a["side"] == "B": box = (a["x"] - w / 2, a["y"] + AD / 2 + 2, w, 16, "center")
        elif a["side"] == "L": box = (a["x"] - AD / 2 - 4 - w, a["y"] - 8, w, 16, "right")
        else:                  box = (a["x"] + AD / 2 + 4, a["y"] - 8, w, 16, "left")
        texts.append(dict(box=box, text=a["name"], size=11, bg=False))
    for r in p.rels:
        for w, m in (("a", r["ma"]), ("b", r["mb"])):
            pe, pr = rel_endpoints(p, r, w)
            mx, my = (pe[0] + pr[0]) / 2, (pe[1] + pr[1]) / 2
            t = mult(m)
            if r["roles"]:
                t = r["roles"][0 if w == "a" else 1] + " " + t
            wd = tw(t) + 8
            texts.append(dict(box=(mx - wd / 2, my - 8, wd, 16, "center"), text=t, size=11, bg=True))
        cw = tw(r["card"], 12, True) + 8
        pad = 8 if r["ident"] else 0
        ox_, oy_ = r["card_off"]
        if ox_ and not oy_:
            ox_ = (1 if ox_ > 0 else -1) * (r["w"] / 2 + pad + cw / 2 + 4)
        elif oy_ and not ox_:
            oy_ = (1 if oy_ > 0 else -1) * (RH / 2 + pad + 14)
        texts.append(dict(box=(r["x"] + ox_ - cw / 2, r["y"] + oy_ - 9, cw, 18, "center"),
                          text=r["card"], size=12, bold=True, bg=True))
    return shapes, lines, texts

def shape_bbox(sh):
    if sh["kind"] == "ent":
        e = sh["e"]; pad = 6 if e["weak"] else 0
        return (e["x"] - EW / 2 - pad, e["y"] - EH / 2 - pad, e["x"] + EW / 2 + pad, e["y"] + EH / 2 + pad)
    if sh["kind"] == "rel":
        r = sh["r"]; pad = 8 if r["ident"] else 0
        return (r["x"] - r["w"] / 2 - pad, r["y"] - RH / 2 - pad, r["x"] + r["w"] / 2 + pad, r["y"] + RH / 2 + pad)
    if sh["kind"] == "isa":
        s = sh["s"]; return (s["x"] - TRI_W / 2, s["y"] - TRI_H / 2, s["x"] + TRI_W / 2, s["y"] + TRI_H / 2)
    a = sh["a"]; return (a["x"] - AD / 2, a["y"] - AD / 2, a["x"] + AD / 2, a["y"] + AD / 2)

def shape_id(sh):
    if sh["kind"] == "ent": return ("ent", sh["key"])
    if sh["kind"] == "rel": return ("rel", id(sh["r"]))
    if sh["kind"] == "isa": return ("isa", id(sh["s"]))
    return ("attr", id(sh["a"]))

# ---------------------------------------------------------------- comprobación
def seg_rect(p1, p2, r, shrink=2):
    x0, y0, x1, y1 = r[0] + shrink, r[1] + shrink, r[2] - shrink, r[3] - shrink
    # Liang-Barsky
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p1[0] - x0), (dx, x1 - p1[0]), (-dy, p1[1] - y0), (dy, y1 - p1[1])):
        if pp == 0:
            if qq < 0: return False
        else:
            t = qq / pp
            if pp < 0:
                if t > t1: return False
                t0 = max(t0, t)
            else:
                if t < t0: return False
                t1 = min(t1, t)
    return True
def rect_ov(a, b, m=0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])

def check(p):
    shapes, lines, texts = build(p)
    probs = []
    boxes = [(shape_bbox(s), shape_id(s), s) for s in shapes]
    tboxes = [((t["box"][0], t["box"][1], t["box"][0] + t["box"][2], t["box"][1] + t["box"][3]), t) for t in texts]
    def nm(sid, s):
        if s["kind"] == "ent": return s["key"]
        if s["kind"] == "rel": return "<" + s["r"]["name"] + ">"
        if s["kind"] == "isa": return "ISA"
        return "attr:" + s["a"]["ent"] + "." + s["a"]["name"]
    for ln in lines:
        for bb, sid, s in boxes:
            if sid in (ln["src"], ln["dst"]): continue
            if seg_rect(ln["p1"], ln["p2"], bb):
                probs.append("linea %s->%s cruza %s" % (ln["src"][1] if ln["src"][0] == "ent" else ln["src"][0], ln["dst"][1] if ln["dst"][0]=="ent" else ln["dst"][0], nm(sid, s)))
        for bb, t in tboxes:
            if t["bg"]: continue
            if seg_rect(ln["p1"], ln["p2"], bb, shrink=1):
                # se permite si la línea es la del propio atributo (sale del círculo hacia abajo/arriba)
                probs.append("linea %s cruza texto '%s'" % (ln["src"][1] if ln["src"][0]=="ent" else ln["dst"][1] if ln["dst"][0]=="ent" else "?", t["text"]))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if rect_ov(boxes[i][0], boxes[j][0], 4):
                probs.append("formas se tocan: %s / %s" % (nm(boxes[i][1], boxes[i][2]), nm(boxes[j][1], boxes[j][2])))
    for i in range(len(tboxes)):
        for bb, sid, s in boxes:
            if rect_ov(tboxes[i][0], bb, 1):
                probs.append("texto '%s' sobre %s" % (tboxes[i][1]["text"], nm(sid, s)))
        for j in range(i + 1, len(tboxes)):
            if rect_ov(tboxes[i][0], tboxes[j][0], 2):
                probs.append("textos se tocan: '%s' / '%s' en (%d,%d)" % (tboxes[i][1]["text"], tboxes[j][1]["text"], tboxes[i][0][0], tboxes[i][0][1]))
    return probs

# ---------------------------------------------------------------- extensión total y leyenda
def extent(p):
    shapes, lines, texts = build(p)
    xs, ys = [], []
    for s in shapes:
        b = shape_bbox(s); xs += [b[0], b[2]]; ys += [b[1], b[3]]
    for t in texts:
        b = t["box"]; xs += [b[0], b[0] + b[2]]; ys += [b[1], b[1] + b[3]]
    return min(xs), min(ys), max(xs), max(ys)

LEGEND = [("ent", "Entidad fuerte"), ("weak", "Entidad débil (depende de otra)"), ("ref", "Entidad detallada en otra hoja"),
          ("rel", "Relación"), ("irel", "Relación identificadora (entidad débil)"), ("isa", "Especialización (d = disjunta)"),
          ("k", "Atributo identificador (clave)"), ("d", "Atributo discriminador (entidad débil)"),
          ("n", "Atributo descriptivo"), ("v", "Atributo derivado"),
          ("txt", "(min,max) participación · 1:N cardinalidad")]

# ---------------------------------------------------------------- drawio
STY = {
 "ent": "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#212121;strokeWidth=2;fontStyle=1;fontSize=13;",
 "ref": "rounded=0;whiteSpace=wrap;html=1;fillColor=#F2F2F2;strokeColor=#757575;strokeWidth=1.5;dashed=1;fontStyle=3;fontSize=13;fontColor=#424242;",
 "outer": "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#212121;strokeWidth=1.3;",
 "rel": "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF3B0;strokeColor=#212121;strokeWidth=2;fontStyle=1;fontSize=11;",
 "relouter": "rhombus;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#212121;strokeWidth=1.3;",
 "isa": "triangle;direction=south;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#212121;strokeWidth=2;fontStyle=1;fontSize=12;verticalAlign=top;spacingTop=2;",
 "k": "ellipse;whiteSpace=wrap;html=1;fillColor=#1A1A1A;strokeColor=#212121;strokeWidth=1.5;",
 "d": "ellipse;whiteSpace=wrap;html=1;fillColor=#43A047;strokeColor=#212121;strokeWidth=1.3;",
 "n": "ellipse;whiteSpace=wrap;html=1;fillColor=#EDE7F6;strokeColor=#212121;strokeWidth=1.3;",
 "v": "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#212121;strokeWidth=1.3;dashed=1;",
 "edge": "edgeStyle=none;html=1;endArrow=none;startArrow=none;strokeColor=#212121;strokeWidth=1.3;",
}
def esc(s): return html.escape(s, quote=True)

def drawio_page(p, ox, oy):
    out = []; n = [0]
    def nid():
        n[0] += 1; return "c%d" % n[0]
    ids = {}
    cells_v, cells_e = [], []
    def vtx(style, value, x, y, w, h, key=None):
        i = nid()
        if key is not None: ids[key] = i
        cells_v.append('<mxCell id="%s" parent="1" style="%s" value="%s" vertex="1"><mxGeometry x="%.1f" y="%.1f" width="%.1f" height="%.1f" as="geometry"/></mxCell>'
                       % (i, style, esc(value), x + ox, y + oy, w, h))
        return i
    # vértices: primero los marcos exteriores, luego formas
    for k, e in p.ents.items():
        if e["weak"]:
            vtx(STY["outer"], "", e["x"] - EW / 2 - 6, e["y"] - EH / 2 - 6, EW + 12, EH + 12)
        vtx(STY["ref"] if e["ref"] else (STY["ent"].replace("#FFFFFF", e["fill"]) if e.get("fill") else STY["ent"]), e["label"], e["x"] - EW / 2, e["y"] - EH / 2, EW, EH, ("ent", k))
    for r in p.rels:
        if r["ident"]:
            vtx(STY["relouter"], "", r["x"] - r["w"] / 2 - 8, r["y"] - RH / 2 - 8, r["w"] + 16, RH + 16)
        vtx(STY["rel"], r["name"], r["x"] - r["w"] / 2, r["y"] - RH / 2, r["w"], RH, ("rel", id(r)))
    for s in p.isa:
        vtx(STY["isa"], s["label"], s["x"] - TRI_W / 2, s["y"] - TRI_H / 2, TRI_W, TRI_H, ("isa", id(s)))
    for a in p.attrs:
        vtx(STY[a["kind"]], "", a["x"] - AD / 2, a["y"] - AD / 2, AD, AD, ("attr", id(a)))
    shapes, lines, texts = build(p)
    for t in texts:
        x, y, w, h, al = t["box"]
        st = "text;html=1;align=%s;verticalAlign=middle;fontSize=%d;strokeColor=none;spacing=0;%s%s" % (
            al, t["size"], "fontStyle=1;" if t.get("bold") else "", "fillColor=#FFFFFF;" if t["bg"] else "fillColor=none;")
        vtx(st, t["text"], x, y, w, h)
    for ln in lines:
        i = nid(); st = STY["edge"]
        if "anchor" in ln:
            (fx, fy), (gx, gy) = ln["anchor"]
            st += "exitX=%.3f;exitY=%.3f;exitDx=0;exitDy=0;entryX=%.3f;entryY=%.3f;entryDx=0;entryDy=0;" % (fx, fy, gx, gy)
        cells_e.append('<mxCell id="%s" parent="1" style="%s" edge="1" source="%s" target="%s"><mxGeometry relative="1" as="geometry"/></mxCell>'
                       % (i, st, ids[ln["src"]], ids[ln["dst"]]))
    return cells_v, cells_e, vtx

# ---------------------------------------------------------------- PNG
def png_page(p, path, scale=1.5):
    x0, y0, x1, y1 = extent(p)
    M = 50
    title_h = 70
    leg_h = 150 + (50 if getattr(p, "modules", None) else 0)
    W = int((x1 - x0 + 2 * M)); H = int((y1 - y0 + 2 * M + title_h + leg_h))
    W = max(W, 1500)
    ox, oy = -x0 + M, -y0 + M + title_h
    img = Image.new("RGB", (int(W * scale), int(H * scale)), "white")
    d = ImageDraw.Draw(img)
    S = lambda v: v * scale
    def P(pt): return (S(pt[0] + ox), S(pt[1] + oy))
    f = lambda size, b=False, bi=False: ImageFont.truetype(FONTBI if bi else (FONTB if b else FONT), int(round(size * scale)))
    shapes, lines, texts = build(p)
    for ln in lines:
        d.line([P(ln["p1"]), P(ln["p2"])], fill="#212121", width=max(1, int(round(1.3 * scale))))
    def dashed_ellipse(bb, w):
        for k in range(0, 360, 30):
            d.arc(bb, k, k + 17, fill="#212121", width=w)
    def dashed_rect(bb, w, dash=8):
        x0_, y0_, x1_, y1_ = bb
        for (a, b) in (((x0_, y0_), (x1_, y0_)), ((x1_, y0_), (x1_, y1_)), ((x1_, y1_), (x0_, y1_)), ((x0_, y1_), (x0_, y0_))):
            L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L // (dash * 2)) + 1
            for i in range(n):
                t0, t1 = i * 2 * dash / L, min(1, (i * 2 * dash + dash) / L)
                d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill="#757575", width=w)
    def center_text(cx, cy, txt, font, color="#000000"):
        lines_ = txt.split("\n"); lh = font.size * 1.2
        y = cy - lh * len(lines_) / 2
        for l in lines_:
            w = d.textlength(l, font=font); d.text((cx - w / 2, y), l, font=font, fill=color); y += lh
    def fit_font(txt, maxw, size, bold=True):
        while size > 7 and ImageFont.truetype(FONTB if bold else FONT, int(round(size * scale))).getlength(txt) > S(maxw - 10):
            size -= 0.5
        return f(size, bold)
    for sh in shapes:
        if sh["kind"] == "ent":
            e = sh["e"]
            bb = [P((e["x"] - EW / 2, e["y"] - EH / 2)), P((e["x"] + EW / 2, e["y"] + EH / 2))]
            if e["weak"]:
                ob = [P((e["x"] - EW / 2 - 6, e["y"] - EH / 2 - 6)), P((e["x"] + EW / 2 + 6, e["y"] + EH / 2 + 6))]
                d.rectangle(ob, outline="#212121", width=max(1, int(1.3 * scale)))
            if e["ref"]:
                d.rectangle(bb, fill="#F2F2F2")
                dashed_rect((bb[0][0], bb[0][1], bb[1][0], bb[1][1]), int(1.5 * scale))
                center_text(e["x"] * scale + ox * scale, e["y"] * scale + oy * scale, e["label"], fit_font(e["label"], EW, 13), "#424242")
            else:
                d.rectangle(bb, fill=e.get("fill") or "white", outline="#212121", width=int(2 * scale))
                center_text(S(e["x"] + ox), S(e["y"] + oy), e["label"], fit_font(e["label"], EW, 13))
        elif sh["kind"] == "rel":
            r = sh["r"]
            def rh(w, h):
                return [P((r["x"], r["y"] - h / 2)), P((r["x"] + w / 2, r["y"])), P((r["x"], r["y"] + h / 2)), P((r["x"] - w / 2, r["y"]))]
            if r["ident"]:
                d.polygon(rh(r["w"] + 16, RH + 16), outline="#212121", width=max(1, int(1.3 * scale)))
            d.polygon(rh(r["w"], RH), fill="#FFF3B0", outline="#212121", width=int(2 * scale))
            center_text(S(r["x"] + ox), S(r["y"] + oy), r["name"], fit_font(r["name"], r["w"] * 0.78, 11))
        elif sh["kind"] == "isa":
            s = sh["s"]
            pts = [P((s["x"] - TRI_W / 2, s["y"] - TRI_H / 2)), P((s["x"] + TRI_W / 2, s["y"] - TRI_H / 2)), P((s["x"], s["y"] + TRI_H / 2))]
            d.polygon(pts, fill="white", outline="#212121", width=int(2 * scale))
            center_text(S(s["x"] + ox), S(s["y"] + oy - 8), s["label"], f(12, True))
        else:
            a = sh["a"]
            bb = [P((a["x"] - AD / 2, a["y"] - AD / 2)), P((a["x"] + AD / 2, a["y"] + AD / 2))]
            fill = {"k": "#1A1A1A", "d": "#43A047", "n": "#EDE7F6", "v": "white"}[a["kind"]]
            if a["kind"] == "v":
                d.ellipse(bb, fill="white"); dashed_ellipse(bb, max(1, int(1.3 * scale)))
            else:
                d.ellipse(bb, fill=fill, outline="#212121", width=max(1, int(1.3 * scale)))
    for t in texts:
        x, y, w, h, al = t["box"]
        font = f(t["size"], t.get("bold", False))
        if t["bg"]:
            d.rectangle([P((x, y)), P((x + w, y + h))], fill="white")
        tl = d.textlength(t["text"], font=font)
        if al == "center": tx = S(x + ox + w / 2) - tl / 2
        elif al == "right": tx = S(x + ox + w) - tl
        else: tx = S(x + ox)
        d.text((tx, S(y + oy + h / 2) - font.size * 0.6), t["text"], font=font, fill="#000000")
    # título
    d.text((S(M), S(18)), p.title, font=f(22, True), fill="#000000")
    d.text((S(M), S(48)), "Sistema de Gestión Comercial y Clientes (SGCC) · notación de Chen · derivado del modelo de clases Clases_SGCC.mdj",
           font=f(12), fill="#424242")
    # leyenda
    ly = H - leg_h + 20
    d.text((S(M), S(ly - 8)), "Leyenda", font=f(13, True), fill="#000000")
    lx = M; row = 0; colw = 0
    items_per_row = 6
    for i, (k, txt) in enumerate(LEGEND):
        cx = M + (i % items_per_row) * 330; cy = ly + 30 + (i // items_per_row) * 50
        sx, sy = cx + 30, cy + 12
        if k in ("ent", "weak", "ref"):
            bb = [P((sx - 28, sy - 12 - oy + oy)), P((sx + 28, sy + 12))]
            bb = [(S(sx - 28), S(sy - 12)), (S(sx + 28), S(sy + 12))]
            if k == "weak":
                d.rectangle([(S(sx - 32), S(sy - 16)), (S(sx + 32), S(sy + 16))], outline="#212121", width=max(1, int(1.3 * scale)))
            if k == "ref":
                d.rectangle(bb, fill="#F2F2F2"); dashed_rect((bb[0][0], bb[0][1], bb[1][0], bb[1][1]), int(1.5 * scale))
            else:
                d.rectangle(bb, fill="white", outline="#212121", width=int(2 * scale))
        elif k in ("rel", "irel"):
            def rh(w, h): return [(S(sx), S(sy - h / 2)), (S(sx + w / 2), S(sy)), (S(sx), S(sy + h / 2)), (S(sx - w / 2), S(sy))]
            if k == "irel": d.polygon(rh(70, 36), outline="#212121", width=max(1, int(1.3 * scale)))
            d.polygon(rh(56, 26), fill="#FFF3B0", outline="#212121", width=int(2 * scale))
        elif k == "isa":
            d.polygon([(S(sx - 16), S(sy - 12)), (S(sx + 16), S(sy - 12)), (S(sx), S(sy + 12))], fill="white", outline="#212121", width=int(2 * scale))
            center_text(S(sx), S(sy - 4), "d", f(10, True))
        elif k in ("k", "d", "n", "v"):
            bb = [(S(sx - 11), S(sy - 11)), (S(sx + 11), S(sy + 11))]
            fill = {"k": "#1A1A1A", "d": "#43A047", "n": "#EDE7F6", "v": "white"}[k]
            if k == "v": d.ellipse(bb, fill="white"); dashed_ellipse(bb, max(1, int(1.3 * scale)))
            else: d.ellipse(bb, fill=fill, outline="#212121", width=max(1, int(1.3 * scale)))
        else:
            d.text((S(sx - 28), S(sy - 8)), "(1,N)  1:N", font=f(11, True), fill="#000000")
        d.text((S(cx + 72), S(sy - 8)), txt, font=f(11), fill="#000000")
    for i, (col, txt) in enumerate(getattr(p, "modules", [])):
        cx = M + i * 330; sy = ly + 30 + 2 * 50 + 12
        d.rectangle([(S(cx + 2), S(sy - 12)), (S(cx + 58), S(sy + 12))], fill=col, outline="#212121", width=int(2 * scale))
        d.text((S(cx + 72), S(sy - 8)), txt, font=f(11), fill="#000000")
    img.save(path, optimize=True)
    return ox, oy, W, H

# ---------------------------------------------------------------- drawio leyenda y título (mismas posiciones que el PNG)
def drawio_full(pages, path):
    out = ['<mxfile host="app.diagrams.net" agent="SGCC-DER" version="24.0.0">']
    for pi, p in enumerate(pages):
        x0, y0, x1, y1 = extent(p)
        M, title_h, leg_h = 50, 70, 150 + (50 if getattr(p, "modules", None) else 0)
        W = max(int(x1 - x0 + 2 * M), 1500); H = int(y1 - y0 + 2 * M + title_h + leg_h)
        ox, oy = -x0 + M, -y0 + M + title_h
        cv, ce, vtx = drawio_page(p, ox, oy)
        def v2(style, value, x, y, w, h):  # coordenadas absolutas de página
            vtx(style, value, x - ox, y - oy, w, h)
        v2("text;html=1;align=left;verticalAlign=middle;fontSize=22;fontStyle=1;strokeColor=none;fillColor=none;", p.title, M, 14, 1400, 30)
        v2("text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#424242;strokeColor=none;fillColor=none;",
           "Sistema de Gestión Comercial y Clientes (SGCC) · notación de Chen · derivado del modelo de clases Clases_SGCC.mdj", M, 44, 1400, 20)
        ly = H - leg_h + 20
        v2("text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=1;strokeColor=none;fillColor=none;", "Leyenda", M, ly - 10, 200, 20)
        for i, (k, txt) in enumerate(LEGEND):
            cx = M + (i % 6) * 330; cy = ly + 30 + (i // 6) * 50; sx, sy = cx + 30, cy + 12
            if k == "weak": v2(STY["outer"], "", sx - 32, sy - 16, 64, 32)
            if k in ("ent", "weak"): v2(STY["ent"], "", sx - 28, sy - 12, 56, 24)
            if k == "ref": v2(STY["ref"], "", sx - 28, sy - 12, 56, 24)
            if k == "irel": v2(STY["relouter"], "", sx - 35, sy - 18, 70, 36)
            if k in ("rel", "irel"): v2(STY["rel"], "", sx - 28, sy - 13, 56, 26)
            if k == "isa": v2(STY["isa"].replace("fontSize=12", "fontSize=10"), "d", sx - 16, sy - 12, 32, 24)
            if k in ("k", "d", "n", "v"): v2(STY[k], "", sx - 11, sy - 11, 22, 22)
            if k == "txt": v2("text;html=1;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;strokeColor=none;fillColor=none;", "(1,N)  1:N", sx - 28, sy - 8, 80, 16)
            v2("text;html=1;align=left;verticalAlign=middle;fontSize=11;strokeColor=none;fillColor=none;", txt, cx + 72, sy - 8, 250, 16)
        for i, (col, txt) in enumerate(getattr(p, "modules", [])):
            cx = M + i * 330; sy = ly + 30 + 2 * 50 + 12
            v2(STY["ent"].replace("#FFFFFF", col), "", cx + 2, sy - 12, 56, 24)
            v2("text;html=1;align=left;verticalAlign=middle;fontSize=11;strokeColor=none;fillColor=none;", txt, cx + 72, sy - 8, 250, 16)
        out.append('<diagram name="%s" id="der_%d"><mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
                   % (esc(p.name), pi + 1, W, H))
        out += ce      # aristas primero: quedan debajo de las formas
        out += cv
        out.append('</root></mxGraphModel></diagram>')
    out.append('</mxfile>')
    open(path, "w", encoding="utf-8").write("\n".join(out))
