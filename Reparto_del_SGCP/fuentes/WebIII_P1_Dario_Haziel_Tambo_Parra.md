# Web III · Parte 1 · Dario Haziel Tambo Parra

Código: **W3-P1**. Repositorio: **SGCPapi**. Usuario de GitHub: `SuperGenio56`.

## Lo que ya está hecho

### 1. SQL Server como motor elegible · PR SGCPapi#3 (v4.1.2)
- `BaseDatos:Proveedor` = `SqlServer` o `MySql`; el valor por defecto sigue siendo MySql, así que no rompe la web, Android ni el CI.
- `SgcpContextSqlServer` con su propia migración, `InicialSqlServer`, de 41 tablas, y el script idempotente `database/EsquemaSqlServer.sql`.
- Manejo de interbloqueos de SQL Server (errores 1205 y 1222, que responden 409).
- El verificador acepta `SGCP_SQLSERVER_TEST`, y hay un flujo de CI que levanta SQL Server 2022, aplica la migración y corre todas las pruebas.
- Sección «Usar SQL Server en lugar de MySQL» en el README: conexión de ejemplo sin credenciales, migraciones, datos de prueba y Swagger.

### 2. Huecos que pidió la web · PR SGCPapi#2 (v4.1.1)
- Versión de la entrega en `GET recepciones/conflictos` y en `GET recepciones/{id}`.
- Columna con el id de la entrega en el reporte ENTREGAS.
- Endpoint `GET pedidos/{pedidoId}/constancia`.
- 11 pruebas nuevas con una cuenta VENTAS.

### 3. Antes de esta tarea
Toda la API de los Sprints 1 a 4: modelo, migraciones de MySQL, seguridad, servicios y verificador de 116 comprobaciones.

## Lo que falta: integrar (jueves 19)

1. Revisar y comentar los PR de P2, P3 y P4. No los fusiona Dario si es coautor de algo; los fusiona otro integrante.
2. Con todo en `main`, correr el verificador en MySQL y confirmar que el CI de SQL Server esté en verde.
3. Generar el ZIP con el script de P3, revisar que no tenga `bin`, `obj`, `.vs`, secretos ni `appsettings.Development.json` con credenciales, y subirlo a Teams antes del viernes a las 07:00.
4. Si alguna parte no llegó el miércoles a las 24:00, hacerla el jueves y registrarlo en el Historial.
