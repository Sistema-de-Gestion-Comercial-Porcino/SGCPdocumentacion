from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import sys,json,subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).parent/'.deps/python'))
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START,WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];TMP=Path('/tmp/sgcp_patrones_20261105');SPECS=json.loads(Path(__file__).with_name('especificacion.json').read_text());manifest=json.loads((TMP/'manifest.json').read_text())
source=ROOT/'02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales/Patrones_Creacionales_SGCC.docx'
with ZipFile(source)as z:
 ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
 body=etree.fromstring(z.read('word/document.xml')).find('w:body',ns);rels=etree.fromstring(z.read('word/_rels/document.xml.rels'))
 for el in list(body)[:27]:
  for rid in el.xpath('.//a:blip/@r:embed',namespaces=ns):
   target=next(r.get('Target')for r in rels if r.get('Id')==rid);logo=TMP/('logo'+Path(target).suffix);logo.write_bytes(z.read('word/'+target))
def render(item):subprocess.run(['pdftoppm','-singlefile','-scale-to','3600','-png',item['pdf'],item['png'][:-4]],check=True)
with ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(render,manifest))
for cat in ['estructurales','comportamiento']:
 pats=[p for p in SPECS if p['category']==cat];items=[p for p in manifest if p['category']==cat];selected=[p for p in pats if p['apply']]
 label='estructurales'if cat=='estructurales'else'de comportamiento';base='Estructurales'if cat=='estructurales'else'Comportamiento';out=Path(items[0]['png']).parent.parent
 doc=Document();pending=False;table_n=0
 for name in ['Normal','Title','Heading 1','Heading 2','Heading 3','Header','Footer']:
  st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(12);st.font.color.rgb=RGBColor(0,0,0);st.font.bold=name in ['Title','Heading 1','Heading 2','Heading 3']
  fonts=st.element.get_or_add_rPr().find(qn('w:rFonts'))
  for k in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:fonts.attrib.pop(qn('w:'+k),None)
  f=st.paragraph_format;f.space_before=f.space_after=Pt(0);f.line_spacing=2;f.first_line_indent=Inches(.5);f.widow_control=True
  if name!='Normal':f.first_line_indent=Inches(0)
  if name in ['Title','Heading 1']:f.alignment=WD_ALIGN_PARAGRAPH.CENTER
  if name.startswith('Heading'):f.keep_with_next=True;f.keep_together=True
 lang=OxmlElement('w:lang');lang.set(qn('w:val'),'es-BO');doc.styles['Normal'].element.get_or_add_rPr().append(lang)
 def section(s,land=False):
  s.page_width=Inches(11 if land else 8.5);s.page_height=Inches(8.5 if land else 11);s.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
  s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Inches(1);s.header_distance=s.footer_distance=Inches(.5)
  s.header.is_linked_to_previous=False;q=s.header.paragraphs[0];q.alignment=WD_ALIGN_PARAGRAPH.RIGHT;q.paragraph_format.line_spacing=1
  fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');r=OxmlElement('w:r');t=OxmlElement('w:t');t.text='1';r.append(t);fld.append(r);q._p.append(fld)
 def apply_page(q):
  global pending
  if pending:q.paragraph_format.page_break_before=True;pending=False
  return q
 def p(s='',indent=True,bold=False,italic=False):
  q=apply_page(doc.add_paragraph());q.paragraph_format.first_line_indent=Inches(.5 if indent else 0);r=q.add_run(s);r.bold=bold;r.italic=italic;return q
 def h(s,level=1):return apply_page(doc.add_heading(s,level))
 def newpage():
  global pending
  pending=True
 def newsection(land=False):
  s=doc.add_section(WD_SECTION_START.NEW_PAGE);q=doc.paragraphs[-1];q.paragraph_format.line_spacing=Pt(1);q.paragraph_format.space_before=q.paragraph_format.space_after=Pt(0);q.add_run().font.size=Pt(1);section(s,land)
 def caption(kind,n,title):
  q=p(f'{kind} {n}',False,True);q.paragraph_format.keep_with_next=True;q=p(title,False,False,True);q.paragraph_format.keep_with_next=True
 def note(s):
  q=p('',False);q.add_run('Nota. ').italic=True;q.add_run(s)
 def table(title,headers,rows,widths):
  global table_n
  table_n+=1;caption('Tabla',table_n,title);t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
  for c,w in zip(t.columns,widths):c.width=Inches(w)
  borders=OxmlElement('w:tblBorders')
  for edge in ['top','bottom','left','right','insideH','insideV']:
   e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single'if edge in ['top','bottom']else'nil');e.set(qn('w:sz'),'6');borders.append(e)
  t._tbl.tblPr.append(borders)
  for ri,vals in enumerate([headers]+rows):
   row=t.rows[0]if ri==0 else t.add_row();pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
   if ri==0:pr.append(OxmlElement('w:tblHeader'))
   for ci,(c,text)in enumerate(zip(row.cells,vals)):
    c.width=Inches(widths[ci]);c.text=str(text)
    if ri==0:
     bs=OxmlElement('w:tcBorders');e=OxmlElement('w:bottom');e.set(qn('w:val'),'single');e.set(qn('w:sz'),'6');bs.append(e);c._tc.get_or_add_tcPr().append(bs)
    for q in c.paragraphs:
     q.paragraph_format.first_line_indent=Inches(0);q.paragraph_format.line_spacing=1;q.paragraph_format.space_before=q.paragraph_format.space_after=Pt(3);q.paragraph_format.keep_with_next=(ri==0)
     for r in q.runs:r.font.size=Pt(12);r.bold=ri==0
  return t
 section(doc.sections[0]);title=f'Patrones {label} para el CRM de la chanchería'
 q=p(title,False,True);q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.line_spacing=1.15;q.paragraph_format.space_before=Pt(18);q.paragraph_format.space_after=Pt(14)
 for r in q.runs:r.font.size=Pt(18)
 q=p('',False);q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.line_spacing=1;q.paragraph_format.space_after=Pt(18);q.add_run().add_picture(str(logo),width=Inches(4.25))
 for s,bold in [('Estudiantes:',True),('Dario Haziel Tambo Parra',False),('Angel Sebastian Eguez Mur',False),('Sofia Cuellar Roca',False),('Victor Manuel Manrique Arancivia',False),('Materia:',True),('Ingeniería de Software',False),('Docente:',True),('Rolando Lara Sánchez',False),('Fecha:',True),('5 de noviembre de 2026',False)]:
  q=p(s,False,bold);q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.line_spacing=1
 # A bookmark lets LibreOffice insert a real, updatable table of contents.
 newpage();q=p('',False);start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),'501');start.set(qn('w:name'),'indice');end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),'501');q._p.append(start);q._p.append(end)
 newpage();h('1. Introducción')
 p(f'El Sistema de Gestión Comercial Porcino (SGCP), denominado SGCC en los modelos anteriores, mantiene el alcance del CRM de la chanchería. Este documento analiza los patrones {label}, selecciona los que resuelven necesidades presentes y explica los demás mediante ejemplos externos. Las reglas comerciales y los doce casos de uso se conservan (Tambo Parra et al., 2026).')
 p('El trabajo sigue la presentación del documento de patrones creacionales revisado por el equipo: portada institucional, índice, apartados numerados, cuerpo con citas autor–año y figuras horizontales. Los ejemplos y diagramas de clases son elaboración propia; no constituyen evidencia de una aplicación terminada.')
 h('2. Identificación y clasificación')
 p(('Los patrones estructurales organizan relaciones entre clases y objetos. Se revisan los siete del catálogo GoF (Gamma et al., 1995).'if cat=='estructurales'else'Los patrones de comportamiento organizan algoritmos, comunicación y responsabilidades. Se revisan once del catálogo GoF. Refactoring Guru desarrolla diez en su catálogo principal; Interpreter se incluye con apoyo en la clasificación original (Gamma et al., 1995).'))
 p('La Tabla 1 distingue las decisiones de diseño de los ejemplos de aprendizaje. Un patrón presente en una biblioteca no exige volver a programarlo dentro del proyecto.')
 table('Patrones evaluados y decisión para el sistema',['Patrón','Propósito','Decisión'],[[x['name'],x['intent'],('Aplicar: '+x['scope'])if x['apply']else('Ejemplo externo; iteradores de biblioteca permitidos.'if x['name']=='Iterator'else'Ejemplo externo; sin implementación propia en el CRM.')]for x in pats],[1.25,2.8,2.45])
 h('3. Escenarios y distribución entre repositorios')
 p('La organización de GitHub se llama Sistema de Gestion Comercial Porcino. Tres repositorios separan los productos de software; esta separación no convierte al backend en microservicios. Ambos frontends consumen la misma API y nunca acceden directamente a la base central.')
 table('Responsabilidad de cada repositorio',['Repositorio','Responsabilidad'],[['SGCPapi','API, autorización, reglas comerciales, transacciones, persistencia central y reportes.'],['SGCPuiweb','Web responsiva para gestión y portal del comprador. Todas sus operaciones requieren conexión.'],['SGCPuimovil','Android nativo en Kotlin para reparto. Room/SQLite guarda únicamente recepciones autorizadas y descargadas pendientes de sincronizar.']],[1.6,4.9])
 p('Se seleccionan '+', '.join(x['name']for x in selected)+'. La selección responde a variaciones ya identificadas. No se añaden sensores, alertas comerciales, optimización de rutas, pasarelas de pago ni lenguajes de reglas configurables. La tecnología concreta de API y web se definirá al implementar.')
 p('El contrato de la API debe fijar DTO, permisos, errores, versiones e idempotencia. Android conserva clave, versión base y evidencia; el servidor vuelve a validar. La captura local no actualiza por sí sola la entrega central, el inventario o la deuda.')
 h('4. Aplicación de patrones y ejemplos de uso')
 ordered=sorted([x for x in pats if x['name']!='Interpreter'],key=lambda x:x['name']);letters={x['name']:chr(97+i)for i,x in enumerate(ordered)}
 for i,x in enumerate(pats,1):
  h(x['name']+(' aplicado al sistema'if x['apply']else': ejemplo externo'),2)
  cite='Gamma et al., 1995'if x['name']=='Interpreter'else'Refactoring Guru, s. f.-'+letters[x['name']]
  p(x['intent']+' ('+cite+'). '+x['reason'])
  p(x['scenario']+' '+x['flow'])
  p(x['caution']+f' La Figura {i} muestra los participantes y relaciones; '+('su ubicación es '+x['scope']+'.'if x['apply']else'el ejemplo no añade funciones al SGCP.'))
 h('5. Diagramas UML')
 p('Los diagramas siguientes están contenidos en un único MDJ de esta categoría, separados entre aplicación al sistema y ejemplos externos. Cada uno tiene un icono propio en StarUML. Los triángulos vacíos representan herencia o realización de interfaz; la línea discontinua distingue la realización. Los rombos negros señalan composición y los números indican multiplicidades. Las clases técnicas no representan necesariamente nuevas tablas.')
 newsection(True)
 for i,(x,item)in enumerate(zip(pats,items),1):
  if i>1:newpage()
  caption('Figura',i,x['name']+(' aplicado al SGCP'if x['apply']else': ejemplo externo'))
  im=Image.open(item['png']);w,ht=im.size;width=min(9.0,5.25*w/ht)
  q=p('',False);q.paragraph_format.line_spacing=1;q.paragraph_format.keep_with_next=True;shape=q.add_run().add_picture(item['png'],width=Inches(width));shape._inline.docPr.set('descr',x['scenario'])
  note('Elaboración propia. '+(x['scope']+'.'if x['apply']else x['scope']+'.'))
 newsection(False);h('6. Comparación de patrones')
 p('La comparación es cualitativa. No se midió rendimiento de producción y no se atribuye a un patrón un porcentaje de mejora. El tamaño de los datos, la red, la biblioteca y la base de datos pueden dominar el costo real.')
 table('Eficiencia y mantenibilidad',['Patrón','Evaluación'],[[x['name'],x['efficiency']]for x in pats],[1.5,5.0])
 p(('Adapter cambia el contrato visible; Facade simplifica el acceso a varios colaboradores. Proxy conserva el contrato y controla acceso o carga; Decorator conserva el contrato y añade responsabilidades. Composite requiere recursión de hojas y grupos; una asociación de uno a muchos no basta.'if cat=='estructurales'else'State responde al estado del objeto; Strategy elige una regla intercambiable. Command representa una operación pendiente y no garantiza idempotencia por sí solo. Observer distribuye cambios a suscriptores y Mediator coordina colaboradores. Memento restaura memoria de un objeto, no corrige automáticamente operaciones comerciales persistidas.'))
 h('7. Mejores prácticas')
 practices=[('Alcance antes que catálogo','Mantener los doce casos de uso y sus reglas. Los patrones son decisiones de implementación, no requisitos nuevos ni un patrón obligatorio por pantalla.'),('Autoridad de la API','Validar sesión, permisos, pertenencia, versión y reglas en el servidor. Los clientes pueden ayudar al usuario a corregir datos, pero no sustituyen esa validación.'),('Operaciones coherentes','Guardar efectos relacionados en una transacción; usar restricciones únicas y claves de idempotencia con huella del contenido. Una consulta previa no elimina carreras entre solicitudes.'),('Dependencias explícitas','Inyectar contratos para sustituir bibliotecas y probar colaboradores. Compartir Room por proceso no implica almacenar usuario, saldo o pedido en un estado global.'),('Pruebas y cambios graduales','Probar rechazos, reintentos, estados terminales, errores externos y las variantes autorizadas. Medir antes de introducir cachés o nuevas jerarquías; conservar una solución simple cuando no haya variación real.')]
 for title2,text in practices:h(title2,2);p(text)
 h('8. Casos de estudio y evaluación')
 for x in selected:
  h(x['name']+' en '+x['scope'].split(' · ')[0],2)
  cases={
  'Adapter':('Reporte de costilla y lomo con un nombre que contiene caracteres de HTML.','El adaptador conserva las filas recibidas y escapa el contenido antes de entregarlo al motor de prueba. La generación real del PDF queda fuera de este prototipo.'),
  'Facade':('La misma recepción se reenvía porque el teléfono no recibió la respuesta.','Se devuelve el resultado previo sin incrementar otra vez la versión. Una clave con otro contenido o una asignación inválida se rechaza. El prototipo es secuencial; las garantías concurrentes deben implementarse en la base real.'),
  'Command':('Una captura autorizada se almacena y se envía al volver la señal.','La operación lleva su misma clave y datos durante los reintentos. En la prueba, dos ejecuciones obtienen el mismo resultado; no se simulan Room ni transporte HTTP reales.'),
  'State':('Se pierde la conexión durante el envío y después aparece un conflicto.','El fallo de red retorna a Pendiente. Conflicto impide el reenvío automático; solo un descarte autorizado alcanza Descartada. Confirmada y Descartada rechazan nuevos envíos.'),
  'Strategy':('Un pedido al contado conserva saldo; otro tiene crédito autorizado y fecha acordada.','La política contado bloquea el primero; la de crédito permite la condición comercial del segundo conservando deuda. En ambos casos sigue siendo obligatoria la aptitud del producto y la preparación.')}
  a,b=cases[x['name']];p(a+' '+b)
 count=6 if cat=='estructurales'else 8
 p(f'Se ejecutaron {count} comprobaciones de esta categoría, todas correctas, dentro de un prototipo didáctico de 14 comprobaciones. La evidencia está en 99_Herramientas/patrones_20261105/prototipo.py. No se probó una aplicación completa, concurrencia, persistencia real, red ni codificación PDF. Los beneficios de mantenibilidad descritos son expectativas del diseño, no métricas observadas en producción.')
 h('9. Conclusión')
 p('Se proponen '+', '.join(x['name']for x in selected)+' para necesidades concretas del SGCP. Los demás patrones se explican con ejemplos independientes. El diseño conserva la API como autoridad común de la web y Android, la recepción offline limitada y la separación entre entrega, existencias y deuda.')
 p(f'El archivo Patrones_{base}_SGCP.mdj contiene {len(pats)} diagramas editables: {len(selected)} del sistema y {len(pats)-len(selected)} ejemplos. Los nombres SGCPapi, SGCPuiweb y SGCPuimovil corresponden a carpetas locales vacías preparadas para los futuros repositorios; no se afirma haber publicado código en GitHub.')
 newpage();h('10. Referencias')
 def ref(before,title,after='',url=None):
  q=p('',False);q.paragraph_format.left_indent=Inches(.5);q.paragraph_format.first_line_indent=Inches(-.5);q.add_run(before);q.add_run(title).italic=True;q.add_run(after)
  if url:
   q.add_run(' ');hl=OxmlElement('w:hyperlink');hl.set(qn('r:id'),q.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=url;r.append(t);hl.append(r);q._p.append(hl)
 ref('Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1995). ','Design patterns: Elements of reusable object-oriented software','. Addison-Wesley.')
 for x in ordered:ref('Refactoring Guru. (s. f.-'+letters[x['name']]+'). ',x['name']+'.',url=x['source'].replace('/design-patterns/memento','/es/design-patterns/memento'))
 ref('Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026). ','Especificación de requerimientos: CRM de ventas para una chanchería',' [Trabajo académico no publicado]. Universidad del Valle.')
 doc.core_properties.title=f'Patrones {label} para el SGCP';doc.core_properties.author='Dario Haziel Tambo Parra; Angel Sebastian Eguez Mur; Sofia Cuellar Roca; Victor Manuel Manrique Arancivia';doc.core_properties.language='es-BO'
 fn=out/f'Patrones_{base}_SGCP.docx';doc.save(fn);print(fn)
