import json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];out=R/'02_Ingenieria_de_Software/Patrones de diseño/Patrones creacionales';raw=json.loads((out/'Patrones_Creacionales_SGCC.mdj').read_text());objects=[];refs=[]
def walk(x):
 if isinstance(x,dict):
  if '_id'in x:objects.append(x)
  if '$ref'in x:refs.append(x['$ref'])
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(raw);idx={x['_id']:x for x in objects};assert len(idx)==len(objects);assert not(set(refs)-set(idx));ds=[o for o in objects if o['_type'].endswith('Diagram')];assert len(ds)==5 and sum(bool(d.get('defaultDiagram'))for d in ds)==1
errors=[]
for d in ds:
 nodes=[v for v in d['ownedViews']if v['_type']in ['UMLClassView','UMLInterfaceView']];edges=[v for v in d['ownedViews']if 'points'in v]
 for i,a in enumerate(nodes):
  for b in nodes[i+1:]:
   if min(a['left']+a['width'],b['left']+b['width'])>max(a['left'],b['left'])and min(a['top']+a['height'],b['top']+b['height'])>max(a['top'],b['top']):errors.append(('Nodos superpuestos',d['name']))
 for e in edges:
  ps=[tuple(map(float,p.split(':')))for p in e['points'].split(';')if ':'in p]
  for n in nodes:
   if n['_id']in [e['head']['$ref'],e['tail']['$ref']]:continue
   l,r=n['left']+2,n['left']+n['width']-2;t,b=n['top']+2,n['top']+n['height']-2
   for (x,y),(xx,yy)in zip(ps,ps[1:]):
    if (x==xx and l<x<r and min(max(y,yy),b)>max(min(y,yy),t))or(y==yy and t<y<b and min(max(x,xx),r)>max(min(x,xx),l)):errors.append(('Línea atraviesa clase',d['name'],idx[n['model']['$ref']]['name']))
 for v in nodes:assert v.get('width',0)>0 and v.get('height',0)>0
assert not errors,errors
creator=next(o for o in objects if o.get('name')=='ExportacionReporte'and o['_type']=='UMLClass');assert creator['isAbstract'];assert any(x.get('isAbstract')and x['name']=='crearExportador'for x in creator['operations'])
single=next(o for o in objects if o.get('name')=='ConfiguracionVisor'and o['_type']=='UMLClass');assert any(x['name']=='obtenerInstancia'and x['isStatic']for x in single['operations']);assert any(x['name']=='ConfiguracionVisor'and x['visibility']=='private'for x in single['operations'])
assert all(any(o['_type']=='UMLClassDiagram'for o in g['ownedElements'])for g in raw['ownedElements'])
result={'diagramas':5,'aplicadosCRM':2,'ejemplosExternos':3,'referenciasValidas':True,'identificadoresUnicos':True,'erroresGeometria':errors,'factoryMethodSobrescribible':True,'singletonConstructorPrivadoYAccesoEstatico':True}
Path('/tmp/sgcc_patrones_20261103/validacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(result)
