from pathlib import Path
import json,collections
P=Path('/tmp/sgcc_reorganizacion_20261029');reports=[]
def walk(x):
 if isinstance(x,dict):
  if '_id'in x:yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def refs(x):
 if isinstance(x,dict):
  if '$ref'in x:yield x['$ref']
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def seg(e):
 ps=[tuple(map(float,z.split(':')))for z in e['points'].split(';')if ':'in z];return list(zip(ps,ps[1:]))
for p in sorted((P/'BPMN').glob('*.mdj')):
 raw=json.loads(p.read_text());obs=list(walk(raw));idx={o['_id']:o for o in obs};assert len(idx)==len(obs)and not(set(refs(raw))-set(idx))
 flows=[o for o in obs if o['_type']=='BPMNSequenceFlow'];nodes=[o for o in obs if o.get('id','').startswith('T')and o['_type'] not in ['BPMNSequenceFlow']];adj=collections.defaultdict(set)
 for e in flows:adj[e['source']['$ref']].add(e['target']['$ref'])
 catches=collections.defaultdict(list);throws=[]
 for n in nodes:
  for e in n.get('eventDefinitions',[]):
   if e['_type']=='BPMNLinkEventDefinition':
    if n['_type']=='BPMNIntermediateCatchEvent':catches[e['name']].append(n['_id'])
    else:throws.append((n['_id'],e['name']))
 for a,code in throws:
  assert len(catches[code])==1,(code,catches[code]);adj[a].update(catches[code])
 start=[o['_id']for o in nodes if o['_type']=='BPMNStartEvent'];assert len(start)==1
 reached=set(start);q=list(start)
 while q:
  for b in adj[q.pop()]:
   if b not in reached:reached.add(b);q.append(b)
 unreachable=[o.get('id')for o in nodes if o['_id']not in reached];assert not unreachable,unreachable
 ends={o['_id']for o in nodes if o['_type']=='BPMNEndEvent'}
 while True:
  old=len(ends)
  for a,bs in adj.items():
   if bs&ends:ends.add(a)
  if old==len(ends):break
 assert all(o['_id']in ends for o in nodes)
 for n in nodes:
  if n['_type']=='BPMNExclusiveGateway'and len(adj[n['_id']])>1:
   assert all(e.get('condition')for e in flows if e['source']['$ref']==n['_id'])
 vs=[o for o in obs if o['_type']in ['BPMNTaskView','BPMNGatewayView','BPMNEventView']];es=[o for o in obs if o['_type']=='BPMNSequenceFlowView'];hits=[];cross=[];stack=[]
 for e in es:
  for n in vs:
   if n['_id']in [e['head']['$ref'],e['tail']['$ref']]:continue
   l,t,w,h=[n[k]for k in ['left','top','width','height']]
   for (x,y),(a,b) in seg(e):
    if (x==a and l+2<x<l+w-2 and min(max(y,b),t+h-2)>max(min(y,b),t+2))or(y==b and t+2<y<t+h-2 and min(max(x,a),l+w-2)>max(min(x,a),l+2)):hits.append([e['_id'],n['_id']])
 for i,e in enumerate(es):
  for f in es[i+1:]:
   for (x,y),(a,b)in seg(e):
    for (u,v),(c,d)in seg(f):
     if (x==a and v==d and min(u,c)<x<max(u,c)and min(y,b)<v<max(y,b))or(y==b and u==c and min(x,a)<u<max(x,a)and min(v,d)<y<max(v,d)):cross.append([e['_id'],f['_id']])
     if (x==a==u==c and min(max(y,b),max(v,d))>max(min(y,b),min(v,d)))or(y==b==v==d and min(max(x,a),max(u,c))>max(min(x,a),min(u,c))):stack.append([e['_id'],f['_id']])
 report={'archivo':p.name,'pasos':len(nodes),'flujos':len(flows),'inalcanzables':unreachable,'lineasSobreNodos':hits,'cruces':cross,'superpuestas':stack};reports.append(report);assert not hits and not cross and not stack,report
 print(p.name,'flujo alcanzable y con salida; cero cruces, superposiciones o líneas sobre nodos.')
(P/'Validacion_BPMN.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
