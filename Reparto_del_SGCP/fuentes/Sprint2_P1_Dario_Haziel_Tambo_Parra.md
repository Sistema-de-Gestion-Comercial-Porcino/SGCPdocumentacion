# Sprint 2 · Parte 1 · Dario Haziel Tambo Parra

Código de seguimiento: **S2-P1**. Rol: Desarrollador. Repositorio: **SGCPapi**.

## Qué te toca

La API del Sprint 2 completa: el modelo de datos de producción e inventario, la migración de MySQL, las reglas del negocio y los endpoints que la web va a consumir. Sos el bloqueo del sprint: hasta que publiques el contrato en Swagger, S2-P2 no puede avanzar.

Antes de escribir una línea, leé el criterio de validación del Sprint 2 en el documento general de esta carpeta. Las cuatro afirmaciones que contiene son el diseño: no son pruebas que se agregan al final, son la razón de que el modelo tenga la forma que tiene.

## Tus tareas

### 1. Entidades y enumeraciones · RF-04, RF-17, RF-18, RF-20

En `src/SGCP.Api/Dominio/Entidades/`, una clase por archivo, siguiendo la convención del Sprint 1: nombres en español, `Guid` como identificador, propiedades con valor inicial.

Once entidades: `Animal`, `ControlSanitario`, `OrdenProduccion`, `InsumoProduccion`, `Lote`, `ResultadoProduccion`, `Pesaje`, `EntradaInventario`, `Existencia`, `Reserva`, `ControlFrio`. Más `Cargo` con su tipo, para RF-20.

En `Dominio/Enumeraciones/`, las que hagan falta: `TipoOrdenProduccion` con faeneo y fabricación, `ResultadoSanitario` con aprobado y rechazado, `EstadoOrdenProduccion`, `EstadoAnimal`, `TipoCargo` con producto y servicio, `EvaluacionFrio`.

Las enumeraciones se guardan como texto, con `HasConversion<string>()`, igual que en el Sprint 1. Es para que una consulta SQL se pueda leer sin diccionario.

**Entregás:** los archivos de entidades y enumeraciones. **Se comprueba:** compila sin advertencias.

### 2. Configuración Fluent y migración · RF-04

En `src/SGCP.Api/Datos/Configuraciones/`, una clase `IEntityTypeConfiguration<T>` por entidad. Longitudes, precisiones, índices y comportamiento de borrado explícitos, como ya están las del Sprint 1.

Cuatro cosas que no se pueden olvidar:

- **Cantidades con tres decimales, importes con dos.** `HasPrecision(12, 3)` para cantidades, `HasPrecision(12, 2)` para dinero.
- **Entrada física única por lote y producto.** Índice único sobre esa combinación en `EntradaInventario`. Es la defensa contra el stock inflado por un doble clic, y tiene que estar en la base, no solo en el servicio.
- **Una sola reserva abierta por detalle de pedido**, si el diseño lo requiere. Si hace falta una unicidad parcial, el patrón es columna generada más índice único, como está explicado en `00_Definicion/Cambio_a_MySQL.md` sección 3. **No uses `HasFilter`**: MySQL no tiene índices filtrados y la migración no se genera.
- **`Restrict` por defecto en lo que tenga historial.** Un lote con entrada no se borra, un animal con control sanitario no se borra. `Cascade` solo de un propietario a sus detalles.

Después, la migración:

```bash
dotnet ef migrations add Sprint2Produccion --project src/SGCP.Api
dotnet ef migrations script --project src/SGCP.Api -o database/Sprint2Produccion.sql
```

**Sin `--idempotent`**: en MySQL genera sintaxis de T-SQL y el script no se puede aplicar. La explicación está en `Cambio_a_MySQL.md` sección 4.

**Entregás:** configuraciones, migración y script. **Se comprueba:** `dotnet ef database update` contra MySQL real, dos veces seguidas, y `dotnet ef migrations has-pending-model-changes` sin cambios pendientes.

### 3. Permisos nuevos · RNF-03

En `src/SGCP.Api/Seguridad/Permisos.cs`, los permisos de los dos actores nuevos: producción y almacén. Y en `Datos/DatosIniciales.cs`, las responsabilidades que los agrupan, sembradas de forma idempotente como las del Sprint 1.

Producción administra animales, sanidad y órdenes. Almacén registra pesajes, entradas y consulta existencias. Ninguno de los dos ve precios de venta ni márgenes: eso es de administración y ventas.

**Entregás:** permisos y responsabilidades sembradas. **Se comprueba:** un usuario de producción recibe 403 al pedir precios o márgenes.

### 4. Las cuatro reglas del criterio de validación · RF-04, RF-18

Esta es la tarea que define el sprint. En `src/SGCP.Api/Servicios/`.

**4.1 Una orden produce varios productos en lotes distintos.** Confirmar una orden de faeneo crea un `ResultadoProduccion` por cada producto obtenido, cada uno con su `Lote`. El servicio acepta una lista, no un solo producto.

**4.2 Confirmar el peso no suma stock. La entrada física sí.** Dos operaciones separadas, con dos endpoints distintos. Registrar un `Pesaje` guarda bruto, tara, neto, unidad, producto, lote y responsable, y **no modifica `Existencia`**. Solo `EntradaInventario` la modifica. Que sean dos endpoints no es un detalle de diseño: es cómo se demuestra la regla.

**4.3 El rechazo bloquea.** Un `ControlSanitario` con resultado de rechazo pasa el animal a bloqueado e impide crear o confirmar una orden de faeneo sobre él. Y la parte que se olvida: si un insumo ya se consumió en una fabricación y después se rechaza, **el consumo no se revierte**. Se registra el rechazo y queda la trazabilidad de que ese derivado salió de un insumo que después fue rechazado. No hay compensación automática.

**4.4 No se reservan previsiones.** Crear una `Reserva` valida contra la `Existencia` física apta. Si no hay stock, la operación se rechaza con un código de error claro. Una orden de producción planificada no genera disponibilidad de ninguna clase.

Los errores se devuelven con `ReglaException`, con código en mayúsculas y mensaje en lenguaje del negocio, como los del Sprint 1: `ANIMAL_RECHAZADO`, `SIN_EXISTENCIA_DISPONIBLE`, `ENTRADA_YA_REGISTRADA`, `PESAJE_NO_MUEVE_STOCK` si alguien intenta usarlo mal.

**Entregás:** los servicios con las cuatro reglas. **Se comprueba:** cada una por HTTP, en los dos sentidos: que el caso válido pasa y que el inválido se rechaza con su código.

### 5. Factory Method · RF-04

En `src/SGCP.Api/Patrones/Produccion/`, junto al `PedidoBuilder` del Sprint 1 que te sirve de modelo de estilo.

El producto resultante de una orden no se construye igual en un faeneo que en una fabricación: el primero hereda procedencia y lote del animal, el segundo la trazabilidad de los insumos. En lugar de un condicional dentro del servicio que crece con cada tipo nuevo, una fábrica por tipo de orden y un método que las elige.

Lo importante para la defensa oral: tenés que poder explicar **por qué** este patrón acá y no otro. La respuesta es que la decisión de qué crear depende del tipo de orden, y se espera que aparezcan más tipos.

**Entregás:** el patrón y su uso desde el servicio de confirmación. **Se comprueba:** agregar un tipo de orden nuevo no obliga a modificar el servicio.

### 6. Trazabilidad · RNF-06

El `ServicioAuditoria` del Sprint 1 ya guarda usuario, fecha, entidad y referencia. Extendelo a las operaciones nuevas: sanidad, confirmación de orden, pesaje, entrada, reserva y control de frío.

Lo que pide RNF-06 y conviene no olvidar: **las anulaciones mantienen historial**. Anular una entrada no borra la fila: registra la anulación con su autor y su motivo.

**Entregás:** auditoría extendida. **Se comprueba:** el conteo de registros de auditoría crece con cada operación nueva del recorrido.

### 7. Endpoints y documentación

En `src/SGCP.Api/Controllers/`, los controladores nuevos. Rutas bajo `/api/v1`, en plural y en español, siguiendo las que ya existen.

Al terminar, actualizá la tabla de rutas del `README.md` de SGCPapi. S2-P2 trabaja contra esa tabla y contra Swagger: si no está, te va a preguntar lo mismo cinco veces.

**Entregás:** controladores, Swagger al día y README actualizado. **Se comprueba:** Swagger lista todas las rutas nuevas con sus cuerpos y enumeraciones.

## Qué no te toca

Pantallas, vistas Razor y Kotlin: eso es S2-P2. Diagramas UML: S2-P4. Escribir los criterios de aceptación: S2-P3. Poner la etiqueta de versión: S2-P4, al cerrar el sprint.

Tampoco te toca pagos, transporte, entregas ni reportes: son los sprints 3 y 4.

## De quién dependés y quién depende de vos

**Dependés de** S2-P3 para los criterios de aceptación detallados. No es un bloqueo total: el parámetro de aceptación del Excel ya está escrito y alcanza para empezar.

**Depende de vos** S2-P2, que no puede hacer nada hasta que haya endpoints en Swagger. Por eso conviene publicar el contrato temprano, aunque la implementación esté a medias: primero las rutas y los cuerpos, después las reglas finas.

## Cómo entregarlo

```bash
git checkout -b sprint2/p1-api-produccion
git commit -m "v2.1.0 - Sprint 2 - API de produccion e inventario"
git push -u origin sprint2/p1-api-produccion
```

Pull Request con el código `S2-P1` en el cuerpo. La etiqueta de versión la pone S2-P4 al cerrar el sprint; no la pongas vos.

Antes de abrir el PR, las cuatro condiciones de terminado: compila sin advertencias, las cuatro reglas comprobadas por HTTP, README actualizado, migración aplicada contra MySQL real dos veces.

## Tres cosas que ya se rompieron una vez

Están documentadas en `00_Definicion/Errores_encontrados_Sprint1.md` y la misma clase de error vuelve con el primer campo decimal que agregues:

1. **`[Range(typeof(decimal), "0.01", ...)]` sin `ParseLimitsInInvariantCulture`** devuelve 500 en toda petición con decimales cuando la máquina está en español. Vas a agregar muchos campos decimales en este sprint.
2. **`HasFilter` no existe en MySQL.** Si necesitás unicidad parcial, columna generada más índice único.
3. **Correr las pruebas con `LANG` sin definir** esconde los defectos de cultura. Usá `LANG=es_BO.UTF-8` y repetí con `LANG=C`.
