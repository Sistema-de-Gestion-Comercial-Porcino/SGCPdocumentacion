const b=require('./base'),{M,D,V,E,text,project,contain,save,T}=b,{casos}=require('./specs');
function readable(op){return op.replace(/\(([^)]*)\)/g,(_,a)=>a?'\nDatos: '+a.replace(/,/g,', '):'').replace(/([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])/g,'$1 $2').replace(/^./,s=>s.toUpperCase());}
function lifeline(m,d,name,x,y,h){const o=M('UMLLifeline',name,m,'participants');return V(d,'UMLSeqLifelineView',o,x,y,330,h);}
async function sequence(c){
 const {p,m}=project(c.id+' — '+c.nombre,'UMLInteraction'),d=D(m,'UMLSequenceDiagram',c.id+' — Secuencia · '+c.nombre);d.showActivation=true;d.showSequenceNumber=false;
 const heights=c.branches.map(q=>270+q.ops.length*100+(q.after?450:0)),full=heights.reduce((a,z)=>a+z,0)+1450;
 text(d,c.id+' · '+c.nombre,80,8,2400,30,26);
 
 const life=['solicitante: Usuario','interfaz: Web / Android autorizado','control: '+c.servicio,'datos: Repositorio'+c.servicio].map((n,i)=>lifeline(m,d,n,100+i*680,190,full-430));
 const msg=(a,z,label,y,reply=false)=>{const mm=M('UMLMessage',label,m,'messages');mm.source=life[a].model;mm.target=life[z].model;mm.messageSort=reply?'reply':'synchCall';return E(d,'UMLSeqMessageView',mm,life[a].linePart,life[z].linePart,[[life[a].left+165,y],[life[z].left+165,y]]);};
 msg(0,1,'seleccionar operación de '+c.nombre,350);msg(1,2,c.id==='CU01'?'validar operación de acceso':'validar sesión, permisos y alcance de datos',440);msg(2,3,'consultar datos y condición de la operación',530);msg(3,2,'datos autorizados o motivo de rechazo',610,true);
 const cf=M('UMLCombinedFragment','',m,'fragments');cf.interactionOperator='alt';const cv=V(d,'UMLCombinedFragmentView',cf,140,670,2490,heights.reduce((a,z)=>a+z,0)+270);let cursor=680;
 for(let k=0;k<c.branches.length;k++){
  const q=c.branches[k],o=M('UMLInteractionOperand','',cf,'operands');o.guard=q.nombre+'; actor: '+q.actor+'; '+q.condicion;const ov=new T.UMLInteractionOperandView();ov.model=o;ov.height=heights[k];cv.operandCompartment.addSubView(ov);let yy=cursor+115;
  for(const op of q.ops){const input=/^(seleccionar|porCada)/i.test(op),show=/^(mostrar|presentar|listar)/i.test(op);msg(input?1:2,input?2:show?1:3,op,yy,show);yy+=100;}
  if(q.after){
   const nested=M('UMLCombinedFragment','',o);nested.interactionOperator='alt';const nv=V(d,'UMLCombinedFragmentView',nested,710,yy+10,1870,400);
   for(const [j,ok]of [true,false].entries()){const no=M('UMLInteractionOperand','',nested,'operands');no.guard=(ok?'Sí: ':'No: ')+q.after.question;const vv=new T.UMLInteractionOperandView();vv.model=no;vv.height=200;nv.operandCompartment.addSubView(vv);msg(2,3,ok?q.after.yes:q.after.no,yy+110+j*200);}
   yy+=450;
  }
  msg(3,2,'resultado de la operación seleccionada',yy,true);msg(2,1,'mostrar resultado de esta operación',yy+65,true);
  if(c.id==='CU08'&&[2,3].includes(k)){
   const lp=M('UMLCombinedFragment','',o);lp.interactionOperator='loop';const lo=M('UMLInteractionOperand','',lp,'operands');lo.guard='por cada producto/corte y lote obtenido';const lv=V(d,'UMLCombinedFragmentView',lp,710,cursor+(k===2?170:60),1870,115+(q.ops.length-1)*100+45-(k===2?170:60)),lov=new T.UMLInteractionOperandView();lov.model=lo;lov.height=115+(q.ops.length-1)*100+45-(k===2?170:60);lv.operandCompartment.addSubView(lov);
  }
  cursor+=heights[k];
 }
 const err=M('UMLInteractionOperand','',cf,'operands');err.guard='else: permiso, datos o condición de la operación no válidos';const errView=new T.UMLInteractionOperandView();errView.model=err;errView.height=270;cv.operandCompartment.addSubView(errView);
 const y=cursor+120;msg(2,1,'si falla una validación: conservar datos e informar motivo / acción pendiente',y,true);msg(1,0,'resultado de la rama elegida o rechazo informado',y+80,true);
 text(d,'Precondición: '+c.pre+'\n'+c.regla+'\nAlternativas: '+c.branches.map(q=>q.nombre+': '+q.alternativa).join('\n'),80,y+170,2470,600,17);
 m.documentation='Las ramas alt son operaciones mutuamente excluyentes del caso general, nunca un CRUD ejecutado completo. Sus guardas incluyen condiciones; ante fallo no se persiste éxito. Roles autorizados: '+c.actors.join(', ')+'. '+c.regla;
 await save(p,d,'06_Secuencias/'+c.id+'_Secuencia.mdj',{caso:c.id});
}
async function activity(c){
 const {p,m}=project(c.id+' — '+c.nombre,'UMLActivity'),d=D(m,'UMLActivityDiagram',c.id+' — Actividad · '+c.nombre);const letters='ABCDEFGH',connectors={};
 text(d,c.id+' · '+c.nombre,70,20,4000,65,28);text(d,'Elegir una operación. Los círculos con la misma letra continúan en el bloque correspondiente.\nLas acciones CRUD son alternativas; se conserva trazabilidad y se validan permisos.',70,100,3900,100,19);
 function node(kind,label,x,y,w=300,h=90,parent=m){const mm=M(kind,label,parent,kind==='UMLControlFlow'?'edges':'nodes');return V(d,kind==='UMLAction'?'UMLActionView':kind==='UMLActivityEdgeConnector'?'UMLActivityEdgeConnectorView':'UMLControlNodeView',mm,x,y,w,h);}
 const start=node('UMLInitialNode','',100,270,35,35),choose=node('UMLDecisionNode','Elegir operación',700,250,65,65),request=node('UMLAction',c.id==='CU01'?'Solicitar acceso o alta':'Acceder con sesión y permisos',240,240,350,100);E(d,'UMLControlFlowView',M('UMLControlFlow','',m,'edges'),start,request,[[135,287],[240,287]]);const f=d.ownedViews.at(-1).model;f.source=start.model;f.target=request.model;const f2=M('UMLControlFlow','',m,'edges');f2.source=request.model;f2.target=choose.model;E(d,'UMLControlFlowView',f2,request,choose,[[590,287],[700,287]]);
 c.branches.forEach((q,k)=>{const mm=M('UMLActivityEdgeConnector',letters[k],m,'nodes');connectors[k]=mm;const v=V(d,'UMLActivityEdgeConnectorView',mm,120+k*530,480,50,50);text(d,q.nombre,70+k*530,545,440,90,18);const flow=M('UMLControlFlow','',m,'edges');flow.source=choose.model;flow.target=mm;flow.guard=letters[k];const e=E(d,'UMLControlFlowView',flow,choose,v,[[732,315],[v.left+25,480]]);e.lineStyle=T.EdgeView.LS_OBLIQUE;});
 const panels=[];const maxOps=Math.max(...c.branches.map(q=>q.ops.length+(q.after?3:0))),ph=620+(maxOps+3)*190;
 for(const [k,q]of c.branches.entries()){
  const ox=70+(k%3)*1330,oy=790+Math.floor(k/3)*(ph+210);text(d,letters[k]+' · '+q.nombre,ox,oy,1230,80,24);
  const role=q.actor==='Todos'?'Usuarios autorizados':q.actor,groups=[M('UMLActivityPartition',role,m,'groups'),M('UMLActivityPartition','SGCC',m,'groups')],lanes=groups.map((g,i)=>{const v=V(d,'UMLSwimlaneView',g,ox+i*610,oy+110,610,ph-100);v.isVertical=true;v.font.size=18;return v});
  const vs=[],entry=V(d,'UMLActivityEdgeConnectorView',connectors[k],ox+260,oy+210,50,50);vs.push(entry);const req=node('UMLAction','Seleccionar: '+q.nombre,ox+105,oy+350,360,100,groups[0]);contain(lanes[0],req);vs.push(req);
  const val=node('UMLAction','Validar permisos, datos y condición de la operación',ox+735,oy+350,360,100,groups[1]);contain(lanes[1],val);vs.push(val);const gate=node('UMLDecisionNode','',ox+880,oy+550,65,65,groups[1]);contain(lanes[1],gate);vs.push(gate);const question=text(d,'¿'+q.condicion+'?',ox+725,oy+470,380,75,17);vs.push(question);
  const steps=q.ops.map((op,i)=>{const v=node('UMLAction',readable(op),ox+715,oy+700+i*190,400,120,groups[1]);v.font.size=16;v.showProperty=false;contain(lanes[1],v);vs.push(v);return v});
  const fail=node('UMLAction',q.alternativa,ox+90,oy+700,380,155,groups[0]);fail.font.size=16;contain(lanes[0],fail);vs.push(fail);const bad=node('UMLActivityFinalNode','',ox+265,oy+955,35,35,groups[0]);vs.push(bad);const good=node('UMLActivityFinalNode','',ox+895,oy+740+(q.ops.length+(q.after?3:0))*190,35,35,groups[1]);vs.push(good);
  const links=[[entry,req,''],[req,val,''],[val,gate,''],[gate,steps[0],'Sí'],[gate,fail,'No'],...steps.slice(1).map((v,i)=>[steps[i],v,'']),[steps.at(-1),good,''],[fail,bad,'']];
  if(q.after){
   const y=oy+735+q.ops.length*190;const gate2=node('UMLDecisionNode','',ox+880,y+60,65,65,groups[1]);vs.push(gate2);contain(lanes[1],gate2);
   vs.push(text(d,q.after.question,ox+710,y-25,410,65,17));
   const yes=node('UMLAction',q.after.yes,ox+715,y+250,400,130,groups[1]),no=node('UMLAction',q.after.no,ox+90,y+240,380,160,groups[0]);vs.push(yes,no);contain(lanes[1],yes);contain(lanes[0],no);
   const fin=node('UMLActivityFinalNode','',ox+265,y+470,35,35,groups[0]);vs.push(fin);
   const i=links.findIndex(z=>z[0]===steps.at(-1)&&z[1]===good);links.splice(i,1,[steps.at(-1),gate2,''],[gate2,yes,'Sí'],[gate2,no,'No'],[yes,good,''],[no,fin,'']);
  }
  const route=require('./rutas').router(vs);for(const [a,z,g]of links){const flow=M('UMLControlFlow','',m,'edges');flow.source=a.model;flow.target=z.model;flow.guard=g;const e=E(d,'UMLControlFlowView',flow,a,z,route(a,z));e.nameLabel.font.size=17;}
  text(d,'Resultado: solo la operación seleccionada. '+(c.id==='CU08'&&[2,3].includes(k)?'Repetir selección y registro por cada producto y lote obtenido. ':''),ox+20,oy+ph+30,1200,85,17);panels.push(oy+ph+140);
 }
 text(d,'Precondición: '+c.pre+'\n'+c.regla,70,Math.max(...panels)+50,3900,230,19);m.documentation='Un diagrama con alternativas internas del caso general. Cada conector de letra es el mismo nodo lógico mostrado en dos lugares. Cada salida de rechazo indica una acción; un fin de rama termina la operación seleccionada, no el sistema. '+c.regla;
 await save(p,d,'05_Actividades/'+c.id+'_Actividad.mdj',{caso:c.id});
}
async function collaboration(c){
 const {p,m}=project(c.id+' — '+c.nombre),pkg=M('UMLPackage','Participantes de análisis',m),co=M('UMLCollaboration',c.nombre,m),inter=M('UMLInteraction',c.id+' — Colaboración',co),d=D(inter,'UMLCommunicationDiagram',c.id+' — Colaboración');d.showSequenceNumber=true;d.sequenceNumbering='custom';
 text(d,c.id+' · '+c.nombre,80,20,2500,65,27);text(d,'Actores autorizados: '+c.actors.join(' · ')+'. Se ejecuta la rama de la operación seleccionada.',80,100,2400,90,18);
 const ps=[['solicitante','Usuario autorizado','actor',100,340],['interfaz','Interfaz'+c.servicio,'boundary',1800,340],['control','Control'+c.servicio,'control',1800,1130],['datos','Repositorio'+c.servicio,'entity',100,1130]],vs=[];
 for(const [n,cl,st,x,y]of ps){const classifier=M(st==='actor'?'UMLActor':'UMLClass',cl,pkg);if(st!=='actor')classifier.stereotype=st;const attr=M('UMLAttribute',n,co,'attributes');attr.type=classifier;const life=M('UMLLifeline',n,inter,'participants');life.represent=attr;vs.push(V(d,'UMLCommLifelineView',life,x,y,400,110));}
 const hosts={};for(const [a,z,pts]of [[0,1,[[500,395],[1800,395]]],[1,2,[[2000,450],[2000,1130]]],[2,3,[[1800,1185],[500,1185]]]]){const r=M('UMLConnector','',co);r.end1.reference=vs[a].model.represent;r.end2.reference=vs[z].model.represent;hosts[[a,z].sort().join(',')]=E(d,'UMLConnectorView',r,vs[a],vs[z],pts);}
 function at(v,e,x,y){const ps=e.points,i=0,a=ps.getPoint(i),z=ps.getPoint(i+1),center={x:(a.x+z.x)/2,y:(a.y+z.y)/2};const q=T.Coord.getPointAwayLine(center,z,0,1000),theta=Math.atan2(-q.y,q.x);v.edgePosition=T.EdgeParasiticView.EP_MIDDLE;v.distance=Math.hypot(x-center.x,y-center.y);v.alpha=Math.atan2(-(y-center.y),x-center.x)-theta;}
 const msgs=[{a:0,z:1,n:'seleccionarOperacion(datos)',number:'1',x:1060,y:265},{a:1,z:2,n:'validarSesionPermisosYOperacion()',number:'1.1',x:2000,y:680},{a:2,z:3,n:'consultarDatosAutorizados()',number:'1.1.1',x:1150,y:1310}];
 let y=1440;c.branches.forEach((q,k)=>{text(d,(k+1)+'. '+q.nombre+' · '+q.condicion,600,y-45,1550,70,17);y+=85;[...q.ops,...(q.after?['si '+q.after.question+': '+q.after.yes,'si no: '+q.after.no]:[])].forEach((op,j)=>{msgs.push({a:2,z:3,n:op,guard:'operación '+(k+1),number:'1.2.'+(k+1)+'.'+(j+1),x:1150,y});y+=100;});y+=65;});
 msgs.push({a:2,z:1,n:'presentarResultadoOAlternativa()',number:'1.3',x:2000,y:900,reply:true},{a:1,z:0,n:'mostrarRespuestaSinEjecutarOtrasRamas()',number:'1.4',x:1100,y:550,reply:true});
 for(const s of msgs){const host=hosts[[s.a,s.z].sort().join(',')],mm=M('UMLMessage',s.n,inter,'messages');mm.source=vs[s.a].model;mm.target=vs[s.z].model;mm.connector=host.model;mm.sequenceNumber=s.number;mm.messageSort=s.reply?'reply':'synchCall';mm.guard=s.guard||'';const v=V(d,'UMLCommMessageView',mm,0,0,40,20);v.hostEdge=host;v.nameLabel.font.size=14;v.nameLabel.wordWrap=true;v.nameLabel.width=1450;at(v,host,s.x,s.y);}
 text(d,'Ramas mutuamente excluyentes: las guardas identifican la operación. Los mensajes al repositorio representan servicios de consulta/persistencia coordinados por el control. Selección de productos y acuerdos procede de la interfaz y del actor autorizado.\n'+c.regla+'\nAlternativas: '+c.branches.map(q=>q.alternativa).join('; '),80,y+100,2450,500,17);
 inter.documentation='Colaboración del caso general con mensajes agrupados por operación. No ejecutar todas las ramas. Participantes de análisis; control no es tabla. '+c.regla;await save(p,d,'02_Colaboracion/'+c.id+'_Colaboracion.mdj',{caso:c.id});
}
module.exports={sequence,activity,collaboration};
