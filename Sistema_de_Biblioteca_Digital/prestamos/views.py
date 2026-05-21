from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
import csv

from .models import Prestamo
from .forms import PrestamoForm, DevolucionForm, PrestamoEditForm
from libros.models import Libro
from notificaciones.services import ServicioNotificaciones


@login_required
def lista_prestamos(request):

    if request.user.perfil.rol == 'ADMIN':

        prestamos = Prestamo.objects.select_related(
            'usuario',
            'libro'
        ).all()

    else:

        prestamos = Prestamo.objects.select_related(
            'usuario',
            'libro'
        ).filter(
            usuario=request.user
        )

    return render(
        request,
        'prestamos/lista_prestamos.html',
        {
            'prestamos': prestamos
        }
    )


@login_required
def reservar_libro(request, libro_id):

    libro = get_object_or_404(
        Libro,
        id=libro_id
    )

    if request.user.perfil.sancionado:

        messages.error(
            request,
            'No puedes solicitar libros porque estás sancionado.'
        )

        return redirect(
            'lista_libros'
        )

    # Verificar si ya existe una solicitud
    solicitud_existente = Prestamo.objects.filter(
        usuario=request.user,
        libro=libro,
        estado__in=['PENDIENTE','ACTIVO','RETRASADO']
    ).exists()

    if solicitud_existente:

        messages.warning(
            request,
            'Ya tienes una solicitud o préstamo activo para este libro.'
        )

        return redirect(
            'lista_libros'
        )

    if libro.disponibles <= 0:

        messages.error(
            request,
            'No hay ejemplares disponibles.'
        )

        return redirect(
            'lista_libros'
        )

    Prestamo.objects.create(

        usuario=request.user,

        libro=libro,

        fecha_devolucion=timezone.localdate()+timedelta(days=7),

        estado='PENDIENTE'
    )

    messages.success(
        request,
        'Solicitud enviada al bibliotecario.'
    )

    return redirect(
        'lista_prestamos'
    )


@login_required
def cancelar_prestamo(request, prestamo_id):

    prestamo = get_object_or_404(
        Prestamo,
        id=prestamo_id
    )

    if request.user.perfil.rol == 'ADMIN' or prestamo.usuario == request.user:

        if prestamo.estado == 'PENDIENTE':

            prestamo.estado = 'CANCELADO'
            prestamo.save()

            if request.user.perfil.rol == 'ADMIN':
                ServicioNotificaciones.crear_notificacion(
                    prestamo=prestamo,
                    tipo='CANCELACION',
                    asunto='Tu solicitud de préstamo ha sido cancelada',
                    mensaje=(
                        f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
                        f'Tu solicitud de préstamo para el libro "{prestamo.libro.titulo}" '
                        f'ha sido cancelada por el bibliotecario.\n\nSaludos,\nBiblioteca Digital'
                    )
                )

            messages.success(
                request,
                'Solicitud cancelada.'
            )

    else:

        messages.error(
            request,
            'No tienes permiso para cancelar esta solicitud.'
        )

    return redirect(
        'lista_prestamos'
    )

@login_required
def aprobar_prestamo(request, prestamo_id):

    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')

    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == 'POST':
        fecha_devolucion = request.POST.get('fecha_devolucion')
        if not fecha_devolucion:
            messages.error(request, 'Debe indicar una fecha de devolución.')
            return redirect('lista_prestamos')

        if prestamo.estado == 'PENDIENTE':
            prestamo.fecha_devolucion = fecha_devolucion
            prestamo.estado = 'ACTIVO'
            prestamo.save()

            ServicioNotificaciones.notificar_aprobacion_prestamo(prestamo)

            messages.success(request, 'Solicitud aprobada y fecha asignada correctamente.')
        else:
            messages.error(request, 'Solo se pueden aprobar préstamos pendientes.')

    return redirect('lista_prestamos')


@login_required
def crear_prestamo(request):

    if request.user.perfil.rol != 'ADMIN':

        return redirect(
            'lista_prestamos'
        )

    form = PrestamoForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Préstamo registrado correctamente.'
        )

        return redirect(
            'lista_prestamos'
        )

    return render(
        request,
        'prestamos/form_prestamo.html',
        {
            'form': form,
            'titulo': 'Nuevo préstamo'
        }
    )


@login_required
def devolver_prestamo(request, prestamo_id):

    if request.user.perfil.rol != 'ADMIN':

        return redirect(
            'lista_prestamos'
        )

    prestamo = get_object_or_404(
        Prestamo,
        id=prestamo_id
    )

    if prestamo.estado in ['DEVUELTO', 'CANCELADO']:

        messages.error(
            request,
            'Este préstamo ya fue cerrado.'
        )

        return redirect(
            'lista_prestamos'
        )

    prestamo.marcar_devuelto()

    ServicioNotificaciones.notificar_devolucion(prestamo)

    messages.success(
        request,
        'Devolución registrada correctamente.'
    )

    return redirect(
        'lista_prestamos'
    )


@login_required
def detalle_prestamo(request, prestamo_id):

    prestamo = get_object_or_404(
        Prestamo,
        id=prestamo_id
    )

    return render(
        request,
        'prestamos/detalle_prestamo.html',
        {
            'prestamo': prestamo
        }
    )

@login_required
def editar_prestamo(request, prestamo_id):

    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')

    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == 'POST':
        form = PrestamoEditForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Préstamo actualizado correctamente.')
            return redirect('lista_prestamos')
    else:
        form = PrestamoEditForm(instance=prestamo)

    return render(
        request,
        'prestamos/form_prestamo.html',
        {
            'form': form,
            'titulo': 'Editar préstamo'
        }
    )

@login_required
def exportar_prestamos_csv(request):
    
    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')
        
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="prestamos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Libro', 'Usuario', 'Fecha Préstamo', 'Fecha Devolución', 'Fecha Entrega', 'Estado', 'Multa'])

    prestamos = Prestamo.objects.select_related('usuario', 'libro').all()
    
    for p in prestamos:
        writer.writerow([
            p.libro.titulo,
            p.usuario.username,
            p.fecha_prestamo,
            p.fecha_devolucion,
            p.fecha_entrega if p.fecha_entrega else 'No entregado',
            p.get_estado_display(),
            p.multa
        ])

    return response

@login_required
def exportar_prestamos_pdf(request):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io

    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Reporte de Préstamos")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Reporte de Préstamos")

    p.setFont("Helvetica", 10)
    y = 720
    prestamos = Prestamo.objects.select_related('usuario', 'libro').all()
    
    p.drawString(50, y, "Libro")
    p.drawString(250, y, "Usuario")
    p.drawString(350, y, "Fecha Dev.")
    p.drawString(450, y, "Estado")
    p.drawString(520, y, "Multa")
    y -= 20

    for prestamo in prestamos:
        p.drawString(50, y, str(prestamo.libro.titulo)[:40])
        p.drawString(250, y, str(prestamo.usuario.username))
        p.drawString(350, y, str(prestamo.fecha_devolucion))
        p.drawString(450, y, prestamo.get_estado_display())
        p.drawString(520, y, f"${prestamo.multa}")
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750

    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prestamos.pdf"'
    return response