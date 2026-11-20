# Web III · API Integrador

Entrega en Teams: vence el **20 de noviembre de 2026 a las 07:00**.

## Qué se sube

| Archivo | Contenido |
|---|---|
| `SGCPapi_API_Integrador.zip` | Proyecto completo de la Web API (`SGCPapi`) con sus migraciones de SQL Server y de MySQL, el README de entrega y el PDF de evidencias en `docs/`. Se generó con `git archive`, así que no lleva `bin`, `obj` ni `.vs`. |
| `Evidencias_API_Integrador.pdf` | La misma copia que va dentro del ZIP, por si la quieren revisar sin descomprimir. |

En Teams basta con subir el ZIP. El PDF va adentro (`SGCPapi/docs/Evidencias_API_Integrador.pdf`).

El ZIP sale de la rama `webiii/p1-entrega` de SGCPapi (commit `v4.1.3`), que parte de `main` con los PR #5 y #6 de Victor ya integrados. Compila sin advertencias (`dotnet build -c Release -warnaserror`).

## Cumplimiento de la rúbrica

| Criterio | Dónde está |
|---|---|
| Modelo relacional y SQL Server | Entidades en `src/SGCP.Api/Dominio`, configuraciones en `Datos/Configuraciones`, migración `Datos/MigracionesSqlServer/20261118035108_InicialSqlServer` y `database/EsquemaSqlServer.sql` |
| Datos de prueba y persistencia | Siembra con `DatosIniciales:Ejemplos`; pruebas 12a y 12b del PDF (GET 200 antes y después de reiniciar) |
| Listado y consulta por id | `GET clientes` y `GET clientes/{id}`; pruebas 2 y 4 |
| POST con 201 y Location | `POST clientes`; prueba 3 |
| PUT y DELETE | Pruebas 7, 10 (409, regla del dominio), 11 (204) y 11b (404) |
| Recurso relacionado | `GET clientes/{id}/pedidos`; prueba 8 |
| DTO y organización | `Contratos/Peticiones`, `Contratos/Respuestas`, `Controllers`, `Servicios` y `Datos`; contexto inyectado y operaciones asíncronas |
| Validación y errores | Pruebas 5 (400 por campo obligatorio), 6 (400 por referencia inválida) y 9 (404) |
| Swagger | Prueba 0 y anotaciones `ProducesResponseType` en los controladores |
| README | Sección «Entrega Web III · API Integrador» al inicio del README de SGCPapi |
| Participación en Git | Commits de SuperGenio56, VictorManrique01 y sebaxtianmur89 en SGCPapi. Sofía (sof1345) figura como integrante, sin commits en ese repositorio |

## Antes de subir

1. Hacer push de la rama `webiii/p1-entrega` de SGCPapi, abrir el PR y que otro integrante lo apruebe y lo fusione a `main`. Así el README y el PDF del ZIP quedan también en el repositorio.
2. **El repositorio SGCPapi es privado.** El docente tiene que poder revisarlo: agréguenlo como colaborador con permiso de lectura (o a la organización), o hagan público el repositorio.
