from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .decorators import BibliotecarioRequiredMixin
from .forms import RegistroUsuarioForm, UsuarioForm
from .models import Usuario


class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("dashboard:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Cuenta creada correctamente. Bienvenido a Biblioteca Digital.")
        return response


class UsuarioListView(BibliotecarioRequiredMixin, ListView):
    model = Usuario
    template_name = "usuarios/usuario_list.html"
    context_object_name = "usuarios"
    paginate_by = 10

    def get_queryset(self):
        qs = Usuario.objects.all()
        q = self.request.GET.get("q", "").strip()
        rol = self.request.GET.get("rol", "").strip()
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(nombre__icontains=q))
        if rol:
            qs = qs.filter(rol=rol)
        return qs


class UsuarioUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "usuarios/usuario_form.html"
    success_url = reverse_lazy("usuarios:list")

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)


class PerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ["nombre", "first_name", "last_name", "email"]
    template_name = "usuarios/perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        return form

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)

