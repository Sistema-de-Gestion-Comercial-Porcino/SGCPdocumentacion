# Validación del Sprint 2

Código de seguimiento: **S2-P3**. Responsable: Sofia Cuellar Roca, Parte 3. Fecha del guion: 11 de noviembre de 2026 (hora de La Paz).

El criterio del Excel:

> Una orden produce costilla y lomo en lotes distintos. Confirmar peso no suma stock; entrada física sí. Rechazo bloquea; consumo de derivado rechazado no se revierte por ficción. No se reservan previsiones.

Este guion es el criterio. El 11 de noviembre de 2026 lo corrí contra la API ya entregada, con el verificador del repositorio y MySQL 8.0. Pasaron las 89 comprobaciones de los sprints 2 a 4. Abajo queda solo lo que corresponde a cada prueba. No cambié el código de la API.

El archivo `Formato Proyecto - SGCC Actualizado.xlsx` no se modificó.

## V2-01 · Una orden produce varios productos en lotes distintos

| Campo | Contenido |
|---|---|
| Requerimiento | RF-04 |
| Precondición | Hay un animal apto, con control sanitario aprobado. Existen los productos Costilla de cerdo y Lomo, unidad kg. |
| Pasos | 1. Crear una orden de faeneo para ese animal. 2. Confirmar dos resultados: costilla, lote propio, 8,000 kg; lomo, otro lote, 5,000 kg. 3. Abrir el detalle de la orden. |
| Resultado esperado | El detalle muestra los dos productos, cada uno con su lote. Las cantidades no se suman en un solo lote. |
| Resultado obtenido | La API devolvió costilla y lomo en lotes distintos. Comprobación «Faeneo obtiene costilla y lomo en lotes separados». |
| Cumple | Sí. |

## V2-02 · El pesaje no suma stock; la entrada sí

| Campo | Contenido |
|---|---|
| Requerimiento | RF-04 |
| Precondición | El lote de costilla del V2-01 existe y todavía no tiene entrada física. Anotar la existencia de costilla antes de empezar. Si no hay fila, la existencia es 0. |
| Pasos | 1. Registrar el pesaje: bruto 13,000 kg, tara 0,500 kg. El neto es 12,500 kg. 2. Volver a Existencias. 3. Confirmar la entrada física de ese pesaje. 4. Volver a Existencias. |
| Resultado esperado | Después del paso 2 la existencia sigue igual que al empezar. Después del paso 4 subió 12,500 kg en la cantidad física. |
| Resultado obtenido | El pesaje confirmado no creó stock. La entrada física sumó el neto exacto, con tres decimales. |
| Cumple | Sí. |

## V2-03 · El rechazo bloquea

| Campo | Contenido |
|---|---|
| Requerimiento | RF-18 |
| Precondición | Hay un animal sin orden de faeneo. En otra orden ya confirmada, un derivado ya fue consumido como insumo. |
| Pasos | 1. Registrar el control sanitario de ese animal con resultado rechazo y una observación. 2. Intentar crear una orden de faeneo sobre él. 3. Sobre el insumo ya consumido, registrar después un rechazo de ese lote. 4. Mirar el consumo y la existencia. |
| Resultado esperado | El paso 2 se niega y el mensaje dice el motivo del rechazo. El paso 4 no devuelve la cantidad consumida: el consumo queda y el rechazo queda, los dos. |
| Resultado obtenido | Sin aprobación sanitaria la orden responde `ANIMAL_RECHAZADO`. Un rechazo posterior no devolvió el insumo ya consumido. |
| Cumple | Sí. |

## V2-04 · No se reservan previsiones

| Campo | Contenido |
|---|---|
| Requerimiento | RF-04 |
| Precondición | Hay una orden de producción solo planificada, con una previsión de costilla, sin confirmar y sin entrada física. |
| Pasos | 1. Intentar reservar contra esa previsión. 2. Confirmar un pesaje y una entrada física de un lote apto. 3. Reservar contra esa existencia. |
| Resultado esperado | El paso 1 se niega. La disponibilidad no incluye la cantidad prevista. El paso 3 solo puede usar la existencia física apta menos lo ya reservado. |
| Resultado obtenido | La previsión quedó anotada y la existencia siguió en cero. Reservar sin existencia respondió `SIN_EXISTENCIA_DISPONIBLE`. |
| Cumple | Sí. |

## Límites que no se construyen

| Límite | Lo que queda fuera |
|---|---|
| Control de frío | Se anota a mano. La evaluación es de la persona. El sistema no mide la temperatura. |
| Balanza | Es un aparato físico, sin conexión. El peso se escribe. |
| Tiempo de faeneo | Se anota el estimado y el real. No hay una duración estándar. |
| Costos de producción | Fuera de alcance. El costo sigue siendo el de referencia que carga administración. |

## Pantallas ya construidas, contrastadas con la regla

No abrí el archivo Balsamiq. Miré las pantallas que ya están en `SGCPuiweb` y no las modifiqué.

- Pesar y entrada física son dos pantallas. Pesar dice que registrar el peso no da de alta la existencia. La entrada dice que, al confirmar, el neto suma al stock.
- Existencias muestra tres números separados: físico, reservado y disponible.
- Confirmar la orden avisa que los lotes nacen sin cantidad y que el stock sube recién con la entrada de almacén.
- Un animal rechazado se muestra rechazado, con el motivo, y la pantalla dice que no se puede faenar.

No vi una pantalla que sume la cantidad prevista a lo disponible. Si aparece, se corrige el mockup, no la regla.

## Prioridad y estimación, para el backlog

El Excel no se tocó. Estos son los valores de la Parte 3 para las filas que estaban sin llenar:

| Código | Prioridad | Estimación |
|---|---|---|
| RF-04 | Alta | 5 días |
| RF-18 | Alta | 1 día |
| RF-17 | Media | 1 día |
| RF-20 | Media | 1 día |
| RNF-03 | Alta | 1 día |
| RNF-06 | Alta | 1 día |

Estado al 11 de noviembre de 2026: las cuatro pruebas cumplen en la API. El Excel no se modificó.
