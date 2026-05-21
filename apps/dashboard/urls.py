from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/libros-reservados/", views.chart_libros_reservados, name="chart_libros_reservados"),
    path("dashboard/prestamos-mes/", views.chart_prestamos_mes, name="chart_prestamos_mes"),
    path("dashboard/categorias/", views.chart_categorias, name="chart_categorias"),
    path("dashboard/autores-leidos/", views.chart_autores_leidos, name="chart_autores_leidos"),
]

