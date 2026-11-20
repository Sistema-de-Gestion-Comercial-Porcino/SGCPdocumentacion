"""Genera Casos_de_Uso_SGCC.mdj (StarUML) y su PNG sin ejecutar JavaScript.

Uso: python3 generar_mdj.py <raiz de 02_Ingenieria_de_Software>
Las vistas se clonan del .mdj anterior (y de Clases/Componentes) para respetar el formato de StarUML.
"""
import base64, copy, json, os, subprocess, sys
import disposicion as D
from modelo import ACTORES, CASOS, ASOCIACIONES, GENERALIZACIONES, EXTENSIONES
import vista_previa

RAIZ = sys.argv[1]
SALIDA = os.path.join(RAIZ, "01_Generales", "Casos_de_Uso_SGCC.mdj")

def git_show(ruta):  # plantilla: versión de main, no la que estamos sobrescribiendo
    rel = os.path.relpath(ruta, os.path.dirname(RAIZ))
    return json.loads(subprocess.check_output(["git", "-C", os.path.dirname(RAIZ), "show", "2bb5dfc:" + rel]))

def buscar(o, t, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        if o.get("_type") == t: acc.append(o)
        for v in o.values(): buscar(v, t, acc)
    elif isinstance(o, list):
        for x in o: buscar(x, t, acc)
    return acc

usados = set()
def nid():
    while True:
        i = base64.b64encode(os.urandom(11)).decode()
        if i not in usados and "/" not in i[:2]:
            usados.add(i); return i

def clonar(plantilla, mapa):
    c = copy.deepcopy(plantilla)
    for o in buscar_todos(c):
        if "_id" in o: mapa[o["_id"]] = nid()
    def rem(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k == "_id": o[k] = mapa.get(v, v)
                elif isinstance(v, dict) and set(v) == {"$ref"}: v["$ref"] = mapa.get(v["$ref"], v["$ref"])
                else: rem(v)
        elif isinstance(o, list):
            for x in o: rem(x)
    rem(c); return c

def buscar_todos(o, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        acc.append(o)
        for v in o.values(): buscar_todos(v, acc)
    elif isinstance(o, list):
        for x in o: buscar_todos(x, acc)
    return acc

viejo = git_show(SALIDA)
clases = git_show(os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj"))
comp = git_show(os.path.join(RAIZ, "01_Generales", "Componentes_SGCC.mdj"))
T = {t: buscar(viejo, t)[0] for t in ["UMLActorView", "UMLUseCaseView", "UMLAssociationView", "UMLUseCaseSubjectView", "UMLTextView"]}
T["UMLGeneralizationView"] = buscar(clases, "UMLGeneralizationView")[0]
T["UMLDependencyView"] = buscar(comp, "UMLDependencyView")[0]
diag_viejo = buscar(viejo, "UMLUseCaseDiagram")[0]["_id"]
modelo_viejo = buscar(viejo, "UMLModel")[0]["_id"]
sub_viejo = buscar(viejo, "UMLSubsystem")[0]["_id"]

def ref(i): return {"$ref": i}

def poner_nombre(vista, texto):
    for lab in buscar(vista, "UMLNameCompartmentView")[0]["subViews"]:
        if lab.get("text") is not None and not lab.get("visible", True) is False and "(from" not in str(lab.get("text")):
            lab["text"] = texto

# ---------------- modelo
P, M, G, S = nid(), nid(), nid(), nid()
proyecto = {"_type": "Project", "_id": P, "name": "SGCC — Casos de uso", "documentVersion": 1, "ownedElements": []}
modelo = {"_type": "UMLModel", "_id": M, "_parent": ref(P), "name": "SGCC — Casos de uso", "ownedElements": []}
proyecto["ownedElements"].append(modelo)
diagrama = {"_type": "UMLUseCaseDiagram", "_id": G, "_parent": ref(M), "name": "Casos de uso generales del SGCC", "defaultDiagram": True, "ownedViews": []}
subsistema = {"_type": "UMLSubsystem", "_id": S, "_parent": ref(M), "name": "Sistema de Gestión Comercial y Clientes (SGCC)"}
modelo["ownedElements"] += [diagrama, subsistema]

nombre_actor = {k: n for k, n, _ in ACTORES}
actor_id, caso_id = {}, {}
for k, n, _ in ACTORES:
    actor_id[k] = nid()
    usa = [c for c in ASOCIACIONES[k]]
    modelo["ownedElements"].append({"_type": "UMLActor", "_id": actor_id[k], "_parent": ref(M), "name": n,
        "documentation": "Casos directos: " + ", ".join(usa) + ".", "ownedElements": []})
def actores_de(c):
    return [nombre_actor[a] for a in ASOCIACIONES if c in ASOCIACIONES[a]]
for k, n, secc, ext, doc in CASOS:
    caso_id[k] = nid()
    modelo["ownedElements"].append({"_type": "UMLUseCase", "_id": caso_id[k], "_parent": ref(M),
        "name": f"{n} ({secc})", "ownedElements": [],
        "documentation": f"Actores directos: {', '.join(actores_de(k))}. Secciones: {secc}. {doc}"})
porid = {o["_id"]: o for o in modelo["ownedElements"]}

# ---------------- vistas
pc = D.casos()
lay = json.load(open(os.path.join(os.path.dirname(__file__) or ".", "actores.json")))
pa = D.actores(lay["izq"], lay["der"], lay["y_izq"], lay["y_der"])
ALTO = int(max(r[1] + r[3] for r in pc.values()) + 140)

def texto(t, left, top, w, h, tam):
    v = clonar(T["UMLTextView"], {diag_viejo: G})
    v.update(_parent=ref(G), left=left, top=top, width=w, height=h, text=t, font=f"Arial;{tam};0")
    diagrama["ownedViews"].append(v)
texto("SGCC · Diagrama de casos de uso general", 80, 20, 2800, 60, 34)
texto("Cada actor aparece una sola vez. Entre paréntesis: secciones del menú de la web / Android que implementan el caso.\n"
      "Superadministrador ▷ Propietario ▷ Administrador: cada nivel hereda los casos del nivel inferior y suma los propios. "
      "Finanzas es un rol que solo delega el Propietario.", 80, 90, 2800, 80, 20)

sv = clonar(T["UMLUseCaseSubjectView"], {diag_viejo: G, sub_viejo: S})
bx0 = D.CX - D.UC_W / 2 - 90
sv.update(_parent=ref(G), model=ref(S), left=bx0, top=190, width=D.UC_W + 180, height=ALTO - 190, containedViews=[])
poner_nombre(sv, subsistema["name"])
diagrama["ownedViews"].append(sv)

vista = {}
for k, n, secc, ext, doc in CASOS:
    old_model = buscar(viejo, "UMLUseCaseView")[0]["model"]["$ref"]
    v = clonar(T["UMLUseCaseView"], {diag_viejo: G, old_model: caso_id[k], sv_id: sv["_id"]} if (sv_id := T["UMLUseCaseSubjectView"]["_id"]) else {})
    x, y, w, h = pc[k]
    color = "#fff4e0" if ext else "#eef3fb"
    v.update(_parent=ref(G), model=ref(caso_id[k]), containerView=ref(sv["_id"]), left=x, top=y, width=w, height=h,
             fillColor=color, font="Arial;18;0")
    for s in buscar_todos(v):
        if s.get("_type") == "LabelView" or s.get("_type", "").endswith("CompartmentView"):
            s["fillColor"] = color; s["font"] = s["font"].replace(";23;", ";18;")
    poner_nombre(v, porid[caso_id[k]]["name"])
    diagrama["ownedViews"].append(v); sv["containedViews"].append(ref(v["_id"])); vista[k] = v

old_actor = buscar(viejo, "UMLActorView")[0]["model"]["$ref"]
for k, n, _ in ACTORES:
    v = clonar(T["UMLActorView"], {diag_viejo: G, old_actor: actor_id[k]})
    x, y, w, h = pa[k]
    v.update(_parent=ref(G), model=ref(actor_id[k]), left=x, top=y, width=w, height=h)
    poner_nombre(v, n)
    diagrama["ownedViews"].append(v); vista[k] = v

def pts(lista): return ";".join(f"{round(a)}:{round(b)}" for a, b in lista)

tA = T["UMLAssociationView"]; old_as = tA["model"]["$ref"]
old_assoc = [o for o in buscar(viejo, "UMLAssociation") if o["_id"] == old_as][0]
for a, lista in ASOCIACIONES.items():
    for c in lista:
        A, E1, E2 = nid(), nid(), nid()
        modelo["ownedElements"].append({"_type": "UMLAssociation", "_id": A, "_parent": ref(M),
            "end1": {"_type": "UMLAssociationEnd", "_id": E1, "_parent": ref(A), "reference": ref(actor_id[a])},
            "end2": {"_type": "UMLAssociationEnd", "_id": E2, "_parent": ref(A), "reference": ref(caso_id[c])}})
        v = clonar(tA, {diag_viejo: G, old_as: A, old_assoc["end1"]["_id"]: E1, old_assoc["end2"]["_id"]: E2})
        tip = D.punta(pc[c], pa[a]); pre = (tip[0] - 14 if tip[0] == pc[c][0] else tip[0] + 14, tip[1])
        ini = vista_previa.borde_rect(pa[a], tip)
        v.update(_parent=ref(G), model=ref(A), tail=ref(vista[a]["_id"]), head=ref(vista[c]["_id"]),
                 points=pts([ini, pre, tip]), lineStyle=1)
        diagrama["ownedViews"].append(v)

tG = T["UMLGeneralizationView"]; old_g = tG["model"]["$ref"]
for h, p in GENERALIZACIONES:
    Gi = nid()
    porid[actor_id[h]]["ownedElements"].append({"_type": "UMLGeneralization", "_id": Gi, "_parent": ref(actor_id[h]),
        "source": ref(actor_id[h]), "target": ref(actor_id[p])})
    v = clonar(tG, {old_g: Gi})
    a = vista_previa.borde_rect(pa[h], D.centro(pa[p])); b = vista_previa.borde_rect(pa[p], D.centro(pa[h]))
    v.update(_parent=ref(G), model=ref(Gi), tail=ref(vista[h]["_id"]), head=ref(vista[p]["_id"]), points=pts([a, b]))
    diagrama["ownedViews"].append(v)

tD = T["UMLDependencyView"]; old_d = tD["model"]["$ref"]
for x, base in EXTENSIONES:
    X = nid()
    porid[caso_id[x]]["ownedElements"].append({"_type": "UMLExtend", "_id": X, "_parent": ref(caso_id[x]),
        "source": ref(caso_id[x]), "target": ref(caso_id[base])})
    v = clonar(tD, {old_d: X})
    v["_type"] = "UMLExtendView"
    a = vista_previa.borde_elipse(pc[x], D.centro(pc[base])); b = vista_previa.borde_elipse(pc[base], D.centro(pc[x]))
    v.update(_parent=ref(G), model=ref(X), tail=ref(vista[x]["_id"]), head=ref(vista[base]["_id"]), points=pts([a, b]))
    diagrama["ownedViews"].append(v)

for o in porid.values():
    if not o.get("ownedElements"): o.pop("ownedElements", None)

# Comprobación: toda $ref apunta a un _id existente
ids = {o["_id"] for o in buscar_todos(proyecto) if "_id" in o}
malas = [o["$ref"] for o in buscar_todos(proyecto) if set(o) == {"$ref"} and o["$ref"] not in ids]
assert not malas, malas[:5]
json.dump(proyecto, open(SALIDA, "w"), ensure_ascii=False, indent="\t")
vista_previa.dibujar(pa, pc, SALIDA.replace(".mdj", ".png"))
print("ok", SALIDA, len(ids), "ids; asociaciones", sum(map(len, ASOCIACIONES.values())))
