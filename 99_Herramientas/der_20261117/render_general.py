import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from gen_der import Page, check, png_page, drawio_full
from general import ENTS, RELS, ISA, CW, CH

MOD = {"A": ("#E3F2FD", "Acceso y seguridad (hoja 1)"), "C": ("#FFF8E1", "Comercial (hoja 2)"),
       "F": ("#FCE4EC", "Cobranza y facturación (hoja 3)"), "P": ("#E8F5E9", "Producción y pesaje (hojas 4 y 7)"),
       "I": ("#EDE7F6", "Inventario y frío (hoja 5)"), "E": ("#FFF3E0", "Entregas y sincronización (hoja 6)")}

def build_general(cells, rel_pos=None, isa_pos=None, reflex=None, card_offs=None, ent_shift=None):
    rel_pos = rel_pos or {}; card_offs = card_offs or {}; ent_shift = ent_shift or {}
    p = Page("0 Vista general", "DER SGCC · Vista general · 41 entidades y 59 relaciones (atributos en las hojas 1 a 7)")
    p.modules = [MOD[k] for k in "ACFPIE"]
    for k, (lab, m, weak) in ENTS.items():
        cx, cy = cells[k]; dx, dy = ent_shift.get(k, (0, 0))
        p.ent(k, lab, cx * CW + dx, cy * CH + dy, weak=bool(weak), fill=MOD[m][0])
    for name, a, ma, b, mb, ident in RELS:
        p.rel(name, a, ma, b, mb, ident=bool(ident), pos=rel_pos.get(name), card_off=card_offs.get(name, (0, -46)))
    sup, subs = ISA
    if isa_pos is None:
        xs = [p.ents[s]["x"] for s in subs]; ys = [p.ents[s]["y"] for s in subs]
        isa_pos = ((p.ents[sup]["x"] + sum(xs) / 2) / 2, (p.ents[sup]["y"] + sum(ys) / 2) / 2)
    p.isa_(sup, subs, isa_pos)
    if reflex:
        pos, anchors, coff = reflex
        p.rel("version_anterior", "COT", "0..1", "COT", "0..1", pos=pos, anchors=anchors, roles=("anterior", "nueva"), card_off=coff)
    return p

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    ov = {}
    if len(sys.argv) > 2:
        exec(open(sys.argv[2]).read(), ov)
    cells = {k: tuple(v) for k, v in data["cells"].items()}
    cells.update(ov.get("CELLS", {}))
    p = build_general(cells, ov.get("REL_POS"), ov.get("ISA_POS"), ov.get("REFLEX"), ov.get("CARD"), ov.get("SHIFT"))
    pr = check(p)
    print(len(pr)); [print("  ", x) for x in pr[:60]]
    png_page(p, os.path.join(here, "out", "DER_SGCC_0_Vista_general.png"), scale=1.25)
