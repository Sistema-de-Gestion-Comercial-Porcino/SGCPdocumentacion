# Reportes por perfil · base de integración P1

Propuesta autorizada por Dario Haziel Tambo Parra el 7 de noviembre de 2026 para iniciar su parte de API. Pendiente revisión del equipo/P3, sin atribuirle una aprobación que no realizó.

| Perfil | Clientes | Cotizaciones | Pedidos | Producción | Inventario | Pagos | Entregas |
|---|---|---|---|---|---|---|---|
| Administración | Todos | Todas | Todos, costos y margen histórico | Toda | Todo | Todos | Todas |
| Ventas / cobranza | Todos | Todas | Todos, costos y margen histórico | No | No | Todos | Todas |
| Producción | No | No | No | Toda, sin importes | Todo, sin importes | No | No |
| Almacén | No | No | No | Toda, sin importes | Todo, sin importes | No | No |
| Responsable de entrega | No | No | No | No | No | No | Asignadas a su cuenta, sin importes |
| Comprador | No | Propias | Propios, sin costos ni márgenes | No | No | Propios | Propias |

No se agrega un actor Finanzas: el modelo vigente asigna cobranza a Ventas. Una persona puede asumir varias responsabilidades, pero COMPRADOR siempre conserva aislamiento por cliente. El mismo Facade autoriza consulta, PDF y Excel. Solicitar cliente ajeno devuelve 403; la exportación no incluye columnas sensibles ocultas.

El contrato de filtros y las rutas están en [README de API](../../SGCPapi/README.md). Almacén y reparto consultan pedidos operativos sin importes por una ruta aparte; eso no les concede el reporte comercial de pedidos.

La constancia definitiva incluye el saldo conservado al confirmar la recepción: solo administración/ventas o comprador propio. El responsable de entrega accede a su recepción y evidencias, sin saldo.
