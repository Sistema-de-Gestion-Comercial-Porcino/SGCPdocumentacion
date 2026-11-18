# Entrega técnica P1 · Sprints 2, 3 y 4

Dario Haziel Tambo Parra · 7 de noviembre de 2026 · SGCPapi.

Implementación local de S2-P1, S3-P1 y S4-P1 en la rama `trabajo/p1-sprints2-4`. No se realizaron commits, push, etiquetas ni PR; la integración y aprobación del equipo siguen pendientes. No se modifica SGCPuiweb ni SGCPuimovil ni se declara terminado el trabajo de P2/P3/P4.

## Qué se implementó

| Parte | API entregada | Patrón |
|---|---|---|
| S2-P1 | Animales, sanidad, órdenes y previsiones, resultados de cortes/derivados por lote, consumos idempotentes, pesajes, entradas físicas, reservas, frío, incidencias y cargos separados | Factory Method |
| S3-P1 | Condiciones de contado/crédito, pagos y señas, saldos por concepto, transportes, rutas, preparación/despacho, recepción con peso/evidencia, sincronización atómica y revisión humana de conflictos | Strategy |
| S4-P1 | Siete reportes por perfil, filtros, PDF/XLSX, constancia con evidencia y saldo histórico, registro fiscal pendiente sin proveedor | Facade y Adapter |

Builder del Sprint 1 se conserva. Command y State de Android corresponden a P2. El reparto dice seis patrones, pero su tabla enumera siete; no se agrega ningún patrón para llenar una lista.

## Cambios de la revisión

Se conservaron las correcciones previas de configuración regional y la separación de credenciales de ejecución/diseño de migraciones. No se volvió a SQL Server.

El contraste con el Excel completó lo omitido en la guía resumida: referencia del consumo, previsiones sin disponibilidad, peso/unidad de recepción, unidad del frío, cargos por servicios efectivamente prestados, cancelación de entrega preparada y saldo conservado en constancia. Los cargos por producto usan redondeo acumulado para coincidir con el total acordado aun con fracciones de kilo. El margen guardado no se recalcula.

Se cerró el acceso a precios comerciales desde catálogo para producción/almacén/entrega. Esos perfiles usan consultas operativas sin importes. El comprador no recibe costos ni márgenes. La constancia incluye saldo y queda para administración/ventas o comprador propio; reparto consulta recepción/evidencia sin saldo.

## Verificación ejecutada

Motor: MySQL Community 8.4 en contenedor temporal independiente, puerto local 3307, base aleatoria por ejecución. No se migró ni modificó la base habitual del usuario. El verificador elimina sus bases al terminar.

| Comprobación | Resultado |
|---|---|
| Compilación con `--warnaserror` | 0 advertencias, 0 errores |
| MySQL con `LANG=es_BO.UTF-8` | 27 del Sprint 1 + 89 de S2–S4 correctas |
| MySQL con `LANG=C` | 27 del Sprint 1 + 89 de S2–S4 correctas |
| Actualización de base Sprint 1 con pedido existente | Migraciones aplicadas dos veces; cargo Bs 80,50 y margen Bs 20,50 conservados |
| Base nueva | Todas las migraciones aplicadas dos veces, sin pendientes |
| SQLite, regresión Sprint 1 | 27 comprobaciones correctas; no sustituye MySQL |
| Consistencia modelo/migraciones | `has-pending-model-changes`: sin cambios |
| PDF y Excel | Generados por HTTP; XLSX inspeccionado para descartar columnas sensibles; PDF revisado visualmente |
| Volumen con es-BO | 2007 pedidos; 186 ms (API HTTP + JSON). |
| Volumen con C | 2007 pedidos; 228 ms (API HTTP + JSON). |

Se ejercitaron los rechazos sanitarios, múltiples cortes, previsiones sin stock, pesaje separado de entrada, consumo sin duplicación ni devolución ficticia, reserva sin disponibilidad, entrada duplicada/anulada, seña de uso único, acuerdo antes de cancelar, contado pendiente y crédito con vencimiento, entrega sin saldar deuda, peso y evidencia, rollback de lote inválido, reintentos simultáneos, conflictos revisados, rutas, acceso cruzado entre compradores, exportación sin costos/márgenes, constancia pendiente/observada y registro fiscal idempotente sin emisión.

La medida de volumen es local y técnica, no acredita RNF de usabilidad, desempeño en la máquina del docente ni funcionamiento Android en teléfono. El flujo de GitHub Actions quedó actualizado, pero no se ejecutó remotamente.

## Cómo integrar

1. Revisar los cambios locales de SGCPapi y los contratos del [README](../../SGCPapi/README.md).
2. Aplicar **todas** las migraciones con `dotnet ef database update --project src/SGCP.Api --context SgcpContext` usando la configuración del equipo. Los scripts incrementales y el esquema completo están en `SGCPapi/database/`.
3. Arrancar la API con `DatosIniciales:Habilitar=true` una vez para actualizar las seis responsabilidades sin reemplazar cuentas. Volver a iniciar sesión en los clientes para renovar su información de permisos.
4. P2 implementa web y Android contra Swagger, incluyendo `pesoRecibido`, `unidad`, `referenciaUnica` de consumo, evidencia y la cola Android. La descarga offline solo incluye entregas a domicilio; retiro local se registra online.
5. P3 revisa [reportes por perfil](Reportes_por_perfil_propuesta_P1.md) y [decisiones autorizadas por Dario](Decisiones_P1_Sprints234.md), sin dar por aprobada una revisión que todavía no hizo.
6. P4 adapta diagramas/diccionario y prepara PR, versión y entrega. No se modificaron esos archivos por cuenta de otro integrante.

Los nombres del reparto implementados necesitan reflejarse en los diagramas de P4: `CargoPedido` se concreta como `Cargo`; `ConsumoInsumo`, como `InsumoProduccion`; `AcuerdoCredito`, como `CondicionPago`; faeneo/fabricación usan `OrdenProduccion.Tipo` y fábricas; la captura y su evidencia se conservan en `Recepcion` y `EvidenciaRecepcion`, separadas de `Entrega`. `PrevisionProducto` registra cantidades estimadas que nunca se reservan.

## Límites acordados

- RF-11 no emite comprobantes fiscales: no hay proveedor ni modalidad confirmados. Conserva referencia, estado SIN_PROVEEDOR y motivo, sin simular factura.
- Una entrega completa por pedido; sin entregas parciales. Una entrada física por lote/producto; una ubicación textual por existencia; sin transferencias entre cámaras en este alcance.
- La API no detecta capturas que nunca salieron del teléfono. P2 debe bloquear el cierre de ruta mientras exista cola local pendiente. No hay escritura offline de stock, cobros, sanidad o producción.
- Una seña aplicada conserva su aplicación al registrar un acuerdo de resolución. No se ejecutan automáticamente devoluciones ni retenciones; la cancelación mantiene el historial monetario.
- No se inventan rendimientos de animales, tiempos estándar de faeneo ni costos de producción automáticos. Se registran estimaciones y hechos reales.
- Quedan por hacer la integración de pantallas, pruebas de dispositivo, validación humana, adecuación documental de P4 y revisión/aprobación del equipo. La entrega de P1 no equivale al cierre de los sprints completos.
