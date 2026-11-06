# Cómo ejecutar el SGCP

Guía para que cualquiera del equipo levante el sistema completo en su propia máquina. El orden importa: **la API primero**, porque la web y Android no arrancan contra nada.

Cada repositorio tiene su propio README con el detalle. Esto es el camino corto de principio a fin.

## Lo que hace falta antes de empezar

| Pieza | Qué se necesita |
|---|---|
| SGCPapi | SDK de .NET 10 y una instancia de MySQL 8.0.13 o posterior |
| SGCPuiweb | SDK de .NET 10 y la API ya corriendo |
| SGCPuimovil | Android Studio con JDK 21, o el APK ya compilado |

Comprobación rápida de .NET:

```bash
dotnet --version
```

Tiene que responder `10.x`. Si responde otra cosa, la compilación va a fallar con mensajes que no dicen nada útil.

## 1. MySQL

La API usa MySQL y nada más. No hay modo SQLite en la aplicación: SQLite existe únicamente dentro del proyecto de pruebas.

Hace falta **MySQL 8.0.13 o posterior**. MariaDB no sirve, por dos razones concretas: el proveedor que usa la API es el oficial de Oracle, y el esquema usa columnas generadas de MySQL 8 para tres reglas de unicidad.

Cualquiera de estas tres opciones sirve:

- **MySQL Community Server** en Windows, con el instalador oficial. Durante la instalación elegí "Development Computer" y anotá la contraseña de `root`.
- **Un contenedor**, si ya usás Docker. Una línea:

  ```bash
  docker run -d --name sgcp_mysql -p 127.0.0.1:3306:3306 \
    -e MYSQL_ROOT_PASSWORD=TU_CLAVE -e MYSQL_DATABASE=sgcp \
    -e MYSQL_USER=sgcp -e MYSQL_PASSWORD=TU_CLAVE mysql:8.4
  ```

- **La instancia de un compañero**, si está en la misma red. Hay que abrir el puerto 3306 solo para la red local, nunca hacia internet, y crear el usuario con `'sgcp'@'%'` en lugar de `'sgcp'@'localhost'`.

Si instalaste MySQL a mano, creá la base y el usuario una vez:

```sql
CREATE DATABASE sgcp CHARACTER SET utf8mb4;
CREATE USER 'sgcp'@'localhost' IDENTIFIED BY 'TU_CLAVE';
GRANT ALL PRIVILEGES ON `sgcp`.* TO 'sgcp'@'localhost';
```

Las tablas no se crean a mano: las crea la migración, en el paso siguiente.

## 2. Levantar la API

```bash
cd SGCPapi
dotnet restore
dotnet tool restore
```

Los tres valores sensibles **no están en el repositorio** y hay que configurarlos una vez por máquina. En PowerShell 7 el script los pide sin mostrarlos en pantalla:

```powershell
./scripts/Preparar-Desarrollo.ps1
```

Si preferís hacerlo a mano, o no usás PowerShell 7:

```bash
cd src/SGCP.Api
dotnet user-secrets set "ConnectionStrings:Sgcp" "Server=localhost;Port=3306;Database=sgcp;User ID=sgcp;Password=TU_CLAVE;SslMode=Preferred"
dotnet user-secrets set "Jwt:Clave" "una-cadena-aleatoria-de-al-menos-32-caracteres"
dotnet user-secrets set "DatosIniciales:ClaveAdministrador" "TuClaveInicial2026"
cd ../..
```

`dotnet user-secrets` guarda los valores fuera del repositorio, en tu perfil de usuario. Por eso cada integrante los configura en su máquina y nunca se suben a GitHub. La cadena de conexión de `appsettings.json` está vacía a propósito: si no la configurás, la API se detiene al arrancar y te dice el formato exacto, en vez de intentar conectarse a un servidor que no existe.

Crear el esquema y arrancar:

```bash
dotnet ef database update --project src/SGCP.Api
dotnet run --project src/SGCP.Api
```

Queda escuchando en `http://localhost:5081`. Swagger está en `http://localhost:5081/swagger` y sirve para probar la API sin la web.

La primera ejecución siembra permisos, responsabilidades y la cuenta `admin` con la contraseña que configuraste. Es idempotente: podés arrancar las veces que quieras sin duplicar nada. **No** siembra precios, cotizaciones ni pedidos; esos se crean en la demostración.

Si querés que el catálogo arranque con cortes y derivados de ejemplo:

```bash
dotnet user-secrets set "DatosIniciales:Ejemplos" "true" --project src/SGCP.Api
```

## 3. Levantar la web

En **otra terminal**, dejando la API corriendo:

```bash
cd SGCPuiweb
dotnet restore
dotnet run --project src/SGCP.Web
```

Queda en `http://localhost:5080`. Se entra con `admin` y la contraseña que configuraste en el paso anterior.

La web no toca la base de datos: todo lo pide a la API. Si la API no está levantada, las pantallas cargan pero cualquier operación devuelve un error de conexión. Eso no es un defecto de la web.

La dirección de la API está en `src/SGCP.Web/appsettings.json`, clave `Api:UrlBase`. Solo hay que cambiarla si corrés la API en otro puerto o en otra máquina:

```json
{ "Api": { "UrlBase": "http://localhost:5081/api/v1/" } }
```

Para no editar el archivo del repositorio, se puede pasar por variable de entorno:

```bash
Api__UrlBase=http://192.168.1.50:5081/api/v1/ dotnet run --project src/SGCP.Web
```

## 4. Android

Lo más rápido para la presentación es instalar el APK ya compilado:

```
SGCPuimovil/app/build/outputs/apk/debug/app-debug.apk
```

Se copia al teléfono y se instala permitiendo orígenes desconocidos. En la pantalla de acceso hay un campo para la dirección de la API, que tiene que ser la **IP de red** de la máquina donde corre, no `localhost`: el teléfono no puede resolver el `localhost` de la laptop. Se averigua con `ipconfig` en Windows o `ip addr` en Linux, y ambos tienen que estar en el mismo wifi.

Para compilarlo de nuevo:

```bash
cd SGCPuimovil
./gradlew assembleDebug
```

Hace falta `local.properties` con la ruta del SDK de Android, que es propia de cada máquina y por eso no está en el repositorio:

```
sdk.dir=C:\\Users\\TuUsuario\\AppData\\Local\\Android\\Sdk
```

## 5. Comprobar que todo quedó bien

Este recorrido es la demostración del sprint. Si sale completo, está funcionando:

1. Entrar a la web con `admin`.
2. Crear una clasificación `Costilla`, familia `Carne fresca`.
3. Crear el producto `Costilla de cerdo`, unidad `kg`. **Queda sin stock**: no existe inventario en este sprint.
4. En Gestión de costos, registrar costo `28.00` y precio `35.00`.
5. Crear un cliente.
6. Crear una cotización con 4 kg de costilla a Bs 35 y presentarla.
7. Intentar crear el pedido: **tiene que negarse**, porque la cotización está presentada y no aceptada.
8. Aceptarla y confirmar el pedido. El margen tiene que mostrar `4 kg × (Bs 35 − Bs 28) = Bs 28`.
9. Registrar una vigencia nueva de Bs 40 y volver al pedido: **el margen sigue en Bs 28**.

Los pasos 7, 8 y 9 son los que el docente va a mirar, porque son los que están escritos como criterio de validación del Sprint 1 en el Excel de planificación.

## Si algo falla

| Síntoma | Causa y solución |
|---|---|
| `Configura Jwt:Clave mediante user-secrets...` al arrancar | Falta el secreto. Es intencional: la API se niega a arrancar sin clave de firma en vez de usar una insegura. Volvé al paso 2 |
| `Configura ConnectionStrings:Sgcp mediante user-secrets...` | Falta la cadena de conexión. Es intencional, por la misma razón que `Jwt:Clave`. Volvé al paso 2 |
| `Unable to connect to any of the specified MySQL hosts` | El servidor no está corriendo, o el puerto no es 3306. En Windows verificá el servicio `MySQL84`; con Docker, `docker ps` |
| `Access denied for user 'sgcp'@'localhost'` | La contraseña no coincide, o el usuario se creó como `'sgcp'@'%'` y te conectás como `localhost`. Revisá con `SELECT user, host FROM mysql.user;` |
| `Unknown database 'sgcp'` | Falta `CREATE DATABASE sgcp;`. La migración crea las tablas, no la base |
| `Specified key was too long` al migrar | El servidor es MariaDB, o un MySQL anterior a 8.0.13. Hace falta MySQL 8 |
| `dotnet ef` no se reconoce | Falta `dotnet tool restore` en la raíz del repositorio |
| La web carga pero todo da error de conexión | La API no está levantada, o `Api:UrlBase` apunta a otro puerto |
| El teléfono no conecta | Pusiste `localhost` en vez de la IP de red, o el firewall de Windows bloquea el puerto. Los dos tienen que estar en el mismo wifi |
| Los importes se guardan multiplicados por cien | Esto estaba roto y se corrigió. Si vuelve a pasar, leé `Metodo_de_verificacion.md`, sección 4: es la configuración regional |

## Qué no hay que esperar de este sprint

Inventario, existencias, reservas, producción, pesajes, control sanitario, control de frío, pagos, crédito, transporte, entregas, reportes y exportación a PDF o Excel **no están implementados**, y es correcto que no lo estén: corresponden a los sprints 2, 3 y 4 según la planificación. En la barra lateral aparecen deshabilitados a propósito, para que se vea el avance y lo que falta.
