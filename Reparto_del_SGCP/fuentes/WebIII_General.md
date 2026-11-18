# Web III · API Integrador · Reparto general

Entrega en Teams: **viernes 20 de noviembre de 2026, 07:00**. Se sube un ZIP con la Web API (**SGCPapi**) y sus migraciones, sin `bin`, `obj` ni `.vs`, junto con el README y el PDF de evidencias.

## La regla que decide la nota individual

La rúbrica da **15 puntos por persona** según el historial de Git:

- **5 puntos** por tener commits atribuibles a tu usuario.
- **10 puntos** por aportes concretos que se vean en los cambios de esos commits.

Para que cuenten:

- **Haz los commits en SGCPapi con tu propia cuenta de GitHub.** Antes de commitear, revisa `git config user.name` y `git config user.email`. El correo tiene que ser uno que tu cuenta de GitHub tenga verificado; si no, el commit aparece sin dueño.
- **Un cambio de una línea no basta**, según el docente. Cada parte de este reparto es código, pruebas o documentación técnica de verdad.
- Se mantienen las reglas del equipo:
  - rama propia y PR a `main`;
  - el autor no fusiona su propio PR;
  - sin marcas de IA en los commits;
  - una fila nueva en el Historial del README.

**Plazo interno: miércoles 18 de noviembre a las 24:00.** Si a esa hora tu PR no está abierto, Dario hace tu parte el jueves y **quedas fuera de los aportes a la API**. No hay segunda vuelta: el viernes a las 07:00 se entrega.

## Qué pide la rúbrica y quién lo cubre

| Criterio (puntos) | Qué hay que mostrar | Parte |
|---|---|---|
| Modelo relacional y SQL Server (20) | Entidades, claves y relaciones; EF Core con migración aplicable en SQL Server; datos de prueba que siguen ahí después de reiniciar | **P1 Dario**: hecho, PR SGCPapi#3 |
| Operaciones de la API (25) | Listado y consulta por ID; POST con 201 y `Location`; PUT y DELETE funcionales; consulta del recurso relacionado | **P2 Sebastián** |
| Organización y DTO (10) | Modelos, controladores, DTO y datos separados; DTO de entrada y de salida; contexto inyectado y operaciones asíncronas | **P2 Sebastián** (DTO de salida de Clientes); el resto ya existe |
| Validación y errores (10) | Campos obligatorios y regla de dominio; referencias inválidas; 400 y 404 verificables | **P2 Sebastián** (DELETE con regla) y **P4 Victor** (lo documenta y lo prueba) |
| Swagger y pruebas (15) | Swagger con rutas, parámetros, esquemas y respuestas; evidencias de éxitos, errores y persistencia | **P4 Victor** |
| Entrega (5) | ZIP limpio; README reproducible con el enlace al repositorio | **P3 Sofía**; Dario arma el ZIP final |

## Recurso principal elegido: Clientes

Para la evidencia se usa **Clientes** como recurso principal y **Pedidos** como recurso relacionado (un cliente tiene muchos pedidos). Es el recurso más simple de explicar y ya tiene reglas de dominio reales:

- la identificación fiscal no se repite entre clientes activos;
- no se desactiva un cliente con pedidos pendientes.

## Orden de trabajo

1. **Ahora:** alguien que no sea Dario aprueba y fusiona **SGCPapi#2** y **SGCPapi#3**. Todos parten de ese `main`.
2. **P2 y P4 en paralelo:** Sebastián toca `ClientesController` y Victor los demás controladores y la configuración de Swagger. No editan los mismos archivos, así que no chocan.
3. **P3 en paralelo:** README y script de empaquetado.
4. **Jueves 19:**
   - Victor saca las capturas sobre `main` ya integrado.
   - Sofía arma el PDF de evidencias.
   - Dario genera el ZIP y lo sube.

## Versiones de cada PR

Esquema `vSPRINT.PARTE.PARCHE`, con el título `vN.P.x - Sprint 4 - ...`:

| Parte | Rama | Versión |
|---|---|---|
| P1 Dario | `webiii/p1-sqlserver` | v4.1.2 (hecho) |
| P2 Sebastián | `sprint4/p2-api-clientes-rest` | v4.2.0 |
| P3 Sofía | `sprint4/p3-api-entrega-webiii` | v4.3.0 |
| P4 Victor | `sprint4/p4-api-swagger-evidencias` | v4.4.1 |
