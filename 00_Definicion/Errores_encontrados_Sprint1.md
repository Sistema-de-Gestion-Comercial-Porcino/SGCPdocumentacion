# Errores encontrados y corregidos en el Sprint 1

Revisión del 6 de noviembre de 2026 sobre la implementación de los tres repositorios. Todo lo que figura aquí **ya está corregido**. Se documenta porque son errores que vuelven a aparecer en los sprints siguientes si no se conoce la causa.

El método que los encontró está en `Metodo_de_verificacion.md`. El cambio de motor a MySQL está en `Cambio_a_MySQL.md`, con sus propias tres trampas. Ninguno de los tres aparecía al compilar, ni en la revisión del código, ni en la batería de 27 comprobaciones original.

## 1 · La API devolvía 500 en toda petición con decimales

**Gravedad: bloqueante.** El sistema era inusable en las máquinas del equipo.

Con la configuración regional en español, abrir una vigencia de precio, crear una cotización o confirmar un pedido devolvía `HTTP 500`:

```
System.ArgumentException: 0.01 is not a valid value for Decimal. (Parameter 'value')
 ---> System.FormatException: The input string '0.01' was not in a correct format.
       at System.ComponentModel.DataAnnotations.RangeAttribute.SetupConversion()
```

**Causa.** `RangeAttribute` convierte sus límites, que están escritos como texto, usando `CultureInfo.CurrentCulture`. En `es-BO` y `es-ES` el separador decimal es la coma, de modo que `"0.01"` no se puede convertir y el atributo lanza durante la validación del modelo. El valor que mande el cliente es indiferente: el atributo falla al construirse.

**Corrección.** Ocho atributos, en `SGCPapi/.../Contratos/Peticiones/Peticiones.cs` y `SGCPuiweb/.../Models/ViewModels/ViewModels.cs`:

```csharp
[Range(typeof(decimal), "0.01", "9999999999.99",
       ParseLimitsInInvariantCulture = true, ConvertValueInInvariantCulture = true)]
```

**Regla para adelante.** Todo `Range` con `typeof(decimal)` y límites en texto lleva las dos propiedades. Lo más seguro en los sprints siguientes es no usar límites en texto: validar el rango dentro del servicio, donde la cultura no interviene.

## 2 · La web guardaba los importes multiplicados por cien

**Gravedad: crítica, y peor que la anterior**, porque no producía ningún error. Un precio de Bs 88,50 se guardaba como Bs 8850 y la pantalla no avisaba nada.

Comprobado enviando el formulario de precios y releyendo el valor desde la API:

```
sin la corrección:  se envía 66.25 / 88.50  ->  se guarda 6625 / 8850
con la corrección:  se envía 55.25 / 77.50  ->  se guarda 55.25 / 77.50
```

**Causa.** Las vistas escriben los valores con `ToString(CultureInfo.InvariantCulture)`, que es lo correcto: `<input type="number">` exige el punto como separador decimal, por especificación de HTML. Pero ASP.NET Core enlaza los campos de formulario con `CultureInfo.CurrentCulture`. En `es-BO` el punto es separador de miles, así que `"35.00"` se interpreta como treinta y cinco mil. Medido:

```
es-BO       separador ','   decimal.TryParse("35.00") = True, valor = 3500
invariante  separador '.'   decimal.TryParse("35.00") = True, valor = 35.00
```

Las dos devuelven `True`. Por eso no hay error: hay un número distinto.

**Corrección.** Dos cambios en `SGCPuiweb`:

- `Models/EnlaceDecimalInvariante.cs`, nuevo: un `IModelBinder` con su proveedor, que lee `decimal` y `decimal?` en cultura invariante.
- `Program.cs`: registro del enlace y `app.UseRequestLocalization()` fijado a `es-BO`.

Se dejó la cultura de la aplicación en `es-BO` a propósito, para que los importes se sigan mostrando `Bs 35,00` con coma, como en el mockup w05, y las fechas largas salgan en español. Lo único que cambia es cómo se **leen** los números del formulario. Fijar la cultura explícitamente además hace que la aplicación se comporte igual en las cuatro laptops, sin depender del idioma de cada Windows.

**Regla para adelante.** Las fechas no necesitaron nada porque los formularios usan `datetime-local` con `asp-format="{0:yyyy-MM-ddTHH:mm}"`, que es ISO y se interpreta igual en cualquier cultura. Conviene mantener ese formato en los campos de fecha que se agreguen.

## 3 · Por qué las pruebas no los vieron

Es la parte importante, porque la batería de 27 comprobaciones estaba bien escrita y aun así pasó en verde con el sistema roto.

```
sin la variable LANG:   CurrentCulture = ''        "35.00" -> 35.00
LANG=es_BO.UTF-8:       CurrentCulture = es-BO     "35.00" -> 3500
```

Cuando `LANG` no está definida —lo habitual en un intérprete de comandos lanzado por una herramienta— .NET usa la cultura invariante y los dos defectos desaparecen. Las pruebas corrían en un entorno que no era el de los usuarios.

**Regla para adelante.** Correr la verificación con `LANG=es_BO.UTF-8 LC_ALL=es_BO.UTF-8`, y repetirla con `LANG=C` para confirmar que el comportamiento no depende de la cultura en ningún sentido.

Y al comprobar un arreglo, verificar en los dos sentidos: que con el arreglo funciona **y** que sin el arreglo falla. Si solo se comprueba lo primero, no se sabe si el arreglo hizo algo.

## 4 · Legibilidad del código

No era un defecto de funcionamiento, pero sí un problema para la defensa oral, que consiste en modificar líneas de código en vivo.

Los servicios, controladores y configuraciones Fluent estaban comprimidos en líneas de hasta **797 caracteres**, con 269 líneas por encima de 160. Las entidades estaban bien; el resto no.

Se aplicó `dotnet format whitespace` con un `.editorconfig` añadido a cada repositorio, y luego se partieron las expresiones largas restantes en los puntos habituales: antes de cada eslabón de una cadena de llamadas, después de las comas de una lista de argumentos o de un objeto anónimo, y antes de `&&` y `||` en las condiciones largas. Las clases de DTO y ViewModel que tenían todas sus propiedades en una línea quedaron con un miembro por línea.

| | Antes | Después |
|---|---|---|
| Líneas de C# sobre 160 caracteres | 269 | 47 |
| Línea de C# más larga | 797 | 560 |
| Línea de vista Razor más larga | 2109 | 754 |
| Líneas de Kotlin sobre 160 caracteres | 16 | 9 |

Las vistas Razor se partieron **solo entre etiquetas de bloque**, donde el navegador ignora el espacio en blanco. No se tocaron los elementos en línea, porque ahí un salto de línea se convierte en un espacio visible. Lo que queda largo es precisamente eso: cadenas de elementos en línea que no se pueden partir sin cambiar lo que se ve.

**Cómo se comprobó que el reformateo no cambió nada:**

- Comparación del código antes y después ignorando todos los espacios: idéntico en todos los archivos salvo el que se editó a propósito.
- Las ocho páginas de la web descargadas antes y después: HTML idéntico, salvo la hora del último acceso, que cambia sola.
- Las once comprobaciones de la API y las nueve de la web, repetidas después del reformateo.
- APK recompilado y pruebas unitarias de Android en verde.

**Regla para adelante.** El `.editorconfig` ya está en los dos repositorios de .NET. Conviene correr `dotnet format` antes de cada entrega, y escribir una sentencia por línea desde el principio: es más barato que reformatear después.

## 5 · Estado de la verificación

Hecho, bajo `LANG=es_BO.UTF-8`, contra MySQL 8.4 en una base desechable:

| Qué | Resultado |
|---|---|
| Compilación de SGCPapi y SGCPuiweb | 0 errores, 0 advertencias |
| `dotnet ef database update` contra MySQL real, dos veces | aplicada, luego «already up to date» |
| `dotnet ef migrations has-pending-model-changes` | modelo y migración sincronizados |
| Las tres reglas de unicidad, probadas en los dos sentidos | 7 de 7 |
| Recorrido completo de la API por HTTP | 27 de 27 |
| El mismo recorrido por la vía SQLite, sin motor instalado | 27 de 27 |
| Páginas de la web y envío del formulario de precios | 9 de 9 |
| APK y pruebas unitarias de Android | correctos |
| Los cuatro pasos del flujo de GitHub Actions, replicados en local | pasan |

Al cambiar de motor se introdujo un cuarto defecto, que apareció en GitHub Actions y no en local: exigir la cadena de conexión también en la fábrica de diseño, que `dotnet ef` usa para construir el modelo sin conectarse. Está corregido y explicado en `Cambio_a_MySQL.md`, sección 2. El motor pasó de SQL Server a MySQL el 6 de noviembre de 2026. Lo que cambió, y las tres trampas que aparecieron al hacerlo, está en `Cambio_a_MySQL.md`. El cambio cerró el pendiente que antes encabezaba esta lista: **la migración ya se ejecutó contra el motor de entrega**, porque un MySQL de prueba se levanta en veinte segundos y SQL Server no.

Pendiente, y no se puede cerrar desde esta máquina:

1. **Instalar el APK en un teléfono** y comprobar el acceso contra la API del equipo. Compila y las pruebas pasan, pero nunca se ejecutó en un dispositivo.
2. **RNF-02 y RNF-04**, desempeño y usabilidad, que se miden con usuarios y un guion acordado. No se puede fabricar esa evidencia.
3. **Aplicar la migración en el MySQL que use el equipo para la presentación.** Está probada contra MySQL 8.4; lo que ninguna prueba de acá cubre son los permisos y la versión del servidor de esa máquina. Si es MySQL 8 y el usuario puede crear tablas, funciona.
