from django.urls import path

from .views import PerfilView, RegistroView, UsuarioListView, UsuarioUpdateView

app_name = "usuarios"

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
    path("usuarios/", UsuarioListView.as_view(), name="list"),
    path("usuarios/<int:pk>/editar/", UsuarioUpdateView.as_view(), name="update"),
]

