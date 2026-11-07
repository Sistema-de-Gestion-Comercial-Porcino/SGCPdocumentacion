# Decisiones de integración P1 · 7 de noviembre de 2026

Dario Haziel Tambo Parra autorizó implementar su parte de los sprints 2, 3 y 4 primero, y que sus compañeros integren/revisen esa base posteriormente. Alcance: SGCPapi; no se completa ni se aprueba el trabajo de P2, P3 o P4 en su nombre.

## Fiscal

Dario confirmó que todavía no hay proveedor fiscal. Se entrega Adapter y registro de operación SIN_PROVEEDOR, con referencia única y sin número ni comprobante fiscal. No se declara RF-11 emitido o integrado. Si aparece proveedor se necesitarán modalidad, contrato técnico, credenciales externas y pruebas reales; no se deducen del código actual.

## Reportes

Se adoptan los seis actores vigentes y la [matriz por perfil](Reportes_por_perfil_propuesta_P1.md). La mención a «finanzas» en el reparto se interpreta como Ventas/cobranza; no se modifica el reparto original de los compañeros.

## Android y sincronización

Contrato propuesto por P1 y autorizado por Dario para que P2 lo consuma: lote de hasta 20 recepciones, UUID por captura generado en Android, versión base, autor autenticado, fecha real UTC, receptor, peso recibido con unidad, observación y evidencia JPEG/PNG en el mismo envío. Hasta tres imágenes de 512 KiB por captura y 12 MiB por solicitud; el teléfono reduce imágenes y divide lotes si hace falta.

Se guarda todo el lote atómicamente. Reintentar conserva claves y contenido y devuelve la recepción existente. Conflictos conservan captura/evidencia sin sobrescribir entrega; un usuario autorizado aplica o descarta con motivo. Un 409 de concurrencia se reintenta con las mismas claves. Fecha de captura y sincronización son distintas. La recepción conforme habilita constancia; observada no. Entrega y deuda son independientes.

La API solo entrega al responsable sus entregas despachadas y autorizadas. P2 implementará descarga, almacenamiento local, estados de cola, reintentos y experiencia móvil. No se afirma que Android ya tenga estas funciones.

La descripción completa y JSON del contrato están en [README de API](../../SGCPapi/README.md). No hubo contacto ni aprobación atribuida a Sofía o Sebastián: esta es la base que Dario pidió dejarles para revisión.

## Precisión al contrastar con el Excel

El reparto resumido no incluía todos los campos del requisito original. P1 incorpora además previsiones por producto sin stock, referencia única de consumo, peso/unidad de recepción, unidad °C del control de frío, acuerdo y fecha de servicio prestado para cargos, y saldo histórico en constancia. Se mantiene historial de entrega CANCELADA cuando el pedido se cancela antes del despacho.

La constancia contiene saldo histórico y, por tanto, se limita a administración/ventas y comprador propio; el responsable de entrega consulta recepción/evidencia sin importes. El retiro local se registra online en la web con el mismo contrato; no se descarga como entrega offline Android. La API no puede saber si un teléfono conserva capturas nunca enviadas: P2 debe impedir el cierre de ruta mientras tenga cola local pendiente.

El reparto dice «seis patrones» pero enumera siete: cinco en API (incluido Builder previo) y Command/State en Android. Esta entrega no cambia los documentos de asignación ni declara completados esos dos patrones de P2.
