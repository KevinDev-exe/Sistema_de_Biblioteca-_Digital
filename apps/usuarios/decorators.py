from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


def bibliotecario_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not getattr(request.user, "es_bibliotecario", False):
            messages.error(request, "No tienes permisos para acceder a esta seccion.")
            return redirect("libros:catalogo")
        return view_func(request, *args, **kwargs)

    return wrapper


class BibliotecarioRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user, "es_bibliotecario", False)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta seccion.")
        return redirect("libros:catalogo")

