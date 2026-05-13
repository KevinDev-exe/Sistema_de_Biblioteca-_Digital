from django import forms

from .models import Libro


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