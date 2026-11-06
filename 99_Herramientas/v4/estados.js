const {project,M,D,V,E,text,rel,save}=require('./base'),{domain,enums}=require('./dominio'),{router}=require('./rutas');
const specs=[];
function S(file,cl,attr,initial,transitions,finals,note,activities={}){specs.push({file,cl,attr,initial,transitions,finals,note,activities});}
// Transición: origen, destino, evento, guarda, efecto.
S('01_Cotizacion','Cotizacion','estado','BORRADOR',[
 ['BORRADOR','PRESENTADA','presentar','detalles completos','guardar versión'],['PRESENTADA','BORRADOR','solicitarCambios','','crear nueva versión'],['PRESENTADA','ACEPTADA','aceptar','vigente','registrar respuesta'],['PRESENTADA','RECHAZADA','desistir','','registrar rechazo'],['PRESENTADA','VENCIDA','vencerVigencia'],['ACEPTADA','VENCIDA','vencerVigencia','sin pedido'],['ACEPTADA','fin','confirmarPedido','aceptación vigente','crear pedido']
 ],['RECHAZADA','VENCIDA'],'BORRADOR puede guardar una solicitud del portal. Rechazar o vencer no crea un pedido.',{PRESENTADA:'esperar respuesta del cliente'});
S('02_Pedido_Comercial','Pedido','estadoComercial','CONFIRMADO',[
 ['CONFIRMADO','PENDIENTE_ACUERDO','registrarIncidencia','afecta al pedido','suspender despacho'],['PENDIENTE_ACUERDO','CONFIRMADO','registrarAcuerdo','continuar; fecha aceptada','actualizar compromiso'],['PENDIENTE_ACUERDO','CANCELADO','registrarAcuerdo','cancelar; anticipo resuelto','liberar reservas'],['CONFIRMADO','CERRADO','revisarCierre','entrega cerrada; saldo = 0','registrar cierre']
 ],['CANCELADO','CERRADO'],'Precondición de creación: cotización aceptada y condiciones vigentes. Una entrega con deuda conserva el pedido abierto.');
S('03_Pedido_Preparacion','Pedido','estadoPreparacion','PENDIENTE',[
 ['PENDIENTE','PREPARADO','consolidarReservas','todo disponible y apto'],['PENDIENTE','PROGRAMADA','programarFaltantes','fecha aceptada'],['PROGRAMADA','EN_PREPARACION','iniciarPreparacion','recursos habilitados'],['EN_PREPARACION','PREPARADO','confirmarDetalles','todos completos y aptos'],['PROGRAMADA','BLOQUEADO','detectarImpedimento','','abrir incidencia'],['EN_PREPARACION','BLOQUEADO','rechazarControl','','abrir incidencia'],['BLOQUEADO','PENDIENTE','registrarSolucion','reemplazo o reprogramación aceptados'],['PREPARADO','BLOQUEADO','detectarDiferencia','antes de despacho']
 ],[],'La preparación no mide la deuda. Un pedido comercial CANCELADO inhibe nuevas acciones. El tiempo estimado no genera stock.',{PROGRAMADA:'esperar turno acordado'});
S('04_DetallePedido','DetallePedido','estado','PENDIENTE',[
 ['PENDIENTE','RESERVADO','reservar','stock apto suficiente'],['PENDIENTE','EN_PREPARACION','iniciarOrden','faltante programado'],['EN_PREPARACION','RESERVADO','registrarEntrada','lote apto; entrada física','reservar cantidad'],['RESERVADO','PREPARADO','verificarDetalle','cantidad y peso confirmados'],['RESERVADO','PENDIENTE','detectarFaltante','','liberar reserva afectada'],['PREPARADO','PENDIENTE','observarDetalle','antes del despacho'],['PENDIENTE','CANCELADO','cancelarDetalle','acuerdo registrado'],['EN_PREPARACION','CANCELADO','cancelarDetalle','acuerdo registrado'],['RESERVADO','CANCELADO','cancelarDetalle','acuerdo registrado','liberar reserva']
 ],['CANCELADO'],'Los faltantes vuelven a revisión. Preparar un detalle no significa que todo el pedido esté listo.');
S('05_Reserva','Reserva','estado','ACTIVA',[
 ['ACTIVA','CONFIRMADA','consolidarPedido','cantidades completas'],['CONFIRMADA','CONSUMIDA','registrarSalida','salida física autorizada','actualizar existencia una vez'],['ACTIVA','LIBERADA','cancelarOReemplazar','acuerdo registrado'],['CONFIRMADA','LIBERADA','cancelarOReemplazar','sin salida física']
 ],['CONSUMIDA','LIBERADA'],'Crear reserva exige stock apto. Reenviar la misma referencia recupera la reserva existente; confirmar no vuelve a restar stock.');
S('06_OrdenProduccion','OrdenProduccion','estado','PROGRAMADA',[
 ['PROGRAMADA','PENDIENTE','detectarFaltante','','solicitar recursos o nueva fecha'],['PENDIENTE','PROGRAMADA','reprogramar','recursos y fecha acordados'],['PROGRAMADA','EN_CURSO','iniciar','recursos aptos; turno llegado','registrar inicio real'],['EN_CURSO','COMPLETADA','finalizar','pesos y calidad válidos','registrar lotes y fin real'],['PROGRAMADA','BLOQUEADA','rechazarSanidad','','abrir incidencia'],['EN_CURSO','BLOQUEADA','rechazarCalidad','','bloquear lote'],['BLOQUEADA','PENDIENTE','registrarSolucion','recursos reemplazados'],['PROGRAMADA','CANCELADA','cancelar','acuerdo autorizado'],['PENDIENTE','CANCELADA','cancelar','acuerdo autorizado'],['BLOQUEADA','CANCELADA','cancelar','acuerdo autorizado']
 ],['COMPLETADA','CANCELADA'],'Aplica a FaeneoDesposte y FabricacionDerivado. Faeneo exige animal apto; fabricación exige insumos y calidad aprobada. CU12 registra la entrada física.',{PROGRAMADA:'esperar inicio previsto',EN_CURSO:'registrar avance y tiempos reales'});
S('07_Animal','Animal','estado','RECIBIDO',[
 ['RECIBIDO','APTO','registrarControl','resultado = APTO'],['RECIBIDO','RECHAZADO','registrarControl','resultado = RECHAZADO','aislar y trazar procedencia'],['APTO','FAENADO','finalizarFaeneo','control vigente apto','registrar pesos'],['APTO','RECHAZADO','registrarNuevoControl','resultado = RECHAZADO','bloquear orden']
 ],['RECHAZADO','FAENADO'],'No hay transición de un animal rechazado al faeneo. El responsable sanitario decide la aptitud.');
S('08_Lote','Lote','estadoCalidad','PENDIENTE',[
 ['PENDIENTE','APTO','aprobarEvaluacion','resultado conforme'],['PENDIENTE','BLOQUEADO','rechazarEvaluacion','','impedir reserva y despacho'],['APTO','BLOQUEADO','registrarIncidencia','sanidad o calidad afectadas','retener disponibilidad'],['BLOQUEADO','PENDIENTE','autorizarReevaluacion','corresponde según responsable']
 ],[],'Estar APTO no implica tener existencia física ni saldo disponible. Un bloqueo no se levanta automáticamente.');
S('09_Incidencia','Incidencia','estado','ABIERTA',[
 ['ABIERTA','EN_ACUERDO','comunicarProblema','','registrar propuesta'],['EN_ACUERDO','EN_ACUERDO','solicitarCambios','','actualizar propuesta'],['EN_ACUERDO','RESUELTA','registrarAcuerdo','solución y anticipo definidos','aplicar solución acordada']
 ],['RESUELTA'],'Sin acuerdo, la incidencia sigue abierta a negociación y no habilita el despacho.',{EN_ACUERDO:'esperar respuesta del cliente'});
S('10_Pago','Pago','estado','REGISTRADO',[
 ['REGISTRADO','ANULADO_CON_TRAZA','anularRegistro','error comprobado; autorizado','revertir aplicaciones y auditar']
 ],['ANULADO_CON_TRAZA'],'Se crea solo por dinero recibido e identificado. Cancelar un pedido no anula la seña ni ordena reembolso. Una anulación corrige un registro; la disposición del dinero exige acuerdo.');
S('11_AcuerdoCredito','AcuerdoCredito','estado','VIGENTE',[
 ['VIGENTE','VENCIDO','alcanzarVencimiento','saldo > 0','programar cobranza'],['VIGENTE','SALDADO','registrarPago','saldo = 0','cerrar seguimiento'],['VENCIDO','SALDADO','registrarPago','saldo = 0','cerrar seguimiento'],['VENCIDO','VIGENTE','renegociar','nueva fecha autorizada','auditar vencimiento anterior'],['VIGENTE','CANCELADO','sustituirAcuerdo','reemplazo autorizado y registrado','conservar deuda'],['VENCIDO','CANCELADO','sustituirAcuerdo','reemplazo autorizado y registrado','conservar deuda']
 ],['SALDADO','CANCELADO'],'Un abono parcial conserva VIGENTE o VENCIDO según la fecha. Cancelar el acuerdo por sustitución no perdona ni borra deuda.');
S('12_SeguimientoCobro','SeguimientoCobro','estado','PENDIENTE',[
 ['PENDIENTE','REALIZADO','contactarCliente','fecha de gestión alcanzada','registrar resultado'],['REALIZADO','PENDIENTE','reprogramar','saldo > 0','registrar próxima fecha'],['PENDIENTE','CERRADO','verificarSaldo','saldo = 0'],['REALIZADO','CERRADO','verificarSaldo','saldo = 0']
 ],['CERRADO'],'Esperar la siguiente fecha evita repetir contactos en un ciclo inmediato. La gestión de cobro no reabre una entrega.',{PENDIENTE:'esperar fecha o nuevo abono'});
S('13_Entrega','Entrega','estado','PENDIENTE',[
 ['PENDIENTE','PREPARADA','autorizarDespacho','pedido completo; pago habilitado','asignar retiro o ruta'],['PREPARADA','EN_TRASLADO','salir','modalidad = reparto','registrar salida'],['PREPARADA','ENTREGADA','confirmarRetiro','recepción y evidencia completas','registrar receptor y peso'],['EN_TRASLADO','ENTREGADA','confirmarRecepcion','servidor valida permisos, versión y evidencia','registrar recepción una vez'],['PREPARADA','OBSERVADA','registrarObservacion'],['EN_TRASLADO','OBSERVADA','registrarObservacion'],['OBSERVADA','PREPARADA','resolverObservacion','despacho nuevamente autorizado'],['PENDIENTE','CANCELADA','cancelar','acuerdo registrado'],['PREPARADA','CANCELADA','cancelar','sin salida física; autorizado'],['OBSERVADA','CANCELADA','cancelar','retorno registrado; autorizado']
 ],['ENTREGADA','CANCELADA'],'Pago habilitado: contado cubierto o crédito aprobado, con servicio resuelto según acuerdo. Solo recepción conforme validada por servidor pasa a ENTREGADA; una observación validada queda OBSERVADA. No cambia deuda. Una captura Android PENDIENTE conserva el estado central previo. Retiro web requiere conexión.');
S('14_Ruta','Ruta','estado','PLANIFICADA',[
 ['PLANIFICADA','EN_CURSO','iniciarReparto','entregas autorizadas'],['EN_CURSO','FINALIZADA','cerrarRecorrido','cada entrega ENTREGADA, OBSERVADA o CANCELADA; sin capturas pendientes']
 ],['FINALIZADA'],'Finalizar la ruta no declara entregadas las entregas observadas; estas conservan su resolución pendiente. El cierre central espera las recepciones Android pendientes de sincronización.');
S('15_ComprobanteFiscal','ComprobanteFiscal','estado','PENDIENTE',[
 ['PENDIENTE','EMITIDO','recibirRespuesta','aceptada por proveedor','guardar número fiscal'],['PENDIENTE','RECHAZADO','recibirRespuesta','rechazada por proveedor','guardar motivo'],['RECHAZADO','PENDIENTE','corregirYReintentar','datos corregidos','consultar referencia existente'],['PENDIENTE','PENDIENTE','recuperarConexion','respuesta no confirmada','consultar misma referencia'],['EMITIDO','ANULADO','confirmarAnulacion','proveedor confirma','guardar respuesta y motivo']
 ],['ANULADO'],'Sin respuesta, la emisión queda pendiente. Reintentar no genera automáticamente otra factura. La anulación se registra únicamente si la confirma el proveedor.');
S('16_OperacionPendiente','OperacionPendiente','estado','PENDIENTE',[
 ['PENDIENTE','ENVIANDO','sincronizar','Android abierto; conexión y sesión válidas','enviar clave, versión y evidencia'],['ENVIANDO','CONFIRMADA','recibirConfirmacion','guardada o ya existente','conservar identificador remoto'],['ENVIANDO','PENDIENTE','perderConexionOAgotarTiempo','','conservar operación y evidencia local'],['ENVIANDO','CONFLICTO','recibirConflicto','versión o condición incompatible','mostrar causa'],['CONFLICTO','PENDIENTE','resolverConflicto','corrección autorizada; entrega aún aplicable','conservar traza de resolución'],['CONFLICTO','DESCARTADA','descartarAutorizado','registro no aplicable; revisión registrada','conservar evidencia y traza']
 ],['CONFIRMADA','DESCARTADA'],'Solo recepción de entregas asignadas, autorizadas y descargadas en Android Kotlin. PENDIENTE local no cierra Entrega central. CONFIRMADA indica envío validado; Entrega puede quedar ENTREGADA u OBSERVADA. Inicio de sesión y descarga requieren conexión. Envío al reconectar con app abierta o pulsar Sincronizar; sin promesa de segundo plano. No se registran pedidos, cobros, créditos, stock ni facturas offline.');
S('17_Usuario','Usuario','estado','ACTIVO',[
 ['ACTIVO','BLOQUEADO','fallarAutenticacion','intentos >= límite configurado','registrar bloqueo'],['BLOQUEADO','ACTIVO','desbloquear','autorización válida','reiniciar contador'],['ACTIVO','DESHABILITADO','deshabilitar','administración autorizada','revocar sesiones'],['BLOQUEADO','DESHABILITADO','deshabilitar','administración autorizada','revocar sesiones'],['DESHABILITADO','ACTIVO','habilitar','administración autorizada']
 ],[],'Un acceso válido reinicia intentos. No se inventa un número de intentos: se usa el límite configurado.');
S('18_AlertaCliente','AlertaCliente','estado','ABIERTA',[
 ['ABIERTA','CONTACTADA','contactar','','registrar resultado'],['CONTACTADA','CERRADA','cerrarSeguimiento','gestión concluida'],['ABIERTA','CERRADA','registrarNuevaCompra','','cancelar aviso obsoleto']
 ],['CERRADA'],'Se crea al detectar tres días sin compras de un cliente habitual. Una alerta abierta se recupera en vez de duplicarse.');


const stateUpdates={
 '03_Pedido_Preparacion':'La orden vigente puede cubrir varios pedidos. PROGRAMADA no significa stock reservado: solo pasa a PREPARADO cuando todos los detalles tienen cantidades reales aptas recibidas y reservas verificadas. Un faltante real exige nueva fecha, reemplazo o cancelación acordados; no habilita despacho.',
 '04_DetallePedido':'Una previsión vinculada no crea reserva. Tras producción o recepción externa se comprueba stock físico apto y libre; si no alcanza, continúa EN_PREPARACION/PENDIENTE y se gestiona el faltante. La falta de plazo exige acuerdo; no se completa automáticamente.',
 '05_Reserva':'La reserva solo se crea con existencia física APTO y disponible suficiente. Confirmar no descuenta otra vez. La salida física se aplica una vez; producción prevista nunca es reservable. Reintento recupera referencia existente.',
 '06_OrdenProduccion':'Puede reponer stock o atender varios detalles. Antes de crear se revisan órdenes vigentes y sus previsiones por producto. COMPLETADA exige resultados reales por producto/lote/unidad y evaluación aprobada; no crea existencia. CU12 confirma recepción. Los consumos físicos de fabricación se descuentan una vez y se conservan aun si la calidad resulta rechazada. No hay tiempo ni rendimiento fijo.',
 '08_Lote':'Un resultado propio guarda cantidadProducida real y unidad, distinta de la previsión. APTO no significa existencia: CU12 registra recepción física por ubicación y referencia. BLOQUEADO puede conservar custodia física pero no disponibilidad. Sin aprobación no se reserva ni despacha.',
 '15_ComprobanteFiscal':'RF11 exige modalidad y proveedor confirmados. Sin integración habilitada permanece PENDIENTE con motivo; no simula emisión. Reintento consulta la misma referencia. Solo una respuesta válida del proveedor autoriza EMITIDO o ANULADO.',
 '18_AlertaCliente':'FUTURO · RF09 fuera de alcance actual según el Excel entregado. Este ciclo es diseño de una fase posterior; no se activa en la entrega actual. Una alerta abierta se recupera sin duplicarla.'
};
for(const s of specs)if(stateUpdates[s.file])s.note=stateUpdates[s.file];
const orden=specs.find(s=>s.file==='06_OrdenProduccion');
const fin=orden.transitions.find(t=>t[0]==='EN_CURSO'&&t[1]==='COMPLETADA');fin[3]='resultados reales y calidad aprobados';fin[4]='guardar lotes y fin real; sin entrada de stock';
const preparado=specs.find(s=>s.file==='03_Pedido_Preparacion');
preparado.transitions.push(['PROGRAMADA','PREPARADO','recibirReposicionExterna','entradas aptas y reservas completas']);
const fiscal=specs.find(s=>s.file==='15_ComprobanteFiscal');fiscal.transitions[0][3]='integración habilitada; aceptada por proveedor';

async function build(s){
 const {p,m}=project('SGCC — Estados de '+s.cl),{cs}=domain(m),attr=cs[s.cl].attributes.find(a=>a.name===s.attr);if(!attr||typeof attr.type==='string')throw Error('Falta enumeración '+s.cl+'.'+s.attr);
 const values=attr.type.literals.map(l=>l.name),sm=M('UMLStateMachine',s.cl+'.'+s.attr,cs[s.cl],'behaviors'),region=M('UMLRegion','Ciclo de vida',sm,'regions'),d=D(sm,'UMLStatechartDiagram','Estados · '+s.cl+'.'+s.attr);
 text(d,(s.file==='18_AlertaCliente'?'FUTURO · ':'')+s.cl+' · '+s.attr,90,20,2100,50,25);
 const vs={};
 // Recorrido en zigzag: deja corredores amplios para retornos y condiciones.
 const order=[s.initial,...values.filter(v=>v!==s.initial)];
 for(const[i,n]of order.entries()){const row=Math.floor(i/3),col=row%2===0?i%3:2-i%3,mm=M('UMLState',n,region,'vertices');if(s.activities[n])M('UMLActivity',s.activities[n],mm,'doActivities');const v=V(d,'UMLStateView',mm,230+col*760,230+row*520,350,140);v.fillColor=['BLOQUEADO','BLOQUEADA','RECHAZADO','RECHAZADA','OBSERVADA','CONFLICTO'].includes(n)?'#fff3e4':'#f1f6fa';vs[n]=v;}
 const initial=M('UMLPseudostate','',region,'vertices');initial.kind='initial';vs.inicio=V(d,'UMLPseudostateView',initial,90,280,30,30);
 const finalNeeded=s.finals.length||s.transitions.some(e=>e[1]==='fin');if(finalNeeded)vs.fin=V(d,'UMLFinalStateView',M('UMLFinalState','',region,'vertices'),1935,230+Math.ceil(values.length/3)*520,35,35);
 const edges=[['inicio',s.initial],...s.transitions,...s.finals.map(n=>[n,'fin'])];
 const route=router(Object.values(vs));
 for(const[a,z,event='',guard='',effect='']of edges){if(!vs[a]||!vs[z])throw Error('Estado desconocido '+a+' '+z);const r=rel(region,'UMLTransition',vs[a],vs[z],'','transitions');r.guard=guard;if(event){const ev=M('UMLEvent',event,r,'triggers');ev.kind='signal';}if(effect)M('UMLActivity',effect,r,'effects');let pts;
  if(a===z){const v=vs[a];pts=[[v.left+v.width,v.top+40],[v.left+v.width+210,v.top+40],[v.left+v.width+210,v.top+240],[v.left+v.width-50,v.top+240],[v.left+v.width-50,v.top+v.height]];}else pts=route(vs[a],vs[z]);
  const e=E(d,'UMLTransitionView',r,vs[a],vs[z],pts);e.nameLabel.font.size=15;e.nameLabel.wordWrap=true;e.nameLabel.width=390;e.nameLabel.distance=32;
 }
 const bottom=390+Math.ceil(values.length/3)*520;text(d,s.note,90,bottom,2070,220,17);
 sm.documentation=s.note+' Cada estado corresponde a un literal de '+attr.type.name+'. Las flechas llevan evento [guarda] / efecto cuando corresponde. Las transiciones sin etiqueta al final representan finalización del ciclo ya alcanzado. No confundir los estados de un objeto con actividades ejecutadas por varios actores.';
 await save(p,d,'04_Estados/'+s.file+'_Estados.mdj',{clase:s.cl,atributo:s.attr});
}
module.exports={specs,build};
