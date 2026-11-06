# Sprint 2 · Parte 3 · Sofia Cuellar Roca

Código de seguimiento: **S2-P3**. Rol: Product Owner. Terreno: requisitos, criterios y validación.

## Qué te toca

Dos momentos distintos del sprint, no uno.

**Al principio**, en paralelo con S2-P1: convertir el parámetro de aceptación del Excel en un guion de prueba concreto, con pasos y resultados esperados, para que los dos desarrolladores sepan exactamente contra qué se los va a medir.

**Al final**, después de S2-P2: ejecutar ese guion contra lo construido y decir si cumple o no cumple. Esa decisión es tuya: es lo que el perfil de proyecto describe como "verifica que el sistema cumpla lo solicitado".

Lo importante del orden: si el guion se escribe al final, ya no es un criterio, es una descripción de lo que salió.

## Tus tareas

### 1. El guion de prueba del Sprint 2

El Excel dice el criterio así:

> Una orden produce costilla y lomo en lotes distintos. Confirmar peso no suma stock; entrada física sí. Rechazo bloquea; consumo de derivado rechazado no se revierte por ficción. No se reservan previsiones.

Son cuatro afirmaciones. Cada una se convierte en una prueba escrita con esta forma, que es la que permite que cualquiera la ejecute sin preguntarte nada:

| Campo | Contenido |
|---|---|
| Código | `V2-01` y siguientes |
| Requerimiento | RF-04, RF-17, RF-18 o RF-20 |
| Precondición | Qué tiene que existir antes |
| Pasos | Numerados, con los datos exactos a escribir |
| Resultado esperado | Qué tiene que pasar, sin ambigüedad |
| Resultado obtenido | Se llena al ejecutar |
| Cumple | Sí o no |

Las cuatro pruebas imprescindibles, con los datos ya elegidos para que no haya que inventarlos el día de la demostración:

**V2-01 · Una orden produce varios productos en lotes distintos.** Crear una orden de faeneo y registrar dos resultados: costilla con un lote y lomo con otro, con cantidades distintas. Esperado: el detalle de la orden muestra los dos productos con sus dos lotes separados.

**V2-02 · El pesaje no suma stock; la entrada sí.** Anotar la existencia de la costilla antes de empezar. Registrar un pesaje de 12,500 kg. Volver a mirar la existencia: **tiene que seguir igual**. Confirmar la entrada física. Mirar otra vez: **ahora sí subió 12,500**. Esta prueba es la más probable de que falle, porque es la más fácil de implementar mal.

**V2-03 · El rechazo bloquea.** Registrar un control sanitario con rechazo sobre un animal. Intentar crear una orden de faeneo sobre él: tiene que negarse con un mensaje que explique el motivo. Y la segunda parte, que es la que se olvida: si un insumo ya consumido en una fabricación se rechaza después, **el consumo no se revierte**; queda registrado el rechazo y la trazabilidad, sin deshacer nada.

**V2-04 · No se reservan previsiones.** Crear una orden de producción planificada, sin confirmar. Intentar reservar contra ella: tiene que negarse. La disponibilidad solo sale de existencia física apta menos reservas.

**Entregás:** el guion en `00_Definicion/Validacion_Sprint2.md`. **Se comprueba:** otra persona lo ejecuta sin preguntarte nada.

### 2. Confirmar el alcance antes de que se construya

Hay cuatro límites del Excel que conviene confirmar por escrito antes de que alguien construya de más. No son dudas tuyas: son límites que el propio Excel fija y que es fácil pasar por alto cuando uno quiere ser servicial con el usuario.

| Límite | Lo que dice el Excel |
|---|---|
| Control de frío | Registro **manual**, con evaluación **humana**. El sistema no mide temperatura |
| Balanza | Herramienta física sin conexión. Los pesajes se escriben a mano |
| Tiempo de faeneo | Se registra estimado y real. **No** se fija una duración estándar sin datos observados |
| Costos de producción | Fuera de alcance. El costo sigue siendo el de referencia que carga administración |

Dejalo escrito y avisado a los dos desarrolladores. Es trabajo que se evita, no trabajo que se agrega.

**Entregás:** la confirmación escrita en el mismo documento de validación. **Se comprueba:** nadie construyó nada de esta lista.

### 3. Validar los mockups de producción e inventario

En `04_Mockups_Balsamiq/SGCC_Web_Android.bmpr` están las 67 pantallas diseñadas. Revisá las de producción, inventario, pesajes y frío **antes** de que S2-P2 las construya, y decí si siguen siendo lo que se quiere.

Si una pantalla del mockup contradice una regla del Excel, el mockup es el que se corrige. El caso típico: un mockup que muestra pesaje y entrada en un mismo formulario, cuando la regla pide que sean dos pasos.

Dos cosas que vale confirmar en las pantallas de inventario: que se vean **las tres cantidades** por separado —física, reservada y disponible—, y que en ninguna aparezca una cantidad prevista sumada a la disponibilidad.

**Entregás:** una lista corta de pantallas revisadas, con las correcciones si hay. **Se comprueba:** las pantallas construidas coinciden con los mockups aprobados.

### 4. Actualizar el backlog del Excel

En la hoja **Requerimientos**, sección V, Sprint Backlog, Sprint 2: completar prioridad y estimación de RF-04, RF-17, RF-18, RF-20, RNF-03 y RNF-06, que están sin llenar.

Y en la sección III, la lista general de requerimientos, poner el estado de cada uno al terminar el sprint.

El Excel tiene arriba una tabla de versionamiento del documento con fecha de creación, modificación y aprobación, y las filas V1.0 y V1.1 vacías. Llenala: es parte del control de versiones de la documentación, y está pedido en el formato.

**Entregás:** el Excel actualizado. **Se comprueba:** no queda ninguna celda de prioridad o estimación vacía en el Sprint 2.

### 5. Validar al cierre y decidir

Cuando S2-P2 termine, ejecutá el guion del punto 1 y llená las columnas de resultado obtenido y cumple.

Si algo no cumple, se registra con el código de la prueba y la parte responsable —`V2-02 no cumple, corresponde a S2-P1`— y se corrige antes de cerrar el sprint. No se cierra con pruebas en rojo, y no se cambia el criterio para que pase: eso es lo único que invalidaría todo el ejercicio.

**Entregás:** el guion ejecutado con su veredicto. **Se comprueba:** cada prueba tiene resultado obtenido escrito.

### 6. Pendiente del Sprint 1: usabilidad con usuarios

RNF-04 quedó sin medir y es tuyo por rol. Pide validar la interfaz con **personal representativo**, no entre ustedes cuatro.

Lo mínimo que sirve como evidencia: dos o tres personas que no hayan participado del desarrollo, una tarea concreta por persona —cargar un cliente, armar una cotización, confirmar un pedido—, el tiempo que tardaron, dónde se trabaron, y qué palabra de la pantalla no entendieron. RNF-04 pide lenguaje del negocio, búsqueda ágil, unidades visibles y confirmación de operaciones: cada una se puede observar.

Esto no se puede inventar, y es lo que vuelve el requerimiento no funcional algo demostrable en lugar de una frase en el documento.

**Entregás:** una nota de una página en `00_Definicion/`. **Se comprueba:** hay nombres de tareas, tiempos y observaciones concretas.

## Qué no te toca

Escribir código, migraciones ni pantallas. Si una prueba falla, la reportás con su código y la parte responsable; no la arreglás.

Tampoco los diagramas UML, que son de S2-P4.

## De quién dependés y quién depende de vos

**Depende de vos todo el sprint al principio**: los dos desarrolladores necesitan saber contra qué se los mide. El guion del punto 1 es lo primero que tiene que existir, y el Excel ya te da la materia prima.

**Dependés de S2-P2** para validar al cierre, porque validás sobre las pantallas terminadas.

## Cómo entregarlo

Tus entregables son documentos, van al repositorio **SGCPdocumentacion**:

```bash
git checkout -b sprint2/p3-criterios-validacion
git commit -m "v2.3.0 - Sprint 2 - Criterios de aceptacion y validacion"
git push -u origin sprint2/p3-criterios-validacion
```

Pull Request con el código `S2-P3` en el cuerpo. El Excel va en el mismo PR.

## Una nota sobre el Sprint 1

El docente todavía no lo revisó. Cuando haya devolución, lo que observe entra por tu parte: lo traducís a cambios concretos con su requerimiento y su responsable, y recién después se reparte. Si va directo a los desarrolladores sin pasar por ahí, se pierde el registro de por qué se cambió algo.
