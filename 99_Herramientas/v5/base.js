const fs=require('fs'),path=require('path');
const rt=require('../staruml_runtime'),T=rt.T;
const ROOT=path.resolve(__dirname,'../..');
const OUT=process.env.SGCC_V5_OUT||'/tmp/sgcc_reorganizacion_20261029/Software';
const PDF=process.env.SGCC_V5_PDF||'/tmp/sgcc_reorganizacion_20261029/Previsualizacion';
const manifest=[];
function own(p,o,f='ownedElements'){o._parent=p;(p[f]||(p[f]=[])).push(o);return o;}
function M(t,n,p,f){const o=new T[t]();o.name=n||'';if(p)own(p,o,f);return o;}
function project(n,kind='UMLModel'){const p=M('Project',n),m=M(kind,n,p);return {p,m};}
function D(m,t,n){const d=M(t,n,m);d.defaultDiagram=true;return d;}
function style(v,size=15){v.font.face='Arial';v.font.size=size;v.lineColor='#303744';v.fontColor='#202735';v.fillColor='#ffffff';v.showShadow=false;v.wordWrap=true;return v;}
function V(d,t,m,x,y,w,h){const v=style(new T[t]());v.model=m;v.left=x;v.top=y;v.width=w;v.height=h;own(d,v,'ownedViews');return v;}
function text(d,s,x,y,w,h=45,size=20){const v=V(d,'UMLTextView',null,x,y,w,h);v.text=s;v.font.size=size;return v;}
function points(v,p){v.points.clear();p.forEach(q=>v.points.add(new T.Point(...q)));}
function E(d,t,m,a,b,p){const v=style(new T[t](),13);v.model=m;v.tail=a;v.head=b;v.lineStyle=T.EdgeView.LS_RECTILINEAR;v.showVisibility=false;v.showProperty=false;points(v,p);own(d,v,'ownedViews');if(v.nameLabel){v.nameLabel.font.size=13;v.nameLabel.distance=18;}return v;}
function rel(p,t,a,b,n='',f){const m=M(t,n,p,f);m.source=a.model||a;m.target=b.model||b;return m;}
function assoc(p,d,a,b,ma='',mb='',name='',route,kind='UMLAssociation'){
 const r=M(kind,name,p);r.end1.reference=a.model;r.end2.reference=b.model;r.end1.multiplicity=ma;r.end2.multiplicity=mb;r.end1.navigable='unspecified';r.end2.navigable='unspecified';
 return E(d,kind==='UMLLink'?'UMLLinkView':kind==='UMLCommunicationPath'?'UMLCommunicationPathView':'UMLAssociationView',r,a,b,route);
}
function contain(a,b){b.containerView=a;a.containedViews.push(b);}
async function save(p,d,file,extra={}){
 const dest=path.join(OUT,file),pdf=path.join(PDF,file.replace(/\.mdj$/,'.pdf'));
 fs.mkdirSync(path.dirname(dest),{recursive:true});fs.mkdirSync(path.dirname(pdf),{recursive:true});
 await rt.render(d,pdf);
 const arranged=rt.app.repository.get(d._id);separateLabels(arranged);
 const dims=await rt.render(arranged,pdf);const norm=rt.app.repository.get(p._id);
 fs.writeFileSync(dest,rt.app.repository.writeObject(norm));
 manifest.push({archivo:path.relative(ROOT,dest),pdf:path.relative(ROOT,pdf),tipo:d.constructor.name,...dims,...extra});
 console.log(file,dims.width+'x'+dims.height);return norm;
}
function separateLabels(d){
 if(d instanceof T.UMLSequenceDiagram)return;
 const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas;
 const scratch=new Doc({size:[100,100],margin:0}),canvas=new Canvas(scratch);
 const nodes=d.ownedViews.filter(v=>v instanceof T.NodeView&&!(v instanceof T.ParasiticView)&&!['UMLPackageView','UMLUseCaseSubjectView'].includes(v.constructor.name));
 const edges=d.ownedViews.filter(v=>v instanceof T.EdgeView);
 const labels=edges.flatMap(e=>e.subViews.filter(v=>v instanceof T.EdgeLabelView&&v.visible&&v.text));
 const overlap=(a,c,pad=4)=>Math.min(a.left+a.width+pad,c.left+c.width)-Math.max(a.left-pad,c.left)>0&&Math.min(a.top+a.height+pad,c.top+c.height)-Math.max(a.top-pad,c.top)>0;
 for(let pass=0;pass<4;pass++)for(const l of labels){
  const collisions=()=>nodes.filter(n=>overlap(l,n)).length*10000+labels.filter(x=>x!==l&&overlap(l,x)).length*3000+(l.left<25||l.top<85?10000:0);
  if(!collisions())continue;
  const oldA=l.alpha,oldD=l.distance;let best={cost:Infinity};
  for(const dist of [18,25,35,48,65,85,110,145,190,240])for(const angle of [oldA,...Array.from({length:24},(_,i)=>i*Math.PI/12-Math.PI)]){
   l.distance=dist;l.alpha=angle;l.arrangeObject(canvas);
   const score=collisions()+Math.abs(dist-oldD)*.4+Math.abs(angle-oldA)*3;
   if(score<best.cost)best={cost:score,dist,angle};
  }
  l.distance=best.dist;l.alpha=best.angle;l.arrangeObject(canvas);
 }
 scratch.end();
}
module.exports={fs,path,rt,T,ROOT,OUT,PDF,manifest,own,M,project,D,V,E,text,points,rel,assoc,contain,save,separateLabels};
