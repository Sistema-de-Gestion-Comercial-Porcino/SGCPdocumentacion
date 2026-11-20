"""Genera 00_Documentacion/Diccionario_clases.md a partir de 01_Generales/Clases_SGCC.mdj.

Uso: python3 diccionario.py <02_Ingenieria_de_Software>
"""
import json, os, sys

RAIZ = sys.argv[1]
P = json.load(open(os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj"), encoding="utf-8"))
ids = {}
def w(o):
    if isinstance(o, dict):
        if "_id" in o: ids[o["_id"]] = o
        for v in o.values(): w(v)
    elif isinstance(o, list):
        for x in o: w(x)
w(P)
clases = [o for o in ids.values() if o.get("_type") == "UMLClass"]
enums = [o for o in ids.values() if o.get("_type") == "UMLEnumeration"]
asocs = [o for o in ids.values() if o.get("_type") == "UMLAssociation"]

def tipo(t):
    return ids[t["$ref"]]["name"] if isinstance(t, dict) else (t or "")
def mult(e):
    return e.get("multiplicity", "") or "1"

L = ["# Diccionario del modelo de clases", "",
     f"Modelo general con {len(clases)} clases, {len(asocs)} asociaciones y {len(enums)} enumeraciones, alineado con el dominio de "
     "SGCPapi (`src/SGCP.Api/Dominio`). Los nombres de clase y de atributo son los de la API en camelCase; `[0..1]` marca un valor "
     "opcional (fecha, número o enumeración que admite nulo). Cada operación corresponde a un método real de un servicio de la API, indicado junto a "
     "cada operación. Las clases de interfaz/control de las secuencias y colaboraciones son participantes de análisis; no son tablas.", "",
     "Cadena del producto obtenido: OrdenProduccion → ResultadoProduccion → Lote → Producto → ClasificacionProducto. "
     "La previsión, el resultado real y la existencia física son conceptos diferentes.", "",
     "**SeguimientoCobro** (con la enumeración EstadoSeguimiento) es el seguimiento de cobros de Finanzas; se agregó a SGCPapi en "
     "v4.3.0 (endpoints `api/v1/seguimientos-cobro`).", ""]

def nombre_rel(a):
    e1, e2 = a["end1"], a["end2"]
    return ids[e1["reference"]["$ref"]]["name"], mult(e1), ids[e2["reference"]["$ref"]]["name"], mult(e2), a.get("name", "")

for c in clases:
    L += [f"## {c['name']}", ""]
    if c.get("documentation"): L += [c["documentation"], ""]
    L += ["| Atributo | Tipo |", "|---|---|"]
    for a in c.get("attributes", []):
        L.append(f"| {a['name']} | {tipo(a.get('type'))}{' [0..1]' if a.get('multiplicity') == '0..1' else ''} |")
    L.append("")
    ops = c.get("operations", [])
    if ops:
        L.append("Operaciones:")
        L.append("")
        for o in ops:
            ps = ", ".join(p["name"] for p in o.get("parameters", []) if p.get("direction") != "return")
            doc = f" — {o['documentation'].removesuffix(' en SGCPapi.')}" if o.get("documentation") else ""
            L.append(f"- `{o['name']}({ps})`{doc}")
        L.append("")
    rel = []
    for a in asocs:
        n1, m1, n2, m2, nom = nombre_rel(a)
        if c["name"] in (n1, n2):
            otro, mo, mc = (n2, m2, m1) if n1 == c["name"] else (n1, m1, m2)
            rel.append(f"{c['name']} {mc} — {mo} {otro}{' («' + nom + '»)' if nom else ''}")
    if rel:
        L += ["Asociaciones:", ""] + [f"- {r}" for r in rel] + [""]

L += ["## Enumeraciones", ""]
for e in enums:
    L.append(f"- {e['name']}: {', '.join(l['name'] for l in e.get('literals', []))}.")
L.append("")
open(os.path.join(RAIZ, "00_Documentacion", "Diccionario_clases.md"), "w", encoding="utf-8").write("\n".join(L))
print(len(clases), "clases;", len(asocs), "asociaciones;", len(enums), "enumeraciones")
