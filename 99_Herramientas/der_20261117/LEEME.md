# Generador del DER del SGCC

Genera `02_Ingenieria_de_Software/DER/`: el diagrama entidad-relación en notación de Chen, derivado de `01_Generales/Clases_SGCC.mdj`.

```bash
python3 -I armar_todo.py ../../02_Ingenieria_de_Software/DER
```

Solo necesita Python 3 y Pillow. Las fuentes son DejaVu, en `/usr/share/fonts/truetype/dejavu/`.

| Archivo | Qué contiene |
|---|---|
| `gen_der.py` | Motor: geometría Chen, verificador de choques, PNG con Pillow y `.drawio` multipágina con las mismas coordenadas |
| `paginas.py` | Hojas 1 a 7: entidades, atributos (`*` clave, `#` discriminador, `~` derivado), posiciones y relaciones con multiplicidad UML |
| `general.py` | Lista de las 41 entidades y 59 relaciones de la vista general, y búsqueda del acomodo en grilla por recocido simulado |
| `gen_32.json`, `ov.py` | Acomodo elegido para la vista general y ajustes manuales de rombos |
| `general_attrs.py`, `attr_overrides.json` | Vista general con atributos: lado de los atributos de cada entidad, ya fijado |
| `init_manual.py` | Acomodo inicial por módulos con que se refinó la búsqueda |

Para cambiar el modelo, edita `paginas.py` (atributos) y `general.py` (relaciones). Después corre `armar_todo.py`. Si el verificador reporta choques, mueve el rombo afectado en `ov.py` o `attr_overrides.json`.
