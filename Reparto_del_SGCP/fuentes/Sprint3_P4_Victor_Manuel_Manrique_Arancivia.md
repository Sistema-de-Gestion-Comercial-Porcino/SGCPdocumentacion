# Sprint 3 · Parte 4 · Victor Manuel Manrique Arancivia

Código de seguimiento: **S3-P4**. Rol: Scrum Master. Terreno: planificación, modelado, pruebas y entrega.

## Qué te toca

Abrís con los diagramas de estado, que en este sprint son más importantes que en cualquier otro, y cerrás con las pruebas de duplicados y conflictos, que son lo que define si el sprint funciona.

Y una tarea de coordinación que es tuya por rol: **vigilar que el contrato de sincronización se acuerde en la primera semana.** Es el mayor riesgo del sprint y no es técnico, es de organización.

## Tus tareas

### 1. Vigilar el contrato de sincronización

S3-P1 y S3-P2 tienen que acordar el cuerpo de la petición y la respuesta antes de escribir código. Si eso se define a mitad del sprint, los dos rehacen trabajo y el sprint no entra.

Tu trabajo acá es simple y no es técnico: que la reunión pase en la primera semana y que el resultado quede **escrito** en el README de SGCPapi, no acordado de palabra.

Lo que tiene que estar decidido: quién genera la clave única —el teléfono—, qué responde el servidor ante una clave repetida, qué pasa con un conflicto, si se manda una recepción o un lote, y si la evidencia va en el mismo envío.

**Entregás:** el contrato escrito, con fecha. **Se comprueba:** existe antes de que haya código de sincronización en cualquiera de los dos repositorios.

### 2. Diagramas de estado · RF-07

Este sprint es de estados, así que las máquinas de estados son el diagrama que importa. En StarUML, en `02_Ingenieria_de_Software/`.

**La máquina de estados de la recepción**, que es la central: pendiente, sincronizada, entregada, observada y conflicto. Con las transiciones válidas y, sobre todo, **las que no son válidas**: no se llega a entregada sin pasar por sincronizada.

**La de la entrega** y **la de la deuda**, por separado, que es la forma de mostrar en un diagrama que son independientes. Si quedan en una sola máquina, el diagrama contradice el criterio de validación.

Un diagrama de secuencia de la sincronización, con los tres caminos: normal, reintento y conflicto. Es el que conviene tener a mano en la defensa, porque es lo que el docente va a querer que le expliquen.

Y el diccionario de clases con las nueve entidades nuevas.

Una cosa que vale revisar al final: que la máquina de estados del diagrama y la que implementó S3-P2 con el patrón State **coincidan**. Si no coinciden, uno de los dos está mal, y encontrarlo es justamente el valor de haber hecho el diagrama.

**Entregás:** `.mdj` actualizados, PDF y diccionario. **Se comprueba:** cada estado del código está en el diagrama y al revés.

### 3. Probar duplicados y conflictos · RNF-01

Esta es tu tarea más valiosa del proyecto. El Excel pide que «el reintento no duplique datos y los conflictos requieran revisión», y eso **no se prueba con buena señal**: con buena señal nunca falla.

Extendé el verificador de `SGCPapi/tests/SGCP.Verificacion/Program.cs` con las comprobaciones del sprint. Las que no pueden faltar:

```
Lote de recepciones se sincroniza y crea las filas
El mismo lote reenviado NO crea filas nuevas
Clave repetida devuelve el identificador original, no un error
Version base distinta marca conflicto y no aplica el cambio
Un conflicto no se resuelve solo
Recepcion conforme queda ENTREGADA
Recepcion con observaciones queda OBSERVADA
Confirmar entrega no cambia el saldo del cliente
Registrar un pago no cambia el estado de la entrega
Un responsable no descarga entregas de otro
Una sena no se aplica dos veces
```

La segunda es la que más vale: mandar el mismo lote dos veces y **contar las filas en MySQL**, no confiar en lo que responde la API.

Y la prueba manual que ninguna automática reemplaza: el teléfono en **modo avión de verdad**, capturar, cortar la sincronización a mitad y reintentar. Coordinalo con S3-P3, que necesita lo mismo.

Las dos corridas, con `LANG=es_BO.UTF-8` y con `LANG=C`, por lo explicado en `00_Definicion/Metodo_de_verificacion.md`.

**Entregás:** el verificador extendido. **Se comprueba:** pasa contra MySQL real, y el conteo de filas después de un reenvío es el mismo.

### 4. RNF-05, compatibilidad, con evidencia

La aplicación tiene que haber corrido en **dispositivos reales**. El mínimo declarado es Android 8.0, API 26.

Lo que falta anotar, y falta desde el Sprint 1: marca, modelo y versión de Android de cada teléfono probado, y si la captura sin conexión funcionó en cada uno. Dos dispositivos distintos como mínimo, porque uno solo no dice nada sobre compatibilidad.

Coordinalo con S3-P2, que los necesita para desarrollar.

**Entregás:** la tabla de dispositivos probados. **Se comprueba:** hay dos modelos con versión y resultado.

### 5. Integración continua

El flujo de GitHub Actions ya levanta MySQL temporal, compila con `--warnaserror`, revisa el modelo y corre la verificación. Agregá las comprobaciones nuevas.

Lo que no cambia y vale recordar: **nunca `--idempotent`** en el paso del script, porque en MySQL genera sintaxis de T-SQL. Y si un paso falla, reproducilo **con el entorno de CI**, no con el tuyo: sin la variable de conexión y en Release. Está en `00_Definicion/Cambio_a_MySQL.md` sección 2.

Las pruebas de Android se pueden agregar al flujo con `./gradlew testDebugUnitTest`. Lo que **no** se puede automatizar es la captura sin conexión en un dispositivo real: eso queda manual y hay que decirlo, no fingir que está cubierto.

**Entregás:** el flujo al día y verde. **Se comprueba:** la ejecución en GitHub está en verde. Que el archivo exista no significa que haya corrido.

### 6. Versión, etiqueta y entrega

Tu commit es el último del sprint, `v3.4.0`, y **esa misma versión es la etiqueta de cierre** en los cuatro repositorios. No se etiqueta `v3.0.0`: quedaría por detrás de lo que ya entregaron tus compañeros.

```bash
git checkout main && git pull
git tag -a v3.4.0 -m "Sprint 3 entregado"
git push origin v3.4.0
```

**Después del commit, nunca antes.** Y la fila nueva en la tabla de historial del README de cada repositorio.

**Entregás:** las cuatro etiquetas y los README. **Se comprueba:** `git show v3.4.0` muestra el estado entregado.

### 7. El estado real

`00_Definicion/Estado_Sprint3.md` con lo hecho, contra qué entorno, y **qué quedó sin probar**.

En este sprint la tercera parte es la que más importa, porque hay cosas que solo se prueban con un teléfono y es fácil que queden sin hacer. Si la captura sin conexión se probó en un solo dispositivo, se escribe que fue uno. Si el conflicto no se llegó a provocar, se escribe que no se provocó.

**Entregás:** el documento de estado. **Se comprueba:** dice en qué dispositivos y con qué configuración regional se probó.

## Qué no te toca

Programar la API ni Android. Si una prueba falla, la reportás con el código de la parte responsable.

Los criterios de aceptación son de S3-P3: ella los define y da el veredicto, vos los automatizás.

## De quién dependés y quién depende de vos

**Dependés de S3-P1 y S3-P2** para la mitad final. Y necesitás un teléfono con la aplicación.

**Depende de vos** que el contrato se acuerde temprano, que es el mayor riesgo del sprint, y la entrega al final.

## Cómo entregarlo

Diagramas y documentos a **SGCPdocumentacion**; verificador y CI a **SGCPapi**. Dos Pull Requests.

```bash
git checkout -b sprint3/p4-estados-pruebas
git commit -m "v3.4.0 - Sprint 3 - Diagramas de estado, pruebas de sincronizacion y entrega"
git push -u origin sprint3/p4-estados-pruebas
```

Los dos con el código `S3-P4` en el cuerpo.
