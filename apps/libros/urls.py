from django.urls import path

from .views import (
    AutorCreateView,
    AutorDeleteView,
    AutorListView,
    AutorUpdateView,
    CatalogoView,
    CategoriaCreateView,
    CategoriaDeleteView,
    CategoriaListView,
    CategoriaUpdateView,
    LibroCreateView,
    LibroDeleteView,
    LibroDetailView,
    LibroListView,
    LibroUpdateView,
)

app_name = "libros"

urlpatterns = [
    path("", CatalogoView.as_view(), name="catalogo"),
    path("admin/libros/", LibroListView.as_view(), name="libro_list"),
    path("admin/libros/crear/", LibroCreateView.as_view(), name="libro_create"),
    path("admin/libros/<int:pk>/editar/", LibroUpdateView.as_view(), name="libro_update"),
    path("admin/libros/<int:pk>/eliminar/", LibroDeleteView.as_view(), name="libro_delete"),
    path("<int:pk>/", LibroDetailView.as_view(), name="libro_detail"),
    path("autores/", AutorListView.as_view(), name="autor_list"),
    path("autores/crear/", AutorCreateView.as_view(), name="autor_create"),
    path("autores/<int:pk>/editar/", AutorUpdateView.as_view(), name="autor_update"),
    path("autores/<int:pk>/eliminar/", AutorDeleteView.as_view(), name="autor_delete"),
    path("categorias/", CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/crear/", CategoriaCreateView.as_view(), name="categoria_create"),
    path("categorias/<int:pk>/editar/", CategoriaUpdateView.as_view(), name="categoria_update"),
    path("categorias/<int:pk>/eliminar/", CategoriaDeleteView.as_view(), name="categoria_delete"),
]

