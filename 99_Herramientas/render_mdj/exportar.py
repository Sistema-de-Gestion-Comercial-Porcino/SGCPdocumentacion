"""Exporta .mdj a SVG/PDF/PNG sin StarUML. Uso:
python3 exportar.py <salida_dir> <archivo.mdj>... [--png]
Un PDF por diagrama: <nombre del archivo>.pdf (o <archivo>__<n>.pdf si tiene varios).
"""
import json, os, subprocess, sys, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import diagramas, indice, svg_de

def exportar(mdjs, salida, png=False):
    os.makedirs(salida, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="mdj_svg_")
    hechos = []
    for f in mdjs:
        d = json.load(open(f, encoding="utf-8"))
        ids = indice(d)
        ds = diagramas(d)
        base = os.path.splitext(os.path.basename(f))[0]
        for i, dg in enumerate(ds):
            svg, w, h = svg_de(dg, ids)
            nombre = base if len(ds) == 1 else f"{base}__{i+1:02d}"
            p = os.path.join(tmp, nombre + ".svg")
            open(p, "w", encoding="utf-8").write(svg)
            hechos.append((nombre, p))
    svgs = [p for _, p in hechos]
    for i in range(0, len(svgs), 40):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf:draw_pdf_Export", "--outdir", salida] + svgs[i:i+40],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1200)
        if png:
            subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", salida] + svgs[i:i+40],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1200)
    shutil.rmtree(tmp)
    return [n for n, _ in hechos]

if __name__ == "__main__":
    png = "--png" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--png"]
    print(exportar(args[1:], args[0], png))
