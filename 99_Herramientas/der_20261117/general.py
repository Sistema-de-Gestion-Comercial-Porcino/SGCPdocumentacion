# Vista general: 40 entidades + 62 relaciones (+ version_anterior), sin atributos. Ubicación en grilla por recocido simulado.
import sys, os, random, math, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from gen_der import EW, EH, RH, tw

ENTS = {  # clave: (etiqueta, módulo, débil)
 "PERMISO": ("PERMISO", "A", 0), "ROL": ("ROL", "A", 0), "USUARIO": ("USUARIO", "A", 0), "SESION": ("SESION", "A", 1),
 "RECUP": ("RECUPERACION_ACCESO", "A", 1), "AUDIT": ("REGISTRO_AUDITORIA", "A", 0),
 "CLIENTE": ("CLIENTE", "C", 0), "COT": ("COTIZACION", "C", 0), "DETCOT": ("DETALLE_COTIZACION", "C", 1),
 "PEDIDO": ("PEDIDO", "C", 0), "DETPED": ("DETALLE_PEDIDO", "C", 1), "PRODUCTO": ("PRODUCTO", "C", 0),
 "PRECIO": ("PRECIO_PRODUCTO", "C", 1), "CLASIF": ("CLASIFICACION_PRODUCTO", "C", 0), "CARGO": ("CARGO", "C", 1),
 "PAGO": ("PAGO", "F", 0), "APLIC": ("APLICACION_PAGO", "F", 1), "SENA": ("SENA", "F", 0), "CONDPAGO": ("CONDICION_PAGO", "F", 0),
 "SEGUI": ("SEGUIMIENTO_COBRO", "F", 1), "COMPROB": ("COMPROBANTE_FISCAL", "F", 0),
 "OP": ("ORDEN_PRODUCCION", "P", 0), "ANIMAL": ("ANIMAL", "P", 0), "CSAN": ("CONTROL_SANITARIO", "P", 1),
 "INSUMO": ("INSUMO_PRODUCCION", "P", 1), "PREV": ("PREVISION_PRODUCTO", "P", 1), "RES": ("RESULTADO_PRODUCCION", "P", 1),
 "INCID": ("INCIDENCIA", "P", 0), "PESAJE": ("PESAJE", "P", 0),
 "LOTE": ("LOTE", "I", 0), "EXIST": ("EXISTENCIA", "I", 0), "ENTRADA": ("ENTRADA_INVENTARIO", "I", 0), "MOV": ("MOVIMIENTO_STOCK", "I", 0),
 "RESERVA": ("RESERVA", "I", 0), "CFRIO": ("CONTROL_FRIO", "I", 0),
 "ENTREGA": ("ENTREGA", "E", 0), "RUTA": ("RUTA", "E", 0), "TRANSP": ("TRANSPORTE", "E", 0),
 "RECEP": ("RECEPCION", "E", 0), "EVID": ("EVIDENCIA_RECEPCION", "E", 1),
}
# (nombre, a, mult_a, b, mult_b, identificadora) — las mismas relaciones de las hojas 1 a 7
RELS = [
 ("autoriza", "ROL", "0..*", "PERMISO", "1..*", 0), ("asignado", "USUARIO", "0..*", "ROL", "1..*", 0),
 ("inicia", "USUARIO", "1", "SESION", "0..*", 1), ("registra", "USUARIO", "1", "AUDIT", "0..*", 0),
 ("solicita_acceso", "USUARIO", "1", "RECUP", "0..*", 1), ("cuenta_portal", "CLIENTE", "0..1", "USUARIO", "0..*", 0),
 ("registra_recepcion", "USUARIO", "1", "RECEP", "0..*", 0), ("responsable_entrega", "USUARIO", "1", "ENTREGA", "0..*", 0),
 ("responsable_orden", "USUARIO", "1", "OP", "0..*", 0), ("captura", "USUARIO", "1", "PESAJE", "0..*", 0),
 ("responsable_ruta", "USUARIO", "1", "RUTA", "0..*", 0),
 ("solicita", "CLIENTE", "1", "COT", "0..*", 0), ("contiene_cot", "COT", "1", "DETCOT", "0..*", 1),
 ("origina", "COT", "1", "PEDIDO", "0..1", 0), ("realiza", "CLIENTE", "1", "PEDIDO", "0..*", 0),
 ("contiene_ped", "PEDIDO", "1", "DETPED", "1..*", 1), ("cotizado_en", "PRODUCTO", "1", "DETCOT", "0..*", 0),
 ("pedido_en", "PRODUCTO", "1", "DETPED", "0..*", 0), ("tiene_precio", "PRODUCTO", "1", "PRECIO", "0..*", 1),
 ("genera_cargo", "PEDIDO", "1", "CARGO", "0..*", 1), ("detalla", "CARGO", "0..*", "DETPED", "0..1", 0),
 ("clasifica", "CLASIF", "1", "PRODUCTO", "0..*", 0),
 ("paga", "CLIENTE", "1", "PAGO", "0..*", 0), ("se_aplica", "PAGO", "1", "APLIC", "0..*", 1),
 ("cubre", "CARGO", "1", "APLIC", "0..*", 0), ("retiene", "SENA", "0..*", "PAGO", "1", 0),
 ("aplica_sena", "APLIC", "0..*", "SENA", "0..1", 0), ("asegura", "SENA", "0..*", "PEDIDO", "1", 0),
 ("define_condicion", "PEDIDO", "1", "CONDPAGO", "0..*", 0), ("da_seguimiento", "CONDPAGO", "1", "SEGUI", "0..*", 1),
 ("factura", "PEDIDO", "1", "COMPROB", "0..*", 0),
 ("procesa", "OP", "0..*", "ANIMAL", "0..1", 0), ("controla", "ANIMAL", "1", "CSAN", "0..*", 1),
 ("incide_animal", "INCID", "0..*", "ANIMAL", "0..1", 0), ("incide_lote", "INCID", "0..*", "LOTE", "0..1", 0),
 ("origen_orden", "LOTE", "0..*", "OP", "0..1", 0), ("consume", "OP", "1", "INSUMO", "0..*", 1),
 ("provee_insumo", "EXIST", "1", "INSUMO", "0..*", 0), ("preve", "OP", "1", "PREV", "1..*", 1),
 ("previsto_en", "PRODUCTO", "1", "PREV", "0..*", 0), ("obtiene", "OP", "1", "RES", "0..*", 1),
 ("identifica", "RES", "0..1", "LOTE", "1", 0), ("obtiene_producto", "RES", "0..*", "PRODUCTO", "1", 0),
 ("produce", "PRODUCTO", "1", "LOTE", "0..*", 0), ("almacena", "LOTE", "1", "EXIST", "0..*", 0),
 ("existencia_de", "EXIST", "0..*", "PRODUCTO", "1", 0), ("ingresa_producto", "ENTRADA", "0..*", "PRODUCTO", "1", 0),
 ("ingresa_lote", "ENTRADA", "0..*", "LOTE", "1", 0), ("ingresa_en", "ENTRADA", "0..*", "EXIST", "1", 0),
 ("origina_entrada", "ENTRADA", "0..*", "PESAJE", "1", 0), ("controla_lote", "LOTE", "0..1", "CFRIO", "0..*", 0),
 ("controla_entrega", "ENTREGA", "0..1", "CFRIO", "0..*", 0), ("registra_mov", "EXIST", "1", "MOV", "0..*", 0),
 ("reservada_en", "EXIST", "1", "RESERVA", "0..*", 0), ("reserva", "DETPED", "1", "RESERVA", "0..*", 0),
 ("pesa_lote", "LOTE", "1", "PESAJE", "0..*", 0), ("pesa_producto", "PESAJE", "0..*", "PRODUCTO", "1", 0),
 ("se_entrega", "PEDIDO", "1", "ENTREGA", "0..*", 0), ("agrupa", "RUTA", "0..1", "ENTREGA", "0..*", 0),
 ("asignado_a", "TRANSP", "1", "RUTA", "0..*", 0), ("confirma", "ENTREGA", "1", "RECEP", "0..*", 0),
 ("respalda", "RECEP", "1", "EVID", "0..*", 1),
]
# sin especialización: el modelo actual ya no tiene subclases de OrdenProduccion (tipo es un atributo)
ISA = None
REFLEX = ("COT", "version_anterior")

CW, CH = 470, 300

def rw(name): return max(128, tw(name, 11, True) / 0.62 + 10)

def boxes_for(pos):
    eb = {k: (x - EW / 2 - 12, y - EH / 2 - 12, x + EW / 2 + 12, y + EH / 2 + 12) for k, (x, y) in pos.items()}
    return eb

def seg_box(p1, p2, r):
    x0, y0, x1, y1 = r
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p1[0] - x0), (dx, x1 - p1[0]), (-dy, p1[1] - y0), (dy, y1 - p1[1])):
        if pp == 0:
            if qq < 0: return False
        else:
            t = qq / pp
            if pp < 0:
                if t > t1: return False
                if t > t0: t0 = t
            else:
                if t < t0: return False
                if t < t1: t1 = t
    return True
def segx(a, b, c, d):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if a in (c, d) or b in (c, d): return False
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)

COLS, ROWS = 11, 9

def hubs_for(pos):
    out = []
    for r in RELS:
        a, b = r[1], r[3]; pa, pb = pos[a], pos[b]
        out.append(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, rw(r[0]) + (16 if r[5] else 0), RH + (16 if r[5] else 0), [a, b]))
    if ISA:
        sup, subs = ISA
        mx = sum(pos[s][0] for s in subs) / 2; my = sum(pos[s][1] for s in subs) / 2
        out.append(((pos[sup][0] + mx) / 2, (pos[sup][1] + my) / 2, 70, 56, [sup] + subs))
    return out

def cost(cells, detail=False):
    pos = {k: (c[0] * CW, c[1] * CH) for k, c in cells.items()}
    eb = boxes_for(pos)
    hubs = hubs_for(pos)
    segs = []; hb = []
    for i, (hx, hy, w, h, ents) in enumerate(hubs):
        hb.append((hx - w / 2 - 6, hy - h / 2 - 6, hx + w / 2 + 6, hy + h / 2 + 6))
        for e in ents: segs.append((pos[e], (hx, hy), e, i))
    c = 0.0; bad = []
    for p1, p2, e, i in segs:
        for k, bx in eb.items():
            if k == e: continue
            if seg_box(p1, p2, bx): c += 1000; bad.append(("seg-ent", e, i, k))
        for j, bx in enumerate(hb):
            if j == i: continue
            if seg_box(p1, p2, bx): c += 1000; bad.append(("seg-rel", e, i, j))
    for i, d in enumerate(hb):
        for k, bx in eb.items():
            if not (d[2] <= bx[0] or bx[2] <= d[0] or d[3] <= bx[1] or bx[3] <= d[1]):
                c += 1000; bad.append(("rel-ent", i, k))
        for j in range(i + 1, len(hb)):
            e = hb[j]
            if not (d[2] <= e[0] or e[2] <= d[0] or d[3] <= e[1] or e[3] <= d[1]):
                c += 1000; bad.append(("rel-rel", i, j))
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            if segx(segs[i][0], segs[i][1], segs[j][0], segs[j][1]): c += 25
    for r in RELS:
        ca, cb = cells[r[1]], cells[r[3]]
        L = abs(ca[0] - cb[0]) + abs(ca[1] - cb[1])
        c += 6 * L * L
    # cohesión por módulo
    mods = {}
    for k, (lab, m, w) in ENTS.items(): mods.setdefault(m, []).append(cells[k])
    for m, lst in mods.items():
        mx = sum(x for x, y in lst) / len(lst); my = sum(y for x, y in lst) / len(lst)
        for x, y in lst: c += COH * (abs(x - mx) + abs(y - my))
    return (c, bad) if detail else c

REGION = {"A": (0, 0, 3, 3), "C": (3, 0, 8, 3), "F": (8, 0, 11, 4), "E": (3, 3, 7, 5), "P": (3, 5, 9, 8), "I": (0, 4, 3, 8)}

COH = 12
INIT = None
T0G = 300.0
def anneal(seed, iters):
    rnd = random.Random(seed)
    keys = list(ENTS)
    cells = {}; used = set()
    for k in keys:
        x0, y0, x1, y1 = REGION[ENTS[k][1]]
        free = [(x, y) for x in range(x0, x1) for y in range(y0, y1) if (x, y) not in used]
        if not free: free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in used]
        c = rnd.choice(free); cells[k] = c; used.add(c)
    if INIT: cells = dict(INIT)
    cur = cost(cells); best = (cur, dict(cells))
    T0 = T0G
    for it in range(iters):
        T = T0 * (1 - it / iters) + 1
        k = rnd.choice(keys)
        old = cells[k]
        nc = (rnd.randrange(COLS), rnd.randrange(ROWS)) if rnd.random() < 0.3 else \
             (min(COLS - 1, max(0, old[0] + rnd.choice((-1, 0, 1)))), min(ROWS - 1, max(0, old[1] + rnd.choice((-1, 0, 1)))))
        other = next((q for q, c in cells.items() if c == nc), None)
        cells[k] = nc
        if other: cells[other] = old
        new = cost(cells)
        if new <= cur or rnd.random() < math.exp((cur - new) / T):
            cur = new
            if cur < best[0]: best = (cur, dict(cells))
        else:
            cells[k] = old
            if other: cells[other] = nc
    return best

if __name__ == "__main__":
    seed = int(sys.argv[1]); iters = int(sys.argv[2])
    if len(sys.argv) > 3:
        g = {}; exec(open(sys.argv[3]).read(), g)
        INIT = g["INIT"]; COH = g.get("COH", COH); T0G = g.get("T0", T0G)
    b = anneal(seed, iters)
    c, bad = cost(b[1], True)
    json.dump({"cost": c, "cells": b[1], "bad": bad}, open(os.path.join(here, "gen_%d.json" % seed), "w"))
    print(seed, round(c), len(bad))
