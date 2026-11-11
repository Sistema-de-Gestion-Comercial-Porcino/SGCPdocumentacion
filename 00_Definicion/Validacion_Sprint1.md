# Validación del Sprint 1

Código de seguimiento: **S1-P3**. Responsable: Sofia Cuellar Roca, Parte 3. Fecha: 11 de noviembre de 2026 (hora de La Paz).

El criterio del Excel, palabra por palabra:

> Todos se autentican; alta pública solo comprador. Producto sin stock inicial. Cotización rechazada no crea pedido; acuerdos históricos conservados. CRUD autorizado y desactivación sin borrar historial.

Veredicto de las cinco afirmaciones: **cumplen**. Cada una tiene abajo cómo se comprobó. La tercera columna anota lo que no está mal y conviene mirar en el sprint siguiente.

## Cómo se comprobó

El 11 de noviembre de 2026 ejecuté el recorrido del repositorio `SGCPapi` dos veces.

La primera, con `--solo-sprint1`, dio **27 de 27** sobre SQLite aislado. La segunda, el mismo día, corrió el verificador completo contra MySQL 8.0: otra vez **27 de 27**, y además la migración del Sprint 1 se aplicó dos veces sobre un pedido ya existente sin perder el cargo ni el margen. Cultura de ambas: `en-US`.

No recorrí las nueve pantallas de la sección 5 de `Como_ejecutar_el_sistema.md` con el navegador. Las reglas de los pasos 7, 8 y 9 sí están en las comprobaciones 7, 8, 10, 11 y 12. La lectura de la web es sobre las vistas de `SGCPuiweb` en `main` a esa fecha.

## Las cinco afirmaciones

| Afirmación | Veredicto | Cómo se comprobó | Qué podría ser mejor |
|---|---|---|---|
| Todos se autentican | Cumple | La comprobación 1 pide clientes sin token y recibe 401. El mismo recorrido entra como administrador y como comprador. La 27 cierra la sesión y el token deja de servir. En la web, la entrada es `Cuenta/IniciarSesion` y el pie dice que el acceso requiere conexión. | El texto está claro. No hace falta cambiarlo para este criterio. |
| Alta pública solo comprador | Cumple | La única alta visible sin sesión es «Crear cuenta de comprador». El formulario publica en `auth/registro-comprador` y avisa que la cuenta sirve solo para las operaciones de esa persona. Las comprobaciones 15 a 18 confirman que ese usuario recibe 403 en usuarios y en cotizaciones ajenas, y que no ve costo ni margen. | El personal no tiene alta pública. El alta de usuarios internos queda detrás del permiso `usuarios.administrar`. |
| Producto sin stock inicial | Cumple | La comprobación 4 mira el producto `PRD-001` y el JSON no trae stock. La ficha web dice «Crear un producto define el catálogo. No agrega existencias.» Al guardar, el aviso es «Producto guardado. Esta operación no crea existencias.» El listado muestra nombre, clasificación, presentación y unidad; no hay columna de stock. | El aviso nombra la regla en el momento de guardar. Conviene dejarlo así cuando entre el inventario del Sprint 2, para que no parezca que crear el producto ya cargó kilos. |
| Cotización rechazada no crea pedido; acuerdos históricos conservados | Cumple | Presentada y rechazada responden `COTIZACION_NO_ACEPTADA` (comprobaciones 7 y 8). La versión 2 conserva el vínculo (9). El pedido toma el precio aceptado de 35 aunque el catálogo ya esté en 40 (10). El margen de 4 kg × (35 − 28) queda en 28 (11). Una vigencia nueva de costo 30 y precio 45 no lo recalcula (12). La misma cotización no genera un segundo pedido (13). Aceptada y vencida responde `COTIZACION_NO_VIGENTE` (20). La cancelación conserva el motivo (19). En la cotización, «Crear pedido» queda deshabilitado si no está aceptada y vigente, y el pie dice que una rechazada o vencida no genera pedido. | El estado se muestra con el código (`PRESENTADA`, `ACEPTADA`, `RECHAZADA`). La regla se cumple. En la medición de RNF-04 hay que preguntar si el personal entiende «PRESENTADA» o espera una frase como «enviada al cliente». |
| CRUD autorizado y desactivación sin borrar historial | Cumple | Sin token, 401. El comprador, sin permiso interno, recibe 403. Desactivar un cliente con pedido pendiente responde `CLIENTE_CON_PEDIDOS` (14). La desactivación pone `Activo` en falso y registra `DESACTIVAR` en auditoría; no hay borrado de la ficha. Una clasificación con productos activos responde `CLASIFICACION_EN_USO` (6). El último administrador no se puede deshabilitar ni quedarse sin ese rol (2 y 3). | Cuando la desactivación sí procede, la web dice «Estado del cliente actualizado.» El mensaje de la API, cuando no procede, es más concreto: «Resuelve los pedidos pendientes antes de desactivar.» Conviene que la pantalla use esa frase, para que quien opera sepa qué resolver. |

## Importes y unidades

RNF-04 pide unidades visibles y el formato de los mockups. No forma parte de las cinco afirmaciones y lo miré igual.

- La web fija la cultura `es-BO`. Los importes mostrados van con el prefijo `Bs` y `ToString("N2")`: en esa cultura el detalle de una cotización se lee `Bs 35,00/kg` y el total `Bs 140,00`. El margen del pedido confirmado se titula «Margen estimado de productos» y aclara que no es la utilidad real por animal.
- La cantidad se muestra junto a la unidad (`4 kg`). La ficha de producto ofrece «Kilogramos · kg», «Gramos · g» y «Unidad». El listado de productos muestra «presentación · unidad».
- Los campos numéricos del formulario usan cultura invariante (`35.00`) porque el control `type="number"` del navegador exige punto. En la pantalla de detalle el mismo importe aparece con coma. No rompe el criterio. Es lo primero que puede trabar a alguien que escribe importes con coma.

## Qué queda fuera de esta nota

RNF-04 con personal representativo está en `Usabilidad_RNF04_Sprint1.md`. Esa sesión no se hizo: no hay personas ajenas al equipo en esta comprobación.

RNF-02, el desempeño, es S1-P4. No lo mido aquí.

No hubo devolución del docente todavía. La tarea 3 de S1-P3, traducir esa devolución a cambios con responsable, espera a que exista.
