import json,subprocess,re,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
review=ROOT/'03_Revision/V4'
def inspect(p):
    info=subprocess.check_output(['pdfinfo',str(p)],text=True)
    assert re.search(r'Pages:\s+1\b',info),str(p)
    txt=subprocess.check_output(['pdftotext',str(p),'-'],text=True)
    assert len(txt.strip())>40,str(p)
    size=re.search(r'Page size:\s+([\d.]+) x ([\d.]+)',info)
    return {'archivo':str(p.relative_to(review)),'paginas':1,'texto':len(txt),'ancho':float(size[1]),'alto':float(size[2])}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(inspect,sorted(review.rglob('*.pdf'))))
assert len(rows)==74
(review/'PDF_Validados.json').write_text(json.dumps({'total':len(rows),'archivos':rows},indent=2))
manifest_path=review/'Manifiesto_V4.json';manifest=json.loads(manifest_path.read_text())
for row in rows:
    record=next(r for r in manifest['archivos'] if r['pdf']=='03_Revision/V4/'+row['archivo']);record['width']=row['ancho'];record['height']=row['alto']
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('PDF válidos:',len(rows))
