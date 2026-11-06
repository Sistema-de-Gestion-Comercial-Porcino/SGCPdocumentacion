const {M}=require('./base');
// Una definición compartida por clases, instantáneas y máquinas de estados.
const defs={
 Permiso:[0,0,['codigo:String','descripcion:String']],
 Rol:[1,0,['id:UUID','nombre:String']],
 Usuario:[2,0,['id:UUID','nombre:String','login:String','hashClave:String','estado:EstadoUsuario','intentosFallidos:Integer'],['autenticar','bloquear']],
 Cliente:[3,0,['id:UUID','nombre:String','tipo:String','telefono:String','direccion:String','identificacionFiscal:String','condicionHabitual:FormaPago','esHabitual:Boolean']],
 Cotizacion:[4,0,['id:UUID','version:Integer','fecha:DateTime','vigenteHasta:DateTime','canal:CanalSolicitud','estado:EstadoCotizacion'],['presentar','aceptar','rechazar']],
 DetalleCotizacion:[5,0,['id:UUID','cantidad:Decimal','unidad:String','precioUnitario:Decimal','subtotal:Decimal']],
 RegistroAuditoria:[0,1,['id:UUID','operacion:String','entidad:String','entidadId:UUID','fecha:DateTime']],
 Sesion:[1,1,['id:UUID','inicio:DateTime','expira:DateTime','revocada:Boolean']],
 OperacionPendiente:[2,1,['id:UUID','claveUnica:String','tipo:String','fechaLocal:DateTime','versionBase:Integer','estado:EstadoSincronizacion','contenido:JSON','idRemoto:UUID?','detalleConflicto:String','entregaId:UUID','dispositivoId:String','evidenciaLocal:String?']],
 AlertaCliente:[3,1,['id:UUID','fecha:DateTime','estado:EstadoAlerta','resultadoContacto:String']],
 Pedido:[4,1,['id:UUID','fecha:DateTime','fechaComprometida:DateTime','estadoComercial:EstadoComercial','estadoPreparacion:EstadoPreparacion','condicionPago:FormaPago','costoEstimadoConfirmado:Decimal','margenEstimadoConfirmado:Decimal'],['calcularSaldo','autorizarDespacho']],
 DetallePedido:[5,1,['id:UUID','cantidadSolicitada:Decimal','cantidadConfirmada:Decimal','unidad:String','precioAcordado:Decimal','costoReferenciaAcordado:Decimal','estado:EstadoDetalle']],
 ControlSanitario:[0,2,['id:UUID','fecha:DateTime','resultado:ResultadoSanitario','observacion:String','responsable:String']],
 Animal:[1,2,['id:UUID','identificacion:String','procedencia:String','proveedor:String','pesoIngreso:Decimal','estado:EstadoAnimal']],
 OrdenProduccion:[2,2,['id:UUID','estado:EstadoProduccion','inicioPrevisto:DateTime','finPrevisto:DateTime','inicioReal:DateTime?','finReal:DateTime?'],['programar','iniciar','finalizar']],
 Incidencia:[3,2,['id:UUID','tipo:String','motivo:String','estado:EstadoIncidencia','acuerdo:String','resolucionAnticipo:String','fechaResolucion:DateTime?']],
 CargoPedido:[4,2,['id:UUID','concepto:ConceptoCargo','descripcion:String','importe:Decimal','fecha:DateTime']],
 Producto:[5,2,['id:UUID','nombre:String','tipo:TipoProducto','presentacion:String','unidadVenta:String','activo:Boolean']],
 Pesaje:[0,3,['id:UUID','tipo:TipoPesaje','peso:Decimal','unidad:String','fecha:DateTime','origen:OrigenPesaje']],
 FaeneoDesposte:[1,3,['observacionCortes:String'],['validarControlSanitario']],
 FabricacionDerivado:[2,3,['formulaReferencia:String','resultadoCalidad:ResultadoCalidad'],['validarInsumos']],
 Pago:[3,3,['id:UUID','referenciaUnica:String','tipo:TipoPago','importe:Decimal','fecha:DateTime','medio:String','estado:EstadoPago']],
 AplicacionPago:[4,3,['id:UUID','importe:Decimal','fecha:DateTime']],
 PrecioProducto:[5,3,['id:UUID','costoReferencia:Decimal','precioVenta:Decimal','vigenteDesde:DateTime','vigenteHasta:DateTime?']],
 ControlFrio:[0,4,['id:UUID','temperatura:Decimal','unidad:String','fecha:DateTime','responsable:String','evaluacion:String']],
 Lote:[1,4,['id:UUID','codigo:String','fechaProduccion:DateTime','vencimiento:DateTime','estadoCalidad:EstadoCalidad','procedencia:String','cantidadProducida:Decimal?','unidad:String']],
 ConsumoInsumo:[2,4,['id:UUID','cantidad:Decimal','unidad:String','fecha:DateTime']],
 AcuerdoCredito:[3,4,['id:UUID','importeAutorizado:Decimal','fechaAcuerdo:DateTime','vencimiento:DateTime','estado:EstadoCredito']],
 SeguimientoCobro:[4,4,['id:UUID','fechaGestion:DateTime?','resultado:String','proximaFecha:DateTime','estado:EstadoSeguimiento']],
 ComprobanteFiscal:[5,4,['id:UUID','referenciaUnica:String','numeroFiscal:String?','fecha:DateTime?','estado:EstadoEmision','respuestaProveedor:String']],
 Ubicacion:[0,5,['id:UUID','nombre:String','tipo:String']],
 Existencia:[1,5,['id:UUID','cantidadFisica:Decimal','unidad:String'],['cantidadReservada','disponible']],
 MovimientoStock:[2,5,['id:UUID','referenciaUnica:String','tipo:TipoMovimiento','cantidad:Decimal','fecha:DateTime','motivo:String']],
 Reserva:[3,5,['id:UUID','referenciaUnica:String','cantidad:Decimal','estado:EstadoReserva','fecha:DateTime']],
 Entrega:[4,5,['id:UUID','version:Integer','modalidad:ModalidadEntrega','estado:EstadoEntrega','fechaPrevista:DateTime','fechaReal:DateTime?','fechaConfirmacion:DateTime?','receptor:String?','observacionRecepcion:String?','ordenEnRuta:Integer?'],['registrarRecepcion']],
 Ruta:[5,5,['id:UUID','fecha:DateTime','transportista:String','vehiculo:String','zona:String','estado:EstadoRuta']],
 PrevisionProducto:[1,6,['id:UUID','cantidadEstimada:Decimal','unidad:String']],
 EvidenciaEntrega:[4,6,['id:UUID','tipo:String','ubicacionArchivo:String','fecha:DateTime']]
};
const enums={
 EstadoUsuario:['ACTIVO','BLOQUEADO','DESHABILITADO'],FormaPago:['CONTADO','CREDITO_ACORDADO'],CanalSolicitud:['WHATSAPP','LOCAL','PORTAL'],
 EstadoCotizacion:['BORRADOR','PRESENTADA','ACEPTADA','RECHAZADA','VENCIDA'],EstadoComercial:['CONFIRMADO','PENDIENTE_ACUERDO','CANCELADO','CERRADO'],
 EstadoPreparacion:['PENDIENTE','PROGRAMADA','EN_PREPARACION','PREPARADO','BLOQUEADO'],EstadoDetalle:['PENDIENTE','RESERVADO','EN_PREPARACION','PREPARADO','CANCELADO'],
 ResultadoSanitario:['APTO','RECHAZADO'],EstadoAnimal:['RECIBIDO','APTO','RECHAZADO','FAENADO'],EstadoProduccion:['PROGRAMADA','PENDIENTE','EN_CURSO','COMPLETADA','BLOQUEADA','CANCELADA'],
 EstadoIncidencia:['ABIERTA','EN_ACUERDO','RESUELTA'],ConceptoCargo:['PRODUCTO','SERVICIO'],TipoProducto:['CARNE_FRESCA','DERIVADO','INSUMO'],TipoPesaje:['ANIMAL','CORTE','DESPACHO','RECEPCION'],OrigenPesaje:['BALANZA','REGISTRO_MANUAL_AUTORIZADO'],
 ResultadoCalidad:['PENDIENTE','APROBADO','RECHAZADO'],TipoPago:['SENA','COBRO','ABONO'],EstadoPago:['REGISTRADO','ANULADO_CON_TRAZA'],EstadoCalidad:['PENDIENTE','APTO','BLOQUEADO'],EstadoCredito:['VIGENTE','VENCIDO','SALDADO','CANCELADO'],EstadoSeguimiento:['PENDIENTE','REALIZADO','CERRADO'],
 EstadoEmision:['PENDIENTE','EMITIDO','RECHAZADO','ANULADO'],TipoMovimiento:['ENTRADA','SALIDA','CONSUMO','AJUSTE'],EstadoReserva:['ACTIVA','CONFIRMADA','CONSUMIDA','LIBERADA'],ModalidadEntrega:['RETIRO','REPARTO_PROPIO','TRANSPORTE_EXTERNO'],EstadoEntrega:['PENDIENTE','PREPARADA','EN_TRASLADO','OBSERVADA','ENTREGADA','CANCELADA'],EstadoRuta:['PLANIFICADA','EN_CURSO','FINALIZADA'],EstadoAlerta:['ABIERTA','CONTACTADA','CERRADA'],EstadoSincronizacion:['PENDIENTE','ENVIANDO','CONFIRMADA','CONFLICTO','DESCARTADA']
};
// A, B, multiplicidades en A/B, nombre, agregación en A.
const links=[
 ['Rol','Permiso','0..*','1..*','autoriza'],['Usuario','Rol','0..*','1..*','asignado'],['Usuario','Sesion','1','0..*','','composite'],['Usuario','RegistroAuditoria','1','0..*','registra'],['Usuario','OperacionPendiente','1','0..*','origina'],['Cliente','Usuario','0..1','0..*','cuentaPortal'],['Cliente','AlertaCliente','1','0..*'],
 ['Cliente','Cotizacion','1','0..*'],['Cotizacion','DetalleCotizacion','1','0..*','','composite'],['Cotizacion','Pedido','1','0..1','origina'],['Cliente','Pedido','1','0..*'],['Pedido','DetallePedido','1','1..*','','composite'],['Producto','DetalleCotizacion','1','0..*'],['Producto','DetallePedido','1','0..*'],['Producto','PrecioProducto','1','0..*','','composite'],
 ['Pedido','CargoPedido','1','0..*','','composite'],['Pedido','Incidencia','1','0..*'],['Pedido','Pago','1','0..*'],['Pago','AplicacionPago','1','0..*','','composite'],['CargoPedido','AplicacionPago','1','0..*'],['Pedido','AcuerdoCredito','1','0..*'],['AcuerdoCredito','SeguimientoCobro','1','0..*','','composite'],['Pedido','ComprobanteFiscal','1','0..*'],
 ['DetallePedido','OrdenProduccion','0..*','0..*','demandaPrevista'],['FaeneoDesposte','Animal','0..1','1..*','procesa'],['Animal','ControlSanitario','1','0..*','','composite'],['OrdenProduccion','Pesaje','0..1','0..*'],['OrdenProduccion','Lote','0..1','0..*','produce'],['FabricacionDerivado','ConsumoInsumo','1','0..*','','composite'],['Lote','ConsumoInsumo','1','0..*'],['Producto','Lote','1','0..*'],
 ['Lote','Existencia','1','0..*'],['Ubicacion','Existencia','1','0..*'],['Existencia','MovimientoStock','1','0..*'],['Existencia','Reserva','1','0..*'],['DetallePedido','Reserva','1','0..*'],
 ['Pedido','Entrega','1','0..*'],['Ruta','Entrega','0..1','0..*','agrupa','shared'],['Entrega','EvidenciaEntrega','1','0..*','','composite'],['Entrega','Pesaje','0..1','0..*'],['Entrega','ControlFrio','0..1','0..*'],['Lote','ControlFrio','0..1','0..*'],['Ubicacion','ControlFrio','0..1','0..*']
];
links.push(['Entrega','OperacionPendiente','1','0..*','recepcionPendiente'],['Usuario','Entrega','0..1','0..*','responsable']);
links.push(['Animal','Pesaje','0..1','0..*'],['Lote','Pesaje','0..1','0..*']);
links.push(['OrdenProduccion','PrevisionProducto','1','1..*','','composite'],['Producto','PrevisionProducto','1','0..*'],['ConsumoInsumo','MovimientoStock','0..1','1','descuenta']);
const inheritance=[['FaeneoDesposte','OrdenProduccion'],['FabricacionDerivado','OrdenProduccion']];
function domain(m){
 const cs={},es={},rels=[];const ep=M('UMLPackage','Tipos de datos',m);
 for(const[n,values]of Object.entries(enums)){es[n]=M('UMLEnumeration',n,ep);for(const s of values)M('UMLEnumerationLiteral',s,es[n],'literals');}
 for(const[n,[x,y,attrs,ops=[]]]of Object.entries(defs)){const c=M('UMLClass',n,m);cs[n]=c;c.isAbstract=n==='OrdenProduccion';for(const s of attrs){const[a,type]=s.split(':'),v=M('UMLAttribute',a,c,'attributes'),t=type.replace('?','');v.type=es[t]||t;v.visibility='private';if(type.endsWith('?'))v.multiplicity='0..1';}for(const s of ops)M('UMLOperation',s,c,'operations');}
 for(const[a,b,ma,mb,n='',ag='none']of links){const r=M('UMLAssociation',n,m);r.end1.reference=cs[a];r.end2.reference=cs[b];r.end1.multiplicity=ma;r.end2.multiplicity=mb;r.end1.aggregation=ag;r.end1.navigable='unspecified';r.end2.navigable='unspecified';rels.push(r);}
 for(const[a,b]of inheritance){const r=M('UMLGeneralization','',m);r.source=cs[a];r.target=cs[b];rels.push(r);}
 cs.AlertaCliente.stereotype='futuro';cs.AlertaCliente.documentation='RF09 fuera de alcance actual; diseño futuro.';
 cs.Cliente.attributes.find(a=>a.name==='esHabitual').documentation='Marca reservada para RF09 futuro; no activa alertas en esta entrega.';
 cs.PrevisionProducto.documentation='Estimación manual por producto de una orden; no genera existencia ni reserva. Se revisa junto a demanda vinculada antes de reutilizar una orden.';
 cs.Lote.documentation='cantidadProducida es el resultado real propio; recepción externa conserva origen y movimientos. Aptitud y existencia se controlan por separado.';
 cs.Pedido.documentation='Costo y margen estimados al confirmar: se conservan con los costos por detalle; no son rentabilidad real por animal.';
 return {cs,es,rels};
}
function attribute(cs,cl,name){const a=cs[cl].attributes.find(x=>x.name===name);if(a)return a;const b=inheritance.find(x=>x[0]===cl);return b?attribute(cs,b[1],name):null;}
function isA(a,b){return a===b||inheritance.some(([x,y])=>x===a&&isA(y,b));}
module.exports={defs,enums,links,inheritance,domain,attribute,isA};
