"""Alinea Componentes_SGCC.mdj y Despliegue_SGCC.mdj con los proyectos reales (SGCPapi, SGCPuiweb, SGCPuimovil).

Uso: python3 generales_api.py <02_Ingenieria_de_Software>
- Renombra componentes, nodos y artefactos (modelo y vistas).
- Quita el nodo "Almacén central de evidencias": la API guarda la evidencia en la base (EvidenciaRecepcion.Contenido + Sha256).
"""
import json, os, sys
RAIZ = sys.argv[1]
REN = {
 "Web de gestión online": "SGCP.Web · gestión (ASP.NET Core MVC)",
 "Portal comprador online": "SGCP.Web · portal comprador",
 "App Android · Kotlin": "SGCP Reparto · Android Kotlin",
 "Persistencia local · Room y archivos": "Persistencia local · Room (SQLite)",
 "API comercial · HTTPS": "SGCP.Api · REST HTTPS + JWT",
 "Persistencia central": "SgcpContext · EF Core (MySQL o SQL Server)",
 "Archivos de evidencia": "Evidencias en la base (contenido + sha256)",
 "Adaptador fiscal": "ProveedorFiscalAdapter",
 "Servicio fiscal externo": "Servicio fiscal externo (pendiente de confirmar)",
 "sgcc-web · gestión responsiva": "SGCP.Web · gestión responsiva",
 "sgcc-portal · web responsiva": "SGCP.Web · portal comprador",
 "sgcc-reparto.apk · Kotlin": "bo.edu.univalle.sgcp · APK Kotlin",
 "Room / SQLite · entregas y cola": "Room / SQLite · entregas y cola de recepciones",
 "Evidencias · archivos privados": "Evidencias · archivos privados de la app",
 "sgcc-web + sgcc-portal": "SGCP.Web · .NET 10",
 "sgcc-api · negocio y validación sync": "SGCP.Api · .NET 10, EF Core, JWT",
 "Gestor relacional": "MySQL 8 (por defecto) o SQL Server 2022",
 "sgcc · datos centrales": "base sgcp · datos y evidencias",
 "Proveedor fiscal externo": "Proveedor fiscal externo (pendiente)",
 "Servicio de emisión y consulta": "Emisión fiscal · aún no integrada",
 "copias de base y evidencias": "copias de la base (incluye evidencias)",
}
QUITAR_NODO = "Almacén central de evidencias"

def todos(o, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        acc.append(o)
        for v in o.values(): todos(v, acc)
    elif isinstance(o, list):
        for x in o: todos(x, acc)
    return acc

for f in ("Componentes_SGCC.mdj", "Despliegue_SGCC.mdj"):
    ruta = os.path.join(RAIZ, "01_Generales", f)
    P = json.load(open(ruta, encoding="utf-8"))
    n = 0
    for o in todos(P):
        for k in ("name", "text"):
            if isinstance(o.get(k), str) and o[k] in REN: o[k] = REN[o[k]]; n += 1
    quitados = 0
    nodo = next((o for o in todos(P) if o.get("_type") == "UMLNode" and o.get("name") == QUITAR_NODO), None)
    if nodo:
        borrar = {x["_id"] for x in todos(nodo) if "_id" in x}
        # caminos de comunicación que tocan el nodo
        for o in todos(P):
            if o.get("_type") in ("UMLCommunicationPath", "UMLDependency", "UMLAssociation", "UMLDeployment"):
                ends = [o.get("end1", {}).get("reference", {}).get("$ref"), o.get("end2", {}).get("reference", {}).get("$ref"),
                        o.get("source", {}).get("$ref"), o.get("target", {}).get("$ref")]
                if any(e in borrar for e in ends): borrar |= {x["_id"] for x in todos(o) if "_id" in x}
        # vistas cuyo modelo se borra, o aristas que apuntan a vistas borradas
        cambio = True
        while cambio:
            cambio = False
            for o in todos(P):
                if "_id" in o and o["_id"] not in borrar:
                    refs = [o.get(k, {}).get("$ref") for k in ("model", "head", "tail", "hostEdge") if isinstance(o.get(k), dict)]
                    if any(r in borrar for r in refs):
                        borrar |= {x["_id"] for x in todos(o) if "_id" in x}; cambio = True
        def podar(o):
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if isinstance(v, list):
                        o[k] = [x for x in v if not (isinstance(x, dict) and x.get("_id") in borrar)]
                    podar(o[k])
            elif isinstance(o, list):
                for x in o: podar(x)
        podar(P); quitados = len(borrar)
    ids = {o["_id"] for o in todos(P) if "_id" in o}
    malas = [o["$ref"] for o in todos(P) if set(o) == {"$ref"} and o["$ref"] not in ids]
    assert not malas, (f, malas[:5])
    json.dump(P, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
    print(f, "renombrados", n, "quitados", quitados)
