"""Alinea 01_Generales/Clases_SGCC.mdj con las entidades reales de SGCPapi.

Uso: python3 actualizar_clases.py <SGCPapi> <Clases_SGCC.mdj>

- Clases con el nombre de la API, sus atributos reales (sin claves foráneas, que van como asociaciones)
  y como operaciones los métodos públicos reales del servicio que las gestiona.
- SeguimientoCobro se conserva (falta agregarlo a la API).
- Las asociaciones salen de las claves foráneas de la API; se conservan nombre, multiplicidad y composición
  de las que ya existían.
- Cada clase queda en su celda de la cuadrícula; las líneas van solo por los pasillos.
- Las enumeraciones de la API se dibujan debajo.
Es idempotente: parte siempre del modelo que recibe.
"""
import base64, copy, json, os, re, sys
from api_modelo import leer, clasificar

API, MDJ = sys.argv[1], sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__))

RENOMBRAR = {"AcuerdoCredito": "CondicionPago", "CargoPedido": "Cargo", "ConsumoInsumo": "InsumoProduccion",
             "EvidenciaEntrega": "EvidenciaRecepcion", "OperacionPendiente": "Recepcion"}
QUITAR = ["FaeneoDesposte", "FabricacionDerivado", "Ubicacion"]
FUERA_DE_API = ["SeguimientoCobro"]          # se conserva en el diagrama
# Asociaciones que pasan de una clase eliminada a otra: (clase vieja) -> clase nueva
REUBICAR_EXTREMO = {"FaeneoDesposte": "OrdenProduccion", "FabricacionDerivado": "OrdenProduccion"}
# Extremos que cambian en una asociación concreta: {par viejo: (extremo viejo, extremo nuevo)}
CAMBIAR_EXTREMO = {frozenset(("Entrega", "EvidenciaRecepcion")): ("Entrega", "Recepcion"),
                   frozenset(("InsumoProduccion", "Lote")): ("Lote", "Existencia"),
                   frozenset(("Pago", "Pedido")): ("Pedido", "Cliente")}
# Celdas (columna, fila) que cambian; el resto queda donde estaba
CELDAS_NUEVAS = {"Sena": (4, 3), "EntradaInventario": (4, 4), "InsumoProduccion": (3, 3)}

# Métodos públicos reales de SGCPapi (Servicios y Patrones) que operan sobre cada clase
OPERACIONES = {
    "Usuario": [("guardar", "ServicioUsuarios"), ("estado", "ServicioUsuarios"), ("consulta", "ServicioUsuarios"), ("registrar", "ServicioAutenticacion")],
    "Sesion": [("acceder", "ServicioAutenticacion")],
    "RecuperacionAcceso": [("recuperar", "ServicioAutenticacion"), ("restablecer", "ServicioAutenticacion")],
    "RegistroAuditoria": [("registrar", "ServicioAuditoria")],
    "Cliente": [("guardar", "ServicioClientes"), ("estado", "ServicioClientes"), ("eliminar", "ServicioClientes"), ("saldos", "ServicioFinanzas")],
    "Cotizacion": [("guardar", "ServicioCotizaciones"), ("cambiar", "ServicioCotizaciones"), ("nuevaVersion", "ServicioCotizaciones"), ("vencer", "ServicioCotizaciones"), ("obtener", "ServicioCotizaciones")],
    "Pedido": [("confirmarAsync", "ServicioConfirmarPedido"), ("cancelar", "ServicioConfirmarPedido"), ("autorizarDespacho", "ServicioFinanzas")],
    "ClasificacionProducto": [("clasificacion", "ServicioCatalogo"), ("estadoClasificacion", "ServicioCatalogo")],
    "Producto": [("producto", "ServicioCatalogo"), ("estadoProducto", "ServicioCatalogo")],
    "PrecioProducto": [("vigente", "ServicioPrecios"), ("abrir", "ServicioPrecios"), ("editar", "ServicioPrecios"), ("finalizar", "ServicioPrecios")],
    "Cargo": [("cargoServicio", "ServicioFinanzas"), ("anularCargo", "ServicioFinanzas")],
    "CondicionPago": [("condicion", "ServicioFinanzas")],
    "Pago": [("pago", "ServicioFinanzas"), ("anularPago", "ServicioFinanzas")],
    "Sena": [("sena", "ServicioFinanzas"), ("aplicarSena", "ServicioFinanzas"), ("resolverSena", "ServicioFinanzas")],
    "ComprobanteFiscal": [("registrar", "ServicioFiscal")],
    "Animal": [("animal", "ServicioProduccion"), ("cambiarEstadoAnimal", "ServicioProduccion")],
    "ControlSanitario": [("sanidad", "ServicioProduccion")],
    "OrdenProduccion": [("crear", "ServicioProduccion"), ("iniciar", "ServicioProduccion"), ("confirmar", "ServicioProduccion"), ("anular", "ServicioProduccion")],
    "InsumoProduccion": [("consumir", "ServicioProduccion")],
    "ResultadoProduccion": [("crear", "FabricaResultado")],
    "Lote": [("loteApto", "ServicioInventario"), ("loteExterno", "ServicioInventario"), ("bloquearLote", "ServicioInventario"), ("rechazarLote", "ServicioInventario")],
    "Existencia": [("disponible", "ServicioInventario")],
    "MovimientoStock": [("movimiento", "ServicioInventario")],
    "Pesaje": [("pesar", "ServicioInventario")],
    "EntradaInventario": [("entrada", "ServicioInventario"), ("anularEntrada", "ServicioInventario")],
    "Reserva": [("reservar", "ServicioInventario"), ("liberar", "ServicioInventario")],
    "ControlFrio": [("frio", "ServicioInventario")],
    "Transporte": [("transporte", "ServicioEntregas"), ("estadoTransporte", "ServicioEntregas")],
    "Ruta": [("crearRuta", "ServicioEntregas"), ("finalizarRuta", "ServicioEntregas")],
    "Entrega": [("preparar", "ServicioEntregas"), ("despachar", "ServicioEntregas"), ("reasignar", "ServicioEntregas"), ("obtener", "ServicioEntregas")],
    "Recepcion": [("sincronizar", "ServicioEntregas"), ("revisar", "ServicioEntregas")],
}
NOTA = ("Clases = entidades de SGCPapi (Dominio/Entidades) con sus atributos reales; las claves foráneas se dibujan como asociaciones. "
        "Las operaciones son los métodos públicos de los servicios de la API que actúan sobre cada clase.\n"
        "OrdenProduccion cubre faeneo/desposte y fabricación de derivados con su atributo tipo (TipoOrdenProduccion). "
        "Recepcion es lo que Android sincroniza al confirmar una entrega; EvidenciaRecepcion guarda sus fotos y firma.\n"
        "Existencia y ControlFrio guardan la ubicación (cámara) como texto. Sena y AplicacionPago aplican anticipos a cargos.\n"
        "SeguimientoCobro todavía no existe en la API: se conserva porque Finanzas lo necesita para el seguimiento de cobros.\n"
        "Casi todas las operaciones guardan su responsable (ResponsableId → Usuario); solo se dibujan las asociaciones con Usuario más relevantes.")

PITCH_X, X0, ANCHO = 700, 100, 470
GAP_FILA = 220
LINEA = 18

# ------------------------------------------------------------------ utilidades
usados = set()
def nid():
    while True:
        i = base64.b64encode(os.urandom(12)).decode()
        if i not in usados:
            usados.add(i); return i
def ref(i): return {"$ref": i}
def todos(o, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        acc.append(o)
        for v in o.values(): todos(v, acc)
    elif isinstance(o, list):
        for x in o: todos(x, acc)
    return acc
def clonar(pl, mapa_extra=None):
    c = copy.deepcopy(pl); mapa = dict(mapa_extra or {})
    for o in todos(c):
        if "_id" in o: mapa[o["_id"]] = nid()
    for o in todos(c):
        if "_id" in o: o["_id"] = mapa[o["_id"]]
        for k, v in list(o.items()):
            if isinstance(v, dict) and set(v) == {"$ref"} and v["$ref"] in mapa:
                v["$ref"] = mapa[v["$ref"]]
    return c

crudo = open(MDJ, encoding="utf-8").read()
P = json.loads(crudo)
ids = {o["_id"]: o for o in todos(P) if "_id" in o}
def padre(o): return ids[o["_parent"]["$ref"]]
def quitar(o): padre(o)["ownedElements"].remove(o)
usados.update(ids)
modelo = next(o for o in ids.values() if o.get("_type") == "UMLModel")
diag = next(o for o in ids.values() if o.get("_type") == "UMLClassDiagram")
clases = {o["name"]: o for o in ids.values() if o.get("_type") == "UMLClass"}
enums = {o["name"]: o for o in ids.values() if o.get("_type") == "UMLEnumeration"}
vistas_clase = {ids[v["model"]["$ref"]]["name"]: v for v in diag["ownedViews"] if v["_type"] == "UMLClassView"}

# plantillas (antes de borrar vistas)
T_CLASE = copy.deepcopy(vistas_clase["Usuario"])
T_ASOC = copy.deepcopy(next(v for v in diag["ownedViews"] if v["_type"] == "UMLAssociationView"))
T_ENUM = json.load(open(os.path.join(AQUI, "plantilla_enum_view.json"), encoding="utf-8"))
T_TEXTO = copy.deepcopy(next(v for v in diag["ownedViews"] if v["_type"] == "UMLTextView"))
def compart(v, tipo): return next(s for s in v["subViews"] if s["_type"] == tipo)
T_ATTR = copy.deepcopy(compart(T_CLASE, "UMLAttributeCompartmentView")["subViews"][0])
T_OPER = copy.deepcopy(compart(T_CLASE, "UMLOperationCompartmentView")["subViews"][0])
T_LIT = copy.deepcopy(compart(T_ENUM, "UMLEnumerationLiteralCompartmentView")["subViews"][0])
celdas = {}
xs = sorted({v["left"] for v in vistas_clase.values()}); ys = sorted({v["top"] for v in vistas_clase.values()})
for n, v in vistas_clase.items():
    celdas[RENOMBRAR.get(n, n)] = (xs.index(v["left"]), ys.index(v["top"]))
colores = {RENOMBRAR.get(n, n): v.get("fillColor") for n, v in vistas_clase.items()}
for n in QUITAR: celdas.pop(n, None)
celdas.update(CELDAS_NUEVAS)

# ------------------------------------------------------------------ API
cl, en = leer(API)
api = clasificar(cl, en)

# ------------------------------------------------------------------ enumeraciones
paquete_tipos = next(o for o in modelo["ownedElements"] if o.get("_type") == "UMLPackage")
nuevas_enum = dict(en)
nuevas_enum["EstadoSeguimiento"] = [l["name"] for l in enums.get("EstadoSeguimiento", {}).get("literals", [])] or ["PENDIENTE", "REALIZADO"]
for n in list(enums):
    if n not in nuevas_enum:
        quitar(enums[n]); del enums[n]
for n, lits in sorted(nuevas_enum.items()):
    e = enums.get(n)
    if not e:
        e = {"_type": "UMLEnumeration", "_id": nid(), "_parent": ref(paquete_tipos["_id"]), "name": n}
        paquete_tipos["ownedElements"].append(e); enums[n] = e
    viejos = {l["name"]: l for l in e.get("literals", [])}
    e["literals"] = [viejos.get(l) or {"_type": "UMLEnumerationLiteral", "_id": nid(), "_parent": ref(e["_id"]), "name": l} for l in lits]

# ------------------------------------------------------------------ clases
for viejo, nuevo in RENOMBRAR.items():
    if viejo in clases:
        c = clases.pop(viejo); c["name"] = nuevo; clases[nuevo] = c
borrados = set()
for n in QUITAR:
    if n in clases:
        borrados.add(clases[n]["_id"]); quitar(clases[n]); del clases[n]
for n in api:
    if n not in clases:
        c = {"_type": "UMLClass", "_id": nid(), "_parent": ref(modelo["_id"]), "name": n}
        modelo["ownedElements"].append(c); clases[n] = c

def tipo_uml(t):
    base = t.rstrip("?")
    if base in enums:
        return ref(enums[base]["_id"]), t.endswith("?")
    return base, t.endswith("?")
for n, c in clases.items():
    if n in FUERA_DE_API:
        for a in c.get("attributes", []):
            t = a.get("type")
            if isinstance(t, dict) and t["$ref"] not in {e["_id"] for e in enums.values()}:
                a["type"] = ref(enums["EstadoSeguimiento"]["_id"])
        c["documentation"] = "Entidad SeguimientoCobro de SGCPapi (Dominio/Entidades/SeguimientoCobro.cs): seguimiento de cobros de Finanzas."
        continue
    viejos = {a["name"].lower(): a for a in c.get("attributes", [])}
    nuevos = []
    for nombre, t in api[n]["attrs"]:
        a = viejos.get(nombre.lower()) or {"_type": "UMLAttribute", "_id": nid(), "_parent": ref(c["_id"]), "visibility": "private"}
        a["name"] = nombre
        tu, opcional = tipo_uml(t)
        a["type"] = tu
        if opcional: a["multiplicity"] = "0..1"
        else: a.pop("multiplicity", None)
        nuevos.append(a)
    c["attributes"] = nuevos
    ops_v = {o["name"]: o for o in c.get("operations", [])}
    c["operations"] = []
    for nombre, servicio in OPERACIONES.get(n, []):
        o = ops_v.get(nombre) or {"_type": "UMLOperation", "_id": nid(), "_parent": ref(c["_id"]), "visibility": "public"}
        o["name"] = nombre; o["documentation"] = f"{servicio}.{nombre[0].upper() + nombre[1:]} en SGCPapi."
        c["operations"].append(o)
    c["documentation"] = f"Entidad {n} de SGCPapi (Dominio/Entidades/{n}.cs)."
    c.pop("ownedElements", None) if not c.get("ownedElements") else None

# generalizaciones de las clases quitadas
for c in clases.values():
    if "ownedElements" in c:
        c["ownedElements"] = [g for g in c["ownedElements"] if not (g.get("_type") == "UMLGeneralization"
                              and (g["target"]["$ref"] in borrados or g["source"]["$ref"] in borrados))]
for o in list(modelo["ownedElements"]):
    if o.get("_type") == "UMLGeneralization" and (o["target"]["$ref"] in borrados or o["source"]["$ref"] in borrados):
        modelo["ownedElements"].remove(o)

# ------------------------------------------------------------------ asociaciones
id_de = {n: c["_id"] for n, c in clases.items()}
nombre_de = {c["_id"]: n for n, c in clases.items()}
viejo_nombre = {}
for o in todos(json.loads(crudo)):
    if o.get("_type") == "UMLClass": viejo_nombre[o["_id"]] = o["name"]
def nom(e): return nombre_de.get(e["reference"]["$ref"]) or viejo_nombre.get(e["reference"]["$ref"])

asociaciones = [o for o in list(modelo["ownedElements"]) if o.get("_type") == "UMLAssociation"]
# pares que exige la API
requeridos = {}
for c, v in api.items():
    nav = {p: t for p, t, _ in v["navs"]}
    for fk, t in v["fks"]:
        dest = nav.get(fk[:-2]) or (fk[:-2] if fk[:-2] in api else None)
        if fk in ("ResponsableId", "AutorId", "RevisadaPorId", "AnuladaPorId"):
            dest = "Usuario"
        if not dest or fk == "ReferenciaId": continue
        requeridos.setdefault(frozenset((c, dest)), (c, dest, t.endswith("?")))
    # muchos a muchos (colección sin clave foránea de vuelta), p. ej. Usuario.Roles y Rol.Permisos
    for p_, t_, k_ in v["navs"]:
        if k_ == "*" and not any(f[:-2] == c for f, _ in api[t_]["fks"]):
            requeridos.setdefault(frozenset((c, t_)), (None, None, None))
quedan, vistos = [], set()
for a in asociaciones:
    for e in (a["end1"], a["end2"]):
        n = nom(e)
        if n in REUBICAR_EXTREMO:
            e["reference"] = ref(id_de[REUBICAR_EXTREMO[n]])
    par = frozenset((nom(a["end1"]), nom(a["end2"])))
    if par in CAMBIAR_EXTREMO:
        viejo, nuevo = CAMBIAR_EXTREMO[par]
        for e in (a["end1"], a["end2"]):
            if nom(e) == viejo: e["reference"] = ref(id_de[nuevo])
    n1, n2 = nom(a["end1"]), nom(a["end2"])
    par = frozenset((n1, n2))
    valido = n1 in clases and n2 in clases and (par in requeridos or "SeguimientoCobro" in par)
    if not valido or par in vistos:
        quitar(a); continue
    vistos.add(par); quedan.append(a)
# las que pide la API y faltan (sin dibujar todas las de responsable)
for par, (origen, dest, opcional) in sorted(requeridos.items(), key=lambda x: sorted(x[0])):
    if par in vistos or dest == "Usuario" or origen is None:
        continue
    A = nid()
    a = {"_type": "UMLAssociation", "_id": A, "_parent": ref(modelo["_id"]),
         "end1": {"_type": "UMLAssociationEnd", "_id": nid(), "_parent": ref(A), "reference": ref(id_de[origen]), "multiplicity": "0..*"},
         "end2": {"_type": "UMLAssociationEnd", "_id": nid(), "_parent": ref(A), "reference": ref(id_de[dest]), "multiplicity": "0..1" if opcional else "1"}}
    modelo["ownedElements"].append(a); quedan.append(a); vistos.add(par)

# multiplicidades según la clave foránea real: quien la tiene es "muchos", el otro 1 o 0..1 según sea nula
NOMBRES = {frozenset(("Entrega", "Recepcion")): "confirma", frozenset(("Usuario", "Recepcion")): "registra",
           frozenset(("Animal", "OrdenProduccion")): "procesa"}
for a in quedan:
    n1, n2 = nombre_de[a["end1"]["reference"]["$ref"]], nombre_de[a["end2"]["reference"]["$ref"]]
    par = frozenset((n1, n2))
    if par in NOMBRES: a["name"] = NOMBRES[par]
    if n1 == n2 or par not in requeridos or requeridos[par][0] is None: continue
    origen, dest, opcional = requeridos[par]
    for e in (a["end1"], a["end2"]):
        n = nombre_de[e["reference"]["$ref"]]
        if n == origen:
            if e.get("multiplicity") not in ("0..*", "1..*", "0..1") or (n, dest) == ("OrdenProduccion", "Animal"):
                e["multiplicity"] = "0..*"
        else:
            e["multiplicity"] = "0..1" if opcional else "1"

# ------------------------------------------------------------------ vistas: cajas
diag["ownedViews"] = []
def alto_clase(c):
    return 30 + 10 + LINEA * max(1, len(c.get("attributes", []))) + 10 + LINEA * max(1, len(c.get("operations", []))) + 6
max_fila = {}
for n, (col, fila) in celdas.items():
    max_fila[fila] = max(max_fila.get(fila, 0), alto_clase(clases[n]))
top_fila, y = {}, 150
for fila in sorted(max_fila):
    top_fila[fila] = y; y += max_fila[fila] + GAP_FILA
y_fin_clases = y
caja = {}
def poner_texto_attr(t_attr, parent_id, model_id, texto, x, y_):
    a = clonar(t_attr, {}); a["_parent"] = ref(parent_id); a["model"] = ref(model_id)
    a.update(left=x + 5, top=y_, width=ANCHO - 10, height=16, text=texto); return a
def texto_attr(a):
    t = a.get("type")
    if isinstance(t, dict): t = ids.get(t["$ref"], {}).get("name") or next((e["name"] for e in enums.values() if e["_id"] == t["$ref"]), "?")
    return f"-{a['name']}: {t}{'[0..1]' if a.get('multiplicity') == '0..1' else ''}"

old_model_ref = T_CLASE["model"]["$ref"]
for n, (col, fila) in sorted(celdas.items(), key=lambda x: (x[1][1], x[1][0])):
    c = clases[n]; x = X0 + col * PITCH_X; y = top_fila[fila]; h = alto_clase(c)
    v = clonar(T_CLASE, {old_model_ref: c["_id"]})
    v.update(_parent=ref(diag["_id"]), model=ref(c["_id"]), left=x, top=y, width=ANCHO, height=h)
    if colores.get(n): v["fillColor"] = colores[n]
    else: v.pop("fillColor", None)
    nc = compart(v, "UMLNameCompartmentView"); nc.update(left=x, top=y, width=ANCHO, height=30)
    for lab in nc["subViews"]:
        if lab.get("text") and "(from" not in lab["text"] and lab.get("visible", True) is not False:
            lab.update(text=n, left=x + 5, top=y + 7, width=ANCHO - 10, height=16)
        if "model" in lab: lab["model"] = ref(c["_id"])
    ac = compart(v, "UMLAttributeCompartmentView"); n_at = max(1, len(c.get("attributes", [])))
    ac.update(left=x, top=y + 30, width=ANCHO, height=10 + LINEA * n_at)
    ac["subViews"] = [poner_texto_attr(T_ATTR, ac["_id"], a["_id"], texto_attr(a), x, y + 35 + LINEA * i) for i, a in enumerate(c.get("attributes", []))]
    oc = compart(v, "UMLOperationCompartmentView"); n_op = max(1, len(c.get("operations", [])))
    oc.update(left=x, top=y + 40 + LINEA * n_at, width=ANCHO, height=6 + LINEA * n_op, visible=True)
    oc["subViews"] = [poner_texto_attr(T_OPER, oc["_id"], o["_id"], f"+{o['name']}()", x, y + 45 + LINEA * n_at + LINEA * i) for i, o in enumerate(c.get("operations", []))]
    v["suppressOperations"] = False
    for s in todos(v):
        if (s.get("model") or {}).get("$ref") == old_model_ref: s["model"] = ref(c["_id"])
    diag["ownedViews"].append(v); caja[n] = (x, y, ANCHO, h, v["_id"], col, fila)

# ------------------------------------------------------------------ vistas: asociaciones por pasillos
col_der = lambda col: X0 + col * PITCH_X + ANCHO          # inicio del pasillo vertical a la derecha de col
carriles = {}
def carril(clave, base, paso, maxn):
    i = carriles.get(clave, 0); carriles[clave] = i + 1
    return base + paso * (i % maxn)
ocupado = {}   # (clase, lado) -> coordenadas ya usadas en ese lado
def _libre(claves, candidatos):
    for c in candidatos:
        if all(c not in ocupado.get(k, ()) for k in claves):
            for k in claves: ocupado.setdefault(k, set()).add(c)
            return c
    raise RuntimeError("sin lugar en %s" % (claves,))
def salida(n, lado):
    """Punto libre en un lado de la caja: der/izq desde arriba, abajo desde la izquierda, arriba desde la derecha."""
    x, y, w, h = caja[n][:4]
    if lado == "der":   cand = list(range(y + 25, y + h - 10, 20)) + list(range(y + 35, y + h - 10, 20))
    elif lado == "izq": cand = list(range(y + 35, y + h - 10, 20)) + list(range(y + 25, y + h - 10, 20))
    elif lado == "abajo": cand = list(range(x + 25, x + w - 10, 44)) + list(range(x + 47, x + w - 10, 44))
    else: cand = list(range(x + w - 25, x + 10, -44)) + list(range(x + w - 47, x + 10, -44))
    return _libre([(n, lado)], cand)
def pasillo_v(col_izq):     # pasillo entre col_izq y col_izq+1
    return carril(("v", col_izq), col_der(col_izq) + 22, 13, 14)
def pasillo_h(fila_arriba):  # pasillo debajo de la fila
    return carril(("h", fila_arriba), top_fila[fila_arriba] + max_fila[fila_arriba] + 24, 13, 13)

def ruta(a, b):
    xa, ya, wa, ha, _, ca, fa = caja[a]; xb, yb, wb, hb, _, cb, fb = caja[b]
    if fa == fb and abs(ca - cb) == 1:
        iz, de = (a, b) if ca < cb else (b, a)
        y = _libre([(iz, "der"), (de, "izq")], list(range(max(ya, yb) + 25, min(ya + ha, yb + hb) - 10, 20)) + list(range(max(ya, yb) + 35, min(ya + ha, yb + hb) - 10, 20)))
        return [(xa + wa, y), (xb, y)] if ca < cb else [(xa, y), (xb + wb, y)]
    if ca == cb and abs(fa - fb) == 1:
        ar, ab = (a, b) if fa < fb else (b, a)
        x = _libre([(ar, "abajo"), (ab, "arriba")], list(range(xa + 25, xa + wa - 10, 44)) + list(range(xa + 47, xa + wa - 10, 44)))
        return [(x, ya + ha), (x, yb)] if fa < fb else [(x, ya), (x, yb + hb)]
    if fa == fb:
        yh = pasillo_h(fa)
        x1 = salida(a, "abajo"); x2 = salida(b, "abajo")
        return [(x1, ya + ha), (x1, yh), (x2, yh), (x2, yb + hb)]
    # lateral de A -> pasillo vertical -> pasillo horizontal junto a B -> B
    if ca <= cb:
        lado_x, colv, y1 = xa + wa, ca, salida(a, "der")
    else:
        lado_x, colv, y1 = xa, ca - 1, salida(a, "izq")
    xv = pasillo_v(colv)
    if fb > fa:
        yh = pasillo_h(fb - 1); x2 = salida(b, "arriba")
        return [(lado_x, y1), (xv, y1), (xv, yh), (x2, yh), (x2, yb)]
    yh = pasillo_h(fb); x2 = salida(b, "abajo")
    return [(lado_x, y1), (xv, y1), (xv, yh), (x2, yh), (x2, yb + hb)]

old_asoc = T_ASOC["model"]["$ref"]
old_e1 = next(o for o in todos(json.loads(crudo)) if o.get("_id") == old_asoc)["end1"]["_id"]
old_e2 = next(o for o in todos(json.loads(crudo)) if o.get("_id") == old_asoc)["end2"]["_id"]
for a in quedan:
    n1, n2 = nombre_de[a["end1"]["reference"]["$ref"]], nombre_de[a["end2"]["reference"]["$ref"]]
    pts = ruta(n1, n2)
    v = clonar(T_ASOC, {old_asoc: a["_id"], old_e1: a["end1"]["_id"], old_e2: a["end2"]["_id"]})
    v.update(_parent=ref(diag["_id"]), model=ref(a["_id"]), tail=ref(caja[n1][4]), head=ref(caja[n2][4]),
             points=";".join(f"{round(x)}:{round(y)}" for x, y in pts), lineStyle=0)
    etiquetas = {s["_id"]: s for s in v["subViews"] if s["_type"] == "EdgeLabelView"}
    def poner(clave, texto, x, y):
        s = etiquetas.get(v.get(clave, {}).get("$ref"))
        if not s: return
        if texto:
            s.update(text=texto, left=round(x), top=round(y), width=round(len(texto) * 7 + 4), height=13, visible=True)
        else:
            s["visible"] = False; s.pop("text", None)
    # multiplicidades junto a cada extremo, nombre en el tramo más largo
    def junto(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        if abs(dx) >= abs(dy):
            return (p[0] + (12 if dx > 0 else -40), p[1] - 17)
        return (p[0] + 6, p[1] + (8 if dy > 0 else -22))
    poner("tailMultiplicityLabel", a["end1"].get("multiplicity", ""), *junto(pts[0], pts[1]))
    poner("headMultiplicityLabel", a["end2"].get("multiplicity", ""), *junto(pts[-1], pts[-2]))
    tramos = sorted(zip(pts, pts[1:]), key=lambda s: -abs(s[1][0] - s[0][0]) - abs(s[1][1] - s[0][1]))
    (p, q) = tramos[0]
    nombre = a.get("name", "")
    poner("nameLabel", nombre, (p[0] + q[0]) / 2 - len(nombre) * 3.5, (p[1] + q[1]) / 2 - 16)
    for k in ("stereotypeLabel", "propertyLabel", "tailRoleNameLabel", "tailPropertyLabel", "headRoleNameLabel", "headPropertyLabel"):
        poner(k, "", 0, 0)
    diag["ownedViews"].append(v)

# ------------------------------------------------------------------ vistas: enumeraciones
old_enum_model = T_ENUM["model"]["$ref"]
y = y_fin_clases + 80
tit = clonar(T_TEXTO); tit.update(_parent=ref(diag["_id"]), left=X0, top=y, width=3000, height=40, text="Enumeraciones de SGCPapi (Dominio/Enumeraciones)", font="Arial;22;1")
diag["ownedViews"].append(tit); y += 60
fila_y, alto_max, i = y, 0, 0
for n in sorted(enums):
    e = enums[n]; col = i % 6
    if col == 0 and i:
        fila_y += alto_max + 60; alto_max = 0
    x = X0 + col * PITCH_X; lits = e.get("literals", [])
    h = 50 + LINEA * len(lits) + 10
    v = clonar(T_ENUM, {old_enum_model: e["_id"]})
    v.update(_parent=ref(diag["_id"]), model=ref(e["_id"]), left=x, top=fila_y, width=ANCHO, height=h, lineColor="#303744", fontColor="#202735")
    nc = compart(v, "UMLNameCompartmentView"); nc.update(left=x, top=fila_y, width=ANCHO, height=44)
    vis = [l for l in nc["subViews"] if l.get("visible", True) is not False]
    vis[0].update(left=x + 5, top=fila_y + 5, width=ANCHO - 10, height=15, text="«enumeration»")
    vis[1].update(left=x + 5, top=fila_y + 22, width=ANCHO - 10, height=15, text=n)
    lc = compart(v, "UMLEnumerationLiteralCompartmentView"); lc.update(left=x, top=fila_y + 44, width=ANCHO, height=10 + LINEA * len(lits))
    lc["subViews"] = []
    for j, l in enumerate(lits):
        lv = clonar(T_LIT); lv.update(_parent=ref(lc["_id"]), model=ref(l["_id"]), left=x + 5, top=fila_y + 49 + LINEA * j, width=ANCHO - 10, height=15, text=l["name"])
        lc["subViews"].append(lv)
    for s in todos(v):
        if "lineColor" in s: s["lineColor"] = "#303744"
        if "fontColor" in s: s["fontColor"] = "#202735"
        if (s.get("model") or {}).get("$ref") == old_enum_model: s["model"] = ref(e["_id"])
    diag["ownedViews"].append(v); alto_max = max(alto_max, h); i += 1
y_nota = fila_y + alto_max + 80

titulo = clonar(T_TEXTO); titulo.update(_parent=ref(diag["_id"]), left=X0, top=20, width=3400, height=60, text="SGCC · Clases del sistema (alineadas con SGCPapi)")
nota = clonar(T_TEXTO); nota.update(_parent=ref(diag["_id"]), left=X0, top=y_nota, width=4000, height=200, text=NOTA, font="Arial;18;0")
diag["ownedViews"][:0] = [titulo]
diag["ownedViews"].append(nota)

# ------------------------------------------------------------------ comprobación y guardado
ids2 = {o["_id"] for o in todos(P) if "_id" in o}
malas = [o["$ref"] for o in todos(P) if isinstance(o, dict) and set(o) == {"$ref"} and o["$ref"] not in ids2]
assert not malas, malas[:5]
assert len(ids2) == len([o for o in todos(P) if "_id" in o]), "ids repetidos"
json.dump(P, open(MDJ, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
print("clases", len(clases), "asociaciones", len(quedan), "enumeraciones", len(enums), "carriles", carriles)
