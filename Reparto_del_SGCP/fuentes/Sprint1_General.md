# Sprint 1 · Documento general

Acceso y registro de comprador, administración de usuarios, clientes, catálogo de cortes y derivados, productos, costos, cotizaciones y pedidos. Datos centrales y base técnica de Android.

> **Este sprint está construido y verificado, pero el docente todavía no lo revisó.** Hasta que haya devolución, lo que reparte este documento son los tres pendientes que no se pudieron cerrar y la obligación de atender lo que el docente observe. No es un sprint para empezar: es un sprint para cerrar.

## Qué entró

| Código | Nombre | Estado |
|---|---|---|
| RF-01 | Registrar solicitud, cotización y pedido | Implementado y verificado |
| RF-02 | Administrar costos y precios vigentes | Implementado y verificado |
| RF-03 | Calcular margen estimado por pedido | Implementado y verificado |
| RF-10 | Gestionar clientes | Implementado y verificado |
| RF-12 | Gestionar acceso autenticado | Implementado y verificado |
| RF-13 | Administrar usuarios y permisos | Implementado y verificado |
| RNF-02 | Eficiencia de desempeño | **Sin medir**: necesita usuarios |
| RNF-04 | Usabilidad | **Sin medir**: necesita usuarios |

Más la parametrización de RF-04 que correspondía a este sprint: clasificaciones de cortes y derivados, y productos. Sin existencias, que son del Sprint 2.

## El criterio de validación, y cómo quedó

> Todos se autentican; alta pública solo comprador. Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar historial.

Las cinco afirmaciones están cubiertas y comprobadas por HTTP. El recorrido automático de 27 comprobaciones las ejerce, y las tres que el docente va a mirar de cerca son las de cotizaciones y margen:

- Una cotización presentada o rechazada **no** crea pedido.
- El pedido toma el precio de la cotización aceptada, aunque el catálogo haya cambiado después.
- Una vigencia de precio nueva **no** recalcula el margen de un pedido ya confirmado.

## Lo que está verificado, y contra qué

Esto importa tanto como el resultado: un verde en un entorno que no es el de entrega es un verde provisional.

| Qué | Resultado |
|---|---|
| Compilación de los tres repositorios | 0 errores, 0 advertencias |
| `dotnet ef database update` contra MySQL 8.4 real, dos veces | aplicada, luego sin cambios |
| Modelo y migración sincronizados | sí |
| Reglas de unicidad probadas en los dos sentidos | 7 de 7 |
| Recorrido completo de la API por HTTP | 27 de 27 |
| El mismo recorrido por la vía SQLite | 27 de 27 |
| Con `LANG=es_BO.UTF-8` y con `LANG=C` | pasa en los dos |
| Páginas de la web y envío del formulario de precios | 9 de 9 |
| APK y pruebas unitarias de Android | correctos |
| Flujo de integración continua en GitHub Actions | pasa |

El detalle del método está en `00_Definicion/Metodo_de_verificacion.md`, y los cuatro defectos encontrados y corregidos en `00_Definicion/Errores_encontrados_Sprint1.md`.

## Los tres pendientes, repartidos

Ninguno se puede cerrar con más programación. Dos necesitan usuarios y uno un teléfono.

| Código | Pendiente | Responsable | Por qué quedó abierto |
|---|---|---|---|
| S1-P2 | Instalar el APK en un teléfono y probar el acceso | Angel Sebastian Eguez Mur | Compila y las pruebas pasan, pero nunca corrió en un dispositivo |
| S1-P3 | Medir RNF-04, usabilidad, con usuarios representativos | Sofia Cuellar Roca | Se mide observando personas, no se calcula |
| S1-P4 | Medir RNF-02, desempeño, comparado con la anotación manual | Victor Manuel Manrique Arancivia | Es una comparación cronometrada, necesita usuarios |

Y uno que no tiene fecha porque no depende del equipo:

| Código | Pendiente | Responsable |
|---|---|---|
| S1-P1 | Atender lo que observe el docente en la revisión | Dario Haziel Tambo Parra, con reparto según lo que pida |

## Cuándo se hacen

Durante el Sprint 2, en paralelo con el trabajo nuevo. Son tareas cortas que no compiten con el desarrollo: una tarde de teléfono y dos sesiones con personas que no sean del equipo.

Lo que **no** conviene es dejarlos para el final del proyecto. RNF-02 y RNF-04 son requerimientos no funcionales del Sprint 1 según el Excel: si se miden en el Sprint 4, se está presentando evidencia de otro sistema.

## El cambio de motor, por si surge en la revisión

El Sprint 1 se construyó primero sobre SQL Server y después se pasó a **MySQL 8**, cuando el docente autorizó cualquier motor. Conviene tenerlo claro porque es probable que pregunte.

Dos cosas que vale decir si sale el tema. La primera: el cambio **no tocó servicios, controladores, entidades ni el patrón Builder**, solo la capa de datos y la configuración, que es la prueba de que la separación por capas estaba bien hecha. La segunda: el cambio **mejoró** la verificación, porque un MySQL de prueba se levanta en veinte segundos en un contenedor y eso permitió correr la migración contra el motor real, algo que con SQL Server nunca se consiguió.

Lo que sí hubo que rediseñar fueron tres reglas de unicidad, porque MySQL no tiene índices filtrados. Están resueltas con columnas generadas y probadas en los dos sentidos. Todo el detalle, con las tres trampas de MySQL, está en `00_Definicion/Cambio_a_MySQL.md`.

## Riesgo del que conviene hablar antes

Si el docente pide cambios de modelo, **arrastran al Sprint 2**, porque producción e inventario se apoyan en el catálogo y los productos de este sprint. Por eso el documento general del reparto recomienda no empezar S2-P1 hasta tener la devolución, o aceptar de entrada que puede haber retrabajo.

Lo barato es esperar la devolución para el modelo de datos y, mientras tanto, avanzar con lo que no depende de él: los criterios de aceptación del Sprint 2, los diagramas y los tres pendientes de esta lista.
