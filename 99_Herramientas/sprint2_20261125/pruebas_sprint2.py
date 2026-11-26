"""Genera el Word «Prueba integral del Sprint 2 del SGCP» (APA 7).

Uso: python3 pruebas_sprint2.py <salida.docx>

Desglosa el Sprint 2 del Excel (RF-04, RF-18, RF-17, RF-20, RNF-03, RNF-06) en 50 pasos para probarlo en la web.
Ayudantes de formato copiados de agilidad_20261123/agilidad_en_accion.py; el contenido está en contenido.py.
"""
import os, re, subprocess, sys, tempfile
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "patrones_20261105" / ".deps" / "python"))
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()
for name in ["Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "Header"]:
    st = doc.styles[name]; st.font.name = "Times New Roman"; st.font.size = Pt(12); st.font.color.rgb = RGBColor(0, 0, 0)
    st.font.bold = name in ["Title", "Heading 1", "Heading 2", "Heading 3"]; st.font.italic = name == "Heading 3"
    fonts = st.element.get_or_add_rPr().find(qn("w:rFonts"))
    if fonts is not None:
        for k in ["asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"]: fonts.attrib.pop(qn("w:" + k), None)
        for k in ["ascii", "hAnsi", "cs"]: fonts.set(qn("w:" + k), "Times New Roman")
    f = st.paragraph_format; f.space_before = f.space_after = Pt(0); f.line_spacing = 2; f.widow_control = True
    f.first_line_indent = Inches(0.5) if name == "Normal" else Inches(0)
    if name == "Heading 1": f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if name.startswith("Heading"): f.keep_with_next = True
lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "es-BO"); doc.styles["Normal"].element.get_or_add_rPr().append(lang)
s = doc.sections[0]
s.page_width, s.page_height = Inches(8.5), Inches(11)
s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)
s.different_first_page_header_footer = False
q = s.header.paragraphs[0]; q.alignment = WD_ALIGN_PARAGRAPH.RIGHT; q.paragraph_format.line_spacing = 1
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "1"; r.append(t); fld.append(r); q._p.append(fld)

def p(texto="", sangria=True, negrita=False, cursiva=False, centrado=False, interlineado=None):
    q = doc.add_paragraph(); q.paragraph_format.first_line_indent = Inches(0.5 if sangria else 0)
    if centrado: q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if interlineado: q.paragraph_format.line_spacing = interlineado
    # **negrita** y `código` dentro del texto
    for parte in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", texto):
        if not parte: continue
        if parte.startswith("**"): rr = q.add_run(parte[2:-2]); rr.bold = True
        elif parte.startswith("`"): rr = q.add_run(parte[1:-1]); rr.font.name = "Courier New"; rr.font.size = Pt(10.5)
        else: rr = q.add_run(parte); rr.bold = negrita
        rr.italic = cursiva or rr.italic
    return q
def salto():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
TITULOS = []
def h(texto, nivel=1):
    q = doc.add_heading(texto, nivel); TITULOS.append((nivel, texto)); return q
def vineta(texto):
    q = p(texto, False); q.paragraph_format.left_indent = Inches(0.5); q.paragraph_format.first_line_indent = Inches(-0.25)
    q.runs[0].text = "• " + q.runs[0].text if q.runs else None
    return q
NT = 0
def tabla(titulo, cab, filas, anchos, tam=10, nota=None):
    global NT
    NT += 1
    a = p(f"Tabla {NT}", False, True); a.paragraph_format.keep_with_next = True
    b = p(titulo, False, cursiva=True); b.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(cab)); t.autofit = False; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes = OxmlElement("w:tblBorders")
    for e in ["top", "bottom", "left", "right", "insideH", "insideV"]:
        x = OxmlElement("w:" + e); x.set(qn("w:val"), "single" if e in ("top", "bottom") else "nil"); x.set(qn("w:sz"), "6"); bordes.append(x)
    t._tbl.tblPr.append(bordes)
    # anchos fijos: LibreOffice usa tblGrid, Word usa tcW; se fijan los dos
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); t._tbl.tblPr.append(lay)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(sum(anchos) * 1440))); tw.set(qn("w:type"), "dxa")
    for viejo in t._tbl.tblPr.findall(qn("w:tblW")): t._tbl.tblPr.remove(viejo)
    t._tbl.tblPr.append(tw)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), anchos): gc.set(qn("w:w"), str(int(w * 1440)))
    for ri, vals in enumerate([cab] + filas):
        row = t.rows[0] if ri == 0 else t.add_row()
        pr = row._tr.get_or_add_trPr(); pr.append(OxmlElement("w:cantSplit"))
        if ri == 0: pr.append(OxmlElement("w:tblHeader"))
        for ci, (c, txt) in enumerate(zip(row.cells, vals)):
            c.width = Inches(anchos[ci]); c.text = ""
            if ri == 0:
                bs = OxmlElement("w:tcBorders"); e = OxmlElement("w:bottom"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6"); bs.append(e); c._tc.get_or_add_tcPr().append(bs)
            q = c.paragraphs[0]; q.paragraph_format.first_line_indent = Inches(0); q.paragraph_format.line_spacing = 1
            q.paragraph_format.space_before = q.paragraph_format.space_after = Pt(2)
            for parte in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", str(txt)):
                if not parte: continue
                negrita = parte.startswith("**")
                rr = q.add_run(parte[2:-2] if negrita else parte.strip("`")); rr.font.size = Pt(tam); rr.bold = ri == 0 or negrita
                if parte.startswith("`"): rr.font.name = "Courier New"; rr.font.size = Pt(tam - 1)
    if nota:
        q = p("", False); q.paragraph_format.line_spacing = 2; q.add_run("Nota. ").italic = True
        for parte in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", nota):
            if not parte: continue
            rr = q.add_run(parte[2:-2] if parte.startswith("**") else parte.strip("`")); rr.bold = parte.startswith("**")
            if parte.startswith("`"): rr.font.name = "Courier New"; rr.font.size = Pt(10.5)
    else:
        doc.add_paragraph().paragraph_format.line_spacing = 1
    return t


exec(open(AQUI / "contenido.py", encoding="utf-8").read())

def campo_toc(paginas):
    def run_fld(tipo):
        r = OxmlElement("w:r"); f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), tipo); r.append(f); return r
    parrafos = []
    for i, (nivel, texto) in enumerate(TITULOS):
        pp = OxmlElement("w:p"); ppr = OxmlElement("w:pPr")
        tabs = OxmlElement("w:tabs"); tb = OxmlElement("w:tab"); tb.set(qn("w:val"), "right"); tb.set(qn("w:leader"), "dot"); tb.set(qn("w:pos"), "9350"); tabs.append(tb); ppr.append(tabs)
        sp = OxmlElement("w:spacing"); sp.set(qn("w:line"), "360"); sp.set(qn("w:lineRule"), "auto"); sp.set(qn("w:before"), "0"); sp.set(qn("w:after"), "0"); ppr.append(sp)
        ind = OxmlElement("w:ind"); ind.set(qn("w:left"), str(0 if nivel == 1 else 360)); ind.set(qn("w:firstLine"), "0"); ppr.append(ind)
        pp.append(ppr)
        if i == 0:
            pp.append(run_fld("begin"))
            r = OxmlElement("w:r"); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = ' TOC \\o "1-2" \\h \\z \\u '; r.append(it); pp.append(r)
            pp.append(run_fld("separate"))
        r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = texto; r.append(t); pp.append(r)
        r = OxmlElement("w:r"); r.append(OxmlElement("w:tab")); pp.append(r)
        r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = str(paginas.get(texto, "")); r.append(t); pp.append(r)
        if i == len(TITULOS) - 1: pp.append(run_fld("end"))
        parrafos.append(pp)
    return parrafos

def guardar(paginas, ruta):
    padre = indice_p._p.getparent(); pos = padre.index(indice_p._p)
    viejos = getattr(guardar, "previos", [])
    for v in viejos: padre.remove(v)
    nuevos = campo_toc(paginas)
    for k, pp in enumerate(nuevos): padre.insert(pos + 1 + k, pp)
    guardar.previos = nuevos
    doc.core_properties.title = TITULO_DOC
    doc.core_properties.author = "Dario Haziel Tambo Parra; Angel Sebastian Eguez Mur; Sofia Cuellar Roca; Victor Manuel Manrique Arancivia"
    doc.core_properties.language = "es-BO"
    doc.save(ruta)

def paginas_reales(ruta):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, ruta], check=True, capture_output=True)
        pdf = os.path.join(d, Path(ruta).stem + ".pdf")
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
        txt = [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]
    pags = {}
    for nivel, titulo in TITULOS:
        clave = re.sub(r"\s+", " ", titulo)
        for i in range(3, n + 1):        # desde la página 3: 1 es portada, 2 el índice
            if any(re.sub(r"\s+", " ", l).strip() == clave for l in txt[i - 1].splitlines()):
                pags[titulo] = i; break
    return pags, n


salida = os.path.abspath(sys.argv[1])
pags = {t: 0 for _, t in TITULOS}
for vuelta in range(3):
    guardar(pags, salida)
    nuevas, n = paginas_reales(salida)
    faltan = [t for _, t in TITULOS if t not in nuevas]
    assert not faltan, faltan
    if nuevas == pags: break
    pags = nuevas
print(salida, n, "páginas;", len(TITULOS), "títulos en el índice")
