"""Comprobaciones aisladas de diseño; no implementa SGCP ni prueba red, SQLite o PDF reales."""
from dataclasses import dataclass
from html import escape
from copy import deepcopy
import json,unittest
from pathlib import Path
class MotorPDFPrueba:
 def renderizar(self,html):self.html=html;return html.encode()
class ExportadorPDF:
 def __init__(self,motor):self.motor=motor
 def generar(self,filas):return self.motor.renderizar('<table>'+''.join('<tr><td>'+escape(str(f))+'</td></tr>'for f in filas)+'</table>')
class FachadaRecepcion:
 def __init__(self):self.entregas={'E1':{'responsable':'U1','version':1,'estado':'EN_TRASLADO'}};self.resultados={}
 def registrar(self,d,usuario):
  actual=self.entregas[d['entrega']]
  if actual['responsable']!=usuario:raise PermissionError('Asignación')
  huella=json.dumps(d,sort_keys=True)
  if d['clave']in self.resultados:
   vieja,res=self.resultados[d['clave']]
   if vieja!=huella:raise ValueError('Clave con otro contenido')
   return deepcopy(res)
  if actual['version']!=d['version']or actual['estado']!='EN_TRASLADO':raise ValueError('Conflicto')
  res={'estado':'ENTREGADA'if d['conforme']else'OBSERVADA','constancia':d['conforme'],'version':actual['version']+1}
  actual.update(res);self.resultados[d['clave']]=(huella,deepcopy(res));return res
@dataclass(frozen=True)
class ComandoRecepcion:
 datos:dict
 api:object
 def ejecutar(self):return self.api.registrar(deepcopy(self.datos),'U1')
class EstadoEnvio:
 def manejar(self,e,autorizado=False):raise ValueError('Evento no permitido')
class Pendiente(EstadoEnvio):
 def manejar(self,e,autorizado=False):
  if e=='enviar':return Enviando()
  return super().manejar(e,autorizado)
class Enviando(EstadoEnvio):
 def manejar(self,e,autorizado=False):
  if e in ['fallo_red','sesion_vencida']:return Pendiente()
  if e=='confirmar':return Confirmada()
  if e=='conflicto':return Conflicto()
  return super().manejar(e,autorizado)
class Confirmada(EstadoEnvio):pass
class Descartada(EstadoEnvio):pass
class Conflicto(EstadoEnvio):
 def manejar(self,e,autorizado=False):
  if e=='descartar'and autorizado:return Descartada()
  return super().manejar(e,autorizado)
class Contado:
 def evaluar(self,d):return d['saldo']==0
class CreditoAcordado:
 def evaluar(self,d):return bool(d.get('autorizado')and d.get('vencimiento'))
def despachar(preparado,apto,politica,datos):return preparado and apto and politica.evaluar(datos)
class Pruebas(unittest.TestCase):
 def setUp(self):self.api=FachadaRecepcion();self.d={'clave':'K1','entrega':'E1','version':1,'conforme':True}
 def test_e01_adaptador_escape(self):
  m=MotorPDFPrueba();ExportadorPDF(m).generar(['<script>']);self.assertIn('&lt;script&gt;',m.html)
 def test_e02_adaptador_no_cambia_filas(self):
  filas=['costilla','lomo'];m=MotorPDFPrueba();ExportadorPDF(m).generar(filas);self.assertEqual(m.html.count('<tr>'),2);self.assertEqual(filas,['costilla','lomo'])
 def test_e03_fachada_no_duplica(self):
  a=self.api.registrar(self.d,'U1');b=self.api.registrar(self.d,'U1');self.assertEqual(a,b);self.assertEqual(self.api.entregas['E1']['version'],2)
 def test_e04_fachada_conflicto_sin_mutacion(self):
  self.d['version']=0
  with self.assertRaises(ValueError):self.api.registrar(self.d,'U1')
  self.assertEqual(self.api.entregas['E1']['version'],1);self.assertFalse(self.api.resultados)
 def test_e05_fachada_reevalua_autorizacion(self):
  self.api.registrar(self.d,'U1')
  with self.assertRaises(PermissionError):self.api.registrar(self.d,'U2')
 def test_e06_fachada_clave_con_otro_contenido(self):
  self.api.registrar(self.d,'U1');self.d['conforme']=False
  with self.assertRaises(ValueError):self.api.registrar(self.d,'U1')
 def test_b01_command_reintento_misma_clave(self):
  c=ComandoRecepcion(self.d,self.api);self.assertEqual(c.ejecutar(),c.ejecutar());self.assertEqual(list(self.api.resultados),['K1'])
 def test_b02_recepcion_observada_sin_constancia(self):
  self.d['conforme']=False;r=ComandoRecepcion(self.d,self.api).ejecutar();self.assertEqual(r['estado'],'OBSERVADA');self.assertFalse(r['constancia'])
 def test_b03_state_recupera_red(self):self.assertIsInstance(Pendiente().manejar('enviar').manejar('fallo_red'),Pendiente)
 def test_b04_state_conflicto_sin_reenvio(self):
  c=Enviando().manejar('conflicto')
  with self.assertRaises(ValueError):c.manejar('enviar')
  with self.assertRaises(ValueError):c.manejar('descartar',False)
  self.assertIsInstance(c.manejar('descartar',True),Descartada)
 def test_b05_state_terminal(self):
  with self.assertRaises(ValueError):Confirmada().manejar('enviar')
  with self.assertRaises(ValueError):Descartada().manejar('enviar')
 def test_b06_strategy_contado(self):self.assertFalse(Contado().evaluar({'saldo':50}));self.assertTrue(Contado().evaluar({'saldo':0}))
 def test_b07_strategy_credito(self):
  self.assertTrue(CreditoAcordado().evaluar({'saldo':50,'autorizado':True,'vencimiento':'2026-11-20'}));self.assertFalse(CreditoAcordado().evaluar({'autorizado':True}))
 def test_b08_strategy_no_omite_sanidad(self):self.assertFalse(despachar(True,False,Contado(),{'saldo':0}))
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Pruebas);result=unittest.TextTestRunner(verbosity=2).run(suite)
 out=Path('/tmp/sgcp_patrones_20261105');out.mkdir(exist_ok=True)
 (out/'pruebas.json').write_text(json.dumps({'total':result.testsRun,'estructurales':6,'comportamiento':8,'correctas':result.wasSuccessful(),'fallos':len(result.failures),'errores':len(result.errors),'limite':'Prototipo en memoria; no valida producción, concurrencia, red, persistencia real ni codificación PDF.'},ensure_ascii=False,indent=2));raise SystemExit(not result.wasSuccessful())
