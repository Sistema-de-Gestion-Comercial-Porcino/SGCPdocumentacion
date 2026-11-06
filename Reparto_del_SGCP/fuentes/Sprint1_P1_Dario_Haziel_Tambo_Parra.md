# Sprint 1 · Parte 1 · Dario Haziel Tambo Parra

Código de seguimiento: **S1-P1**. Rol: Desarrollador. Repositorio: **SGCPapi**.

## Estado: entregado, a la espera de la revisión

Tu parte del Sprint 1 está construida y verificada. Lo que queda abierto no depende de vos todavía: es atender lo que el docente observe cuando revise.

## Qué quedó hecho

La API completa del Sprint 1: acceso autenticado con JWT y sesiones revocables, permisos y responsabilidades, registro público de comprador, recuperación de contraseña, usuarios, clientes, clasificaciones de cortes y derivados, productos, vigencias de costo y precio, cotizaciones versionadas y pedidos con margen histórico. RF-01, RF-02, RF-03, RF-10, RF-12, RF-13, más la parametrización de RF-04.

El patrón **Builder** construye el pedido a partir de la cotización aceptada.

Verificado con 27 comprobaciones por HTTP contra MySQL 8.4 real, con la migración aplicada dos veces y sin cambios pendientes en el modelo.

## Lo que tenés que poder defender oralmente

La defensa consiste en modificar código en vivo, así que conviene tener ubicadas estas cuatro cosas antes de entrar:

**1. Por qué Builder y no otro patrón.** Un pedido se arma por pasos a partir de una cotización aceptada: cliente, condición de pago, fecha comprometida y cada detalle con su precio y su costo congelados. El constructor tendría demasiados parámetros y el objeto no debe existir a medio armar. Está en `src/SGCP.Api/Patrones/Comercial/PedidoBuilder.cs` y lo usa `ServicioConfirmarPedido`.

**2. Dónde se congela el precio y el costo.** Al confirmar el pedido, cada detalle guarda el precio acordado de la cotización y el costo de referencia vigente en ese momento. Por eso una vigencia nueva no mueve el margen de un pedido ya confirmado. Es la regla RF-03 y la pregunta más probable del docente.

**3. Por qué el margen es estimado.** Es la suma de cantidad por precio menos cantidad por costo de referencia, por producto. No es utilidad real por animal: no incluye merma, servicio ni gasto operativo. El Excel lo dice así y conviene decirlo igual.

**4. Las tres reglas de unicidad en MySQL.** MySQL no tiene índices filtrados, así que una vigencia abierta por producto y un NIT único entre clientes activos se sostienen con columnas generadas más índice único. Si el docente pregunta cómo se garantiza que no haya dos precios abiertos, la respuesta es la base de datos, no el servicio. Está en `00_Definicion/Cambio_a_MySQL.md` sección 3.

## Tu única tarea abierta

### Atender la devolución del docente

Cuando llegue, el camino es: la devolución pasa por **S1-P3**, que la traduce a cambios concretos con su requerimiento y su responsable, y de ahí se reparte. Así queda registrado por qué se cambió cada cosa, en lugar de aparecer un commit sin explicación.

Si lo que pide toca el modelo de datos, avisá antes de empezar el Sprint 2: producción e inventario se apoyan en el catálogo y los productos de este sprint, y un cambio de modelo arrastra.

**Entregás:** los cambios que pida, con su versión de parche. **Se comprueba:** las 27 comprobaciones siguen pasando después del cambio.

## Lo que ya no te toca

Las dos mediciones pendientes del Sprint 1 no son tuyas: RNF-02 es de S1-P4 y RNF-04 de S1-P3. El APK en un teléfono es de S1-P2. Son los tres pendientes que quedaron, y ninguno se cierra programando.

## Mientras esperás

Lo útil es leer el documento general del Sprint 2 y empezar a diseñar el modelo de producción e inventario **sin escribirlo**. Las once entidades nuevas y las cuatro reglas del criterio de validación están en `Sprint2_P1_Dario_Haziel_Tambo_Parra.pdf`. Tener el diseño pensado antes de la devolución no se pierde aunque haya cambios.

Lo que no conviene es empezar la migración del Sprint 2 antes de la devolución: si el docente pide un cambio de modelo del Sprint 1, hay que rehacerla.

## Una nota sobre el commit y la versión

El Sprint 1 cierra en **`v1.0.0`** en los cuatro repositorios, y la etiqueta la pone S1-P4 una sola vez, después del último PR. No la pongas vos, y recordá que la etiqueta va **después** del commit o apunta al estado anterior.
