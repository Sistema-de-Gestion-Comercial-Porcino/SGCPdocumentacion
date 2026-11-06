const b=require('./base'),{M,D,V,E,text,project,rel,assoc,contain,save}=b;
const {defs,domain}=require('./dominio'),{router}=require('./rutas');
const {casos}=require('../especificacion_v3');
async function clases(){
 const {p,m}=project('SGCC — Clases V4'),d=D(m,'UMLClassDiagram','Clases generales del SGCC'),{cs,rels}=domain(m),vs={};
 text(d,'SGCC · Modelo de clases',100,20,2200,45,26);
 for(const[n,[col,row,attrs,ops=[]]]of Object.entries(defs)){
  const h=55+attrs.length*19+ops.length*19;const v=V(d,'UMLClassView',cs[n],100+col*570,140+row*390,390,h);v.suppressOperations=!ops.length;v.showVisibility=true;v.font.size=14;vs[n]=v;
  if(['Pedido','Cotizacion','OrdenProduccion','Pago','Entrega'].includes(n))v.fillColor='#edf3f8';
 }
 const route=router(Object.values(vs));
 for(const r of rels){const gen=r.constructor.name==='UMLGeneralization',a=vs[gen?r.source.name:r.end1.reference.name],c=vs[gen?r.target.name:r.end2.reference.name];E(d,gen?'UMLGeneralizationView':'UMLAssociationView',r,a,c,route(a,c));}
 text(d,'Composición: detalle exclusivo de su documento. Agregación: una ruta agrupa entregas que existen por separado.\nFaeneoDesposte y FabricacionDerivado especializan OrdenProduccion. Los roles se asignan al usuario.\nLa cotización presentada exige al menos un detalle; el borrador puede estar vacío. Pedido requiere aceptación vigente.\nSaldo = cargos - aplicaciones de pagos válidos. Entrega y deuda se controlan por separado.\nOperacionPendiente: solo recepción Android de entrega asignada; no cambia entrega central hasta sincronización válida.\nUna orden puede atender varios detalles o reponer stock. PrevisionProducto no es existencia.\nCada producto obtenido se registra como lote con cantidad real; Almacén confirma su entrada.\nCostos de referencia y margen estimado se conservan por pedido; sin reparto automático de costos por corte.\nAlertaCliente y esHabitual pertenecen a RF09 FUTURO. Las restricciones están en el diccionario V4.',100,2920,3000,250,16);
 m.documentation='Modelo de dominio único. Cada clase se dibuja una sola vez. Las clases de interfaz/control de los diagramas de colaboración pertenecen al diseño, no son tablas del dominio. La composición indica propiedad exclusiva, no ordena borrar físicamente registros comerciales. Ruta agrupa entregas que pueden reasignarse. OrdenProduccion es abstracta y tiene especializaciones completas y excluyentes. Un animal no pasa por dos órdenes de faeneo. Una orden puede reabastecer stock sin detalle de pedido. Las cantidades y precios conservan unidades; saldo y stock disponible se calculan. Una lectura de frío identifica lote, entrega o ubicación. Un pesaje se vincula a producción o entrega. Las reglas completas están en Diccionario_V4.md.';
 await save(p,d,'01_Generales/Clases_SGCC_V4.mdj');
}
async function casosUso(){
 const {p,m}=project('SGCC — Casos de uso V4'),d=D(m,'UMLUseCaseDiagram','Casos de uso generales');
 text(d,'SGCC · Casos de uso',420,20,1800,50,26);
 const sub=M('UMLSubsystem','Sistema de Gestión Comercial y Clientes',m),box=V(d,'UMLUseCaseSubjectView',sub,370,210,2260,2400);
 const actors={},vs={};
 const aa=[['Usuario',1450,65],['Ventas / cobranza',80,1230],['Propietario',1450,2670],['Comprador',2210,2670],['Producción',2780,610],['Almacén',2780,1300],['Responsable de entrega',2780,2090],['Balanza',2780,300],['Proveedor fiscal',80,2460]];
 for(const[n,x,y]of aa)actors[n]=V(d,'UMLActorView',M('UMLActor',n,m),x,y,180,115);
 const pos={CU01:[1330,320],CU02:[1240,620],CU04:[1240,850],CU24:[1240,1830],CU25:[1240,2070],CU26:[1240,2320]};
 ['CU03','CU05','CU06','CU13','CU14','CU15','CU16','CU17','CU18','CU19','CU23'].forEach((id,i)=>pos[id]=[470,350+i*198]);
 ['CU08','CU09','CU10','CU11','CU07','CU12','CU20','CU21','CU22'].forEach((id,i)=>pos[id]=[1990,400+i*240]);
 for(const c of casos){const u=M('UMLUseCase',c.id+' · '+c.nombre,m);if(c.alcance==='FUTURO')u.stereotype='futuro';u.documentation='Actor: '+c.actor+'\nPrecondición: '+c.pre+'\nResultado: '+c.post+'\nAlternativa: '+c.alternativa+'\nFuente: '+c.fuente;vs[c.id]=V(d,'UMLUseCaseView',u,...pos[c.id],510,110);contain(box,vs[c.id]);if(c.alcance==='FUTURO'){vs[c.id].fillColor='#eeeeee';vs[c.id].lineColor='#888888';}}
 text(d,'Acceso y gestión',1250,540,530,40,17);text(d,'Portal del comprador',1250,1740,530,40,17);
 const route=router([...Object.values(vs),...Object.values(actors)]);
 for(const c of casos.filter(c=>c.alcance!=='FUTURO'))assoc(m,d,actors[c.actor],vs[c.id],'','','',route(actors[c.actor],vs[c.id]));
 for(const[a,id]of [['Balanza','CU10'],['Proveedor fiscal','CU19']])assoc(m,d,actors[a],vs[id],'','','',route(actors[a],vs[id]));
 m.documentation='Los 26 casos conservan sus identificadores para relacionarlos con secuencias y actividades existentes. Usuario representa a cualquier persona con acceso autenticado; cada actor de negocio representa una responsabilidad y una persona puede ejercer varias. La autenticación y los permisos son precondiciones, no una ejecución incluida en cada acción. La aprobación de cotización precede a confirmar pedido; no es una relación include entre objetivos. El comprador del portal es una ampliación de la propuesta del BPM frente al funcionamiento actual de la entrevista. WhatsApp es un canal atendido por ventas, sin un bot supuesto.';
 text(d,'Canales: web responsiva online para gestión y portal. Android Kotlin para reparto.\nCU21 permite captura local de recepción descargada y autorizada; CU01, CU20 y CU22 requieren conexión.\nLos demás casos operan con conexión. CU23/RF09 está FUTURO, sin participación activa en esta entrega.\nRF11/CU19 requiere modalidad y proveedor fiscal confirmados. RF16 y RF21 también quedan fuera del alcance actual.',430,2900,2250,210,18);
 await save(p,d,'01_Generales/Casos_de_Uso_SGCC_V4.mdj');
}
const {componentes,despliegue}=require('./arquitectura_web_android');
module.exports={clases,casosUso,componentes,despliegue};
