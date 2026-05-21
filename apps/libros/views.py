from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.usuarios.decorators import BibliotecarioRequiredMixin
from .forms import AutorForm, CategoriaForm, LibroForm
from .models import Autor, Categoria, Libro


class CatalogoView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = "libros/catalogo.html"
    context_object_name = "libros"
    paginate_by = 9

    def get_queryset(self):
        qs = Libro.objects.filter(activo=True).select_related("autor", "categoria")
        return filtrar_libros(qs, self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["autores"] = Autor.objects.filter(activo=True)
        context["categorias"] = Categoria.objects.filter(activo=True)
        context["estados"] = Libro.Estados.choices
        return context


class LibroListView(BibliotecarioRequiredMixin, ListView):
    model = Libro
    template_name = "libros/libro_list.html"
    context_object_name = "libros"
    paginate_by = 10

    def get_queryset(self):
        qs = Libro.objects.select_related("autor", "categoria")
        return filtrar_libros(qs, self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["autores"] = Autor.objects.all()
        context["categorias"] = Categoria.objects.all()
        context["estados"] = Libro.Estados.choices
        return context


def filtrar_libros(qs, params):
    q = params.get("q", "").strip()
    autor = params.get("autor", "").strip()
    categoria = params.get("categoria", "").strip()
    estado = params.get("estado", "").strip()
    if q:
        qs = qs.filter(
            Q(titulo__icontains=q)
            | Q(isbn__icontains=q)
            | Q(autor__nombre__icontains=q)
            | Q(categoria__nombre__icontains=q)
        )
    if autor:
        qs = qs.filter(autor_id=autor)
    if categoria:
        qs = qs.filter(categoria_id=categoria)
    if estado:
        qs = qs.filter(estado=estado)
    return qs


class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = "libros/libro_detail.html"
    context_object_name = "libro"


class LibroCreateView(BibliotecarioRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:libro_list")

    def form_valid(self, form):
        messages.success(self.request, "Libro creado correctamente.")
        return super().form_valid(form)


class LibroUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:libro_list")

    def form_valid(self, form):
        messages.success(self.request, "Libro actualizado correctamente.")
        return super().form_valid(form)


class LibroDeleteView(BibliotecarioRequiredMixin, DeleteView):
    model = Libro
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("libros:libro_list")

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save(update_fields=["activo", "actualizado"])
        messages.success(self.request, "Libro eliminado correctamente.")
        return redirect(self.success_url)


class AutorListView(BibliotecarioRequiredMixin, ListView):
    model = Autor
    template_name = "libros/autor_list.html"
    context_object_name = "autores"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Autor.objects.all()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(nacionalidad__icontains=q))
        return qs


class AutorCreateView(BibliotecarioRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:autor_list")


class AutorUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:autor_list")


class AutorDeleteView(BibliotecarioRequiredMixin, DeleteView):
    model = Autor
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("libros:autor_list")

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save(update_fields=["activo", "actualizado"])
        messages.success(self.request, "Autor eliminado correctamente.")
        return redirect(self.success_url)


class CategoriaListView(BibliotecarioRequiredMixin, ListView):
    model = Categoria
    template_name = "libros/categoria_list.html"
    context_object_name = "categorias"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Categoria.objects.all()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        return qs


class CategoriaCreateView(BibliotecarioRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:categoria_list")


class CategoriaUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "libros/form.html"
    success_url = reverse_lazy("libros:categoria_list")


class CategoriaDeleteView(BibliotecarioRequiredMixin, DeleteView):
    model = Categoria
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("libros:categoria_list")

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save(update_fields=["activo", "actualizado"])
        messages.success(self.request, "Categoria eliminada correctamente.")
        return redirect(self.success_url)
