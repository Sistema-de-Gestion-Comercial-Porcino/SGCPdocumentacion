# Sprint 2 · Parte 2 · Angel Sebastian Eguez Mur

Código de seguimiento: **S2-P2**. Rol: Desarrollador. Repositorio: **SGCPuiweb**.

## Qué te toca

Las pantallas web del Sprint 2: sanidad, órdenes de producción, resultados por lote, pesajes, entradas de inventario, existencias, control de frío y separación de cargos. Todo lo que el personal de producción y almacén va a usar.

Android no entra en este sprint. La aplicación móvil recién tiene trabajo real en el Sprint 3, con la captura sin conexión. Lo único tuyo que la toca en el Sprint 2 es el pendiente del Sprint 1: instalar el APK en un teléfono y probar el acceso.

## Antes de empezar: lo que no cambia

Dos reglas de la arquitectura que no se negocian:

- **La web no toca la base de datos.** No hay EF Core en este repositorio y no se agrega. Todo pasa por la API, con los clientes HTTP tipados que ya están en `src/SGCP.Web/Services/`.
- **Si falta un dato, se pide un endpoint.** Si una pantalla necesita algo que la API no devuelve, se lo pedís a S2-P1. No hay atajo, y buscarlo rompe el sprint siguiente.

Tu punto de partida es Swagger, en `http://localhost:5081/swagger`, y la tabla de rutas del README de SGCPapi. Si una ruta no está ahí, todavía no existe.

## Tus tareas

### 1. Clientes de API · RF-04, RF-17, RF-18, RF-20

En `src/SGCP.Web/Services/`, un cliente por módulo nuevo, siguiendo exactamente el estilo de los que ya están: heredan de `ClienteApiBase`, devuelven DTO, no lanzan excepciones crudas a la vista.

`ProduccionApi`, `SanidadApi`, `InventarioApi`, `FrioApi`. Y los DTO en `Models/Dtos/Dtos.cs`.

**Entregás:** los clientes registrados en `Program.cs`. **Se comprueba:** compila sin advertencias y una llamada de prueba devuelve datos.

### 2. ViewModels con validación · RF-04

En `src/SGCP.Web/Models/ViewModels/ViewModels.cs`.

Acá hay una trampa con nombre y apellido. **Todo atributo `[Range]` sobre un `decimal` con límites escritos como texto necesita las dos propiedades de cultura invariante:**

```csharp
[Range(typeof(decimal), "0.001", "9999999.999",
       ParseLimitsInInvariantCulture = true, ConvertValueInInvariantCulture = true)]
```

Sin eso, en una máquina en español la pantalla devuelve error 500 en cuanto alguien escribe un número. Pasó en el Sprint 1 con cuatro atributos y está documentado en `00_Definicion/Errores_encontrados_Sprint1.md` sección 1. En este sprint vas a cargar pesos y temperaturas, así que te va a tocar varias veces.

El enlace de decimales ya está resuelto para todo el repositorio por `Models/EnlaceDecimalInvariante.cs`: no hay que hacer nada más que no romperlo.

**Entregás:** los ViewModels. **Se comprueba:** enviar `12.500` en un peso y releerlo desde la API devuelve `12.5`, no `12500`.

### 3. Pantallas de sanidad · RF-18

Listado de animales con su estado, formulario de alta, y el registro del control sanitario con identificación, procedencia, responsable y resultado.

Lo que tiene que verse sin ambigüedad: **un animal rechazado se ve rechazado**. Y al intentar crear una orden de faeneo sobre él, la pantalla muestra el motivo del rechazo, no un error genérico. El código que devuelve la API es `ANIMAL_RECHAZADO`; traducilo a un mensaje que el personal entienda.

**Entregás:** vistas y controlador de sanidad. **Se comprueba:** el recorrido de rechazo termina en un mensaje claro, no en una página de error.

### 4. Pantallas de producción · RF-04

Órdenes de faeneo y de fabricación, con su estado, responsable y tiempos estimado y real.

La pantalla clave del sprint es **registrar los resultados de una orden**: un formulario que permite cargar **varios productos, cada uno con su lote y su cantidad real**. Si el formulario solo admite un producto, el criterio de validación del sprint no se puede demostrar, porque el Excel pide explícitamente que una orden produzca costilla y lomo en lotes distintos.

Para fabricación, además, los insumos realmente consumidos.

**Entregás:** vistas y controlador de producción. **Se comprueba:** una orden queda con dos resultados en dos lotes distintos, visibles en el detalle.

### 5. Pesajes y entradas: dos pantallas separadas · RF-04

Esta es la parte donde más fácil es equivocarse, y es el criterio más visible del sprint.

**Son dos pantallas distintas, con dos nombres distintos, y no se pueden mezclar:**

| Pantalla | Qué hace | Qué le pasa al stock |
|---|---|---|
| Registrar pesaje | Guarda bruto, tara, neto, unidad, producto, lote y responsable | **Nada** |
| Confirmar entrada física | Almacén confirma que el producto entró | **Suma stock** |

Si las unís en un solo formulario "por comodidad", el sprint no cumple. La pantalla de pesaje tiene que decir, en texto visible, que registrar el peso no da de alta la existencia. El personal de almacén viene de un cuaderno: si no lo dice, va a asumir lo contrario.

La entrada física es **única por lote y producto**. La API la rechaza con `ENTRADA_YA_REGISTRADA`; la pantalla tiene que explicar que ya fue registrada y por quién, no mostrar un error rojo sin información.

**Entregás:** dos vistas separadas y su controlador. **Se comprueba:** registrar un pesaje no cambia la existencia; confirmar la entrada sí.

### 6. Existencias y reservas · RF-04

Listado de existencias por producto y lote, mostrando **las tres cantidades distintas**: física apta, reservada y disponible. Disponible es físico menos reservado, y conviene mostrar la resta, porque es la que el negocio mira para comprometer un pedido.

Lo que no debe aparecer en ninguna parte: cantidades previstas o planificadas sumadas a la disponibilidad. El Excel lo prohíbe y es un error fácil de cometer al querer ser servicial con el usuario.

**Entregás:** vista de existencias. **Se comprueba:** una orden planificada no cambia ninguna de las tres columnas.

### 7. Control de frío · RF-17

Formulario de registro manual: temperatura con su unidad, fecha, referencia a lote, ubicación o entrega, responsable y la evaluación.

Dos cosas que el formulario tiene que dejar claras, porque son límites de alcance del propio Excel: el sistema **no mide** la temperatura, la registra; y la evaluación es **humana**, no un cálculo automático a partir de un umbral.

**Entregás:** vista y controlador de frío. **Se comprueba:** un registro queda con responsable y evaluación guardados.

### 8. Separación de cargos · RF-20

Donde se muestran los importes de un pedido, el cargo de producto y el de servicio de faeneo o corte van **separados**, nunca sumados en una sola línea. El servicio solo aparece cuando se acordó y se prestó.

**Entregás:** la vista de cargos ajustada. **Se comprueba:** un pedido con servicio muestra dos líneas; uno sin servicio, una.

### 9. Habilitar el menú · RF-04

En `src/SGCP.Web/Views/Shared/_Layout.cshtml`, los ítems de producción e inventario están deshabilitados a propósito desde el Sprint 1, para que se vea el avance. Habilitá los que ahora existen y dejá deshabilitados los de los sprints 3 y 4.

Cada ítem se muestra según el permiso del usuario: producción no ve almacén, almacén no ve precios de venta.

**Entregás:** el layout ajustado. **Se comprueba:** un usuario de producción no ve en el menú lo que no le corresponde.

### 10. Pendiente del Sprint 1: el APK en un teléfono

Esto viene del sprint anterior y sigue abierto. El APK compila y las pruebas unitarias pasan, pero **nunca se ejecutó en un dispositivo real**.

```
SGCPuimovil/app/build/outputs/apk/debug/app-debug.apk
```

Se copia al teléfono y se instala permitiendo orígenes desconocidos. En la pantalla de acceso hay un campo para la dirección de la API, que tiene que ser la **IP de red** de la máquina donde corre, no `localhost`: el teléfono no resuelve el `localhost` de la laptop. Los dos en el mismo wifi.

Dejá escrito el resultado, con la versión de Android del teléfono, porque RNF-05 pide compatibilidad con los dispositivos acordados y esa evidencia no existe todavía.

**Entregás:** una nota corta con el resultado, para `00_Definicion/`. **Se comprueba:** el acceso funciona desde el teléfono contra la API del equipo.

## Qué no te toca

El modelo de datos, las migraciones y las reglas del negocio: S2-P1. Si una regla te parece mal, se discute, no se implementa de nuevo en la pantalla.

Los diagramas UML son de S2-P4 y los criterios de aceptación de S2-P3. Android, más allá del pendiente del punto 10, es Sprint 3.

## De quién dependés y quién depende de vos

**Dependés de S2-P1.** Sin endpoints no hay pantalla. Lo práctico es pedirle que publique las rutas y los cuerpos en Swagger temprano, aunque las reglas estén a medias: con el contrato ya podés armar clientes, DTO y vistas.

**Depende de vos S2-P3**, que valida contra las pantallas, y **S2-P4**, que prueba el recorrido completo. Si tus pantallas llegan el último día, ellos no tienen cuándo trabajar.

## Cómo entregarlo

```bash
git checkout -b sprint2/p2-web-produccion
git commit -m "v2.2.0 - Sprint 2 - Pantallas de produccion e inventario"
git push -u origin sprint2/p2-web-produccion
```

Pull Request con el código `S2-P2` en el cuerpo.

Antes de abrirlo: compila sin advertencias, las pantallas cargan con la API levantada, los decimales se guardan exactos, y `dotnet format` corrido. Y una línea en el README de SGCPuiweb con las pantallas nuevas.

## Dos errores del Sprint 1 que te van a tocar de nuevo

1. **Los decimales y la cultura.** Dos defectos distintos salieron de esto: uno devolvía 500 y el otro guardaba 88,50 como 8850 sin avisar nada. Están en `00_Definicion/Errores_encontrados_Sprint1.md` secciones 1 y 2. Probá siempre con `LANG=es_BO.UTF-8`, no con la variable sin definir, porque sin ella los dos defectos desaparecen y las pruebas pasan con el sistema roto.
2. **Las fechas.** Usá `datetime-local` con `asp-format="{0:yyyy-MM-ddTHH:mm}"`, que es ISO y se interpreta igual en cualquier cultura. Es lo que hicieron las pantallas del Sprint 1 y por eso las fechas no dieron problema.
