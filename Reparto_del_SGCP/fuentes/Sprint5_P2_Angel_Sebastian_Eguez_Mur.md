# Sprint 5 · Parte 2 · Angel Sebastian Eguez Mur

Código de seguimiento: **S5-P2**. Rol: Desarrollador. Repositorios: **SGCPuiweb**, **SGCPuimovil** y, si se hace, **SGCPuireact**.

> Sprint de reserva. **Nada de acá se arranca sin la lista de pendientes de S5-P4.** Las tareas 1 y 2 son pendientes reales y van siempre; las demás son condicionales.

## Qué te toca

Cerrar los pendientes de web y Android, probar el APK en un teléfono de verdad, y —si todo lo demás está cerrado y el equipo lo decide— la prueba acotada de React.

## Tus tareas

### 1. El APK en un teléfono físico · siempre, es un pendiente del Sprint 1

Quedó pendiente desde el Sprint 1 y es la prueba que ningún emulador reemplaza. Hay cuatro cosas que solo se ven en un teléfono real:

- **Los permisos de cámara y almacenamiento** en una versión de Android real, con el usuario aceptando o rechazando. Un rechazo no puede dejar la aplicación trabada.
- **La captura sin red de verdad**, con el modo avión puesto, no con el servidor apagado. Son situaciones distintas: sin red el sistema operativo corta antes, y los errores que aparecen no son los mismos.
- **Las fotos reales**, de varios megas, no las del emulador. Es donde aparece el problema de memoria si no se redimensionan.
- **Cómo se ve en una pantalla chica**, con el teclado abierto tapando la mitad.

Anotá el modelo del teléfono, la versión de Android y qué pasó en cada punto. Con capturas, que sirven para la defensa.

**Entregás:** una página con el resultado y las capturas. **Se comprueba:** hay un modelo y una versión anotados, no «se probó en Android».

### 2. Repasar web y Android

Sin agregar nada:

- Los dos proyectos compilan sin errores ni advertencias.
- Ninguna pantalla con texto de relleno, botones muertos o enlaces roto.
- Los mensajes de error no muestran rutas, consultas ni nombres de clases.
- Las pantallas se ven bien en una ventana angosta.
- La aplicación Android no tiene credenciales ni direcciones fijas en el código: van en configuración.
- Lo que escribe el usuario se muestra escapado.

**Entregás:** una lista corta de lo corregido. **Se comprueba:** los dos proyectos limpios.

### 3. La prueba de React · condicional, y la última de la cola

**Tres condiciones, las tres:** los sprints 1 a 4 cerrados, los pendientes de arriba hechos, y el equipo de acuerdo. Si falta una, esta tarea no se hace.

Si va:

**Repositorio nuevo, `SGCPuireact`.** No se toca `SGCPuiweb`. Eso es lo que hace que la prueba no tenga riesgo: si no sale, se descarta el repositorio y no pasó nada.

**Dos o tres pantallas, de solo lectura.** El catálogo de productos y el listado de pedidos. Nada que escriba: sin formularios, sin confirmaciones, sin pagos. Las pantallas que escriben son las que tienen validación, y duplicar validación es exactamente lo que no queremos.

**Consumiendo el API que ya existe**, con el token, igual que la aplicación Android.

Lo que hay que resolver y conviene saber de antes, porque es donde se va el tiempo:

- **Dónde se guarda el token** en el navegador. Es una decisión de seguridad, no de comodidad, y hay que poder explicarla.
- **CORS**, que lo configura S5-P1 para tu origen.
- **Qué se muestra mientras carga y si falla.** En Razor la página llega armada; en React llega vacía y se llena. Una pantalla en blanco de dos segundos se ve peor que una página lenta, y una llamada que falla sin aviso se ve como un sistema roto.

Para la defensa, el argumento es este y conviene decirlo así: **demuestra que el API sirve para cualquier cliente.** No es que React sea mejor que Razor; es que la arquitectura permite los dos, y ya lo demostraba con Android.

Y anotá honestamente qué costó. Un «esto funcionó, nos llevó tanto, y reescribir todo habría llevado tanto más» es una conclusión de ingeniería. Es lo más valioso que deja la tarea.

**Entregás:** el repositorio con las pantallas y una página con la conclusión. **Se comprueba:** `SGCPuiweb` quedó sin tocar, verificable en el historial.

### 4. RF-09 en la pantalla · solo si se aprueba

Si RF-09 va, la pantalla de alertas para almacén y producción: producto, stock, umbral, fecha y estado.

Una sola cosa: que las alertas abiertas se vean de un vistazo, separadas de las cerradas. Una lista de doscientas alertas mezcladas no sirve para nada.

**Entregás:** la pantalla. **Se comprueba:** se ve lo que está abierto sin tener que filtrar.

## Qué no te toca

El API ni CORS: S5-P1. Decidir si React se hace: es del equipo, con S5-P4 confirmando que lo demás cerró.

## De quién dependés y quién depende de vos

**Dependés de S5-P4** para la lista de pendientes y para saber si hay margen para React, y de **S5-P1** para CORS si se hace.

Las tareas 1 y 2 no dependen de nadie y hay que hacerlas igual. Arrancá por la 1: es la que lleva más tiempo conseguir, porque hay que tener el teléfono a mano.

## Cómo entregarlo

```bash
git checkout -b sprint5/p2-ui-cierre
git commit -m "v5.2.0 - Sprint 5 - APK en dispositivo y cierre de interfaces"
git push -u origin sprint5/p2-ui-cierre
```

Pull Request con el código `S5-P2` en el cuerpo. Si se hace React, va en su propio repositorio con su propio commit inicial.
