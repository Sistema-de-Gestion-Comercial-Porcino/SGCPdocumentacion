"""Lleva los roles nuevos (SUPERADMIN, PROPIETARIO, ADMINISTRADOR, FINANZAS...) a los demás diagramas.

Uso: python3 actualizar_roles.py <raiz de 02_Ingenieria_de_Software>
Reemplaza solo textos; no mueve vistas. Idempotente. No toca BPMN_Actual (proceso AS-IS del negocio).
"""
import glob, json, os, re, sys
from modelo import ACTORES, ASOCIACIONES, GENERALIZACIONES

RAIZ = sys.argv[1]
NOMBRE = {k: n for k, n, _ in ACTORES}
ORDEN = [k for k, _, _ in ACTORES]
PADRES = {h: p for h, p in GENERALIZACIONES}

def autorizados(cu):
    ks = {a for a, l in ASOCIACIONES.items() if cu in l}
    cambio = True
    while cambio:  # herencia: si el padre participa, el hijo también
        cambio = False
        for h, p in PADRES.items():
            if p in ks and h not in ks: ks.add(h); cambio = True
    return [NOMBRE[k] for k in ORDEN if k in ks]

# Actor que ejecuta lo que antes era "Propietario / administración", según el permiso real de la API.
PA = {"CU01": "Administrador", "CU02": "Administrador", "CU03": "Administrador", "CU04": "Propietario",
      "CU07": "Administrador", "CU10": "Propietario", "CU12": "Propietario"}

FIJOS = [
    ("El personal recibe una cuenta de administración.", "El personal recibe una cuenta con el rol de su puesto."),
    ("permiso de administración", "permiso usuarios.consultar"),
    ("se conserva administración activa", "queda un Superadministrador activo"),
    ("administración autorizada", "actor de nivel superior autorizado"),
    ("Comprador solo CLI-17; administración puede consultar alcance autorizado.",
     "Comprador solo CLI-17; Administrador y Propietario consultan según la matriz de reportes de su rol."),
    ("Reportes disponibles durante la operación para los seis perfiles.", "Reportes disponibles durante la operación para los nueve perfiles."),
    ("Este tramo muestra la consulta de administración;", "Este tramo muestra la consulta del Propietario;"),
    ("Ventas / cobranza", "Ventas"),
]

def texto(s, cu):
    if cu:
        lista = autorizados(cu)
        s = re.sub(r"Actores autorizados: [^.]*\. Se ejecuta", "Actores autorizados: " + " · ".join(lista) + ". Se ejecuta", s)
        s = re.sub(r"Roles autorizados: [^.]*\.", "Roles autorizados: " + ", ".join(lista) + ".", s)
    for a, b in FIJOS:
        s = s.replace(a, b)
    if "Propietario / administración" in s:
        s = s.replace("Propietario / administración", PA.get(cu, "Propietario"))
    return s

def recorrer(o, cu, cambios):
    if isinstance(o, dict):
        n = o.get("name")
        if isinstance(n, str) and (m := re.match(r"CU(\d\d)\b", n)):
            cu = "CU" + m.group(1)
        for k, v in o.items():
            if isinstance(v, str) and k not in ("_id", "_type"):
                nv = texto(v, cu)
                if nv != v: o[k] = nv; cambios[0] += 1
            else:
                recorrer(v, cu, cambios)
    elif isinstance(o, list):
        for x in o: recorrer(x, cu, cambios)

def cu_de_archivo(ruta):
    m = re.match(r"(CU\d\d)_", os.path.basename(ruta))
    return m.group(1) if m else None

total = 0
for ruta in sorted(glob.glob(os.path.join(RAIZ, "*", "*.mdj"))):
    base = os.path.basename(ruta)
    if base in ("BPMN_Actual.mdj", "Casos_de_Uso_SGCC.mdj", "Clases_SGCC.mdj"):
        continue
    crudo = open(ruta, encoding="utf-8").read()
    d = json.loads(crudo)
    cambios = [0]
    recorrer(d, cu_de_archivo(ruta), cambios)
    if cambios[0]:
        sangria = "\t" if crudo.startswith("{\n\t") else (None if "\n" not in crudo[:200] else 2)
        json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=sangria,
                  separators=None if sangria else (",", ":"))
        print(f"{cambios[0]:4d}  {os.path.relpath(ruta, RAIZ)}"); total += cambios[0]
print("textos cambiados:", total)
