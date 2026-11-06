from pathlib import Path
import json,collections,hashlib
T=Path('/tmp/sgcc_reorganizacion_20261029');D=T/'Definicion';S=T/'Documentacion';D.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
spec=json.loads((T/'especificacion.json').read_text());casos=spec['casos'];exports=json.loads((T/'Exportacion_final.json').read_text());root=Path(__file__).resolve().parents[2]
rfmap={'CU01':['RF12'],'CU02':['RF13'],'CU03':['RF10'],'CU04':['RF02','RF03'],'CU05':['RF01','RF02'],'CU06':['RF01','RF03','RF05','RF19'],'CU07':['RF02','RF04'],'CU08':['RF04','RF18','RF20'],'CU09':['RF04'],'CU10':['RF05','RF06','RF11','RF19','RF20'],'CU11':['RF07','RF08','RF14','RF17','RNF01'],'CU12':['RF15']}
lines=['# Casos de uso del SGCC','', 'Doce objetivos generales. El CRUD y las alternativas son acciones internas. Todas las cuentas humanas se autentican; los permisos limitan acciones y datos. Numeración vigente desde la reorganización de octubre de 2026.','', '| CU | Nombre | Participantes | RF principales |','|---|---|---|---|']
for c in casos:lines.append('| '+c['id']+' | '+c['nombre']+' | '+', '.join(c['actors'])+' | '+', '.join(rfmap[c['id']])+' |')
for c in casos:
 lines.extend(['',f"## {c['id']} · {c['nombre']}",'',c['pre'],'',c['regla'],'','| Acción | Responsable | Condición | Si no se cumple |','|---|---|---|---|'])
 for a in c['branches']:lines.append('| '+' | '.join([a['nombre'],a['actor'],a['condicion'],a['alternativa']])+' |')
 lines.extend(['','Reagrupa: '+(', '.join(c['old'])if c['old']else'consultas y reportes de los módulos existentes')+'.'])
lines+=['','Las antiguas referencias CUxx deben leerse con la matriz de equivalencias. RF09, RF16 y RF21 quedan fuera de alcance activo. RF11 es condicional; no se fabrica una respuesta fiscal.']
(D/'Catalogo_casos_de_uso.md').write_text('\n'.join(lines)+'\n')
lines=['# Trazabilidad y equivalencias','', '| Caso vigente | Referencias anteriores | RF |','|---|---|---|']
for c in casos:lines.append('| '+c['id']+' '+c['nombre']+' | '+', '.join(c['old'])+' | '+', '.join(rfmap[c['id']])+' |')
lines+=['','Cada CU vigente posee un diagrama de secuencia, actividad, colaboración y objetos. Las máquinas de estados describen entidades con ciclo de vida; no se obliga a crear una por cada menú. Clases, casos de uso, componentes y despliegue son generales.','', 'Los reportes consultan datos de los módulos: producción por producto/corte/derivado, pedidos, clientes, inventario, pagos y entregas. RF15 agrupa las consultas y la exportación; RF04 cubre catálogo y producción. Las exportaciones vuelven a validar permisos.','', 'Los RF mantienen sus identificadores: 21 RF y 6 RNF. No existe correspondencia obligatoria de un RF con un solo CU. CU23 anterior (alertas) no se conserva como caso activo.','', '| Etapa | Acciones |','|---|---|','| Parametrización | Usuarios, clientes, clasificaciones, productos, costos; animales, ubicaciones y transportes en sus módulos. |','| Operación | Cotización aceptada, pedido, preparación, producción, stock, pagos, transporte y entrega. |','| Reportes | Filtros y exportación de información autorizada; comprador únicamente sus datos. |']
(D/'Matriz_trazabilidad.md').write_text('\n'.join(lines)+'\n')
(D/'Reglas_del_sistema.md').write_text('''# Reglas vigentes del SGCC

Seis actores humanos: Propietario / administración, Ventas / cobranza, Producción, Almacén, Responsable de entrega y Comprador. Una persona puede asumir varias responsabilidades. Todos se autentican; comprador se registra sin privilegios internos. Proveedor fiscal es una integración condicional. La balanza es una herramienta física: no existe actor ni interfaz informática de balanza.

El propietario administra el catálogo. ClasificacionProducto identifica familia y tipo (por ejemplo, CARNE_FRESCA / Costilla y DERIVADO / Jamón elaborado). Producto añade código, nombre, presentación, unidad y estado. Crear o editar un producto no crea existencia. Las desactivaciones conservan historia y revisan dependencias; no se elimina un producto usado.

OrdenProduccion se especializa en FaeneoDesposte y FabricacionDerivado. Cada orden obtiene cero o varios ResultadoProduccion, según su estado. Cada resultado corresponde a un lote y el lote a un producto con clasificación: el tipo se consulta por esa relación. Una sola orden de faeneo puede producir costilla y lomo en lotes diferentes. La fabricación selecciona el derivado del catálogo y registra insumos realmente consumidos. Los ejemplos de cortes, derivados, kilos, horas y precios son ilustrativos, no catálogo comercial ni rendimientos confirmados.

Producción identifica resultados; Almacén registra bruto, tara, neto, unidad y responsable. Resultado PENDIENTE_PESAJE no tiene cantidad real confirmada. Neto = bruto − tara, con unidad compatible. Resultado CONFIRMADO no equivale a ingreso de stock. La entrada física se registra una sola vez por referencia, lote y ubicación; también se permite recepción externa documentada. Disponible = físico apto − reservas activas. El consumo real se descuenta aunque se rechace el derivado; no se devuelve ficticiamente al stock.

La cotización vigente debe aceptarse antes del pedido. Rechazo conduce a cambios/nueva aceptación o cierre sin pedido. Faltantes consultan stock y órdenes vigentes antes de planificar otra; si no hay plazo viable se registra acuerdo o incidencia. Los tiempos previstos y reales se registran por orden; no se garantiza un tiempo fijo de faeneo. Control sanitario humano previo: rechazo bloquea animal/orden e inicia incidencia. El control de frío registra conservación o transporte, no temperatura corporal ni diagnóstico.

El propietario fija costo de referencia y precio por producto/unidad. El sistema conserva costo y precio históricos por detalle y calcula margen estimado; no distribuye automáticamente el costo del animal entre cortes. Productos y servicios acordados/prestados son conceptos separados. Seña solo con dinero recibido; cancelación exige acuerdo sin devolución o retención automática. Crédito conserva vencimiento acordado. Entrega y deuda son independientes.

Transportes propios o externos se identifican con código, transportista, contacto, vehículo, condiciones y estado. La ruta asocia transporte, responsable y entregas. Despacho exige preparación, existencia apta y pago/crédito resuelto. La recepción conforme confirmada habilita constancia; una observada queda para resolución. La ruta puede terminar con observación registrada sin cerrar su incidencia ni saldar deuda, siempre sin capturas pendientes de enviar.

Web online y Android Kotlin comparten API. Únicamente recepción de entregas asignadas, autorizadas y descargadas admite captura local Android. Clave única, versión base y evidencia se conservan en reintentos. El servidor confirma ENTREGADA u OBSERVADA según la recepción o informa conflicto para revisión autorizada. No hay operaciones comerciales, stock, cobros o control de frío offline. No se garantiza envío con la app cerrada ni respaldo central de datos todavía locales.

RF09 y RF16 son futuros; RF21 permanece pendiente, fuera de la entrega. RF11 depende de modalidad y proveedor fiscal confirmados. No se activa módulo de alertas. El nuevo Excel es copia de trabajo: el Excel ya entregado se conserva sin modificaciones y su bloque de versionamiento tampoco se cambia en la copia.
''')
# Keep the established offline policy and replace outdated references only.
(D/'Plataforma_y_operacion_sin_conexion.md').write_text((root/'00_Definicion/Plataforma_y_operacion_sin_conexion.md').read_text())
(D/'Fuentes_vigentes.md').write_text('''# Fuentes y decisiones vigentes

La base del negocio son los BPM corregidos por el compañero y la entrevista al propietario. Los BPM fueron actualizados por autorización del usuario para reflejar las correcciones de las dos asignaturas; las versiones vigentes están en [BPM vertical](../01_Proyecto_de_Sistemas/BPM_Vertical/). El original anterior se conserva en el respaldo de trabajo fuera de la entrega.

- [Entrevista al propietario](/home/supergenio/Escritorio/Tarea/entrevista_chancheria.md).
- [Documento comercial](</home/supergenio/Escritorio/Tarea/GestionComercialChancheriaGrupoB.docx>).
- [ASA1](<../ASA1 - Especificacion de Requerimientos - CRM Chancheria.docx>), con su estructura conservada.
- [Excel presentado](<../Formato Proyecto - SGCC 1 1.xlsx>), intacto.
- [Excel actualizado de trabajo](<../Formato Proyecto - SGCC Actualizado.xlsx>), alineado al ASA1; versionamiento sin cambios.
- Correcciones y alcance expresados por el usuario en la conversación: seis actores humanos, doce casos generales, cortes/derivados explícitos, CRUD interno, pesaje manual de Almacén, transporte y reportes.

La transcripción del audio descartada por el usuario no se usa como evidencia. Las decisiones de diseño no se atribuyen como nuevas respuestas de la entrevista. Catálogo definitivo, presentaciones, tiempos, rendimientos, equipos y proveedor fiscal requieren datos del negocio; los ejemplos no los sustituyen.

Los dos BPM verticales pertenecen a Proyecto de Sistemas y se mantienen fuera del PDF conjunto de Ingeniería de Software. [Índice de los 72 diagramas de software](../02_Ingenieria_de_Software/00_Documentacion/Indice_entrega.md).
''')
lines=['# Diccionario del modelo de clases','',f"Modelo general con {len(spec['defs'])} clases. Las clases de interfaz/control en secuencias y colaboración representan participantes de análisis; no son tablas del dominio.",'', 'Cadena del producto obtenido: OrdenProduccion → ResultadoProduccion → Lote → Producto → ClasificacionProducto. Una orden puede tener varios resultados. La previsión, el resultado real y la existencia física son conceptos diferentes.']
for n,data in spec['defs'].items():
 lines+=['',f'## {n}','', '| Atributo | Tipo |','|---|---|']
 for a in data[2]:an,at=a.split(':',1);lines.append(f'| {an} | {at} |')
 if len(data)>3:lines+=['','Operaciones: '+', '.join(data[3])+'.']
lines+=['','## Relaciones','', '| Origen | Destino | Multiplicidad origen / destino | Relación |','|---|---|---|---|']
for l in spec['links']:lines.append('| '+' | '.join([l[0],l[1],l[2]+' / '+l[3],('Composición'if len(l)>5 and l[5]=='composite'else'Agregación'if len(l)>5 and l[5]=='shared'else'Asociación')+(' · '+l[4]if len(l)>4 and l[4]else'')])+' |')
for a,b in spec['inheritance']:lines.append(f'| {a} | {b} | — | Herencia |')
lines+=['','Composición expresa propiedad exclusiva; no obliga a borrar historia comercial. Agregación de Ruta sobre Entrega permite reasignar una entrega. Las eliminaciones físicas deben respetar referencias y trazabilidad.','', 'Restricciones: código de producto y referencia de resultado únicos; lote asociado a un solo producto; unidad compatible; un resultado confirmado exige pesaje válido. Producto inactivo conserva operaciones. Transporte inactivo conserva rutas. Precio/costo acordados no se recalculan al cambiar vigencias.','', '## Enumeraciones','']
for n,l in spec['enums'].items():lines.append('- '+n+': '+', '.join(l)+'.')
(S/'Diccionario_clases.md').write_text('\n'.join(lines)+'\n')
# Export paths were staged; rewrite manifest to published, relative destinations.
for r in exports['archivos']:
 mdj=r['mdj'];r['mdj']='02_Ingenieria_de_Software/'+str(Path(mdj).relative_to(Path(mdj).parents[1])) if False else '02_Ingenieria_de_Software/'+ '/'.join(Path(mdj).parts[-2:])
(S/'Exportacion_final.json').write_text(json.dumps(exports,ensure_ascii=False,indent=2))
lines=['# Índice de entrega','', '[PDF conjunto](../PDFentrega/Diagramas_SGCC_Completo.pdf) · [PDF individuales](../PDFentrega/03_Revision/) · [MDJ agrupados y generales](../Entrega/).','', '72 diagramas únicos de Ingeniería de Software. Los cinco consolidados contienen los mismos diagramas individuales; no se duplican en el PDF. ASA1 es un PDF separado. Los dos BPM verticales están en Proyecto de Sistemas.','', '| Categoría | Páginas | Cantidad |','|---|---:|---:|']
for cat in exports['orden']:
 rr=[r for r in exports['archivos']if r['categoria']==cat];pp=str(rr[0]['pagina'])if len(rr)==1 else str(rr[0]['pagina'])+'–'+str(rr[-1]['pagina']);lines.append(f'| {cat} | {pp} | {len(rr)} |')
lines+=['','| Página | Diagrama | PDF individual |','|---:|---|---|']
for r in exports['archivos']:lines.append(f"| {r['pagina']} | [{Path(r['mdj']).stem}](../../{r['mdj']}) | [Abrir](../PDFentrega/{r['pdf']}) |")
(S/'Indice_entrega.md').write_text('\n'.join(lines)+'\n')
(S/'Criterios_de_revision.md').write_text('''# Revisión de la entrega

Se revisaron referencias e identificadores MDJ, tipos y asociaciones de objetos, enumeraciones y alcance de estados, diagramas predeterminados, geometría de nodos y conexiones, y carga con el motor nativo de StarUML. Los cinco consolidados conservan el contenido individual y muestran los diagramas directamente en su árbol.

Los BPM y BPMN se comprobaron por alcanzabilidad, salida final, guardas de decisiones y geometría. Las continuaciones con la misma letra/código pertenecen a un único flujo; los tramos son secciones visuales del mismo diagrama. Las ramas de rechazo llevan a corrección, incidencia, acuerdo o cierre según el caso.

Los PDF se generan desde los MDJ nativos, una página vectorial por diagrama, con marcadores en el conjunto. Se inspeccionaron muestras de casos de uso, clases, producción, actividades, colaboración, BPMN y documentos. Los archivos JSON de validación documentan los controles ejecutados.

El prototipo Balsamiq es SQLite BMPR nativo y mantiene enlaces internos válidos. La comprobación visual auxiliar del prototipo no equivale a ejecutar una aplicación ni a validar una implementación de software. Los botones navegan entre escenarios ilustrativos.

Las pruebas de negocio del ASA1 son criterios para implementar y aceptar el futuro sistema. No se afirma haber construido ni probado el backend, el sitio web o la app Android. Catálogo comercial, rendimientos y tiempos concretos quedan por validar con el negocio.
''')
for src,dest in [('Validacion_UML.json','Validacion_UML.json'),('Validacion_BPMN.json','Validacion_BPMN_horizontal.json'),('Validacion_nativa.json','Validacion_nativa.json'),('Validacion_Excel.json','Validacion_Excel.json')]:
 (S/dest).write_bytes((T/src).read_bytes())
(S/'Validacion_BPM_vertical.json').write_bytes(Path('/tmp/Validacion_BPM_vertical.json').read_bytes())
print('Catálogo, equivalencias, reglas, diccionario de',len(spec['defs']),'clases e índice de',len(exports['archivos']),'diagramas preparados.')
