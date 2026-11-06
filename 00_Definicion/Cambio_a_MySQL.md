# Cambio de SQL Server a MySQL

El 6 de noviembre de 2026 el docente autorizó usar cualquier motor de base de datos y el equipo decidió MySQL. Este documento dice qué se cambió, por qué, y las tres trampas que aparecieron al hacerlo. Solo se tocó **SGCPapi**: la web y Android nunca hablaron con la base de datos, siempre con la API.

El resultado quedó mejor que antes en un punto que importaba: **la migración y las 27 comprobaciones ya corren contra el motor real**, cosa que con SQL Server no se consiguió nunca desde una máquina del equipo.

## 1. Qué proveedor y por qué ese

Se usa **`MySql.EntityFrameworkCore` 10.0.12**, el proveedor oficial de Oracle.

La alternativa conocida es Pomelo, que es muy usada, pero **su última versión estable es la 9.0.0 y está hecha para EF Core 9**. Adoptarla obligaba a bajar todo el proyecto de .NET 10 a .NET 9. El de Oracle publica un grupo `net10.0` que depende exactamente de `Microsoft.EntityFrameworkCore 10.0.12`, la versión que ya usaba el proyecto, así que no hubo que mover nada más.

Esto importa para el Sprint 2: **no cambien a Pomelo** sin bajar el framework, y no mezclen los dos proveedores en la misma solución.

## 2. Lo que se cambió en el código

| Archivo | Cambio |
|---|---|
| `src/SGCP.Api/SGCP.Api.csproj` | `Microsoft.EntityFrameworkCore.SqlServer` → `MySql.EntityFrameworkCore` |
| `src/SGCP.Api/Arranque.cs` | `UseSqlServer(...)` → `UseMySQL(...)` |
| `src/SGCP.Api/Datos/FabricaContexto.cs` | lo mismo, para el diseño de migraciones |
| `src/SGCP.Api/Comun/CadenaConexion.cs` | **nuevo**: exige la cadena de conexión y explica el formato si falta |
| `src/SGCP.Api/Comun/ErroresMiddleware.cs` | `SqlException` → `MySqlException`, con los números de error de MySQL |
| `src/SGCP.Api/appsettings.json` | la cadena de conexión queda vacía |
| `src/SGCP.Api/Datos/Configuraciones/` | tres índices filtrados reemplazados, ver sección 3 |
| `src/SGCP.Api/Datos/Migraciones/` | migración regenerada desde cero con el proveedor de MySQL |
| `database/InicialSprint1.sql` | script regenerado, **sin** `--idempotent`, ver sección 4 |
| `tests/SGCP.Verificacion/Program.cs` | `SGCP_SQLSERVER_TEST` → `SGCP_MYSQL_TEST` |
| `scripts/Verificar-MySql.ps1` | renombrado desde `Verificar-SqlServer.ps1` |
| `.github/workflows/sprint1-mysql.yml` | reescrito, levanta `mysql:8.4` en vez de SQL Server 2022 |

Los servicios, controladores, entidades y el Builder **no se tocaron**. Esa es la prueba de que la separación por capas estaba bien hecha: cambiar de motor no llegó a la lógica de negocio.

### La cadena de conexión ya no tiene valor por defecto

Antes había una cadena de SQL Server escrita en el código como respaldo. Se quitó. MySQL no tiene autenticación integrada de Windows, así que cualquier valor por defecto tendría que incluir una contraseña, y eso no va en un repositorio.

Ahora, si falta `ConnectionStrings:Sgcp`, la API **se detiene al arrancar** y dice el formato esperado, igual que ya hacía con `Jwt:Clave`. Es más claro que intentar conectarse a un servidor inventado y fallar con un error de red.

#### Y eso rompió GitHub Actions, por una distinción que al principio se pasó por alto

La primera versión aplicaba esa exigencia también a `FabricaContexto`, que es la fábrica **de diseño**: la que usa `dotnet ef`. El flujo de CI falló en el paso «Revisar migraciones» con:

```
Unable to create a 'DbContext' of type 'SgcpContext'. The exception
'Configura ConnectionStrings:Sgcp mediante user-secrets o variable de entorno...'
was thrown while attempting to create an instance.
```

**La causa.** Las órdenes de `dotnet ef` no son todas iguales. `migrations add`, `migrations script` y `has-pending-model-changes` solo **construyen el modelo**: no abren ninguna conexión. La única que se conecta de verdad es `database update`. Exigirles credenciales a las tres primeras es pedir algo que no necesitan, y en CI no hay ni `user-secrets` ni ninguna base todavía.

No se vio antes porque durante el desarrollo se exportaba `ConnectionStrings__Sgcp` a mano en cada orden. El entorno de prueba tenía la variable; el de CI, no. **Es el mismo error de fondo que los dos defectos de cultura**: probar en un entorno que no es el de ejecución.

**La corrección.** Dos métodos en `Comun/CadenaConexion.cs`, uno por cada uso:

| Método | Quién lo usa | Qué hace si falta la cadena |
|---|---|---|
| `Exigir` | `Arranque.cs`, la aplicación | lanza y la API no arranca |
| `ParaDisenio` | `FabricaContexto`, `dotnet ef` | avisa por la salida de error y devuelve un marcador que nunca se conecta |

Así, generar y revisar migraciones funciona en cualquier máquina sin configurar nada, y la aplicación sigue negándose a arrancar sin una cadena real.

**Regla para adelante.** Un `IDesignTimeDbContextFactory` no debe exigir credenciales: corre en máquinas de desarrollo y en CI, donde no hay secretos. Y cuando un paso de CI falla, hay que reproducirlo con el mismo entorno que CI —en este caso, `env -u ConnectionStrings__Sgcp` y `--configuration Release --no-build`— antes de cambiar nada. Los cuatro pasos del flujo se volvieron a ejecutar así, uno por uno, y pasan.

## 3. Trampa 1 · MySQL no tiene índices filtrados

Es el único cambio de modelado que hizo falta, y el que hay que entender para no romperlo después.

En SQL Server había tres índices únicos **con `WHERE`**, que hacían que la unicidad valiera solo para algunas filas. MySQL no soporta eso. La solución que se aplicó son **columnas generadas**: columnas calculadas por la base, que valen `NULL` cuando la fila no participa de la regla, con un índice único encima. Y como MySQL considera **distintos** entre sí a los `NULL` de un índice único, las filas que no participan nunca chocan.

| Regla del negocio | Antes, en SQL Server | Ahora, en MySQL |
|---|---|---|
| Un producto tiene una sola vigencia de precio abierta | índice único en `ProductoId` con `WHERE VigenteHasta IS NULL` | columna `ProductoConVigenciaAbierta` = `ProductoId` si la vigencia está abierta, `NULL` si está cerrada, con índice único |
| El NIT no se repite entre clientes activos que tienen NIT | índice único en `IdentificacionFiscal` con `WHERE Activo = 1 AND IdentificacionFiscal <> ''` | columna `IdentificacionFiscalUnica` = el NIT si el cliente está activo y tiene NIT, `NULL` si no, con índice único |
| Una cotización origina una sola versión nueva | índice único en `CotizacionOrigenId` con `WHERE CotizacionOrigenId IS NOT NULL` | índice único **sin nada más**: en MySQL los `NULL` ya no chocan entre sí |

El tercer caso salió gratis. Los dos primeros son columnas de la base, declaradas con `HasComputedColumnSql` en la configuración Fluent; **no son propiedades de las entidades** y el código de negocio no las ve.

Se comprobaron una por una contra MySQL 8.4, en los dos sentidos:

```
Regla 1  segunda vigencia abierta del mismo producto   -> rechazada, error 1062
         dos vigencias cerradas del mismo producto     -> aceptadas
Regla 2  segundo cliente ACTIVO con el mismo NIT       -> rechazado, error 1062
         cliente INACTIVO con el mismo NIT             -> aceptado
         tres clientes activos sin NIT                 -> aceptados
Regla 3  tres cotizaciones raíz (origen NULL)          -> aceptadas
         segunda versión de la misma cotización origen -> rechazada, error 1062
```

**Regla para el Sprint 2.** Si hace falta otra unicidad parcial, el patrón es este mismo, no un `CHECK` ni una validación solo en el servicio. Y cuidado: una columna generada no admite valor en un `INSERT`, así que los `INSERT` posicionales dejan de funcionar y hay que listar las columnas.

## 4. Trampa 2 · el script `--idempotent` no sirve en MySQL

`dotnet ef migrations script --idempotent` genera, para MySQL, instrucciones envueltas así:

```sql
IF NOT EXISTS(SELECT * FROM `__EFMigrationsHistory` WHERE `MigrationId` = '...')
BEGIN
    CREATE TABLE ...
END;
```

Eso es sintaxis de T-SQL. MySQL solo acepta `IF ... THEN ... END IF` dentro de un procedimiento almacenado, así que el script falla con error 1064 en la primera línea. EF no avisa: genera el archivo sin queja.

Por eso `database/InicialSprint1.sql` es el script **plano**, que sí es MySQL válido, y se aplica una sola vez sobre una base vacía. Para aplicar o reaplicar sin riesgo está `dotnet ef database update`, que consulta `__EFMigrationsHistory` desde el cliente y no necesita envoltura ninguna.

## 5. Trampa 3 · los errores de concurrencia tienen otros números

`ErroresMiddleware` traducía dos errores de SQL Server a una respuesta 409. Los equivalentes de MySQL son otros:

| Situación | SQL Server | MySQL |
|---|---|---|
| Interbloqueo | 1205 | **1213** |
| Espera de bloqueo agotada | 1222 | **1205** |

El 1205 existe en los dos motores y **significa cosas distintas**. Copiar los números sin mirar deja el interbloqueo sin tratar, devolviendo 500 en vez de 409.

## 6. Lo que ya no es un problema

Mientras el motor fue SQL Server, la preocupación principal era el **Msg 1785**, «multiple cascade paths»: SQL Server se niega a crear dos caminos en cascada hacia la misma tabla y aborta la migración entera. Buena parte del método de verificación existía para descartarlo sin tener el servidor.

MySQL permite varios caminos en cascada, así que ese riesgo desapareció. Las reglas `Restrict` del modelo **se dejaron tal cual**: están para conservar el histórico comercial —que no se borre un cliente con pedidos, que no se borre una cotización con pedido— y esa razón no tenía nada que ver con el motor.

## 7. Diferencias de tipos, para que nadie se sorprenda

| En el modelo | SQL Server | MySQL |
|---|---|---|
| `Guid` | `uniqueidentifier` | `char(36)` |
| `string` con `HasMaxLength(n)` | `nvarchar(n)` | `varchar(n)` en `utf8mb4` |
| `DateTime` | `datetime2` | `datetime(6)` |
| `bool` | `bit` | `tinyint(1)` |
| `decimal` con `HasPrecision(p,s)` | `decimal(p,s)` | `decimal(p,s)` |

Dos consecuencias prácticas. La primera: en `utf8mb4` cada carácter ocupa hasta 4 bytes, y la clave de un índice de InnoDB no puede pasar de 3072 bytes, así que una columna indexada no debe declararse más larga que `varchar(768)`. Las columnas indexadas del SGCP son todas cortas —la mayor es `varchar(80)`—, pero conviene tenerlo presente al agregar campos. La segunda: la intercalación por defecto de MySQL 8 no distingue mayúsculas, así que las comparaciones de texto son insensibles a ellas, igual que ocurría en SQL Server con la intercalación habitual.

## 8. Qué quedó verificado

Todo con `LANG=es_BO.UTF-8`, contra MySQL 8.4 en un contenedor desechable, en el puerto 3307 para no tocar ninguna otra instancia:

| Qué | Resultado |
|---|---|
| Compilación de SGCPapi y SGCPuiweb | 0 errores, 0 advertencias |
| Los cuatro pasos de `.github/workflows/sprint1-mysql.yml`, en Release y sin `ConnectionStrings__Sgcp` | pasan |
| `dotnet ef database update` contra MySQL real | aplicada |
| La misma orden por segunda vez | «already up to date», sin cambios |
| `dotnet ef migrations has-pending-model-changes` | modelo y migración sincronizados |
| Las tres reglas de unicidad, en los dos sentidos | 7 de 7 |
| Recorrido completo de la API por HTTP | **27 de 27** |
| El mismo recorrido por la vía SQLite | 27 de 27 |
| Páginas de la web y envío del formulario de precios | **9 de 9** |
| Importes decimales guardados en MySQL | `55.25` y `77.50` exactos en `decimal(12,2)` |

Sigue pendiente, y no se puede cerrar sin un teléfono y sin usuarios: instalar el APK en un dispositivo, y medir RNF-02 y RNF-04.
