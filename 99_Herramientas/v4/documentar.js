const b=require('./base'),{defs,enums,links,inheritance}=require('./dominio'),{casos}=require('../especificacion_v3'),{specs}=require('./estados');
const {fs,path,ROOT,OUT,PDF}=b,doc=path.join(OUT,'00_Documentacion');fs.mkdirSync(doc,{recursive:true});
const count=Object.keys(defs).length;
const rules=[
 'Pedido nace únicamente de una cotización aceptada y vigente. El cliente de la cotización y del pedido debe coincidir. Una cotización origina como máximo un pedido; las revisiones se conservan por versión.',
 'Una cotización BORRADOR admite cero detalles. PRESENTADA y ACEPTADA exigen al menos uno. Un pedido confirmado exige uno o más detalles.',
 'Cada detalle conserva cantidad, unidad, precio acordado y costoReferenciaAcordado; actualizar PrecioProducto no cambia pedidos anteriores. La vigencia de precios de un mismo producto no se solapa.',
 'OrdenProduccion es abstracta: una orden concreta es FaeneoDesposte o FabricacionDerivado, sin pertenecer a las dos especializaciones. Una orden puede reponer stock sin pedido o atender varios detalles. PrevisionProducto registra estimación manual por producto y unidad; no es stock ni reserva. Antes de crear, el responsable revisa órdenes vigentes, previsiones y demanda vinculada; no se activa reposición automática RF16.',
 'FaeneoDesposte procesa uno o más animales identificados; un animal pertenece como máximo a una orden de faeneo. Antes de iniciar, el control humano vigente debe ser APTO. Rechazo no conduce a faeneo.',
 'FabricacionDerivado registra sus consumos por lote y su resultado de calidad. Cada consumo tiene un movimiento CONSUMO único que descuenta existencia física; un rechazo del derivado no repone insumos realmente utilizados. Completar fabricación requiere consumos válidos y calidad aprobada. La fórmula de referencia no inventa una gestión completa de recetas.',
 'inicioPrevisto y finPrevisto los establece el responsable. inicioReal y finReal permanecen vacíos hasta registrar los hechos. finPrevisto >= inicioPrevisto y finReal >= inicioReal. Llegar a la fecha prevista no genera producto disponible.',
 'Un lote puede proceder de una orden propia o de una recepción externa. Cada resultado propio identifica producto, cantidadProducida real y unidad. Una orden puede producir varios lotes de distintos productos. Para que haya disponibilidad se exige entrada física, estado APTO y saldo libre de reservas. Almacén confirma recepción y aplica movimientos una vez. Si el rendimiento real no cubre el detalle, se acuerda nueva fecha, sustitución o cancelación; no se reserva una previsión. Producto tipo INSUMO no se publica como artículo vendible por defecto.',
 'Existencia es única por lote y ubicación. Cantidades e importes son decimales y siempre se interpretan junto a su unidad. No se suman kilos con unidades.',
 'Disponible = cantidadFisica - reservas ACTIVA/CONFIRMADA. Confirmar la misma reserva no vuelve a descontar. CONSUMIDA se produce al registrar la salida física; LIBERADA devuelve disponibilidad sin crear entrada.',
 'Las referencias de pago, movimiento, reserva, emisión y sincronización son únicas en su ámbito. Reintentar recupera el registro existente o informa conflicto; no repite efectos.',
 'Pago pertenece a un pedido; el cliente se obtiene de ese pedido. Cada AplicacionPago pertenece a un pago y a un cargo del mismo pedido. Su importe es positivo y la suma de aplicaciones no supera el dinero válido recibido ni el saldo aplicable.',
 'Saldo del pedido = suma de CargoPedido - aplicaciones de pagos REGISTRADO. La seña no es un descuento comercial: se aplica una vez. La parte todavía no aplicada permanece identificada.',
 'CargoPedido separa PRODUCTO y SERVICIO. El servicio se cobra solo si corresponde y se acuerda; fabricar un derivado no agrega automáticamente un servicio al cliente.',
 'Cancelar pedido exige registrar la solución del anticipo. No implica devolución automática, retención automática ni anulación del pago. ANULADO_CON_TRAZA corrige un registro erróneo autorizado y revierte aplicaciones con auditoría; no ejecuta por sí mismo un reembolso.',
 'Para crédito se consulta saldo previo y se registra aprobación, importe y vencimiento. Como máximo un acuerdo activo por pedido. Sustituir un acuerdo conserva deuda y vincula la operación en auditoría; no es condonación.',
 'Despacho exige pedido completo, preparación PREPARADO y condición de pago cumplida: contado cubierto o crédito aprobado y servicios resueltos según acuerdo. No se autoriza entrega parcial por deducirla de una multiplicidad 0..*.',
 'Entrega ENTREGADA exige receptor, fecha, peso y evidencia de recepción conforme. fechaReal conserva la recepción física y fechaConfirmacion la validación central; observacionRecepcion conserva el detalle. Su cierre no cambia el saldo. El pedido comercial CERRADO exige entrega cerrada y saldo cero.',
 'Ruta agrupa entregas que pueden existir sin ruta o reasignarse. Es agregación compartida, no composición. Terminar una ruta exige resultados centrales registrados y ningún envío local pendiente. Admite entregas OBSERVADAS o CANCELADAS registradas; no las cambia a ENTREGADA.',
 'ControlFrio debe identificar al menos lote, entrega o ubicación de cámara. Registra lectura y evaluación del responsable; no se fija un umbral sanitario inventado.',
 'Pesaje de ANIMAL identifica el animal; el de CORTE identifica el lote. DESPACHO/RECEPCION se vinculan a la entrega. Cada registro tiene contexto de producción o entrega y una fuente de medición.',
 'La composición indica propietario exclusivo de un detalle o registro dependiente. Los registros comerciales se conservan por trazabilidad: el rombo negro no ordena borrado físico en cascada.',
 'RF09 y AlertaCliente son FUTUROS, fuera de la entrega actual. Cliente.esHabitual queda reservado para esa fase y no activa alertas. RF16 y RF21 también están fuera de alcance. Un usuario puede tener varios roles. Los roles combinan permisos y no se representan como subclases de persona. Los compradores del portal solo acceden a sus propios clientes/pedidos.',
 'El bloqueo de acceso usa un límite configurable de intentos. Las operaciones protegidas verifican sesión y permisos. RegistroAuditoria conserva autor, operación, entidad, identificador y fecha.',
 'OperacionPendiente existe solo para REGISTRAR_RECEPCION_ENTREGA en Android Kotlin. Identifica entrega, dispositivo, autor, clave única, versión base, fecha real y evidencia local. Exige descarga online previa de una entrega asignada y autorizada. Con app abierta y conexión se envía a la API; esta valida permiso, asignación, versión y evidencia y confirma una vez o informa conflicto. Timeout conserva PENDIENTE. Conflicto requiere revisión; si no aplica, se descarta con traza y evidencia conservada. No modifica stock, cobros ni deuda. La sincronización CONFIRMADA puede registrar Entrega ENTREGADA (conforme) u OBSERVADA; solo la primera habilita constancia conforme.',
 'El propietario ingresa costo de referencia y precio por producto y unidad. Pedido conserva costoEstimadoConfirmado y margenEstimadoConfirmado calculados con costos y precios por detalle. No se prorratea automáticamente costo de animal/faeneo entre cortes ni se informa utilidad real. Servicio separado solo si se acuerda y presta.',
 'RF11 exige modalidad y proveedor confirmados; sin integración permanece pendiente, sin factura simulada. RF17 registra frío de conservación/transporte y evaluación humana; RF18 conserva bloqueo prefaeneo por rechazo sanitario. No se mide temperatura corporal ni se diagnostica automáticamente.',
 'Los diagramas de objetos son instantáneas parciales con datos ficticios. Omitir un objeto de contexto en una vista no cambia la multiplicidad del modelo. Las horas de los ejemplos no establecen un tiempo estándar de faeneo.'
];
let dict='# Diccionario y reglas del modelo V4\n\n'+count+' clases de dominio, un solo diagrama general. Las enumeraciones están definidas como elementos UML editables en cada MDJ que las utiliza.\n\n';
for(const[n,[, ,attrs,ops=[]]]of Object.entries(defs)){dict+='## '+n+(n==='OrdenProduccion'?' (abstracta)':'')+'\n\n| Atributo | Tipo |\n|---|---|\n';for(const a of attrs){const [name,type]=a.split(':');dict+='| '+name+' | '+type.replace('?',' [0..1]')+' |\n';}if(ops.length)dict+='\nOperaciones: '+ops.map(x=>'`'+x+'()`').join(', ')+'.\n';dict+='\n';}
dict+='## Relaciones\n\n| A | Multiplicidad en A | Relación | B | Multiplicidad en B |\n|---|---|---|---|---|\n';for(const[a,c,ma,mb,n='',ag='none']of links)dict+=`| ${a} | ${ma} | ${ag==='composite'?'Composición':ag==='shared'?'Agregación':'Asociación'}${n?' · '+n:''} | ${c} | ${mb} |\n`;
dict+='\nHerencia: '+inheritance.map(([a,c])=>'`'+a+'` especializa `'+c+'`').join('; ')+'.\n\n';
dict+='## Enumeraciones\n\n| Tipo | Literales |\n|---|---|\n';for(const[n,v]of Object.entries(enums))dict+='| '+n+' | '+v.join(', ')+' |\n';
dict+='\n## Restricciones\n\n'+rules.map((s,i)=>(i+1)+'. '+s).join('\n')+'\n\nLa implementación relacional puede usar una tabla por clase concreta de producción con clave compartida hacia OrdenProduccion. Las asociaciones se traducen a claves foráneas o tablas de unión según multiplicidad. Este modelo UML no es todavía un esquema SQL ejecutable.\n';
fs.writeFileSync(path.join(doc,'Diccionario_V4.md'),dict);

let index='# Diagramas UML corregidos — V4\n\n74 MDJ editables y 74 PDF de revisión: 4 diagramas generales, 26 colaboraciones, 26 diagramas de objetos y 18 diagramas de estados.\n\n';
index+='## Generales\n\n| Diagrama | MDJ | PDF |\n|---|---|---|\n';
for(const[n,label]of [['Clases','Clases'],['Casos_de_Uso','Casos de uso'],['Componentes','Componentes'],['Despliegue','Despliegue']])index+=`| ${label} | [Abrir](../02_Ingenieria_de_Software/01_Generales/${n}_SGCC_V4.mdj) | [Ver](V4/01_Generales/${n}_SGCC_V4.pdf) |\n`;
index+='\n## Por caso de uso\n\nLos identificadores CU01–CU26 conservan la correspondencia con las secuencias y actividades existentes.\n\n| Caso | Colaboración MDJ | PDF | Objetos MDJ | PDF |\n|---|---|---|---|---|\n';
for(const c of casos)index+=`| ${c.id} · ${c.nombre} | [MDJ](../02_Ingenieria_de_Software/02_Colaboracion/${c.id}_Colaboracion.mdj) | [PDF](V4/02_Colaboracion/${c.id}_Colaboracion.pdf) | [MDJ](../02_Ingenieria_de_Software/03_Objetos/${c.id}_Objetos.mdj) | [PDF](V4/03_Objetos/${c.id}_Objetos.pdf) |\n`;
index+='\n## Estados por entidad\n\nCada diagrama explica el ciclo de vida de un objeto o de uno de sus aspectos. Pedido separa estado comercial y preparación; entrega y crédito conservan sus propios ciclos. No se inventa un diagrama de estados para una consulta que no cambia el objeto.\n\n| Entidad / atributo | MDJ | PDF |\n|---|---|---|\n';
for(const s of specs)index+=`| ${s.cl}.${s.attr} | [MDJ](../02_Ingenieria_de_Software/04_Estados/${s.file}_Estados.mdj) | [PDF](V4/04_Estados/${s.file}_Estados.pdf) |\n`;
index+='\n## Documentación y otros diagramas\n\n- [Diccionario y reglas V4](../02_Ingenieria_de_Software/00_Documentacion/Diccionario_V4.md).\n- [Criterios aplicados](../02_Ingenieria_de_Software/00_Documentacion/Criterios_V4.md).\n- [BPM, BPMN, secuencias y actividades actualizados](Indice_V3.md).\n- [Validación de archivos y geometría](V4/Validacion_V4.json).\n\nLos PDF conservan el tamaño de cada diagrama y permiten ampliarlo. Los MDJ contienen elementos nativos de StarUML, no imágenes insertadas.\n';
if(!process.env.SGCC_SKIP_PDFS)fs.writeFileSync(path.join(ROOT,'03_Revision/Indice_V4.md'),index);
fs.writeFileSync(path.join(OUT,'LEEME.md'),'# UML corregido — V4\n\n[Índice completo con enlaces a MDJ y PDF](../03_Revision/Indice_V4.md).\n\n- `01_Generales`: clases, casos de uso, componentes y despliegue.\n- `02_Colaboracion`: una interacción por cada uno de los 26 casos de uso.\n- `03_Objetos`: una instantánea por cada caso de uso.\n- `04_Estados`: 18 ciclos de vida específicos.\n- `00_Documentacion`: reglas del modelo y decisiones de diseño.\n\nLos PDF están en `03_Revision/V4`, organizados por las mismas carpetas.\n');
fs.writeFileSync(path.join(doc,'Criterios_V4.md'),`# Criterios de la corrección V4

Fuentes: los dos BPM corregidos del compañero, la entrevista al propietario, ASA1 y Clase _XXIII_IS.pdf, en particular las diapositivas 13–20. Se conserva la lógica de la reconstrucción autorizada: aceptación antes del pedido, tratamiento de faltantes, tiempos previstos/reales, trazabilidad del anticipo y separación entre entrega y deuda.

## Alcance

Clases, casos de uso, componentes y despliegue son generales. Colaboración desarrolla cada CU mediante participantes, conectores y mensajes numerados. Objetos muestra instancias, valores y enlaces conformes a las clases. Estados describe el ciclo de una entidad; no es un flujo de tareas entre actores.

La diapositiva 20 ilustra nuevamente componentes. Para despliegue se sigue su definición textual: distribución de software sobre hardware. Por eso se muestran equipos, entornos de ejecución, artefactos y enlaces de comunicación.

## Estructura

Composición: detalles de cotización/pedido, aplicaciones de pago, historial de precio, sesiones, controles de un animal, consumos de fabricación, seguimientos de un crédito y evidencias de entrega. Agregación: Ruta agrupa Entrega. Herencia: FaeneoDesposte y FabricacionDerivado especializan OrdenProduccion. Las personas pueden combinar roles; no se crea herencia artificial de roles.

La asociación Producto–PrecioProducto es composición histórica exclusiva; los cambios crean una nueva vigencia. Existencia conserva cantidad física y calcula disponibilidad usando reservas. ControlFrio permite identificar la cámara, además de lote o entrega. Pesaje identifica animal o lote cuando corresponde.

## Plataforma e integración

Se define un sistema web responsivo con conexión para gestión y portal comprador, y una app Android nativa en Kotlin para reparto. iOS y aplicaciones nativas de escritorio quedan fuera del alcance. La plataforma queda definida por decisión del equipo; proveedor de alojamiento, equipos y reglas operativas pendientes se validan por separado. El backend agrupa los componentes de negocio en un único despliegue; no se presuponen microservicios, marca de servidor ni fabricante de balanza.

Los módulos de análisis de las secuencias se relacionan así con componentes: Identidad → Identidad y permisos; Clientes/Precios → Clientes y precios; Ventas → Cotizaciones y pedidos; Stock/Produccion → Stock y producción; Tesoreria/Facturacion → Cobros y facturación; Entregas → Entregas y evidencias; Portal → Portal comprador. Los controladores y repositorios de colaboración son participantes del diseño, no tablas adicionales.

sgcc-web contiene gestión online; sgcc-portal es el portal comprador online. sgcc-reparto.apk (Kotlin) contiene reparto, Room/SQLite y archivos privados locales. sgcc-api comparte negocio, validación de sincronización, auditoría y adaptadores. Android requiere sesión y descarga previa con conexión; solo CU21 permite capturar recepción de esas entregas sin señal. CU22 requiere conexión. La sincronización funciona con app abierta o botón manual; al reconectar se revalida en servidor. No se promete ejecución en segundo plano. Cobros, pedidos, crédito, stock y facturación requieren conexión. La cola local no reemplaza respaldos centrales.

El comprador del portal procede del BPM propuesto, aunque la entrevista describe clientes que hoy no usan software. WhatsApp continúa como canal atendido por ventas; no se introduce un bot. RF-09 y RF-16 permanecen como mejoras futuras y RF-21 pendiente; los tres fuera de alcance actual. CU23 conserva diseño identificado FUTURO y sin asociación de actor activa en el diagrama general. RF11 depende de modalidad y proveedor confirmados.

## Alcance sin conexión

La app Android consulta solo entregas ya descargadas y guarda receptor, fecha, peso confirmado, conformidad, observación y evidencia. La UI distingue PENDIENTE local de Entrega central. Sincronización CONFIRMADA produce ENTREGADA si la recepción es conforme u OBSERVADA si requiere resolución; esta última no genera constancia definitiva. Sin asignación descargada se pide conexión y descarga; un error de guardado exige corregir antes de informar éxito. Al sincronizar: autenticación, asignación, versión, clave única y evidencia se validan en servidor. Una recepción ya aplicada devuelve su identificador, sin repetir efectos; una entrega cancelada o reasignada no se sobrescribe. La sesión expirada exige reautenticación online conservando pendientes. Borrar datos/desinstalar puede perder capturas no enviadas; no equivale a respaldo.

Referencias técnicas: [Arquitectura con datos locales y red de Android](https://developer.android.com/topic/architecture/data-layer/offline-first), [Room](https://developer.android.com/training/data-storage/room).

## Estados y datos

Los estados están definidos como enumeraciones nativas. Se incorpora VENCIDO para distinguir el crédito fuera de plazo y CANCELADA para entrega suspendida por acuerdo, sin confundirlos con pago completado. Los usuarios distinguen ACTIVO, BLOQUEADO y DESHABILITADO. Las fechas y ejemplos monetarios de objetos son ficticios.

Los 26 identificadores de casos de uso permanecen: 25 vigentes y CU23 reservado como FUTURO. La clase PrevisionProducto separa planificación de resultados reales por producto/lote y de existencia recibida. El margen de producto es estimado con costo de referencia manual. Los consumos de fabricación descuentan stock una vez incluso si se rechaza el resultado. Se actualizan secuencias, actividades y procesos propuestos para los canales web/Android y la confirmación central de la recepción. Los modelos actuales y las bases verticales del compañero se conservan como fuentes. Los nombres de atributos internos refinados aquí se consultan en el diccionario V4.
`);
console.log('Documentación V4 creada. Clases:',count);
