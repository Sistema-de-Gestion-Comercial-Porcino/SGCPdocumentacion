# Casos de uso del SGCC

Doce objetivos generales. El CRUD y las alternativas son acciones internas. Todas las cuentas humanas se autentican; los permisos limitan acciones y datos. Numeración vigente desde la reorganización de octubre de 2026.

| CU | Nombre | Participantes | RF principales |
|---|---|---|---|
| CU01 | Gestionar acceso | Propietario / administración, Ventas / cobranza, Producción, Almacén, Responsable de entrega, Comprador | RF12 |
| CU02 | Administrar usuarios | Propietario / administración | RF13 |
| CU03 | Gestionar clientes | Ventas / cobranza, Propietario / administración | RF10 |
| CU04 | Gestión de costos | Propietario / administración | RF02, RF03 |
| CU05 | Gestión de cotizaciones | Ventas / cobranza, Comprador | RF01, RF02 |
| CU06 | Gestionar pedidos | Ventas / cobranza, Comprador | RF01, RF03, RF05, RF19 |
| CU07 | Gestionar productos | Propietario / administración, Almacén, Comprador | RF02, RF04 |
| CU08 | Gestionar producción | Producción, Almacén | RF04, RF18, RF20 |
| CU09 | Gestionar inventario | Almacén | RF04 |
| CU10 | Gestionar pagos y cobranza | Ventas / cobranza, Propietario / administración | RF05, RF06, RF11, RF19, RF20 |
| CU11 | Gestionar transporte y entregas | Responsable de entrega, Comprador | RF07, RF08, RF14, RF17, RNF01 |
| CU12 | Gestionar reportes | Propietario / administración, Ventas / cobranza, Producción, Almacén, Responsable de entrega, Comprador | RF15 |

## CU01 · Gestionar acceso

Conexión para crear cuenta, autenticar o renovar sesión.

El personal recibe una cuenta de administración. El comprador puede registrarse sin obtener permisos internos. Alta de cuenta no equivale a crear una sesión.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Crear cuenta de comprador | Comprador | datos completos; identidad no duplicada | Informar duplicado o datos faltantes; no crear cuenta interna |
| Iniciar sesión | Todos | credenciales válidas; cuenta activa | Registrar intento y denegar acceso; conservar capturas locales |
| Recuperar acceso | Todos | identidad verificada; token vigente | No cambiar credenciales con token inválido o vencido |
| Cerrar sesión | Todos | sesión identificada | Conservar recepción pendiente para posterior acceso autorizado |

Reagrupa: CU01.

## CU02 · Administrar usuarios

Propietario autenticado y autorizado.

Crear cuentas, asignar permisos y desactivar sin borrar historial. Una persona puede ejercer varias responsabilidades.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Consultar usuarios | Propietario / administración | permiso de administración | Denegar consulta no autorizada |
| Crear usuario | Propietario / administración | login único; permisos autorizados | Informar duplicado o datos faltantes |
| Editar usuario | Propietario / administración | usuario existente; cambio autorizado | Rechazar conflicto o escalamiento de permisos |
| Desactivar o habilitar | Propietario / administración | se conserva administración activa | Impedir dejar el sistema sin administrador habilitado |

Reagrupa: CU02.

## CU03 · Gestionar clientes

Sesión y permiso de gestión de clientes.

Cliente y usuario son conceptos distintos: atención presencial no requiere que el cliente tenga cuenta.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Consultar y buscar | Ventas / cobranza | consulta autorizada | Mostrar sin resultados; no crear cliente automáticamente |
| Crear cliente | Ventas / cobranza | identificación y contacto válidos; sin duplicado | Recuperar coincidencia o solicitar corrección |
| Editar cliente | Ventas / cobranza | cliente existente y versión vigente | Conservar datos anteriores ante conflicto |
| Desactivar cliente | Propietario / administración | sin operaciones que requieran atención activa | Informar pedidos o deuda pendiente; no borrar información |

Reagrupa: CU03.

## CU04 · Gestión de costos

Producto definido; propietario autenticado.

Costo de referencia por producto y unidad; precio con vigencia. Margen estimado, sin costeo automático por animal. El histórico del pedido no se recalcula.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Consultar costos y precios | Propietario / administración | producto accesible | Informar producto inexistente |
| Definir nueva vigencia | Propietario / administración | costo y precio válidos; margen aceptado | Pedir corregir margen, fechas o unidades; conservar vigencia actual |
| Corregir o finalizar vigencia | Propietario / administración | cambio autorizado; sin alterar acuerdos históricos | Rechazar modificación retroactiva de pedidos confirmados |

Reagrupa: CU04.

## CU05 · Gestión de cotizaciones

Sesión válida; comprador consulta solo sus solicitudes.

Cotización y pedido separados. Rechazar no inicia preparación; cambiar lo cotizado requiere nueva aceptación.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Solicitar o crear cotización | Comprador | cliente identificado; productos activos | Mostrar producto inactivo o cantidad inválida; no crear pedido |
| Preparar y presentar | Ventas / cobranza | precios vigentes; detalles válidos | Conservar borrador y solicitar datos faltantes |
| Aceptar cotización | Comprador | versión presentada y vigente; aceptación verificable | Solicitar nueva cotización si cambió o venció |
| Modificar o rechazar | Comprador | solicitud propia y respuesta identificada | Mantener pendiente cuando no existe respuesta |
| Consultar cotizaciones | Ventas / cobranza | alcance autorizado; comprador solo propias | Denegar consulta de otro comprador |

Reagrupa: CU05, CU25.

## CU06 · Gestionar pedidos

Autenticación; confirmación exige cotización aceptada.

Reservas y pagos se gestionan en sus módulos con referencia al pedido. Cancelar resuelve seña y reservas por acuerdo; no borra dinero.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Confirmar pedido | Ventas / cobranza | aceptación vigente; fecha y condiciones acordadas | Mantener solicitud pendiente; no generar pedido sin aceptación |
| Consultar pedidos | Comprador | pedido propio; personal según permiso | Denegar información de otro cliente |
| Gestionar cambio o incidencia | Ventas / cobranza | acuerdo con cliente identificado | Mantener pedido bloqueado para despacho mientras no haya acuerdo |
| Cancelar pedido | Ventas / cobranza | cancelación autorizada; efecto de seña definido | Conservar pendiente de acuerdo; no devolver ni retener automáticamente |

Reagrupa: CU06, CU13, CU26.

## CU07 · Gestionar productos

Administrador gestiona; Almacén y comprador consultan según permiso.

El catálogo define qué es cada corte o derivado. Crear un producto no crea stock. Catálogo ilustrativo pendiente de validación comercial.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Administrar clasificaciones | Propietario / administración | código único; familia válida | Conservar clasificación usada y explicar dependencias |
| Crear producto | Propietario / administración | clasificación activa; código y unidad válidos | Informar duplicado o clasificación incompatible |
| Editar o desactivar producto | Propietario / administración | cambio autorizado; historia conservada | Impedir cambiar unidades incompatibles o borrar producto utilizado |
| Consultar catálogo | Comprador | sesión y visibilidad autorizadas | Mostrar sin stock; no reservar ni prometer fecha automáticamente |

Reagrupa: CU24.

## CU08 · Gestionar producción

Personal autorizado; producción online.

La orden produce varios resultados identificados. Cada resultado se vincula a producto/clasificación y lote. Cantidades previstas no son stock. Almacén captura pesajes manualmente; no hay interfaz automática de balanza.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Gestionar animales y órdenes | Producción | animal identificado; capacidad y fecha viables | Acordar reprogramación, abastecimiento o incidencia; no duplicar orden |
| Registrar control sanitario | Producción | evaluación humana y animal identificado | Corregir datos faltantes; conservar orden pendiente sin habilitar faeneo |
| Registrar faeneo y desposte | Producción | animales aptos; orden habilitada | No continuar si existe rechazo sanitario o producto incompatible |
| Confirmar resultados y pesajes | Almacén | productos/cortes identificados; peso y unidad válidos | Corregir peso, producto o diferencia; conservar resultado pendiente |
| Fabricar derivados | Producción | insumos aptos libres de reservas; fórmula de referencia | Corregir selección o insumos; no iniciar fabricación |
| Finalizar o reprogramar orden | Producción | orden existente y cambio autorizado | Corregir identificación o permisos; no cerrar la orden |

Reagrupa: CU08, CU09, CU10, CU11.

## CU09 · Gestionar inventario

Almacén autenticado; recepción o movimiento físico verificable.

Disponible = físico apto menos reservas activas. Cada movimiento y reserva tiene referencia única. La confirmación de producción no es una entrada.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Consultar existencias y ubicaciones | Almacén | permiso de inventario | Mostrar faltante; no crear stock previsto |
| Recibir productos | Almacén | origen, producto, corte/derivado, lote y cantidades verificadas | Registrar diferencia o custodia bloqueada; recuperar referencia duplicada |
| Reservar o liberar | Almacén | pedido confirmado; existencia apta libre suficiente | Registrar faltante y consultar preparación; no reservar previsiones |
| Registrar salida o consumo | Almacén | salida física autorizada; referencia nueva | Rechazar stock insuficiente o recuperar movimiento ya aplicado |
| Corregir diferencia | Almacén | ajuste autorizado y justificado | No sustituir ni borrar el saldo sin movimiento justificativo |

Reagrupa: CU07, CU12.

## CU10 · Gestionar pagos y cobranza

Personal autorizado; pagos requieren dinero realmente recibido.

Productos y servicios acordados/prestados separados. Deuda independiente de entrega. Facturación externa solo con integración habilitada y respuesta confirmada.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Registrar seña, cobro o abono | Ventas / cobranza | importe positivo; referencia nueva y dinero recibido | Recuperar duplicado o corregir aplicación; no registrar un pago supuesto |
| Acordar crédito | Ventas / cobranza | autorización e importe/vencimiento acordados | Mantener pendiente si no hay autorización; acordar otra condición |
| Consultar y seguir deuda | Ventas / cobranza | cliente identificado y alcance permitido | Conservar deuda y reprogramar contacto si no recibe abono |
| Corregir registro de pago | Propietario / administración | error comprobado; corrección autorizada | Cancelación de pedido no anula automáticamente el pago |
| Gestionar comprobante fiscal | Ventas / cobranza | integración habilitada; datos de venta válidos | Dejar pendiente/rechazado según respuesta; no simular factura ni duplicar emisión |

Reagrupa: CU14, CU15, CU16, CU17, CU18, CU19.

## CU11 · Gestionar transporte y entregas

Responsable autorizado. Descarga de reparto requiere conexión y sesión.

Solo recepción de entregas asignadas/autorizadas/descargadas admite captura offline. Confirmación central distingue conforme/observada; no modifica deuda.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Administrar transporte y ruta | Responsable de entrega | datos del transportista y vehículo válidos | Reasignar si no está disponible; conservar entregas existentes |
| Preparar retiro o despacho | Responsable de entrega | pedido completo; stock apto; pago o crédito habilitado | Mantener pendiente y comunicar faltante, bloqueo o condición de pago |
| Registrar control de frío | Responsable de entrega | conexión; medición y responsable identificados | Informar incidencia; no inferir diagnóstico ni umbral automático |
| Capturar recepción | Responsable de entrega | entrega autorizada; comprador verifica peso y productos | Sin señal conservar PENDIENTE; no declarar cierre central |
| Sincronizar y resolver | Responsable de entrega | conexión y sesión válidas; app abierta | Conservar conflicto para revisión; no sobrescribir ni perder evidencia |
| Cerrar ruta o corregir entrega | Responsable de entrega | resultados centrales registrados; sin envíos pendientes | Mantener ruta abierta si hay capturas por enviar; observación conserva resolución |

Reagrupa: CU20, CU21, CU22.

## CU12 · Gestionar reportes

Usuario autenticado; filtros y alcance autorizados.

Todos acceden según permiso. Comprador solo sus operaciones; costos y resultados generales quedan restringidos. Son consultas: no crean pedidos, stock ni pagos.

| Acción | Responsable | Condición | Si no se cumple |
|---|---|---|---|
| Seleccionar reporte y filtros | Todos | tipo permitido; fechas coherentes | Denegar datos ajenos o filtros incompatibles |
| Consultar resultados | Todos | consulta autorizada | Mostrar sin resultados sin inventar registros |
| Exportar reporte | Todos | misma autorización y filtros de la consulta | Informar error de exportación y permitir reintento |

Reagrupa: consultas y reportes de los módulos existentes.

Las antiguas referencias CUxx deben leerse con la matriz de equivalencias. RF09, RF16 y RF21 quedan fuera de alcance activo. RF11 es condicional; no se fabrica una respuesta fiscal.
