"""Regenera 02_Ingenieria_de_Software/04_Estados con los estados y transiciones reales de SGCPapi.

Uso: python3 estados_api.py <02_Ingenieria_de_Software>

Cada archivo lleva el modelo de clases vigente (01_Generales/Clases_SGCC.mdj) y la máquina de estados
cuelga de su clase, igual que antes. Los disparadores son los métodos públicos de la API; las guardas
son las validaciones del servicio. Valores de enumeración que ninguna operación asigna van en la nota.
"""
import base64, copy, json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render_mdj"))
from render import envolver, fuente

RAIZ = sys.argv[1]
CARPETA = os.path.join(RAIZ, "04_Estados")
PLANTILLA = "02_Ingenieria_de_Software/04_Estados/05_Reserva_Estados.mdj"

# ---------------------------------------------------------------- especificación
# estados: nombre -> (col, fila). "•" = inicial, "◆x" = decisión, "◉x" = final.
# transiciones: (origen, destino, disparador, guarda, efecto)
M = {}
M["01_Cotizacion_Estados"] = dict(
    clase="Cotizacion", atributo="estado", titulo="Cotizacion · estado (EstadoCotizacion)",
    estados={"•": (0, 0), "BORRADOR": (1, 0), "PRESENTADA": (2, 0), "ACEPTADA": (3, 0),
             "RECHAZADA": (2, 1), "VENCIDA": (3, 1), "◉": (3, 2)},
    trans=[("•", "BORRADOR", "guardar", "", ""),
           ("BORRADOR", "PRESENTADA", "cambiar(PRESENTADA)", "vigente; con detalle; productos y cliente activos", ""),
           ("PRESENTADA", "ACEPTADA", "cambiar(ACEPTADA)", "vigente", "registrar respuesta"),
           ("PRESENTADA", "RECHAZADA", "cambiar(RECHAZADA)", "con motivo", "guardar motivoRespuesta"),
           ("PRESENTADA", "VENCIDA", "vencer", "vigenteHasta <= ahora", ""),
           ("ACEPTADA", "◉", "confirmarAsync", "", "crear Pedido"),
           ("RECHAZADA", "◉", "", "", ""), ("VENCIDA", "◉", "", "", "")],
    nota="nuevaVersion crea otra Cotizacion en BORRADOR a partir de una PRESENTADA, ACEPTADA, RECHAZADA o VENCIDA sin pedido; "
         "la versión anterior conserva su estado. Una ACEPTADA sigue ACEPTADA cuando se confirma el pedido (ServicioConfirmarPedido).")
M["02_Pedido_Comercial_Estados"] = dict(
    clase="Pedido", atributo="estadoComercial", titulo="Pedido · estadoComercial (EstadoComercial)",
    estados={"•": (0, 0), "CONFIRMADO": (1, 0), "CANCELADO": (2, 0), "◉": (3, 0)},
    trans=[("•", "CONFIRMADO", "confirmarAsync", "cotización ACEPTADA y vigente", "PedidoBuilder.Construir"),
           ("CONFIRMADO", "CANCELADO", "cancelar", "señas resueltas; ninguna reserva CONSUMIDA; entrega PREPARADA o sin entrega",
            "liberar reservas; cancelar entrega y detalles"),
           ("CANCELADO", "◉", "", "", "")],
    nota="EstadoComercial define también PENDIENTE_ACUERDO y CERRADO, pero ninguna operación de SGCPapi los asigna todavía. "
         "Un pedido CONFIRMADO es el único que admite reservas, entregas, cargos, condición de pago y comprobante fiscal.")
M["03_Pedido_Preparacion_Estados"] = dict(
    clase="Pedido", atributo="estadoPreparacion", titulo="Pedido · estadoPreparacion (EstadoPreparacion)",
    estados={"•": (0, 0), "PENDIENTE": (1, 0), "PREPARADO": (2, 0), "BLOQUEADO": (1, 1)},
    trans=[("•", "PENDIENTE", "confirmarAsync", "", "PedidoBuilder.Construir"),
           ("PENDIENTE", "PREPARADO", "preparar", "reservas completas; lotes aptos", "crear Entrega PREPARADA"),
           ("PREPARADO", "PENDIENTE", "liberar", "reserva ACTIVA", "detalle PENDIENTE"),
           ("PENDIENTE", "BLOQUEADO", "bloquearLote", "reserva sobre el lote", "liberar reserva; registrar Incidencia"),
           ("PREPARADO", "BLOQUEADO", "bloquearLote", "reserva sobre el lote", "liberar reserva; registrar Incidencia"),
           ("BLOQUEADO", "PREPARADO", "preparar", "reservas repuestas y completas", "")],
    nota="EstadoPreparacion define también PROGRAMADA y EN_PREPARACION, pero ninguna operación de SGCPapi los asigna todavía. "
         "bloquearLote se ejecuta por rechazarLote o por un control sanitario rechazado del animal de origen.")
M["04_DetallePedido_Estados"] = dict(
    clase="DetallePedido", atributo="estado", titulo="DetallePedido · estado (EstadoDetalle)",
    estados={"•": (0, 0), "PENDIENTE": (1, 0), "RESERVADO": (2, 0), "PREPARADO": (3, 0), "CANCELADO": (2, 1), "◉": (3, 1)},
    trans=[("•", "PENDIENTE", "confirmarAsync", "", ""),
           ("PENDIENTE", "RESERVADO", "reservar", "suma reservada = cantidadConfirmada", ""),
           ("RESERVADO", "PENDIENTE", "liberar | bloquearLote", "", "reserva LIBERADA"),
           ("RESERVADO", "PREPARADO", "preparar", "reservas completas; lotes aptos", ""),
           ("PREPARADO", "PENDIENTE", "liberar | bloquearLote", "antes del despacho", "reserva LIBERADA"),
           ("PENDIENTE", "CANCELADO", "cancelar (pedido)", "", ""),
           ("RESERVADO", "CANCELADO", "cancelar (pedido)", "", "liberar reservas"),
           ("PREPARADO", "CANCELADO", "cancelar (pedido)", "entrega PREPARADA", "liberar reservas"),
           ("CANCELADO", "◉", "", "", "")],
    nota="Una reserva parcial deja el detalle en PENDIENTE. EstadoDetalle define también EN_PREPARACION, que ninguna operación asigna todavía.")
M["05_Reserva_Estados"] = dict(
    clase="Reserva", atributo="estado", titulo="Reserva · estado (EstadoReserva)",
    estados={"•": (0, 0), "ACTIVA": (1, 0), "CONSUMIDA": (2, 0), "LIBERADA": (1, 1), "◉": (2, 1)},
    trans=[("•", "ACTIVA", "reservar", "pedido CONFIRMADO; stock apto disponible", ""),
           ("ACTIVA", "CONSUMIDA", "despachar", "entrega PREPARADA; despacho autorizado", "MovimientoStock DESPACHO"),
           ("ACTIVA", "LIBERADA", "liberar | bloquearLote | cancelar", "con motivo", "guardar motivoLiberacion"),
           ("CONSUMIDA", "◉", "", "", ""), ("LIBERADA", "◉", "", "", "")],
    nota="Solo se reserva stock físico de un lote APTO y no vencido, descontando las reservas ACTIVA. "
         "La salida física se descuenta una sola vez, al despachar.")
M["06_OrdenProduccion_Estados"] = dict(
    clase="OrdenProduccion", atributo="estado", titulo="OrdenProduccion · estado (EstadoOrdenProduccion)",
    estados={"•": (0, 0), "PLANIFICADA": (1, 0), "EN_PROCESO": (2, 0), "CONFIRMADA": (3, 0), "◉": (4, 0),
             "BLOQUEADA": (1.5, 1), "ANULADA": (1.5, 2), "◉2": (1.5, 3)},
    trans=[("•", "PLANIFICADA", "crear", "FAENEO: animal APTO", ""),
           ("PLANIFICADA", "EN_PROCESO", "iniciar", "", "registrar inicioReal"),
           ("EN_PROCESO", "CONFIRMADA", "confirmar", "resultados válidos", "crear Lotes y ResultadoProduccion; FAENEO: animal FAENADO"),
           ("PLANIFICADA", "BLOQUEADA", "sanidad | bloquearLote", "control rechazado o insumo bloqueado", ""),
           ("EN_PROCESO", "BLOQUEADA", "sanidad | bloquearLote", "control rechazado o insumo bloqueado", ""),
           ("PLANIFICADA", "ANULADA", "anular", "", ""),
           ("EN_PROCESO", "ANULADA", "anular", "", ""),
           ("BLOQUEADA", "ANULADA", "anular", "", ""),
           ("CONFIRMADA", "◉", "", "", ""), ("ANULADA", "◉2", "", "", "")],
    nota="tipo = FAENEO o FABRICACION (TipoOrdenProduccion). consumir registra InsumoProduccion solo en una orden FABRICACION EN_PROCESO. "
         "Una orden CONFIRMADA no se bloquea: se bloquean sus lotes.")
M["07_Animal_Estados"] = dict(
    clase="Animal", atributo="estado", titulo="Animal · estado (EstadoAnimal)",
    estados={"•": (0, 0), "PENDIENTE": (1, 0), "APTO": (2, 0), "FAENADO": (3, 0), "BLOQUEADO": (2, 1)},
    trans=[("•", "PENDIENTE", "animal", "alta", ""),
           ("PENDIENTE", "APTO", "sanidad", "resultado = APROBADO", "ControlSanitario"),
           ("APTO", "FAENADO", "confirmar (orden FAENEO)", "control vigente apto", ""),
           ("PENDIENTE", "BLOQUEADO", "sanidad", "resultado = RECHAZADO", "Incidencia; bloquear órdenes y lotes"),
           ("APTO", "BLOQUEADO", "sanidad", "resultado = RECHAZADO", "Incidencia; bloquear órdenes y lotes"),
           ("FAENADO", "BLOQUEADO", "sanidad", "resultado = RECHAZADO", "Incidencia; bloquear lotes derivados")],
    nota="Un animal BLOQUEADO o FAENADO no vuelve a APTO con un control aprobado. cambiarEstadoAnimal solo cambia activo (no el estado).")
M["08_Lote_Estados"] = dict(
    clase="Lote", atributo="estado", titulo="Lote · estado (EstadoLote)",
    estados={"•": (0, 0), "APTO": (1, 0), "BLOQUEADO": (2, 0)},
    trans=[("•", "APTO", "confirmar | loteExterno", "", "FabricaResultado / lote de compra"),
           ("APTO", "BLOQUEADO", "rechazarLote | bloquearLote", "con motivo", "Incidencia; liberar reservas; bloquear derivados")],
    nota="Un lote APTO solo se reserva o despacha mientras su vencimiento sea posterior a la fecha actual (loteApto).")
M["09_Incidencia_Estados"] = dict(
    clase="Incidencia", atributo="resuelta", titulo="Incidencia · resuelta (Boolean)",
    estados={"•": (0, 0), "ABIERTA (resuelta = false)": (1, 0)},
    trans=[("•", "ABIERTA (resuelta = false)", "sanidad | bloquearLote", "control rechazado o lote bloqueado", "guardar motivo y responsable")],
    nota="Incidencia no tiene enumeración de estado: usa resuelta, resolucion y resueltaEn. "
         "SGCPapi todavía no expone una operación para resolverla, por eso no hay transición a resuelta = true.")
M["10_Pago_Estados"] = dict(
    clase="Pago", atributo="anulado", titulo="Pago · anulado (Boolean)",
    estados={"•": (0, 0), "REGISTRADO (anulado = false)": (1, 0), "ANULADO (anulado = true)": (2, 0), "◉": (3, 0)},
    trans=[("•", "REGISTRADO (anulado = false)", "pago | sena", "", "AplicacionPago a cargos o Sena"),
           ("REGISTRADO (anulado = false)", "ANULADO (anulado = true)", "anularPago", "tipo = PAGO; con motivo", "guardar motivoAnulacion"),
           ("ANULADO (anulado = true)", "◉", "", "", "")],
    nota="Un pago de tipo SENA no se anula automáticamente: requiere resolverSena con acuerdo explícito.")
M["11_CondicionPago_Estados"] = dict(
    clase="CondicionPago", atributo="activa", titulo="CondicionPago · activa (Boolean)",
    estados={"•": (0, 0), "ACTIVA (activa = true)": (1, 0), "HISTÓRICA (activa = false)": (2, 0), "◉": (3, 0)},
    trans=[("•", "ACTIVA (activa = true)", "condicion", "pedido CONFIRMADO; crédito con importe y vencimiento", "pedido.condicionPago = modalidad"),
           ("ACTIVA (activa = true)", "HISTÓRICA (activa = false)", "condicion", "nueva condición del mismo pedido", "conservar la anterior"),
           ("HISTÓRICA (activa = false)", "◉", "", "", "")],
    nota="Un pedido tiene una sola CondicionPago activa. autorizarDespacho exige crédito vigente o saldo cero antes de despachar.",
    archivo_anterior="11_AcuerdoCredito_Estados")
M["12_SeguimientoCobro_Estados"] = dict(
    clase="SeguimientoCobro", atributo="estado", titulo="SeguimientoCobro · estado (EstadoSeguimiento) · pendiente en SGCPapi",
    estados={"•": (0, 0), "PENDIENTE": (1, 0), "REALIZADO": (2, 0), "CERRADO": (1, 1), "◉": (2, 1)},
    trans=[("•", "PENDIENTE", "programarGestion", "condición de crédito con saldo", "fijar proximaFecha"),
           ("PENDIENTE", "REALIZADO", "contactarCliente", "fecha de gestión alcanzada", "registrar resultado"),
           ("REALIZADO", "PENDIENTE", "reprogramar", "saldo > 0", "registrar próxima fecha"),
           ("PENDIENTE", "CERRADO", "verificarSaldo", "saldo = 0", ""),
           ("REALIZADO", "CERRADO", "verificarSaldo", "saldo = 0", ""),
           ("CERRADO", "◉", "", "", "")],
    nota="SeguimientoCobro todavía no existe en SGCPapi: se conserva porque Finanzas lo necesita para el seguimiento de cobros "
         "de cada CondicionPago a crédito. Las operaciones del diagrama son las que tendrá el servicio cuando se agregue a la API.")
M["13_Entrega_Estados"] = dict(
    clase="Entrega", atributo="estado", titulo="Entrega · estado (EstadoEntrega)",
    estados={"•": (0, 0), "PREPARADA": (1, 0), "DESPACHADA": (2, 0), "ENTREGADA": (3, 0),
             "CANCELADA": (1, 1), "OBSERVADA": (3, 1), "◉": (4, 0), "◉2": (4, 1), "◉3": (1, 2)},
    trans=[("•", "PREPARADA", "preparar", "pedido CONFIRMADO; reservas completas", ""),
           ("PREPARADA", "DESPACHADA", "despachar", "autorizarDespacho; transporte activo", "consumir reservas; Ruta EN_REPARTO"),
           ("DESPACHADA", "ENTREGADA", "sincronizar | revisar", "conforme; versión vigente", "registrar Recepcion"),
           ("DESPACHADA", "OBSERVADA", "sincronizar | revisar", "no conforme; con observación", "registrar Recepcion"),
           ("PREPARADA", "CANCELADA", "cancelar (pedido)", "", ""),
           ("ENTREGADA", "◉", "", "", ""), ("OBSERVADA", "◉2", "", "", ""), ("CANCELADA", "◉3", "", "", "")],
    nota="reasignar cambia responsable o ruta sin cambiar el estado, mientras no esté ENTREGADA, OBSERVADA ni CANCELADA. "
         "Cada cambio incrementa version, que Android usa para detectar conflictos.")
M["14_Ruta_Estados"] = dict(
    clase="Ruta", atributo="estado", titulo="Ruta · estado (EstadoRuta)",
    estados={"•": (0, 0), "PLANIFICADA": (1, 0), "EN_REPARTO": (2, 0), "FINALIZADA": (2, 1), "◉": (3, 1)},
    trans=[("•", "PLANIFICADA", "crearRuta", "transporte activo", ""),
           ("PLANIFICADA", "EN_REPARTO", "despachar", "primera entrega de la ruta", "registrar salidaReal"),
           ("EN_REPARTO", "FINALIZADA", "finalizarRuta", "entregas ENTREGADA, OBSERVADA o CANCELADA; sin conflictos", "registrar retornoReal"),
           ("PLANIFICADA", "FINALIZADA", "finalizarRuta", "todas sus entregas CANCELADA", "registrar retornoReal"),
           ("FINALIZADA", "◉", "", "", "")],
    nota="Solo se asignan entregas a una ruta PLANIFICADA del mismo responsable. Un transporte con ruta EN_REPARTO no se reasigna.")
M["15_ComprobanteFiscal_Estados"] = dict(
    clase="ComprobanteFiscal", atributo="estado", titulo="ComprobanteFiscal · estado (String)",
    estados={"•": (0, 0), "SIN_PROVEEDOR": (1, 0)},
    trans=[("•", "SIN_PROVEEDOR", "registrar", "pedido CONFIRMADO; sin comprobante previo", "ProveedorFiscalAdapter.Registrar")],
    nota="El estado es el texto que devuelve ProveedorFiscalAdapter. Mientras no se confirme el proveedor de facturación en línea, "
         "devuelve SIN_PROVEEDOR; un segundo registrar del mismo pedido devuelve el comprobante existente.")
M["16_Recepcion_Estados"] = dict(
    clase="Recepcion", atributo="estado", titulo="Recepcion · estado (EstadoRecepcion)",
    estados={"•": (0, 0), "◆": (1, 0), "CONFIRMADA": (2, 0), "CONFLICTO": (1, 1), "DESCARTADA": (2, 1), "◉": (3, 1)},
    trans=[("•", "◆", "sincronizar", "claveUnica nueva", "guardar evidencias"),
           ("◆", "CONFIRMADA", "", "versionBase vigente; entrega DESPACHADA", "aplicar a la Entrega"),
           ("◆", "CONFLICTO", "", "versión o estado cambiaron", "guardar motivoConflicto"),
           ("CONFLICTO", "CONFIRMADA", "revisar", "aplicar; entrega DESPACHADA sin recepción", "aplicar a la Entrega"),
           ("CONFLICTO", "DESCARTADA", "revisar", "no aplicar; con motivo", "guardar resolucion"),
           ("CONFIRMADA", "◉", "", "", ""), ("DESCARTADA", "◉", "", "", "")],
    nota="Android envía la recepción con claveUnica; si ya existe, la API devuelve la anterior sin duplicarla. "
         "Las capturas en CONFLICTO aparecen en Conflictos de recepción.",
    archivo_anterior="16_OperacionPendiente_Estados")
M["17_Usuario_Estados"] = dict(
    clase="Usuario", atributo="estado", titulo="Usuario · estado (EstadoUsuario)",
    estados={"•": (0, 0), "ACTIVO": (1, 0), "BLOQUEADO": (2, 0), "DESHABILITADO": (1, 1)},
    trans=[("•", "ACTIVO", "guardar | registrar", "", ""),
           ("ACTIVO", "BLOQUEADO", "acceder | estado", "intentosFallidos >= máximo, o gestión", "revocar sesiones"),
           ("BLOQUEADO", "ACTIVO", "estado(ACTIVO)", "actor de nivel superior", "intentosFallidos = 0"),
           ("ACTIVO", "DESHABILITADO", "estado(DESHABILITADO)", "queda un Superadministrador activo", "revocar sesiones"),
           ("DESHABILITADO", "ACTIVO", "estado(ACTIVO)", "actor de nivel superior", "intentosFallidos = 0"),
           ("BLOQUEADO", "DESHABILITADO", "estado(DESHABILITADO)", "actor de nivel superior", "revocar sesiones")],
    nota="Solo un usuario ACTIVO inicia sesión o recupera su acceso. PuedeGestionar exige un rol de nivel superior al del usuario gestionado.")
M["18_ResultadoProduccion_Estados"] = dict(
    clase="ResultadoProduccion", atributo="estado", titulo="ResultadoProduccion · estado (EstadoResultado)",
    estados={"•": (0, 0), "PENDIENTE_PESAJE": (1, 0), "CONFIRMADO": (2, 0), "BLOQUEADO": (1, 1)},
    trans=[("•", "PENDIENTE_PESAJE", "confirmar (orden)", "", "FabricaResultado.Crear"),
           ("PENDIENTE_PESAJE", "CONFIRMADO", "pesar", "lote apto; misma unidad; sin pesaje previo", "cantidadReal = neto"),
           ("PENDIENTE_PESAJE", "BLOQUEADO", "bloquearLote", "", ""),
           ("CONFIRMADO", "BLOQUEADO", "bloquearLote", "", "")],
    nota="El pesaje no mueve stock: la existencia física se crea con entrada (EntradaInventario).")

# ---------------------------------------------------------------- utilidades
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
        for v in o.values():
            if isinstance(v, dict) and set(v) == {"$ref"} and v["$ref"] in mapa: v["$ref"] = mapa[v["$ref"]]
    return c

plant = json.loads(subprocess.check_output(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "show", "HEAD:" + PLANTILLA]))
pid = {o["_id"]: o for o in todos(plant) if "_id" in o}
dg_pl = next(o for o in pid.values() if o.get("_type") == "UMLStatechartDiagram")
T = {}
for v in dg_pl["ownedViews"]:
    T.setdefault(v["_type"], v)
T_TEXTO = [v for v in dg_pl["ownedViews"] if v["_type"] == "UMLTextView"]
T_TITULO, T_NOTA = T_TEXTO[0], T_TEXTO[1]
T_TRANS = next(v for v in dg_pl["ownedViews"] if v["_type"] == "UMLTransitionView" and v["subViews"][0].get("text"))

clases_mdj = json.load(open(os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj"), encoding="utf-8"))
modelo_clases = clases_mdj["ownedElements"][0]

CW, CH, X0, Y0 = 620, 330, 90, 150
SW, SH = 330, 64          # caja de estado
F = fuente(14)
LINEA = 18

def caja_nodo(n, pos):
    col, fila = pos
    x, y = X0 + col * CW, Y0 + fila * CH
    if n == "•": return (x + SW - 30, y + SH / 2 - 15, 30, 30)
    if n.startswith("◆"): return (x + SW / 2 - 22, y + SH / 2 - 22, 44, 44)
    if n.startswith("◉"): return (x + SW / 2 - 17, y + SH / 2 - 17, 35, 35)
    return (x, y, SW, SH)

def construir(nombre, s):
    P = {"_type": "Project", "_id": nid(), "name": "SGCC — Estados de " + s["clase"], "documentVersion": 1}
    mod = copy.deepcopy(modelo_clases)
    # ids nuevos para todo el modelo copiado (cada archivo es independiente)
    mapa = {o["_id"]: nid() for o in todos(mod) if "_id" in o}
    for o in todos(mod):
        if "_id" in o: o["_id"] = mapa[o["_id"]]
        for v in o.values():
            if isinstance(v, dict) and set(v) == {"$ref"} and v["$ref"] in mapa: v["$ref"] = mapa[v["$ref"]]
    mod["_parent"] = ref(P["_id"]); mod["name"] = P["name"]
    mod["ownedElements"] = [o for o in mod["ownedElements"] if o["_type"] != "UMLClassDiagram"]
    P["ownedElements"] = [mod]
    clase = next(o for o in mod["ownedElements"] if o["_type"] == "UMLClass" and o["name"] == s["clase"])
    SM = {"_type": "UMLStateMachine", "_id": nid(), "_parent": ref(clase["_id"]), "name": f"{s['clase']}.{s['atributo']}",
          "documentation": s["nota"]}
    R = {"_type": "UMLRegion", "_id": nid(), "_parent": ref(SM["_id"]), "name": "Ciclo de vida", "vertices": [], "transitions": []}
    SM["regions"] = [R]
    D = {"_type": "UMLStatechartDiagram", "_id": nid(), "_parent": ref(SM["_id"]), "name": f"Estados · {s['clase']}.{s['atributo']}",
         "defaultDiagram": True, "ownedViews": []}
    SM["ownedElements"] = [D]
    clase.setdefault("ownedElements", []).append(SM)

    vistas, cajas = {}, {}
    for n, pos in s["estados"].items():
        x, y, w, h = caja_nodo(n, pos); cajas[n] = (x, y, w, h)
        if n == "•":
            e = {"_type": "UMLPseudostate", "_id": nid(), "_parent": ref(R["_id"]), "kind": "initial"}; tv = T["UMLPseudostateView"]
        elif n.startswith("◆"):
            e = {"_type": "UMLPseudostate", "_id": nid(), "_parent": ref(R["_id"]), "kind": "choice"}; tv = T["UMLPseudostateView"]
        elif n.startswith("◉"):
            e = {"_type": "UMLFinalState", "_id": nid(), "_parent": ref(R["_id"])}; tv = T["UMLFinalStateView"]
        else:
            e = {"_type": "UMLState", "_id": nid(), "_parent": ref(R["_id"]), "name": n}; tv = T["UMLStateView"]
        R["vertices"].append(e)
        v = clonar(tv); v.update(_parent=ref(D["_id"]), model=ref(e["_id"]), left=x, top=y, width=w, height=h)
        for sv in todos(v):
            if "model" in sv: sv["model"] = ref(e["_id"])
        if e["_type"] == "UMLState":
            nc = next(sv for sv in v["subViews"] if sv["_type"] == "UMLNameCompartmentView")
            nc.update(left=x, top=y, width=w, height=h)
            lab = next(sv for sv in nc["subViews"] if sv.get("text") and "(from" not in sv["text"])
            lab.update(text=n, left=x + 5, top=y + h / 2 - 9, width=w - 10, height=18, font="Arial;15;1")
            for sv in v["subViews"]:
                if sv["_type"] == "UMLDecompositionCompartmentView": sv.update(left=x, top=y + h, width=w, height=0)
        vistas[n] = (v, e)
        D["ownedViews"].append(v)

    # ---- rutas
    ocupados = []           # rectángulos de etiquetas ya puestas
    segmentos = []          # segmentos ya dibujados
    pares = {}
    def centro(n):
        x, y, w, h = cajas[n]; return x + w / 2, y + h / 2
    def cruza(pts, excl):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            for n, (x, y, w, h) in cajas.items():
                if n in excl: continue
                if max(x1, x2) > x - 4 and min(x1, x2) < x + w + 4 and max(y1, y2) > y - 4 and min(y1, y2) < y + h + 4:
                    return True
            for (a, b, c, d) in segmentos:
                if x1 == x2 == a == c and min(max(y1, y2), max(b, d)) - max(min(y1, y2), min(b, d)) > 2: return True
                if y1 == y2 == b == d and min(max(x1, x2), max(a, c)) - max(min(x1, x2), min(a, c)) > 2: return True
        return False
    def ruta(a, b, k):
        xa, ya, wa, ha = cajas[a]; xb, yb, wb, hb = cajas[b]
        ca, cb = centro(a), centro(b)
        off = (k % 3) * 14 - 14 if k else 0
        cands = []
        if abs(ca[1] - cb[1]) < 1:                                  # misma fila
            for dy in (off, off + 14, off - 14, off + 28, off - 28):
                y = ca[1] + dy
                cands.append([(xa + wa, y), (xb, y)] if xb > xa else [(xa, y), (xb + wb, y)])
            for d in (1, -1):
                for extra in (0, 14, 28, 42):
                    yy = (min(ya, yb) - 40 - extra) if d < 0 else (max(ya + ha, yb + hb) + 40 + extra)
                    for dx in (12, 30, 48):
                        sx, tx = ca[0] + (dx if xb > xa else -dx), cb[0] + (-dx if xb > xa else dx)
                        cands.append([(sx, ya if d < 0 else ya + ha), (sx, yy), (tx, yy), (tx, yb if d < 0 else yb + hb)])
        elif abs(ca[0] - cb[0]) < 1:                                # misma columna
            for dx in (off, off + 16, off - 16, off + 32, off - 32, 60, -60):
                x = ca[0] + dx
                cands.append([(x, ya + ha), (x, yb)] if yb > ya else [(x, ya), (x, yb + hb)])
            for d in (1, -1):
                for extra in (0, 14, 28):
                    xx = (max(xa + wa, xb + wb) + 50 + extra) if d > 0 else (min(xa, xb) - 50 - extra)
                    for dy in (14, -14, 22):
                        cands.append([(xa + wa if d > 0 else xa, ca[1] + dy), (xx, ca[1] + dy), (xx, cb[1] + dy), (xb + wb if d > 0 else xb, cb[1] + dy)])
        else:
            # horizontal desde A y luego vertical hasta B
            sx = xa + wa if cb[0] > ca[0] else xa
            ty = yb if cb[1] > ca[1] else yb + hb
            for dy in (0, 14, -14, 28):
                cands.append([(sx, ca[1] + dy), (cb[0] + off, ca[1] + dy), (cb[0] + off, ty)])
            # vertical desde A y luego horizontal hasta B
            sy = ya + ha if cb[1] > ca[1] else ya
            tx = xb if cb[0] > ca[0] else xb + wb
            for dx in (0, 14, -14, 28):
                cands.append([(ca[0] + dx, sy), (ca[0] + dx, cb[1] + off), (tx, cb[1] + off)])
            # por el pasillo entre filas
            yy = (ya + ha + yb) / 2 if cb[1] > ca[1] else (yb + hb + ya) / 2
            for dy in (0, 16, -16, 32):
                for dx in (0, 16, -16):
                    cands.append([(ca[0] + dx, sy), (ca[0] + dx, yy + dy), (cb[0] + dx, yy + dy), (cb[0] + dx, ty)])
        for c in cands:
            if not cruza(c, {a, b}):
                return c
        raise RuntimeError(f"{nombre}: sin ruta libre {a} -> {b}")

    def etiqueta(pts, texto):
        if not texto: return None
        tramos = sorted(zip(pts, pts[1:]), key=lambda t: -(abs(t[1][0] - t[0][0]) + abs(t[1][1] - t[0][1])))
        opciones = []
        for (p, q) in tramos:
            horizontal = abs(p[1] - q[1]) < 1
            largo = abs(q[0] - p[0]) if horizontal else abs(q[1] - p[1])
            ancho_t = max(150, min(300, largo - 30)) if horizontal else 260
            lineas = envolver(texto, ancho_t - 10, 14, 0)
            h = len(lineas) * LINEA + 4
            w = max(F.getlength(l) for l in lineas) + 12
            if horizontal:
                mx = (p[0] + q[0]) / 2
                for fr in (0.5, 0.35, 0.65):
                    mx = p[0] + (q[0] - p[0]) * fr
                    opciones.append((mx - w / 2, p[1] - h - 4, w, h))
                    opciones.append((mx - w / 2, p[1] + 6, w, h))
            else:
                for fr in (0.5, 0.3, 0.7):
                    my = p[1] + (q[1] - p[1]) * fr
                    opciones.append((p[0] + 8, my - h / 2, w, h))
                    opciones.append((p[0] - 8 - w, my - h / 2, w, h))
        def choca(r):
            x, y, w, h = r
            for n, (bx, by, bw, bh) in cajas.items():
                if x < bx + bw + 4 and x + w > bx - 4 and y < by + bh + 4 and y + h > by - 4: return True
            for (ox, oy, ow, oh) in ocupados:
                if x < ox + ow and x + w > ox and y < oy + oh and y + h > oy: return True
            for (a, b, c, d) in segmentos_todos:
                if min(a, c) < x + w and max(a, c) > x and min(b, d) < y + h and max(b, d) > y: return True
            return False
        for r in opciones:
            if not choca(r):
                ocupados.append(r); return r
        raise RuntimeError(f"{nombre}: sin lugar para la etiqueta '{texto}'")

    rutas = []
    for i, (a, b, ev, guarda, efecto) in enumerate(s["trans"]):
        k = pares.get(frozenset((a, b)), 0); pares[frozenset((a, b))] = k + 1
        pts = ruta(a, b, k)
        for p, q in zip(pts, pts[1:]): segmentos.append((p[0], p[1], q[0], q[1]))
        rutas.append(pts)
    segmentos_todos = list(segmentos)
    for (a, b, ev, guarda, efecto), pts in zip(s["trans"], rutas):
        texto = ev + (f" [{guarda}]" if guarda else "") + (f" / {efecto}" if efecto else "")
        texto = texto.strip()
        e = {"_type": "UMLTransition", "_id": nid(), "_parent": ref(R["_id"]),
             "source": ref(vistas[a][1]["_id"]), "target": ref(vistas[b][1]["_id"])}
        if guarda: e["guard"] = guarda
        if ev: e["triggers"] = [{"_type": "UMLEvent", "_id": nid(), "_parent": ref(e["_id"]), "name": ev, "kind": "signal"}]
        if efecto: e["effects"] = [{"_type": "UMLActivity", "_id": nid(), "_parent": ref(e["_id"]), "name": efecto}]
        R["transitions"].append(e)
        v = clonar(T_TRANS)
        v.update(_parent=ref(D["_id"]), model=ref(e["_id"]), tail=ref(vistas[a][0]["_id"]), head=ref(vistas[b][0]["_id"]),
                 points=";".join(f"{round(x)}:{round(y)}" for x, y in pts), lineStyle=0)
        for sv in v["subViews"]:
            sv["model"] = ref(e["_id"]); sv["hostEdge"] = ref(v["_id"])
        lab = v["subViews"][0]
        r = etiqueta(pts, texto)
        if r:
            lab.update(text=texto, left=round(r[0]), top=round(r[1]), width=round(r[2]), height=round(r[3]), font="Arial;14;0", wordWrap=True, visible=True)
        else:
            lab["visible"] = False; lab.pop("text", None)
        D["ownedViews"].append(v)

    # ---- textos
    ancho_total = max(x + w for x, y, w, h in cajas.values()) + 60
    alto_total = max([y + h for x, y, w, h in cajas.values()] + [r[1] + r[3] for r in ocupados]) + 40
    alto_total = max(alto_total, max(max(b, d) for a, b, c, d in segmentos) + 30)
    t = clonar(T_TITULO); t.update(_parent=ref(D["_id"]), left=X0, top=40, width=max(1400, ancho_total - X0), height=50, text=s["titulo"])
    lin = envolver(s["nota"], max(1400, ancho_total - X0) - 10, 17, 0)
    n = clonar(T_NOTA); n.update(_parent=ref(D["_id"]), left=X0, top=alto_total + 20, width=max(1400, ancho_total - X0),
                                 height=len(lin) * 22 + 10, text=s["nota"])
    D["ownedViews"][:0] = [t]; D["ownedViews"].append(n)

    # comprobación de referencias
    idsP = {o["_id"] for o in todos(P) if "_id" in o}
    malas = [o["$ref"] for o in todos(P) if isinstance(o, dict) and set(o) == {"$ref"} and o["$ref"] not in idsP]
    assert not malas, (nombre, malas[:3])
    return P

solo = sys.argv[2:]   # opcional: nombres a generar
for nombre, s in M.items():
    if solo and nombre not in solo: continue
    P = construir(nombre, s)
    destino = os.path.join(CARPETA, nombre + ".mdj")
    json.dump(P, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent="\t")
    if s.get("archivo_anterior"):
        viejo = os.path.join(CARPETA, s["archivo_anterior"] + ".mdj")
        if os.path.exists(viejo): os.remove(viejo)
    print("ok", nombre)
