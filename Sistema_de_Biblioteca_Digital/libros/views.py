from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (LibroForm, AutorForm, CategoriaForm)
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
@login_required
def crear_autor(request):

    form = AutorForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Autor creado correctamente.'
        )

        return redirect('lista_autores')

    return render(
        request,
        'libros/crear_autor.html',
        {
            'form': form
        }
    )


@login_required
def editar_autor(request, autor_id):

    autor = get_object_or_404(
        Autor,
        id=autor_id
    )

    form = AutorForm(
        request.POST or None,
        instance=autor
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Autor actualizado correctamente.'
        )

        return redirect('lista_autores')

    return render(
        request,
        'libros/crear_autor.html',
        {
            'form': form
        }
    )


@login_required
def eliminar_autor(request, autor_id):

    autor = get_object_or_404(
        Autor,
        id=autor_id
    )

    autor.delete()

    messages.success(
        request,
        'Autor eliminado correctamente.'
    )

    return redirect('lista_autores')

# categorias
@login_required
def crear_categoria(request):

    form = CategoriaForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Categoría creada correctamente.'
        )

        return redirect('lista_categorias')

    return render(
        request,
        'libros/crear_categoria.html',
        {
            'form': form
        }
    )


@login_required
def editar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    form = CategoriaForm(
        request.POST or None,
        instance=categoria
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Categoría actualizada correctamente.'
        )

        return redirect('lista_categorias')

    return render(
        request,
        'libros/crear_categoria.html',
        {
            'form': form
        }
    )


@login_required
def eliminar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    categoria.delete()

    messages.success(
        request,
        'Categoría eliminada correctamente.'
    )

    return redirect('lista_categorias')