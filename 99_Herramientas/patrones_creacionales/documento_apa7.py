"""Maquetación APA 7 del contenido aprobado; no altera los diagramas MDJ."""
from pathlib import Path
from copy import deepcopy
import ast, re, sys, json, hashlib
sys.path.insert(0,'/tmp/sgcc_patrones_20261103/libs')
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales'
TMP=Path('/tmp/sgcc_patrones_apa7');TMP.mkdir(exist_ok=True)
# Extract the approved prose and tables instead of rewriting the analysis.
tree=ast.parse(Path(__file__).with_name('documento.py').read_text())
sections={};current=None;patterns=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='patterns'for t in node.targets):patterns=ast.literal_eval(node.value)
 if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name):
  c=node.value;kind=c.func.id
  if kind not in ('h','p','page','table','bullet'):continue
  try:args=[ast.literal_eval(a)for a in c.args]
  except(ValueError,TypeError):continue
  if kind in ('h','page')and args and re.match(r'^\d+\. ',args[0]):
   current=int(args[0].split('.')[0]);sections[current]=[];continue
  if current is not None:sections[current].append((kind,args))
 if isinstance(node,ast.For)and isinstance(node.iter,ast.List)and isinstance(node.target,ast.Tuple) and [x.id for x in node.target.elts]==['title','body']:
  for title,body in ast.literal_eval(node.iter):sections[current]+=[('h',[title,2]),('p',[body])]
assert set(sections)=={1,2,8,9,10,11} and len(patterns)==5
D=Document();FONT='Times New Roman';SZ=12
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption','List Bullet','Header','Footer']:
 st=D.styles[name];st.font.name=FONT;st.font.size=Pt(SZ);st.font.color.rgb=RGBColor(0,0,0)
 fonts=st.element.get_or_add_rPr().find(qn('w:rFonts'))
 for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
  fonts.attrib.pop(qn('w:'+key),None)
 pf=st.paragraph_format;pf.space_before=Pt(0);pf.space_after=Pt(0);pf.line_spacing=2;pf.widow_control=True
 pf.left_indent=Inches(0);pf.right_indent=Inches(0);pf.first_line_indent=Inches(.5);pf.alignment=WD_ALIGN_PARAGRAPH.LEFT
 st.font.bold=False;st.font.italic=False
 if name in ['Heading 1','Heading 2','Heading 3','Title']:
  st.font.bold=True;pf.first_line_indent=Inches(0);pf.keep_with_next=True;pf.keep_together=True
  pf.alignment=WD_ALIGN_PARAGRAPH.CENTER if name in ['Heading 1','Title']else WD_ALIGN_PARAGRAPH.LEFT
 if name=='Heading 3':st.font.italic=True
for name in ['Header','Footer','Caption']:
 D.styles[name].paragraph_format.first_line_indent=Inches(0)
# Explicit Spanish language, black text, letter paper and one-inch margins.
lang=OxmlElement('w:lang');lang.set(qn('w:val'),'es-BO');D.styles['Normal'].element.get_or_add_rPr().append(lang)
def setup_section(s,landscape=False):
 s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
 s.page_width=Inches(11 if landscape else 8.5);s.page_height=Inches(8.5 if landscape else 11)
 s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Inches(1)
 s.header_distance=s.footer_distance=Inches(.5)
 # Each header is right-aligned to its own section width; numbering stays continuous.
 s.header.is_linked_to_previous=False
 hp=s.header.paragraphs[0];hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT;hp.paragraph_format.first_line_indent=Inches(0)
 hp.paragraph_format.line_spacing=1
 field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');run=OxmlElement('w:r');t=OxmlElement('w:t');t.text='1';run.append(t);field.append(run);hp._p.append(field)
 s.footer.paragraphs[0].text=''
setup_section(D.sections[0])
D.core_properties.title='Patrones creacionales para el CRM de la chanchería'
D.core_properties.subject='Selección de patrones creacionales para SGCC; formato APA 7'
D.core_properties.author='Dario Haziel Tambo Parra; Angel Sebastian Eguez Mur; Sofia Cuellar Roca; Victor Manuel Manrique Arancivia'
D.core_properties.language='es-BO'
def clean(s):return s.replace(' [1]',' (Gamma et al., 1995)').replace(' [2]',' (Oracle, s. f.)')
pending_page=False
def apply_page(q):
 global pending_page
 if pending_page:q.paragraph_format.page_break_before=True;pending_page=False
 return q
def para(s='',bold=False,italic=False,indent=True,center=False):
 q=apply_page(D.add_paragraph());q.paragraph_format.first_line_indent=Inches(.5 if indent else 0)
 if center:q.alignment=WD_ALIGN_PARAGRAPH.CENTER
 r=q.add_run(clean(s));r.bold=bold;r.italic=italic
 return q
def heading(s,level=1):return apply_page(D.add_heading(s,level))
def fresh_section(landscape=False):
 s=D.add_section(WD_SECTION_START.NEW_PAGE)
 q=D.paragraphs[-1];q.paragraph_format.first_line_indent=Inches(0);q.paragraph_format.line_spacing=Pt(1)
 q.paragraph_format.space_before=q.paragraph_format.space_after=Pt(0);q.paragraph_format.keep_with_next=False
 q.add_run().font.size=Pt(1)
 setup_section(s,landscape);return s
def pagebreak():
 global pending_page
 pending_page=True
def note(s):
 q=para('',indent=False);q.add_run('Nota. ').italic=True;q.add_run(s);return q
def caption(kind,n,title):
 q=para(f'{kind} {n}',bold=True,indent=False);q.paragraph_format.keep_with_next=True
 q=para(title,italic=True,indent=False);q.paragraph_format.keep_with_next=True
 return q
TABLES=[
('Clasificación y selección de patrones creacionales',[1.15,2.45,2.9], 'Clasificación basada en Gamma et al. (1995); selección elaborada para el SGCC.'),
('Evaluación de escenarios del SGCC',[2.10,2.55,1.85], None),
('Comparación de eficiencia, mantenibilidad y aplicabilidad',[1.12,2.13,3.25], 'La evaluación es cualitativa y no representa mediciones de rendimiento del sistema.'),
('Resultados del prototipo didáctico',[4.50,.75,1.25], 'Las comprobaciones corresponden al prototipo aislado, no a una implementación completa de SGCC.'),
('Diagramas incluidos en el archivo MDJ',[1.75,4.75], None)]
table_no=0
def table(headers,rows):
 global table_no
 title,widths,nt=TABLES[table_no];table_no+=1
 para(f'La Tabla {table_no} presenta '+{1:'los cinco patrones y su selección para el proyecto.',2:'los escenarios utilizados para evaluar su aplicabilidad.',3:'la comparación de las alternativas.',4:'los resultados de las comprobaciones ejecutadas.',5:'la organización del proyecto de StarUML.'}[table_no])
 caption('Tabla',table_no,title)
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False;t.style='Normal Table'
 for col,w in zip(t.columns,widths):col.width=Inches(w)
 pr=t._tbl.tblPr
 borders=OxmlElement('w:tblBorders')
 for edge in ['top','bottom','left','right','insideH','insideV']:
  e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single'if edge in ('top','bottom')else'nil');e.set(qn('w:sz'),'6');e.set(qn('w:color'),'000000');borders.append(e)
 pr.append(borders)
 margin=OxmlElement('w:tblCellMar')
 for name,val in [('top','50'),('bottom','50'),('left','90'),('right','90')]:
  e=OxmlElement('w:'+name);e.set(qn('w:w'),val);e.set(qn('w:type'),'dxa');margin.append(e)
 pr.append(margin)
 allrows=[headers]+rows
 for ri,vals in enumerate(allrows):
  row=t.rows[0]if ri==0 else t.add_row();rowpr=row._tr.get_or_add_trPr();rowpr.append(OxmlElement('w:cantSplit'))
  if ri==0:rowpr.append(OxmlElement('w:tblHeader'))
  for ci,(cell,value)in enumerate(zip(row.cells,vals)):
   cell.width=Inches(widths[ci]);cell.text=clean(value)
   if ri==0:
    bs=OxmlElement('w:tcBorders');e=OxmlElement('w:bottom');e.set(qn('w:val'),'single');e.set(qn('w:sz'),'6');bs.append(e);cell._tc.get_or_add_tcPr().append(bs)
   for q in cell.paragraphs:
    q.paragraph_format.first_line_indent=Inches(0);q.paragraph_format.line_spacing=1;q.paragraph_format.keep_with_next=(ri<len(allrows)-1);q.paragraph_format.keep_together=True
    for r in q.runs:r.font.name=FONT;r.font.size=Pt(SZ);r.bold=(ri==0)
 if nt:note(nt)
 return t

def emit(events):
 for kind,args in events:
  if kind=='h':heading(*args)
  elif kind in ('p','bullet'):para(args[0])
  elif kind=='table':table(args[0],args[1])

# Student title page. Names and affiliation match the project's ASA1.
for _ in range(3):para('',indent=False,center=True)
title='Patrones creacionales para el CRM de la chanchería'
para(title,bold=True,indent=False,center=True)
para('',indent=False,center=True)
para('Dario Haziel Tambo Parra, Angel Sebastian Eguez Mur,\nSofia Cuellar Roca y Victor Manuel Manrique Arancivia',indent=False,center=True)
para('Universidad del Valle',indent=False,center=True)
para('Ingeniería de Software',indent=False,center=True)
para('Rolando Lara Sánchez',indent=False,center=True)
para('3 de noviembre de 2026',indent=False,center=True)
pagebreak()
heading(title)
para('El Sistema de Gestión Comercial y Clientes (SGCC) es el CRM de la chanchería descrito en la especificación de requerimientos del equipo (Tambo Parra et al., 2026). Este análisis conserva sus casos de uso y reglas comerciales, y selecciona patrones creacionales para el diseño de su implementación.')
heading('Identificación y clasificación de patrones creacionales')
emit(sections[1])
heading('Evaluación de escenarios del CRM')
emit(sections[2])
heading('Aplicación de los patrones y ejemplos de uso')
for i,(name,img,a,b) in enumerate(patterns,1):
 heading(re.sub(r'^\d+\. ','',name),2)
 para(a);para(b)
 if i==5:
  para('La exclusión se refiere a una clase Singleton manual con acceso global al negocio. No excluye compartir una dependencia de infraestructura: Android recomienda una instancia de Room por proceso, y Hilt permite administrarla con alcance @Singleton (Google, 2026a, 2026b). La inyección de dependencias y el alcance singleton son compatibles. Esta posibilidad no agrega un tercer patrón manual a los diagramas seleccionados para el CRM.')
  para('En Kotlin, una declaración object ofrece una instancia cuya inicialización es segura entre hilos y ocurre al primer acceso (JetBrains, 2026). Esa garantía no vuelve seguras automáticamente todas las operaciones sobre su estado mutable.')
 para(f'La Figura {i} representa las clases y relaciones de este escenario.')
# Diagrams remain on landscape pages, with APA figure number, title and note.
fresh_section(True)
for i,(name,img,a,b)in enumerate(patterns,1):
 if i>1:pagebreak()
 caption('Figura',i,re.sub(r'^\d+\. ','',name))
 image_path=TMP/'figuras'/img
 im=Image.open(image_path);w,h=im.size
 width=min(9.0,5.20*w/h)
 q=para('',indent=False);q.paragraph_format.line_spacing=1;q.paragraph_format.keep_with_next=True
 shape=q.add_run().add_picture(str(image_path),width=Inches(width))
 shape._inline.docPr.set('descr',re.sub(r'^\d+\. ','',name)+'; diagrama de clases UML editable en el archivo MDJ adjunto.')
 note('Elaboración propia. '+('Aplicación propuesta para el SGCC.'if i<=2 else'Ejemplo externo al SGCC.'))
fresh_section(False)
heading('Comparación de los patrones');emit(sections[8])
heading('Mejores prácticas de implementación');emit(sections[9])
heading('Casos de estudio y evaluación');emit(sections[10])
heading('Decisión final')
# Keep all final content up to the old numbered reference list.
end=[]
for ev in sections[11]:
 if ev[0]=='h'and ev[1][0]=='Fuentes':break
 end.append(ev)
emit(end)
# APA author-date references, alphabetical order and hanging indent.
pagebreak();heading('Referencias')
def reference(before,title,after='',url=None):
 q=para('',indent=False);q.paragraph_format.left_indent=Inches(.5);q.paragraph_format.first_line_indent=Inches(-.5)
 q.add_run(before);q.add_run(title).italic=True;q.add_run(after)
 if url:
  q.add_run(' ');hl=OxmlElement('w:hyperlink');hl.set(qn('r:id'),q.part.relate_to(url,RT.HYPERLINK,is_external=True))
  r=OxmlElement('w:r');rp=OxmlElement('w:rPr');fonts=OxmlElement('w:rFonts');fonts.set(qn('w:ascii'),FONT);fonts.set(qn('w:hAnsi'),FONT);rp.append(fonts)
  sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');rp.append(sz);r.append(rp);text=OxmlElement('w:t');text.text=url;r.append(text);hl.append(r);q._p.append(hl)
reference('Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1995). ','Design patterns: Elements of reusable object-oriented software','. Addison-Wesley.')
reference('Google. (2026a, 23 de octubre). ','Save data in a local database using Room','. Android Developers.', 'https://developer.android.com/training/data-storage/room')
reference('Google. (2026b, 28 de octubre). ','Dependency injection with Hilt','. Android Developers.', 'https://developer.android.com/training/dependency-injection/hilt-android')
reference('JetBrains. (2026, 20 de octubre). ','Object declarations and expressions','. Kotlin.', 'https://kotlinlang.org/docs/object-declarations.html')
reference('Oracle. (s. f.). ','HttpRequest.Builder','. Java SE 25 & JDK 25.', 'https://docs.oracle.com/en/java/javase/25/docs/api/java.net.http/java/net/http/HttpRequest.Builder.html')
reference('Tambo Parra, D. H., Eguez Mur, A. S., Cuellar Roca, S., & Manrique Arancivia, V. M. (2026). ','Especificación de requerimientos: CRM de ventas para una chanchería',' [Trabajo académico no publicado]. Universidad del Valle.')
# Make field updates automatic when opened in Word.
settings=D.settings.element;upd=OxmlElement('w:updateFields');upd.set(qn('w:val'),'true');settings.append(upd)
file=OUT/'Patrones_Creacionales_SGCC.docx';D.save(file)
print(file)
(TMP/'control.json').write_text(json.dumps({'tablas':table_no,'figuras':len(patterns),'orientaciones':['vertical','horizontal','vertical'],'mdj_sha256':hashlib.sha256((OUT/'Patrones_Creacionales_SGCC.mdj').read_bytes()).hexdigest()},indent=2))
