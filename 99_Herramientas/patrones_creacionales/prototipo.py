"""Prototipo didáctico aislado: valida creación de objetos; no implementa SGCC ni codifica PDF/XLSX."""
from abc import ABC,abstractmethod
from dataclasses import dataclass
from datetime import datetime,timedelta
from decimal import Decimal
from uuid import uuid4
import unittest,json,pathlib
@dataclass(frozen=True)
class ArchivoPrueba:
 formato:str
 filas:tuple
class ExportadorReporte(ABC):
 @abstractmethod
 def generar(self,datos):pass
class ExportadorPDF(ExportadorReporte):
 def generar(self,datos):return ArchivoPrueba('PDF',tuple(tuple(r)for r in datos))
class ExportadorExcel(ExportadorReporte):
 def generar(self,datos):return ArchivoPrueba('XLSX',tuple(tuple(r)for r in datos))
class ExportacionReporte(ABC):
 def exportar(self,datos):return self.crearExportador().generar(datos)
 @abstractmethod
 def crearExportador(self):pass
class ExportacionPDF(ExportacionReporte):
 def crearExportador(self):return ExportadorPDF()
class ExportacionExcel(ExportacionReporte):
 def crearExportador(self):return ExportadorExcel()
@dataclass(frozen=True)
class Cotizacion:
 id:str
 version:int
 estado:str
 vigenteHasta:datetime
@dataclass(frozen=True)
class DetallePedido:
 productoId:str
 cantidad:Decimal
 unidad:str
 precioAcordado:Decimal
 costoReferenciaAcordado:Decimal
@dataclass(frozen=True)
class Pedido:
 id:str
 cotizacionId:str
 detalles:tuple
 fechaComprometida:datetime
 condicionPago:str
 estadoComercial:str='CONFIRMADO'
 estadoPreparacion:str='PENDIENTE'
class PedidoBuilder:
 def __init__(self,ahora):self.ahora=ahora;self.cotizacion=None;self.detalles=[];self.fecha=None;self.pago=None
 def desdeCotizacion(self,aceptada):
  if aceptada.estado!='ACEPTADA' or aceptada.vigenteHasta<self.ahora:raise ValueError('Cotización no aceptada o vencida')
  self.cotizacion=aceptada;return self
 def agregarDetalle(self,datos):
  if not datos.productoId or datos.cantidad<=0 or not datos.unidad or datos.precioAcordado<0 or datos.costoReferenciaAcordado<0:raise ValueError('Detalle inválido')
  self.detalles.append(datos);return self
 def conFecha(self,fecha):self.fecha=fecha;return self
 def conPago(self,condicion):self.pago=condicion;return self
 def build(self):
  if self.cotizacion is None or not self.detalles or self.fecha is None or self.pago not in ['CONTADO','CREDITO_ACORDADO']:raise ValueError('Pedido incompleto')
  if self.fecha<self.ahora:raise ValueError('Fecha inválida')
  return Pedido(str(uuid4()),self.cotizacion.id,tuple(self.detalles),self.fecha,self.pago)
class Pruebas(unittest.TestCase):
 def setUp(self):
  self.now=datetime(2026,11,3,10);self.q=Cotizacion('COT-028',2,'ACEPTADA',self.now+timedelta(hours=2));self.d=DetallePedido('COS-KG',Decimal('4'),'kg',Decimal('35'),Decimal('28'))
 def builder(self):return PedidoBuilder(self.now).desdeCotizacion(self.q).agregarDetalle(self.d).conFecha(self.now+timedelta(days=1)).conPago('CONTADO')
 def test_01_factory_pdf(self):self.assertIsInstance(ExportacionPDF().crearExportador(),ExportadorPDF)
 def test_02_factory_excel(self):self.assertIsInstance(ExportacionExcel().crearExportador(),ExportadorExcel)
 def test_03_mismos_datos_ambos_formatos(self):
  datos=[['CLI-017','PED-042',Decimal('80')]];self.assertEqual(ExportacionPDF().exportar(datos).filas,ExportacionExcel().exportar(datos).filas)
 def test_04_extension_sin_cambiar_metodo_exportar(self):
  class ExportadorTexto(ExportadorReporte):
   def generar(self,datos):return ArchivoPrueba('TXT',tuple(datos))
  class ExportacionTexto(ExportacionReporte):
   def crearExportador(self):return ExportadorTexto()
  self.assertIs(ExportacionTexto.exportar,ExportacionReporte.exportar);self.assertEqual(ExportacionTexto().exportar([]).formato,'TXT')
 def test_05_no_altera_entrada(self):
  datos=[['PED-042',80]];result=ExportacionPDF().exportar(datos);datos[0][1]=0;self.assertEqual(result.filas[0][1],80)
 def test_06_pedido_con_dos_productos(self):
  b=self.builder().agregarDetalle(DetallePedido('LOM-KG',Decimal('2'),'kg',Decimal('40'),Decimal('31')));p=b.build();self.assertEqual(len(p.detalles),2);self.assertEqual(p.estadoPreparacion,'PENDIENTE')
 def test_07_rechazada_no_construye(self):
  with self.assertRaises(ValueError):PedidoBuilder(self.now).desdeCotizacion(Cotizacion('Q',1,'RECHAZADA',self.now+timedelta(hours=1)))
 def test_08_vencida_no_construye(self):
  with self.assertRaises(ValueError):PedidoBuilder(self.now).desdeCotizacion(Cotizacion('Q',1,'ACEPTADA',self.now-timedelta(minutes=1)))
 def test_09_sin_detalles_no_construye(self):
  with self.assertRaises(ValueError):PedidoBuilder(self.now).desdeCotizacion(self.q).conFecha(self.now).conPago('CONTADO').build()
 def test_10_cantidad_invalida(self):
  with self.assertRaises(ValueError):self.builder().agregarDetalle(DetallePedido('COS-KG',Decimal('-1'),'kg',Decimal('35'),Decimal('28')))
 def test_11_costo_y_precio_conservados(self):
  p=self.builder().build();margen=sum(d.cantidad*(d.precioAcordado-d.costoReferenciaAcordado)for d in p.detalles);self.assertEqual(margen,Decimal('28'))
 def test_12_resultado_independiente_del_builder(self):
  b=self.builder();p=b.build();b.detalles.clear();self.assertEqual(len(p.detalles),1)
 def test_13_estado_incompleto_no_visible(self):
  with self.assertRaises(ValueError):PedidoBuilder(self.now).desdeCotizacion(self.q).agregarDetalle(self.d).build()
 def test_14_sin_efectos_stock_pagos(self):
  p=self.builder().build();self.assertFalse(hasattr(p,'pagoRegistrado'));self.assertFalse(hasattr(p,'reserva'));self.assertEqual(p.estadoPreparacion,'PENDIENTE')
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Pruebas);r=unittest.TextTestRunner(verbosity=2).run(suite)
 out={'pruebas':r.testsRun,'fallos':len(r.failures),'errores':len(r.errors),'exito':r.wasSuccessful(),'alcance':'Prototipo aislado con dobles de exportación; no comprueba codificación PDF/XLSX, autenticación, persistencia ni concurrencia de SGCC.'}
 pathlib.Path('/tmp/sgcc_patrones_20261103').mkdir(parents=True,exist_ok=True)
 pathlib.Path('/tmp/sgcc_patrones_20261103/pruebas.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(not r.wasSuccessful())
