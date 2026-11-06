from pathlib import Path
import json,hashlib,base64,copy
ROOT=Path(__file__).resolve().parents[1]/'02_Ingenieria_de_Software'
TMP=Path('/tmp/sgcc_ajuste_stock_20261026/unificados');TMP.mkdir(exist_ok=True)
GROUPS=[('02_Colaboracion','Colaboracion_SGCC_Completo.mdj','Colaboración',26,'UMLCommunicationDiagram'),('03_Objetos','Objetos_SGCC_Completo.mdj','Objetos',26,'UMLObjectDiagram'),('04_Estados','Estados_SGCC_Completo.mdj','Estados',18,'UMLStatechartDiagram'),('05_Actividades','Actividades_SGCC_Completo.mdj','Actividades',26,'UMLActivityDiagram'),('06_Secuencias','Secuencias_SGCC_Completo.mdj','Secuencias',26,'UMLSequenceDiagram')]
def walk(x):
 if isinstance(x,dict):
  if '_id' in x:yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def idfor(key):return base64.b64encode(hashlib.sha256(('SGCC-unificados-20261026/'+key).encode()).digest()[:15]).decode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def refs(x):
 if isinstance(x,dict):
  if '$ref' in x:yield x['$ref']
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def remap(x,ids):
 if isinstance(x,dict):return {k:ids[v] if k in ['_id','$ref'] else remap(v,ids) for k,v in x.items()}
 if isinstance(x,list):return [remap(v,ids) for v in x]
 return x
report=[]
for folder,filename,label,count,kind in GROUPS:
 dest=ROOT/folder/filename

 sources=sorted(p for p in (ROOT/folder).glob('*.mdj') if not p.name.endswith('_Completo.mdj'))
 assert len(sources)==count,(folder,len(sources))
 project={'_type':'Project','_id':idfor(folder),'name':f'SGCC — {label}','ownedElements':[]}
 source_rows=[];diagram_rows=[]
 for i,p in enumerate(sources):
  raw=json.loads(p.read_text());obs=list(walk(raw));old_ids={o['_id'] for o in obs}
  assert len(old_ids)==len(obs) and not(set(refs(raw))-old_ids),p
  ds=[o for o in obs if o.get('_type','').endswith('Diagram')]
  assert len(ds)==1 and ds[0]['_type']==kind,p
  assert raw['_type']=='Project' and list(k for k in raw if k not in ['_type','_id','name','ownedElements','documentVersion'])==[],p
  project.setdefault('documentVersion',raw.get('documentVersion','5.0.0'))
  assert raw.get('documentVersion')==project['documentVersion'],p
  ids={old:idfor(folder+'/'+p.name+'/'+old) for old in old_ids};ids[raw['_id']]=project['_id']
  merged=remap(raw,ids)
  d=next(o for o in walk(merged) if o['_type']==kind);d['defaultDiagram']=i==0
  # Dos modelos de estados de Pedido se distinguen por el ordinal del archivo.
  if folder=='04_Estados':
   for top in merged['ownedElements']:top['name']=p.stem.split('_',1)[0]+' — '+top.get('name',p.stem)
  # Comprobar que todo el modelo copiado conserva su contenido y distribución.
  inverse={v:k for k,v in ids.items()};restored=remap(merged,inverse)
  restored['name']=raw['name']
  rd=next(o for o in walk(restored) if o['_type']==kind)
  if 'defaultDiagram' in ds[0]:rd['defaultDiagram']=ds[0]['defaultDiagram']
  else:rd.pop('defaultDiagram',None)
  if folder=='04_Estados':
   for top,original in zip(restored['ownedElements'],raw['ownedElements']):top['name']=original['name']
  assert restored==raw,('Contenido alterado',p)
  # Mantener icono de diagrama directamente visible en colaboración y estados.
  if folder in ['02_Colaboracion','04_Estados']:
   idx={x['_id']:x for x in walk(merged)}
   for top in merged['ownedElements']:
    ds2=[x for x in walk(top) if x['_type']==kind];assert len(ds2)==1
    diagram=ds2[0];parent=idx[diagram['_parent']['$ref']]
    if parent is not top:
     parent['ownedElements'].remove(diagram);top.setdefault('ownedElements',[]).insert(0,diagram);diagram['_parent']={'$ref':top['_id']}
    if folder=='04_Estados':top['name']=p.stem.split('_',1)[0]+' — '+diagram['name'].removeprefix('Estados · ')
  project['ownedElements'].extend(merged['ownedElements'])
  source_rows.append({'archivo':str(p),'sha256':sha(p),'contenidoConservado':True})
  diagram_rows.append({'id':d['_id'],'nombre':d.get('name'),'tipo':kind,'vistas':len(d.get('ownedViews',[])),'archivoOrigen':p.name})
 obs=list(walk(project));ids={o['_id'] for o in obs}
 assert len(ids)==len(obs) and not(set(refs(project))-ids)
 ds=[o for o in obs if o.get('_type','').endswith('Diagram')]
 assert len(ds)==count and sum(bool(d.get('defaultDiagram')) for d in ds)==1
 staged=TMP/filename;staged.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
 report.append({'destino':str(dest),'temporal':str(staged),'categoria':label,'diagramas':diagram_rows,'fuentes':source_rows,'elementos':len(obs)})
(TMP/'plan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Preparados:',len(report),'proyectos;',sum(len(x['diagramas']) for x in report),'diagramas. Fuentes intactas y contenido conservado.')

# Sustituir consolidados; fuentes individuales verificadas, sin modificaciones.
for row in report:
 for source in row['fuentes']:assert sha(Path(source['archivo']))==source['sha256']
 dest=Path(row['destino']);dest.write_bytes(Path(row['temporal']).read_bytes())
 mirror=ROOT/'Entrega'/dest.name
 if mirror.exists():mirror.write_bytes(dest.read_bytes())
print('Cinco consolidados y sus copias actualizados; navegación directa conservada.')
