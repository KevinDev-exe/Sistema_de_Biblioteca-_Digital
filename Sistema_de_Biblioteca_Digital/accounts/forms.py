from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Perfil


class RegistroForm(UserCreationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

    email = forms.EmailField()

    primer_nombre = forms.CharField(max_length=100)
    segundo_nombre = forms.CharField(max_length=100, required=False)

    primer_apellido = forms.CharField(max_length=100)
    segundo_apellido = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'password1',
            'password2',
        )

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                'Este correo ya está registrado.'
            )

        return email

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:

            user.save()

            perfil = user.perfil

            perfil.primer_nombre = self.cleaned_data['primer_nombre']

            perfil.segundo_nombre = self.cleaned_data['segundo_nombre']

            perfil.primer_apellido = self.cleaned_data['primer_apellido']

            perfil.segundo_apellido = self.cleaned_data['segundo_apellido']

            perfil.rol = 'LECTOR'

            perfil.save()

        return user


class PerfilForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:

        model = Perfil

        fields = [
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
        ]


class UsuarioUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['rol'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:

        model = Perfil

        fields = [
            'rol',
            'sancionado',
            'activo',
        ]