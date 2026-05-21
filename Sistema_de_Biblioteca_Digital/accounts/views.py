from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import (RegistroForm,PerfilForm,UsuarioUpdateForm,)
from django.contrib.auth.forms import PasswordResetForm
from prestamos.models import Prestamo
from django.db.models import Count
from django.db.models.functions import TruncMonth
from libros.models import Libro, Autor
import json

@login_required
def dashboard(request):

    # DASHBOARD BIBLIOTECARIO
    if request.user.perfil.rol == 'ADMIN':
        return redirect('dashboard:home')

        total_libros = Libro.objects.count()

        solicitudes_pendientes = Prestamo.objects.filter(
            estado='PENDIENTE'
        ).count()

        prestamos_activos = Prestamo.objects.filter(
            estado='ACTIVO'
        ).count()

        retrasados = Prestamo.objects.filter(
            estado='RETRASADO'
        ).count()

        top_libros = Libro.objects.annotate(
            total=Count('prestamos')
        ).order_by('-total')[:5]
        libros_labels = [x.titulo for x in top_libros]
        libros_data = [x.total for x in top_libros]

        top_autores = Autor.objects.annotate(
            total=Count('libro__prestamos')
        ).order_by('-total')[:5]
        autores_labels = [x.nombre for x in top_autores]
        autores_data = [x.total for x in top_autores]

        prestamos_mes = Prestamo.objects.annotate(
            mes=TruncMonth('fecha_prestamo')
        ).values('mes').annotate(total=Count('id')).order_by('mes')
        meses_labels = [p['mes'].strftime('%m/%Y') for p in prestamos_mes if p['mes']]
        meses_data = [p['total'] for p in prestamos_mes if p['mes']]

        return render(
            request,
            'accounts/dashboard_admin.html',
            {
                'total_libros': total_libros,
                'solicitudes_pendientes': solicitudes_pendientes,
                'prestamos_activos': prestamos_activos,
                'retrasados': retrasados,
                'libros_labels': json.dumps(libros_labels),
                'libros_data': json.dumps(libros_data),
                'autores_labels': json.dumps(autores_labels),
                'autores_data': json.dumps(autores_data),
                'meses_labels': json.dumps(meses_labels),
                'meses_data': json.dumps(meses_data),
            }
        )


    # DASHBOARD LECTOR
    prestamos_usuario = Prestamo.objects.filter(
        usuario=request.user
    )

    activos = prestamos_usuario.filter(
        estado='ACTIVO'
    ).count()

    retrasados = prestamos_usuario.filter(
        estado='RETRASADO'
    ).count()

    devueltos = prestamos_usuario.filter(
        estado='DEVUELTO'
    ).count()

    total_libros = Libro.objects.count()

    return render(
        request,
        'accounts/dashboard.html',
        {
            'activos': activos,
            'retrasados': retrasados,
            'devueltos': devueltos,
            'total_libros': total_libros
        }
    )

def login_view(request):

    if request.user.is_authenticated:

        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Bienvenido al sistema.'
            )

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'accounts/login.html'
    )

def password_reset_view(request):

    if request.method == 'POST':

        form = PasswordResetForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            if not User.objects.filter(email=email).exists():

                messages.error(
                    request,
                    'No existe una cuenta registrada con ese correo.'
                )

            else:

                form.save(
                    request=request,
                    use_https=False,
                    email_template_name='accounts/password_reset_email.html'
                )

                request.session['reset_email'] = email

                return redirect('password_reset_done')

    else:

        form = PasswordResetForm()

    return render(
        request,
        'accounts/password_reset.html',
        {
            'form': form
        }
    )

def registro(request):

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Cuenta creada correctamente.'
            )

            return redirect('perfil')

    else:

        form = RegistroForm()

    return render(
        request,
        'accounts/registro.html',
        {
            'form': form
        }
    )


@login_required
def perfil(request):

    perfil = request.user.perfil

    if request.method == 'POST':

        form = PerfilForm(
            request.POST,
            instance=perfil
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Perfil actualizado correctamente.'
            )

            return redirect('perfil')

    else:

        form = PerfilForm(instance=perfil)

    return render(
        request,
        'accounts/perfil.html',
        {
            'form': form
        }
    )


@login_required
def usuarios(request):

    if request.user.perfil.rol != 'ADMIN':

        return redirect('perfil')

    usuarios = User.objects.all()

    return render(
        request,
        'accounts/usuarios.html',
        {
            'usuarios': usuarios
        }
    )


@login_required
def editar_usuario(request, user_id):

    if request.user.perfil.rol != 'ADMIN':

        return redirect('perfil')

    usuario = get_object_or_404(
        User,
        id=user_id
    )

    perfil = usuario.perfil

    if request.method == 'POST':

        form = UsuarioUpdateForm(
            request.POST,
            instance=perfil
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Usuario actualizado correctamente.'
            )

            return redirect('usuarios')

    else:

        form = UsuarioUpdateForm(instance=perfil)

    return render(
        request,
        'accounts/editar_usuario.html',
        {
            'form': form,
            'usuario': usuario,
        }
    )