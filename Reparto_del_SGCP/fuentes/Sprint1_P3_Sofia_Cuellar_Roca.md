# Sprint 1 · Parte 3 · Sofia Cuellar Roca

Código de seguimiento: **S1-P3**. Rol: Product Owner. Terreno: requisitos, criterios y validación.

## Estado: dos tareas abiertas

El Sprint 1 está construido y verificado técnicamente, pero falta tu parte: **decir si cumple lo solicitado**. Eso no lo dice una prueba automática, lo dice el Product Owner.

Y falta medir RNF-04, usabilidad, que es tuyo por rol y no se puede calcular: se observa.

## Tu tarea 1: validar los criterios contra lo entregado

El criterio de validación del Sprint 1 en el Excel dice:

> Todos se autentican; alta pública solo comprador. Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar historial.

Son cinco afirmaciones. Hay un recorrido automático de 27 comprobaciones que las ejerce, pero **una prueba automática comprueba que el sistema hace lo que el programador entendió**, no que haga lo que el negocio pidió. Lo segundo es tu trabajo.

El recorrido que conviene hacer a mano, en la web, es el que está en `00_Definicion/Como_ejecutar_el_sistema.md` sección 5. Son nueve pasos y termina en la regla más importante del sprint:

1. Entrar con `admin`.
2. Crear una clasificación `Costilla`, familia `Carne fresca`.
3. Crear el producto `Costilla de cerdo`, unidad `kg`. **Tiene que quedar sin stock.**
4. Registrar costo `28.00` y precio `35.00`.
5. Crear un cliente.
6. Crear una cotización con 4 kg a Bs 35 y presentarla.
7. Intentar crear el pedido: **tiene que negarse**, porque está presentada y no aceptada.
8. Aceptarla y confirmar el pedido. El margen tiene que mostrar **Bs 28**.
9. Registrar una vigencia nueva de Bs 40 y volver al pedido: **el margen sigue en Bs 28**.

Los pasos 7, 8 y 9 son los que el docente va a mirar, porque son los que están escritos como criterio de validación.

Lo que tenés que registrar por cada una de las cinco afirmaciones: si cumple, cómo lo comprobaste, y qué observaste que no está mal pero podría ser mejor. Esa tercera columna es la que vale para el sprint siguiente.

Y dos cosas que conviene mirar aunque no estén en el criterio, porque son de tu terreno: que los importes se vean en formato boliviano, con coma decimal y el símbolo `Bs`, igual que en los mockups; y que las unidades estén visibles en pantalla, porque RNF-04 lo pide explícitamente.

**Entregás:** `00_Definicion/Validacion_Sprint1.md` con las cinco afirmaciones y su veredicto. **Se comprueba:** cada una tiene escrito cómo se comprobó, no solo un sí.

## Tu tarea 2: medir RNF-04, usabilidad

El requerimiento dice:

> La interfaz priorizará lenguaje del negocio, búsqueda ágil, unidades visibles y confirmación de operaciones; su uso se validará con personal representativo.

La última frase es la que falta. **Personal representativo significa gente que no participó del desarrollo.** Entre ustedes cuatro no sirve: ya saben dónde está cada botón.

Lo mínimo que funciona como evidencia, y que se hace en una sesión de media hora:

- **Dos o tres personas** ajenas al equipo. Alguien que use WhatsApp y cuaderno es el perfil exacto que describe el perfil de proyecto.
- **Una tarea concreta por persona**, dicha en lenguaje del negocio y sin explicar cómo: «cargá este cliente nuevo», «armá una cotización de 4 kilos de costilla», «confirmá este pedido».
- **No ayudar.** Si se traban, eso es el dato.

Lo que se anota, que son las cuatro cosas que el requerimiento nombra:

| Qué observar | Qué anotar |
|---|---|
| Lenguaje del negocio | Qué palabra de la pantalla no entendieron |
| Búsqueda ágil | Cuánto tardaron en encontrar un cliente en la lista |
| Unidades visibles | Si dudaron de si era kilos o unidades |
| Confirmación de operaciones | Si supieron que la operación se había guardado |

Más: la tarea, quién la hizo, cuánto tardó y dónde se trabó.

Esto no se puede inventar. Es lo que convierte a RNF-04 en algo demostrable en lugar de una frase en el documento, y es el tipo de evidencia que un docente de Ingeniería de Software reconoce de inmediato.

**Entregás:** una nota de una página en `00_Definicion/`. **Se comprueba:** hay nombres de tareas, tiempos y frases textuales de lo que dijeron.

## Tu tarea 3, cuando llegue: traducir la devolución del docente

Cuando el docente revise, lo que observe entra por vos. El camino es: lo traducís a cambios concretos, cada uno con su requerimiento afectado y su parte responsable, y de ahí se reparte.

Si va directo del docente a los desarrolladores, se pierde el registro de por qué se cambió algo, y en la siguiente revisión nadie sabe de dónde salió ese cambio.

**Entregás:** la lista de cambios pedidos con su responsable. **Se comprueba:** cada cambio tiene un código de parte asignado.

## Lo que no te toca

Programar, ni corregir lo que falle. Si una validación no cumple, la reportás con la afirmación que falla y la parte responsable.

RNF-02, desempeño, es de S1-P4.

## Cuándo

Durante el Sprint 2, en paralelo. Son dos tareas cortas que no compiten con el desarrollo.

Lo que **no** conviene es dejar RNF-04 para el final del proyecto: es un requerimiento no funcional del Sprint 1 según el Excel. Si se mide en el Sprint 4, se está presentando evidencia de otro sistema.

## Cómo entregarlo

Tus entregables son documentos, van a **SGCPdocumentacion**:

```bash
git checkout -b sprint1/p3-validacion
git commit -m "v1.0.1 - Sprint 1 - Validacion de criterios y usabilidad"
git push -u origin sprint1/p3-validacion
```

Pull Request con el código `S1-P3` en el cuerpo.
