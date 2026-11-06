"""Prototipo Balsamiq nativo. Datos ilustrativos coherentes; navegación entre escenarios."""
from pathlib import Path
import sqlite3,json,uuid,time,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Mockups_Balsamiq';OUT.mkdir(exist_ok=True)
DEST=OUT/'SGCC_Web_Android.bmpr'
NS=uuid.UUID('c0941a6b-5afb-4d46-8db0-690fb8412912')
uid=lambda key:str(uuid.uuid5(NS,key)).upper()
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SCREENS=[]
class Screen:
 def __init__(self,key,title,kind='web',cu=(),note=''):
  self.key=key;self.title=title;self.kind=kind;self.cu=list(cu);self.note=note;self.cs=[];self.W,self.H=(414,896) if kind in ['android','responsive'] else (1440,920)
  self.add('Canvas',0,0,self.W,self.H,'');SCREENS.append(self)
 def add(self,t,x,y,w,h,txt='',**p):
  props={'text':str(txt),'size':'14',**{k:str(v).lower() if isinstance(v,bool) else str(v) for k,v in p.items()}}
  o=dict(ID=str(len(self.cs)),typeID=t,x=str(x),y=str(y),w=str(w),h=str(h),measuredW=str(w),measuredH=str(h),zOrder=str(len(self.cs)),properties=props);self.cs.append(o);return o
 def label(self,x,y,w,txt,size=14,bold=False,h=26):return self.add('Label',x,y,w,h,txt,size=size,bold=bold)
 def para(self,x,y,w,h,txt,size=14,bold=False):return self.add('Paragraph',x,y,w,h,txt,size=size,bold=bold)
 def line(self,x,y,w):return self.add('HRule',x,y,w,2)
 def btn(self,x,y,w,txt,target=None,disabled=False,h=42):
  props={'size':14}
  if disabled:props['state']='disabled'
  elif target:props['href']='mockup://'+uid(target)
  return self.add('Button',x,y,w,h,txt,**props)
 def link(self,x,y,w,txt,target):return self.add('Link',x,y,w,28,txt,size=14,href='mockup://'+uid(target))
 def field(self,x,y,w,name,value='',hint=None):
  self.label(x,y,w,name,13,True,h=24);self.add('TextInput',x,y+28,w,40,value,size=15)
  if hint:self.para(x,y+75,w,42,hint,12)
 def card(self,x,y,w,h,title,body):
  self.add('Canvas',x,y,w,h,'');self.label(x+20,y+16,w-40,title,16,True);self.para(x+20,y+53,w-40,h-65,body,14)
 def banner(self,y,txt,w=1092,x=280):
  self.add('Canvas',x,y,w,58,'');self.para(x+16,y+12,w-32,38,txt,14)
 def web(self,active):
  self.label(28,24,210,'SGCC',25,True,h=42);self.label(280,30,650,'Gestión comercial y clientes',17,True)
  self.link(1140,30,250,'Ana · Administración  |  Salir','w01');self.line(20,83,1400)
  nav=[('Inicio','w02'),('Clientes','w03'),('Usuarios y roles','w04'),('Cotizaciones','w06'),('Pedidos','w09'),('Productos / precios','w05'),('Inventario','w10'),('Producción','w12'),('Cobranza','w17'),('Entregas / rutas','w20'),('Control de frío','w22')]
  for i,(n,k) in enumerate(nav):self.btn(24,112+i*48,220,('> ' if n==active else '')+n,k,h=39)
  self.label(28,750,210,'Conectado',12);self.link(28,800,215,'Portal comprador','p01');self.link(28,838,215,'Vista móvil web','r01')
  self.label(280,110,1085,self.title,25,True,h=44);self.label(280,158,1080,'26 oct 2026  ·  Chanchería',12)
 def portal(self):
  self.label(38,25,530,'Chanchería · Catálogo y pedidos',23,True,h=42)
  for x,w,n,k in [(830,150,'Catálogo','p01'),(1000,190,'Mis pedidos','p03'),(1210,180,'Salir','w01')]:self.btn(x,27,w,n,k)
  self.line(30,85,1380);self.label(54,118,1320,self.title,26,True,h=46)
  self.label(54,170,1320,'Restaurante El Patio · Tu cuenta',14)
 def phone(self,connection='Conectado',back=None):
  self.label(22,17,360,'SGCC Reparto' if self.kind=='android' else 'SGCC · Navegador web',15,True)
  self.label(22,54,370,self.title,22,True,h=40)
  self.add('Canvas',18,110,378,48,'');self.label(30,122,354,connection,13,True)
  self.line(18,817,378)
  if back:self.btn(22,837,170,'Volver',back,h=44)
  self.btn(222,837,170,'Mis entregas' if self.kind=='android' else 'Inicio', 'a03' if self.kind=='android' else 'r01',h=44)
 def table(self,x,y,widths,headers,rows,actions=None,rowh=66):
  W=sum(widths);self.add('Canvas',x,y,W,42+rowh*len(rows),'')
  px=x
  for width,h in zip(widths,headers):self.para(px+12,y+12,width-24,26,h,12,True);px+=width
  self.line(x,y+42,W)
  for ri,row in enumerate(rows):
   py=y+42+ri*rowh;px=x
   for ci,(width,cell) in enumerate(zip(widths,row)):
    if isinstance(cell,tuple):self.btn(px+10,py+12,width-20,cell[0],cell[1],h=38)
    else:self.para(px+12,py+12,width-24,rowh-16,cell,14)
    px+=width
   if ri+1<len(rows):self.line(x,py+rowh,W)

s=Screen('w01','Iniciar sesión',cu=['CU01']);s.label(120,100,1180,'SGCC · Gestión comercial',32,True,h=55);s.para(120,170,570,160,'Clientes, cotizaciones, preparación, entregas y cobros en un mismo sistema.',21)
s.card(120,400,480,170,'Acceso con conexión','La web requiere internet. Usa tu cuenta y los permisos asignados por la administración.')
s.field(760,240,510,'Usuario','ana.ventas');s.field(760,335,510,'Contraseña','••••••••');s.btn(760,440,510,'Ingresar a gestión','w02',h=48);s.link(760,520,510,'Entrar al portal comprador','p01')

s=Screen('w02','Resumen del negocio',cu=['CU17','CU08']);s.web('Inicio')
for x,n,v in [(280,'En preparación','12 pedidos'),(560,'Por cobrar','Bs 3.240'),(840,'Reparto de hoy','4 entregas'),(1120,'Producción prevista','2 órdenes')]:s.card(x,210,252,135,n,v)
s.label(280,385,800,'Seguimiento de hoy',19,True)
s.table(280,433,[190,330,340,232],['Referencia','Cliente','Situación','Acción'],[['PED-042','Restaurante El Patio','Preparado · crédito autorizado',('Ver pedido','w09')],['ENT-042','Restaurante El Patio','Asignada · ruta Norte',('Ver reparto','w20')],['CLI-017','Restaurante El Patio','Saldo pendiente: Bs 80',('Ver cuenta','w17')]],rowh=74)
s.btn(280,760,245,'Nueva cotización','w06');s.btn(550,760,245,'Revisar producción','w12')

s=Screen('w03','Clientes y ficha comercial',cu=['CU03','CU17']);s.web('Clientes');s.field(280,205,620,'Buscar cliente','Restaurante El Patio');s.btn(925,234,230,'Buscar','w03')
s.table(280,310,[300,230,300,262],['Cliente','Tipo','Contacto','Acción'],[['Restaurante El Patio','Restaurante','700 123 456',('Ver cuenta','w17')]],rowh=68)
s.field(280,460,520,'Nombre / razón social','Restaurante El Patio');s.field(852,460,520,'Teléfono','700 123 456');s.field(280,565,520,'Dirección de entrega','Av. Norte, local 17');s.field(852,565,520,'Condición habitual de pago','Crédito por acuerdo')
s.para(280,665,1090,50,'La ficha identifica al cliente y sus operaciones. Cada venta a crédito requiere autorización y vencimiento acordados.',14)
s.btn(280,748,255,'Guardar ficha','w03');s.btn(558,748,255,'Cotizar al cliente','w06')

s=Screen('w04','Usuarios y permisos',cu=['CU02']);s.web('Usuarios y roles');s.table(280,212,[260,250,380,202],['Usuario','Estado','Roles asignados','Acción'],[['ana.ventas','Activo','Administración / ventas / cobranza',('Editar','w04')],['reparto.01','Activo','Responsable de entrega',('Editar','w04')]],rowh=70)
s.field(280,460,520,'Cuenta','reparto.01');s.field(852,460,520,'Rol','Responsable de entrega');s.card(280,570,1092,130,'Permisos del reparto','Consultar asignaciones autorizadas, registrar recepción y sincronizar. El rol no permite registrar cobros ni modificar precios.')
s.btn(280,750,240,'Guardar permisos','w04');s.para(550,752,820,50,'Los cambios quedan auditados. Una persona puede tener varios roles.',13)

s=Screen('w05','Productos, costos y precios',cu=['CU04','CU24']);s.web('Productos / precios');s.table(280,212,[310,160,205,205,212],['Producto','Unidad','Costo referencia','Precio vigente','Vigencia'],[['Carne de cerdo / corte','kg','Bs 28,00','Bs 35,00','Desde 25 oct'],['Jamón','kg','Según costo','Por confirmar','No publicado']],rowh=76)
s.field(280,475,335,'Precio de venta','Bs 35,00');s.field(658,475,335,'Inicio de vigencia','25/10/2026 · 06:00');s.field(1035,475,335,'Costo de referencia','Bs 28,00')
s.banner(595,'El propietario fija costo de referencia y precio. Margen estimado: Bs 7/kg; el histórico se conserva.')
s.btn(280,714,260,'Registrar vigencia','w05');s.btn(566,714,260,'Ver catálogo público','p01');s.para(280,790,1092,55,'Costo de referencia ingresado manualmente. No se distribuye automáticamente el costo del animal o del faeneo entre cortes.',14)

for key,title,accepted in [('w06','Cotización COT-028 · presentada',False),('w07','Cotización COT-028 · aceptada',True)]:
 s=Screen(key,title,cu=['CU05','CU06']);s.web('Cotizaciones');s.banner(206,'ACEPTADA · versión 2 · vigente hasta 26 oct, 18:00' if accepted else 'PRESENTADA · versión 2 · esperando respuesta del cliente')
 s.label(280,292,1090,'Restaurante El Patio · Fecha propuesta: 26 oct, 12:00',17,True)
 s.table(280,345,[440,180,230,242],['Producto','Cantidad','Precio acordado','Importe'],[['Carne de cerdo / corte','4 kg','Bs 35/kg','Bs 140']],rowh=72)
 s.card(280,500,1092,114,'Servicio de faeneo / corte','Bs 30 acordados por separado, solo si se realiza el servicio. El total final del ejemplo será Bs 170 cuando se preste.')
 if accepted:
  s.btn(280,695,320,'Crear pedido confirmado','w09');s.para(640,697,710,55,'Se conserva el precio y costo acordados. La preparación comienza después de confirmar.',14)
 else:
  s.btn(280,695,310,'Registrar aceptación','w07');s.btn(612,695,310,'Registrar rechazo / cambios','w08');s.btn(944,695,310,'Crear pedido',disabled=True)
  s.para(280,767,1050,42,'La solicitud todavía no es un pedido. No se reserva producto ni se inicia preparación.',14)

s=Screen('w08','Respuesta del cliente · sin pedido',cu=['CU05']);s.web('Cotizaciones');s.banner(206,'COT-028 · El cliente no acepta las condiciones actuales.')
s.card(280,300,520,235,'Solicita cambios','Registrar cantidades, productos o fecha solicitada. Preparar una nueva versión y obtener una nueva aceptación.')
s.card(852,300,520,235,'Desiste de la compra','Conservar la cotización rechazada y el motivo. Cerrar la solicitud sin generar pedido, reserva ni cobro.')
s.btn(300,568,480,'Preparar nueva cotización','w06');s.btn(872,568,480,'Conservar rechazo y volver','w02');s.btn(280,695,330,'Crear pedido',disabled=True)

s=Screen('w09','Pedido PED-042',cu=['CU06','CU07','CU08','CU13']);s.web('Pedidos');s.banner(206,'CONFIRMADO · origen COT-028 aceptada · Restaurante El Patio')
s.table(280,300,[350,180,240,322],['Concepto','Cantidad','Importe','Preparación'],[['Carne de cerdo','4 kg','Bs 140','Preparado'],['Servicio de faeneo / corte','Realizado','Bs 30','Prestación registrada']],rowh=72)
s.card(280,525,520,136,'Preparación','Entrega comprometida: 26 oct, 12:00. Stock apto y pesajes confirmados.')
s.card(852,525,520,136,'Condición de pago','Crédito autorizado. Saldo vigente del ejemplo: Bs 80. Entrega y deuda se consultan por separado.')
s.para(280,685,1092,35,'Margen estimado de productos: 4 kg × (Bs 35 - Bs 28) = Bs 28. Servicio registrado por separado.',14);s.btn(280,730,240,'Revisar reservas','w10');s.btn(545,730,240,'Ver preparación','w12');s.btn(810,730,240,'Ver despacho','w20');s.link(1080,739,280,'Resolver incidencia','w16')

s=Screen('w10','Inventario y reserva',cu=['CU07']);s.web('Inventario');s.table(280,220,[275,190,190,190,247],['Producto / lote','Ubicación','Físico','Reservado','Disponible'],[['Carne · CAR-2510','Cámara 1','10 kg','4 kg','6 kg aptos']],rowh=84)
s.field(280,410,500,'Pedido / detalle','PED-042 · carne 4 kg');s.field(830,410,540,'Referencia de reserva','R-042-A')
s.banner(535,'La referencia ya existe: se conserva la misma reserva de 4 kg. No se descuenta de nuevo.')
s.btn(280,675,300,'Consultar reserva','w09');s.btn(610,675,300,'Registrar entrada física','w11');s.btn(940,675,300,'Ver escenario sin stock','w10f')

s=Screen('w10f','Faltante antes de la preparación',cu=['CU07','CU08']);s.web('Inventario');s.banner(210,'PED-042 · Se necesitan 4 kg de carne · no se puede reservar todavía')
s.table(280,315,[330,230,240,292],['Producto','Físico apto','Reservado','Disponible'],[['Carne de cerdo','0 kg','0 kg','0 kg']],rowh=66)
s.card(280,465,1092,150,'Ya existe una orden prevista: OP-007','Previsión de carne: 10 kg; fin previsto 26 oct, 11:00. Revisar capacidad y confirmar fecha con el cliente. La previsión no cuenta como stock ni garantiza el resultado.')
s.btn(280,680,320,'Revisar orden vigente','w12');s.btn(630,680,320,'Acordar otra solución','w16');s.btn(980,680,320,'Reservar sin existencia',disabled=True)
s.para(280,765,1092,55,'Si vence la fecha sin recepción, registrar retraso y acordar otra solución. Almacén confirma cantidades reales antes de reservar.',14)

s=Screen('w11','Entrada o movimiento físico',cu=['CU12']);s.web('Inventario');s.field(280,220,500,'Referencia única','ENT-008');s.field(830,220,540,'Tipo de movimiento','Entrada');s.field(280,330,500,'Lote / producto / aptitud','CAR-2510 · carne · APTO');s.field(830,330,540,'Ubicación','Cámara 1');s.field(280,440,500,'Cantidad recibida / unidad','8 kg');s.field(830,440,540,'Origen identificado','OP-007 · producción propia')
s.card(280,555,1092,130,'Almacén confirma lo recibido','Entrada parcial anterior: 2 kg. Nueva entrada: 8 kg. Resultado físico: 10 kg. Reenviar ENT-008 recupera el registro; no vuelve a sumar.')
s.btn(280,730,300,'Confirmar entrada única','w10');s.btn(610,730,300,'Cancelar registro','w10');s.para(280,795,1092,45,'El origen también puede ser recepción externa documentada. Las previsiones no son cantidades recibidas.',14)

s=Screen('w12','Órdenes y previsiones de producción',cu=['CU08']);s.web('Producción')
s.table(280,215,[180,260,190,250,212],['Orden','Tipo','Estado','Fin previsto','Acción'],[['OP-007','Faeneo / desposte','Programada','26 oct · 11:00',('Revisar','w14')],['OP-009','Derivado: jamón','Pendiente','Por acordar',('Revisar','w15')]],rowh=65)
s.table(280,440,[350,300,442],['Previsión OP-007','Cantidad estimada','Demanda / disponibilidad'],[['Carne de cerdo','10 kg','PED-042 solicita 4 kg; aún sin reserva'],['Costilla','6 kg','Reposición manual de stock']],rowh=57)
s.para(280,630,1092,70,'Producción revisa órdenes vigentes antes de crear otra. Las previsiones por producto no son existencias. El responsable registra inicio y fin previstos; si el plazo no sirve, acuerda otra solución.',14)
s.btn(280,750,300,'Control sanitario','w13');s.btn(610,750,300,'Revisar faltante','w10f');s.btn(940,750,300,'Resolver plazo / recursos','w16')

s.link(280,825,1000,'Crear orden manual cuando no exista reposición viable','w12n')

s=Screen('w12n','Nueva orden manual de producción',cu=['CU08']);s.web('Producción');s.banner(210,'Ejemplo: OP-010 para reposición de stock del 27 oct · sin pedido vinculado')
s.field(280,305,510,'Tipo de orden','Faeneo / desposte');s.field(852,305,520,'Responsable','Producción');s.field(280,405,510,'Inicio previsto','27/10/2026 · por definir');s.field(852,405,520,'Fin previsto','27/10/2026 · por definir')
s.table(280,510,[350,240,240,262],['Producto previsto','Cantidad estimada','Unidad','Demanda'],[['Carne de cerdo','Ingresar estimación','kg','Reposición manual'],['Costilla','Ingresar estimación','kg','Reposición manual']],rowh=54)
s.para(280,690,1092,60,'Revisar órdenes vigentes y recursos antes de guardar. Las cantidades se estiman por producto; los animales y su control sanitario se verifican antes del faeneo.',14)
s.btn(280,790,330,'Volver a órdenes vigentes','w12');s.btn(640,790,330,'Guardar sin fecha ni cantidades',disabled=True)

s=Screen('w13','Control sanitario previo',cu=['CU09']);s.web('Producción');s.field(280,215,510,'Animal','ANI-007');s.field(852,215,520,'Procedencia','Proveedor identificado en registro');s.field(280,325,510,'Responsable del control','Responsable sanitario');s.field(852,325,520,'Fecha de control','26/10/2026 · 07:45');s.field(280,435,1092,'Observación','Registrar la evaluación del responsable')
s.card(280,550,1092,115,'Antes del faeneo','Un rechazo bloquea la orden y abre una incidencia. No genera lote apto ni permite continuar al faeneo.')
s.btn(280,730,330,'Registrar APTO','w14');s.btn(640,730,330,'Registrar RECHAZADO','w16')

s=Screen('w14','Faeneo · resultados reales por producto',cu=['CU10']);s.web('Producción');s.banner(210,'OP-007 · control sanitario APTO · ANI-007 · peso de ingreso 100 kg')
s.field(280,300,510,'Inicio real','26/10/2026 · 08:10');s.field(852,300,520,'Fin real','26/10/2026 · 10:55')
s.table(280,410,[320,240,230,302],['Producto obtenido','Lote','Cantidad real','Origen del pesaje'],[['Carne de cerdo','CAR-2510','10 kg','Balanza'],['Costilla','COS-2610','6 kg','Balanza']],rowh=67)
s.btn(280,620,270,'Añadir otro resultado','w14');s.para(580,620,790,64,'Vista parcial de los resultados registrados. Los pesos y tiempos son ejemplos; no representan un rendimiento ni una duración estándar.',14)
s.para(280,710,1092,45,'Registrar resultados no aumenta existencias. Almacén debe confirmar la entrada física de cada lote.',14)
s.btn(280,785,360,'Guardar resultados y fin real','w11');s.link(680,790,650,'Continuar con recepción física en Almacén','w11')

s=Screen('w15','Fabricación de derivados · OP-009',cu=['CU11']);s.web('Producción')
s.table(280,215,[350,250,200,292],['Insumo','Lote','Consumo real','Movimiento único'],[['Carne de cerdo','CAR-2510','3 kg','CONS-009-CAR-01'],['Otros ingredientes','Identificar cada lote','Registrar cantidad','Referencia por consumo']],rowh=68)
s.field(280,450,335,'Derivado / lote','Jamón · JAM-2610');s.field(658,450,335,'Cantidad real / unidad','3,2 kg');s.field(1035,450,335,'Calidad evaluada','Aprobada / rechazada')
s.field(280,550,510,'Inicio real','26/10/2026 · 12:00');s.field(852,550,520,'Fin real','26/10/2026 · hora registrada al finalizar');s.para(280,650,1092,70,'10 kg físicos - 3 kg consumidos = 7 kg. Con 4 kg reservados quedan 3 kg disponibles. Si se rechaza el derivado, los insumos realmente consumidos no vuelven a estar disponibles.',14)
s.btn(280,745,330,'Guardar resultado aprobado','w11');s.btn(640,745,330,'Guardar resultado rechazado','w16');s.para(280,810,1092,42,'Almacén registra la entrada del derivado apto por separado. El consumo conserva su referencia única.',13)

s=Screen('w16','Incidencia y resolución del anticipo',cu=['CU13']);s.web('Pedidos');s.banner(210,'PED-042 · PENDIENTE DE ACUERDO · despacho suspendido')
s.card(280,305,520,185,'Incidencia de preparación','Animal/lote rechazado o faltante sin resolver. Registrar reemplazo, nueva fecha o cancelación acordada.')
s.card(852,305,520,185,'Seña registrada: Bs 50','La seña conserva su referencia S-042. La cancelación no ordena devolución ni retención automática.')
s.field(280,535,1092,'Acuerdo y tratamiento de la seña','Pendiente de acuerdo con el cliente');s.para(280,640,1090,55,'Sin acuerdo registrado, el pedido conserva su estado pendiente y no se habilita el despacho.',14)
s.btn(280,740,320,'Conservar pendiente','w16');s.btn(630,740,320,'Registrar acuerdo',disabled=True);s.btn(980,740,320,'Autorizar despacho',disabled=True)

s=Screen('w17','Cuenta y pagos · Restaurante El Patio',cu=['CU14','CU16','CU17']);s.web('Cobranza');s.table(280,215,[390,240,242,220],['Concepto / referencia','Cargo','Pago aplicado','Saldo'],[['Carne · PED-042','Bs 140','Bs 20 seña + Bs 40 abono','Bs 80'],['Servicio prestado','Bs 30','Bs 30 de la seña','Bs 0']],rowh=85)
s.label(280,470,1092,'Total Bs 170 − seña Bs 50 − abono Bs 40 = saldo Bs 80',19,True,h=40)
s.field(280,545,335,'Tipo de pago','Abono');s.field(660,545,335,'Referencia recibida','A-042-01');s.field(1040,545,332,'Importe recibido','Bs 40')
s.para(280,655,1090,55,'La referencia A-042-01 ya existe: se recupera el pago registrado. Solo se crea un pago cuando hubo dinero recibido.',14)
s.btn(280,755,300,'Recuperar pago existente','w17');s.btn(610,755,300,'Crédito y seguimiento','w18');s.btn(940,755,300,'Comprobante fiscal','w19')

s=Screen('w18','Crédito y seguimiento de cobranza',cu=['CU15','CU18']);s.web('Cobranza');s.field(280,220,510,'Importe originalmente autorizado','Bs 120');s.field(852,220,520,'Vencimiento acordado','28/10/2026 · 18:00');s.field(280,330,510,'Saldo actual','Bs 80 · vigente');s.field(852,330,520,'Responsable que autorizó','Propietario / usuario autorizado');s.field(280,440,1092,'Resultado de la gestión','Sin nuevo abono; contactar en la fecha acordada');s.field(280,550,510,'Próximo seguimiento','29/10/2026 · 09:00')
s.para(852,558,520,80,'El plazo corresponde al acuerdo de esta operación. No se aplica un vencimiento fijo de treinta días.',14)
s.btn(280,740,300,'Guardar seguimiento','w18');s.btn(610,740,300,'Registrar dinero recibido','w17')

s=Screen('w19','Comprobante fiscal',cu=['CU19']);s.web('Cobranza');s.banner(210,'PED-042 · referencia F-042 · INTEGRACIÓN FISCAL PENDIENTE DE CONFIRMACIÓN')
s.card(280,310,1092,160,'Resultado pendiente','Confirmar modalidad y proveedor antes de habilitar emisión o consulta. Mientras tanto permanece pendiente, sin número fiscal. Con integración habilitada, los reintentos conservan la misma referencia.')
s.field(280,530,510,'Modalidad / proveedor','Pendiente de confirmar y configurar');s.field(852,530,520,'Número fiscal','Todavía no emitido')
s.btn(280,735,320,'Consultar al proveedor',disabled=True);s.btn(630,735,320,'Descargar comprobante',disabled=True)

s=Screen('w20','Despacho y ruta Norte',cu=['CU20']);s.web('Entregas / rutas');s.table(280,220,[210,280,230,200,172],['Entrega / pedido','Cliente','Modalidad','Autorización','Acción'],[['ENT-042 / PED-042','El Patio','Reparto propio','Preparado + crédito',('Abrir','w20')]],rowh=85)
s.field(280,430,510,'Responsable asignado','reparto.01');s.field(852,430,520,'Vehículo','Vehículo registrado');s.card(280,545,1092,136,'Antes de salir','El responsable descarga online las entregas preparadas y autorizadas en su app Android. La hoja de despacho no es constancia de recepción.')
s.btn(280,750,300,'Guardar asignación','w20');s.btn(610,750,300,'Registrar retiro local','w21');s.btn(940,750,300,'Control de frío','w22')

s=Screen('w21','Recepción de retiro en local',cu=['CU21']);s.web('Entregas / rutas');s.banner(210,'Escenario de retiro local · requiere conexión · entrega autorizada')
s.field(280,320,510,'Quién recibe','Encargada del restaurante');s.field(852,320,520,'Peso confirmado','4 kg');s.field(280,430,510,'Fecha / hora física','26/10/2026 · 12:20');s.field(852,430,520,'Evidencia','recepcion042.jpg');s.field(280,540,1092,'Observaciones','Recepción conforme')
s.btn(280,730,330,'Confirmar retiro conforme','p03');s.btn(640,730,330,'Registrar observación','w16');s.para(280,795,1060,38,'La constancia se habilita tras la confirmación del servidor. El saldo se conserva.',13)

s=Screen('w22','Control de frío',cu=['CU22']);s.web('Control de frío');s.field(280,220,510,'Ubicación / lote / entrega','ENT-042 · transporte');s.field(852,220,520,'Responsable del control','Responsable de reparto');s.field(280,330,510,'Temperatura registrada','3,5 °C');s.field(852,330,520,'Fecha y hora','26/10/2026 · 11:45');s.field(280,440,1092,'Evaluación del responsable','Conforme según evaluación del responsable')
s.banner(580,'Lectura de conservación de carne o transporte, evaluada por el responsable. Umbrales automáticos pendientes de validación.')
s.btn(280,735,330,'Guardar control online','w20');s.btn(640,735,330,'Registrar incidencia','w16')

s=Screen('w23','FUTURO · alertas de clientes',cu=['CU23'],note='RF09 fuera del alcance de la entrega actual.');s.web('')
s.banner(220,'Función futura · fuera del alcance actual según la planificación presentada')
s.card(280,345,1092,200,'Diseño reservado para otra fase','Se conserva la idea de avisar tras tres días sin compras de un cliente habitual. Antes de implementarla se deberá acordar cómo identificar habitualidad. Esta entrega no genera alertas ni exige registrar contactos por inactividad.')
s.btn(280,640,330,'Activar alertas',disabled=True);s.btn(640,640,330,'Registrar contacto',disabled=True);s.btn(280,750,330,'Volver al inicio','w02')

s=Screen('p01','Catálogo disponible',kind='portal',cu=['CU24']);s.portal();s.card(54,250,620,210,'Carne de cerdo · cortes','Bs 35 / kg · precio vigente\nDisponibilidad referencial. La cantidad se confirma al atender la solicitud.')
s.card(720,250,620,210,'Derivados','Jamón: sin stock disponible. Consulta reposición; fecha y cantidad se confirman con ventas antes de aceptar una cotización.')
s.btn(74,520,580,'Solicitar 4 kg de carne','p02');s.btn(740,520,580,'Consultar mis pedidos','p03');s.link(54,760,600,'Ver portal en pantalla móvil','r02')

s=Screen('p02','Solicitar una cotización',kind='portal',cu=['CU25']);s.portal();s.field(54,250,620,'Producto','Carne de cerdo · corte por kg');s.field(720,250,620,'Cantidad solicitada','4 kg');s.field(54,365,620,'Modalidad','Reparto');s.field(720,365,620,'Fecha solicitada','26/10/2026 · por confirmar');s.field(54,480,1286,'Observación','Indicar cortes y dirección de entrega')
s.para(54,610,1286,70,'Enviar esta solicitud no confirma la compra ni reserva producto. Ventas presentará la cotización y solicitará tu aceptación.',17)
s.btn(54,745,380,'Enviar solicitud de cotización','p04');s.btn(465,745,280,'Volver al catálogo','p01')

s=Screen('p04','Solicitud recibida',kind='portal',cu=['CU25']);s.portal();s.banner(250,'COT-029 · BORRADOR · pendiente de atención de ventas',1286,54);s.card(54,370,1286,170,'Todavía no hay un pedido','Recibimos la solicitud de carne por 4 kg. Podrás aceptar o pedir cambios cuando ventas presente la cotización con precio y condiciones. No se ha reservado stock.')
s.btn(54,650,360,'Volver al catálogo','p01');s.btn(445,650,360,'Ver mis pedidos anteriores','p03')

s=Screen('p03','Mi pedido PED-042',kind='portal',cu=['CU26']);s.portal();s.card(54,250,620,200,'Entrega confirmada','ENT-042 · recibió la encargada\nPeso: 4 kg · fecha física 26 oct, 12:20\nConfirmación del servidor: 26 oct, 12:25')
s.card(720,250,620,200,'Saldo pendiente: Bs 80','Producto Bs 140 + servicio Bs 30\nSeña Bs 50 + abono Bs 40\nVencimiento acordado: 28 oct')
s.btn(54,515,390,'Ver constancia de recepción','p05');s.btn(475,515,390,'Comprobante fiscal pendiente',disabled=True)
s.para(54,650,1286,60,'Esta cuenta solo puede consultar sus propios pedidos y comprobantes. Confirmar la entrega no registra un pago.',16)

s=Screen('p05','Constancia de recepción',kind='portal',cu=['CU26','CU21']);s.portal();s.card(54,240,1286,330,'ENT-042 · recepción conforme confirmada','Cliente: Restaurante El Patio\nPedido: PED-042\nRecibió: encargada del restaurante\nFecha física: 26/10/2026 · 12:20\nConfirmación central: 26/10/2026 · 12:25\nPeso confirmado: 4 kg\nEvidencia: recepcion042.jpg')
s.para(54,615,1286,55,'Esta constancia acredita recepción. No acredita saldo cero ni reemplaza el comprobante fiscal.',16)
s.btn(54,745,350,'Volver al pedido','p03')

s=Screen('r01','Resumen de gestión',kind='responsive',cu=['CU17','CU23']);s.phone('Web con conexión');s.card(22,183,370,112,'Pedidos en preparación','12 pedidos');s.card(22,315,370,112,'Por cobrar','Bs 3.240');s.card(22,447,370,112,'Reparto de hoy','4 entregas')
s.btn(22,590,370,'Clientes y cuentas','w03',h=48);s.btn(22,654,370,'Cotizaciones','w06',h=48);s.link(22,730,370,'Abrir gestión en escritorio','w02')
s=Screen('r02','Mi pedido',kind='responsive',cu=['CU26']);s.phone('Portal web con conexión');s.card(22,183,370,168,'PED-042 · El Patio','Entrega ENTREGADA\nRecibió: encargada · 4 kg\n26 oct · 12:20')
s.card(22,374,370,138,'Saldo pendiente: Bs 80','Vencimiento: 28 oct\nLa entrega no salda la deuda.')
s.btn(22,556,370,'Constancia de recepción','p05',h=48);s.btn(22,624,370,'Solicitar cotización','p02',h=48);s.link(22,716,370,'Ver catálogo','p01')

s=Screen('a01','Acceder al reparto',kind='android',cu=['CU01']);s.phone('Conectado');s.field(22,200,370,'Usuario','reparto.01');s.field(22,307,370,'Contraseña','••••••••');s.btn(22,419,370,'Iniciar sesión','a02',h=50)
s.para(22,508,370,110,'Inicia sesión y descarga tus entregas antes de salir. Sin conexión puedes continuar un reparto ya descargado con tu cuenta.',15);s.link(22,680,370,'Abrir reparto ya descargado','a03')

s=Screen('a02','Descargar mi reparto',kind='android',cu=['CU01','CU20']);s.phone('Conectado · sesión válida','a01');s.card(22,187,370,200,'Ruta Norte · 1 entrega','ENT-042 · PED-042\nRestaurante El Patio\nCarne 4 kg · preparada\nDespacho con crédito autorizado')
s.btn(22,430,370,'Descargar entrega y datos','a03',h=50);s.para(22,526,370,115,'La descarga incluye la dirección, el responsable y los datos necesarios para registrar la recepción. Verifica que termine antes de salir.',15)

s=Screen('a03','Mis entregas',kind='android',cu=['CU21']);s.phone('Sin conexión · datos descargados','a02');s.card(22,190,370,230,'ENT-042 · El Patio','PED-042 · carne 4 kg\nAv. Norte, local 17\nResponsable: reparto.01\nDescargada: 26 oct · 11:00\nEstado al descargar: EN TRASLADO')
s.btn(22,465,370,'Registrar recepción','a04',h=50);s.btn(22,534,370,'Ver envíos pendientes','a05',h=50);s.para(22,635,370,100,'Solo aparecen entregas descargadas y asignadas a tu cuenta. Para recibir nuevas asignaciones necesitas conexión.',14)

for key,observed in [('a04',False),('a04o',True)]:
 s=Screen(key,'Registrar recepción',kind='android',cu=['CU21'],note='Alternativa observada' if observed else 'Recepción conforme');s.phone('Sin conexión · ENT-042','a03');s.field(22,185,370,'Quién recibió','Encargada del restaurante');s.field(22,282,170,'Fecha y hora real','26 oct · 12:20');s.field(214,282,178,'Peso confirmado','4 kg')
 s.label(22,380,370,'Resultado de la recepción',13,True);s.btn(22,412,174,'Conforme','a04',h=44);s.btn(210,412,182,'Con observaciones','a04o',h=44)
 s.field(22,488,370,'Observación', 'Peso pendiente de revisión' if observed else 'Recepción conforme')
 s.label(22,585,370,'Evidencia: recepcion042.jpg',14);s.btn(22,630,370,'Guardar recepción en el teléfono','a05o' if observed else 'a05',h=50)
 s.para(22,711,370,75,'El envío queda pendiente. El sistema central recibirá la información al sincronizar.',14)

for key,observed in [('a05',False),('a05o',True)]:
 s=Screen(key,'Recepción guardada',kind='android',cu=['CU21']);s.phone('Sin conexión · pendiente de envío','a03');s.card(22,190,370,213,'ENT-042 · guardada en el teléfono','Receptor y peso conservados\nEvidencia local disponible\nResultado: '+('con observaciones' if observed else 'conforme')+'\nAún no registrada en el servidor')
 s.para(22,438,370,92,'No borres los datos ni desinstales la app antes de enviar las recepciones pendientes.',15)
 s.btn(22,582,370,'Sincronizar',disabled=True,h=50);s.para(22,652,370,80,'Conéctate y abre Sincronización para enviar. La deuda conserva su propio estado.',14)
 s.link(22,750,370,'Revisar conexión y envíos','a06o' if observed else 'a06')

for key,observed in [('a06',False),('a06o',True)]:
 s=Screen(key,'Sincronización',kind='android',cu=['CU21']);s.phone('Conectado · sesión válida','a03');s.card(22,190,370,180,'1 recepción pendiente','ENT-042 · El Patio\nDatos y evidencia listos para enviar\n'+('Recepción con observaciones' if observed else 'Recepción conforme'))
 s.btn(22,419,370,'Enviar recepción pendiente','a09' if observed else 'a08',h=50)
 s.para(22,513,370,105,'Mantén la app abierta. Si el envío se interrumpe, la recepción se conserva para reintentar.',15)
 s.link(22,669,370,'Ver caso de conflicto','a07');s.link(22,718,370,'Ver sesión vencida','a10')

s=Screen('a07','Recepción por revisar',kind='android',cu=['CU21']);s.phone('Conectado · conflicto informado','a06');s.card(22,189,370,178,'ENT-042 · no aplicada','La asignación cambió después de la descarga. El servidor no aplicó la recepción.')
s.para(22,406,370,108,'Conserva la evidencia y comunica el caso al responsable. No vuelvas a registrar la entrega para forzar el envío.',15)
s.btn(22,565,370,'Conservar para revisión','a07',h=50);s.btn(22,635,370,'Forzar confirmación',disabled=True,h=50);s.para(22,717,370,65,'La corrección o descarte requiere revisión autorizada y deja historial.',13)

s=Screen('a08','Recepción sincronizada',kind='android',cu=['CU21']);s.phone('Conectado · confirmación recibida','a03');s.card(22,185,370,234,'ENT-042 · ENTREGADA','Recibió: encargada del restaurante\nPeso: 4 kg\nRecepción física: 12:20\nConfirmación central: 12:25\nReferencia: RC-2091')
s.para(22,466,370,102,'La recepción conforme ya está registrada. La cobranza se gestiona por separado y esta acción no registra un pago.',15)
s.btn(22,626,370,'Volver a mis entregas','a03',h=50);s.para(22,714,370,54,'La constancia puede consultarse en la web.',14)

s=Screen('a09','Observación sincronizada',kind='android',cu=['CU21']);s.phone('Conectado · confirmación recibida','a03');s.card(22,186,370,230,'ENT-042 · OBSERVADA','Se enviaron datos y evidencia.\nObservación: peso pendiente de revisión.\nLa entrega requiere resolver la observación; no está cerrada.')
s.para(22,465,370,115,'El envío está confirmado, pero la entrega permanece observada. El responsable registra la solución antes del cierre.',15)
s.btn(22,636,370,'Volver a mis entregas','a03',h=50)

s=Screen('a10','Renovar acceso',kind='android',cu=['CU01','CU21']);s.phone('Conectado · sesión vencida','a06');s.card(22,188,370,132,'Tus capturas están conservadas','Renueva la sesión con la misma cuenta para enviar los pendientes.')
s.field(22,368,370,'Usuario','reparto.01');s.field(22,475,370,'Contraseña','••••••••');s.btn(22,591,370,'Autenticar y volver al envío','a06',h=50);s.para(22,695,370,70,'No necesitas volver a capturar la recepción ni borrar los datos locales.',14)

# Validación de navegación, dimensiones y cobertura antes de escribir la base.
keys={s.key for s in SCREENS};ids={uid(k) for k in keys};assert len(keys)==len(SCREENS)
links=0
for s in SCREENS:
 for c in s.cs:
  x,y,w,h=[float(c[k]) for k in ['x','y','w','h']];assert min(x,y)>=0 and min(w,h)>0
  assert x+w<=s.W+1 and y+h<=s.H+1,(s.key,c)
  href=c['properties'].get('href')
  if href:assert href.split('mockup://')[-1] in ids;links+=1
assert {f'CU{i:02}' for i in range(1,27)}<={cu for s in SCREENS for cu in s.cu}
now=int(time.time()*1000);tmp=DEST.with_suffix('.nuevo.bmpr')
if tmp.exists():tmp.unlink()
db=sqlite3.connect(tmp);db.executescript('CREATE TABLE INFO(NAME TEXT PRIMARY KEY,VALUE TEXT); CREATE TABLE BRANCHES(ID TEXT PRIMARY KEY,ATTRIBUTES TEXT); CREATE TABLE RESOURCES(ID TEXT,BRANCHID TEXT,ATTRIBUTES TEXT,DATA TEXT,PRIMARY KEY(ID,BRANCHID)); CREATE TABLE THUMBNAILS(ID TEXT PRIMARY KEY,ATTRIBUTES TEXT);')
j=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':'))
db.executemany('INSERT INTO INFO VALUES(?,?)',[('SchemaVersion','1.2'),('ArchiveRevision','3'),('ArchiveRevisionUUID',str(uuid.uuid4()).upper()),('ArchiveFormat','bmpr'),('ArchiveAttributes',j({'creationDate':now,'name':'SGCC · Web y Android · stock y alcance 26-10'}))])
db.execute('INSERT INTO BRANCHES VALUES(?,?)',('Master',j({'branchDescription':'','creationDate':now,'fontFace':'Balsamiq Sans','fontSize':14,'linkColor':545684,'modifiedBy':[],'projectDescription':'Web responsiva y Android Kotlin para reparto. Prototipo enlazado; datos de ejemplo.','selectionColor':9813234,'skinName':'sketch','symbolLibraryID':''})))
for index,s in enumerate(SCREENS):
 attrs={'creationDate':now,'importedFrom':'','parentID':'','kind':'mockup','mimeType':'text/vnd.balsamiq.bmml','modifiedBy':None,'name':f'{index+1:02} · {s.key.upper()} · {s.title}','notes':f'Canal: {s.kind}. Casos: {", ".join(s.cu)}. '+s.note,'order':index,'thumbnailID':'','trashed':False}
 data={'mockup':{'controls':{'control':s.cs},'measuredW':str(s.W),'measuredH':str(s.H),'version':'1.0'}}
 db.execute('INSERT INTO RESOURCES VALUES(?,?,?,?)',(uid(s.key),'Master',j(attrs),j(data)))
db.commit();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close();tmp.replace(DEST)
summary={'pantallas':len(SCREENS),'enlaces':links,'controles':sum(len(s.cs) for s in SCREENS),'archivos':[{'clave':s.key,'nombre':s.title,'canal':s.kind,'ancho':s.W,'alto':s.H,'casos':s.cu} for s in SCREENS]}
(OUT/'Indice_pantallas.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
readme='# Mockups SGCC · revisión integral\n\n[Abrir SGCC_Web_Android.bmpr](SGCC_Web_Android.bmpr). '+str(len(SCREENS))+' pantallas editables, enlazadas para usar el modo Presentación de Balsamiq. Son escenarios ilustrativos; el prototipo no ejecuta validaciones, pagos ni descargas reales.\n\n'
readme+='La web usa lienzos de 1440 × 920; las vistas web móviles y Android usan 414 × 896. Gestión y portal requieren conexión. Android permite guardar recepción solo de entregas asignadas y descargadas antes del reparto.\n\n## Recorridos para revisar\n\n- Venta: W01 → W02 → W06 → W07 → W09. W08 muestra rechazo/cambios sin crear pedido.\n- Preparación: W09 → W10/W12 → W13 → W14/W15 → W11. W16 conserva incidencia y anticipo hasta acuerdo.\n- Cobro y reparto: W17 → W18 → W20. W21 muestra retiro online; W22 registra frío online.\n- Comprador: P01 → P02 → P04 (solicitud sin pedido); P03 → P05 (pedido previo y constancia).\n- Android conforme: A01 → A02 → A03 → A04 → A05 → A06 → A08.\n- Android observado: A04O → A05O → A06O → A09. Confirmar el envío deja la entrega OBSERVADA. A07 muestra conflicto y A10 sesión vencida.\n\n'
readme+='## Alcance actualizado\n\nRF09/CU23 se conserva como pantalla FUTURA aislada del menú, sin acciones activas. RF16 y RF21 también están fuera de alcance. W10F muestra un faltante con orden ya prevista; W12 separa previsión de existencia; W14 registra varios productos; W11 confirma entrada real y W15 descuenta consumos. RF11 permanece pendiente hasta confirmar integración.\n\n## Datos ilustrativos\n\nRestaurante El Patio, PED-042 y ENT-042. Carne: 4 kg × Bs 35 = Bs 140; servicio prestado Bs 30; total Bs 170. Seña Bs 50 + abono Bs 40 = saldo Bs 80. Las páginas representan momentos distintos del mismo ejemplo; antes de aceptar la cotización todavía no hay pedido. Las horas de faeneo no establecen duración estándar. Costo de referencia Bs 28/kg: margen estimado de los 4 kg vendidos Bs 28. OP-007 muestra carne 10 kg y costilla 6 kg como resultados parciales del ejemplo. Entrada anterior 2 + nueva 8 = físico 10; reserva 4 deja disponible 6; consumo posterior 3 deja físico 7 y disponible 3.\n\n'
readme+='## Cobertura\n\n| Pantalla | Canal | Casos |\n|---|---|---|\n'
for s in SCREENS:readme+=f'| {s.key.upper()} · {s.title} | {s.kind} | {", ".join(s.cu)} |\n'
readme+='\nLos botones deshabilitados expresan condiciones todavía no cumplidas. Los enlaces cambian de escenario; los campos son controles editables del diseño. Referencia de uso: [enlaces y modo Presentación de Balsamiq](https://balsamiq.com/support/creating-and-editing/linking/).\n'
(OUT/'LEEME.md').write_text(readme)
# Vista auxiliar para revisión interna de composición: no es exportación nativa ni captura de Balsamiq.
preview=Path('/tmp/sgcc_mockups_revision');preview.mkdir(exist_ok=True)
fontcache={}
def font(size,bold=False):
 key=(size,bold)
 if key not in fontcache:fontcache[key]=ImageFont.truetype(fontpath.replace('.ttf','-Bold.ttf') if bold else fontpath,size)
 return fontcache[key]
def wrap(draw,text,ff,width):
 lines=[]
 for line in text.split('\n'):
  buf=''
  for word in line.split():
   test=(buf+' '+word).strip()
   if draw.textlength(test,font=ff)>width and buf:lines.append(buf);buf=word
   else:buf=test
  lines.append(buf)
 return lines
for s in SCREENS:
 im=Image.new('RGB',(s.W,s.H),'white');dr=ImageDraw.Draw(im)
 for c in s.cs:
  x,y,w,h=[int(c[k]) for k in ['x','y','w','h']];p=c['properties'];t=c['typeID'];txt=p.get('text','');fs=int(p.get('size',14));ff=font(fs,p.get('bold')=='true');fill='#777777' if p.get('state')=='disabled' else '#202020'
  if t=='Canvas':dr.rectangle([x,y,x+w-1,y+h-1],outline='#949494')
  elif t=='HRule':dr.line([x,y,x+w,y],fill='#aaaaaa',width=1)
  elif t in ['Button','TextInput']:
   dr.rounded_rectangle([x,y,x+w-1,y+h-1],radius=4,outline='#999999' if p.get('state')=='disabled' else '#333333',fill='#f4f4f4' if p.get('state')=='disabled' else '#ffffff')
   yy=y+(h-fs)/2-3;xx=x+(w-dr.textlength(txt,font=ff))/2 if t=='Button' else x+10;dr.text((xx,yy),txt,font=ff,fill=fill)
  else:
   lines=wrap(dr,txt,ff,w) if t=='Paragraph' else txt.split('\n')
   for i,line in enumerate(lines):dr.text((x,y+i*(fs+5)),line,font=ff,fill=fill)
   if t=='Link':dr.line([x,y+fs+4,x+min(w,dr.textlength(txt,font=ff)),y+fs+4],fill='#555555')
 im.save(preview/(s.key+'.png'))
print(json.dumps({k:v for k,v in summary.items() if k!='archivos'},ensure_ascii=False))
