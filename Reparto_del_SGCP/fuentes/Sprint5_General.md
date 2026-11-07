# Sprint 5 · Documento general

Sprint de reserva. No tiene requerimientos asignados en el Sprint Backlog: en `Formato Proyecto - SGCC Actualizado.xlsx` aparece como encabezado, sin filas.

## Para qué sirve este sprint

Tres cosas, en este orden de prioridad:

1. **Terminar lo que quedó.** Cualquier cosa de los sprints 1 a 4 que no cerró.
2. **Los requerimientos diferidos**, si el docente los aprueba: RF-09, RF-16 y RF-21.
3. **Las mejoras técnicas** que no caben en un sprint con requerimientos, entre ellas la versión del frontend en React.

Y una cuarta que conviene decir en voz alta: **si al llegar acá todo está cerrado, el sprint se declara sin trabajo y se entrega.** Un proyecto que termina en el Sprint 4 con todo funcionando es mejor que uno que agrega cosas a medias en el Sprint 5. Inventar trabajo para llenar un sprint es la forma más común de romper algo que ya andaba.

> **Nada de este documento se arranca sin confirmar con el docente.** Este sprint no está en el Backlog, así que todo lo de acá es propuesta.

## Lo primero: la lista de lo que quedó

Antes de proponer nada, S5-P4 arma la lista real de pendientes, revisando el estado de los cuatro sprints. Pendientes conocidos al cerrar el Sprint 1:

| Pendiente | De quién | Sprint de origen |
|---|---|---|
| Probar el APK en un teléfono físico | S5-P2 | Sprint 1 |
| RNF-04, usabilidad, medir con una persona real | S5-P3 | Sprint 1 |
| RNF-02, rendimiento, medir con datos de volumen | S5-P4 | Sprint 1 |
| Atender las observaciones del docente | S5-P1 | Sprint 1 |

Si estos cuatro ya se cerraron en los sprints 2, 3 o 4, mejor: el sprint arranca libre.

## Los requerimientos diferidos

Están fuera del alcance según el perfil del proyecto. Solo se toman **si el docente lo autoriza por escrito**, y uno a la vez.

| Código | Qué es | Cuánto cuesta | Recomendación |
|---|---|---|---|
| RF-09 | Alertas automáticas de inventario | Bajo. El inventario y sus umbrales ya existen desde el Sprint 3 | El más razonable de los tres |
| RF-16 | Panel de indicadores | Medio. Los datos existen, el trabajo es de presentación | Razonable si hay tiempo |
| RF-21 | Integración con contabilidad externa | Alto. Es un sistema externo que no existe definido | No tomarlo |

RF-21 no conviene por el mismo motivo por el que RF-11 es condicional: sin un sistema externo confirmado, lo único que se puede entregar es un diseño, y ya hay un Adapter entregado en el Sprint 4 que demuestra lo mismo.

**Si hay que elegir uno, RF-09.** Es el más corto, se apoya en lo que ya está construido y se demuestra en treinta segundos: bajás el stock, salta la alerta.

## La versión en React

Es una propuesta del equipo, no un requerimiento. La idea es que el navegador del visitante arme la pantalla en lugar de que el servidor la mande armada.

**La decisión tomada: no se reescribe el frontend. Se hace una prueba acotada, en un repositorio nuevo, y solo si lo demás está cerrado.**

Los motivos, para poder defenderlos:

- El frontend actual son vistas Razor que el servidor renderiza, con Bootstrap y validación de jQuery. Funciona, está entregado y sus criterios pasan. Reescribirlo pone en riesgo trabajo ya aprobado para ganar algo que el docente no pidió.
- React obliga a separar el frontend del API de verdad: autenticación por token en el navegador, CORS, manejo de sesión del lado del cliente. Son temas nuevos, no una traducción de pantallas.
- Un frontend a medio migrar es peor que cualquiera de los dos completos: dos formas de autenticar, dos de validar, y los criterios de validación pasando en una mitad.

Lo que sí se puede hacer, y es defendible: **un repositorio nuevo, `SGCPuireact`, con dos o tres pantallas de solo lectura** —el catálogo de productos y el listado de pedidos— consumiendo el API que ya existe. Eso demuestra que el API sirve para cualquier cliente, que es un argumento de arquitectura real, sin tocar nada entregado.

Y una observación que vale decir en la defensa: el proyecto **ya tiene** un cliente que renderiza del lado del dispositivo. Es la aplicación Android nativa del Sprint 3, consumiendo el mismo API. El argumento de «que el dispositivo renderice» ya está demostrado; React sería un segundo caso, no el primero.

| Si se hace | Si no se hace |
|---|---|
| Repositorio aparte, `SGCPuireact` | No pasa nada. No es un requerimiento |
| Dos o tres pantallas de lectura, nada más | El argumento de arquitectura ya lo cubre Android |
| Sin tocar `SGCPuiweb` | Se menciona como trabajo futuro y se cierra |
| Solo si los sprints 1 a 4 están cerrados | |

## Reparto

Las mismas partes de siempre, con el mismo número por persona, para que el seguimiento no cambie:

| Código | Integrante | Trabajo |
|---|---|---|
| S5-P1 | Dario Haziel Tambo Parra | Pendientes del API, RF-09 si se aprueba, observaciones del docente |
| S5-P2 | Angel Sebastian Eguez Mur | Pendientes de web y Android, APK en teléfono, prueba de React si se hace |
| S5-P3 | Sofia Cuellar Roca | Criterios de lo que se agregue, RNF-04, validación final |
| S5-P4 | Victor Manuel Manrique Arancivia | La lista de pendientes, RNF-02, cierre documental y entrega |

**S5-P4 arranca primero**, porque la lista de pendientes define el sprint. Hasta que esa lista no exista, los demás no saben qué les toca.

## Riesgos de este sprint

| Riesgo | Por qué importa | Qué hacer |
|---|---|---|
| Inventar trabajo para llenar el sprint | Rompe lo que ya funcionaba | Si no hay pendientes, se declara sin trabajo y se entrega |
| Empezar la reescritura en React | Pone en riesgo trabajo aprobado | Repositorio aparte, lectura nada más, y solo si lo demás cerró |
| Tomar RF-21 | Depende de un sistema externo que no existe definido | No tomarlo |
| Tomar los tres diferidos | Tres cosas a medias en lugar de una terminada | Uno solo, y completo |
| Agregar sin criterios | No se puede validar ni defender | Nada entra sin su criterio escrito por S5-P3 |

## Definición de terminado

Si el sprint tiene trabajo:

1. Cada cosa agregada tiene su criterio escrito y cumplido.
2. Los criterios de los sprints 1 a 4 **siguen pasando**. Es la condición más importante de este sprint: no romper nada.
3. La verificación automática pasa completa.
4. Los diagramas y el diccionario incluyen lo agregado.
5. Etiqueta `v5.4.0` en los repositorios tocados, la versión del último commit del sprint.

Si el sprint no tiene trabajo:

1. Una página que diga que el sprint se cerró sin trabajo, con la lista de lo que se revisó para concluirlo.
2. La entrega del Sprint 4 queda como entrega final.

La segunda opción es un resultado perfectamente bueno y conviene decirlo así en la defensa. Un sprint de reserva que no se usó significa que los cuatro anteriores se cumplieron.
