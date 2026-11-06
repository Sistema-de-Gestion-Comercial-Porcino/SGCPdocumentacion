from pathlib import Path
import json,collections,os,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'01_Proyecto_de_Sistemas/BPM_Vertical'
def walk(x):
 if isinstance(x,dict):
  if '_id' in x:yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def allrefs(x):
 if isinstance(x,dict):
  if '$ref'in x:yield x['$ref']
  for v in x.values():yield from allrefs(v)
 elif isinstance(x,list):
  for v in x:yield from allrefs(v)
def segments(o):
 ps=[tuple(map(float,p.split(':')))for p in o['points'].split(';')];return list(zip(ps,ps[1:]))
def overlap(a,b):return min(a['left']+a['width'],b['left']+b['width'])>max(a['left'],b['left']) and min(a['top']+a['height'],b['top']+b['height'])>max(a['top'],b['top'])
reports=[]
for p in sorted(root.glob('*.mdj')):
 raw=json.loads(p.read_text());obs=list(walk(raw));idx={o['_id']:o for o in obs};assert len(idx)==len(obs);missing=set(allrefs(raw))-set(idx);assert not missing,missing
 ds=[o for o in obs if o['_type'].endswith('Diagram')];assert len(ds)==1
 nodes=[o for o in obs if o['_type'] in ['UMLAction','UMLInitialNode','UMLActivityFinalNode','UMLDecisionNode','UMLMergeNode','UMLActivityEdgeConnector']];flows=[o for o in obs if o['_type']=='UMLControlFlow'];adj=collections.defaultdict(set)
 for e in flows:adj[e['source']['$ref']].add(e['target']['$ref'])
 start=[o['_id'] for o in nodes if o['_type']=='UMLInitialNode'];assert len(start)==1
 reached=set(start);todo=list(start)
 while todo:
  for b in adj[todo.pop()]:
   if b not in reached:reached.add(b);todo.append(b)
 unreachable=[o.get('name') for o in nodes if o['_id'] not in reached]
 canend={o['_id'] for o in nodes if o['_type']=='UMLActivityFinalNode'}
 while True:
  count=len(canend)
  for a,bs in adj.items():
   if bs&canend:canend.add(a)
  if len(canend)==count:break
 noend=[o.get('name')for o in nodes if o['_id'] not in canend]
 for o in nodes:
  if o['_type']=='UMLDecisionNode':
   exits=[e for e in flows if e['source']['$ref']==o['_id']];assert len(exits)>=2 and all(e.get('guard')for e in exits),o
 views=[o for o in obs if o['_type'] in ['UMLActionView','UMLControlNodeView','UMLActivityEdgeConnectorView']];edges=[o for o in obs if o['_type']=='UMLControlFlowView'];hits=[];cross=[];stack=[];nodehits=[]
 for i,a in enumerate(views):
  for b in views[i+1:]:
   if overlap(a,b):nodehits.append([a['_id'],b['_id']])
 for e in edges:
  for n in views:
   if n['_id'] in [e['head']['$ref'],e['tail']['$ref']]:continue
   l,t,w,h=[n[k]for k in ['left','top','width','height']]
   for (x,y),(a,b) in segments(e):
    if x==a and l+2<x<l+w-2 and min(max(y,b),t+h-2)>max(min(y,b),t+2) or y==b and t+2<y<t+h-2 and min(max(x,a),l+w-2)>max(min(x,a),l+2):hits.append([e['_id'],n['_id']])
 for i,e in enumerate(edges):
  for f in edges[i+1:]:
   for (x,y),(a,b) in segments(e):
    for (u,v),(c,d) in segments(f):
     if x==a and v==d and min(u,c)<x<max(u,c) and min(y,b)<v<max(y,b) or y==b and u==c and min(x,a)<u<max(x,a) and min(v,d)<y<max(v,d):cross.append([e['_id'],f['_id']])
     if x==a==u==c and min(max(y,b),max(v,d))>max(min(y,b),min(v,d)) or y==b==v==d and min(max(x,a),max(u,c))>max(min(x,a),min(u,c)):stack.append([e['_id'],f['_id']])
 report={'archivo':p.name,'diagramas':len(ds),'pasos':len(views),'nodosModelo':len(nodes),'decisiones':sum(o['_type']=='UMLDecisionNode'for o in nodes),'flujos':len(flows),'inalcanzables':unreachable,'sinSalidaFinal':noend,'nodosSuperpuestos':nodehits,'lineasSobreNodos':hits,'cruces':cross,'segmentosSuperpuestos':stack};reports.append(report)
 print(p.name,'pasos',len(views),'inalcanzables',len(unreachable),'sinFinal',len(noend),'nodosSuperpuestos',len(nodehits),'sobreNodos',len(hits),'cruces',len(cross),'superpuestas',len(stack))
Path(os.environ.get('SGCC_VERTICAL_REPORT','/tmp/Validacion_BPM_vertical.json')).write_text(json.dumps(reports,ensure_ascii=False,indent=2))
