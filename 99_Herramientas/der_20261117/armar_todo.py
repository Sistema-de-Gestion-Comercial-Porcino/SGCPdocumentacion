# Regenera el DER completo: hojas 1-7 (PNG), hoja 0 con atributos (PNG) y DER_SGCC.drawio con las 8 hojas.
# Uso: python3 -I armar_todo.py [carpeta_salida]   (por defecto ./out)
import sys, os
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "out")
os.makedirs(out, exist_ok=True)
g = {}; sys.argv = ["paginas.py"]
exec(open(os.path.join(here, "paginas.py")).read(), g)
import gen_der
for p in g["pages"]:
    assert not gen_der.check(p), p.name
    gen_der.png_page(p, os.path.join(out, "DER_SGCC_%s.png" % p.name.replace(" ", "_")))
import general_attrs
os.environ.setdefault("RAPIDO", "1")  # reutiliza attr_choice.json (la búsqueda completa: general_attrs.py sin RAPIDO)
p0 = general_attrs.main()
gen_der.png_page(p0, os.path.join(out, "DER_SGCC_0_Vista_general.png"), scale=1.0)
gen_der.drawio_full([p0] + g["pages"], os.path.join(out, "DER_SGCC.drawio"))
print("listo en", out)
