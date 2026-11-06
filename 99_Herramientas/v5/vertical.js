// BPM vertical: actores en columnas, una actividad completa por modelo.
// Reutiliza las reglas vigentes del BPMN; las representa con notación de actividad.
const {specs}=require('./bpmn');
const b=require('./base'),{M,D,V,E,text,project,contain,rt,T,fs,path}=b;
const OUT=process.env.SGCC_VERTICAL_STAGE||'/tmp/sgcc_reorganizacion_20261029/BPM';fs.mkdirSync(OUT,{recursive:true});
const dests={'SEÑA':[2,'A'],'STOCK':[2,'B'],'PRODUCIR':[3,'C'],'RECIBIR':[4,'D'],'ACUERDO':[4,'E'],'COBRO':[5,'F'],'DESPACHO':[6,'G'],'RECEPCIÓN':[7,'H'],'SALDO':[8,'I'],'MENÚ':[0,'J'],'COMERCIAL':[1,'K'],'REPORTES':[9,'L']};
const ranks={
 1:{i:0,precios:1,margen:2,ajuste:2,publicar:3,solicitud:4,acepta:5,cambios:6,cambiar:6,rechazar:7,finRechazo:8,confirmar:7,linkSeña:8,solicitarCliente:3.6},
 2:{inSeña:0,recibeSeña:1,registrarSeña:2,stock:1,mergeStock:2,consultar:3,hay:4,reservar:5,mas:6,otro:7,listo:7,pago:8,reponer:5,fecha:6,aceptaFecha:7,tipoOrigen:8,producir:9,espera:9,incFecha:8},
 3:{prodIn:0,plan:1,derivado:2,sanidad:3,apto:4,faenar:5,insumos:3,abastecer:4,fabricar:4,calidad:5,lotes:6,termino:7,finReal:8,recibirProd:9,bloquear:7,incProd:8},
 4:{recibirIn:0,esperar:1,recibido:2,revisar:3,loteApto:4,ingreso:5,stockBack:6,retraso:3,retener:5,acuerdoIn:0,mergeInc:2,negociar:3,hayAcuerdo:4,pendiente:5,continua:5,actualizar:6,retStock:7,cancelar:6,finCancel:7},
 5:{cobroIn:0,totales:1,medio:2,contado:3,credito:3,mergeDin:4,dinero:5,registro:6,habilita:7,esperaPago:8,aDespacho:8},
 6:{despIn:0,fiscal:1,emitir:2,fiscalPend:2,mergeDesp:3,local:4,retiro:5,ruta:5,frio:6,mergeEntrega:7,aEntrega:8},
 7:{entIn:0,entregar:1,verificarCliente:2,confirmSync:3,sinSync:4,sync:5,conforme:4,observada:6,cerrar:6,saldoNext:7},
 8:{saldoIn:0,saldo:1,deuda:2,cerrado:3,fin:4,mantener:3,fechaCobro:4,contactar:5,abono:6,registrarAbono:7,reagendar:7}
};
const slots={1:{ajuste:1,cambiar:0,rechazar:1,finRechazo:1},2:{registrarSeña:1,otro:1,reponer:1,fecha:0,aceptaFecha:0,tipoOrigen:1,producir:0,espera:1,incFecha:1},3:{insumos:1,abastecer:2,fabricar:1,calidad:1,lotes:1,bloquear:1,incProd:1},4:{retraso:1,retener:1,pendiente:1,cancelar:1,finCancel:1},5:{credito:1,esperaPago:1},6:{fiscalPend:1,ruta:1,frio:1},7:{sinSync:1,sync:1,observada:1},8:{mantener:1,fechaCobro:1,contactar:1,abono:1,registrarAbono:1}};
function prepare(p){
 const stages=specs(p);
 for(const s of stages){
  if(s.num===1){s.nodes.push({id:'solicitarCliente',kind:'task',role:'Comprador',label:p?'Solicitar productos por portal, WhatsApp o en el local':'Solicitar productos por WhatsApp o en el local'});s.edges=s.edges.filter(e=>!(e.a==='publicar'&&e.z==='solicitud'));s.edges.push({a:'publicar',z:'solicitarCliente',label:''},{a:'solicitarCliente',z:'solicitud',label:''});}
  if(s.num===7){s.nodes.push({id:'verificarCliente',kind:'task',role:'Comprador',label:'Verificar productos y peso; indicar conformidad u observaciones'});const edge=s.edges.find(e=>e.a==='entregar');edge.a='verificarCliente';s.edges.push({a:'entregar',z:'verificarCliente',label:''});}
  for(const n of s.nodes){
   n.rank=ranks[s.num]?.[n.id]??n.col;n.slot=slots[s.num]?.[n.id]??n.row??0;n.system=n.role==='SGCC';
   if(n.system&&[0,9].includes(s.num))n.role='Propietario / administración';
   else if(n.system){n.role=[2,4].includes(s.num)&&!['registrarSeña'].includes(n.id)?'Almacén':s.num===7?'Responsable de entrega':'Ventas / cobranza';}
   if(['acepta','cambios','aceptaFecha','conforme'].includes(n.id))n.role='Comprador';
   if(p&&s.num===1&&['precios','margen','ajuste','publicar'].includes(n.id))n.role='Propietario / administración';
   if(p&&s.num===0){n.rank={inicioSistema:0,accederSistema:1,sesionValida:2,denegarAcceso:2,menuIn:3,elegirOperacion:4,datosBase:5,validarCatalogo:6,volverMenu:7,comercial:5,reportes:6,cerrarSesion:7,finSesion:8}[n.id];n.slot=['denegarAcceso','datosBase','validarCatalogo','volverMenu'].includes(n.id)?1:0;}
   if(p&&s.num===9){n.rank={reporteIn:0,filtrosReporte:1,autorizarReporte:2,denegarReporte:3,consultarReporte:3,mostrarReporte:4,exportarReporte:5,generarReporte:6,regresarReporte:7}[n.id];n.slot=['denegarReporte','generarReporte'].includes(n.id)?1:0;}
   if(p&&s.num===3&&['pesarResultados','pesajesValidos','corregirPesaje','finReal','recibirProd'].includes(n.id)){n.rank={pesarResultados:8,pesajesValidos:9,corregirPesaje:9,finReal:10,recibirProd:11}[n.id];n.slot=n.id==='corregirPesaje'?1:0;}
   if(!p&&n.role==='Almacén')n.role='Producción';
   if(p&&s.num===3&&n.id==='abastecer')n.slot=0;
   if(!p&&s.num===7&&['conforme','observada','cerrar','saldoNext'].includes(n.id))n.rank={conforme:3,observada:4,cerrar:4,saldoNext:5}[n.id];
   if(n.system&&n.kind==='task')n.label='En SGCC: '+n.label.charAt(0).toLowerCase()+n.label.slice(1);
   if(p&&n.id==='precios')n.label='Definir costo de referencia y precio por producto en SGCC';
   if(p&&n.id==='finReal')n.label='Guardar fin real en SGCC; entregar lotes a Almacén';
   if(!p&&n.id==='finReal')n.label='Anotar fin real; pasar lotes a recepción y revisión';
   if(p&&n.id==='entregar')n.label='Entregar; capturar receptor, peso, fecha y evidencia en web / Android';
   if(n.id==='registro')n.slot=0;
   if(!Number.isFinite(n.rank))throw Error('Sin posición '+n.id);
  }
 }
 return stages;
}
function labels(d){
 const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas,scratch=new Doc({size:[100,100],margin:0}),canvas=new Canvas(scratch);
 const overlap=(a,c,pad=5)=>Math.min(a.left+a.width+pad,c.left+c.width)>Math.max(a.left-pad,c.left)&&Math.min(a.top+a.height+pad,c.top+c.height)>Math.max(a.top-pad,c.top);
 const obstacles=d.ownedViews.filter(v=>['UMLActionView','UMLControlNodeView','UMLActivityEdgeConnectorView','UMLTextView'].includes(v.constructor.name)),placed=[],edges=d.ownedViews.filter(v=>v.constructor.name==='UMLControlFlowView');
 const seg=e=>Array.from({length:e.points.count()-1},(_,i)=>[e.points.getPoint(i),e.points.getPoint(i+1)]);
 const dist=(x,y,a,z)=>{const dx=z.x-a.x,dy=z.y-a.y,t=Math.max(0,Math.min(1,((x-a.x)*dx+(y-a.y)*dy)/(dx*dx+dy*dy||1)));return Math.hypot(x-a.x-t*dx,y-a.y-t*dy)};
 function cuts(l,a,z){const left=l.left-5,right=l.left+l.width+5,top=l.top-5,bottom=l.top+l.height+5;return a.x===z.x?a.x>left&&a.x<right&&Math.min(Math.max(a.y,z.y),bottom)>Math.max(Math.min(a.y,z.y),top):a.y>top&&a.y<bottom&&Math.min(Math.max(a.x,z.x),right)>Math.max(Math.min(a.x,z.x),left)}
 function place(l,e,x,y){l.edgePosition=T.EdgeParasiticView.EP_MIDDLE;const ps=e.points;let i=Math.floor(ps.count()/2);if(ps.count()%2===0)i--;const a=ps.getPoint(i).copy(),z=ps.getPoint(i+1);if(ps.count()%2===0){a.x=(a.x+z.x)/2;a.y=(a.y+z.y)/2;}const q=T.Coord.getPointAwayLine(a,z,0,1000),theta=Math.atan2(-q.y,q.x);l.distance=Math.hypot(x-a.x,y-a.y);l.alpha=Math.atan2(-(y-a.y),x-a.x)-theta;l.arrangeObject(canvas);}
 for(const e of edges.filter(v=>v.model.guard)){
  const l=e.nameLabel;l.fontColor=e.lineColor;let best;let distance=0;
  for(const [a,z]of seg(e)){const len=Math.abs(z.x-a.x)+Math.abs(z.y-a.y);if(len<20){distance+=len;continue;}
   for(const f of [.25,.5,.75])for(const off of [24,-24,36,-36,52,-52,70,-70]){
    const x=a.x+(z.x-a.x)*f+(a.x===z.x?off:0),y=a.y+(z.y-a.y)*f+(a.y===z.y?off:0);place(l,e,x,y);const hit=[...obstacles,...placed].filter(n=>overlap(l,n)).length;
    const cx=l.left+l.width/2,cy=l.top+l.height/2,own=dist(cx,cy,a,z);let cut=0,other=Infinity;
    for(const edge of edges)for(const [u,v]of seg(edge)){if(cuts(l,u,v))cut++;if(edge!==e)other=Math.min(other,dist(cx,cy,u,v));}
    const score=hit*1e6+cut*1e5+Math.max(0,own+12-other)*1e4+distance+len*f+Math.abs(off);if(!best||score<best.score)best={score,x,y};
   }distance+=len;
  }if(best)place(l,e,best.x,best.y);placed.push(l);
 }scratch.end();
}
async function build(proposed){
 const name='BPM '+(proposed?'propuesto':'actual')+' — Flujo completo actualizado',file=proposed?'Modelo_Propuesto':'Modelo_Actual';
 const {p,m}=project(name,'UMLActivity'),d=D(m,'UMLActivityDiagram',name),stages=prepare(proposed),laneModels={},laneViews={},connectors={};
 const roleSpecs=[['Comprador',440],...(proposed?[['Propietario / administración',850]]:[]),['Ventas / cobranza',850],['Producción',1040],...(proposed?[['Almacén',760]]:[]),['Responsable de entrega',850]];
 let x=70;const columns={};for(const [role,w]of roleSpecs){columns[role]={left:x,width:w};x+=w;}const fullWidth=x-70;
 let top=450;for(const s of stages){s.top=top;s.height=300+Math.max(...s.nodes.map(n=>n.rank))*190;top+=s.height+160;}const bottom=top;
 text(d,name,70,25,fullWidth,65,29);
 text(d,(proposed?'Acceso y datos base: 0. Reportes: 9. ':'')+'Recorrido vertical: 1, 2, 5, 6, 7 y 8. Faltante: 2, 3 / 4 y regreso a 2.',70,105,fullWidth,50,21);
 text(d,'Los círculos con la misma letra conectan el mismo flujo. Ejemplo: B continúa en STOCK del tramo 2. No son finales.',70,160,fullWidth,50,20);
 text(d,proposed?'SGCC = sistema de gestión. Web con conexión; Android para recepción asignada y descargada. Verde: registro o apoyo del sistema.':'Operación actual manual: precios, solicitudes, preparación, entrega y cobranza mediante atención directa y anotaciones.',70,215,fullWidth,65,19);
 for(const [role,w]of roleSpecs){const title=proposed?role:role==='Ventas / cobranza'?'Propietario / atención y cobro':role==='Producción'?'Producción: carne, derivados y existencias':role;const lm=M('UMLActivityPartition',title,m,'groups'),lv=V(d,'UMLSwimlaneView',lm,columns[role].left,320,w,bottom-320);lv.isVertical=true;lv.font.size=20;lv.fillColor='#f2f5f9';laneModels[role]=lm;laneViews[role]=lv;}
 for(const [code,[num,letter]]of Object.entries(dests)){if(!stages.some(s=>s.nodes.some(n=>n.code===code)))continue;const c=M('UMLActivityEdgeConnector',letter,m,'nodes');c.documentation=code+' — continuación en tramo '+num;connectors[code]=c;}
 const meta=[];
 for(const s of stages){
  text(d,String(s.num).padStart(2,'0')+' · '+s.title,85,s.top-25,fullWidth-30,55,24);
  const map={},obstacles=[];
  for(const n of s.nodes){const c=columns[n.role];const cx=c.left+(n.role==='Comprador'?c.width/2:n.role==='Producción'?[185,520,855][n.slot]:n.slot?c.width-210:210),cy=s.top+130+n.rank*190;let type,vtype,w,h;
   if(['task','wait'].includes(n.kind)){type='UMLAction';vtype='UMLActionView';w=n.role==='Comprador'?300:280;h=100;}
   else if(['gate','merge'].includes(n.kind)){type=n.kind==='gate'?'UMLDecisionNode':'UMLMergeNode';vtype='UMLControlNodeView';w=h=n.kind==='gate'?62:36;}
   else if(n.code){type='UMLActivityEdgeConnector';vtype='UMLActivityEdgeConnectorView';w=h=50;}
   else{type=n.kind==='start'?'UMLInitialNode':'UMLActivityFinalNode';vtype='UMLControlNodeView';w=h=36;}
   const mm=n.code?connectors[n.code]:M(type,n.label,laneModels[n.role],'nodes');if(!n.code)mm.documentation='Tramo '+s.num+' · '+n.id;
   const vv=V(d,vtype,mm,cx-w/2,cy-h/2,w,h);vv.font.size=n.code?23:18;vv.fillColor=n.kind==='gate'?'#fff0c2':n.kind==='wait'?'#ece8f6':proposed&&n.system?'#def1e6':'#f1f5fb';contain(laneViews[n.role],vv);obstacles.push(vv);
   if(vtype==='UMLActionView'){vv.showProperty=false;vv.font.size=17;vv.nameCompartment.width=w;vv.nameCompartment.nameLabel.width=w-20;vv.nameCompartment.nameLabel.font.style=0;}
   if(['gate','start','end'].includes(n.kind)||n.code){const label=n.code?(n.kind==='throw'?'Continuar: ':'Retomar: ')+n.code+' ('+dests[n.code][0]+')':n.label;const yy=n.kind==='gate'?cy-100:cy+36;const tv=text(d,label,cx-150,yy,300,60,n.kind==='gate'?18:16);tv.horzAlign=T.Canvas.AL_CENTER;obstacles.push(tv);}
   map[n.id]={m:mm,v:vv,n};
  }
  const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas,sizing=new Doc({size:[100,100],margin:0}),cv=new Canvas(sizing);
  rt.app.repository.readObject(rt.app.repository.writeObject(p));const sized=rt.app.repository.get(d._id);
  for(let k=0;k<3;k++)sized.arrangeDiagram(cv);
  for(const q of Object.values(map))if(q.v.constructor.name==='UMLActionView'){
   const nv=rt.app.repository.get(q.v._id);q.v.height=Math.max(100,nv.minHeight);q.v.width=Math.max(q.v.width,nv.minWidth);
  }sizing.end();
  let routed,last;
  for(let attempt=0;attempt<90&&!routed;attempt++){
   const route=require('../rutas_bpmn_limpias').router(obstacles);let seed=s.num*100+attempt;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
   const es=s.edges.map((e,i)=>({...e,order:attempt===0?i:attempt===1?-i:rand()})).sort((a,b)=>a.order-b.order),result=[];
   try{for(const e of es){const a=map[e.a],z=map[e.z];result.push({e,pts:route(a.v,z.v)})}routed=result;}catch(err){last=err.message;}
  }
  if(!routed)throw Error((proposed?'Propuesto':'Actual')+' tramo '+s.num+': '+last);
  for(const {e,pts}of routed){const a=map[e.a],z=map[e.z],flow=M('UMLControlFlow','',m,'edges');flow.source=a.m;flow.target=z.m;flow.guard=e.label;const ev=E(d,'UMLControlFlowView',flow,a.v,z.v,pts);ev.lineColor=e.label.startsWith('Sí')?'#216247':e.label.startsWith('No')?'#944829':'#344252';ev.nameLabel.font.size=17;}
  text(d,s.note,90,s.top+s.height-15,fullWidth-40,95,17);
  meta.push({tramo:s.num,titulo:s.title,arriba:s.top,alto:s.height,nodos:s.nodes.length,flujos:s.edges.length});console.log(file,'tramo',s.num,'listo');
 }
 m.documentation='BPM vertical actualizado a partir de las reglas vigentes de Ingeniería de Software. Un solo proceso con actores en columnas; conectores de continuidad nativos evitan líneas largas. Incluye preparación, sanidad, inventario, cobro y entrega dentro del mismo flujo. '+(proposed?'Web online y Android limitado a recepción.':'Actual manual; las alternativas precisan las condiciones sin atribuir automatización.');
 await rt.render(d,path.join(OUT,file+'.pdf'));labels(rt.app.repository.get(d._id));const dims=await rt.render(rt.app.repository.get(d._id),path.join(OUT,file+'.pdf'));
 fs.writeFileSync(path.join(OUT,file+'.mdj'),rt.app.repository.writeObject(rt.app.repository.get(p._id)));const pdfSize=await exportPDF(rt.app.repository.get(d._id),path.join(OUT,file+'.pdf'));fs.writeFileSync(path.join(OUT,file+'_resumen.json'),JSON.stringify({dimensiones:dims,pdf:pdfSize,tramos:meta},null,2));console.log(file,dims);
}
async function exportPDF(d,file){
 const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas,scratch=new Doc({size:[100,100],margin:0}),canvas=new Canvas(scratch);
 for(let i=0;i<3;i++)d.arrangeDiagram(canvas);const box=d.getBoundingBox(canvas),w=Math.ceil(box.x2+35),h=Math.ceil(box.y2+35),scale=Math.min(1,14000/w,14000/h);scratch.end();
 const width=Math.ceil(w*scale),height=Math.ceil(h*scale),pdf=new Doc({size:[width,height],margin:0,compress:true,info:{Title:d.name,Author:'Equipo SGCC',Subject:'Proyecto de Sistemas — BPM vertical'}}),out=fs.createWriteStream(file);pdf.pipe(out);pdf.scale(scale);d.drawDiagram(new Canvas(pdf),false);pdf.end();await new Promise((resolve,reject)=>{out.on('finish',resolve);out.on('error',reject)});return {width,height,scale};
}
module.exports={build,prepare,labels,exportPDF};if(require.main===module)(async()=>{await build(false);await build(true)})().catch(e=>{console.error(e);process.exitCode=1});
