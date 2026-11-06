const b=require('./base'),{fs,path}=b;const rows=[];
function files(p){return fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(p,e.name)):[path.join(p,e.name)]);}
for(const file of [...files(b.OUT).filter(f=>f.endsWith('.mdj')),...files('/tmp/sgcc_reorganizacion_20261029/BPM').filter(f=>f.endsWith('.mdj'))]){
 const p=b.rt.app.repository.readObject(fs.readFileSync(file,'utf8')),ds=[];function walk(o){if(o instanceof b.T.Diagram)ds.push(o);for(const key of ['ownedElements','behaviors'])for(const x of o[key]||[])walk(x)}walk(p);
 const grouped=file.endsWith('_Completo.mdj'),expected=grouped?(file.includes('Estados_')?18:12):1;
 if(ds.length!==expected||ds.filter(d=>d.defaultDiagram).length!==1)throw Error('Diagramas/inicio incorrecto: '+file);
 if(grouped)for(const top of p.ownedElements)if(!top.ownedElements.some(x=>x instanceof b.T.Diagram))throw Error('Icono de diagrama no accesible: '+file);
 rows.push({archivo:path.relative('/tmp/sgcc_reorganizacion_20261029',file),diagramas:ds.length,cargaNativa:true});
}
if(rows.length!==79)throw Error('Archivos incorrectos: '+rows.length);
fs.writeFileSync('/tmp/sgcc_reorganizacion_20261029/Validacion_nativa.json',JSON.stringify(rows,null,2));console.log('Carga nativa: 74 individuales + 5 consolidados, acceso directo a cada diagrama.');
