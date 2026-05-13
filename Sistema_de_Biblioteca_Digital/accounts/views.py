from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib import messages

from .forms import (
    RegistroForm,
    PerfilForm,
    UsuarioUpdateForm,
)

def login_view(request):

    if request.user.is_authenticated:

        return redirect('perfil')

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

            return redirect('perfil')

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'accounts/login.html'
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