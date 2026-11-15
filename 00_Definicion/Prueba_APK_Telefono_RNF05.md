# Prueba del APK en un teléfono real · RNF-05

Código de seguimiento: **S1-P2**, el pendiente del Sprint 1. Responsable: Angel Sebastian Eguez Mur, Parte 2. Fecha: 14 de noviembre de 2026, hora de Bolivia (UTC−4).

## Dispositivo

| Campo | Valor |
|---|---|
| Marca | TECNO |
| Modelo | TECNO CK7n |
| Versión de Android | 14 (API 34) |
| Mínimo declarado por el proyecto | Android 8.0 (API 26) |

Los datos se leyeron del propio teléfono con `adb shell getprop` (`ro.product.brand`, `ro.product.model`, `ro.build.version.release` y `ro.build.version.sdk`), no de memoria.

## Qué se instaló

- APK de depuración compilado desde `SGCPuimovil` en `main` (`v1.0.1`), con el JDK 21 de Android Studio y el SDK 36.
- `gradlew assembleDebug testDebugUnitTest`: compilación correcta y pruebas unitarias en verde.
- Instalado por USB con `adb install`.

## Contra qué servidor

- API `SGCPapi` en `main` (`v4.1.0`), en la laptop del desarrollador, levantada con `--urls http://0.0.0.0:5081`.
- MySQL 8.0.30 con las cinco migraciones aplicadas.

## Resultado

Se probó el acceso dos veces, por dos caminos distintos. Las dos funcionaron.

| Prueba | Dirección escrita en la app | Resultado | Comprobación en el servidor |
|---|---|---|---|
| 1 · Por cable USB (`adb reverse tcp:5081 tcp:5081`) | `http://127.0.0.1:5081/api/v1/` | Correcto | Sesión de `admin` en la tabla `sesiones` a las 19:53:32 UTC (15:53 en Bolivia) y `INICIAR_SESION` en la auditoría |
| 2 · **Por wifi**, sin el puente USB | `http://192.168.0.71:5081/api/v1/` | **Correcto** | `CERRAR_SESION` a las 20:01:43 UTC y una sesión nueva a las 20:02:32 UTC (16:02 en Bolivia) |

En las dos pruebas la app muestra «Mis entregas · Hola, Administración. Tu cuenta está conectada al reparto», con los botones «Verificar conexión» y «Cerrar sesión». El aviso «No hay reparto descargado» es lo esperado: la descarga de entregas y la captura sin conexión son del Sprint 3.

Para que la prueba 2 fuera realmente por wifi se quitó el puente USB (`adb reverse --remove-all`). Desde el teléfono, `127.0.0.1:5081` pasó a responder «Connection refused», y `192.168.0.71:5081` aceptaba la conexión. Teléfono y laptop estaban en la misma red, con las direcciones 192.168.0.68 y 192.168.0.71.

Evidencia, en `Evidencias_RNF05/`:

- `TECNO_CK7n_acceso_usb.png`: prueba 1.
- `TECNO_CK7n_acceso_wifi.png`: prueba 2.

## Lo que hizo falta en la laptop para el wifi

Es lo mismo que dice `Como_ejecutar_el_sistema.md` en «El teléfono no conecta», con un detalle más:

1. La red wifi estaba marcada en Windows como **pública**. Con ese perfil, Windows bloquea toda conexión que entra. Se cambió a **privada**.
2. Se abrió el puerto 5081 **solo para redes privadas**:

   ```powershell
   New-NetFirewallRule -DisplayName "SGCP API 5081" -Direction Inbound -Protocol TCP -LocalPort 5081 -Action Allow -Profile Private
   ```

En una red pública, como la de la universidad, la regla no aplica y el puerto sigue cerrado. Para la presentación conviene usar una red privada o el punto de acceso de un teléfono marcado como privado.

## Lo que esta nota no cubre

- **Segundo teléfono.** El Sprint 3 pide al menos dos modelos distintos para RNF-05. Por ahora hay uno.
- **Funciones del Sprint 3:** descarga de entregas, captura sin conexión y sincronización todavía no existen en la app.
- **Modo avión con cable:** con el puente USB activo, el teléfono sigue llegando a la API aunque esté en modo avión. Las pruebas sin conexión del Sprint 3 se tienen que hacer sin `adb reverse`.
