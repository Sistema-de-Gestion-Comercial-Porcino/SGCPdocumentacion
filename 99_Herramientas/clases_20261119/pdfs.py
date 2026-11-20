"""Regenera los PDF de entrega con render_mdj (sin la exportación de StarUML) y el índice.

Uso: python3 pdfs.py <02_Ingenieria_de_Software>
"""
import glob, os, subprocess, sys
RAIZ = os.path.abspath(sys.argv[1])
REND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render_mdj")
REV = os.path.join(RAIZ, "PDFentrega", "03_Revision")
ind = lambda c: sorted(f for f in glob.glob(os.path.join(RAIZ, c, "*.mdj")) if not f.endswith("_Completo.mdj"))
G = [("01_Casos_de_Uso", "Casos de uso", [os.path.join(RAIZ, "01_Generales", "Casos_de_Uso_SGCC.mdj")]),
     ("02_Secuencias", "Secuencias", ind("06_Secuencias")),
     ("03_Clases", "Clases", [os.path.join(RAIZ, "01_Generales", "Clases_SGCC.mdj")]),
     ("04_Actividades", "Actividades", ind("05_Actividades")),
     ("05_Estados", "Estados", ind("04_Estados")),
     ("06_Colaboracion", "Colaboración", ind("02_Colaboracion")),
     ("07_Componentes", "Componentes", [os.path.join(RAIZ, "01_Generales", "Componentes_SGCC.mdj")]),
     ("08_Despliegue", "Despliegue", [os.path.join(RAIZ, "01_Generales", "Despliegue_SGCC.mdj")]),
     ("09_Objetos", "Objetos", ind("03_Objetos")),
     ("10_BPMN_Horizontal", "BPMN horizontal", ind("BPMN_Horizontal"))]
orden = []
for carpeta, _, fuentes in G:
    dst = os.path.join(REV, carpeta); os.makedirs(dst, exist_ok=True)
    esperados = {os.path.splitext(os.path.basename(f))[0] + ".pdf" for f in fuentes}
    for viejo in os.listdir(dst):
        if viejo.endswith(".pdf") and viejo not in esperados:
            os.remove(os.path.join(dst, viejo)); print("quitado", carpeta, viejo)
    subprocess.run([sys.executable, "exportar.py", dst] + fuentes, cwd=REND, check=True, stdout=subprocess.DEVNULL)
    for f in fuentes:
        pdf = os.path.join(dst, os.path.splitext(os.path.basename(f))[0] + ".pdf")
        assert os.path.getsize(pdf) > 1000, pdf
        orden.append((carpeta, f, pdf))
salida = os.path.join(RAIZ, "PDFentrega", "Diagramas_SGCC_Completo.pdf")
subprocess.run(["pdfunite"] + [p for _, _, p in orden] + [salida], check=True)
# índice
rel = lambda p: os.path.relpath(p, os.path.join(RAIZ, "00_Documentacion"))
L = ["# Índice de entrega", "",
     "[PDF conjunto](../PDFentrega/Diagramas_SGCC_Completo.pdf) · [PDF individuales](../PDFentrega/03_Revision/) · [MDJ agrupados y generales](../Entrega/).", "",
     f"{len(orden)} diagramas únicos de Ingeniería de Software, renderizados desde los .mdj con `99_Herramientas/render_mdj` "
     "(sin la exportación de StarUML). Los cinco consolidados contienen los mismos diagramas individuales; no se duplican en el PDF. "
     "El DER está en `DER/` (DER_SGCC.drawio y un PNG por hoja). ASA1 es un PDF separado.", "",
     "| Categoría | Páginas | Cantidad |", "|---|---:|---:|"]
pag = 1
for carpeta, nombre, fuentes in G:
    n = len(fuentes); L.append(f"| {nombre} | {pag}{'–' + str(pag + n - 1) if n > 1 else ''} | {n} |"); pag += n
L += ["", "| Página | Diagrama | PDF individual |", "|---:|---|---|"]
for i, (carpeta, f, pdf) in enumerate(orden, 1):
    L.append(f"| {i} | [{os.path.splitext(os.path.basename(f))[0]}]({rel(f)}) | [Abrir]({rel(pdf)}) |")
open(os.path.join(RAIZ, "00_Documentacion", "Indice_entrega.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(orden), "PDF;", salida)
