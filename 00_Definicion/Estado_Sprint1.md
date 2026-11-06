# Estado del Sprint 1 — 6 de noviembre de 2026

Implementación local en los tres repositorios. No se hicieron commits ni push; no se añadieron firmas de coautor. El motor es MySQL 8; el recorrido se verificó contra MySQL 8.4 en una base desechable.

## Implementado

- SGCPapi: CU01–CU07, JWT y sesiones revocables, permisos, registro público comprador, recuperación local/SMTP configurable, usuarios, clientes, clasificación de cortes/derivados, productos, costos/precios versionados, cotizaciones, pedidos y Builder. MySQL como proveedor de la aplicación.
- SGCPuiweb: MVC, ViewModels separados, clientes HTTP, cookies, antiforgery, formularios y listados de los módulos del sprint, portal comprador con permisos, cotizaciones y pedidos; presentación responsiva.
- SGCPuimovil: Kotlin, Retrofit/OkHttp, acceso online, token cifrado con Android Keystore, renovación y cierre, pantalla vacía de entregas. APK compilado en `SGCPuimovil/app/build/outputs/apk/debug/app-debug.apk`.

## Verificado

- API y web compilan sin errores ni advertencias.
- API: 27 comprobaciones HTTP correctas sobre SQLite temporal aislado. Incluye cotización rechazada/vencida, unicidad de pedido, conservación de precio/margen, privacidad, recuperación y revocación.
- Web: 12 pantallas abiertas, recorrido real con la API de pruebas: acceso → cliente → costo/precio → cotización → presentación → aceptación → pedido. Margen de Bs 28 comprobado. Navegación móvil sin desbordamiento y sin errores JavaScript. Capturas revisadas.
- Android: `assembleDebug` y `testDebugUnitTest` correctos; 4 pruebas. Compilado con JDK completo 21 y SDK Android 36. No se ejecutó en teléfono ni emulador.
- Migración inicial generada con el proveedor MySQL de Oracle, aplicada dos veces contra MySQL 8.4 y con comprobación de ausencia de cambios pendientes en el modelo EF. El script del repositorio es el plano: `--idempotent` genera sintaxis de T-SQL que MySQL rechaza. Relaciones en cascada limitadas a propietarios; índices únicos en códigos, versiones, pedido por cotización y vigencia abierta.

## Pendiente real antes de declarar el sprint validado

1. ~~Ejecutar contra el motor real.~~ **Cerrado.** La migración se aplicó dos veces contra MySQL 8.4 en una base desechable, sin cambios pendientes en el modelo, y las 27 comprobaciones pasaron por HTTP sobre ese motor. Quedan disponibles `.github/workflows/sprint1-mysql.yml` para GitHub Actions y `scripts/Verificar-MySql.ps1` para otra máquina. Lo único que ninguna prueba de acá cubre son los permisos y la versión del MySQL que use el equipo en la presentación.
2. Instalar el APK en un teléfono y comprobar login contra la API del equipo. La URL es configurable en el acceso. No correr un emulador pesado en esta laptop.
3. Medir desempeño/usabilidad con usuarios representativos según el criterio acordado; no se fabricó esa evidencia.
4. Recuperación de producción: configurar SMTP real. En desarrollo, los mensajes están en una carpeta privada local, no se devuelven al solicitante anónimo.

## Documentación y modelos

Actualizados `Clases_SGCC.mdj` de generales y entrega, PDF individual de clases y diccionario: `Permiso.id`, códigos, motivo de respuesta, motivo de cancelación y relación de versiones. La guía Markdown incluye correcciones inmediatas y la decisión de MySQL.

Aún pendientes: Word/PDF de la guía de Claude, ASA1 y arquitectura/componentes/despliegue con los nombres tecnológicos concretos; secuencias/actividades afectadas por las precisiones de versiones y confirmación; reemplazar la página de clases dentro del PDF combinado. No regenerar los demás diagramas por rutina. Los documentos anteriores conservan el diseño general futuro y no son evidencia de funciones ya implementadas.

## Arranque para entrega

Seguir los README de cada repositorio, o la guía `Como_ejecutar_el_sistema.md`. En la máquina con acceso a MySQL:

```text
SGCPapi: scripts/Preparar-Desarrollo.ps1 (PowerShell 7), luego dotnet run --project src/SGCP.Api
SGCPuiweb: configurar Api:UrlBase, luego dotnet run --project src/SGCP.Web
Android: instalar app-debug.apk y configurar http(s)://IP_API:PUERTO/api/v1/
```

La base de pruebas local es efímera y no se entrega como base del sistema. La aplicación principal no permite seleccionar SQLite.

## Continuidad técnica

Herramientas de verificación en `99_Herramientas/sprint1/`. JDK local: `~/.cache/sgcp-herramientas/java-home.txt`. SDK Android existente: `~/.android-docker/sdk`. Gradle un trabajador/768 MB. Las herramientas descargadas no están en los repositorios. El verificador de navegador está guardado como referencia; usa credenciales solo de la base temporal, nunca productivas.

Los servidores locales de pruebas se detuvieron al cerrar la verificación para liberar memoria.
