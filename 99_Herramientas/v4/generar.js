const b=require('./base'),g=require('./generales'),c=require('./colaboracion'),o=require('./objetos'),s=require('./estados');
(async()=>{
 await g.clases();await g.casosUso();await g.componentes();await g.despliegue();
 for(const x of c.casos)await c.build(x);
 for(const x of o.snapshots)await o.build(x);
 for(const x of s.specs)await s.build(x);
 b.fs.writeFileSync(b.path.join(b.PDF,'Manifiesto_V4.json'),JSON.stringify({fecha:'2026-10-25',total:b.manifest.length,archivos:b.manifest},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
