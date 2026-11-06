from playwright.sync_api import sync_playwright
from pathlib import Path
import json,datetime
out=Path('/tmp/sgcp-sprint1/visual');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage','--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:5080');page.screenshot(path=str(out/'01-acceso.png'),full_page=True)
 page.get_by_label('Usuario',exact=True).fill('admin');page.get_by_label('Contraseña',exact=True).fill('Prueba-local-2026!');page.get_by_role('button',name='Ingresar',exact=False).click();page.wait_for_url('http://localhost:5080/')
 page.screenshot(path=str(out/'02-resumen.png'),full_page=True)
 pages=['Usuarios','Clientes','Productos','Clasificaciones','Precios','Cotizaciones','Pedidos','Usuarios/Formulario','Clientes/Formulario','Productos/Formulario','Clasificaciones/Formulario','Cotizaciones/Formulario']
 for ruta in pages:
  res=page.goto('http://localhost:5080/'+ruta)
  assert res.status==200,(ruta,res.status,page.locator('body').inner_text()[:500])
 print('Pantallas GET:',len(pages),'correctas',flush=True)
 page.goto('http://localhost:5080/Clientes/Formulario')
 page.get_by_label('Nombre o razón comercial').fill('Restaurante El Patio')
 page.get_by_label('Teléfono').fill('70001234')
 page.get_by_label('Tipo de cliente').select_option('Restaurante')
 page.get_by_role('button',name='Guardar cambios').click();page.wait_for_load_state('networkidle');print('CLIENTE:',page.url,page.locator('.validation').all_text_contents(),flush=True);page.wait_for_url('**/Clientes')
 assert page.get_by_text('Restaurante El Patio',exact=True).count()==1
 page.goto('http://localhost:5080/Precios');page.get_by_role('row').filter(has_text='PRD-001').get_by_role('link',name='Ver vigencias').click();page.get_by_role('link',name='Nueva vigencia').click()
 page.get_by_label('Costo de referencia').fill('28');page.get_by_label('Precio de venta').fill('35');page.get_by_label('Vigente desde').fill('2026-11-05T10:00')
 page.get_by_role('button',name='Guardar cambios').click();page.wait_for_url('**/Precios/Historial/*')
 page.goto('http://localhost:5080/Cotizaciones/Formulario')
 page.get_by_label('Cliente',exact=True).select_option(label='Restaurante El Patio')
 page.locator('.producto-select').select_option(label='Costilla de cerdo · Pieza')
 page.get_by_label('Cantidad',exact=True).fill('4');page.get_by_role('button',name='Guardar borrador').click();page.wait_for_url('**/Cotizaciones/Detalle/*')
 page.get_by_role('button',name='Presentar cotización').click();page.wait_for_load_state('networkidle')
 page.get_by_role('link',name='Registrar aceptación').click();page.get_by_role('button',name='Confirmar operación').click();page.wait_for_url('**/Cotizaciones/Detalle/*')
 page.screenshot(path=str(out/'03-cotizacion.png'),full_page=True)
 page.get_by_role('link',name='Crear pedido confirmado').click();page.get_by_role('button',name='Confirmar pedido').click();page.wait_for_url('**/Pedidos/Detalle/*')
 assert 'Bs 28.00' in page.locator('.margin-card').inner_text(),page.locator('.margin-card').inner_text()
 page.screenshot(path=str(out/'04-pedido.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.goto('http://localhost:5080/');page.screenshot(path=str(out/'05-movil.png'),full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),'Desbordamiento horizontal'
 page.get_by_role('button',name='Abrir navegación').click();page.wait_for_timeout(300);assert page.locator('#navegacion').evaluate("e=>e.getBoundingClientRect().left")>=-1
 page.keyboard.press('Escape');page.wait_for_timeout(250)
 page.goto('http://localhost:5080/Productos');assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
 page.screenshot(path=str(out/'06-productos-movil.png'),full_page=True)
 assert not errors,errors
 print('Recorrido web: acceso → cliente → vigencia → cotización → aceptación → pedido, margen Bs 28; móvil sin desbordamiento. Sin errores JS.',flush=True)
 (out/'resultado.json').write_text(json.dumps({'pantallas':len(pages),'recorrido_comercial':True,'movil':True,'errores_js':errors},indent=2))
 browser.close()
