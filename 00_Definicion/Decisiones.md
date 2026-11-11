# Decisiones de la Parte 3

## RF-11 · 11 de noviembre de 2026

La toma Sofia Cuellar Roca, Product Owner. El docente todavía no la confirmó en esta fecha. La decisión de trabajo queda tomada igual, para que el Sprint 4 no se quede esperando.

**RF-11 no se emite.** No hay modalidad fiscal ni proveedor confirmados. El Excel lo condiciona a eso. Sin proveedor, integrar una emisión sería inventar un servicio que no existe.

Lo que sí queda, y ya está en la API:

- El punto de integración es el Adapter `ProveedorFiscalNoConfiguradoAdapter`.
- Registrar la operación de un pedido confirmado guarda estado `SIN_PROVEEDOR`, número fiscal vacío y la referencia única `FIS-` seguida del identificador del pedido.
- La respuesta dice que la operación comercial quedó registrada sin comprobante fiscal.
- Un segundo intento del mismo pedido devuelve ese mismo registro. No crea otra referencia.
- La venta sigue su curso sin comprobante, como dice el Excel mientras la emisión no esté habilitada.

Esto no declara RF-11 cumplido. Declara el diseño y el motivo por el que no se emite.

Si el docente después confirma un proveedor, hacen falta la modalidad, los datos de conexión y qué devuelve. Con eso se reemplaza el Adapter. Hasta entonces no se piden credenciales ni se simula un número fiscal.

La nota de Darío del 7 de noviembre de 2026, en `Decisiones_P1_Sprints234.md`, dice lo mismo: no hay proveedor. Esta página es la decisión de la Parte 3 sobre esa base.
