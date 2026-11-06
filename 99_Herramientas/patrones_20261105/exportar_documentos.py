"""Actualiza índices y exporta mediante LibreOffice; solo los archivos recibidos."""
from pathlib import Path
import sys,time,subprocess,json
import uno
from com.sun.star.beans import PropertyValue
TMP=Path('/tmp/sgcp_patrones_20261105');TMP.mkdir(exist_ok=True)
def prop(n,v):p=PropertyValue();p.Name=n;p.Value=v;return p
port=20115
log=open(TMP/'libreoffice.log','w')
proc=subprocess.Popen(['libreoffice','-env:UserInstallation=file:///tmp/sgcp_patrones_20261105/lo','--headless','--norestore','--nodefault','--nofirststartwizard',f'--accept=socket,host=127.0.0.1,port={port};urp;StarOffice.ServiceManager'],stdout=log,stderr=log)
try:
 local=uno.getComponentContext();resolver=local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',local)
 for attempt in range(120):
  try:ctx=resolver.resolve(f'uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext');break
  except Exception:time.sleep(.25)
 else:raise RuntimeError('LibreOffice no respondió')
 desktop=ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',ctx)
 for arg in sys.argv[1:]:
  path=Path(arg).resolve();doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(path)),'_blank',0,(prop('Hidden',True),prop('UpdateDocMode',3)))
  if not doc:raise RuntimeError('No se abrió '+str(path))
  if doc.Bookmarks.hasByName('indice')and doc.DocumentIndexes.Count==0:
   anchor=doc.Bookmarks.getByName('indice').Anchor;idx=doc.createInstance('com.sun.star.text.ContentIndex');idx.Title='Índice';idx.CreateFromOutline=True;idx.Level=2;doc.Text.insertTextContent(anchor,idx,False)
  styles=doc.StyleFamilies.getByName('ParagraphStyles')
  for name in ['Contents Heading','Contents 1','Contents 2']:
   if styles.hasByName(name):
    st=styles.getByName(name);st.CharFontName='Times New Roman';st.CharHeight=12.;st.ParaTopMargin=0;st.ParaBottomMargin=0
    spacing=uno.createUnoStruct('com.sun.star.style.LineSpacing');spacing.Mode=0;spacing.Height=200;st.ParaLineSpacing=spacing
    if name=='Contents Heading':st.CharWeight=150.;st.ParaAdjust=3
  doc.refresh()
  for i in range(doc.DocumentIndexes.Count):doc.DocumentIndexes.getByIndex(i).update()
  doc.refresh()
  for i in range(doc.DocumentIndexes.Count):doc.DocumentIndexes.getByIndex(i).update()
  # Store the populated Word index, not only its PDF rendering.
  doc.store();pdf=path.with_suffix('.pdf');doc.storeToURL(uno.systemPathToFileUrl(str(pdf)),(prop('FilterName','writer_pdf_Export'),prop('Overwrite',True)))
  print(json.dumps({'word':str(path),'pdf':str(pdf),'indices':doc.DocumentIndexes.Count,'paginas':doc.CurrentController.PageCount},ensure_ascii=False),flush=True)
  doc.close(True)
 desktop.terminate()
finally:
 try:proc.wait(timeout=8)
 except subprocess.TimeoutExpired:proc.terminate()
 log.close()
