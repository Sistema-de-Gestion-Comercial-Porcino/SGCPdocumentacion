"""Mockups Balsamiq alineados con la web real (SGCPuiweb, 19 nov 2026).

Uso: python3 actualizar_20261119.py <carpeta temporal>

Reutiliza generar_mockups.py + v5/mockups.py (las 67 pantallas ya revisadas) y cambia:
- la barra lateral por el menú exacto de Views/Shared/_Layout.cshtml (secciones y nombres), visto por PROPIETARIO,
  que tiene todos los permisos (DatosIniciales); en CU13 la cuenta es SUPERADMIN;
- W16: la seña se resuelve en Cobranza → Señas con un acuerdo de resolución (la incidencia ya no cuelga del pedido);
- pantallas nuevas para las opciones del menú que no tenían una: Rutas, Conflictos de recepción, Auditoría,
  y las de CU13 (cuentas de nivel superior) y CU14 (delegar Finanzas).
Escribe 04_Mockups_Balsamiq/SGCC_Web_Android.bmpr, su Indice_pantallas.json y la copia en 02_Ingenieria_de_Software.
"""
import shutil, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parents[1]
STAGE = Path(sys.argv[1]).resolve()
(STAGE / "04_Mockups_Balsamiq").mkdir(parents=True, exist_ok=True)

v5 = (AQUI.parent / "v5" / "mockups.py").read_text(encoding="utf-8")
v5 = v5.replace("STAGE=Path('/tmp/sgcc_reorganizacion_20261029')", f"STAGE=Path({str(STAGE)!r})")
v5 = v5.replace("Path('/tmp/sgcc_reorganizacion_20261029')", f"Path({str(STAGE)!r})")
v5 = v5.replace("'/tmp/sgcc_reorganizacion_20261029/Mockups_preview'", repr(str(STAGE / "Mockups_preview")))

# --- barra lateral igual a _Layout.cshtml
WEB_NUEVO = r'''
 def web(self,active):
  MENU=[('ESPACIO DE TRABAJO',[('Resumen','w02'),('Usuarios','w04'),('Clientes','w03'),('Productos','wcat'),('Gestión de costos','w05'),('Cotizaciones','w06'),('Pedidos','w09')]),
        ('PRODUCCIÓN E INVENTARIO',[('Sanidad','w13'),('Producción','w12'),('Existencias','w10'),('Pesajes y entradas','w14p'),('Control de frío','w22')]),
        ('COBRANZA',[('Saldos y pagos','w17')]),
        ('TRANSPORTE Y ENTREGAS',[('Entregas','w20'),('Rutas','wrutas'),('Transportes','wtrans'),('Conflictos de recepción','wconf')]),
        ('CONSULTAS',[('Reportes','wreport'),('Auditoría','waudit')])]
  ALIAS={'Inicio':'Resumen','Inventario':'Existencias','Cobranza':'Saldos y pagos','Transporte / entregas':'Entregas','Entregas / rutas':'Entregas','Usuarios y roles':'Usuarios','Productos / precios':'Gestión de costos'}
  POR_CLAVE={'w13':'Sanidad','w14p':'Pesajes y entradas','w15p':'Pesajes y entradas','w11':'Pesajes y entradas','w11d':'Pesajes y entradas','w22':'Control de frío','wtrans':'Transportes','wtransedit':'Transportes','wtransoff':'Transportes','w16':'Saldos y pagos'}
  active=POR_CLAVE.get(self.key,ALIAS.get(active,active))
  self.label(28,18,210,'SGCP',24,True,h=38);self.label(28,54,210,'Gestión comercial porcino',11)
  self.label(280,30,560,'Gestión comercial · Chanchería',17,True);self.link(860,30,250,'Portal comprador','p01')
  self.link(1140,30,280,('superadmin · SUPERADMIN' if self.key=='wsuper' else 'Ana · PROPIETARIO')+'  |  Salir','w01');self.line(20,83,1400)
  y=96
  for sec,items in MENU:
   self.label(28,y,220,sec,10,True,h=18);y+=21
   for n,k in items:self.btn(24,y,220,('> ' if n==active else '')+n,k,h=30);y+=35
   y+=5
  self.label(28,y+4,215,'Operación con conexión',11)
  self.label(280,110,1085,self.title,25,True,h=44);self.label(280,158,1080,'26 oct 2026  ·  Chanchería',12)
'''
marca = "exec(compile(prefix,'mockups_base','exec'),globals())"
assert marca in v5
v5 = v5.replace(marca, "_i=prefix.index(' def web(self,active):');_f=prefix.index(' def portal(self):')\n"
                "prefix=prefix[:_i]+WEB_NUEVO.lstrip('\\n')+prefix[_f:]\n"
                "assert 'MENU=[' in prefix\n" + marca)

# --- pantallas nuevas y W16, antes de añadir las notas comunes
EXTRA = r'''
s=replace('w16','Señas de PED-042',['CU10'],'Saldos y pagos');s.banner(210,'Si una seña se cancela, se registra el acuerdo de resolución. El sistema no devuelve ni retiene dinero automáticamente.')
s.table(280,300,[170,170,170,150,250,182],['Referencia','Fecha','Medio','Importe','Situación','Acciones'],[['SEN-042','25 oct','Efectivo','Bs 50','Registrada',('Aplicar a…','w17')],['SEN-043','25 oct','QR','Bs 20','Con acuerdo de resolución','—']],rowh=64)
s.field(280,480,335,'Referencia','SEN-044');s.field(658,480,335,'Importe · Bs','30,00');s.field(1035,480,335,'Medio','Transferencia')
s.btn(280,600,300,'Registrar seña','w16');s.btn(610,600,300,'Registrar acuerdo','w16');s.btn(940,600,300,'Volver al pedido','w09')
s.para(280,690,1092,60,'Si la seña ya se aplicó, el sistema lo rechaza y lo avisa: no se aplica dos veces. La incidencia de calidad se registra en el animal o el lote, no en el pedido.',14)
s=Screen('wrutas','Rutas',cu=['CU11']);s.web('Rutas');s.para(280,200,1092,30,'Cada ruta asocia un transporte, un responsable y sus entregas a domicilio.',14)
s.table(280,250,[220,220,380,272],['Ruta','Salida','Transporte y responsable','Estado'],[['RUT-NORTE','26 oct · 09:30','TRA-02 · reparto.01','EN_REPARTO'],['RUT-SUR','27 oct · por definir','TRA-01 · reparto.02','PLANIFICADA']],rowh=62)
s.btn(280,470,300,'+ Planificar ruta','w20');s.btn(610,470,300,'Finalizar',disabled=True)
s.para(280,560,1092,80,'Finalizar una ruta exige que todas sus entregas tengan resultado (entregada, observada o cancelada) y que no queden conflictos. No resuelve observaciones ni salda deudas.',14)
s=Screen('wconf','Conflictos de recepción',cu=['CU11']);s.web('Conflictos de recepción');s.para(280,200,1092,50,'Capturas que llegaron cuando la entrega ya había cambiado (reasignada, cancelada o con otra versión). Esperan que una persona las revise.',14)
s.table(280,270,[150,170,110,160,170,150,182],['Entrega','Receptor','Peso','Fecha real','Llegó al servidor','Versión','Acción'],[['ENT-042','Encargado','4 kg','26 oct 12:05','26 oct 15:40','3 (actual 4)',('Revisar','wconf')]],rowh=66)
s.card(280,420,1092,120,'Un conflicto nunca se resuelve solo','No sobrescribe la entrega. Al revisar, se aplica la captura o se descarta con un motivo; la captura original y su evidencia se conservan.')
s.btn(280,600,300,'Aplicar captura','wconf');s.btn(610,600,300,'Descartar con motivo','wconf');s.btn(940,600,300,'Ver entregas','w20')
s=Screen('waudit','Auditoría',cu=['CU15']);s.web('Auditoría');s.para(280,200,1092,30,'Historial de acciones del sistema. Solo consulta.',14)
s.table(280,250,[260,220,330,282],['Fecha (Bolivia)','Usuario','Acción','Módulo'],[['19 nov 2026 · 10:40','dueno','ESTADO DESHABILITADO','Usuario'],['19 nov 2026 · 09:05','dueno','EDITAR PERMISOS','Usuario'],['19 nov 2026 · 08:30','superadmin','CREAR','Usuario']],rowh=56)
s.btn(280,520,200,'Anterior',disabled=True);s.btn(500,520,200,'Siguiente','waudit');s.para(730,526,640,30,'Página 1 de 3 · 52 registros',13)
s.para(280,610,1092,60,'Solo Superadministrador y Propietario tienen el permiso auditoria.consultar. La consulta no crea, edita ni borra registros.',14)
s=Screen('wsuper','Cuenta de nivel superior',cu=['CU13']);s.web('Usuarios');s.banner(206,'Solo el Superadministrador crea, edita o desactiva cuentas con rol PROPIETARIO o SUPERADMIN.')
s.field(280,300,510,'Nombre completo','Rosa');s.field(852,300,520,'Usuario','rosa');s.field(280,405,510,'Correo electrónico','rosa@example.invalid');s.field(852,405,520,'Contraseña inicial o nueva','••••••••')
s.card(280,515,1092,120,'Responsabilidades','[x] PROPIETARIO   [ ] SUPERADMIN   [ ] ADMINISTRADOR   [ ] FINANZAS   [ ] VENTAS ... Nadie cambia sus propios privilegios; siempre queda un Superadministrador activo.')
s.btn(280,700,300,'Guardar cambios','w04');s.btn(610,700,300,'Cancelar','w04')
s=Screen('wfinanzas','Delegar rol de Finanzas',cu=['CU14']);s.web('Usuarios');s.banner(206,'Solo PROPIETARIO o SUPERADMIN asignan o retiran FINANZAS. Un Administrador no puede delegarlo.')
s.field(280,300,510,'Nombre completo','Carla');s.field(852,300,520,'Usuario','carla')
s.card(280,410,1092,120,'Responsabilidades','[x] VENTAS   [x] FINANZAS   [ ] ADMINISTRADOR   [ ] ALMACEN ... FINANZAS da costos, cargos, pagos, saldos y comprobante fiscal.')
s.para(280,560,1092,50,'Un cambio de permisos cerrará las sesiones del usuario: el próximo ingreso trae los permisos financieros.',14)
s.btn(280,660,300,'Guardar cambios','w04');s.btn(610,660,300,'Cancelar','w04')
for c in get('w04').cs:
 t=c['properties']['text']
 if t=='Administración / ventas / cobranza':c['properties']['text']='VENTAS · FINANZAS'
 if t=='Responsable de entrega':c['properties']['text']='ENTREGA'
s=get('w04');s.btn(820,825,250,'Cuenta superior (CU13)','wsuper');s.btn(1090,825,250,'Delegar Finanzas (CU14)','wfinanzas')
'''
marca2 = "for s in SCREENS:\n s.note="
assert marca2 in v5
v5 = v5.replace(marca2, EXTRA + marca2, 1)
v5 = v5.replace("footer=footer.replace('range(1,27)','range(1,13)')", "footer=footer.replace('range(1,27)','range(1,16)')")
assert "range(1,16)" in v5
v5 = v5.replace("'SGCC · Doce módulos · 29-10-2026'", "'SGCC · Web y Android · alineado con la web 19-11-2026'")

g = {"__name__": "mockups_20261119", "__file__": str(AQUI.parent / "v5" / "mockups.py"), "WEB_NUEVO": WEB_NUEVO}
exec(compile(v5, "v5_mockups_20261119", "exec"), g)

origen = STAGE / "04_Mockups_Balsamiq"
if "--publicar" not in sys.argv:
    print("revisión en", origen); sys.exit(0)
for n in ("SGCC_Web_Android.bmpr", "Indice_pantallas.json"):
    shutil.copy2(origen / n, BASE / "04_Mockups_Balsamiq" / n)
shutil.copy2(origen / "SGCC_Web_Android.bmpr", BASE / "02_Ingenieria_de_Software" / "SGCC_Web_Android.bmpr")
print("copiado a", BASE / "04_Mockups_Balsamiq", "y 02_Ingenieria_de_Software")
