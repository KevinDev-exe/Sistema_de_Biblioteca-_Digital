from django.urls import path

from .views import (
    MisReservasView,
    ReservaCreateView,
    ReservaDeleteView,
    ReservaListView,
    ReservaUpdateView,
    cancelar_reserva,
    reservar_libro,
)

app_name = "reservas"

urlpatterns = [
    path("", ReservaListView.as_view(), name="list"),
    path("mis-reservas/", MisReservasView.as_view(), name="mis_reservas"),
    path("crear/", ReservaCreateView.as_view(), name="create"),
    path("libro/<int:libro_id>/reservar/", reservar_libro, name="reservar_libro"),
    path("<int:pk>/editar/", ReservaUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", ReservaDeleteView.as_view(), name="delete"),
    path("<int:pk>/cancelar/", cancelar_reserva, name="cancelar"),
]

