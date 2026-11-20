"""Alinea los diagramas de objetos (03_Objetos/CUxx_Objetos.mdj) con el modelo de clases vigente.

Uso: python3 objetos_api.py <02_Ingenieria_de_Software> [CUxx ...]

- Cada archivo vuelve a llevar una copia del modelo de 01_Generales/Clases_SGCC.mdj.
- Objetos, slots y enlaces se remapean por nombre (clase, atributo, asociación). Un slot sin atributo o un
  valor de enumeración que no exista en la API detiene el proceso: se corrige en AJUSTES, nunca se adivina.
- Las cajas conservan su posición; el compartimiento de slots y los enlaces se recalculan.
"""
import base64, copy, json, os, sys

RAIZ = sys.argv[1]
SOLO = sys.argv[2:]
RENOMBRAR = {"AcuerdoCredito": "CondicionPago", "CargoPedido": "Cargo", "ConsumoInsumo": "InsumoProduccion",
             "EvidenciaEntrega": "EvidenciaRecepcion", "OperacionPendiente": "Recepcion"}

# objeto: {"clase": nueva, "nombre": nuevo, "slots": [(atributo, valor)] (reemplaza todos), "quitar": [...], "poner": [(a, v)]}
UID = lambda n: f'"{n}"'
AJUSTES = {
    # valores alineados con DatosIniciales (rol: Descripcion = Nombre; permiso: modulo.accion) y con
    # ServicioUsuarios (auditoría CREAR, EDITAR_PERMISOS, ESTADO_<estado>)
    "CU02": {"objetos": {
        "auditoria1": {"quitar": ["entidadId"], "valores": {"operacion": '"EDITAR_PERMISOS"'}},
        "rolAlmacen": {"valores": {"nombre": '"ALMACEN"', "descripcion": '"ALMACEN"'}},
        "permInventario": {"valores": {"codigo": '"inventario.administrar"', "descripcion": '"inventario administrar"',
                                       "modulo": '"inventario"', "accion": '"administrar"'}}}},
    "CU13": {"desde": "CU02", "nombre": "Administrar cuentas de nivel superior",
        "objetos": {
            "ana": {"nombre": "rosa", "slots": [("id", UID("0b6f3c1e-5a2d-4e8b-9c71-2d4f8a6b1e30")), ("nombre", '"Rosa"'),
                    ("login", '"rosa"'), ("correo", '"rosa@example.invalid"'), ("estado", "ACTIVO")]},
            "rolAlmacen": {"nombre": "rolPropietario", "slots": [("nombre", '"PROPIETARIO"'), ("descripcion", '"PROPIETARIO"'), ("activo", "true")]},
            "permInventario": {"nombre": "permUsuarios", "slots": [("codigo", '"usuarios.administrar"'), ("descripcion", '"usuarios administrar"'),
                    ("modulo", '"usuarios"'), ("accion", '"administrar"')]},
            "auditoria1": {"slots": [("operacion", '"CREAR"'), ("entidad", '"Usuario"'), ("fecha", '"2026-11-19T08:30:00"')]}},
        "nuevos": [{"nombre": "superadmin", "clase": "Usuario", "junto_a": "auditoria1", "enlaces": ["auditoria1"],
                    "slots": [("login", '"superadmin"'), ("estado", "ACTIVO")]}],
        "enlaces": {("rosa", "auditoria1"): None},
        "textos": {"CU02 · Usuario administrado con permisos explícitos": "CU13 · Cuenta de Propietario creada por el Superadministrador",
                   "Datos ilustrativos; instantánea parcial. Administrar usuarios agrupa alta, consulta, edición y desactivación. La desactivación conserva auditoría.":
                   "Datos ilustrativos; instantánea parcial. Solo SUPERADMIN asigna PROPIETARIO (RolesSistema.Asignable); el registro de auditoría\n"
                   "queda a nombre de quien creó la cuenta. Ninguna cuenta modifica sus propios privilegios."}},
    "CU14": {"desde": "CU02", "nombre": "Delegar rol de Finanzas",
        "objetos": {
            "ana": {"nombre": "carla", "slots": [("id", UID("7d2a9e44-1c3b-4f6a-8e05-93b1c7d2f6a8")), ("nombre", '"Carla"'),
                    ("login", '"carla"'), ("correo", '"carla@example.invalid"'), ("estado", "ACTIVO")]},
            "rolAlmacen": {"nombre": "rolFinanzas", "slots": [("nombre", '"FINANZAS"'), ("descripcion", '"FINANZAS"'), ("activo", "true")]},
            "permInventario": {"nombre": "permSaldos", "slots": [("codigo", '"saldos.consultar"'), ("descripcion", '"saldos consultar"'),
                    ("modulo", '"saldos"'), ("accion", '"consultar"')]},
            "auditoria1": {"slots": [("operacion", '"EDITAR_PERMISOS"'), ("entidad", '"Usuario"'), ("fecha", '"2026-11-19T09:05:00"')]}},
        "nuevos": [{"nombre": "propietario", "clase": "Usuario", "junto_a": "auditoria1", "enlaces": ["auditoria1"],
                    "slots": [("login", '"dueno"'), ("estado", "ACTIVO")]},
                   {"nombre": "sesionCarla", "clase": "Sesion", "junto_a": "carla", "enlaces": ["carla"],
                    "slots": [("inicio", '"2026-11-19T08:00:00"'), ("expira", '"2026-11-19T16:00:00"'), ("revocada", "true")]}],
        "enlaces": {("carla", "auditoria1"): None},
        "textos": {"CU02 · Usuario administrado con permisos explícitos": "CU14 · Rol FINANZAS delegado por el Propietario",
                   "Datos ilustrativos; instantánea parcial. Administrar usuarios agrupa alta, consulta, edición y desactivación. La desactivación conserva auditoría.":
                   "Datos ilustrativos; instantánea parcial. Solo PROPIETARIO o SUPERADMIN asignan FINANZAS; al cambiar los roles se revocan las\n"
                   "sesiones abiertas de la cuenta (revocada = true) para que el token nuevo traiga los permisos financieros."}},
    "CU15": {"desde": "CU02", "nombre": "Consultar auditoría",
        "objetos": {
            "ana": {"nombre": "propietario", "slots": [("id", UID("c41e8b02-6f7a-4d39-a2c5-58e0b9f3d714")), ("nombre", '"Dueño"'),
                    ("login", '"dueno"'), ("correo", '"dueno@example.invalid"'), ("estado", "ACTIVO")]},
            "rolAlmacen": {"nombre": "rolPropietario", "slots": [("nombre", '"PROPIETARIO"'), ("descripcion", '"PROPIETARIO"'), ("activo", "true")]},
            "permInventario": {"nombre": "permAuditoria", "slots": [("codigo", '"auditoria.consultar"'), ("descripcion", '"auditoria consultar"'),
                    ("modulo", '"auditoria"'), ("accion", '"consultar"')]},
            "auditoria1": {"nombre": "registro1", "slots": [("operacion", '"EDITAR_PERMISOS"'), ("entidad", '"Usuario"'), ("fecha", '"2026-11-19T09:05:00"')]}},
        "nuevos": [{"nombre": "registro2", "clase": "RegistroAuditoria", "junto_a": "registro1", "enlaces": ["propietario"],
                    "slots": [("operacion", '"ESTADO_DESHABILITADO"'), ("entidad", '"Usuario"'), ("fecha", '"2026-11-19T10:40:00"')]}],
        "textos": {"CU02 · Usuario administrado con permisos explícitos": "CU15 · Historial de auditoría consultado por el Propietario",
                   "Datos ilustrativos; instantánea parcial. Administrar usuarios agrupa alta, consulta, edición y desactivación. La desactivación conserva auditoría.":
                   "Datos ilustrativos; instantánea parcial. GET api/v1/auditoria lista los registros por fecha descendente con el login de quien\n"
                   "actuó; la consulta no crea, edita ni borra registros."}},
    "CU06": {
        "objetos": {"incidencia42": {"clase": "Sena", "nombre": "sena42",
                                     "slots": [("acuerdoResolucion", '""'), ("resueltaEn", "null")]}},
        "textos": {"CU06 · Pedido confirmado y una incidencia pendiente de acuerdo": "CU06 · Pedido confirmado con una seña sin resolver",
                   "Datos ilustrativos; instantánea parcial. Instantánea parcial. Una incidencia con efecto en despacho cambia el pedido a PENDIENTE_ACUERDO; no crea otro pedido.":
                   "Datos ilustrativos; instantánea parcial. Mientras la Sena del pedido no tenga acuerdoResolucion (resueltaEn vacío), "
                   "cancelar el pedido se rechaza con SENA_SIN_ACUERDO: no hay devolución ni retención automáticas."}},
    "CU08": {
        "objetos": {
            "faeneo29": {"clase": "OrdenProduccion", "nombre": "orden29",
                         "slots": [("id", '"086ee1e8-0ab7-4c02-8457-a89bc3e95014"'), ("codigo", '"OP-029"'), ("tipo", "FAENEO"), ("estado", "CONFIRMADA")]},
            "fabricacion30": {"clase": "OrdenProduccion", "nombre": "orden30",
                              "slots": [("id", '"f9397798-d8cf-4c9c-872e-1762961d365e"'), ("codigo", '"OP-030"'), ("tipo", "FABRICACION"), ("estado", "CONFIRMADA")]},
            "*Lote": {"renombrar": {"estadoCalidad": "estado"}},
            "*ResultadoProduccion": {"quitar": ["referenciaUnica", "unidad"]},
            "*Pesaje": {"quitar": ["tipo", "origen"], "renombrar": {"peso": "neto"}},
        },
        "enlaces": {("resultadoCostilla", "pesajeCostilla"): ("loteCostilla", "pesajeCostilla"),
                    ("resultadoLomo", "pesajeLomo"): ("loteLomo", "pesajeLomo"),
                    ("almacenero", "resultadoCostilla"): None, ("almacenero", "resultadoJamon"): None,
                    ("almacenero", "resultadoLomo"): None}},
    "CU09": {
        "objetos": {
            "*Lote": {"renombrar": {"estadoCalidad": "estado"}},
            "*ResultadoProduccion": {"quitar": ["referenciaUnica", "unidad"]},
            "existencia1": {"slots": [("ubicacion", '"Cámara principal"'), ("cantidadFisica", "6")]},
            "entrada1": {"clase": "EntradaInventario", "slots": [("cantidad", "6"), ("anulada", "false")]},
            "reserva1": {"quitar": ["referenciaUnica"]},
        },
        "quitar_objetos": ["camara"],
        "textos": {"Datos ilustrativos; instantánea parcial. Físico apto 6 kg, reserva 4 kg, disponible 2 kg. Recibir y reservar son operaciones distintas; la referencia impide repetir la entrada.":
                   "Datos ilustrativos; instantánea parcial. Físico apto 6 kg en la Cámara principal (ubicacion de Existencia), reserva ACTIVA 4 kg, "
                   "disponible 2 kg. Recibir (EntradaInventario sobre el pesaje confirmado) y reservar son operaciones distintas."}},
    "CU10": {
        "objetos": {
            "cargo1": {"slots": [("tipo", "PRODUCTO"), ("concepto", '"4 kg de costilla"'), ("importe", "140")]},
            "pago1": {"slots": [("referenciaUnica", '"SENA-042"'), ("tipo", "SENA"), ("importe", "50"), ("anulado", "false")]},
            "credito1": {"slots": [("modalidad", "CREDITO_ACORDADO"), ("importeAutorizado", "90"), ("vencimiento", '"2026-11-05T18:00:00"'), ("activa", "true")]},
        },
        "nuevos": [{"nombre": "sena1", "clase": "Sena", "junto_a": "pago1", "slots": [("acuerdoResolucion", '""'), ("resueltaEn", "null")],
                    "enlaces": ["pago1", "pedido42"]}],
        "enlaces": {("pedido42", "pago1"): None}},
    "CU11": {
        "objetos": {
            "ruta1": {"valores": {"estado": "EN_REPARTO"}},
            "entrega1": {"slots": [("id", '"785fcea1-a4ba-4e27-866a-290df9c6b501"'), ("version", "4"), ("modalidad", "DOMICILIO"), ("estado", "ENTREGADA")]},
            "pendiente1": {"nombre": "recepcion1",
                           "slots": [("claveUnica", '"3f6c0d7e-2b41-4c1a-9a55-0f1e8b2d4c73"'), ("versionBase", "3"), ("estado", "CONFIRMADA"),
                                     ("pesoRecibido", "4"), ("unidad", '"kg"'), ("conforme", "true"), ("receptor", '"Encargado del local"')]},
        },
        "textos": {"CU11 · Reparto asignado y recepción local pendiente": "CU11 · Reparto y recepción sincronizada",
                   "Datos ilustrativos; instantánea parcial. Android guarda solo una recepción autorizada descargada. Sin confirmación central, Entrega sigue EN_TRASLADO y la deuda no cambia.":
                   "Datos ilustrativos; instantánea parcial. Android sincroniza la recepción con claveUnica y versionBase 3; como la entrega seguía "
                   "DESPACHADA en esa versión, la API la confirma y pasa la entrega a ENTREGADA (versión 4). Entregar no cambia la deuda."}},
}

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
def clonar(pl):
    c = copy.deepcopy(pl); mapa = {o["_id"]: nid() for o in todos(c) if "_id" in o}
    for o in todos(c):
        if "_id" in o: o["_id"] = mapa[o["_id"]]
        if set(o) == {"$ref"} and o["$ref"] in mapa: o["$ref"] = mapa[o["$ref"]]
    return c

CLASES = json.load(open(os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj"), encoding="utf-8"))["ownedElements"][0]

def procesar(ruta, cu):
    P = json.load(open(ruta, encoding="utf-8"))
    ids = {o["_id"]: o for o in todos(P) if "_id" in o}
    usados.update(ids)
    mod = P["ownedElements"][0]
    diag = next(o for o in mod["ownedElements"] if o["_type"] == "UMLObjectDiagram")
    objetos = [o for o in mod["ownedElements"] if o["_type"] == "UMLObject"]
    enlaces = [o for o in mod["ownedElements"] if o["_type"] == "UMLLink"]
    aj = AJUSTES.get(cu, {})

    # nuevo modelo de clases con ids propios
    nuevo = clonar([o for o in CLASES["ownedElements"] if o["_type"] != "UMLClassDiagram"])
    for o in nuevo: o["_parent"] = ref(mod["_id"])
    nids = {o["_id"]: o for o in todos(nuevo) if "_id" in o}
    NC = {o["name"]: o for o in nids.values() if o["_type"] == "UMLClass"}
    NE = {o["name"]: o for o in nids.values() if o["_type"] == "UMLEnumeration"}
    NA = []
    for o in nids.values():
        if o["_type"] == "UMLAssociation":
            NA.append((nids[o["end1"]["reference"]["$ref"]]["name"], nids[o["end2"]["reference"]["$ref"]]["name"], o))

    viejo_clase = {o["_id"]: ids[o["classifier"]["$ref"]]["name"] for o in objetos}
    # --- ajustes de objetos
    por_nombre = {o["name"]: o for o in objetos}
    quitar = set(aj.get("quitar_objetos", []))
    for o in objetos:
        cls = RENOMBRAR.get(viejo_clase[o["_id"]], viejo_clase[o["_id"]])
        reglas = [aj.get("objetos", {}).get("*" + cls, {}), aj.get("objetos", {}).get(o["name"], {})]
        for r in reglas:
            if "clase" in r: cls = r["clase"]
            if "nombre" in r: o["name"] = r["nombre"]
            slots = [(s.get("name") or ids[s["definingFeature"]["$ref"]]["name"], s.get("value")) for s in o.get("slots", [])]
            if "slots" in r: slots = list(r["slots"])
            slots = [(r.get("renombrar", {}).get(n, n), v) for n, v in slots if n not in r.get("quitar", [])]
            slots = [(n, r.get("valores", {}).get(n, v)) for n, v in slots]
            slots += r.get("poner", [])
            o["slots"] = [{"_type": "UMLSlot", "_id": nid(), "_parent": ref(o["_id"]), "name": n, "value": v} for n, v in slots]
        o["_clase"] = cls
    for n in aj.get("nuevos", []):
        o = {"_type": "UMLObject", "_id": nid(), "_parent": ref(mod["_id"]), "name": n["nombre"], "_clase": n["clase"],
             "_junto_a": n["junto_a"], "_enlaces": n["enlaces"]}
        o["slots"] = [{"_type": "UMLSlot", "_id": nid(), "_parent": ref(o["_id"]), "name": a, "value": v} for a, v in n["slots"]]
        objetos.append(o); mod["ownedElements"].append(o); por_nombre[o["name"]] = o
    por_nombre = {o["name"]: o for o in objetos}
    por_id = {o["_id"]: o for o in objetos}

    # --- slots: atributo real y valor de enumeración válido
    errores = []
    for o in objetos:
        if o["name"] in quitar: continue
        c = NC.get(o["_clase"])
        if not c: errores.append(f"{o['name']}: clase {o['_clase']} no existe"); continue
        o["classifier"] = ref(c["_id"])
        attrs = {a["name"]: a for a in c.get("attributes", [])}
        for s in o["slots"]:
            a = attrs.get(s["name"])
            if not a: errores.append(f"{o['name']}:{o['_clase']} slot {s['name']} sin atributo"); continue
            s["definingFeature"] = ref(a["_id"]); s["type"] = copy.deepcopy(a["type"])
            t = a["type"]
            if isinstance(t, dict):
                e = nids[t["$ref"]]
                if s["value"] not in [l["name"] for l in e.get("literals", [])]:
                    errores.append(f"{o['name']}.{s['name']} = {s['value']} no es literal de {e['name']}")
    # --- enlaces
    ren = aj.get("enlaces", {})
    for l in list(enlaces):
        a, b = por_id[l["end1"]["reference"]["$ref"]], por_id[l["end2"]["reference"]["$ref"]]
        k = next((k for k in ren if set(k) == {a["name"], b["name"]}), None)
        if a["name"] in quitar or b["name"] in quitar or (k is not None and ren[k] is None):
            enlaces.remove(l); mod["ownedElements"].remove(l); l["_quitado"] = True; continue
        if k is not None:
            na, nb = por_nombre[ren[k][0]], por_nombre[ren[k][1]]
            l["end1"]["reference"] = ref(na["_id"]); l["end2"]["reference"] = ref(nb["_id"]); l["_cambio"] = True
    for o in objetos:
        for otro in o.get("_enlaces", []):
            L = {"_type": "UMLLink", "_id": nid(), "_parent": ref(mod["_id"]),
                 "end1": {"_type": "UMLLinkEnd", "_id": nid(), "reference": ref(por_nombre[otro]["_id"])},
                 "end2": {"_type": "UMLLinkEnd", "_id": nid(), "reference": ref(o["_id"])}, "_cambio": True, "_nuevo": True}
            L["end1"]["_parent"] = ref(L["_id"]); L["end2"]["_parent"] = ref(L["_id"])
            enlaces.append(L); mod["ownedElements"].append(L)
    for l in enlaces:
        a, b = por_id[l["end1"]["reference"]["$ref"]], por_id[l["end2"]["reference"]["$ref"]]
        nombre_viejo = ids[l["association"]["$ref"]].get("name") if l.get("association") and l["association"]["$ref"] in ids else None
        cands = [x for x in NA if {x[0], x[1]} == {a["_clase"], b["_clase"]}]
        if len(cands) > 1 and nombre_viejo:
            cands = [x for x in cands if x[2].get("name") == nombre_viejo] or cands
        if not cands: errores.append(f"enlace {a['name']}:{a['_clase']} - {b['name']}:{b['_clase']} sin asociación"); continue
        l["association"] = ref(cands[0][2]["_id"])
    if errores:
        raise SystemExit(f"{cu}:\n  " + "\n  ".join(errores))

    # --- reemplazar el modelo embebido
    mod["ownedElements"] = [o for o in mod["ownedElements"] if o["_type"] in ("UMLObjectDiagram", "UMLObject", "UMLLink") and o.get("name") not in quitar]
    mod["ownedElements"][1:1] = nuevo

    # --- vistas
    vistas = diag["ownedViews"]
    vobj = {v["model"]["$ref"]: v for v in vistas if v["_type"] == "UMLObjectView"}
    T_OBJ = copy.deepcopy(next(iter(vobj.values())))
    T_SLOT = copy.deepcopy(next(s for v in vobj.values() for c in v["subViews"] if c["_type"] == "UMLSlotCompartmentView" for s in c["subViews"]))
    T_LINK = copy.deepcopy(next(v for v in vistas if v["_type"] == "UMLLinkView"))
    for n in quitar:
        o = next(x for x in objetos if x["name"] == n)
        vistas.remove(vobj.pop(o["_id"]))
    def tipo_txt(s):
        t = s["type"]
        return nids[t["$ref"]]["name"] if isinstance(t, dict) else t
    for o in objetos:
        if o["name"] in quitar: continue
        v = vobj.get(o["_id"])
        if v is None:
            base = vobj[por_nombre[o["_junto_a"]]["_id"]]
            v = clonar(T_OBJ); v["_parent"] = ref(diag["_id"]); v["model"] = ref(o["_id"])
            v["left"] = base["left"]; v["top"] = base["top"] + base["height"] + 70; v["width"] = base["width"]
            for s in todos(v):
                if "model" in s: s["model"] = ref(o["_id"])
            vistas.append(v); vobj[o["_id"]] = v
        x, y, w = v["left"], v["top"], v["width"]
        nc = next(c for c in v["subViews"] if c["_type"] == "UMLNameCompartmentView")
        lab = next(c for c in nc["subViews"] if c.get("underline") or (c.get("text") and ":" in c.get("text", "")))
        lab["text"] = f"{o['name']}: {o['_clase']}"
        nc.update(left=x, top=y, width=w + 1)
        lab.update(left=x + 5, top=y + 7, width=w - 9)
        sc = next(c for c in v["subViews"] if c["_type"] == "UMLSlotCompartmentView")
        sc["subViews"] = []
        for i, s in enumerate(o["slots"]):
            sv = clonar(T_SLOT); sv.update(_parent=ref(sc["_id"]), model=ref(s["_id"]), left=x + 5, top=y + 34 + 19 * i, width=w - 9,
                                          text=f"{s['name']}: {tipo_txt(s)} = {s['value']}")
            sc["subViews"].append(sv)
        sc.update(left=x, top=y + 29, width=w + 1, height=10 + 19 * len(o["slots"]))
        v["height"] = 29 + 10 + 19 * len(o["slots"]) + 12
    # enlaces: quitar vistas de enlaces quitados, recalcular todos los puntos
    vivos = {l["_id"]: l for l in enlaces}
    for v in [v for v in vistas if v["_type"] == "UMLLinkView"]:
        if v["model"]["$ref"] not in vivos: vistas.remove(v)
    vlink = {v["model"]["$ref"]: v for v in vistas if v["_type"] == "UMLLinkView"}
    def borde(vv, hacia):
        cx, cy = vv["left"] + vv["width"] / 2, vv["top"] + vv["height"] / 2
        dx, dy = hacia[0] - cx, hacia[1] - cy
        if dx == 0 and dy == 0: return cx, cy
        sx = (vv["width"] / 2) / abs(dx) if dx else 1e9
        sy = (vv["height"] / 2) / abs(dy) if dy else 1e9
        s = min(sx, sy)
        return cx + dx * s, cy + dy * s
    cajas = {oid: (vv["left"], vv["top"], vv["width"], vv["height"]) for oid, vv in vobj.items()}
    segs = []
    def cruza(pts, excl):
        n = 0
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            for k, (x, y, w, h) in cajas.items():
                if k in excl: continue
                if max(x1, x2) > x - 6 and min(x1, x2) < x + w + 6 and max(y1, y2) > y - 6 and min(y1, y2) < y + h + 6: n += 10
            for (a1, b1, c1, d1) in segs:
                if x1 == x2 == a1 == c1 and min(max(y1, y2), max(b1, d1)) - max(min(y1, y2), min(b1, d1)) > 2: n += 5
                if y1 == y2 == b1 == d1 and min(max(x1, x2), max(a1, c1)) - max(min(x1, x2), min(a1, c1)) > 2: n += 5
        return n
    def candidatos(A, B):
        xa, ya, wa, ha = A; xb, yb, wb, hb = B
        offs = [0, 18, -18, 36, -36, 54, -54, 72, -72]
        lo, hi = max(xa, xb) + 15, min(xa + wa, xb + wb) - 15
        if hi > lo:                                   # columnas que se solapan: vertical recta
            for d in offs:
                x = (lo + hi) / 2 + d
                if lo <= x <= hi:
                    yield [(x, ya + ha), (x, yb)] if yb > ya else [(x, ya), (x, yb + hb)]
        lo, hi = max(ya, yb) + 12, min(ya + ha, yb + hb) - 12
        if hi > lo:                                   # filas que se solapan: horizontal recta
            for d in offs:
                y = (lo + hi) / 2 + d
                if lo <= y <= hi:
                    yield [(xa + wa, y), (xb, y)] if xb > xa else [(xa, y), (xb + wb, y)]
        cxa, cya, cxb, cyb = xa + wa / 2, ya + ha / 2, xb + wb / 2, yb + hb / 2
        sy = ya + ha if cyb > cya else ya; ty = yb if cyb > cya else yb + hb
        sx = xa + wa if cxb > cxa else xa; tx = xb if cxb > cxa else xb + wb
        for d in offs:
            for e in offs[:5]:
                # Z por el pasillo horizontal entre filas
                if (cyb > cya and yb > ya + ha) or (cyb < cya and yb + hb < ya):
                    ym = (sy + ty) / 2 + e
                    yield [(cxa + d, sy), (cxa + d, ym), (cxb + d, ym), (cxb + d, ty)]
                # Z por el pasillo vertical entre columnas
                if (cxb > cxa and xb > xa + wa) or (cxb < cxa and xb + wb < xa):
                    xm = (sx + tx) / 2 + e
                    yield [(sx, cya + d), (xm, cya + d), (xm, cyb + d), (tx, cyb + d)]
                # L: horizontal y luego vertical, y al revés
                yield [(sx, cya + e), (cxb + d, cya + e), (cxb + d, ty)]
                yield [(cxa + d, sy), (cxa + d, cyb + e), (tx, cyb + e)]
    def pasillos(ejes):
        # centros de los huecos libres entre cajas sobre un eje
        tramos = sorted((c[ejes[0]], c[ejes[0]] + c[ejes[1]]) for c in cajas.values())
        res, fin = [], None
        for a0, a1 in tramos:
            if fin is not None and a0 > fin + 40: res.append((fin + a0) / 2)
            fin = a1 if fin is None else max(fin, a1)
        return res
    PX, PY = pasillos((0, 2)), pasillos((1, 3))
    PY += [min(c[1] for c in cajas.values()) - 45, max(c[1] + c[3] for c in cajas.values()) + 45]
    PX += [min(c[0] for c in cajas.values()) - 45, max(c[0] + c[2] for c in cajas.values()) + 45]
    def rodeos(A, B):
        xa, ya, wa, ha = A; xb, yb, wb, hb = B
        cya, cxb = ya + ha / 2, xb + wb / 2
        for xg in sorted(PX, key=lambda x: abs(x - (xa + wa / 2))):
            sx = xa + wa if xg > xa else xa
            for yg in sorted(PY, key=lambda y: abs(y - (yb + hb / 2))):
                ty = yb if yg < yb else yb + hb
                for d in (0, 14, -14, 28, -28):
                    for e in (0, 12, -12, 24, -24):
                        yield [(sx, cya + d), (xg + e, cya + d), (xg + e, yg + e), (cxb + d, yg + e), (cxb + d, ty)]
    for l in enlaces:
        v = vlink.get(l["_id"])
        if v is None:
            v = clonar(T_LINK); v["_parent"] = ref(diag["_id"]); vistas.append(v)
        v["model"] = ref(l["_id"])
        for s in v.get("subViews", []):
            s["model"] = ref(l["_id"]); s["hostEdge"] = ref(v["_id"])
        ia, ib = l["end1"]["reference"]["$ref"], l["end2"]["reference"]["$ref"]
        va, vb = vobj[ia], vobj[ib]
        v["tail"] = ref(va["_id"]); v["head"] = ref(vb["_id"])
        mejor, pm = None, 1e9
        for c in candidatos(cajas[ia], cajas[ib]):
            c = [(round(x), round(y)) for x, y in c]
            n = cruza(c, {ia, ib}) + len(c)
            if n < pm: mejor, pm = c, n
            if n <= 4: break
        if pm >= 5:
            for c in rodeos(cajas[ia], cajas[ib]):
                c = [(round(x), round(y)) for x, y in c]
                n = cruza(c, {ia, ib}) + len(c)
                if n < pm: mejor, pm = c, n
                if n <= 5: break
        if pm >= 10: print(f"  aviso {cu}: enlace {por_id[ia]['name']}-{por_id[ib]['name']} cruza (costo {pm})")
        pts = mejor
        for p_, q_ in zip(pts, pts[1:]): segs.append((p_[0], p_[1], q_[0], q_[1]))
        v["points"] = ";".join(f"{x}:{y}" for x, y in pts)
        v["lineStyle"] = 0
        p, q = max(zip(pts, pts[1:]), key=lambda t: abs(t[1][0] - t[0][0]) + abs(t[1][1] - t[0][1]))
        nombre = next(o for o in todos(nuevo) if o.get("_id") == l["association"]["$ref"]).get("name", "")
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        for s in v.get("subViews", []):
            if s.get("_type") == "EdgeLabelView":
                if s["_id"] == v.get("nameLabel", {}).get("$ref") and nombre:
                    s.update(text=nombre, left=round(mx + 6), top=round(my - 16), width=len(nombre) * 8 + 6, height=14, visible=True)
                else:
                    s["visible"] = False; s.pop("text", None)
    # textos
    for v in vistas:
        if v["_type"] == "UMLTextView" and v.get("text") in aj.get("textos", {}):
            v["text"] = aj["textos"][v["text"]]
    # limpiar marcas internas
    for o in todos(P):
        for k in [k for k in o if k.startswith("_") and k not in ("_type", "_id", "_parent")]:
            o.pop(k)
    ids2 = {o["_id"] for o in todos(P) if "_id" in o}
    malas = [o["$ref"] for o in todos(P) if isinstance(o, dict) and set(o) == {"$ref"} and o["$ref"] not in ids2]
    assert not malas, (cu, malas[:5])
    assert len(ids2) == len([o for o in todos(P) if "_id" in o]), (cu, "ids repetidos")
    json.dump(P, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
    return len(objetos) - len(quitar), len(enlaces)

carpeta = os.path.join(RAIZ, "03_Objetos")
for cu, aj in AJUSTES.items():
    if "desde" not in aj or (SOLO and cu not in SOLO): continue
    origen = json.load(open(os.path.join(carpeta, f"{aj['desde']}_Objetos.mdj"), encoding="utf-8"))
    usados.update(o["_id"] for o in todos(origen) if "_id" in o)
    P = clonar(origen)
    viejo = next(o for o in P["ownedElements"][0]["ownedElements"] if o["_type"] == "UMLObjectDiagram")["name"].split(" — ")[1]
    for o in todos(P):
        for k in ("name", "text"):
            if isinstance(o.get(k), str):
                o[k] = o[k].replace(f"{aj['desde']} — {viejo}", f"{cu} — {aj['nombre']}").replace(f"{aj['desde']} — ", f"{cu} — ")
    json.dump(P, open(os.path.join(carpeta, f"{cu}_Objetos.mdj"), "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
for f in sorted(os.listdir(carpeta)):
    if not f.startswith("CU") or not f.endswith("_Objetos.mdj"): continue
    cu = f[:4]
    if SOLO and cu not in SOLO: continue
    print(cu, *procesar(os.path.join(carpeta, f), cu))
