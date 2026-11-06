# Diccionario del modelo de clases

Modelo general con 41 clases. Las clases de interfaz/control en secuencias y colaboración representan participantes de análisis; no son tablas del dominio.

Cadena del producto obtenido: OrdenProduccion → ResultadoProduccion → Lote → Producto → ClasificacionProducto. Una orden puede tener varios resultados. La previsión, el resultado real y la existencia física son conceptos diferentes.

## Permiso

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| descripcion | String |
| modulo | String |
| accion | String |

## Rol

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| descripcion | String |
| activo | Boolean |

## Usuario

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| login | String |
| hashClave | String |
| estado | EstadoUsuario |
| intentosFallidos | Integer |
| correo | String |
| telefono | String? |
| creadoEn | DateTime |
| ultimoAcceso | DateTime? |

Operaciones: autenticar, bloquear.

## Cliente

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| tipo | String |
| telefono | String |
| direccion | String |
| identificacionFiscal | String |
| condicionHabitual | FormaPago |
| activo | Boolean |
| fechaAlta | DateTime |
| observaciones | String |

Operaciones: crear, editar, desactivar, consultarFicha.

## Cotizacion

| Atributo | Tipo |
|---|---|
| motivoRespuesta | String |
| codigo | String |
| id | UUID |
| version | Integer |
| fecha | DateTime |
| vigenteHasta | DateTime |
| canal | CanalSolicitud |
| estado | EstadoCotizacion |

Operaciones: presentar, aceptar, rechazar.

## DetalleCotizacion

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidad | Decimal |
| unidad | String |
| precioUnitario | Decimal |
| subtotal | Decimal |

## RegistroAuditoria

| Atributo | Tipo |
|---|---|
| id | UUID |
| operacion | String |
| entidad | String |
| entidadId | UUID |
| fecha | DateTime |

## Sesion

| Atributo | Tipo |
|---|---|
| id | UUID |
| inicio | DateTime |
| expira | DateTime |
| revocada | Boolean |

## OperacionPendiente

| Atributo | Tipo |
|---|---|
| id | UUID |
| claveUnica | String |
| tipo | String |
| fechaLocal | DateTime |
| versionBase | Integer |
| estado | EstadoSincronizacion |
| contenido | JSON |
| idRemoto | UUID? |
| detalleConflicto | String |
| entregaId | UUID |
| dispositivoId | String |
| evidenciaLocal | String? |

## Pedido

| Atributo | Tipo |
|---|---|
| motivoCancelacion | String |
| codigo | String |
| id | UUID |
| fecha | DateTime |
| fechaComprometida | DateTime |
| estadoComercial | EstadoComercial |
| estadoPreparacion | EstadoPreparacion |
| condicionPago | FormaPago |
| costoEstimadoConfirmado | Decimal |
| margenEstimadoConfirmado | Decimal |

Operaciones: calcularSaldo, autorizarDespacho.

## DetallePedido

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadSolicitada | Decimal |
| cantidadConfirmada | Decimal |
| unidad | String |
| precioAcordado | Decimal |
| costoReferenciaAcordado | Decimal |
| estado | EstadoDetalle |

## ControlSanitario

| Atributo | Tipo |
|---|---|
| id | UUID |
| fecha | DateTime |
| resultado | ResultadoSanitario |
| observacion | String |
| responsable | String |

## Animal

| Atributo | Tipo |
|---|---|
| id | UUID |
| identificacion | String |
| procedencia | String |
| proveedor | String |
| pesoIngreso | Decimal |
| estado | EstadoAnimal |

## OrdenProduccion

| Atributo | Tipo |
|---|---|
| id | UUID |
| estado | EstadoProduccion |
| inicioPrevisto | DateTime |
| finPrevisto | DateTime |
| inicioReal | DateTime? |
| finReal | DateTime? |
| codigo | String |
| fechaCreacion | DateTime |
| prioridad | String |
| observacion | String |

Operaciones: programar, iniciar, finalizar.

## Incidencia

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | String |
| motivo | String |
| estado | EstadoIncidencia |
| acuerdo | String |
| resolucionAnticipo | String |
| fechaResolucion | DateTime? |

## CargoPedido

| Atributo | Tipo |
|---|---|
| id | UUID |
| concepto | ConceptoCargo |
| descripcion | String |
| importe | Decimal |
| fecha | DateTime |

## Producto

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| nombre | String |
| presentacion | String |
| unidadVenta | String |
| descripcion | String |
| activo | Boolean |
| fechaAlta | DateTime |

Operaciones: crear, editar, desactivar, consultarDisponible.

## Pesaje

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | TipoPesaje |
| pesoBruto | Decimal |
| tara | Decimal |
| peso | Decimal |
| unidad | String |
| fecha | DateTime |
| origen | OrigenPesaje |
| observacion | String |

## FaeneoDesposte

| Atributo | Tipo |
|---|---|
| referenciaFaena | String |
| lugarFaena | String |
| inicioDesposte | DateTime? |
| finDesposte | DateTime? |
| observacionCortes | String |

Operaciones: validarControlSanitario, seleccionarCortes, registrarResultados.

## FabricacionDerivado

| Atributo | Tipo |
|---|---|
| formulaReferencia | String |
| versionFormula | String |
| descripcionProceso | String |
| resultadoCalidad | ResultadoCalidad |
| observacionCalidad | String |

Operaciones: seleccionarDerivado, validarInsumos, registrarConsumos, registrarResultado.

## Pago

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| tipo | TipoPago |
| importe | Decimal |
| fecha | DateTime |
| medio | String |
| estado | EstadoPago |

## AplicacionPago

| Atributo | Tipo |
|---|---|
| id | UUID |
| importe | Decimal |
| fecha | DateTime |

## PrecioProducto

| Atributo | Tipo |
|---|---|
| id | UUID |
| costoReferencia | Decimal |
| precioVenta | Decimal |
| vigenteDesde | DateTime |
| vigenteHasta | DateTime? |

## ControlFrio

| Atributo | Tipo |
|---|---|
| id | UUID |
| temperatura | Decimal |
| unidad | String |
| fecha | DateTime |
| responsable | String |
| evaluacion | String |

## Lote

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| fechaProduccion | DateTime |
| vencimiento | DateTime |
| estadoCalidad | EstadoCalidad |
| procedencia | String |
| unidad | String |

Operaciones: consultarProducto, evaluarAptitud.

## ConsumoInsumo

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidad | Decimal |
| unidad | String |
| fecha | DateTime |

## AcuerdoCredito

| Atributo | Tipo |
|---|---|
| id | UUID |
| importeAutorizado | Decimal |
| fechaAcuerdo | DateTime |
| vencimiento | DateTime |
| estado | EstadoCredito |

## SeguimientoCobro

| Atributo | Tipo |
|---|---|
| id | UUID |
| fechaGestion | DateTime? |
| resultado | String |
| proximaFecha | DateTime |
| estado | EstadoSeguimiento |

## ComprobanteFiscal

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| numeroFiscal | String? |
| fecha | DateTime? |
| estado | EstadoEmision |
| respuestaProveedor | String |

## Ubicacion

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| tipo | String |

## Existencia

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadFisica | Decimal |
| unidad | String |

Operaciones: cantidadReservada, disponible.

## MovimientoStock

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| tipo | TipoMovimiento |
| cantidad | Decimal |
| fecha | DateTime |
| motivo | String |

## Reserva

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| cantidad | Decimal |
| estado | EstadoReserva |
| fecha | DateTime |

## Entrega

| Atributo | Tipo |
|---|---|
| id | UUID |
| version | Integer |
| modalidad | ModalidadEntrega |
| estado | EstadoEntrega |
| fechaPrevista | DateTime |
| fechaReal | DateTime? |
| fechaConfirmacion | DateTime? |
| receptor | String? |
| observacionRecepcion | String? |
| ordenEnRuta | Integer? |

Operaciones: registrarRecepcion.

## Ruta

| Atributo | Tipo |
|---|---|
| id | UUID |
| fecha | DateTime |
| zona | String |
| estado | EstadoRuta |
| codigo | String |
| salidaPrevista | DateTime? |
| salidaReal | DateTime? |
| retornoReal | DateTime? |

## PrevisionProducto

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadEstimada | Decimal |
| unidad | String |

## EvidenciaEntrega

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | String |
| ubicacionArchivo | String |
| fecha | DateTime |

## ClasificacionProducto

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| nombre | String |
| familia | TipoProducto |
| descripcion | String |
| activo | Boolean |

Operaciones: crear, editar, desactivar.

## ResultadoProduccion

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| cantidadReal | Decimal? |
| unidad | String |
| fechaRegistro | DateTime |
| estado | EstadoResultado |
| observacion | String |

Operaciones: seleccionarProducto, confirmarPesaje, bloquear.

## Transporte

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| modalidad | TipoTransporte |
| transportista | String |
| contacto | String |
| placa | String |
| descripcionVehiculo | String |
| conservacion | String |
| capacidadReferencia | Decimal? |
| unidadCapacidad | String? |
| activo | Boolean |

Operaciones: crear, editar, desactivar.

## RecuperacionAcceso

| Atributo | Tipo |
|---|---|
| id | UUID |
| tokenHash | String |
| solicitadoEn | DateTime |
| expiraEn | DateTime |
| utilizadoEn | DateTime? |
| invalidado | Boolean |

Operaciones: validar, consumir.

## Relaciones

| Origen | Destino | Multiplicidad origen / destino | Relación |
|---|---|---|---|
| Rol | Permiso | 0..* / 1..* | Asociación · autoriza |
| Usuario | Rol | 0..* / 1..* | Asociación · asignado |
| Usuario | Sesion | 1 / 0..* | Composición |
| Usuario | RegistroAuditoria | 1 / 0..* | Asociación · registra |
| Usuario | OperacionPendiente | 1 / 0..* | Asociación · origina |
| Cliente | Usuario | 0..1 / 0..* | Asociación · cuentaPortal |
| Cliente | Cotizacion | 1 / 0..* | Asociación |
| Cotizacion | DetalleCotizacion | 1 / 0..* | Composición |
| Cotizacion | Cotizacion | 0..1 / 0..1 | Asociación · versionAnterior |
| Cotizacion | Pedido | 1 / 0..1 | Asociación · origina |
| Cliente | Pedido | 1 / 0..* | Asociación |
| Pedido | DetallePedido | 1 / 1..* | Composición |
| Producto | DetalleCotizacion | 1 / 0..* | Asociación |
| Producto | DetallePedido | 1 / 0..* | Asociación |
| Producto | PrecioProducto | 1 / 0..* | Composición |
| Pedido | CargoPedido | 1 / 0..* | Composición |
| Pedido | Incidencia | 1 / 0..* | Asociación |
| Pedido | Pago | 1 / 0..* | Asociación |
| Pago | AplicacionPago | 1 / 0..* | Composición |
| CargoPedido | AplicacionPago | 1 / 0..* | Asociación |
| Pedido | AcuerdoCredito | 1 / 0..* | Asociación |
| AcuerdoCredito | SeguimientoCobro | 1 / 0..* | Composición |
| Pedido | ComprobanteFiscal | 1 / 0..* | Asociación |
| DetallePedido | OrdenProduccion | 0..* / 0..* | Asociación · demandaPrevista |
| FaeneoDesposte | Animal | 0..1 / 1..* | Asociación · procesa |
| Animal | ControlSanitario | 1 / 0..* | Composición |
| OrdenProduccion | Pesaje | 0..1 / 0..* | Asociación |
| FabricacionDerivado | ConsumoInsumo | 1 / 0..* | Composición |
| Lote | ConsumoInsumo | 1 / 0..* | Asociación |
| Producto | Lote | 1 / 0..* | Asociación |
| Lote | Existencia | 1 / 0..* | Asociación |
| Ubicacion | Existencia | 1 / 0..* | Asociación |
| Existencia | MovimientoStock | 1 / 0..* | Asociación |
| Existencia | Reserva | 1 / 0..* | Asociación |
| DetallePedido | Reserva | 1 / 0..* | Asociación |
| Pedido | Entrega | 1 / 0..* | Asociación |
| Ruta | Entrega | 0..1 / 0..* | Agregación · agrupa |
| Entrega | EvidenciaEntrega | 1 / 0..* | Composición |
| Entrega | Pesaje | 0..1 / 0..* | Asociación |
| Entrega | ControlFrio | 0..1 / 0..* | Asociación |
| Lote | ControlFrio | 0..1 / 0..* | Asociación |
| Ubicacion | ControlFrio | 0..1 / 0..* | Asociación |
| Entrega | OperacionPendiente | 1 / 0..* | Asociación · recepcionPendiente |
| Usuario | Entrega | 0..1 / 0..* | Asociación · responsable |
| Animal | Pesaje | 0..1 / 0..* | Asociación |
| Lote | Pesaje | 0..1 / 0..* | Asociación |
| OrdenProduccion | PrevisionProducto | 1 / 1..* | Composición |
| Producto | PrevisionProducto | 1 / 0..* | Asociación |
| ConsumoInsumo | MovimientoStock | 0..1 / 1 | Asociación · descuenta |
| ClasificacionProducto | Producto | 1 / 0..* | Asociación · clasifica |
| OrdenProduccion | ResultadoProduccion | 1 / 0..* | Composición · obtiene |
| ResultadoProduccion | Lote | 0..1 / 1 | Asociación · identifica |
| ResultadoProduccion | Pesaje | 0..1 / 0..* | Asociación · confirma |
| Usuario | ResultadoProduccion | 1 / 0..* | Asociación · registra |
| Usuario | OrdenProduccion | 1 / 0..* | Asociación · responsable |
| Usuario | Pesaje | 1 / 0..* | Asociación · captura |
| Transporte | Ruta | 1 / 0..* | Asociación · asignado |
| Usuario | Ruta | 1 / 0..* | Asociación · responsable |
| Usuario | RecuperacionAcceso | 1 / 0..* | Composición |
| FaeneoDesposte | OrdenProduccion | — | Herencia |
| FabricacionDerivado | OrdenProduccion | — | Herencia |

Composición expresa propiedad exclusiva; no obliga a borrar historia comercial. Agregación de Ruta sobre Entrega permite reasignar una entrega. Las eliminaciones físicas deben respetar referencias y trazabilidad.

Restricciones: código de producto y referencia de resultado únicos; lote asociado a un solo producto; unidad compatible; un resultado confirmado exige pesaje válido. Producto inactivo conserva operaciones. Transporte inactivo conserva rutas. Precio/costo acordados no se recalculan al cambiar vigencias.

## Enumeraciones

- EstadoUsuario: ACTIVO, BLOQUEADO, DESHABILITADO.
- FormaPago: CONTADO, CREDITO_ACORDADO.
- CanalSolicitud: WHATSAPP, LOCAL, PORTAL.
- EstadoCotizacion: BORRADOR, PRESENTADA, ACEPTADA, RECHAZADA, VENCIDA.
- EstadoComercial: CONFIRMADO, PENDIENTE_ACUERDO, CANCELADO, CERRADO.
- EstadoPreparacion: PENDIENTE, PROGRAMADA, EN_PREPARACION, PREPARADO, BLOQUEADO.
- EstadoDetalle: PENDIENTE, RESERVADO, EN_PREPARACION, PREPARADO, CANCELADO.
- ResultadoSanitario: APTO, RECHAZADO.
- EstadoAnimal: RECIBIDO, APTO, RECHAZADO, FAENADO.
- EstadoProduccion: PROGRAMADA, PENDIENTE, EN_CURSO, COMPLETADA, BLOQUEADA, CANCELADA.
- EstadoIncidencia: ABIERTA, EN_ACUERDO, RESUELTA.
- ConceptoCargo: PRODUCTO, SERVICIO.
- TipoProducto: CARNE_FRESCA, DERIVADO, INSUMO.
- TipoPesaje: ANIMAL, CORTE, DERIVADO, DESPACHO, RECEPCION.
- OrigenPesaje: REGISTRO_MANUAL_AUTORIZADO.
- ResultadoCalidad: PENDIENTE, APROBADO, RECHAZADO.
- TipoPago: SENA, COBRO, ABONO.
- EstadoPago: REGISTRADO, ANULADO_CON_TRAZA.
- EstadoCalidad: PENDIENTE, APTO, BLOQUEADO.
- EstadoCredito: VIGENTE, VENCIDO, SALDADO, CANCELADO.
- EstadoSeguimiento: PENDIENTE, REALIZADO, CERRADO.
- EstadoEmision: PENDIENTE, EMITIDO, RECHAZADO, ANULADO.
- TipoMovimiento: ENTRADA, SALIDA, CONSUMO, AJUSTE.
- EstadoReserva: ACTIVA, CONFIRMADA, CONSUMIDA, LIBERADA.
- ModalidadEntrega: RETIRO, REPARTO_PROPIO, TRANSPORTE_EXTERNO.
- EstadoEntrega: PENDIENTE, PREPARADA, EN_TRASLADO, OBSERVADA, ENTREGADA, CANCELADA.
- EstadoRuta: PLANIFICADA, EN_CURSO, FINALIZADA.
- EstadoSincronizacion: PENDIENTE, ENVIANDO, CONFIRMADA, CONFLICTO, DESCARTADA.
- EstadoResultado: PENDIENTE_PESAJE, CONFIRMADO, BLOQUEADO.
- TipoTransporte: PROPIO, EXTERNO.

## Implementación del Sprint 1

API ASP.NET Core 10, EF Core y MySQL 8; web MVC online; Android Kotlin con acceso y base técnica. `codigo` es único por cotización/pedido. Cada nueva versión conserva su antecesora y tiene código propio. `motivoRespuesta` conserva el rechazo; `motivoCancelacion` conserva la cancelación. Las claves foráneas materializan las asociaciones del modelo. Los detalles del pedido conservan el precio aceptado y el costo vigente al confirmar. No se crea existencia al parametrizar productos.
