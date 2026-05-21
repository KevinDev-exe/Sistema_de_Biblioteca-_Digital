import csv
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db import models

from apps.libros.models import Libro, Autor, Categoria
from apps.prestamos.models import Prestamo
from apps.reservas.models import Reserva
from apps.usuarios.models import Usuario

REPORTES = {
    "libros": {
        "titulo": "Reporte de libros",
        "headers": ["Título", "ISBN", "Autor", "Categoría", "Cantidad", "Disponibles", "Estado"],
    },
    "usuarios": {
        "titulo": "Reporte de usuarios",
        "headers": ["Usuario", "Nombre", "Email", "Rol", "Sancionado", "Activo"],
    },
    "prestamos": {
        "titulo": "Reporte de préstamos",
        "headers": ["Usuario", "Libro", "Fecha préstamo", "Fecha devolución", "Entrega", "Estado", "Multa"],
    },
    "reservas": {
        "titulo": "Reporte de reservas",
        "headers": ["Usuario", "Libro", "Fecha reserva", "Estado"],
    },
    "multas": {
        "titulo": "Reporte de multas",
        "headers": ["Usuario", "Libro", "Estado", "Días retraso", "Multa"],
    },
}


def obtener_query(tipo, params=None):
    if not params:
        params = {}
    
    if tipo == "libros":
        queryset = Libro.objects.select_related("autor", "categoria")
        categoria_id = params.get("categoria")
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        autor_id = params.get("autor")
        if autor_id:
            queryset = queryset.filter(autor_id=autor_id)
        estado = params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        search = params.get("search")
        if search:
            queryset = queryset.filter(models.Q(titulo__icontains=search) | models.Q(isbn__icontains=search))
        return queryset.order_by("titulo")

    if tipo == "usuarios":
        queryset = Usuario.objects.all()
        rol = params.get("rol")
        if rol:
            queryset = queryset.filter(rol=rol)
        sancionado = params.get("sancionado")
        if sancionado:
            val = sancionado == "1"
            queryset = queryset.filter(sancionado=val)
        activo = params.get("activo")
        if activo:
            val = activo == "1"
            queryset = queryset.filter(is_active=val)
        search = params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) | 
                models.Q(nombre__icontains=search) | 
                models.Q(email__icontains=search)
            )
        return queryset.order_by("-fecha_registro")

    if tipo == "prestamos":
        queryset = Prestamo.objects.select_related("usuario", "libro")
        estado = params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        desde = params.get("desde")
        if desde:
            queryset = queryset.filter(fecha_prestamo__gte=desde)
        hasta = params.get("hasta")
        if hasta:
            queryset = queryset.filter(fecha_prestamo__lte=hasta)
        search = params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(usuario__username__icontains=search) | 
                models.Q(usuario__nombre__icontains=search) | 
                models.Q(libro__titulo__icontains=search)
            )
        return queryset.order_by("-fecha_prestamo")

    if tipo == "reservas":
        queryset = Reserva.objects.select_related("usuario", "libro")
        estado = params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        desde = params.get("desde")
        if desde:
            queryset = queryset.filter(fecha_reserva__date__gte=desde)
        hasta = params.get("hasta")
        if hasta:
            queryset = queryset.filter(fecha_reserva__date__lte=hasta)
        search = params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(usuario__username__icontains=search) | 
                models.Q(usuario__nombre__icontains=search) | 
                models.Q(libro__titulo__icontains=search)
            )
        return queryset.order_by("-fecha_reserva")

    if tipo == "multas":
        queryset = Prestamo.objects.select_related("usuario", "libro").exclude(multa=0)
        estado = params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        desde = params.get("desde")
        if desde:
            queryset = queryset.filter(fecha_prestamo__gte=desde)
        hasta = params.get("hasta")
        if hasta:
            queryset = queryset.filter(fecha_prestamo__lte=hasta)
        search = params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(usuario__username__icontains=search) | 
                models.Q(usuario__nombre__icontains=search) | 
                models.Q(libro__titulo__icontains=search)
            )
        return queryset.order_by("-fecha_prestamo")
    
    return []


def obtener_filas_desde_query(tipo, queryset):
    if tipo == "libros":
        return [
            [l.titulo, l.isbn, l.autor.nombre, l.categoria.nombre, l.cantidad, l.cantidad_disponible, l.get_estado_display()]
            for l in queryset
        ]
    if tipo == "usuarios":
        return [
            [u.username, u.nombre, u.email, u.get_rol_display(), "Sí" if u.sancionado else "No", "Sí" if u.is_active else "No"]
            for u in queryset
        ]
    if tipo == "prestamos":
        return [
            [
                p.usuario.username,
                p.libro.titulo,
                p.fecha_prestamo.strftime("%Y-%m-%d") if p.fecha_prestamo else "",
                p.fecha_devolucion.strftime("%Y-%m-%d") if p.fecha_devolucion else "",
                p.fecha_entrega.strftime("%Y-%m-%d") if p.fecha_entrega else "",
                p.get_estado_display(),
                f"${p.multa}",
            ]
            for p in queryset
        ]
    if tipo == "reservas":
        return [
            [r.usuario.username, r.libro.titulo, timezone.localtime(r.fecha_reserva).strftime("%Y-%m-%d %H:%M"), r.get_estado_display()]
            for r in queryset
        ]
    if tipo == "multas":
        return [
            [p.usuario.username, p.libro.titulo, p.get_estado_display(), p.dias_retraso, f"${p.multa}"]
            for p in queryset
        ]
    return []


def obtener_filas(tipo, params=None):
    qs = obtener_query(tipo, params)
    return obtener_filas_desde_query(tipo, qs)


@login_required
def index(request):
    if not request.user.es_bibliotecario:
        return redirect("libros:catalogo")
    
    tipo_activo = request.GET.get("tipo", "libros")
    if tipo_activo not in REPORTES:
        tipo_activo = "libros"
        
    params = request.GET
    queryset = obtener_query(tipo_activo, params)
    total_resultados = queryset.count() if hasattr(queryset, "count") else len(queryset)
    
    preview_data = queryset[:20] if hasattr(queryset, "count") else queryset
    preview_rows = obtener_filas_desde_query(tipo_activo, preview_data)
    
    categorias = Categoria.objects.all()
    autores = Autor.objects.all()
    
    context = {
        "reportes": REPORTES,
        "tipo_activo": tipo_activo,
        "headers": REPORTES[tipo_activo]["headers"],
        "preview_rows": preview_rows,
        "total_resultados": total_resultados,
        "categorias": categorias,
        "autores": autores,
        "filtros": {
            "categoria": params.get("categoria", ""),
            "autor": params.get("autor", ""),
            "estado": params.get("estado", ""),
            "rol": params.get("rol", ""),
            "sancionado": params.get("sancionado", ""),
            "activo": params.get("activo", ""),
            "desde": params.get("desde", ""),
            "hasta": params.get("hasta", ""),
            "search": params.get("search", ""),
        }
    }
    return render(request, "reportes/index.html", context)


@login_required
def exportar(request, tipo, formato):
    if not request.user.es_bibliotecario:
        return redirect("libros:catalogo")
    if tipo not in REPORTES:
        return redirect("reportes:index")
    headers = REPORTES[tipo]["headers"]
    rows = obtener_filas(tipo, request.GET)
    filename = f"{tipo}_{timezone.localdate().isoformat()}"
    if formato == "csv":
        return exportar_csv(filename, headers, rows)
    if formato == "excel":
        return exportar_excel(filename, headers, rows)
    if formato == "pdf":
        return exportar_pdf(filename, REPORTES[tipo]["titulo"], headers, rows, tipo)
    return redirect("reportes:index")


def exportar_csv(filename, headers, rows):
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(rows)
    return response


def exportar_excel(filename, headers, rows):
    import pandas as pd
    output = BytesIO()
    df = pd.DataFrame(rows, columns=headers)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Reporte", index=False)
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    return response


def obtener_anchos_columnas(tipo):
    # Widths sum should fit letter landscape (~684 printable points or 720 points)
    if tipo == "libros":
        return [180, 80, 110, 110, 50, 50, 70]
    if tipo == "usuarios":
        return [100, 140, 160, 110, 70, 70]
    if tipo == "prestamos":
        return [80, 170, 75, 75, 75, 75, 60]
    if tipo == "reservas":
        return [120, 240, 130, 130]
    if tipo == "multas":
        return [100, 220, 100, 80, 80]
    return None


def exportar_pdf(filename, titulo, headers, rows, tipo):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
    )
    header_style = ParagraphStyle(
        'HeaderCellText',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.white,
        fontName='Helvetica-Bold',
    )
    
    data = []
    # Add headers
    data.append([Paragraph(h, header_style) for h in headers])
    # Add rows
    for row in rows:
        data.append([Paragraph(str(value), cell_style) for value in row])
        
    col_widths = obtener_anchos_columnas(tipo)
    if col_widths:
        table = Table(data, colWidths=col_widths, repeatRows=1)
    else:
        table = Table(data, repeatRows=1)
        
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d7dde8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1f3a5f"),
        spaceAfter=12
    )
    
    elements = [
        Paragraph(titulo, title_style),
        Spacer(1, 10),
        table
    ]
    doc.build(elements)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
    return response
