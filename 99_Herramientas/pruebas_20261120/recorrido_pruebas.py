"""Genera el Word «Recorrido de pruebas del SGCP · Sprints 1 a 4» (APA 7).

Uso: python3 recorrido_pruebas.py <salida.docx>

Los resultados vienen de resultados_20261120.json, que guarda la salida real de:
- SGCPapi  `dotnet run --project tests/SGCP.Verificacion` contra MySQL 8.4 desechable (commit c7cb9ae);
- SGCPuiweb `dotnet run --project tests/SGCP.Web.Verificacion` (commit 4821c2a);
- SGCPuimovil `./gradlew testDebugUnitTest` (commit fe8cbd8).
El índice es un campo TOC real; sus números de página se calculan con LibreOffice (dos pasadas)
y quedan como resultado guardado del campo, así se ven sin actualizar y Word los puede recalcular.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "patrones_20261105" / ".deps" / "python"))
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

R = json.load(open(AQUI / "resultados_20261120.json", encoding="utf-8"))

# ---------------------------------------------------------------- comprobaciones por grupo
def grupo(linea):
    m = re.match(r"OK (P1|P2|PERFILES|WEB|MIGRACIÓN)? ?(\d+)? ?· (.*)", linea)
    g, n, t = m.group(1) or "S1", m.group(2), m.group(3)
    if n is None: g, n = ("MIG" if g == "MIGRACIÓN" else g, "M")
    return g, n, t
API = {}
for l in R["api"]:
    g, n, t = grupo(l)
    if g == "PERFILES" and n == "M": g = "MIGP"
    API[(g, n)] = t
WEB = {n: t for g, n, t in map(grupo, R["web"])}
cuenta = {g: sum(1 for k in API if k[0] == g) for g in ("S1", "PERFILES", "P1", "P2", "MIG", "MIGP")}
N_ANDROID = sum(len(c) for _, c in R["android"])
TOTAL = len(API) + len(WEB) + N_ANDROID
assert cuenta["S1"] == 27 and cuenta["PERFILES"] == 18 and cuenta["P1"] == 111 and cuenta["P2"] == 20, cuenta

def rango(*partes):
    out = []
    for p in partes:
        if isinstance(p, tuple): out += list(range(p[0], p[1] + 1))
        else: out.append(p)
    return out
SPRINT_P1 = {}
for n in rango((2, 28), (34, 37), 97, 103): SPRINT_P1[n] = "Sprint 2"
for n in rango((38, 43), (45, 63), 65, (92, 96), (98, 100), 102): SPRINT_P1[n] = "Sprint 3"
for n in rango(44, (64, 64), (66, 91), 101, (104, 106)): SPRINT_P1[n] = "Sprint 4"
for n in rango((29, 33), (107, 111)): SPRINT_P1[n] = "Después del Sprint 4 (v4.3.x)"
SPRINT_P1[1] = "Web III"
assert all(n in SPRINT_P1 for n in range(1, 112))

def ck(pref, nums):
    return ", ".join(f"{pref}{n}" for n in nums)

# ---------------------------------------------------------------- documento
doc = Document()
for name in ["Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "Header"]:
    st = doc.styles[name]; st.font.name = "Times New Roman"; st.font.size = Pt(12); st.font.color.rgb = RGBColor(0, 0, 0)
    st.font.bold = name in ["Title", "Heading 1", "Heading 2", "Heading 3"]; st.font.italic = name == "Heading 3"
    fonts = st.element.get_or_add_rPr().find(qn("w:rFonts"))
    if fonts is not None:
        for k in ["asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"]: fonts.attrib.pop(qn("w:" + k), None)
        for k in ["ascii", "hAnsi", "cs"]: fonts.set(qn("w:" + k), "Times New Roman")
    f = st.paragraph_format; f.space_before = f.space_after = Pt(0); f.line_spacing = 2; f.widow_control = True
    f.first_line_indent = Inches(0.5) if name == "Normal" else Inches(0)
    if name == "Heading 1": f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if name.startswith("Heading"): f.keep_with_next = True
lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "es-BO"); doc.styles["Normal"].element.get_or_add_rPr().append(lang)
s = doc.sections[0]
s.page_width, s.page_height = Inches(8.5), Inches(11)
s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)
s.different_first_page_header_footer = False
q = s.header.paragraphs[0]; q.alignment = WD_ALIGN_PARAGRAPH.RIGHT; q.paragraph_format.line_spacing = 1
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "1"; r.append(t); fld.append(r); q._p.append(fld)

def p(texto="", sangria=True, negrita=False, cursiva=False, centrado=False, interlineado=None):
    q = doc.add_paragraph(); q.paragraph_format.first_line_indent = Inches(0.5 if sangria else 0)
    if centrado: q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if interlineado: q.paragraph_format.line_spacing = interlineado
    # **negrita** y `código` dentro del texto
    for parte in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", texto):
        if not parte: continue
        if parte.startswith("**"): rr = q.add_run(parte[2:-2]); rr.bold = True
        elif parte.startswith("`"): rr = q.add_run(parte[1:-1]); rr.font.name = "Courier New"; rr.font.size = Pt(10.5)
        else: rr = q.add_run(parte); rr.bold = negrita
        rr.italic = cursiva or rr.italic
    return q
def salto():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
TITULOS = []
def h(texto, nivel=1):
    q = doc.add_heading(texto, nivel); TITULOS.append((nivel, texto)); return q
def vineta(texto):
    q = p(texto, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)
    q.runs[0].text = "• " + q.runs[0].text if q.runs else None
    return q
NT = 0
def tabla(titulo, cab, filas, anchos, tam=10, nota=None):
    global NT
    NT += 1
    a = p(f"Tabla {NT}", False, True); a.paragraph_format.keep_with_next = True
    b = p(titulo, False, cursiva=True); b.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(cab)); t.autofit = False; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes = OxmlElement("w:tblBorders")
    for e in ["top", "bottom", "left", "right", "insideH", "insideV"]:
        x = OxmlElement("w:" + e); x.set(qn("w:val"), "single" if e in ("top", "bottom") else "nil"); x.set(qn("w:sz"), "6"); bordes.append(x)
    t._tbl.tblPr.append(bordes)
    # anchos fijos: LibreOffice usa tblGrid, Word usa tcW; se fijan los dos
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); t._tbl.tblPr.append(lay)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(sum(anchos) * 1440))); tw.set(qn("w:type"), "dxa")
    for viejo in t._tbl.tblPr.findall(qn("w:tblW")): t._tbl.tblPr.remove(viejo)
    t._tbl.tblPr.append(tw)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), anchos): gc.set(qn("w:w"), str(int(w * 1440)))
    for ri, vals in enumerate([cab] + filas):
        row = t.rows[0] if ri == 0 else t.add_row()
        pr = row._tr.get_or_add_trPr(); pr.append(OxmlElement("w:cantSplit"))
        if ri == 0: pr.append(OxmlElement("w:tblHeader"))
        for ci, (c, txt) in enumerate(zip(row.cells, vals)):
            c.width = Inches(anchos[ci]); c.text = ""
            if ri == 0:
                bs = OxmlElement("w:tcBorders"); e = OxmlElement("w:bottom"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6"); bs.append(e); c._tc.get_or_add_tcPr().append(bs)
            q = c.paragraphs[0]; q.paragraph_format.first_line_indent = Inches(0); q.paragraph_format.line_spacing = 1
            q.paragraph_format.space_before = q.paragraph_format.space_after = Pt(2)
            for parte in re.split(r"(`[^`]+`)", str(txt)):
                if not parte: continue
                rr = q.add_run(parte.strip("`")); rr.font.size = Pt(tam); rr.bold = ri == 0
                if parte.startswith("`"): rr.font.name = "Courier New"; rr.font.size = Pt(tam - 1)
    if nota:
        q = p("", False); q.paragraph_format.line_spacing = 2; q.add_run("Nota. ").italic = True
        for parte in re.split(r"(`[^`]+`)", nota):
            if not parte: continue
            rr = q.add_run(parte.strip("`"))
            if parte.startswith("`"): rr.font.name = "Courier New"; rr.font.size = Pt(10.5)
    else:
        doc.add_paragraph().paragraph_format.line_spacing = 1
    return t

# ---------------------------------------------------------------- portada
q = p("Recorrido de pruebas del SGCP: Sprints 1 a 4", False, True, centrado=True, interlineado=1.15)
q.paragraph_format.space_before = Pt(24); q.paragraph_format.space_after = Pt(18); q.runs[0].font.size = Pt(18)
q = p("", False, centrado=True, interlineado=1); q.paragraph_format.space_after = Pt(24); q.add_run().add_picture(str(AQUI / "logo_univalle.png"), width=Inches(1.9))
for txt, neg in [("Integrantes:", True), ("Dario Haziel Tambo Parra", False), ("Angel Sebastian Eguez Mur", False), ("Sofia Cuellar Roca", False),
                 ("Victor Manuel Manrique Arancivia", False), ("", False), ("Materia:", True), ("Ingeniería de Software", False), ("", False),
                 ("Docente:", True), ("Rolando Lara Sánchez", False), ("", False), ("Universidad del Valle · Bolivia", False), ("", False),
                 ("Fecha:", True), ("20 de noviembre de 2026", False)]:
    p(txt, False, neg, centrado=True, interlineado=1.15)
salto()

# ---------------------------------------------------------------- índice (campo TOC con resultado guardado)
p("Índice", False, True, centrado=True)
indice_p = doc.add_paragraph()      # se reemplaza por el campo al final
salto()

# ---------------------------------------------------------------- 1
h("1. Propósito y alcance")
p("Este documento recorre, sprint por sprint, las pruebas del Sistema de Gestión Comercial Porcino (SGCP), el CRM de ventas de la chanchería. "
  "Para cada sprint se transcribe el criterio de validación del Sprint Backlog (`Formato Proyecto - SGCC Actualizado.xlsx`), se indica qué "
  "acción ejerce cada prueba, qué resultado se espera y qué resultado se obtuvo. Los números de comprobación remiten al Anexo A, que lista "
  f"las {TOTAL} comprobaciones con su nombre exacto.")
p("Todas las pruebas se volvieron a ejecutar el **20 de noviembre de 2026** sobre la rama `main` de los tres repositorios de código, ya con los "
  "cambios de la versión 4.3 (seguimiento de cobros, corrección de órdenes anuladas y resolución de incidencias). No se reutilizaron resultados "
  "anteriores: los del 11 de noviembre, registrados en `Validacion_Sprint1.md` a `Validacion_Sprint4.md`, se citan solo para comparar.")
p("El Sprint 5 es de reserva: el Backlog no le asigna requerimientos (Tambo Parra et al., 2026b). Por eso el recorrido termina en el Sprint 4, "
  "y lo que quedó pendiente se lista en la sección 8.")

# ---------------------------------------------------------------- 2
h("2. Entorno y método")
p("Se usaron los verificadores que cada repositorio ya trae. Ninguno se modificó para esta corrida. La API se probó contra un motor MySQL 8.4 "
  "propio y desechable, levantado en un contenedor en el puerto 3308 con una clave aleatoria que no se escribió en ningún archivo del proyecto; al "
  "terminar se eliminaron el contenedor y la clave. El verificador crea su propia base `sgcp_pruebas_<uuid>`, aplica la migración dos veces para "
  "comprobar que es idempotente, ejecuta las comprobaciones por HTTP y borra esa base al salir (Tambo Parra et al., 2026a).")
tabla("Entorno de cada suite de pruebas",
      ["Repositorio y commit", "Suite", "Motor o plataforma", "Comando"],
      [["SGCPapi `c7cb9ae`", "SGCP.Verificacion", "MySQL 8.4, base aislada, cultura `es-BO`", "`dotnet run --project tests/SGCP.Verificacion`"],
       ["SGCPuiweb `4821c2a`", "SGCP.Web.Verificacion", ".NET 10, sin servidor", "`dotnet run --project tests/SGCP.Web.Verificacion`"],
       ["SGCPuimovil `fe8cbd8`", "Pruebas unitarias JUnit", "JDK 21, SDK Android 36, Robolectric con Room real", "`./gradlew testDebugUnitTest`"],
       ["SGCPapi `c7cb9ae`", "Integración continua", "GitHub Actions: MySQL y SQL Server 2022", "`sprint1-mysql.yml`, `sqlserver.yml`"]],
      [1.35, 1.35, 1.9, 1.9], 9,
      "La variable `SGCP_MYSQL_TEST` indica la cadena de conexión de pruebas; sin ella, la API corre solo los Sprints 1 y perfiles sobre SQLite. "
      "La app Android se compiló en una copia temporal, porque el `local.properties` de la laptop apunta a una ruta del SDK que ya no existe.")
p("Cada comprobación de la API llama a un endpoint real con un usuario real del perfil que corresponde y compara el código HTTP, el cuerpo o el "
  "estado en la base. Si una sola falla, el verificador se detiene con el mensaje `FALLÓ: <nombre>`; por eso un recorrido completo significa que "
  "pasaron todas, en orden.")

# ---------------------------------------------------------------- 3
h("3. Resumen de resultados")
tabla("Resultado por suite el 20 de noviembre de 2026",
      ["Suite", "Qué cubre", "Comprobaciones", "Resultado"],
      [["API · Sprint 1", "Acceso, catálogo, cotización, pedido, margen, clientes", "27", "27 de 27"],
       ["API · Perfiles", "Roles jerárquicos, auditoría estratégica, documento único", "18", "18 de 18"],
       ["API · Sprints 2 a 4 (P1)", "Producción, inventario, cobranza, entregas, reportes, seguimiento de cobros", "111", "111 de 111"],
       ["API · Clientes REST (P2)", "201 con Location, 400, 404, 409, aislamiento del comprador", "20", "20 de 20"],
       ["API · Migraciones", "Migración aplicada dos veces sin perder datos", "2", "2 de 2"],
       ["Web", "Compatibilidad de reportes y permisos de gestión", str(len(WEB)), f"{len(WEB)} de {len(WEB)}"],
       ["Android", "Estados de envío, cola, Room, contrato y conexión", str(N_ANDROID), f"{N_ANDROID} de {N_ANDROID}"],
       ["Total", "", str(TOTAL), f"{TOTAL} de {TOTAL}"]],
      [1.7, 2.65, 1.25, 0.9], 10,
      "El 11 de noviembre la suite P1 tenía 89 comprobaciones; las 22 nuevas cubren constancias por pedido, conflictos para Ventas, "
      "seguimiento de cobros, incidencias y órdenes anuladas. En GitHub Actions, el commit `c7cb9ae` pasó en MySQL (ejecución 44675450553) "
      "y en SQL Server 2022 (ejecución 44675450695).")

# ---------------------------------------------------------------- 4 Sprint 1
h("4. Sprint 1: acceso, catálogo, cotizaciones y pedidos")
p("Requerimientos: RF-01 (solicitud, cotización y pedido), RF-02 (costos y precios vigentes), RF-03 (margen estimado), RF-10 (clientes), "
  "RF-12 (acceso autenticado) y RF-13 (usuarios y permisos). El criterio del Backlog dice: «Todos se autentican; alta pública solo comprador. "
  "Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar "
  "historial».")
tabla("Recorrido del Sprint 1",
      ["Paso", "Acción", "Resultado esperado", "Comprob.", "Obtenido"],
      [["1", "Pedir clientes sin token; entrar como administrador y como comprador; cerrar sesión", "401 sin token; después del cierre el token deja de servir", ck("S1-", [1, 27]), "Cumple"],
       ["2", "Pedir recuperación de acceso como anónimo y usar el token dos veces", "No se entrega el token al solicitante; el token sirve una sola vez y revoca sesiones", ck("S1-", [21, 22, 23]), "Cumple"],
       ["3", "Fallar cinco veces la clave de `ventas.prueba`; desactivar un usuario con sesión abierta", "La cuenta queda bloqueada (403); el JWT activo deja de valer", ck("S1-", [24, 25]), "Cumple"],
       ["4", "Registrar un comprador por el alta pública y pedir usuarios, cotizaciones ajenas y el catálogo", "403 en datos internos; no ve costo ni margen", ck("S1-", [15, 16, 17, 18]), "Cumple"],
       ["5", "Crear el producto `PRD-001`; cambiar su unidad con precios; desactivar una clasificación con productos", "Sin stock inicial; unidad protegida; `CLASIFICACION_EN_USO`", ck("S1-", [4, 5, 6]), "Cumple"],
       ["6", "Intentar crear pedido desde una cotización presentada, una rechazada y una aceptada vencida", "`COTIZACION_NO_ACEPTADA` y `COTIZACION_NO_VIGENTE`", ck("S1-", [7, 8, 20]), "Cumple"],
       ["7", "Aceptar la versión 2, confirmar el pedido de 4 kg a Bs 35 con costo Bs 28 y cambiar después el catálogo a Bs 40 y luego Bs 45", "Conserva el vínculo; precio 35; margen Bs 28 que no se recalcula; un solo pedido", ck("S1-", [9, 10, 11, 12, 13]), "Cumple"],
       ["8", "Cancelar un pedido con motivo; desactivar un cliente con pedido pendiente", "Motivo e historial conservados; `CLIENTE_CON_PEDIDOS`", ck("S1-", [19, 14]), "Cumple"],
       ["9", "Deshabilitar al último administrador o quitarle el rol; revisar auditoría", "Se rechaza; quedan más de 20 operaciones auditadas", ck("S1-", [2, 3, 26]), "Cumple"],
       ["10", "Aplicar la migración del Sprint 1 dos veces sobre un pedido existente", "Cargo 80,50 y margen 20,50 conservados", "MIG", "Cumple"]],
      [0.4, 2.15, 2.05, 0.95, 0.75], 9)

# ---------------------------------------------------------------- 5 Sprint 2
h("5. Sprint 2: producción, inventario y pesajes")
p("Requerimientos: RF-04 (catálogo, producción, inventario y pesajes), RF-17 (control de frío), RF-18 (control sanitario previo al faeneo), "
  "RF-20 (cargos de producto y de servicio), RNF-03 (confidencialidad) y RNF-06 (trazabilidad). El criterio dice: «Una orden produce costilla y "
  "lomo en lotes distintos. Confirmar peso no suma stock; entrada física sí. Rechazo bloquea; consumo de derivado rechazado no se revierte por "
  "ficción. No se reservan previsiones».")
tabla("Recorrido del Sprint 2",
      ["Paso", "Acción", "Resultado esperado", "Comprob.", "Obtenido"],
      [["1", "Con el perfil Producción y con Almacén, pedir precios, catálogo con precios y detalle comercial", "403 o datos sin importes; Almacén ve pedidos operativos sin precios", ck("P1-", [2, 3, 4, 5, 6]), "Cumple"],
       ["2", "Crear una orden de faeneo sin control sanitario, y otra omitiendo el resultado del control", "Se rechaza; omitir el resultado no aprueba por defecto", ck("P1-", [7, 8]), "Cumple"],
       ["3", "Registrar la previsión de la orden y confirmar costilla 8,000 kg y lomo 5,000 kg; confirmar otra vez", "La previsión no crea disponibilidad; dos lotes separados; no se confirma dos veces", ck("P1-", [9, 10, 11, 12]), "Cumple"],
       ["4", "Pesar bruto 13,000 kg y tara 0,500 kg; mirar existencias; confirmar la entrada física", "El pesaje no suma; la entrada suma 12,500 kg exactos", ck("P1-", [13, 14, 15, 16, 19, 20, 24, 25]), "Cumple"],
       ["5", "Repetir la entrada, repetir la referencia de consumo y anular una entrada válida y otra reservada", "Duplicados rechazados; la anulación revierte stock; la reservada no se anula", ck("P1-", [21, 22, 23, 35]), "Cumple"],
       ["6", "Cambiar la unidad de un producto con lotes; desactivar un producto con stock", "Ambas operaciones se rechazan", ck("P1-", [17, 18]), "Cumple"],
       ["7", "Rechazar en sanidad un animal y bloquear un lote ya consumido como insumo", "No devuelve el insumo consumido; el bloqueo pasa al derivado y a la producción", ck("P1-", [26, 27, 28]), "Cumple"],
       ["8", "Reservar contra una previsión sin existencia física", "`SIN_EXISTENCIA_DISPONIBLE`", ck("P1-", [34]), "Cumple"],
       ["9", "Generar cargos de producto con centavos y fracciones de kilo, y un servicio no prestado", "Precio acordado exacto; sin centavos extra; el servicio no prestado no genera cargo", ck("P1-", [36, 37, 97]), "Cumple"],
       ["10", "Contar en MySQL las entradas físicas después de un reintento", "Una sola fila", ck("P1-", [103]), "Cumple"]],
      [0.4, 2.15, 2.05, 0.95, 0.75], 9,
      "RF-17 (control de frío) no tiene una comprobación automática propia: es un registro manual con evaluación humana y se revisó en pantalla. "
      "RNF-06 se apoya en la auditoría que comprueban S1-26 y P1-105.")

# ---------------------------------------------------------------- 6 Sprint 3
h("6. Sprint 3: cobranza, transporte y entregas sin conexión")
p("Requerimientos: RF-05 (condición de pago), RF-06 (saldo por cliente y concepto), RF-07 (evidencia de entrega), RF-08 (transporte y rutas), "
  "RF-19 (seña), RNF-01 (recepción sin conexión en Android) y RNF-05 (compatibilidad de dispositivos). El criterio dice: «Captura pendiente hasta "
  "sincronizar. Conforme: ENTREGADA; con observaciones: OBSERVADA. El reintento no duplica datos y los conflictos requieren revisión. Entrega y "
  "deuda mantienen estados independientes».")
tabla("Recorrido del Sprint 3 en la API",
      ["Paso", "Acción", "Resultado esperado", "Comprob.", "Obtenido"],
      [["1", "Registrar una seña y aplicarla dos veces; cancelar un pedido con seña sin acuerdo y con acuerdo", "Se aplica una vez; la cancelación exige acuerdo y no inventa devolución", ck("P1-", [38, 98, 99, 100]), "Cumple"],
       ["2", "Consultar el saldo por concepto; despachar sin condición, al contado con deuda y a crédito sin vencimiento", "Saldo = cargos − pagos; los tres despachos se rechazan", ck("P1-", [39, 40, 41, 42]), "Cumple"],
       ["3", "Autorizar crédito y confirmar una entrega conforme", "El saldo sigue en Bs 60,25: ni el crédito ni la entrega cobran", ck("P1-", [43, 65]), "Cumple"],
       ["4", "Como repartidor, descargar entregas y consultar saldos, lotes y entregas ajenas", "Solo entregas propias autorizadas, sin importes ni saldos", ck("P1-", [45, 46, 47, 48, 57]), "Cumple"],
       ["5", "Sincronizar un lote con una recepción inválida y provocar un rollback", "Se rechaza el lote completo; nada queda a medias", ck("P1-", [49, 50]), "Cumple"],
       ["6", "Reenviar la misma recepción con la misma clave, también en paralelo; contar filas en MySQL", "Devuelve la recepción original; una sola fila", ck("P1-", [51, 55, 102]), "Cumple"],
       ["7", "Sincronizar una recepción conforme con peso real y evidencia", "ENTREGADA; peso y unidad conservados; evidencia visible sin saldo", ck("P1-", [52, 53, 58]), "Cumple"],
       ["8", "Sincronizar con una versión vieja de la entrega", "Queda en `CONFLICTO` y no pisa el estado del servidor", ck("P1-", [56, 59]), "Cumple"],
       ["9", "Como Ventas, revisar la bandeja de conflictos y resolver uno con la versión leída", "Ve versión y estado actuales; resuelve sin administrar entregas", ck("P1-", [60, 61, 62, 63]), "Cumple"],
       ["10", "Desactivar un transporte con ruta pendiente; cerrar rutas con recepciones sin sincronizar y con observación", "Se rechaza; la ruta con observación termina sin liquidar deuda", ck("P1-", [92, 93, 94, 95]), "Cumple"],
       ["11", "Leer de MySQL las fechas de captura y de sincronización", "Conservan el contrato UTC", ck("P1-", [96]), "Cumple"]],
      [0.4, 2.15, 2.05, 0.95, 0.75], 9)
p("En el teléfono, las 27 pruebas unitarias de SGCPuimovil ejercen la parte cliente de RNF-01: el estado de envío, la cola de recepciones y la "
  "base Room real con Robolectric. La Tabla 6 las agrupa.")
tabla("Pruebas unitarias de Android",
      ["Clase", "Pruebas", "Qué demuestran"],
      [["EstadoEnvioTest", "8", "Sin conexión vuelve a Pendiente; un conflicto no se reenvía solo; Confirmada y Descartada son terminales"],
       ["ColaRecepcionesTest", "8", "Tres capturas salen en orden; cortar después de que el servidor guardó no duplica; la sesión vencida detiene la cola sin perder nada"],
       ["BaseLocalTest", "2", "La captura sobrevive al cerrar y reabrir la app; descargar no borra entregas con captura"],
       ["ContratoYFormatoTest", "5", "Peso con tres decimales y punto; fecha de Bolivia enviada en UTC; «ya existe» cuenta como éxito"],
       ["ConexionTest", "4", "Rechaza credenciales en la URL y HTTP en producción; detecta el vencimiento de la sesión"]],
      [1.6, 0.7, 4.2], 10,
      "RNF-05 se comprobó a mano el 14 de noviembre de 2026 en un TECNO CK7n con Android 14: tres recepciones capturadas en modo avión y sin wifi "
      "sobrevivieron al cierre de la app y se enviaron solas, en orden, al volver la señal (Eguez Mur, 2026).")

# ---------------------------------------------------------------- 7 Sprint 4
h("7. Sprint 4: constancias, comprobante fiscal y reportes")
p("Requerimientos: RF-11 (comprobante fiscal, condicional), RF-14 (constancia de entrega) y RF-15 (reportes e historial). Los ocho casos C4-01 "
  "a C4-08 están definidos en `Criterios_Sprint4.md` (Cuellar Roca, 2026). La Tabla 7 los cruza con las comprobaciones que los ejecutan.")
tabla("Casos del Sprint 4",
      ["Caso", "Situación", "Resultado esperado", "Comprob.", "Obtenido"],
      [["C4-01", "Un comprador pide el reporte y el Excel de otro cliente", "403 en pantalla y en el archivo", ck("P1-", [86, 87]), "Cumple"],
       ["C4-02", "El comprador exporta sus pedidos", "El XLSX no trae costo ni margen en ninguna columna", ck("P1-", [88, 89, 90]), "Cumple"],
       ["C4-03", "Producción pide el reporte de pagos", "No disponible para ese perfil", ck("P1-", [85]), "Cumple"],
       ["C4-04", "Exportar el mismo filtro que se ve en pantalla", "Mismas filas y mismo aislamiento", ck("P1-", [83, 87, 91]), "Cumple"],
       ["C4-05", "Consultar el margen de un pedido después de cambiar el catálogo", "Margen histórico, no recalculado", ck("P1-", [84]), "Cumple"],
       ["C4-06", "Pedir la constancia con la recepción todavía en el teléfono", "`RECEPCION_PENDIENTE`", ck("P1-", [44]), "Cumple"],
       ["C4-07", "Pedir la constancia de una entrega OBSERVADA", "`RECEPCION_OBSERVADA`", ck("P1-", [64]), "Cumple"],
       ["C4-08", "Emitir dos veces el comprobante del mismo pedido", "Mismo registro y referencia, estado `SIN_PROVEEDOR`", ck("P1-", [75]), "Cumple"]],
      [0.6, 2.05, 1.95, 1.1, 0.8], 9)
tabla("Otras comprobaciones del Sprint 4",
      ["Tema", "Qué se comprobó", "Comprob.", "Obtenido"],
      [["Constancias", "PDF con evidencia; por pedido para Ventas y para el comprador sin conocer el id; 404 si no existe; el reparto no la obtiene; conserva el saldo de la confirmación", ck("P1-", [54, 66, 69, 70, 71, 72, 73, 74, 104]), "Cumple"],
       ["Reportes", "Los siete reportes ejecutan contra MySQL; filtro por tipo de corte; reporte de entregas sin GUID", ck("P1-", [67, 68, 76, 77, 78, 79, 80, 81, 82, 101]), "Cumple"],
       ["Rendimiento y auditoría", "2000 pedidos adicionales sin una consulta por fila; consultar registra acceso sin alterar pedidos", ck("P1-", [105, 106]), "Cumple"],
       ["Perfiles jerárquicos", "Último superadmin protegido; el Administrador no crea superadmins ni concede Finanzas; el Propietario consulta auditoría y los siete reportes", "PERF-1 a PERF-18", "Cumple"],
       ["Web", "El reporte muestra el documento y no el GUID; la constancia solo enlaza entregas confirmadas; el Administrador no gestiona al Propietario", "WEB-1 a WEB-8", "Cumple"]],
      [1.25, 3.0, 1.45, 0.8], 9,
      "RF-11 queda como punto de integración: el adaptador fiscal registra la operación sin proveedor y conserva la referencia única. No se emite "
      "factura porque no hay proveedor fiscal confirmado.")

# ---------------------------------------------------------------- 8 después
h("8. Pruebas agregadas después del Sprint 4")
p("Al alinear los diagramas con la API (19 de noviembre) aparecieron dos defectos y una clase del modelo que faltaba. Sofia Cuellar Roca los "
  "resolvió en SGCPapi v4.3.0 a v4.3.2, cada uno con sus pruebas. La entrega de Web III agregó, además, las pruebas de Clientes REST.")
tabla("Comprobaciones agregadas en noviembre",
      ["Versión", "Cambio", "Qué se comprobó", "Comprob."],
      [["v4.3.0", "Seguimiento de cobros para Finanzas", "Crear responde 201; con saldo la gestión vuelve a PENDIENTE; al pagar el total queda CERRADO; cerrado no admite otra gestión; no se abre sobre una condición de contado", ck("P1-", [107, 108, 109, 110, 111])],
       ["v4.3.1", "Una orden ANULADA ya no pasa a BLOQUEADA", "Rechazar en sanidad el animal de una orden anulada la deja ANULADA", ck("P1-", [33])],
       ["v4.3.2", "Resolver incidencias", "200 al resolver; 400 la segunda vez; 404 si no existe; resolver no rehabilita al animal", ck("P1-", [29, 30, 31, 32])],
       ["Web III", "Clientes REST y Swagger", "201 con Location; 400 sin campos obligatorios; 404; 409 `CLIENTE_CON_HISTORIAL`; el comprador solo ve sus pedidos", "P1-1, P2-1 a P2-20"]],
      [0.7, 1.6, 3.0, 1.2], 9)

# ---------------------------------------------------------------- 9 límites
h("9. Lo que las pruebas automáticas no cubren")
p("Pasar todas las comprobaciones no cierra todos los requerimientos. Estos quedan fuera, y se dicen para no dar por medido lo que no se midió:")
for x in ["**RNF-04, usabilidad.** La sesión con personal ajeno al equipo no se hizo; el guion de media hora está en `Usabilidad_RNF04_Sprint1.md`.",
          "**RNF-02, desempeño.** Hay una medición puntual (un reporte de 2007 pedidos respondió en 47 ms el 11 de noviembre) y la prueba P1-106 de "
          "consultas, pero no una prueba de carga con usuarios simultáneos.",
          "**RF-17, control de frío.** Es un registro manual; no tiene comprobación automática.",
          "**SQL Server.** Solo se verifica en GitHub Actions: la laptop del equipo no puede correrlo (procesador sin AVX y 3,6 GB de RAM).",
          "**Teléfono real.** El modo avión verdadero se probó a mano una vez (14 de noviembre); las pruebas unitarias no lo reemplazan.",
          "**RF-11.** Sin proveedor fiscal no hay factura que probar; solo el adaptador."]:
    q = p(x, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25); q.runs[0].text = "• " + q.runs[0].text

# ---------------------------------------------------------------- 10 defectos
h("10. Defectos que encontraron las pruebas")
tabla("Defectos encontrados y su corrección",
      ["Defecto", "Cómo apareció", "Corrección y prueba que lo cubre"],
      [["La API devolvía 500 en toda petición con decimales", "Con cultura `es-BO`, `RangeAttribute` no podía leer `\"0.01\"`", "Límites en cultura invariante (Sprint 1). La suite corre ahora en `es-BO`"],
       ["La web guardaba los importes multiplicados por cien", "El navegador manda punto decimal y el servidor esperaba coma", "Enlace de modelo en cultura invariante (Sprint 1)"],
       ["Una orden ANULADA pasaba a BLOQUEADA", "Al revisar la API contra el diagrama de estados", "v4.3.1; P1-33"],
       ["Una incidencia no se podía resolver", "El modelo tenía `resuelta`, pero ningún endpoint la cambiaba", "v4.3.2; P1-29 a P1-32"]],
      [1.9, 2.3, 2.3], 10,
      "Los dos primeros están detallados en `Errores_encontrados_Sprint1.md`: compilaban y pasaban sobre SQLite, y solo aparecieron con la "
      "cultura regional del equipo y el motor real (Tambo Parra et al., 2026a).")

# ---------------------------------------------------------------- 11 reproducir
h("11. Cómo repetir el recorrido")
p("Desde la raíz de cada repositorio, en `main`:")
for x in ["SGCPapi: levantar un MySQL desechable (`docker run -d --name sgcp_mysql_prueba -p 127.0.0.1:3307:3306 ... mysql:8.4`), darle al usuario "
          "de pruebas `GRANT ALL ON sgcp%.*`, definir `SGCP_MYSQL_TEST` y ejecutar `dotnet run --project tests/SGCP.Verificacion`. Debe terminar en "
          "`RESULTADO Clientes REST: 20 comprobaciones correctas.`",
          "SGCPuiweb: `dotnet run --project tests/SGCP.Web.Verificacion`. Debe terminar en `RESULTADO WEB: 8 comprobaciones de compatibilidad correctas.`",
          "SGCPuimovil: con `sdk.dir` apuntando al SDK de Android y el JDK 21, `./gradlew testDebugUnitTest --max-workers=1`. Los resultados quedan en "
          "`app/build/test-results/testDebugUnitTest/`."]:
    q = p(x, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25); q.runs[0].text = "• " + q.runs[0].text
p("El generador de este documento y la salida de la corrida están en `SGCPdocumentacion/99_Herramientas/pruebas_20261120/`.")

# ---------------------------------------------------------------- 12 conclusión
h("12. Conclusión")
p(f"Las {TOTAL} comprobaciones automáticas pasaron el 20 de noviembre de 2026 sobre el código de `main`, contra el motor real. Los cuatro criterios "
  "del Backlog se cumplen en la API, y la parte del teléfono que se puede automatizar también. Queda por medir lo que necesita personas o carga real "
  "(RNF-04 y RNF-02), que es justamente lo que el Sprint 5 tiene reservado.")

# ---------------------------------------------------------------- referencias
salto()
h("Referencias")
for antes, titulo, despues in [
    ("Cuellar Roca, S. (2026). ", "Criterios y validación del Sprint 4", " [Documento técnico no publicado]. Repositorio SGCPdocumentacion, Universidad del Valle."),
    ("Eguez Mur, A. S. (2026). ", "Prueba del APK en un teléfono real (RNF-05)", " [Documento técnico no publicado]. Repositorio SGCPdocumentacion, Universidad del Valle."),
    ("Pressman, R. S., & Maxim, B. R. (2020). ", "Software engineering: A practitioner’s approach", " (9th ed.). McGraw-Hill Education."),
    ("Sommerville, I. (2016). ", "Software engineering", " (10th ed.). Pearson."),
    ("Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026a). ", "Método de verificación del SGCP", " [Documento técnico no publicado]. Universidad del Valle."),
    ("Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026b). ", "Reparto del SGCP por sprint e integrante", " [Documento técnico no publicado]. Universidad del Valle.")]:
    q = p("", False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.5)
    q.add_run(antes); q.add_run(titulo).italic = True; q.add_run(despues)

# ---------------------------------------------------------------- anexo
salto()
h("Anexo A. Lista completa de comprobaciones")
p("Nombre exacto con que cada verificador imprimió la comprobación el 20 de noviembre de 2026. Todas terminaron en «OK».", True)
filas = [[f"S1-{n}", t, "Sprint 1"] for (g, n), t in API.items() if g == "S1"]
filas += [["MIG", API[("MIG", "M")], "Sprint 1"], ["MIG-P", API[("MIGP", "M")], "Sprint 4"]]
filas += [[f"PERF-{n}", t, "Sprint 4"] for (g, n), t in API.items() if g == "PERFILES"]
filas += [[f"P1-{n}", t, SPRINT_P1[int(n)]] for (g, n), t in API.items() if g == "P1"]
filas += [[f"P2-{n}", t, "Web III"] for (g, n), t in API.items() if g == "P2"]
filas += [[f"WEB-{n}", t, "Sprint 4"] for n, t in WEB.items()]
filas += [[f"AND-{c}", m, "Sprint 3"] for c, ms in R["android"] for m in ms]
tabla("Comprobaciones ejecutadas", ["Código", "Comprobación", "Sprint"], filas, [0.8, 4.5, 1.2], 9,
      "S1: Sprint 1 de la API; PERF: perfiles; P1: sprints 2 a 4 de la API; P2: Clientes REST; WEB: SGCPuiweb; AND: SGCPuimovil (clase JUnit).")

# ---------------------------------------------------------------- índice: campo TOC con resultado guardado
def campo_toc(paginas):
    def run_fld(tipo):
        r = OxmlElement("w:r"); f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), tipo); r.append(f); return r
    parrafos = []
    for i, (nivel, texto) in enumerate(TITULOS):
        pp = OxmlElement("w:p"); ppr = OxmlElement("w:pPr")
        tabs = OxmlElement("w:tabs"); tb = OxmlElement("w:tab"); tb.set(qn("w:val"), "right"); tb.set(qn("w:leader"), "dot"); tb.set(qn("w:pos"), "9350"); tabs.append(tb); ppr.append(tabs)
        sp = OxmlElement("w:spacing"); sp.set(qn("w:line"), "360"); sp.set(qn("w:lineRule"), "auto"); sp.set(qn("w:before"), "0"); sp.set(qn("w:after"), "0"); ppr.append(sp)
        ind = OxmlElement("w:ind"); ind.set(qn("w:left"), str(0 if nivel == 1 else 360)); ind.set(qn("w:firstLine"), "0"); ppr.append(ind)
        pp.append(ppr)
        if i == 0:
            pp.append(run_fld("begin"))
            r = OxmlElement("w:r"); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = ' TOC \\o "1-2" \\h \\z \\u '; r.append(it); pp.append(r)
            pp.append(run_fld("separate"))
        r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = texto; r.append(t); pp.append(r)
        r = OxmlElement("w:r"); r.append(OxmlElement("w:tab")); pp.append(r)
        r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = str(paginas.get(texto, "")); r.append(t); pp.append(r)
        if i == len(TITULOS) - 1: pp.append(run_fld("end"))
        parrafos.append(pp)
    return parrafos

def guardar(paginas, ruta):
    padre = indice_p._p.getparent(); pos = padre.index(indice_p._p)
    viejos = getattr(guardar, "previos", [])
    for v in viejos: padre.remove(v)
    nuevos = campo_toc(paginas)
    for k, pp in enumerate(nuevos): padre.insert(pos + 1 + k, pp)
    guardar.previos = nuevos
    doc.core_properties.title = "Recorrido de pruebas del SGCP: Sprints 1 a 4"
    doc.core_properties.author = "Dario Haziel Tambo Parra; Angel Sebastian Eguez Mur; Sofia Cuellar Roca; Victor Manuel Manrique Arancivia"
    doc.core_properties.language = "es-BO"
    doc.save(ruta)

def paginas_reales(ruta):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, ruta], check=True, capture_output=True)
        pdf = os.path.join(d, Path(ruta).stem + ".pdf")
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
        txt = [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]
    pags = {}
    for nivel, titulo in TITULOS:
        clave = re.sub(r"\s+", " ", titulo)
        for i in range(3, n + 1):        # desde la página 3: 1 es portada, 2 el índice
            if any(re.sub(r"\s+", " ", l).strip() == clave for l in txt[i - 1].splitlines()):
                pags[titulo] = i; break
    return pags, n

salida = os.path.abspath(sys.argv[1])
pags = {t: 0 for _, t in TITULOS}
for vuelta in range(3):
    guardar(pags, salida)
    nuevas, n = paginas_reales(salida)
    faltan = [t for _, t in TITULOS if t not in nuevas]
    assert not faltan, faltan
    if nuevas == pags: break
    pags = nuevas
print(salida, n, "páginas;", TOTAL, "comprobaciones;", len(TITULOS), "títulos en el índice")
