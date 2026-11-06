from pathlib import Path
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side
import hashlib,json,math
B=Path(__file__).resolve().parents[2];T=Path('/tmp/sgcc_reorganizacion_20261029');p=B/'Formato Proyecto - SGCC 1 1.xlsx';before=hashlib.sha256(p.read_bytes()).hexdigest();w=load_workbook(p);s1,s2=w.worksheets[:2]
def locked(s):
 return [(c.coordinate,c.value,c.data_type,str(c._style),c.number_format)for row in s.iter_rows(min_row=29,max_row=40)for c in row],[(n,s.row_dimensions[n].height)for n in range(29,41)],sorted(str(r)for r in s.merged_cells.ranges if r.min_row>=29 and r.max_row<=40)
protected=locked(s2)
for c,s in {
'E26':'Doce módulos: acceso, usuarios, clientes, costos, cotizaciones, pedidos, productos, producción, inventario, pagos/cobranza, transporte/entregas y reportes. Catálogo explícito de cortes y derivados; cada orden registra resultados por producto/lote y pesajes manuales. Venta de carne y derivados; servicio de faeneo/corte separado cuando se presta.',
'E37':'Cotización aceptada antes del pedido. Producto del catálogo no crea stock; previsión tampoco. Resultado identifica corte/derivado, lote y cantidad real. Almacén confirma pesaje y entrada física posterior. Disponible = físico apto menos reservas. Rechazo sanitario bloquea. Entrega/deuda separadas. Offline solo recepción Android asignada/descargada. RF09/RF16/RF21 diferidos; RF11 condicional.',
'H57':'Plan iterativo de cuatro sprints, fechas/estimaciones por acordar. ASA1: 21 RF y 6 RNF, agrupados en doce casos generales. El CRUD es interno a cada módulo. Web y Android comparten API. Pruebas de recepción offline, duplicados y conflictos. RF09/RF16/RF21 fuera de alcance; fiscal condicionado.',
'I60':'Acceso y registro de comprador; administración de usuarios, clientes, catálogo de cortes/derivados, productos, costos, cotizaciones y pedidos. Datos centrales y base técnica Android. RF01/02/03/10/12/13 y parametrización RF04.',
'S60':'Todos se autentican; alta pública solo comprador. Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar historial.',
'I65':'Producción, catálogo parametrizado, inventario/reservas, sanidad y frío. Cada faeneo obtiene varios cortes por lote; fabricación identifica derivado e insumos reales. Almacén registra pesajes manuales y entrada física única. RF04/17/18/20; RNF03/06.',
'S65':'Una orden produce costilla y lomo en lotes distintos. Confirmar peso no suma stock; entrada física sí. Rechazo bloquea; consumo de derivado rechazado no se revierte por ficción. No se reservan previsiones.',
'I70':'Pagos, crédito, transportes, rutas y entregas. Android Kotlin: captura de recepción autorizada/descargada, evidencia y sincronización. RF05/06/07/08/19; RNF01/05.',
'I75':'Reportes por perfil con filtros y exportación PDF/Excel, portal comprador, constancias e integración fiscal condicional. RF11/14/15. Integración y pruebas finales.',
'S75':'Comprador consulta/exporta solo sus datos. Reportes no modifican operaciones. Constancia solo tras recepción conforme central. Emisión fiscal confirmada conserva referencia única.'}.items():s1[c]=s
# Preserve the versioning block exactly; use only its preceding actor area.
styles={k:copy(s2[k]._style)for k in ['A13','D13','K13']}
for r in list(s2.merged_cells.ranges):
 if r.min_row>=13 and r.max_row<=27:s2.unmerge_cells(str(r))
for row in s2.iter_rows(min_row=13,max_row=27):
 for c in row:c.value=None
actors=[('ACT-01','Propietario / administración','Usuarios, permisos, catálogo de cortes/derivados, costos y reportes.'),('ACT-02','Ventas / cobranza','Clientes, cotizaciones, pedidos, pagos, crédito y seguimiento de deuda.'),('ACT-03','Producción','Animales, sanidad, órdenes y resultados de cortes/derivados por lote.'),('ACT-04','Almacén','Pesajes manuales: bruto, tara, neto, producto/lote; entradas, stock y reservas.'),('ACT-05','Responsable de entrega','Transportes, rutas, frío y recepción. Android: descarga previa y envío validado.'),('ACT-06','Comprador','Cuenta autenticada; catálogo, cotizaciones, pedidos y reportes propios.'),('EXT-01','Proveedor fiscal externo','Integración condicional. Balanza: herramienta física sin conexión automática.')]
for i,(id,n,desc)in enumerate(actors):
 row=13+2*i;end=row+1 if i<6 else 27
 for col,last,key,val in [('A','C','A13',id),('D','J','D13',n),('K','AB','K13',desc)]:
  c=s2[f'{col}{row}'];c.value=val;c._style=copy(styles[key]);c.alignment=Alignment(horizontal='left',vertical='center',wrap_text=True);thin=Side(style='thin',color='000000');c.border=Border(left=thin,right=thin,top=thin,bottom=thin);s2.merge_cells(f'{col}{row}:{last}{end}')
 for rr in range(row,end+1):s2.row_dimensions[rr].height=25
updates=json.loads((T/'Requisitos_actualizados.json').read_text());rf=updates['rf'];criteria=updates['criterios']
from zipfile import ZipFile
from lxml import etree as E
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
asa=E.fromstring(ZipFile(T/'Documentos'/'ASA1 - Especificacion de Requerimientos - CRM Chancheria.docx').read('word/document.xml')).find('w:body',ns)
text=lambda e:''.join(e.xpath('.//w:t/text()',namespaces=ns))
for idx in [164,169]:
 for row in asa[idx].findall('w:tr',ns)[1:]:
  values=[text(c)for c in row.findall('w:tc',ns)];rf[values[0]]=(values[1],values[2],values[5])
priorities={}
for row in asa[222].findall('w:tr',ns)[1:]:
 values=[text(c)for c in row.findall('w:tc',ns)];criteria[values[0]]=values[5];priorities[values[0]]={'M':'Must','S':'Should','C':'Could','W':'Won’t have'}[values[3]]
for row in s2.iter_rows():
 id=str(row[0].value or '').strip()
 if id in rf:
  n=row[0].row;s2[f'D{n}']=rf[id][0];s2[f'I{n}']=rf[id][1];s2[f'{"V"if 89<=n<=94 else "R"if n<100 else "Q"}{n}']=criteria[id]
  if n>=100:s2[f'X{n}']=priorities[id]
 if id=='RF-17':
  n=row[0].row;s2[f'I{n}']='Registro manual de frío de conservación/transporte: temperatura, unidad, fecha, lote/ubicación/entrega y responsable; evaluación humana. No mide temperatura corporal de cerdos ni diagnostica. No se aplican umbrales o alertas automáticos sin validación. Requiere conexión.'
for sh in w:
 for row in sh:
  for c in row:
   if sh is s2 and 29<=c.row<=40:continue
   if isinstance(c.value,str):c.value=c.value.replace('UML V4','UML de doce casos generales').replace('modelo V4','modelo vigente').replace('CU21','CU11').replace('CU26','CU12');c.alignment=Alignment(horizontal=c.alignment.horizontal or 'left',vertical='center',wrap_text=True)
# Taller narrative rows need room. These are outside the preserved versioning section.
for row in s2.iter_rows():
 id=str(row[0].value or '').strip();n=row[0].row
 if id in rf:
  desc=str(s2[f'I{n}'].value);criterion=criteria[id];chars=52 if 89<=n<=94 else 35
  s2.row_dimensions[n].height=max(s2.row_dimensions[n].height or 20,min(400,30+max(math.ceil(len(desc)/chars),math.ceil(len(criterion)/28))*15))
for n in [26,37,57,60,65,70,75]:s1.row_dimensions[n].height=max(s1.row_dimensions[n].height or 20,50)
assert locked(s2)==protected
out=T/'Documentos'/'Formato Proyecto - SGCC Actualizado.xlsx';w.save(out)
r=load_workbook(out);assert locked(r.worksheets[1])==protected
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
(T/'Validacion_Excel.json').write_text(json.dumps({'originalConservado':before,'bloqueVersionamientoConservado':True,'actoresHumanos':6,'nuevoArchivo':out.name},indent=2))
print(out.name,'original intacto; versionamiento sin cambios; seis actores + proveedor externo.')
