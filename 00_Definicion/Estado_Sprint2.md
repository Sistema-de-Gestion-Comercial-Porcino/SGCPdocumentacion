# Estado del Sprint 2

Corte del informe: 17 de noviembre de 2026 (Bolivia).

## Implementado

| Repositorio | Qué quedó integrado en `main` | Referencia |
|---|---|---|
| SGCPapi | Producción e inventario: control sanitario, órdenes y previsiones, resultados por lote, pesajes, entradas físicas y reservas. | Commit `c87f823` (entrega de la API de los sprints 2 a 4). |
| SGCPuiweb | Pantallas de producción y almacén para operar los flujos del sprint. | PR #1, merge `c1bf7fb`. |

## Verificado y entorno

El 11 de noviembre, las pruebas V2-01 a V2-04 cumplieron contra la API con MySQL 8.0. La API registró los productos en lotes separados, sumó existencias al confirmar la entrada física, bloqueó el faeneo de un animal rechazado y rechazó una reserva sin existencia disponible. El [informe de validación](Validacion_Sprint2.md) detalla los resultados. La configuración regional de esa corrida quedó sin registrar.

La [entrega técnica de la API](Entrega_P1_Sprints234.md) documenta otra corrida automatizada en MySQL Community 8.4, en un contenedor temporal, con `LANG=es_BO.UTF-8` y `LANG=C`. En ambas configuraciones pasaron las 89 comprobaciones conjuntas de los sprints 2 a 4.

## Pendiente de verificar

- **Recorrido web completo.** Registrar un resultado de producción y confirmar el pesaje. Consultar las existencias antes y después de confirmar la entrada física en almacén para comprobar que solo la entrada suma el peso neto.
- **Cierre del sprint.** La etiqueta `v2.4.0` queda pendiente.

Al ejecutar el recorrido, registrar la fecha, las versiones de la web y la API, el motor de base de datos, la configuración regional, el resultado y el enlace a la evidencia.
