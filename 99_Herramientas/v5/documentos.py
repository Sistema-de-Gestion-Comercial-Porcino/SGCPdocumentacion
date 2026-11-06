from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import json, hashlib, copy, re
BASE=Path(__file__).resolve().parents[2]
STAGE=Path('/tmp/sgcc_reorganizacion_20261029'); OUT=STAGE/'Documentos';OUT.mkdir(exist_ok=True)
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+NS['w']+'}'
name='ASA1 - Especificacion de Requerimientos - CRM Chancheria.docx'
with ZipFile(BASE/name)as z:parts={n:z.read(n)for n in z.namelist()}
x=E.fromstring(parts['word/document.xml']);b=x.find('w:body',NS);original=copy.deepcopy(b)
def txt(e):return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
def put(e,s):
 ts=e.findall('.//w:t',NS);assert ts
 ts[0].text=s;ts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
 for t in ts[1:]:t.text=''
def cell(t,row,col,s):put(b[t].findall('w:tr',NS)[row].findall('w:tc',NS)[col],s)
def rowid(t,id):return next(i for i,r in enumerate(b[t].findall('w:tr',NS))if txt(r.findall('w:tc',NS)[0])==id)
paragraphs={
15:'Fecha: 29 de octubre de 2026',41:'Versión 1.4',
49:'Documentar las necesidades del propietario de una chanchería de Santa Cruz de la Sierra con requerimientos verificables y trazables. Esta revisión conserva la estructura del ASA1 y alinea BPM, BPMN y UML en doce casos de uso generales. El equipo define una web responsiva y una app Android nativa en Kotlin; los parámetros comerciales no confirmados siguen sujetos a validación.',
54:'El SGCC gestiona carne de cerdo en cortes y derivados, y el servicio de faeneo/corte cuando se acuerda y presta. Primero se parametrizan usuarios, clientes, clasificaciones de cortes/derivados, productos, costos y transportes. Luego se gestionan cotizaciones, pedidos, producción, inventario, pagos y entregas; los reportes consultan esas operaciones según permisos. Una orden puede generar varios resultados: cada uno identifica lote, producto, tipo de corte o derivado, cantidad real y unidad. Almacén registra el pesaje y confirma después la entrada física. La cotización debe aceptarse antes del pedido. Un faltante exige fecha o solución acordada; previsión no es stock. Web online para gestión y comprador; Android Kotlin para reparto; servidor compartido. WhatsApp permanece atendido por una persona.',
126:'Los seis actores humanos son Propietario / administración, Ventas / cobranza, Producción, Almacén, Responsable de entrega y Comprador. Todos deben autenticarse; una persona puede ejercer varias responsabilidades. El comprador se registra con acceso limitado a sus datos; las cuentas internas las administra el propietario. Almacén captura los pesajes de producción manualmente. La balanza es una herramienta física y no un actor informático. El proveedor fiscal es una integración externa condicional. Gestión y portal usan web online; reparto utiliza Android Kotlin, con recepción offline limitada.',
138:'WhatsApp es un canal atendido por una persona. La emisión fiscal depende de la modalidad y del proveedor autorizado que se confirmen. El alcance actual no incluye integración automática con balanza: Almacén registra bruto, tara, neto, unidad, producto y lote. La aplicación de reparto comparte la API y los datos centrales con la web.',
146:'Actores humanos coherentes con el BPM propuesto y los doce casos de uso. Todos se autentican y operan según permisos; una persona puede asumir varias responsabilidades. El proveedor fiscal se identifica aparte como servicio externo condicional. La balanza no se integra al software en esta versión.',
163:'Se conservan 21 RF y 6 RNF, realizados por doce casos generales: CU01 Gestionar acceso (RF12); CU02 Administrar usuarios (RF13); CU03 Gestionar clientes (RF10); CU04 Gestión de costos (RF02/RF03); CU05 Gestión de cotizaciones (RF01/RF02); CU06 Gestionar pedidos (RF01/RF03/RF05/RF19); CU07 Gestionar productos (RF02/RF04); CU08 Gestionar producción (RF04/RF18/RF20); CU09 Gestionar inventario (RF04); CU10 Gestionar pagos y cobranza (RF05/RF06/RF11/RF19/RF20); CU11 Gestionar transporte y entregas (RF07/RF08/RF14/RF17 y RNF01); CU12 Gestionar reportes (RF15 y consultas autorizadas de los módulos). El CRUD es una alternativa interna de cada caso, no una cadena obligatoria ni un CU por requisito. Cortes y derivados se seleccionan del catálogo; cada resultado de producción se relaciona con lote, producto y clasificación. Almacén confirma pesajes manuales y entradas físicas separadas. RF09, RF16 y RF21 quedan diferidos; RF11 sigue condicionado a integración confirmada.',
172:'La entrevista identifica reposición como mejora futura, control de frío y control sanitario previo al faeneo. La reorganización académica agrupa las operaciones en doce casos de uso e incorpora catálogo explícito de cortes/derivados, resultados reales por orden, transportes y reportes autorizados. Son decisiones de diseño del equipo; no se atribuyen como nuevas respuestas de la entrevista.',
203:'Almacén registra manualmente bruto, tara, neto y unidad por producto/corte o derivado y lote. No se conecta automáticamente una balanza.',
206:'Administrar transporte propio o externo, vehículo, responsable y ruta de entregas; consultar reportes con filtros autorizados.',
226:'Propietario / administración, Ventas / cobranza, Producción, Almacén, Responsable de entrega y Comprador. Los permisos dependen de la responsabilidad; todas las cuentas requieren autenticación.',
273:'El SGCC integra parametrización, operaciones y reportes en doce casos de uso generales. El CRUD se detalla dentro de secuencias, actividades y colaboraciones. Clases, objetos y estados reflejan productos clasificados, resultados de producción, lotes, pesajes, stock y transporte. Se mantiene web responsiva online y Android Kotlin para reparto, con API y base central compartidas, sin modificar la estructura del ASA1.',
275:'Cada faeneo/desposte puede producir varios cortes y cada fabricación identifica el derivado obtenido. ResultadoProduccion se vincula a Lote, Producto y ClasificacionProducto; evita copiar un único tipo en toda la orden. Almacén confirma pesajes manuales y recibe físicamente; las previsiones no crean stock ni garantizan rendimientos. El catálogo y cantidades de los ejemplos son ilustrativos. Costos y precios los define el propietario; el margen es estimado. RF09/RF16/RF21 permanecen futuros y RF11 condicional. La evaluación sanitaria y el control de frío son registros humanos.'}
for i,s in paragraphs.items():put(b[i],s)
for col,s in enumerate(['29/10/2026','1.4','Reorganización en doce casos generales; seis actores humanos, catálogo de cortes/derivados, resultados por lote, pesaje manual, transportes y reportes. Se conservan estructura, 21 RF y 6 RNF.','Equipo ASA #1']):cell(42,3,col,s)
stake=[
['1','Propietario / administración','Administrar usuarios, catálogo, costos y permisos; consultar resultados.','Alta / alto','Crea cuentas internas y valida parámetros del negocio.','RF02/RF03/RF12/RF13/RF15'],
['2','Ventas / cobranza','Gestionar clientes, cotizaciones, pedidos, pagos y deuda.','Media / alto','Atención humana de WhatsApp; pago y entrega separados.','RF01/RF05/RF06/RF10/RF19/RF20'],
['3','Producción','Gestionar animales, sanidad, órdenes, cortes y derivados obtenidos.','Media / alto','Registra resultados identificados; no crea stock previsto.','RF04/RF18/RF20'],
['4','Almacén','Confirmar pesajes, recibir productos y gestionar existencias y reservas.','Media / alto','Captura manual: producto, lote, bruto, tara, neto y unidad.','RF04'],
['5','Responsable de entrega','Administrar transporte/ruta y registrar frío y recepción.','Media / alto','Android: recepción asignada/descargada; captura pendiente hasta envío validado.','RF07/RF08/RF14/RF17; RNF01'],
['6','Comprador','Cotizar, aceptar y consultar productos y operaciones propias.','Baja / alto','Cuenta de comprador; reportes limitados a sus datos.','RF01/RF10/RF12/RF14/RF15'],
['7','Proveedor fiscal externo','Emitir o consultar comprobantes según integración habilitada.','Media / medio','Servicio externo condicional; no es cuenta humana interna.','RF11']]
for i,row in enumerate(stake,1):
 for j,s in enumerate(row):cell(147,i,j,s)
rf={
'RF-04':('Gestionar catálogo, producción, inventario y pesajes','El propietario administrará clasificaciones de cortes y derivados y productos con código, presentación, unidad y estado. Crear producto no crea stock. Producción gestiona animales y órdenes con previsiones y tiempos; cada faeneo/desposte puede generar varios cortes y cada fabricación un derivado seleccionado del catálogo. Cada ResultadoProduccion identifica lote, producto, clasificación y cantidad real. Almacén registra bruto, tara, neto, unidad y responsable manualmente; valida el resultado sin aumentar stock. La entrada física posterior por lote/ubicación se aplica una sola vez. Consumos reales se descuentan aunque el resultado se rechace. Disponible es físico apto menos reservas; previsiones no se reservan. El faltante exige acuerdo, no rendimiento o plazo supuesto.','Catálogo y resultados explícitos; pesaje manual; cantidades ilustrativas no son rendimiento estándar.'),
'RF-08':('Gestionar transporte y rutas','El responsable administrará transporte propio o externo con código, transportista, contacto, vehículo y estado; podrá consultar, editar o desactivar sin borrar historial. Asignará transporte, responsable y entregas preparadas a una ruta. Android descarga asignaciones online. Finalizar ruta exige resultados centrales ENTREGADA, OBSERVADA o CANCELADA y ninguna captura por enviar; no cierra observaciones ni deuda.','CU11; transportes identificados; condiciones y capacidad por validar.'),
'RF-10':('Gestionar clientes','El sistema permitirá crear, buscar, consultar, editar y desactivar clientes con identificación, contacto, tipo y condición habitual de pago. Evitará duplicados y conservará operaciones. Desactivar exige revisar pedidos y deuda pendientes; no elimina historial. Cliente y usuario son distintos: una venta presencial no exige cuenta del cliente; el comprador con cuenta consulta solo sus datos.','CU03; datos y permisos diferenciados de las cuentas de acceso.'),
'RF-12':('Gestionar acceso autenticado','Todos los actores humanos deberán autenticarse online. El comprador podrá registrar su cuenta sin permisos internos; el personal recibe cuentas de administración. Se permitirá iniciar/cerrar sesión y recuperar acceso mediante verificación y token temporal de un solo uso. Credenciales protegidas y bloqueo configurable. Android exige login y descarga previos; sin señal no crea sesión. Reautenticar o cerrar sesión conserva capturas pendientes.','CU01; registro de comprador separado del alta de personal.'),
'RF-13':('Administrar usuarios y permisos','El propietario podrá crear, consultar, editar, habilitar/desactivar usuarios y asignar permisos. La desactivación revoca sesiones sin borrar historial y no debe dejar el sistema sin administrador activo. Una persona puede ejercer varias responsabilidades. El servidor valida permiso y alcance en cada operación y reporte.','CU02; seis actores humanos alineados con el BPM propuesto.'),
'RF-15':('Gestionar reportes e historial','Los seis perfiles podrán consultar y exportar PDF o Excel de reportes permitidos de clientes, cotizaciones, pedidos, producción por producto/corte/derivado, inventario, pagos y entregas. Filtrarán fechas, producto, cliente y estado cuando corresponda. Comprador solo sus operaciones; costos y resultados globales requieren permiso. La exportación revalida el mismo alcance. Una consulta no modifica stock, pedidos ni pagos.','CU12; consulta online, reportes restringidos por perfil y propiedad de datos.')}
for id,(title,desc,status)in rf.items():
 i=rowid(164,id);cell(164,i,1,title);cell(164,i,2,desc);cell(164,i,5,status)
 # Keep the two existing matrices aligned without adding rows.
 cell(222,rowid(222,id),2,title)
criteria={
'RF-04':'Crear costilla y lomo como cortes y jamón elaborado como derivado. Una orden obtiene costilla y lomo en lotes separados con pesajes propios; otra fabrica jamón. Confirmar resultado no suma stock; recepción física única sí. Una referencia repetida no duplica entrada ni consumo.',
'RF-08':'Transporte identificado se asigna a ruta con responsable. Desactivar conserva historial. Descarga previa online; cierre sin capturas pendientes y sin saldar deuda por sí mismo.',
'RF-10':'Crear, buscar, editar y desactivar conservando historial. Pedidos o deuda pendiente impiden desactivación sin resolución. Cliente presencial no requiere cuenta.',
'RF-12':'Todos se autentican. Registro público solo comprador; recuperación verifica token vigente de un uso. Login/cierre/renovación conservan capturas Android.',
'RF-13':'Administrar usuarios con permisos auditados. Desactivar revoca sesiones, conserva historial y mantiene al menos un administrador habilitado.',
'RF-15':'Filtros por fecha, producto/corte/derivado y estado muestran datos autorizados. Comprador no consulta ni exporta datos ajenos. Exportar no modifica operaciones.'}
for id,s in criteria.items():
 cell(222,rowid(222,id),5,s);cell(270,rowid(270,id),3,s)
cell(270,rowid(270,'RF-04'),5,'Inspeccionar catálogo, dos resultados de una misma orden, lotes y pesajes; comprobar entrada física y consumo únicos, reserva y bloqueo sanitario.')
cell(270,rowid(270,'RF-15'),5,'Comparar consulta y exportación con los mismos permisos; comprobar restricción del comprador a sus datos.')
cell(160,8,1,'Identificar cortes y derivados del catálogo, resultados por orden/lote, pesajes manuales y recepción física. Control sanitario humano previo; rechazo bloquea. Previsiones no crean stock. (Producción/Almacén)')
# Replace only references to superseded model numbering in narrative; interview contents stay intact.
for e in b:
 for t in e.findall('.//w:t',NS):
  if t.text:t.text=t.text.replace('UML V4','UML reorganizados').replace('modelo V4','modelo vigente').replace('flujo V4','flujo vigente').replace('con V4','con el modelo vigente').replace('CU21/CU26','CU11/CU12').replace('CU21','CU11').replace('Versión actual: CU26','Versión actual: CU12')
assert len(b)==len(original)==278
assert [len(t.findall('w:tr',NS))for t in b.findall('w:tbl',NS)]==[len(t.findall('w:tr',NS))for t in original.findall('w:tbl',NS)]
assert [[len(r.findall('w:tc',NS))for r in t.findall('w:tr',NS)]for t in b.findall('w:tbl',NS)]==[[len(r.findall('w:tc',NS))for r in t.findall('w:tr',NS)]for t in original.findall('w:tbl',NS)]
parts['word/document.xml']=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(OUT/name,'w',ZIP_DEFLATED)as z:
 for k,v in parts.items():z.writestr(k,v)
(STAGE/'Requisitos_actualizados.json').write_text(json.dumps({'rf':rf,'criterios':criteria},ensure_ascii=False,indent=2))
print('ASA actualizado: 278 elementos, 12 tablas; estructura y dimensiones conservadas.')
