from django import forms
from .models import Prestamo
from libros.models import Libro
from django.utils import timezone
from datetime import timedelta


class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_devolucion', 'observaciones']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].queryset = Libro.objects.filter(disponibles__gt=0)
        self.fields['fecha_devolucion'].initial = (timezone.localdate() + timedelta(days=7)).strftime('%Y-%m-%d')

    def clean_fecha_devolucion(self):
        fecha = self.cleaned_data.get('fecha_devolucion')
        if fecha and fecha <= timezone.localdate():
            raise forms.ValidationError('La fecha de devolución debe ser posterior a hoy.')
        return fecha


class PrestamoEditForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['estado', 'fecha_devolucion', 'multa', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'multa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DevolucionForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }