const fs=require('fs'),path=require('path'),crypto=require('crypto');
const rt=require('./staruml_runtime'),T=rt.T;
const {casos,proceso}=require('./especificacion_v3');
const ROOT=path.resolve(__dirname,'..'),OUT=process.env.SGCC_PREVIEW_DIR?path.join(process.env.SGCC_PREVIEW_DIR,'V3'):path.join(ROOT,'03_Revision','V3');
fs.mkdirSync(OUT,{recursive:true});
const manifest=[];
function own(p,o,field='ownedElements'){o._parent=p;(p[field]||(p[field]=[])).push(o);return o;}
function model(kind,name,p,field){const o=new T[kind]();if(name!==undefined)o.name=name;if(p)own(p,o,field);return o;}
function project(name,kind='UMLModel'){const p=model('Project',name);const m=model(kind,name,p);return {p,m};}
function diagram(m,kind,name){const d=model(kind,name,m);d.defaultDiagram=true;return d;}
function style(v){v.font.face='Arial';v.font.size=14;v.lineColor='#334155';v.fillColor='#ffffff';v.fontColor='#172235';v.showShadow=false;v.wordWrap=true;return v;}
function view(d,kind,m,x,y,w,h){const v=style(new T[kind]());v.model=m;v.left=x;v.top=y;v.width=w;v.height=h;v._parent=d;d.ownedViews.push(v);return v;}
function text(d,s,x,y,w=900,h=65,size=19){const v=view(d,'UMLTextView',null,x,y,w,h);v.text=s;v.font.size=size;return v;}
function note(d,s,x,y,w=700,h=100){const v=view(d,'UMLNoteView',null,x,y,w,h);v.text=s;v.fillColor='#fff9e9';return v;}
function contain(container,v){v.containerView=container;container.containedViews.push(v);}
function points(v,ps){v.points.clear();ps.forEach(p=>v.points.add(new T.Point(...p)));}
function edge(d,kind,m,a,b,ps){const v=style(new T[kind]());v.model=m;v.tail=a;v.head=b;v._parent=d;v.lineStyle=T.EdgeView.LS_RECTILINEAR;v.showVisibility=false;v.showProperty=false;points(v,ps);d.ownedViews.push(v);if(v.nameLabel){v.nameLabel.font.size=12;v.nameLabel.distance=17;}return v;}
function relation(m,kind,a,b,name=''){const r=model(kind,name,m,kind==='UMLControlFlow'?'edges':'ownedElements');r.source=a;r.target=b;return r;}
function assoc(m,d,a,b,ma='1',mb='0..*',name='',kind='UMLAssociation',ps){const r=model(kind,name,m);r.end1.reference=a.model;r.end2.reference=b.model;r.end1.multiplicity=ma;r.end2.multiplicity=mb;r.end1.navigable='unspecified';r.end2.navigable='unspecified';return edge(d,kind==='UMLLink'?'UMLLinkView':'UMLAssociationView',r,a,b,ps||[[a.left+a.width,a.top+a.height/2],[b.left,b.top+b.height/2]]);}
async function save(p,d,relative){const dest=path.join(ROOT,relative);fs.mkdirSync(path.dirname(dest),{recursive:true});const pdf=path.join(OUT,path.basename(relative,'.mdj')+'.pdf');const dims=await rt.render(d,pdf);const norm=rt.app.repository.get(p._id);fs.writeFileSync(dest,rt.app.repository.writeObject(norm));manifest.push({archivo:relative,pdf:path.relative(ROOT,pdf),diagramas:1,...dims});console.log(path.basename(dest),dims.width+'x'+dims.height);}
// El recorrido principal tiene una posición por paso; los retornos usan corredores laterales.
function flowRoute(a,b,horizontal,tracks){
 const r1=horizontal?a.left:a.top,r2=horizontal?b.left:b.top;
 const c1=horizontal?a.top+a.height/2:a.left+a.width/2,c2=horizontal?b.top+b.height/2:b.left+b.width/2;
 if(r2>r1&&r2-r1<370){const mid=horizontal?(a.left+a.width+b.left)/2:(a.top+a.height+b.top)/2;return horizontal?[[a.left+a.width,c1],[mid,c1],[mid,c2],[b.left,c2]]:[[c1,a.top+a.height],[c1,mid],[c2,mid],[c2,b.top]];}
 const start=horizontal?a.left+a.width:a.top+a.height,end=horizontal?b.left:b.top;
 const lo=Math.min(start,end),hi=Math.max(start,end);let tr=tracks.findIndex(t=>t.every(q=>hi<q[0]||lo>q[1]));if(tr<0){tr=tracks.length;tracks.push([]);}tracks[tr].push([lo,hi]);
 const corridor=c1-(horizontal?135:220)-tr*15;
 const lead=start+35,approach=end-30;
 return horizontal?[[start,c1],[lead,c1],[lead,corridor],[approach,corridor],[approach,c2],[end,c2]]:[[c1,start],[c1,lead],[corridor,lead],[corridor,approach],[c2,approach],[c2,end]];
}
async function business(proposed,bpmn){
 const title=(bpmn?'BPMN horizontal':'BPM vertical')+' — '+(proposed?'Modelo propuesto':'Modelo actual')+' — V3';
 const {p,m}=project(title,bpmn?'BPMNProcess':'UMLActivity'),d=diagram(m,bpmn?'BPMNDiagram':'UMLActivityDiagram',title);
 const spec=proceso(proposed);
 if(bpmn){const before=spec.nodes.find(x=>x.id==='cotizar');spec.nodes.forEach(x=>{if(x.rank>before.rank)x.rank+=1;});spec.nodes.push({id:'respuesta',t:'task',l:1,text:'Recibir respuesta del cliente',rank:before.rank+1});const e=spec.edges.find(x=>x.a==='cotizar'&&x.b==='acepta');e.b='respuesta';spec.edges.push({a:'respuesta',b:'acepta',g:''});}
 // Una alternativa que retorna se reúne antes de ejecutar una acción: no crea una sincronización implícita.
 for(const target of [...spec.nodes]){const incoming=spec.edges.filter(e=>e.b===target.id);if(incoming.length>1&&!['merge','end'].includes(target.t)){const id='join_'+target.id;spec.nodes.push({id,t:'merge',l:target.l,text:'',rank:target.rank-.25});incoming.forEach(e=>e.b=id);spec.edges.push({a:id,b:target.id,g:''});}}
 const roles=proposed?['Comprador','Ventas / cobranza','Producción','Almacén','Responsable de entrega']:['Comprador','Propietario / atención y cobro','Producción: carne y derivados','Responsable de entrega'];
 const lanes=[],vlanes=[],maps={};let customer;
 const span=(Math.max(...spec.nodes.map(n=>n.rank))+1)*(bpmn?500:260)+430;
 const sys=new Set(['precio','publicar','senaReg','stockC','stockD','reserva','total','registrar','abonoReg','syncOk','recuperarPago','referenciaPago','consultarSaldo','constancia']);
 let poolV;
 if(bpmn){
  const cp=model('BPMNParticipant','Comprador',m);customer=view(d,'BPMNPoolView',cp,70,100,span,120);
  const pool=model('BPMNParticipant','Chanchería — '+(proposed?'operación con SGCC':'operación actual'),m);poolV=view(d,'BPMNPoolView',pool,70,300,span,(proposed?5:3)*490);
  const names=proposed?['Ventas / cobranza','Producción','Almacén','Responsable de entrega','SGCC — automatizaciones']:['Propietario / atención y cobro','Producción: carne y derivados','Responsable de entrega'];
  names.forEach((s,i)=>{lanes.push(model('BPMNLane',s,pool));const v=view(d,'BPMNLaneView',lanes[i],105,300+i*490,span-35,490);contain(poolV,v);vlanes.push(v);});
 }else roles.forEach((s,i)=>{lanes.push(model('UMLActivityPartition',s,m,'groups'));const v=view(d,'UMLSwimlaneView',lanes[i],130+i*620,160,620,span);v.isVertical=true;vlanes.push(v);});
 text(d,title,100,25,1400,55,23);
 if(!bpmn)note(d,'Las fechas de preparación y resolución de anticipos siguen el acuerdo registrado. Propuesta: web online y Android Kotlin; la recepción local pendiente no cierra la entrega central.',150,span+220,1700,100);
 for(const n of spec.nodes){
  let lane=n.l;if(bpmn){if(lane===0)lane=n.id==='recibe'?4:1;lane=proposed?(sys.has(n.id)?4:lane-1):(lane===1?0:lane===4?2:1);}else if(!proposed)lane=n.l===4?3:n.l===3?2:n.l;
  let kind, vk;
  if(bpmn){kind=n.t==='start'?'BPMNStartEvent':n.t==='end'?'BPMNEndEvent':n.t==='decision'||n.t==='merge'?'BPMNExclusiveGateway':n.t==='wait'?'BPMNIntermediateCatchEvent':proposed&&lane===4?'BPMNServiceTask':proposed?'BPMNUserTask':'BPMNManualTask';if(['solicitud','respuesta','recibe'].includes(n.id))kind='BPMNReceiveTask';vk=/Event$/.test(kind)?'BPMNEventView':/Gateway$/.test(kind)?'BPMNGatewayView':'BPMNTaskView';}
  else{kind=n.t==='start'?'UMLInitialNode':n.t==='end'?'UMLActivityFinalNode':n.t==='decision'?'UMLDecisionNode':n.t==='merge'?'UMLMergeNode':'UMLAction';vk=['task','wait'].includes(n.t)?'UMLActionView':'UMLControlNodeView';}
  let label=n.text;if(bpmn&&n.id==='solicitud')label=proposed?'Recibir solicitud por WhatsApp, local o portal':'Recibir solicitud por WhatsApp o local';if(bpmn&&n.id==='recibe')label='Recibir conformidad u observaciones del comprador';if(bpmn&&n.id==='fecha')label='Esperar próxima fecha de seguimiento';
  const mm=model(kind,label,lanes[lane],bpmn?'ownedElements':'nodes');
  if(bpmn&&n.t==='wait'){const ev=model(n.id==='fecha'?'BPMNTimerEventDefinition':'BPMNConditionalEventDefinition','',mm,'eventDefinitions');ev.documentation=n.id==='fecha'?'Se alcanza la fecha de seguimiento; un abono puede registrarse mediante CU16 y se consulta al retomar.':'Continuar cuando se confirme la condición o disponibilidad indicada. No equivale a una duración fija.';}
  let w=['start','end','merge'].includes(n.t)?38:n.t==='decision'?100:300,h=['start','end','merge'].includes(n.t)?38:n.t==='decision'?90:104;
  if(bpmn&&n.t==='wait'){w=44;h=44;}
  const x=bpmn?300+n.rank*500:130+lane*620+(620-w)/2,y=bpmn?300+lane*490+245-h/2:270+n.rank*260;
  const vv=view(d,vk,mm,x,y,w,h);contain(vlanes[lane],vv);vv.fillColor=n.t==='decision'?'#fff2c5':n.t==='wait'?'#e9e8fd':proposed&&bpmn&&lane===4?'#ddf3ec':'#f2f7fc';
  if(vv.nameLabel){vv.nameLabel.wordWrap=true;vv.nameLabel.width=n.t==='decision'?250:300;vv.nameLabel.font.size=13;}
  if(!bpmn&&['decision','end','start'].includes(n.t))text(d,label,x+w+15,y+10,205,90,15);
  maps[n.id]={m:mm,v:vv,n};
 }
 const tracks={};for(const e of spec.edges){const a=maps[e.a],b=maps[e.b];const rel=relation(m,bpmn?'BPMNSequenceFlow':'UMLControlFlow',a.m,b.m,bpmn?e.g:'');if(bpmn)rel.condition=e.g;else rel.guard=e.g;
  const key=bpmn?Math.round(a.v.top/490):Math.round(a.v.left/620);tracks[key]||=[];edge(d,bpmn?'BPMNSequenceFlowView':'UMLControlFlowView',rel,a.v,b.v,flowRoute(a.v,b.v,bpmn,tracks[key]));}
 if(bpmn){for(const [id,out] of [['solicitud',false],['cotizar',true],['respuesta',false],['acuerdo',true],['recibe',false]]){const v=maps[id].v;const r=relation(m,'BPMNMessageFlow',out?v.model:customer.model,out?customer.model:v.model);const x=v.left+v.width/2;edge(d,'BPMNMessageFlowView',r,out?v:customer,out?customer:v,out?[[x,v.top],[x,220]]:[[x,220],[x,v.top]]);}}
 const filename=(bpmn?'BPMN_':'BPM_')+(proposed?'Propuesto':'Actual')+'_V3.mdj';
 await save(p,d,(bpmn?'02_Ingenieria_de_Software/BPMN_Horizontal/':'01_Proyecto_de_Sistemas/BPM_Vertical/Versiones_Codex/')+filename);
}

async function usecases(){
 const {p,m}=project('SGCC — Casos de uso V3'),d=diagram(m,'UMLUseCaseDiagram','Casos de uso del SGCC');
 text(d,'SGCC — Objetivos de sus usuarios',80,25,1300,50,24);
 const subject=model('UMLSubsystem','Sistema de Gestión Comercial y Clientes',m),box=view(d,'UMLUseCaseSubjectView',subject,290,110,1000,26*170+80);
 const actors={};let y=160;
 for(const c of casos){
  actors[c.actor]||=model('UMLActor',c.actor,m);const av=view(d,'UMLActorView',actors[c.actor],90,y+3,135,90);
  const u=model('UMLUseCase',c.id+' — '+c.nombre,m);u.documentation=c.pre+'\nResultado: '+c.post+'\nAlternativa: '+c.alternativa+'\nFuente: '+c.fuente;
  const uv=view(d,'UMLUseCaseView',u,410,y,680,95);contain(box,uv);assoc(m,d,av,uv,'','','','UMLAssociation',[[225,y+48],[410,y+48]]);
  if(c.id==='CU19'||c.id==='CU10'){const an=c.id==='CU19'?'Proveedor fiscal':'Balanza';actors[an]||=model('UMLActor',an,m);const ext=view(d,'UMLActorView',actors[an],1380,y+3,160,90);assoc(m,d,uv,ext,'','','','UMLAssociation',[[1090,y+48],[1380,y+48]]);}
  y+=170;
 }
 note(d,'Cada aparición de un actor con el mismo nombre representa al mismo actor.\nLos CU describen objetivos del usuario; los pasos físicos están en los BPM.\nAutenticación y permisos son precondiciones de las operaciones protegidas.',90,y+90,1100,110);
 await save(p,d,'02_Ingenieria_de_Software/Casos_de_Uso/Casos_de_Uso_SGCC_V3.mdj');
}

async function activity(c){
 if(c.id==='CU21')return require('./v4/movil').activity();
 const {p,m}=project(c.id+' — '+c.nombre,'UMLActivity'),d=diagram(m,'UMLActivityDiagram',c.id+' — Actividad');
 text(d,c.id+' — '+c.nombre,70,25,1510,70,23);
 const fiscal=c.id==='CU19',shift=fiscal?390:c.id==='CU10'?180:0;
 const parts=[model('UMLActivityPartition',c.actor,m,'groups'),model('UMLActivityPartition','SGCC',m,'groups')];
 const pv=parts.map((x,i)=>{const v=view(d,'UMLSwimlaneView',x,100+i*760,120,760,2310+shift);v.isVertical=true;return v});
 const ops=c.operaciones.filter(op=>!(c.id==='CU19'&&op==='solicitarEmision'));
 const list=[['i','start',0,240,''],['sol','task',0,370,'Solicitar: '+c.nombre],['datos','task',1,540,c.validar+'()'],
 ...(fiscal?[['preval','decision',1,720,'¿Integración habilitada y datos de venta válidos?']]:[]),
 ...(shift?[['ext','task',1,fiscal?900:720,fiscal?'Solicitar / consultar al proveedor con la misma referencia; recibir respuesta o error':'Solicitar peso a balanza o registro manual autorizado; recibir lectura']]:[]),
 ['val','decision',1,740+shift,'¿'+c.condicion+'?'],...ops.map((op,i)=>['op'+i,'task',1,960+i*180+shift,op+'()']),
 ['ok','task',0,1510+shift,'Recibir resultado: '+c.post],['end','end',0,1710+shift,'Objetivo atendido'],
 ...(fiscal?[['errJoin','merge',1,2080,'']]:[]),['error','task',1,1790+shift,c.operacionAlternativa+'()'],['resp','task',0,2010+shift,c.alternativa],['e2','end',0,2220+shift,'Alternativa informada / pendiente']];
 const map={};
 for(const[id,t,l,y,label]of list){const kind=t==='start'?'UMLInitialNode':t==='end'?'UMLActivityFinalNode':t==='decision'?'UMLDecisionNode':t==='merge'?'UMLMergeNode':'UMLAction',mm=model(kind,t==='task'?label:'',parts[l],'nodes'),w=['start','end','merge'].includes(t)?35:t==='decision'?110:500,h=['start','end','merge'].includes(t)?35:t==='decision'?100:130,x=100+l*760+(760-w)/2;
 const v=view(d,t==='task'?'UMLActionView':'UMLControlNodeView',mm,x,y,w,h);contain(pv[l],v);if(t==='decision')text(d,label,x+130,y,225,150,14);if(t==='end')text(d,label,x+50,y,260,70,14);map[id]={m:mm,v};}
 const es=[['i','sol'],['sol','datos'],...(fiscal?[['datos','preval'],['preval','ext','Sí'],['preval','errJoin','No'],['ext','val'],['errJoin','error']]:shift?[['datos','ext'],['ext','val']]:[['datos','val']]),['val','op0','Sí'],['val',fiscal?'errJoin':'error','No'],...ops.slice(1).map((_,i)=>['op'+i,'op'+(i+1)]),['op'+(ops.length-1),'ok'],['ok','end'],['error','resp'],['resp','e2']];
 const route=require('./v4/rutas').router(Object.values(map).map(x=>x.v));
 for(const[a,z,g='']of es){const r=relation(m,'UMLControlFlow',map[a].m,map[z].m);r.guard=g;edge(d,'UMLControlFlowView',r,map[a].v,map[z].v,['end','e2'].includes(z)?[[map[a].v.left+map[a].v.width/2,map[a].v.top+map[a].v.height],[map[z].v.left+map[z].v.width/2,map[z].v.top]]:route(map[a].v,map[z].v));}
 note(d,'Precondición: '+c.pre+'\nFuente: '+c.fuente+'\nCanal: '+c.canal+'. El SGCC registra el resultado alternativo; el usuario recibe la acción pendiente. Una alternativa no declara cumplido el objetivo.',100,2500+shift,1500,310);
 await save(p,d,'02_Ingenieria_de_Software/05_Actividades/'+c.id+'_Actividad.mdj');
}

async function sequence(c){
 if(c.id==='CU21')return require('./v4/movil').sequence();
 const {p,m}=project(c.id+' — '+c.nombre,'UMLInteraction'),d=diagram(m,'UMLSequenceDiagram',c.id+' — Secuencia');d.showActivation=true;d.showSequenceNumber=false;
 text(d,c.id+' — '+c.nombre,80,2,1500,30,22);
 const external=c.id==='CU19'?'externo: ProveedorFiscal':c.id==='CU10'?'dispositivo: Balanza':null,offset=external?90:0;
 const lif=[];['usuario: '+c.actor,'interfaz: '+(c.id==='CU01'?'Web / Android online':c.id==='CU22'?'Web / Android online':'Web responsiva'),'control: '+c.servicio,'datos: Repositorio',...(external?[external]:[])].forEach((name,i)=>{const mm=model('UMLLifeline',name,m,'participants');const vv=view(d,'UMLSeqLifelineView',mm,80+i*440,120,270,1490+offset);lif.push(vv);});
 function msg(a,b,label,y,reply=false){const r=model('UMLMessage',label,m,'messages');r.source=lif[a].model;r.target=lif[b].model;r.messageSort=reply?'reply':'synchCall';const av=lif[a].linePart,bv=lif[b].linePart;const v=edge(d,'UMLSeqMessageView',r,av,bv,[[lif[a].left+135,y],[lif[b].left+135,y]]);v.nameLabel.font.size=12;return v;}
 msg(0,1,c.nombre,250);msg(1,2,c.validar+'()',340);msg(2,3,'consultar('+c.entidades.slice(0,2).join(', ')+')',430);msg(3,2,'datos y condiciones actuales',500,true);
 if(external){const call=msg(2,4,c.id==='CU19'?'solicitarEmision(referenciaUnica)':'capturarPeso()',540);call.model.guard=c.id==='CU19'?'integración habilitada; datos válidos; emisión no confirmada':'control apto; orden habilitada';msg(4,2,c.id==='CU19'?'respuesta fiscal o error':'peso o error de lectura',600,true);}
 const cf=model('UMLCombinedFragment','',m,'fragments');cf.interactionOperator='alt';const cv=view(d,'UMLCombinedFragmentView',cf,110,570+offset,1570+(external?440:0),930);
 const good=model('UMLInteractionOperand','',cf,'operands');good.guard=c.condicion;const bad=model('UMLInteractionOperand','',cf,'operands');bad.guard='else';
 for(const [operand,height]of [[good,560],[bad,340]]){const ov=style(new T.UMLInteractionOperandView());ov.model=operand;ov.height=height;cv.operandCompartment.addSubView(ov);}
 // Las vistas de operandos se crean por el motor desde los dos modelos.
 let yy=660+offset;for(const op of c.operaciones.filter(x=>!(c.id==='CU19'&&x==='solicitarEmision'))){msg(2,3,op+'()',yy);yy+=85;}msg(3,2,'resultado persistido',yy,true);msg(2,1,'mostrar resultado confirmado',yy+65,true);msg(1,0,c.post,yy+130,true);
 msg(2,3,c.operacionAlternativa+'()',1220+offset);msg(3,2,'resultado alternativo',1290+offset,true);msg(2,1,'informar alternativa sin confirmar éxito',1360+offset,true);msg(1,0,c.alternativa,1430+offset,true);
 note(d,'Precondición: '+c.pre+'\nLos mensajes de cada operando son alternativas. El actor resuelve las decisiones comerciales.\nDatos: '+c.entidades.join(', ')+'. Fuente: '+c.fuente+('\nCanal: '+c.canal+'. Sin conexión no se confirma esta operación.'),80,1660+offset,1650+(external?440:0),310);
 await save(p,d,'02_Ingenieria_de_Software/06_Secuencias/'+c.id+'_Secuencia.mdj');
}

module.exports={rt,T,ROOT,OUT,manifest,casos,own,model,project,diagram,view,text,note,contain,points,edge,relation,assoc,save,business,usecases,activity,sequence};
if(require.main===module)(async()=>{for(const b of [false,true])for(const p of [false,true])await business(p,b);for(const c of casos){await sequence(c);await activity(c);}fs.writeFileSync(path.join(OUT,'Manifiesto_parcial.json'),JSON.stringify(manifest,null,2));})().catch(e=>{console.error(e);process.exitCode=1;});
