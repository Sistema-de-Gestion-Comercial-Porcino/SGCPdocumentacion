// Un proceso y un diagrama por modelo. Los carriles se repiten visualmente por tramo;
// todos referencian al mismo participante y los mismos roles. Enlaces BPMN reemplazan
// únicamente las continuaciones largas: cada código tiene un único evento receptor.
const b=require('./v4/base'),{M,D,V,E,text,project,contain,points,rt,fs,path}=b;
const ROOT=b.ROOT,T=b.T;
const TMP=process.env.SGCC_BPMN_STAGE||'/tmp/sgcc_bpmn_entrega_20261026';
fs.mkdirSync(TMP,{recursive:true});
const PW=2780,LH=370,GAP=80,ROW=1900;
function specs(p){
 const S=[];let c;
 function panel(num,title,roles,note=''){c={num,title,roles,note,nodes:[],edges:[]};S.push(c)}
 function n(id,kind,role,col,row,label,code=''){c.nodes.push({id,kind,role,col,row,label,code});}
 function e(a,z,label=''){c.edges.push({a,z,label});}
 const v='Ventas / cobranza',a='Almacén',pr='Producción',de='Responsable de entrega',sys='SGCC';
 const sa=p?sys:v,ap=p?sys:a;
 panel(1,'COTIZACIÓN Y ACEPTACIÓN',p?[v,sys]:[v],p?'Web y portal online; WhatsApp se atiende manualmente. Solo una cotización vigente aceptada crea pedido.':'Operación manual: conversación, lista de precios y anotaciones. Una solicitud rechazada no inicia preparación.');
 n('i','start',v,0,0,'Inicio');n('precios','task',v,1,0,p?'Fijar costo de referencia y precio por producto':'Revisar costos y definir precios');
 n('margen','gate',v,2,0,'¿Margen aceptado?');n('ajuste','task',v,2,1,'Ajustar costo o precio');
 n('publicar','task',sa,3,0,p?'Publicar lista vigente':'Anotar lista vigente');
 n('solicitud','task',v,4,0,p?'Identificar cliente y cotizar la solicitud':'Recibir solicitud y ofrecer precio / condiciones');
 n('acepta','gate',v,5,0,'¿Cliente acepta?');n('cambios','gate',v,5,1,'¿Pide cambios?');
 n('cambiar','task',v,4,1,'Ajustar y volver a cotizar');n('rechazar','task',v,6,1,'Anotar rechazo; no crear pedido');n('finRechazo','end',v,7,1,'Sin pedido');
 n('confirmar','task',sa,6,0,p?'Crear pedido; conservar costos, precios y fecha':'Anotar pedido aceptado y fecha');
 n('linkSeña','throw',sa,7,0,'SEÑA → 2','SEÑA');
 e('i','precios');e('precios','margen');e('margen','publicar','Sí');e('margen','ajuste','No');e('ajuste','precios');e('publicar','solicitud');e('solicitud','acepta');e('acepta','confirmar','Sí');e('acepta','cambios','No');e('cambios','cambiar','Sí');e('cambiar','solicitud');e('cambios','rechazar','No');e('rechazar','finRechazo');e('confirmar','linkSeña');
 panel(2,'SEÑA, STOCK Y FECHA',p?[v,a,pr,sys]:[v,a,pr],p?'Existencia disponible = físico APTO menos reservas. La previsión de producción no se reserva. La reposición manual puede existir sin pedido.':'Consultar existencias reales. Esperar producción o recepción requiere acordar fecha; un faltante nunca se declara listo.');
 n('inSeña','catch',v,0,0,'SEÑA','SEÑA');n('recibeSeña','gate',v,1,0,'¿Recibe seña?');n('registrarSeña','task',sa,2,1,p?'Registrar referencia de seña una sola vez':'Anotar seña a cuenta');
 n('stock','catch',a,0,0,'STOCK','STOCK');n('mergeStock','merge',a,1,0,'');n('consultar','task',a,2,0,p?'Consultar físico APTO y reservas del detalle':'Revisar stock apto del detalle');n('hay','gate',a,3,0,'¿Alcanza el stock?');n('reservar','task',ap,4,0,p?'Reservar cantidad disponible una sola vez':'Separar producto para el pedido');
 n('mas','gate',a,5,0,'¿Quedan detalles?');n('otro','throw',a,5,1,'STOCK ↺','STOCK');n('listo','task',a,6,0,'Verificar todos los detalles, cantidades y aptitud');n('pago','throw',a,7,0,'COBRO → 5','COBRO');
 n('reponer','task',pr,3,0,p?'Revisar órdenes vigentes y recepción externa; evitar duplicar':'Revisar preparación o recepción necesaria');n('fecha','task',v,4,1,'Proponer fecha viable al cliente');n('aceptaFecha','gate',v,5,1,'¿Acepta el plazo?');n('tipoOrigen','gate',pr,5,1,'¿Producción nueva?');
 n('producir','throw',pr,6,1,'PRODUCIR → 3','PRODUCIR');n('espera','throw',pr,7,0,'RECIBIR → 4','RECIBIR');n('incFecha','throw',v,6,1,'ACUERDO → 4','ACUERDO');
 e('inSeña','recibeSeña');e('recibeSeña','registrarSeña','Sí');e('recibeSeña','mergeStock','No');e('registrarSeña','mergeStock');e('stock','mergeStock');e('mergeStock','consultar');e('consultar','hay');e('hay','reservar','Sí');e('reservar','mas');e('mas','otro','Sí');e('mas','listo','No');e('listo','pago');e('hay','reponer','No');e('reponer','fecha');e('fecha','aceptaFecha');e('aceptaFecha','incFecha','No');e('aceptaFecha','tipoOrigen','Sí');e('tipoOrigen','producir','Sí');e('tipoOrigen','espera','No: vigente / externa');
 panel(3,'PREPARACIÓN Y CONTROL',p?[pr,a,sys]:[pr,a],p?'Producción registra resultados REALES por producto, lote y unidad; varios productos por animal/orden. No se fija duración ni rendimiento. Consumos físicos únicos aunque se rechace el derivado.':'Faeneo y fabricación son alternativas según el producto. Control humano previo, espera real, pesos y calidad; no se omite el tiempo de preparación.');
 n('prodIn','catch',pr,0,0,'PRODUCIR','PRODUCIR');n('plan','task',pr,1,0,p?'Programar orden, previsiones y tiempos; esperar turno':'Programar preparación y esperar turno acordado');n('derivado','gate',pr,2,0,'¿Es derivado?');
 n('sanidad','task',pr,3,0,'Identificar animal y registrar control sanitario humano');n('apto','gate',pr,4,0,'¿Animal APTO?');n('faenar','task',pr,5,0,p?'Faenar / despostar; guardar pesos y lotes por producto':'Faenar / despostar; registrar pesos y cortes');
 n('insumos','gate',a,2,0,'¿Insumos aptos disponibles?');n('abastecer','task',a,2,1,'Abastecer y recibir insumos; esperar disponibilidad');n('fabricar','task',pr,3,1,p?'Fabricar y descontar consumos reales por lote':'Fabricar con carne e ingredientes disponibles');n('calidad','gate',pr,4,1,'¿Resultado conforme?');n('lotes','task',pr,5,1,'Registrar cantidad real del derivado y su lote');
 n('termino','merge',pr,6,0,'');n('finReal','task',pr,7,0,'Registrar fin real; entregar lotes a Almacén');n('recibirProd','throw',a,7,0,'RECIBIR → 4','RECIBIR');
 n('bloquear','task',a,5,1,'Bloquear animal / lote; anotar motivo e incidencia');n('incProd','throw',a,6,1,'ACUERDO → 4','ACUERDO');
 e('prodIn','plan');e('plan','derivado');e('derivado','sanidad','No: carne fresca');e('sanidad','apto');e('apto','faenar','Sí');e('apto','bloquear','No');e('faenar','termino');e('derivado','insumos','Sí');e('insumos','fabricar','Sí');e('insumos','abastecer','No');e('abastecer','insumos');e('fabricar','calidad');e('calidad','lotes','Sí');e('calidad','bloquear','No');e('lotes','termino');e('termino','finReal');e('finReal','recibirProd');e('bloquear','incProd');
 panel(4,'RECEPCIÓN DE STOCK E INCIDENCIAS',p?[a,v,sys]:[a,v],p?'Un lote bloqueado puede permanecer en custodia, pero no se reserva. El ingreso suma la cantidad física una vez; el stock final puede ser menor que la previsión.':'Registrar lo recibido y revisar el faltante. La resolución de la seña depende del acuerdo; no hay pérdida ni devolución automática.');
 n('recibirIn','catch',a,0,0,'RECIBIR','RECIBIR');n('esperar','wait',a,1,0,'Esperar recepción o fecha límite');n('recibido','gate',a,2,0,'¿Producto recibido?');n('revisar','task',a,3,0,'Verificar producto, lote, cantidad real y aptitud');n('loteApto','gate',a,4,0,'¿Recepción apta?');n('ingreso','task',ap,5,0,p?'Registrar entrada física única por lote y ubicación':'Anotar entrada física y existencia');n('stockBack','throw',ap,6,0,'STOCK → 2','STOCK');
 n('retraso','task',a,2,1,'Anotar retraso al vencer la fecha; informar faltante');n('retener','task',a,4,1,'Retener lote rechazado y registrar incidencia');
 n('acuerdoIn','catch',v,0,0,'ACUERDO','ACUERDO');n('mergeInc','merge',v,1,0,'');n('negociar','task',v,2,0,'Comunicar incidencia y acordar solución y efecto de seña');n('hayAcuerdo','gate',v,3,0,'¿Hay acuerdo?');n('pendiente','wait',v,3,1,'Esperar respuesta; pedido bloqueado para despacho');
 n('continua','gate',v,4,0,'¿Continúa el pedido?');n('actualizar','task',v,5,0,'Registrar sustitución / fecha y revisar reservas');n('retStock','throw',v,6,0,'STOCK → 2','STOCK');n('cancelar','task',v,5,1,'Cancelar; liberar reservas y resolver seña según acuerdo');n('finCancel','end',v,6,1,'Cancelado');
 e('recibirIn','esperar');e('esperar','recibido');e('recibido','revisar','Sí');e('recibido','retraso','No: fecha vencida');e('revisar','loteApto');e('loteApto','ingreso','Sí');e('ingreso','stockBack');e('loteApto','retener','No');e('retraso','mergeInc');e('retener','mergeInc');e('acuerdoIn','mergeInc');e('mergeInc','negociar');e('negociar','hayAcuerdo');e('hayAcuerdo','continua','Sí');e('hayAcuerdo','pendiente','No');e('pendiente','negociar');e('continua','actualizar','Sí');e('actualizar','retStock');e('continua','cancelar','No');e('cancelar','finCancel');
 panel(5,'LIQUIDACIÓN Y CONDICIÓN DE PAGO',p?[v,sys]:[v],p?'El sistema separa producto y servicio. Margen estimado con costos de referencia históricos; no prorratea costo del animal. Cada pago se identifica por referencia.':'Se mantiene por separado el cobro de carne y del servicio efectivamente prestado. La seña se descuenta una vez del saldo.');
 n('cobroIn','catch',v,0,0,'COBRO','COBRO');n('totales','task',sa,1,0,'Calcular productos; añadir solo servicio acordado y prestado');n('medio','gate',v,2,0,'¿Venta a crédito?');n('contado','task',v,3,0,'Recibir saldo al contado, considerando seña');n('credito','task',v,3,1,'Autorizar crédito y vencimiento; resolver servicio por separado');n('mergeDin','merge',v,4,0,'');n('dinero','gate',v,5,0,'¿Dinero recibido?');n('registro','task',sa,5,1,p?'Registrar pago por referencia y concepto; recuperar duplicado':'Anotar dinero recibido por concepto; actualizar saldo');n('habilita','gate',v,6,0,'¿Despacho habilitado?');n('esperaPago','task',v,6,1,'Mantener pendiente; esperar pago o acuerdo autorizado');n('aDespacho','throw',v,7,0,'DESPACHO → 6','DESPACHO');
 e('cobroIn','totales');e('totales','medio');e('medio','credito','Sí');e('medio','contado','No');e('credito','mergeDin');e('contado','mergeDin');e('mergeDin','dinero');e('dinero','registro','Sí');e('registro','habilita');e('dinero','habilita','No');e('habilita','aDespacho','Sí');e('habilita','esperaPago','No');e('esperaPago','medio');
 panel(6,'COMPROBANTE Y DESPACHO',p?[v,de,sys]:[v,de],p?'Despacho: pedido completo, stock APTO y contado cubierto o crédito aprobado. Hoja de despacho no acredita recepción. Control de frío online registra conservación/transporte, no temperatura corporal.':'Coordinar retiro o transporte y conservación del producto. El comprobante y el despacho no saldan por sí mismos la deuda.');
 n('despIn','catch',v,0,0,'DESPACHO','DESPACHO');
 n('fiscal','gate',v,1,0,p?'¿Integración fiscal habilitada?':'¿Corresponde comprobante?');n('emitir','task',sa,2,0,p?'Solicitar / consultar con misma referencia; guardar respuesta':'Emitir comprobante según práctica aplicable');n('fiscalPend','task',v,2,1,p?'Dejar emisión pendiente; no simular factura':'Anotar condición del comprobante');n('mergeDesp','merge',de,3,0,'');n('local','gate',de,4,0,'¿Retiro local?');n('retiro','task',de,5,0,'Preparar retiro y hoja de despacho');n('ruta','task',de,5,1,p?'Asignar ruta / responsable; descargar entregas Android online':'Coordinar ruta, transporte y responsable');n('frio','task',de,6,1,p?'Registrar lectura de frío y evaluación humana':'Verificar conservación y cadena de frío');n('mergeEntrega','merge',de,6,0,'');n('aEntrega','throw',de,7,0,'RECEPCIÓN → 7','RECEPCIÓN');
 e('despIn','fiscal');e('fiscal','emitir','Sí');e('fiscal','fiscalPend','No');e('emitir','mergeDesp');e('fiscalPend','mergeDesp');e('mergeDesp','local');e('local','retiro','Sí');e('local','ruta','No');e('retiro','mergeEntrega');e('ruta','frio');e('frio','mergeEntrega');e('mergeEntrega','aEntrega');
 panel(7,'ENTREGA Y RECEPCIÓN',p?[de,sys]:[de],p?'Android: solo entregas asignadas, autorizadas y descargadas. Sin señal, recepción local PENDIENTE. Reintentar misma clave; conflicto se revisa sin sobrescribir. Web requiere conexión.':'El comprador verifica recepción y peso. Una observación exige corrección; cerrar la entrega conserva cualquier deuda pendiente.');
 n('entIn','catch',de,0,0,'RECEPCIÓN','RECEPCIÓN');n('entregar','task',de,1,0,p?'Entregar; capturar receptor, peso, fecha y evidencia':'Entregar; verificar peso y receptor');
 if(p){
  n('confirmSync','gate',sys,2,0,'¿Servidor confirma recepción?');n('sinSync','task',de,2,1,'Conservar pendiente; esperar conexión y sesión válida');n('sync','task',sys,3,1,'Validar clave y versión; revisar conflictos con autorización');
  n('conforme','gate',sys,4,0,'¿Recepción conforme?');n('observada','task',de,4,1,'Registrar OBSERVADA y acordar corrección de entrega');n('cerrar','task',sys,5,0,'Confirmar ENTREGADA y generar constancia');
  e('entregar','confirmSync');e('confirmSync','conforme','Sí');e('confirmSync','sinSync','No');e('sinSync','sync');e('sync','confirmSync');
 }else{
  n('conforme','gate',de,3,0,'¿Recepción conforme?');n('observada','task',de,3,1,'Anotar observación y acordar corrección');n('cerrar','task',de,5,0,'Anotar entrega y constancia de recepción');e('entregar','conforme');
 }
 n('saldoNext','throw',de,6,0,'SALDO → 8','SALDO');e('entIn','entregar');e('conforme','cerrar','Sí');e('conforme','observada','No');e('observada','entregar');e('cerrar','saldoNext');
 panel(8,'SALDO Y COBRANZA',p?[v,sys]:[v],p?'Cierre de ruta: resultados centrales registrados y ninguna captura por enviar. Una entrega OBSERVADA conserva resolución pendiente. Cobrar no reabre la entrega.':'Entrega y deuda se controlan por separado. El proceso comercial termina al cerrar la entrega y cubrir el saldo.');
 n('saldoIn','catch',v,0,0,'SALDO','SALDO');n('saldo','task',sa,1,0,'Revisar cargos, seña y pagos aplicados');n('deuda','gate',v,2,0,'¿Queda saldo?');n('cerrado','task',v,3,0,'Registrar pedido y saldo cerrados');n('fin','end',v,4,0,'Fin');n('mantener','task',v,2,1,'Conservar deuda y vencimiento; entrega cerrada');n('fechaCobro','wait',v,3,1,'Esperar fecha de gestión o nuevo abono');n('contactar','task',v,4,1,'Contactar cliente y anotar gestión');n('abono','gate',v,5,1,'¿Se recibió abono?');n('registrarAbono','task',sa,6,1,p?'Registrar abono único por concepto; recalcular saldo':'Anotar abono y recalcular saldo');n('reagendar','task',v,5,0,'Acordar próxima fecha de seguimiento');
 e('saldoIn','saldo');e('saldo','deuda');e('deuda','cerrado','No');e('cerrado','fin');e('deuda','mantener','Sí');e('mantener','fechaCobro');e('fechaCobro','contactar');e('contactar','abono');e('abono','registrarAbono','Sí');e('registrarAbono','saldo');e('abono','reagendar','No');e('reagendar','fechaCobro');
 return S;
}

function placeConditions(d){
 const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas;
 const scratch=new Doc({size:[100,100],margin:0}),canvas=new Canvas(scratch);
 const overlap=(a,c,pad=5)=>Math.min(a.left+a.width+pad,c.left+c.width)>Math.max(a.left-pad,c.left)&&Math.min(a.top+a.height+pad,c.top+c.height)>Math.max(a.top-pad,c.top);
 const obstacles=d.ownedViews.filter(v=>['BPMNTaskView','BPMNGatewayView','BPMNEventView','UMLTextView'].includes(v.constructor.name));
 for(const v of d.ownedViews)if(['BPMNGatewayView','BPMNEventView'].includes(v.constructor.name)&&v.nameLabel.visible)obstacles.push(v.nameLabel);
 const placed=[];
 const edges=d.ownedViews.filter(v=>['BPMNSequenceFlowView','BPMNMessageFlowView'].includes(v.constructor.name));
 const segments=e=>Array.from({length:e.points.count()-1},(_,i)=>[e.points.getPoint(i),e.points.getPoint(i+1)]);
 const dist=(x,y,a,z)=>{const dx=z.x-a.x,dy=z.y-a.y,t=Math.max(0,Math.min(1,((x-a.x)*dx+(y-a.y)*dy)/(dx*dx+dy*dy||1)));return Math.hypot(x-a.x-t*dx,y-a.y-t*dy)};
 function cuts(l,a,z){const left=l.left-5,right=l.left+l.width+5,top=l.top-5,bottom=l.top+l.height+5;return a.x===z.x?a.x>left&&a.x<right&&Math.min(Math.max(a.y,z.y),bottom)>Math.max(Math.min(a.y,z.y),top):a.y>top&&a.y<bottom&&Math.min(Math.max(a.x,z.x),right)>Math.max(Math.min(a.x,z.x),left)}
 function place(l,e,x,y){
  l.edgePosition=T.EdgeParasiticView.EP_MIDDLE;
  const ps=e.points;let i=Math.floor(ps.count()/2);if(ps.count()%2===0)i--;
  const a=ps.getPoint(i).copy(),z=ps.getPoint(i+1);if(ps.count()%2===0){a.x=(a.x+z.x)/2;a.y=(a.y+z.y)/2;}
  const q=T.Coord.getPointAwayLine(a,z,0,1000),theta=Math.atan2(-q.y,q.x);l.distance=Math.hypot(x-a.x,y-a.y);l.alpha=Math.atan2(-(y-a.y),x-a.x)-theta;l.arrangeObject(canvas);
 }
 for(const e of d.ownedViews.filter(v=>v.constructor.name==='BPMNSequenceFlowView'&&v.model.name)){
  const l=e.nameLabel;l.fontColor=e.lineColor;let best=null;const pts=Array.from({length:e.points.count()},(_,i)=>e.points.getPoint(i));let distance=0;
  for(let i=1;i<pts.length;i++){const a=pts[i-1],z=pts[i],len=Math.abs(z.x-a.x)+Math.abs(z.y-a.y);if(len<15){distance+=len;continue;}
   for(const f of [.25,.5,.75])for(const off of [20,-20,32,-32,48,-48]){
    const x=a.x+(z.x-a.x)*f+(a.x===z.x?off:0),y=a.y+(z.y-a.y)*f+(a.y===z.y?off:0);place(l,e,x,y);
    const hit=[...obstacles,...placed].filter(n=>overlap(l,n)).length;
    const cx=l.left+l.width/2,cy=l.top+l.height/2,own=dist(cx,cy,a,z);
    let cut=0,other=Infinity;for(const edge of edges)for(const [u,v]of segments(edge)){if(cuts(l,u,v))cut++;if(edge!==e)other=Math.min(other,dist(cx,cy,u,v));}
    const ambiguity=Math.max(0,own+12-other);
    const score=hit*1000000+cut*100000+ambiguity*10000+distance+len*f+Math.abs(off);if(!best||score<best.score)best={score,x,y};
   }
   distance+=len;
  }
  if(best)place(l,e,best.x,best.y);placed.push(l);
 }
 scratch.end();
}

async function build(proposed){
 const title='BPMN — Modelo '+(proposed?'propuesto':'actual');const {p,m}=project(title,'BPMNProcess'),d=D(m,'BPMNDiagram',title);
 const participant=M('BPMNParticipant','Chanchería',m),buyer=M('BPMNParticipant','Comprador',m),lanes={};const stages=specs(proposed),meta=[];
 text(d,title+' · recorrido completo',60,25,5000,60,32);
 text(d,'LECTURA: 1 > 2 > 5 > 6 > 7 > 8. Si falta stock: 2 > 3 / 4 > 2. Incidencias: 4. Las flechas de enlace con el mismo nombre continúan el mismo proceso, sin líneas largas.',60,100,11200,70,21);
 text(d,'Cada tramo muestra de nuevo los carriles necesarios de la misma chanchería. No son procesos separados. Todas las decisiones tienen sus salidas rotuladas.',60,165,11200,50,18);
 for(const stage of stages){
  const k=stage.num-1,ox=60+(k%4)*(PW+GAP),oy=260+Math.floor(k/4)*ROW;
  const ph=stage.roles.length*LH+60;
  text(d,String(stage.num).padStart(2,'0')+' · '+stage.title,ox,oy,PW,55,25);
  const pool=V(d,'BPMNPoolView',participant,ox,oy+160,PW,ph);pool.fillColor='#ffffff';pool.isVertical=false;
  const laneVs={};for(const [i,role]of stage.roles.entries()){
   lanes[role]||=M('BPMNLane',role,participant);const lv=V(d,'BPMNLaneView',lanes[role],ox+35,oy+160+i*LH,PW-35,LH);lv.isVertical=false;contain(pool,lv);laneVs[role]=lv;
  }
  const map={},labels=[];
  for(const n of stage.nodes){
   const li=stage.roles.indexOf(n.role);if(li<0)throw Error('Rol no dibujado '+n.role);
   const cx=ox+180+n.col*330,cy=oy+160+li*LH+100+n.row*180;
   let type,vtype,w,h;
   if(n.kind==='task'){type=proposed?(n.role==='SGCC'?'BPMNServiceTask':'BPMNUserTask'):'BPMNManualTask';vtype='BPMNTaskView';w=240;h=100;}
   else if(['gate','merge'].includes(n.kind)){type='BPMNExclusiveGateway';vtype='BPMNGatewayView';w=65;h=65;}
   else{type=n.kind==='start'?'BPMNStartEvent':n.kind==='end'?'BPMNEndEvent':n.kind==='throw'?'BPMNIntermediateThrowEvent':'BPMNIntermediateCatchEvent';vtype='BPMNEventView';w=45;h=45;}
   const destinations={'SEÑA':2,'STOCK':2,'PRODUCIR':3,'RECIBIR':4,'ACUERDO':4,'COBRO':5,'DESPACHO':6,'RECEPCIÓN':7,'SALDO':8};
   const model=M(type,n.code?n.code+' ['+destinations[n.code]+']':n.kind==='task'?n.label:'',lanes[n.role]);model.id='T'+stage.num+'_'+n.id;
   model.documentation=n.label+(n.code?' · Enlace de continuidad '+n.code:'');
   if(['throw','catch'].includes(n.kind))M('BPMNLinkEventDefinition',n.code,model,'eventDefinitions');
   if(n.kind==='wait')M('BPMNConditionalEventDefinition','Condición indicada en el evento',model,'eventDefinitions');
   const v=V(d,vtype,model,cx-w/2,cy-h/2,w,h);v.font.size=16;v.fillColor=n.kind==='gate'?'#fff1c4':n.role==='SGCC'?'#dff2e8':n.kind==='task'?'#f0f5fb':'#ffffff';contain(laneVs[n.role],v);
   if(v.nameLabel){v.nameLabel.font.size=16;v.nameLabel.wordWrap=true;v.nameLabel.width=w-16;if(n.kind!=='task'){v.nameLabel.width=240;v.nameLabel.height=55;v.nameLabel.distance=65;}}
   if(!['task','merge','catch','throw'].includes(n.kind)){
    const label=text(d,n.label,cx-140,cy+(n.kind==='gate'?-86:32),280,n.kind==='gate'?50:50,n.kind==='gate'?17:15);label.horzAlign=T.Canvas.AL_CENTER;labels.push(label);
   }
   map[n.id]={n,v,m:model};
  }
  const reserved=[];
  if([1,7].includes(stage.num)){
   const target=map[stage.num===1?'solicitud':'entregar'].v,cx=target.left+target.width/2;
   const buyerView=V(d,'BPMNPoolView',buyer,cx-130,oy+65,260,55);buyerView.isVertical=false;
   for(const [offset,out] of [[-55,false],[55,true]]){
    const x=cx+offset,ps=out?[[x,target.top],[x,oy+120]]:[[x,oy+120],[x,target.top]];
    const message=M('BPMNMessageFlow','',m);message.source=out?target.model:buyer;message.target=out?buyer:target.model;
    E(d,'BPMNMessageFlowView',message,out?target:buyerView,out?buyerView:target,ps);reserved.push([ps[0],ps[1]]);
   }
  }
  let routed,lastError;
  for(let attempt=0;attempt<72&&!routed;attempt++){
   const route=require('./rutas_bpmn_limpias').router([...Object.values(map).map(x=>x.v),...labels],reserved);
   let seed=stage.num*100+attempt;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
   const links=stage.edges.map((e,i)=>({...e,order:attempt===0?i:attempt===1?-i:rand()})).sort((a,z)=>a.order-z.order);
   const result=[];
   try{for(const link of links){const a=map[link.a],z=map[link.z];const normalNo=['deuda','derivado','medio','tipoOrigen'].includes(link.a);const side=a.n.kind==='gate'?(link.label.startsWith(normalNo?'No':'Sí')?'R':'B'):undefined;result.push({link,pts:route(a.v,z.v,attempt<18?side:undefined)})}routed=result;}
   catch(e){lastError=e.message;}
  }
  if(!routed)throw Error('Tramo '+stage.num+' sin trazado libre: '+lastError);
  for(const {link,pts}of routed){const a=map[link.a],z=map[link.z];
   const flow=M('BPMNSequenceFlow',link.label,m);flow.source=a.m;flow.target=z.m;flow.condition=link.label;
   const ev=E(d,'BPMNSequenceFlowView',flow,a.v,z.v,pts);ev.lineColor=link.label.startsWith('Sí')?'#226246':link.label.startsWith('No')?'#8b452c':'#354155';ev.nameLabel.font.size=15;ev.nameLabel.distance=25;ev.nameLabel.edgePosition=T.EdgeParasiticView.EP_TAIL;
  }
  text(d,stage.note,ox+45,oy+170+ph,PW-80,105,17);
  meta.push({tramo:stage.num,titulo:stage.title,nodos:stage.nodes.length,flujos:stage.edges.length});
 }
 m.documentation='Un proceso completo. Ocho tramos horizontales en una sola lámina; los pools y carriles repetidos son vistas del mismo participante y los mismos roles. Enlaces BPMN por nombre, un único receptor por código. No hay subprocesos ocultos. '+(proposed?'SGCC visible en automatizaciones; web online y Android con recepción offline limitada.':'AS IS manual conservado con precios, preparación, control sanitario, pagos, entrega y deuda.');
 const file='BPMN_'+(proposed?'Propuesto':'Actual')+'_V3';
 await rt.render(d,path.join(TMP,file+'.pdf'));const arranged=rt.app.repository.get(d._id);placeConditions(arranged);const dims=await rt.render(arranged,path.join(TMP,file+'.pdf'));const normalized=rt.app.repository.get(p._id);
 fs.writeFileSync(path.join(TMP,file+'.mdj'),rt.app.repository.writeObject(normalized));
 fs.writeFileSync(path.join(TMP,file+'_resumen.json'),JSON.stringify({dimensiones:dims,tramos:meta},null,2));console.log(file,dims);
}
module.exports={build,specs,placeConditions};if(require.main===module)(async()=>{await build(false);await build(true)})().catch(e=>{console.error(e);process.exitCode=1});
