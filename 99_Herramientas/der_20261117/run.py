import sys, os
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
exec(open(os.path.join(here, "paginas.py")).read())
from gen_der import check, png_page, drawio_full
out = sys.argv[1] if len(sys.argv) > 1 else here + "/out"
os.makedirs(out, exist_ok=True)
tot = 0
for i, p in enumerate(pages):
    pr = check(p); tot += len(pr)
    print("==", p.name, len(pr))
    for x in pr[:40]: print("   ", x)
    png_page(p, os.path.join(out, "DER_SGCC_%s.png" % p.name.replace(" ", "_")))
drawio_full(pages, os.path.join(out, "DER_SGCC.drawio"))
print("total", tot)
