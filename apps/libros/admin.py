from django.contrib import admin

from .models import Autor, Categoria, Libro


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nacionalidad", "activo", "creado")
    list_filter = ("activo", "nacionalidad")
    search_fields = ("nombre", "nacionalidad")
    ordering = ("nombre",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "isbn", "autor", "categoria", "cantidad", "estado", "activo")
    list_filter = ("estado", "categoria", "autor", "activo")
    search_fields = ("titulo", "isbn", "autor__nombre", "categoria__nombre")
    ordering = ("titulo",)
    autocomplete_fields = ("autor", "categoria")
    readonly_fields = ("creado", "actualizado")

