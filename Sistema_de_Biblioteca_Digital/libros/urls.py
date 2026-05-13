from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.lista_libros,
        name='lista_libros'
    ),

    path(
        'crear/',
        views.crear_libro,
        name='crear_libro'
    ),

    path(
    'editar/<int:libro_id>/',
    views.editar_libro,
    name='editar_libro'
    ),

    path(
    'autores/',
    views.lista_autores,
    name='lista_autores'
    ),

    path(
        'categorias/',
        views.lista_categorias,
        name='lista_categorias'
    ),

]