# Sprint 4 · Parte 3 · Sofia Cuellar Roca

Código de seguimiento: **S4-P3**. Rol: Product Owner. Repositorio: **SGCPdocumentacion**.

## Qué te toca

Este sprint tu parte **arranca primero y es bloqueante**, a diferencia de los anteriores. Hay dos decisiones que nadie puede tomar en tu lugar y que detienen a los dos desarrolladores si no están:

1. **Qué reporte ve cada perfil.** Sin esa matriz no se puede implementar la autorización.
2. **Si RF-11 se hace o no.** Es condicional y la decisión es tuya, con el docente.

Las dos el primer día del sprint. Lo demás —criterios y validación final— viene después.

## Tus tareas

### 1. La matriz de perfiles y reportes · primero, es bloqueante

Son seis perfiles —administrador, ventas, producción, almacén, finanzas, comprador— y los reportes que pide el Excel: clientes, cotizaciones, pedidos, producción por producto y lote, inventario, pagos y entregas.

Hacé una tabla con los perfiles en las filas, los reportes en las columnas, y en cada celda si ve todo, si ve una parte o si no ve nada.

Dos reglas que ya están fijadas desde el Sprint 1 y que la matriz **tiene que** respetar:

- El comprador no ve costos ni márgenes, nunca, en ningún reporte.
- Producción y almacén no ven precios de venta.

Y para las celdas donde «ve una parte», escribí qué parte. «Ventas ve el reporte de pedidos» no alcanza: ¿de todos los clientes o solo de los que atiende? Esa ambigüedad se convierte en una decisión que el programador toma solo, y puede tomarla mal.

**Entregás:** `00_Definicion/Reportes_por_perfil.md` con la matriz. **Se comprueba:** no queda ninguna celda vacía ni ambigua.

### 2. La decisión sobre RF-11 · primero, es bloqueante

El Excel dice que la emisión y consulta fiscal «requieren modalidad aplicable y proveedor confirmados y configurados». Y el perfil del proyecto lista RF-11 como condicional.

Preguntale al docente, de forma directa: ¿hay proveedor fiscal para integrar, o RF-11 queda como punto de integración diseñado y no implementado?

Las dos respuestas son válidas. La que no sirve es no preguntar y dejar que el sprint se consuma esperando.

Si hay proveedor: necesitás la modalidad, los datos de conexión y qué devuelve. Si no hay: se registra la decisión y se entrega el Adapter diseñado, que es lo que el Excel contempla cuando dice que la operación «se registra sin comprobante» mientras no esté habilitada.

**Entregás:** la decisión escrita, con fecha y con quién la confirmó, en `00_Definicion/Decisiones.md`. **Se comprueba:** está tomada en la primera semana del sprint.

### 3. Criterios de aceptación de RF-14 y RF-15

Como en los sprints anteriores, en `00_Definicion/Criterios_Sprint4.md`, con el formato Dado/Cuando/Entonces.

Los casos que no pueden faltar:

- Un comprador pide un reporte de otro comprador. Entonces: rechazado.
- Un comprador exporta sus pedidos. Entonces: el archivo no tiene ninguna columna de costo ni de margen.
- Un perfil de producción pide el reporte de pagos. Entonces: el reporte no está disponible para ese perfil.
- Se consulta el reporte de pedidos de un mes y se exporta. Entonces: el archivo trae las mismas filas que la pantalla.
- Un pedido viejo se reporta después de que el precio del producto cambió. Entonces: el margen reportado es el histórico, no el recalculado.
- Se pide constancia de una entrega con recepción pendiente de sincronizar. Entonces: rechazada.
- Se pide constancia de una entrega observada. Entonces: rechazada, con motivo distinto al anterior.
- Se intenta emitir dos veces el comprobante del mismo pedido. Entonces: la segunda conserva la referencia de la primera, no crea una nueva.

El quinto caso es el más fácil de pasar por alto y el que más probablemente esté mal implementado, porque recalcular el margen «parece» mejor. Insistí en ese.

**Entregás:** el archivo de criterios. **Se comprueba:** los ocho casos están, con sus resultados esperados.

### 4. Validar el sprint

Como siempre: recorrer el sistema con los criterios en la mano. Y en este sprint, además, hacer la prueba de los dos compradores vos misma, porque es la que importa: dos cuentas, pedidos distintos, y verificar que ninguna ve nada de la otra, ni en pantalla ni en el archivo exportado.

Abrí el Excel exportado y revisá **todas** las columnas, incluso las que están a la derecha y no se ven sin desplazar. Ahí es donde aparece el costo olvidado.

**Entregás:** el registro de validación. **Se comprueba:** cada criterio tiene resultado, y los defectos están anotados.

### 5. Validar los cuatro sprints, no solo este

Es el último sprint, así que corré también los criterios de los sprints 1, 2 y 3. Una función del Sprint 1 que dejó de funcionar es peor que una del Sprint 4 que falta: significa que algo que el docente ya vio aprobado se rompió.

**Entregás:** `00_Definicion/Validacion_final.md` con el estado de los cuatro sprints. **Se comprueba:** ningún criterio de un sprint anterior quedó en rojo.

### 6. Revisar los RNF de usabilidad

El RNF-04 —que un usuario entrenado complete el flujo sin ayuda— era tu pendiente desde el Sprint 1. Si todavía no se midió, este es el último sprint donde se puede.

La medición es simple: alguien que no sea del equipo, con una explicación de cinco minutos, intenta registrar un cliente, armar una cotización y confirmar el pedido. Se anota qué tardó, dónde se trabó y qué preguntó. Si la persona puede ser un compañero de otro grupo, mejor: no conoce el sistema.

**Entregás:** una página con lo observado. **Se comprueba:** hay una medición real, con una persona real.

### 7. Cerrar el Excel

Marcá en `Formato Proyecto - SGCC Actualizado.xlsx` los cuatro sprints como cerrados, con lo entregado y lo que no, y el motivo en cada caso. Es el documento que el docente usa para calificar.

Si RF-11 no se hizo, que esté escrito ahí con el motivo y la fecha de la decisión. Un requerimiento condicional que no se cumplió **con su justificación** es diferente de uno que falta sin explicación, y el docente lo va a leer de ese Excel.

**Entregás:** el Excel actualizado. **Se comprueba:** los cuatro sprints tienen estado y lo condicional está justificado.

## Qué no te toca

Escribir código. Los diagramas: S4-P4.

## De quién dependés y quién depende de vos

**Dependés de nadie para empezar.** Dependés del docente para la respuesta sobre RF-11.

**Dependen de vos S4-P1 y S4-P2, los dos, desde el primer día.** Este sprint vos abrís el trabajo. Si la matriz de perfiles tarda una semana, el sprint pierde una semana.

## Cómo entregarlo

```bash
git checkout -b sprint4/p3-criterios
git commit -m "v4.1.0 - Sprint 4 - Reportes por perfil, decision fiscal y validacion final"
git push -u origin sprint4/p3-criterios
```

Pull Request con el código `S4-P3` en el cuerpo.
