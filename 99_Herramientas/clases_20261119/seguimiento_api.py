"""Lleva a los diagramas lo que agregó SGCPapi v4.3.0-v4.3.2 (PR #10-#12, 20 nov 2026):
SeguimientoCobro implementado, Incidencia con resolverIncidencia y orden ANULADA final.

Uso: python3 seguimiento_api.py <02_Ingenieria_de_Software>
"""
import copy, glob, json, os, random, string, sys
RAIZ = sys.argv[1]
DOC_VIEJA = "Pendiente de agregar a SGCPapi: seguimiento de cobros pedido por Finanzas."
DOC_NUEVA = "Entidad SeguimientoCobro de SGCPapi (Dominio/Entidades/SeguimientoCobro.cs): seguimiento de cobros de Finanzas."
TIT_VIEJO = " · EstadoSeguimiento acompaña a SeguimientoCobro, pendiente en la API"

def cargar(f):
    d = json.load(open(f, encoding="utf-8")); ids = {}
    def w(o):
        if isinstance(o, dict):
            if "_id" in o: ids[o["_id"]] = o
            for v in o.values(): w(v)
        elif isinstance(o, list):
            for x in o: w(x)
    w(d); return d, ids
def guardar(f, d): json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
def nid(): return "".join(random.choice(string.ascii_letters + string.digits + "+/") for _ in range(16))
def clonar(o, extra=None):
    o = copy.deepcopy(o); mapa = dict(extra or {})
    def ids_(x):
        if isinstance(x, dict):
            if "_id" in x: mapa.setdefault(x["_id"], nid())
            for v in x.values(): ids_(v)
        elif isinstance(x, list):
            for y in x: ids_(y)
    ids_(o)
    def re_(x):
        if isinstance(x, dict):
            if "_id" in x: x["_id"] = mapa[x["_id"]]
            for k, v in x.items():
                if isinstance(v, dict) and set(v) == {"$ref"} and v["$ref"] in mapa: v["$ref"] = mapa[v["$ref"]]
                else: re_(v)
        elif isinstance(x, list):
            for i, y in enumerate(x):
                if isinstance(y, dict) and set(y) == {"$ref"} and y["$ref"] in mapa: x[i] = {"$ref": mapa[y["$ref"]]}
                else: re_(y)
    re_(o); return o

# 1) textos en todas las copias del modelo
n = 0
for f in glob.glob(os.path.join(RAIZ, "**", "*.mdj"), recursive=True):
    s = open(f, encoding="utf-8").read()
    t = s.replace(DOC_VIEJA, DOC_NUEVA).replace(TIT_VIEJO, "")
    if t != s: open(f, "w", encoding="utf-8").write(t); n += 1
print("textos actualizados en", n, "archivos")

# 2) operaciones reales en el diagrama de clases
f = os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj"); d, ids = cargar(f)
OPS = {"SeguimientoCobro": [("crearSeguimiento", ["condicionId", "proximaFecha"], "ServicioFinanzas.CrearSeguimiento"),
                            ("registrarGestion", ["resultado", "proximaFecha"], "ServicioFinanzas.RegistrarGestion"),
                            ("cerrarSeguimiento", [], "ServicioFinanzas.CerrarSeguimiento")],
       "Incidencia": [("resolverIncidencia", ["motivo"], "ServicioInventario.ResolverIncidencia")]}
LINEA = 18
plant_op = next(o for o in ids.values() if o.get("_type") == "UMLOperation")
plant_ov = next(o for o in ids.values() if o.get("_type") == "UMLOperationView")
for nom, ops in OPS.items():
    c = next(o for o in ids.values() if o.get("_type") == "UMLClass" and o["name"] == nom)
    if any(o["name"] == ops[0][0] for o in c.get("operations", [])): continue
    v = next(o for o in ids.values() if o.get("_type") == "UMLClassView" and o["model"]["$ref"] == c["_id"])
    oc = next(s for s in v["subViews"] if s["_type"] == "UMLOperationCompartmentView")
    antes = len(c.get("operations", [])); c.setdefault("operations", [])
    for nombre, params, doc in ops:
        op = {"_type": "UMLOperation", "_id": nid(), "_parent": {"$ref": c["_id"]}, "visibility": "public", "name": nombre,
              "documentation": doc + " en SGCPapi."}
        if params:
            op["parameters"] = [{"_type": "UMLParameter", "_id": nid(), "_parent": {"$ref": op["_id"]}, "name": p} for p in params]
        c["operations"].append(op)
        ov = clonar(plant_ov); ov.update(_parent={"$ref": oc["_id"]}, model={"$ref": op["_id"]}, left=v["left"] + 5,
                                         top=oc["top"] + 5 + LINEA * len(oc["subViews"]), width=v["width"] - 10, height=16, text=f"+{nombre}()")
        oc["subViews"].append(ov)
    crece = LINEA * (len(c["operations"]) - max(1, antes))
    oc["height"] = 6 + LINEA * len(c["operations"]); fondo = v["top"] + v["height"]; v["height"] += crece
    for e in ids.values():                         # extremos de asociaciones apoyados en el borde inferior
        if e.get("_type", "").endswith("View") and e.get("points") and v["_id"] in (e.get("head", {}).get("$ref"), e.get("tail", {}).get("$ref")):
            pts = [tuple(map(float, p.split(":"))) for p in e["points"].split(";")]
            pts = [(x, y + crece) if abs(y - fondo) < 2 and v["left"] - 2 <= x <= v["left"] + v["width"] + 2 else (x, y) for x, y in pts]
            e["points"] = ";".join(f"{x:g}:{y:g}" for x, y in pts)
    print(nom, "+", len(ops), "operaciones; caja +", crece, "px")
guardar(f, d)

# 3) estados de SeguimientoCobro: disparadores reales
f = os.path.join(RAIZ, "04_Estados", "12_SeguimientoCobro_Estados.mdj"); d, ids = cargar(f)
nombre = lambda r: (ids.get(r["$ref"]) or {}).get("name")
NUEVO = {(None, "PENDIENTE"): ("crearSeguimiento", "condición a crédito con saldo", "fijar proximaFecha"),
         ("PENDIENTE", "REALIZADO"): ("registrarGestion", "resultado indicado", "guardar fechaGestion y resultado"),
         ("REALIZADO", "PENDIENTE"): ("registrarGestion", "saldo > 0", "fijar la próxima fecha"),
         ("PENDIENTE", "CERRADO"): ("cerrarSeguimiento", "saldo = 0", None),
         ("REALIZADO", "CERRADO"): ("registrarGestion", "saldo = 0", None)}
for t in [o for o in ids.values() if o.get("_type") == "UMLTransition"]:
    k = (nombre(t["source"]), nombre(t["target"]))
    if k not in NUEVO: continue
    trig, guard, eff = NUEVO[k]
    t["triggers"][0]["name"] = trig; t["guard"] = guard
    if eff: t["effects"] = t.get("effects") or [{"_type": "UMLActivity", "_id": nid(), "_parent": {"$ref": t["_id"]}}]; t["effects"][0]["name"] = eff
    tv = next(o for o in ids.values() if o.get("_type") == "UMLTransitionView" and o["model"]["$ref"] == t["_id"])
    ids[tv["nameLabel"]["$ref"]]["text"] = f"{trig} [{guard}]" + (f" / {eff}" if eff else "")
for o in ids.values():
    if o.get("_type") == "UMLTextView":
        if o["text"].endswith("· pendiente en SGCPapi"): o["text"] = "SeguimientoCobro · estado (EstadoSeguimiento) · SGCPapi v4.3.0"
        elif o["text"].startswith("SeguimientoCobro todavía no existe"):
            o["text"] = ("registrarGestion pasa a REALIZADO y, en la misma operación, vuelve a PENDIENTE con la próxima fecha si queda saldo, "
                         "o queda CERRADO si el saldo es 0. CERRADO no admite cambios (SEGUIMIENTO_CERRADO). Endpoints: api/v1/seguimientos-cobro.")
guardar(f, d)

# 4) estados de Incidencia: ABIERTA -> RESUELTA con resolverIncidencia
f = os.path.join(RAIZ, "04_Estados", "09_Incidencia_Estados.mdj"); d, ids = cargar(f)
if not any(o.get("_type") == "UMLState" and o["name"].startswith("RESUELTA") for o in ids.values()):
    ab = next(o for o in ids.values() if o.get("_type") == "UMLState")
    abv = next(o for o in ids.values() if o.get("_type") == "UMLStateView")
    t0 = next(o for o in ids.values() if o.get("_type") == "UMLTransition")
    t0v = next(o for o in ids.values() if o.get("_type") == "UMLTransitionView")
    reg = ids[ab["_parent"]["$ref"]]; diag = ids[abv["_parent"]["$ref"]]
    DY = 230
    rs = clonar(ab); rs["name"] = "RESUELTA (resuelta = true)"; reg["vertices"].append(rs)
    rsv = clonar(abv, {ab["_id"]: rs["_id"]})
    def bajar(x):
        if isinstance(x, dict):
            if isinstance(x.get("top"), (int, float)): x["top"] += DY
            for v in x.values(): bajar(v)
        elif isinstance(x, list):
            for y in x: bajar(y)
    bajar(rsv)
    for s in rsv["subViews"][0]["subViews"]:
        if s.get("text") == ab["name"]: s["text"] = rs["name"]
    diag["ownedViews"].append(rsv)
    tr = clonar(t0); tr.update(source={"$ref": ab["_id"]}, target={"$ref": rs["_id"]}, guard="motivo no vacío")
    tr["triggers"][0]["name"] = "resolverIncidencia"; tr["effects"][0]["name"] = "guardar resolucion y resueltaEn"
    reg["transitions"].append(tr)
    x = abv["left"] + abv["width"] / 2; y1 = abv["top"] + abv["height"]; y2 = y1 + DY - abv["height"]
    trv = clonar(t0v, {t0["_id"]: tr["_id"], abv["_id"]: rsv["_id"]})
    trv.update(tail={"$ref": abv["_id"]}, head={"$ref": rsv["_id"]}, points=f"{x:g}:{y1:g};{x:g}:{y2:g}")
    lab = next(s for s in trv["subViews"] if s["_id"] == trv["nameLabel"]["$ref"])
    lab.update(text="resolverIncidencia [motivo no vacío] / guardar resolucion y resueltaEn", left=x + 20, top=y1 + 50, width=300, height=58)
    for s in trv["subViews"]:
        if s is not lab: s["left"] = x + 20; s["top"] = y1 + 60
    diag["ownedViews"].append(trv)
    for o in ids.values():
        if o.get("_type") == "UMLTextView" and o["text"].startswith("Incidencia no tiene enumeración"):
            o["top"] += DY + 40
            o["text"] = ("Incidencia no tiene enumeración de estado: usa resuelta, resolucion y resueltaEn. Resolverla (POST incidencias/{id}/resolver, "
                         "SGCPapi v4.3.2) no rehabilita el animal ni el lote; resolverla dos veces da INCIDENCIA_YA_RESUELTA.")
    guardar(f, d); print("Incidencia: estado RESUELTA agregado")
