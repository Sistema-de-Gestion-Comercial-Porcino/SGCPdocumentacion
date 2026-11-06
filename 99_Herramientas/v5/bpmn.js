// Un proceso y un diagrama por modelo. Los carriles se repiten visualmente por tramo;
// todos referencian al mismo participante y los mismos roles. Enlaces BPMN reemplazan
// únicamente las continuaciones largas: cada código tiene un único evento receptor.
const b=require('./base'),{M,D,V,E,text,project,contain,points,rt,fs,path}=b;
const ROOT=b.ROOT,T=b.T;
const TMP=process.env.SGCC_BPMN_STAGE||'/tmp/sgcc_reorganizacion_20261029/BPMN';
fs.mkdirSync(TMP,{recursive:true});
const PW=2780,LH=370,GAP=80,ROW=1900;
const {specs}=require('./procesos');

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
 text(d,(proposed?'ACCESO Y DATOS BASE: 0. OPERACIÓN: 1 > 2 > 5 > 6 > 7 > 8. REPORTES: 9. ':'OPERACIÓN MANUAL: 1 > 2 > 5 > 6 > 7 > 8. ')+'Faltante: 2 > 3 / 4 > 2. Incidencias: 4. Enlaces con el mismo nombre continúan el flujo.',60,100,11200,70,21);
 text(d,'Cada tramo muestra de nuevo los carriles necesarios de la misma chanchería. No son procesos separados. Todas las decisiones tienen sus salidas rotuladas.',60,165,11200,50,18);
 for(const stage of stages){
  const k=stages.indexOf(stage),ox=60+(k%4)*(PW+GAP),oy=260+Math.floor(k/4)*ROW;
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
   const destinations={'SEÑA':2,'STOCK':2,'PRODUCIR':3,'RECIBIR':4,'ACUERDO':4,'COBRO':5,'DESPACHO':6,'RECEPCIÓN':7,'SALDO':8,'COMERCIAL':1,'MENÚ':0,'REPORTES':9};
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
  for(let attempt=0;attempt<90&&!routed;attempt++){
   const route=require('../rutas_bpmn_limpias').router([...Object.values(map).map(x=>x.v),...labels],reserved);
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
 m.documentation='Un proceso completo. Tramos horizontales en una sola lámina; los pools y carriles repetidos son vistas del mismo participante y los mismos roles. Enlaces BPMN por nombre, un único receptor por código. No hay subprocesos ocultos. '+(proposed?'SGCC visible en automatizaciones; web online y Android con recepción offline limitada.':'AS IS manual conservado con precios, preparación, control sanitario, pagos, entrega y deuda.');
 const file='BPMN_'+(proposed?'Propuesto':'Actual');
 await rt.render(d,path.join(TMP,file+'.pdf'));const arranged=rt.app.repository.get(d._id);placeConditions(arranged);const dims=await rt.render(arranged,path.join(TMP,file+'.pdf'));const normalized=rt.app.repository.get(p._id);
 fs.writeFileSync(path.join(TMP,file+'.mdj'),rt.app.repository.writeObject(normalized));
 fs.writeFileSync(path.join(TMP,file+'_resumen.json'),JSON.stringify({dimensiones:dims,tramos:meta},null,2));console.log(file,dims);
}
module.exports={build,specs,placeConditions};if(require.main===module)(async()=>{await build(false);await build(true)})().catch(e=>{console.error(e);process.exitCode=1});
