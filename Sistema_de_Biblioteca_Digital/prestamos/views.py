from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Prestamo
from .forms import PrestamoForm, DevolucionForm
from libros.models import Libro


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

            prestamo.delete()

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