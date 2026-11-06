const b=require('./base'),{fs,path}=b;
function files(p){return fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(p,e.name)):[path.join(p,e.name)]);}
const rows=[];
for(const file of files(b.OUT).filter(f=>f.endsWith('.mdj'))){
 const p=b.rt.app.repository.readObject(fs.readFileSync(file,'utf8')),ds=[];
 function walk(o){if(o instanceof b.T.Diagram)ds.push(o);for(const key of ['ownedElements','behaviors'])for(const x of o[key]||[])walk(x);}
 walk(p);if(ds.length!==1||!ds[0].defaultDiagram)throw Error('Diagrama inicial inválido: '+file);
 rows.push({archivo:path.relative(b.ROOT,file),cargaNativa:true,tipo:ds[0].constructor.name,vistas:ds[0].ownedViews.length});
}
if(rows.length!==74)throw Error('Número de archivos incorrecto');
fs.writeFileSync(path.join(b.PDF,'Carga_nativa_V4.json'),JSON.stringify({total:rows.length,archivos:rows},null,2));console.log('Carga nativa correcta:',rows.length);
