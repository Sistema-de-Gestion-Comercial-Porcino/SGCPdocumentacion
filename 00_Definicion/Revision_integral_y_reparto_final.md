# Revisión integral del SGCP y reparto del trabajo final

Fecha de la revisión: **25 de noviembre de 2026**. Presentación: **viernes 27 de noviembre de 2026**.

Este documento compara el **Sprint Backlog del Excel** (`Formato Proyecto - SGCC Actualizado.xlsx`, hoja *Requerimientos*, sección V) y el catálogo de casos de uso (`Catalogo_casos_de_uso.md`) con el código real de los tres repositorios: **SGCPapi**, **SGCPuiweb** y **SGCPuimovil**. No dice qué *debería* haber: dice qué hay, qué se probó y qué falta, con la prueba que lo demuestra.

Somos tres para cerrar: **Dario, Sebastián y Victor**. Sofía está enferma. Desde ahora no hay roles: los tres somos desarrolladores y cada uno toca API, web o Android según lo que le toque. **Lo primero es el Sprint 2**, que es lo que se presenta el viernes.

---

## 0. Resumen en cinco líneas

1. **La API está completa y probada.** 209 comprobaciones pasan en MySQL y en SQL Server (GitHub Actions, commit `76dfccd`, 20 de noviembre). Los criterios del Excel de los sprints 1 a 4 se cumplen en el servidor.
2. **El Sprint 2 funciona de punta a punta por la web**: 34 de 35 comprobaciones (sección 2). Lo que falta son **tres pantallas** cuya lógica ya existe en la API: incidencias, reservas y movimientos de stock.
3. **Hay un bloqueo grave para el Sprint 3**: la web **no puede reservar stock**. Sin reserva no se puede preparar una entrega, y sin entrega no hay reparto, Android ni constancia. Hoy solo se destraba desde Swagger (sección 3.1).
4. **El perfil FINANZAS no puede usar la web**: ve «Cobranza» y «Gestión de costos» en el menú, pero las dos pantallas le dicen «Sin permiso» (sección 3.2). Se arregla en una línea.
5. **El cierre está sin hacer**: no hay etiquetas de versión en ningún repo, falta `RNF_resultados.md`, falta el guion de defensa y el Excel no cambia desde el 6 de noviembre (sección 5).

---

## 1. Cómo se revisó

| Qué | Cómo | Resultado |
|---|---|---|
| API completa | Verificador `tests/SGCP.Verificacion` en GitHub Actions sobre `main` (`76dfccd`) | MySQL **éxito** y SQL Server **éxito**, 209 comprobaciones |
| Web, compatibilidad | `dotnet run --project tests/SGCP.Web.Verificacion` el 25/11 | 12 de 12 |
| Sprint 2 por la web | Script que **llena los formularios reales** de la web (cookie, antiforgery y POST), con las cuentas `produccion1`, `almacen1` y `admin`, contra MySQL 8.4 local | 34 de 35 (sección 2) |
| Todas las pantallas web | Cada uno de los 9 perfiles abre cada enlace de su menú y el primer detalle o formulario de cada listado | Sin errores 500. **2 fallas de permiso** (FINANZAS) |
| Flujo pedido → entrega | Pedido real (cliente, precio, cotización, aceptación y pedido) y luego **Preparar entrega en la web** | **Se niega** por falta de reserva. Funciona solo si se reserva por la API |
| Cobertura API ↔ web | Lista de los 124 endpoints de la API cruzada con las llamadas de cada controlador web | 14 endpoints sin pantalla (sección 4) |
| Android | Código, manifiesto y endpoints que consume; pruebas unitarias del 20/11 (sin cambios desde entonces) | Cumple RF-07 y RNF-01. Detalles menores (sección 4.3) |

### Cuentas de prueba

Se crearon en la base local de Dario con la API. Para tenerlas en otra máquina, se crean igual desde **Usuarios → Nuevo**. El comprador se registra desde **Crear cuenta**. Las contraseñas no van en el repositorio: se pasan por el grupo.

| Usuario | Perfil | Para probar |
|---|---|---|
| `admin` | SUPERADMIN | Todo |
| `propietario1` | PROPIETARIO | Todo, reportes globales y auditoría |
| `administrador1` | ADMINISTRADOR | Usuarios, clientes, catálogo y operación; **no** ve dinero |
| `finanzas1` | FINANZAS | Cobranza, pagos, costos y seguimiento de cobros |
| `ventas1` | VENTAS | Clientes, cotizaciones, pedidos y cargos |
| `produccion1` | PRODUCCION | Sanidad y producción |
| `almacen1` | ALMACEN | Pesajes, entradas, existencias y frío |
| `entrega1` | ENTREGA | Transporte, rutas y entregas; **usuario de la app Android** |
| `comprador1` | COMPRADOR | Portal: catálogo, solicitar y aceptar cotización, sus pedidos |

---

## 2. Sprint 2 en detalle (prioridad del viernes)

### 2.1 Lo que pide el Excel

| Código | Prioridad | Parámetro de aceptación (literal del Excel) |
|---|---|---|
| RF-04 | Should | Crear costilla y lomo como cortes y jamón elaborado como derivado. Una orden obtiene costilla y lomo en lotes separados con pesajes propios; otra fabrica jamón. Confirmar resultado no suma stock; recepción física única sí. Una referencia repetida no duplica entrada ni consumo. |
| RF-18 | Must | Animal rechazado no inicia faeneo ni produce lote apto; **queda incidencia**. |
| RF-17 | Could | Lectura con valor, unidad, fecha, contexto y responsable; evaluación humana. Sin temperatura corporal ni acciones automáticas no validadas. |
| RF-20 | Should | El estado de cuenta distingue producto/servicio; no crea cargo de servicio no prestado. |
| RNF-03 | Should | Restauración central verificable; datos locales privados; pendiente local no se supone respaldado. |
| RNF-06 | Should | Autor, fecha real/central, clave, versión y resolución de conflicto conservados. |

Además, la descripción de RF-04 dice: *«Disponible es físico apto menos reservas; **previsiones no se reservan**.»*

### 2.2 Lo que se probó por la web, paso por paso

Cada fila es un formulario real enviado a la web. La columna «Comprobación» dice cómo se verificó el efecto.

| N.º | Paso en la web | Usuario | Resultado | Comprobación |
|---|---|---|---|---|
| S2-01 | Productos: existen Costilla de cerdo y Lomo de cerdo (cortes) y Jamón elaborado (derivado) | admin | ✅ | Listado de productos |
| S2-02 | Sanidad → Registrar animal (dos animales) | produccion1 | ✅ | Aparecen en Sanidad |
| S2-03 | Registrar control → **Aprobado** | produccion1 | ✅ | |
| S2-04 | Registrar control → **Rechazado**, observación «Fiebre al ingreso» | produccion1 | ✅ | |
| S2-05 | El animal rechazado queda **BLOQUEADO** | — | ✅ | Estado del animal en la API |
| S2-06 | El rechazo **abre una incidencia** con motivo y responsable | — | ✅ en la API | `GET /incidencias` |
| S2-06b | La incidencia **se ve en la web** | admin | ❌ **FALTA** | No hay pantalla. Ver tarea **D-2** |
| S2-07 | Planificar orden de faeneo con el animal rechazado | produccion1 | ✅ se niega | Mensaje: «No se puede faenar el animal …: fue rechazado en el control sanitario del … Motivo: Fiebre al ingreso» |
| S2-08 | Planificar orden de faeneo con previsiones de costilla 8 kg y lomo 5 kg | produccion1 | ✅ | |
| S2-09 | Iniciar orden | produccion1 | ✅ | |
| S2-10 | Registrar resultados: costilla con un lote y lomo con otro → Confirmar orden | produccion1 | ✅ | |
| S2-11 | **Una orden obtiene costilla y lomo en lotes separados** | — | ✅ | Detalle de la orden |
| S2-12 | **Confirmar resultado no suma stock** | — | ✅ | Existencias 0 → 0 |
| S2-13 | El lote nuevo aparece en Registrar pesaje | almacen1 | ✅ | |
| S2-14 | Registrar pesaje: bruto 13, tara 0,5 | almacen1 | ✅ | |
| S2-15 | Neto 12,500 y responsable guardado | — | ✅ | `neto: 12.5`, `responsableId` |
| S2-16 | **El pesaje no suma stock** | — | ✅ | Existencias 0 → 0 |
| S2-17 | Confirmar entrada física, ubicación Cámara 1 | almacen1 | ✅ | |
| S2-18 | **La entrada física suma 12,500** | — | ✅ | Existencias 0 → 12,5 |
| S2-19 | **Entrada repetida del mismo pesaje** | almacen1 | ✅ se niega | «Este lote ya tiene su entrada física… No se vuelve a sumar al stock.» |
| S2-20 | Existencias muestra Física apta, Reservada y Disponible por lote | almacen1 | ✅ | |
| S2-21 | Lomo con pesaje propio y entrada | almacen1 | ✅ | |
| S2-22 | Planificar **fabricación** de jamón | produccion1 | ✅ | |
| S2-23 | Registrar insumo consumido: 2 kg de costilla | produccion1 | ✅ | |
| S2-24 | **Reenviar el mismo consumo con la misma referencia** | produccion1 | ✅ no duplica | Costilla 12,5 → 10,5 (no 8,5) |
| S2-25 | **Otra orden fabrica jamón** (confirmar con lote de jamón) | produccion1 | ✅ | |
| S2-26 | Control de frío **Rechazado** sobre el lote de costilla | almacen1 | ✅ | |
| S2-27 | El frío guarda temperatura, unidad, fecha, lote, ubicación, responsable y evaluación | — | ✅ | Campos en la API |
| S2-28 | El lote rechazado queda **BLOQUEADO** | — | ✅ | |
| S2-29 | El jamón que consumió ese insumo queda **BLOQUEADO** | — | ✅ | Lote de jamón BLOQUEADO |
| S2-30 | **El consumo no se revierte** | — | ✅ | Movimiento `CONSUMO −2` sigue; disponible del lote bloqueado = 0 |
| S2-31 | Las previsiones **no suman disponible** | — | ✅ | Jamón sin entrada física = 0 |
| S2-32 | **Reservar o liberar desde la web** | — | ❌ **FALTA** | El botón «Revisar reservas» del pedido está deshabilitado. Ver tarea **D-1** |
| S2-33 | Permisos: Producción no abre Pesajes ni Frío; Almacén no abre Planificar orden ni Registrar animal | — | ✅ | Redirige a Sin permiso |
| S2-34 | La auditoría registra `BLOQUEAR_SIN_REVERTIR_CONSUMO` | — | ✅ | `GET /auditoria` |
| S2-35 | La pantalla Auditoría muestra usuario, fecha y entidad | admin | ✅ | |

**Conclusión del Sprint 2:** la regla de negocio está completa y probada desde la web. Para el viernes faltan **pantallas**, no lógica:

| Hueco | Criterio del Excel que afecta | Tarea |
|---|---|---|
| No se ven ni se resuelven las incidencias | RF-18: «queda incidencia» | **D-2** |
| No se puede reservar ni liberar | RF-04: «previsiones no se reservan» y «disponible = físico apto − reservas» | **D-1** |
| No hay historial de movimientos de stock | RNF-06: trazabilidad | **D-3** |
| No se puede rechazar un lote sin pasar por frío; no se puede recibir un lote comprado a terceros | RF-04 y CU09 «Recibir productos» | **S-2** |
| El frío no se puede asociar a una **entrega**, y el perfil ENTREGA no lo ve | RF-17: «lote/ubicación/entrega» | **S-1** |
| No se puede anular un cargo de servicio mal cargado | RF-20 (correcciones) | **S-3** |
| No hay procedimiento de respaldo y restauración | RNF-03: «restauración central verificable» | **V-3** |

### 2.3 Guion de la demostración del Sprint 2 (para el viernes)

Hacerlo con dos ventanas: `produccion1` y `almacen1`. Hay que ensayarlo antes sobre el servidor.

1. **Producción**: Sanidad → registrar `CERDO-001` (apto) y `CERDO-002` (rechazado, «Fiebre al ingreso»).
2. Producción → Planificar orden de faeneo con `CERDO-002` → **se niega con el motivo**. *(RF-18)*
3. Abrir **Incidencias** y mostrar la incidencia abierta. *(RF-18, pantalla de la tarea D-2)*
4. Planificar faeneo con `CERDO-001`, con previsiones de costilla 8 kg y lomo 5 kg → Iniciar.
5. **Almacén**: Existencias → costilla en 0. Explicar que una previsión no es stock.
6. Producción → Registrar resultados con `L-COS-001` y `L-LOM-001` → Confirmar → **dos lotes separados**. Existencias sigue en 0. *(RF-04)*
7. Almacén → Pesar `L-COS-001`, bruto 13 y tara 0,5 → neto 12,500. Existencias **sigue en 0**.
8. Almacén → Confirmar entrada → Existencias **12,500**. Intentar la misma entrada otra vez → **se niega**.
9. Producción → Fabricación de jamón → consumir 2 kg de costilla → confirmar con lote `L-JAM-001`.
10. Almacén → Control de frío **Rechazado** sobre `L-COS-001` → el lote y el jamón quedan **BLOQUEADOS** y el consumo de 2 kg **sigue**.
11. Ventas → en un pedido confirmado, **Registrar servicio prestado** → aparece aparte de los productos. *(RF-20)*
12. Admin → **Auditoría** → se ve todo lo anterior con usuario y fecha. *(RNF-06)*

---

## 3. Errores encontrados (bloquean una demostración)

### 3.1 BLOQUEANTE · La web no puede reservar stock y por eso no puede preparar entregas

- **Dónde:** `SGCPuiweb/src/SGCP.Web/Views/Pedidos/Detalle.cshtml`, línea 58: `<button class="button secondary" disabled>Revisar reservas</button>` y el aviso «estará disponible en una etapa posterior».
- **Por qué rompe:** `ServicioEntregas.ReservasCompletas` (SGCPapi) exige que cada detalle del pedido tenga su cantidad confirmada **reservada** antes de preparar o despachar.
- **Prueba hecha el 25/11:**
  1. Se creó un pedido de 2 kg de lomo por la API.
  2. En la web, **Entregas → Preparar** con ese pedido respondió: *«Reserva toda la cantidad confirmada de cada producto antes de preparar la entrega.»*
  3. Se reservó por la API (`POST /api/v1/reservas` → 201).
  4. La misma pantalla web preparó la entrega sin problema.
- **Qué arrastra:** sin reserva no hay entrega, y sin entrega no hay ruta, descarga en Android, recepción, constancia (RF-14) ni reporte de entregas. Es decir, todo el Sprint 3 y parte del Sprint 4 **no se pueden mostrar desde la web**.
- **Tarea:** **D-1**.

### 3.2 GRAVE · El perfil FINANZAS no puede abrir sus propias pantallas

- **Síntoma:** `finanzas1` ve en el menú «Cobranza» y «Gestión de costos», pero las dos redirigen a **Sin permiso**.
- **Causa:** `CobranzaController.Index` carga `GET clientes` y `PreciosController.Index` carga `GET productos`. El rol FINANZAS (`RolesSistema.Financieros`) no tiene `clientes.consultar`, `catalogo.consultar` ni `pedidos.consultar`. La API responde 403 y la web lo convierte en «Sin permiso».
- **Dónde:** `SGCPapi/src/SGCP.Api/Datos/DatosIniciales.cs`, línea `["FINANZAS"] = RolesSistema.Financieros`.
- **Corrección:** `["FINANZAS"] = [.. RolesSistema.Financieros, "clientes.consultar", "catalogo.consultar", "pedidos.consultar", "precios.consultar", "reportes.consultar"]`. **No** se toca `RolesSistema.Financieros`, porque esa lista también sirve para *quitarle* el dinero al ADMINISTRADOR en `GeneradorToken.PermisosEfectivos`.
- **No hace falta migración:** `DatosIniciales` vuelve a asignar los permisos de cada rol en cada arranque. Basta reiniciar la API y volver a iniciar sesión.
- **Prueba de aceptación:** `finanzas1` abre Cobranza, elige un cliente y ve saldos y pagos; abre Gestión de costos y ve los precios. Y `administrador1` **sigue sin ver** Cobranza ni Gestión de costos.
- **Tarea:** **V-1**.

### 3.3 MEDIO · El perfil ENTREGA no puede registrar frío desde la web

- **Síntoma:** CU11 dice que el *Responsable de entrega* registra el control de frío, y RF-17 pide el contexto «lote/ubicación/**entrega**». El menú solo muestra «Control de frío» con `frio.administrar` **y** `inventario.consultar`. ENTREGA no tiene `inventario.consultar`, así que no lo ve.
- **Además:** el formulario web de frío solo permite elegir un **lote**. La API ya acepta `EntregaId` (`FrioPeticion(Guid? LoteId, …, Guid? EntregaId = null)`), pero ninguna pantalla lo usa.
- **Tarea:** **S-1**.

---

## 4. Cobertura completa: API ↔ web ↔ Android, por sprint

✅ = hecho y probado. ⚠️ = funciona pero con un detalle. ❌ = falta.

### 4.1 Sprint 1 · Acceso, usuarios, clientes, catálogo, costos, cotización y pedido

| Req. | Criterio del Excel | API | Web | Estado |
|---|---|---|---|---|
| RF-01 | Rechazada o vencida no crea pedido; aceptada vigente sí | ✅ | ✅ Cotizaciones, Responder, Pedidos/Confirmar | ✅ |
| RF-02 | Costo y precio por unidad; el cambio no altera pedidos | ✅ | ✅ Gestión de costos | ⚠️ FINANZAS no entra (3.2) |
| RF-03 | 4 kg × (35 − 28) = Bs 28 | ✅ | ✅ Detalle del pedido | ✅ |
| RF-10 | Crear, buscar, editar y desactivar conservando historial | ✅ | ✅ Clientes | ✅ |
| RF-12 | Login; registro público solo comprador; recuperación con token de un uso | ✅ | ✅ Cuenta | ⚠️ En el servidor la recuperación necesita SMTP real (sección 6) |
| RF-13 | Usuarios con permisos auditados; al menos un administrador | ✅ | ✅ Usuarios | ✅ |
| RNF-02 | No más lento que anotar en el cuaderno | — | — | ❌ **Sin medir** (tarea V-4) |
| RNF-04 | Usuario representativo completa operaciones con guion | — | — | ❌ **Sin sesión con usuarios** (tarea V-4) |
| CU05 | Solicitud del comprador desde el portal | ✅ `POST cotizaciones/solicitudes` | ✅ Solicitar cotización | ✅ (avance del 20/11) |

### 4.2 Sprint 2 · Ver la sección 2

### 4.3 Sprint 3 · Pagos, crédito, transporte, rutas, entregas y Android sin conexión

| Req. | Criterio del Excel | API | Web | Android | Estado |
|---|---|---|---|---|---|
| RF-05 | Contado o crédito y vencimiento acordados | ✅ | ✅ Cobranza → Condición | — | ⚠️ FINANZAS no entra |
| RF-06 | Saldo = cargos − pagos aplicados, sin duplicar | ✅ | ✅ Cobranza | — | ⚠️ FINANZAS no entra |
| RF-07 | Pendiente hasta envío validado; conforme → ENTREGADA; observaciones → OBSERVADA; web retiro online | ✅ | ✅ Recepción (retiro local) | ✅ Captura sin conexión | ❌ **Bloqueado en la demo** por 3.1 |
| RF-08 | Transporte asignado a ruta; desactivar conserva historial; cierre sin capturas pendientes | ✅ | ✅ Transportes, Rutas | ✅ Finalizar ruta | ❌ **Bloqueado** por 3.1 |
| RF-19 | La referencia no duplica el pago; cancelación con acuerdo | ✅ | ✅ Señas, Aplicar, Resolver | — | ✅ |
| RNF-01 | Reintento sin duplicar; conserva datos tras timeout o conflicto | ✅ | ✅ Conflictos, Revisar | ✅ Room y cola | ✅ en pruebas unitarias |
| RNF-05 | Web en navegadores; Android real | — | ✅ responsiva | ✅ TECNO CK7n, 14/11 | ⚠️ Volver a probar **contra el servidor** |
| Seguimiento de cobros (v4.3.0) | Finanzas registra gestiones de cobro | ✅ 4 endpoints | ❌ **Sin pantalla** | — | ❌ tarea **V-2** |

**Android, detalles:**
- Consume `auth/login`, `auth/yo`, `auth/cerrar-sesion`, `mis-entregas`, `recepciones/sincronizar`, `recepciones/{id}` y `rutas/{id}/finalizar`. Todos existen en la API con las mismas rutas.
- `AndroidManifest.xml` tiene `usesCleartextTraffic="false"`: **solo habla con HTTPS**. Para el servidor con dominio propio está bien; para probar en local hay que usar la URL HTTPS o ajustar ese valor solo en debug.
- El `README.md` dice «cuenta ENTREGA o ADMINISTRACION». El rol ADMINISTRACION **ya no existe** desde los perfiles jerárquicos; se corrige el texto (tarea S-4).
- La app no registra frío. No es obligatorio: RF-17 pide registro manual con conexión, y la web lo cubre cuando se haga **S-1**.

### 4.4 Sprint 4 · Comprobante fiscal, constancia y reportes

| Req. | Criterio del Excel | API | Web | Estado |
|---|---|---|---|---|
| RF-11 | Sin integración habilitada queda pendiente; con proveedor, referencia única | ✅ Adapter con registro pendiente | ✅ Pedidos → Registro fiscal | ✅ (decisión: sin proveedor, queda pendiente con motivo) |
| RF-14 | Constancia solo con recepción conforme confirmada | ✅ | ✅ Constancia PDF | ❌ **Bloqueado en la demo** por 3.1 (no hay entrega sin reserva) |
| RF-15 | Filtros, alcance por perfil, comprador solo lo suyo, exportar PDF/Excel | ✅ | ✅ Reportes, Exportar | ✅ |

### 4.5 Endpoints de la API sin pantalla en la web

| Endpoint | Para qué | ¿Hace falta? | Tarea |
|---|---|---|---|
| `GET/POST /reservas`, `POST /reservas/{id}/liberar` | Reservar y liberar stock para un pedido | **Sí, bloqueante** | D-1 |
| `GET /pedidos-operativos` | Cola de pedidos confirmados por preparar | Sí, para reservar con orden | D-1 |
| `GET /incidencias`, `POST /incidencias/{id}/resolver` | Ver y resolver incidencias sanitarias y de calidad | **Sí, criterio RF-18** | D-2 |
| `GET /movimientos-stock` | Historial de entradas, consumos, despachos y anulaciones | Sí, RNF-06 | D-3 |
| `POST /lotes/{id}/rechazar` | Rechazar un lote por calidad sin pasar por frío | Sí | S-2 |
| `POST /lotes/externos` | Recibir un lote comprado a otro proveedor | Sí, CU09 «Recibir productos» | S-2 |
| `POST /cargos/{id}/anular` | Anular un cargo de servicio mal registrado | Recomendable | S-3 |
| `GET/POST seguimientos-cobro…` (4) | Seguimiento de cobros de Finanzas | Sí, se programó para eso | V-2 |
| `DELETE /clientes/{id}` | Borrado físico | **No**: la web desactiva, que es lo que pide RF-10 | — |
| `POST /animales/{id}/estado` | Dar de baja un animal | Opcional | — |

---

## 5. Cierre del proyecto que falta

| Tarea | Estado al 25/11 | Tarea asignada |
|---|---|---|
| Etiquetas de versión en los 4 repos (`v4.4.0` o la última del cierre) | **Ningún repo tiene etiquetas** (`git ls-remote --tags` vacío) | V-5 |
| `00_Definicion/RNF_resultados.md` con los seis RNF, medidos o no y por qué | No existe | V-4 |
| Medición RNF-02 (tiempos con datos de volumen) | Solo hay una medición: un reporte de 2007 pedidos en 47 ms | V-4 |
| Sesión RNF-04 con una persona ajena al equipo | No se hizo (`Usabilidad_RNF04_Sprint1.md` dice «no ejecutada») | V-4 |
| `00_Definicion/Guion_de_defensa.md` | No existe | V-6 |
| Excel con los sprints cerrados y RF-11 justificado | Sin cambios desde el 6/11. Era de Sofía | V-6 |
| Diagramas de CU05 alineados con los dos endpoints nuevos | Pendiente menor | D-4 |
| Rama vacía `sprint3/p2-web-cobranza-entregas` en SGCPuiweb | Sin diferencias con `main` | S-4 (borrarla) |

---

## 6. Para el servidor (lo coordina Dario)

Las instrucciones de despliegue llegan aparte. Lo que esta revisión deja anotado para no descubrirlo el viernes:

- **HTTPS obligatorio para Android** (`usesCleartextTraffic="false"`). El dominio necesita certificado válido; el teléfono no acepta certificados autofirmados.
- **Proxy inverso:** la API y la web usan `UseHttpsRedirection()` y `UseHsts()` fuera de Development, y ninguna configura `ForwardedHeaders`. Detrás de nginx esto puede producir un bucle de redirecciones o URLs `http://`. Hay que revisarlo al desplegar.
- **Secretos:** en el servidor no hay user-secrets. `ConnectionStrings:Sgcp`, `Jwt:Clave` y `DatosIniciales:ClaveAdministrador` van como variables de entorno (`ConnectionStrings__Sgcp`, etc.), nunca en el repo.
- **Migraciones:** la API no migra sola. En el servidor hay que correr `dotnet ef database update --context SgcpContext`, o el script SQL, antes de arrancar. En la máquina de Dario faltaban **tres**: `PerfilesYDocumentoCliente`, `SeguimientoCobro` y `SolicitudCotizacionComprador`. **Cada uno revise su base local.**
- **Recuperación de contraseña:** en desarrollo los correos se guardan en una carpeta local. En el servidor hace falta SMTP real o se avisa que la recuperación no se demuestra.
- **Respaldo (RNF-03):** no hay script de respaldo ni de restauración. Ver V-3.
- **Datos de ejemplo:** con `DatosIniciales:Ejemplos=true` se siembran Costilla, Lomo, Jamón elaborado y Sal de cura. Conviene activarlo en el servidor para la demo.

---

## 7. Reparto entre los tres

Reglas de siempre: rama propia, **pull request revisado por otro de los tres**, el autor no fusiona lo suyo, y el commit con el formato `vSPRINT.PARTE.PARCHE - Sprint N - …`. Como es trabajo de cierre, va como **Sprint 5** y cada uno conserva su número de parte: Dario `v5.1.x`, Sebastián `v5.2.x`, Victor `v5.4.x`.

**Plazo interno: jueves 26 a las 20:00**, todo fusionado en `main` para desplegar y ensayar. Lo marcado 🔴 es para el viernes sí o sí.

### Dario · inventario (Sprint 2 y desbloqueo del Sprint 3)

> **Estado al 25 nov:** D-1, D-2 y D-3 están hechos en **un solo PR**, el [SGCPuiweb #9](https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPuiweb/pull/9) (rama `sprint5/p1-web-inventario`, v5.1.0), y esperan revisión de Sebastián. D-4 está en la rama `sprint5/p1-diagramas-cu05` de este repositorio (v5.1.0).
> - **Probado por la web (22/22)** con los perfiles almacén, producción, ventas y administrador. El recorrido cubre:
>   - reservar y liberar con motivo;
>   - **preparar la entrega después de reservar desde la web**;
>   - ver y resolver incidencias (el animal sigue BLOQUEADO);
>   - movimientos de la costilla: +12,5 de entrada y −2 de consumo.
> - **Verificador web:** 18/18.
> - **Regla que apareció al probar:** la API admite **una sola reserva activa por producto del pedido y por lote** (índice `IX_Reservas_DetalleActivo_ExistenciaId`). Para sumar más del mismo lote hay que liberar y volver a reservar la cantidad total. La pantalla ya no ofrece ese lote y lo explica.
> - Con D-1 resuelto quedan desbloqueados S2-32, el bug 3.1 y la demo de RF-14. Con D-2 queda resuelto S2-06b.

#### 🔴 D-1 · Reservas y cola de pedidos en la web
- **Rama:** `sprint5/p1-web-reservas` en **SGCPuiweb**.
- **Qué:**
  1. Nueva pantalla **Almacén → Pedidos por preparar**, con `GET pedidos-operativos`: pedido, cliente, fecha comprometida y, por cada detalle, producto, cantidad confirmada, **reservado** y **falta reservar**.
  2. Por cada detalle, un botón **Reservar** que abre un formulario con:
     - Select de existencias del mismo producto con disponible > 0, de `GET existencias?productoId=`, mostrando lote, ubicación y disponible.
     - Cantidad, con un máximo igual a lo que falta y a lo disponible.
     - Envío con `POST reservas {detallePedidoId, existenciaId, cantidad}`.
  3. En la lista de reservas de un pedido (`GET reservas?detallePedidoId=`), un botón **Liberar** con motivo → `POST reservas/{id}/liberar {motivo}`.
  4. En `Views/Pedidos/Detalle.cshtml`, el botón «Revisar reservas» deja de estar deshabilitado y lleva a esa pantalla; se quita el aviso «etapa posterior».
  5. Menú: el ítem aparece con `inventario.administrar`.
- **Archivos:**
  - `Controllers/AlmacenController.cs`: acciones `Pedidos`, `Reservar` (GET y POST) y `Liberar` (GET y POST).
  - `Services/InventarioApi.cs`: ya hereda `Get`, `Post` y `Todos`.
  - `Models/Dtos/Dtos.cs`: `PedidoOperativoDto`, `ReservaDto`.
  - `Models/ViewModels/`: `ReservaFormViewModel`.
  - `Views/Almacen/Pedidos.cshtml` y `Reservar.cshtml`.
  - `Views/Shared/_Layout.cshtml`.
- **Mensajes de la API que la pantalla debe mostrar tal cual:** `SIN_EXISTENCIA_DISPONIBLE`, lote bloqueado.
- **Aceptación:**
  1. Pedido de 2 kg de lomo → Reservar 2 kg del lote con stock → Existencias muestra Reservada 2 y el Disponible baja 2.
  2. Reservar más de lo disponible → mensaje de la API, nada cambia.
  3. **Entregas → Preparar** con ese pedido → **funciona** (hoy se niega).
  4. Liberar → Disponible vuelve.
  5. Un producto que solo está en previsión **no aparece** para reservar.
- **Agregar** dos comprobaciones a `tests/SGCP.Web.Verificacion` (mapeo de DTO y cálculo de «falta reservar»).

#### 🔴 D-2 · Incidencias
- **Rama:** `sprint5/p1-web-incidencias` en **SGCPuiweb**.
- **Qué:** pantalla **Producción → Incidencias** con:
  - Filtro Pendientes, Resueltas o Todas (`GET incidencias?resuelta=`).
  - Columnas: fecha, origen (animal o lote, con su identificación o código, no el GUID), motivo, responsable y estado.
  - Botón **Resolver** con motivo obligatorio → `POST incidencias/{id}/resolver {motivo}`. Solo con `produccion.administrar`.
  - Aviso fijo: *«Resolver registra la decisión; no rehabilita el animal ni el lote.»* Es la regla de v4.3.2.
  - En `Sanidad/Detalle`, si el animal tiene incidencia, mostrarla con un enlace.
- **Aceptación:** rechazar un animal → la incidencia aparece pendiente → resolverla con motivo → queda resuelta con el motivo, y **el animal sigue BLOQUEADO**.

#### D-3 · Movimientos de stock
- **Rama:** `sprint5/p1-web-movimientos` en **SGCPuiweb**.
- **Qué:** en Existencias, por fila, un enlace **Movimientos** → `GET movimientos-stock?existenciaId=` con fecha, tipo (`ENTRADA`, `CONSUMO`, `DESPACHO` o `ANULACION_ENTRADA`, que son los que registra `ServicioInventario.Movimiento`), cantidad con signo, motivo y responsable. Las reservas no son movimientos físicos: se ven en la columna Reservada y en la pantalla de D-1.
- **Aceptación:** con los datos del recorrido del Sprint 2, la costilla muestra `ENTRADA +12,5` y `CONSUMO −2`.

#### D-4 · Diagramas de CU05 y despliegue
- **Rama:** `sprint5/p1-diagramas-cu05` en **SGCPdocumentacion**.
  - En la secuencia, la colaboración y la actividad de CU05 se nombran `POST cotizaciones/solicitudes` y `PUT cotizaciones/{id}/solicitud`.
  - En la clase Permiso, `cotizaciones.solicitar`.
  - En Cotizacion, `vigenteHasta` opcional mientras está en `BORRADOR`.
- **Despliegue en el servidor:** con las instrucciones que llegan aparte.

### Sebastián · frío, lotes, cargos y Android

#### 🔴 S-1 · Frío con contexto de entrega y acceso para ENTREGA
- **Ramas:** `sprint5/p2-frio-entrega` en **SGCPuiweb**; si hace falta permiso, otra en **SGCPapi**.
- **Qué:**
  1. En `Views/Frio/Registrar.cshtml`, agregar «¿Qué se controla?» con dos opciones: **Lote en cámara** (como hoy) o **Entrega en transporte** (select de entregas despachadas o en ruta de `GET entregas`). Se envía `LoteId` o `EntregaId`, nunca los dos.
  2. `FrioController`: si el usuario no tiene `inventario.consultar`, **no** se llama a `GET lotes` (hoy daría 403) y solo se ofrece la opción de entrega.
  3. `_Layout.cshtml`: «Control de frío» visible con `frio.administrar` **o** `entregas.administrar`. Quitar la condición `&& inventario.consultar`.
  4. El listado de frío muestra la columna **Contexto**: «Lote L-COS-001» o «Entrega E-0003».
- **Aceptación:**
  - `entrega1` ve Control de frío, registra 3 °C «Apto» sobre una entrega y aparece en el listado con su responsable.
  - `almacen1` sigue pudiendo registrar sobre un lote.
  - Un «Rechazado» sobre un lote lo sigue bloqueando (S2-28).

#### 🔴 S-2 · Rechazar lote y recibir lote externo
- **Rama:** `sprint5/p2-web-lotes` en **SGCPuiweb**.
- **Qué:**
  1. En Existencias, por lote, el botón **Rechazar lote** con motivo → `POST lotes/{id}/rechazar {motivo}`. Solo con `produccion.administrar`. Confirmación previa: *«El lote quedará bloqueado. Lo ya consumido no se devuelve y los derivados que lo usaron también se bloquean.»*
  2. **Almacén → Recibir lote externo**: producto, código de lote, referencia del proveedor, procedencia, fecha de producción y vencimiento → `POST lotes/externos`. Después se pesa y se da entrada como cualquier lote (S2-13 a S2-18).
- **Aceptación:**
  - Rechazar `L-LOM-001` → queda BLOQUEADO, Disponible 0, y aparece en Incidencias (D-2).
  - Recibir `L-EXT-001` de lomo → aparece en Registrar pesaje → pesar → entrada → suma stock.

#### S-3 · Anular cargo de servicio
- **Rama:** `sprint5/p2-web-cargos` en **SGCPuiweb**.
- **Qué:** en `Pedidos/Detalle` → *Cargos del pedido*, un botón **Anular** por cargo vigente, con motivo → `POST cargos/{id}/anular`. El cargo anulado queda en la tabla marcado como anulado (no desaparece).
- **Aceptación:** registrar «Desposte» Bs 20 → anular → el saldo del cliente baja Bs 20 y el cargo sigue visible como Anulado.

#### S-4 · Android contra el servidor y limpieza
- **Ramas:** `sprint5/p2-android-servidor` en **SGCPuimovil**; la limpieza de ramas, en SGCPuiweb.
- **Qué:**
  1. Compilar el APK con `API_BASE_URL` apuntando al dominio del servidor (por HTTPS).
  2. Instalarlo en el teléfono y repetir el recorrido de RNF-01 **contra el servidor**: descargar, modo avión, capturar con foto, volver a conectar, sincronizar y comprobar ENTREGADA en la web. Capturas en `00_Definicion/Evidencias_RNF05/`.
  3. Corregir el README: «cuenta ENTREGA» (quitar ADMINISTRACION).
  4. Borrar la rama vacía `sprint3/p2-web-cobranza-entregas` de SGCPuiweb.
- **Depende de:** D-1, para tener una entrega preparada, y del despliegue.

### Victor · Finanzas y cierre

#### 🔴 V-1 · Permisos de FINANZAS
- **Rama:** `sprint5/p4-permisos-finanzas` en **SGCPapi**.
- **Qué:** lo descrito en **3.2**. Agregar en `tests/SGCP.Verificacion/Perfiles.cs` una comprobación: *«FINANZAS consulta clientes y catálogo para cobrar»*, y otra que confirme que *ADMINISTRADOR sigue sin `saldos.consultar`*.
- **Aceptación:** la del punto 3.2, y el verificador completo en verde en MySQL y SQL Server (GitHub Actions).

#### V-2 · Seguimiento de cobros en la web
- **Rama:** `sprint5/p4-web-seguimiento-cobros` en **SGCPuiweb**.
- **Qué:** pantalla **Cobranza → Seguimiento**:
  - Lista desde `GET seguimientos-cobro?clienteId=&estado=` (PENDIENTE, REALIZADO o CERRADO), con cliente, pedido, vencimiento, próxima fecha y última gestión.
  - **Crear seguimiento** desde una condición de pago a crédito → `POST condiciones-pago/{id}/seguimientos {proximaFecha}`.
  - **Registrar gestión** → `POST seguimientos-cobro/{id}/gestion {resultado, proximaFecha?}`.
  - **Cerrar** → `POST seguimientos-cobro/{id}/cerrar`.
- **Aceptación:** pedido a crédito con vencimiento mañana → crear seguimiento → registrar «Llamé, paga el lunes» → cerrar → todo queda en Auditoría. Probar con `finanzas1` (requiere V-1).

#### V-3 · Respaldo y restauración (RNF-03)
- **Rama:** `sprint5/p4-respaldo` en **SGCPapi**.
- **Qué:**
  - `scripts/respaldo.sh`: `mysqldump --single-transaction --routines` a un archivo con fecha, sin escribir la clave en el script.
  - `scripts/restaurar.sh`: restaura en una base nueva.
  - En `docs/Respaldo.md`, el procedimiento y **una restauración real comprobada**: contar pedidos antes y después.

#### V-4 · RNF pendientes y `RNF_resultados.md`
- **Rama:** `sprint5/p4-rnf-resultados` en **SGCPdocumentacion**.
- **Qué:**
  - **RNF-02:** cronometrar «registrar pedido» en el sistema frente a anotarlo en papel, con 3 repeticiones. Medir también los reportes con datos de volumen.
  - **RNF-04:** media hora con 2 personas de otro grupo siguiendo `Usabilidad_RNF04_Sprint1.md`. Anotar tiempos, dónde se trabaron y qué preguntaron.
  - Escribir `00_Definicion/RNF_resultados.md` con los seis RNF: medido con qué resultado, o no medido con qué motivo. **Ninguno vacío.**

#### V-5 · Etiquetas de versión
- **Cuándo:** **después** de fusionar todo y desplegar.
- **Qué:** la etiqueta de cierre en los cuatro repos sobre el último commit de `main`:
  ```bash
  git tag -a v5.4.0 -m "Cierre del proyecto"
  git push origin --tags
  ```
  Y su fila en el Historial de cada README.

#### V-6 · Excel y guion de defensa
- **Excel** (`Formato Proyecto - SGCC Actualizado.xlsx`): estado de cada RF y RNF de los sprints 1 a 4 («Implementado y verificado», «Condicional: sin proveedor fiscal» para RF-11, etc.).
- **`00_Definicion/Guion_de_defensa.md`:**
  - Cómo levantar en dos minutos.
  - El recorrido del Sprint 2 (sección 2.3 de este documento).
  - Los siete patrones con su archivo.
  - Lo que no se entregó y por qué: RF-09, RF-16, RF-21 y RF-11 sin proveedor.

---

## 8. Orden de trabajo hasta el viernes

| Cuándo | Dario | Sebastián | Victor |
|---|---|---|---|
| Mié 25, tarde | D-1 Reservas | S-1 Frío con entrega | V-1 Permisos FINANZAS (corto) → V-2 |
| Mié 25, noche | D-2 Incidencias | S-2 Rechazar lote y lote externo | V-2 Seguimiento de cobros |
| Jue 26, mañana | Revisa los PR de S-1 y S-2 · D-3 | Revisa los PR de D-1 y D-2 · S-3 | Revisa los PR de V-1 y V-2 · V-3 |
| Jue 26, tarde | Despliegue en el servidor · D-4 | S-4 Android contra el servidor | V-4 RNF y V-6 guion |
| Jue 26, 20:00 | **Todo en `main` y desplegado** | | |
| Jue 26, noche | **Ensayo completo** con el guion 2.3 en el servidor | ← | ← |
| Vie 27 | Presentación · V-5 etiquetas después | | |

**Revisiones cruzadas:** Dario revisa a Sebastián, Sebastián revisa a Dario y Victor, y Dario revisa a Victor. Nadie fusiona lo suyo.

### Antes de abrir cada PR

1. `dotnet build` sin advertencias nuevas.
2. Los verificadores que correspondan:
   - API: `dotnet run --project tests/SGCP.Verificacion` con `SGCP_MYSQL_TEST`.
   - Web: `dotnet run --project tests/SGCP.Web.Verificacion`.
   - Android: `./gradlew testDebugUnitTest`.
3. **Probar la pantalla con el perfil que la va a usar**, no con `admin`: `admin` tiene todos los permisos y esconde los errores como el de FINANZAS.
4. Los números se prueban con coma y con punto (cultura `es-BO`). Es el error que más nos costó en el Sprint 1.
5. En el cuerpo del PR: qué criterio del Excel cubre, cómo se probó y una captura.
