from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.usuarios.decorators import BibliotecarioRequiredMixin, bibliotecario_required
from .forms import PrestamoForm
from .models import Prestamo


class PrestamoListView(BibliotecarioRequiredMixin, ListView):
    model = Prestamo
    template_name = "prestamos/prestamo_list.html"
    context_object_name = "prestamos"
    paginate_by = 10

    def get_queryset(self):
        qs = Prestamo.objects.select_related("usuario", "libro", "libro__autor")
        q = self.request.GET.get("q", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        if q:
            qs = qs.filter(Q(usuario__username__icontains=q) | Q(usuario__email__icontains=q) | Q(libro__titulo__icontains=q))
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Prestamo.Estados.choices
        return context


class MisPrestamosView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = "prestamos/mis_prestamos.html"
    context_object_name = "prestamos"
    paginate_by = 10

    def get_queryset(self):
        return Prestamo.objects.filter(usuario=self.request.user).select_related("libro", "libro__autor")


class PrestamoCreateView(BibliotecarioRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = "prestamos/form.html"
    success_url = reverse_lazy("prestamos:list")

    def form_valid(self, form):
        messages.success(self.request, "Prestamo registrado correctamente.")
        return super().form_valid(form)


class PrestamoUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = "prestamos/form.html"
    success_url = reverse_lazy("prestamos:list")

    def form_valid(self, form):
        messages.success(self.request, "Prestamo actualizado correctamente.")
        return super().form_valid(form)


class PrestamoDeleteView(BibliotecarioRequiredMixin, DeleteView):
    model = Prestamo
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("prestamos:list")

    def form_valid(self, form):
        messages.success(self.request, "Prestamo eliminado correctamente.")
        return super().form_valid(form)


@bibliotecario_required
def marcar_devuelto(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    prestamo.marcar_devuelto()
    messages.success(request, "Prestamo marcado como devuelto.")
    return redirect("prestamos:list")

