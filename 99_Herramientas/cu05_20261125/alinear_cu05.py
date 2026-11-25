"""D-4 · Alinea CU05 con los endpoints de solicitud del comprador (SGCPapi v4.x).

- Secuencia, colaboración y actividad: POST cotizaciones/solicitudes y PUT cotizaciones/{id}/solicitud.
- Objetos CU05: objeto Permiso «cotizaciones.solicitar» y nota sobre vigenteHasta.
- Todos los .mdj que embeben el modelo: Cotizacion.vigenteHasta pasa a multiplicidad 0..1.
Edición quirúrgica del JSON; no usa StarUML ni JS. Idempotente.
Uso: python3 alinear_cu05.py <carpeta 02_Ingenieria_de_Software>
"""
import copy, glob, json, os, random, string, sys

RAIZ = sys.argv[1]
SEQ_POST = "POST cotizaciones/solicitudes (clienteId,detalles)"
SEQ_PUT = "PUT cotizaciones/{id}/solicitud (detalles)"
ACT_POST = "POST cotizaciones/solicitudes\nDatos: cliente Id, detalles"
ACT_PUT = "Corregir solicitud (opcional)\nPUT cotizaciones/{id}/solicitud"
# Nombre anterior → nombre final. Las dos últimas filas de cada grupo migran una primera versión de este script.
RENOMBRES = {
    "guardarBorradorConCantidadesYUnidad(clienteId,detalles)": SEQ_POST,
    "enviarSolicitudAVentas()": SEQ_PUT,
    "Guardar Borrador Con Cantidades YUnidad\nDatos: cliente Id, detalles": ACT_POST,
    "Enviar Solicitud AVentas": ACT_PUT,
    "guardarYEnviarSolicitud(clienteId,detalles): POST cotizaciones/solicitudes": SEQ_POST,
    "corregirSolicitudPendiente(id,detalles): PUT cotizaciones/{id}/solicitud": SEQ_PUT,
    "Guardar y enviar solicitud a Ventas\nPOST cotizaciones/solicitudes\nDatos: cliente Id, detalles": ACT_POST,
    "Corregir solicitud no revisada\nPUT cotizaciones/{id}/solicitud": ACT_PUT,
    "PUT cotizaciones/{id}/solicitud\nOpcional: corregir antes de la revisión": ACT_PUT,
}
NOTA = (" vigenteHasta es opcional mientras la cotización está en BORRADOR (solicitud del comprador) y se fija al presentarla."
        " El comprador solicita y corrige con el permiso cotizaciones.solicitar.")

def nuevo_id():
    return "".join(random.choice(string.ascii_letters + string.digits + "+/") for _ in range(16))

def recorrer(o, f):
    if isinstance(o, dict):
        f(o)
        for v in list(o.values()): recorrer(v, f)
    elif isinstance(o, list):
        for v in o: recorrer(v, f)

def guardar(ruta, d):
    # Respeta la sangría del archivo: los individuales usan tabulador; los consolidados, dos espacios.
    original = open(ruta, encoding="utf-8").read()
    sangria = "\t" if original[2:3] == "\t" else "  "
    texto = json.dumps(d, ensure_ascii=False, indent=sangria)
    with open(ruta, "w", encoding="utf-8") as h:
        h.write(texto + ("\n" if original.endswith("\n") else ""))

def renombrar(ruta):
    d = json.load(open(ruta, encoding="utf-8")); n = [0]
    def f(o):
        for k in ("name", "text"):
            for viejo, nuevo in RENOMBRES.items():
                # Las etiquetas de colaboración llevan prefijo de numeración: «1.2.1.2 [operación 1] : …».
                if isinstance(o.get(k), str) and viejo in o[k]:
                    o[k] = o[k].replace(viejo, nuevo); n[0] += 1
    recorrer(d, f)
    # En secuencia, la etiqueta del mensaje conserva el ancho medido del nombre anterior y se parte en
    # varias líneas que cruzan la flecha: se ensancha a la medida del texto nuevo, manteniendo el centro.
    idx = {}
    recorrer(d, lambda o: idx.__setitem__(o["_id"], o) if "_id" in o else None)
    for v in idx.values():
        if v.get("_type") == "UMLSeqMessageView" and isinstance(v.get("nameLabel"), dict):
            l = idx[v["nameLabel"]["$ref"]]
            if l.get("text") in (SEQ_POST, SEQ_PUT):
                ancho = round(len(l["text"]) * 6.81, 3)
                if (l.get("width") or 0) < ancho:
                    centro = l["left"] + l["width"] / 2
                    l["width"], l["left"] = ancho, round(centro - ancho / 2); n[0] += 1
    guardar(ruta, d); return n[0]

def multiplicidad(ruta):
    d = json.load(open(ruta, encoding="utf-8")); n = [0]
    cotizaciones = set()
    recorrer(d, lambda o: cotizaciones.add(o["_id"]) if o.get("_type") == "UMLClass" and o.get("name") == "Cotizacion" else None)
    def f(o):
        if o.get("_type") == "UMLAttribute" and o.get("name") == "vigenteHasta" and o.get("_parent", {}).get("$ref") in cotizaciones and o.get("multiplicity") != "0..1":
            o["multiplicity"] = "0..1"; n[0] += 1
    recorrer(d, f)
    # La vista guarda el texto del atributo ya compuesto: se actualiza igual que lo haría StarUML.
    atributos = set()
    recorrer(d, lambda o: atributos.add(o["_id"]) if o.get("_type") == "UMLAttribute" and o.get("name") == "vigenteHasta" and o.get("_parent", {}).get("$ref") in cotizaciones else None)
    def vista(o):
        if isinstance(o.get("model"), dict) and o["model"].get("$ref") in atributos and isinstance(o.get("text"), str) and o["text"].endswith("vigenteHasta: DateTime"):
            o["text"] += "[0..1]"; n[0] += 1
    recorrer(d, vista)
    if n[0]: guardar(ruta, d)
    return n[0]

def objetos(ruta):
    d = json.load(open(ruta, encoding="utf-8")); idx = {}
    recorrer(d, lambda o: idx.__setitem__(o["_id"], o) if "_id" in o else None)
    if any(o.get("_type") == "UMLObject" and o.get("name") == "permisoSolicitar" for o in idx.values()):
        return "ya aplicado"
    def en_cu05(o): return idx[o["_parent"]["$ref"]].get("name") == "CU05 — Objetos"
    base = next(o for o in idx.values() if o.get("_type") == "UMLObject" and o.get("name") == "tipoJamon" and en_cu05(o))
    vista = next(o for o in idx.values() if o.get("_type") == "UMLObjectView" and o["model"]["$ref"] == base["_id"])
    vjam = next(o for o in idx.values() if o.get("_type") == "UMLObjectView" and idx[o["model"]["$ref"]]["name"] == "productoJamon" and en_cu05(idx[o["model"]["$ref"]]))
    paquete = idx[base["classifier"]["$ref"]]["_parent"]["$ref"]
    permiso = next(o for o in idx.values() if o.get("_type") == "UMLClass" and o.get("name") == "Permiso" and o["_parent"]["$ref"] == paquete)
    attr = {a["name"]: a["_id"] for a in permiso["attributes"]}
    valores = [("codigo", '"cotizaciones.solicitar"'), ("modulo", '"cotizaciones"'), ("accion", '"solicitar"'),
               ("descripcion", '"Comprador envía o corrige su solicitud"')]
    obj = {"_type": "UMLObject", "_id": nuevo_id(), "_parent": base["_parent"], "name": "permisoSolicitar",
           "classifier": {"$ref": permiso["_id"]}, "slots": []}
    for nombre, valor in valores:
        obj["slots"].append({"_type": "UMLSlot", "_id": nuevo_id(), "_parent": {"$ref": obj["_id"]}, "name": nombre,
                             "value": valor, "definingFeature": {"$ref": attr[nombre]}, "type": "String"})
    idx[base["_parent"]["$ref"]]["ownedElements"].append(obj)
    v = copy.deepcopy(vista); dx = vjam["left"] - vista["left"]
    ids = {}
    def reid(o):
        if "_id" in o: ids[o["_id"]] = nuevo_id(); o["_id"] = ids[o["_id"]]
    recorrer(v, reid)
    def ajustar(o):
        for k in ("_parent", "stereotypeLabel", "nameLabel", "namespaceLabel", "propertyLabel"):
            if isinstance(o.get(k), dict) and o[k].get("$ref") in ids: o[k]["$ref"] = ids[o[k]["$ref"]]
        if isinstance(o.get("model"), dict) and o["model"]["$ref"] == base["_id"]: o["model"]["$ref"] = obj["_id"]
        if isinstance(o.get("left"), (int, float)): o["left"] += dx
    recorrer(v, ajustar)
    v["_parent"] = vista["_parent"]
    nombre = next(o for o in v["subViews"] if o["_type"] == "UMLNameCompartmentView")
    next(l for l in nombre["subViews"] if l.get("text", "").startswith("tipoJamon"))["text"] = "permisoSolicitar: Permiso"
    slots = next(o for o in v["subViews"] if o["_type"] == "UMLSlotCompartmentView")
    for sv, s in zip(slots["subViews"], obj["slots"]):
        sv["model"]["$ref"] = s["_id"]; sv["text"] = f'{s["name"]}: String = {s["value"]}'
    idx[vista["_parent"]["$ref"]]["ownedViews"].append(v)
    nota = next(o for o in idx[vista["_parent"]["$ref"]]["ownedViews"] if o.get("_type") == "UMLTextView" and o.get("text", "").startswith("Datos ilustrativos"))
    if NOTA.strip() not in nota["text"]: nota["text"] += NOTA
    guardar(ruta, d); return "objeto y nota agregados"

for f in ("06_Secuencias/CU05_Secuencia.mdj", "02_Colaboracion/CU05_Colaboracion.mdj", "05_Actividades/CU05_Actividad.mdj",
          "06_Secuencias/Secuencias_SGCC_Completo.mdj", "02_Colaboracion/Colaboracion_SGCC_Completo.mdj", "05_Actividades/Actividades_SGCC_Completo.mdj",
          "Entrega/Secuencias_SGCC_Completo.mdj", "Entrega/Colaboracion_SGCC_Completo.mdj", "Entrega/Actividades_SGCC_Completo.mdj"):
    print(f, "renombrados:", renombrar(os.path.join(RAIZ, f)))
for f in ("03_Objetos/CU05_Objetos.mdj", "03_Objetos/Objetos_SGCC_Completo.mdj", "Entrega/Objetos_SGCC_Completo.mdj"):
    print(f, objetos(os.path.join(RAIZ, f)))
total = 0
for f in sorted(glob.glob(os.path.join(RAIZ, "**/*.mdj"), recursive=True)):
    if "Respaldo" in f or "PDFentrega" in f or "Patrones de dise" in f: continue  # otras entregas no se tocan
    total += multiplicidad(f)
print("vigenteHasta 0..1 en", total, "modelos")
