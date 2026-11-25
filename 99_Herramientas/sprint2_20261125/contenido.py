TITULO_DOC = "Prueba integral del Sprint 2 del SGCP"

def lista(items):
    for x in items:
        q = p(x, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)
        q.runs[0].text = "• " + q.runs[0].text

CAB = ["N.º", "Perfil", "Qué hacer en la web", "Qué debe pasar", "✓"]
ANCHOS = [0.5, 0.95, 2.4, 2.25, 0.4]
def pasos(titulo, filas, nota=None):
    tabla(titulo, CAB, [f + ["☐"] for f in filas], ANCHOS, 9, nota)

# ---------------------------------------------------------------- portada
q = p(TITULO_DOC, False, True, centrado=True, interlineado=1.15)
q.paragraph_format.space_before = Pt(24); q.paragraph_format.space_after = Pt(6); q.runs[0].font.size = Pt(18)
q = p("Guía de pruebas paso a paso: catálogo, sanidad, producción, inventario, frío, cargos y trazabilidad", False, cursiva=True, centrado=True, interlineado=1.15)
q.paragraph_format.space_after = Pt(18)
q = p("", False, centrado=True, interlineado=1); q.paragraph_format.space_after = Pt(24); q.add_run().add_picture(str(AQUI / "logo_univalle.png"), width=Inches(1.9))
for txt, neg in [("Integrantes:", True), ("Dario Haziel Tambo Parra", False), ("Angel Sebastian Eguez Mur", False), ("Sofia Cuellar Roca", False),
                 ("Victor Manuel Manrique Arancivia", False), ("", False), ("Materia:", True), ("Ingeniería de Software", False), ("", False),
                 ("Docente:", True), ("Rolando Lara Sánchez", False), ("", False), ("Universidad del Valle · Bolivia", False), ("", False),
                 ("Fecha:", True), ("25 de noviembre de 2026", False)]:
    p(txt, False, neg, centrado=True, interlineado=1.15)
salto()

p("Índice", False, True, centrado=True)
indice_p = doc.add_paragraph()
salto()

# ---------------------------------------------------------------- 1
h("1. Propósito de la guía")
p("Este documento desglosa el **Sprint 2** del Sistema de Gestión Comercial Porcino (SGCP) en pasos que cualquier integrante puede "
  "ejecutar en la web, con el resultado que debe observar en cada uno. Sirve para dos cosas: que el equipo pruebe el sprint completo antes "
  "de la presentación del viernes 27 de noviembre, y que la demostración ante el docente siga un recorrido ordenado en el que cada "
  "criterio de aceptación del Product Backlog se vea cumplir en pantalla.")
p("El Sprint 2 cubre la parte operativa de la chanchería: desde que llega un cerdo y pasa el control sanitario hasta que sus cortes "
  "entran pesados al almacén, quedan disponibles para vender y se pueden reservar para un pedido. Es el sprint que reemplaza el cuaderno "
  "donde hoy se anota lo despachado por orden de salida, y por eso su regla central es que **el stock solo sube con una entrada física "
  "pesada, nunca con una previsión**.")
p("Cada tabla de pasos tiene una última columna (✓) para marcar el paso cuando se haya comprobado. Si un paso falla, se anota el mensaje "
  "que mostró la web y se avisa en el grupo antes de seguir: los pasos dependen unos de otros.")

# ---------------------------------------------------------------- 2
h("2. Alcance del Sprint 2 según el Product Backlog")
p("El Excel del proyecto (Product Backlog y Sprint Backlog) asigna al Sprint 2 cuatro requerimientos funcionales y dos no funcionales. "
  "La tabla reproduce su parámetro de aceptación tal como figura en el Excel e indica en qué sección de esta guía se prueba.")
tabla("Requerimientos del Sprint 2 y dónde se prueban",
      ["Código", "Prioridad", "Parámetro de aceptación (literal del Excel)", "Secciones"],
      [["RF-04 Catálogo, producción, inventario y pesajes", "Should",
        "Crear costilla y lomo como cortes y jamón elaborado como derivado. Una orden obtiene costilla y lomo en lotes separados con pesajes "
        "propios; otra fabrica jamón. Confirmar resultado no suma stock; recepción física única sí. Una referencia repetida no duplica entrada "
        "ni consumo. (Descripción: disponible es físico apto menos reservas; previsiones no se reservan.)", "4.1, 4.3, 4.4, 4.5, 4.6"],
       ["RF-18 Control sanitario previo al faeneo", "Must", "Animal rechazado no inicia faeneo ni produce lote apto; queda incidencia.", "4.2"],
       ["RF-17 Control de frío", "Could", "Lectura con valor, unidad, fecha, contexto y responsable; evaluación humana. Sin temperatura corporal "
        "ni acciones automáticas no validadas.", "4.7"],
       ["RF-20 Cargos de producto y servicio", "Should", "El estado de cuenta distingue producto/servicio; no crea cargo de servicio no prestado.", "4.8"],
       ["RNF-03 Confidencialidad y respaldo", "Should", "Restauración central verificable; datos locales privados; pendiente local no se supone respaldado.", "4.9"],
       ["RNF-06 Trazabilidad", "Should", "Autor, fecha real/central, clave, versión y resolución de conflicto conservados.", "4.6, 4.9"]],
      [1.35, 0.7, 3.65, 0.8], 9)

# ---------------------------------------------------------------- 3
h("3. Preparación")
h("3.1 Entorno y perfiles", 2)
p("La prueba se hace en la web del SGCP con la API levantada y la base de datos con todas las migraciones aplicadas. Conviene abrir dos "
  "ventanas privadas del navegador, una para Producción y otra para Almacén, para ver en paralelo cómo una acción de un perfil cambia lo "
  "que ve el otro. Se usan cuentas de prueba, una por perfil; sus contraseñas se comparten por el grupo del equipo y no se escriben en "
  "este documento ni en los repositorios.")
tabla("Perfiles que intervienen en la prueba",
      ["Cuenta", "Perfil", "Qué hace en el Sprint 2"],
      [["`admin`", "Superadministrador", "Revisa productos, incidencias y la auditoría."],
       ["`produccion1`", "PRODUCCION", "Registra animales y controles sanitarios, planifica órdenes, registra resultados y consumos, resuelve incidencias."],
       ["`almacen1`", "ALMACEN", "Pesa lotes, confirma entradas físicas, consulta existencias y movimientos, reserva stock y registra control de frío."],
       ["`ventas1`", "VENTAS", "Tiene el pedido confirmado que se reserva y registra el cargo por servicio prestado."]],
      [1.3, 1.4, 3.8], 9.5)
h("3.2 Datos de partida", 2)
p("Antes de empezar deben existir en el catálogo los productos **Costilla de cerdo** y **Lomo de cerdo**, clasificados como cortes, y "
  "**Jamón elaborado**, clasificado como derivado; el Lomo de cerdo necesita un costo y un precio vigentes (por ejemplo, costo Bs 28 y "
  "precio Bs 35 por kg). Para la sección 4.6 hace falta además un pedido **confirmado** de 2 kg de lomo, que se arma con el flujo del "
  "Sprint 1: Ventas registra la cotización, el comprador o Ventas la acepta y se confirma el pedido. Los códigos de esta guía (CERDO-001, "
  "L-COS-001, etc.) son ejemplos; si ya existen en la base, se usa otro sufijo.")

# ---------------------------------------------------------------- 4
h("4. Recorrido de prueba paso a paso")
h("4.1 Catálogo de cortes y derivados (RF-04)", 2)
pasos("Pasos 1 a 3: catálogo", [
    ["1", "admin", "Menú **Productos**. Buscar «Costilla», «Lomo» y «Jamón».", "Aparecen Costilla de cerdo y Lomo de cerdo con clasificación de corte y Jamón elaborado como derivado, con código, presentación, unidad kg y estado activo."],
    ["2", "almacen1", "Menú **Existencias**, filtrar por Costilla de cerdo.", "No hay existencias: crear un producto **no crea stock**."],
    ["3", "admin", "Menú **Gestión de costos**: revisar el precio vigente del lomo.", "Lomo con costo de referencia y precio de venta vigentes."]])

h("4.2 Control sanitario e incidencias (RF-18)", 2)
pasos("Pasos 4 a 11: sanidad, rechazo e incidencia", [
    ["4", "produccion1", "**Sanidad → + Registrar animal**: identificación CERDO-001, peso de ingreso 95 kg, procedencia y proveedor. Guardar.", "El animal aparece en Sanidad en estado PENDIENTE."],
    ["5", "produccion1", "Registrar otro animal: CERDO-002.", "Dos animales pendientes."],
    ["6", "produccion1", "Abrir CERDO-001 → **Registrar control** → Resultado «Aprobado · apto para faeneo».", "CERDO-001 queda APTO; el control guarda fecha y responsable."],
    ["7", "produccion1", "Abrir CERDO-002 → **Registrar control** → «Rechazado · no se faena», observación «Fiebre al ingreso».", "CERDO-002 queda **RECHAZADO** y la ficha muestra el motivo y la fecha."],
    ["8", "produccion1", "**Producción → + Planificar orden**, tipo Faeneo, animal CERDO-002.", "**Se niega**: «No se puede faenar el animal …: fue rechazado en el control sanitario del … Motivo: Fiebre al ingreso»."],
    ["9", "produccion1", "Menú **Incidencias** (filtro Pendientes).", "Aparece la incidencia «Animal CERDO-002» con el motivo, quién la registró y estado PENDIENTE. Desde la ficha del animal hay un enlace «Ver la incidencia»."],
    ["10", "produccion1", "En la incidencia, **Resolver**; probar primero sin motivo y luego con «Animal devuelto al proveedor».", "Sin motivo se niega. Con motivo queda RESUELTA con la resolución y la fecha."],
    ["11", "produccion1", "Volver a Sanidad → CERDO-002.", "Sigue **RECHAZADO**: resolver la incidencia registra la decisión, **no rehabilita** al animal."]],
    "Los pasos 9 y 10 usan la pantalla Incidencias, agregada en el PR SGCPuiweb #9 (v5.1.0). En `almacen1` la misma pantalla se ve sin el botón Resolver.")

h("4.3 Orden de faeneo con dos lotes separados (RF-04)", 2)
pasos("Pasos 12 a 17: faeneo, previsiones y resultados", [
    ["12", "produccion1", "**+ Planificar orden**: tipo Faeneo, animal CERDO-001, inicio previsto ahora, fin previsto en 3 horas; previsiones Costilla de cerdo 8 kg y Lomo de cerdo 5 kg.", "Orden PLANIFICADA con sus dos previsiones."],
    ["13", "almacen1", "**Existencias** → Costilla de cerdo.", "Sigue en 0: **una previsión no es stock**."],
    ["14", "produccion1", "Abrir la orden → **Iniciar orden**.", "Orden EN_PROCESO."],
    ["15", "produccion1", "**Registrar resultados**: Costilla de cerdo con lote L-COS-001 y Lomo de cerdo con lote L-LOM-001, cada uno con su vencimiento. **Confirmar orden**.", "La orden queda CONFIRMADA con **dos lotes separados**, uno por producto."],
    ["16", "almacen1", "**Existencias**.", "Siguen en 0: **confirmar el resultado no suma stock** (los lotes nacen sin cantidad)."],
    ["17", "almacen1", "**Pesajes y entradas → Registrar pesaje**: abrir la lista de lotes.", "L-COS-001 y L-LOM-001 aparecen pendientes de pesaje, cada uno con su unidad."]])

h("4.4 Pesaje y entrada física única (RF-04)", 2)
pasos("Pasos 18 a 23: pesaje y entrada", [
    ["18", "almacen1", "**Registrar pesaje** de L-COS-001: bruto 13, tara 0.5.", "El formulario calcula **neto 12,500 kg** y guarda el responsable. El aviso recuerda que pesar no da de alta la existencia."],
    ["19", "almacen1", "**Existencias** → Costilla.", "Sigue en 0: **el pesaje no suma stock**."],
    ["20", "almacen1", "**Confirmar entrada física** del pesaje de L-COS-001, ubicación «Cámara 1».", "Existencias de costilla pasa a **12,500 kg**: Física apta 12,5; Reservada 0; Disponible 12,5."],
    ["21", "almacen1", "Intentar confirmar otra vez la entrada del mismo pesaje.", "**Se niega**: «Este lote ya tiene su entrada física… No se vuelve a sumar al stock.» Existencias sigue en 12,5."],
    ["22", "almacen1", "Pesar L-LOM-001 (bruto 5.4, tara 0.4) y confirmar su entrada en «Cámara 1».", "Lomo con 5,000 kg disponibles, en lote distinto de la costilla: **cada corte con su pesaje propio**."],
    ["23", "almacen1", "En Existencias, enlace **Movimientos** de la costilla.", "Un movimiento «Entrada física» +12,5 con responsable y fecha."]])

h("4.5 Fabricación de un derivado y consumo sin duplicar (RF-04)", 2)
pasos("Pasos 24 a 28: jamón elaborado", [
    ["24", "produccion1", "**+ Planificar orden**: tipo Fabricación, previsión Jamón elaborado 3 kg. **Iniciar orden**.", "Segunda orden, EN_PROCESO: **otra orden fabrica jamón**."],
    ["25", "produccion1", "**Registrar insumo consumido**: existencia de Costilla de cerdo (L-COS-001), cantidad 2.", "La costilla baja de 12,5 a **10,5** kg."],
    ["26", "produccion1", "Volver atrás en el navegador y reenviar el mismo formulario (o hacer doble clic en Registrar consumo).", "La costilla **sigue en 10,5**, no en 8,5: el formulario lleva una referencia única y **una referencia repetida no duplica el consumo**."],
    ["27", "produccion1", "**Registrar resultados**: Jamón elaborado, lote L-JAM-001. **Confirmar orden**.", "Lote de jamón creado sin cantidad; como en 4.3, no suma stock hasta pesarlo y darle entrada."],
    ["28", "almacen1", "**Movimientos** de la costilla.", "Entrada +12,5 y «Consumo en producción» −2, cada uno con su responsable."]])

h("4.6 Disponible y reservas para un pedido (RF-04, RNF-06)", 2)
pasos("Pasos 29 a 35: reservar y liberar", [
    ["29", "almacen1", "**Pedidos por preparar**.", "Aparece el pedido confirmado de 2 kg de lomo con «FALTA RESERVAR» y, por producto, confirmado, reservado y falta."],
    ["30", "almacen1", "**Reservar** en el lomo. Revisar la lista de existencias.", "Solo se ofrecen existencias **físicas, aptas y con disponible** (L-LOM-001 · Cámara 1). El jamón u otra previsión no aparecen: **las previsiones no se reservan**."],
    ["31", "almacen1", "Reservar 5 kg.", "**Se niega** con el mensaje de la API: «El producto o la cantidad no corresponden al pedido.» Nada cambia."],
    ["32", "almacen1", "Reservar 2 kg desde L-LOM-001.", "El pedido pasa a «RESERVA COMPLETA». En Existencias el lomo muestra Reservada 2 y Disponible 3: **disponible = físico apto − reservas**."],
    ["33", "almacen1", "En la reserva, **Liberar**; probar sin motivo y luego con «El cliente pidió otro lote».", "Sin motivo se niega. Con motivo, Disponible vuelve a 5 y la reserva queda LIBERADA con su motivo (no se borra)."],
    ["34", "almacen1", "Reservar de nuevo 2 kg.", "Reserva completa otra vez."],
    ["35", "admin", "**Entregas → Preparar** con ese pedido.", "La entrega se prepara. Sin la reserva completa la web lo niega con «Reserva toda la cantidad confirmada…». Es el enlace con el Sprint 3."]],
    "La pantalla Pedidos por preparar es parte del PR SGCPuiweb #9 (v5.1.0). La API admite una sola reserva activa por producto del pedido y por lote: para sumar más del mismo lote, se libera y se reserva el total.")

h("4.7 Control de frío y bloqueo sin revertir consumos (RF-17)", 2)
pasos("Pasos 36 a 41: frío", [
    ["36", "almacen1", "**Control de frío → + Registrar control**: lote L-COS-001, temperatura 9 °C, ubicación Cámara 1, fecha de la lectura, evaluación «Rechazado», observación «Cámara sin frío durante la noche».", "Se guarda la lectura con **valor, unidad, fecha, lote, ubicación y responsable**. El aviso aclara que el sistema no mide la temperatura ni la evalúa: **la evaluación es humana**."],
    ["37", "almacen1", "Registrar otra lectura de 2 °C sobre L-LOM-001 con evaluación «Apto».", "Se guarda y el lote sigue APTO: no hay umbrales ni acciones automáticas."],
    ["38", "almacen1", "**Existencias**.", "L-COS-001 queda **BLOQUEADO** con disponible 0."],
    ["39", "produccion1", "**Producción** → abrir la orden de fabricación del jamón → tabla de resultados.", "El lote L-JAM-001, que consumió costilla de ese lote, también figura **BLOQUEADO**."],
    ["40", "almacen1", "**Movimientos** de la costilla.", "El «Consumo en producción» −2 **sigue registrado**: bloquear no revierte el consumo real."],
    ["41", "produccion1", "**Incidencias** (filtro Todas).", "Aparecen las incidencias de los lotes L-COS-001 y L-JAM-001 con su motivo."]])

h("4.8 Cargos de producto y de servicio (RF-20)", 2)
pasos("Pasos 42 a 44: cargos separados", [
    ["42", "ventas1", "**Pedidos** → abrir el pedido confirmado → sección «Cargos del pedido».", "El cargo por producto aparece solo; en «Cargo por servicio» se lee que el pedido no tiene servicios acordados y prestados: **no se crea un cargo de servicio no prestado**."],
    ["43", "ventas1", "**+ Registrar servicio prestado**: concepto «Corte a pedido», importe Bs 30, cómo se acordó («acordado por WhatsApp con el cliente») y fecha en que se prestó.", "El servicio aparece en su propia tabla, separado del producto, con el acuerdo y la fecha."],
    ["44", "ventas1", "Revisar el total del pedido.", "Producto y servicio figuran por separado; fabricar el jamón (4.5) no generó ningún cargo de servicio."]])

h("4.9 Permisos, auditoría y respaldo (RNF-03, RNF-06)", 2)
pasos("Pasos 45 a 50: seguridad y trazabilidad", [
    ["45", "produccion1", "Escribir en la barra de direcciones `/Almacen/Pesajes` y `/Frio`.", "Redirige a «Sin permiso»: Producción no pesa ni registra frío."],
    ["46", "almacen1", "Abrir `/Produccion/Nueva` y `/Sanidad`.", "Redirige a «Sin permiso»: Almacén no planifica órdenes ni registra animales."],
    ["47", "ventas1", "Abrir `/Almacen/Pedidos`.", "Redirige a «Sin permiso»; en el detalle del pedido no ve el botón «Revisar reservas»."],
    ["48", "admin", "Menú **Auditoría**.", "Cada acción del recorrido figura con fecha, usuario, acción y módulo, entre ellas el bloqueo de lotes como `BLOQUEAR_SIN_REVERTIR_CONSUMO`, las reservas y la resolución de la incidencia."],
    ["49", "admin", "Revisar una reserva liberada y una incidencia resuelta.", "Ninguna se borró: conservan su motivo, su autor y su fecha. Las anulaciones mantienen historial."],
    ["50", "—", "Respaldo y restauración de la base central.", "Se demuestra con el procedimiento de respaldo y restauración de la tarea V-3 (pendiente al 25 de noviembre)."]])

# ---------------------------------------------------------------- 5
h("5. Matriz de cumplimiento")
p("La matriz cruza cada parte del parámetro de aceptación con los pasos que lo demuestran. Si todos los pasos de una fila quedan "
  "marcados, el criterio se da por cumplido.")
tabla("Criterio de aceptación y pasos que lo demuestran",
      ["Req.", "Criterio", "Pasos"],
      [["RF-04", "Costilla y lomo como cortes; jamón elaborado como derivado", "1"],
       ["RF-04", "Crear producto no crea stock", "2"],
       ["RF-04", "Una orden obtiene costilla y lomo en lotes separados con pesajes propios", "12, 15, 18, 22"],
       ["RF-04", "Otra orden fabrica jamón", "24, 27"],
       ["RF-04", "Confirmar resultado no suma stock", "13, 16, 19"],
       ["RF-04", "La recepción física única sí suma stock", "20, 21"],
       ["RF-04", "Una referencia repetida no duplica entrada ni consumo", "21, 26"],
       ["RF-04", "Disponible = físico apto − reservas; las previsiones no se reservan", "30, 32, 33"],
       ["RF-18", "El animal rechazado no inicia faeneo", "7, 8"],
       ["RF-18", "No produce lote apto y queda incidencia trazable", "9, 10, 11"],
       ["RF-17", "Lectura con valor, unidad, fecha, contexto y responsable", "36"],
       ["RF-17", "Evaluación humana; sin acciones automáticas", "36, 37"],
       ["RF-20", "Producto y servicio por separado; sin servicio no prestado", "42, 43, 44"],
       ["RNF-03", "Permisos por perfil y datos confidenciales", "45, 46, 47"],
       ["RNF-03", "Restauración central verificable", "50"],
       ["RNF-06", "Autor y fecha en cada operación; anulaciones con historial", "23, 28, 33, 48, 49"]],
      [0.8, 4.4, 1.3], 9.5)

# ---------------------------------------------------------------- 6
h("6. Estado al 25 de noviembre y pendientes")
p("Toda la regla de negocio del Sprint 2 está en la API y se probó desde la web el 25 de noviembre. Lo que faltaba eran pantallas: las "
  "de reservas, incidencias y movimientos se agregaron en el PR SGCPuiweb #9, que debe estar fusionado antes de ensayar. Quedan tres "
  "tareas de compañeros que completan criterios secundarios del sprint; mientras no estén, los pasos afectados se explican en vez de "
  "mostrarse.")
tabla("Tareas que completan el Sprint 2",
      ["Tarea", "Responsable", "Qué agrega", "Pasos afectados"],
      [["PR SGCPuiweb #9 (D-1, D-2, D-3)", "Dario", "Pedidos por preparar, Incidencias y Movimientos", "9–11, 23, 28–35, 41"],
       ["S-1", "Sebastián", "Control de frío asociado a una entrega y visible para el perfil ENTREGA", "36 (variante de entrega)"],
       ["S-2", "Sebastián", "Rechazar un lote sin pasar por frío y recibir un lote comprado a terceros", "Complementa 38–39"],
       ["S-3", "Sebastián", "Anular un cargo de servicio mal registrado", "Complementa 43"],
       ["V-3", "Victor", "Procedimiento de respaldo y restauración verificable", "50"]],
      [1.7, 0.95, 2.75, 1.1], 9.5)

# ---------------------------------------------------------------- 7
h("7. Guion corto para la demostración")
p("Para la presentación no hace falta ejecutar los 50 pasos. Este recorrido de doce pasos muestra cada criterio una vez, con dos ventanas "
  "abiertas (Producción y Almacén) y la sesión de administrador para el cierre.")
for i, t in enumerate([
    "Sanidad: registrar CERDO-001 (aprobado) y CERDO-002 (rechazado, «Fiebre al ingreso»).",
    "Planificar faeneo con CERDO-002: el sistema lo niega con el motivo.",
    "Incidencias: mostrar la incidencia abierta y resolverla; el animal sigue rechazado.",
    "Planificar faeneo con CERDO-001 con previsiones de costilla 8 kg y lomo 5 kg; mostrar que Existencias sigue en 0.",
    "Registrar resultados con L-COS-001 y L-LOM-001 y confirmar: dos lotes separados, stock todavía en 0.",
    "Almacén: pesar L-COS-001 (bruto 13, tara 0,5 → neto 12,5); el stock sigue en 0.",
    "Confirmar la entrada: stock 12,5. Repetir la entrada: se niega.",
    "Fabricación de jamón: consumir 2 kg de costilla; reenviar el consumo no lo duplica (10,5).",
    "Pedidos por preparar: reservar 2 kg de lomo; Disponible baja; liberar con motivo y volver a reservar.",
    "Control de frío Rechazado sobre L-COS-001: el lote y el jamón quedan bloqueados y el consumo sigue en Movimientos.",
    "Pedido: registrar el servicio «Corte a pedido» aparte del producto.",
    "Auditoría: cada acción con usuario, fecha y módulo."], 1):
    q = p(f"{i}. {t}", False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)

# ---------------------------------------------------------------- refs
h("Referencias")
for antes, titulo, despues in [
    ("Pressman, R. S. (2010). ", "Ingeniería del software: Un enfoque práctico", " (7.ª ed.). McGraw-Hill."),
    ("Schwaber, K., & Sutherland, J. (2020). ", "La Guía Scrum", ". https://scrumguides.org/"),
    ("Sommerville, I. (2011). ", "Ingeniería de software", " (9.ª ed.). Pearson Educación."),
    ("Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026a). ", "Formato Proyecto - SGCC Actualizado",
     " [Product Backlog y Sprint Backlog, hoja de cálculo no publicada]. Repositorio SGCPdocumentacion, Universidad del Valle."),
    ("Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026b). ", "Revisión integral de los sprints y reparto final",
     " [Documento técnico no publicado]. Repositorio SGCPdocumentacion, Universidad del Valle.")]:
    q = p("", False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.5)
    q.add_run(antes); q.add_run(titulo).italic = True; q.add_run(despues)
