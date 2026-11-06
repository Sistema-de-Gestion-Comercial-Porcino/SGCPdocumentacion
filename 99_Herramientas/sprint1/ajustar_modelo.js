const fs=require('fs'),path=require('path'),rt=require('../staruml_runtime');
const base=path.resolve(__dirname,'../..'),root=path.join(base,'02_Ingenieria_de_Software');
(async()=>{
 const file=path.join(root,'01_Generales/Clases_SGCC.mdj');const project=rt.app.repository.readObject(fs.readFileSync(file,'utf8'));
 const all=rt.app.repository.getInstancesOf('UMLClass');const classes=Object.fromEntries(all.map(x=>[x.name,x]));
 const changes={Permiso:[['id','UUID']],Cotizacion:[['codigo','String'],['motivoRespuesta','String']],Pedido:[['codigo','String'],['motivoCancelacion','String']]};
 for(const [name,attrs]of Object.entries(changes))for(const[n,t]of attrs){const c=classes[name];if(!c.attributes.some(x=>x.name===n)){const a=new rt.T.UMLAttribute();a.name=n;a.type=t;a.visibility='private';a._parent=c;c.attributes.push(a);}}
 const diagram=rt.app.repository.getInstancesOf('UMLClassDiagram')[0],c=classes.Cotizacion;
 if(!rt.app.repository.getInstancesOf('UMLAssociation').some(x=>x.name==='versionAnterior')){
  const r=new rt.T.UMLAssociation();r.name='versionAnterior';r._parent=c._parent;c._parent.ownedElements.push(r);r.end1.reference=c;r.end1.multiplicity='0..1';r.end2.reference=c;r.end2.multiplicity='0..1';r.documentation='Una nueva versión enlaza su antecesora. Como máximo una sucesora directa; cada versión conserva código e historial. Una versión sustituida no habilita un pedido.';
  const v=diagram.ownedViews.find(x=>x.model===c),e=new rt.T.UMLAssociationView();e.model=r;e.tail=v;e.head=v;e._parent=diagram;e.lineStyle=rt.T.EdgeView.LS_RECTILINEAR;e.points.clear();[[v.left+v.width,v.top+65],[v.left+v.width+95,v.top+65],[v.left+v.width+95,v.top+v.height+45],[v.left+v.width-45,v.top+v.height+45],[v.left+v.width-45,v.top+v.height]].forEach(q=>e.points.add(new rt.T.Point(...q)));diagram.ownedViews.push(e);
 }
 c.documentation+=' Sprint 1: código legible único, respuesta conservada y versiones relacionadas. Precio del pedido procede del detalle aceptado; costo vigente se conserva al confirmar.';
 classes.Pedido.documentation+=' Sprint 1: código único y motivo de cancelación persistente. Confirmación no reserva, no cobra y no prepara.';
 const pdf=path.join(root,'PDFentrega/03_Revision/03_Clases/Clases_SGCC.pdf');await rt.render(diagram,pdf);
 fs.writeFileSync(file,rt.app.repository.writeObject(rt.app.repository.get(project._id)));fs.copyFileSync(file,path.join(root,'Entrega/Clases_SGCC.mdj'));
 console.log('Clases: atributos, versiones, MDJ y PDF individual actualizados.');
})().catch(e=>{console.error(e);process.exitCode=1});
