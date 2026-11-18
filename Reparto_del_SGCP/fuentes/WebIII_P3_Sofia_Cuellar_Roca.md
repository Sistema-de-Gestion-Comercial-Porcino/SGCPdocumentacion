# Web III · Parte 3 · Sofia Cuellar Roca

Código: **W3-P3**. Repositorio: **SGCPapi**. Usuario de GitHub: `sof1345`. Rama: `sprint4/p3-api-entrega-webiii`. Versión: **v4.3.0**.

> Ojo con la identidad: en SGCPdocumentacion tus commits salen con dos nombres, «Sofia Cuellar Roca» y «sof1345». Antes de empezar, revisa que `git config user.email` sea un correo verificado en tu cuenta `sof1345`. Si no, tus commits no se te atribuyen y pierdes los 5 puntos de participación.

## Qué te toca

La documentación técnica de la entrega: el README que pide la consigna, el script que arma el ZIP limpio y el PDF de evidencias.

## Tus tareas

### 1. Sección «Entrega Web III · API Integrador» al principio del README · rúbrica «README» (2)
**Se agrega sin borrar nada de lo que ya tiene el README.** Va justo debajo del título y contiene:
- **Proyecto:** SGCP · Sistema de Gestión Comercial Porcino (CRM de ventas para una chanchería), con dos o tres líneas que expliquen qué hace la API.
- **Versión de .NET:** .NET 10 (`net10.0`), EF Core 10.0.12.
- **Integrantes y usuarios de GitHub**, en tabla:

  | Integrante | GitHub |
  |---|---|
  | Dario Haziel Tambo Parra | `SuperGenio56` |
  | Angel Sebastian Eguez Mur | `sebaxtianmur89` |
  | Sofia Cuellar Roca | `sof1345` |
  | Victor Manuel Manrique Arancivia | `VictorManrique01` |

- **Repositorio:** https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPapi
- **Pasos rápidos para SQL Server**, numerados del 1 al 4 (conexión, migración, datos de prueba y Swagger). Son un resumen que enlaza a la sección «Usar SQL Server en lugar de MySQL» que ya escribió Dario; no la copies entera.
- **Recurso principal y relacionado:** Clientes y Pedidos del cliente, con las rutas que deja Sebastián.
- **Evidencias:** un enlace a `docs/Evidencias_API_Integrador.pdf`.

### 2. Script de empaquetado · rúbrica «ZIP completo y limpio» (3)
`scripts/Empaquetar-Entrega.sh` (y su versión `.ps1` para Windows), que genere `SGCPapi_Entrega.zip` con `git archive`. Así solo entra lo versionado y nunca `bin`, `obj`, `.vs` ni secretos. Además tiene que:
- agregar `docs/Evidencias_API_Integrador.pdf` aunque no esté versionado;
- terminar listando el contenido del ZIP y **fallando** si encuentra `bin/`, `obj/`, `.vs/`, `secrets.json` o `appsettings.Development.json`.

**Se comprueba:** se corre el script y se lista el ZIP, sin esas carpetas.

### 3. PDF de evidencias · rúbrica «Evidencias» (7)
`docs/Evidencias_API_Integrador.pdf`, armado con las capturas que te pasa Victor el jueves. La consigna pide:
1. **Una captura de Swagger UI** donde se vean los endpoints.
2. **Cada prueba identificada con su operación y su código HTTP**, por ejemplo «POST /api/v1/clientes → 201 Created». Usa una tabla con número, operación, entrada, código esperado, código obtenido y captura.
3. **Las respuestas 400 y 404**, como mínimo: un POST con un campo obligatorio vacío da 400, y un GET o DELETE de un id inexistente da 404.
4. **La persistencia:** un `GET` hecho **después de reiniciar la API** que devuelve el cliente creado antes. En las capturas tiene que verse la hora de antes y de después del reinicio.

Portada con el logo de la universidad, la materia (Web III), los integrantes y la fecha.

## Entregas
Un PR `v4.3.0 - Sprint 4 - Documentacion: README de entrega Web III, empaquetado y evidencias`. Puedes abrirlo el miércoles con los puntos 1 y 2, y agregar el PDF el jueves con un segundo commit en la misma rama.
