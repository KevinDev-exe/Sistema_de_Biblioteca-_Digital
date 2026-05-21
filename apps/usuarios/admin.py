from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "nombre", "rol", "sancionado", "is_active", "fecha_registro")
    list_filter = ("rol", "sancionado", "is_active", "is_staff")
    search_fields = ("username", "email", "nombre", "first_name", "last_name")
    ordering = ("-fecha_registro",)
    fieldsets = UserAdmin.fieldsets + (
        ("Biblioteca", {"fields": ("nombre", "rol", "sancionado", "fecha_registro")}),
    )
    readonly_fields = ("fecha_registro",)

