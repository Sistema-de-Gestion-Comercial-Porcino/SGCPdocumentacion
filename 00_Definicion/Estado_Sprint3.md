# Estado del Sprint 3

Corte del informe: 17 de noviembre de 2026 (Bolivia).

## Implementado

| Repositorio | Qué quedó integrado en `main` | Referencia |
|---|---|---|
| SGCPapi | Pagos, señas, crédito, saldos, rutas, despachos, recepciones y sincronización. | Commit `c87f823` (entrega de la API de los sprints 2 a 4). |
| SGCPuiweb | Pantallas de cobranza, transporte y entregas. | PR #2, merge `8745911`. |
| SGCPuimovil | Descarga de entregas, captura de recepciones sin conexión y sincronización. | PR #1, merge `fe8cbd8`. |

## Verificado y entorno

- **API.** El 11 de noviembre, V3-01 a V3-04 cumplieron contra la API con MySQL 8.0 mediante el verificador del proyecto. Se comprobaron la recepción pendiente, la confirmación de entregas conformes, el tratamiento de recepciones observadas, el reintento sin duplicados, el conflicto de versión y la independencia del saldo respecto de la entrega. La configuración regional de esa corrida quedó sin registrar. [Validación del Sprint 3](Validacion_Sprint3.md).
- **Configuración regional.** La entrega técnica registra otra corrida automatizada en MySQL Community 8.4, en un contenedor temporal, con `LANG=es_BO.UTF-8` y `LANG=C`. En ambas pasaron las 89 comprobaciones conjuntas de los sprints 2 a 4. [Entrega técnica de la API](Entrega_P1_Sprints234.md).
- **Android físico.** La evidencia disponible corresponde al inicio de sesión con el APK del Sprint 1 en un TECNO CK7n con Android 14, conectado a la API con MySQL 8.0.30. [Prueba del APK en teléfono](Prueba_APK_Telefono_RNF05.md).

## Pendiente de verificar

- **Recorrido web completo.** Registrar un pago y comprobar que el estado de la entrega se conserva. Confirmar una recepción y comprobar que el saldo se mantiene.
- **Android sin conexión.** Probar en teléfonos físicos la descarga de una entrega asignada, la captura en modo avión y la sincronización al recuperar la conexión. Comprobar el reintento y el conflicto de versión desde la app. Para RNF-05 queda pendiente la prueba en el segundo modelo, Redmi Note 11 con Android 13.
- **Cierre del sprint.** La etiqueta `v3.4.0` queda pendiente.

Al ejecutar las pruebas, registrar la fecha, las versiones probadas, el entorno de la API, el modelo y la versión de Android cuando corresponda, la configuración regional, el resultado y el enlace a la evidencia.
