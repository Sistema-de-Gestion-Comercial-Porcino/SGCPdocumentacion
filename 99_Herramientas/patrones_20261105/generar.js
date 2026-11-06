const fs=require('fs'),path=require('path');
const b=require('../v5/base'),{M,D,V,rel}=b,rt=b.rt,T=b.T;
const vizlib=require('./.deps/viz/package/dist/viz.cjs');
const specs=require('./especificacion.json'),ROOT=path.resolve(__dirname,'../..'),TMP='/tmp/sgcp_patrones_20261105';
const PDF=rt.req('node_modules/pdfkit');const measure=new PDF({size:[100,100]});
const manifest=[];
function E(...args){const v=b.E(...args);v.font.size=28;for(const x of v.subViews||[])if(x.font)x.font.size=28;return v}
function dimension(n){measure.font('Helvetica').fontSize(32);const lines=[n.name,...n.attrs.map(x=>'-'+x),...n.ops.map(x=>'+'+x)];const w=Math.max(420,...lines.map(x=>measure.widthOfString(x)+75));return {w:Math.ceil(w),h:Math.ceil(115+(n.attrs.length+n.ops.length)*45+(n.kind==='interface'?45:0))}}
function operation(m,signature,abstract=false){const s=signature.match(/^([^()]+)\(([^)]*)\)(?::\s*(.+))?$/);const o=M('UMLOperation',s?s[1]:signature,m,'operations');o.visibility='public';o.isAbstract=abstract;
 if(s){for(const arg of s[2].split(',').filter(Boolean)){const [name,type]=arg.trim().split(':');const p=M('UMLParameter',name,o,'parameters');p.type=(type||'Object').trim();p.direction='in'}if(s[3]){const p=M('UMLParameter','',o,'parameters');p.type=s[3];p.direction='return'}}
 if(m.name==='Importador'){o.visibility=o.name==='importar'?'public':'protected';o.isAbstract=o.name==='convertir';o.isLeaf=o.name==='importar'}
 return o;
}
(async()=>{const viz=await vizlib.instance();
for(const category of ['estructurales','comportamiento']){
 const title=category==='estructurales'?'Estructurales':'Comportamiento';const dir=path.join(ROOT,'02_Ingenieria_de_Software/Patrones de diseño',category==='estructurales'?'Patrones estructurales':'Patrones de comportamiento');fs.mkdirSync(path.join(dir,'Diagramas'),{recursive:true});fs.mkdirSync(path.join(TMP,category),{recursive:true});
 const project=M('Project',`SGCP · Patrones ${category}`);const groups=[M('UMLModel','01 · Aplicados al sistema',project),M('UMLModel','02 · Ejemplos externos',project)];let index=0;
 for(const spec of specs.filter(s=>s.category===category)){
  index++;const model=M('UMLModel',String(index).padStart(2,'0')+' · '+spec.name,groups[spec.apply?0:1]);model.documentation=[spec.scope,spec.intent,spec.reason,spec.scenario,spec.flow,spec.caution].join('\n\n');
  const d=D(model,'UMLClassDiagram',`${String(index).padStart(2,'0')} · ${spec.name} · ${spec.apply?'SGCP':'Ejemplo'}`);d.defaultDiagram=index===1;
  const sizes=spec.nodes.map(dimension),nid=new Map(spec.nodes.map((n,i)=>[n.name,'n'+i]));
  let dot='digraph G { graph[rankdir=TB,splines=ortho,nodesep=1.5,ranksep=1.9,pad=0.2,outputorder=edgesfirst]; node[shape=box,fixedsize=true,label=""]; edge[arrowsize=0.5];';
  spec.nodes.forEach((n,i)=>dot+=`n${i}[width=${sizes[i].w/72},height=${sizes[i].h/72}];`);
  spec.links.forEach((l,i)=>{const rev=['gen','real'].includes(l.kind);const from=nid.get(rev?l.b:l.a),to=nid.get(rev?l.a:l.b);dot+=`${from}->${to}[id="e${i}"${!rev&&spec.links.some(x=>['gen','real'].includes(x.kind)&&x.a===l.a&&x.b===l.b)?',constraint=false':''}];`;});dot+='}';
  const options=['TB','LR'].map(direction=>{const source=dot.replace('rankdir=TB','rankdir='+direction),graph=viz.renderJSON(source),bb=graph.bb.split(',').map(Number);return {source,graph,score:Math.min(648/(bb[2]+100),374/(bb[3]+100))}}).sort((a,b)=>b.score-a.score);
  dot=options[0].source;fs.writeFileSync(path.join(TMP,category,spec.slug+'.dot'),dot);const graph=options[0].graph;const H=Number(graph.bb.split(',')[3]),nodes={};
  spec.nodes.forEach((n,i)=>{const obj=graph.objects.find(x=>x.name==='n'+i),[cx,cy]=obj.pos.split(',').map(Number);const m=M(n.kind==='interface'?'UMLInterface':'UMLClass',n.name,model);m.isAbstract=n.kind==='abstract';m.documentation=n.role||spec.scenario;
   for(const at of n.attrs){const [name,type]=at.split(':');const a=M('UMLAttribute',name,m,'attributes');a.type=type.trim();a.visibility='private';if(['TipoArbol','RecuerdoTexto'].includes(n.name))a.isReadOnly=true;}
   n.ops.forEach(sig=>operation(m,sig,n.kind==='interface'||n.name==='Figura'));
   const v=V(d,n.kind==='interface'?'UMLInterfaceView':'UMLClassView',m,Math.round(cx-sizes[i].w/2+50),Math.round(H-cy-sizes[i].h/2+50),sizes[i].w,sizes[i].h);v.font.size=32;v.stereotypeDisplay='label';v.showVisibility=true;v.suppressAttributes=!n.attrs.length;v.suppressOperations=!n.ops.length;v.fillColor=n.kind==='interface'?'#e6eef4':n.kind==='abstract'?'#eef1f5':spec.apply?'#eaf3ed':'#ffffff';nodes[n.name]=v;
  });
  spec.links.forEach((l,i)=>{const ge=graph.edges.find(e=>e.id==='e'+i);if(!ge)throw Error('Falta arista '+spec.name+i);const rev=['gen','real'].includes(l.kind);let points=ge._draw_.find(x=>x.op==='b').points.map(([x,y])=>[Math.round(x+50),Math.round(H-y+50)]);points=points.filter((p,j)=>!j||p[0]!==points[j-1][0]||p[1]!==points[j-1][1]);if(rev)points.reverse();
   let r,kind;if(['assoc','comp'].includes(l.kind)){kind='UMLAssociation';r=M(kind,l.label,model);r.end1.reference=nodes[l.a].model;r.end2.reference=nodes[l.b].model;r.end1.multiplicity=l.m1;r.end2.multiplicity=l.m2;r.end1.navigable='unspecified';r.end2.navigable='unspecified';if(l.kind==='comp')r.end1.aggregation='composite';}
   else{kind=l.kind==='gen'?'UMLGeneralization':l.kind==='real'?'UMLInterfaceRealization':'UMLDependency';r=rel(model,kind,nodes[l.a],nodes[l.b],l.label)}
   E(d,kind+'View',r,nodes[l.a],nodes[l.b],points);
  });
  const pdf=path.join(TMP,category,String(index).padStart(2,'0')+'_'+spec.slug+'.pdf');await rt.render(d,pdf);let arranged=rt.app.repository.get(d._id);b.separateLabels(arranged);await rt.render(arranged,pdf);arranged=rt.app.repository.get(d._id);model.ownedElements[model.ownedElements.indexOf(d)]=arranged;arranged._parent=model;
  manifest.push({category,index,name:spec.name,apply:spec.apply,id:d._id,pdf,png:path.join(dir,'Diagramas',String(index).padStart(2,'0')+'_'+spec.slug+'.png')});console.log(category,spec.name);
 }
 const dest=path.join(dir,`Patrones_${title}_SGCP.mdj`);const normalized=rt.app.repository.readObject(rt.app.repository.writeObject(project));fs.writeFileSync(dest,rt.app.repository.writeObject(normalized));
 // Reopen the deliverable itself for the definitive native exports.
 const read=rt.app.repository.readObject(fs.readFileSync(dest,'utf8'));
 for(const item of manifest.filter(x=>x.category===category))await rt.render(rt.app.repository.get(item.id),item.pdf);
}
measure.end();fs.writeFileSync(path.join(TMP,'manifest.json'),JSON.stringify(manifest,null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
