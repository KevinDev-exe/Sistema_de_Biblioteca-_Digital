from django import forms

from apps.libros.models import Libro
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["usuario", "libro", "estado", "notas"]
        widgets = {"notas": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        self.usuario_actual = kwargs.pop("usuario_actual", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)
        self.fields["libro"].queryset = Libro.objects.filter(activo=True).select_related("autor", "categoria")
        if self.usuario_actual and not getattr(self.usuario_actual, "es_bibliotecario", False):
            self.fields.pop("usuario")
            self.fields.pop("estado")

    def clean(self):
        cleaned = super().clean()
        if self.usuario_actual and not getattr(self.usuario_actual, "es_bibliotecario", False):
            cleaned["usuario"] = self.usuario_actual
            cleaned["estado"] = Reserva.Estados.ACTIVA
        libro = cleaned.get("libro")
        usuario = cleaned.get("usuario")
        estado = cleaned.get("estado")
        if libro and usuario and estado == Reserva.Estados.ACTIVA:
            qs = Reserva.objects.filter(usuario=usuario, libro=libro, estado=Reserva.Estados.ACTIVA)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe una reserva activa para este usuario y libro.")
            prestamos = libro.prestamos.filter(estado__in=["activo", "retrasado"]).count()
            reservas = libro.reservas.filter(estado=Reserva.Estados.ACTIVA)
            if self.instance.pk:
                reservas = reservas.exclude(pk=self.instance.pk)
            if prestamos + reservas.count() >= libro.cantidad:
                raise forms.ValidationError("No hay stock disponible para reservar este libro.")
        return cleaned

    def save(self, commit=True):
        reserva = super().save(commit=False)
        if self.usuario_actual and not getattr(self.usuario_actual, "es_bibliotecario", False):
            reserva.usuario = self.usuario_actual
            reserva.estado = Reserva.Estados.ACTIVA
        if commit:
            reserva.save()
        return reserva

