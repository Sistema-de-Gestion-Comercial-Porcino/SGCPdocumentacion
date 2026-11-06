# SGCC · entrega reorganizada

[MDJ generales y consolidados](02_Ingenieria_de_Software/Entrega/) · [PDF completo de software](02_Ingenieria_de_Software/PDFentrega/Diagramas_SGCC_Completo.pdf) · [Índice de diagramas](02_Ingenieria_de_Software/00_Documentacion/Indice_entrega.md).

Doce casos de uso generales; 72 diagramas de Ingeniería de Software. Los cinco archivos consolidados reúnen colaboración, objetos, estados, actividades y secuencias. Hay 12 por categoría dependiente de CU y 18 máquinas de estados. Los cuatro diagramas generales son casos de uso, clases, componentes y despliegue. Se añaden dos BPMN horizontales.

Los dos [BPM verticales](01_Proyecto_de_Sistemas/BPM_Vertical/) pertenecen a Proyecto de Sistemas y están separados del PDF conjunto. Total único del proyecto: 74 diagramas; los consolidados y copias no se cuentan otra vez.

[ASA1](<ASA1 - Especificacion de Requerimientos - CRM Chancheria.docx>) conserva su estructura. [Excel actualizado de trabajo](<Formato Proyecto - SGCC Actualizado.xlsx>) mantiene el versionamiento sin cambios; [Excel ya presentado](<Formato Proyecto - SGCC 1 1.xlsx>) se conserva intacto.

[Mockups web y Android](04_Mockups_Balsamiq/SGCC_Web_Android.bmpr): 67 pantallas editables con navegación. [Casos y acciones](00_Definicion/Catalogo_casos_de_uso.md), [equivalencias](00_Definicion/Matriz_trazabilidad.md) y [reglas vigentes](00_Definicion/Reglas_del_sistema.md).

Sprint 1 implementado en tres repositorios: [SGCPapi](SGCPapi/), [SGCPuiweb](SGCPuiweb/) y [SGCPuimovil](SGCPuimovil/). API en ASP.NET Core 10 con EF Core y **MySQL 8**; web en ASP.NET Core MVC con vistas Razor renderizadas en el servidor; móvil en Kotlin nativo. Para levantarlo: [cómo ejecutar el sistema](00_Definicion/Como_ejecutar_el_sistema.md). El cambio de motor a MySQL está en [Cambio_a_MySQL.md](00_Definicion/Cambio_a_MySQL.md), los defectos corregidos en [Errores_encontrados_Sprint1.md](00_Definicion/Errores_encontrados_Sprint1.md) y cómo se verificó en [Metodo_de_verificacion.md](00_Definicion/Metodo_de_verificacion.md).

Catálogo, cantidades, tiempos y precios de los ejemplos son ilustrativos; requieren validación comercial. Web online y Android Kotlin para recepción autorizada/descargada. Prototipos y diagramas son diseño del sistema, no una aplicación ya implementada.
