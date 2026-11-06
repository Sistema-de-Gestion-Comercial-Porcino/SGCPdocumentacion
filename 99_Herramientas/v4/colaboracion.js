const b=require('./base'),{project,M,D,V,E,text,rel,save}=b;
const {casos}=require('../especificacion_v3');
function place(v,host,x,y){
 const ps=host.points;let i=Math.floor(ps.count()/2);if(ps.count()%2===0)i--;const a=ps.getPoint(i).copy(),c=ps.getPoint(i+1);
 if(ps.count()%2===0){a.x=Math.floor((a.x+c.x)/2);a.y=Math.floor((a.y+c.y)/2);}
 const q=b.T.Coord.getPointAwayLine(a,c,0,1000),theta=Math.atan2(-q.y,q.x);v.distance=Math.hypot(x-a.x,y-a.y);v.alpha=Math.atan2(-(y-a.y),x-a.x)-theta;
}
async function build(c){
 if(c.id==='CU21')return require('./movil').collaboration();
 const {p,m}=project(c.id+' — Colaboración V4'),design=M('UMLPackage','Participantes de análisis',m),coll=M('UMLCollaboration',c.nombre,m),inter=M('UMLInteraction',c.id+' — Interacción',coll),d=D(inter,'UMLCommunicationDiagram',c.id+' — Colaboración');d.showSequenceNumber=true;d.sequenceNumbering='custom';
 text(d,c.id+' · '+c.nombre,80,20,1800,55,25);
 const participants=[['usuario',c.actor,'actor',90,350,310],['pantalla','Pantalla'+c.servicio+(c.id==='CU01'||c.id==='CU22'?'WebAndroid':'Web'),'boundary',1000,350,370],['control','Control'+c.servicio,'control',1000,1050,370],['datos','Repositorio'+c.servicio,'entity',90,1050,370]];
 if(c.id==='CU10'||c.id==='CU19')participants.push(['externo',c.id==='CU10'?'Balanza':'ProveedorFiscal','external',1980,1050,360]);
 const vs=[];
 for(const[n,type,st,x,y,w]of participants){const cl=M(st==='actor'?'UMLActor':'UMLClass',type,design);if(st!=='actor')cl.stereotype=st;const part=M('UMLAttribute',n,coll,'attributes');part.type=cl;const life=M('UMLLifeline',n,inter,'participants');life.represent=part;const v=V(d,'UMLCommLifelineView',life,x,y,w,100);v.stereotypeDisplay='label';vs.push(v);}
 const links={};
 for(const[a,c,pts]of [[0,1,[[400,400],[1000,400]]],[1,2,[[1185,450],[1185,1050]]],[2,3,[[1000,1100],[460,1100]]],...(vs.length===5?[[2,4,[[1370,1100],[1980,1100]]]]:[])]){
  const r=M('UMLConnector','',coll);r.end1.reference=vs[a].model.represent;r.end2.reference=vs[c].model.represent;
  links[[a,c].sort().join(',')]=E(d,'UMLConnectorView',r,vs[a],vs[c],pts);
 }
 const messages=[];
 const add=(a,z,n,guard='',reply=false)=>messages.push({a,z,n,guard,reply});
 add(0,1,'solicitar '+c.nombre);add(1,2,c.validar+'()');add(2,3,'consultar('+c.entidades.slice(0,2).join(', ')+')');add(3,2,'datos actuales','',true);
 if(vs.length===5){add(2,4,c.id==='CU10'?'capturarPeso()':'solicitarEmision(referenciaUnica)',c.id==='CU10'?'control apto':'integración habilitada; datos válidos; sin emisión confirmada');add(4,2,c.id==='CU10'?'peso o error':'respuesta fiscal o error','',true);}
 for(const op of c.operaciones.filter(op=>!(c.id==='CU19'&&op==='solicitarEmision')))add(2,3,op+'()','válido');
 add(2,3,c.operacionAlternativa+'()','alternativa');add(3,2,'resultado de la rama ejecutada','',true);add(2,1,'presentar resultado o alternativa','',true);add(1,0,'mostrar respuesta','',true);
 const counts={};
 for(const[msgIndex,s]of messages.entries()){
  const key=[s.a,s.z].sort().join(','),host=links[key],i=counts[key]||0;counts[key]=i+1;
  const mm=M('UMLMessage',s.n,inter,'messages');mm.source=vs[s.a].model;mm.target=vs[s.z].model;mm.connector=host.model;mm.messageSort=s.reply?'reply':'synchCall';mm.sequenceNumber=String(msgIndex+1);mm.guard=s.guard;
  const v=V(d,'UMLCommMessageView',mm,0,0,40,20);v.hostEdge=host;v.nameLabel.font.size=16;
  let x,y;if(key==='0,1'){x=700;y=i===0?255:520;}
  else if(key==='1,2'){x=1185;y=i===0?640:850;v.nameLabel.alpha=0;v.nameLabel.distance=310;}
  else if(key==='2,3'){x=710;y=1220+i*85;}
  else{x=1660;y=1240+i*140;}
  place(v,host,x,y);
 }
 const bottom=Math.max(1940,1260+(counts['2,3']||0)*85);
 text(d,'[válido]: '+c.condicion+'.\n[alternativa]: '+c.alternativa+'.\nPrecondición: '+c.pre+'.\nCanal: '+c.canal+'.\n'+(c.regla||''),90,bottom,vs.length===5?2200:1750,310,17);
 inter.documentation='Mensajes numerados por orden de ejecución. Válido y alternativa son ramas mutuamente excluyentes; las respuestas finales corresponden a la rama ejecutada. Los mensajes síncronos de persistencia se ejecutan dentro de la operación del control; el repositorio no toma decisiones comerciales. Las clases boundary/control/repository son participantes de diseño, no nuevas tablas del modelo de dominio. Fuente: '+c.fuente+'. Resultado: '+c.post+'.';
 await save(p,d,'02_Colaboracion/'+c.id+'_Colaboracion.mdj',{caso:c.id});
}
module.exports={build,casos};
