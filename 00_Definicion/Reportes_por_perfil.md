# Reportes por perfil

Código de seguimiento: **S4-P3**. Decisión de Sofia Cuellar Roca, Product Owner. Fecha: 11 de noviembre de 2026 (hora de La Paz).

Revisé `Reportes_por_perfil_propuesta_P1.md`. La adopto. Esta página es la matriz oficial. Las celdas de abajo son las que usa la autorización: no queda ninguna vacía.

## Decisiones que cierran la ambigüedad

- **Finanzas no es un perfil.** En el reparto se nombra «finanzas»; en el sistema la cobranza es Ventas. No se crea un rol nuevo.
- **Ventas ve los pedidos de todos los clientes.** El sistema no asigna una cartera por vendedor. «Los que atiende» no existe y no se inventa.
- **El comprador manda sobre cualquier otro rol de la misma cuenta.** Si la cuenta es COMPRADOR, solo ve lo propio, aunque también tenga otro rol.
- **Producción y almacén no ven precios de venta, costos ni márgenes.** Ni en su reporte ni en el de otro.
- **El comprador no ve costos ni márgenes.** En ningún reporte y en ninguna exportación.
- Consulta, PDF y Excel salen de la misma tabla. El archivo no agrega columnas que la pantalla ocultó.
- Un reporte no modifica operaciones: no cambia estados ni recalcula importes. El margen de un pedido, cuando se muestra, es el histórico guardado al confirmar.

## Matriz

| Perfil | Clientes | Cotizaciones | Pedidos | Producción por producto y lote | Inventario | Pagos | Entregas |
|---|---|---|---|---|---|---|---|
| Administración | Todos: nombre, tipo, teléfono y si está activo | Todas, con total | Todos los clientes, con total, costo histórico y margen histórico | Toda, sin importes | Todo: físico, reservado y disponible, sin importes | Todos | Todas, sin precios |
| Ventas / cobranza | Todos: nombre, tipo, teléfono y si está activo | Todas, con total | Todos los clientes, con total, costo histórico y margen histórico | No | No | Todos | Todas, sin precios |
| Producción | No | No | No | Toda, sin importes: orden, producto, corte o derivado, familia, lote, cantidad real, unidad y estado | Todo, sin importes: producto, lote, físico, reservado, disponible, unidad, estado y vencimiento | No | No |
| Almacén | No | No | No | La misma tabla que producción, sin importes | La misma tabla que producción, sin importes | No | No |
| Responsable de entrega | No | No | No | No | No | No | Solo las asignadas a su usuario, sin precios. No ve las de otro responsable |
| Comprador | No | Solo las suyas, con total. Sin costo ni margen | Solo los suyos. Columnas: código, fecha, cliente, estado comercial, preparación y total. Sin costo y sin margen | No | No | Solo los suyos | Solo las suyas, sin precios |

Pedir el reporte de otro comprador, o un cliente que no es el de la cuenta, se rechaza. Producción que pida pagos, o almacén que pida el reporte comercial de pedidos, se rechaza: ese reporte no está en su fila.

Almacén y reparto pueden consultar el pedido operativo por la vía de preparación y despacho, sin importes. Eso no les abre la columna de pedidos de esta matriz.
