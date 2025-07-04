# GalleryNet



En el proyecto, utilicé ayuda de la IA en las siguientes partes (en las partes de javascript):

- **Buscador de servicios/categorías**: Para que al seleccionar una categoría en el buscador, la página se redirija automáticamente a los resultados filtrados.
- **Confirmación de borrado**: Uso de modales para confirmar la eliminación de categorías u otros elementos, mostrando una ventana emergente antes de borrar.
- **Menú de usuario en el header**: Para desplegar el menú de usuario correctamente usando scripts de Bootstrap.
- **Paginación personalizada**: Para mejorar la experiencia de navegación entre páginas de obras, con controles de paginación dinámicos.

## ¿Qué partes tiene el proyecto?

- **Usuarios**: Registro, login, perfiles, seguidores.
- **Obras**: Subir, ver y buscar obras de arte.
- **Comisiones**: Pedir y gestionar encargos de arte.
- **Categorías**: Organizar las obras por tipo o tema.
- **Backoffice**: Panel para que el admin gestione usuarios, obras y categorías.

## Tecnologías
- Django (Python)
- HTML, CSS, Bootstrap
- PostgreSQL

## ABI PASAR PROYECTO
1. Clona el repo
2. Crea un entorno virtual
3. Instala las dependencias: `pip install -r requirements.txt`
4. Haz las migraciones: `python manage.py migrate`
5. Arranca el servidor: `python manage.py runserver`

## Estructura de URLs
- `/` página principal
- `/usuarios/` usuarios y perfiles
- `/obras/` galería de arte
- `/comisiones/` encargos
- `/backoffice/` panel admin
- `/categorias/` categorías

