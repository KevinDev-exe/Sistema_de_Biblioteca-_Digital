from django.urls import path

from .views import (
    MisPrestamosView,
    PrestamoCreateView,
    PrestamoDeleteView,
    PrestamoListView,
    PrestamoUpdateView,
    marcar_devuelto,
)

app_name = "prestamos"

urlpatterns = [
    path("", PrestamoListView.as_view(), name="list"),
    path("mis-prestamos/", MisPrestamosView.as_view(), name="mis_prestamos"),
    path("crear/", PrestamoCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", PrestamoUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", PrestamoDeleteView.as_view(), name="delete"),
    path("<int:pk>/devolver/", marcar_devuelto, name="devolver"),
]

