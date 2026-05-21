from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import redirect, render

from apps.libros.models import Autor, Libro
from apps.prestamos.models import Prestamo
from apps.reservas.models import Reserva
from apps.usuarios.models import Usuario


@login_required
def home(request):
    if not request.user.es_bibliotecario:
        return redirect("libros:catalogo")

    prestamos_recientes = Prestamo.objects.select_related("usuario", "libro").order_by("-creado")[:5]
    reservas_recientes = Reserva.objects.select_related("usuario", "libro").order_by("-fecha_reserva")[:5]
    actividad = sorted(
        chain(prestamos_recientes, reservas_recientes),
        key=lambda item: getattr(item, "creado", getattr(item, "fecha_reserva", None)),
        reverse=True,
    )[:8]

    context = {
        "total_libros": Libro.objects.filter(activo=True).count(),
        "total_usuarios": Usuario.objects.filter(is_active=True).count(),
        "libros_prestados": Prestamo.objects.filter(estado__in=[Prestamo.Estados.ACTIVO, Prestamo.Estados.RETRASADO]).count(),
        "reservas_activas": Reserva.objects.filter(estado=Reserva.Estados.ACTIVA).count(),
        "usuarios_sancionados": Usuario.objects.filter(sancionado=True).count(),
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
        Libro.objects.filter(activo=True)
        .values("categoria__nombre")
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
        Autor.objects.filter(activo=True)
        .annotate(total_prestamos=Count("libros__prestamos"))
        .filter(total_prestamos__gt=0)
        .order_by("-total_prestamos")[:8]
    )
    return JsonResponse(
        {
            "labels": [row.nombre for row in rows],
            "values": [row.total_prestamos for row in rows],
        }
    )


