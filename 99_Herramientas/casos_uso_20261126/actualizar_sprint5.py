"""Sprint 5 · Casos de uso alineados con las pantallas y permisos nuevos (S-1, D-1, V-1, V-2).

- CU08 suma la sección «Incidencias»; CU09 suma «Pedidos por preparar»; CU10 suma «Seguimiento».
- FINANZAS consulta clientes, catálogo, pedidos y reportes (V-1): asociaciones con CU03, CU06, CU07 y CU12.
- ENTREGA registra el control de frío de sus entregas (S-1): asociación con CU09.

Edición quirúrgica del JSON: no cambia la posición ni la ruta de ningún elemento existente
(la disposición manual del diagrama se conserva). Solo agrega cinco líneas nuevas. Idempotente.
Uso: python3 actualizar_sprint5.py <Casos_de_Uso_SGCC.mdj>
"""
import base64, copy, json, os, sys

RUTA = sys.argv[1]
RENOMBRES = {
    "CU08 · Gestionar producción (Sanidad · Producción)":
        "CU08 · Gestionar producción (Sanidad · Producción · Incidencias)",
    "CU09 · Gestionar inventario (Existencias · Pesajes y entradas · Control de frío)":
        "CU09 · Gestionar inventario (Existencias · Pesajes y entradas · Pedidos por preparar · Control de frío)",
    "CU10 · Gestionar pagos y cobranza (Saldos y pagos)":
        "CU10 · Gestionar pagos y cobranza (Saldos y pagos · Seguimiento)",
}
DOCS = {  # prefijo «Actores directos … Secciones: …» de la documentación de cada caso
    "CU03": ("Administrador, Ventas", "Administrador, Ventas, Finanzas", None, None),
    "CU06": ("Propietario, Ventas, Comprador", "Propietario, Ventas, Comprador, Finanzas", None, None),
    "CU07": ("Almacén, Responsable de entrega.", "Almacén, Responsable de entrega, Finanzas.", None, None),
    "CU12": ("Almacén, Responsable de entrega.", "Almacén, Responsable de entrega, Finanzas.", None, None),
    "CU08": (None, None, "Sanidad · Producción.", "Sanidad · Producción · Incidencias."),
    "CU09": ("Producción, Almacén.", "Producción, Almacén, Responsable de entrega.",
             "Pesajes y entradas · Control de frío.", "Pesajes y entradas · Pedidos por preparar · Control de frío."),
    "CU10": (None, None, "Secciones: Saldos y pagos.", "Secciones: Saldos y pagos · Seguimiento."),
}
# actor, caso, ruta ortogonal. Carriles libres: x 800/820/840 a la izquierda, x 2120 a la derecha.
NUEVAS = [
    ("Finanzas", "CU03", "461:2452;800:2452;800:1015;1149:1015"),
    ("Finanzas", "CU07", "461:2464;820:2464;820:1185;1149:1185"),
    ("Finanzas", "CU06", "461:2476;840:2476;840:1675;1149:1675"),
    ("Finanzas", "CU12", "461:2492;1149:2492"),
    ("Responsable de entrega", "CU09", "2519:2650;2120:2650;2120:1992;1851:1992"),
]

def nuevo_id():
    return base64.b64encode(os.urandom(11)).decode()

texto = open(RUTA, encoding="utf-8").read()
for viejo, nuevo in RENOMBRES.items():
    texto = texto.replace(json.dumps(viejo, ensure_ascii=False), json.dumps(nuevo, ensure_ascii=False))
d = json.loads(texto)
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

for cu, (a0, a1, s0, s1) in DOCS.items():
    doc = casos[cu]["documentation"]
    cab, _, resto = doc.partition(" Secciones: ")
    if a0 and a1 not in cab: cab = cab.replace(a0, a1, 1)
    doc = cab + " Secciones: " + resto
    if s0 and s1 not in doc: doc = doc.replace(s0, s1, 1)
    casos[cu]["documentation"] = doc

def asociados(actor, caso):
    for o in idx.values():
        if o.get("_type") == "UMLAssociation":
            ends = {o["end1"]["reference"]["$ref"], o["end2"]["reference"]["$ref"]}
            if ends == {actor["_id"], caso["_id"]}: return True
    return False

# Plantilla: una asociación actor→caso ya existente (Finanzas → CU10)
plantilla_m = next(o for o in idx.values() if o.get("_type") == "UMLAssociation"
                   and o["end1"]["reference"]["$ref"] == actores["Finanzas"]["_id"]
                   and o["end2"]["reference"]["$ref"] == casos["CU10"]["_id"])
plantilla_v = next(o for o in idx.values() if o.get("_type") == "UMLAssociationView"
                   and o["model"]["$ref"] == plantilla_m["_id"])
padre_m = idx[plantilla_m["_parent"]["$ref"]]
diagrama = idx[plantilla_v["_parent"]["$ref"]]
vista_actor = vistas["Finanzas"]
cola_es_actor = plantilla_v["tail"]["$ref"] == vista_actor["_id"]

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
    va, vc = vistas[actor_n], vistas[cu]
    v["tail" if cola_es_actor else "head"]["$ref"] = va["_id"]
    v["head" if cola_es_actor else "tail"]["$ref"] = vc["_id"]
    v["points"] = puntos
    padre_m["ownedElements"].append(m)
    diagrama["ownedViews"].append(v)
    agregadas += 1

open(RUTA, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent="\t"))
print(f"{RUTA}: {agregadas} asociaciones nuevas; nombres y documentación actualizados")
