const b=require('./base'),{T,M,D,V,E,text,project,own,rel,contain}=b;
const {router}=require('./rutas');
async function saveExtra(p,d,folder,file){
 const dest=b.path.join(b.ROOT,'02_Ingenieria_de_Software',folder,file+'.mdj');
 const pdf=b.path.join(process.env.SGCC_PREVIEW_DIR?b.path.join(process.env.SGCC_PREVIEW_DIR,'V3'):b.path.join(b.ROOT,'03_Revision/V3'),file+'.pdf');
 await b.rt.render(d,pdf);const norm=b.rt.app.repository.get(p._id);b.fs.writeFileSync(dest,b.rt.app.repository.writeObject(norm));
 console.log(folder+'/'+file+'.mdj');
}
async function sequence(){
 const {p,m}=project('CU21 — Recepción Android y confirmación del servidor','UMLInteraction'),d=D(m,'UMLSequenceDiagram','CU21 — Secuencia');d.showSequenceNumber=false;d.showActivation=true;
 text(d,'CU21 · Recepción Android con sincronización limitada',70,15,2750,60,26);
 const specs=[['responsable: ResponsableEntrega',80],['app: Android Kotlin',600],['local: Room + archivos',1120],['api: SGCC Entregas',1780],['datos: Base central',2440]];
 const lif=specs.map(([n,x])=>V(d,'UMLSeqLifelineView',M('UMLLifeline',n,m,'participants'),x,140,320,3260));let n=0;
 function msg(a,z,label,y,reply=false){const mm=M('UMLMessage',label,m,'messages');mm.source=lif[a].model;mm.target=lif[z].model;mm.messageSort=reply?'reply':'synchCall';mm.sequenceNumber=String(++n);const e=E(d,'UMLSeqMessageView',mm,lif[a].linePart,lif[z].linePart,[[lif[a].left+160,y],[lif[z].left+160,y]]);e.nameLabel.font.size=14;return mm;}
 function frame(op,y,h,guards,heights,x=70,w=2720){const cf=M('UMLCombinedFragment','',m,'fragments');cf.interactionOperator=op;const v=V(d,'UMLCombinedFragmentView',cf,x,y,w,h);for(let i=0;i<guards.length;i++){const operand=M('UMLInteractionOperand','',cf,'operands');operand.guard=guards[i];const ov=new T.UMLInteractionOperandView();ov.model=operand;ov.height=heights[i];v.operandCompartment.addSubView(ov);}return cf;}
 frame('opt',230,550,['preparación del reparto con conexión y sesión válida'],[520]);
 msg(0,1,'descargar entregas asignadas y autorizadas',310);
 msg(1,3,'consultarAsignadas(sesión)',390);
 msg(3,4,'validar responsable y autorización de despacho',470);
 msg(4,3,'asignaciones, versión y datos de entrega',540,true);
 msg(3,1,'paquete autorizado para el dispositivo',620,true);
 msg(1,2,'guardar paquete descargado',710);
 text(d,'Captura local · entrega descargada y usuario del reparto',80,830,2600,45,19);
 msg(0,1,'seleccionar entrega; registrar receptor, peso, conformidad y foto',940);
 msg(1,2,'comprobar asignación descargada; guardar clave y evidencia',1050);
 msg(2,1,'guardado local PENDIENTE o error de captura',1150,true);
 msg(1,0,'mostrar pendiente; si falla el guardado, pedir corrección',1250,true);
 frame('opt',1380,1760,['hay PENDIENTE; app abierta; conexión y sesión válidas'],[1730]);
 msg(1,2,'leer recepción pendiente',1500);msg(2,1,'clave, entregaId, versión, conformidad y evidencia',1590,true);
 msg(1,3,'sincronizarRecepcion(misma clave)',1710);
 msg(3,4,'validar permiso/asignación/versión; registrar recepción una vez',1840);
 msg(4,3,'confirmada, ya existente o conflicto',1970,true);
 frame('alt',2110,960,['confirmada o ya registrada','conflicto de datos, asignación, estado o versión','sin respuesta / tiempo agotado'],[360,300,270],120,2600);
 msg(3,1,'confirmación, referencia y estado ENTREGADA / OBSERVADA',2220,true);msg(1,2,'marcar CONFIRMADA; conservar referencia',2320);msg(1,0,'recepción sincronizada; mostrar estado de entrega',2420,true);
 msg(3,1,'CONFLICTO con causa',2570,true);msg(1,2,'guardar conflicto; no sobrescribir servidor',2670);msg(1,0,'solicitar revisión autorizada',2770,true);
 msg(1,2,'mantener PENDIENTE y evidencia para reintento',2910);msg(1,0,'informar envío pendiente; usar misma clave',3010,true);
 text(d,'Precondición: iniciar sesión y descargar previamente entregas asignadas, preparadas y autorizadas. Sin paquete local: conectarse y descargar.\nLa fecha de recepción física se conserva; la entrega central pasa a ENTREGADA u OBSERVADA según recepción validada. No se promete sincronización con la app cerrada.\nRetiro en local: formulario web online invoca la misma validación del servidor; no usa Room ni captura offline.\nSin conexión no se crean pedidos, pagos, créditos, reservas, movimientos ni facturas. CU22 (frío) requiere conexión.',80,3470,2690,210,17);
 m.documentation='CU21: el registro local de recepción es una operación pendiente del Android Kotlin. Solo asignaciones autorizadas descargadas. Room/SQLite y archivos privados. Guardado local debe finalizar antes de mostrar éxito; ante error solicitar corrección. El servidor aplica una recepción una vez tras validar usuario, asignación, versión y evidencia. Sesión expirada: reautenticar online conservando cola. Conflicto: revisión autorizada; entrega cancelada no se fuerza a ENTREGADA. Timeout: reintento con misma clave. Web retiro solo online. RF-04, RF-07, RF-14, RNF-01.';
 await saveExtra(p,d,'06_Secuencias','CU21_Secuencia');
}
async function activity(){
 const {p,m}=project('CU21 — Recepción Android','UMLActivity'),d=D(m,'UMLActivityDiagram','CU21 — Actividad');
 text(d,'CU21 · Captura Android y sincronización de recepción',70,20,2500,55,25);
 const parts=['Responsable de entrega','Android Kotlin · Room / archivos','Servidor SGCC'].map(n=>M('UMLActivityPartition',n,m,'groups'));
 const pv=parts.map((mm,i)=>{const v=V(d,'UMLSwimlaneView',mm,80+i*780,120,780,4090);v.isVertical=true;return v;});
 const nodes={},items=[
 ['start','start',0,240,''],['mergeSelect','merge',0,305,''],['mergeCapture','merge',0,995,''],['select','task',0,360,'Seleccionar entrega del reparto'],['loaded','decision',1,560,'¿Asignada y descargada con sesión previa?'],
 ['download','task',0,760,'Conectarse, iniciar sesión y descargar entregas autorizadas'],['capture','task',0,1080,'Registrar receptor, fecha, peso, conformidad y evidencia'],
 ['save','task',1,1320,'Validar datos y guardar recepción + evidencia con clave única'],['saved','decision',1,1520,'¿Guardado local completo?'],['fix','task',0,1740,'Corregir datos o resolver error de almacenamiento'],
 ['pending','task',1,1920,'Mostrar PENDIENTE de sincronización'],['online','decision',1,2130,'¿App abierta, conexión y sesión válidas?'],['wait','task',0,2330,'Conservar captura; reconectar o reautenticar y reintentar'],['endPending','end',0,2540,'Pendiente local conservado'],
 ['send','task',1,2420,'Enviar misma clave, versión, datos y evidencia'],['validate','task',2,2650,'Validar permisos, asignación, versión y evidencia; registrar una vez si procede'],
 ['response','decision',1,2890,'¿Llegó respuesta?'],['timeout','task',0,3090,'Mantener PENDIENTE y evidencia; reintentar misma clave'],['endTimeout','end',0,3300,'Envío sin confirmar'],
 ['accepted','decision',2,3110,'¿Confirmada o ya registrada?'],['conflict','task',1,3400,'Guardar CONFLICTO y mostrar causa'],['review','task',0,3610,'Revisión autorizada: corregir o descartar con traza; no forzar entrega cancelada'],['endConflict','end',0,3890,'Resolución pendiente o registrada'],
 ['confirmed','task',2,3420,'Devolver referencia; ENTREGADA si conforme u OBSERVADA; deuda separada'],['localDone','task',1,3690,'Marcar CONFIRMADA; conservar identificador remoto'],['endDone','end',2,3970,'Recepción sincronizada; consultar estado central']
 ];
 for(const[id,kind,l,y,label]of items){const type=kind==='start'?'UMLInitialNode':kind==='end'?'UMLActivityFinalNode':kind==='decision'?'UMLDecisionNode':kind==='merge'?'UMLMergeNode':'UMLAction';const model=M(type,kind==='task'?label:'',parts[l],'nodes');const w=kind==='task'?500:kind==='decision'?120:35,h=kind==='task'?120:kind==='decision'?110:35,x=80+l*780+(780-w)/2;const v=V(d,kind==='task'?'UMLActionView':'UMLControlNodeView',model,x,y,w,h);contain(pv[l],v);if(kind==='decision')text(d,label,x+140,y-5,235,125,15);if(kind==='end')text(d,label,x-220,y+45,470,70,15);nodes[id]=v;}
 const edges=[['start','mergeSelect'],['mergeSelect','select'],['select','loaded'],['loaded','mergeCapture','Sí'],['mergeCapture','capture'],['loaded','download','No'],['download','mergeSelect','Descarga confirmada'],['capture','save'],['save','saved'],['saved','fix','No'],['fix','mergeCapture','Reintentar captura'],['saved','pending','Sí'],['pending','online'],['online','wait','No'],['wait','endPending'],['online','send','Sí'],['send','validate'],['validate','response'],['response','timeout','No'],['timeout','endTimeout'],['response','accepted','Sí'],['accepted','conflict','No'],['conflict','review'],['review','endConflict'],['accepted','confirmed','Sí'],['confirmed','localDone'],['localDone','endDone']];
 const route=router(Object.values(nodes));for(const[a,z,guard='']of edges){const rr=M('UMLControlFlow','',m,'edges');rr.source=nodes[a].model;rr.target=nodes[z].model;rr.guard=guard;const v=E(d,'UMLControlFlowView',rr,nodes[a],nodes[z],route(nodes[a],nodes[z]));v.nameLabel.font.size=14;}
 text(d,'Registro físico y confirmación central son diferentes: PENDIENTE no cambia Entrega central ni deuda. El reintento comienza leyendo la misma operación.\nRetiro en local: captura en web con conexión y la misma validación central, sin almacenamiento offline.\nSolo recepción descargada opera sin señal. Pedidos, cobros, créditos, stock, facturación y control de frío requieren conexión.',90,4300,2290,200,17);
 m.documentation='Recepción de reparto en Android Kotlin con descarga previa, validación local, persistencia y sincronización en primer plano. Cada decisión No tiene tratamiento: descarga online, corrección de captura, conservación pendiente, reintento o revisión de conflicto. El registro central requiere respuesta confirmada; una recepción observada no cierra la entrega. Un registro local no cierra la deuda. Guardas de descarga y sesión verificadas antes del reparto; la sesión puede renovarse al enviar sin borrar datos pendientes.';
 await saveExtra(p,d,'05_Actividades','CU21_Actividad');
}
function place(v,host,x,y){const ps=host.points;let i=Math.floor(ps.count()/2);if(ps.count()%2===0)i--;const a=ps.getPoint(i).copy(),c=ps.getPoint(i+1);if(ps.count()%2===0){a.x=(a.x+c.x)/2;a.y=(a.y+c.y)/2;}const q=T.Coord.getPointAwayLine(a,c,0,1000),theta=Math.atan2(-q.y,q.x);v.distance=Math.hypot(x-a.x,y-a.y);v.alpha=Math.atan2(-(y-a.y),x-a.x)-theta;}
async function collaboration(){
 const {p,m}=project('CU21 — Colaboración Android V4'),design=M('UMLPackage','Participantes de diseño',m),coll=M('UMLCollaboration','Recepción Android y sincronización',m),inter=M('UMLInteraction','CU21',coll),d=D(inter,'UMLCommunicationDiagram','CU21 — Colaboración');d.showSequenceNumber=true;d.sequenceNumbering='custom';
 text(d,'CU21 · Recepción Android y confirmación central',80,20,2800,55,26);
 const specs=[['responsable','Responsable de entrega','actor',80,420,330],['app','AndroidKotlin','boundary',1060,420,430],['local','RoomArchivos','entity',1060,1470,430],['api','ControlRecepcionSGCC','control',2250,420,430],['datos','RepositorioCentral','entity',2250,1470,430]];
 const vs=specs.map(([n,cl,st,x,y,w])=>{const cls=M(st==='actor'?'UMLActor':'UMLClass',cl,design);if(st!=='actor')cls.stereotype=st;const part=M('UMLAttribute',n,coll,'attributes');part.type=cls;const ll=M('UMLLifeline',n,inter,'participants');ll.represent=part;return V(d,'UMLCommLifelineView',ll,x,y,w,110);});
 const links={};for(const[a,z,points]of [[0,1,[[410,475],[1060,475]]],[1,2,[[1275,530],[1275,1470]]],[1,3,[[1490,475],[2250,475]]],[3,4,[[2465,530],[2465,1470]]]]){const rr=M('UMLConnector','',coll);rr.end1.reference=vs[a].model.represent;rr.end2.reference=vs[z].model.represent;links[[a,z].sort().join(',')]=E(d,'UMLConnectorView',rr,vs[a],vs[z],points);}
 const msgs=[
 [0,1,'descargarAsignadas()','online',730,260],
 [1,3,'consultarAsignadas()','sesión válida',1850,230],
 [3,1,'paquete y versión','asignadas/autorizadas',1850,680],
 [1,2,'guardarDescarga()','online',1275,760],
 [0,1,'registrarRecepcion()','paquete local',730,680],
 [1,2,'guardarPendiente(clave, evidencia)','captura válida',1275,970],
 [1,3,'enviarRecepcion(clave, versión)','online; app abierta',1850,860],
 [3,4,'validarYRegistrarUnaVez()','permiso y evidencia',2465,800],
 [4,3,'confirmada / conflicto','',2465,1100],
 [3,1,'respuesta o tiempo agotado','',1850,1080],
 [1,2,'actualizarEstadoLocal()','respuesta; conservar si timeout',1275,1260]
 ];
 msgs.forEach(([a,z,name,guard,x,y],i)=>{const host=links[[a,z].sort().join(',')],mm=M('UMLMessage',name,inter,'messages');mm.source=vs[a].model;mm.target=vs[z].model;mm.connector=host.model;mm.messageSort=[2,8,9].includes(i)?'reply':'synchCall';mm.sequenceNumber=String(i+1);mm.guard=guard;const v=V(d,'UMLCommMessageView',mm,0,0,40,20);v.hostEdge=host;v.nameLabel.font.size=16;place(v,host,x,y);if(a===1&&z===2){v.nameLabel.distance=360;v.nameLabel.alpha=0;}if((a===3&&z===4)||(a===4&&z===3)){v.nameLabel.distance=370;v.nameLabel.alpha=0;}});
 text(d,'1–4: preparación con conexión. 5–6: captura local solo de una entrega descargada y autorizada. 7–11: sincronización al reconectar con app abierta.\nConfirmada o ya existente → CONFIRMADA. Sin respuesta → PENDIENTE. Conflicto → revisión autorizada; no sobrescribir.\nLa fecha real se conserva; el servidor registra ENTREGADA u OBSERVADA según recepción. La deuda se gestiona por separado. Retiro web opera online.',80,1810,2850,190,17);
 inter.documentation='CU21 Android Kotlin: consulta local de asignaciones y recepción con persistencia Room/archivos. Cada mensaje usa conectores reales y numeración. Las respuestas de confirmación y conflicto son excluyentes; timeout conserva el registro. Solo se capturan recepciones, nunca pedidos/cobros/stock offline. La web de retiro requiere conexión y utiliza el mismo control central.';
 await b.save(p,d,'02_Colaboracion/CU21_Colaboracion.mdj',{caso:'CU21'});
}
module.exports={sequence,activity,collaboration};
