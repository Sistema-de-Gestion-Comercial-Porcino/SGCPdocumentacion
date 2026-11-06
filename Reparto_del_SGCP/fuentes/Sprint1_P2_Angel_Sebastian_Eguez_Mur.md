# Sprint 1 · Parte 2 · Angel Sebastian Eguez Mur

Código de seguimiento: **S1-P2**. Rol: Desarrollador. Repositorios: **SGCPuiweb** y **SGCPuimovil**.

## Estado: la web entregada, el APK sin probar en un dispositivo

La web del Sprint 1 está construida y verificada: 8 páginas responden y el formulario de precios guarda los decimales exactos. La aplicación Android compila y sus pruebas unitarias pasan, pero **nunca se ejecutó en un teléfono real**. Eso es lo que queda abierto y es tu pendiente.

## Qué quedó hecho

**SGCPuiweb**: ASP.NET Core MVC con vistas Razor renderizadas en el servidor, Bootstrap y jQuery-validation. Pantallas de acceso, registro, recuperación, usuarios, clientes, clasificaciones, productos, precios, cotizaciones y pedidos. Sin EF Core: todo pasa por la API.

**SGCPuimovil**: Kotlin nativo con la base técnica y el acceso con dirección de API configurable. La captura sin conexión es Sprint 3.

## Tu tarea abierta

### Instalar el APK en un teléfono y probar el acceso · RNF-05

El archivo ya está compilado:

```
SGCPuimovil/app/build/outputs/apk/debug/app-debug.apk
```

Se copia al teléfono y se instala permitiendo orígenes desconocidos.

Lo que más falla, y conviene saberlo antes de pelearse con el teléfono: en la pantalla de acceso hay un campo para la dirección de la API, y tiene que ser la **IP de red** de la máquina donde corre la API, **no `localhost`**. El teléfono no resuelve el `localhost` de la laptop. Se averigua con `ipconfig` en Windows o `ip addr` en Linux, y los dos equipos tienen que estar en el mismo wifi. Si el firewall de Windows bloquea el puerto, hay que abrirlo solo para la red local.

El recorrido mínimo: instalar, configurar la dirección, entrar con una cuenta, y comprobar que la sesión se mantiene.

Lo que hay que dejar escrito, porque es la evidencia que falta:

- Marca y modelo del teléfono.
- Versión de Android. El proyecto declara API 26 como mínimo.
- Si instaló sin problemas.
- Si el acceso funcionó contra la API del equipo.
- Qué no funcionó, si algo no funcionó.

RNF-05 pide compatibilidad con los dispositivos acordados. Sin un dispositivo real probado, ese requerimiento no tiene evidencia de ninguna clase.

**Entregás:** una nota de media página en `00_Definicion/`. **Se comprueba:** dice modelo, versión de Android y resultado del acceso.

### Si hay que recompilar

```bash
cd SGCPuimovil
./gradlew assembleDebug
```

Hace falta `local.properties` con la ruta del SDK de Android, que es propia de cada máquina y por eso no está en el repositorio:

```
sdk.dir=C:\\Users\\TuUsuario\\AppData\\Local\\Android\\Sdk
```

Y `JAVA_HOME` apuntando a un JDK 21.

## Lo que no te toca

Las dos mediciones pendientes: RNF-02 es de S1-P4 y RNF-04 de S1-P3.

## Dos cosas que vas a querer saber antes del Sprint 2

Los dos defectos más caros del Sprint 1 fueron tuyos por terreno y los dos salieron de lo mismo, la configuración regional. Están en `00_Definicion/Errores_encontrados_Sprint1.md`:

1. **Un `[Range(typeof(decimal), "0.01", ...)]` sin `ParseLimitsInInvariantCulture`** devolvía error 500 en toda pantalla con decimales, en cualquier máquina configurada en español.
2. **El enlace de formularios leía los decimales con la cultura local**, así que Bs 88,50 se guardaba como 8850 **sin mostrar ningún error**. Ese es el peor tipo de defecto: el que no avisa.

El segundo está resuelto para todo el repositorio por `Models/EnlaceDecimalInvariante.cs`. No hay que hacer nada más que no romperlo. El primero vuelve con cada atributo `[Range]` nuevo sobre un decimal, y en el Sprint 2 vas a cargar pesos y temperaturas.

Y la regla de prueba que sale de ahí: **probá con `LANG=es_BO.UTF-8`**, no con la variable sin definir. Sin ella, .NET usa cultura invariante y los dos defectos desaparecen: las pruebas pasan con el sistema roto. Así se escaparon.

## Sobre cambiar la web a React

Se discutió pasar el frontend a React para que el renderizado lo haga el navegador. **No está decidido y no es parte de ningún sprint todavía.** La recomendación registrada es dejarlo para el Sprint 5 de reserva, en un repositorio aparte, por tres razones: la web actual funciona y está verificada, el trabajo de datos lo hace la API y no cambiaría, y el JWT hoy viaja en una cookie del servidor, que es más seguro que guardarlo en el navegador.

Lo que sí es cierto, y conviene saberlo: la arquitectura ya lo permite sin tocar la API, porque la web es un cliente puro. Es una decisión reversible, no urgente.
