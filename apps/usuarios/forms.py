from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "nombre", "first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electronico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.rol = Usuario.Roles.LECTOR
        if commit:
            user.save()
        return user


class UsuarioForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ["username", "nombre", "first_name", "last_name", "email", "rol", "sancionado", "is_active"]

