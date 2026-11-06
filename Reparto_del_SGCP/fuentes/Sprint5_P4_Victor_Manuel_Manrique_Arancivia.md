# Sprint 5 · Parte 4 · Victor Manuel Manrique Arancivia

Código de seguimiento: **S5-P4**. Rol: Scrum Master. Repositorio: **SGCPdocumentacion**.

> Sprint de reserva. **Tu parte arranca primero y define el sprint**: hasta que la lista de pendientes no exista, nadie sabe qué le toca.

## Qué te toca

Armar la lista real de pendientes, cerrar el RNF-02, decidir con el equipo si hay margen para la prueba de React, y cerrar el proyecto de forma definitiva.

## Tus tareas

### 1. La lista de pendientes · primero, bloquea a todos

Recorré los cuatro sprints y armá la lista de lo que quedó. No de memoria: con el Excel y los documentos de validación al lado.

Para cada sprint, tres preguntas:

- ¿Todos sus requerimientos están entregados? Si no, cuáles faltan.
- ¿Su criterio de validación pasa hoy? No cuando se entregó: **hoy**.
- ¿Quedó algo marcado como pendiente en su documento de validación?

Pendientes conocidos al cerrar el Sprint 1, si no se cerraron después:

| Pendiente | De quién |
|---|---|
| APK probado en un teléfono físico | S5-P2 |
| RNF-04, usabilidad | S5-P3 |
| RNF-02, rendimiento | S5-P4, vos |
| Observaciones del docente atendidas | S5-P1 |

La segunda pregunta es la importante. Un criterio que pasaba en el Sprint 2 y hoy no pasa es una regresión, y una regresión vale más que cualquier cosa nueva que se pueda agregar en este sprint.

**Entregás:** `00_Definicion/Pendientes_Sprint5.md` con la lista y a quién le toca cada cosa. **Se comprueba:** está el primer día del sprint.

### 2. RNF-02, el rendimiento · es tu pendiente desde el Sprint 1

Si el Sprint 4 lo cerró con las pruebas de volumen, esta tarea no existe. Si no:

Sembrá datos de volumen —unos miles de pedidos con sus detalles, clientes, productos y movimientos de inventario— y medí los tiempos de respuesta de lo que más se usa: listados con filtros, confirmación de pedido, consulta de stock y los reportes.

Lo que buscás no es un número bonito: es **la consulta que con cinco filas responde al instante y con mil tarda veinte segundos.** Casi siempre existe. Encontrarla ahora es mucho mejor que encontrarla en la defensa.

Dónde mirar cuando aparezca: consultas que recorren tablas enteras, y el patrón de una consulta dentro de un bucle, que con pocos datos no se nota. Activá el registro de consultas de EF Core y mirá el SQL que realmente se ejecuta; si una pantalla genera cien consultas, el registro lo muestra enseguida.

**Entregás:** una tabla de operación, cantidad de datos y tiempo. **Se comprueba:** hay medición con volumen, no con la base vacía.

### 3. Decidir si hay margen para React

La prueba de React tiene tres condiciones y vos sos el que puede verificar la primera: que los sprints 1 a 4 estén cerrados de verdad, con la lista de la tarea 1 en la mano.

Si queda **un solo** pendiente abierto, la respuesta es no. Y conviene decirlo sin rodeos en la reunión: el riesgo de una prueba técnica mientras hay funcionalidad abierta no se compensa con nada.

Si todo está cerrado: repositorio nuevo, `SGCPuireact`, dos o tres pantallas de lectura, sin tocar `SGCPuiweb`.

**Entregás:** la decisión escrita con el motivo. **Se comprueba:** se apoya en la lista de pendientes, no en ganas.

### 4. Cerrar la documentación

Última pasada por todo:

- Los diagramas coinciden con el código entregado, incluido lo que se haya agregado en este sprint.
- El diccionario de datos coincide con `information_schema`.
- El Excel tiene los cinco sprints con su estado. El 5 también, aunque el estado sea «cerrado sin trabajo».
- El índice de `SGCPdocumentacion` lista todos los documentos y ningún enlace está roto.
- Los cuatro README tienen su tabla de historial al día.

Para los enlaces, una revisión rápida en lugar de abrirlos uno por uno:

```bash
grep -oP '\]\(\K[^)#]+(?=\))' LEEME.md | while read r; do
  [ -e "$r" ] || echo "roto: $r"
done; echo "sin salida = todo bien"
```

**Entregás:** la documentación cerrada. **Se comprueba:** el comando no devuelve nada.

### 5. El paquete de entrega definitivo

Si el sprint agregó algo, se rearma. Si no, el del Sprint 4 queda como final y se deja constancia de eso.

```bash
zip -r SGCP_Entrega_Final.zip SGCPapi SGCPuiweb SGCPuimovil SGCPdocumentacion \
  -x '*/bin/*' '*/obj/*' '*/.vs/*' '*/.git/*' '*/build/*' '*/.gradle/*' '*/node_modules/*'
unzip -l SGCP_Entrega_Final.zip | grep -E '/(bin|obj|\.vs)/' ; echo "vacio = correcto"
```

Y lo mismo que en el Sprint 4: descomprimilo en otra carpeta y revisá que no haya quedado ninguna clave adentro.

**Entregás:** el `.zip`. **Se comprueba:** la revisión no devuelve nada.

### 6. Las versiones finales

Si el sprint tuvo trabajo, `v5.0.0` en los repositorios tocados, después del commit:

```bash
git tag -a v5.0.0 -m "Sprint 5 - Cierre del proyecto"
git push origin main --follow-tags
```

Si no tuvo trabajo, **no se crea `v5.0.0`.** `v4.0.0` queda como la versión final y se registra en el documento de cierre. Una etiqueta sin cambios no agrega nada y confunde el historial.

**Entregás:** las etiquetas o la constancia de que no se crearon. **Se comprueba:** `git tag -l` coincide con lo entregado.

### 7. El documento de cierre

Una página, en `00_Definicion/Cierre_del_proyecto.md`:

- Qué se hizo en este sprint, o que se cerró sin trabajo y qué se revisó para concluirlo.
- El estado final de los cinco sprints.
- La versión final de cada repositorio.
- Qué quedó fuera y por qué.
- El trabajo futuro: los diferidos no tomados, RF-11 si quedó sin habilitar, la versión en React si no se hizo.

El último punto conviene escribirlo bien. Un proyecto que dice «esto queda para después, por este motivo» se ve terminado; uno que no lo dice se ve incompleto, aunque haya entregado exactamente lo mismo.

**Entregás:** el documento de cierre. **Se comprueba:** responde qué se entregó, qué no y por qué, sin tener que preguntarle a nadie.

## Qué no te toca

Escribir código. La consulta al docente y la aceptación del producto: S5-P3.

## De quién dependés y quién depende de vos

**No dependés de nadie para la tarea 1**, y esa tarea bloquea a los otros tres. Hacela el primer día.

**Dependés de S5-P3** para saber qué dijo el docente.

**Depende de vos el cierre del proyecto.**

## Cómo entregarlo

```bash
git checkout -b sprint5/p4-cierre-proyecto
git commit -m "v5.1.0 - Sprint 5 - Pendientes, rendimiento y cierre del proyecto"
git push -u origin sprint5/p4-cierre-proyecto
```

Pull Request con el código `S5-P4` en el cuerpo.
