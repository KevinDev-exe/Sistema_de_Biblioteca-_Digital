from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:tipo>/<str:formato>/", views.exportar, name="exportar"),
]

