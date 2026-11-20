"""Renderiza diagramas de StarUML (.mdj) a SVG usando la geometría guardada en el archivo.

No usa StarUML (sin marca de agua) ni JavaScript. Uso como módulo:
    from render import diagramas, svg_de
    for d in diagramas(modelo): svg = svg_de(d, indice)
"""
import html, json, math
from PIL import ImageFont

FUENTES = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"
_cache = {}
def fuente(tam, estilo=0):
    k = (tam, estilo)
    if k not in _cache:
        nombre = {0: "Regular", 1: "Bold", 2: "Italic", 3: "BoldItalic"}[estilo]
        _cache[k] = ImageFont.truetype(FUENTES.format(nombre), max(1, int(round(tam))))
    return _cache[k]

def ancho(t, tam, estilo=0):
    return fuente(tam, estilo).getlength(t)

def esc(t):
    return html.escape(str(t), quote=True)

def parse_font(f):
    try:
        n, tam, est = f.split(";")
        return float(tam), int(est)
    except Exception:
        return 13.0, 0

def envolver(texto, w, tam, est):
    lineas = []
    for parrafo in str(texto).split("\n"):
        if w <= 0:
            lineas.append(parrafo); continue
        palabras = parrafo.split(" ")
        actual = ""
        for p in palabras:
            prueba = p if not actual else actual + " " + p
            if ancho(prueba, tam, est) <= w + 0.5 or not actual:
                actual = prueba
            else:
                lineas.append(actual); actual = p
        lineas.append(actual)
    return lineas

def indice(proyecto):
    ids = {}
    def w(o, padre=None):
        if isinstance(o, dict):
            if "_id" in o:
                ids[o["_id"]] = o
            for v in o.values():
                w(v)
        elif isinstance(o, list):
            for x in o:
                w(x)
    w(proyecto)
    return ids

def diagramas(proyecto):
    out = []
    def w(o):
        if isinstance(o, dict):
            if o.get("_type", "").endswith("Diagram"):
                out.append(o)
            for k, v in o.items():
                if k != "ownedViews":
                    w(v)
        elif isinstance(o, list):
            for x in o:
                w(x)
    w(proyecto)
    return out

def puntos(s):
    r = []
    for par in (s or "").split(";"):
        if ":" in par:
            x, y = par.split(":")
            r.append((float(x), float(y)))
    return r

class Lienzo:
    def __init__(self):
        self.partes = []
        self.minx = self.miny = 1e18
        self.maxx = self.maxy = -1e18
    def caja(self, x0, y0, x1, y1):
        self.minx = min(self.minx, x0); self.miny = min(self.miny, y0)
        self.maxx = max(self.maxx, x1); self.maxy = max(self.maxy, y1)
    def add(self, s):
        self.partes.append(s)

def color(v, k, defecto):
    c = v.get(k)
    return c if c else defecto

def es_visible(v):
    return v.get("visible", True) is not False

class Render:
    def __init__(self, ids):
        self.ids = ids
        self.L = Lienzo()

    def ref(self, r):
        return self.ids.get(r["$ref"]) if isinstance(r, dict) and "$ref" in r else None

    def modelo(self, v):
        return self.ref(v.get("model"))

    # ---------- primitivas
    def rect(self, x, y, w, h, v, rx=0, fill=None, dash=False, sw=1.2):
        f = fill if fill is not None else color(v, "fillColor", "#ffffff")
        d = ' stroke-dasharray="6,4"' if dash else ""
        self.L.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" ry="{rx}" fill="{f}" stroke="{color(v,"lineColor","#303744")}" stroke-width="{sw}"{d}/>')
        self.L.caja(x, y, x + w, y + h)

    def linea(self, pts, v, dash=False, sw=1.2):
        if len(pts) < 2:
            return
        d = ' stroke-dasharray="7,5"' if dash else ""
        s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.L.add(f'<polyline points="{s}" fill="none" stroke="{color(v,"lineColor","#303744")}" stroke-width="{sw}"{d}/>')
        for x, y in pts:
            self.L.caja(x, y, x, y)

    def punta(self, a, b, v, tipo):
        """Decoración en b, llegando desde a."""
        ang = math.atan2(b[1] - a[1], b[0] - a[0]); c = color(v, "lineColor", "#303744")
        def p(d, da):
            return (b[0] - d * math.cos(ang + da), b[1] - d * math.sin(ang + da))
        if tipo == "abierta":
            q1, q2 = p(14, 0.45), p(14, -0.45)
            self.L.add(f'<polyline points="{q1[0]:.1f},{q1[1]:.1f} {b[0]:.1f},{b[1]:.1f} {q2[0]:.1f},{q2[1]:.1f}" fill="none" stroke="{c}" stroke-width="1.3"/>')
        elif tipo in ("llena", "triangulo"):
            q1, q2 = p(14 if tipo == "llena" else 18, 0.42), p(14 if tipo == "llena" else 18, -0.42)
            f = c if tipo == "llena" else "#ffffff"
            self.L.add(f'<polygon points="{b[0]:.1f},{b[1]:.1f} {q1[0]:.1f},{q1[1]:.1f} {q2[0]:.1f},{q2[1]:.1f}" fill="{f}" stroke="{c}" stroke-width="1.2"/>')
        elif tipo in ("rombo", "rombo_lleno"):
            q1, q2, q3 = p(10, 0.5), p(20, 0), p(10, -0.5)
            f = c if tipo == "rombo_lleno" else "#ffffff"
            self.L.add(f'<polygon points="{b[0]:.1f},{b[1]:.1f} {q1[0]:.1f},{q1[1]:.1f} {q2[0]:.1f},{q2[1]:.1f} {q3[0]:.1f},{q3[1]:.1f}" fill="{f}" stroke="{c}" stroke-width="1.2"/>')
        elif tipo == "circulo":
            cx, cy = b[0] - 5 * math.cos(ang), b[1] - 5 * math.sin(ang)
            self.L.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="#ffffff" stroke="{c}" stroke-width="1.2"/>')

    def texto(self, v, texto=None, x=None, y=None, w=None, h=None, subrayado=False, halign=None, valign=None, rot=False):
        t = v.get("text") if texto is None else texto
        if t is None or t == "":
            return
        tam, est = parse_font(v.get("font", "Arial;13;0"))
        x = v.get("left", 0) if x is None else x
        y = v.get("top", 0) if y is None else y
        w = v.get("width", 0) if w is None else w
        h = v.get("height", 0) if h is None else h
        ha = v.get("horizontalAlignment", 2) if halign is None else halign
        va = v.get("verticalAlignment", 5) if valign is None else valign
        lineas = envolver(t, w, tam, est) if (v.get("wordWrap") or w and max(ancho(l, tam, est) for l in str(t).split("\n")) > w + 2) else str(t).split("\n")
        lh = tam * 1.18
        alto = lh * len(lineas)
        if va == 3:      # arriba
            y0 = y
        elif va == 4:    # abajo
            y0 = y + h - alto
        else:
            y0 = y + (h - alto) / 2 if h else y
        peso = ' font-weight="bold"' if est in (1, 3) else ""
        it = ' font-style="italic"' if est in (2, 3) else ""
        sub = ' text-decoration="underline"' if subrayado else ""
        c = color(v, "fontColor", "#202735")
        for i, l in enumerate(lineas):
            lw = ancho(l, tam, est)
            if ha == 0:
                lx, anchor = x, "start"
            elif ha == 1:
                lx, anchor = x + w, "end"
            else:
                lx, anchor = x + w / 2, "middle"
            ly = y0 + lh * i + tam * 0.92
            self.L.add(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Liberation Sans, Arial, sans-serif" font-size="{tam:.1f}" fill="{c}" text-anchor="{anchor}"{peso}{it}{sub} xml:space="preserve">{esc(l)}</text>')
            ax = lx if anchor == "start" else (lx - lw if anchor == "end" else lx - lw / 2)
            self.L.caja(ax, ly - tam, ax + lw, ly + tam * 0.3)

    # ---------- nodos
    def nodo(self, v):
        t = v["_type"]; m = self.modelo(v) or {}
        x, y, w, h = v.get("left", 0), v.get("top", 0), v.get("width", 0), v.get("height", 0)
        if t in ("UMLClassView", "UMLInterfaceView", "UMLEnumerationView", "UMLDataTypeView", "UMLSignalView"):
            self.rect(x, y, w, h, v)
            for k in ("attributeCompartment", "operationCompartment", "literalCompartment", "receptionCompartment"):
                c = self.ref(v.get(k))
                if c and es_visible(c) and c.get("height", 0) > 0 and c.get("top"):
                    self.linea([(x, c["top"]), (x + w, c["top"])], v)
        elif t == "UMLObjectView":
            self.rect(x, y, w, h, v)
            c = self.ref(v.get("slotCompartment"))
            if c and es_visible(c) and c.get("top"):
                self.linea([(x, c["top"]), (x + w, c["top"])], v)
        elif t == "UMLUseCaseView":
            f = color(v, "fillColor", "#ffffff")
            self.L.add(f'<ellipse cx="{x+w/2:.1f}" cy="{y+h/2:.1f}" rx="{w/2:.1f}" ry="{h/2:.1f}" fill="{f}" stroke="{color(v,"lineColor","#303744")}" stroke-width="1.3"/>')
            self.L.caja(x, y, x + w, y + h)
        elif t in ("UMLUseCaseSubjectView",):
            self.rect(x, y, w, h, v, fill="none")
        elif t == "UMLActorView":
            c = color(v, "lineColor", "#303744")
            nc = self.ref(v.get("nameCompartment"))
            alto_fig = (nc["top"] - y) if nc and nc.get("top") and nc["top"] > y + 20 else h * 0.7
            cx = x + w / 2; s = alto_fig / 100
            r = 12 * s
            self.L.add(f'<g fill="none" stroke="{c}" stroke-width="1.5"><circle cx="{cx:.1f}" cy="{y+r+2:.1f}" r="{r:.1f}" fill="#ffffff"/>'
                       f'<line x1="{cx:.1f}" y1="{y+2*r+2:.1f}" x2="{cx:.1f}" y2="{y+62*s:.1f}"/>'
                       f'<line x1="{cx-24*s:.1f}" y1="{y+38*s:.1f}" x2="{cx+24*s:.1f}" y2="{y+38*s:.1f}"/>'
                       f'<line x1="{cx:.1f}" y1="{y+62*s:.1f}" x2="{cx-20*s:.1f}" y2="{y+95*s:.1f}"/>'
                       f'<line x1="{cx:.1f}" y1="{y+62*s:.1f}" x2="{cx+20*s:.1f}" y2="{y+95*s:.1f}"/></g>')
            self.L.caja(x, y, x + w, y + h)
        elif t in ("UMLComponentView",):
            self.rect(x, y, w, h, v)
            ix, iy = x + w - 34, y + 8
            self.L.add(f'<g fill="#ffffff" stroke="{color(v,"lineColor","#303744")}" stroke-width="1"><rect x="{ix+6}" y="{iy}" width="20" height="24"/><rect x="{ix}" y="{iy+5}" width="12" height="5"/><rect x="{ix}" y="{iy+14}" width="12" height="5"/></g>')
        elif t == "UMLArtifactView":
            self.rect(x, y, w, h, v)
            ix, iy = x + w - 28, y + 8
            self.L.add(f'<g fill="#ffffff" stroke="{color(v,"lineColor","#303744")}" stroke-width="1"><polygon points="{ix},{iy} {ix+12},{iy} {ix+18},{iy+6} {ix+18},{iy+22} {ix},{iy+22}"/><polyline points="{ix+12},{iy} {ix+12},{iy+6} {ix+18},{iy+6}"/></g>')
        elif t == "UMLNodeView":
            d = 14; c = color(v, "lineColor", "#303744"); f = color(v, "fillColor", "#ffffff")
            self.L.add(f'<polygon points="{x},{y+d} {x+d},{y} {x+w},{y} {x+w},{y+h-d} {x+w-d},{y+h}" fill="{f}" stroke="{c}" stroke-width="1.2"/>')
            self.rect(x, y + d, w - d, h - d, v)
            self.linea([(x + w - d, y + d), (x + w, y)], v)
        elif t == "UMLPackageView":
            self.rect(x, y, min(160, w * 0.4), 24, v)
            self.rect(x, y + 24, w, h - 24, v)
        elif t in ("UMLCommLifelineView",):
            self.rect(x, y, w, h, v)
        elif t == "UMLSeqLifelineView":
            lp = self.ref(v.get("linePart"))
            nc = self.ref(v.get("nameCompartment"))
            hb = (lp["top"] - y) if lp else 40
            self.rect(x, y, w, hb, v)
            if lp:
                lx = lp["left"]
                self.linea([(lx, lp["top"]), (lx, lp["top"] + lp["height"])], v, dash=True)
        elif t == "UMLActivationView":
            self.rect(x, y, w, h, v, fill="#ffffff")
        elif t == "UMLCombinedFragmentView":
            self.rect(x, y, w, h, v, fill="none")
            fl = self.ref(v.get("frameTypeLabel"))
            if fl:
                tw = ancho(fl.get("text", "alt"), *parse_font(fl.get("font", "Arial;15;0"))) + 16
                hh = fl.get("height", 18) + 8
                self.L.add(f'<polygon points="{x},{y} {x+tw+10:.1f},{y} {x+tw+10:.1f},{y+hh-8:.1f} {x+tw:.1f},{y+hh:.1f} {x},{y+hh:.1f}" fill="#ffffff" stroke="{color(v,"lineColor","#303744")}" stroke-width="1.2"/>')
        elif t == "UMLInteractionOperandView":
            par = self.ref(v.get("_parent"))
            if par and par.get("subViews") and par["subViews"][0] is not v:
                self.linea([(x, y), (x + w, y)], v, dash=True)
        elif t == "UMLActionView":
            self.rect(x, y, w, h, v, rx=16)
        elif t == "UMLControlNodeView":
            mt = m.get("_type", ""); c = color(v, "lineColor", "#303744")
            cx, cy, r = x + w / 2, y + h / 2, min(w, h) / 2
            if mt == "UMLInitialNode":
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>')
            elif mt == "UMLActivityFinalNode":
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{c}" stroke-width="1.5"/><circle cx="{cx}" cy="{cy}" r="{r*0.6:.1f}" fill="{c}"/>')
            elif mt == "UMLFlowFinalNode":
                k = r * 0.7
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{c}" stroke-width="1.5"/><path d="M{cx-k},{cy-k} L{cx+k},{cy+k} M{cx+k},{cy-k} L{cx-k},{cy+k}" stroke="{c}" stroke-width="1.5"/>')
            elif mt in ("UMLForkNode", "UMLJoinNode"):
                self.L.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
            else:
                f = color(v, "fillColor", "#ffffff")
                self.L.add(f'<polygon points="{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}" fill="{f}" stroke="{c}" stroke-width="1.3"/>')
            self.L.caja(x, y, x + w, y + h)
        elif t == "UMLActivityEdgeConnectorView":
            self.L.add(f'<circle cx="{x+w/2}" cy="{y+h/2}" r="{min(w,h)/2}" fill="#ffffff" stroke="{color(v,"lineColor","#303744")}" stroke-width="1.3"/>')
            self.L.caja(x, y, x + w, y + h)
            if not any(s.get("text") for s in v.get("subViews", [])) and m.get("name"):
                self.texto(v, m["name"], x, y, w, h)
        elif t == "UMLSwimlaneView":
            self.rect(x, y, w, h, v, fill="none")
            lab = [s for s in v.get("subViews", []) if s.get("text") and es_visible(s)]
            if lab:
                b = max(s.get("top", y) + s.get("height", 0) for s in lab) + 8
                self.linea([(x, b), (x + w, b)], v)
        elif t == "UMLStateView":
            self.rect(x, y, w, h, v, rx=14)
            nc = self.ref(v.get("nameCompartment"))
            if nc and nc.get("height"):
                yy = nc["top"] + nc["height"]
                if yy < y + h - 4:
                    self.linea([(x, yy), (x + w, yy)], v)
        elif t == "UMLPseudostateView":
            k = m.get("kind", "initial"); c = color(v, "lineColor", "#303744")
            cx, cy, r = x + w / 2, y + h / 2, min(w, h) / 2
            if k == "choice":
                self.L.add(f'<polygon points="{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}" fill="#ffffff" stroke="{c}" stroke-width="1.3"/>')
            elif k in ("fork", "join"):
                self.L.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
            else:
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>')
            self.L.caja(x, y, x + w, y + h)
        elif t == "UMLFinalStateView":
            c = color(v, "lineColor", "#303744"); cx, cy, r = x + w / 2, y + h / 2, min(w, h) / 2
            self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{c}" stroke-width="1.5"/><circle cx="{cx}" cy="{cy}" r="{r*0.6:.1f}" fill="{c}"/>')
            self.L.caja(x, y, x + w, y + h)
        elif t in ("BPMNPoolView", "BPMNLaneView"):
            self.rect(x, y, w, h, v, fill="none" if t == "BPMNLaneView" else color(v, "fillColor", "#ffffff"))
            banda = 40 if t == "BPMNPoolView" else 0
            if banda:
                self.linea([(x + banda, y), (x + banda, y + h)], v)
            nombre = m.get("name", "")
            if nombre and not any(s.get("text") == nombre and es_visible(s) for s in v.get("subViews", [])):
                tam, est = parse_font(v.get("font", "Arial;15;0"))
                bx = x + (20 if t == "BPMNPoolView" else (60 if self._en_pool(v) else 20))
                self.L.add(f'<text transform="translate({bx:.1f},{y+h/2:.1f}) rotate(-90)" font-family="Liberation Sans, Arial" font-size="{tam}" text-anchor="middle" dominant-baseline="middle" font-weight="bold" fill="{color(v,"fontColor","#202735")}">{esc(nombre)}</text>')
        elif t == "BPMNTaskView":
            self.rect(x, y, w, h, v, rx=12)
            if not any(s.get("text") and es_visible(s) for s in v.get("subViews", [])):
                self.texto(v, m.get("name", ""), x + 6, y, w - 12, h)
        elif t == "BPMNEventView":
            mt = m.get("_type", ""); c = color(v, "lineColor", "#303744"); cx, cy, r = x + w / 2, y + h / 2, min(w, h) / 2
            sw = 3.5 if "End" in mt else 1.4
            f = color(v, "fillColor", "#ffffff")
            self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" stroke="{c}" stroke-width="{sw}"/>')
            if "Intermediate" in mt or "Boundary" in mt:
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r-4}" fill="none" stroke="{c}" stroke-width="1.2"/>')
            defs = m.get("eventDefinitions") or []
            if defs:
                dt = defs[0].get("_type", "")
                if "Link" in dt:
                    self.L.add(f'<polygon points="{cx-r*0.45:.1f},{cy-r*0.2:.1f} {cx+r*0.05:.1f},{cy-r*0.2:.1f} {cx+r*0.05:.1f},{cy-r*0.45:.1f} {cx+r*0.5:.1f},{cy:.1f} {cx+r*0.05:.1f},{cy+r*0.45:.1f} {cx+r*0.05:.1f},{cy+r*0.2:.1f} {cx-r*0.45:.1f},{cy+r*0.2:.1f}" fill="{c if "Throw" in mt else "#ffffff"}" stroke="{c}"/>')
                elif "Message" in dt:
                    self.L.add(f'<rect x="{cx-r*0.45:.1f}" y="{cy-r*0.3:.1f}" width="{r*0.9:.1f}" height="{r*0.6:.1f}" fill="#ffffff" stroke="{c}"/><polyline points="{cx-r*0.45:.1f},{cy-r*0.3:.1f} {cx:.1f},{cy+r*0.05:.1f} {cx+r*0.45:.1f},{cy-r*0.3:.1f}" fill="none" stroke="{c}"/>')
                elif "Timer" in dt:
                    self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{r*0.5:.1f}" fill="#ffffff" stroke="{c}"/><polyline points="{cx},{cy-r*0.35:.1f} {cx},{cy} {cx+r*0.25:.1f},{cy}" fill="none" stroke="{c}"/>')
            self.L.caja(x, y, x + w, y + h)
        elif t == "BPMNGatewayView":
            mt = m.get("_type", ""); c = color(v, "lineColor", "#303744"); cx, cy = x + w / 2, y + h / 2
            f = color(v, "fillColor", "#ffffff")
            self.L.add(f'<polygon points="{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}" fill="{f}" stroke="{c}" stroke-width="1.4"/>')
            k = w * 0.18
            if "Parallel" in mt:
                self.L.add(f'<path d="M{cx},{cy-k*1.3} L{cx},{cy+k*1.3} M{cx-k*1.3},{cy} L{cx+k*1.3},{cy}" stroke="{c}" stroke-width="3"/>')
            elif "Exclusive" in mt:
                self.L.add(f'<path d="M{cx-k},{cy-k} L{cx+k},{cy+k} M{cx+k},{cy-k} L{cx-k},{cy+k}" stroke="{c}" stroke-width="3"/>')
            elif "Inclusive" in mt:
                self.L.add(f'<circle cx="{cx}" cy="{cy}" r="{k*1.2:.1f}" fill="none" stroke="{c}" stroke-width="2.5"/>')
            self.L.caja(x, y, x + w, y + h)

    def _en_pool(self, v):
        return bool(self.ref(v.get("containerView")))

    # ---------- aristas
    def arista(self, v):
        t = v["_type"]; m = self.modelo(v) or {}
        pts = puntos(v.get("points"))
        if len(pts) < 2:
            return
        dash = t in ("UMLDependencyView", "UMLExtendView", "UMLIncludeView", "UMLInterfaceRealizationView",
                     "UMLRealizationView", "UMLAbstractionView", "BPMNMessageFlowView")
        if t == "UMLSeqMessageView" and m.get("messageSort") in ("reply", "createMessage"):
            dash = True
        self.linea(pts, v, dash=dash, sw=1.25)
        cab, cola = (pts[-2], pts[-1]), (pts[1], pts[0])
        if t in ("UMLGeneralizationView", "UMLInterfaceRealizationView", "UMLRealizationView"):
            self.punta(*cab, v, "triangulo")
        elif t in ("UMLDependencyView", "UMLExtendView", "UMLIncludeView", "UMLAbstractionView",
                   "UMLTransitionView", "UMLControlFlowView", "UMLObjectFlowView"):
            self.punta(*cab, v, "abierta")
        elif t == "BPMNSequenceFlowView":
            self.punta(*cab, v, "llena")
        elif t == "BPMNMessageFlowView":
            self.punta(*cab, v, "triangulo"); self.punta(*cola, v, "circulo")
        elif t == "UMLSeqMessageView":
            s = m.get("messageSort", "synchCall")
            self.punta(*cab, v, "llena" if s == "synchCall" else "abierta")
        elif t in ("UMLAssociationView", "UMLLinkView", "UMLConnectorView", "UMLCommunicationPathView"):
            e1, e2 = m.get("end1") or {}, m.get("end2") or {}
            for e, seg in ((e1, cola), (e2, cab)):
                ag = e.get("aggregation")
                if ag == "composite":
                    self.punta(*seg, v, "rombo_lleno")
                elif ag == "shared":
                    self.punta(*seg, v, "rombo")
            for e, seg, otro in ((e1, cola, e2), (e2, cab, e1)):
                if e.get("navigable") == "navigable" and otro.get("navigable") != "navigable":
                    self.punta(*seg, v, "abierta")

    def mensaje_comm(self, v):
        """Flecha corta de un mensaje en diagrama de comunicación."""
        host = self.ref(v.get("hostEdge"))
        if not host:
            return
        pts = puntos(host.get("points"))
        if len(pts) < 2:
            return
        m = self.modelo(v) or {}
        (ax, ay), (bx, by) = pts[0], pts[-1]
        hacia_cab = True
        tail = self.ref(host.get("tail")); fuente_m = self.ref(m.get("source"))
        if tail and fuente_m and self.modelo(tail) is not None:
            hacia_cab = self.modelo(tail).get("_id") == fuente_m.get("_id")
        dx, dy = (bx - ax, by - ay) if hacia_cab else (ax - bx, ay - by)
        n = math.hypot(dx, dy) or 1
        x, y = v.get("left", 0), v.get("top", 0); L = v.get("width", 40) or 40
        a = (x - dx / n * L / 2, y - dy / n * L / 2); b = (x + dx / n * L / 2, y + dy / n * L / 2)
        self.linea([a, b], v, sw=1.4); self.punta(a, b, v, "llena")

    # ---------- recorrido
    ETIQUETAS = ("LabelView", "NodeLabelView", "EdgeLabelView", "UMLAttributeView", "UMLOperationView",
                 "UMLSlotView", "UMLInternalActivityView", "UMLEnumerationLiteralView", "UMLTextView", "UMLReceptionView")

    def vista(self, v, solo_texto=False):
        if not isinstance(v, dict) or not es_visible(v):
            return
        t = v.get("_type", "")
        if t in self.ETIQUETAS:
            if solo_texto:
                sub = False
                par = self.ref(v.get("_parent"))
                if par and par.get("_type") == "UMLNameCompartmentView":
                    abuelo = self.ref(par.get("_parent"))
                    if abuelo and abuelo.get("_type") in ("UMLObjectView",) and par.get("nameLabel", {}).get("$ref") == v.get("_id"):
                        sub = True
                if t == "UMLTextView":
                    self.texto(v, halign=0, valign=3)
                else:
                    self.texto(v, subrayado=sub)
            return
        if not solo_texto:
            if t == "UMLCommMessageView":
                self.mensaje_comm(v)
            elif "points" in v:
                self.arista(v)
            elif "left" in v and t not in ("UMLNameCompartmentView",) and not t.endswith("CompartmentView"):
                self.nodo(v)
        for s in v.get("subViews", []):
            self.vista(s, solo_texto)

    def diagrama(self, d):
        vs = d.get("ownedViews", [])
        # orden: contenedores, nodos, aristas y al final todo el texto encima
        cont = [v for v in vs if v.get("_type") in ("BPMNPoolView", "BPMNLaneView", "UMLSwimlaneView", "UMLUseCaseSubjectView", "UMLPackageView", "UMLNodeView", "UMLCombinedFragmentView")]
        aristas = [v for v in vs if "points" in v]
        resto = [v for v in vs if v not in cont and v not in aristas]
        for grupo in (cont, aristas, resto):
            for v in grupo:
                self.vista(v)
        for v in vs:
            self.vista(v, solo_texto=True)
        L = self.L; mg = 40
        x0, y0 = L.minx - mg, L.miny - mg
        w, h = L.maxx - L.minx + 2 * mg, L.maxy - L.miny + 2 * mg
        cuerpo = "\n".join(L.partes)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}">'
                f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#ffffff"/>\n{cuerpo}\n</svg>'), w, h

def svg_de(diagrama, ids):
    return Render(ids).diagrama(diagrama)
