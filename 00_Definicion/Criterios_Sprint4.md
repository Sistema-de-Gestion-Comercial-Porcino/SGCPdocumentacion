# Criterios del Sprint 4

Código de seguimiento: **S4-P3**. Responsable: Sofia Cuellar Roca, Parte 3. Fecha: 11 de noviembre de 2026 (hora de La Paz).

La matriz de quién ve cada reporte está en `Reportes_por_perfil.md`. La decisión de no emitir RF-11 está en `Decisiones.md`. Aquí están los casos de RF-14 y RF-15. El resultado de ejecutarlos está en `Validacion_Sprint4.md`.

## C4-01 · Un comprador no ve lo de otro

- **Dado** dos compradores, cada uno con sus pedidos.
- **Cuando** el primero pide el reporte de pedidos del segundo.
- **Entonces** el sistema lo rechaza. No devuelve filas del otro, ni en pantalla ni en el archivo.

## C4-02 · La exportación del comprador no trae costo ni margen

- **Dado** un comprador con un pedido propio que tiene costo y margen guardados.
- **Cuando** exporta sus pedidos a Excel y a PDF.
- **Entonces** el archivo trae sus filas y no tiene columna de costo ni de margen. Hay que revisar también las columnas de la derecha.

## C4-03 · Producción no consulta pagos

- **Dado** un usuario con perfil de producción, sin otro rol.
- **Cuando** pide el reporte de pagos.
- **Entonces** ese reporte no está disponible para ese perfil.

## C4-04 · La exportación trae las mismas filas que la pantalla

- **Dado** un filtro de pedidos de un mes, con un resultado visible en pantalla.
- **Cuando** se exporta ese mismo filtro.
- **Entonces** el archivo trae las mismas filas, ni una más ni una menos.

## C4-05 · El margen reportado es el histórico

- **Dado** un pedido confirmado con margen histórico de Bs 28, y un precio de catálogo cambiado después.
- **Cuando** se consulta y se exporta el reporte de ese pedido.
- **Entonces** el margen que aparece es Bs 28. No se recalcula con el precio nuevo.

## C4-06 · No hay constancia si la recepción no está en el servidor

- **Dado** una entrega cuya recepción sigue pendiente de sincronizar.
- **Cuando** se pide la constancia.
- **Entonces** se rechaza. Una captura que solo está en el teléfono no alcanza.

## C4-07 · No hay constancia de una entrega observada

- **Dado** una entrega en estado OBSERVADA, ya sincronizada.
- **Cuando** se pide la constancia.
- **Entonces** se rechaza, con un motivo distinto al de C4-06: aquí la recepción sí llegó, pero no fue conforme.

## C4-08 · La segunda emisión no crea otra referencia

- **Dado** un pedido que ya tiene una operación fiscal registrada, con su referencia única.
- **Cuando** se intenta emitir otra vez el comprobante de ese pedido.
- **Entonces** la segunda respuesta es el mismo registro y la misma referencia. No crea una nueva.

Con la decisión vigente, esa referencia es la de la operación sin proveedor. No es un número fiscal.
