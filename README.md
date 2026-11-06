# SGCPdocumentacion

Documentación del Sistema de Gestión Comercial Porcino: requerimientos, modelado UML, mockups, definiciones del sistema y planificación de sprints. El código vive en los otros tres repositorios de la organización.

El índice completo de la entrega está en [LEEME.md](LEEME.md).

## Equipo

- Dario Haziel Tambo Parra · Desarrollador
- Angel Sebastian Eguez Mur · Desarrollador
- Sofia Cuellar Roca · Product Owner
- Victor Manuel Manrique Arancivia · Scrum Master

## Repositorios del proyecto

| Repositorio | Contenido |
|---|---|
| [SGCPapi](https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPapi) | API ASP.NET Core 10 con EF Core y MySQL 8 |
| [SGCPuiweb](https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPuiweb) | Web ASP.NET Core MVC, consume la API |
| [SGCPuimovil](https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPuimovil) | Aplicación Android en Kotlin |
| SGCPdocumentacion | este repositorio |

## Contenido

| Carpeta | Qué hay |
|---|---|
| `00_Definicion/` | Reglas del sistema, catálogo de casos de uso, matriz de trazabilidad, guías de ejecución y verificación |
| `01_Proyecto_de_Sistemas/` | BPM verticales |
| `02_Ingenieria_de_Software/` | Modelos UML, diagramas y diccionario de clases |
| `04_Mockups_Balsamiq/` | 67 pantallas editables de web y Android |
| `99_Herramientas/` | Utilidades de apoyo |

Documentos de referencia para quien retome la implementación:

- [Cómo ejecutar el sistema](00_Definicion/Como_ejecutar_el_sistema.md) · levantar API, web y Android en orden
- [Cambio a MySQL](00_Definicion/Cambio_a_MySQL.md) · qué se cambió al dejar SQL Server y las tres trampas de MySQL
- [Errores encontrados en el Sprint 1](00_Definicion/Errores_encontrados_Sprint1.md) · defectos corregidos, con su causa
- [Método de verificación](00_Definicion/Metodo_de_verificacion.md) · cómo se comprueba que funciona

## Control de versiones

Formato `vMAYOR.MENOR.PARCHE`, donde **MAYOR es el número de sprint**:

| Posición | Significado | Ejemplo |
|---|---|---|
| MAYOR | sprint entregado. `0` es el trabajo anterior a la primera entrega | `v2.0.0` es el Sprint 2 |
| MENOR | un caso de uso o una funcionalidad terminada | `v1.2.0` |
| PARCHE | corrección que no agrega funcionalidad | `v1.2.1` |

Los cuatro repositorios comparten MAYOR, porque el sprint es el mismo para todos, y avanzan MENOR y PARCHE por separado: no hay que forzarlos al mismo número.

Cada versión de la tabla tiene su etiqueta en git, así que `git show v1.0.0` muestra el estado exacto de esa fila. **La etiqueta se crea después del commit**, nunca antes, o apunta al estado anterior:

```bash
git commit -m "v1.0.0 - Sprint 1"
git tag -a v1.0.0 -m "Sprint 1 entregado"
git push origin main --follow-tags
```

En la columna *Cambio*, los prefijos son fijos para que la tabla se pueda leer de un tirón: `Corrección:`, `Documentación:`, `Infraestructura:`, o nada cuando es funcionalidad nueva. Si el cambio llegó por una rama, la fila termina en `(PR #n)`; la rama en sí no se anota, porque git ya la guarda en el commit de fusión.

Desde `v1.0.0` el prefijo es `v` sin punto, que es la convención y lo que admite una etiqueta de git. Las filas anteriores se conservan como se escribieron.

### Historial

Más reciente arriba.

| Versión | Fecha | Sprint | Cambio | Autor |
|---|---|---|---|---|
| v1.0.0 | 2026-11-06 | 1 | Documentación: reparto del trabajo por sprint e integrante, y convención de versionamiento de los cuatro repositorios | Dario Haziel Tambo Parra |
| v.0.1.0 | 2026-11-06 | 1 | Modelado UML, mockups, definiciones del sistema, planificación del Sprint 1, cambio de motor a MySQL, guía de ejecución y método de verificación | Dario Haziel Tambo Parra |
