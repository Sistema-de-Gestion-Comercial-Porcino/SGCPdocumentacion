# Sprint 2 · Documento general

Producción, catálogo parametrizado, inventario y reservas, control sanitario y control de frío.

Alcance tomado del Sprint Backlog de `Formato Proyecto - SGCC Actualizado.xlsx`. Este documento no agrega ni quita requerimientos: reparte el trabajo y dice cómo se comprueba.

## Qué entra en este sprint

| Código | Nombre | Parte responsable |
|---|---|---|
| RF-04 | Gestionar catálogo, producción, inventario y pesajes | S2-P1, S2-P2 |
| RF-18 | Registrar control sanitario previo al faeneo | S2-P1, S2-P2 |
| RF-17 | Registrar control de frío | S2-P1, S2-P2 |
| RF-20 | Separar cargos de producto y servicio | S2-P1, S2-P2 |
| RNF-03 | Seguridad: confidencialidad y respaldo | S2-P1, S2-P4 |
| RNF-06 | Seguridad: trazabilidad | S2-P1, S2-P4 |

Actores que entran en juego: **ACT-03 Producción** (animales, sanidad, órdenes y resultados por lote) y **ACT-04 Almacén** (pesajes manuales, entradas, stock y reservas). Los dos son nuevos: en el Sprint 1 solo existían administración, ventas y comprador.

## El criterio de validación, palabra por palabra

El Excel lo dice así, y es exactamente lo que hay que poder demostrar:

> Una orden produce costilla y lomo en lotes distintos. Confirmar peso no suma stock; entrada física sí. Rechazo bloquea; consumo de derivado rechazado no se revierte por ficción. No se reservan previsiones.

Son cuatro afirmaciones y conviene leerlas como cuatro pruebas separadas:

1. **Una orden produce varios productos en lotes distintos.** Un faeneo no da "carne": da costilla en un lote y lomo en otro, cada uno con su cantidad real.
2. **Confirmar el peso no suma stock. La entrada física sí.** Son dos pasos distintos y en ese orden. El pesaje es un dato registrado; el stock solo cambia cuando almacén confirma que el producto entró de verdad.
3. **Un rechazo sanitario bloquea.** El animal rechazado no se faena y la orden asociada queda bloqueada. Y si un insumo ya se consumió y después se rechaza, el consumo **no se revierte**: se registra el hecho, no se finge que no pasó.
4. **No se reservan previsiones.** Solo se puede reservar stock físico que existe. Una producción planificada no genera disponibilidad.

## Lo que este sprint no hace

Conviene decirlo para que nadie construya de más:

- No hay pagos, crédito ni saldos: eso es Sprint 3.
- No hay transporte, rutas ni entregas: Sprint 3.
- No hay captura sin conexión en Android: Sprint 3.
- No hay reportes ni exportación a PDF o Excel: Sprint 4.
- No se mide temperatura automáticamente. RF-17 es **registro manual** con evaluación humana. La balanza es una herramienta física sin conexión al sistema: los pesajes se escriben a mano.
- No se calcula costo de producción automáticamente. El tiempo de faeneo se registra como estimado y real, sin fijar una duración estándar.

## Reparto

| Código | Integrante | Trabajo | Empieza |
|---|---|---|---|
| S2-P1 | Dario Haziel Tambo Parra | API: modelo de datos, migración, reglas, endpoints, Factory Method | Primero |
| S2-P2 | Angel Sebastian Eguez Mur | Web: pantallas de sanidad, producción, pesajes, inventario, frío y cargos | Cuando P1 publique los endpoints en Swagger |
| S2-P3 | Sofia Cuellar Roca | Criterios de aceptación, guion de prueba, validación de mockups, backlog | En paralelo con P1; cierra validando |
| S2-P4 | Victor Manuel Manrique Arancivia | Diagramas, pruebas automáticas, CI, medición, versión y entrega | En paralelo con P1; cierra entregando |

## Dependencias, en orden

```
S2-P3 (criterios)  ──┐
                     ├──> S2-P1 (API) ──> S2-P2 (web) ──> S2-P3 (validacion) ──> S2-P4 (entrega)
S2-P4 (diagramas) ──┘
```

El único bloqueo duro es **P1 antes de P2**. Y dentro de P1 hay un orden obligatorio por el propio modelo: sanidad antes de producción, producción antes de pesaje, pesaje antes de entrada, entrada antes de reserva. Si se construye al revés no hay forma de probar nada, porque cada paso necesita el anterior para existir.

## El modelo de datos nuevo

Once entidades nuevas. Los nombres están propuestos para seguir la convención del Sprint 1, en español y en singular.

| Entidad | Para qué | Reglas que la gobiernan |
|---|---|---|
| `Animal` | Identificación y procedencia del animal | Un animal rechazado no puede entrar a una orden de faeneo |
| `ControlSanitario` | Resultado sanitario previo al faeneo | Un resultado de rechazo bloquea al animal y a su orden |
| `OrdenProduccion` | Faeneo o fabricación | Lleva tipo, estado, responsable, tiempo estimado y tiempo real |
| `InsumoProduccion` | Lo que consume una orden de fabricación | Cantidad real consumida, no planificada |
| `Lote` | Agrupa lo producido en una corrida | Código único; una orden puede generar varios |
| `ResultadoProduccion` | Producto obtenido, su lote y su cantidad real | Varios por orden, cada uno con su lote |
| `Pesaje` | Bruto, tara, neto, unidad, producto, lote, responsable | Registrarlo **no** mueve stock |
| `EntradaInventario` | Entrada física confirmada por almacén | Única por lote y producto. Esto **sí** mueve stock |
| `Existencia` | Cantidad física apta por producto y lote | Disponible = físico apto − reservas |
| `Reserva` | Cantidad comprometida con un pedido | Solo sobre existencia física; nunca sobre previsión |
| `ControlFrio` | Temperatura registrada a mano y su evaluación | Referencia a lote, ubicación o entrega, y responsable |

Para RF-20, los cargos de producto y de servicio se separan. La forma más simple y menos invasiva es una entidad `Cargo` con un campo de tipo (`PRODUCTO` o `SERVICIO`), en lugar de dos tablas paralelas que después hay que sumar en todas las consultas.

## El patrón de este sprint

**Factory Method**, en la API. Una orden de producción termina creando el producto resultante, y el resultado no se construye igual según el caso:

- Un **faeneo** produce cortes a partir de un animal: el resultado hereda la procedencia y el lote del animal.
- Una **fabricación** produce un derivado a partir de insumos: el resultado hereda la trazabilidad de los insumos consumidos.

Es el caso para el que sirve Factory Method: la decisión de qué crear y cómo depende del tipo de orden, y el servicio que la confirma no debería tener un condicional creciendo cada vez que aparece un tipo nuevo.

Esta asignación es una propuesta: el documento `00_Definicion/Organizacion_repositorios_y_patrones.md` lista los siete patrones pero no los reparte por sprint. Lo confirma Sofía, o se consulta al docente.

## Riesgos de este sprint

| Riesgo | Por qué importa | Qué hacer |
|---|---|---|
| El docente pide cambios del Sprint 1 | Producción e inventario se apoyan en productos y catálogo. Un cambio de modelo arrastra | No empezar P1 hasta tener la devolución, o aceptar que puede haber retrabajo |
| Confundir pesaje con entrada | Rompe el criterio de validación más visible del sprint | Dos endpoints y dos pantallas separadas, con nombres distintos |
| Reservar sobre previsiones | El Excel lo prohíbe explícitamente | La reserva valida contra `Existencia`, nunca contra una orden planificada |
| Querer calcular costos automáticamente | Está fuera de alcance y agrega trabajo que nadie pidió | El costo sigue siendo el de referencia que carga administración |
| Entrada física duplicada | Infla el stock y es difícil de detectar después | Restricción de unicidad en la base, no solo validación en el servicio |

## Qué significa que el Sprint 2 está terminado

1. Los cuatro puntos del criterio de validación se pueden demostrar en una corrida seguida, delante del docente.
2. Los tres repositorios compilan sin errores y sin advertencias.
3. La verificación automática cubre los casos nuevos y pasa contra MySQL real.
4. Los diagramas y el diccionario de clases incluyen las entidades nuevas.
5. El backlog del Excel tiene el Sprint 2 marcado y los parámetros de aceptación confirmados.
6. Los cuatro Pull Requests están aprobados y en `main`, con la etiqueta `v2.4.0` puesta por P4.
