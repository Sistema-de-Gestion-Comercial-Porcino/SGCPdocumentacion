# Sprint 4 · Documento general

Reportes por perfil con filtros y exportación a PDF y Excel, portal del comprador, constancias de entrega e integración fiscal condicional. Integración y pruebas finales.

Alcance tomado del Sprint Backlog de `Formato Proyecto - SGCC Actualizado.xlsx`.

> Es el último sprint de desarrollo y el que el docente va a ver completo. Tiene menos requerimientos que los anteriores —tres— pero cada uno cruza todos los módulos construidos antes, y uno de ellos **puede no hacerse** si no se cumple su condición.

## Qué entra en este sprint

| Código | Nombre | Parte responsable |
|---|---|---|
| RF-11 | Emitir o consultar comprobante fiscal | S4-P1, S4-P2. **Condicional** |
| RF-14 | Generar constancia de entrega | S4-P1, S4-P2 |
| RF-15 | Gestionar reportes e historial | S4-P1, S4-P2 |

Más la integración y las pruebas finales de todo el sistema, que son de S4-P4, y el portal del comprador, que ya existe desde el Sprint 1 y acá se completa con consulta y exportación de sus propios datos.

## El criterio de validación, palabra por palabra

> Comprador consulta/exporta solo sus datos. Reportes no modifican operaciones. Constancia solo tras recepción conforme central. Emisión fiscal confirmada conserva referencia única.

1. **El comprador ve y exporta solo lo suyo.** Esto se prueba intentando ver lo de otro. Es un control de autorización y es la prueba más importante del sprint: una fuga acá es grave.
2. **Los reportes no modifican nada.** Son de lectura. Ni cambian estados, ni marcan como visto, ni dejan rastro en los datos operativos.
3. **La constancia sale solo después de una recepción conforme confirmada en el servidor.** Una captura pendiente no basta. Y una entrega OBSERVADA tampoco.
4. **Una emisión fiscal confirmada conserva su referencia única.** No se emite dos veces lo mismo.

## RF-11 es condicional: puede no hacerse

El Excel es explícito: la emisión y consulta fiscal «requieren modalidad aplicable y proveedor confirmados y configurados». Y el perfil de proyecto lista RF-11 como condicional, junto a los diferidos.

Qué significa en la práctica: **si no hay proveedor fiscal confirmado, RF-11 no se implementa**, y eso no es una falta. Lo que sí hay que entregar es el diseño del punto de integración —el Adapter— y la decisión escrita de por qué no se completó.

La decisión la toma S4-P3 como Product Owner, con el docente, y conviene tomarla **al principio del sprint**, no al final. Si se deja para el final, se pierde el tiempo de todos esperando una confirmación que no va a llegar.

Mientras no esté habilitada, la operación se registra sin comprobante fiscal, como dice el Excel.

## Lo que este sprint no hace

- No agrega funcionalidad operativa nueva. Todo lo que se reporta ya existe.
- Los reportes **no recalculan** nada. Un margen reportado es el margen histórico que quedó guardado al confirmar el pedido, no un cálculo nuevo con los precios de hoy.
- No se implementan RF-09, RF-16 ni RF-21: están fuera de la entrega según el perfil.

## Reparto

| Código | Integrante | Trabajo | Empieza |
|---|---|---|---|
| S4-P1 | Dario Haziel Tambo Parra | API: consultas de reporte, exportación, constancia, Adapter fiscal y Facade | Primero |
| S4-P2 | Angel Sebastian Eguez Mur | Web: pantallas de reportes con filtros, descargas, portal del comprador | Cuando P1 publique los endpoints |
| S4-P3 | Sofia Cuellar Roca | Criterios, decisión sobre RF-11, qué reporte ve cada perfil, validación final | Primero: la matriz de perfiles bloquea a P1 |
| S4-P4 | Victor Manuel Manrique Arancivia | Diagramas finales, pruebas de todo el sistema, RNF pendientes, entrega final | En paralelo; cierra el proyecto |

Este sprint tiene una particularidad en el orden: **S4-P3 arranca antes que S4-P1**, porque sin saber qué reporte ve cada perfil no se puede implementar la autorización. En los sprints anteriores los criterios se podían derivar del Excel; acá hay una decisión que tomar.

## Lo que hay que decidir antes de construir

**Qué reporte ve cada perfil.** Son seis perfiles y varios reportes: clientes, cotizaciones, pedidos, producción por producto y lote, inventario, pagos y entregas. La matriz de quién ve qué es una decisión del negocio, no del programador, y es lo que S4-P3 entrega primero.

Dos reglas que ya están fijadas desde el Sprint 1 y que la matriz tiene que respetar: el comprador **nunca** ve costos ni márgenes, y producción y almacén tampoco ven precios de venta.

## El modelo de datos nuevo

Poco, y es una buena señal: significa que los sprints anteriores modelaron bien.

| Entidad | Para qué |
|---|---|
| `ConstanciaEntrega` | Pedido, entrega, receptor, fecha y evidencia, generada tras recepción conforme |
| `ComprobanteFiscal` | Referencia única, respuesta y estado del proveedor. Solo si RF-11 se habilita |

Los reportes **no tienen entidades propias**: son consultas sobre lo que ya existe. Si alguien propone tablas de reporte, es porque está pensando en precalcular, y eso agrega un lugar donde los números pueden no coincidir.

## Los patrones de este sprint

| Patrón | Dónde | Para qué |
|---|---|---|
| Adapter | API | Hablar con el proveedor fiscal externo sin acoplarse a él. Es el caso de libro: un sistema externo que no controlamos y que puede cambiar o no existir |
| Facade | API | Una sola entrada para los reportes, que cruzan clientes, pedidos, producción, inventario, pagos y entregas |

Adapter es el patrón que mejor se defiende de los seis, justamente porque RF-11 es condicional: **el Adapter permite que el sistema funcione sin proveedor fiscal**. Si la integración se hace con llamadas directas repartidas, no hay forma de que funcione sin ella. Eso es exactamente lo que el patrón resuelve y conviene decirlo así en la defensa.

## Riesgos de este sprint

| Riesgo | Por qué importa | Qué hacer |
|---|---|---|
| Esperar la confirmación fiscal hasta el final | Paraliza RF-11 y se pierde el sprint | Decidirlo en la primera semana. Si no hay proveedor, se entrega el Adapter y la decisión escrita |
| Fuga de datos entre compradores | Es la prueba más grave del sprint | Filtrar en el servidor por el usuario autenticado, nunca por un parámetro del cliente |
| Reportes que recalculan | Contradice RF-03 y el margen histórico | El reporte lee lo guardado, no recalcula |
| Reportes lentos | Cruzan todos los módulos | Medir con datos de volumen, no con cinco filas |
| Constancia emitida antes de tiempo | Rompe el criterio | La constancia valida que la recepción esté confirmada **y conforme** en el servidor |
| Dejar los RNF sin medir | Son del Sprint 1 y 3, y no se pueden medir retroactivamente | Que estén cerrados antes de llegar acá |

## Qué significa que el proyecto está terminado

Este sprint cierra el proyecto, así que la definición es más amplia:

1. Las cuatro afirmaciones del criterio del Sprint 4, demostrables.
2. Los criterios de validación de los sprints 1, 2 y 3 **siguen pasando**. Una regresión en el Sprint 1 a esta altura es peor que una función que falta.
3. Los tres repositorios compilan sin errores ni advertencias.
4. La verificación automática cubre los cuatro sprints y pasa contra MySQL real, con las dos configuraciones regionales.
5. Los seis patrones están implementados, usados de verdad y se pueden explicar.
6. Todos los requerimientos no funcionales están medidos o declarados sin medir, con el motivo.
7. Los diagramas y el diccionario coinciden con el código entregado.
8. El Excel tiene los cuatro sprints cerrados.
9. Etiqueta `v4.0.0` en los cuatro repositorios.
10. El proyecto se puede levantar desde cero siguiendo `00_Definicion/Como_ejecutar_el_sistema.md`, en una máquina que nunca lo tuvo.

El punto 10 es el que conviene probar de verdad, en la laptop de alguien que no lo haya instalado nunca. Es la prueba que más defectos encuentra al final de un proyecto.
