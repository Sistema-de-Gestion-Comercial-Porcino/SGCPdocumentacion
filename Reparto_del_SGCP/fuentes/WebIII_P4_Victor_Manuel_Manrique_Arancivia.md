# Web III · Parte 4 · Victor Manuel Manrique Arancivia

Código: **W3-P4**. Repositorio: **SGCPapi**. Usuario de GitHub: `VictorManrique01`. Rama: `sprint4/p4-api-swagger-evidencias`. Versión: **v4.4.1**.

## Qué te toca

Que Swagger documente la API como pide la rúbrica, que dice «rutas, parámetros, esquemas y respuestas» (8 puntos), y que las pruebas de la evidencia se puedan repetir. El viernes el docente abre Swagger: lo que vea ahí es tu parte.

No toques `ClientesController`, que es de Sebastián. Tu trabajo es la configuración de Swagger y los demás controladores.

## Tus tareas

### 1. Configuración de Swagger (`Arranque.cs`, en `AddSwaggerGen`)
- Incluir el archivo de documentación XML (`IncludeXmlComments`). El proyecto ya lo genera (`GenerateDocumentationFile`), pero hay que conectarlo para que los `/// <summary>` salgan en la UI.
- Una descripción de la API con nombre, versión y contacto del equipo.
- Revisar que el botón **Authorize** con JWT funcione. Si falta la definición de seguridad Bearer, agrégala.
- Que los enums se muestren como texto (por ejemplo `ACTIVA`), no como números, si hoy salen como números.

### 2. Respuestas documentadas en Productos, Cotizaciones y Pedidos
En cada acción de `ProductosController`, `CotizacionesController` y `PedidosController`:
- `[ProducesResponseType]` con todas las respuestas posibles (200/201/204, 400, 401, 403, 404, 409), con el tipo `ErrorRespuesta` en los errores;
- y un `/// <summary>` de una línea.

**Se comprueba:** en Swagger, cada operación de esos tres controladores muestra sus códigos y el esquema de error.

### 3. Archivo de pruebas reproducible: `pruebas/API_Integrador.http`
Un archivo `.http`, que se ejecuta desde Visual Studio, Rider o la extensión REST Client de VS Code. Contiene, en orden y con un comentario `### N · OPERACIÓN → código esperado` en cada uno:
1. `POST auth/login` → 200, y guarda el token en una variable.
2. `GET clientes` → 200.
3. `POST clientes` válido → **201 con Location**.
4. `GET clientes/{id}`, usando la Location → 200.
5. `POST clientes` sin nombre → **400**.
6. `POST cotizaciones` con un `clienteId` inexistente → **400 o 404**: la referencia inválida.
7. `PUT clientes/{id}` → 200.
8. `GET clientes/{id}/pedidos` → 200.
9. `GET clientes/{guid inexistente}` → **404**.
10. `DELETE clientes/{id}` con historial → **409**.
11. `DELETE clientes/{id}` sin historial → **204**, y otro GET a ese id → 404.
12. **Persistencia:** detener la API, arrancarla de nuevo y hacer `GET clientes/{id}` del cliente del paso 3 → 200 con los mismos datos.

### 4. Capturas para la evidencia (jueves 19, sobre `main` ya integrado)
Ejecuta el `.http` con la API apuntando a SQL Server, o a MySQL si nadie tiene SQL Server. Saca una captura por paso, con la operación, la URL, el código y el cuerpo visibles, más una de la vista general de Swagger UI. Pásaselas a Sofía en una carpeta nombrada `NN_operacion_codigo.png`, por ejemplo `03_POST_clientes_201.png`.

## Entregas
Un PR `v4.4.1 - Sprint 4 - Swagger documentado y pruebas reproducibles de la API` el miércoles, con los puntos 1 a 3 y su fila en el Historial. Las capturas van el jueves a Sofía.
