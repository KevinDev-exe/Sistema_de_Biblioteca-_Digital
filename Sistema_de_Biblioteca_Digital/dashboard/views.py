from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import redirect, render

from libros.models import Autor, Libro
from prestamos.models import Prestamo
from reservas.models import Reserva


@login_required
def home(request):
    if not request.user.es_bibliotecario:
        return redirect("lista_libros")

    prestamos_recientes = Prestamo.objects.select_related("usuario", "libro").order_by("-creado")[:5]
    reservas_recientes = Reserva.objects.select_related("usuario", "libro").order_by("-fecha_reserva")[:5]
    actividad = sorted(
        chain(prestamos_recientes, reservas_recientes),
        key=lambda item: getattr(item, "creado", getattr(item, "fecha_reserva", None)),
        reverse=True,
    )[:8]

    context = {
        "total_libros": Libro.objects.count(),
        "total_usuarios": User.objects.filter(is_active=True).count(),
        "libros_prestados": Prestamo.objects.filter(estado__in=["ACTIVO", "RETRASADO"]).count(),
        "reservas_activas": Reserva.objects.filter(estado="activa").count(),
        "usuarios_sancionados": User.objects.filter(perfil__sancionado=True).count(),
        "actividad": actividad,
    }
    return render(request, "dashboard/home.html", context)


@login_required
def chart_libros_reservados(request):
    if not request.user.es_bibliotecario:
        return JsonResponse({"labels": [], "values": []})
    data = Libro.mas_reservados(8)
    return JsonResponse(
        {
            "labels": [libro.titulo for libro in data],
            "values": [libro.total_reservas for libro in data],
        }
    )


@login_required
def chart_prestamos_mes(request):
    if not request.user.es_bibliotecario:
        return JsonResponse({"labels": [], "values": []})
    rows = (
        Prestamo.objects.annotate(year=ExtractYear("fecha_prestamo"), month=ExtractMonth("fecha_prestamo"))
        .values("year", "month")
        .annotate(total=Count("id"))
        .order_by("year", "month")
    )
    return JsonResponse(
        {
            "labels": [f"{row['month']:02d}/{row['year']}" for row in rows],
            "values": [row["total"] for row in rows],
        }
    )


@login_required
def chart_categorias(request):
    if not request.user.es_bibliotecario:
        return JsonResponse({"labels": [], "values": []})
    rows = (
        Libro.objects.values("categoria__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    return JsonResponse(
        {
            "labels": [row["categoria__nombre"] for row in rows],
            "values": [row["total"] for row in rows],
        }
    )


@login_required
def chart_autores_leidos(request):
    if not request.user.es_bibliotecario:
        return JsonResponse({"labels": [], "values": []})
    rows = (
        Autor.objects.annotate(total_prestamos=Count("libro__prestamos"))
        .filter(total_prestamos__gt=0)
        .order_by("-total_prestamos")[:8]
    )
    return JsonResponse(
        {
            "labels": [row.nombre for row in rows],
            "values": [row.total_prestamos for row in rows],
        }
    )
