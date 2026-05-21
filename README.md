# Sistema de Biblioteca Digital

Sistema web para la gestión de una biblioteca digital desarrollado con Django. Permite administrar libros, préstamos, reservas, notificaciones y reportes con roles diferenciados para administradores/bibliotecarios y lectores.

## Características

- Gestión de libros (CRUD con portada, autor, editorial, categoría)
- Préstamos y devoluciones con control de fechas y sanciones
- Reservas de libros
- Dashboard con estadísticas y gráficos
- Notificaciones por correo electrónico
- Reportes exportables
- Roles: Administrador/Bibliotecario y Lector
- Registro de usuarios

## Requisitos

- Python 3.10+
- Django 6.0.5
- Ver `requirements.txt` para dependencias completas

## Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/KevinDev-exe/Sistema_de_Biblioteca-_Digital.git
cd "Sistema_de_Biblioteca_Digital/Sistema_de_Biblioteca_Digital"

# Instalar dependencias
pip install django
pip install -r requirements.txt

# Crear superusuario (opcional, si no existe)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

El servidor se ejecutará en `http://127.0.0.1:8000/`

## Credenciales predefinidas

> **Nota:** Puedes crear tu propio usuario desde la página de registro o desde el panel de administrador. Desde el panel de administrador también puedes cambiar el rol de cualquier usuario (Administrador o Lector).

### Administrador - Panel Django

| Campo    | Valor            |
|----------|------------------|
| Usuario  | `django` |
| Clave    | `12345Abc*` |


### Administrador - Biblioteca

| Campo    | Valor            |
|----------|------------------|
| Usuario  | `django` |
| Clave    | `12345Abc*` |

### Lector - Biblioteca

| Campo    | Valor            |
|----------|------------------|
| Usuario  | `Angie` |
| Clave    | `Prueba123*` |

## Estructura del proyecto

El proyecto está dividido en aplicaciones modulares para facilitar el mantenimiento y la escalabilidad:

```text
Sistema_de_Biblioteca_Digital/
├── accounts/          # Gestión de usuarios, roles, autenticación y perfiles
├── dashboard/         # Panel principal con métricas, gráficos y actividad reciente
├── libros/            # Gestión del catálogo: libros, autores y categorías
├── notificaciones/    # Lógica de envío de correos y alertas del sistema
├── prestamos/         # Registro de préstamos, devoluciones, estados y sanciones
├── reportes/          # Módulo para generar y exportar datos a PDF, Excel y CSV
├── reservas/          # Solicitudes de libros y listas de espera
├── static/            # Archivos estáticos del diseño premium (CSS, JS, iconos)
├── templates/         # Plantillas HTML globales y layouts principales (base.html)
└── Sistema_de_Biblioteca_Digital/ # Configuración principal de Django (settings, urls)
```
