# Diccionario del modelo de clases

Modelo general con 40 clases, 63 asociaciones y 24 enumeraciones, alineado con el dominio de SGCPapi (`src/SGCP.Api/Dominio`). Los nombres de clase y de atributo son los de la API en camelCase; `[0..1]` marca un valor opcional (fecha, número o enumeración que admite nulo). Cada operación corresponde a un método real de un servicio de la API, indicado junto a cada operación. Las clases de interfaz/control de las secuencias y colaboraciones son participantes de análisis; no son tablas.

Cadena del producto obtenido: OrdenProduccion → ResultadoProduccion → Lote → Producto → ClasificacionProducto. La previsión, el resultado real y la existencia física son conceptos diferentes.

**SeguimientoCobro** (con la enumeración EstadoSeguimiento) es el seguimiento de cobros de Finanzas; se agregó a SGCPapi en v4.3.0 (endpoints `api/v1/seguimientos-cobro`).

## Permiso

Entidad Permiso de SGCPapi (Dominio/Entidades/Permiso.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| descripcion | String |
| modulo | String |
| accion | String |

Asociaciones:

- Permiso 1..* — 0..* Rol («autoriza»)

## Rol

Entidad Rol de SGCPapi (Dominio/Entidades/Rol.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| descripcion | String |
| activo | Boolean |

Asociaciones:

- Rol 0..* — 1..* Permiso («autoriza»)
- Rol 1..* — 0..* Usuario («asignado»)

## Usuario

Entidad Usuario de SGCPapi (Dominio/Entidades/Usuario.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| login | String |
| hashClave | String |
| estado | EstadoUsuario |
| intentosFallidos | Integer |
| correo | String |
| telefono | String |
| creadoEn | DateTime |
| ultimoAcceso | DateTime [0..1] |

Operaciones:

- `guardar()` — ServicioUsuarios.Guardar
- `estado()` — ServicioUsuarios.Estado
- `consulta()` — ServicioUsuarios.Consulta
- `registrar()` — ServicioAutenticacion.Registrar

Asociaciones:

- Usuario 0..* — 1..* Rol («asignado»)
- Usuario 1 — 0..* Sesion
- Usuario 1 — 0..* RegistroAuditoria («registra»)
- Usuario 1 — 0..* Recepcion («registra»)
- Usuario 0..* — 0..1 Cliente («cuentaPortal»)
- Usuario 1 — 0..* Entrega («responsable»)
- Usuario 1 — 0..* OrdenProduccion («responsable»)
- Usuario 1 — 0..* Pesaje («captura»)
- Usuario 1 — 0..* Ruta («responsable»)
- Usuario 1 — 0..* RecuperacionAcceso

## Cliente

Entidad Cliente de SGCPapi (Dominio/Entidades/Cliente.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| nombre | String |
| tipo | String |
| telefono | String |
| direccion | String |
| identificacionFiscal | String |
| tipoDocumento | String |
| condicionHabitual | FormaPago |
| activo | Boolean |
| fechaAlta | DateTime |
| observaciones | String |

Operaciones:

- `guardar()` — ServicioClientes.Guardar
- `estado()` — ServicioClientes.Estado
- `eliminar()` — ServicioClientes.Eliminar
- `saldos()` — ServicioFinanzas.Saldos

Asociaciones:

- Cliente 0..1 — 0..* Usuario («cuentaPortal»)
- Cliente 1 — 0..* Cotizacion
- Cliente 1 — 0..* Pedido
- Cliente 1 — 0..* Pago

## Cotizacion

Entidad Cotizacion de SGCPapi (Dominio/Entidades/Cotizacion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| version | Integer |
| fecha | DateTime |
| vigenteHasta | DateTime |
| canal | CanalSolicitud |
| estado | EstadoCotizacion |
| motivoRespuesta | String |

Operaciones:

- `guardar()` — ServicioCotizaciones.Guardar
- `cambiar()` — ServicioCotizaciones.Cambiar
- `nuevaVersion()` — ServicioCotizaciones.NuevaVersion
- `vencer()` — ServicioCotizaciones.Vencer
- `obtener()` — ServicioCotizaciones.Obtener

Asociaciones:

- Cotizacion 0..* — 1 Cliente
- Cotizacion 1 — 0..* DetalleCotizacion
- Cotizacion 1 — 0..1 Pedido («origina»)
- Cotizacion 0..1 — 0..1 Cotizacion («versionAnterior»)

## DetalleCotizacion

Entidad DetalleCotizacion de SGCPapi (Dominio/Entidades/DetalleCotizacion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidad | Decimal |
| unidad | String |
| precioUnitario | Decimal |
| subtotal | Decimal |

Asociaciones:

- DetalleCotizacion 0..* — 1 Cotizacion
- DetalleCotizacion 0..* — 1 Producto

## RegistroAuditoria

Entidad RegistroAuditoria de SGCPapi (Dominio/Entidades/RegistroAuditoria.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| operacion | String |
| entidad | String |
| fecha | DateTime |

Operaciones:

- `registrar()` — ServicioAuditoria.Registrar

Asociaciones:

- RegistroAuditoria 0..* — 1 Usuario («registra»)

## Sesion

Entidad Sesion de SGCPapi (Dominio/Entidades/Sesion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| inicio | DateTime |
| expira | DateTime |
| revocada | Boolean |

Operaciones:

- `acceder()` — ServicioAutenticacion.Acceder

Asociaciones:

- Sesion 0..* — 1 Usuario

## Recepcion

Entidad Recepcion de SGCPapi (Dominio/Entidades/Recepcion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| claveUnica | UUID |
| versionBase | Integer |
| fechaReal | DateTime |
| fechaSincronizacion | DateTime |
| pesoRecibido | Decimal |
| unidad | String |
| saldoPendienteAlConfirmar | Decimal [0..1] |
| conforme | Boolean |
| receptor | String |
| observacion | String |
| estado | EstadoRecepcion |
| huellaContenido | String |
| motivoConflicto | String |
| revisadaEn | DateTime [0..1] |
| resolucion | String |

Operaciones:

- `sincronizar()` — ServicioEntregas.Sincronizar
- `revisar()` — ServicioEntregas.Revisar

Asociaciones:

- Recepcion 0..* — 1 Usuario («registra»)
- Recepcion 1 — 0..* EvidenciaRecepcion
- Recepcion 0..* — 1 Entrega («confirma»)

## Pedido

Entidad Pedido de SGCPapi (Dominio/Entidades/Pedido.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| fecha | DateTime |
| fechaComprometida | DateTime |
| estadoComercial | EstadoComercial |
| estadoPreparacion | EstadoPreparacion |
| condicionPago | FormaPago |
| costoEstimadoConfirmado | Decimal |
| margenEstimadoConfirmado | Decimal |
| motivoCancelacion | String |

Operaciones:

- `confirmarAsync()` — ServicioConfirmarPedido.ConfirmarAsync
- `cancelar()` — ServicioConfirmarPedido.Cancelar
- `autorizarDespacho()` — ServicioFinanzas.AutorizarDespacho

Asociaciones:

- Pedido 0..1 — 1 Cotizacion («origina»)
- Pedido 0..* — 1 Cliente
- Pedido 1 — 1..* DetallePedido
- Pedido 1 — 0..* Cargo
- Pedido 1 — 0..* CondicionPago
- Pedido 1 — 0..* ComprobanteFiscal
- Pedido 1 — 0..* Entrega
- Pedido 1 — 0..* Sena

## DetallePedido

Entidad DetallePedido de SGCPapi (Dominio/Entidades/DetallePedido.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadSolicitada | Decimal |
| cantidadConfirmada | Decimal |
| unidad | String |
| precioAcordado | Decimal |
| costoReferenciaAcordado | Decimal |
| estado | EstadoDetalle |

Asociaciones:

- DetallePedido 1..* — 1 Pedido
- DetallePedido 0..* — 1 Producto
- DetallePedido 1 — 0..* Reserva
- DetallePedido 0..1 — 0..* Cargo

## ControlSanitario

Entidad ControlSanitario de SGCPapi (Dominio/Entidades/ControlSanitario.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| resultado | ResultadoSanitario |
| observacion | String |
| fecha | DateTime |

Operaciones:

- `sanidad()` — ServicioProduccion.Sanidad

Asociaciones:

- ControlSanitario 0..* — 1 Animal

## Animal

Entidad Animal de SGCPapi (Dominio/Entidades/Animal.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| identificacion | String |
| procedencia | String |
| proveedor | String |
| pesoIngreso | Decimal |
| estado | EstadoAnimal |
| fechaIngreso | DateTime |
| activo | Boolean |

Operaciones:

- `animal()` — ServicioProduccion.Animal
- `cambiarEstadoAnimal()` — ServicioProduccion.CambiarEstadoAnimal

Asociaciones:

- Animal 0..1 — 0..* OrdenProduccion («procesa»)
- Animal 1 — 0..* ControlSanitario
- Animal 0..1 — 0..* Incidencia

## OrdenProduccion

Entidad OrdenProduccion de SGCPapi (Dominio/Entidades/OrdenProduccion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| tipo | TipoOrdenProduccion |
| estado | EstadoOrdenProduccion |
| fechaCreacion | DateTime |
| inicioPrevisto | DateTime |
| finPrevisto | DateTime |
| inicioReal | DateTime [0..1] |
| finReal | DateTime [0..1] |
| observacion | String |

Operaciones:

- `crear()` — ServicioProduccion.Crear
- `iniciar()` — ServicioProduccion.Iniciar
- `confirmar()` — ServicioProduccion.Confirmar
- `anular()` — ServicioProduccion.Anular

Asociaciones:

- OrdenProduccion 0..* — 0..1 Animal («procesa»)
- OrdenProduccion 1 — 0..* InsumoProduccion
- OrdenProduccion 1 — 1..* PrevisionProducto
- OrdenProduccion 1 — 0..* ResultadoProduccion («obtiene»)
- OrdenProduccion 0..* — 1 Usuario («responsable»)
- OrdenProduccion 0..1 — 0..* Lote

## Incidencia

Entidad Incidencia de SGCPapi (Dominio/Entidades/Incidencia.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| motivo | String |
| fecha | DateTime |
| resuelta | Boolean |
| resolucion | String |
| resueltaEn | DateTime [0..1] |

Operaciones:

- `resolverIncidencia(motivo)` — ServicioInventario.ResolverIncidencia

Asociaciones:

- Incidencia 0..* — 0..1 Animal
- Incidencia 0..* — 0..1 Lote

## Cargo

Entidad Cargo de SGCPapi (Dominio/Entidades/Cargo.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | TipoCargo |
| concepto | String |
| importe | Decimal |
| acuerdoServicio | String |
| prestadoEn | DateTime [0..1] |
| fecha | DateTime |
| anulado | Boolean |
| motivoAnulacion | String |

Operaciones:

- `cargoServicio()` — ServicioFinanzas.CargoServicio
- `anularCargo()` — ServicioFinanzas.AnularCargo

Asociaciones:

- Cargo 0..* — 1 Pedido
- Cargo 1 — 0..* AplicacionPago
- Cargo 0..* — 0..1 DetallePedido

## Producto

Entidad Producto de SGCPapi (Dominio/Entidades/Producto.cs).

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

Operaciones:

- `producto()` — ServicioCatalogo.Producto
- `estadoProducto()` — ServicioCatalogo.EstadoProducto

Asociaciones:

- Producto 1 — 0..* DetalleCotizacion
- Producto 1 — 0..* DetallePedido
- Producto 1 — 0..* PrecioProducto
- Producto 1 — 0..* Lote
- Producto 1 — 0..* PrevisionProducto
- Producto 0..* — 1 ClasificacionProducto («clasifica»)
- Producto 1 — 0..* EntradaInventario
- Producto 1 — 0..* Existencia
- Producto 1 — 0..* Pesaje
- Producto 1 — 0..* ResultadoProduccion

## Pesaje

Entidad Pesaje de SGCPapi (Dominio/Entidades/Pesaje.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| pesoBruto | Decimal |
| tara | Decimal |
| neto | Decimal |
| unidad | String |
| fecha | DateTime |
| observacion | String |

Operaciones:

- `pesar()` — ServicioInventario.Pesar

Asociaciones:

- Pesaje 0..* — 1 Lote
- Pesaje 0..* — 1 Usuario («captura»)
- Pesaje 1 — 0..* EntradaInventario
- Pesaje 0..* — 1 Producto

## Pago

Entidad Pago de SGCPapi (Dominio/Entidades/Pago.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| importe | Decimal |
| fecha | DateTime |
| medio | String |
| tipo | TipoPago |
| anulado | Boolean |
| motivoAnulacion | String |

Operaciones:

- `pago()` — ServicioFinanzas.Pago
- `anularPago()` — ServicioFinanzas.AnularPago

Asociaciones:

- Pago 0..* — 1 Cliente
- Pago 1 — 0..* AplicacionPago
- Pago 1 — 0..* Sena

## AplicacionPago

Entidad AplicacionPago de SGCPapi (Dominio/Entidades/AplicacionPago.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| importe | Decimal |
| fecha | DateTime |

Asociaciones:

- AplicacionPago 0..* — 1 Pago
- AplicacionPago 0..* — 1 Cargo
- AplicacionPago 0..* — 0..1 Sena

## PrecioProducto

Entidad PrecioProducto de SGCPapi (Dominio/Entidades/PrecioProducto.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| costoReferencia | Decimal |
| precioVenta | Decimal |
| vigenteDesde | DateTime |
| vigenteHasta | DateTime [0..1] |

Operaciones:

- `vigente()` — ServicioPrecios.Vigente
- `abrir()` — ServicioPrecios.Abrir
- `editar()` — ServicioPrecios.Editar
- `finalizar()` — ServicioPrecios.Finalizar

Asociaciones:

- PrecioProducto 0..* — 1 Producto

## ControlFrio

Entidad ControlFrio de SGCPapi (Dominio/Entidades/ControlFrio.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| unidad | String |
| temperatura | Decimal |
| ubicacion | String |
| evaluacion | EvaluacionFrio |
| observacion | String |
| fecha | DateTime |

Operaciones:

- `frio()` — ServicioInventario.Frio

Asociaciones:

- ControlFrio 0..* — 0..1 Entrega
- ControlFrio 0..* — 0..1 Lote

## Lote

Entidad Lote de SGCPapi (Dominio/Entidades/Lote.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| fechaProduccion | DateTime |
| vencimiento | DateTime |
| unidad | String |
| procedencia | String |
| referenciaExterna | String |
| estado | EstadoLote |

Operaciones:

- `loteApto()` — ServicioInventario.LoteApto
- `loteExterno()` — ServicioInventario.LoteExterno
- `bloquearLote()` — ServicioInventario.BloquearLote
- `rechazarLote()` — ServicioInventario.RechazarLote

Asociaciones:

- Lote 0..* — 1 Producto
- Lote 1 — 0..* Existencia
- Lote 0..1 — 0..* ControlFrio
- Lote 1 — 0..* Pesaje
- Lote 1 — 0..1 ResultadoProduccion («identifica»)
- Lote 1 — 0..* EntradaInventario
- Lote 0..1 — 0..* Incidencia
- Lote 0..* — 0..1 OrdenProduccion

## InsumoProduccion

Entidad InsumoProduccion de SGCPapi (Dominio/Entidades/InsumoProduccion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | UUID |
| cantidad | Decimal |
| unidad | String |
| fecha | DateTime |

Operaciones:

- `consumir()` — ServicioProduccion.Consumir

Asociaciones:

- InsumoProduccion 0..* — 1 OrdenProduccion
- InsumoProduccion 0..* — 1 Existencia

## CondicionPago

Entidad CondicionPago de SGCPapi (Dominio/Entidades/CondicionPago.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| modalidad | FormaPago |
| importeAutorizado | Decimal |
| fechaAcuerdo | DateTime |
| vencimiento | DateTime [0..1] |
| activa | Boolean |

Operaciones:

- `condicion()` — ServicioFinanzas.Condicion

Asociaciones:

- CondicionPago 0..* — 1 Pedido
- CondicionPago 1 — 0..* SeguimientoCobro

## SeguimientoCobro

Entidad SeguimientoCobro de SGCPapi (Dominio/Entidades/SeguimientoCobro.cs): seguimiento de cobros de Finanzas.

| Atributo | Tipo |
|---|---|
| id | UUID |
| fechaGestion | DateTime [0..1] |
| resultado | String |
| proximaFecha | DateTime |
| estado | EstadoSeguimiento |

Operaciones:

- `crearSeguimiento(condicionId, proximaFecha)` — ServicioFinanzas.CrearSeguimiento
- `registrarGestion(resultado, proximaFecha)` — ServicioFinanzas.RegistrarGestion
- `cerrarSeguimiento()` — ServicioFinanzas.CerrarSeguimiento

Asociaciones:

- SeguimientoCobro 0..* — 1 CondicionPago

## ComprobanteFiscal

Entidad ComprobanteFiscal de SGCPapi (Dominio/Entidades/ComprobanteFiscal.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| referenciaUnica | String |
| estado | String |
| numeroFiscal | String |
| respuestaProveedor | String |
| fecha | DateTime |

Operaciones:

- `registrar()` — ServicioFiscal.Registrar

Asociaciones:

- ComprobanteFiscal 0..* — 1 Pedido

## Existencia

Entidad Existencia de SGCPapi (Dominio/Entidades/Existencia.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| ubicacion | String |
| cantidadFisica | Decimal |

Operaciones:

- `disponible()` — ServicioInventario.Disponible

Asociaciones:

- Existencia 1 — 0..* InsumoProduccion
- Existencia 0..* — 1 Lote
- Existencia 1 — 0..* MovimientoStock
- Existencia 1 — 0..* Reserva
- Existencia 1 — 0..* EntradaInventario
- Existencia 0..* — 1 Producto

## MovimientoStock

Entidad MovimientoStock de SGCPapi (Dominio/Entidades/MovimientoStock.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | String |
| cantidad | Decimal |
| fecha | DateTime |
| motivo | String |

Operaciones:

- `movimiento()` — ServicioInventario.Movimiento

Asociaciones:

- MovimientoStock 0..* — 1 Existencia

## Reserva

Entidad Reserva de SGCPapi (Dominio/Entidades/Reserva.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidad | Decimal |
| estado | EstadoReserva |
| fecha | DateTime |
| motivoLiberacion | String |

Operaciones:

- `reservar()` — ServicioInventario.Reservar
- `liberar()` — ServicioInventario.Liberar

Asociaciones:

- Reserva 0..* — 1 Existencia
- Reserva 0..* — 1 DetallePedido

## Entrega

Entidad Entrega de SGCPapi (Dominio/Entidades/Entrega.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| modalidad | ModalidadEntrega |
| estado | EstadoEntrega |
| version | Integer |
| fechaPrevista | DateTime |
| fechaReal | DateTime [0..1] |
| fechaConfirmacion | DateTime [0..1] |
| receptor | String |
| observacionRecepcion | String |
| ordenEnRuta | Integer |

Operaciones:

- `preparar()` — ServicioEntregas.Preparar
- `despachar()` — ServicioEntregas.Despachar
- `reasignar()` — ServicioEntregas.Reasignar
- `obtener()` — ServicioEntregas.Obtener

Asociaciones:

- Entrega 0..* — 1 Pedido
- Entrega 0..* — 0..1 Ruta («agrupa»)
- Entrega 0..1 — 0..* ControlFrio
- Entrega 1 — 0..* Recepcion («confirma»)
- Entrega 0..* — 1 Usuario («responsable»)

## Ruta

Entidad Ruta de SGCPapi (Dominio/Entidades/Ruta.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| fecha | DateTime |
| zona | String |
| estado | EstadoRuta |
| salidaReal | DateTime [0..1] |
| retornoReal | DateTime [0..1] |

Operaciones:

- `crearRuta()` — ServicioEntregas.CrearRuta
- `finalizarRuta()` — ServicioEntregas.FinalizarRuta

Asociaciones:

- Ruta 0..1 — 0..* Entrega («agrupa»)
- Ruta 0..* — 1 Transporte («asignado»)
- Ruta 0..* — 1 Usuario («responsable»)

## PrevisionProducto

Entidad PrevisionProducto de SGCPapi (Dominio/Entidades/PrevisionProducto.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadEstimada | Decimal |
| unidad | String |

Asociaciones:

- PrevisionProducto 1..* — 1 OrdenProduccion
- PrevisionProducto 0..* — 1 Producto

## EvidenciaRecepcion

Entidad EvidenciaRecepcion de SGCPapi (Dominio/Entidades/EvidenciaRecepcion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| tipo | String |
| contenido | Bytes |
| sha256 | String |

Asociaciones:

- EvidenciaRecepcion 0..* — 1 Recepcion

## ClasificacionProducto

Entidad ClasificacionProducto de SGCPapi (Dominio/Entidades/ClasificacionProducto.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| codigo | String |
| nombre | String |
| familia | TipoProducto |
| descripcion | String |
| activo | Boolean |

Operaciones:

- `clasificacion()` — ServicioCatalogo.Clasificacion
- `estadoClasificacion()` — ServicioCatalogo.EstadoClasificacion

Asociaciones:

- ClasificacionProducto 1 — 0..* Producto («clasifica»)

## ResultadoProduccion

Entidad ResultadoProduccion de SGCPapi (Dominio/Entidades/ResultadoProduccion.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| cantidadReal | Decimal [0..1] |
| estado | EstadoResultado |
| fechaRegistro | DateTime |

Operaciones:

- `crear()` — FabricaResultado.Crear

Asociaciones:

- ResultadoProduccion 0..* — 1 OrdenProduccion («obtiene»)
- ResultadoProduccion 0..1 — 1 Lote («identifica»)
- ResultadoProduccion 0..* — 1 Producto

## Transporte

Entidad Transporte de SGCPapi (Dominio/Entidades/Transporte.cs).

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
| activo | Boolean |

Operaciones:

- `transporte()` — ServicioEntregas.Transporte
- `estadoTransporte()` — ServicioEntregas.EstadoTransporte

Asociaciones:

- Transporte 1 — 0..* Ruta («asignado»)

## RecuperacionAcceso

Entidad RecuperacionAcceso de SGCPapi (Dominio/Entidades/RecuperacionAcceso.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| tokenHash | String |
| solicitadoEn | DateTime |
| expiraEn | DateTime |
| utilizadoEn | DateTime [0..1] |
| invalidado | Boolean |

Operaciones:

- `recuperar()` — ServicioAutenticacion.Recuperar
- `restablecer()` — ServicioAutenticacion.Restablecer

Asociaciones:

- RecuperacionAcceso 0..* — 1 Usuario

## EntradaInventario

Entidad EntradaInventario de SGCPapi (Dominio/Entidades/EntradaInventario.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| fecha | DateTime |
| cantidad | Decimal |
| anulada | Boolean |
| anuladaEn | DateTime [0..1] |
| motivoAnulacion | String |

Operaciones:

- `entrada()` — ServicioInventario.Entrada
- `anularEntrada()` — ServicioInventario.AnularEntrada

Asociaciones:

- EntradaInventario 0..* — 1 Existencia
- EntradaInventario 0..* — 1 Lote
- EntradaInventario 0..* — 1 Pesaje
- EntradaInventario 0..* — 1 Producto

## Sena

Entidad Sena de SGCPapi (Dominio/Entidades/Sena.cs).

| Atributo | Tipo |
|---|---|
| id | UUID |
| acuerdoResolucion | String |
| resueltaEn | DateTime [0..1] |

Operaciones:

- `sena()` — ServicioFinanzas.Sena
- `aplicarSena()` — ServicioFinanzas.AplicarSena
- `resolverSena()` — ServicioFinanzas.ResolverSena

Asociaciones:

- Sena 0..1 — 0..* AplicacionPago
- Sena 0..* — 1 Pago
- Sena 0..* — 1 Pedido

## Enumeraciones

- EstadoUsuario: ACTIVO, BLOQUEADO, DESHABILITADO.
- FormaPago: CONTADO, CREDITO_ACORDADO.
- CanalSolicitud: WHATSAPP, LOCAL, PORTAL.
- EstadoCotizacion: BORRADOR, PRESENTADA, ACEPTADA, RECHAZADA, VENCIDA.
- EstadoComercial: CONFIRMADO, PENDIENTE_ACUERDO, CANCELADO, CERRADO.
- EstadoPreparacion: PENDIENTE, PROGRAMADA, EN_PREPARACION, PREPARADO, BLOQUEADO.
- EstadoDetalle: PENDIENTE, RESERVADO, EN_PREPARACION, PREPARADO, CANCELADO.
- ResultadoSanitario: APROBADO, RECHAZADO.
- EstadoAnimal: PENDIENTE, APTO, BLOQUEADO, FAENADO.
- TipoProducto: CARNE_FRESCA, DERIVADO, INSUMO.
- TipoPago: PAGO, SENA.
- EstadoSeguimiento: PENDIENTE, REALIZADO, CERRADO.
- EstadoReserva: ACTIVA, LIBERADA, CONSUMIDA.
- ModalidadEntrega: RETIRO_LOCAL, DOMICILIO.
- EstadoEntrega: PREPARADA, DESPACHADA, ENTREGADA, OBSERVADA, CANCELADA.
- EstadoRuta: PLANIFICADA, EN_REPARTO, FINALIZADA.
- EstadoResultado: PENDIENTE_PESAJE, CONFIRMADO, BLOQUEADO.
- TipoTransporte: PROPIO, EXTERNO.
- EstadoLote: APTO, BLOQUEADO.
- EstadoOrdenProduccion: PLANIFICADA, EN_PROCESO, CONFIRMADA, BLOQUEADA, ANULADA.
- EstadoRecepcion: CONFIRMADA, CONFLICTO, DESCARTADA.
- EvaluacionFrio: APTO, OBSERVADO, RECHAZADO.
- TipoCargo: PRODUCTO, SERVICIO.
- TipoOrdenProduccion: FAENEO, FABRICACION.
