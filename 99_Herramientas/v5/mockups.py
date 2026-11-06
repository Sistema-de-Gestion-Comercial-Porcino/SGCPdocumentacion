from pathlib import Path
BASE=Path(__file__).resolve().parents[2];STAGE=Path('/tmp/sgcc_reorganizacion_20261029')
source=(BASE/'99_Herramientas/balsamiq/generar_mockups.py').read_text();prefix,footer=source.split('# Validación de navegación, dimensiones y cobertura antes de escribir la base.',1)
prefix=prefix.replace("ROOT=Path(__file__).resolve().parents[2]","ROOT=Path('/tmp/sgcc_reorganizacion_20261029')")
prefix=prefix.replace("nav=[('Inicio','w02'),('Clientes','w03'),('Usuarios y roles','w04'),('Cotizaciones','w06'),('Pedidos','w09'),('Productos / precios','w05'),('Inventario','w10'),('Producción','w12'),('Cobranza','w17'),('Entregas / rutas','w20'),('Control de frío','w22')]","nav=[('Inicio','w02'),('Usuarios','w04'),('Clientes','w03'),('Productos','wcat'),('Gestión de costos','w05'),('Cotizaciones','w06'),('Pedidos','w09'),('Producción','w12'),('Inventario','w10'),('Cobranza','w17'),('Transporte / entregas','wtrans'),('Reportes','wreport')]")
prefix=prefix.replace("s.web('Usuarios y roles')","s.web('Usuarios')").replace("s.web('Productos / precios')","s.web('Gestión de costos')").replace("s.web('Entregas / rutas')","s.web('Transporte / entregas')").replace("s.web('Control de frío')","s.web('Transporte / entregas')")
exec(compile(prefix,'mockups_base','exec'),globals())
oldmap={1:1,2:2,3:3,4:4,5:5,6:6,7:9,8:8,9:8,10:8,11:8,12:9,13:6,14:10,15:10,16:10,17:10,18:10,19:10,20:11,21:11,22:11,24:7,25:5,26:12}
SCREENS[:]=[s for s in SCREENS if s.key!='w23']
for s in SCREENS:
 s.cu=sorted(set('CU%02d'%oldmap[int(c[2:])]for c in s.cu if int(c[2:]) in oldmap))
 for c in s.cs:
  t=c['properties']['text'];t=t.replace('Carne de cerdo / corte','Costilla de cerdo').replace('Carne de cerdo · cortes','Costilla de cerdo').replace('Carne de cerdo · corte por kg','Costilla de cerdo · kg').replace('Carne de cerdo','Costilla de cerdo').replace('CAR-2510','COS-2510').replace('carne · APTO','costilla · APTO').replace('Origen del pesaje','Captura del peso').replace('Balanza','Manual · Almacén')
  c['properties']['text']=t

def get(k):return next(s for s in SCREENS if s.key==k)
def replace(k,title,cu,active):
 old=get(k);i=SCREENS.index(old);SCREENS.remove(old);s=Screen(k,title,cu=cu);SCREENS.pop();SCREENS.insert(i,s);s.web(active);return s
s=get('w01');s.link(760,580,510,'Crear cuenta de comprador','preg');s.link(760,630,510,'Recuperar acceso','pforgot')
for c in s.cs:
 if c['properties']['text']=='Entrar al portal comprador':c['properties']['text']='Ingresar como comprador'
s=get('w03');s.btn(280,825,255,'Nuevo cliente','wclient');s.btn(558,825,255,'Desactivar cliente','wclientblock')
s=get('w04');s.btn(280,825,240,'Crear usuario','wuser');s.btn(550,825,240,'Desactivar cuenta','wuseroff')
s=get('w05');s.title='Gestión de costos y precios'
for c in s.cs:
 if c['properties']['text']=='Productos, costos y precios':c['properties']['text']=s.title
s=get('p03');s.btn(54,825,330,'Ver mis reportes','preport')
s=get('w20');s.link(280,825,900,'Administrar transportes y volver a asignar la ruta','wtrans')
# Keep the original physical-stock example, now with named products rather than generic meat.
s=replace('w14','Faeneo · cortes obtenidos por lote',['CU08'],'Producción');s.banner(210,'OP-007 · control sanitario APTO · ANI-007 · resultados pendientes de confirmar peso')
s.field(280,300,510,'Inicio real del faeneo','26/10/2026 · 08:10');s.field(852,300,520,'Fin real del desposte','26/10/2026 · 10:55')
s.table(280,415,[290,230,220,352],['Producto del catálogo','Tipo de corte','Lote','Estado del resultado'],[['Costilla de cerdo','Costilla · carne fresca','COS-2510','Pendiente de pesaje'],['Lomo de cerdo','Lomo · carne fresca','LOM-2610','Pendiente de pesaje']],rowh=65)
s.para(280,610,1092,60,'Una orden puede obtener varios cortes. Seleccionar cada producto y su lote; los resultados todavía no aumentan las existencias.',15)
s.btn(280,700,315,'Añadir corte del catálogo','wresult');s.btn(625,700,315,'Enviar a pesaje de Almacén','w14p');s.btn(970,700,320,'Consultar catálogo','wcat')
s.para(280,790,1092,55,'Tiempos y cantidades son ilustrativos. No se promete un rendimiento estándar del animal.',14)
s=Screen('w14p','Almacén · confirmar resultados y pesajes',cu=['CU08']);s.web('Producción');s.banner(210,'OP-007 · registro manual de pesos · no hay conexión automática a balanza')
s.table(280,310,[260,220,150,150,150,162],['Producto / corte','Lote','Bruto','Tara','Neto','Unidad'],[['Costilla de cerdo','COS-2510','10,4','0,4','10','kg'],['Lomo de cerdo','LOM-2610','6,4','0,4','6','kg']],rowh=72)
s.field(280,565,510,'Responsable de la captura','Almacén');s.field(852,565,520,'Fecha y hora del pesaje','26/10/2026 · 11:00')
s.para(280,680,1092,55,'Validar producto, lote y unidad. Neto = bruto − tara. Confirmar el pesaje conserva el resultado; recibir físicamente es otra operación.',14)
s.btn(280,785,340,'Confirmar y pasar a recepción','w11');s.btn(650,785,310,'Corregir resultado','wresult')
s=Screen('wresult','Seleccionar corte o derivado obtenido',cu=['CU08','CU07']);s.web('Producción');s.field(280,220,510,'Orden de producción','OP-007 · Faeneo / desposte');s.field(852,220,520,'Familia','Carne fresca')
s.field(280,335,510,'Tipo de corte','Lomo');s.field(852,335,520,'Producto activo del catálogo','LOM-KG · Lomo de cerdo');s.field(280,450,510,'Lote obtenido','LOM-2610');s.field(852,450,520,'Unidad de registro','kg')
s.card(280,575,1092,120,'Producto identificado','La clasificación pertenece al producto. Cada corte o derivado se registra en su propia fila y lote. No se introduce una cantidad prevista como stock.')
s.btn(280,760,330,'Guardar resultado pendiente','w14');s.btn(640,760,330,'Cancelar','w14')
# Show the derivative selection explicitly and send approval to manual weighing.
s=get('w15')
for c in s.cs:
 t=c['properties']['text']
 if t=='Derivado / lote':c['properties']['text']='Producto / tipo / lote'
 if t=='Jamón · JAM-2610':c['properties']['text']='JAM-KG · Jamón elaborado · JAM-2610';c['properties']['size']='12'
 if t=='Cantidad real / unidad':c['properties']['text']='Resultado para pesar / unidad'
 if t=='Guardar resultado aprobado':c['properties']['href']='mockup://'+uid('w15p')
s=Screen('w15p','Almacén · pesaje del derivado',cu=['CU08']);s.web('Producción');s.banner(210,'OP-009 · derivado aprobado · producto JAM-KG · Jamón elaborado')
for x,y,w,n,v in [(280,310,510,'Lote obtenido','JAM-2610'),(852,310,520,'Clasificación','DERIVADO · Jamón elaborado'),(280,425,335,'Peso bruto','3,6 kg'),(658,425,335,'Tara','0,4 kg'),(1035,425,335,'Peso neto','3,2 kg'),(280,540,510,'Responsable','Almacén'),(852,540,520,'Fecha y hora','26/10/2026 · registro real')]:s.field(x,y,w,n,v)
s.para(280,665,1092,60,'La cantidad obtenida queda confirmada con su producto y lote. La entrada física del derivado se registra después; los consumos reales ya conservan su salida.',14)
s.btn(280,780,350,'Confirmar y recibir derivado','w11');s.btn(660,780,310,'Corregir datos','w15')
s=Screen('wcat','Productos: cortes, derivados e insumos',cu=['CU07']);s.web('Productos');s.field(280,205,620,'Buscar por código, producto o tipo','Costilla, lomo, jamón…');s.btn(930,235,230,'Buscar','wcat')
s.table(280,330,[150,260,260,150,272],['Código','Producto','Familia / tipo','Unidad','Acción'],[['COS-KG','Costilla de cerdo','Carne fresca / Costilla','kg',('Editar','wprod')],['LOM-KG','Lomo de cerdo','Carne fresca / Lomo','kg',('Editar','wprod')],['JAM-KG','Jamón elaborado','Derivado / Jamón','kg',('Editar','wprod')]],rowh=68)
s.btn(280,660,300,'Crear producto','wprod');s.btn(610,660,300,'Administrar clasificaciones','wclass');s.btn(940,660,300,'Costos y precios','w05');s.para(280,760,1092,70,'Crear o editar un producto define qué se comercializa. La existencia se actualiza mediante recepción y movimientos autorizados; desactivar conserva lotes e historial.',14)
s=Screen('wprod','Ficha de producto',cu=['CU07']);s.web('Productos')
for x,y,w,n,v in [(280,220,510,'Código único','COS-KG'),(852,220,520,'Nombre comercial','Costilla de cerdo'),(280,335,510,'Familia','Carne fresca'),(852,335,520,'Tipo de corte / derivado','Costilla'),(280,450,510,'Presentación','Fresca por kilogramo'),(852,450,520,'Unidad','kg'),(280,565,1092,'Descripción','Corte identificado en el catálogo del negocio')]:s.field(x,y,w,n,v)
s.btn(280,735,300,'Guardar producto','wcat');s.btn(610,735,300,'Desactivar sin borrar','wprodoff');s.btn(940,735,300,'Cancelar','wcat');s.para(280,810,1092,45,'No cambiar una unidad usada en operaciones históricas. El nuevo producto comienza sin stock.',13)
s=Screen('wprodoff','Producto desactivado',cu=['CU07']);s.web('Productos');s.card(280,240,1092,190,'COS-KG · Inactivo','El producto conserva lotes, pedidos y movimientos históricos. No se ofrece para nuevas cotizaciones. Resolver operaciones abiertas antes de confirmar la desactivación.');s.btn(280,520,330,'Volver al catálogo','wcat');s.btn(640,520,330,'Editar / habilitar','wprod')
s=Screen('wclass','Clasificaciones de productos',cu=['CU07']);s.web('Productos');s.table(280,215,[200,300,300,292],['Código','Nombre del tipo','Familia','Estado'],[['COR-COS','Costilla','Carne fresca','Activo'],['COR-LOM','Lomo','Carne fresca','Activo'],['DER-JAM','Jamón elaborado','Derivado','Activo']],rowh=58)
s.field(280,490,335,'Código','COR-COS');s.field(658,490,335,'Nombre','Costilla');s.field(1035,490,335,'Familia','Carne fresca');s.field(280,595,1092,'Descripción','Clasificación de corte usada por productos del catálogo');s.btn(280,760,300,'Guardar clasificación','wclass');s.btn(610,760,300,'Desactivar con uso activo',disabled=True);s.btn(940,760,300,'Volver a productos','wcat')
s=Screen('wtrans','Transportes y entregas',cu=['CU11']);s.web('Transporte / entregas');s.table(280,220,[170,260,210,220,232],['Código','Transportista','Modalidad','Estado','Acción'],[['TRA-01','Transportista registrado','Externo','Activo',('Editar','wtransedit')],['TRA-02','Chanchería','Propio','Activo',('Editar','wtransedit')]],rowh=75)
s.card(280,485,1092,130,'Ruta Norte · responsable de entrega asignado','Seleccionar un transporte disponible antes de despachar. La ruta y cada entrega conservan su estado; cerrar recorrido no salda deuda.');s.btn(280,730,300,'Crear transporte','wtransedit');s.btn(610,730,300,'Asignar ruta / entregas','w20');s.btn(940,730,300,'Control de frío','w22')
s=Screen('wtransedit','Ficha de transporte',cu=['CU11']);s.web('Transporte / entregas')
for x,y,w,n,v in [(280,220,510,'Código','TRA-01'),(852,220,520,'Modalidad','Externo'),(280,325,510,'Transportista / responsable','Transportista registrado'),(852,325,520,'Contacto','Contacto del transportista'),(280,430,510,'Placa e identificación','Completar vehículo'),(852,430,520,'Conservación / descripción','Condiciones verificadas por responsable'),(280,535,510,'Capacidad de referencia','Definir cantidad y unidad'),(852,535,520,'Estado','Activo')]:s.field(x,y,w,n,v)
s.para(280,650,1092,50,'Consultar, editar o desactivar conserva rutas e historial. Reasignar entregas pendientes antes de desactivar.',14);s.btn(280,755,300,'Guardar transporte','wtrans');s.btn(610,755,300,'Desactivar','wtransoff');s.btn(940,755,300,'Cancelar','wtrans')
s=Screen('wtransoff','Desactivación de transporte',cu=['CU11']);s.web('Transporte / entregas');s.card(280,250,1092,170,'TRA-01 · revisión de asignaciones','Si hay entregas pendientes, reasignarlas antes de desactivar. Con dependencias resueltas, conservar el transporte inactivo y todo su historial.');s.btn(280,540,330,'Revisar ruta y reasignar','w20');s.btn(640,540,330,'Volver a transportes','wtrans')
s=Screen('wreport','Reportes del negocio',cu=['CU12']);s.web('Reportes');s.field(280,220,335,'Reporte autorizado','Producción obtenida');s.field(658,220,335,'Desde','26/10/2026');s.field(1035,220,335,'Hasta','26/10/2026');s.field(280,325,510,'Producto / tipo','Todos los cortes y derivados');s.field(852,325,520,'Estado','Resultado confirmado')
s.table(280,455,[200,280,280,180,152],['Orden','Producto','Tipo','Cantidad','Unidad'],[['OP-007','Costilla de cerdo','Carne fresca / Costilla','10','kg'],['OP-007','Lomo de cerdo','Carne fresca / Lomo','6','kg'],['OP-009','Jamón elaborado','Derivado / Jamón','3,2','kg']],rowh=58)
s.btn(280,725,300,'Aplicar filtros','wreport');s.btn(610,725,300,'Exportar PDF / Excel','wexport');s.para(280,810,1092,45,'Datos ilustrativos. Reportes según permisos: clientes, pedidos, producción, inventario, cobranza y entregas.',13)
s=Screen('wexport','Exportación del reporte',cu=['CU12']);s.web('Reportes');s.card(280,240,1092,180,'Producción obtenida · 26/10/2026','Conserva filtros y permisos de la consulta. Incluye orden, producto, tipo de corte/derivado, cantidad y unidad. La exportación no modifica las operaciones.');s.btn(280,530,300,'Elegir PDF','wreport');s.btn(610,530,300,'Elegir Excel','wreport');s.btn(940,530,300,'Volver','wreport')
s=Screen('preport','Mis reportes',kind='portal',cu=['CU12']);s.portal();s.field(54,250,620,'Desde','01/10/2026');s.field(720,250,620,'Hasta','31/10/2026');s.table(54,390,[250,360,300,376],['Pedido','Situación de entrega','Cargos / pagos','Saldo'],[['PED-042','Entregada conforme','Bs 170 / Bs 90','Bs 80']],rowh=85);s.para(54,590,1286,60,'Solo tus operaciones y documentos confirmados. La entrega está cerrada; el saldo conserva su vencimiento acordado.',16);s.btn(54,725,360,'Consultar con estos filtros','preport');s.btn(445,725,360,'Exportar mis datos','pexport')
s=Screen('pexport','Exportar mis operaciones',kind='portal',cu=['CU12']);s.portal();s.card(54,260,1286,180,'Reporte de Restaurante El Patio','Período 01–31 octubre de 2026. Incluye exclusivamente tus pedidos, entregas y saldos. Se vuelven a comprobar los permisos antes de generar el archivo.');s.btn(54,550,360,'Elegir PDF','preport');s.btn(445,550,360,'Elegir Excel','preport');s.btn(836,550,360,'Volver a mis reportes','preport')
s=Screen('preg','Crear cuenta de comprador',cu=['CU01']);s.label(120,90,1200,s.title,30,True,h=55)
for x,y,w,n,v in [(120,210,560,'Nombre / razón social',''),(750,210,560,'Identificación',''),(120,330,560,'Correo de contacto',''),(750,330,560,'Teléfono',''),(120,450,560,'Usuario',''),(750,450,560,'Contraseña','')]:s.field(x,y,w,n,v)
s.para(120,590,1180,65,'Esta cuenta permite gestionar tus solicitudes y consultar tus operaciones. Las cuentas del personal las crea la administración.',17);s.btn(120,730,360,'Registrar cuenta','pregdone');s.btn(510,730,360,'Ya tengo cuenta','w01')
s=Screen('pregdone','Cuenta de comprador registrada',cu=['CU01']);s.label(120,110,1180,s.title,30,True,h=55);s.card(120,260,1180,180,'Registro completado','Inicia sesión con tus credenciales para acceder al portal. Si tus datos ya existen, recupera acceso; no se crea una cuenta duplicada.');s.btn(120,560,360,'Ir a iniciar sesión','w01')
s=Screen('pforgot','Recuperar acceso',cu=['CU01']);s.label(120,110,1180,s.title,30,True,h=55);s.field(120,260,800,'Contacto asociado a la cuenta','');s.para(120,390,1180,75,'Si el contacto corresponde a una cuenta, recibirás instrucciones de recuperación. El enlace tiene vigencia limitada y se usa una sola vez.',18);s.btn(120,550,360,'Solicitar recuperación','preset');s.btn(510,550,360,'Volver','w01')
s=Screen('preset','Establecer nueva contraseña',cu=['CU01']);s.label(120,110,1180,s.title,30,True,h=55);s.field(120,260,800,'Token del enlace verificado','');s.field(120,380,800,'Nueva contraseña','');s.para(120,510,1180,75,'Con token válido se guarda la nueva contraseña y se invalidan las sesiones anteriores. Token inválido o vencido: solicitar otro, sin cambiar credenciales.',17);s.btn(120,670,360,'Guardar e iniciar sesión','w01');s.btn(510,670,360,'Solicitar otro enlace','pforgot')
s=Screen('wclient','Nuevo cliente',cu=['CU03']);s.web('Clientes');s.field(280,225,510,'Nombre / razón social','');s.field(852,225,520,'Identificación','');s.field(280,350,510,'Teléfono','');s.field(852,350,520,'Tipo de cliente','Restaurante / comercio / particular');s.field(280,475,1092,'Dirección de entrega','');s.para(280,615,1092,60,'Buscar coincidencias antes de guardar. Un cliente presencial puede comprar sin tener cuenta en el portal.',16);s.btn(280,755,330,'Guardar cliente','w03');s.btn(640,755,330,'Cancelar','w03')
s=Screen('wclientblock','Revisar desactivación del cliente',cu=['CU03']);s.web('Clientes');s.card(280,250,1092,180,'Restaurante El Patio · saldo pendiente Bs 80','Resolver pedidos y deuda pendientes antes de desactivar. Se conserva el historial; no se elimina la ficha ni las operaciones.');s.btn(280,540,330,'Consultar deuda','w17');s.btn(640,540,330,'Volver a la ficha','w03');s.btn(1000,540,330,'Desactivar',disabled=True)
s=Screen('wuser','Crear usuario del personal',cu=['CU02']);s.web('Usuarios');s.field(280,225,510,'Nombre','');s.field(852,225,520,'Usuario único','');s.field(280,350,510,'Contacto','');s.field(852,350,520,'Responsabilidad','Almacén');s.field(280,475,1092,'Permisos autorizados','Pesajes de producción, recepción, movimientos y reservas');s.para(280,615,1092,60,'La administración asigna permisos. No se conceden funciones internas mediante registro público de comprador.',16);s.btn(280,755,330,'Crear usuario','w04');s.btn(640,755,330,'Cancelar','w04')
s=Screen('wuseroff','Desactivar usuario',cu=['CU02']);s.web('Usuarios');s.card(280,250,1092,185,'Cuenta seleccionada · revisión previa','Se revocan sus sesiones y se conserva su historial. Reasignar responsabilidades pendientes y mantener al menos un administrador habilitado. Las capturas de reparto pendientes deben resolverse con autorización.');s.btn(280,550,330,'Confirmar desactivación','w04');s.btn(640,550,330,'Cancelar','w04')
for key in ['w12','w12n']:
 for c in get(key).cs:
  if c['properties']['text']=='Costilla':c['properties']['text']='Lomo de cerdo'
# Product-specific receipt preserves the derivative context instead of sending it to the cut receipt.
s=Screen('w11d','Almacén · recibir derivado físicamente',cu=['CU09']);s.web('Inventario');s.banner(210,'OP-009 · resultado confirmado · Jamón elaborado · JAM-KG')
s.field(280,310,510,'Referencia única de entrada','ENT-009-JAM');s.field(852,310,520,'Lote / aptitud','JAM-2610 · APTO');s.field(280,425,510,'Cantidad recibida / unidad','3,2 kg');s.field(852,425,520,'Ubicación','Cámara 1');s.card(280,550,1092,120,'Recepción física del resultado','La referencia se aplica una sola vez. Esta entrada corresponde a jamón elaborado; los consumos de fabricación ya quedaron registrados por separado.');s.btn(280,750,350,'Confirmar entrada de derivado','w10');s.btn(660,750,310,'Corregir pesaje','w15p')
for c in get('w15p').cs:
 if c['properties']['text']=='Confirmar y recibir derivado':c['properties']['href']='mockup://'+uid('w11d')
# Present new module screens near related existing screens, preserving native resource links.
for s in SCREENS:
 s.note='Datos ilustrativos; prototipo navegable, no ejecución de operaciones. '+s.note
footer=footer.replace('range(1,27)','range(1,13)').replace('SGCC · Web y Android · stock y alcance 26-10','SGCC · Doce módulos · 29-10-2026')
a=footer.index("readme='# Mockups");z=footer.index('# Vista auxiliar',a);footer=footer[:a]+footer[z:]
footer=footer.replace("Path('/tmp/sgcc_mockups_revision')","Path('/tmp/sgcc_reorganizacion_20261029/Mockups_preview')")
exec(compile(footer,'mockups_export','exec'),globals())
