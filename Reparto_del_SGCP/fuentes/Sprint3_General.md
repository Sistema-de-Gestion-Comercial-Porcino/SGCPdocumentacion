# Sprint 3 · Documento general

Pagos, crédito, transportes, rutas y entregas. Android Kotlin con captura de recepción sin conexión, evidencia y sincronización.

Alcance tomado del Sprint Backlog de `Formato Proyecto - SGCC Actualizado.xlsx`.

> **Este es el sprint más difícil del proyecto.** No por la cantidad de requerimientos, sino porque introduce lo único que no es una pantalla más contra una API: datos que se crean sin conexión, en un dispositivo, y que después tienen que llegar al servidor sin duplicarse. Eso se llama sincronización y es donde fallan los sistemas reales.

## Qué entra en este sprint

| Código | Nombre | Parte responsable |
|---|---|---|
| RF-05 | Registrar condición de pago acordada | S3-P1, S3-P2 |
| RF-06 | Consultar saldo por cliente y concepto | S3-P1, S3-P2 |
| RF-07 | Registrar evidencia de entrega | S3-P1, S3-P2 |
| RF-08 | Gestionar transporte y rutas | S3-P1, S3-P2 |
| RF-19 | Registrar seña o pago anticipado | S3-P1, S3-P2 |
| RNF-01 | Fiabilidad: recepción sin conexión en Android | S3-P1, S3-P2, S3-P4 |
| RNF-05 | Compatibilidad de dispositivos | S3-P2, S3-P4 |

Actor nuevo: **ACT-05 Responsable de entrega**, que administra transportes, rutas, frío y recepción, y es el único que usa Android para descargar entregas y enviar lo capturado.

## El criterio de validación, palabra por palabra

> Captura pendiente hasta sincronizar. Conforme: ENTREGADA; con observaciones: OBSERVADA. El reintento no duplica datos y los conflictos requieren revisión. Entrega y deuda mantienen estados independientes.

Cuatro afirmaciones, y las cuatro son sobre estado:

1. **Una captura hecha sin conexión está «pendiente» hasta que se sincroniza.** No es una entrega todavía. En el teléfono se ve pendiente y en el servidor no existe.
2. **Conforme da ENTREGADA; con observaciones da OBSERVADA.** Son dos estados distintos y una observación no es un rechazo: la entrega ocurrió, con reparos.
3. **El reintento no duplica datos.** Si el teléfono manda lo mismo dos veces porque se cortó la conexión, el servidor tiene que guardar uno. Y si hay conflicto, **lo revisa una persona**: no se sobrescribe automáticamente.
4. **Entrega y deuda son independientes.** Que la mercadería llegue no cancela la deuda, y que se pague no implica que llegó. Son dos estados que avanzan por separado.

## Lo que este sprint no hace

- No hay reportes ni exportación a PDF o Excel: Sprint 4.
- No hay constancia de entrega: es RF-14, Sprint 4, y depende de que la recepción conforme esté confirmada en el servidor.
- No hay integración fiscal: Sprint 4 y condicional.
- **No hay operaciones comerciales sin conexión.** Lo único que Android captura sin señal es la **recepción de entregas ya asignadas, autorizadas y descargadas**. No se cotiza, no se vende, no se cobra sin conexión. El perfil de proyecto lo dice explícitamente y es el límite más importante del sprint.
- No hay devolución ni retención automática de señas. Si una seña se cancela, se registra el acuerdo de resolución; el sistema no decide.
- El crédito **no liquida deuda**. Autorizar crédito no es cobrar.

## Reparto

| Código | Integrante | Trabajo | Empieza |
|---|---|---|---|
| S3-P1 | Dario Haziel Tambo Parra | API: pagos, saldos, transporte, rutas, entregas, endpoint de sincronización idempotente, Strategy y Facade | Primero |
| S3-P2 | Angel Sebastian Eguez Mur | Android con Room y captura sin conexión, Command y State; pantallas web de pagos, transporte y entregas | Cuando P1 publique el contrato de sincronización |
| S3-P3 | Sofia Cuellar Roca | Criterios, guion de prueba sin conexión, validación | En paralelo con P1; cierra validando |
| S3-P4 | Victor Manuel Manrique Arancivia | Diagramas de estado, pruebas de duplicados y conflictos, RNF-01 y RNF-05, versión y entrega | En paralelo con P1; cierra entregando |

El reparto tiene un desbalance real: **S3-P2 es la parte más cargada del proyecto**, porque Android pasa de tener solo acceso a tener almacenamiento local, captura de evidencia y sincronización. Conviene reconocerlo al planificar y, si hace falta, que S3-P1 tome las pantallas web de pagos y transporte para que S3-P2 se concentre en Android.

## El modelo de datos nuevo

| Entidad | Para qué | Reglas que la gobiernan |
|---|---|---|
| `CondicionPago` | Contado o crédito autorizado, con importe y vencimiento | Acordada por operación. **No** hay plazo por defecto |
| `Cargo` | Lo que el cliente debe, separado en producto y servicio | Ya empieza en el Sprint 2 con RF-20 |
| `Pago` | Pago aplicado a cargos | Un pago se aplica una sola vez |
| `Sena` | Pago anticipado con referencia, importe, fecha y medio | Se aplica **una sola vez**. Si se cancela, se registra el acuerdo |
| `Transporte` | Propio o externo, con transportista, vehículo y estado | Se desactiva sin borrar historial |
| `Ruta` | Transporte, responsable y entregas preparadas | |
| `Entrega` | Lo que se despacha a un cliente | Estado propio, independiente de la deuda |
| `Recepcion` | Receptor, fecha real, peso, conformidad, observaciones, evidencia | Llega del teléfono o se carga en la web |
| `EvidenciaRecepcion` | Archivo de respaldo de la recepción | |

El saldo **no se guarda**: se calcula como cargos menos pagos aplicados, distinguiendo producto, servicio, contado, crédito vigente y vencido. Guardar un saldo acumulado es la forma más rápida de tener dos números que no coinciden.

## La sincronización, que es el corazón del sprint

Hay que acordarlo entre S3-P1 y S3-P2 **antes** de escribir código de los dos lados. Es el único punto del proyecto donde dos partes tienen que ponerse de acuerdo en un contrato antes de empezar.

Lo que RNF-01 exige guardar en el teléfono, textual: «clave única, versión base, autor, fecha real, datos y evidencia». Cada uno de esos campos tiene una razón:

| Campo | Para qué sirve |
|---|---|
| Clave única | Generada **en el teléfono**. Es lo que permite que un reintento no duplique |
| Versión base | Sobre qué versión del dato se capturó. Es lo que detecta el conflicto |
| Autor | Quién capturó |
| Fecha real | Cuándo ocurrió físicamente, distinta de cuándo se sincronizó |
| Datos y evidencia | El contenido |

La clave única la genera el cliente, no el servidor. Es la diferencia entre un reintento que es inofensivo y uno que duplica: si el servidor ya vio esa clave, responde que ya existe en lugar de crear otra fila.

Y RNF-06 pide distinguir **fecha física y fecha de sincronización**. Son dos campos, no uno: una recepción puede haber ocurrido el martes y llegar al servidor el jueves.

## Los patrones de este sprint

Tres de los seis, y los tres caen acá porque es donde hay estado y variantes.

| Patrón | Dónde | Para qué |
|---|---|---|
| Strategy | API | La condición comercial del despacho. Contado y crédito se resuelven distinto y se esperan más modalidades |
| Command | Android | Cada captura sin conexión es una orden que se guarda, se encola y se reintenta. Es lo que hace que el reintento sea natural en lugar de un parche |
| State | Android | Los estados de la entrega: pendiente, sincronizada, entregada, observada. Las transiciones válidas están en el patrón, no en condicionales repartidos |

Command y State encajan tan bien acá que conviene decirlo en la defensa: no se eligieron para cumplir con el requisito de usar patrones, se eligieron porque el problema tiene exactamente esa forma.

## Riesgos de este sprint

| Riesgo | Por qué importa | Qué hacer |
|---|---|---|
| El contrato de sincronización se define tarde | Bloquea a los dos lados y es lo más difícil de cambiar después | Acordarlo en la primera semana, antes de escribir código |
| Sincronización que duplica | Rompe el criterio de validación y es difícil de ver | Clave única generada en el cliente, más restricción de unicidad en la base |
| Resolver conflictos automáticamente | El Excel pide revisión humana | El conflicto se marca y espera a una persona. No se sobrescribe |
| S3-P2 sobrecargado | Es la parte más grande del proyecto | Pasar las pantallas web de pagos y transporte a S3-P1 |
| Probar sin conexión con conexión | No se prueba nada | Modo avión de verdad, no simulado |
| Confundir entrega con cobro | El Excel los separa explícitamente | Dos estados, dos pantallas, ninguna regla que los una |

## Qué significa que el Sprint 3 está terminado

1. Las cuatro afirmaciones del criterio se pueden demostrar en una corrida, **con el teléfono en modo avión** y después sincronizando.
2. Un reintento del mismo envío no crea una segunda recepción, comprobado.
3. Un conflicto queda marcado para revisión y no se sobrescribe, comprobado.
4. Los tres repositorios compilan sin errores ni advertencias.
5. La verificación automática cubre duplicados y conflictos, y pasa contra MySQL real.
6. RNF-05 tiene evidencia: la aplicación corrió en dispositivos reales, con modelo y versión anotados.
7. Los cuatro Pull Requests aprobados y en `main`, con la etiqueta `v3.0.0` puesta por S3-P4.
