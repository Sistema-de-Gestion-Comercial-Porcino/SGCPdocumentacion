# Sprint 4 · Parte 1 · Dario Haziel Tambo Parra

Código de seguimiento: **S4-P1**. Rol: Desarrollador. Repositorio: **SGCPapi**.

## Qué te toca

Las consultas de reporte con sus filtros y autorización, la exportación a PDF y Excel, la constancia de entrega, y el Adapter del proveedor fiscal, que puede quedar sin completarse si no hay proveedor confirmado.

A diferencia de los sprints anteriores, acá **no arrancás primero**: necesitás la matriz de perfiles de S4-P3 para saber qué reporte ve quién. Pedila el primer día.

## Tus tareas

### 1. Consultas de reporte con autorización · RF-15

Los reportes que pide el Excel: clientes, cotizaciones, pedidos, producción por producto, corte o derivado, inventario, pagos y entregas. Con filtros de fecha, producto, cliente y estado.

Dos reglas que gobiernan todo:

**Los reportes no modifican nada.** Son consultas de lectura. No cambian estados, no marcan como visto, no escriben en los datos operativos. Usá `AsNoTracking()` y que no haya ningún `SaveChanges` en ese camino.

**Los reportes no recalculan.** El margen de un pedido reportado es el margen histórico que quedó guardado al confirmarlo, no un cálculo nuevo con los precios de hoy. Es la regla RF-03 del Sprint 1 y acá es fácil romperla sin darse cuenta, porque es tentador «mejorar» el reporte con un cálculo fresco.

La autorización se filtra **en el servidor, por el usuario autenticado**. Nunca por un parámetro que el cliente manda: un identificador de cliente en la URL es exactamente la forma de que un comprador vea lo de otro.

**Entregás:** los endpoints de reporte. **Se comprueba:** un comprador pidiendo el reporte de otro recibe 403, no datos.

### 2. Facade para los reportes · RF-15

En `src/SGCP.Api/Patrones/Reportes/`.

Los reportes cruzan clientes, pedidos, producción, inventario, pagos y entregas: seis módulos. Sin una fachada, cada controlador de reporte termina conociendo seis servicios y la autorización se repite en cada uno, que es donde aparecen los agujeros.

Una sola entrada que recibe qué reporte, qué filtros y qué usuario, resuelve la autorización en un lugar y arma el resultado.

Para la defensa: Facade va acá porque hay un subsistema complejo —seis módulos— y un cliente que necesita una vista simple. Y porque concentrar la autorización en un punto es más seguro que repetirla en seis.

**Entregás:** el patrón y su uso desde los controladores. **Se comprueba:** la autorización está en un solo lugar.

### 3. Exportación a PDF y Excel · RF-15

El Excel pide que los seis perfiles puedan «consultar y exportar PDF o Excel de reportes permitidos».

Lo importante y fácil de pasar por alto: **la exportación respeta exactamente la misma autorización que la consulta.** Es el agujero clásico: la pantalla filtra bien y el botón de exportar devuelve todo. Que la exportación pase por el mismo Facade, no por un camino paralelo.

Y que el archivo exportado **no incluya columnas que el perfil no puede ver**. Un comprador que exporta sus pedidos no recibe una columna de costo escondida en la hoja.

Elegí las bibliotecas y anotalas en el README con su versión. Son dependencias nuevas y el docente puede preguntar por qué esas.

**Entregás:** los endpoints de exportación. **Se comprueba:** el archivo exportado por un comprador no tiene costos ni márgenes en ninguna columna.

### 4. Constancia de entrega · RF-14

La constancia lleva pedido, entrega, receptor, fecha y evidencia. Y se genera **solo después de confirmar una recepción conforme en el servidor**.

Las dos condiciones que hay que validar, las dos:

- La recepción está **confirmada en el servidor**. Una captura pendiente en el teléfono no alcanza.
- La recepción es **conforme**. Una entrega OBSERVADA no emite constancia definitiva.

Es el enganche con el Sprint 3 y la prueba que lo conecta todo.

**Entregás:** el endpoint de constancia. **Se comprueba:** una recepción pendiente y una observada son rechazadas, cada una con su código.

### 5. Adapter fiscal · RF-11, condicional

En `src/SGCP.Api/Patrones/Fiscal/`.

**Antes de implementar, confirmá con S4-P3 si hay proveedor.** Si no lo hay, RF-11 no se completa, y eso está previsto: el Excel lo pone como condicional.

Lo que entregás en cualquiera de los dos casos es el **Adapter**: la interfaz que el sistema usa para emitir, con una implementación que registra la operación sin comprobante mientras la integración no esté habilitada. Eso es lo que el Excel pide textualmente: «mientras no esté habilitada, se registra» la operación.

Si hay proveedor, se agrega la implementación real detrás de la misma interfaz, y conserva **referencia única, respuesta y estado**.

La referencia única necesita una restricción en la base: una emisión confirmada no se puede duplicar. Es el cuarto punto del criterio de validación.

Para la defensa, y es el mejor argumento de patrón de todo el proyecto: **el Adapter es lo que permite que el sistema funcione sin proveedor fiscal.** Con llamadas directas repartidas por los servicios, no habría forma. Es el patrón resolviendo un problema real, no cumpliendo un requisito académico.

**Entregás:** el Adapter, con o sin implementación real. **Se comprueba:** el sistema funciona completo con la integración deshabilitada.

### 6. Portal del comprador · RF-15

El comprador ya tiene cuenta y ve sus cotizaciones y pedidos desde el Sprint 1. Acá se completa con consulta y exportación de sus propios reportes.

La regla no cambia y es la más importante del sprint: **solo sus datos, y nunca costos ni márgenes.** Ya está implementada desde el Sprint 1; lo que hay que hacer es no romperla al agregar reportes.

**Entregás:** los endpoints del portal. **Se comprueba:** el recorrido del Sprint 1 que verifica que el comprador no ve márgenes sigue pasando.

### 7. Rendimiento con datos de volumen

Los reportes cruzan todos los módulos, así que son lo primero que se pone lento. Probalos con datos de volumen, no con cinco filas: unos miles de pedidos sembrados en una base de prueba.

Lo que hay que mirar: consultas que recorren tablas enteras, y el patrón de una consulta por fila dentro de un bucle, que con cinco filas no se nota y con mil sí. Mirá el SQL que genera EF Core con el registro de consultas activado.

**Entregás:** una nota corta con lo que medís. **Se comprueba:** ningún reporte tarda de forma desproporcionada con datos de volumen.

## Qué no te toca

Pantallas: S4-P2. Diagramas: S4-P4. La matriz de qué perfil ve qué reporte y la decisión sobre RF-11: S4-P3.

## De quién dependés y quién depende de vos

**Dependés de S4-P3**, y esta vez de verdad: sin la matriz de perfiles no se puede implementar la autorización, y sin la decisión sobre RF-11 no sabés si hacer el proveedor real. Pedí las dos el primer día.

**Depende de vos S4-P2.**

## Cómo entregarlo

```bash
git checkout -b sprint4/p1-api-reportes
git commit -m "v4.1.0 - Sprint 4 - Reportes, constancia e integracion fiscal"
git push -u origin sprint4/p1-api-reportes
```

Pull Request con el código `S4-P1` en el cuerpo.

## Una última cosa, porque es el sprint final

Antes de cerrar, corré el recorrido completo de los cuatro sprints. Una regresión en el Sprint 1 a esta altura es peor que una función que falta: significa que algo que el docente ya vio funcionando dejó de funcionar.
