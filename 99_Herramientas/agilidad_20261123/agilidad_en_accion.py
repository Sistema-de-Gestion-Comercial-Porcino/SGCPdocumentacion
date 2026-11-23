"""Genera el Word «Agilidad en acción: los 12 principios aplicados al SGCP» (APA 7).

Uso: python3 agilidad_en_accion.py <salida.docx>

Resuelve la dinámica grupal de la Clase XXVIII (Unidad 5) con el proyecto real del grupo.
Los ayudantes de formato (estilos APA, tablas, campo TOC) son los de pruebas_20261120/recorrido_pruebas.py.
"""
import os, re, subprocess, sys, tempfile
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "patrones_20261105" / ".deps" / "python"))
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

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


TITULO_DOC = "Agilidad en acción: los 12 principios aplicados al SGCP"

def lista(items):
    for x in items:
        q = p(x, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)
        q.runs[0].text = "• " + q.runs[0].text

# ---------------------------------------------------------------- portada
q = p(TITULO_DOC, False, True, centrado=True, interlineado=1.15)
q.paragraph_format.space_before = Pt(24); q.paragraph_format.space_after = Pt(6); q.runs[0].font.size = Pt(18)
q = p("Dinámica grupal «Agilidad en acción: 12 principios, un solo equipo»", False, cursiva=True, centrado=True, interlineado=1.15)
q.paragraph_format.space_after = Pt(18)
q = p("", False, centrado=True, interlineado=1); q.paragraph_format.space_after = Pt(24); q.add_run().add_picture(str(AQUI / "logo_univalle.png"), width=Inches(1.9))
for txt, neg in [("Integrantes:", True), ("Dario Haziel Tambo Parra", False), ("Angel Sebastian Eguez Mur", False), ("Sofia Cuellar Roca", False),
                 ("Victor Manuel Manrique Arancivia", False), ("", False), ("Materia:", True), ("Ingeniería de Software", False), ("", False),
                 ("Docente:", True), ("Rolando Lara Sánchez", False), ("", False), ("Universidad del Valle · Bolivia", False), ("", False),
                 ("Fecha:", True), ("23 de noviembre de 2026", False)]:
    p(txt, False, neg, centrado=True, interlineado=1.15)
salto()

p("Índice", False, True, centrado=True)
indice_p = doc.add_paragraph()
salto()

# ---------------------------------------------------------------- 1
h("1. Introducción")
p("La dinámica propone un «Sistema de Gestión de Ventas» genérico que nunca termina. En lugar de ese caso usamos el proyecto real del "
  "grupo: el **Sistema de Gestión Comercial Porcino (SGCP)**, el CRM de ventas de una chanchería de Santa Cruz de la Sierra que compra "
  "canales, las desposta en cortes y las vende a carnicerías, chicharronerías, restaurantes y consumidores finales. El sistema tiene una "
  "API en ASP.NET Core 10 con MySQL, una web MVC y una aplicación Android en Kotlin, y lo construimos en sprints desde noviembre de 2026.")
p("Usar nuestro propio proyecto tiene una ventaja: los problemas de la situación planteada no son hipotéticos. Varios nos pasaron, y otros "
  "los evitamos justamente por aplicar alguno de los principios. Cada ejemplo de este documento remite a algo que se puede comprobar en los "
  "repositorios del proyecto (Tambo Parra et al., 2026).")
tabla("Correspondencia entre el pedido inicial del caso y los módulos del SGCP",
      ["Pedido del caso", "Equivalente en el SGCP", "Caso de uso"],
      [["Registro de productos", "Catálogo de cortes y derivados, productos con unidad y estado", "CU07 Gestionar productos"],
       ["Control de inventario", "Lotes por orden de producción, pesajes, entradas físicas y reservas", "CU08 y CU09"],
       ["Registro de ventas", "Solicitud del comprador, cotización con vigencia y pedido confirmado con su margen", "CU05 y CU06"],
       ["Gestión de clientes", "Carnicerías, chicharronerías, restaurantes y consumidores, con su condición de pago", "CU03 Gestionar clientes"],
       ["Reportes de ventas", "Reportes por perfil con filtros y exportación a PDF y Excel", "CU12 Gestionar reportes"],
       ["Control de usuarios", "Acceso con sesión revocable, seis perfiles y permisos por rol", "CU01 y CU02"]],
      [1.6, 3.4, 1.5], 10)

# ---------------------------------------------------------------- 2
h("2. La situación problemática vista desde el SGCP")
p("La dinámica describe seis problemas de un equipo que trabaja con un plan tradicional. Antes de aplicar los principios revisamos, con "
  "honestidad, cuáles de esos problemas aparecieron en nuestro proyecto y cuáles no.")
tabla("Los seis problemas del caso contrastados con lo que pasó en el SGCP",
      ["Problema del caso", "¿Ocurrió en el SGCP?", "Qué pasó realmente"],
      [["1. El cliente cambia constantemente sus necesidades", "Sí",
        "El 7 de octubre cambió el tema del proyecto, de incidencias urbanas a la chanchería. El 6 de noviembre se autorizó cambiar SQL Server "
        "por MySQL, y en la tarea de Web III se pidió volver a soportar SQL Server como segundo motor."],
       ["2. Los desarrolladores no se comunican con el cliente", "En riesgo",
        "El cliente real es el propietario de la chanchería y no participa todos los días. La Product Owner lo representa, y RF-16 y RF-17 "
        "quedaron pendientes hasta confirmarlos con una chanchería real."],
       ["3. Dos meses sin versión funcional", "No",
        "El Sprint 1 se entregó el 6 de noviembre funcionando: login, clientes, costos, cotización y pedido, con 27 comprobaciones "
        "automáticas contra MySQL."],
       ["4. El gerente exige resultados inmediatos", "Sí",
        "La entrega de Web III cerraba el 20 de noviembre a las 07:00, en medio del Sprint 4."],
       ["5. Dificultad para coordinarse", "Parcial",
        "Se resolvió con un reparto fijo por parte (P1 a P4) y ramas con pull request, pero con el apuro del plazo algunos cambios se "
        "fusionaron sin la revisión de otro integrante."],
       ["6. Errores descubiertos casi al final", "Sí, dos casos",
        "Con la cultura regional `es-BO` la API respondía error 500 a cualquier decimal; apareció recién al probar con el motor real. "
        "Y una orden ANULADA podía pasar a BLOQUEADA; se detectó al comparar la API con el diagrama de estados."]],
      [1.7, 1.0, 3.8], 9.5)
p("La conclusión de este contraste guía el resto del documento: el SGCP no es un proyecto que nunca termina, porque desde el primer "
  "sprint hubo software funcionando. Sus riesgos están en los cambios de requisitos, la presión de los plazos y la revisión entre pares.")

# ---------------------------------------------------------------- 3
h("3. Fase 1. Los 12 principios con ejemplos del SGCP")
p("Cada integrante explicó tres principios con sus propias palabras. Los repartimos según el rol de cada uno en el proyecto: la Product "
  "Owner tomó los que hablan del cliente, el Scrum Master los del equipo, y los dos desarrolladores los de entrega y calidad técnica. "
  "Así cada uno habla de lo que vive en su propia parte del trabajo.")
tabla("Reparto de los principios entre los integrantes",
      ["Integrante", "Rol en el SGCP", "Principios", "Bloque"],
      [["Sofia Cuellar Roca", "Product Owner", "1, 2 y 4", "A · Cliente y entregas"],
       ["Victor Manuel Manrique Arancivia", "Scrum Master", "5, 6 y 8", "B · Equipo y comunicación"],
       ["Angel Sebastian Eguez Mur", "Desarrollador web y Android", "3, 7 y 10", "A, B y C"],
       ["Dario Haziel Tambo Parra", "Desarrollador de la API", "9, 11 y 12", "C · Calidad y mejora continua"]],
      [2.2, 1.8, 1.0, 1.5], 10)

FILAS_P = [
 ("1", "Sofía", "Lo más importante es que el cliente reciba pronto algo que le sirva, y que lo siga recibiendo.",
  "El primer sprint ya resolvía la causa raíz del caso: que el precio se acuerde de memoria. Desde el Sprint 1 la cotización guarda el "
  "costo vigente y calcula el margen del pedido."),
 ("2", "Sofía", "Un cambio tardío no es un fracaso del plan: puede ser lo que le da ventaja al cliente.",
  "El comprador pidió poder armar su propia solicitud desde el portal. Entró como avance de CU05 después de cerrar el Sprint 4, sin rehacer "
  "lo que ya funcionaba: Ventas sigue preparando el precio y confirmando el pedido."),
 ("4", "Sofía", "Quien conoce el negocio y quien programa deben trabajar juntos todo el proyecto, no solo al inicio.",
  "La condición de diseño del caso salió del negocio: si cargar un pedido toma más que anotarlo en el cuaderno, el sistema no se usa. Cada "
  "pantalla se revisa contra esa frase."),
 ("5", "Victor", "Si se confía en gente motivada y se le dan las herramientas, hace bien el trabajo.",
  "Cada integrante tiene su terreno fijo (P1 API, P2 web y Android, P3 validación, P4 planificación y pruebas) y una guía con lo que necesita. "
  "Nadie espera que otro le diga qué hacer cada día."),
 ("6", "Victor", "Lo que se puede decir hablando no debería esperar a un documento.",
  "Las dudas de un sprint se resuelven conversando en el grupo y en clase; los documentos de reparto quedan para lo que hay que recordar, "
  "como el orden de las partes y los criterios de aceptación."),
 ("8", "Victor", "El ritmo tiene que poder mantenerse; trabajar de noche para llegar es una señal de mala planificación.",
  "La semana de la entrega de Web III mostró lo contrario: mucho trabajo concentrado en pocos días. Por eso se fijó un plazo interno, el "
  "miércoles a las 24:00, antes de la entrega real del jueves."),
 ("3", "Sebastián", "Hay que entregar software que funcione cada pocas semanas, no todo al final.",
  "Cada sprint cierra con una versión etiquetada que se puede ejecutar (`v1.0.0`, `vN.4.0`). La app Android ya instalaba en un teléfono real "
  "(TECNO CK7n con Android 14) antes de terminar el proyecto."),
 ("7", "Sebastián", "El avance se mide por lo que funciona, no por los documentos que se escribieron.",
  "El avance del SGCP se comprueba con sus verificadores: 209 comprobaciones de la API pasan en MySQL y en SQL Server. Un caso de uso sin "
  "comprobaciones no se cuenta como terminado."),
 ("10", "Sebastián", "Lo más simple que resuelve el problema es lo mejor; lo que no se necesita, no se construye.",
  "Las pantallas del Sprint 1 conservaron la disposición del mockup, pero solo con los datos que ya existían; lo de módulos posteriores lleva "
  "el aviso «Disponible en el siguiente sprint». RF-09 y RF-16 quedaron fuera porque el cliente no los necesita aún."),
 ("9", "Dario", "Cuidar la calidad técnica desde el inicio hace que cambiar después sea barato.",
  "Cuando se pidió SQL Server como segundo motor, bastó agregar otro contexto de datos y su migración: el diseño ya separaba la base de las "
  "reglas del negocio. Las pruebas automáticas confirmaron que nada se rompió."),
 ("11", "Dario", "Las mejores decisiones de diseño salen del equipo que hace el trabajo, no se imponen desde afuera.",
  "Los siete patrones de diseño los eligió el equipo según dónde servían de verdad: por ejemplo, Builder para armar un pedido pieza por pieza "
  "con su precio y su costo congelados."),
 ("12", "Dario", "Cada cierto tiempo hay que mirar cómo trabajamos y corregirlo.",
  "Después del Sprint 1 se escribió `Errores_encontrados_Sprint1.md` con la causa de cada defecto. Desde entonces, todas las pruebas se corren "
  "también con la cultura `es-BO`, que fue la que causó los errores."),
]
tabla("Los 12 principios explicados con ejemplos del SGCP",
      ["N.º", "Quién", "Con nuestras palabras", "Ejemplo en el SGCP"],
      [[n, quien, palabras, ej] for n, quien, palabras, ej in sorted(FILAS_P, key=lambda f: int(f[0]))],
      [0.4, 0.8, 2.0, 3.3], 9.5,
      "Los principios se citan según la traducción del Manifiesto Ágil que presenta Pressman (2010).")

# ---------------------------------------------------------------- 4
h("4. Fase 2. Matriz de análisis")
p("Las cuatro situaciones de la dinámica se resolvieron con lo que nos pasó en el SGCP. Para cada una se indica cómo se presentó en el "
  "proyecto, qué principios la resuelven y qué decidimos hacer.")
tabla("Matriz de análisis de las cuatro situaciones",
      ["Situación", "Cómo se presentó en el SGCP", "Principios", "Solución propuesta"],
      [["El cliente pide una funcionalidad nueva con el sistema avanzado",
        "El portal del comprador debía permitirle armar su propia solicitud de cotización, con el Sprint 4 ya cerrado.",
        "2, 1 y 10",
        "Se analizó qué parte del flujo cambiaba y se agregó solo esa (solicitud y modificación propias). Lo que ya funcionaba, que Ventas prepare "
        "el precio y confirme el pedido, no se tocó. Las mejoras restantes quedaron en el backlog para otro incremento."],
       ["Un mes de trabajo y nada funcional que mostrar",
        "No ocurrió: se evitó entregando el Sprint 1 completo y funcionando antes de empezar el Sprint 2.",
        "3 y 7",
        "Cada sprint termina en una versión ejecutable y en un recorrido demostrable: acceso, cliente, costo, cotización, aceptación y pedido. El "
        "avance se demuestra corriendo el sistema, no con un informe."],
       ["Los desarrolladores no se ponen de acuerdo y trabajan aislados",
        "La web y Android dependen de los endpoints de la API; si cada uno avanza por su lado, las pantallas consumen contratos que no existen.",
        "4, 6 y 11",
        "Orden fijo dentro del sprint: P1 publica el contrato en Swagger, P2 arranca sobre ese contrato y P3 y P4 abren y cierran el sprint. "
        "Todo cambio entra por pull request revisado por otro integrante."],
       ["El equipo trabaja horas extras y los errores aumentan",
        "La semana de la entrega de Web III. Con el apuro, algunos pull request se fusionaron sin revisión.",
        "8, 12 y 9",
        "Plazo interno un día antes de la entrega real, nada de trabajo nuevo la última noche y revisión obligatoria aunque haya prisa. Tras la "
        "entrega se volvió a correr la suite completa para confirmar que nada se rompió."]],
      [1.3, 1.8, 0.9, 2.5], 9.5)

# ---------------------------------------------------------------- 5
h("5. Fase 3. Simulación: construye, entrega y adapta")
h("5.1 Roles del equipo", 2)
p("Usamos los mismos roles que ya tenemos en el proyecto. La dinámica pide un QA aparte; como somos cuatro, el control de calidad lo "
  "comparten la Product Owner, que valida contra los criterios de aceptación, y el Scrum Master, que ejecuta las pruebas al cierre.")
tabla("Roles de la simulación",
      ["Rol", "Integrante", "Responsabilidad en la simulación"],
      [["Product Owner", "Sofia Cuellar Roca", "Representa al propietario de la chanchería, ordena el backlog y acepta o rechaza lo entregado"],
       ["Scrum Master", "Victor Manuel Manrique Arancivia", "Facilita la planificación, cuida el ritmo, ejecuta las pruebas de cierre y etiqueta la versión"],
       ["Desarrollador", "Dario Haziel Tambo Parra", "API: modelo de datos, reglas del negocio y endpoints"],
       ["Desarrollador", "Angel Sebastian Eguez Mur", "Pantallas web y aplicación Android"],
       ["QA", "Sofía y Victor", "Criterios de aceptación y guion de prueba (Sofía); ejecución de los verificadores automáticos (Victor)"]],
      [1.2, 2.1, 3.2], 10)

h("5.2 Sprint 1 simulado: primera entrega", 2)
p("La Product Owner eligió las tres funcionalidades que dan valor de inmediato al propietario: saber qué vende, a cuánto lo vende y qué "
  "tiene disponible. Para cada una se definió cómo se demuestra que funciona, porque sin esa demostración no se considera entregada.")
tabla("Funcionalidades del Sprint 1 simulado",
      ["Funcionalidad", "Historia de usuario", "Criterio de aceptación", "Cómo lo demostramos"],
      [["Registrar productos",
        "Como propietario quiero registrar mis cortes y derivados para venderlos con su unidad y su precio",
        "Un producto nuevo se crea sin stock inicial; el stock solo entra por una entrada física",
        "Crear «Costilla» por kg y mostrar que su stock es cero hasta registrar una entrada"],
       ["Registrar ventas",
        "Como vendedor quiero convertir una cotización aceptada en pedido sin volver a cargar los datos",
        "Una cotización rechazada o vencida no crea pedido; el pedido conserva el precio y el costo acordados",
        "Recorrido en vivo: cotización, aceptación, pedido y margen calculado; luego intentar confirmar una rechazada"],
       ["Consultar inventario",
        "Como encargado de almacén quiero ver el stock disponible por producto y lote",
        "Lo reservado para un pedido no aparece como disponible; una previsión no se puede reservar",
        "Reservar 10 kg para un pedido y mostrar que el disponible baja"]],
      [1.1, 1.8, 1.8, 1.8], 9.5,
      "En el proyecto real el inventario entró en el Sprint 2, porque primero había que modelar la producción por lotes. En la simulación "
      "lo adelantamos porque así lo pide la dinámica.")

h("5.3 Sprint 2 simulado: el cambio inesperado", 2)
p("Llega la solicitud urgente: registrar ventas mediante códigos QR y consultar las ventas desde el celular. Siguiendo el principio 2 no la "
  "rechazamos, pero tampoco la metemos entera sin analizarla.")
p("**Análisis del cambio.** El SGCP ya tiene una aplicación Android con acceso autenticado y una API que cualquier cliente puede consultar, "
  "así que buena parte del trabajo ya está hecha. Hoy la app sirve para las entregas, no para las ventas, y no usa la cámara para códigos.", False)
tabla("Impacto del cambio sobre lo que ya existe",
      ["Parte del cambio", "Qué ya existe en el SGCP", "Qué falta construir", "Esfuerzo"],
      [["Consultar ventas desde el celular", "API de pedidos con permisos por perfil; app Android con sesión segura",
        "Una pantalla de solo lectura con los pedidos del día y su estado", "Bajo"],
       ["Generar el QR del pedido", "Cada pedido ya tiene un código único", "Imprimir o mostrar ese código como QR en la web", "Bajo"],
       ["Registrar la venta escaneando el QR", "Captura sin conexión con cola de envío (Sprint 3)",
        "Lectura con la cámara, validación del producto y del precio vigente, y qué pasa si no hay señal", "Alto"]],
      [1.6, 1.9, 2.1, 0.9], 9.5)
p("**Revisión de prioridades y decisión.** Primero se desarrolla la consulta de ventas desde el celular y la generación del QR, porque dan "
  "valor en pocos días y reutilizan lo que ya existe. El registro de ventas por escaneo va después, porque es el único punto que toca dinero "
  "sin conexión y exige el mismo cuidado que tuvo la sincronización del Sprint 3: el reintento no debe duplicar una venta.")
p("**Efecto en lo planificado.** Para no alargar el sprint ni recargar al equipo (principio 8), la Product Owner saca del Sprint 2 lo de "
  "menor valor inmediato: el reporte exportable a Excel pasa al sprint siguiente. Nada de lo ya entregado se rehace.")
p("**Cómo entregamos valor.** Al cierre del sprint el propietario puede revisar desde su celular lo vendido en el día, que es lo que hoy "
  "solo sabe preguntando o revisando el cuaderno. El escaneo se demuestra en el sprint siguiente con una prueba de conexión cortada.")

# ---------------------------------------------------------------- 6
h("6. Fase 4. El tribunal ágil")
TRIB = [
 ("¿Por qué entregar software funcional es más importante que presentar muchos documentos?",
  "Porque el software funcionando es lo único que el cliente puede usar y lo único que demuestra que el problema está resuelto. En el SGCP "
  "los diagramas llegaron a describir estados que la API no permitía, como resolver una incidencia, y solo se notó al contrastarlos con el "
  "sistema real. Los documentos siguen siendo útiles, pero acompañan al software: no lo reemplazan."),
 ("¿Aceptar cambios significa que el proyecto no necesita planificación?",
  "No. Sin un plan no se puede saber qué cuesta un cambio ni qué se deja de hacer para incorporarlo. El SGCP tiene cinco sprints planificados "
  "y uno de ellos, el 5, es justamente de reserva para absorber lo que cambie. Planificar sirve para poder cambiar con orden."),
 ("¿Qué diferencia existe entre trabajar muchas horas y mantener un ritmo sostenible?",
  "Trabajar muchas horas produce más código esa semana y más errores la siguiente. El ritmo sostenible es el que el equipo puede repetir "
  "sprint tras sprint sin que baje la calidad. En la semana de la entrega de Web III se vio: con prisa se saltaron revisiones."),
 ("¿Por qué la autoorganización no significa trabajar sin responsabilidades?",
  "Porque el equipo decide cómo hacer el trabajo, pero cada parte tiene un responsable con nombre. En el SGCP el código `S3-P2` dice de "
  "inmediato que es la parte de Sebastián en el Sprint 3. Organizarse solos exige más compromiso, no menos."),
 ("¿Cómo puede un equipo saber si está mejorando?",
  "Midiendo y comparando. Los verificadores del SGCP pasaron de 27 comprobaciones en el Sprint 1 a 209 en la API, y cada defecto encontrado "
  "se registró con su causa para que no se repita. También cuenta cuántos defectos aparecen al final: si cada vez son menos, el equipo mejora."),
 ("¿Por qué es importante entregar valor al cliente desde las primeras etapas?",
  "Porque el cliente confirma pronto si vamos bien y el equipo corrige cuando todavía es barato. En la chanchería el riesgo es de adopción: "
  "si el primer contacto con el sistema es lento, el propietario vuelve al cuaderno. Entregar temprano permite medir eso a tiempo."),
]
for i, (preg, resp) in enumerate(TRIB, 1):
    p(f"**{i}. {preg}**", False)
    p(resp)

# ---------------------------------------------------------------- 7
h("7. Fase 5. Reflexión individual")
p("Cada integrante respondió las tres preguntas de la fase. Las respuestas son personales y reflejan la parte del proyecto que le tocó a cada uno.")
tabla("Reflexión de cada integrante",
      ["Integrante", "Principio más importante", "Más difícil en un equipo universitario", "Lo aplicaría de inmediato"],
      [["Sofia Cuellar Roca", "1: sin valor para el cliente, lo demás no importa",
        "4: el cliente real no está disponible todos los días", "4: validar cada sprint con una chanchería real"],
       ["Victor Manuel Manrique Arancivia", "6: la conversación evita malentendidos que un documento no ve",
        "8: las entregas de varias materias coinciden en la misma semana", "8: plazos internos antes de cada entrega"],
       ["Angel Sebastian Eguez Mur", "7: lo que no funciona no cuenta como avance",
        "3: entregar seguido cuando se depende de la API de otro", "10: construir solo lo que se va a usar"],
       ["Dario Haziel Tambo Parra", "9: la calidad técnica hace que el cambio sea barato",
        "12: detenerse a revisar cuando el plazo aprieta", "12: una retrospectiva corta al cierre de cada sprint"]],
      [1.6, 1.7, 1.6, 1.6], 9.5)

# ---------------------------------------------------------------- 8
h("8. Factores humanos del equipo ágil")
p("La clase XXVIII presenta los factores humanos que un equipo ágil debe compartir (Cockburn y Highsmith, 2001). Los contrastamos con el "
  "equipo del SGCP para reconocer en qué estamos bien y qué nos falta.")
tabla("Factores humanos en el equipo del SGCP",
      ["Factor", "Cómo se ve en el equipo", "Qué mejorar"],
      [["Competencia", "Cada parte la toma quien conoce su tecnología: API, web y Android", "Que más de uno sepa levantar cada parte"],
       ["Enfoque común", "Todos trabajan sobre el mismo backlog y los mismos criterios de aceptación", "Repasar la meta del sprint al empezarlo"],
       ["Colaboración", "La web y Android se construyen sobre el contrato publicado por la API", "Avisar antes de cambiar un contrato"],
       ["Habilidad para tomar decisiones", "El cambio de motor a MySQL se decidió en un día y quedó documentado", "Registrar cada decisión con su motivo"],
       ["Resolver problemas difusos", "RF-11, la facturación, quedó condicional hasta conocer al proveedor", "Separar lo incierto en tareas pequeñas"],
       ["Confianza y respeto mutuos", "Los cambios se revisan por pull request, no a escondidas", "Revisar siempre, también con prisa"],
       ["Organización propia", "El reparto P1 a P4 y su orden dentro del sprint los definió el equipo", "Ajustarlo en cada retrospectiva"]],
      [1.6, 2.8, 2.1], 9.5)

# ---------------------------------------------------------------- 9
h("9. Mini evaluación")
tabla("Respuestas de la mini evaluación",
      ["Situación", "Respuesta", "Por qué"],
      [["1. El cliente recibe una versión funcional cada dos semanas", "Principio 3", "Es la entrega frecuente de software que funcione, de dos semanas a un par de meses"],
       ["2. El cliente pide modificar el sistema con el desarrollo ya iniciado", "Principio 2", "Son bienvenidos los requerimientos cambiantes, aun en etapas avanzadas"],
       ["3. Desarrolladores y gerente se reúnen seguido para resolver dudas", "Principio 6", "La conversación cara a cara es el medio más eficaz de transmitir información"],
       ["4. El equipo analiza qué hizo bien y qué mejorar al terminar una iteración", "Principio 12", "Es la reflexión a intervalos regulares para ajustar el comportamiento"],
       ["5. El equipo elimina funcionalidades innecesarias", "Principio 10", "La simplicidad: maximizar la cantidad de trabajo no realizado"]],
      [2.4, 1.0, 3.1], 9.5)

# ---------------------------------------------------------------- 10
h("10. Conclusiones")
p("Aplicar los 12 principios a nuestro propio proyecto mostró que la agilidad no es una lista para memorizar: cada principio explica una "
  "decisión que tomamos o un problema que tuvimos. Entregar el Sprint 1 funcionando (principios 1, 3 y 7) es lo que evitó que el SGCP se "
  "convirtiera en «el proyecto que nunca termina».")
p("Los cambios de requisitos (principio 2) fueron constantes, del tema del proyecto al motor de base de datos, y se absorbieron gracias a "
  "un diseño cuidado y a pruebas automáticas (principio 9). Donde más nos falta mejorar es en el ritmo sostenible y en la revisión entre "
  "pares cuando aprieta el plazo (principios 8 y 12). Para lo que queda del proyecto nos comprometemos a fijar plazos internos, a revisar "
  "cada pull request y a hacer una retrospectiva corta al cierre de cada sprint.")

# ---------------------------------------------------------------- referencias
salto()
h("Referencias")
for antes, titulo, despues in [
    ("Beck, K., Beedle, M., van Bennekum, A., Cockburn, A., Cunningham, W., Fowler, M., Grenning, J., Highsmith, J., Hunt, A., Jeffries, R., "
     "Kern, J., Marick, B., Martin, R. C., Mellor, S., Schwaber, K., Sutherland, J., & Thomas, D. (2001). ", "Manifiesto por el desarrollo ágil de software",
     ". https://agilemanifesto.org/iso/es/manifesto.html"),
    ("Cockburn, A., & Highsmith, J. (2001). Agile software development: The people factor. ", "Computer, 34", "(11), 131–133. https://doi.org/10.1109/2.963450"),
    ("Pressman, R. S. (2010). ", "Ingeniería del software: Un enfoque práctico", " (7.ª ed.). McGraw-Hill."),
    ("Schwaber, K., & Sutherland, J. (2020). ", "La Guía Scrum", ". https://scrumguides.org/"),
    ("Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026). ", "Reparto del SGCP por sprint e integrante",
     " [Documento técnico no publicado]. Repositorio SGCPdocumentacion, Universidad del Valle.")]:
    q = p("", False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.5)
    q.add_run(antes); q.add_run(titulo).italic = True; q.add_run(despues)

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
    doc.core_properties.title = TITULO_DOC
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
print(salida, n, "páginas;", len(TITULOS), "títulos en el índice")
