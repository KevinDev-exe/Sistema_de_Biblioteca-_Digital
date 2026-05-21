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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def inicio(request):

    return redirect('login')


urlpatterns = [

    path('', inicio),
    path('admin/',admin.site.urls),
    path('',include('accounts.urls')),
    path('libros/',include('libros.urls')),
    path('prestamos/', include('prestamos.urls')),
    path('', include('dashboard.urls')),
    path('reportes/', include('reportes.urls')),
    path('reservas/', include('reservas.urls')),
    
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
