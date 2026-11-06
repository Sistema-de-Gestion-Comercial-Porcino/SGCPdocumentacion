# Trazabilidad y equivalencias

| Caso vigente | Referencias anteriores | RF |
|---|---|---|
| CU01 Gestionar acceso | CU01 | RF12 |
| CU02 Administrar usuarios | CU02 | RF13 |
| CU03 Gestionar clientes | CU03 | RF10 |
| CU04 Gestión de costos | CU04 | RF02, RF03 |
| CU05 Gestión de cotizaciones | CU05, CU25 | RF01, RF02 |
| CU06 Gestionar pedidos | CU06, CU13, CU26 | RF01, RF03, RF05, RF19 |
| CU07 Gestionar productos | CU24 | RF02, RF04 |
| CU08 Gestionar producción | CU08, CU09, CU10, CU11 | RF04, RF18, RF20 |
| CU09 Gestionar inventario | CU07, CU12 | RF04 |
| CU10 Gestionar pagos y cobranza | CU14, CU15, CU16, CU17, CU18, CU19 | RF05, RF06, RF11, RF19, RF20 |
| CU11 Gestionar transporte y entregas | CU20, CU21, CU22 | RF07, RF08, RF14, RF17, RNF01 |
| CU12 Gestionar reportes |  | RF15 |

Cada CU vigente posee un diagrama de secuencia, actividad, colaboración y objetos. Las máquinas de estados describen entidades con ciclo de vida; no se obliga a crear una por cada menú. Clases, casos de uso, componentes y despliegue son generales.

Los reportes consultan datos de los módulos: producción por producto/corte/derivado, pedidos, clientes, inventario, pagos y entregas. RF15 agrupa las consultas y la exportación; RF04 cubre catálogo y producción. Las exportaciones vuelven a validar permisos.

Los RF mantienen sus identificadores: 21 RF y 6 RNF. No existe correspondencia obligatoria de un RF con un solo CU. CU23 anterior (alertas) no se conserva como caso activo.

| Etapa | Acciones |
|---|---|
| Parametrización | Usuarios, clientes, clasificaciones, productos, costos; animales, ubicaciones y transportes en sus módulos. |
| Operación | Cotización aceptada, pedido, preparación, producción, stock, pagos, transporte y entrega. |
| Reportes | Filtros y exportación de información autorizada; comprador únicamente sus datos. |
