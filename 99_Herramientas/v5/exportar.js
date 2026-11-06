// Exportación directa de los MDJ vigentes; no regenera ni modifica sus modelos.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),rt=require('../staruml_runtime');
const ROOT=path.resolve(__dirname,'../..'),SOURCE='/tmp/sgcc_reorganizacion_20261029/Software';
const OUT=process.env.SGCC_ENTREGA_STAGE||path.join(SOURCE,'PDFentrega');
const Doc=rt.req('node_modules/pdfkit'),Canvas=rt.req('src/engine/pdf-graphics').PDFCanvas;
const groups=[
 ['01_Casos_de_Uso','Casos de uso','01_Generales',/^Casos_de_Uso.*\.mdj$/],
 ['02_Secuencias','Secuencias','06_Secuencias',/^CU\d+_Secuencia\.mdj$/],
 ['03_Clases','Clases','01_Generales',/^Clases.*\.mdj$/],
 ['04_Actividades','Actividades','05_Actividades',/^CU\d+_Actividad\.mdj$/],
 ['05_Estados','Estados','04_Estados',/^\d+.*_Estados\.mdj$/],
 ['06_Colaboracion','Colaboración','02_Colaboracion',/^CU\d+_Colaboracion\.mdj$/],
 ['07_Componentes','Componentes','01_Generales',/^Componentes.*\.mdj$/],
 ['08_Despliegue','Despliegue','01_Generales',/^Despliegue.*\.mdj$/],
 ['09_Objetos','Objetos','03_Objetos',/^CU\d+_Objetos\.mdj$/],
 ['10_BPMN_Horizontal','BPMN horizontal','BPMN_Horizontal',/^BPMN_.*\.mdj$/]
];
function walk(x,out=[]){if(x&&typeof x==='object'){if(x._id)out.push(x);for(const v of Object.values(x))if(v&&typeof v==='object')walk(v,out)}return out}
async function finish(pdf,out){pdf.end();await new Promise((resolve,reject)=>{out.on('finish',resolve);out.on('error',reject)});}
(async()=>{
 fs.mkdirSync(OUT,{recursive:true});const finalPath=path.join(OUT,'Diagramas_SGCC_Completo.pdf');
 const combined=new Doc({autoFirstPage:false,margin:0,compress:true,info:{Title:'SGCC — Todos los diagramas',Author:'Equipo SGCC',Subject:'Casos de uso, secuencias, clases, actividades, estados, colaboración, componentes, despliegue, objetos y BPMN'}});
 const finalOut=fs.createWriteStream(finalPath);combined.pipe(finalOut);const rows=[];let page=0;
 for(const [folder,title,src,filter]of groups){
  const files=fs.readdirSync(path.join(SOURCE,src)).filter(n=>filter.test(n)).sort();let bookmark;
  for(const name of files){
   const file=path.join(SOURCE,src,name),raw=fs.readFileSync(file),obs=walk(JSON.parse(raw)),ds=obs.filter(o=>o._type.endsWith('Diagram'));if(ds.length!==1)throw Error(file+': número de diagramas no esperado');
   rt.app.repository.readObject(raw.toString());const d=rt.app.repository.get(ds[0]._id);
   const scratch=new Doc({size:[100,100],margin:0}),canvas=new Canvas(scratch);for(let i=0;i<3;i++)d.arrangeDiagram(canvas);
   const box=d.getBoundingBox(canvas),width=Math.ceil(box.x2+35),height=Math.ceil(box.y2+35),scale=Math.min(1,14000/width,14000/height),pw=Math.ceil(width*scale),ph=Math.ceil(height*scale);scratch.end();
   const relative=path.join('03_Revision',folder,name.replace('.mdj','.pdf')),dest=path.join(OUT,relative);fs.mkdirSync(path.dirname(dest),{recursive:true});
   const pdf=new Doc({size:[pw,ph],margin:0,compress:true,info:{Title:d.name,Author:'Equipo SGCC'}}),out=fs.createWriteStream(dest);pdf.pipe(out);pdf.scale(scale);d.drawDiagram(new Canvas(pdf),false);await finish(pdf,out);
   combined.addPage({size:[pw,ph],margin:0});if(!bookmark)bookmark=combined.outline.addItem(title,{expanded:false});bookmark.addItem(d.name||name);combined.save();combined.scale(scale);d.drawDiagram(new Canvas(combined),false);combined.restore();page++;
   if(!raw.equals(fs.readFileSync(file)))throw Error('MDJ modificado durante exportación: '+file);
   rows.push({pagina:page,categoria:title,mdj:path.relative(ROOT,file),pdf:relative,tipo:ds[0]._type,ancho:pw,alto:ph,escala:scale,sha256MDJ:crypto.createHash('sha256').update(raw).digest('hex')});
  }
  console.log(title+': '+files.length+' diagramas');
 }
 if(page!==72)throw Error('Cantidad inesperada: '+page);await finish(combined,finalOut);
 const manifest=process.env.SGCC_ENTREGA_MANIFEST||path.join(ROOT,'02_Ingenieria_de_Software/00_Documentacion/Exportacion_final.json');fs.writeFileSync(manifest,JSON.stringify({paginas:page,orden:groups.map(g=>g[1]),archivos:rows},null,2));
 console.log('PDF final: '+page+' páginas con marcadores. Fuentes MDJ intactas.');
})().catch(e=>{console.error(e);process.exitCode=1});
