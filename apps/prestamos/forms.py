from datetime import timedelta

from django import forms
from django.utils import timezone

from apps.libros.models import Libro
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ["usuario", "libro", "fecha_prestamo", "fecha_devolucion", "fecha_entrega", "estado", "multa", "observaciones"]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date"}),
            "fecha_devolucion": forms.DateInput(attrs={"type": "date"}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)
        self.fields["fecha_prestamo"].initial = self.fields["fecha_prestamo"].initial or timezone.localdate()
        self.fields["fecha_devolucion"].initial = self.fields["fecha_devolucion"].initial or timezone.localdate() + timedelta(days=7)
        self.fields["libro"].queryset = Libro.objects.filter(activo=True).select_related("autor", "categoria")

    def clean(self):
        cleaned = super().clean()
        libro = cleaned.get("libro")
        estado = cleaned.get("estado")
        if libro and estado in [Prestamo.Estados.ACTIVO, Prestamo.Estados.RETRASADO]:
            prestamos = libro.prestamos.filter(estado__in=[Prestamo.Estados.ACTIVO, Prestamo.Estados.RETRASADO])
            if self.instance.pk:
                prestamos = prestamos.exclude(pk=self.instance.pk)
            reservas = libro.reservas.filter(estado="activa").count()
            if prestamos.count() + reservas >= libro.cantidad:
                raise forms.ValidationError("No hay stock disponible para prestar este libro.")
        return cleaned

