# Sprint 5 · Parte 1 · Dario Haziel Tambo Parra

Código de seguimiento: **S5-P1**. Rol: Desarrollador. Repositorio: **SGCPapi**.

> Sprint de reserva. **Nada de acá se arranca sin la lista de pendientes de S5-P4 y sin la autorización del docente** para lo que sea nuevo. Si los sprints 1 a 4 están cerrados, tu parte puede quedar en las tareas 1 y 2 nada más, y eso está bien.

## Qué te toca

Cerrar lo que quedó del API, atender las observaciones del docente, y RF-09 si se aprueba.

## Tus tareas

### 1. Atender las observaciones del docente · siempre, prioridad máxima

Era tu pendiente desde el Sprint 1: el docente todavía no había revisado la entrega cuando se cerró.

Cuando llegue la revisión, lo que diga va **antes que cualquier otra cosa de este documento**. Una observación del docente no atendida cuesta más que un requerimiento diferido que no se hizo.

Para cada observación: qué dijo, qué se cambió, y dónde. Si una no se puede atender, el motivo escrito.

**Entregás:** `00_Definicion/Observaciones_atendidas.md`. **Se comprueba:** cada observación tiene su renglón con el resultado.

### 2. Repasar el API completo

Sin agregar nada, una pasada por lo construido en cuatro sprints:

- Compila sin errores ni advertencias, con `--warnaserror`.
- No hay `TODO`, ni código comentado, ni endpoints de prueba olvidados.
- Ningún endpoint quedó sin autorización. Revisá uno por uno que cada controlador tenga su `[Authorize]` con el rol que corresponde; es el defecto más fácil de dejar y el que peor se ve.
- `appsettings.json` tiene la cadena de conexión vacía, como corresponde: las credenciales van por `user-secrets` o variable de entorno, nunca en el repositorio.
- No hay migraciones pendientes: `dotnet ef migrations has-pending-model-changes --context SgcpContext` (y `--context SgcpContextSqlServer`) no devuelve nada.
- La verificación pasa contra MySQL real.

**Entregás:** una lista corta de lo corregido. **Se comprueba:** los seis puntos revisados.

### 3. RF-09, alertas de inventario · solo si el docente lo aprueba

Es el más razonable de los tres diferidos: el inventario y sus umbrales ya existen desde el Sprint 3, así que el trabajo es la alerta, no el modelo.

Qué hace: cuando el stock de un producto baja del umbral, se genera una alerta para los perfiles de almacén y producción, con producto, stock actual, umbral y fecha.

Tres cosas que hay que decidir antes de escribir código, y que define S5-P3:

- **Cuándo se dispara.** Al momento del movimiento que cruza el umbral, no cada cierto tiempo. Una alerta que aparece al rato es una alerta que llega tarde.
- **Si se repite.** Si el stock sigue bajo, no se genera una alerta por cada movimiento posterior: se genera una y se mantiene abierta hasta que el stock vuelva arriba del umbral. Sin esto, el sistema produce cien alertas de lo mismo y nadie las mira, que es el error clásico de las alertas.
- **Quién las ve y quién las cierra.** Almacén y producción, según la matriz del Sprint 4.

La entidad es una sola: `AlertaInventario`, con producto, stock registrado, umbral, fecha, estado y cuándo se cerró.

**Entregás:** la entidad, su migración y los endpoints. **Se comprueba:** bajás el stock por debajo del umbral y la alerta aparece una vez, no cien.

### 4. El API como servicio para cualquier cliente · si se hace la prueba de React

Si el equipo hace la prueba de React, tu parte es que el API lo permita sin cambiar nada del resto:

- **CORS** habilitado solo para el origen del cliente de React, por configuración, no abierto a todos. Un `AllowAnyOrigin` en un API con autenticación es un hallazgo de seguridad, y si el docente lo ve, pregunta.
- La autenticación por token ya funciona: es lo que usa la aplicación Android desde el Sprint 3. No hay que agregar nada, solo confirmar que sirve desde un navegador.
- Las respuestas ya son JSON con la misma forma. Tampoco hay que cambiar nada.

Esa es la parte interesante del argumento: **el API no necesita cambios para que React funcione**, y poder decir eso en la defensa vale más que las pantallas en sí.

**Entregás:** la configuración de CORS. **Se comprueba:** el cliente de React consulta el API y ningún otro origen puede.

## Qué no te toca

Las pantallas de React: S5-P2. La lista de pendientes y el cierre: S5-P4. Decidir qué se agrega: S5-P3 con el docente.

## De quién dependés y quién depende de vos

**Dependés de S5-P4** para la lista de pendientes, y del **docente** para las observaciones y la autorización de RF-09.

La tarea 2 no depende de nadie. Si el sprint arranca y todavía no hay lista, hacé esa.

## Cómo entregarlo

```bash
git checkout -b sprint5/p1-api-cierre
git commit -m "v5.1.0 - Sprint 5 - Observaciones atendidas y cierre del API"
git push -u origin sprint5/p1-api-cierre
```

Pull Request con el código `S5-P1` en el cuerpo.

Si el sprint se cierra sin trabajo, no hay rama: se deja constancia en el documento de cierre de S5-P4 y listo.
