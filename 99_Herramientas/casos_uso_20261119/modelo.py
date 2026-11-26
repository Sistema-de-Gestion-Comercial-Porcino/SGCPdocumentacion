"""Contenido del diagrama de casos de uso del SGCC (19 nov 2026).

Fuente: SGCPapi main (DatosIniciales.cs, RolesSistema.cs, ReportesFacade.cs) y el menú
de SGCPuiweb (Views/Shared/_Layout.cshtml). Cada actor aparece una sola vez.
"""

# clave, nombre visible, lado
ACTORES = [
    ("SA", "Superadministrador", "izq"),
    ("PR", "Propietario", "izq"),
    ("AD", "Administrador", "izq"),
    ("FI", "Finanzas", "izq"),
    ("CO", "Comprador", "der"),
    ("VE", "Ventas", "der"),
    ("PD", "Producción", "der"),
    ("AL", "Almacén", "der"),
    ("EN", "Responsable de entrega", "der"),
]

# Generalización (hijo -> padre): el hijo hereda los casos del padre. Nivel 100 > 80 > 60.
GENERALIZACIONES = [("SA", "PR"), ("PR", "AD")]

# clave, nombre, secciones del menú (web/Android), es_extension, documentación
CASOS = [
    ("CU01", "CU01 · Gestionar acceso", "Iniciar sesión · Registro · Recuperar acceso", False,
     "Cuenta: iniciar sesión, registrarse como comprador, recuperar y restablecer la clave, cerrar sesión."),
    ("CU13", "CU13 · Administrar cuentas de nivel superior", "Usuarios › cuentas de Propietario y Superadministrador", True,
     "Solo el Superadministrador modifica cuentas de Propietario o de otro Superadministrador. No se puede desactivar al último Superadministrador activo."),
    ("CU02", "CU02 · Administrar usuarios", "Usuarios", False,
     "Usuarios: consultar, crear, editar, asignar roles de nivel inferior al propio, desactivar y habilitar. Nadie se autoeleva privilegios."),
    ("CU14", "CU14 · Delegar rol de Finanzas", "Usuarios › rol FINANZAS", True,
     "Solo el Propietario (o el Superadministrador) asigna o retira el rol FINANZAS. El Administrador no puede."),
    ("CU03", "CU03 · Gestionar clientes", "Clientes", False,
     "Clientes: alta con tipo y número de documento únicos, edición, baja con regla de historial y pedidos del cliente."),
    ("CU07", "CU07 · Gestionar productos", "Productos · Clasificaciones", False,
     "Productos y clasificaciones del catálogo. El comprador y el personal operativo solo consultan."),
    ("CU04", "CU04 · Gestión de costos", "Gestión de costos", False,
     "Gestión de costos: costo de reposición y precio vigente por producto; Ventas consulta."),
    ("CU05", "CU05 · Gestión de cotizaciones", "Cotizaciones", False,
     "Cotizaciones: Ventas prepara y presenta; el comprador acepta o rechaza las suyas."),
    ("CU06", "CU06 · Gestionar pedidos", "Pedidos", False,
     "Pedidos: confirmar desde una cotización aceptada, condición de pago, señas y cancelación con motivo."),
    ("CU08", "CU08 · Gestionar producción", "Sanidad · Producción · Incidencias", False,
     "Producción e inventario: control sanitario, faeneo/desposte y fabricación de derivados."),
    ("CU09", "CU09 · Gestionar inventario", "Existencias · Pesajes y entradas · Pedidos por preparar · Control de frío", False,
     "Producción e inventario: existencias, pesajes y entradas a almacén, control de frío."),
    ("CU10", "CU10 · Gestionar pagos y cobranza", "Saldos y pagos · Seguimiento", False,
     "Cobranza: cargos, señas, pagos, crédito, saldos y comprobante fiscal."),
    ("CU11", "CU11 · Gestionar transporte y entregas", "Entregas · Rutas · Transportes · Conflictos de recepción", False,
     "Transporte y entregas: preparar y asignar entregas, rutas, transportes; captura sin conexión en Android; revisión de conflictos de recepción."),
    ("CU12", "CU12 · Gestionar reportes", "Reportes · Mis reportes · Constancia de entrega", False,
     "Consultas: reportes en PDF/Excel según la matriz de cada rol; el comprador ve solo los suyos y descarga la constancia."),
    ("CU15", "CU15 · Consultar auditoría", "Auditoría", True,
     "Consultas: registro de auditoría de solo lectura (permiso auditoria.consultar)."),
]

# extensión -> caso base
EXTENSIONES = [("CU13", "CU02"), ("CU14", "CU02"), ("CU15", "CU12")]

ASOCIACIONES = {
    "SA": ["CU13"],
    "PR": ["CU14", "CU04", "CU05", "CU06", "CU10", "CU15"],
    "AD": ["CU01", "CU02", "CU03", "CU07", "CU08", "CU09", "CU11", "CU12"],
    "FI": ["CU01", "CU03", "CU04", "CU06", "CU07", "CU10", "CU12"],
    "VE": ["CU01", "CU03", "CU04", "CU05", "CU06", "CU07", "CU10", "CU11", "CU12"],
    "CO": ["CU01", "CU05", "CU06", "CU07", "CU11", "CU12"],
    "PD": ["CU01", "CU07", "CU08", "CU09", "CU12"],
    "AL": ["CU01", "CU07", "CU08", "CU09", "CU12"],
    "EN": ["CU01", "CU07", "CU09", "CU11", "CU12"],
}
