# Levantar el SGCP en local con Docker

Camino corto para dejar el sistema funcionando en tu máquina usando un contenedor para la base de datos. Complementa a [Como_ejecutar_el_sistema.md](Como_ejecutar_el_sistema.md), que explica el camino con MySQL instalado a mano y el detalle de Android.

**Solo la base de datos va en contenedor.** La API y la web se ejecutan con el SDK de .NET, porque los repositorios no tienen `Dockerfile`: construir imágenes obligaría a bajar más de un giga de imágenes del SDK para no ganar nada en una máquina de desarrollo.

## Lo que hace falta

| Pieza | Versión | Comprobación |
|---|---|---|
| Docker | cualquiera reciente | `docker --version` |
| SDK de .NET | 10.x | `dotnet --version` responde `10.x` |

MySQL no hace falta instalarlo: lo trae la imagen.

## 1. Antes de crear el contenedor: elegir el puerto

Si en tu máquina ya hay otro MySQL corriendo, el puerto 3306 está ocupado y el contenedor no va a arrancar. Revisá primero:

```bash
docker ps
ss -ltnp | grep 3306
```

Si 3306 está tomado, usá **3307** hacia afuera. El contenedor sigue escuchando en 3306 por dentro; lo único que cambia es el puerto del lado de tu máquina, y por lo tanto el `Port=` de la cadena de conexión.

> **No borres contenedores ni volúmenes que no sean de este proyecto.** Los de este proyecto son exactamente dos: el contenedor `sgcp_mysql` y el volumen `sgcp_mysql_data`. Cualquier otro nombre que aparezca en `docker ps -a` o `docker volume ls` pertenece a otra cosa.

## 2. Crear el contenedor

El volumen se crea aparte para que los datos sobrevivan si el contenedor se borra:

```bash
docker volume create sgcp_mysql_data

docker run -d \
  --name sgcp_mysql \
  --restart unless-stopped \
  -p 127.0.0.1:3307:3306 \
  -e MYSQL_ROOT_PASSWORD=TU_CLAVE_ROOT \
  -e MYSQL_DATABASE=sgcp \
  -e MYSQL_USER=sgcp \
  -e MYSQL_PASSWORD=TU_CLAVE \
  -v sgcp_mysql_data:/var/lib/mysql \
  mysql:8.4 \
  --innodb-buffer-pool-size=96M \
  --performance-schema=OFF \
  --max-connections=50
```

Qué hace cada parte, porque conviene entenderla antes de copiarla:

| Opción | Para qué |
|---|---|
| `-p 127.0.0.1:3307:3306` | Publica el puerto **solo hacia tu máquina**. Sin el `127.0.0.1` quedaría abierto a toda la red |
| `--restart unless-stopped` | Vuelve a levantarse si reiniciás la laptop, hasta que lo pares vos |
| `-v sgcp_mysql_data:/var/lib/mysql` | Los datos viven en el volumen, no en el contenedor |
| `MYSQL_DATABASE=sgcp` | Crea la base vacía al primer arranque. Las tablas las crea la migración, no esto |
| `MYSQL_USER` / `MYSQL_PASSWORD` | Crea el usuario de la aplicación como `'sgcp'@'%'` |
| `--innodb-buffer-pool-size=96M` | Baja el consumo. Con los valores por omisión el contenedor pide bastante más memoria |
| `--performance-schema=OFF` | Apaga instrumentación que en desarrollo no se usa |

La primera vez tarda entre veinte y cuarenta segundos en quedar usable. Para saber cuándo está listo:

```bash
docker exec sgcp_mysql mysql -usgcp -pTU_CLAVE -e "SELECT VERSION();" sgcp
```

Mientras siga dando `Can't connect` o `Access denied`, todavía está inicializando. Si pasa un minuto y no responde, mirá `docker logs sgcp_mysql`.

## 3. Configurar los tres valores sensibles

No están en el repositorio a propósito, y la API se niega a arrancar sin ellos. Se guardan en tu perfil de usuario, fuera del repositorio, así que nunca se suben a GitHub:

```bash
cd SGCPapi/src/SGCP.Api

dotnet user-secrets set "ConnectionStrings:Sgcp" "Server=127.0.0.1;Port=3307;Database=sgcp;User ID=sgcp;Password=TU_CLAVE;SslMode=Preferred"
dotnet user-secrets set "Jwt:Clave" "una-cadena-aleatoria-de-al-menos-32-caracteres"
dotnet user-secrets set "DatosIniciales:ClaveAdministrador" "TuClaveInicial2026"
```

El `Port=3307` tiene que coincidir con el puerto que publicaste en el paso 2. Es el error más común de este camino.

Opcional, para que el catálogo arranque con cortes y derivados de ejemplo en vez de vacío:

```bash
dotnet user-secrets set "DatosIniciales:Ejemplos" "true"
```

Para ver qué quedó configurado, sin mostrar los valores: `dotnet user-secrets list`.

## 4. Crear el esquema

Desde la raíz de `SGCPapi`:

```bash
dotnet tool restore
dotnet ef database update --project src/SGCP.Api
```

Tienen que aplicarse las cinco migraciones en orden. Para comprobar que quedó completo:

```bash
dotnet ef migrations has-pending-model-changes --project src/SGCP.Api
docker exec sgcp_mysql mysql -usgcp -pTU_CLAVE -N \
  -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='sgcp';" sgcp
```

La primera orden tiene que responder que no hay cambios en el modelo. La segunda devuelve **42** tablas con las migraciones de los sprints 1 a 4 aplicadas.

## 5. Levantar la API y la web

La API primero, siempre: la web no arranca contra nada.

```bash
# terminal 1, en SGCPapi
dotnet run --project src/SGCP.Api

# terminal 2, en SGCPuiweb
dotnet run --project src/SGCP.Web
```

| Servicio | Dirección |
|---|---|
| API | `http://localhost:5081` |
| Swagger | `http://localhost:5081/swagger` |
| Web | `http://localhost:5080`, se entra con `admin` y la clave del paso 3 |

La primera ejecución de la API siembra permisos, responsabilidades y la cuenta `admin`. Es idempotente: podés arrancar las veces que quieras sin duplicar nada.

### Variante que gasta menos memoria

`dotnet run` deja vivo un proceso de compilación además de la aplicación, unos 150 MB por cada proyecto. Si la máquina tiene 4 GB o menos, compilá una vez y ejecutá el binario:

```bash
# una sola vez
dotnet build src/SGCP.Api
dotnet build src/SGCP.Web

# cada vez que quieras levantarlo
cd SGCPapi/src/SGCP.Api
ASPNETCORE_ENVIRONMENT=Development ASPNETCORE_URLS=http://127.0.0.1:5081 \
  dotnet bin/Debug/net10.0/SGCP.Api.dll

cd SGCPuiweb/src/SGCP.Web
ASPNETCORE_ENVIRONMENT=Development ASPNETCORE_URLS=http://127.0.0.1:5080 \
  Api__UrlBase=http://127.0.0.1:5081/api/v1/ dotnet bin/Debug/net10.0/SGCP.Web.dll
```

Hay que ejecutarlo desde la carpeta del proyecto, no desde la del binario: la raíz de contenido es el directorio actual, y de ahí salen las vistas y los archivos estáticos.

## 6. Comprobar que quedó bien

Dos niveles. El primero es el recorrido de la demostración, que está paso a paso en la [sección 5 de Como_ejecutar_el_sistema.md](Como_ejecutar_el_sistema.md): crear clasificación, producto, costo y precio, cliente, cotización, y comprobar que el pedido se niega si la cotización no está aceptada, que el margen queda en Bs 28 y que no se recalcula al cambiar el precio.

El segundo es la verificación automática del repositorio, que aplica las migraciones en una base aislada y recorre la API por HTTP:

```bash
cd SGCPapi
SGCP_MYSQL_TEST="Server=127.0.0.1;Port=3307;User ID=root;Password=TU_CLAVE_ROOT;SslMode=Preferred" \
  dotnet run --project tests/SGCP.Verificacion
```

Usa `root` porque necesita crear bases. Se crea una propia con nombre `sgcp_pruebas_<identificador>`, la usa y la borra al terminar: **no toca la base `sgcp`**. Al final informa 27 comprobaciones del Sprint 1 y 89 de los sprints 2 a 4.

Conviene correrla también con `LANG=C` delante. Hubo un defecto de configuración regional que multiplicaba los importes por cien, y esa es la prueba que lo detecta.

### La comprobación corta, antes de una demostración

El recorrido de aceptación del sprint también está automatizado, contra la API ya levantada y sobre la base que vas a mostrar:

```bash
cd SGCPapi
SGCP_CLAVE_ADMIN='la-clave-del-paso-3' python3 scripts/Verificar-Sprint1.py
```

Tarda segundos y termina en `14 correctas, 0 fallas`. Comprueba lo mismo que mirarías a mano: que el pedido se niega con `409 COTIZACION_NO_ACEPTADA` si la cotización solo está presentada, que al aceptarla el pedido queda con costo Bs 112,00 y margen Bs 28,00, que una vigencia posterior de Bs 40 no recalcula ese margen, y que sin token la API responde 401.

Devuelve `0` si todo pasa y `1` si algo falla, así que sirve igual desde otro script. Necesita Python 3.8 o posterior, sin paquetes externos. Como crea registros de prueba, si querés mostrar la base vacía corré después el paso 8.

## 7. Operación de todos los días

| Qué querés | Orden |
|---|---|
| Ver si está corriendo | `docker ps --filter name=sgcp_mysql` |
| Parar la base | `docker stop sgcp_mysql` |
| Volver a levantarla | `docker start sgcp_mysql` |
| Ver sus registros | `docker logs --tail 50 sgcp_mysql` |
| Entrar al cliente de MySQL | `docker exec -it sgcp_mysql mysql -usgcp -pTU_CLAVE sgcp` |
| Ver cuánta memoria usa | `docker stats sgcp_mysql --no-stream` |

Los datos están en el volumen, así que `stop` y `start` no pierden nada.

## 8. Dejar la base como recién instalada

Útil antes de una presentación, para que no queden datos de prueba a la vista. Parar la API y la web primero:

```bash
docker exec sgcp_mysql mysql -uroot -pTU_CLAVE_ROOT -e \
  "DROP DATABASE IF EXISTS sgcp; CREATE DATABASE sgcp CHARACTER SET utf8mb4; \
   GRANT ALL PRIVILEGES ON \`sgcp\`.* TO 'sgcp'@'%'; FLUSH PRIVILEGES;"

cd SGCPapi
dotnet ef database update --project src/SGCP.Api
```

Al volver a levantar la API se siembra de nuevo el administrador y los permisos. Queda con la cuenta `admin`, los permisos, las clasificaciones y productos de ejemplo si activaste `DatosIniciales:Ejemplos`, y **sin** clientes, cotizaciones ni pedidos: esos se crean en la demostración.

## 9. Quitar todo

```bash
docker rm -f sgcp_mysql
docker volume rm sgcp_mysql_data
```

La segunda orden **borra los datos de forma definitiva**. Para quitar también los valores guardados en tu perfil:

```bash
cd SGCPapi/src/SGCP.Api
dotnet user-secrets clear
```

## 10. Si algo falla

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` al crear el contenedor | Otro servicio usa ese puerto. Cambiá `-p 127.0.0.1:3308:3306` y ajustá el `Port=` de la cadena de conexión |
| El contenedor aparece `Exited` enseguida | `docker logs sgcp_mysql`. Casi siempre es que faltó `MYSQL_ROOT_PASSWORD`, o que el volumen traía datos de una contraseña anterior |
| `Access denied for user 'sgcp'` | La contraseña del paso 3 no coincide con la del paso 2. Si cambiaste `MYSQL_PASSWORD` después del primer arranque, no sirvió de nada: esa variable solo se aplica cuando el volumen está vacío |
| `Unknown database 'sgcp'` | Se borró el volumen, o `MYSQL_DATABASE` no era `sgcp`. La migración crea las tablas, no la base |
| `Unable to connect to any of the specified MySQL hosts` | El contenedor está parado, o el puerto de la cadena no es el que publicaste |
| `Configura ConnectionStrings:Sgcp mediante user-secrets...` | Falta el paso 3. Es intencional: la API se niega a arrancar sin configuración en vez de intentar conectarse a un servidor inventado |
| `Configura Jwt:Clave mediante user-secrets...` | Lo mismo, con la clave de firma |
| `Specified key was too long` al migrar | La imagen es de MariaDB o de un MySQL anterior al 8.0.13. Tiene que ser `mysql:8.4` o similar |
| La web carga pero toda operación da error de conexión | La API no está levantada, o `Api:UrlBase` apunta a otro puerto |
| La web no alcanza a la API aunque las dos estén arriba | Si la API escucha en `127.0.0.1` y la web la busca en `localhost`, puede resolverse por IPv6 y fallar. Usá `127.0.0.1` en las dos puntas |
| Los importes se guardan multiplicados por cien | Configuración regional. Está en `Metodo_de_verificacion.md`, sección 4 |

## 11. Memoria en máquinas de 4 GB

Medido con el sistema completo corriendo: la API ocupa unos 190 MB, la web unos 120 MB y el contenedor de MySQL unos 200 MB, cerca de 510 MB en total. Tres cosas ayudan cuando queda justo:

1. Ejecutar los binarios en vez de `dotnet run`, como está en el paso 5. Ahorra unos 300 MB entre los dos proyectos.
2. Después de compilar queda vivo `VBCSCompiler`, el servidor de compilación, que puede ocupar más de 300 MB. Se puede cerrar sin consecuencias: vuelve a levantarse en la siguiente compilación.
3. Las opciones de memoria del contenedor del paso 2.

## Lo que este camino no cubre

**Android.** El teléfono no puede resolver el `localhost` de la laptop, así que para probar el APK la API tiene que escuchar en la dirección de red:

```bash
ASPNETCORE_URLS=http://0.0.0.0:5081 dotnet bin/Debug/net10.0/SGCP.Api.dll
```

Eso la deja accesible a toda la red local, no solo a tu máquina. Hacelo únicamente mientras lo necesites, en una red de confianza, y volvé a `127.0.0.1` cuando termines. La dirección que se carga en la pantalla de acceso del APK se averigua con `ip addr` en Linux o `ipconfig` en Windows, y los dos equipos tienen que estar en el mismo wifi. El detalle está en la sección 4 de [Como_ejecutar_el_sistema.md](Como_ejecutar_el_sistema.md).
