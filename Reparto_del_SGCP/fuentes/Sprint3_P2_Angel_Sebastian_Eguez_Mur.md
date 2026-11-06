# Sprint 3 · Parte 2 · Angel Sebastian Eguez Mur

Código de seguimiento: **S3-P2**. Rol: Desarrollador. Repositorios: **SGCPuimovil** y **SGCPuiweb**.

> **Esta es la parte más grande del proyecto.** Android pasa de tener solo una pantalla de acceso a tener almacenamiento local, captura de evidencia y sincronización. Está reconocido en el documento general: si la carga no entra, S3-P1 toma las pantallas web de pagos y transporte para que te concentres en el teléfono. Pedilo temprano, no el último día.

## Qué te toca

**Android**, que es el centro del sprint: descargar las entregas asignadas, capturar la recepción **sin señal**, guardar evidencia y sincronizar cuando haya conexión. Con los patrones Command y State.

**Web**, lo que quede del reparto: pantallas de condición de pago, saldos, señas, transporte, rutas y entregas.

## Antes de empezar: el contrato con S3-P1

No escribas el cliente de sincronización antes de que el contrato esté acordado y escrito en el README de SGCPapi. Es la tarea 0 de S3-P1 y te involucra: **sentate con él la primera semana**.

Lo que RNF-01 exige guardar en el teléfono, textual: «clave única, versión base, autor, fecha real, datos y evidencia». Lo que te importa de cada campo:

| Campo | Por qué te afecta |
|---|---|
| Clave única | **La generás vos, en el teléfono.** Es lo que hace que un reintento sea inofensivo |
| Versión base | Sobre qué versión capturaste. El servidor lo usa para detectar conflicto |
| Fecha real | Cuándo ocurrió físicamente. **Distinta** de cuándo sincronizaste |
| Evidencia | Archivo local, con su ruta privada |

Si el servidor responde «ya existe», **eso es un éxito**: el dato llegó. Marcá la captura como sincronizada y seguí. Tratarlo como error deja el teléfono reintentando para siempre.

## Tus tareas en Android

### 1. Almacenamiento local con Room · RNF-01

Entidades locales para la entrega descargada, la captura de recepción y la evidencia. Con los seis campos del contrato.

Los archivos de evidencia van en **almacenamiento privado de la aplicación**, no en la galería. RNF-03 pide proteger las evidencias, y una foto en la galería la ve cualquier aplicación con permiso de lectura.

Lo que el requerimiento advierte y conviene mostrar en la interfaz: **las capturas pendientes se pierden si se borra la aplicación o se pierde el teléfono.** Eso no es un defecto, es una consecuencia de capturar sin conexión. Mostrar cuántas capturas hay sin sincronizar es la forma de que el usuario no acumule veinte.

**Entregás:** la base local y sus pruebas. **Se comprueba:** una captura sobrevive al cierre y reapertura de la aplicación.

### 2. Descargar entregas autorizadas · RF-07

Solo se descargan las entregas **asignadas al responsable, autorizadas y con conexión**. El teléfono no inventa entregas ni captura sobre algo que no descargó: ese es el límite del sprint y el servidor lo filtra por el usuario autenticado.

La pantalla tiene que dejar claro qué entregas están disponibles para capturar sin señal. Si el repartidor sale sin descargar, no puede trabajar, y es mejor que lo sepa en la puerta.

**Entregás:** pantalla de descarga. **Se comprueba:** sin descargar previamente, no hay nada que capturar.

### 3. Capturar la recepción sin conexión · RF-07, RNF-01

El formulario: receptor, fecha real, peso con unidad, conformidad, observaciones y evidencia.

**Probar esto en modo avión de verdad, no simulado.** Es la única forma de saber si funciona. Un mock de «sin conexión» prueba el mock.

La captura queda **pendiente** hasta sincronizar. En el teléfono se ve pendiente y en el servidor no existe todavía. Esa es la primera afirmación del criterio de validación del sprint.

**Entregás:** el formulario de captura. **Se comprueba:** en modo avión se captura y queda pendiente; no se pierde al cerrar la aplicación.

### 4. Command para las capturas · RNF-01

Cada captura sin conexión es una **orden** que se guarda, se encola y se reintenta. Eso es exactamente el patrón Command, y por eso está elegido: el reintento sale natural en lugar de ser un parche.

Una cola de órdenes pendientes, que se procesa cuando hay conexión, y que sobrevive al cierre de la aplicación porque está en Room y no en memoria.

Para la defensa: Command va acá porque la operación se tiene que poder guardar, pasar y reintentar como si fuera un dato. Una llamada directa a la API no se puede guardar para después.

**Entregás:** el patrón y la cola. **Se comprueba:** tres capturas en modo avión se sincronizan en orden al recuperar la señal.

### 5. State para los estados de la entrega · RF-07

Pendiente, sincronizada, entregada, observada. Y conflicto, si el servidor lo marca.

Las transiciones válidas viven en el patrón, no en condicionales repartidos por las pantallas. Una pendiente no puede pasar a entregada sin pasar por sincronizada: eso es una regla, no una validación de interfaz.

**Conforme da ENTREGADA; con observaciones da OBSERVADA.** Las dos son entregas que ocurrieron; una observación no es un rechazo. Que se vean distinto, pero que ninguna se vea como un error.

**Entregás:** la máquina de estados. **Se comprueba:** no existe forma de llegar a entregada sin sincronizar.

### 6. Sincronización y reintento · RNF-01

Según el perfil de proyecto, la sincronización requiere **conexión, sesión válida y la aplicación abierta, o envío manual**. No hay sincronización en segundo plano con la aplicación cerrada: no se promete.

Lo que la pantalla tiene que mostrar siempre: cuántas capturas hay pendientes, cuándo fue el último envío, y qué quedó en conflicto esperando revisión.

Un conflicto **no se resuelve en el teléfono**. Se muestra y se avisa que alguien lo tiene que revisar. El Excel lo pide así.

**Entregás:** la pantalla de sincronización. **Se comprueba:** cortar la conexión a mitad de un envío y reintentar no duplica nada en el servidor.

### 7. Compatibilidad real · RNF-05

La aplicación tiene que correr en **dispositivos reales**, no solo en el emulador. El proyecto declara Android 8.0, API 26, como mínimo.

Probá en al menos dos teléfonos distintos y anotá marca, modelo y versión de Android de cada uno. Esa es la evidencia de RNF-05, que todavía no existe ni para el Sprint 1.

**Entregás:** una nota con los dispositivos probados. **Se comprueba:** hay dos modelos con su versión anotada.

## Tus tareas en la web

Si la carga de Android lo permite. Si no, se las pasás a S3-P1.

Condición de pago acordada por operación, con importe y vencimiento cuando es crédito. Saldos por cliente, con las cinco distinciones: producto, servicio, contado, crédito vigente y vencido. Señas. Transporte y rutas. Entregas y carga manual de recepción desde la web.

**Dos pantallas que no se pueden mezclar:** el estado de la entrega y el estado de la deuda. El Excel los separa explícitamente. Que una entrega esté entregada no dice nada del saldo, y mostrarlos juntos como si fueran una sola cosa es el error que el criterio de validación busca.

Y los `[Range]` sobre decimales con `ParseLimitsInInvariantCulture` y `ConvertValueInInvariantCulture`, siempre. Importes y pesos, todo el sprint.

## Qué no te toca

El modelo de datos y el endpoint de sincronización: S3-P1. Diagramas de estado: S3-P4, aunque te conviene mirarlos para que tu máquina de estados coincida con el diagrama.

La constancia de entrega es RF-14, Sprint 4.

## De quién dependés y quién depende de vos

**Dependés de S3-P1** para el contrato de sincronización y para el endpoint. Es el bloqueo más duro del proyecto: sin contrato no podés ni empezar el cliente.

**Depende de vos S3-P3 y S3-P4**, que prueban con el teléfono en la mano. Si la aplicación llega el último día, no hay cuándo probar la captura sin conexión, que es lo único que realmente hay que probar en este sprint.

## Cómo entregarlo

Dos repositorios, dos Pull Requests:

```bash
git checkout -b sprint3/p2-android-offline
git commit -m "v3.2.0 - Sprint 3 - Captura sin conexion y sincronizacion"
git push -u origin sprint3/p2-android-offline
```

Los dos con el código `S3-P2` en el cuerpo.
