# Casos de uso del SGCC (19 nov 2026)

Rehace `02_Ingenieria_de_Software/01_Generales/Casos_de_Uso_SGCC.mdj` sin JavaScript, con Python.

- `modelo.py`: actores (los 9 roles de SGCPapi), casos CU01–CU12 con las secciones del menú de la web entre paréntesis, extensiones y asociaciones. Fuente: `DatosIniciales.cs`, `RolesSistema.cs`, `ReportesFacade.cs` y `_Layout.cshtml` de SGCPuiweb.
- `disposicion.py` y `actores.json`: coordenadas. Cada línea llega al extremo izquierdo o derecho de su elipse, por eso ninguna atraviesa otro caso.
- `generar_mdj.py <ruta a 02_Ingenieria_de_Software>`: escribe el `.mdj` (vistas clonadas del formato de StarUML) y el PNG de vista previa. Después copiar el `.mdj` a `Entrega/`.
- `actualizar_roles.py <ruta>`: lleva los roles nuevos a colaboración, secuencias, actividades, objetos, estados y BPMN propuesto (individuales, consolidados y `Entrega/`). Es idempotente. No toca `BPMN_Actual` (proceso AS-IS).

Reglas del diagrama: cada actor aparece una sola vez. Superadministrador ▷ Propietario ▷ Administrador es una generalización (el hijo hereda los casos del padre). Finanzas es un rol delegado por el Propietario.
