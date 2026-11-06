# Sprint 1 · Parte 4 · Victor Manuel Manrique Arancivia

Código de seguimiento: **S1-P4**. Rol: Scrum Master. Terreno: planificación, modelado, pruebas y entrega.

## Estado: dos tareas abiertas

Falta medir RNF-02, desempeño, que es tuyo por rol y no se puede calcular. Y falta cerrar formalmente el sprint: poner la etiqueta `v1.0.0` en los cuatro repositorios.

## Tu tarea 1: medir RNF-02, desempeño

El requerimiento dice:

> El registro de una operación frecuente no deberá tomar más tiempo que una anotación manual comparable, medido con usuarios y escenarios acordados.

Lo que suele malinterpretarse: **no es un número absoluto, es una comparación.** No alcanza con decir «la pantalla carga en 300 milisegundos». Hay que cronometrar las dos cosas, el sistema y el cuaderno, y mostrar que el sistema no es más lento.

Cómo hacerlo, en una sesión:

1. **Elegí dos o tres operaciones frecuentes.** Cargar un cliente nuevo y armar una cotización son las candidatas obvias: son las que más veces por día va a hacer el personal.
2. **Cronometrá la anotación manual.** Que alguien escriba lo mismo en un cuaderno, como lo hacen hoy. Ese es el punto de comparación que el requerimiento pide.
3. **Cronometrá la misma operación en el sistema**, con la misma persona, sin ayuda.
4. **Anotá los dos tiempos**, quién lo hizo, en qué equipo y con qué conexión.

Lo que se entrega es una tabla así, con números reales:

| Operación | A mano | En el sistema | Cumple |
|---|---|---|---|
| Cargar un cliente nuevo | | | |
| Armar una cotización de un producto | | | |
| Confirmar un pedido | | | |

Si el sistema sale más lento en alguna, eso también es un resultado válido y hay que escribirlo. Un requerimiento no funcional que no se cumple y está medido es mejor evidencia que uno que se declara cumplido sin datos.

Conviene coordinarlo con S1-P3, que necesita personas para medir usabilidad: es la misma sesión y la misma gente.

**Entregás:** una nota de una página en `00_Definicion/`. **Se comprueba:** hay dos tiempos comparados por operación, no una afirmación.

## Tu tarea 2: cerrar el sprint con la etiqueta

Los cuatro repositorios tienen commits pero **ninguna etiqueta**. Ahora mismo la versión existe como frase en el README y nada en git apunta a ella: si el docente pide ver la `v1.0.0`, no hay nada que mostrar. En una materia de Ingeniería de Software eso es justo lo que se mira.

El Sprint 1 cierra en **`v1.0.0`** en los cuatro, según el esquema del README donde MAYOR es el número de sprint. En cada repositorio, después del último PR aprobado:

```bash
git checkout main && git pull
git tag -a v1.0.0 -m "Sprint 1 entregado"
git push origin v1.0.0
```

**La etiqueta va después del commit, nunca antes**, o apunta al estado anterior. Es el error más fácil de cometer.

Y la fila correspondiente en la tabla de historial del README de cada repositorio, que ya está armada: versión, fecha, sprint, cambio y autor.

**Entregás:** las cuatro etiquetas empujadas. **Se comprueba:** `git show v1.0.0` muestra el estado entregado en cada repositorio.

## Tu tarea 3: verificar en otra máquina

Todo lo verificado hasta ahora corrió en una sola máquina. Vale repetirlo en la tuya, que es un entorno distinto y es exactamente donde aparecen los defectos que nadie vio.

Con MySQL en contenedor:

```bash
docker run -d --name sgcp_mysql_prueba -p 127.0.0.1:3307:3306 \
  -e MYSQL_ROOT_PASSWORD=CLAVE -e MYSQL_DATABASE=sgcp \
  -e MYSQL_USER=sgcp -e MYSQL_PASSWORD=CLAVE mysql:8.4

export SGCP_MYSQL_TEST="Server=127.0.0.1;Port=3307;User ID=sgcp;Password=CLAVE;SslMode=Preferred"
LANG=es_BO.UTF-8 dotnet run --project tests/SGCP.Verificacion
LANG=C            dotnet run --project tests/SGCP.Verificacion
```

El puerto 3307 es a propósito: si ya hay un MySQL en 3306, no se lo pisa. Al terminar, `docker rm -f -v sgcp_mysql_prueba`.

**Las dos corridas, no una.** Con `LANG` sin definir, .NET usa cultura invariante y los defectos de decimales desaparecen: las pruebas pasan con el sistema roto. Así se escaparon dos defectos en este sprint, y está documentado en `00_Definicion/Errores_encontrados_Sprint1.md` sección 3.

Si no tenés Docker, el mismo verificador corre sobre SQLite sin la variable de entorno. No certifica MySQL, pero comprueba el comportamiento.

**Entregás:** el resultado anotado en el documento de estado. **Se comprueba:** dice en qué máquina, contra qué base y con qué configuración regional.

## Tu tarea 4: fechas del proyecto

El perfil de proyecto tiene «Fecha de inicio: Por acordar» y «Fecha Fin: Por acordar», y la tabla de sprints sin fechas de entrega. El Excel dice explícitamente que **no se inventan fechas de sprint**: se acuerdan con el grupo y el docente, y se anotan.

Es tu rol y es lo primero que un docente mira en una planificación.

**Entregás:** el Excel con las fechas acordadas. **Se comprueba:** no quedan celdas «Por acordar» en la planificación.

## Lo que no te toca

Programar. RNF-04, usabilidad, es de S1-P3. El APK en un teléfono es de S1-P2.

## Cuándo

Durante el Sprint 2, en paralelo. La etiqueta, en cuanto el docente dé la devolución y se cierre lo que pida: si se etiqueta antes y hay cambios, la `v1.0.0` queda apuntando a algo que después se corrigió.

## Cómo entregarlo

Documentos y Excel van a **SGCPdocumentacion**:

```bash
git checkout -b sprint1/p4-cierre
git commit -m "v1.0.1 - Sprint 1 - Medicion de desempeno y cierre"
git push -u origin sprint1/p4-cierre
```

Pull Request con el código `S1-P4` en el cuerpo. Las etiquetas van aparte, después del PR aprobado.
