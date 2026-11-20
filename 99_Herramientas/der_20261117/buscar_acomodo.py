# Búsqueda voraz del acomodo de la vista general. Uso: python3 -I buscar_acomodo.py <semilla>  -> busca_<semilla>.json (renombrar a gen_40.json)
import sys, json, random
sys.path.insert(0, ".")
import general as G
INIT = {
 "COT": (3,0), "DETCOT": (5,0), "CLASIF": (8,0), "CLIENTE": (1,0),
 "SENA": (1,2), "PAGO": (0,2), "APLIC": (0,3), "CONDPAGO": (2,3), "SEGUI": (2,4), "COMPROB": (4,3),
 "PEDIDO": (3,2), "DETPED": (5,2), "CARGO": (1,4), "PRODUCTO": (7,1), "PRECIO": (9,1),
 "ENTRADA": (8,2), "LOTE": (10,2), "EXIST": (8,3), "MOV": (9,4), "RESERVA": (7,4), "CFRIO": (10,4),
 "PESAJE": (8,5), "PREV": (6,1), "RES": (9,3), "OP": (6,5), "INSUMO": (7,6), "ANIMAL": (5,6), "CSAN": (4,7), "INCID": (6,7),
 "ENTREGA": (3,5), "RUTA": (2,6), "TRANSP": (1,6), "RECEP": (3,7), "EVID": (2,8),
 "USUARIO": (4,6), "ROL": (5,8), "PERMISO": (6,8), "SESION": (4,8), "RECUP": (0,7), "AUDIT": (1,8),
}
assert set(INIT) == set(G.ENTS) and len(set(INIT.values())) == len(INIT), set(G.ENTS) ^ set(INIT)
seed = int(sys.argv[1]); rnd = random.Random(seed)
cells = dict(INIT)
if seed:  # perturbación inicial leve
    ks = list(cells)
    for _ in range(6):
        a, b = rnd.sample(ks, 2); cells[a], cells[b] = cells[b], cells[a]
cur = G.cost(cells); print("inicio", round(cur), flush=True)
todas = [(x, y) for x in range(G.COLS) for y in range(G.ROWS)]
for ps in range(6):
    mejora = False
    orden = list(cells); rnd.shuffle(orden)
    for k in orden:
        old = cells[k]; best = (cur, None)
        for nc in todas:
            if nc == old: continue
            other = next((q for q, c in cells.items() if c == nc), None)
            cells[k] = nc
            if other: cells[other] = old
            c = G.cost(cells)
            if c < best[0] - 1e-6: best = (c, nc)
            cells[k] = old
            if other: cells[other] = nc
        if best[1]:
            nc = best[1]; other = next((q for q, c in cells.items() if c == nc), None)
            cells[k] = nc
            if other: cells[other] = old
            cur = best[0]; mejora = True
    c, bad = G.cost(cells, True)
    print("pasada", ps, round(c), len(bad), flush=True)
    json.dump({"cost": c, "cells": cells, "bad": bad}, open("busca_%d.json" % seed, "w"))
    if not mejora: break
