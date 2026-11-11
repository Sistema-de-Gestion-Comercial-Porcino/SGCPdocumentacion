# RNF-04 · Usabilidad del Sprint 1

Código de seguimiento: **S1-P3**. Responsable: Sofia Cuellar Roca. Fecha: 11 de noviembre de 2026 (hora de La Paz).

El requerimiento dice:

> La interfaz priorizará lenguaje del negocio, búsqueda ágil, unidades visibles y confirmación de operaciones; su uso se validará con personal representativo.

## Sesión con personal representativo: no ejecutada

Personal representativo es gente que no participó del desarrollo. Esta nota no trae nombres, tiempos ni frases textuales porque esa sesión no se hizo. Inventarla dejaría RNF-04 como una frase con apariencia de evidencia.

Lo que falta, y se hace en una sola sentada de media hora, con la web del Sprint 1 ya levantada:

1. Dos o tres personas ajenas al equipo, del perfil del proyecto: usan WhatsApp y anotan en cuaderno.
2. Una tarea por persona, dicha así, sin indicar en qué menú está:
   - «Cargá este cliente nuevo.»
   - «Armá una cotización de 4 kilos de costilla.»
   - «Confirmá este pedido.»
3. No ayudar. Si se traban, eso es el dato.

Por cada persona se anota la tarea, el tiempo, dónde se trabó, y estas cuatro cosas:

| Qué pide RNF-04 | Qué anotar, con sus palabras |
|---|---|
| Lenguaje del negocio | Qué palabra de la pantalla no entendieron |
| Búsqueda ágil | Cuánto tardaron en encontrar un cliente en la lista |
| Unidades visibles | Si dudaron de si era kilos o unidades |
| Confirmación de operaciones | Si supieron que la operación se había guardado |

Cuando exista, esta misma nota se completa con esa tabla llena. Hasta entonces el estado de RNF-04 es **sin medir**.

## Lo que la interfaz ya muestra, sin sustituir la sesión

Revisé las pantallas de `SGCPuiweb` en `main`. Sirve para saber qué preguntar. No sustituye a las personas.

- **Lenguaje.** Cliente, cotización, pedido, costilla, kilogramos y «chanchería» están en las pantallas. Los estados de la cotización se ven como `BORRADOR`, `PRESENTADA`, `ACEPTADA` y `RECHAZADA`. Esa es la palabra que hay que poner delante de alguien que no programó.
- **Búsqueda.** Clientes, productos, cotizaciones y pedidos tienen un campo «Buscar por nombre o código» y un botón Buscar. No busca mientras se escribe: hay que enviar el formulario.
- **Unidades.** La ficha ofrece kg, g o unidad. El listado y la cotización muestran la unidad al lado de la cantidad y del precio (`Bs 35,00/kg`).
- **Confirmación.** Al guardar aparece un aviso: «Ficha de cliente guardada.», «Producto guardado. Esta operación no crea existencias.», «Pedido confirmado. Precio y costo históricos conservados.» Si la cotización no está aceptada, el botón de crear pedido está deshabilitado y el pie explica que una rechazada o vencida no genera pedido.

La sesión tiene que comprobar si eso se entiende, no si el texto está escrito.
