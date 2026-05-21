from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from libros.models import Libro
from .forms import ReservaForm
from .models import Reserva


class BibliotecarioRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, "es_bibliotecario", False)


class ReservaListView(BibliotecarioRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        qs = Reserva.objects.select_related("usuario", "libro", "libro__autor")
        q = self.request.GET.get("q", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        if q:
            qs = qs.filter(Q(usuario__username__icontains=q) | Q(usuario__email__icontains=q) | Q(libro__titulo__icontains=q))
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Reserva.Estados.choices
        return context


class MisReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related("libro", "libro__autor")


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/form.html"

    def get_success_url(self):
        return reverse_lazy("reservas:list" if getattr(self.request.user, "es_bibliotecario", False) else "reservas:mis_reservas")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario_actual"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        libro_id = self.request.GET.get("libro")
        if libro_id:
            initial["libro"] = libro_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Reserva creada correctamente.")
        return super().form_valid(form)


class ReservaUpdateView(BibliotecarioRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/form.html"
    success_url = reverse_lazy("reservas:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario_actual"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Reserva actualizada correctamente.")
        return super().form_valid(form)


class ReservaDeleteView(BibliotecarioRequiredMixin, DeleteView):
    model = Reserva
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("reservas:list")

    def form_valid(self, form):
        messages.success(self.request, "Reserva eliminada correctamente.")
        return super().form_valid(form)


def reservar_libro(request, libro_id):
    if not request.user.is_authenticated:
        return redirect("login")
    libro = get_object_or_404(Libro, pk=libro_id)
    reserva = Reserva(usuario=request.user, libro=libro)
    try:
        reserva.full_clean()
        reserva.save()
        messages.success(request, "Libro reservado correctamente.")
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect("lista_libros")


def cancelar_reserva(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.usuario != request.user and not getattr(request.user, "es_bibliotecario", False):
        messages.error(request, "No puedes cancelar esta reserva.")
        return redirect("reservas:mis_reservas")
    reserva.estado = Reserva.Estados.CANCELADA
    reserva.save(update_fields=["estado"])
    if hasattr(reserva.libro, 'sincronizar_estado'):
        reserva.libro.sincronizar_estado()
    messages.success(request, "Reserva cancelada correctamente.")
    return redirect("reservas:list" if getattr(request.user, "es_bibliotecario", False) else "reservas:mis_reservas")
