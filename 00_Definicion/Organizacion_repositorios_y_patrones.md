# Organización del proyecto SGCP

Nombre actual: Sistema de Gestión Comercial Porcino (SGCP). SGCC es la denominación anterior del mismo alcance.

- SGCPapi: API, reglas, autorización, transacciones, base central y reportes.
- SGCPuiweb: web responsiva online para gestión y comprador.
- SGCPuimovil: Android Kotlin; captura de recepciones descargadas y autorizadas, con sincronización posterior.

Ambos clientes consumen la misma API. Ninguno accede directamente a la base central. Tres repositorios no implican microservicios. Las carpetas locales se mantienen vacías hasta inicializar los proyectos.

Patrones seleccionados en esta entrega: Adapter y Facade en la API; Command y State en Android; Strategy en la API para la condición comercial del despacho. Complementan Factory Method y Builder. Los restantes diagramas son ejemplos externos, sin ampliar las funciones del negocio.

La API conserva permisos, versión, restricciones únicas e idempotencia. Crédito no liquida deuda; sincronización confirmada no implica recepción conforme. No se añaden alertas, sensores, costeo automático ni operaciones comerciales offline.
