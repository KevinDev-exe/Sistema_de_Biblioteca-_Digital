# Biblioteca Digital

Sistema web profesional desarrollado con Django bajo arquitectura MVT para gestionar libros, autores, categorias, usuarios, prestamos, reservas, dashboard estadistico y reportes exportables.

## Tecnologias

- Django y Python 3
- SQLite para desarrollo local y PostgreSQL para produccion
- Bootstrap 5, HTML5, CSS3 y JavaScript
- Chart.js para graficos dinamicos
- reportlab, pandas y openpyxl para PDF, CSV y Excel
- gunicorn y whitenoise para despliegue

## Funcionalidades

- Registro, login, logout y recuperacion de contrasena
- Roles: Administrador/Bibliotecario y Lector
- CRUD completo de libros, autores, categorias, prestamos y reservas
- Busqueda y filtros por titulo, autor, categoria, estado y usuario
- Validacion de stock, fechas, duplicados y formularios
- Dashboard con totales, actividad reciente y graficos reales
- Reportes PDF, Excel y CSV de libros, usuarios, prestamos, reservas y multas
- Panel admin de Django personalizado
- Interfaz responsive tipo dashboard administrativo
- Configuracion lista para Render, variables de entorno, static y media

## Instalacion local

```bash
cd trabajo_final/Sistema_de_Biblioteca_Digital
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_biblioteca
python manage.py runserver
```

Credenciales de demostracion:

- Administrador: `bibliotecario` / `Admin12345`
- Lector: `lector` / `Lector12345`

## Configuracion

Copia `.env.example` como referencia para produccion. Las variables importantes son:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`

Si `DATABASE_URL` existe y `dj-database-url` esta instalado, el proyecto usa PostgreSQL. Si no existe, usa SQLite local.

## Estructura

```text
Sistema_de_Biblioteca_Digital/
├── apps/
│   ├── usuarios/
│   ├── libros/
│   ├── prestamos/
│   ├── reservas/
│   ├── dashboard/
│   └── reportes/
├── templates/
├── static/
├── media/
├── requirements.txt
├── render.yaml
├── Procfile
└── manage.py
```

## Despliegue en Render

1. Crear un Web Service desde el repositorio.
2. Crear una base de datos PostgreSQL.
3. Configurar `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`.
4. Usar:
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start: `gunicorn Sistema_de_Biblioteca_Digital.wsgi:application`

## Capturas

Agregar capturas del dashboard, catalogo, CRUD de libros y reportes antes de la entrega final.

## URL del proyecto

Pendiente de publicar en Render.

