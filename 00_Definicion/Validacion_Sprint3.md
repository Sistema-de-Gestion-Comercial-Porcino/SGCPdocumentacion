# Validación del Sprint 3

Código de seguimiento: **S3-P3**. Responsable: Sofia Cuellar Roca, Parte 3. Fecha del guion: 11 de noviembre de 2026 (hora de La Paz).

El criterio del Excel:

> Captura pendiente hasta sincronizar. Conforme: ENTREGADA; con observaciones: OBSERVADA. El reintento no duplica datos y los conflictos requieren revisión. Entrega y deuda mantienen estados independientes.

Estas cuatro pruebas se hacen con un teléfono. En esta sesión no hubo teléfono ni modo avión, así que el resultado es **no ejecutada**. No se anota «cumple».

El archivo `Formato Proyecto - SGCC Actualizado.xlsx` no se modificó.

## V3-01 · La captura queda pendiente hasta sincronizar

| Campo | Contenido |
|---|---|
| Requerimiento | RF-07, RNF-01 |
| Precondición | Hay una entrega asignada a la cuenta del responsable, autorizada y descargada en el teléfono. El teléfono tiene señal. |
| Pasos | 1. Con señal, comprobar que la entrega está en el teléfono. 2. Activar el modo avión. 3. Capturar la recepción: receptor «Ana Rojas», fecha real de hoy, peso 12,500 kg, conformidad conforme y una foto. 4. Mirar la cola del teléfono. 5. En la web, con el servidor al lado, buscar esa recepción. |
| Resultado esperado | En el teléfono la captura figura pendiente. En la web esa recepción no existe. |
| Resultado obtenido | No ejecutada. |
| Cumple | No ejecutada. |

## V3-02 · Conforme da ENTREGADA; con observaciones da OBSERVADA

| Campo | Contenido |
|---|---|
| Requerimiento | RF-07 |
| Precondición | Hay dos entregas descargadas. El teléfono vuelve a tener señal. |
| Pasos | 1. Capturar la primera como conforme, sin observaciones. 2. Capturar la segunda con observaciones «Faltó un kilo de costilla». 3. Sincronizar las dos. 4. Abrir las dos en la web. |
| Resultado esperado | La primera queda ENTREGADA. La segunda queda OBSERVADA. La observada no se muestra como error ni como rechazo: la entrega ocurrió, con reparos. |
| Resultado obtenido | No ejecutada. |
| Cumple | No ejecutada. |

## V3-03 · El reintento no duplica y el conflicto espera revisión

| Campo | Contenido |
|---|---|
| Requerimiento | RNF-01 |
| Precondición | Hay una captura hecha sin señal, con su clave generada en el teléfono. |
| Pasos | 1. Empezar a sincronizar y cortar la señal a mitad del envío. 2. Volver a intentar con la misma clave. 3. En el servidor, contar las recepciones de esa entrega. 4. Provocar un conflicto de versión y sincronizar de nuevo. |
| Resultado esperado | Después del paso 3 hay una sola recepción. El conflicto queda marcado para que una persona lo revise. El servidor no pisa la entrega solo. |
| Resultado obtenido | No ejecutada. No se cortó una conexión real. |
| Cumple | No ejecutada. |

## V3-04 · Entrega y deuda son independientes

| Campo | Contenido |
|---|---|
| Requerimiento | RF-05, RF-06, RF-07 |
| Precondición | El cliente tiene un saldo conocido y una entrega sin recepcionar. |
| Pasos | 1. Anotar el saldo. 2. Confirmar la entrega como conforme y sincronizarla. 3. Volver a mirar el saldo. 4. Registrar un pago. 5. Volver a mirar el estado de la entrega. |
| Resultado esperado | Después del paso 3 el saldo es el mismo. Después del paso 5 el estado de la entrega es el mismo. Llegar no cobra, y pagar no marca la entrega. |
| Resultado obtenido | No ejecutada. |
| Cumple | No ejecutada. |

## Límites que no se construyen

| Límite | Lo que queda fuera |
|---|---|
| Qué se captura sin conexión | Solo la recepción de entregas ya asignadas, autorizadas y descargadas. |
| Qué no | No se cotiza, no se vende y no se cobra sin señal. |
| Sincronización | Hace falta señal, sesión válida y la aplicación abierta, o un envío manual. No hay sincronización en segundo plano. |
| Conflictos | Los revisa una persona. No se resuelven solos. |
| Pérdida de datos | Si se borra la aplicación o se pierde el teléfono, las capturas que no se sincronizaron se pueden perder. Es una consecuencia conocida, no un defecto. |
| Señas canceladas | Se anota el acuerdo. No hay devolución ni retención automáticas. |
| Crédito | Autorizar crédito no liquida la deuda. |

## Pantallas

No abrí el Balsamiq y no instalé la aplicación en un teléfono. En la web que ya está en el repositorio, la ficha del cliente todavía dice que la gestión de saldo y cobranza queda para una etapa posterior. Pagos, rutas y entregas no tienen pantalla propia en `SGCPuiweb` a esta fecha. El guion queda antes de esas pantallas.

Cuando Sebastián las construya, en Android tiene que verse cuántas capturas están pendientes, la diferencia entre pendiente y sincronizada, y el conflicto como «esperando revisión». En la web, el estado de la entrega y el saldo del cliente no pueden aparecer como una sola cosa.

## Prioridad y estimación, para el backlog

El Excel no se tocó. Estos son los valores de la Parte 3:

| Código | Prioridad | Estimación |
|---|---|---|
| RF-05 | Alta | 1 día |
| RF-06 | Alta | 1 día |
| RF-07 | Alta | 2 días |
| RF-08 | Media | 2 días |
| RF-19 | Media | 1 día |
| RNF-01 | Alta | 3 días |
| RNF-05 | Media | 1 día |

Estado al 11 de noviembre de 2026: guion escrito. Las cuatro pruebas, no ejecutadas.
