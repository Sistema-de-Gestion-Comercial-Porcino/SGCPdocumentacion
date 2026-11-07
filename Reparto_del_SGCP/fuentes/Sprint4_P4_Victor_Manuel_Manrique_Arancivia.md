# Sprint 4 · Parte 4 · Victor Manuel Manrique Arancivia

Código de seguimiento: **S4-P4**. Rol: Scrum Master. Repositorio: **SGCPdocumentacion**.

## Qué te toca

Cerrar el proyecto. Los diagramas finales, la prueba del sistema completo, los requerimientos no funcionales que quedaron sin medir, el paquete de entrega y la etiqueta `v4.4.0`.

Tu parte es la que decide si el proyecto se ve terminado o se ve a medias. Dos equipos pueden tener el mismo código y uno aprueba mejor que el otro por cómo está armada la entrega.

## Tus tareas

### 1. Diagramas finales del sistema completo

En `02_Analisis/` y `03_Diseño/`, actualizados con todo lo construido en los cuatro sprints:

- **Casos de uso**, con todos los requerimientos entregados y marcando los que no se hicieron.
- **Clases**, con las entidades de los cuatro sprints y los siete patrones visibles.
- **Secuencia** de los flujos principales: cotización a pedido, producción a inventario, entrega a recepción a constancia, y reporte exportado.
- **Componentes**, mostrando los tres repositorios, la base de datos y el proveedor fiscal externo como sistema aparte.
- **Modelo de datos** completo.

El de componentes es el que más conviene tener bien: es el que explica de un vistazo que el proyecto son tres aplicaciones y no una, y que el proveedor fiscal está afuera. Si RF-11 quedó sin implementar, el proveedor aparece igual, marcado como punto de integración diseñado y no habilitado.

**Entregás:** los diagramas en `.png` y su fuente. **Se comprueba:** cada elemento del diagrama existe en el código entregado.

### 2. Diccionario de datos completo

En `02_Analisis/Diccionario_de_datos.md`, todas las entidades de los cuatro sprints: campo, tipo, longitud, si acepta vacío, su regla y de dónde viene.

Para generarlo sin equivocarte, sacá los tipos reales de la base, no del código:

```sql
SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, EXTRA
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'sgcp'
ORDER BY TABLE_NAME, ORDINAL_POSITION;
```

Dos avisos sobre esa consulta: las columnas con `EXTRA` que dice `STORED GENERATED` son columnas calculadas que existen para sostener índices únicos que MySQL no puede hacer de otra forma, y conviene que el diccionario lo aclare en una línea. Y si una columna de la base no coincide con lo que dice el diseño, el que está mal es el documento: la base es la que corre.

**Entregás:** el diccionario. **Se comprueba:** coincide con `information_schema`.

### 3. Pruebas del sistema completo

Extendé `tests/SGCP.Verificacion` para cubrir los cuatro sprints de punta a punta. Y agregá los casos propios de este sprint:

- Un comprador pidiendo datos de otro: rechazado.
- Un archivo exportado por un comprador: sin costos ni márgenes en ninguna columna.
- Un pedido viejo reportado después de un cambio de precio: margen histórico, no recalculado.
- Constancia con recepción pendiente: rechazada.
- Constancia con entrega observada: rechazada.
- Doble emisión fiscal: la segunda conserva la referencia de la primera.

Corrélo contra MySQL real y con las dos configuraciones regionales, `es_BO.UTF-8` y `C`, como en los sprints anteriores. El motivo está en `00_Definicion/Metodo_de_verificacion.md`: dos defectos del Sprint 1 fueron exactamente de eso.

**Entregás:** la verificación cubriendo los cuatro sprints. **Se comprueba:** pasa entera, en las dos configuraciones.

### 4. Pruebas de volumen

Los reportes cruzan todos los módulos, así que son lo primero que se pone lento. Sembrá datos de volumen —unos miles de pedidos con sus detalles— y medí cuánto tarda cada reporte y cada exportación.

Lo que buscás no es un número bonito: es encontrar el reporte que con cinco filas responde al instante y con mil tarda veinte segundos. Ese existe casi siempre, y encontrarlo antes de la defensa es mucho mejor que encontrarlo durante.

**Entregás:** una tabla de reporte, cantidad de filas y tiempo. **Se comprueba:** hay medición con datos de volumen, no con la base vacía.

### 5. Los requerimientos no funcionales pendientes

Repasá los seis. El RNF-02 de rendimiento era tu pendiente desde el Sprint 1 y el RNF-04 de usabilidad es de S4-P3.

Para cada uno: medido con qué resultado, o no medido con qué motivo. Las dos respuestas sirven; lo que no sirve es que el renglón esté vacío.

**Entregás:** `00_Definicion/RNF_resultados.md` con los seis. **Se comprueba:** ninguno sin estado.

### 6. El paquete de entrega

Según el formato: el proyecto en un `.zip` **sin `bin`, `obj` ni `.vs`**.

```bash
cd /ruta/al/padre/de/los/repos
zip -r SGCP_Entrega_Final.zip SGCPapi SGCPuiweb SGCPuimovil SGCPdocumentacion \
  -x '*/bin/*' '*/obj/*' '*/.vs/*' '*/.git/*' '*/build/*' '*/.gradle/*' '*/node_modules/*'
```

Después **descomprimilo en otra carpeta y revisalo**. Que no haya quedado ninguna carpeta `bin` ni `obj` escondida, y que no haya quedado ninguna clave: revisá `appsettings.json`, que tiene que estar con la cadena de conexión vacía a propósito, y los archivos de configuración de Android.

```bash
unzip -l SGCP_Entrega_Final.zip | grep -E '/(bin|obj|\.vs)/' ; echo "vacio = correcto"
```

**Entregás:** el `.zip`. **Se comprueba:** la revisión de arriba no devuelve nada y no hay claves adentro.

### 7. La prueba de instalación desde cero

La que más defectos encuentra al final de un proyecto, y la que casi nadie hace: en una máquina que nunca tuvo el sistema, seguí `00_Definicion/Como_ejecutar_el_sistema.md` paso por paso, **sin saltarte nada y sin usar lo que ya sabés**.

Si en algún paso tuviste que adivinar algo, el documento está incompleto y hay que corregirlo. Esa es la prueba: no que vos lo logres, sino que el documento alcance.

Vale la laptop de un compañero, o una máquina virtual.

**Entregás:** el documento corregido con lo que faltaba. **Se comprueba:** alguien ajeno al equipo lo levanta siguiendo solo el documento.

### 8. El cierre de versiones

Última versión del proyecto. Tu commit es el último del sprint, `v4.4.0`, y **esa misma versión es la etiqueta** en los cuatro repositorios. Va **después** del commit de cada uno, nunca antes:

```bash
git tag -a v4.4.0 -m "Sprint 4 - Entrega final"
git push origin main --follow-tags
```

Y la tabla de historial de cada README con el renglón de `v4.4.0`.

**Entregás:** las cuatro etiquetas. **Se comprueba:** `git tag -l` las muestra y apuntan al commit de entrega.

### 9. Preparar la defensa

No es un entregable del Excel, pero es lo que se califica. Armá una página con:

- Cómo levantar el sistema en dos minutos, con los comandos escritos y copiables.
- El recorrido que vas a mostrar, en orden, y qué dice el criterio de cada paso.
- Los siete patrones, uno por renglón, con el archivo donde está cada uno y por qué ese patrón ahí.
- Lo que no se entregó, con su motivo.

Lo último es lo que más conviene tener preparado. Un equipo que dice «RF-11 quedó como punto de integración diseñado porque no hubo proveedor confirmado, y acá está el Adapter que permite habilitarlo sin tocar el resto» responde mucho mejor que uno que se sorprende con la pregunta.

Y ensayá el arranque antes. El sistema que no levanta en la defensa es la forma más común de perder una nota que el código ya tenía ganada.

**Entregás:** `00_Definicion/Guion_de_defensa.md`. **Se comprueba:** cualquiera del equipo puede hacer la demostración leyéndolo.

## Qué no te toca

Escribir el código de las funciones. Los criterios de aceptación y la decisión fiscal: S4-P3.

## De quién dependés y quién depende de vos

**Dependés de S4-P1 y S4-P2** para probar el sistema completo, y de **S4-P3** para los criterios.

**Depende de vos el cierre del proyecto.** Nadie entrega hasta que la verificación pase, el paquete esté armado y las etiquetas estén puestas.

Las tareas 1, 2 y 5 no dependen de nadie: arrancá por ahí mientras los demás construyen.

## Cómo entregarlo

```bash
git checkout -b sprint4/p4-entrega-final
git commit -m "v4.4.0 - Sprint 4 - Diagramas finales, pruebas de sistema y entrega"
git push -u origin sprint4/p4-entrega-final
```

Pull Request con el código `S4-P4` en el cuerpo.

Y después del merge, las etiquetas `v4.4.0` en los cuatro repositorios.
