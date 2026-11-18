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
- [Levantar con Docker](00_Definicion/Levantar_con_Docker.md) · la base en contenedor, con operación diaria, reinicio limpio y solución de fallas
- [Cambio a MySQL](00_Definicion/Cambio_a_MySQL.md) · qué se cambió al dejar SQL Server y las tres trampas de MySQL
- [Errores encontrados en el Sprint 1](00_Definicion/Errores_encontrados_Sprint1.md) · defectos corregidos, con su causa
- [Método de verificación](00_Definicion/Metodo_de_verificacion.md) · cómo se comprueba que funciona

## Control de versiones

Formato `vMAYOR.MENOR.PARCHE`, donde **MAYOR es el número de sprint**:

| Posición | Significado | Ejemplo |
|---|---|---|
| MAYOR | número de sprint. `0` es el trabajo anterior a la primera entrega | `v2.4.0` pertenece al Sprint 2 |
| MENOR | número de parte del reparto: P1, P2, P3 o P4 | `v2.1.0` es la parte 1 del Sprint 2 |
| PARCHE | corrección sobre esa misma parte, sin agregar funcionalidad | `v2.1.1` |

Los cuatro repositorios comparten MAYOR y MENOR, porque el sprint y la parte son los mismos para todos; el PARCHE avanza por separado en cada repositorio.

**La etiqueta de cierre de un sprint es `vN.4.0`**, la versión del commit de P4, que es siempre el último. Desde el Sprint 2 no se crea `vN.0.0`: quedaría por detrás de versiones ya entregadas. El Sprint 1 conserva su `v1.0.0` porque se entregó en un solo bloque.

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
| v4.1.2 | 2026-11-18 | 4 | Documentación: reparto de la tarea «API Integrador» de Web III por integrante, con criterios de la rúbrica, ramas, versiones y plazo interno, en `Reparto_del_SGCP/WebIII_API_Integrador/` | Dario Haziel Tambo Parra |
| v4.1.1 | 2026-11-17 | 4 | Documentación: diagrama entidad-relación en notación de Chen derivado del modelo de clases (41 entidades, 59 relaciones, 259 atributos): vista general y siete hojas por módulo en `.drawio` y PNG, con su generador en `99_Herramientas/der_20261117/` | Dario Haziel Tambo Parra |
| v1.2.0 | 2026-11-14 | 1 | Prueba del APK en un teléfono real (RNF-05): TECNO CK7n con Android 14, acceso correcto por cable y por wifi, con capturas | Angel Sebastian Eguez Mur |
| v4.1.0 | 2026-11-07 | 2, 3 y 4 | Documentación: entrega técnica de la parte de API de P1, decisiones de integración y matriz de reportes propuesta | Dario Haziel Tambo Parra |
| v1.0.1 | 2026-11-07 | 1 | Corrección: el reparto decía seis patrones y la lista oficial tiene siete; el esquema de versiones aclara que MENOR es el número de parte y que la etiqueta de cierre es `vN.4.0` | Dario Haziel Tambo Parra |
| v1.0.0 | 2026-11-06 | 1 | Documentación: reparto del trabajo por sprint e integrante, y convención de versionamiento de los cuatro repositorios | Dario Haziel Tambo Parra |
| v.0.1.0 | 2026-11-06 | 1 | Modelado UML, mockups, definiciones del sistema, planificación del Sprint 1, cambio de motor a MySQL, guía de ejecución y método de verificación | Dario Haziel Tambo Parra |
