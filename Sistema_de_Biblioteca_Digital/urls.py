"""
URL configuration for Sistema_de_Biblioteca_Digital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('cuenta/', include('apps.usuarios.urls')),
    path('cuenta/', include('django.contrib.auth.urls')),
    path('libros/', include('apps.libros.urls')),
    path('prestamos/', include('apps.prestamos.urls')),
    path('reservas/', include('apps.reservas.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path(
        'recuperar-password/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "Sistema_de_Biblioteca_Digital.views.error_403"
handler404 = "Sistema_de_Biblioteca_Digital.views.error_404"
handler500 = "Sistema_de_Biblioteca_Digital.views.error_500"
