from django import forms

from .models import (Libro,Autor, Categoria)


class LibroForm(forms.ModelForm):

    class Meta:

        model = Libro

        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

class AutorForm(forms.ModelForm):

    class Meta:

        model = Autor

        fields = ['nombre']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria

        fields = ['nombre']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }            