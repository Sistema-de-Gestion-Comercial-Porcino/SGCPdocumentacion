# Sprint 3 · Parte 1 · Dario Haziel Tambo Parra

Código de seguimiento: **S3-P1**. Rol: Desarrollador. Repositorio: **SGCPapi**.

## Qué te toca

La API de pagos, saldos, transporte, rutas y entregas, más **el endpoint de sincronización**, que es la pieza más delicada de todo el proyecto.

Y una responsabilidad extra: el contrato de sincronización lo acordás con S3-P2 **antes** de que ninguno de los dos escriba código. Es el único punto del proyecto donde dos partes no pueden trabajar en paralelo sin ponerse de acuerdo primero.

## Tarea 0, antes que todo: acordar el contrato de sincronización

Sentate con S3-P2 y definan el cuerpo exacto de la petición y la respuesta. RNF-01 ya dice qué campos tiene que llevar: clave única, versión base, autor, fecha real, datos y evidencia.

Lo que hay que dejar decidido y escrito:

| Decisión | Lo que recomienda el requerimiento |
|---|---|
| ¿Quién genera la clave única? | **El teléfono.** Es lo que permite que un reintento no duplique |
| ¿Qué pasa si la clave ya existe? | El servidor responde que ya existe, con el identificador de la recepción, y **no crea nada** |
| ¿Qué pasa si la versión base no coincide? | Se marca conflicto y **espera revisión humana**. No se sobrescribe |
| ¿Se manda una recepción o un lote? | Un lote, porque el teléfono puede acumular varias sin señal |
| ¿La evidencia va en el mismo envío? | Decidir: en el mismo cuerpo o en una segunda llamada. Un archivo grande con mala señal falla distinto |
| ¿Fecha física y fecha de sincronización? | **Dos campos distintos**, lo pide RNF-06 |

Escribilo en el README de SGCPapi antes de implementar. Si esto se define a mitad del sprint, los dos lados rehacen trabajo.

**Entregás:** el contrato escrito y acordado. **Se comprueba:** S3-P2 puede escribir el cliente sin preguntarte nada más.

## Tus tareas

### 1. Entidades y configuración · RF-05, RF-06, RF-07, RF-08, RF-19

Nueve entidades: `CondicionPago`, `Pago`, `Sena`, `Transporte`, `Ruta`, `Entrega`, `Recepcion`, `EvidenciaRecepcion`, y la extensión de `Cargo` que empezó en el Sprint 2.

Tres cosas que definen el diseño:

**El saldo no se guarda.** Se calcula: cargos menos pagos aplicados, distinguiendo producto, servicio, contado, crédito vigente y vencido. Un campo de saldo acumulado es la forma más rápida de tener dos números que no coinciden.

**La seña se aplica una sola vez.** Necesita una restricción real, no una validación en el servicio. Si una seña se cancela, se registra el acuerdo de resolución: no hay devolución ni retención automáticas.

**Entrega y deuda son independientes.** Dos campos de estado que no se tocan entre sí. Ninguna regla hace que confirmar una entrega modifique el saldo, ni al revés.

Para la unicidad de la clave de sincronización: índice único sobre la clave que manda el cliente. **En la base de datos, no en el servicio.** Es la única defensa real contra el duplicado, porque dos peticiones simultáneas pasan las dos la validación del servicio.

Y la migración, **sin `--idempotent`**, por lo explicado en `00_Definicion/Cambio_a_MySQL.md` sección 4.

**Entregás:** entidades, configuraciones y migración. **Se comprueba:** `database update` contra MySQL real dos veces, sin cambios pendientes en el modelo.

### 2. El endpoint de sincronización · RF-07, RNF-01

La pieza crítica. Tres comportamientos, y los tres se prueban por separado:

**Caso normal.** Llega un lote de recepciones con claves que el servidor no conoce. Las crea, devuelve el identificador de cada una y la fecha de sincronización.

**Reintento.** Llega una clave que ya existe. El servidor **no crea nada**, responde que ya existe y devuelve el identificador de la recepción original. Desde el teléfono tiene que parecer un éxito, porque lo es: el dato llegó. Si respondés un error, el teléfono va a reintentar para siempre.

**Conflicto.** Llega una recepción cuya versión base no coincide con lo que hay en el servidor. Se marca para revisión y **no se aplica**. Alguien la mira y decide. El Excel es explícito: «los conflictos requieren revisión».

La operación entera va en una transacción: o entra el lote completo o no entra nada. Un lote a medio aplicar deja al teléfono sin saber qué reenviar.

**Entregás:** el endpoint con los tres comportamientos. **Se comprueba:** mandar el mismo lote dos veces deja una sola recepción, verificado contando filas en MySQL.

### 3. Los dos estados de la recepción · RF-07

Conforme da **ENTREGADA**. Con observaciones da **OBSERVADA**.

Lo que conviene no confundir: una observación **no es un rechazo**. La entrega ocurrió, con reparos. Y una recepción OBSERVADA **no emite constancia** definitiva, que es RF-14 del Sprint 4, pero eso se implementa allá, no acá. Lo que te toca es que el estado quede bien guardado.

**Entregás:** la regla de estados. **Se comprueba:** una recepción con observaciones queda OBSERVADA y una conforme ENTREGADA.

### 4. Strategy para la condición comercial · RF-05

En `src/SGCP.Api/Patrones/Comercial/`, junto al `PedidoBuilder` del Sprint 1.

Contado y crédito autorizado se resuelven distinto: el crédito necesita importe y fecha de vencimiento acordados para esa operación, el contado no. Y el Excel dice que **no se aplica un plazo por defecto**: cada operación lleva lo acordado.

En lugar de un condicional que crece con cada modalidad, una estrategia por condición y un selector.

La regla que no se puede romper: **autorizar crédito no liquida deuda.** El crédito es una forma de pago acordada, no un cobro. Está en `00_Definicion/Organizacion_repositorios_y_patrones.md`.

Para la defensa: Strategy va acá porque hay varias formas de resolver lo mismo, se eligen en tiempo de ejecución y se esperan más.

**Entregás:** el patrón y su uso. **Se comprueba:** agregar una modalidad no obliga a modificar el servicio.

### 5. Transporte y rutas · RF-08

Transporte propio o externo con código, transportista, contacto, vehículo y estado. Consultar, editar y **desactivar sin borrar historial**, como todo en este sistema.

Una ruta asigna transporte, responsable y las entregas preparadas. Y el teléfono descarga **solo las entregas asignadas y autorizadas** de su responsable: ese endpoint es el que habilita toda la captura sin conexión, así que tiene que filtrar por el usuario autenticado, no por un parámetro que el cliente manda.

**Entregás:** controladores de transporte, rutas y descarga de entregas. **Se comprueba:** un responsable no puede descargar entregas de otro.

### 6. Pagos, saldos y señas · RF-05, RF-06, RF-19

Registrar pagos y aplicarlos a cargos. Consultar el saldo por cliente y por concepto, con las cinco distinciones que pide el Excel: producto, servicio, contado, crédito vigente y crédito vencido.

Las señas con referencia, importe, fecha y medio, aplicables una sola vez.

**Entregás:** controladores y servicios. **Se comprueba:** el saldo cuadra con cargos menos pagos, y una seña no se puede aplicar dos veces.

### 7. Permisos del responsable de entrega · RNF-03

ACT-05 es el actor nuevo. Administra transportes, rutas, frío y recepción. Lo que **no** ve: precios de venta, márgenes ni saldos de clientes. Un repartidor no necesita saber cuánto gana la chanchería por kilo.

**Entregás:** permisos y responsabilidad sembrada. **Se comprueba:** un usuario de reparto recibe 403 al pedir márgenes o saldos.

## Qué no te toca

Android: es S3-P2, y es la parte más grande del sprint. Si te sobra tiempo, lo más útil que podés hacer es tomar las **pantallas web** de pagos y transporte para que S3-P2 se concentre en el teléfono. Está previsto en el documento general como ajuste de carga.

Diagramas de estado: S3-P4. Criterios: S3-P3.

## De quién dependés y quién depende de vos

**Depende de vos todo el sprint**, y más que en los anteriores: S3-P2 no puede escribir el cliente de sincronización sin el contrato, y el contrato es lo más caro de cambiar después. Es lo primero que tiene que existir.

## Cómo entregarlo

```bash
git checkout -b sprint3/p1-api-pagos-entregas
git commit -m "v3.1.0 - Sprint 3 - Pagos, entregas y sincronizacion"
git push -u origin sprint3/p1-api-pagos-entregas
```

Pull Request con el código `S3-P1` en el cuerpo.
