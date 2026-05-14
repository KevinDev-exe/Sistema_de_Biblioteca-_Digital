from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prestamo
from .forms import PrestamoForm, DevolucionForm


@login_required
def lista_prestamos(request):
    if request.user.perfil.rol == 'ADMIN':
        prestamos = Prestamo.objects.select_related('usuario', 'libro').all()
    else:
        prestamos = Prestamo.objects.select_related('usuario', 'libro').filter(usuario=request.user)
    return render(request, 'prestamos/lista_prestamos.html', {'prestamos': prestamos})


@login_required
def crear_prestamo(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')
    form = PrestamoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Préstamo registrado correctamente.')
        return redirect('lista_prestamos')
    return render(request, 'prestamos/form_prestamo.html', {'form': form, 'titulo': 'Nuevo Préstamo'})


@login_required
def devolver_prestamo(request, prestamo_id):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('lista_prestamos')
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.estado in ['DEVUELTO', 'CANCELADO']:
        messages.error(request, 'Este préstamo ya fue cerrado.')
        return redirect('lista_prestamos')
    form = DevolucionForm(request.POST or None, instance=prestamo)
    if form.is_valid():
        prestamo.marcar_devuelto()
        messages.success(request, f'Devolución registrada. Multa: ${prestamo.multa:,.0f} COP' if prestamo.multa > 0 else 'Devolución registrada sin multa.')
        return redirect('lista_prestamos')
    return render(request, 'prestamos/form_prestamo.html', {'form': form, 'prestamo': prestamo, 'titulo': 'Registrar Devolución'})


@login_required
def detalle_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.user.perfil.rol != 'ADMIN' and prestamo.usuario != request.user:
        return redirect('lista_prestamos')
    return render(request, 'prestamos/detalle_prestamo.html', {'prestamo': prestamo})