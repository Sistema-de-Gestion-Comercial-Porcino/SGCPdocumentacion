"""Comprueba referencias, notación UML, estados, instancias y geometría de la V4."""
import json, collections, re, sys, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'02_Ingenieria_de_Software'
def walk(x):
    if isinstance(x,dict):
        if '_id' in x:yield x
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
def intersects(a,b,pad=2):
    return min(a['left']+a['width']+pad,b['left']+b['width'])>max(a['left']-pad,b['left']) and min(a['top']+a['height']+pad,b['top']+b['height'])>max(a['top']-pad,b['top'])
def pts(e):return [tuple(map(float,p.split(':'))) for p in e.get('points','').split(';') if ':' in p]
node_types={'UMLClassView','UMLObjectView','UMLActorView','UMLUseCaseView','UMLComponentView','UMLStateView','UMLPseudostateView','UMLFinalStateView','UMLCommLifelineView','UMLArtifactView','UMLNodeView'}
reports=[];failures=[]
for file in sorted(p for folder in ['01_Generales','02_Colaboracion','03_Objetos','04_Estados'] for p in (OUT/folder).glob('*.mdj') if not p.name.endswith('_Completo.mdj')):
    data=json.loads(file.read_text());all_o=list(walk(data));idx={o['_id']:o for o in all_o};errors=[];warnings=[]
    def ref(x):return idx.get(x.get('$ref'),{}) if isinstance(x,dict) else {}
    def name(x):return ref(x.get('model')).get('name',x.get('name',x['_type']))
    def isa(cl,parent):
        return cl==parent or any(x.get('_type')=='UMLGeneralization' and x['source']['$ref']==cl and isa(x['target']['$ref'],parent) for x in all_o)
    if len(idx)!=len(all_o):errors.append('Identificadores repetidos')
    def checkrefs(x):
        if isinstance(x,dict):
            if '$ref' in x and x['$ref'] not in idx:errors.append('Referencia rota: '+x['$ref'])
            for v in x.values():checkrefs(v)
        elif isinstance(x,list):
            for v in x:checkrefs(v)
    checkrefs(data)
    ds=[o for o in all_o if o['_type'].endswith('Diagram')]
    if len(ds)!=1 or not ds[0].get('defaultDiagram'):errors.append('Falta diagrama inicial único')
    d=ds[0];views=d.get('ownedViews',[])
    if not views:errors.append('Sin vistas')
    if any(v.get('left',0)<0 or v.get('top',0)<0 for v in views):errors.append('Vista fuera del lienzo')
    for obj in [x for x in all_o if x['_type']=='UMLObject']:
        cls=ref(obj.get('classifier'))
        if cls.get('isAbstract'):errors.append('Instancia de clase abstracta: '+obj['name'])
        for slot in obj.get('slots',[]):
            a=ref(slot.get('definingFeature'))
            if not a:errors.append('Slot sin atributo: '+slot.get('name',''))
            elif not isa(cls['_id'],a['_parent']['$ref']):errors.append('Slot de otra clase')
            en=ref(a.get('type'))
            if en.get('_type')=='UMLEnumeration' and slot.get('value') not in [v['name'] for v in en['literals']]:errors.append('Literal fuera de enumeración: '+slot['value'])
            if a.get('type')=='UUID' and not re.fullmatch(r'"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}"',slot.get('value','')):errors.append('UUID ilustrativo inválido')
    for link in [x for x in all_o if x['_type']=='UMLLink']:
        r=ref(link.get('association'))
        if not r:errors.append('Enlace sin asociación')
        else:
            for n in ['end1','end2']:
                obj=ref(link[n].get('reference'));cl=ref(obj.get('classifier'))
                if not isa(cl['_id'],r[n]['reference']['$ref']):errors.append('Enlace incompatible con su asociación')
    for msg in [x for x in all_o if x['_type']=='UMLMessage']:
        if not msg.get('sequenceNumber'):errors.append('Mensaje sin número')
        source=ref(msg.get('source'));target=ref(msg.get('target'));conn=ref(msg.get('connector'))
        if not conn:errors.append('Mensaje sin conector')
        elif set([source['represent']['$ref'],target['represent']['$ref']])!=set([conn['end1']['reference']['$ref'],conn['end2']['reference']['$ref']]):errors.append('Conector no une participantes del mensaje')
    for region in [x for x in all_o if x['_type']=='UMLRegion']:
        vertices=region.get('vertices',[]);trans=region.get('transitions',[])
        initial=[v for v in vertices if v['_type']=='UMLPseudostate' and v.get('kind','initial')=='initial']
        if len(initial)!=1:errors.append('Inicio de estados no único')
        seen={v['_id'] for v in initial};change=True
        while change:
            change=False
            for e in trans:
                if e['source']['$ref'] in seen and e['target']['$ref'] not in seen:seen.add(e['target']['$ref']);change=True
        for v in vertices:
            if v['_id'] not in seen:errors.append('Estado inalcanzable: '+v.get('name',''))
        for v in initial:
            es=[e for e in trans if e['source']['$ref']==v['_id']]
            if len(es)!=1 or es[0].get('guard') or es[0].get('triggers'):errors.append('Transición inicial inválida')
        sm=ref(region['_parent']);cl=ref(sm['_parent']);attr_name=sm['name'].split('.')[-1];a=next(a for a in cl['attributes'] if a['name']==attr_name);en=ref(a['type'])
        if {v['name'] for v in vertices if v['_type']=='UMLState'}!={v['name'] for v in en['literals']}:errors.append('Estados no coinciden con el atributo del dominio')
    nodes=[v for v in views if v['_type'] in node_types];edges=[v for v in views if 'points' in v and 'head' in v and 'tail' in v]
    for n in nodes:
        parent=ref(n.get('containerView'))
        if parent and (n['left']<parent['left']-2 or n['top']<parent['top']-2 or n['left']+n['width']>parent['left']+parent['width']+2 or n['top']+n['height']>parent['top']+parent['height']+2):errors.append('Elemento fuera del contenedor: '+name(n))
    def contained(a,b):
        cv=a.get('containerView')
        while cv:
            if cv['$ref']==b['_id']:return True
            cv=ref(cv).get('containerView')
        return False
    for i,a in enumerate(nodes):
        for bb in nodes[i+1:]:
            if not contained(a,bb) and not contained(bb,a) and intersects(a,bb,-3):errors.append('Nodos superpuestos: '+name(a)+' / '+name(bb))
    for e in edges:
        endpoints=[ref(e['head']),ref(e['tail'])]
        for n in nodes:
            if n['_id'] in [v['_id'] for v in endpoints] or any(contained(n,v) or contained(v,n) for v in endpoints):continue
            for (x,y),(xx,yy) in zip(pts(e),pts(e)[1:]):
                l=n['left']+3;r=n['left']+n['width']-3;t=n['top']+3;bot=n['top']+n['height']-3
                if (abs(x-xx)<.01 and l<x<r and min(max(y,yy),bot)>max(min(y,yy),t)) or (abs(y-yy)<.01 and t<y<bot and min(max(x,xx),r)>max(min(x,xx),l)):
                    errors.append('Línea atraviesa nodo: '+name(endpoints[0])+' / '+name(endpoints[1])+' -> '+name(n));break
    labels=[x for x in all_o if x['_type']=='EdgeLabelView' and x.get('visible',True) and x.get('text')]
    for i,a in enumerate(labels):
        if a.get('left',0)<0 or a.get('top',0)<0:errors.append('Etiqueta fuera de página: '+a.get('text',''))
        for bb in labels[i+1:]:
            if intersects(a,bb,1):warnings.append('Etiquetas cercanas: '+a.get('text','')+' / '+bb.get('text',''))
    reports.append({'archivo':str(file.relative_to(ROOT)),'tipo':d['_type'],'elementos':len(all_o),'errores':errors,'avisos':warnings})
    failures.extend(file.name+': '+e for e in errors)
counts=collections.Counter(r['tipo'] for r in reports)
expected={'UMLClassDiagram':1,'UMLUseCaseDiagram':1,'UMLComponentDiagram':1,'UMLDeploymentDiagram':1,'UMLCommunicationDiagram':26,'UMLObjectDiagram':26,'UMLStatechartDiagram':18}
if dict(counts)!=expected:failures.append('Cantidad de diagramas distinta de 74')
result={'total':len(reports),'tipos':dict(counts),'errores':failures,'archivos':reports}
Path(os.environ.get('SGCC_VALIDATION_REPORT',str(ROOT/'03_Revision/V4/Validacion_V4.json'))).write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('Diagramas:',len(reports),'Errores:',len(failures),'Avisos de etiquetas:',sum(len(r['avisos']) for r in reports))
for e in failures:print(e)
sys.exit(bool(failures))
