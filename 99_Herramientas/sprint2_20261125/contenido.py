TITULO_DOC = "Prueba integral del Sprint 2 del SGCP"

def lista(items):
    for x in items:
        q = p(x, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)
        q.runs[0].text = "• " + q.runs[0].text

CAB = ["N.º", "Perfil", "Qué hacer en la web", "Qué debe pasar", "✓"]
ANCHOS = [0.5, 0.95, 2.4, 2.25, 0.4]
# Los pasos se numeran solos y se citan por clave con {clave}: insertar un paso no descuadra la matriz ni las notas.
NUM = {}
def R(texto):
    return re.sub(r"\{(\w+)\}", lambda m: str(NUM[m.group(1)]), texto)
def pasos(titulo, filas, nota=None):
    filas_num = []
    for clave, *resto in filas:
        assert clave not in NUM, clave
        NUM[clave] = len([k for k in NUM if k != "total_pasos"]) + 1
        filas_num.append([str(NUM[clave])] + resto + ["☐"])
    NUM["total_pasos"] = len([k for k in NUM if k != "total_pasos"])
    tabla(f"Pasos {filas_num[0][0]} a {filas_num[-1][0]}: {titulo}", CAB, filas_num, ANCHOS, 9, R(nota) if nota else None)

# ---------------------------------------------------------------- portada
q = p(TITULO_DOC, False, True, centrado=True, interlineado=1.15)
q.paragraph_format.space_before = Pt(24); q.paragraph_format.space_after = Pt(6); q.runs[0].font.size = Pt(18)
q = p("Guía de pruebas paso a paso: catálogo, sanidad, producción, inventario, frío, cargos y trazabilidad", False, cursiva=True, centrado=True, interlineado=1.15)
q.paragraph_format.space_after = Pt(18)
q = p("", False, centrado=True, interlineado=1); q.paragraph_format.space_after = Pt(24); q.add_run().add_picture(str(AQUI / "logo_univalle.png"), width=Inches(1.9))
for txt, neg in [("Integrantes:", True), ("Dario Haziel Tambo Parra", False), ("Angel Sebastian Eguez Mur", False), ("Sofia Cuellar Roca", False),
                 ("Victor Manuel Manrique Arancivia", False), ("", False), ("Materia:", True), ("Ingeniería de Software", False), ("", False),
                 ("Docente:", True), ("Rolando Lara Sánchez", False), ("", False), ("Universidad del Valle · Bolivia", False), ("", False),
                 ("Fecha:", True), ("27 de noviembre de 2026", False)]:
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
      [["`administrador1`", "ADMINISTRADOR", "Revisa el catálogo y las incidencias; prepara entregas a domicilio."],
       ["`propietario1`", "PROPIETARIO", "Revisa la auditoría y el historial al cierre."],
       ["`produccion1`", "PRODUCCION", "Registra animales y controles sanitarios, planifica órdenes, registra resultados y consumos, resuelve incidencias."],
       ["`almacen1`", "ALMACEN", "Pesa lotes, confirma entradas físicas, consulta existencias y movimientos, reserva stock y registra control de frío."],
       ["`ventas1`", "VENTAS", "Revisa la gestión de costos, tiene el pedido confirmado que se reserva, prepara su retiro en el local y registra el cargo por servicio prestado."]],
      [1.3, 1.4, 3.8], 9.5)
p("La cuenta `admin` (SUPERADMIN) es del equipo de desarrollo y no participa en la prueba: cada paso se hace con el perfil que lo hará en "
  "la chanchería. La gestión de costos la ven Ventas y el Propietario, no el Administrador, porque el costo de reposición es un dato "
  "comercial reservado.")
h("3.2 Datos de partida", 2)
p("Antes de empezar deben existir en el catálogo los productos **Costilla de cerdo** y **Lomo de cerdo**, clasificados como cortes, y "
  "**Jamón elaborado**, clasificado como derivado; el Lomo de cerdo necesita un costo y un precio vigentes (por ejemplo, costo Bs 28 y "
  "precio Bs 35 por kg). Para la sección 4.6 hace falta además el pedido **confirmado** de un cliente que compra 2 kg de lomo; se arma con el "
  "flujo del Sprint 1: Ventas registra la cotización, el comprador o Ventas la acepta y se confirma el pedido. En la base de prueba los tres "
  "productos ya existen; el precio del lomo, el cliente y su pedido se registran antes de empezar. Los códigos de esta guía (CERDO-001, "
  "L-COS-001, etc.) son ejemplos; si ya existen en la base, se usa otro sufijo.")

# ---------------------------------------------------------------- 4
h("4. Recorrido de prueba paso a paso")
p("Los pasos siguen el orden real de un día de trabajo en la chanchería. Cuando un resultado depende de una regla que no es evidente, "
  "la nota de la tabla explica el porqué.")
h("4.1 Catálogo de cortes y derivados (RF-04)", 2)
pasos("catálogo", [
    ["cat", "administrador1", "Menú **Productos**. Buscar «Costilla», «Lomo» y «Jamón».", "Aparecen Costilla de cerdo y Lomo de cerdo con clasificación de corte y Jamón elaborado como derivado, con código, presentación, unidad kg y estado activo."],
    ["sinstock", "almacen1", "Menú **Existencias**, filtrar por Costilla de cerdo.", "No hay existencias: crear un producto **no crea stock**."],
    ["precio", "ventas1", "Menú **Gestión de costos**: revisar el precio vigente del lomo.", "Lomo con costo de referencia y precio de venta vigentes."]])

h("4.2 Control sanitario e incidencias (RF-18)", 2)
pasos("sanidad, rechazo e incidencia", [
    ["an1", "produccion1", "**Sanidad → + Registrar animal**: identificación CERDO-001, peso de ingreso 95 kg, procedencia y proveedor. Guardar.", "El animal aparece en Sanidad con estado «Pendiente de control»."],
    ["an2", "produccion1", "Registrar otro animal: CERDO-002.", "Dos animales pendientes."],
    ["apto", "produccion1", "Abrir CERDO-001 → **Registrar control** → Resultado «Aprobado · apto para faeneo».", "CERDO-001 queda APTO; el control guarda fecha y responsable."],
    ["rech", "produccion1", "Abrir CERDO-002 → **Registrar control** → «Rechazado · no se faena», observación «Fiebre al ingreso».", "CERDO-002 queda «**Rechazado · bloqueado**» y la ficha muestra el motivo y la fecha."],
    ["faeneo_no", "produccion1", "**Producción → + Planificar orden**, tipo Faeneo, animal CERDO-002.", "**Se niega**: «No se puede faenar el animal …: fue rechazado en el control sanitario del … Motivo: Fiebre al ingreso»."],
    ["inc", "produccion1", "Menú **Incidencias** (filtro Pendientes).", "Aparece la incidencia «Animal CERDO-002» con el motivo, quién la registró y estado PENDIENTE. Desde la ficha del animal hay un enlace «Ver la incidencia»."],
    ["resolver", "produccion1", "En la incidencia, **Resolver**; probar primero sin motivo y luego con «Animal devuelto al proveedor».", "Sin motivo se niega. Con motivo queda RESUELTA con la resolución y la fecha."],
    ["sigue", "produccion1", "Volver a Sanidad → CERDO-002.", "Sigue **RECHAZADO**: resolver la incidencia registra la decisión, **no rehabilita** al animal."],
    ["rehab", "produccion1", "En la ficha de CERDO-002 buscar **Registrar control**. Luego escribir en la barra la dirección del formulario de control de ese animal (la misma que se abrió para rechazarlo).", "La ficha ya **no ofrece** «Registrar control», y la dirección vuelve a la ficha con «Este animal ya fue rechazado: no admite otro control y su incidencia ya está registrada». No se lo puede aprobar ni rechazar de nuevo, y en Incidencias sigue habiendo **una sola** incidencia de CERDO-002."],
    ["filtro", "produccion1", "En **Sanidad**, escribir «cerdo-002» en el filtro y pulsar **Filtrar**; luego elegir el estado «Rechazado · bloqueado».", "Solo aparece CERDO-002, en ambos casos. El filtro busca por arete o proveedor y conserva la paginación."],
    ["an3", "produccion1", "Registrar CERDO-003 y aprobarlo en su control sanitario.", "CERDO-003 queda «Apto para faeneo»."],
    ["apto_rech", "produccion1", "Abrir CERDO-003 → **Registrar control** → «Rechazado», primero con la observación «x» y luego con «Cojera detectada al cargar».", "El formulario avisa que el animal ya estaba apto y pide explicar qué pasó. Con «x» **se niega**: «El animal estaba apto: explica en la observación qué le pasó…». Con el motivo, queda rechazado. La ficha muestra «Pasó de apto a rechazado el …: Cojera detectada al cargar» y la incidencia empieza con «Pasó de apto a rechazado:»."]],
    "Incidencias es parte del PR SGCPuiweb #9 (v5.1.0); en `almacen1` se ve sin el botón Resolver. El paso {rehab} muestra una regla "
    "deliberada: un animal rechazado no vuelve a quedar apto con un control nuevo, y tampoco se rechaza dos veces, porque eso duplicaba su "
    "incidencia. Qué hacer si el animal devuelto se recupera y vuelve a la chanchería es una decisión abierta (sección 6.2).")

h("4.3 Orden de faeneo con dos lotes separados (RF-04)", 2)
pasos("faeneo, previsiones y resultados", [
    ["plan", "produccion1", "**+ Planificar orden**: tipo Faeneo, animal CERDO-001, inicio previsto ahora, fin previsto en 3 horas; previsiones Costilla de cerdo 8 kg y Lomo de cerdo 5 kg.", "Orden PLANIFICADA con sus dos previsiones."],
    ["prev0", "almacen1", "**Existencias** → Costilla de cerdo.", "Sigue en 0: **una previsión no es stock**."],
    ["iniciar", "produccion1", "Abrir la orden → **Iniciar orden**.", "Orden EN_PROCESO."],
    ["result", "produccion1", "**Registrar resultados**: Costilla de cerdo con lote L-COS-001 y Lomo de cerdo con lote L-LOM-001, cada uno con su vencimiento. **Confirmar orden**.", "La orden queda CONFIRMADA con **dos lotes separados**, uno por producto."],
    ["conf0", "almacen1", "**Existencias**.", "Siguen en 0: **confirmar el resultado no suma stock** (los lotes nacen sin cantidad)."],
    ["pend", "almacen1", "**Pesajes y entradas → Registrar pesaje**: abrir la lista de lotes.", "L-COS-001 y L-LOM-001 aparecen pendientes de pesaje, cada uno con su unidad."]])

h("4.4 Pesaje y entrada física única (RF-04)", 2)
pasos("pesaje y entrada", [
    ["pesar", "almacen1", "**Registrar pesaje** de L-COS-001: bruto 13, tara 0.5.", "El formulario calcula **neto 12,500 kg** y guarda el responsable. El aviso recuerda que pesar no da de alta la existencia."],
    ["pes0", "almacen1", "**Existencias** → Costilla.", "Sigue en 0: **el pesaje no suma stock**."],
    ["entrada", "almacen1", "**Confirmar entrada física** del pesaje de L-COS-001, ubicación «Cámara 1».", "Existencias de costilla pasa a **12,500 kg**: Física apta 12,5; Reservada 0; Disponible 12,5."],
    ["entrada2", "almacen1", "Intentar confirmar otra vez la entrada del mismo pesaje.", "**Se niega**: «Este lote ya tiene su entrada física… No se vuelve a sumar al stock.» Existencias sigue en 12,5."],
    ["lomo", "almacen1", "Pesar L-LOM-001 (bruto 5.4, tara 0.4) y confirmar su entrada en «**Cámara 2**».", "Lomo con 5,000 kg disponibles, en otro lote y otra cámara: **cada corte con su pesaje propio**."],
    ["mov1", "almacen1", "En Existencias, enlace **Movimientos** de la costilla.", "Un movimiento «Entrada física» +12,5 con responsable y fecha."]])

h("4.5 Fabricación de un derivado para vender sin pedido (RF-04, RF-20)", 2)
p("La chanchería fabrica jamón para tenerlo en stock y venderlo a quien lo pida; no hace falta un pedido previo. El derivado sigue el "
  "mismo camino que un corte: se registra el insumo que sale de una existencia, se confirma el lote sin cantidad y **la cantidad real la "
  "pesa almacén**. El sistema no suma los insumos ni supone un rendimiento: 2 kg de carne no dan necesariamente 2 kg de jamón. En la "
  "práctica el jamón sale de la pierna; aquí se usa costilla solo porque es el corte que ya tiene stock en la prueba.")
pasos("jamón elaborado", [
    ["fab", "produccion1", "**+ Planificar orden**: tipo Fabricación, previsión Jamón elaborado 3 kg. **Iniciar orden**.", "Segunda orden, EN_PROCESO: **otra orden fabrica jamón**."],
    ["consumo", "produccion1", "**Registrar insumo consumido**: existencia de Costilla de cerdo (L-COS-001), cantidad 2. Leer el aviso rojo y marcar «Confirmo que este insumo ya salió de la cámara y se usó en esta fabricación».", "Sin la marca se niega con «Confirma que el consumo es real e irreversible». Con la marca, la costilla baja de 12,5 a **10,5** kg."],
    ["consumo2", "produccion1", "Volver atrás en el navegador y reenviar el mismo formulario (o hacer doble clic en Registrar consumo).", "La costilla **sigue en 10,5**, no en 8,5: el formulario lleva una referencia única y **una referencia repetida no duplica el consumo**."],
    ["noanular", "produccion1", "Volver a la orden de fabricación y buscar el botón **Anular**.", "Ya no aparece: **una orden que consumió insumos no se anula**, porque la costilla se mezcló en el jamón y no vuelve a su lote. Abrir a mano `/Produccion/Anular/…` vuelve a la orden con el aviso, y la API responde `ORDEN_CON_CONSUMOS`. Lo único que queda es confirmar la orden con lo que realmente salió."],
    ["jam", "produccion1", "**Registrar resultados**: Jamón elaborado, lote L-JAM-001. **Confirmar orden**.", "Lote de jamón creado sin cantidad; igual que en el faeneo, todavía no suma stock."],
    ["jampes", "almacen1", "**Registrar pesaje** de L-JAM-001: bruto 3.2, tara 0.2. **Confirmar entrada** en «Cámara 2».", "Jamón elaborado con **3,000 kg disponibles** para vender a cualquier cliente, sin pedido previo. La cantidad es la pesada, no la suma de insumos."],
    ["mov2", "almacen1", "**Movimientos** de la costilla.", "Entrada +12,5 y «Consumo en producción» −2, cada uno con su responsable."],
    ["sincargo", "ventas1", "Abrir cualquier pedido confirmado → «Cargos del pedido».", "No aparece ningún cargo de servicio por haber fabricado el jamón: **fabricar un derivado no genera un cargo de servicio**."]],
    "El cargo por servicio de RF-20 (sección 4.8) solo existe cuando un cliente pide y recibe un servicio, por ejemplo que le faeneen "
    "su propio animal o le hagan un corte especial. Lo que la chanchería fabrica para su propio stock no tiene a quién cobrarse como "
    "servicio: su costo se refleja en el costo de referencia del producto (RF-02) y se recupera con el precio de venta.")

h("4.6 Disponible y reservas para un pedido (RF-04, RNF-06)", 2)
p("Esta sección no tiene relación con el jamón: es un cliente que compra 2 kg de **lomo** y tiene su pedido confirmado (sección 3.2). "
  "Almacén aparta del stock lo que ese pedido necesita para que nadie más lo venda.")
pasos("reservar y liberar", [
    ["cola", "almacen1", "**Pedidos por preparar**.", "Una tabla compacta, una fila por pedido, con búsqueda por código o cliente, filtro (con reserva pendiente, reserva completa o todos) y paginación. El pedido de 2 kg de lomo aparece con «FALTA RESERVAR» y, por producto, reservado / confirmado y el enlace «Reservar 2 kg»."],
    ["opciones", "almacen1", "**Reservar** en el lomo. Revisar la lista de existencias.", "Solo se ofrecen existencias **físicas, aptas y con disponible** (L-LOM-001 · Cámara 2). Una previsión de producción no aparece: **las previsiones no se reservan**."],
    ["exceso", "almacen1", "Reservar 5 kg.", "**Se niega** con el mensaje de la API: «El producto o la cantidad no corresponden al pedido.» Nada cambia."],
    ["reserva", "almacen1", "Reservar 2 kg desde L-LOM-001.", "El pedido pasa a «RESERVA COMPLETA». En Existencias el lomo muestra Reservada 2 y Disponible 3: **disponible = físico apto − reservas**. La física sigue en 5: reservar no saca la carne de la cámara."],
    ["liberar", "almacen1", "En la reserva, **Liberar**; probar sin motivo y luego con «El cliente pidió otro lote».", "Sin motivo se niega. Con motivo, Disponible vuelve a 5 y la reserva queda LIBERADA con su motivo (no se borra)."],
    ["reserva2", "almacen1", "Reservar de nuevo 2 kg.", "Reserva completa otra vez."],
    ["preparar", "ventas1", "El cliente pasa a recoger el lomo al local. **Entregas → + Preparar entrega** con ese pedido. Revisar la lista de modalidades y la de responsables.", "Ventas solo ve «Retiro en el local» y puede elegirse a sí mismo («· Ventas») o a un repartidor que esté en el local («· Repartidor»). La entrega se prepara con Ventas como responsable. Sin la reserva completa la web lo niega con «Reserva toda la cantidad confirmada…». Es el enlace con el Sprint 3."],
    ["domicilio", "administrador1", "**Entregas → + Preparar entrega**, elegir «A domicilio» y abrir la lista de responsables.", "A domicilio solo se ofrecen repartidores: los vendedores desaparecen de la lista y la API también lo niega. La entrega a domicilio la preparan el Administrador o Reparto, no Ventas. No hace falta guardarla."]],
    "La pantalla Pedidos por preparar es parte del PR SGCPuiweb #9 (v5.1.0). La API admite una sola reserva activa por producto del pedido "
    "y por lote: para sumar más del mismo lote, se libera y se reserva el total.")

h("4.7 Control de frío y bloqueo sin revertir consumos (RF-17)", 2)
p(R("**Qué pasó en la historia de la prueba.** La costilla entró a la Cámara 1 el día anterior (paso {entrada}); el lomo y el jamón están "
  "en la Cámara 2. Durante la noche la Cámara 1 se quedó sin frío y nadie lo notó. A primera hora, producción sacó 2 kg de esa costilla "
  "para el jamón (paso {consumo}). En la revisión de la mañana, almacén lee 9 °C en la Cámara 1, cuando la carne fresca refrigerada se "
  "conserva entre 0 y 4 °C, y el registro de la cámara muestra que estuvo así desde la noche. El responsable decide que esa costilla ya "
  "no es apta para vender. Como los 2 kg que fueron al jamón pasaron la misma noche en esa cámara, el jamón también queda en duda."))
pasos("frío", [
    ["frio", "almacen1", "**Control de frío → + Registrar control**: elegir «**Una cámara completa (todos sus lotes)**» y leer el aviso rojo. Ubicación Cámara 1, temperatura 9 °C, evaluación «Rechazado», fecha y hora de la lectura. Probar primero sin «Fuera de temperatura desde» y luego con la hora que muestra el registro de la cámara (las 22:00 de la noche anterior). Observación «Revisión de la mañana: 9 °C; la cámara estuvo sin frío desde la noche anterior».", "Sin la hora **se niega**: «Para rechazar la cámara indica desde qué hora estuvo fuera de temperatura (revisa antes su registro)». Con la hora se guarda la lectura con **valor, unidad, fecha, cámara, inicio de la falla y responsable**, y el mensaje dice que los lotes que estuvieron en la Cámara 1 desde esa hora quedaron en revisión. El sistema no mide la temperatura ni la evalúa: la cámara se rechaza porque **una persona la evaluó como Rechazado**."],
    ["frio2", "almacen1", "Registrar una lectura de 2 °C en la Cámara 2 sobre L-LOM-001 con evaluación «Apto».", "Se guarda y el lomo sigue APTO y vendible: no hay umbrales ni acciones automáticas, y la falla fue solo de la Cámara 1."],
    ["bloq", "almacen1", "**Existencias**.", "L-COS-001 queda **BLOQUEADO** con disponible 0: los 10,5 kg siguen contados como físicos, pero ya no se pueden vender ni reservar. Debajo del lote se lee su origen (la orden de faeneo) y, debajo de la ubicación, «Ingresó Almacén de prueba · fecha y hora»: quién lo puso en esa cámara y cuándo."],
    ["bloqjam", "almacen1", "Existencias del Jamón elaborado.", "L-JAM-001 también queda **BLOQUEADO** con disponible 0, porque consumió costilla de ese lote **después** del inicio de la falla. El lomo y el jamón de la Cámara 2 no cambian por la falla de la Cámara 1."],
    ["consumo_sigue", "almacen1", "**Movimientos** de la costilla.", "El «Consumo en producción» −2 **sigue registrado**: esos 2 kg salieron de la cámara y se usaron; bloquear no los devuelve."],
    ["inclotes", "produccion1", "**Incidencias** (filtro Todas).", "Aparecen las incidencias de L-COS-001 («Falla de frío en Cámara 1 desde … (lectura …): Revisión de la mañana…») y de L-JAM-001 («Insumo rechazado: L-COS-001»). Quien las registró figura con su nombre, nunca como «Cuenta …»."]],
    "Con la hora de inicio, la API pone en revisión (bloquea, con una incidencia por lote) los lotes que estuvieron en la cámara desde esa "
    "hora, y los derivados **solo si consumieron después**. Un jamón hecho antes de la falla queda libre y lo que salió antes no se toca. "
    "La incidencia anota además cuánto se despachó del lote después del inicio, para avisar a esos clientes. Por eso el aviso del "
    "formulario pide investigar antes la hora real en el registro de la cámara: una hora mal puesta bloquea de más o deja pasar "
    "producto comprometido. Un control sobre un solo lote admite la misma hora; si se deja vacía, la API bloquea por precaución todo "
    "derivado de ese lote. Existencias muestra, por lote, su origen y quién lo ingresó a qué cámara y cuándo.")

h("4.8 Cargos de producto y de servicio (RF-20)", 2)
pasos("cargos separados", [
    ["cargos", "ventas1", "**Pedidos** → abrir el pedido de lomo → sección «Cargos del pedido».", "El cargo por producto aparece solo; en «Cargo por servicio» se lee que el pedido no tiene servicios acordados y prestados: **no se crea un cargo de servicio no prestado**."],
    ["servicio", "ventas1", "El cliente pidió que le corten el lomo en bifes y se acordó cobrarlo: **+ Registrar servicio prestado** con concepto «Corte a pedido», importe Bs 30, cómo se acordó («acordado por WhatsApp con el cliente») y fecha en que se prestó.", "El servicio aparece en su propia tabla, separado del producto, con el acuerdo y la fecha."],
    ["total", "ventas1", "Revisar el total del pedido.", "Producto y servicio figuran por separado y suman al saldo de **ese cliente**."]])

h("4.9 Permisos, auditoría y respaldo (RNF-03, RNF-06)", 2)
pasos("seguridad y trazabilidad", [
    ["perm1", "produccion1", "Escribir en la barra de direcciones `/Almacen/Pesajes` y `/Frio`.", "Redirige a «Sin permiso»: Producción no pesa ni registra frío."],
    ["perm2", "almacen1", "Abrir `/Produccion/Nueva` y `/Sanidad/Formulario`; luego el menú **Sanidad**.", "Las dos direcciones redirigen a «Sin permiso»: Almacén no planifica órdenes ni registra animales. En Sanidad solo consulta: no ve «+ Registrar animal» ni «Registrar control»."],
    ["perm3", "ventas1", "Abrir `/Almacen/Pedidos`.", "Redirige a «Sin permiso»; en el detalle del pedido no ve el botón «Revisar reservas»."],
    ["audit", "propietario1", "Menú **Auditoría**.", "Cada acción del recorrido figura con fecha, usuario (su nombre y, debajo, el login), acción y módulo, entre ellas el bloqueo de lotes como «BLOQUEAR SIN REVERTIR CONSUMO» (módulo Lote), los controles de frío, las reservas y la resolución de la incidencia. La pantalla muestra 20 por página, lo más reciente primero."],
    ["hist", "propietario1", "Revisar una reserva liberada y una incidencia resuelta.", "Ninguna se borró: conservan su motivo, su autor y su fecha. Las anulaciones mantienen historial."],
    ["respaldo", "Servidor", "En la terminal del servidor (SGCPapi, tarea V-3): `scripts/respaldo.sh sgcp <carpeta>` y luego `scripts/restaurar.sh <archivo>.sql sgcp_restaurada`. Comparar los conteos de Pedidos y Lotes en las dos bases.", "El respaldo deja .sql, .meta y .sha256; la restauración crea una base **nueva** con los mismos conteos. Se niega a restaurar sobre la base original, sobre una base existente o con un archivo alterado (`tests/respaldo/verificar.sh` lo comprueba)."]])

# ---------------------------------------------------------------- 5
h("5. Matriz de cumplimiento")
p("La matriz cruza cada parte del parámetro de aceptación con los pasos que lo demuestran. Si todos los pasos de una fila quedan "
  "marcados, el criterio se da por cumplido.")
tabla("Criterio de aceptación y pasos que lo demuestran",
      ["Req.", "Criterio", "Pasos"],
      [[a, b, R(c)] for a, b, c in [
       ["RF-04", "Costilla y lomo como cortes; jamón elaborado como derivado", "{cat}"],
       ["RF-04", "Crear producto no crea stock", "{sinstock}"],
       ["RF-04", "Una orden obtiene costilla y lomo en lotes separados con pesajes propios", "{plan}, {result}, {pesar}, {lomo}"],
       ["RF-04", "Otra orden fabrica jamón; su cantidad es la pesada", "{fab}, {jam}, {jampes}"],
       ["RF-04", "Confirmar resultado no suma stock", "{prev0}, {conf0}, {pes0}"],
       ["RF-04", "La recepción física única sí suma stock", "{entrada}, {entrada2}"],
       ["RF-04", "Una referencia repetida no duplica entrada ni consumo", "{entrada2}, {consumo2}"],
       ["RF-04", "Consumos reales se descuentan aunque el lote se rechace", "{consumo}, {consumo_sigue}"],
       ["RF-04", "El consumo es irreversible: se confirma al registrarlo y la orden ya no se anula", "{consumo}, {noanular}"],
       ["RF-04", "Disponible = físico apto − reservas; las previsiones no se reservan", "{opciones}, {reserva}, {liberar}"],
       ["RF-18", "El animal rechazado no inicia faeneo ni se rehabilita con otro control", "{rech}, {faeneo_no}, {rehab}"],
       ["RF-18", "Un rechazo no se repite ni duplica la incidencia; el paso de apto a rechazado se explica", "{rehab}, {an3}, {apto_rech}"],
       ["RF-18", "No produce lote apto y queda incidencia trazable", "{inc}, {resolver}, {sigue}"],
       ["RF-17", "Lectura con valor, unidad, fecha, contexto y responsable", "{frio}"],
       ["RF-17", "Evaluación humana; sin acciones automáticas", "{frio}, {frio2}"],
       ["RF-17", "Falla de una cámara con fecha y hora de inicio: solo se bloquea lo expuesto", "{frio}, {bloq}, {bloqjam}, {inclotes}"],
       ["RF-20", "Producto y servicio por separado; sin servicio no prestado", "{sincargo}, {cargos}, {servicio}, {total}"],
       ["RNF-03", "Permisos por perfil y datos confidenciales", "{preparar}, {domicilio}, {perm1}, {perm2}, {perm3}"],
       ["RNF-03", "Restauración central verificable", "{respaldo}"],
       ["RNF-06", "Autor y fecha en cada operación; anulaciones con historial", "{mov1}, {mov2}, {liberar}, {bloq}, {audit}, {hist}"]]],
      [0.8, 4.4, 1.3], 9.5)

# ---------------------------------------------------------------- 6
h("6. Estado al 27 de noviembre y decisiones abiertas")
h("6.1 Tareas que completan el Sprint 2", 2)
p(R("Todas las tareas que completan el Sprint 2 están fusionadas. El 26 de noviembre se ejecutaron los 53 pasos que tenía entonces la guía, de punta a punta "
  "sobre una base vacía (solo con el catálogo de ejemplo y las cuentas de prueba): cada paso se hizo en la web, con sus formularios, y "
  "su resultado se comprobó también contra la API. Los pasos se cumplieron. "
  "El 27 de noviembre la guía se corrigió con lo que encontró la prueba a mano: los pasos usan los perfiles reales (Administrador, "
  "Propietario, Ventas) en lugar de la cuenta del equipo de desarrollo, y se agregaron los pasos {filtro}, {an3}, {apto_rech}, {noanular} "
  "y {domicilio}, además de la cámara completa en el paso {frio}. Las correcciones están en revisión en SGCPapi #17 (v5.1.5) y SGCPuiweb #14 "
  "(v5.1.6), y el recorrido de los {total_pasos} pasos se repitió con ellas sobre una base nueva: todos se cumplieron en la web, salvo el respaldo, que se prueba en la terminal. El respaldo de V-3 se probó con una copia real de la base y su restauración en una base nueva."))
tabla("Tareas que completan el Sprint 2",
      ["Tarea", "Responsable", "Qué agrega", "Pasos afectados"],
      [["PR SGCPuiweb #9 (D-1, D-2, D-3)", "Dario", "Pedidos por preparar, Incidencias y Movimientos", R("{inc}–{sigue}, {mov1}, {mov2}, {cola}–{preparar}, {inclotes}")],
       ["S-1", "Sebastián", "Control de frío asociado a una entrega y visible para el perfil ENTREGA", R("{frio} (variante de entrega)")],
       ["S-2", "Sebastián", "Rechazar un lote sin pasar por frío y recibir un lote comprado a terceros", R("Complementa {bloq}–{bloqjam}")],
       ["S-3", "Sebastián", "Anular un cargo de servicio mal registrado", R("Complementa {servicio}")],
       ["V-3", "Victor", "Procedimiento de respaldo y restauración verificable", R("{respaldo}")],
       ["SGCPapi #17 y SGCPuiweb #14 (en revisión)", "Dario", "Correcciones de la prueba a mano: sanidad, nombres, consumo irreversible, frío por cámara, entregas por rol", R("{rehab}–{apto_rech}, {consumo}, {noanular}, {cola}, {preparar}, {domicilio}, {frio}–{inclotes}, {audit}")]],
      [1.7, 0.95, 2.75, 1.1], 9.5)
h("6.2 Decisiones abiertas detectadas al revisar la guía", 2)
p("Al recorrer la guía con casos reales del negocio aparecieron tres situaciones que la API resolvía de forma conservadora. La "
  "segunda quedó resuelta el 27 de noviembre con la hora de inicio de la falla de frío; las otras dos conviene confirmarlas con el "
  "propietario de la chanchería antes de cambiar nada. Ninguna impide demostrar el Sprint 2.")
tabla("Situaciones detectadas y su estado",
      ["Situación", "Qué hace hoy la API", "Opción a confirmar"],
      [["Un animal rechazado se devuelve al proveedor, se recupera y vuelve a la chanchería.",
        "Lo rechaza para siempre («No se revierte un bloqueo…») y la identificación es única, así que tampoco se puede registrar de nuevo con el mismo arete.",
        "Tratarlo como un **reingreso**: nuevo ingreso del mismo animal con su propio control sanitario, conservando el rechazo anterior en el historial."],
       ["La falla de frío ocurrió después de que una parte del lote se usó en un derivado.",
        R("**Resuelta (v5.1.5).** El control pide desde qué hora estuvo fuera de temperatura: el derivado que consumió antes queda libre y solo se bloquea lo expuesto (paso {frio})."),
        "Queda por confirmar si un responsable autorizado puede **liberar con motivo** un derivado bloqueado por un control de lote registrado sin hora de inicio."],
       ["El lote rechazado sigue físicamente en la cámara y se va a desechar.",
        "Queda con disponible 0, pero su cantidad física sigue contada en Existencias.",
        "Registrar una **baja por merma** con motivo y responsable, como movimiento de stock."]],
      [1.9, 2.3, 2.3], 9)

# ---------------------------------------------------------------- 7
h("7. Guion corto para la demostración")
p(R("Para la presentación no hace falta ejecutar los {total_pasos} pasos. Este recorrido de doce pasos muestra cada criterio una vez, con dos "
  "ventanas abiertas (Producción y Almacén) y la sesión del propietario para el cierre."))
for i, t in enumerate([
    "Sanidad: registrar CERDO-001 (aprobado) y CERDO-002 (rechazado, «Fiebre al ingreso»); CERDO-002 ya no ofrece otro control.",
    "Planificar faeneo con CERDO-002: el sistema lo niega con el motivo.",
    "Incidencias: mostrar la incidencia abierta y resolverla; el animal sigue rechazado.",
    "Planificar faeneo con CERDO-001 con previsiones de costilla 8 kg y lomo 5 kg; mostrar que Existencias sigue en 0.",
    "Registrar resultados con L-COS-001 y L-LOM-001 y confirmar: dos lotes separados, stock todavía en 0.",
    "Almacén: pesar L-COS-001 (bruto 13, tara 0,5 → neto 12,5); el stock sigue en 0. Confirmar la entrada en Cámara 1: stock 12,5. Repetir la entrada: se niega.",
    "Lomo pesado y con entrada en Cámara 2.",
    "Fabricación de jamón: consumir 2 kg de costilla confirmando que es irreversible (reenviar no duplica, y la orden ya no ofrece Anular); pesar el jamón (3 kg) y darle entrada: queda a la venta sin pedido.",
    "Pedidos por preparar: reservar 2 kg de lomo para el pedido de un cliente; Disponible baja; liberar con motivo y volver a reservar.",
    "Control de frío: la Cámara 1 estuvo sin frío desde las 22:00 de la noche anterior; lectura de 9 °C y la cámara completa evaluada como Rechazado con esa hora de inicio. La costilla y el jamón que consumió después quedan bloqueados; el lomo de la Cámara 2 sigue apto; el consumo sigue en Movimientos.",
    "Pedido de lomo: registrar el servicio «Corte a pedido» aparte del producto.",
    "Auditoría (propietario): cada acción con el nombre del usuario, fecha y módulo."], 1):
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
