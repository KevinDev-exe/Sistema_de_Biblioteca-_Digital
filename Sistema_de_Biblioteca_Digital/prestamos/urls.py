from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.lista_prestamos,
        name='lista_prestamos'
    ),

    path(
        'nuevo/',
        views.crear_prestamo,
        name='crear_prestamo'
    ),

    path(
        '<int:prestamo_id>/devolver/',
        views.devolver_prestamo,
        name='devolver_prestamo'
    ),

    path(
        '<int:prestamo_id>/',
        views.detalle_prestamo,
        name='detalle_prestamo'
    ),

    path(
        'reservar/<int:libro_id>/',
        views.reservar_libro,
        name='reservar_libro'
    ),

]