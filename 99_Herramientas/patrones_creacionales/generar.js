const fs=require('fs'),path=require('path');
const b=require('../v5/base'),{M,D,V,text,rel,contain}=b,rt=b.rt,T=b.T;
function E(...args){const e=b.E(...args);e.font.size=22;for(const v of e.subViews||[])if(v.font)v.font.size=22;return e;}
const OUT=path.resolve(__dirname,'../../02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales');
const TEMP='/tmp/sgcc_patrones_20261103';fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(TEMP+'/pdf',{recursive:true});
const p=M('Project','SGCC · Patrones creacionales'),groups=[M('UMLModel','01 · Aplicados al CRM',p),M('UMLModel','02 · Ejemplos externos',p)],diagrams=[];
function diagram(group,name,subtitle){const d=D(groups[group],'UMLClassDiagram',name);d.defaultDiagram=diagrams.length===0;diagrams.push(d);text(d,name,60,20,1850,60,38);text(d,subtitle,60,90,1850,65,25);return d}
function cl(d,n,x,y,w,attrs=[],ops=[],opts={}){const m=M(opts.iface?'UMLInterface':'UMLClass',n,d._parent);m.documentation=opts.doc||'';m.isAbstract=!!opts.abstract;
 for(const a of attrs){const [s,type]=a.split(':');const n=s.replace(/^[+\-#]/,'');const at=M('UMLAttribute',n,m,'attributes');at.visibility=s.startsWith('+')?'public':'private';at.type=type||'String';if(n==='instancia')at.isStatic=true;if(opts.readonly)at.isReadOnly=true;}
 for(const desc of ops){const spec=typeof desc==='string'?{name:desc}:desc;const sig=spec.name.match(/^([^()]+)\(([^)]*)\)(?::\s*(.+))?$/);const o=M('UMLOperation',sig?sig[1]:spec.name,m,'operations');if(sig){const types={datos:n==='PedidoBuilder'?'DatosDetalle':'DatosReporte',cotizacionId:'UUID',aceptada:'Cotizacion',fecha:'DateTime',condicion:'FormaPago',documento:'Documento'};for(const arg of sig[2].split(',').filter(Boolean)){const [an,at]=arg.trim().split(':');const par=M('UMLParameter',an,o,'parameters');par.type=at?.trim()||types[an]||'Object';par.direction='in';}if(sig[3]){const par=M('UMLParameter','',o,'parameters');par.type=sig[3];par.direction='return';}}o.visibility=spec.visibility||'public';o.isAbstract=!!spec.abstract;o.isStatic=!!spec.static;if(spec.doc)o.documentation=spec.doc;}
 const v=V(d,opts.iface?'UMLInterfaceView':'UMLClassView',m,x,y,w,110+attrs.length*35+ops.length*40);v.font.size=27;v.showVisibility=true;v.suppressAttributes=!attrs.length;v.suppressOperations=!ops.length;v.fillColor=opts.iface?'#e7f0f5':opts.abstract?'#e9eef7':opts.product?'#e6f1e9':'#ffffff';v.stereotypeDisplay='label';return v}
function edge(d,a,z,kind,ps,label=''){const m=rel(d._parent,kind,a,z,label);return E(d,kind+'View',m,a,z,ps)}
function dep(d,a,z,ps,label=''){return edge(d,a,z,'UMLDependency',ps,label)}
function gen(d,a,z,ps){return edge(d,a,z,'UMLGeneralization',ps)}
function real(d,a,z,ps){return edge(d,a,z,'UMLInterfaceRealization',ps)}
function note(d,str,y=1100){text(d,str,60,y,1880,150,25)}
// 1: genuine overridable factory method; products vary by export format.
{
const d=diagram(0,'01 · Factory Method · Exportar reportes','APLICADO AL CRM · CU12 / RF15 · Un formato, un creador y un exportador concreto.');
const c=cl(d,'ExportacionReporte',180,240,650,[],['exportar(datos): Archivo',{name:'crearExportador(): ExportadorReporte',visibility:'protected',abstract:true}],{abstract:true,doc:'exportar llama crearExportador y luego generar(datos). Recibe datos ya autorizados; no consulta ni cambia el alcance del usuario.'});
const i=cl(d,'ExportadorReporte',1180,240,650,[],['generar(datos): Archivo'],{iface:true});
const cp=cl(d,'ExportacionPDF',180,600,650,[],[{name:'crearExportador(): ExportadorReporte',visibility:'protected'}]);
const ep=cl(d,'ExportadorPDF',1180,600,650,[],['generar(datos): Archivo'],{product:true});
const ce=cl(d,'ExportacionExcel',180,930,650,[],[{name:'crearExportador(): ExportadorReporte',visibility:'protected'}]);
const ee=cl(d,'ExportadorExcel',1180,930,650,[],['generar(datos): Archivo'],{product:true});
dep(d,c,i,[[830,310],[1180,310]],'usa');
gen(d,cp,c,[[340,600],[340,440]]);gen(d,ce,c,[[180,1000],[80,1000],[80,400],[180,400]]);
real(d,ep,i,[[1350,600],[1350,420]]);real(d,ee,i,[[1830,1000],[1940,1000],[1940,380],[1830,380]]);
dep(d,cp,ep,[[830,680],[1180,680]],'«create»');dep(d,ce,ee,[[830,1010],[1180,1010]],'«create»');
note(d,'El servicio de CU12 verifica usuario, filtros y alcance antes de entregar los datos al creador.\ncrearExportador() se redefine en las subclases; exportar() conserva el flujo común.\nArchivo y datos representan valores de transferencia; no son entidades comerciales nuevas.',1180);
}
// 2: fluent builder. The service is director; one builder per confirmation attempt.
{
const d=diagram(0,'02 · Builder · Construir un pedido','APLICADO AL CRM · CU06 / RF01 y RF03 · Construcción gradual; validación antes de guardar.');
const service=cl(d,'ServicioConfirmarPedido',60,240,650,[],['confirmar(cotizacionId): Pedido'],{doc:'Director de la construcción. Autoriza, verifica aceptación/vigencia y versión, toma costo de referencia al confirmar, recorre detalles, usa el builder y persiste una sola vez en transacción.'});
const build=cl(d,'PedidoBuilder',1000,220,850,['-cotizacionAceptada: Cotizacion','-detalles: Lista<DetallePedido>','-fechaComprometida: DateTime','-condicionPago: FormaPago'],['desdeCotizacion(aceptada): PedidoBuilder','agregarDetalle(datos): PedidoBuilder','conFecha(fecha): PedidoBuilder','conPago(condicion): PedidoBuilder','build(): Pedido'],{doc:'Variante fluida de Builder, no necesita interfaz ni dos builders concretos. build valida campos, cantidades, unidades y al menos un detalle, entrega copia independiente; no guarda ni cobra ni reserva.'});
const quote=cl(d,'Cotizacion',60,500,650,['-id: UUID','-version: Integer','-vigenteHasta: DateTime','-estado: EstadoCotizacion'],[],{product:true});
const order=cl(d,'Pedido',1000,860,650,['-id: UUID','-fechaComprometida: DateTime','-estadoComercial: EstadoComercial','-estadoPreparacion: EstadoPreparacion','-condicionPago: FormaPago'],[],{product:true});
const detail=cl(d,'DetallePedido',60,870,650,['-producto: Producto','-cantidadSolicitada: Decimal','-unidad: String','-precioAcordado: Decimal','-costoReferenciaAcordado: Decimal'],[],{product:true});
dep(d,service,build,[[710,315],[1000,315]],'dirige');dep(d,service,quote,[[300,410],[300,500]],'verifica');dep(d,build,order,[[1360,740],[1360,860]],'«create»');dep(d,build,detail,[[1000,620],[820,620],[820,920],[710,920]],'arma detalles');
const r=M('UMLAssociation','contiene',d._parent);r.end1.reference=order.model;r.end2.reference=detail.model;r.end1.multiplicity='1';r.end2.multiplicity='1..*';r.end1.aggregation='composite';r.end1.navigable='unspecified';r.end2.navigable='unspecified';E(d,'UMLAssociationView',r,order,detail,[[1000,1070],[710,1070]]);
note(d,'Vista parcial del dominio vigente: no sustituye el diagrama general de clases.\nCada detalle referencia un Producto y conserva unidad, precio aceptado y costo al confirmar.\nRechazo/vencimiento: sin pedido. El builder no registra pagos, stock ni entregas.',1230);
}
// 3: compatible product families, external theme editor.
{
const d=diagram(1,'03 · Abstract Factory · Editor con temas','EJEMPLO EXTERNO · Familia clara u oscura: botón y campo del mismo tema.');
const f=cl(d,'FabricaTema',60,240,600,[],['crearBoton(): Boton','crearCampo(): CampoTexto'],{iface:true});
const light=cl(d,'FabricaClara',60,620,600,[],['crearBoton(): Boton','crearCampo(): CampoTexto']);
const dark=cl(d,'FabricaOscura',60,1020,600,[],['crearBoton(): Boton','crearCampo(): CampoTexto']);
const bi=cl(d,'Boton',930,240,430,[],['dibujar(): void'],{iface:true});
const ti=cl(d,'CampoTexto',1510,240,430,[],['dibujar(): void'],{iface:true});
const bc=cl(d,'BotonClaro',930,620,430,[],['dibujar(): void'],{product:true});const tc=cl(d,'CampoClaro',1510,620,430,[],['dibujar(): void'],{product:true});
const bo=cl(d,'BotonOscuro',930,1020,430,[],['dibujar(): void'],{product:true});const to=cl(d,'CampoOscuro',1510,1020,430,[],['dibujar(): void'],{product:true});
real(d,light,f,[[240,620],[240,450]]);real(d,dark,f,[[60,1110],[20,1110],[20,420],[60,420]]);
real(d,bc,bi,[[1100,620],[1100,410]]);real(d,bo,bi,[[1360,1100],[1420,1100],[1420,370],[1360,370]]);
real(d,tc,ti,[[1690,620],[1690,410]]);real(d,to,ti,[[1940,1100],[2000,1100],[2000,370],[1940,370]]);
dep(d,light,bc,[[660,700],[930,700]],'«create»');dep(d,light,tc,[[520,830],[520,890],[1690,890],[1690,790]],'«create»');
dep(d,dark,bo,[[660,1100],[930,1100]],'«create»');dep(d,dark,to,[[520,1230],[520,1290],[1690,1290],[1690,1190]],'«create»');
note(d,'El editor recibe una FabricaTema y solicita ambos controles a esa misma fábrica.\nCambiar de tema exige reemplazar la familia completa. Web y Android del CRM son clientes distintos;\nsu existencia por sí sola no justifica una Abstract Factory compartida.',1370);
}
// 4: clone independent mutable configuration in an external slide editor.
{
const d=diagram(1,'04 · Prototype · Duplicar una tarjeta','EJEMPLO EXTERNO · Editor de presentaciones: copiar una tarjeta conservando su diseño.');
const client=cl(d,'EditorPresentaciones',70,250,700,[],['duplicar(p: Prototipo): Prototipo']);
const pi=cl(d,'Prototipo',1120,250,700,[],['clonar(): Prototipo'],{iface:true});
const card=cl(d,'Tarjeta',1120,680,700,['-id: UUID','-titulo: String','-contenido: String'],['clonar(): Tarjeta'],{product:true,doc:'Genera identidad nueva y copia profunda de EstiloTarjeta. La copia puede editarse sin modificar la tarjeta original.'});
const style=cl(d,'EstiloTarjeta',70,700,700,['-color: String','-tipografia: String','-margen: Integer'],['copiar(): EstiloTarjeta']);
dep(d,client,pi,[[770,320],[1120,320]],'solicita copia');real(d,card,pi,[[1460,680],[1460,420]]);
const a=M('UMLAssociation','estilo propio',d._parent);a.end1.reference=card.model;a.end2.reference=style.model;a.end1.aggregation='composite';a.end1.multiplicity='1';a.end2.multiplicity='1';a.end1.navigable='unspecified';a.end2.navigable='unspecified';E(d,'UMLAssociationView',a,card,style,[[1120,810],[770,810]]);
note(d,'La copia obtiene otro id y otro EstiloTarjeta; editar su color no modifica el original.\nEn el CRM, copiar un pedido arriesga arrastrar precios, estados, reservas o pagos.\nLa nueva confirmación se construye desde una cotización aceptada y vigente.',1110);
}
// 5: local read-only configuration; private constructor and static accessor.
{
const d=diagram(1,'05 · Singleton · Configuración de un visor','EJEMPLO EXTERNO · Visor de documentos en un solo proceso; configuración inmutable.');
const viewer=cl(d,'VisorDocumentos',100,290,650,[],['abrir(documento): void']);
const singleton=cl(d,'ConfiguracionVisor',1080,240,820,['-instancia: ConfiguracionVisor','-idioma: String','-tema: String','-zoomInicial: Decimal'],[{name:'ConfiguracionVisor()',visibility:'private'},{name:'obtenerInstancia(): ConfiguracionVisor',static:true},'leerIdioma(): String','leerTema(): String','leerZoom(): Decimal'],{readonly:true,doc:'Una instancia por proceso. Inicialización segura ante concurrencia; propiedades de configuración sin mutación pública. En Kotlin puede representarse mediante object.'});
dep(d,viewer,singleton,[[750,370],[1080,370]],'accede');
text(d,'Primera llamada: crea la instancia\nSiguientes llamadas: devuelven la misma referencia',100,650,780,160,30);
note(d,'Miembros subrayados: estáticos. Constructor privado. Inicialización segura ante varios hilos.\nUna instancia local no coordina varios servidores, teléfonos o procesos.\nPara el CRM se prefiere administrar dependencias y su duración; no guardar usuario, pedido ni saldo global.',1050);
}
(async()=>{
 for(let i=0;i<diagrams.length;i++){const d=diagrams[i];await rt.render(d,TEMP+'/pdf/'+String(i+1).padStart(2,'0')+'.pdf');const current=rt.app.repository.get(d._id);b.separateLabels(current);await rt.render(current,TEMP+'/pdf/'+String(i+1).padStart(2,'0')+'.pdf');const arranged=rt.app.repository.get(d._id); // retain arranged views in the source tree for the unified project
 const parent=d._parent;parent.ownedElements[parent.ownedElements.indexOf(d)]=arranged;arranged._parent=parent;console.log(d.name);
 }
 // Re-load once to normalize model/view references across all diagrams.
 const normalized=rt.app.repository.readObject(rt.app.repository.writeObject(p));
 const dest=path.join(OUT,'Patrones_Creacionales_SGCC.mdj');fs.writeFileSync(dest,rt.app.repository.writeObject(normalized));
 fs.writeFileSync(TEMP+'/diagramas.json',JSON.stringify(diagrams.map((d,i)=>({n:i+1,name:d.name,id:d._id,pdf:String(i+1).padStart(2,'0')+'.pdf'})),null,2));console.log(dest);
})().catch(e=>{console.error(e);process.exitCode=1});
