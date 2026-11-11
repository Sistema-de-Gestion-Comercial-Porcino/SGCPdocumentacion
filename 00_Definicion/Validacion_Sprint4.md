# Validación del Sprint 4

Código de seguimiento: **S4-P3**. Responsable: Sofia Cuellar Roca, Parte 3. Fecha: 11 de noviembre de 2026 (hora de La Paz).

Los ocho casos están definidos en `Criterios_Sprint4.md`. El 11 de noviembre de 2026 los corrí contra la API y MySQL 8.0, con dos compradores distintos creados por el verificador. El Excel del comprador se abrió por dentro del archivo, incluidas las columnas, y no aparecieron costo ni margen.

| Caso | Resultado obtenido | Cumple |
|---|---|---|
| C4-01 Un comprador pide lo de otro | Pedir el reporte y el Excel del otro cliente respondió 403. | Sí. |
| C4-02 El archivo del comprador no trae costo ni margen | El Excel de sus pedidos no contiene «Costo» ni «Margen» en ninguna columna. | Sí. |
| C4-03 Producción pide pagos | El perfil de producción recibió 403 en el reporte de pagos. | Sí. |
| C4-04 El archivo trae las mismas filas que la pantalla | La consulta y la exportación salen de la misma tabla. El archivo del comprador se generó. No conté las filas a mano fuera del verificador. | Sí en la API. |
| C4-05 El margen reportado es el histórico | Administración ve la columna de margen histórico. El comprador no. El reporte no recalcula: lee lo guardado. | Sí. |
| C4-06 Constancia con recepción todavía en el teléfono | Sin recepción sincronizada la constancia responde `RECEPCION_PENDIENTE`. | Sí. |
| C4-07 Constancia de una entrega observada | La observada responde `RECEPCION_OBSERVADA`, distinto del caso anterior. | Sí. |
| C4-08 Segunda emisión, misma referencia | Las dos llamadas devolvieron el mismo registro, estado `SIN_PROVEEDOR`. | Sí. |

No cambié el código de la API. El Excel del proyecto no se modificó.
