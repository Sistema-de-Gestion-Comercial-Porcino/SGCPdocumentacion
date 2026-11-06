# Revisión previa a implementar el Sprint 1

Fecha: 5 de noviembre de 2026. Revisión documental y del entorno; todavía no hay implementación ni pruebas funcionales de los tres repositorios.

## Fuentes revisadas

- `../Guia_SGCP_Sprint1.md`, versión 2.0 completa. Se comprobó la existencia de sus copias Word y PDF; el PDF tiene 39 páginas.
- `../Formato Proyecto - SGCC Actualizado.xlsx`: Perfil, planificación del Sprint 1, y Requerimientos, requisitos y backlog del sprint. Se contrastó con `../Formato Proyecto - SGCC 1 1.xlsx`.
- `../02_Ingenieria_de_Software/00_Documentacion/Diccionario_clases.md`, modelos `Clases_SGCC.mdj` de generales y entrega, `Reglas_del_sistema.md`, `Fuentes_vigentes.md` y `Organizacion_repositorios_y_patrones.md`.
- `../../CLAUDE.md`: contexto histórico de octubre, desactualizado en nombre, requisitos y entregables; no sustituye las fuentes vigentes.
- Memoria de criterios de frontend solicitada por el usuario. El aspecto renderizado y la integración deberán comprobarse al implementar; esta revisión no es una validación visual de una aplicación.

## Alcance confirmado

CU01–CU07: acceso y registro público de comprador; usuarios y permisos; clientes; costos/precios; cotizaciones; confirmación, consulta y cancelación de pedidos; clasificaciones y productos sin stock inicial. RF01/02/03/10/12/13 y parametrización de RF04; RNF02/04 requieren evidencia de desempeño y uso.

API ASP.NET Core 10 con controladores y EF Core; web ASP.NET Core MVC que consume únicamente la API; base Android Kotlin con acceso online y estado vacío de entregas. La base Android propuesta es una concreción técnica de la guía: el Excel no enumera esas pantallas individualmente. SQLite es la decisión provisional de desarrollo de Claude, no una elección confirmada del docente.

Builder corresponde a este sprint. Producción, existencias, reservas, cobros, reparto operativo, captura offline y exportación quedan para sus sprints previstos. Ambos Excel incluyen cotizaciones y pedidos en S1, pero no son documentos idénticos: el actualizado precisa registro público, catálogo, desactivación y conservación de historial.

## Correcciones necesarias al convertir la guía en código

1. **Restos de la guía anterior.** La línea 20 todavía excluye cotizaciones y pedidos; la línea 284 dice diez entidades. Deben prevalecer la sección 4 y las catorce entidades listadas. El criterio de catorce tablas tampoco es exacto: hay tablas de unión de roles/permisos y de usuarios/roles, además de la tabla técnica de migraciones.

2. **Precio aceptado frente a precio vigente.** La línea 553 afirma que precio y costo salen de la vigencia al confirmar. Eso contradice CU06 y el Excel. El precio del pedido se copia de `DetalleCotizacion.PrecioUnitario`; el costo de referencia se obtiene de la vigencia efectiva al confirmar, como concreta CU06. Ambos quedan conservados en el detalle del pedido. Probar cambio de catálogo tanto antes como después de confirmar: no sustituir el precio que el cliente aceptó.

3. **Desactivación de clientes.** La línea 886 revisa únicamente cuentas vinculadas y aplaza pedidos. Ya existen pedidos en S1: deben revisarse dependencias comerciales pendientes, coherentemente con RF10 y el criterio 13. No inventar deuda en este sprint; preparar su comprobación para cuando exista cobranza. Conservar operaciones históricas y explicar qué dependencia impide desactivar.

4. **Diferencias reales con UML.** Los códigos de cotización y pedido no son las únicas diferencias. La guía añade `Cotizacion.MotivoRespuesta`, la autorrelación `CotizacionOrigen` y `Permiso.Id`, ausentes del diccionario y de ambos MDJ de clases. Documentar estas decisiones y alinear el modelo cuando se implemente. Las demás claves foráneas que materializan asociaciones existentes no representan por sí mismas nuevas entidades de negocio. `PedidoConfiguration` además usa `Cliente.Pedidos`, navegación no declarada en el ejemplo de `Cliente`.

5. **Vigencia y duplicación del pedido.** El texto del servicio exige cotización aceptada y vigente, pero el ejemplo solo comprueba el estado. Verificar fecha también al aceptar y al confirmar, no depender de consultar antes la cotización. Proteger la relación cotización–pedido con unicidad en la base y operación atómica; dos peticiones simultáneas no pueden crear dos pedidos. Los códigos correlativos también necesitan unicidad y tratamiento de concurrencia.

6. **Historial de versiones.** Definir el alcance del código y de la numeración de versiones. La guía propone un registro nuevo con código único y enlace a la versión anterior. Evitar ramas accidentales con varias versiones sucesoras iguales y mostrar el historial al usuario. Conservar la versión presentada y exigir aceptación de cualquier cambio; crear otra versión no equivale a aceptar la anterior.

7. **Sesión y permisos efectivos.** Marcar `Sesion.Revocada` no invalida por sí solo un JWT. Asociar el token con la sesión y comprobar su vigencia, la habilitación del usuario y los permisos efectivos en solicitudes protegidas. Cierre, desactivación y recuperación deben dejar inutilizables los tokens anteriores. El último administrador se protege también al editar sus roles, no solo al desactivar su cuenta. El umbral de intentos debe ser configurable; cinco fallos bloquean en el quinto, no en el sexto como dice el criterio 5.

8. **Privacidad del comprador.** El ejemplo de producto devuelve `costoReferencia`, aunque COMPRADOR puede consultar el catálogo sin permiso de costos. Separar la respuesta pública de los datos internos. El comprador tampoco debe recibir costos ni margen interno al consultar sus pedidos. Comprobar alcance por cliente en listados y detalles. Falta concretar el vínculo entre registro público y `Cliente`: no asignar historial existente solo porque alguien conoce una identificación fiscal o un teléfono.

9. **Recuperación de acceso.** Devolver el token en la respuesta anónima de recuperación no verifica la identidad del propietario de la cuenta. Si se usa un mecanismo local para demostrarlo, debe ser exclusivo de desarrollo y accesible únicamente al equipo, con respuesta pública genérica. El mecanismo real de entrega/verificación debe quedar definido para cumplir RF12; no presentar una simulación como recuperación productiva. Consumir el token una sola vez, con vencimiento y revocación de sesiones.

10. **Vigencias y confirmaciones.** La vigencia efectiva debe cumplir sus fechas; una fila abierta con inicio futuro no es necesariamente vigente hoy. Validar solapamientos también al editar, no solo al crear. Pedir confirmación de margen no positivo antes de guardar: la guía combina una respuesta 201 ya persistida con una confirmación y reenvío posterior, que podría duplicar cambios. Conservar el redondeo monetario y las unidades de forma consistente.

11. **Interfaz con datos reales.** No copiar literalmente `Bs 30 acordados` para todos los pedidos: es un ejemplo de Balsamiq y este sprint no registra ese servicio. Mostrar el estado pendiente de esa función, sin atribuir acuerdos ficticios. Tampoco fijar los códigos COT-028/PED-042 ni la fórmula del ejemplo en todas las pantallas. Los indicadores y mensajes dependen de los datos y permisos del usuario; comprador y personal necesitan recorridos apropiados a su acceso.

12. **Demostración coherente.** Los criterios 11–12 cambian costo/precio de 28/35 a 30/38, pero el criterio 21 vuelve a esperar costo 28 sin restablecerlo. Separar escenarios de prueba o preparar explícitamente el estado inicial; con costo vigente 30, cuatro kilos a precio aceptado 35 producen margen 20, no 28. La cancelación también debe conservar el motivo solicitado. Los criterios de desempeño/usabilidad necesitan el guion y la comparación acordados, no solo un build correcto.

13. **Arranque técnico reproducible.** El SDK instalado es 10.0.400. `dotnet new sln --help` confirma formato predeterminado `slnx`; usar `--format sln` si se conservan los comandos `.sln` de la guía. Fijar versiones compatibles de paquetes y herramienta EF. Cambiar de motor requiere regenerar migraciones y validar el proveedor; no presentarlo como una migración resuelta por cambiar una clave. El motor definitivo es MySQL 8: lo que cambió está en `Cambio_a_MySQL.md`.

## Estado local y acceso a GitHub

En esta revisión `SGCPapi`, `SGCPuiweb` y `SGCPuimovil` están vacías, sin `.git`. No hay un clon parcialmente creado. Git 2.43.0 está instalado; GitHub CLI no está instalado, pero `apt-cache policy gh` confirma un paquete disponible en los repositorios de Linux Mint/Ubuntu.

El error mostrado corresponde a autenticación HTTPS: GitHub no admite la contraseña de la cuenta en Git. La alternativa recomendada para esta preparación es iniciar sesión mediante navegador con GitHub CLI, desde la terminal del usuario:

```bash
sudo apt update
sudo apt install gh
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

Completar el acceso en el navegador con la cuenta que tiene permisos en la organización. Luego ejecutar desde la carpeta padre para evitar `SGCPapi/SGCPapi`:

```bash
cd /home/supergenio/Escritorio/TareaSoftware/Modelado_Chancheria
git clone https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPapi.git SGCPapi
git clone https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPuiweb.git SGCPuiweb
git clone https://github.com/Sistema-de-Gestion-Comercial-Porcino/SGCPuimovil.git SGCPuimovil
```

Las URLs proceden de la organización indicada por el usuario; no se ha comprobado acceso a repositorios privados. Esta revisión no instaló programas, inició sesión, clonó ni modificó los modelos o la guía de Claude.

Referencias oficiales: [autenticación de GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github), [acceso mediante GitHub CLI](https://cli.github.com/manual/gh_auth_login).
