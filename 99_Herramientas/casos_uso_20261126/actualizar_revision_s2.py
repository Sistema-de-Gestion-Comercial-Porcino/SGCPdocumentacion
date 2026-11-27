"""Sprint 5 · Casos de uso tras la revisión a mano del Sprint 2 (SGCPapi v5.1.5, SGCPuiweb v5.1.6).

- Administrador consulta pedidos para preparar sus entregas (pedidos.consultar): asociación con CU06.
- CU08 documenta el rechazo sanitario definitivo, el paso de apto a rechazado con motivo y el consumo irreversible.
- CU09 documenta el control de frío de una cámara completa con la hora de inicio de la falla y el ingreso de cada lote.
- CU11 documenta quién responde cada modalidad de entrega (Ventas en el local, repartidor a domicilio).

Edición quirúrgica del JSON: no cambia la posición ni la ruta de ningún elemento existente
(la disposición manual del diagrama se conserva). Solo agrega una línea nueva. Idempotente.
Uso: python3 actualizar_revision_s2.py <Casos_de_Uso_SGCC.mdj>
"""
import base64, copy, json, os, sys

RUTA = sys.argv[1]
# Texto que se agrega al final de la documentación de cada caso, si todavía no está.
AGREGADOS = {
    "CU06": " Administrador consulta los pedidos confirmados para preparar sus entregas.",
    "CU08": (" Un rechazo sanitario es definitivo: el animal no admite otro control y conserva una sola incidencia; rechazar un"
             " animal apto exige el motivo («Pasó de apto a rechazado»). El consumo de una fabricación es irreversible: la orden"
             " que ya consumió no se anula."),
    "CU09": (" El control de frío se registra sobre un lote, una entrega o una cámara completa; rechazar una cámara exige la hora"
             " de inicio de la falla y deja en revisión solo los lotes y derivados expuestos desde esa hora. Existencias muestra el"
             " origen de cada lote y quién lo ingresó a qué cámara y cuándo."),
    "CU11": (" A domicilio responde un repartidor (Responsable de entrega); en retiro en el local, Ventas o un repartidor que esté"
             " en el local. Ventas prepara, despacha y registra la recepción solo de sus retiros en el local."),
}
DOC_ACTORES = {"CU06": ("Propietario, Ventas, Comprador, Finanzas", "Propietario, Administrador, Ventas, Comprador, Finanzas")}
# actor, caso, ruta ortogonal. Sale del Administrador entre sus líneas a CU03 (y 1632) y CU08 (y 1664), baja en x 790
# (libre: la línea de CU03 termina en y 1632 y la de CU08 empieza en y 1664) y entra a CU06 entre Propietario (1649) y Finanzas (1675).
NUEVAS = [("Administrador", "CU06", "461:1646;790:1646;790:1662;1149:1662")]


def nuevo_id():
    return base64.b64encode(os.urandom(11)).decode()


d = json.load(open(RUTA, encoding="utf-8"))
idx = {}
def indexar(o):
    if isinstance(o, dict):
        if "_id" in o: idx[o["_id"]] = o
        for v in o.values(): indexar(v)
    elif isinstance(o, list):
        for v in o: indexar(v)
indexar(d)
vistas = {}
for o in idx.values():
    if o.get("_type") in ("UMLActorView", "UMLUseCaseView"):
        vistas[idx[o["model"]["$ref"]]["name"].split(" · ")[0].split(" (")[0]] = o
casos = {o["name"][:4]: o for o in idx.values() if o.get("_type") == "UMLUseCase"}
actores = {o["name"]: o for o in idx.values() if o.get("_type") == "UMLActor"}

for cu, (viejo, nuevo) in DOC_ACTORES.items():
    doc = casos[cu].get("documentation", "")
    if nuevo not in doc: casos[cu]["documentation"] = doc.replace(viejo, nuevo, 1)
for cu, texto in AGREGADOS.items():
    doc = casos[cu].get("documentation", "")
    if texto.strip() not in doc: casos[cu]["documentation"] = doc.rstrip() + texto

def asociados(actor, caso):
    for o in idx.values():
        if o.get("_type") == "UMLAssociation":
            if {o["end1"]["reference"]["$ref"], o["end2"]["reference"]["$ref"]} == {actor["_id"], caso["_id"]}: return True
    return False

# Plantilla: una asociación ya existente del mismo actor (Administrador → CU08), con su mismo estilo.
plantilla_m = next(o for o in idx.values() if o.get("_type") == "UMLAssociation"
                   and o["end1"]["reference"]["$ref"] == actores["Administrador"]["_id"]
                   and o["end2"]["reference"]["$ref"] == casos["CU08"]["_id"])
plantilla_v = next(o for o in idx.values() if o.get("_type") == "UMLAssociationView" and o["model"]["$ref"] == plantilla_m["_id"])
padre_m = idx[plantilla_m["_parent"]["$ref"]]
diagrama = idx[plantilla_v["_parent"]["$ref"]]
cola_es_actor = plantilla_v["tail"]["$ref"] == vistas["Administrador"]["_id"]

def clonar(obj):
    c = copy.deepcopy(obj); mapa = {}
    def ids(o):
        if isinstance(o, dict):
            if "_id" in o: mapa[o["_id"]] = nuevo_id()
            for v in o.values(): ids(v)
        elif isinstance(o, list):
            for v in o: ids(v)
    ids(c)
    s = json.dumps(c, ensure_ascii=False)
    for a, b in mapa.items(): s = s.replace(f'"{a}"', f'"{b}"')
    return json.loads(s)

agregadas = 0
for actor_n, cu, puntos in NUEVAS:
    actor, caso = actores[actor_n], casos[cu]
    if asociados(actor, caso): continue
    m, v = clonar([plantilla_m, plantilla_v])  # juntos: las subvistas apuntan al modelo y sus extremos
    m["end1"]["reference"]["$ref"] = actor["_id"]; m["end2"]["reference"]["$ref"] = caso["_id"]
    v["tail" if cola_es_actor else "head"]["$ref"] = vistas[actor_n]["_id"]
    v["head" if cola_es_actor else "tail"]["$ref"] = vistas[cu]["_id"]
    v["points"] = puntos
    padre_m["ownedElements"].append(m)
    diagrama["ownedViews"].append(v)
    agregadas += 1

open(RUTA, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent="\t"))
print(f"{RUTA}: {agregadas} asociaciones nuevas; documentación actualizada")
