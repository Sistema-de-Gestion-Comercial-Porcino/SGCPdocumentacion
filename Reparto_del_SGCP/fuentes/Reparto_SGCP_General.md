# Reparto del SGCP · Documento general

Sistema de Gestión Comercial Porcino · Universidad Privada del Valle, Sub-sede Santa Cruz · Ingeniería de Sistemas Informáticos · Grupo B · Gestión 2/2026

Este documento reparte el trabajo de los cinco sprints entre los cuatro integrantes. Cada sprint tiene además su propio documento general y un documento por integrante, en la carpeta del sprint correspondiente.

El alcance de cada sprint no se decide aquí: sale del Sprint Backlog del archivo `Formato Proyecto - SGCC Actualizado.xlsx`, que es la fuente autorizada. Lo que este documento agrega es **quién hace qué, en qué orden y cómo se comprueba**.

## Cómo se identifica cada parte

Cada trabajo tiene un código `S<sprint>-P<parte>`. El número de parte es siempre la misma persona en todos los sprints, para que al decir un código se sepa de inmediato de quién y de qué se habla.

| Parte | Integrante | Rol | Terreno |
|---|---|---|---|
| P1 | Dario Haziel Tambo Parra | Desarrollador | SGCPapi: modelo de datos, migraciones, reglas, endpoints |
| P2 | Angel Sebastian Eguez Mur | Desarrollador | SGCPuiweb y SGCPuimovil: pantallas web y aplicación Android |
| P3 | Sofia Cuellar Roca | Product Owner | Criterios de aceptación, guiones de prueba, validación, backlog |
| P4 | Victor Manuel Manrique Arancivia | Scrum Master | Planificación, diagramas UML, ejecución de pruebas, versión y entrega |

Así, `S3-P2` es la parte de Sebastián en el Sprint 3, que es Android con captura sin conexión. Si algo está atrasado o mal, el código lo señala sin explicaciones.

El reparto por rol no es arbitrario: es el que ya figura en el punto IV del perfil de proyecto, donde Sofía "organiza y prioriza los requisitos y verifica que el sistema cumpla lo solicitado" y Víctor "coordina el trabajo y los sprints; apoya el desarrollo web, Android y las pruebas del sistema".

## El orden dentro de un sprint

El número de parte indica el orden en que cada uno **empieza**, no el único momento en que trabaja.

1. **P1 arranca primero** porque la API es el bloqueo real: sin endpoints no hay nada que consumir.
2. **P2 arranca cuando P1 publica los primeros endpoints.** No hace falta que P1 esté terminado del todo: alcanza con que el contrato esté en Swagger.
3. **P3 arranca en paralelo con P1**, escribiendo el guion de prueba a partir del parámetro de aceptación del Excel. Cierra después de P2, validando lo construido contra ese guion.
4. **P4 arranca en paralelo con P1**, actualizando diagramas y planificación. Cierra al final, ejecutando las pruebas, etiquetando la versión y preparando la entrega.

Dicho de otra forma: P1 y P2 son secuenciales entre sí; P3 y P4 abren y cierran el sprint.

## Los cinco sprints

| Sprint | Contenido | Requerimientos | Estado |
|---|---|---|---|
| 1 | Acceso, usuarios, clientes, catálogo, costos, cotizaciones y pedidos | RF-01, RF-02, RF-03, RF-10, RF-12, RF-13; RNF-02, RNF-04 | Entregado, a la espera de la revisión del docente |
| 2 | Producción, inventario, reservas, sanidad y frío | RF-04, RF-17, RF-18, RF-20; RNF-03, RNF-06 | Siguiente |
| 3 | Pagos, crédito, transporte, rutas, entregas y Android sin conexión | RF-05, RF-06, RF-07, RF-08, RF-19; RNF-01, RNF-05 | Planificado |
| 4 | Reportes con exportación, portal comprador, constancias e integración fiscal | RF-11, RF-14, RF-15 | Planificado |
| 5 | Reserva | RF-09, RF-16, RF-21 si se aprueban | Reserva |

El Sprint 5 figura en el Excel como "SPRINT 5 · RESERVA" con los encabezados y sin requerimientos asignados. No es un sprint de desarrollo nuevo: es el margen para lo que se corra de los anteriores, para los requerimientos diferidos si el docente los aprueba, y para las mediciones de requerimientos no funcionales que necesitan usuarios.

## Requerimientos que quedan fuera

Según el perfil de proyecto, tres requerimientos están fuera de la entrega actual y uno es condicional. Conviene tenerlo claro para no construir lo que nadie pidió:

| Código | Nombre | Situación |
|---|---|---|
| RF-09 | Alertar inactividad de cliente habitual | Futuro, fuera de la entrega |
| RF-16 | Sugerir volumen de compra | Mejora futura, no se incluye |
| RF-21 | Priorizar cola de pedidos | Pendiente de que el propietario apruebe el criterio |
| RF-11 | Emitir o consultar comprobante fiscal | Condicional: requiere modalidad y proveedor confirmados |

## Los patrones de diseño, repartidos

La entrega eligió siete patrones. Repartirlos por sprint evita que se acumulen al final y que alguno quede sin usar de verdad.

| Patrón | Dónde | Sprint | Para qué |
|---|---|---|---|
| Builder | API | 1 | Construir el pedido desde la cotización aceptada. **Ya implementado** |
| Factory Method | API | 2 | Crear el producto resultante de una orden según sea corte o derivado |
| Strategy | API | 3 | Resolver la condición comercial del despacho |
| Command | Android | 3 | Cada captura sin conexión es una orden que se guarda y se reintenta |
| State | Android | 3 | Estados de la entrega: pendiente, sincronizada, entregada, observada |
| Adapter | API | 4 | Hablar con el proveedor fiscal externo sin acoplarse a él |
| Facade | API | 4 | Una sola entrada para los reportes, que cruzan varios módulos |

La asignación de Factory Method al Sprint 2 es una propuesta, porque el documento de patrones no fija sprints. Sofía la confirma como Product Owner, o se consulta al docente.

## Reglas que valen para los cinco sprints

Estas no se repiten en cada documento individual, pero se aplican siempre.

### Lo que nadie debe romper

- **La web y Android no tocan la base de datos.** Todo pasa por la API. Si una pantalla necesita un dato que no existe en la API, se pide un endpoint a P1; no se busca un atajo.
- **No hay borrados físicos.** Desactivar conserva el historial. Esto está en el criterio de validación del Sprint 1 y vale para todo lo que venga.
- **Los acuerdos históricos no se recalculan.** Un precio o un costo acordado queda como estaba, aunque el catálogo cambie después.
- **Las fechas del contrato de la API son UTC.** La web y Android las presentan en hora de Bolivia.
- **Los importes llevan dos decimales y las cantidades tres.** Siempre con punto decimal al enviarlos; la presentación con coma es cosa de la interfaz.

### Cómo se entrega

Cada parte se entrega en una rama propia y llega a `main` por Pull Request, nunca con un empujón directo:

```
rama:    sprint2/p1-api-produccion
commit:  v2.1.0 - Sprint 2 - Produccion e inventario
PR:      titulo igual al commit, con el codigo S2-P1 en el cuerpo
```

El MENOR corresponde al número de parte: P1 entrega `vN.1.0`, P2 `vN.2.0`, P3 `vN.3.0` y P4 `vN.4.0`. Como P4 es siempre el que cierra, **la etiqueta del sprint es su versión, `vN.4.0`**, y la pone él una sola vez, después del último PR aprobado. No se crea una etiqueta `vN.0.0`: iría detrás de versiones que ya existen. El esquema completo está en el README de cada repositorio, en la sección "Control de versiones".

### Qué significa que una parte está terminada

Las cuatro cosas, no tres:

1. Compila sin errores **y sin advertencias**.
2. Cumple el parámetro de aceptación del Excel que le corresponde, comprobado por la vía que indique el documento del sprint.
3. Está documentada en el README del repositorio que tocó.
4. Está en `main` por PR aprobado.

### Dónde está lo que hace falta leer

| Documento | Para qué sirve |
|---|---|
| `Formato Proyecto - SGCC Actualizado.xlsx` | Fuente autorizada del alcance y los parámetros de aceptación |
| `00_Definicion/Como_ejecutar_el_sistema.md` | Levantar API, web y Android en orden, con MySQL |
| `00_Definicion/Cambio_a_MySQL.md` | El motor, el proveedor y las tres trampas de MySQL |
| `00_Definicion/Errores_encontrados_Sprint1.md` | Defectos ya corregidos, con su causa, para no repetirlos |
| `00_Definicion/Metodo_de_verificacion.md` | Cómo se comprueba que algo funciona de verdad |
| `00_Definicion/Reglas_del_sistema.md` | Reglas del negocio vigentes |
| `02_Ingenieria_de_Software/00_Documentacion/Diccionario_clases.md` | Nombres y atributos de las clases |

## Advertencia sobre el Sprint 1

El Sprint 1 está construido y verificado, pero **el docente todavía no lo revisó**. Hasta que haya devolución, los documentos del Sprint 1 reparten solo dos cosas: los tres pendientes que no se pudieron cerrar sin un teléfono y sin usuarios, y la obligación de atender lo que el docente observe.

No conviene empezar el Sprint 2 dando por cerrado el 1. Si el docente pide cambios de modelo o de alcance, arrastran al Sprint 2, porque producción e inventario se apoyan en el catálogo y los productos del Sprint 1.
