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
        'eliminar/<int:libro_id>/',
        views.eliminar_libro,
        name='eliminar_libro'
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

    path(
    'autores/nuevo/',
    views.crear_autor,
    name='crear_autor'
    ),

    path(
        'autores/editar/<int:autor_id>/',
        views.editar_autor,
        name='editar_autor'
    ),

    path(
        'autores/eliminar/<int:autor_id>/',
        views.eliminar_autor,
        name='eliminar_autor'
    ),

    path(
        'categorias/nueva/',
        views.crear_categoria,
        name='crear_categoria'
    ),

    path(
        'categorias/editar/<int:categoria_id>/',
        views.editar_categoria,
        name='editar_categoria'
    ),

    path(
        'categorias/eliminar/<int:categoria_id>/',
        views.eliminar_categoria,
        name='eliminar_categoria'
    ),

]