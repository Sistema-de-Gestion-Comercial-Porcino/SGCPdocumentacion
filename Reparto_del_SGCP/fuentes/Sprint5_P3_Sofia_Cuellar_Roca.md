# Sprint 5 · Parte 3 · Sofia Cuellar Roca

Código de seguimiento: **S5-P3**. Rol: Product Owner. Repositorio: **SGCPdocumentacion**.

> Sprint de reserva. Tu parte tiene una tarea que va siempre —la consulta al docente— y el resto depende de lo que él responda.

## Qué te toca

Preguntarle al docente qué se hace con este sprint, escribir los criterios de lo que se agregue, cerrar el RNF-04 si todavía no se midió, y dar el visto bueno final al proyecto.

## Tus tareas

### 1. La consulta al docente · primero, va siempre

El Sprint 5 no tiene requerimientos en el Backlog. Eso significa que **la decisión de qué hacer con él no es del equipo**: es del docente.

Preguntale, de forma concreta:

- ¿El Sprint 5 se usa para cerrar pendientes y revisar, o espera que se agregue funcionalidad?
- ¿Autoriza alguno de los diferidos? Si sí, ¿cuál?
- ¿Hay observaciones de la entrega del Sprint 4 que haya que atender primero?

Y llevale la recomendación del equipo escrita, que es: **cerrar pendientes y, si hay autorización, RF-09 solamente.** Es más fácil que apruebe una propuesta concreta que una pregunta abierta.

Si la respuesta es que el sprint se usa para cerrar y revisar, **eso es un resultado válido y conviene decirlo así**: un sprint de reserva que no se usó significa que los cuatro anteriores se cumplieron.

**Entregás:** la respuesta registrada en `00_Definicion/Decisiones.md`, con fecha. **Se comprueba:** está antes de que nadie escriba código.

### 2. RNF-04, la usabilidad · si todavía no se midió

Pendiente desde el Sprint 1. Si el Sprint 4 lo cerró, esta tarea no existe.

La medición: alguien que no sea del equipo, con una explicación de cinco minutos, intenta registrar un cliente, armar una cotización y confirmar el pedido. Se anota cuánto tardó, dónde se trabó, qué preguntó y qué no encontró.

Dos consejos sobre cómo hacerla, porque es fácil hacerla mal:

- **No le ayudes mientras lo intenta.** La tentación es decir «está en el otro menú», y ahí se pierde la medición: lo que buscás es exactamente que no lo encuentre.
- **Anotá lo que preguntó, textual.** Las preguntas son el hallazgo. «¿Y acá el precio lo pongo yo?» dice más de la pantalla que cualquier métrica.

Un compañero de otro grupo es el mejor sujeto: entiende el contexto académico y no conoce el sistema.

**Entregás:** una página con lo observado. **Se comprueba:** hay una persona real y un tiempo anotado.

### 3. Criterios de lo que se agregue · si se agrega algo

Mismo formato de siempre, Dado/Cuando/Entonces, en `00_Definicion/Criterios_Sprint5.md`.

Si va RF-09, las tres decisiones que los desarrolladores necesitan de vos antes de escribir código:

- **Cuándo se dispara la alerta.** La recomendación: en el momento del movimiento que cruza el umbral. Una alerta que llega al rato llega tarde.
- **Si se repite.** La recomendación: no. Una alerta por producto, abierta, hasta que el stock vuelva arriba del umbral. Si se genera una por cada movimiento, el sistema produce cien alertas de lo mismo y nadie las mira. Es el error clásico de las alertas y conviene evitarlo desde el criterio.
- **Quién la ve y quién la cierra.** Almacén y producción, según la matriz de perfiles del Sprint 4.

Los casos a escribir:

- El stock baja del umbral. Entonces: se genera una alerta, una sola.
- El stock sigue bajando con más movimientos. Entonces: la alerta sigue siendo una, no se duplica.
- El stock vuelve arriba del umbral. Entonces: la alerta se cierra.
- Un perfil de ventas pide la lista de alertas. Entonces: no está disponible para ese perfil.

**Entregás:** el archivo de criterios. **Se comprueba:** las tres decisiones están tomadas y escritas antes del código.

### 4. Criterios para la prueba de React · si se hace

Es una prueba técnica, no un requerimiento, así que no necesita criterios de aceptación de negocio. Pero sí dos condiciones, y conviene que estén escritas por vos:

- **No se toca `SGCPuiweb`.** Verificable en el historial del repositorio.
- **Las pantallas de React muestran los mismos datos que las de Razor**, con las mismas reglas de visibilidad por perfil. Si el comprador no ve márgenes en Razor, tampoco en React.

La segunda es la que importa: si la versión de React muestra algo que la otra esconde, el problema no es de React, es que el dato nunca debió salir del API, y eso es un hallazgo del Sprint 4 que se escapó.

**Entregás:** las dos condiciones escritas. **Se comprueba:** se verifican antes de aceptar la prueba.

### 5. El visto bueno final

Como Product Owner, la aceptación formal del proyecto. Una página con:

- Qué se entregó, por sprint.
- Qué no se entregó y por qué. Los diferidos con su motivo, RF-11 con la decisión del Sprint 4.
- Los criterios de los cuatro sprints, con su estado.
- Los seis requerimientos no funcionales, medidos o no, con el motivo.
- La aceptación: el producto cumple lo acordado.

Ese documento es el que conviene tener a mano en la defensa: responde de una sola vez la pregunta de «¿qué falta?», que es la que siempre llega. Y la responde con una decisión registrada en lugar de una improvisación.

**Entregás:** `00_Definicion/Aceptacion_del_producto.md`. **Se comprueba:** cada requerimiento del Excel tiene su estado.

## Qué no te toca

Escribir código. La lista técnica de pendientes y el paquete de entrega: S5-P4.

## De quién dependés y quién depende de vos

**Dependés del docente.** Es lo único que te bloquea, y es lo que bloquea a todos los demás.

**Dependen de vos los tres**, para saber si hay trabajo y cuál.

## Cómo entregarlo

```bash
git checkout -b sprint5/p3-cierre-producto
git commit -m "v5.3.0 - Sprint 5 - Criterios finales y aceptacion del producto"
git push -u origin sprint5/p3-cierre-producto
```

Pull Request con el código `S5-P3` en el cuerpo.
