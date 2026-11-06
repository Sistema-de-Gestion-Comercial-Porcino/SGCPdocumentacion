# SGCP · Guía de implementación del Sprint 1

**Sistema de Gestión Comercial Porcino — CRM para una chanchería de Santa Cruz de la Sierra**

Universidad del Valle · Ingeniería de Software · Docente: Rolando Lara Sánchez

Equipo: Dario Haziel Tambo Parra · Angel Sebastian Eguez Mur · Sofia Cuellar Roca · Victor Manuel Manrique Arancivia

Versión 2.0 · 5 de noviembre de 2026 · alcance tomado de `Formato Proyecto - SGCC Actualizado.xlsx`

---

> **Implementación del 6 de noviembre de 2026.** El docente autorizó cualquier motor y el equipo eligió **MySQL 8**, con el proveedor oficial de Oracle `MySql.EntityFrameworkCore`. Las instrucciones SQLite y SQL Server de esta guía quedan sustituidas por los README de SGCPapi, SGCPuiweb y SGCPuimovil, y por `00_Definicion/Cambio_a_MySQL.md`, que explica qué se cambió y las tres trampas de MySQL. SQLite solo existe en el proyecto aislado de pruebas. No hay datos de producción ni credenciales en los repositorios. El modelo se alineó con códigos, motivo de rechazo/cancelación e historial de versiones. Las correcciones detalladas están en `00_Definicion/Revision_Sprint1.md`; el estado real de verificación está en `00_Definicion/Estado_Sprint1.md`. El Word y PDF anteriores de esta guía todavía no incorporan esta actualización.

## 0. Cómo usar esta guía

Este documento es la orden de trabajo para generar el código del Sprint 1. Está escrito para que se ejecute **al pie de la letra**: cada nombre de clase, de enumeración, de carpeta y de endpoint que aparece aquí ya existe en los modelos UML entregados al docente, y el código tiene que coincidir con ellos.

Tres reglas antes de empezar:

1. **No inventar entidades, atributos ni estados.** Si algo no está en este documento, no se agrega. El modelo de clases tiene 41 clases y 31 enumeraciones ya aprobadas; el Sprint 1 usa un subconjunto. La única excepción está marcada como tal en la sección 5.3, y hay que reflejarla en el modelo antes de entregar.
2. **No ampliar el alcance.** Lo que está en la sección 4 es todo. Producción, inventario, pagos, transporte y reportes operativos son sprints siguientes. Cotizaciones y pedidos sí pertenecen al Sprint 1.
3. **Si una regla de este documento choca con una decisión técnica cómoda, gana la regla.** El proyecto se evalúa contra sus propios modelos.

El alcance del Sprint 1 **no es una propuesta de este documento**: está copiado del Excel de planificación del equipo, `Formato Proyecto - SGCC Actualizado.xlsx`, hojas *Perfil* y *Requerimientos*. La sección 4 lo transcribe con sus parámetros de aceptación. Si algo de esta guía contradijera ese Excel, manda el Excel.

Hay una copia de esta guía en Markdown junto al PDF. Para leerla desde una herramienta de generación de código conviene usar el `.md`.

---

## 1. Qué es el sistema

La chanchería compra cerdos vivos o faenados, los convierte en cortes y derivados, y los vende a chicharronerías, restaurantes, carnicerías y consumidor final. Hoy el pedido llega por WhatsApp, lo despachado se anota en un cuaderno por orden de llegada y la deuda vive en la memoria del dueño.

El SGCP reemplaza esos tres soportes. Son **tres repositorios en una sola organización de GitHub**:

| Repositorio | Qué es | Tecnología |
|---|---|---|
| **SGCPapi** | API REST. Única dueña de las reglas, la autorización, las transacciones y la base de datos | ASP.NET Core Web API |
| **SGCPuiweb** | Web responsiva de gestión y portal del comprador | ASP.NET Core MVC |
| **SGCPuimovil** | App de reparto, captura de recepciones sin señal | Android nativo, Kotlin |

**Los dos clientes consumen la misma API y ninguno toca la base de datos directamente.** Tres repositorios no significan microservicios: SGCPapi es una sola aplicación.

### Los seis actores humanos

Propietario / administración · Ventas / cobranza · Producción · Almacén · Responsable de entrega · Comprador.

Todos se autentican. Una persona puede ejercer varias responsabilidades. El comprador se registra solo y no obtiene permisos internos. **La balanza no es un actor ni una integración**: Almacén teclea los pesajes a mano. El proveedor fiscal es una integración externa condicional que todavía no está habilitada.

---

## 2. Reglas del negocio que el código debe respetar

Estas reglas vienen del documento de reglas vigentes y del diccionario de clases. Las que aplican al Sprint 1 están marcadas; las demás se listan para que nada del Sprint 1 las contradiga.

### Aplican al Sprint 1

1. **Crear un producto no crea existencia.** El catálogo define qué es cada corte o derivado; el stock es otra cosa y llega en el Sprint 2.
2. **No se borra: se desactiva.** Cliente, Producto, ClasificacionProducto, Transporte y Usuario tienen `activo` o `estado`. Desactivar conserva la historia y exige revisar dependencias. Nunca `DELETE` físico de una fila usada.
3. **No se puede dejar el sistema sin administrador habilitado.** Desactivar el último usuario con rol de administración se rechaza.
4. **`ClasificacionProducto` identifica familia y tipo**; `Producto` añade código, nombre, presentación, unidad y estado. Ejemplo: familia `CARNE_FRESCA` / nombre `Costilla`, y el producto `Costilla de cerdo`, presentación `Pieza`, unidad `kg`.
5. **Precio y costo tienen vigencia.** Una nueva vigencia **no** recalcula el precio ni el costo conservados en pedidos ya confirmados. Al abrir una vigencia nueva se cierra la anterior con `vigenteHasta`.
6. **Cliente y Usuario son cosas distintas.** Un cliente atendido en el local no necesita cuenta. Un comprador registrado sí tiene `Usuario`, y puede además estar vinculado a un `Cliente`.
7. **Toda operación relevante deja traza**: usuario, fecha, entidad y referencia (`RegistroAuditoria`). Las anulaciones conservan historial.
8. **Los permisos limitan acciones y datos.** El comprador solo ve lo suyo.
9. **Código de producto único.** Código de clasificación único. Login de usuario único.
10. **Una cotización vigente debe aceptarse antes de que exista pedido.** Rechazada o vencida no genera nada: ni pedido, ni reserva, ni cobro. Cambiar lo cotizado exige una versión nueva y una aceptación nueva.
11. **El pedido confirmado congela precio y costo.** Lo que se guarda en el detalle del pedido es lo acordado ese día. Una vigencia posterior no lo recalcula, y por lo tanto tampoco recalcula el margen.
12. **El margen estimado no es utilidad real.** Es `Σ cantidad × (precio acordado − costo de referencia acordado)` y nada más. El servicio de faeneo se cobra aparte, y eso llega en el Sprint 2.

### No aplican al Sprint 1, pero no se deben contradecir

- `Disponible = físico apto − reservas activas`. La confirmación de producción **no** es una entrada de stock.
- `Neto = bruto − tara`, con unidad compatible.
- Entrega y deuda son independientes: confirmar una recepción no salda nada.
- Seña solo con dinero realmente recibido.
- Solo la recepción de entregas asignadas, autorizadas y descargadas admite captura sin conexión, y únicamente en Android.
- RF-09, RF-16 y RF-21 están fuera de alcance. RF-11 (fiscal) depende de proveedor confirmado.

---

## 3. Decisiones técnicas

### Ya decididas

| Punto | Decisión |
|---|---|
| Plataforma API | ASP.NET Core 10, Web API con **controladores** (no minimal APIs) |
| ORM | Entity Framework Core 10, configuración con **Fluent API** en clases `IEntityTypeConfiguration<T>` |
| Identificadores | `Guid` en todas las entidades, porque el diccionario dice `UUID` |
| Autenticación | JWT Bearer emitido por la API |
| Documentación de la API | Swagger / OpenAPI, habilitado en desarrollo |
| Plataforma web | ASP.NET Core 10 **MVC** |
| Acceso a datos desde la web | **Ninguno.** La web no referencia EF Core ni conoce la cadena de conexión. Solo `HttpClient` tipado contra la API |
| Sesión en la web | Autenticación por cookie; el JWT viaja dentro de la cookie y se adjunta a cada llamada |
| Idioma del código | Clases, propiedades y endpoints en **español**, igual que el diccionario. Las carpetas del framework conservan su nombre (`Controllers`, `Models`, `Views`) |
| Enumeraciones | Se guardan como **texto** en la base (`HasConversion<string>()`), para que las consultas SQL se puedan leer |

### Motor de base de datos

**Resuelto.** El docente autorizó usar cualquier motor y el equipo eligió **MySQL 8**. La cadena de conexión va en `ConnectionStrings:Sgcp`, configurada con `dotnet user-secrets` en cada máquina y **vacía en el repositorio**, para que no haya credenciales versionadas:

```text
Server=localhost;Port=3306;Database=sgcp;User ID=sgcp;Password=TU_CLAVE;SslMode=Preferred
```

Si falta, la API se detiene al arrancar indicando el formato, en vez de intentar conectarse a un servidor inventado.

El proveedor es `MySql.EntityFrameworkCore`, el oficial de Oracle, y no Pomelo: la última versión estable de Pomelo está hecha para EF Core 9 y adoptarla obligaba a bajar el proyecto de .NET 10 a .NET 9.

```csharp
builder.Services.AddDbContext<SgcpContext>(opciones =>
    opciones.UseMySQL(builder.Configuration.GetConnectionString("Sgcp")));
```

Lo implementado no tiene selector de proveedor: la aplicación referencia **solo MySQL**, y SQLite vive únicamente en el proyecto de pruebas, que elige motor por variable de entorno. Un selector en la aplicación invita a entregar algo probado en un motor y presentado en otro.

Cambiar de motor **no es cambiar una clave**: hay que regenerar las migraciones y revisar lo que el motor nuevo no soporta. En este proyecto fueron tres índices filtrados, que MySQL no tiene; están resueltos con columnas generadas y documentados en `00_Definicion/Cambio_a_MySQL.md`. **Esto hay que decirlo en la presentación**, no esconderlo.

**Ubicación de los ViewModels en la web.** El docente pidió que la carpeta de ViewModels esté dentro de `Views` o dentro de `Models`. Esta guía los coloca en **`Models/ViewModels/`**, que es la convención de ASP.NET Core MVC. Si el docente aclara que los quería en `Views/ViewModels/`, mover la carpeta es cambiar un namespace; no afecta al resto.

---

## 4. Alcance del Sprint 1

El alcance **no se decide en esta guía**. Está fijado en `Formato Proyecto - SGCC Actualizado.xlsx`, hoja *Perfil*, sección V, fila Sprint Nro. 1, y repetido en la hoja *Requerimientos*, sección V, bloque SPRINT 1. Se transcribe tal cual:

> **Producto mínimo viable.** Acceso y registro de comprador; administración de usuarios, clientes, catálogo de cortes/derivados, productos, costos, cotizaciones y pedidos. Datos centrales y base técnica Android. RF01/02/03/10/12/13 y parametrización RF04.
>
> **Criterio de validación.** Todos se autentican; alta pública solo comprador. Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar historial.

### 4.1 Requerimientos comprometidos

| RF | Nombre | Prior. | Parámetro de aceptación, textual del backlog |
|---|---|---|---|
| RF-12 | Gestionar acceso autenticado | Must | Todos se autentican. Registro público solo comprador; recuperación verifica token vigente de un uso. Login/cierre/renovación conservan capturas Android. |
| RF-13 | Administrar usuarios y permisos | Must | Administrar usuarios con permisos auditados. Desactivar revoca sesiones, conserva historial y mantiene al menos un administrador habilitado. |
| RF-10 | Gestionar clientes | Must | Crear, buscar, editar y desactivar conservando historial. Pedidos o deuda pendiente impiden desactivación sin resolución. Cliente presencial no requiere cuenta. |
| RF-02 | Administrar costos y precios vigentes | Must | Propietario registra costo de referencia y precio por unidad; cambio de catálogo no altera pedidos históricos. |
| RF-01 | Registrar solicitud, cotización y pedido | Must | Una cotización rechazada o vencida no crea pedido; una aceptada vigente permite confirmarlo. |
| RF-03 | Calcular margen estimado por pedido | Must | 4 kg × (Bs 35 − Bs 28) = Bs 28 de margen estimado de productos. No se informa como utilidad real por animal. |
| RF-04 | Catálogo, producción, inventario y pesajes | Should | **Solo la parametrización**: clasificaciones y productos con código, presentación, unidad y estado. Crear producto no crea stock. Producción, inventario y pesajes son del Sprint 2. |
| RNF-02 | Eficiencia de desempeño | Must | Medición comparativa se acuerda y no supera la anotación manual comparable. |
| RNF-04 | Usabilidad | Should | Usuario representativo completa operaciones frecuentes con guion acordado. |

### 4.2 Casos de uso que entran

| CU | Nombre | RF | Sprint 1 |
|---|---|---|---|
| CU01 | Gestionar acceso | RF-12 | **Completo** |
| CU02 | Administrar usuarios | RF-13 | **Completo** |
| CU03 | Gestionar clientes | RF-10 | **Completo** |
| CU07 | Gestionar productos | RF-04 parametrización | **Completo**, sin existencia |
| CU04 | Gestión de costos | RF-02, RF-03 | **Completo** |
| CU05 | Gestión de cotizaciones | RF-01 | **Completo** |
| CU06 | Gestionar pedidos | RF-01, RF-03 | **Confirmar, consultar y cancelar.** Preparación, reservas, incidencias y despacho son de sprints siguientes |
| CU08, CU09 | Producción e inventario | RF-04, RF-17, RF-18, RF-20 | No · Sprint 2 |
| CU10, CU11 | Pagos, cobranza, transporte y entregas | RF-05 a RF-08, RF-19 | No · Sprint 3 |
| CU12 | Reportes, exportación y portal | RF-11, RF-14, RF-15 | No · Sprint 4 |

Tres consecuencias de esta tabla que conviene tener presentes mientras se escribe el código:

- **La exportación a PDF y Excel no es del Sprint 1.** RF-14 y RF-15 son del Sprint 4. Los patrones Factory Method y Adapter se entregan entonces. El patrón del Sprint 1 es **Builder**, que es el que construye el pedido confirmado.
- **`CargoPedido` no se implementa.** Separar el cargo de producto del de servicio es RF-20, Sprint 2. En los mockups w06, w07 y w09 la línea del servicio de faeneo aparece como texto informativo; en el Sprint 1 se deja exactamente así, como texto, sin tabla ni cálculo.
- **El pedido no reserva, no prepara y no cobra.** `EstadoPreparacion` nace en `PENDIENTE` y nadie lo mueve todavía. Reservas son Sprint 2 y pagos Sprint 3.

### 4.3 Pantallas del Sprint 1

Las claves corresponden a los mockups de Balsamiq ya entregados. El diseño debe seguirlos.

| Clave | Pantalla | CU |
|---|---|---|
| w01 | Iniciar sesión | CU01 |
| preg | Crear cuenta de comprador | CU01 |
| pregdone | Cuenta de comprador registrada | CU01 |
| pforgot | Recuperar acceso | CU01 |
| preset | Establecer nueva contraseña | CU01 |
| w02 | Resumen del negocio | — |
| w04 | Usuarios y permisos | CU02 |
| wuser | Crear usuario del personal | CU02 |
| wuseroff | Desactivar usuario | CU02 |
| w03 | Clientes y ficha comercial | CU03 |
| wclient | Nuevo cliente | CU03 |
| wclientblock | Revisar desactivación del cliente | CU03 |
| wcat | Productos: cortes, derivados e insumos | CU07 |
| wprod | Ficha de producto | CU07 |
| wprodoff | Producto desactivado | CU07 |
| wclass | Clasificaciones de productos | CU07 |
| w05 | Gestión de costos y precios | CU04 |
| w06 | Cotización COT-028 · presentada | CU05 |
| w07 | Cotización COT-028 · aceptada | CU05 |
| w08 | Respuesta del cliente · sin pedido | CU05 |
| w09 | Pedido PED-042 | CU06 |
| a01 | Acceder al reparto | CU01, Android |
| a10 | Renovar acceso | CU01, Android |

Las pantallas de listado de cotizaciones y de pedidos no tienen mockup propio: la barra lateral las enlaza y los mockups muestran el detalle. Se construyen con el mismo patrón de listado de w03 y wcat, sin inventar controles nuevos.

---
## 5. SGCPapi

### 5.1 Crear la solución

```bash
cd SGCPapi
dotnet new sln -n SGCPapi
dotnet new webapi -n SGCP.Api -o src/SGCP.Api -f net10.0 --use-controllers
dotnet sln SGCPapi.sln add src/SGCP.Api/SGCP.Api.csproj
cd src/SGCP.Api
dotnet add package MySql.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Swashbuckle.AspNetCore
```

Un solo proyecto. No separar en capas con proyectos distintos: el alcance no lo justifica y complica la entrega.

### 5.2 Estructura de carpetas

```
SGCPapi/
  SGCPapi.sln
  .gitignore
  README.md
  src/SGCP.Api/
    Controllers/
      AutenticacionController.cs
      UsuariosController.cs
      RolesController.cs
      ClientesController.cs
      ClasificacionesController.cs
      ProductosController.cs
      PreciosController.cs
      CotizacionesController.cs
      PedidosController.cs
    Dominio/
      Entidades/
      Enumeraciones/
    Datos/
      SgcpContext.cs
      Configuraciones/
      Migraciones/
      DatosIniciales.cs
    Servicios/
      ServicioAutenticacion.cs
      ServicioUsuarios.cs
      ServicioClientes.cs
      ServicioCatalogo.cs
      ServicioPrecios.cs
      ServicioCotizaciones.cs
      ServicioConfirmarPedido.cs
      ServicioAuditoria.cs
      GeneradorCodigo.cs
    Patrones/
      Comercial/
        PedidoBuilder.cs
    Contratos/
      Peticiones/
      Respuestas/
    Seguridad/
      Permisos.cs
      RequisitoPermiso.cs
      ManejadorPermiso.cs
      GeneradorToken.cs
    Comun/
      ResultadoPaginado.cs
      ErrorRespuesta.cs
      FiltroExcepciones.cs
    Program.cs
    appsettings.json
```

### 5.3 Entidades del Sprint 1

Estas catorce entidades. Los nombres de clase, de propiedad y de enumeración son **exactamente** los del diccionario de clases.

#### Permiso

```csharp
namespace SGCP.Api.Dominio.Entidades;

public class Permiso
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public string Modulo { get; set; } = string.Empty;
    public string Accion { get; set; } = string.Empty;

    public ICollection<Rol> Roles { get; set; } = new List<Rol>();
}
```

#### Rol

```csharp
public class Rol
{
    public Guid Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public bool Activo { get; set; } = true;

    public ICollection<Permiso> Permisos { get; set; } = new List<Permiso>();
    public ICollection<Usuario> Usuarios { get; set; } = new List<Usuario>();
}
```

#### Usuario

```csharp
public class Usuario
{
    public Guid Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Login { get; set; } = string.Empty;
    public string HashClave { get; set; } = string.Empty;
    public EstadoUsuario Estado { get; set; } = EstadoUsuario.ACTIVO;
    public int IntentosFallidos { get; set; }
    public string Correo { get; set; } = string.Empty;
    public string? Telefono { get; set; }
    public DateTime CreadoEn { get; set; }
    public DateTime? UltimoAcceso { get; set; }
    public Guid? ClienteId { get; set; }

    public Cliente? Cliente { get; set; }
    public ICollection<Rol> Roles { get; set; } = new List<Rol>();
    public ICollection<Sesion> Sesiones { get; set; } = new List<Sesion>();
    public ICollection<RecuperacionAcceso> Recuperaciones { get; set; } = new List<RecuperacionAcceso>();
    public ICollection<RegistroAuditoria> Auditorias { get; set; } = new List<RegistroAuditoria>();
}
```

`ClienteId` implementa la asociación `Cliente 0..1 / Usuario 0..*` llamada `cuentaPortal`.

#### Sesion

```csharp
public class Sesion
{
    public Guid Id { get; set; }
    public DateTime Inicio { get; set; }
    public DateTime Expira { get; set; }
    public bool Revocada { get; set; }
    public Guid UsuarioId { get; set; }

    public Usuario Usuario { get; set; } = null!;
}
```

#### RecuperacionAcceso

```csharp
public class RecuperacionAcceso
{
    public Guid Id { get; set; }
    public string TokenHash { get; set; } = string.Empty;
    public DateTime SolicitadoEn { get; set; }
    public DateTime ExpiraEn { get; set; }
    public DateTime? UtilizadoEn { get; set; }
    public bool Invalidado { get; set; }
    public Guid UsuarioId { get; set; }

    public Usuario Usuario { get; set; } = null!;
}
```

#### RegistroAuditoria

```csharp
public class RegistroAuditoria
{
    public Guid Id { get; set; }
    public string Operacion { get; set; } = string.Empty;
    public string Entidad { get; set; } = string.Empty;
    public Guid EntidadId { get; set; }
    public DateTime Fecha { get; set; }
    public Guid UsuarioId { get; set; }

    public Usuario Usuario { get; set; } = null!;
}
```

#### Cliente

```csharp
public class Cliente
{
    public Guid Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Tipo { get; set; } = string.Empty;
    public string Telefono { get; set; } = string.Empty;
    public string Direccion { get; set; } = string.Empty;
    public string IdentificacionFiscal { get; set; } = string.Empty;
    public FormaPago CondicionHabitual { get; set; } = FormaPago.CONTADO;
    public bool Activo { get; set; } = true;
    public DateTime FechaAlta { get; set; }
    public string Observaciones { get; set; } = string.Empty;

    public ICollection<Usuario> CuentasPortal { get; set; } = new List<Usuario>();
}
```

#### ClasificacionProducto

```csharp
public class ClasificacionProducto
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public TipoProducto Familia { get; set; }
    public string Descripcion { get; set; } = string.Empty;
    public bool Activo { get; set; } = true;

    public ICollection<Producto> Productos { get; set; } = new List<Producto>();
}
```

#### Producto

```csharp
public class Producto
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public string Presentacion { get; set; } = string.Empty;
    public string UnidadVenta { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public bool Activo { get; set; } = true;
    public DateTime FechaAlta { get; set; }
    public Guid ClasificacionProductoId { get; set; }

    public ClasificacionProducto ClasificacionProducto { get; set; } = null!;
    public ICollection<PrecioProducto> Precios { get; set; } = new List<PrecioProducto>();
}
```

#### PrecioProducto

```csharp
public class PrecioProducto
{
    public Guid Id { get; set; }
    public decimal CostoReferencia { get; set; }
    public decimal PrecioVenta { get; set; }
    public DateTime VigenteDesde { get; set; }
    public DateTime? VigenteHasta { get; set; }
    public Guid ProductoId { get; set; }

    public Producto Producto { get; set; } = null!;
}
```

#### Cotizacion

```csharp
public class Cotizacion
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public int Version { get; set; } = 1;
    public DateTime Fecha { get; set; }
    public DateTime VigenteHasta { get; set; }
    public CanalSolicitud Canal { get; set; }
    public EstadoCotizacion Estado { get; set; } = EstadoCotizacion.BORRADOR;
    public string MotivoRespuesta { get; set; } = string.Empty;
    public Guid ClienteId { get; set; }
    public Guid? CotizacionOrigenId { get; set; }

    public Cliente Cliente { get; set; } = null!;
    public Cotizacion? CotizacionOrigen { get; set; }
    public Pedido? Pedido { get; set; }
    public ICollection<DetalleCotizacion> Detalles { get; set; } = new List<DetalleCotizacion>();
}
```

`CotizacionOrigen` encadena las versiones: una versión nueva apunta a la anterior y arranca en `BORRADOR` con `Version + 1`. Eso es lo que pide RF-01 cuando dice «cotizaciones versionadas».

#### DetalleCotizacion

```csharp
public class DetalleCotizacion
{
    public Guid Id { get; set; }
    public decimal Cantidad { get; set; }
    public string Unidad { get; set; } = string.Empty;
    public decimal PrecioUnitario { get; set; }
    public decimal Subtotal { get; set; }
    public Guid CotizacionId { get; set; }
    public Guid ProductoId { get; set; }

    public Cotizacion Cotizacion { get; set; } = null!;
    public Producto Producto { get; set; } = null!;
}
```

`Subtotal` se guarda, no se calcula al leer: es `Cantidad × PrecioUnitario` en el momento de registrar el detalle, y queda congelado.

#### Pedido

```csharp
public class Pedido
{
    public Guid Id { get; set; }
    public string Codigo { get; set; } = string.Empty;
    public DateTime Fecha { get; set; }
    public DateTime FechaComprometida { get; set; }
    public EstadoComercial EstadoComercial { get; set; } = EstadoComercial.CONFIRMADO;
    public EstadoPreparacion EstadoPreparacion { get; set; } = EstadoPreparacion.PENDIENTE;
    public FormaPago CondicionPago { get; set; }
    public decimal CostoEstimadoConfirmado { get; set; }
    public decimal MargenEstimadoConfirmado { get; set; }
    public Guid ClienteId { get; set; }
    public Guid CotizacionId { get; set; }

    public Cliente Cliente { get; set; } = null!;
    public Cotizacion Cotizacion { get; set; } = null!;
    public ICollection<DetallePedido> Detalles { get; set; } = new List<DetallePedido>();
}
```

#### DetallePedido

```csharp
public class DetallePedido
{
    public Guid Id { get; set; }
    public decimal CantidadSolicitada { get; set; }
    public decimal CantidadConfirmada { get; set; }
    public string Unidad { get; set; } = string.Empty;
    public decimal PrecioAcordado { get; set; }
    public decimal CostoReferenciaAcordado { get; set; }
    public EstadoDetalle Estado { get; set; } = EstadoDetalle.PENDIENTE;
    public Guid PedidoId { get; set; }
    public Guid ProductoId { get; set; }

    public Pedido Pedido { get; set; } = null!;
    public Producto Producto { get; set; } = null!;
}
```

`PrecioAcordado` se copia de la cotización aceptada; `CostoReferenciaAcordado` se copia de la vigencia efectiva al confirmar el pedido, y **nunca** se vuelven a tocar. Esa copia es lo que hace que RF-02 y RF-03 se cumplan: cambiar el catálogo mañana no mueve el margen de ayer.

> **Cambio al modelo que hay que registrar.** El diccionario de clases no tiene el atributo `codigo` en `Cotizacion` ni en `Pedido`, pero los mockups muestran `COT-028` y `PED-042`, y una pantalla de listado necesita un identificador legible: un UUID no sirve para que el cliente diga «mi pedido». Por eso esta guía agrega `Codigo` (texto, único) a esas dos clases. **No es una licencia para agregar otros atributos.** Antes de la entrega hay que actualizar `Diccionario_clases.md` y el `.mdj` de StarUML con esos dos atributos, para que el modelo y el código no se contradigan en la defensa. El formato es `COT-###` y `PED-###`, correlativo, generado por la API al crear el registro.

### 5.4 Enumeraciones del Sprint 1

Los valores van en MAYÚSCULAS, tal como el diccionario.

```csharp
public enum EstadoUsuario { ACTIVO, BLOQUEADO, DESHABILITADO }

public enum FormaPago { CONTADO, CREDITO_ACORDADO }

public enum TipoProducto { CARNE_FRESCA, DERIVADO, INSUMO }

public enum CanalSolicitud { WHATSAPP, LOCAL, PORTAL }

public enum EstadoCotizacion { BORRADOR, PRESENTADA, ACEPTADA, RECHAZADA, VENCIDA }

public enum EstadoComercial { CONFIRMADO, PENDIENTE_ACUERDO, CANCELADO, CERRADO }

public enum EstadoPreparacion { PENDIENTE, PROGRAMADA, EN_PREPARACION, PREPARADO, BLOQUEADO }

public enum EstadoDetalle { PENDIENTE, RESERVADO, EN_PREPARACION, PREPARADO, CANCELADO }
```

Las otras 23 enumeraciones se agregan en su sprint. No crearlas ahora. De las que sí se crean, `EstadoPreparacion` y `EstadoDetalle` solo usan el valor `PENDIENTE` en este sprint: están completas porque el diccionario las define así, pero nada las mueve todavía.

### 5.5 Configuración Fluent API

Una clase por entidad en `Datos/Configuraciones/`, con el mismo esqueleto: tabla, clave, propiedades, índices, relaciones. Ejemplos de las dos más delicadas.

```csharp
public class ProductoConfiguration : IEntityTypeConfiguration<Producto>
{
    public void Configure(EntityTypeBuilder<Producto> builder)
    {
        builder.ToTable("Productos");
        builder.HasKey(p => p.Id);

        builder.Property(p => p.Codigo).IsRequired().HasMaxLength(20);
        builder.Property(p => p.Nombre).IsRequired().HasMaxLength(120);
        builder.Property(p => p.Presentacion).IsRequired().HasMaxLength(60);
        builder.Property(p => p.UnidadVenta).IsRequired().HasMaxLength(10);
        builder.Property(p => p.Descripcion).HasMaxLength(400);

        builder.HasIndex(p => p.Codigo).IsUnique();

        builder.HasOne(p => p.ClasificacionProducto)
            .WithMany(c => c.Productos)
            .HasForeignKey(p => p.ClasificacionProductoId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

```csharp
public class PrecioProductoConfiguration : IEntityTypeConfiguration<PrecioProducto>
{
    public void Configure(EntityTypeBuilder<PrecioProducto> builder)
    {
        builder.ToTable("PreciosProducto");
        builder.HasKey(p => p.Id);

        builder.Property(p => p.CostoReferencia).HasPrecision(12, 2);
        builder.Property(p => p.PrecioVenta).HasPrecision(12, 2);

        builder.HasIndex(p => new { p.ProductoId, p.VigenteDesde }).IsUnique();

        builder.HasOne(p => p.Producto)
            .WithMany(p => p.Precios)
            .HasForeignKey(p => p.ProductoId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

`Cascade` aquí es correcto porque `Producto → PrecioProducto` es **composición** en el diccionario. `Restrict` en `ClasificacionProducto → Producto` porque es asociación y una clasificación usada no se borra.

Enumeraciones como texto, en cada configuración que corresponda:

```csharp
builder.Property(c => c.CondicionHabitual).HasConversion<string>().HasMaxLength(20);
builder.Property(c => c.Familia).HasConversion<string>().HasMaxLength(20);
builder.Property(u => u.Estado).HasConversion<string>().HasMaxLength(20);
```

Relaciones muchos a muchos (`Usuario ↔ Rol` y `Rol ↔ Permiso`): usar la convención de EF Core con tablas de unión explícitas por nombre.

```csharp
builder.HasMany(r => r.Permisos)
    .WithMany(p => p.Roles)
    .UsingEntity(j => j.ToTable("RolesPermisos"));
```


La parte comercial necesita cuidado con los borrados en cascada, porque `DetallePedido` recibe dos claves foráneas. MySQL sí admite dos caminos en cascada hacia la misma tabla, a diferencia de SQL Server, pero `Restrict` se mantiene de todos modos: está para conservar el histórico comercial, que es una regla del negocio y no una limitación del motor.

```csharp
public class PedidoConfiguration : IEntityTypeConfiguration<Pedido>
{
    public void Configure(EntityTypeBuilder<Pedido> builder)
    {
        builder.ToTable("Pedidos");
        builder.HasKey(p => p.Id);

        builder.Property(p => p.Codigo).IsRequired().HasMaxLength(20);
        builder.Property(p => p.EstadoComercial).HasConversion<string>().HasMaxLength(20);
        builder.Property(p => p.EstadoPreparacion).HasConversion<string>().HasMaxLength(20);
        builder.Property(p => p.CondicionPago).HasConversion<string>().HasMaxLength(20);
        builder.Property(p => p.CostoEstimadoConfirmado).HasPrecision(12, 2);
        builder.Property(p => p.MargenEstimadoConfirmado).HasPrecision(12, 2);

        builder.HasIndex(p => p.Codigo).IsUnique();

        builder.HasOne(p => p.Cliente)
            .WithMany(c => c.Pedidos)
            .HasForeignKey(p => p.ClienteId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(p => p.Cotizacion)
            .WithOne(c => c.Pedido)
            .HasForeignKey<Pedido>(p => p.CotizacionId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

```csharp
public class DetallePedidoConfiguration : IEntityTypeConfiguration<DetallePedido>
{
    public void Configure(EntityTypeBuilder<DetallePedido> builder)
    {
        builder.ToTable("DetallesPedido");
        builder.HasKey(d => d.Id);

        builder.Property(d => d.Unidad).IsRequired().HasMaxLength(10);
        builder.Property(d => d.Estado).HasConversion<string>().HasMaxLength(20);
        builder.Property(d => d.CantidadSolicitada).HasPrecision(12, 3);
        builder.Property(d => d.CantidadConfirmada).HasPrecision(12, 3);
        builder.Property(d => d.PrecioAcordado).HasPrecision(12, 2);
        builder.Property(d => d.CostoReferenciaAcordado).HasPrecision(12, 2);

        builder.HasOne(d => d.Pedido)
            .WithMany(p => p.Detalles)
            .HasForeignKey(d => d.PedidoId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(d => d.Producto)
            .WithMany()
            .HasForeignKey(d => d.ProductoId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

`Cotizacion` y `DetalleCotizacion` se configuran igual: composición hacia el detalle, por lo tanto `Cascade`; `Restrict` hacia `Cliente` y hacia `Producto`. La relación de `Cotizacion` consigo misma (`CotizacionOrigen`) va con `DeleteBehavior.Restrict` y `IsRequired(false)`.

Resumen de comportamientos de borrado del Sprint 1, para no descubrirlos durante la migración:

| Relación | Tipo en el diccionario | OnDelete |
|---|---|---|
| Producto → PrecioProducto | Composición | Cascade |
| Cotizacion → DetalleCotizacion | Composición | Cascade |
| Pedido → DetallePedido | Composición | Cascade |
| ClasificacionProducto → Producto | Asociación | Restrict |
| Cliente → Cotizacion | Asociación | Restrict |
| Cliente → Pedido | Asociación | Restrict |
| Cotizacion → Pedido | Asociación, 1 / 0..1 | Restrict |
| Producto → DetalleCotizacion | Asociación | Restrict |
| Producto → DetallePedido | Asociación | Restrict |
| Cliente → Usuario (cuentaPortal) | Asociación, 0..1 / 0..* | SetNull |
| Usuario → Sesion | Composición | Cascade |

### 5.6 Contexto

```csharp
public class SgcpContext : DbContext
{
    public SgcpContext(DbContextOptions<SgcpContext> options) : base(options) { }

    public DbSet<Permiso> Permisos => Set<Permiso>();
    public DbSet<Rol> Roles => Set<Rol>();
    public DbSet<Usuario> Usuarios => Set<Usuario>();
    public DbSet<Sesion> Sesiones => Set<Sesion>();
    public DbSet<RecuperacionAcceso> RecuperacionesAcceso => Set<RecuperacionAcceso>();
    public DbSet<RegistroAuditoria> RegistrosAuditoria => Set<RegistroAuditoria>();
    public DbSet<Cliente> Clientes => Set<Cliente>();
    public DbSet<ClasificacionProducto> ClasificacionesProducto => Set<ClasificacionProducto>();
    public DbSet<Producto> Productos => Set<Producto>();
    public DbSet<PrecioProducto> PreciosProducto => Set<PrecioProducto>();
    public DbSet<Cotizacion> Cotizaciones => Set<Cotizacion>();
    public DbSet<DetalleCotizacion> DetallesCotizacion => Set<DetalleCotizacion>();
    public DbSet<Pedido> Pedidos => Set<Pedido>();
    public DbSet<DetallePedido> DetallesPedido => Set<DetallePedido>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(SgcpContext).Assembly);
    }
}
```

### 5.7 Seguridad y permisos

Los permisos son cadenas `modulo.accion`. Se declaran en una clase estática y se siembran.

```csharp
public static class Permisos
{
    public const string UsuariosConsultar = "usuarios.consultar";
    public const string UsuariosAdministrar = "usuarios.administrar";
    public const string ClientesConsultar = "clientes.consultar";
    public const string ClientesAdministrar = "clientes.administrar";
    public const string CatalogoConsultar = "catalogo.consultar";
    public const string CatalogoAdministrar = "catalogo.administrar";
    public const string CostosConsultar = "costos.consultar";
    public const string CostosAdministrar = "costos.administrar";
    public const string CotizacionesConsultar = "cotizaciones.consultar";
    public const string CotizacionesAdministrar = "cotizaciones.administrar";
    public const string CotizacionesResponder = "cotizaciones.responder";
    public const string PedidosConsultar = "pedidos.consultar";
    public const string PedidosAdministrar = "pedidos.administrar";
}
```

Autorización por política, una política por permiso, verificada contra los claims del JWT:

```csharp
[Authorize(Policy = Permisos.ClientesAdministrar)]
```

El JWT lleva: `sub` (Id del usuario), `name`, `login`, un claim `rol` por cada rol y un claim `permiso` por cada permiso. Vigencia 8 horas. La `Sesion` se guarda en base con `Inicio`, `Expira` y `Revocada`; cerrar sesión marca `Revocada = true`.

Contraseñas con `PasswordHasher<Usuario>` de `Microsoft.AspNetCore.Identity`. **No** instalar ASP.NET Core Identity completo: solo esa clase, que viene en el framework.

Tras cinco `IntentosFallidos` el usuario pasa a `BLOQUEADO` y solo la administración lo reactiva.

### 5.8 Roles iniciales

| Rol | Permisos |
|---|---|
| ADMINISTRACION | todos |
| VENTAS | clientes.*, cotizaciones.*, pedidos.*, catalogo.consultar, costos.consultar |
| PRODUCCION | catalogo.consultar, pedidos.consultar |
| ALMACEN | catalogo.consultar, pedidos.consultar |
| ENTREGA | catalogo.consultar |
| COMPRADOR | catalogo.consultar, cotizaciones.consultar, cotizaciones.responder, pedidos.consultar |

El comprador tiene `cotizaciones.responder` porque es él quien acepta o rechaza, y `cotizaciones.consultar` **limitado a su propio cliente**: el permiso habilita la acción, y el servicio filtra el alcance. Las dos cosas son necesarias; ninguna reemplaza a la otra.

### 5.9 Respuestas y errores

Todas las respuestas de error usan el mismo cuerpo:

```json
{ "codigo": "CLIENTE_DUPLICADO", "mensaje": "Ya existe un cliente con esa identificación fiscal.", "detalles": [] }
```

Un filtro de excepciones global traduce las excepciones de dominio a `400`, las de autorización a `403`, lo no encontrado a `404` y el resto a `500` sin filtrar la traza.

Los listados devuelven siempre:

```json
{ "elementos": [], "pagina": 1, "tamanoPagina": 20, "totalRegistros": 0, "totalPaginas": 0 }
```

Parámetros de listado comunes: `pagina` (por defecto 1), `tamanoPagina` (por defecto 20, valores permitidos 10, 20, 50, 100), `busqueda`, y los filtros propios de cada recurso.

---
### 5.10 Endpoints

Prefijo `/api/v1`. Todos devuelven JSON. Todos exigen JWT salvo los marcados como anónimos.

#### CU01 · Autenticación

| Método | Ruta | Permiso | Qué hace |
|---|---|---|---|
| POST | `/auth/login` | anónimo | Valida credenciales, crea `Sesion`, devuelve token |
| POST | `/auth/registro-comprador` | anónimo | Crea `Usuario` con rol COMPRADOR. No crea cuentas internas |
| POST | `/auth/recuperar` | anónimo | Crea `RecuperacionAcceso` con token de un solo uso, 30 minutos |
| POST | `/auth/restablecer` | anónimo | Consume el token y cambia la clave |
| POST | `/auth/cerrar-sesion` | autenticado | Marca `Sesion.Revocada` |
| GET | `/auth/yo` | autenticado | Perfil, roles y permisos del usuario actual |

`POST /auth/login`

```json
{ "login": "ana.ventas", "clave": "..." }
```

```json
{
  "token": "eyJ...",
  "expira": "2026-11-06T20:00:00Z",
  "usuario": {
    "id": "....", "nombre": "Ana Rojas", "login": "ana.ventas",
    "roles": ["VENTAS"],
    "permisos": ["clientes.consultar", "clientes.administrar", "catalogo.consultar"]
  }
}
```

Reglas: credenciales inválidas suman `IntentosFallidos` y devuelven `401` con el mismo mensaje genérico tanto si el login no existe como si la clave es incorrecta. Un usuario `BLOQUEADO` o `DESHABILITADO` devuelve `403`. Un login correcto pone `IntentosFallidos = 0` y actualiza `UltimoAcceso`.

En `recuperar`, la respuesta es siempre `202` aunque el correo no exista, para no revelar qué cuentas hay. En desarrollo el token se devuelve en el cuerpo; en producción se enviaría por correo, que no está en el alcance.

#### CU02 · Usuarios

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/usuarios?busqueda=&estado=&rol=&pagina=&tamanoPagina=` | usuarios.consultar |
| GET | `/usuarios/{id}` | usuarios.consultar |
| POST | `/usuarios` | usuarios.administrar |
| PUT | `/usuarios/{id}` | usuarios.administrar |
| POST | `/usuarios/{id}/estado` | usuarios.administrar |
| GET | `/roles` | usuarios.consultar |
| GET | `/permisos` | usuarios.consultar |

Reglas: login único; no se permite asignar permisos que el solicitante no tiene; **no se puede desactivar al último usuario ACTIVO con rol ADMINISTRACION** (devolver `409` con código `ULTIMO_ADMINISTRADOR`); desactivar revoca sus sesiones; nunca se devuelve `HashClave`.

#### CU03 · Clientes

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/clientes?busqueda=&activo=&tipo=&pagina=&tamanoPagina=` | clientes.consultar |
| GET | `/clientes/{id}` | clientes.consultar |
| POST | `/clientes` | clientes.administrar |
| PUT | `/clientes/{id}` | clientes.administrar |
| POST | `/clientes/{id}/desactivar` | clientes.administrar |
| POST | `/clientes/{id}/activar` | clientes.administrar |

Reglas: `IdentificacionFiscal` no se repite entre clientes activos; la búsqueda cubre nombre, teléfono e identificación fiscal; `desactivar` en el Sprint 1 solo comprueba que no haya cuentas de portal activas vinculadas, y a partir del Sprint 2 comprobará además pedidos y deuda. Dejar el punto de extensión marcado en `ServicioClientes` con un método `VerificarDependenciasAsync`.

#### CU07 · Clasificaciones y productos

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/clasificaciones?familia=&activo=&busqueda=` | catalogo.consultar |
| POST | `/clasificaciones` | catalogo.administrar |
| PUT | `/clasificaciones/{id}` | catalogo.administrar |
| POST | `/clasificaciones/{id}/estado` | catalogo.administrar |
| GET | `/productos?busqueda=&clasificacionId=&familia=&activo=&pagina=&tamanoPagina=` | catalogo.consultar |
| GET | `/productos/{id}` | catalogo.consultar |
| POST | `/productos` | catalogo.administrar |
| PUT | `/productos/{id}` | catalogo.administrar |
| POST | `/productos/{id}/estado` | catalogo.administrar |

Reglas: `Codigo` único en productos y en clasificaciones; un producto solo se crea sobre una clasificación **activa**; desactivar una clasificación con productos activos devuelve `409` con código `CLASIFICACION_EN_USO` y la lista de productos que la usan; **cambiar `UnidadVenta` cuando el producto ya tiene precios vigentes se rechaza** con `UNIDAD_INCOMPATIBLE`; el listado de productos devuelve también el precio vigente, si existe.

Respuesta de producto:

```json
{
  "id": "...", "codigo": "PRD-001", "nombre": "Costilla de cerdo",
  "presentacion": "Pieza", "unidadVenta": "kg", "activo": true,
  "clasificacion": { "id": "...", "codigo": "CLS-001", "nombre": "Costilla", "familia": "CARNE_FRESCA" },
  "precioVigente": { "costoReferencia": 28.00, "precioVenta": 35.00, "vigenteDesde": "2026-10-01T00:00:00" }
}
```

#### CU04 · Costos y precios

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/productos/{id}/precios` | costos.consultar |
| POST | `/productos/{id}/precios` | costos.administrar |
| PUT | `/precios/{id}` | costos.administrar |
| POST | `/precios/{id}/finalizar` | costos.administrar |

Reglas, y son las más importantes del sprint:

1. Abrir una vigencia nueva **cierra la anterior**: pone `VigenteHasta` de la vigencia abierta en el instante anterior a la nueva `VigenteDesde`. Las dos operaciones van en **una sola transacción**.
2. No se permiten dos vigencias abiertas para el mismo producto.
3. `VigenteDesde` no puede ser anterior a la `VigenteDesde` de la vigencia que cierra.
4. `PrecioVenta` y `CostoReferencia` deben ser mayores que cero. Si `PrecioVenta <= CostoReferencia`, la API **no lo rechaza**: devuelve `201` con una advertencia `margenNoPositivo` en el cuerpo, porque el propietario puede vender bajo costo a conciencia. La web muestra la advertencia y pide confirmar.
5. El margen estimado se calcula, **no se almacena**: `margen = precioVenta - costoReferencia`.
6. Corregir una vigencia solo cambia importes y fechas de esa fila. **Nunca toca cotizaciones ni pedidos**, que conservan su propio costo y precio acordados. Esta es la regla que se demuestra en el criterio 23 de la sección 10: cambiar el precio después de confirmar un pedido y ver que el margen de ese pedido no se mueve.

#### CU05 · Cotizaciones

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/cotizaciones?busqueda=&estado=&clienteId=&pagina=&tamanoPagina=` | cotizaciones.consultar |
| GET | `/cotizaciones/{id}` | cotizaciones.consultar |
| POST | `/cotizaciones` | cotizaciones.administrar |
| PUT | `/cotizaciones/{id}` | cotizaciones.administrar |
| POST | `/cotizaciones/{id}/presentar` | cotizaciones.administrar |
| POST | `/cotizaciones/{id}/aceptar` | cotizaciones.responder |
| POST | `/cotizaciones/{id}/rechazar` | cotizaciones.responder |
| POST | `/cotizaciones/{id}/nueva-version` | cotizaciones.administrar |

Cuerpo de alta:

```json
{
  "clienteId": "…",
  "canal": "WHATSAPP",
  "vigenteHasta": "2026-10-26T18:00:00Z",
  "detalles": [
    { "productoId": "…", "cantidad": 4, "unidad": "kg", "precioUnitario": 35.00 }
  ]
}
```

Reglas, en este orden:

1. **Estados permitidos**: `BORRADOR → PRESENTADA → ACEPTADA | RECHAZADA`, y `PRESENTADA → VENCIDA` por el paso del tiempo. Cualquier otra transición devuelve `409` con código `TRANSICION_INVALIDA`.
2. `PUT` solo funciona en `BORRADOR`. Una cotización `PRESENTADA` no se edita: se crea una **versión nueva** con `POST /cotizaciones/{id}/nueva-version`, que copia cliente y detalles en una cotización `BORRADOR` con `Version + 1` y `CotizacionOrigenId` apuntando a la anterior. La anterior queda como está; no se borra.
3. **El vencimiento se evalúa al leer y se persiste**: si el estado es `PRESENTADA` y `VigenteHasta < ahora`, el servicio la pasa a `VENCIDA` antes de responder. Así nadie acepta una cotización vencida por haber dejado la pestaña abierta.
4. `aceptar` exige estado `PRESENTADA` y `VigenteHasta >= ahora`. Si no, `409` con `COTIZACION_NO_VIGENTE`.
5. `rechazar` exige `PRESENTADA` y un `motivo` no vacío, que se guarda en `MotivoRespuesta`. **Rechazar no crea pedido, no reserva y no cobra.** Es la pantalla w08.
6. Los detalles solo admiten productos `Activo = true` y con **vigencia de precio abierta**. El `precioUnitario` se propone desde esa vigencia; el usuario de ventas puede cambiarlo, y lo que queda guardado es lo que él puso, no el de catálogo.
7. `Subtotal` se calcula en el servidor. Si el cliente envía uno, se ignora.
8. Un usuario con rol `COMPRADOR` solo ve y responde **sus propias** cotizaciones, filtradas por el `Cliente` vinculado a su `Usuario`. Si pide una ajena recibe `403`, nunca `404` con datos.

#### CU06 · Pedidos

| Método | Ruta | Permiso |
|---|---|---|
| GET | `/pedidos?busqueda=&estadoComercial=&clienteId=&pagina=&tamanoPagina=` | pedidos.consultar |
| GET | `/pedidos/{id}` | pedidos.consultar |
| POST | `/pedidos` | pedidos.administrar |
| POST | `/pedidos/{id}/cancelar` | pedidos.administrar |

Cuerpo de alta, deliberadamente corto: el pedido **no** recibe productos ni precios, los toma de la cotización aceptada.

```json
{ "cotizacionId": "…", "fechaComprometida": "2026-10-26T12:00:00Z", "condicionPago": "CREDITO_ACORDADO" }
```

Reglas:

1. **Sin cotización aceptada no hay pedido.** Si la cotización no está en `ACEPTADA`, o ya tiene un pedido, la respuesta es `409` con `COTIZACION_NO_ACEPTADA` o `COTIZACION_YA_TIENE_PEDIDO`. Esta es la regla que el criterio de validación del sprint nombra primero.
2. El pedido copia, por cada detalle de la cotización: producto, cantidad (a `CantidadSolicitada` **y** a `CantidadConfirmada`), unidad, `PrecioAcordado` desde el `precioUnitario` cotizado, y `CostoReferenciaAcordado` desde la **vigencia abierta del producto al momento de confirmar**.
3. Si algún producto del pedido no tiene vigencia de costo abierta, no se confirma nada: `409` con `SIN_COSTO_VIGENTE` y la lista de productos. Todo o nada, en una transacción.
4. `CostoEstimadoConfirmado = Σ CantidadConfirmada × CostoReferenciaAcordado`.
5. `MargenEstimadoConfirmado = Σ CantidadConfirmada × (PrecioAcordado − CostoReferenciaAcordado)`. Los dos se **guardan** en el pedido; no se recalculan nunca. El ejemplo del backlog tiene que dar exactamente `4 × (35 − 28) = Bs 28`.
6. El pedido nace `EstadoComercial = CONFIRMADO` y `EstadoPreparacion = PENDIENTE`. En el Sprint 1 nada mueve `EstadoPreparacion`.
7. `cancelar` exige motivo y pasa el pedido a `CANCELADO`. **No devuelve dinero, no libera reservas y no borra nada**, porque ni los pagos ni las reservas existen todavía; la cancelación queda registrada para que el Sprint 3 la resuelva por acuerdo.
8. Un pedido **no se borra ni se edita**. Cambiar lo pedido exige una cotización nueva.
9. El comprador consulta solo los pedidos de su propio cliente.

---

## 6. Patrones de diseño

Los nombres de clase de esta sección salen de los `.mdj` de StarUML ya entregados al docente. **No se renombran.** Si el código los llama de otra forma, el modelo entregado y el sistema se contradicen en la defensa.

### En el Sprint 1: Builder

Es el patrón que corresponde, porque el Sprint 1 es el que confirma pedidos. Un pedido confirmado se arma pieza por pieza —cliente, cotización de origen, fecha comprometida, condición de pago, un detalle por producto con su precio y su costo congelados— y recién al final se valida y se calcula el margen. Eso es exactamente para lo que sirve Builder, y evita un constructor de ocho parámetros o un servicio que arma la entidad a mano en medio del controlador.

```csharp
public class PedidoBuilder
{
    private readonly Pedido _pedido = new();
    private readonly List<DetallePedido> _detalles = new();

    public PedidoBuilder ParaCliente(Cliente cliente)
    {
        _pedido.ClienteId = cliente.Id;
        _pedido.CondicionPago = cliente.CondicionHabitual;
        return this;
    }

    public PedidoBuilder DesdeCotizacion(Cotizacion cotizacion)
    {
        _pedido.CotizacionId = cotizacion.Id;
        return this;
    }

    public PedidoBuilder ConCodigo(string codigo)
    {
        _pedido.Codigo = codigo;
        return this;
    }

    public PedidoBuilder ConFechaComprometida(DateTime fecha)
    {
        _pedido.FechaComprometida = fecha;
        return this;
    }

    public PedidoBuilder ConCondicionPago(FormaPago condicion)
    {
        _pedido.CondicionPago = condicion;
        return this;
    }

    public PedidoBuilder AgregarDetalle(Guid productoId, decimal cantidad, string unidad,
                                        decimal precioAcordado, decimal costoReferenciaAcordado)
    {
        _detalles.Add(new DetallePedido
        {
            ProductoId = productoId,
            CantidadSolicitada = cantidad,
            CantidadConfirmada = cantidad,
            Unidad = unidad,
            PrecioAcordado = precioAcordado,
            CostoReferenciaAcordado = costoReferenciaAcordado,
            Estado = EstadoDetalle.PENDIENTE
        });
        return this;
    }

    public Pedido Construir()
    {
        if (_detalles.Count == 0)
        {
            throw new ReglaDeNegocioException("PEDIDO_SIN_DETALLE", "Un pedido necesita al menos un producto.");
        }

        _pedido.Fecha = DateTime.UtcNow;
        _pedido.EstadoComercial = EstadoComercial.CONFIRMADO;
        _pedido.EstadoPreparacion = EstadoPreparacion.PENDIENTE;
        _pedido.CostoEstimadoConfirmado = _detalles.Sum(d => d.CantidadConfirmada * d.CostoReferenciaAcordado);
        _pedido.MargenEstimadoConfirmado = _detalles.Sum(d => d.CantidadConfirmada * (d.PrecioAcordado - d.CostoReferenciaAcordado));

        foreach (var detalle in _detalles)
        {
            _pedido.Detalles.Add(detalle);
        }

        return _pedido;
    }
}
```

`ServicioConfirmarPedido` es quien lo usa, y quien aplica las reglas de CU06: comprueba la cotización aceptada y vigente, busca la vigencia de costo de cada producto, llena el builder y guarda todo en una transacción.

```csharp
public class ServicioConfirmarPedido
{
    private readonly SgcpContext _contexto;
    private readonly IGeneradorCodigo _generadorCodigo;

    public async Task<Pedido> ConfirmarAsync(Guid cotizacionId, DateTime fechaComprometida, FormaPago condicionPago)
    {
        var cotizacion = await _contexto.Cotizaciones
            .Include(c => c.Cliente)
            .Include(c => c.Detalles)
            .Include(c => c.Pedido)
            .FirstOrDefaultAsync(c => c.Id == cotizacionId)
            ?? throw new NoEncontradoException("COTIZACION_NO_ENCONTRADA", "La cotización no existe.");

        if (cotizacion.Estado != EstadoCotizacion.ACEPTADA)
        {
            throw new ReglaDeNegocioException("COTIZACION_NO_ACEPTADA", "Solo una cotización aceptada genera pedido.");
        }

        if (cotizacion.Pedido is not null)
        {
            throw new ReglaDeNegocioException("COTIZACION_YA_TIENE_PEDIDO", "Esa cotización ya generó un pedido.");
        }

        var builder = new PedidoBuilder()
            .ParaCliente(cotizacion.Cliente)
            .DesdeCotizacion(cotizacion)
            .ConCodigo(await _generadorCodigo.SiguienteAsync("PED"))
            .ConFechaComprometida(fechaComprometida)
            .ConCondicionPago(condicionPago);

        foreach (var detalle in cotizacion.Detalles)
        {
            var costo = await ObtenerCostoVigenteAsync(detalle.ProductoId);
            builder.AgregarDetalle(detalle.ProductoId, detalle.Cantidad, detalle.Unidad,
                                   detalle.PrecioUnitario, costo);
        }

        var pedido = builder.Construir();
        _contexto.Pedidos.Add(pedido);
        await _contexto.SaveChangesAsync();
        return pedido;
    }
}
```

Dos cosas que conviene poder explicar en la defensa, porque son la razón de ser del patrón aquí:

- El builder **no toca la base de datos**. Recibe datos, arma el objeto y calcula. Eso lo hace verificable sin base, que es lo que pide la rúbrica cuando habla de separar responsabilidades.
- El cálculo del margen vive en un solo lugar: `Construir()`. Si mañana cambia la fórmula, cambia ahí y en ningún otro sitio.

### Comprometidos para sprints siguientes

Estos **no se implementan ahora**. Están aquí para que nadie los adelante y para que la numeración del documento de patrones coincida.

| Patrón | Clases del UML | Sprint | Para qué |
|---|---|---|---|
| Facade | `FachadaRecepcion`, `ControladorRecepcion`, `PoliticaRecepcion`, `RegistroIdempotente`, `UnidadRecepcion` | 3 | Una sola entrada para registrar una recepción de entrega |
| Strategy | `IPoliticaPagoDespacho`, `Contado`, `CreditoAcordado`, `ServicioDespacho` | 3 | Decidir si se autoriza el despacho según la forma de pago |
| Command | `IComandoEnvio`, `ComandoRecepcion`, `ColaRecepciones`, `AlmacenPendientes` | 3 | Encolar capturas offline de Android y reintentarlas |
| State | `IEstadoEnvio`, `Pendiente`, `Enviando`, `Confirmada`, `Conflicto`, `Descartada` | 3 | El ciclo de vida de una sincronización |
| Factory Method | `IExportadorReporte`, `ExportadorPDF`, `ExportadorExcel`, `ExportacionReporte`, `ExportacionPDF`, `ExportacionExcel` | 4 | Elegir el formato de exportación de un reporte |
| Adapter | `MotorPDFExterno` | 4 | Envolver el motor de PDF de terceros detrás de la interfaz propia |

---

## 7. SGCPuiweb

### 7.1 Crear el proyecto

```bash
cd SGCPuiweb
dotnet new sln -n SGCPuiweb
dotnet new mvc -n SGCP.Web -o src/SGCP.Web -f net10.0
dotnet sln SGCPuiweb.sln add src/SGCP.Web/SGCP.Web.csproj
```

Sin paquetes extra. **No instalar Entity Framework Core en este proyecto.** Si aparece una referencia a EF Core en SGCPuiweb, está mal hecho.

### 7.2 Estructura

```
SGCPuiweb/
  SGCPuiweb.sln
  .gitignore
  README.md
  src/SGCP.Web/
    Controllers/
      CuentaController.cs
      InicioController.cs
      UsuariosController.cs
      ClientesController.cs
      ClasificacionesController.cs
      ProductosController.cs
      PreciosController.cs
      CotizacionesController.cs
      PedidosController.cs
    Models/
      ViewModels/
        Cuenta/        IniciarSesionViewModel, RegistroCompradorViewModel, RecuperarViewModel, RestablecerViewModel
        Inicio/        ResumenViewModel
        Usuarios/      UsuarioListaViewModel, UsuarioFormViewModel
        Clientes/      ClienteListaViewModel, ClienteFormViewModel
        Catalogo/      ProductoListaViewModel, ProductoFormViewModel, ClasificacionListaViewModel, ClasificacionFormViewModel
        Precios/       PrecioListaViewModel, PrecioFormViewModel
        Cotizaciones/  CotizacionListaViewModel, CotizacionFormViewModel, CotizacionDetalleViewModel, RespuestaCotizacionViewModel
        Pedidos/       PedidoListaViewModel, PedidoDetalleViewModel, ConfirmarPedidoViewModel
        Comun/         PaginacionViewModel, MensajeViewModel
      Dtos/            espejo exacto de lo que devuelve la API
    Services/
      ClienteApiBase.cs
      AutenticacionApi.cs
      UsuariosApi.cs
      ClientesApi.cs
      CatalogoApi.cs
      PreciosApi.cs
      CotizacionesApi.cs
      PedidosApi.cs
    Views/
      Shared/
        _Layout.cshtml
        _BarraLateral.cshtml
        _Paginacion.cshtml
        _Mensajes.cshtml
        _ValidationScriptsPartial.cshtml
      Cuenta/  Inicio/  Usuarios/  Clientes/  Clasificaciones/  Productos/  Precios/  Cotizaciones/  Pedidos/
    wwwroot/
    Program.cs
    appsettings.json
```

**Models/ViewModels/ es la carpeta que pidió el docente.** Los DTO que devuelve la API viven aparte, en `Models/Dtos/`, y nunca se usan como modelo de una vista: siempre se traducen a un ViewModel en el controlador. Esa separación es justamente lo que la rúbrica llama separación de responsabilidades.

### 7.3 Cómo habla la web con la API

`appsettings.json`:

```json
{
  "Api": { "UrlBase": "https://localhost:7001/api/v1/" }
}
```

`Program.cs`:

```csharp
builder.Services.AddHttpContextAccessor();

builder.Services.AddHttpClient<AutenticacionApi>(cliente =>
    cliente.BaseAddress = new Uri(builder.Configuration["Api:UrlBase"]!));

builder.Services.AddHttpClient<ClientesApi>(cliente =>
    cliente.BaseAddress = new Uri(builder.Configuration["Api:UrlBase"]!))
    .AddHttpMessageHandler<ManejadorTokenJwt>();
```

`ManejadorTokenJwt` es un `DelegatingHandler` que lee el token de la cookie del usuario y lo pone en la cabecera `Authorization: Bearer`. Así ningún controlador manipula cabeceras a mano.

Autenticación por cookie:

```csharp
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(opciones =>
    {
        opciones.LoginPath = "/Cuenta/IniciarSesion";
        opciones.AccessDeniedPath = "/Cuenta/SinPermiso";
        opciones.ExpireTimeSpan = TimeSpan.FromHours(8);
    });
```

Al iniciar sesión, el controlador llama a `POST /auth/login`, y con la respuesta arma los claims: nombre, login, un claim `rol` por rol, un claim `permiso` por permiso, y el JWT guardado como claim privado `jwt`. Las vistas ocultan botones con un helper `TienePermiso("clientes.administrar")`, y los controladores lo exigen con políticas. **Ocultar el botón no alcanza: la API también valida.**

### 7.4 El diseño, según los mockups

Los 67 mockups de Balsamiq son la referencia visual. Lo que define el `_Layout`:

- **Barra superior**: a la izquierda la marca `SGCP`, al lado el subtítulo `Gestión comercial y clientes`; a la derecha `Nombre · Rol | Salir`. Debajo, una línea horizontal.
- **Barra lateral izquierda**, botones en este orden: Inicio, Usuarios, Clientes, Productos, Gestión de costos, Cotizaciones, Pedidos, Producción, Inventario, Cobranza, Transporte / entregas, Reportes. El activo se marca. Las siete primeras entradas —Inicio, Usuarios, Clientes, Productos, Gestión de costos, Cotizaciones y Pedidos— funcionan. **Las cinco restantes, Producción, Inventario, Cobranza, Transporte / entregas y Reportes, se muestran deshabilitadas**, no se ocultan: así el avance se ve en la presentación y se entiende qué falta.
- **Encabezado de contenido**: título de la pantalla y debajo la fecha más `· Chanchería`.
- **Pie**: a la izquierda la etiqueta `Conectado`, y los enlaces `Portal comprador` y `Vista móvil web`.
- Ancho de referencia 1440 px, responsivo hasta 414 px. Bootstrap 5, el que trae la plantilla.
- Moneda siempre con el prefijo `Bs` y dos decimales. **Las unidades siempre visibles** junto a la cantidad: `4 kg`, nunca `4`.
- Español en toda la interfaz. Nada de texto en inglés.

### 7.5 Pantallas

#### w01 · Iniciar sesión

Título `SGCP · Gestión comercial`. Bajada: *Clientes, cotizaciones, preparación, entregas y cobros en un mismo sistema.* Campos Usuario y Contraseña, aviso `Acceso con conexión`, botón `Ingresar a gestión`, párrafo *La web requiere internet. Usa tu cuenta y los permisos asignados por la administración.* y tres enlaces: `Ingresar como comprador`, `Crear cuenta de comprador`, `Recuperar acceso`.

#### w02 · Resumen del negocio

Cuatro tarjetas en fila. El mockup muestra En preparación, Por cobrar, Reparto de hoy y Producción prevista, que son de módulos posteriores. En el Sprint 1 se conserva **la misma disposición de cuatro tarjetas** con los datos que ya existen: Clientes activos, Productos activos, Cotizaciones vigentes y Pedidos confirmados del mes. Debajo, la tabla `Seguimiento de hoy` lista los últimos pedidos confirmados, con cliente, fecha comprometida y estado comercial; las columnas de preparación y entrega llevan el aviso *Disponible en el siguiente sprint*. Al pie, dos botones de acción directa: `Nuevo cliente` y `Nuevo producto`.

Esto hay que explicarlo en la presentación: la pantalla es la del mockup, con los indicadores que el sprint puede calcular de verdad. No inventar números.

#### w04, wuser, wuseroff · Usuarios

Listado con búsqueda, filtro por estado y por rol, paginación, y columnas Nombre, Login, Roles, Estado, Último acceso. Formulario con nombre, login, correo, teléfono y selección múltiple de roles. La desactivación es una pantalla de confirmación que muestra qué pierde el usuario y **avisa si es el último administrador**, en cuyo caso el botón queda deshabilitado.

#### w03, wclient, wclientblock · Clientes

Listado con búsqueda por nombre, teléfono o identificación fiscal, filtro activo/inactivo, paginación. Ficha comercial del cliente con sus datos y, en el Sprint 1, la sección de pedidos ya con datos reales y la de saldo visible pero vacía, con el aviso *Disponible en el siguiente sprint*. `wclientblock` muestra las dependencias antes de desactivar.

#### wcat, wprod, wprodoff, wclass · Catálogo

`wclass` administra clasificaciones: código, nombre, familia (`CARNE_FRESCA`, `DERIVADO`, `INSUMO`), descripción, estado. `wcat` lista productos con filtro por familia, por clasificación y por estado, y muestra el precio vigente de cada uno. `wprod` es la ficha con sus datos y su historial de precios. `wprodoff` confirma la desactivación.

#### w05 · Gestión de costos y precios

Elegir producto, ver el historial de vigencias en una tabla (Desde, Hasta, Costo, Precio, Margen) y un formulario para abrir una vigencia nueva. Al guardar, si el margen no es positivo, la pantalla pide confirmación explícita antes de reenviar. El margen se muestra calculado, en Bs y en porcentaje.

#### w06, w07, w08 · Cotizaciones

Listado en `/Cotizaciones`, con buscador por cliente o código, filtro por estado y la paginación compartida. El detalle es la pantalla w06 y reproduce el mockup:

- Encabezado `Cotización COT-028 · presentada` y, debajo, la línea de estado: `PRESENTADA · versión 2 · esperando respuesta del cliente`.
- Cliente y fecha propuesta en una línea: `Restaurante El Patio · Fecha propuesta: 26 oct, 12:00`.
- Tabla con cuatro columnas exactas: **Producto · Cantidad · Precio acordado · Importe**. Las cantidades llevan unidad (`4 kg`) y los precios llevan `Bs` y unidad (`Bs 35/kg`).
- El bloque **Servicio de faeneo / corte** se escribe como el mockup, en texto: *Bs 30 acordados por separado, solo si se realiza el servicio.* No es una fila de la tabla ni se suma. RF-20 es del Sprint 2.
- Tres botones: `Registrar aceptación`, `Registrar rechazo / cambios`, `Crear pedido`.
- Al pie, el aviso del mockup, literal: *La solicitud todavía no es un pedido. No se reserva producto ni se inicia preparación.*

`Crear pedido` solo está habilitado cuando el estado es `ACEPTADA`. En w06 (presentada) se muestra deshabilitado; en w07 (aceptada) el botón pasa a ser `Crear pedido confirmado` y aparece el texto *Se conserva el precio y costo acordados. La preparación comienza después de confirmar.* Deshabilitarlo en la vista **no reemplaza** la validación de la API: el servidor vuelve a comprobarlo.

w08 es la pantalla de respuesta negativa, con dos caminos y sus textos del mockup: `Preparar nueva cotización`, que llama a `nueva-version`, y `Conservar rechazo y volver`, que llama a `rechazar` con el motivo. En w08 el botón `Crear pedido` aparece deshabilitado, que es justo lo que el criterio de validación del sprint quiere ver demostrado.

#### w09 · Pedidos

Listado en `/Pedidos` y detalle según el mockup:

- Encabezado `Pedido PED-042` y línea de estado `CONFIRMADO · origen COT-028 aceptada · Restaurante El Patio`, con el código de la cotización enlazado a su detalle.
- Tabla **Concepto · Cantidad · Importe · Preparación**. En el Sprint 1 la columna Preparación muestra `Pendiente` para todas las filas, porque nada la mueve todavía.
- Dos bloques de texto: **Preparación** con la fecha comprometida, y **Condición de pago** con la condición del pedido. El saldo y la deuda del mockup son del Sprint 3: en su lugar va el aviso de que la cobranza llega después.
- La línea del margen, que es la demostración de RF-03, con el cálculo visible tal como el mockup: *Margen estimado de productos: 4 kg × (Bs 35 − Bs 28) = Bs 28.*
- Los botones `Revisar reservas`, `Ver preparación` y `Ver despacho` se muestran **deshabilitados**, con el mismo criterio que las entradas deshabilitadas de la barra lateral: el mockup los tiene y la navegación no existe aún.

---
## 8. SGCPuimovil en el Sprint 1

El Excel pide, textual, «datos centrales y **base técnica Android**». No pide la app funcionando: la aplicación Kotlin con captura offline y sincronización es el **Sprint 3**, RF-05 a RF-08 y RF-19.

Base técnica significa esto y nada más:

1. Proyecto Android creado y compilando, con `minSdk` y `targetSdk` acordados por el equipo y anotados en el README.
2. `.gitignore` de Android antes del primer commit de código: `build/`, `.gradle/`, `local.properties`, `*.iml`, `.idea/`.
3. Cliente HTTP configurado contra la misma API (`Retrofit` + `OkHttp`), con la URL base en un solo lugar.
4. Pantalla `a01 · Acceder al reparto`, que llama a `POST /api/v1/auth/login` de SGCPapi y guarda el token.
5. Pantalla `a10 · Renovar acceso`, que repite el login cuando el token venció.
6. Pantalla `a03 · Mis entregas` con estado vacío y el texto *No hay reparto descargado*.

**Nada de Room todavía, nada de captura sin conexión, nada de sincronización.** Las pantallas a02 y a04 a a09 son del Sprint 3 y dependen de los patrones Command y State, que tampoco se escriben ahora.

Lo que sí se verifica en la presentación de mañana: que la app abre, que el login llega a la API del equipo y que el token se guarda. Eso demuestra que los tres repositorios hablan entre sí, que es el objetivo real de incluir Android en este sprint.

---

## 9. Reparto del trabajo entre los cuatro

El Excel ya asigna roles de equipo, y el reparto los respeta: Sofia es Product Owner y Victor es Scrum Master, que además «apoya el desarrollo web, Android y las pruebas del sistema».

| | Integrante | Rol en el equipo | Repositorio | Entrega del Sprint 1 |
|---|---|---|---|---|
| 1 | **Dario Haziel Tambo Parra** | Desarrollador | SGCPapi | Solución y estructura, EF Core, las 14 entidades, las configuraciones Fluent, migración inicial, datos iniciales, JWT, permisos y políticas, filtro de excepciones, paginación, auditoría, **CU01**, **CU02** y **CU03** |
| 2 | **Angel Sebastian Eguez Mur** | Desarrollador | SGCPapi | **CU07** clasificaciones y productos, **CU04** vigencias de costo y precio con su transacción, **CU05** cotizaciones con versionado y vencimiento, **CU06** pedidos con `PedidoBuilder` y `ServicioConfirmarPedido`, generador de códigos `COT-###` y `PED-###` |
| 3 | **Sofia Cuellar Roca** | Product Owner | SGCPuiweb | Proyecto MVC, `_Layout` con la barra lateral del mockup, `ManejadorTokenJwt`, autenticación por cookie, pantallas w01, preg, pregdone, pforgot, preset, w02, módulo Usuarios (w04, wuser, wuseroff) y módulo Clientes (w03, wclient, wclientblock). Además verifica, uno por uno, los criterios de la sección 10 antes de la presentación |
| 4 | **Victor Manuel Manrique Arancivia** | Scrum Master | SGCPuiweb y SGCPuimovil | Módulo Catálogo (wcat, wprod, wprodoff, wclass), módulo Costos (w05), módulos Cotizaciones (w06, w07, w08) y Pedidos (w09), la paginación compartida con su lista desplegable de tamaño, y la base técnica de Android de la sección 8 |

### Cómo evitar bloqueos

El orden natural sería API primero y web después, pero no hay tiempo para eso. Tres medidas:

1. **El contrato se define antes que el código.** Las secciones 5.9 y 5.10 de esta guía *son* el contrato. Los DTO de `Models/Dtos/` se escriben a partir de este documento, no esperando a que la API responda.
2. **Dario entrega primero la base.** Entidades, migración, JWT y el filtro de excepciones son lo que desbloquea a Angel. Ese es su primer commit, no el último.
3. Mientras la API no está en pie, los `Services/` de la web devuelven datos fijos desde un método `DatosDePrueba()` detrás de la misma interfaz. Se borra en cuanto la API responde. **Ese código de prueba no se sube a `main`**: vive en la rama de quien lo usa y desaparece antes de integrar.

### Ramas y commits

Una rama por integrante y por área:

```
api/base-identidad-clientes     Dario
api/catalogo-costos-comercial   Angel
web/acceso-usuarios-clientes    Sofia
web/catalogo-costos-comercial   Victor
movil/base-tecnica              Victor
```

Cada uno configura su identidad **una vez por repositorio**, con el correo de su cuenta de GitHub, o los commits no se le atribuyen:

```bash
git config user.name "Nombre Apellido"
git config user.email "correo-de-github@ejemplo.com"
```

Mensajes en minúsculas, con prefijo de área y en español. Mínimo cinco commits con contenido real por persona:

```
base: estructura de la solucion y paquetes de SGCPapi
datos: entidades de identidad, cliente, catalogo y comercial
datos: configuraciones fluent api y migracion inicial
seguridad: emision de jwt, politicas y permisos sembrados
cu01: autenticacion, registro de comprador y recuperacion de acceso
cu02: administracion de usuarios, roles y permisos
cu03: mantenimiento de clientes con busqueda y paginacion
cu07: clasificaciones y productos del catalogo
cu04: vigencias de costo y precio en una transaccion
cu05: cotizaciones versionadas con aceptacion y rechazo
cu06: confirmacion de pedido con builder y margen estimado
web: layout con barra lateral y mensajes de operacion
web: acceso, registro de comprador y recuperacion
web: mantenimiento de usuarios, permisos y clientes
web: catalogo, vigencias de precio y paginacion
web: cotizaciones y pedidos segun los mockups
movil: proyecto android, cliente http y acceso al reparto
```

---

## 10. Criterios de aceptación del Sprint 1

La demostración tiene que poder hacerse así, en este orden, sin tocar la base de datos a mano. Los criterios 14 a 20 son los que el Excel nombra explícitamente en la columna *Criterio de validación*; los demás son lo que hace falta para llegar hasta ellos.

| # | Se demuestra | Resultado esperado |
|---|---|---|
| 1 | Clonar los tres repositorios y compilar | `dotnet build` sin errores ni advertencias en SGCPapi y SGCPuiweb; el proyecto Android compila |
| 2 | `dotnet ef database update` en SGCPapi | Crea las tablas de dominio, las tablas de asociación y el historial de migraciones; los datos iniciales se cargan al arrancar la API |
| 3 | Abrir Swagger | Lista todos los endpoints de la sección 5.10 |
| 4 | Entrar a la web con el usuario administrador | Llega al resumen con la barra lateral y las tarjetas del sprint |
| 5 | Entrar con una clave incorrecta cinco veces | Al quinto fallo el usuario queda `BLOQUEADO` |
| 6 | Crear un usuario de ventas y entrar con él | Ve Clientes, Productos, Cotizaciones y Pedidos; **no** ve Usuarios, y si escribe la URL a mano recibe acceso denegado |
| 7 | Intentar desactivar al único administrador | Lo rechaza con mensaje claro |
| 8 | Crear la clasificación `CARNE_FRESCA / Costilla` y el producto `Costilla de cerdo`, unidad kg | Queda activo y **sin stock**: no existe ninguna pantalla ni tabla de existencia en este sprint |
| 9 | Intentar cambiar la unidad de venta de un producto con precios | Lo rechaza con `UNIDAD_INCOMPATIBLE` |
| 10 | Intentar desactivar una clasificación con productos activos | Lo rechaza y nombra los productos |
| 11 | Registrar costo Bs 28 y precio Bs 35 vigentes desde hoy | El listado muestra margen Bs 7 por kg |
| 12 | Registrar una vigencia nueva de Bs 30 / Bs 38 | La anterior queda cerrada; **no hay dos vigencias abiertas** |
| 13 | Crear un cliente, cotizarle y luego intentar desactivarlo | La desactivación se rechaza mientras tenga operaciones pendientes, y el historial se conserva |
| 14 | Registrar una cuenta de comprador desde la web pública | Entra y solo ve lo suyo; **no recibe ningún permiso interno** |
| 15 | Recuperar acceso y establecer una contraseña nueva | El token sirve una sola vez y las sesiones anteriores quedan revocadas |
| 16 | Crear la cotización COT-028 para Restaurante El Patio: 4 kg de costilla a Bs 35/kg, canal WHATSAPP | Queda en `BORRADOR`; al presentarla pasa a `PRESENTADA` |
| 17 | Con la cotización en `PRESENTADA`, intentar crear el pedido | Lo rechaza: `COTIZACION_NO_ACEPTADA`. El botón de la pantalla w06 está deshabilitado y la API también lo rechaza si se llama directamente |
| 18 | Rechazar una cotización con motivo, y luego intentar crear el pedido | **Una cotización rechazada no crea pedido.** Se conserva la cotización y el motivo |
| 19 | Poner una `VigenteHasta` ya pasada y volver a consultarla | Pasa sola a `VENCIDA`, y aceptarla devuelve `COTIZACION_NO_VIGENTE` |
| 20 | Preparar una versión nueva desde una cotización presentada | Nace `BORRADOR` con `Version 2`, apuntando a la anterior, que se conserva intacta |
| 21 | Aceptar COT-028 y confirmar el pedido PED-042 | Se crea con `CONFIRMADO` / `PENDIENTE`, copiando precio Bs 35 y costo Bs 28 por detalle |
| 22 | Leer el margen del pedido | Muestra exactamente `4 kg × (Bs 35 − Bs 28) = Bs 28`, el ejemplo del backlog |
| 23 | Registrar una vigencia nueva de Bs 40 y volver al pedido | **El margen no cambia.** Sigue en Bs 28: los acuerdos históricos se conservan |
| 24 | Intentar confirmar un segundo pedido desde la misma cotización | Lo rechaza con `COTIZACION_YA_TIENE_PEDIDO` |
| 25 | Entrar como el comprador registrado y pedir la cotización de otro cliente | Devuelve `403`, sin filtrar ningún dato del otro cliente |
| 26 | Revisar la tabla `RegistrosAuditoria` | Tiene una fila por cada alta, cambio y baja hechos en la demostración |
| 27 | Entrar en la app Android | Inicia sesión contra la misma API y muestra `No hay reparto descargado` |

Si uno de estos 27 falla, el Sprint 1 no está terminado. Los críticos, los que el docente va a mirar sí o sí porque están escritos en el criterio de validación del Excel, son el **14**, el **18**, el **22** y el **23**.

---

## 11. Lo que no se debe hacer

Esta lista existe porque son los errores que arruinarían la coherencia con los modelos ya entregados o con la nota.

1. **No inventar entidades, atributos ni estados.** Si hace falta un dato que no está en el diccionario de 41 clases, se anota como pendiente y se consulta; no se agrega por cuenta propia.
2. **No cambiar los nombres del diccionario** al inglés ni a otra forma. `ClasificacionProducto` no es `ProductCategory`.
3. **No poner lógica de negocio en los controladores.** El controlador recibe, valida el modelo, llama al servicio y devuelve. Las reglas viven en `Servicios/`.
4. **No poner acceso a datos en SGCPuiweb.** Ni EF Core, ni cadena de conexión, ni SQL.
5. **No usar los DTO de la API como modelo de una vista.** Siempre un ViewModel.
6. **No borrar filas.** Desactivar.
7. **No confiar en la interfaz para autorizar.** Ocultar un botón no es un permiso.
8. **No dejar comentarios explicativos en el código.** Los nombres tienen que alcanzar. La única excepción son los `<summary>` de los endpoints, que Swagger necesita para documentar la API.
9. **No incluir texto generado automáticamente, marcas de herramientas de IA, emojis en el código ni mensajes de commit con atribución a herramientas.** El trabajo lo firma el equipo.
10. **No subir** `bin`, `obj`, `.vs`, `*.user`, `appsettings.Development.json`, archivos `.db`, ni `local.properties` o `build/` en Android. Configurar el `.gitignore` antes del primer commit de código.
11. **No subir secretos.** La clave de firma del JWT va en `appsettings.Development.json` fuera del repositorio o en variables de entorno. En `appsettings.json` solo queda el nombre de la clave y un valor de ejemplo evidente.
12. **No adelantar sprints.** Nada de inventario, existencias, reservas, producción, pesajes, sanidad, frío, pagos, crédito, transporte, entregas, reportes ni exportación a PDF o Excel, aunque parezca fácil. Lo que sobra también resta: la rúbrica mira coherencia con lo planificado, y el Excel dice en qué sprint va cada cosa.
12.b **No implementar `CargoPedido` ni separar cargo de producto y servicio.** Es RF-20, Sprint 2. En las pantallas de cotización y pedido, el servicio de faeneo es un texto informativo copiado del mockup.
13. **No activar alertas de inactividad (RF-09), sugerencia de reposición (RF-16) ni priorización automática (RF-21).** Están fuera de alcance por decisión documentada.
14. **No simular la respuesta de un proveedor fiscal.** RF-11 depende de una integración que todavía no está confirmada.
15. **No inventar números en el resumen del negocio.** Si un indicador no se puede calcular con los datos del sprint, se muestra el aviso de que llega después.

---

## 12. Datos iniciales

La migración inicial siembra lo mínimo para que el sistema se pueda usar y demostrar. Los importes y nombres de catálogo son **ilustrativos y pendientes de validación comercial**; eso ya está dicho en la documentación del proyecto y conviene repetirlo en la presentación.

**Permisos**: los trece de la sección 5.7.

**Roles**: los seis de la sección 5.8, con sus permisos.

**Usuario administrador**: login `admin`, nombre `Administración`, rol `ADMINISTRACION`, estado `ACTIVO`. La clave inicial se define en `appsettings.Development.json` con la clave `DatosIniciales:ClaveAdministrador`; si falta, la aplicación no siembra el usuario y registra el motivo. **No dejar una contraseña escrita en el código ni en el repositorio.**

**Clasificaciones de ejemplo**:

| Código | Nombre | Familia |
|---|---|---|
| CLS-001 | Costilla | CARNE_FRESCA |
| CLS-002 | Lomo | CARNE_FRESCA |
| CLS-003 | Jamón elaborado | DERIVADO |
| CLS-004 | Sal de cura | INSUMO |

**Productos de ejemplo**:

| Código | Nombre | Clasificación | Presentación | Unidad |
|---|---|---|---|---|
| PRD-001 | Costilla de cerdo | CLS-001 | Pieza | kg |
| PRD-002 | Lomo de cerdo | CLS-002 | Pieza | kg |
| PRD-003 | Jamón elaborado | CLS-003 | Pieza | kg |

**Clientes de ejemplo**: `Restaurante El Patio` (tipo Restaurante, condición CREDITO_ACORDADO) y `Chicharronería Doña Rosa` (tipo Chicharronería, condición CONTADO). Son los que aparecen en los mockups, así que la demostración coincide con lo diseñado.

Precios: no se siembran. Cargarlos en vivo es parte de la demostración, y es lo que permite mostrar el criterio 23: cambiar el precio después de confirmar el pedido y comprobar que el margen no se mueve.

Cotizaciones y pedidos: tampoco se siembran, por el mismo motivo. Se crean durante la presentación siguiendo el ejemplo del backlog: 4 kg de costilla a Bs 35/kg con costo Bs 28/kg, que da Bs 28 de margen.

**Códigos.** El generador arranca en 1, así que la demostración producirá `COT-001` y `PED-001`. Los mockups dicen `COT-028` y `PED-042` porque son datos ilustrativos; no hay que forzar esos números ni sembrar registros falsos para que coincidan. Si alguien lo pregunta en la defensa, esa es la respuesta.

---

## 13. README de cada repositorio

Los tres repositorios necesitan un `README.md` con: nombre y descripción, los cuatro integrantes con su usuario de GitHub, requisitos, pasos para ejecutar, cómo crear la base de datos, y qué entra en el Sprint 1. En SGCPapi se agrega la URL de Swagger y la tabla de endpoints. En SGCPuiweb, la clave `Api:UrlBase` y la advertencia de que la API debe estar levantada primero.

---

## 14. Resumen para quien genera el código

Lo mínimo que hay que respetar, en una página:

- **El alcance sale del Excel**, no de esta guía: RF-01, RF-02, RF-03, RF-10, RF-12 y RF-13, más la parametrización de RF-04, más RNF-02 y RNF-04. Es decir CU01, CU02, CU03, CU04, CU05, CU06 y CU07.
- **Dos aplicaciones .NET 10**: `SGCPapi` Web API con controladores y EF Core; `SGCPuiweb` MVC sin acceso a datos, que solo consume la API con `HttpClient` tipado. Más la base técnica de Android en Kotlin.
- **Catorce entidades**, con los nombres exactos del diccionario y `Guid` como identificador: Permiso, Rol, Usuario, Sesion, RecuperacionAcceso, RegistroAuditoria, Cliente, ClasificacionProducto, Producto, PrecioProducto, Cotizacion, DetalleCotizacion, Pedido, DetallePedido.
- **Ocho enumeraciones**, guardadas como texto: EstadoUsuario, FormaPago, TipoProducto, CanalSolicitud, EstadoCotizacion, EstadoComercial, EstadoPreparacion, EstadoDetalle.
- **El único atributo agregado al modelo** es `Codigo` en `Cotizacion` y en `Pedido`. Hay que reflejarlo en el diccionario y en el `.mdj` antes de entregar.
- **Las dos reglas que definen el sprint**: una cotización rechazada o vencida no crea pedido; y el precio y el costo acordados quedan congelados en el pedido, de modo que cambiar el catálogo no mueve el margen histórico.
- **JWT con permisos** en los claims; políticas en la API; cookie en la web.
- **Un patrón**: Builder, con `PedidoBuilder` y `ServicioConfirmarPedido`, con los nombres del UML. Facade, Strategy, Command y State son del Sprint 3; Factory Method y Adapter, del Sprint 4. **Ninguno de esos seis se escribe ahora.**
- **Diseño** según los mockups: barra lateral de doce entradas con las de sprints siguientes deshabilitadas, Bs y unidades siempre visibles, todo en español.
- **Nada de**: entidades inventadas, lógica en controladores, EF Core en la web, borrados físicos, comentarios explicativos, marcas de herramientas, secretos en el repositorio, exportación a PDF o Excel, stock, reservas, pagos ni entregas.
- **Veintisiete criterios de aceptación** en la sección 10. Esa es la definición de terminado.
