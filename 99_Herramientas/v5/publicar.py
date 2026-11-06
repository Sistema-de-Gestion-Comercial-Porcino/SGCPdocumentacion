from pathlib import Path
import shutil,json,hashlib,os
R=Path(__file__).resolve().parents[2];T=Path('/tmp/sgcc_reorganizacion_20261029');S=R/'02_Ingenieria_de_Software';old=json.loads((T/'antes.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Refuse to overwrite changes made by the user after the original inventory.
for rel,h in old.items():
 p=R/rel
 assert p.is_file()and sha(p)==h,('El archivo original cambió durante la preparación',rel)
assert len(list((T/'Software').rglob('*.mdj')))==77
assert len(json.loads((T/'Validacion_nativa.json').read_text()))==79
assert not json.loads((T/'Validacion_UML.json').read_text())['errores']
assert json.loads((T/'Validacion_documentos_PDF.json').read_text())['PDFIndividualesIgualesAConjunto']
assert (T/'respaldo').is_dir()
removed=[];written=[]
def replace_tree(src,dest):
 assert src.is_dir()and list(src.iterdir()),src
 if dest.exists():
  removed.extend(str(p.relative_to(R))for p in dest.rglob('*')if p.is_file());shutil.rmtree(dest)
 shutil.copytree(src,dest);written.extend(str(p.relative_to(R))for p in dest.rglob('*')if p.is_file())
def cp(src,dest):
 dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_name(dest.name+'.nuevo');shutil.copy2(src,tmp);os.replace(tmp,dest);written.append(str(dest.relative_to(R)))
for folder in ['01_Generales','02_Colaboracion','03_Objetos','04_Estados','05_Actividades','06_Secuencias','BPMN_Horizontal']:replace_tree(T/'Software'/folder,S/folder)
V=T/'BPM_Entrega';V.mkdir(exist_ok=True)
for p in (T/'BPM').iterdir():
 if p.suffix in ['.mdj','.pdf']:shutil.copy2(p,V/p.name)
replace_tree(V,R/'01_Proyecto_de_Sistemas/BPM_Vertical')
replace_tree(T/'PDFentrega',S/'PDFentrega')
replace_tree(T/'Definicion',R/'00_Definicion')
replace_tree(T/'Documentacion',S/'00_Documentacion')
replace_tree(T/'04_Mockups_Balsamiq',R/'04_Mockups_Balsamiq')
name='ASA1 - Especificacion de Requerimientos - CRM Chancheria'
cp(T/'Documentos'/(name+'.docx'),R/(name+'.docx'));cp(T/'Documentos'/(name+'.pdf'),S/'PDFentrega'/(name+'.pdf'))
cp(T/'Documentos'/'Formato Proyecto - SGCC Actualizado.xlsx',R/'Formato Proyecto - SGCC Actualizado.xlsx')
cp(T/'04_Mockups_Balsamiq/SGCC_Web_Android.bmpr',S/'SGCC_Web_Android.bmpr')
# Prepare a concise MDJ delivery: four general projects, five consolidated projects, two BPMN.
E=T/'Entrega';E.mkdir(exist_ok=True)
for p in (T/'Software/01_Generales').glob('*.mdj'):shutil.copy2(p,E/p.name)
for p in (T/'Software').rglob('*_Completo.mdj'):shutil.copy2(p,E/p.name)
for p in (T/'Software/BPMN_Horizontal').glob('*.mdj'):shutil.copy2(p,E/p.name)
shutil.copy2(T/'Documentos'/(name+'.docx'),E/(name+'.docx'))
assert len(list(E.glob('*.mdj')))==11
replace_tree(E,S/'Entrega')
for rel in ['Formato Proyecto - SGCC.xlsx','02_Ingenieria_de_Software/Entrega.zip','02_Ingenieria_de_Software/LEEME.md','02_Ingenieria_de_Software/Indice_MDJs.md']:
 p=R/rel
 if p.exists():removed.append(rel);p.unlink()
(R/'LEEME.md').write_text('''# SGCC · entrega reorganizada

[MDJ generales y consolidados](02_Ingenieria_de_Software/Entrega/) · [PDF completo de software](02_Ingenieria_de_Software/PDFentrega/Diagramas_SGCC_Completo.pdf) · [Índice de diagramas](02_Ingenieria_de_Software/00_Documentacion/Indice_entrega.md).

Doce casos de uso generales; 72 diagramas de Ingeniería de Software. Los cinco archivos consolidados reúnen colaboración, objetos, estados, actividades y secuencias. Hay 12 por categoría dependiente de CU y 18 máquinas de estados. Los cuatro diagramas generales son casos de uso, clases, componentes y despliegue. Se añaden dos BPMN horizontales.

Los dos [BPM verticales](01_Proyecto_de_Sistemas/BPM_Vertical/) pertenecen a Proyecto de Sistemas y están separados del PDF conjunto. Total único del proyecto: 74 diagramas; los consolidados y copias no se cuentan otra vez.

[ASA1](<ASA1 - Especificacion de Requerimientos - CRM Chancheria.docx>) conserva su estructura. [Excel actualizado de trabajo](<Formato Proyecto - SGCC Actualizado.xlsx>) mantiene el versionamiento sin cambios; [Excel ya presentado](<Formato Proyecto - SGCC 1 1.xlsx>) se conserva intacto.

[Mockups web y Android](04_Mockups_Balsamiq/SGCC_Web_Android.bmpr): 67 pantallas editables con navegación. [Casos y acciones](00_Definicion/Catalogo_casos_de_uso.md), [equivalencias](00_Definicion/Matriz_trazabilidad.md) y [reglas vigentes](00_Definicion/Reglas_del_sistema.md).

Catálogo, cantidades, tiempos y precios de los ejemplos son ilustrativos; requieren validación comercial. Web online y Android Kotlin para recepción autorizada/descargada. Prototipos y diagramas son diseño del sistema, no una aplicación ya implementada.
''')
assert sha(R/'Formato Proyecto - SGCC 1 1.xlsx')==old['Formato Proyecto - SGCC 1 1.xlsx']
(S/'00_Documentacion/Limpieza_entrega.json').write_text(json.dumps({'retirados_o_reemplazados':removed,'publicados':written,'excelPresentadoConservado':True,'respaldoExterno':str(T/'respaldo')},ensure_ascii=False,indent=2))
print('Publicado:',len(written),'archivos. Versiones anteriores retiradas; Excel presentado intacto.')
