from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'primer_nombre', 'primer_apellido', 'rol', 'activo', 'sancionado')
    list_filter = ('rol', 'activo', 'sancionado')
    search_fields = ('user__username', 'primer_nombre', 'primer_apellido')
