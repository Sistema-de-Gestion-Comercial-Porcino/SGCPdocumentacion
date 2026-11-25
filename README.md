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
| `04_Mockups_Balsamiq/` | 72 pantallas editables de web y Android |
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
| v5.1.1 | 2026-11-25 | 5 | Documentación: guía «Prueba integral del Sprint 2 del SGCP» en Word (APA), en `00_Definicion/Prueba_integral_Sprint2_SGCP.docx`: 50 pasos por perfil para RF-04, RF-18, RF-17, RF-20, RNF-03 y RNF-06 con el resultado esperado de cada uno, matriz de cumplimiento, pendientes y guion corto de la demostración; generador en `99_Herramientas/sprint2_20261125/` | Dario Haziel Tambo Parra |
| v5.1.0 | 2026-11-25 | 5 | Documentación: revisión integral de los sprints contra el código y reparto final entre tres integrantes (`00_Definicion/Revision_integral_y_reparto_final.md`); CU05 alineado con SGCPapi: secuencia, colaboración y actividad nombran `POST cotizaciones/solicitudes` y `PUT cotizaciones/{id}/solicitud`, objetos de CU05 con el permiso `cotizaciones.solicitar`, `Cotizacion.vigenteHasta` 0..1 (opcional en BORRADOR) en todos los modelos; PDF de CU05 y de clases regenerados con `render_mdj`; script en `99_Herramientas/cu05_20261125/` | Dario Haziel Tambo Parra |
| v4.1.10 | 2026-11-23 | 4 | Documentación: dinámica «Agilidad en acción» de la Clase XXVIII resuelta con el SGCP (12 principios con ejemplos del proyecto, matriz de análisis, simulación de dos sprints con el cambio a QR y móvil, tribunal ágil, reflexión y factores humanos) en Word (APA), en `02_Ingenieria_de_Software/Dinamicas/`; generador en `99_Herramientas/agilidad_20261123/` | Dario Haziel Tambo Parra |
| v4.1.9 | 2026-11-20 | 4 | Documentación: se agregan la especificación de requerimientos ASA1 (Word y PDF), la lista de integrantes y el ZIP de entrega de SGCPapi de Web III | Dario Haziel Tambo Parra |
| v4.1.8 | 2026-11-20 | 4 | Documentación: recorrido de pruebas de los sprints 1 a 4 en Word (APA), con las 213 comprobaciones ejecutadas el 20 de noviembre sobre `main` (API contra MySQL 8.4, web y Android), su cruce con los criterios del Backlog y lo que queda sin medir; generador en `99_Herramientas/pruebas_20261120/` | Dario Haziel Tambo Parra |
| v4.1.7 | 2026-11-20 | 4 | Documentación: diagramas alineados con SGCPapi. Clases con los nombres de la API (CondicionPago, Cargo, InsumoProduccion, EvidenciaRecepcion, Recepcion; nuevas Sena y EntradaInventario; sin FaeneoDesposte, FabricacionDerivado ni Ubicacion) y operaciones tomadas de los servicios reales; SeguimientoCobro con sus operaciones de SGCPapi v4.3.0 y estado RESUELTA de Incidencia (v4.3.2). Estados, objetos, mensajes de secuencia/colaboración/actividad, componentes, despliegue y DER (40 entidades, 63 relaciones) rehechos con el modelo nuevo. Casos de extensión numerados CU13–CU15 con sus diagramas de secuencia, actividad, colaboración y objetos. Balsamiq con el menú real de la web y pantallas de Señas, Rutas, Conflictos de recepción, Auditoría, CU13 y CU14. PDF regenerados con `99_Herramientas/render_mdj` (84 diagramas, sin la exportación de StarUML) | Dario Haziel Tambo Parra |
| v4.1.6 | 2026-11-19 | 4 | Documentación: casos de uso rehechos con un solo actor por rol (Superadministrador, Propietario, Administrador, Finanzas, Ventas, Comprador, Producción, Almacén, Responsable de entrega) y con las secciones del menú en cada caso; roles nuevos llevados a colaboración, secuencias, actividades, objetos, estados y BPMN propuesto; `tipoDocumento` en Cliente | Dario Haziel Tambo Parra |
| v4.1.5 | 2026-11-19 | 4 | Corrección: el PDF de evidencias de `WebIII` (y el que va dentro del ZIP) lleva cada captura de Swagger a página completa en A4; se agrega su fuente `.docx` | Dario Haziel Tambo Parra |
| v4.1.4 | 2026-11-19 | 4 | Documentación: carpeta `WebIII` con el ZIP de entrega de SGCPapi (sin `bin`, `obj` ni `.vs`), el PDF de evidencias y la guía de cumplimiento de la rúbrica | Dario Haziel Tambo Parra |
| v4.1.3 | 2026-11-18 | 4 | Corrección: las guías vigentes (ejecución, Docker, método de verificación, entrega P1 y repartos) usan `dotnet ef ... --context SgcpContext`, necesario desde que SGCPapi tiene también el contexto de SQL Server | Dario Haziel Tambo Parra |
| v4.1.2 | 2026-11-18 | 4 | Documentación: reparto de la tarea «API Integrador» de Web III por integrante, con criterios de la rúbrica, ramas, versiones y plazo interno, en `Reparto_del_SGCP/WebIII_API_Integrador/` | Dario Haziel Tambo Parra |
| v4.1.1 | 2026-11-17 | 4 | Documentación: diagrama entidad-relación en notación de Chen derivado del modelo de clases (41 entidades, 59 relaciones, 259 atributos): vista general y siete hojas por módulo en `.drawio` y PNG, con su generador en `99_Herramientas/der_20261117/` | Dario Haziel Tambo Parra |
| v1.2.0 | 2026-11-14 | 1 | Prueba del APK en un teléfono real (RNF-05): TECNO CK7n con Android 14, acceso correcto por cable y por wifi, con capturas | Angel Sebastian Eguez Mur |
| v4.1.0 | 2026-11-07 | 2, 3 y 4 | Documentación: entrega técnica de la parte de API de P1, decisiones de integración y matriz de reportes propuesta | Dario Haziel Tambo Parra |
| v1.0.1 | 2026-11-07 | 1 | Corrección: el reparto decía seis patrones y la lista oficial tiene siete; el esquema de versiones aclara que MENOR es el número de parte y que la etiqueta de cierre es `vN.4.0` | Dario Haziel Tambo Parra |
| v1.0.0 | 2026-11-06 | 1 | Documentación: reparto del trabajo por sprint e integrante, y convención de versionamiento de los cuatro repositorios | Dario Haziel Tambo Parra |
| v.0.1.0 | 2026-11-06 | 1 | Modelado UML, mockups, definiciones del sistema, planificación del Sprint 1, cambio de motor a MySQL, guía de ejecución y método de verificación | Dario Haziel Tambo Parra |
