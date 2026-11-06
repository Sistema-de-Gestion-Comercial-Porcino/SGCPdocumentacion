// Native UML export for the APA figure sheets; source MDJ is read-only.
const fs=require('fs'),path=require('path'),rt=require('../staruml_runtime');
const source=path.resolve(__dirname,'../../02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales/Patrones_Creacionales_SGCC.mdj');
const dest='/tmp/sgcc_patrones_apa7/figuras';fs.mkdirSync(dest,{recursive:true});
(async()=>{const p=rt.app.repository.readObject(fs.readFileSync(source,'utf8'));let i=0;
 for(const group of p.ownedElements)for(const d of group.ownedElements||[])if(d instanceof rt.T.UMLClassDiagram){
  // Titles, explanations and notes are provided as document text outside the APA figure.
  d.ownedViews=d.ownedViews.filter(v=>!(v instanceof rt.T.UMLTextView));
  await rt.render(d,path.join(dest,String(++i).padStart(2,'0')+'.pdf'));
 }
 if(i!==5)throw Error('Faltan figuras');console.log('Cinco figuras exportadas, sin modificar el MDJ.');
})().catch(e=>{console.error(e);process.exitCode=1});
