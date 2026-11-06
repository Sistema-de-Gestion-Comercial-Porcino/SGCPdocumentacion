# Sprint 3 · Parte 3 · Sofia Cuellar Roca

Código de seguimiento: **S3-P3**. Rol: Product Owner. Terreno: requisitos, criterios y validación.

## Qué te toca

El guion de prueba del Sprint 3 y la validación al cierre. Con una diferencia respecto a los sprints anteriores: acá **las pruebas no se pueden hacer en una laptop**. Hacen falta un teléfono y el modo avión.

Es el sprint donde tu papel pesa más, porque el criterio de validación es sobre comportamientos que un desarrollador puede creer que implementó y no.

## Tus tareas

### 1. El guion de prueba del Sprint 3

El Excel dice el criterio así:

> Captura pendiente hasta sincronizar. Conforme: ENTREGADA; con observaciones: OBSERVADA. El reintento no duplica datos y los conflictos requieren revisión. Entrega y deuda mantienen estados independientes.

Cuatro afirmaciones, y las cuatro se prueban con el teléfono en la mano. El formato de cada prueba es el mismo del Sprint 2: código, requerimiento, precondición, pasos con datos exactos, resultado esperado, resultado obtenido y veredicto.

**V3-01 · La captura queda pendiente hasta sincronizar.** Con conexión, descargar una entrega asignada. **Poner el teléfono en modo avión.** Capturar la recepción: receptor, fecha real, peso, conformidad y una foto. En el teléfono tiene que verse **pendiente**. Y en la web, con el servidor al lado, esa recepción **no existe todavía**. Esa segunda mitad es la que prueba de verdad la afirmación.

**V3-02 · Conforme da ENTREGADA; con observaciones da OBSERVADA.** Dos capturas: una conforme y otra con observaciones. Sincronizar. En la web, la primera queda ENTREGADA y la segunda OBSERVADA. Lo que hay que mirar con cuidado: que la observada **no se vea como un error ni como un rechazo**. La entrega ocurrió, con reparos.

**V3-03 · El reintento no duplica y el conflicto espera revisión.** Capturar sin señal. Empezar a sincronizar y **cortar la conexión a mitad**. Reintentar. En el servidor tiene que haber **una sola** recepción, no dos. Esta es la prueba más importante del sprint y la más fácil de pasar por alto, porque con buena señal nunca falla. Y la segunda parte: provocar un conflicto y comprobar que queda **marcado esperando revisión**, sin sobrescribirse solo.

**V3-04 · Entrega y deuda son independientes.** Confirmar una entrega conforme y mirar el saldo del cliente: **no cambió**. Registrar un pago y mirar el estado de la entrega: **no cambió**. Son dos cosas que avanzan por separado y el Excel lo pide explícitamente.

**Entregás:** el guion en `00_Definicion/Validacion_Sprint3.md`. **Se comprueba:** otra persona lo ejecuta con un teléfono y sin preguntarte nada.

### 2. Confirmar los límites antes de que se construya

Este sprint tiene los límites de alcance más fáciles de cruzar de todo el proyecto, porque «sin conexión» suena a que todo debería funcionar sin conexión. No es así, y conviene confirmarlo por escrito antes de que alguien lo construya:

| Límite | Lo que dice el perfil de proyecto |
|---|---|
| Qué se captura sin conexión | **Solo la recepción** de entregas asignadas, autorizadas y descargadas |
| Qué no | No se cotiza, no se vende, no se cobra sin conexión. Ninguna operación comercial |
| Sincronización | Requiere conexión, sesión válida y la aplicación **abierta**, o envío manual. No hay sincronización en segundo plano |
| Conflictos | Los revisa una persona. **No** se resuelven solos |
| Pérdida de datos | Las capturas pendientes se pueden perder si se borra la aplicación o se pierde el teléfono. Es una consecuencia conocida, no un defecto |
| Señas canceladas | Se registra el acuerdo de resolución. **No** hay devolución ni retención automáticas |
| Crédito | Autorizar crédito **no** liquida deuda |

Los dos últimos son reglas del negocio que es fácil «mejorar» por iniciativa propia y que arruinarían la contabilidad.

**Entregás:** la confirmación escrita. **Se comprueba:** nada de esta lista se construyó.

### 3. Validar los mockups de entregas y pagos

En `04_Mockups_Balsamiq/SGCC_Web_Android.bmpr` están las pantallas de Android y las de pagos y entregas. Revisalas **antes** de que S3-P2 las construya.

Tres cosas que vale confirmar en las de Android, porque son las que el usuario va a mirar en la calle con el teléfono en una mano:

- Que se vea **cuántas capturas hay pendientes** de sincronizar. Si no se ve, el repartidor acumula veinte sin saberlo.
- Que se vea la diferencia entre **pendiente** y **sincronizada**, sin ambigüedad.
- Que un conflicto se vea como «esperando revisión» y no como un error del repartidor, que no hizo nada mal.

Y en las de la web: que el estado de la entrega y el saldo del cliente **no aparezcan como una sola cosa**.

**Entregás:** lista de pantallas revisadas con sus correcciones. **Se comprueba:** lo construido coincide con lo aprobado.

### 4. Actualizar el backlog

En la hoja Requerimientos, Sprint Backlog, Sprint 3: prioridad y estimación de RF-05, RF-06, RF-07, RF-08, RF-19, RNF-01 y RNF-05, que están sin llenar. Y el estado de cada requerimiento al cerrar.

**Entregás:** el Excel actualizado. **Se comprueba:** no quedan celdas vacías en el Sprint 3.

### 5. Validar al cierre y decidir

Ejecutá el guion con el teléfono y llená resultado obtenido y veredicto.

Lo que no se puede hacer, y en este sprint la tentación es grande porque probar sin conexión es incómodo: **dar por buena una prueba que no se ejecutó**. Si V3-03 no se probó cortando la conexión de verdad, no está probada. Escribí «no ejecutada» antes que «cumple».

Si algo no cumple, se reporta con el código y la parte responsable: `V3-03 no cumple, corresponde a S3-P1`.

**Entregás:** el guion ejecutado. **Se comprueba:** cada prueba tiene resultado escrito, incluidas las no ejecutadas.

## Qué no te toca

Programar ni corregir. Los diagramas de estado son de S3-P4, aunque te conviene mirarlos: si el diagrama y la aplicación no coinciden, uno de los dos está mal y es un hallazgo tuyo.

## De quién dependés y quién depende de vos

**Depende de vos el arranque**: el guion tiene que existir antes de que se construya, o deja de ser un criterio.

**Dependés de S3-P2** para validar, y necesitás un teléfono con la aplicación instalada. Pedilo con tiempo: si la aplicación llega el último día, no hay cuándo probar lo único que importa.

## Cómo entregarlo

```bash
git checkout -b sprint3/p3-criterios-validacion
git commit -m "v3.3.0 - Sprint 3 - Criterios de aceptacion y validacion"
git push -u origin sprint3/p3-criterios-validacion
```

Pull Request con el código `S3-P3` en el cuerpo, en **SGCPdocumentacion**.
