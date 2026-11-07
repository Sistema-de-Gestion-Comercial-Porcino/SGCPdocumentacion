# Sprint 4 · Parte 2 · Angel Sebastian Eguez Mur

Código de seguimiento: **S4-P2**. Rol: Desarrollador. Repositorio: **SGCPuiweb**.

## Qué te toca

Las pantallas de reportes con filtros y descargas, el portal del comprador terminado, la pantalla de constancia de entrega y, si RF-11 se habilita, la vista de comprobante fiscal.

Es el sprint donde menos lógica nueva hay y más cuidado hay que tener: casi todo lo que vas a mostrar son datos que **no todos pueden ver**.

## Tus tareas

### 1. Pantallas de reportes con filtros · RF-15

Los reportes del Excel: clientes, cotizaciones, pedidos, producción por producto, corte o derivado, inventario, pagos y entregas. Con filtros de fecha, producto, cliente y estado.

Tres cosas que valen para todas las pantallas:

**El menú muestra solo los reportes que el perfil puede ver.** No todos los reportes con un mensaje de error al entrar: los que no corresponden no aparecen. La matriz la define S4-P3.

**Esconder una columna en la vista no es seguridad.** Si el API devuelve un costo y vos no lo pintás, el dato igual viajó y está en el HTML o en la respuesta. La regla es que el API no lo manda; si ves un campo que no debería estar ahí, avisale a S4-P1, no lo tapes con CSS.

**Los reportes son de solo lectura.** Ningún botón de la pantalla de reportes cambia datos. Nada de «marcar como revisado» desde un reporte.

**Entregás:** las pantallas de reporte. **Se comprueba:** entrando con cada perfil, el menú ofrece solo lo que le corresponde.

### 2. Descargas de PDF y Excel · RF-15

Un botón por reporte, con el filtro aplicado actualmente. Si el usuario filtró por un mes, el archivo trae ese mes, no todo.

Lo que hay que cuidar: el botón de descarga pega al **mismo endpoint autorizado**, no a un camino alterno sin filtro. Es el agujero clásico del sprint: la tabla filtra bien y el botón baja todo.

Y dale aviso visible al usuario mientras el archivo se genera. Un reporte grande tarda, y sin aviso la gente toca el botón cinco veces y genera cinco descargas.

**Entregás:** las descargas funcionando. **Se comprueba:** el archivo bajado contiene exactamente las filas que la pantalla mostraba.

### 3. Portal del comprador terminado · RF-15

El comprador ya entra desde el Sprint 1 y ve sus cotizaciones y pedidos. Acá se le agrega consultar y exportar **sus** reportes.

La regla, que es el criterio más importante del sprint: **solo sus datos, nunca costos ni márgenes.** En ninguna pantalla, en ninguna tabla, en ningún archivo exportado, en ningún tooltip.

Probalo con dos compradores distintos, cada uno con pedidos propios, y revisá que ninguno vea nada del otro. Si en alguna pantalla el identificador del cliente viaja en la URL, probá cambiarlo a mano por el del otro comprador: tiene que devolver un error, no datos. Si devuelve datos, es un hallazgo grave y hay que avisar a S4-P1 el mismo día.

**Entregás:** el portal completo. **Se comprueba:** la prueba de los dos compradores, con el cambio de identificador en la URL.

### 4. Constancia de entrega · RF-14

La pantalla que genera y muestra la constancia: pedido, entrega, receptor, fecha y evidencia.

El botón de generar aparece **solo** cuando la entrega tiene recepción confirmada y conforme. Si está pendiente de sincronizar o quedó observada, el botón no está, y la pantalla dice por qué en una frase. No un botón que al tocarlo da error.

**Entregás:** la pantalla de constancia. **Se comprueba:** en una entrega observada no hay botón y la pantalla explica el motivo.

### 5. Comprobante fiscal · RF-11, condicional

**Antes de hacer nada, preguntale a S4-P3 si RF-11 va.** Si no hay proveedor fiscal confirmado, esta tarea no se hace.

Si va: la vista que muestra la referencia única, el estado y la respuesta del proveedor; y el aviso claro cuando la emisión no está disponible, porque el Excel dice que en ese caso la operación **se registra igual, sin comprobante**. Eso el usuario lo tiene que entender desde la pantalla, no descubrirlo después.

Si no va: en la pantalla de pedido confirmado, una leyenda de que la emisión fiscal no está habilitada. Es media hora de trabajo y evita que el docente piense que falta algo sin explicación.

**Entregás:** lo que corresponda según la decisión. **Se comprueba:** con la emisión deshabilitada, el usuario entiende qué pasó sin preguntarle a nadie.

### 6. Repasar la aplicación Android

El Sprint 4 no tiene trabajo nuevo de Android, así que aprovechá para dejarla cerrada: que compile, que el recorrido de captura y sincronización del Sprint 3 siga funcionando, y que la pantalla de pendientes muestre bien el estado.

Si quedó algo del Sprint 3 a medias —y la prueba del APK en un teléfono real era tu pendiente desde el Sprint 1— este es el momento. Después no hay otro.

**Entregás:** la aplicación compilando y el recorrido del Sprint 3 pasando. **Se comprueba:** instalación en un teléfono y captura con el servidor apagado.

### 7. Revisar la interfaz completa

Último sprint, así que vale la pena una pasada por todo lo construido:

- Los mensajes de error no muestran detalles internos: ni rutas de archivo, ni consultas SQL, ni nombres de clases.
- Las pantallas se ven bien en una ventana angosta. El docente puede abrirlo en un portátil chico.
- Ninguna pantalla quedó con texto de relleno, botones que no hacen nada, o enlaces muertos.
- Lo que escribe el usuario se muestra escapado. Un nombre de cliente con `<b>` se ve con los signos, no en negrita.

**Entregás:** una lista corta de lo corregido. **Se comprueba:** no hay pantallas a medio terminar.

## Qué no te toca

El API ni la exportación del lado del servidor: S4-P1. La matriz de perfiles: S4-P3. Los diagramas y la entrega final: S4-P4.

## De quién dependés y quién depende de vos

**Dependés de S4-P1** para los endpoints de reporte y exportación, y de **S4-P3** para saber qué ve cada perfil.

**Depende de vos S4-P4**: no puede probar el sistema completo hasta que las pantallas estén.

Mientras esperás los endpoints: las tareas 6 y 7 no dependen de nadie. Arrancá por ahí.

## Cómo entregarlo

```bash
git checkout -b sprint4/p2-web-reportes
git commit -m "v4.2.0 - Sprint 4 - Reportes, portal del comprador y constancia"
git push -u origin sprint4/p2-web-reportes
```

Pull Request con el código `S4-P2` en el cuerpo.
