"""Genera secuencia, colaboración y actividad de CU13, CU14 y CU15 clonando un caso con la misma forma.

Uso: python3 derivados_cu.py <02_Ingenieria_de_Software>

Cada caso nuevo usa una plantilla con el mismo número de ramas y de mensajes por rama (CU02, CU04, CU12).
Todos los textos se reemplazan desde una especificación explícita; al final se verifica que no quede ningún
texto propio de la plantilla.
"""
import base64, copy, json, os, re, sys

RAIZ = sys.argv[1]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render_mdj"))
import render as R

PLANTILLAS = {
    "CU02": dict(nombre="Administrar usuarios", control="Usuarios", carril="Administrador", actor="Administrador", ramas=[
        ("Consultar usuarios", "permiso usuarios.consultar", "Denegar consulta no autorizada",
         ["buscarUsuarios(filtro)", "mostrarUsuariosYPermisos()"]),
        ("Crear usuario", "login único; permisos autorizados", "Informar duplicado o datos faltantes",
         ["validarDatosYLogin(datos)", "crearUsuarioYAsignarPermisos(datos,permisos)", "auditarAlta()"]),
        ("Editar usuario", "usuario existente; cambio autorizado", "Rechazar conflicto o escalamiento de permisos",
         ["cargarUsuarioYVersion(id)", "actualizarDatosYPermisos(id,version,cambios)", "auditarModificacion()"]),
        ("Desactivar o habilitar", "queda un Superadministrador activo", "Impedir dejar el sistema sin administrador habilitado",
         ["validarDependenciasYResponsable(id)", "cambiarEstadoYRevocarSesionesSiCorresponde(id)", "auditarCambioEstado()"])]),
    "CU04": dict(nombre="Gestión de costos", control="Costos", carril="Propietario", actor="Propietario", ramas=[
        ("Consultar costos y precios", "producto accesible", "Informar producto inexistente",
         ["buscarProductoYClasificacion(filtro)", "consultarVigenciasYMargenEstimado(productoId)"]),
        ("Definir nueva vigencia", "costo y precio válidos; margen aceptado", "Pedir corregir margen, fechas o unidades; conservar vigencia actual",
         ["validarUnidadYValores(productoId,costo,precio)", "guardarVigenciaCostoPrecio(productoId,desde,hasta)", "publicarPrecioVigente()"]),
        ("Corregir o finalizar vigencia", "cambio autorizado; sin alterar acuerdos históricos", "Rechazar modificación retroactiva de pedidos confirmados",
         ["consultarVigenciaYReferencias(id)", "cerrarVigenciaOCrearCorreccionAuditada(id)", "conservarCostoYPrecioDePedidos()"])]),
    "CU12": dict(nombre="Gestionar reportes", control="Reportes", carril="Usuarios autorizados", actor="Todos", ramas=[
        ("Seleccionar reporte y filtros", "tipo permitido; fechas coherentes", "Denegar datos ajenos o filtros incompatibles",
         ["listarReportesPermitidosPorPerfil()", "validarFiltros(fechaDesde,fechaHasta,cliente,producto,estado)", "aplicarAlcanceDeDatosDelUsuario()"]),
        ("Consultar resultados", "consulta autorizada", "Mostrar sin resultados sin inventar registros",
         ["consultarPedidosProduccionInventarioCobranzaOEntregas()", "agruparPorProductoYCorteODerivadoCuandoCorresponda()", "mostrarTotalesUnidadesYPeriodo()"]),
        ("Exportar reporte", "misma autorización y filtros de la consulta", "Informar error de exportación y permitir reintento",
         ["volverAValidarPermisosYFiltros()", "generarArchivoPDFoExcelConDatosAutorizados()", "registrarConsultaSinModificarOperaciones()"])]),
}

NUEVOS = {
    "CU13": dict(plantilla="CU02", nombre="Administrar cuentas de nivel superior", control="CuentasSuperiores",
                 carril="Superadministrador", actor="Superadministrador",
                 roles="Superadministrador", pre="Superadministrador autenticado (nivel 100).",
                 desc="Extiende CU02. Solo el Superadministrador crea, edita o desactiva cuentas con rol PROPIETARIO o SUPERADMIN "
                      "(PuedeGestionar y RolesSistema.Asignable). Nadie cambia sus propios privilegios; siempre queda un Superadministrador activo.",
                 ramas=[
        ("Consultar cuentas de nivel superior", "permiso usuarios.consultar", "Denegar consulta no autorizada",
         ["listar(busqueda,estado,rol)", "vista(usuario)"]),
        ("Crear Propietario o Superadministrador", "login y correo únicos; rol asignable por nivel", "Informar USUARIO_DUPLICADO o JERARQUIA_ROLES",
         ["validarRolesAsignables(roles)", "guardar(datos,roles,clave)", "registrarAuditoria(operacion,entidad)"]),
        ("Editar cuenta de nivel superior", "usuario existente; puedeGestionar; no es la propia cuenta", "Rechazar JERARQUIA_ROLES sin modificar la cuenta",
         ["puedeGestionar(usuario)", "guardar(id,datos,roles)", "revocarSesionesYAuditar(id)"]),
        ("Desactivar o habilitar", "queda un Superadministrador activo", "Impedir desactivar al último Superadministrador activo",
         ["protegerAdministrador(id)", "estado(id,estado)", "revocarSesionesYAuditar(id)"])]),
    "CU14": dict(plantilla="CU04", nombre="Delegar rol de Finanzas", control="DelegacionFinanzas",
                 carril="Propietario", actor="Propietario",
                 roles="Superadministrador, Propietario", pre="Propietario o Superadministrador autenticado.",
                 desc="Extiende CU02. Solo PROPIETARIO o SUPERADMIN asignan o retiran FINANZAS (RolesSistema.Asignable). "
                      "Un Administrador sin FINANZAS no recibe permisos financieros (GeneradorToken.PermisosEfectivos).",
                 ramas=[
        ("Consultar usuarios y roles", "permiso usuarios.consultar", "Denegar consulta no autorizada",
         ["listar(busqueda,estado,rol)", "roles(asignables)"]),
        ("Asignar rol FINANZAS", "actor PROPIETARIO o SUPERADMIN; usuario de nivel inferior", "Rechazar JERARQUIA_ROLES: el Administrador no delega Finanzas",
         ["validarRolesAsignables(roles)", "guardar(id,roles)", "revocarSesionesYAuditar(id)"]),
        ("Retirar rol FINANZAS", "puedeGestionar; queda al menos un rol", "Rechazar ROLES_INVALIDOS o JERARQUIA_ROLES",
         ["puedeGestionar(usuario)", "guardar(id,roles)", "revocarSesionesYAuditar(id)"])]),
    "CU15": dict(plantilla="CU12", nombre="Consultar auditoría", control="Auditoria",
                 carril="Propietario", actor="Propietario",
                 roles="Superadministrador, Propietario", pre="Superadministrador o Propietario autenticado con permiso auditoria.consultar.",
                 desc="Extiende CU12. Historial de solo lectura con fecha, usuario, operación y entidad de cada acción que registra "
                      "ServicioAuditoria; no se edita ni se borra.",
                 ramas=[
        ("Consultar historial reciente", "permiso auditoria.consultar", "Denegar acceso sin permiso (403)",
         ["auditoria(pagina,tamanoPagina)", "ordenarPorFechaDescendente()", "mostrarFechaUsuarioAccionModulo()"]),
        ("Cambiar de página", "página dentro del total", "Mostrar página vacía sin inventar registros",
         ["auditoria(pagina,tamanoPagina)", "paginar(pagina,tamanoPagina)", "mostrarTotalRegistrosYPaginas()"]),
        ("Revisar una acción registrada", "registro en la página actual", "Informar que el registro no está en la página actual",
         ["identificarUsuarioPorLogin(usuario)", "identificarOperacionYEntidad(operacion,entidad)", "conservarRegistroSinModificar()"])]),
}

def accion(m):
    nombre, _, params = m.partition("(")
    params = params.rstrip(")")
    sep = lambda t: re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", t)
    n = sep(nombre); n = n[0].upper() + n[1:]
    return n + ("\nDatos: " + ", ".join(sep(p) for p in params.split(",")) if params else "")

def textos_largos(P, f):
    """Extrae del archivo de la plantilla precondición, descripción y roles."""
    out = {}
    for o in todos(P):
        for k in ("text", "documentation", "name"):
            t = o.get(k)
            if not isinstance(t, str): continue
            m = re.match(r"Precondición: (.*?)\n(.*?)(\n|$)", t, re.S)
            if m and "pre" not in out: out["pre"], out["desc"] = m.group(1), m.group(2)
            m = re.search(r"Roles autorizados: (.*?)\. ", t)
            if m: out["roles"] = m.group(1)
            m = re.search(r"Actores autorizados: (.*?)\. Se ejecuta", t)
            if m: out["roles2"] = m.group(1)
    return out

def todos(o, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        acc.append(o)
        for v in o.values(): todos(v, acc)
    elif isinstance(o, list):
        for x in o: todos(x, acc)
    return acc

def mapa(cu_t, T, cu_n, N, largos):
    exacto, sub = {}, []
    def par(a, b): exacto[a] = b
    nt, nn = T["nombre"], N["nombre"]
    for suf in ("", " — Secuencia", " — Colaboración", " — Actividad"):
        pass
    par(f"{cu_t} — {nt}", f"{cu_n} — {nn}")
    par(f"{cu_t} — Secuencia · {nt}", f"{cu_n} — Secuencia · {nn}")
    par(f"{cu_t} — Actividad · {nt}", f"{cu_n} — Actividad · {nn}")
    par(f"{cu_t} — Colaboración", f"{cu_n} — Colaboración")
    par(f"{cu_t} · {nt}", f"{cu_n} · {nn}")
    par(f"(from {cu_t} — {nt})", f"(from {cu_n} — {nn})")
    par(f"(from {cu_t} — Colaboración)", f"(from {cu_n} — Colaboración)")
    par(nt, nn)
    par(f"seleccionar operación de {nt}", f"seleccionar operación de {nn}")
    tc, nc = T["control"], N["control"]
    par(f"control: {tc}", f"control: {nc}"); par(f"datos: Repositorio{tc}", f"datos: Repositorio{nc}")
    for p in ("Interfaz", "Control", "Repositorio"):
        par(p + tc, p + nc); par(f"{p.lower() if p != 'Repositorio' else 'datos'}: {p}{tc}", f"{p.lower() if p != 'Repositorio' else 'datos'}: {p}{nc}")
    par(f"interfaz: Interfaz{tc}", f"interfaz: Interfaz{nc}")
    par(T["carril"], N["carril"]); par(f"(from {T['carril']})", f"(from {N['carril']})")
    assert len(T["ramas"]) == len(N["ramas"]), cu_n
    for i, (rt, rn) in enumerate(zip(T["ramas"], N["ramas"])):
        L = "ABCD"[i]
        (a, c, r, ms), (a2, c2, r2, ms2) = rt, rn
        assert len(ms) == len(ms2), (cu_n, i)
        g, g2 = f"{a}; actor: {T['actor']}; {c}", f"{a2}; actor: {N['actor']}; {c2}"
        par(g, g2); par(f"[{g}]", f"[{g2}]")
        par(f"{i+1}. {a} · {c}", f"{i+1}. {a2} · {c2}")
        par(a, a2); par(f"{L} · {a}", f"{L} · {a2}"); par(f"Seleccionar: {a}", f"Seleccionar: {a2}")
        par(f"¿{c}?", f"¿{c2}?"); par(r, r2)
        for j, (m, m2) in enumerate(zip(ms, ms2)):
            par(m, m2); par(f"1.2.{i+1}.{j+1} [operación {i+1}] : {m}", f"1.2.{i+1}.{j+1} [operación {i+1}] : {m2}")
            par(accion(m), accion(m2))
    # textos largos: por subcadenas
    roles2 = N["roles"].replace(", ", " · ")
    sub += [(largos["desc"], N["desc"]), (largos["pre"], N["pre"]),
            ("Roles autorizados: " + largos["roles"] + ".", "Roles autorizados: " + N["roles"] + "."),
            ("Actores autorizados: " + largos["roles2"] + ".", "Actores autorizados: " + roles2 + ".")]
    for (a, c, r, ms), (a2, c2, r2, ms2) in zip(T["ramas"], N["ramas"]):
        sub += [(f"{a}: {r}", f"{a2}: {r2}"), (r, r2)]
    return exacto, sub

def nid_factory(usados):
    def nid():
        while True:
            i = base64.b64encode(os.urandom(12)).decode()
            if i not in usados:
                usados.add(i); return i
    return nid

CARPETAS = [("06_Secuencias", "_Secuencia"), ("02_Colaboracion", "_Colaboracion"), ("05_Actividades", "_Actividad")]
for cu_n, N in NUEVOS.items():
    cu_t = N["plantilla"]; T = PLANTILLAS[cu_t]
    for carpeta, suf in CARPETAS:
        src = os.path.join(RAIZ, carpeta, f"{cu_t}{suf}.mdj")
        P = json.load(open(src, encoding="utf-8"))
        largos = textos_largos(json.load(open(os.path.join(RAIZ, "06_Secuencias", f"{cu_t}_Secuencia.mdj"), encoding="utf-8")), src)
        largos.update({k: v for k, v in textos_largos(P, src).items() if k in ("roles", "roles2")})
        largos.setdefault("roles", largos.get("roles2", "").replace(" · ", ", "))
        largos.setdefault("roles2", largos.get("roles", "").replace(", ", " · "))
        exacto, sub = mapa(cu_t, T, cu_n, N, largos)
        originales = set()
        for o in todos(P):
            for k in ("name", "text", "guard", "documentation"):
                t = o.get(k)
                if not isinstance(t, str) or not t: continue
                originales.add(t)
                if t in exacto: o[k] = exacto[t]; continue
                for a, b in sub:
                    if a and a in t: t = t.replace(a, b)
                t = t.replace(f"{cu_t} ", f"{cu_n} ").replace(nt := T["nombre"], N["nombre"])
                o[k] = t
        # ids nuevos para que no choquen al consolidar
        usados = set(); nid = nid_factory(usados)
        m = {o["_id"]: nid() for o in todos(P) if "_id" in o}
        for o in todos(P):
            if "_id" in o: o["_id"] = m[o["_id"]]
            if set(o) == {"$ref"}:
                assert o["$ref"] in m, (cu_n, suf, o["$ref"])
                o["$ref"] = m[o["$ref"]]
        P["name"] = P.get("name", "").replace(cu_t, cu_n)
        # verificación: ningún texto exclusivo de la plantilla
        nuevos_t = set()
        for o in todos(P):
            for k in ("name", "text", "guard", "documentation"):
                if isinstance(o.get(k), str): nuevos_t.add(o[k])
        propios = {t for t in originales if t in nuevos_t and (cu_t in t or any(t == x for x in exacto) and exacto.get(t) != t)}
        restos = [t for t in nuevos_t if cu_t in t.replace(f"Extiende {cu_t}", "") or T["nombre"] in t or T["control"] in t]
        restos += [t for t in nuevos_t for (a, c, r, ms) in T["ramas"] for x in ms + [a, r] if x and x == t and x not in [y for rr in N["ramas"] for y in rr[3] + [rr[0], rr[2]]]]
        if restos:
            raise SystemExit(f"{cu_n}{suf}: quedan textos de {cu_t}: {sorted(set(restos))[:8]}")
        # etiquetas de acciones: el alto depende de las líneas del texto nuevo
        for o in todos(P):
            if o.get("_type") != "UMLActionView": continue
            for c in o.get("subViews", []):
                if c.get("_type") != "UMLNameCompartmentView": continue
                for t in c.get("subViews", []):
                    if t.get("visible", True) and isinstance(t.get("text"), str) and t["text"]:
                        tam, est = R.parse_font(t.get("font", "Arial;13;0"))
                        lineas = len(R.envolver(t["text"], t["width"], tam, est))
                        alto = int(tam * 1.18 * lineas + 2)
                        if t["height"] < alto:
                            t["height"] = alto
                            c["height"] = max(c["height"], t["top"] - c["top"] + alto + 5)
        dst = os.path.join(RAIZ, carpeta, f"{cu_n}{suf}.mdj")
        json.dump(P, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
        print("ok", dst)
