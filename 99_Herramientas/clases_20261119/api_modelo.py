"""Lee las entidades y enumeraciones de SGCPapi (C#) para compararlas con el diagrama de clases."""
import glob, os, re

TIPOS = {"Guid": "UUID", "string": "String", "decimal": "Decimal", "int": "Integer", "long": "Integer",
         "bool": "Boolean", "DateTime": "DateTime", "DateOnly": "Date", "byte[]": "Bytes", "double": "Decimal"}

def leer(api):
    base = os.path.join(api, "src", "SGCP.Api", "Dominio")
    enums = {}
    for f in glob.glob(os.path.join(base, "Enumeraciones", "*.cs")):
        s = open(f, encoding="utf-8").read()
        for m in re.finditer(r"public enum (\w+)\s*\{([^}]*)\}", s):
            enums[m.group(1)] = [x.strip().split("=")[0].strip() for x in re.sub(r"//.*", "", m.group(2)).split(",") if x.strip()]
    clases = {}
    for f in glob.glob(os.path.join(base, "Entidades", "*.cs")):
        s = open(f, encoding="utf-8").read()
        for m in re.finditer(r"public (?:abstract |sealed )?class (\w+)(?:\s*:\s*(\w+))?\s*\{", s):
            nombre = m.group(1)
            # cuerpo hasta la llave que cierra
            i, n = m.end(), 1
            while n and i < len(s):
                n += {"{": 1, "}": -1}.get(s[i], 0); i += 1
            cuerpo = s[m.end():i - 1]
            props = []
            for p in re.finditer(r"public\s+(?:virtual\s+|required\s+)?([\w<>\[\]?,. ]+?)\s+(\w+)\s*(?:\{|=>)", cuerpo):
                tipo, prop = p.group(1).strip(), p.group(2)
                if "(" in tipo:
                    continue
                props.append((prop, tipo))
            clases[nombre] = {"base": m.group(2), "props": props}
    return clases, enums

def clasificar(clases, enums):
    """Separa atributos, claves foráneas y navegaciones."""
    out = {}
    for c, d in clases.items():
        attrs, fks, navs = [], [], []
        for p, t in d["props"]:
            tb = t.rstrip("?")
            col = re.match(r"(?:ICollection|List|IList|IEnumerable|HashSet)<(\w+)>", tb)
            if col:
                navs.append((p, col.group(1), "*")); continue
            if tb in clases:
                navs.append((p, tb, "1")); continue
            if p.endswith("Id") and tb == "Guid" and p != "Id":
                fks.append((p, t)); continue
            uml = TIPOS.get(tb, tb) + ("?" if t.endswith("?") and tb != "string" else "")
            attrs.append((p[0].lower() + p[1:], uml))
        out[c] = {"attrs": attrs, "fks": fks, "navs": navs, "base": d["base"]}
    return out
