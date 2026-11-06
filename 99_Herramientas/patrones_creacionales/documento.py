from pathlib import Path
import sys,json
sys.path.insert(0,'/tmp/sgcc_patrones_20261103/libs')
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.section import WD_SECTION_START,WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image
R=Path(__file__).resolve().parents[2];OUT=R/'02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales';d=Document()
normal=d.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(11);normal.font.color.rgb=RGBColor.from_string('253342');normal.paragraph_format.space_after=Pt(7)
normal.paragraph_format.line_spacing=1.08
for n,sz in [('Title',28),('Heading 1',20),('Heading 2',13)]:
 st=d.styles[n];st.font.name='Calibri';st.font.size=Pt(sz);st.font.color.rgb=RGBColor.from_string('173B4B');st.paragraph_format.space_before=Pt(8);st.paragraph_format.space_after=Pt(9)
for s in d.sections:
 s.page_width=Cm(21);s.page_height=Cm(29.7);s.top_margin=Cm(1.8);s.bottom_margin=Cm(1.6);s.left_margin=Cm(1.8);s.right_margin=Cm(1.8);s.header_distance=Cm(.6);s.footer_distance=Cm(.6)
header=d.sections[0].header.paragraphs[0];header.text='SGCC  /  INGENIERÍA DE SOFTWARE';header.style='Caption';header.runs[0].font.size=Pt(9)
f=d.sections[0].footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;f.add_run('Patrones creacionales · ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
d.core_properties.title='Patrones creacionales — SGCC';d.core_properties.subject='Selección y evaluación de patrones creacionales para el CRM de la chanchería';d.core_properties.author='Proyecto SGCC'
def p(text='',bold=False):
 q=d.add_paragraph();r=q.add_run(text);r.bold=bold;return q
def h(text,level=1):return d.add_heading(text,level)
def bullet(text):return d.add_paragraph(text,style='List Bullet')
def page(title):d.add_page_break();h(title)
def table(headers,rows,widths=None,size=10):
 t=d.add_table(rows=1,cols=len(headers));t.style='Light Shading Accent 1'
 for i,v in enumerate(headers):t.rows[0].cells[i].text=v
 prop=t.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');prop.append(repeat)
 for row in rows:
  cs=t.add_row().cells
  for c,v in zip(cs,row):c.text=v
 for row in t.rows:
  prop=row._tr.get_or_add_trPr();no=OxmlElement('w:cantSplit');prop.append(no)
  for i,c in enumerate(row.cells):
   if widths:c.width=Cm(widths[i])
   for pp in c.paragraphs:
    pp.paragraph_format.space_after=Pt(5);pp.paragraph_format.space_before=Pt(4);pp.paragraph_format.line_spacing=1.0
    for r in pp.runs:r.font.size=Pt(size)
 return t
def link(label,url):
 q=d.add_paragraph();el=OxmlElement('w:hyperlink');el.set(qn('r:id'),q.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'14617A');pr.append(c);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);el.append(r);q._p.append(el)
def newsection(landscape=False):
 s=d.add_section(WD_SECTION_START.NEW_PAGE);s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT;s.page_width=Cm(29.7 if landscape else 21);s.page_height=Cm(21 if landscape else 29.7);s.top_margin=Cm(1.25 if landscape else 1.8);s.bottom_margin=Cm(1.2 if landscape else 1.6);s.left_margin=Cm(1.4 if landscape else 1.8);s.right_margin=Cm(1.4 if landscape else 1.8);return s
h('Patrones creacionales\npara el CRM de la chanchería',0)
p('Sistema de Gestión Comercial y Clientes (SGCC)\nIngeniería de Software · 3 de noviembre de 2026')
h('1. Identificación y clasificación')
p('Se seleccionan Factory Method y Builder para la propuesta del SGCC. Abstract Factory, Prototype y Singleton se estudian con ejemplos externos: no se incorporan al CRM solo para completar la lista. La selección parte del modelo vigente de doce casos de uso y de las reglas del negocio.')
p('Los cinco pertenecen a la categoría creacional del catálogo GoF. Su finalidad es organizar cómo se crean objetos y qué dependencias intervienen. Factory Method se clasifica por alcance de clase; los otros cuatro, por alcance de objeto. Esta segunda clasificación señala el mecanismo predominante, no la ausencia de clases en el diseño [1].')
table(['Patrón','Qué decide o separa','Decisión para SGCC'],[
('Factory Method','Las subclases deciden qué producto concreto crear.','Aplicar en CU12: exportadores PDF y Excel.'),
('Abstract Factory','Una fábrica crea una familia de productos compatibles.','No incorporar ahora. Ejemplo: controles de un tema visual.'),
('Builder','Separa la construcción gradual de un objeto de su representación final.','Aplicar en CU06: pedido con varios detalles y condiciones.'),
('Prototype','Crea un objeto copiando una instancia que actúa como modelo.','No incorporar ahora. Ejemplo: duplicar una tarjeta de presentación.'),
('Singleton','Restringe una clase a una instancia y ofrece acceso compartido.','No incorporar como acceso global del CRM. Ejemplo: configuración de un visor.')],size=10)
p('El MDJ reúne cinco diagramas de clases: dos aplicados al sistema y tres ejemplos externos. Las clases de soporte propuestas no son nuevas tablas ni nuevos casos de uso. Son decisiones para la futura implementación; el informe no afirma que el CRM esté programado.',False)
page('2. Evaluación de escenarios del CRM')
p('El sistema gestiona clientes, productos, cortes y derivados, cotizaciones, pedidos, producción, inventario, pagos, transporte y reportes. La web y Android comparten reglas centrales; únicamente la recepción Android autorizada y descargada admite captura sin conexión.')
table(['Escenario observado','Evaluación','Decisión'],[
('CU12 permite exportar la misma consulta a PDF o Excel.','Varía la clase que codifica el archivo; el recorrido común de exportación puede mantenerse.','Factory Method. El servicio entrega datos ya autorizados.'),
('CU06 confirma pedidos con uno o varios productos, fecha y condición de pago.','Hay pasos de ensamblaje y condiciones que deben cumplirse antes de exponer el objeto terminado.','Builder fluido, nuevo por intento de confirmación.'),
('Existen una web y una app Android.','Son clientes con ciclos y tecnologías propios; no se han requerido familias intercambiables de objetos dentro del mismo cliente.','No justificar Abstract Factory solamente por tener dos plataformas.'),
('Un cliente vuelve a pedir productos similares.','Copiar un pedido completo podría arrastrar aceptación, precios, estados, pagos y reservas anteriores.','No usar Prototype en pedidos. Construir desde una cotización aceptada vigente.'),
('Android mantiene una base local y el servidor tiene recursos compartidos.','Se necesita administrar el ciclo de vida de dependencias. Eso no exige un punto global de acceso a todo el negocio.','Preferir inyección de dependencias. Singleton queda como ejemplo externo.')],size=10)
h('Criterio de selección',2)
p('Se adopta un patrón cuando resuelve una variación o una construcción que ya existe en el alcance. Para objetos simples basta un constructor. Una fábrica simple o un exportador inyectado serían alternativas más ligeras si el flujo no necesitara creadores especializados. Aquí Factory Method deja explícito el punto de extensión PDF/Excel sin trasladar decisiones de formato al servicio comercial.')
p('Builder se aplica en su variante fluida: PedidoBuilder reúne pasos encadenables y build() entrega el resultado válido. No se inventan varios tipos de pedido para dibujar más builders. ServicioConfirmarPedido cumple el papel de director y mantiene la autorización y la transacción fuera del constructor.')
# Five complete diagram sheets; each uses the native PNG of the unified MDJ.
newsection(True)
patterns=[
('3. Factory Method aplicado al CRM','01_Factory_Method_CRM.png',
 'Participantes: ExportacionReporte es el creador; crearExportador() es el método de fábrica sobrescribible. ExportacionPDF y ExportacionExcel lo implementan; ExportadorReporte define el producto y sus dos implementaciones generan cada formato.',
 'Recorrido: CU12 valida permisos y filtros → elige el creador configurado → exportar(datos) llama crearExportador() → el producto genera el archivo. El formato no amplía los datos autorizados. Agregar otro formato exige otro producto y su creador, conservando exportar().'),
('4. Builder aplicado al CRM','02_Builder_CRM.png',
 'Participantes: ServicioConfirmarPedido dirige; PedidoBuilder ensambla; Pedido y sus DetallePedido son el resultado. Es una vista parcial del dominio: cada detalle conserva su producto, unidad, precio aceptado y costo de referencia al confirmar.',
 'Recorrido: verificar aceptación y vigencia → añadir detalles → fijar fecha y condición de pago → build() → guardar en transacción. Si faltan datos, no se guarda un pedido incompleto. Crear el pedido no registra dinero recibido, no reserva stock y no autoriza su despacho.'),
('5. Abstract Factory: ejemplo externo','03_Abstract_Factory_Ejemplo.png',
 'Escenario: un editor permite usar tema claro u oscuro. FabricaTema crea dos productos relacionados, Boton y CampoTexto. FabricaClara produce ambos controles claros; FabricaOscura produce ambos oscuros. El editor recibe una sola fábrica y no mezcla sus familias.',
 'No se aplica ahora al CRM: no se han definido familias de componentes intercambiables que deban cambiar juntas. PDF y Excel son alternativas de un producto, Archivo, no una familia requerida de varios productos. Reconsiderarlo solo si aparece esa necesidad concreta.'),
('6. Prototype: ejemplo externo','04_Prototype_Ejemplo.png',
 'Escenario: un editor duplica una tarjeta de presentación para conservar el diseño. El cliente llama clonar() a través de Prototipo. Tarjeta obtiene una identidad nueva y copia profundamente su EstiloTarjeta; modificar el color de la copia deja intacto el original.',
 'No se aplica ahora al CRM: el objetivo es crear operaciones válidas, con aceptación y referencias nuevas. Una copia de Pedido no debe arrastrar saldo, pagos, reservas, estados ni precios antiguos. Una futura plantilla reutilizable requeriría un alcance específico y reglas de copia.'),
('7. Singleton: ejemplo externo','05_Singleton_Ejemplo.png',
 'Escenario: un visor de documentos de un solo proceso comparte configuración inmutable de idioma, tema y zoom. El constructor es privado; obtenerInstancia() y la referencia instancia son estáticos. La inicialización debe ser segura ante llamadas concurrentes.',
 'No se aplica como estado global del CRM: cada usuario, pedido y dispositivo conserva su propio contexto. Una instancia local no garantiza unicidad entre servidores o teléfonos. Puede haber recursos con duración de aplicación administrados por inyección de dependencias, sin usar un Singleton global para el negocio.')]
for i,(title,img,a,btext) in enumerate(patterns):
 if i:d.add_page_break()
 h(title);im=Image.open(OUT/'Diagramas'/img);w,hpx=im.size;width=min(26.3,14.0*w/hpx)
 q=d.add_paragraph();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.paragraph_format.space_after=Pt(3);q.add_run().add_picture(str(OUT/'Diagramas'/img),width=Cm(width))
 for text in [a,btext]:
  pp=p(text);pp.paragraph_format.space_after=Pt(5);pp.paragraph_format.line_spacing=1.0
  for rr in pp.runs:rr.font.size=Pt(10.5)
newsection(False)
h('8. Comparación de los patrones')
p('La comparación evalúa el diseño propuesto, no resultados de rendimiento medidos en producción. Ningún patrón garantiza por sí mismo que el sistema sea más rápido. El volumen de datos y las bibliotecas concretas suelen dominar el costo de exportar un archivo.')
table(['Patrón','Eficiencia','Mantenibilidad y aplicación'],[
('Factory Method','Añade una llamada y la creación del exportador. No elimina el costo de recorrer datos o codificar PDF/XLSX.','Aísla el formato y permite probar el flujo común. Agrega clases: útil con variantes reales; excesivo para una sola construcción trivial.'),
('Abstract Factory','Crear la familia cuesta lo que cuesten sus componentes. No es una optimización automática.','Mantiene coherencia entre productos. Agregar otra familia es directo; agregar otra clase de producto cambia todas las fábricas.'),
('Builder','Requiere un objeto auxiliar y almacenar los detalles durante la construcción. Ensamblar n detalles supone trabajo proporcional a n.','Hace explícitos los pasos y la validación final. Evitar compartir el builder entre usuarios o convertirlo en repositorio y servicio de pagos.'),
('Prototype','Una copia profunda recorre el estado copiado. Solo ahorra trabajo si reconstruir ese objeto era más costoso.','Facilita duplicar configuraciones complejas. Exige decidir qué copiar, qué compartir y qué identidad regenerar; riesgo de aliasing.'),
('Singleton','Reutiliza una instancia; el estado mutable compartido puede exigir sincronización y generar contención.','El acceso global oculta dependencias y dificulta aislar pruebas. Adecuado solo con necesidad real de unicidad y alcance bien definido.')],size=10)
h('Diferencias que importan en esta propuesta',2)
bullet('Factory Method elige una implementación de un producto; Abstract Factory entrega varias clases de producto que forman una familia coherente.')
bullet('Builder ensambla un objeto válido por pasos; Prototype parte de otro objeto ya configurado y debe controlar las referencias copiadas.')
bullet('Singleton determina cantidad y acceso a instancias. No sustituye autorización, transacciones, bloqueos distribuidos ni restricciones únicas de la base de datos.')
page('9. Mejores prácticas para implementarlos')
for title,body in [
('Mantener responsabilidades delimitadas','El servicio valida quién puede operar. El builder organiza la construcción. El repositorio persiste. Los exportadores codifican únicamente datos cuyo alcance ya se verificó.'),
('Validar las reglas del negocio además del patrón','El servicio de CU06 comprueba aceptación, vigencia, versión y condiciones actuales. El builder valida que haya detalles, cantidades positivas, unidades y campos obligatorios. La unidad del detalle debe corresponder al producto.'),
('Guardar el pedido de forma atómica','Pedido y detalles se guardan juntos. Una restricción única para la cotización aceptada impide crear dos pedidos por el mismo intento repetido. Revalidar versión y vigencia en la transacción; el builder no resuelve concurrencia.'),
('Preservar los acuerdos comerciales','Tomar el precio aceptado de la versión de cotización; el costo de referencia se fija al confirmar según la regla vigente. Evitar referencias mutables compartidas con formularios o catálogo. Un cambio posterior no recalcula el histórico.'),
('Usar un builder por operación','No reutilizarlo entre solicitudes concurrentes. build() entrega detalles independientes del estado temporal. Reservas, cobros y seña permanecen en sus módulos y requieren sus propias condiciones.'),
('Configurar las variantes en un punto explícito','La selección PDF/Excel pertenece a la composición del servicio. Evitar condicionales de formato repetidos en clientes, controladores o entidades. Una función estática con un switch no demuestra por sí sola el Factory Method GoF.'),
('Proteger las exportaciones','Revalidar permisos y filtros al exportar. Comprador solo accede a sus datos. Definir límites de tamaño y una estrategia de escritura para volúmenes grandes; no prometer eficiencia sin medir con datos representativos.'),
('Evitar abstracciones sin uso y estados globales','Revisar Abstract Factory cuando existan familias reales, Prototype cuando haya plantillas aprobadas y Singleton cuando haya unicidad local justificada. Para la base Android puede administrarse una instancia por proceso mediante dependencias; no compartir datos de usuario globalmente.')]:
 h(title,2);p(body)
page('10. Casos de estudio y evaluación')
h('Caso A · El mismo reporte en dos formatos',2)
p('Situación: administración consulta pedidos de un período y solicita PDF o Excel; un comprador solo consulta los propios. El servicio filtra y autoriza antes de invocar el creador. La prueba aislada entrega exactamente las mismas filas a ambos exportadores y agrega una tercera implementación sin modificar exportar().')
p('Resultado observado en el prototipo: se selecciona el exportador correcto y se conserva el conjunto de datos recibido. Impacto esperado: menor duplicación del flujo y cambios de formato localizados. Pendiente al implementar: probar los archivos reales, sus límites, filtros y permisos. El patrón no implementa la autorización por sí mismo.')
h('Caso B · Confirmar un pedido con varios cortes',2)
p('Situación ilustrativa: una cotización aceptada origina un pedido de 4 kg de costilla y 2 kg de lomo. El servicio dirige los pasos y el builder conserva cada detalle. Se comprueba que una cotización rechazada o vencida y un pedido sin detalles no produzcan un resultado válido.')
p('Resultado observado: la construcción admite varios productos, mantiene los valores de cada detalle y devuelve una colección independiente del builder. Para 4 kg con precio Bs 35 y costo Bs 28, el margen estimado del detalle es Bs 28. Son datos de prueba; no representan precios comerciales confirmados.')
table(['Comprobación ejecutada','Pruebas','Resultado'],[
('Tipo concreto, mismo contenido, extensión y copia de datos de exportación','5','Correctas'),
('Varios detalles; rechazo, vencimiento, ausencia de detalles y cantidad inválida','5','Correctas'),
('Precio/costo, independencia de la colección, campos obligatorios y alcance sin pagos/stock','4','Correctas')],size=10)
p('Total: 14/14 comprobaciones aprobadas en un prototipo didáctico aislado. Los exportadores son dobles de prueba: no generan archivos PDF/XLSX reales. Tampoco se probó autenticación, persistencia ni concurrencia de SGCC. Código reproducible: 99_Herramientas/patrones_creacionales/prototipo.py; ejecución: python3 prototipo.py.',False)
h('Caso documentado · Builder en Java',2)
p('La API HttpRequest.Builder permite configurar una petición y construir una instancia HttpRequest inmutable. Su documentación advierte que el builder no sincroniza sus métodos [2]. Es una aplicación real del ensamblaje gradual; respalda la decisión de no compartir un builder mutable entre operaciones del CRM. No aporta un porcentaje de mejora de rendimiento para nuestro sistema.')
page('11. Decisión final y referencias')
p('La propuesta incorpora dos patrones creacionales al diseño de implementación: Factory Method en reportes y Builder en confirmación de pedidos. Cada uno responde a una necesidad ya presente. Los otros tres quedan documentados mediante ejemplos completos, sin aumentar artificialmente el alcance del SGCC.')
h('Contenido del archivo MDJ',2)
table(['Grupo','Diagrama'],[('Aplicados al CRM','01 · Factory Method · Exportar reportes'),('Aplicados al CRM','02 · Builder · Construir un pedido'),('Ejemplos externos','03 · Abstract Factory · Editor con temas'),('Ejemplos externos','04 · Prototype · Duplicar una tarjeta'),('Ejemplos externos','05 · Singleton · Configuración de un visor')],size=10)
p('Abrir Patrones_Creacionales_SGCC.mdj en StarUML y expandir los dos grupos del explorador. Cada diagrama tiene su propio icono. Las imágenes del informe se exportaron desde ese mismo archivo. Las clases y relaciones son editables; no son capturas colocadas dentro del MDJ.')
h('Lectura de los diagramas',2)
p('Triángulo vacío y línea continua: herencia. Triángulo vacío y línea discontinua: realización de interfaz. Flecha discontinua: dependencia; «create» señala creación. Rombo negro: composición. Miembros subrayados: estáticos; texto en cursiva: abstracto. + público, # protegido y − privado.')
h('Fuentes',2)
p('[1] Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1995). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley. Catálogo creacional y clasificación. Definiciones parafraseadas; los ejemplos de este informe son elaboración propia.')
link('Ficha del libro en la editorial InformIT','https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610')
link('Catálogo del libro disponible en O’Reilly','https://www.oreilly.com/library/view/design-patterns-elements/0201633612/front.html')
p('[2] Oracle. Java SE 25: HttpRequest.Builder. Contrato de construcción y comportamiento ante concurrencia. Consulta: 3 de noviembre de 2026.')
link('Documentación oficial de HttpRequest.Builder','https://docs.oracle.com/en/java/javase/25/docs/api/java.net.http/java/net/http/HttpRequest.Builder.html')
p('[3] JetBrains. Kotlin: Object declarations and expressions. Las declaraciones object se inicializan al primer acceso de forma segura entre hilos; esto no vuelve seguro cualquier estado mutable que contengan. Referencia para una posible realización del ejemplo Singleton.')
link('Documentación oficial de object en Kotlin','https://kotlinlang.org/docs/object-declarations.html')
p('[4] Fuentes internas: ASA1 vigente; Catálogo de casos de uso; Reglas del sistema; Clases_SGCC.mdj. Se revisaron CU06, CU12 y las entidades Pedido, DetallePedido y Cotizacion. Este trabajo complementa los modelos generales y conserva sus reglas comerciales.')
# Orphan protection without forcing full pages of body text together.
for para in d.paragraphs:para.paragraph_format.widow_control=True
file=OUT/'Patrones_Creacionales_SGCC.docx';d.save(file);print(file)
