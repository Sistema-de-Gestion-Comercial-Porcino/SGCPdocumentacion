"""Coordenadas del diagrama y conteo de cruces."""
import itertools
from modelo import ACTORES, CASOS, ASOCIACIONES, GENERALIZACIONES, EXTENSIONES

TOP = 330            # primer caso
PASO = 165            # separación vertical entre casos
CX = 1500            # centro de la columna de casos
UC_W, UC_H = 700, 112
EX_W, EX_H = 700, 104
ACT_W, ACT_H = 260, 120
X_IZQ = {"SA": 330, "PR": 330, "AD": 330, "FI": 330}
X_DER = 2650

def casos():
    pos = {}
    for i, (k, *_r) in enumerate(CASOS):
        ext = _r[2]
        w, h = (EX_W, EX_H) if ext else (UC_W, UC_H)
        cy = TOP + i * PASO
        pos[k] = (CX - w / 2, cy - h / 2, w, h)
    return pos

def centro(r):
    return (r[0] + r[2] / 2, r[1] + r[3] / 2)

def cruza(p1, p2, p3, p4):
    def o(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    if len({p1, p2, p3, p4}) < 4:
        return False
    return (o(p1,p2,p3) > 0) != (o(p1,p2,p4) > 0) and (o(p3,p4,p1) > 0) != (o(p3,p4,p2) > 0)

def actores(orden_izq, orden_der, y_izq, y_der):
    pos = {}
    for k, y in zip(orden_izq, y_izq):
        pos[k] = (X_IZQ[k] - ACT_W / 2, y - ACT_H / 2, ACT_W, ACT_H)
    for k, y in zip(orden_der, y_der):
        pos[k] = (X_DER - ACT_W / 2, y - ACT_H / 2, ACT_W, ACT_H)
    return pos

def punta(rc, ra):
    """Extremo izquierdo o derecho de la elipse, del lado del actor."""
    cx, cy = centro(rc)
    return (rc[0], cy) if centro(ra)[0] < cx else (rc[0] + rc[2], cy)

def segmentos(pa, pc):
    s = []
    for a, lst in ASOCIACIONES.items():
        for c in lst:
            s.append((a, c, centro(pa[a]), punta(pc[c], pa[a])))
    for h, p in GENERALIZACIONES:
        s.append((h, p, centro(pa[h]), centro(pa[p])))
    return s

def cruces(pa, pc):
    s = segmentos(pa, pc)
    n = 0
    for (a1, b1, p1, q1), (a2, b2, p2, q2) in itertools.combinations(s, 2):
        if {a1, b1} & {a2, b2}:
            continue
        if cruza(p1, q1, p2, q2):
            n += 1
    return n
