"""Vista previa PNG con Pillow (mismas coordenadas que el .mdj)."""
import math, sys
from PIL import Image, ImageDraw, ImageFont
import disposicion as D
from modelo import ACTORES, CASOS, ASOCIACIONES, GENERALIZACIONES, EXTENSIONES

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s, b=False): return ImageFont.truetype(FB if b else F, s)

def borde_elipse(r, hacia):
    cx, cy = D.centro(r); a, b = r[2] / 2, r[3] / 2
    dx, dy = hacia[0] - cx, hacia[1] - cy
    t = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2)
    return (cx + dx * t, cy + dy * t)

def borde_rect(r, hacia):
    cx, cy = D.centro(r); w, h = r[2] / 2, r[3] / 2
    dx, dy = hacia[0] - cx, hacia[1] - cy
    t = min(w / abs(dx) if dx else 1e9, h / abs(dy) if dy else 1e9)
    return (cx + dx * t, cy + dy * t)

def flecha(d, p, q, hueca=False, punteada=False, color="#303744", ancho=3):
    if punteada:
        L = math.dist(p, q); n = int(L // 18)
        for i in range(n):
            if i % 2 == 0:
                a = i / n; b = min((i + 1) / n, 1)
                d.line([(p[0] + (q[0]-p[0])*a, p[1] + (q[1]-p[1])*a), (p[0] + (q[0]-p[0])*b, p[1] + (q[1]-p[1])*b)], fill=color, width=ancho)
    else:
        d.line([p, q], fill=color, width=ancho)
    ang = math.atan2(q[1]-p[1], q[0]-p[0]); s = 26
    a1 = (q[0] - s*math.cos(ang-0.42), q[1] - s*math.sin(ang-0.42))
    a2 = (q[0] - s*math.cos(ang+0.42), q[1] - s*math.sin(ang+0.42))
    if hueca: d.polygon([q, a1, a2], fill="white", outline=color, width=ancho)
    else: d.line([a1, q, a2], fill=color, width=ancho)

def texto_centrado(d, cx, y, t, f, color="#202735"):
    w = d.textlength(t, font=f); d.text((cx - w/2, y), t, font=f, fill=color)

def dibujar(pa, pc, salida):
    W, H = 2950, int(max(r[1]+r[3] for r in pc.values()) + 160)
    img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img)
    texto_centrado(d, W/2, 30, "SGCC · Diagrama de casos de uso general", font(40, True))
    texto_centrado(d, W/2, 90, "Cada actor aparece una sola vez. Entre paréntesis: secciones del menú de la web / Android que implementan el caso.", font(22))
    texto_centrado(d, W/2, 125, "Superadministrador ▷ Propietario ▷ Administrador: cada nivel hereda los casos del nivel inferior y suma los propios.", font(22))
    bx0, bx1 = D.CX - D.UC_W/2 - 90, D.CX + D.UC_W/2 + 90
    by0, by1 = 190, H - 60
    d.rectangle([bx0, by0, bx1, by1], outline="#303744", width=3)
    texto_centrado(d, D.CX, by0 + 18, "Sistema de Gestión Comercial y Clientes (SGCC)", font(26, True))
    # asociaciones
    for a, lst in ASOCIACIONES.items():
        for c in lst:
            q = D.punta(pc[c], pa[a]); p = borde_rect(pa[a], q)
            d.line([p, q], fill="#303744", width=2)
    for h, p in GENERALIZACIONES:
        a = borde_rect(pa[h], D.centro(pa[p])); b = borde_rect(pa[p], D.centro(pa[h]))
        flecha(d, a, b, hueca=True)
    for x, base in EXTENSIONES:
        a = borde_elipse(pc[x], D.centro(pc[base])); b = borde_elipse(pc[base], D.centro(pc[x]))
        flecha(d, a, b, punteada=True)
        d.text((D.CX + 14, (a[1]+b[1])/2 - 13), "«extend»", font=font(20), fill="#303744")
    for k, nombre, secc, ext, _doc in CASOS:
        r = pc[k]
        d.ellipse([r[0], r[1], r[0]+r[2], r[1]+r[3]], fill="#fff4e0" if ext else "#eef3fb", outline="#303744", width=3)
        cx, cy = D.centro(r)
        texto_centrado(d, cx, cy - 30, nombre, font(24, True))
        texto_centrado(d, cx, cy + 4, f"({secc})", font(19))
    for k, nombre, lado in ACTORES:
        r = pa[k]; cx = r[0] + r[2]/2; y0 = r[1]
        d.ellipse([cx-14, y0, cx+14, y0+28], outline="#303744", width=3, fill="white")
        d.line([(cx, y0+28), (cx, y0+66)], fill="#303744", width=3)
        d.line([(cx-26, y0+40), (cx+26, y0+40)], fill="#303744", width=3)
        d.line([(cx, y0+66), (cx-22, y0+94)], fill="#303744", width=3)
        d.line([(cx, y0+66), (cx+22, y0+94)], fill="#303744", width=3)
        f = font(22, True); w = d.textlength(nombre, font=f)
        d.rectangle([cx - w/2 - 4, y0+97, cx + w/2 + 4, y0+124], fill="white")
        texto_centrado(d, cx, y0 + 98, nombre, f)
    img.save(salida)

if __name__ == "__main__":
    import json
    lay = json.load(open("actores.json"))
    pc = D.casos(); pa = D.actores(lay["izq"], lay["der"], lay["y_izq"], lay["y_der"])
    print("cruces:", D.cruces(pa, pc))
    dibujar(pa, pc, sys.argv[1])
