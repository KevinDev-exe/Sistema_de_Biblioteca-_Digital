from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LibroForm
from .models import (Libro,Autor,Categoria )
from django.shortcuts import get_object_or_404

@login_required
def crear_libro(request):

    if request.user.perfil.rol != 'ADMIN':

        return redirect('perfil')

    if request.method == 'POST':

        form = LibroForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Libro creado correctamente.'
            )

            return redirect('crear_libro')

    else:

        form = LibroForm()

    return render(
        request,
        'libros/crear_libro.html',
        {
            'form': form
        }
    )

@login_required
def lista_libros(request):

    libros = Libro.objects.all()

    return render(
        request,
        'libros/lista_libros.html',
        {
            'libros': libros
        }
    )

@login_required
def editar_libro(request, libro_id):

    if request.user.perfil.rol != 'ADMIN':

        return redirect('perfil')

    libro = get_object_or_404(
        Libro,
        id=libro_id
    )

    if request.method == 'POST':

        form = LibroForm(
            request.POST,
            request.FILES,
            instance=libro
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Libro actualizado correctamente.'
            )

            return redirect('lista_libros')

    else:

        form = LibroForm(instance=libro)

    return render(
        request,
        'libros/editar_libro.html',
        {
            'form': form,
            'libro': libro
        }
    )

@login_required
def lista_autores(request):

    autores = Autor.objects.all()

    return render(
        request,
        'libros/autores.html',
        {
            'autores': autores
        }
    )


@login_required
def lista_categorias(request):

    categorias = Categoria.objects.all()

    return render(
        request,
        'libros/categorias.html',
        {
            'categorias': categorias
        }
    )