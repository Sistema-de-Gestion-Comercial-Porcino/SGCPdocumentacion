from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parents[2];errors=[];counts={}
for path in sorted((ROOT/'02_Ingenieria_de_Software/Patrones de diseño').glob('*/Patrones_*_SGCP.mdj')):
 objs=[];refs=[]
 def walk(x):
  if isinstance(x,dict):
   if '_id'in x:objs.append(x)
   if '$ref'in x:refs.append(x['$ref'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(json.loads(path.read_text()));idx={o['_id']:o for o in objs};assert len(idx)==len(objs)and not(set(refs)-set(idx));ds=[o for o in objs if o['_type']=='UMLClassDiagram'];counts[path.name]=len(ds);assert sum(bool(d.get('defaultDiagram'))for d in ds)==1
 for d in ds:
  nodes=[n for n in d['ownedViews']if n['_type']in ['UMLClassView','UMLInterfaceView']]
  for i,a in enumerate(nodes):
   for b in nodes[i+1:]:
    if min(a['left']+a['width'],b['left']+b['width'])>max(a['left'],b['left'])and min(a['top']+a['height'],b['top']+b['height'])>max(a['top'],b['top']):errors.append([d['name'],'superposición',idx[a['model']['$ref']]['name'],idx[b['model']['$ref']]['name']])
  for e in [v for v in d['ownedViews']if'points'in v]:
   ps=[tuple(map(float,v.split(':')))for v in e['points'].split(';')if':'in v]
   for n in nodes:
    if n['_id']in [e['head']['$ref'],e['tail']['$ref']]:continue
    l,r=n['left']+2,n['left']+n['width']-2;t,b=n['top']+2,n['top']+n['height']-2
    for(x,y),(xx,yy)in zip(ps,ps[1:]):
     if(x==xx and l<x<r and min(max(y,yy),b)>max(min(y,yy),t))or(y==yy and t<y<b and min(max(x,xx),r)>max(min(x,xx),l)):errors.append([d['name'],'arista atraviesa clase',idx[n['model']['$ref']]['name']])
assert sorted(counts.values())==[7,11],counts
result={'diagramas':counts,'ids_unicos':True,'referencias_resueltas':True,'errores':errors}
Path('/tmp/sgcp_patrones_20261105/validacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));assert not errors
