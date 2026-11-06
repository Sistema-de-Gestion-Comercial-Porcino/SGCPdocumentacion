# Sprint 2 · Parte 4 · Victor Manuel Manrique Arancivia

Código de seguimiento: **S2-P4**. Rol: Scrum Master. Terreno: planificación, modelado, pruebas y entrega.

## Qué te toca

Abrís y cerrás el sprint.

**Al principio**, en paralelo con S2-P1: planificación, tablero y diagramas actualizados con las entidades nuevas.

**Al final**, después de S2-P2 y S2-P3: ejecutar las pruebas del recorrido completo, revisar que la integración continua pase, medir lo que haya que medir, poner la versión y la etiqueta, y preparar la entrega.

Tu rol en el perfil de proyecto dice "coordina el trabajo y los sprints; apoya el desarrollo web, Android y las pruebas del sistema". La parte de pruebas es la que más peso tiene en este sprint.

## Tus tareas

### 1. Planificación y tablero

Fechas de inicio y fin del sprint, acordadas con el grupo y el docente. El Excel dice explícitamente que **no se inventan fechas de sprint**, así que se acuerdan y se anotan, no se suponen.

El tablero con las cuatro partes y su estado, y el orden de dependencia:

```
S2-P3 (criterios)  ──┐
                     ├──> S2-P1 (API) ──> S2-P2 (web) ──> S2-P3 (validacion) ──> S2-P4 (entrega)
S2-P4 (diagramas) ──┘
```

El único bloqueo duro es P1 antes de P2. Lo que conviene vigilar es que P1 publique el contrato en Swagger temprano: si lo deja para el final, P2 se queda sin tiempo y P3 y P4 sin nada que probar. Ese es el riesgo real del sprint, no la dificultad técnica.

**Entregás:** fechas y tablero. **Se comprueba:** cada parte sabe cuándo empieza y de qué depende.

### 2. Diagramas UML del Sprint 2

En `02_Ingenieria_de_Software/`, con StarUML, que es la herramienta declarada en el perfil.

Las once entidades nuevas entran al diagrama de clases, con sus asociaciones y multiplicidades. Y los diagramas de comportamiento de los casos de uso nuevos: faeneo con resultados en lotes, pesaje y entrada como **dos pasos separados**, control sanitario con su rechazo.

Hay dos máquinas de estados que valen la pena, porque las reglas del sprint son de estado: la del animal, con el bloqueo por rechazo sanitario, y la de la orden de producción.

Y el diccionario en `02_Ingenieria_de_Software/00_Documentacion/Diccionario_clases.md`, con los atributos y las reglas de cada entidad nueva.

Lo que conviene no hacer: regenerar por rutina los diagramas que no cambiaron. El propio documento de estado del Sprint 1 lo dice, y regenerar todo mete ruido en el control de versiones sin aportar nada.

**Entregás:** `.mdj` actualizados, PDF de clases y diccionario. **Se comprueba:** cada entidad del código está en el diagrama, y cada clase del diagrama existe en el código.

### 3. Extender la verificación automática

En `SGCPapi/tests/SGCP.Verificacion/Program.cs` hay un recorrido de 27 comprobaciones por HTTP que ya pasa contra MySQL real. Agregá las del Sprint 2, siguiendo el mismo estilo: una línea por comprobación, con el nombre de la regla que prueba.

Las cuatro que no pueden faltar son las del criterio de validación. La segunda es la más valiosa, porque es la que más fácil se implementa mal:

```
Pesaje no mueve existencia
Entrada fisica si mueve existencia
Entrada fisica duplicada se rechaza
Animal rechazado no entra a faeneo
Una orden deja dos resultados en lotes distintos
Reserva contra prevision se rechaza
Usuario de produccion no ve precios de venta
```

Cómo correrlo, de las dos maneras:

```bash
export SGCP_MYSQL_TEST="Server=127.0.0.1;Port=3307;User ID=sgcp;Password=CLAVE;SslMode=Preferred"
LANG=es_BO.UTF-8 dotnet run --project tests/SGCP.Verificacion
LANG=C            dotnet run --project tests/SGCP.Verificacion
```

**Las dos corridas, no una.** Con `LANG` sin definir, .NET usa cultura invariante y los defectos de decimales desaparecen: las pruebas pasan con el sistema roto. Así se escaparon dos defectos en el Sprint 1 y está documentado en `00_Definicion/Errores_encontrados_Sprint1.md` sección 3.

El método completo, con el MySQL desechable en contenedor y el puerto 3307 para no pisar otra instancia, está en `00_Definicion/Metodo_de_verificacion.md`.

**Entregás:** el verificador extendido. **Se comprueba:** pasa con las dos configuraciones regionales, contra MySQL real.

### 4. Integración continua

El flujo `.github/workflows/sprint1-mysql.yml` levanta un MySQL 8.4 temporal, compila con `--warnaserror`, revisa que el modelo y la migración estén sincronizados, genera el script y corre la verificación. Renombralo a `sprint2-mysql.yml` o quitale el número, que envejece peor.

Dos cosas que ya mordieron una vez y conviene no repetir:

- **Nunca `--idempotent` en el paso del script.** En MySQL genera sintaxis de T-SQL y el script no sirve.
- **Un paso de CI falla con el entorno de CI, no con el tuyo.** El flujo falló una vez porque la fábrica de diseño exigía la cadena de conexión y en CI no hay secretos. Para reproducirlo hay que quitar la variable y usar Release, igual que hace CI:

```bash
env -u ConnectionStrings__Sgcp dotnet ef migrations has-pending-model-changes \
  --project src/SGCP.Api --configuration Release --no-build
```

Está en `00_Definicion/Cambio_a_MySQL.md` sección 2.

**Entregás:** el flujo al día y verde. **Se comprueba:** la ejecución en GitHub está en verde. Que el archivo exista no significa que haya corrido: hay que mirar el resultado.

### 5. Pendiente del Sprint 1: medir el desempeño

RNF-02 quedó sin medir y es tuyo por rol. Pide que registrar una operación frecuente **no tome más tiempo que la anotación manual comparable**, medido con usuarios y escenarios acordados.

Es una comparación, no un número absoluto: hay que cronometrar las dos cosas. Elegí dos o tres operaciones frecuentes —cargar un cliente, armar una cotización—, cronometrá a alguien haciéndolo en el sistema y cronometrá la anotación en cuaderno. Anotá los dos tiempos, quién lo hizo y en qué equipo.

No se puede inventar, y es lo que vuelve a RNF-02 algo demostrable.

**Entregás:** una nota corta en `00_Definicion/`. **Se comprueba:** hay dos tiempos comparados por operación, no una afirmación.

### 6. Versión, etiqueta y entrega

La versión del sprint la pones vos, una vez, al final. Nadie más etiqueta.

Según el esquema del README, MAYOR es el número de sprint, así que el Sprint 2 cierra en **`v2.0.0`** en los cuatro repositorios. Los números intermedios que usaron las partes durante el sprint quedan en el historial.

En cada repositorio, después del último PR aprobado:

```bash
git checkout main && git pull
git tag -a v2.0.0 -m "Sprint 2 entregado"
git push origin v2.0.0
```

**La etiqueta va después del commit, nunca antes**, o apunta al estado anterior.

Y la fila nueva en la tabla de historial del README de cada repositorio: versión, fecha, sprint, cambio y autor.

**Entregás:** las cuatro etiquetas y los cuatro README actualizados. **Se comprueba:** `git show v2.0.0` muestra el estado entregado en cada repositorio.

### 7. El estado real, sin adornos

Una página en `00_Definicion/Estado_Sprint2.md` con tres cosas: qué quedó hecho y verificado, **contra qué entorno** se verificó, y qué quedó sin probar.

Lo que hace útil este documento es la tercera parte. En el Sprint 1 quedaron tres pendientes escritos, y por eso se sabía exactamente qué faltaba en lugar de descubrirlo en la presentación. Un resultado verde en un entorno que no es el de entrega es un resultado provisional, y conviene escribirlo así.

**Entregás:** el documento de estado. **Se comprueba:** dice contra qué base de datos y con qué configuración regional se probó.

## Qué no te toca

Escribir la API ni las pantallas. Si una prueba falla, la reportás con el código de la parte responsable; no la corregís vos.

Los criterios de aceptación son de S2-P3. Vos los ejecutás de forma automatizada; ella los define y da el veredicto.

## De quién dependés y quién depende de vos

**Dependés de S2-P1 y S2-P2** para la mitad final de tu trabajo: sin código no hay qué probar ni qué etiquetar.

**Depende de vos todo el sprint** para los diagramas y la planificación al principio, y para la entrega al final. Sos el último en firmar: si no cerrás, el sprint no está entregado aunque el código esté.

## Cómo entregarlo

Diagramas y documentos van a **SGCPdocumentacion**; el verificador y el flujo de CI van a **SGCPapi**. Son dos PR.

```bash
git checkout -b sprint2/p4-modelado-pruebas
git commit -m "v2.4.0 - Sprint 2 - Diagramas, verificacion y entrega"
git push -u origin sprint2/p4-modelado-pruebas
```

Los dos con el código `S2-P4` en el cuerpo.
