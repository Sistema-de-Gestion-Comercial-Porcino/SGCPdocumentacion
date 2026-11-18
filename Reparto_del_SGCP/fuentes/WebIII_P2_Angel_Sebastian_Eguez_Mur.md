# Web III · Parte 2 · Angel Sebastian Eguez Mur

Código: **W3-P2**. Repositorio: **SGCPapi**. Usuario de GitHub: `sebaxtianmur89`. Rama: `sprint4/p2-api-clientes-rest`. Versión: **v4.2.0**.

## Qué te toca

Dejar **Clientes** como recurso REST completo, que es lo que el docente va a mirar en Swagger. Es el bloque más grande de la rúbrica: **25 puntos de operaciones**, más parte de DTO y de validación.

Partes de `main` después de que se fusionen SGCPapi#2 y #3. Solo tocas `ClientesController`, sus DTO, `ServicioClientes` y las pruebas. Victor trabaja en los otros controladores, así que no van a chocar.

## Tus tareas

### 1. DTO de salida · rúbrica «DTO de entrada y salida» (5)
Hoy `GET clientes/{id}` devuelve la entidad de EF tal cual. Crea `ClienteRespuesta` en `Contratos/Respuestas/` con lo que el cliente necesita ver:
- `Id`, `Nombre`, `Tipo`, `IdentificacionFiscal`, `Telefono`, `Direccion`, `Activo`;
- y la fecha de alta, si el modelo la tiene.

Úsalo en `GET clientes`, en `GET clientes/{id}` y en la respuesta del POST y del PUT.

**Se comprueba:** Swagger muestra el esquema `ClienteRespuesta`, no `Cliente`.

### 2. POST con 201 y Location · rúbrica (6)
Hoy el POST responde `StatusCode(201, new { Id })`, que **no lleva cabecera `Location`**. Cámbialo a:

```csharp
return CreatedAtAction(nameof(Ver), new { id }, respuesta);
```

donde `respuesta` es el `ClienteRespuesta` del cliente creado. Hazlo también en el POST de **Productos** y en el de **Cotizaciones**, que son los otros dos que usa la evidencia.

**Se comprueba:** la respuesta del POST trae `Location: http://.../api/v1/clientes/{id}` y un `GET` a esa URL devuelve el mismo cliente.

### 3. DELETE con regla de dominio · rúbrica «PUT y DELETE» (9) y «regla del dominio» (5)
Nuevo `DELETE api/v1/clientes/{id}`, con la política `clientes.administrar`:

| Situación | Respuesta |
|---|---|
| El cliente no existe | **404** `NO_ENCONTRADO` |
| Tiene cotizaciones, pedidos, pagos o una cuenta de comprador | **409** `CLIENTE_CON_HISTORIAL`, con un mensaje que diga que hay que desactivarlo en lugar de borrarlo |
| No tiene nada asociado | **204**, borrado físico y registro en la auditoría (`auditoria.Registrar("ELIMINAR_CLIENTE", ...)`) |

La regla existe porque borrar un cliente con historial rompería la trazabilidad de saldos, que es el problema central del caso. Por eso existe el «desactivar».

### 4. Recurso relacionado · rúbrica (4)
Nuevo `GET api/v1/clientes/{id}/pedidos?pagina=&tamanoPagina=`:
- devuelve 404 si el cliente no existe;
- usa una proyección a DTO (código, fecha, estado comercial y total), nunca la entidad completa;
- para el comprador aplica `actor.VerCliente(id)`, para que solo vea los suyos.

### 5. Anotaciones de Swagger en ClientesController
`[ProducesResponseType]` en cada acción, con todas sus respuestas posibles: 200 o 201 o 204, 400, 401, 403, 404 y 409, según corresponda. Agrega un comentario `/// <summary>` corto por acción; el proyecto ya genera la documentación XML.

### 6. Pruebas
En `tests/SGCP.Verificacion` (en `Program.cs` o en un archivo nuevo, `ClientesRest.cs`), una comprobación por cada caso:
- POST devuelve 201 y la cabecera `Location`, y un `GET` a esa `Location` responde 200;
- DELETE de un cliente sin historial da 204 y después el GET da 404;
- DELETE de un cliente con pedido da 409;
- DELETE y GET de un id inexistente dan 404;
- `clientes/{id}/pedidos` devuelve los pedidos del cliente, y el comprador ajeno recibe 403.

**Se comprueba:** el verificador pasa completo con `SGCP_MYSQL_TEST`, y el CI de SQL Server queda en verde en tu PR.

## Entregas
Un PR `v4.2.0 - Sprint 4 - Clientes REST: DTO de salida, 201 con Location, DELETE con regla y pedidos del cliente`, con su fila en el Historial y la sección «Rutas principales» del README actualizada.
