# Herramientas de mantenimiento

- `exportar_entrega_final.js`: exporta los MDJ existentes sin modificarlos. Genera 128 PDF individuales y el PDF completo con marcadores en `02_Ingenieria_de_Software/PDFentrega`. `SGCC_ENTREGA_STAGE` permite preparar otra carpeta; `SGCC_ENTREGA_MANIFEST` define el informe fuera de la entrega. No duplica los diagramas de los cinco MDJ consolidados.
- `bpm_vertical_actualizado.js`: adapta las reglas del BPMN vigente a dos BPM verticales con actores en columnas. `SGCC_VERTICAL_STAGE` define la carpeta temporal de salida; genera MDJ y PDF vectoriales. `validar_bpm_vertical.py` verifica referencias, recorridos, decisiones y geometría.
- `bpmn_legible.js`: genera los dos BPMN horizontales en una carpeta temporal definida por `SGCC_BPMN_STAGE`; un proceso y una lámina por modelo, con ocho tramos y eventos de enlace. Usa `rutas_bpmn_limpias.js` para separar las flechas y los rótulos.
- `especificacion_v3.js`: catálogo CU01–CU26 y reglas de stock. CU23 es futuro.
- `generar_v3.js`: origen de secuencias y actividades. No ejecutar su entrada completa sobre la entrega: también contiene la construcción anterior de BPM/BPMN, sustituida por `bpmn_legible.js`.
- `v4/generar.js`: origen de generales, colaboración, objetos y estados. No regenerar los generales aprobados sin incorporar las ediciones manuales del usuario, especialmente casos de uso.
- `v4/documentar.js` y `documentar_v3.js`: diccionario, catálogo y trazabilidad. Los índices vigentes de PDF están en `00_Documentacion/Indice_entrega.md`.
- `unificar_mdj.py`: reconstruye los cinco consolidados desde los individuales y sincroniza sus copias de Entrega. Conserva acceso directo a diagramas de colaboración y estados.
- `v4/validar.py`: verifica notación, referencias, instancias, estados y geometría; `SGCC_VALIDATION_REPORT` permite una salida temporal.
- `balsamiq/generar_mockups.py`: BMPR nativo con navegación.

Se utiliza el motor instalado de StarUML con `ELECTRON_RUN_AS_NODE=1`. Los PDF de revisión de generadores se redirigen mediante `SGCC_PREVIEW_DIR`; para publicar se usa exclusivamente `exportar_entrega_final.js`. La actualización de BPM verticales se publica exclusivamente en Proyecto de Sistemas. ASA1, los Excel, Balsamiq y la entrega de Software no se modifican. Los informes técnicos quedan en `02_Ingenieria_de_Software/00_Documentacion`, fuera de las carpetas de entrega.
