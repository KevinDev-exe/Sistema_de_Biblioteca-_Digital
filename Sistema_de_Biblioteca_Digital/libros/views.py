from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LibroForm, AutorForm, CategoriaForm
from .models import Libro, Autor, Categoria


def es_admin(usuario):

    return usuario.perfil.rol == 'ADMIN'


@login_required
def crear_libro(request):

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para crear libros.'
        )

        return redirect('lista_libros')

    form = LibroForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Libro creado correctamente.'
        )

        return redirect('lista_libros')

    return render(
        request,
        'libros/crear_libro.html',
        {
            'form': form
        }
    )


@login_required
def lista_libros(request):

    buscar = request.GET.get('buscar')

    libros = Libro.objects.all()

    if buscar:

        libros = libros.filter(
            titulo__icontains=buscar
        )

    return render(
        request,
        'libros/lista_libros.html',
        {
            'libros': libros
        }
    )


@login_required
def editar_libro(request, libro_id):

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para editar libros.'
        )

        return redirect('lista_libros')

    libro = get_object_or_404(
        Libro,
        id=libro_id
    )

    form = LibroForm(
        request.POST or None,
        request.FILES or None,
        instance=libro
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Libro actualizado correctamente.'
        )

        return redirect('lista_libros')

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
def crear_autor(request):

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para crear autores.'
        )

        return redirect('lista_autores')

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

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para editar autores.'
        )

        return redirect('lista_autores')

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

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para eliminar autores.'
        )

        return redirect('lista_autores')

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
def crear_categoria(request):

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para crear categorías.'
        )

        return redirect('lista_categorias')

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

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para editar categorías.'
        )

        return redirect('lista_categorias')

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

    if not es_admin(request.user):

        messages.error(
            request,
            'No tienes permisos para eliminar categorías.'
        )

        return redirect('lista_categorias')

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