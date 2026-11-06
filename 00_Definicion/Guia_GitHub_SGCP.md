# Crear los tres repositorios de la organización

Las carpetas SGCPapi, SGCPuiweb y SGCPuimovil ya existen y están vacías. Git registra archivos; una carpeta vacía no se sube como proyecto por sí sola.

1. En GitHub, entra a tu organización y abre **Repositories → New repository**.
2. En **Owner**, selecciona la organización. Crea **SGCPapi**, **SGCPuiweb** y **SGCPuimovil** por separado. Puedes comenzar con visibilidad privada y activar **Add a README file**; así cada repositorio tendrá su primer commit.
3. Copia el identificador de la organización desde su URL: `https://github.com/IDENTIFICADOR`. El nombre visible puede contener espacios, pero la URL usa otro identificador.
4. Desde una terminal, clona cada repositorio dentro de su carpeta vacía. Sustituye `TU_ORGANIZACION` por ese identificador:

```bash
cd /home/supergenio/Escritorio/TareaSoftware/Modelado_Chancheria
git clone https://github.com/TU_ORGANIZACION/SGCPapi.git SGCPapi
git clone https://github.com/TU_ORGANIZACION/SGCPuiweb.git SGCPuiweb
git clone https://github.com/TU_ORGANIZACION/SGCPuimovil.git SGCPuimovil
```

Git permite clonar en una carpeta existente si está vacía. Cuando termines, cada una tendrá su propio `.git` y README. No ejecutes `git init` en Modelado_Chancheria para combinar los tres proyectos.

Para repositorios privados debes autenticar Git. Si tienes GitHub CLI, usa `gh auth login`, elige GitHub.com, HTTPS y acceso mediante navegador; acepta configurar las credenciales de Git. También puedes usar un token de acceso con los permisos necesarios: la contraseña normal de GitHub no sirve para Git por HTTPS. No pongas tokens dentro de los comandos, archivos o capturas.

Cuando exista código, entra en el repositorio correspondiente y ejecuta:

```bash
git add .
git commit -m "Iniciar proyecto"
git push
```

Antes del primer commit de código, configura el `.gitignore` de su tecnología para excluir dependencias, compilados y archivos locales con credenciales. Las variables secretas quedan fuera del repositorio; una plantilla de configuración puede contener nombres y valores de ejemplo.

La organización administra los repositorios: invita a tus compañeros y asigna acceso desde sus ajustes de miembros/equipos o desde **Settings → Collaborators and teams** del repositorio. No compartan una misma cuenta.

Los repositorios remotos los creas tú siguiendo estos pasos; esta tarea creó únicamente las tres carpetas locales vacías.

Fuentes oficiales: [Crear repositorio](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository), [Clonar repositorio](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
