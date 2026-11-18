# Método de verificación del SGCP

Nota para quien continúe la implementación. Describe cómo verificar el Sprint 1 y qué clase de errores encuentra cada paso. Los dos defectos de la sección 4 se encontraron así, después de que la compilación, las 27 comprobaciones sobre SQLite y la revisión estática del código dieran todas en verde. **Los dos ya están corregidos en los repositorios**; quedan documentados porque la misma clase de error vuelve a aparecer en cuanto se agregue el primer campo decimal del Sprint 2.

La idea de fondo: **compilar no es verificar, y pasar pruebas en una máquina no es pasarlas en la del docente.** Hay tres entornos distintos en juego —SQLite de pruebas, MySQL de entrega, y la configuración regional de cada laptop— y un defecto puede vivir en la diferencia entre ellos.

El motor cambió de SQL Server a MySQL el 6 de noviembre de 2026. Eso mejoró la verificación más de lo que parece: un MySQL de prueba se levanta en veinte segundos en un contenedor, así que **el recorrido completo ya corre contra el motor real**, que con SQL Server nunca se consiguió desde esta máquina. Las secciones 1 y 2 quedaron reescritas por eso. Lo que cambió en el código está en `Cambio_a_MySQL.md`.

## 1. Probar contra el motor real, en una base desechable

Es el camino preferido y el que se usó. No toca ni el repositorio ni ninguna base del equipo:

```bash
docker run -d --name sgcp_mysql_prueba -p 127.0.0.1:3307:3306 \
  -e MYSQL_ROOT_PASSWORD=UNA_CLAVE -e MYSQL_DATABASE=sgcp \
  -e MYSQL_USER=sgcp -e MYSQL_PASSWORD=UNA_CLAVE mysql:8.4
```

El puerto 3307 es a propósito: si ya hay un MySQL propio en 3306, no se lo pisa. Luego:

```bash
export SGCP_MYSQL_TEST="Server=127.0.0.1;Port=3307;User ID=sgcp;Password=UNA_CLAVE;SslMode=Preferred"
dotnet run --project tests/SGCP.Verificacion
```

El verificador crea una base `sgcp_pruebas_<uuid>` propia, aplica la migración **dos veces** para comprobar que es idempotente, verifica que no queden migraciones pendientes, corre las 27 comprobaciones por HTTP y al terminar borra solo esa base. Al final, `docker rm -f sgcp_mysql_prueba` y no queda nada.

Al usuario de pruebas hay que darle permiso de crear bases, acotado al prefijo para que no pueda tocar nada más:

```sql
GRANT ALL PRIVILEGES ON `sgcp%`.* TO 'sgcp'@'%';
```

## 1b. Sustituir el proveedor en una copia desechable, si no hay motor a mano

Sigue sirviendo cuando no se puede levantar MySQL. Se trabaja sobre una **copia fuera del repositorio**:

```bash
W=/tmp/sgcp-prueba
rm -rf "$W"; mkdir -p "$W"
cd SGCPapi && tar -cf - --exclude=bin --exclude=obj --exclude=.git . | (cd "$W" && tar -xf -)
cd "$W"
dotnet add src/SGCP.Api/SGCP.Api.csproj package Microsoft.EntityFrameworkCore.Sqlite
```

En la copia, y solo en la copia, se cambian dos cosas:

1. En `Arranque.cs`, `UseMySQL(...)` por `UseSqlite("Data Source=.../sgcp.db")`.
2. Antes de sembrar los datos iniciales, `await db.Database.EnsureCreatedAsync();`, que construye el esquema **desde el modelo** y evita la migración de MySQL.

Esto no hace falta para el proyecto de pruebas, que ya trae las dos vías: sin `SGCP_MYSQL_TEST` usa SQLite en un archivo temporal, con la variable usa MySQL.

Luego se levanta con configuración por variables de entorno, sin tocar ningún archivo de configuración del repositorio:

```bash
Jwt__Clave='clave-local-de-pruebas-de-al-menos-32-bytes' \
DatosIniciales__Habilitar=true DatosIniciales__ClaveAdministrador='Admin.2026!' \
dotnet run --project src/SGCP.Api --no-launch-profile --urls http://127.0.0.1:5199
```

La copia se borra al terminar. El repositorio nunca llega a tener una referencia a SQLite ni un `EnsureCreated`.

### Lo que esta técnica NO prueba

Que la aplicación arranque sobre SQLite no dice nada sobre si arrancará sobre MySQL. Y al revés: **un fallo en SQLite puede ser un falso positivo.** El caso típico: SQLite no tiene tipo decimal, guarda los `decimal` como texto, y una restricción `CHECK (columna <= 100)` compara cadenas, de modo que `'30' <= '100'` es falso y la restricción falla con un valor perfectamente válido. En MySQL la misma restricción funciona. Antes de dar por bueno un fallo aparecido solo en SQLite hay que mirar el SQL generado para MySQL.

Hay una diferencia más, propia del cambio de motor: las tres reglas de unicidad que antes eran índices filtrados ahora son **columnas generadas**. SQLite también las soporta, así que la vía SQLite las ejerce; pero si en el Sprint 2 se agrega una regla parecida, hay que comprobarla en MySQL, que es donde cuenta.

## 2. Revisar el SQL de la migración antes de aplicarlo

Aunque ahora se pueda ejecutar de verdad, leer el SQL generado sigue encontrando cosas antes de perder tiempo:

```bash
dotnet ef migrations script --project src/SGCP.Api --context SgcpContext -o mysql.sql
```

**Sin `--idempotent`.** Esa opción está rota para MySQL: EF envuelve cada instrucción en `IF NOT EXISTS(...) BEGIN ... END`, que es sintaxis de T-SQL y MySQL rechaza con error de sintaxis. El script del repositorio, `database/InicialSprint1.sql`, es el plano. Para reaplicar sin riesgo está `dotnet ef database update`, que consulta `__EFMigrationsHistory` desde el cliente y no necesita esa envoltura.

Sobre ese archivo se revisan las clases de error propias de MySQL:

| Qué se busca | Error que evita | Cómo se revisa |
|---|---|---|
| Sintaxis de T-SQL colada en el script | Error 1064 al aplicar | `grep -nE 'IF NOT EXISTS\(|^BEGIN|^END|GO$|\[|nvarchar|datetime2|uniqueidentifier'`; no debe haber nada |
| Clave de índice mayor a 3072 bytes | Error 1071 | Sumar las columnas de cada índice: en `utf8mb4` cada carácter cuenta 4 bytes, así que `varchar(768)` ya es el límite |
| Columna generada mal declarada | Error 3105 o 1906 | Que cada `AS (...)` solo use columnas de su propia tabla y funciones deterministas |
| Precisión decimal declarada | Truncamiento silencioso | Que cada columna de dinero tenga `decimal(p,s)` explícito |
| Motor y juego de caracteres | Ordenación y comparación inesperadas | Que las tablas queden en InnoDB y `utf8mb4`, que es el valor por defecto en MySQL 8 |

MySQL **sí admite varios caminos en cascada hacia la misma tabla**, de modo que el Msg 1785 de SQL Server, que fue la preocupación central mientras el motor era ese, dejó de existir. Las reglas `Restrict` del modelo se mantuvieron igual: están para conservar el histórico comercial, no para evitar el error del motor.

## 3. Ejercer los criterios de aceptación por HTTP, no por unidad

Las pruebas unitarias con el servicio en memoria no tocan ni el enlace de modelo, ni la validación por atributos, ni la serialización, ni la configuración regional. Ahí es donde aparecen los errores que importan. Por eso la verificación se hace contra la aplicación levantada, con `curl`, siguiendo el recorrido real de la demostración:

```
login → clasificación → producto → cliente → vigencia de precio
      → cotización → presentar → (intentar pedido: debe fallar)
      → aceptar → confirmar pedido → leer margen
      → nueva vigencia → releer margen (no debe cambiar)
      → intentar segundo pedido (debe fallar)
```

Cada paso compara contra un valor esperado concreto, no contra «no explotó». El margen tiene que dar `28`, el segundo pedido tiene que devolver `COTIZACION_YA_TIENE_PEDIDO`, y la cotización rechazada tiene que devolver `COTIZACION_NO_ACEPTADA`.

Dos detalles que ahorran tiempo:

- Comparar números como números. `28.0` y `28.00` son el mismo margen; un script que compare cadenas reporta una falla que no existe.
- Cuando un paso falla, los siguientes heredan identificadores vacíos y fallan en cascada. Se arregla el primero y se vuelve a correr todo; no se diagnostican los demás por separado.

## 4. Probar con la configuración regional de la máquina de destino

**Este es el paso que faltaba, y el que encontró los dos defectos.**

Las laptops del equipo y la del docente corren en español. En `es-BO` y `es-ES` el separador decimal es la coma y el punto es separador de miles. Una verificación hecha con cultura invariante o en inglés no ve nada de lo que sigue. Comprobación mínima:

```bash
echo $LANG          # es_BO.UTF-8
```

```csharp
CultureInfo.CurrentCulture              // es-BO
decimal.TryParse("35.00", NumberStyles.Number, CultureInfo.CurrentCulture, out var v)
// devuelve true, y v == 3500
```

Ese `3500` no es una hipótesis: es la salida real en esta máquina.

### Defecto 1 · `[Range]` con límites en texto revienta la API

```csharp
[Range(typeof(decimal), "0.01", "9999999999.99")] decimal CostoReferencia
```

`RangeAttribute` convierte los límites `"0.01"` y `"9999999999.99"` con la **cultura actual**. En `es-BO` la conversión lanza `FormatException`, el atributo lanza `ArgumentException` durante la validación del modelo, y el resultado es **HTTP 500 en toda petición que lleve un decimal**: abrir una vigencia de precio, crear una cotización, confirmar un pedido.

Corrección, en cada atributo:

```csharp
[Range(typeof(decimal), "0.01", "9999999999.99",
       ParseLimitsInInvariantCulture = true, ConvertValueInInvariantCulture = true)]
```

Afecta a `Contratos/Peticiones/Peticiones.cs` en la API y a `Models/ViewModels/ViewModels.cs` en la web.

### Defecto 2 · el enlace de formularios lee los decimales con la cultura del sistema

Las vistas escriben los valores con `ToString(CultureInfo.InvariantCulture)`, que es lo correcto porque `<input type="number">` exige el punto. Pero ASP.NET Core enlaza los campos de formulario con `CultureInfo.CurrentCulture`, no con la invariante. En una máquina en español, el `35.00` que el navegador envía se interpreta con el punto como separador de miles y **se guarda 3500**. Sin error, sin advertencia, sin rastro.

Corrección en `Program.cs` de la web, antes de `MapControllerRoute`:

```csharp
var culturaFija = new RequestLocalizationOptions()
    .SetDefaultCulture("es-BO")
    .AddSupportedCultures("es-BO")
    .AddSupportedUICultures("es-BO");
app.UseRequestLocalization(culturaFija);
```

Fijar la cultura no alcanza por sí solo: hay que elegir **una** convención y usarla en los dos extremos. Si la vista escribe con punto, el enlace tiene que leer con punto. Lo más simple es dejar la interfaz en `es-BO` para que las fechas y los textos salgan en español, y marcar los campos numéricos con un enlace invariante explícito, o escribirlos con la misma cultura con que se leen.

### Por qué ninguna prueba automatizada lo vio

Cuando `LANG` no está definida —el caso habitual en un intérprete de comandos lanzado por una herramienta— .NET usa la cultura invariante y **los dos defectos desaparecen**. Medido en esta máquina:

```
sin LANG:            CurrentCulture = ''      "35.00" -> 35.00
LANG=es_BO.UTF-8:    CurrentCulture = es-BO   "35.00" -> 3500
```

De ahí que la batería de 27 comprobaciones pasara en verde mientras la aplicación estaba rota para cualquiera que la abriera desde su escritorio. **Una prueba que no reproduce la configuración regional del usuario no está probando la aplicación del usuario.**

### Cómo comprobar que quedó arreglado

Hay que verificar en los dos sentidos: que con el arreglo funciona, y que sin el arreglo falla. Si solo se comprueba lo primero, no se sabe si el arreglo hizo algo.

```bash
LANG=es_BO.UTF-8 LC_ALL=es_BO.UTF-8 dotnet run ...
```

Para la API, repetir el recorrido de la sección 3: la vigencia de precio tiene que devolver `201` y el margen del pedido tiene que dar `28`.

Para la web, enviar el formulario de precios por HTTP con un importe que tenga decimales y **releer el valor guardado desde la API**, no desde la pantalla. Un `55.25` que vuelve como `5525` es el defecto; mirar la pantalla no sirve porque vuelve a formatear.

Resultado de la verificación hecha con los arreglos aplicados, bajo `LANG=es_BO.UTF-8`:

```
API, 11 de 11 comprobaciones correctas
  vigencia 201 · margen 28 · margen intacto al cambiar el precio
  rechaza COTIZACION_NO_ACEPTADA, duplicado y último administrador
Web, formulario de precios
  con el arreglo:  se envía 55.25 / 77.50  ->  se guarda 55.25 / 77.50
  sin el arreglo:  se envía 66.25 / 88.50  ->  se guarda 6625 / 8850
```

Conviene correr además la misma batería con `LANG=C`, para confirmar que el arreglo no depende de la cultura en ningún sentido.

## 5. Orden recomendado

1. `dotnet build` en los tres repositorios: cero errores y **cero advertencias**.
2. `dotnet ef migrations has-pending-model-changes --context SgcpContext`: el modelo y la migración tienen que estar sincronizados.
3. `dotnet ef migrations script --context SgcpContext` y revisión de la sección 2.
4. MySQL desechable en contenedor y las 27 comprobaciones de la sección 1, con `LANG=es_BO.UTF-8`.
5. La vía SQLite del mismo verificador, que no necesita motor, como red de seguridad.
6. Repetir el recorrido con `LANG=C` para confirmar que nada depende de la cultura.
7. La web levantada contra esa API, incluido el envío del formulario de precios de la sección 4.

Los pasos 1 a 3 y el 5 no necesitan nada instalado. El 4 es el que de verdad certifica la entrega, y ahora es barato.

## 6. Qué registrar

Cada verificación deja dicho **qué se probó, contra qué entorno y qué quedó sin probar**. «27 comprobaciones correctas» no informa si no dice sobre qué base de datos, con qué cultura y por qué vía. Un resultado verde en un entorno que no es el de entrega es un resultado provisional, y conviene escribirlo así.
