from django import forms

from .models import Autor, Categoria, Libro


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)


class AutorForm(BootstrapModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "nacionalidad", "biografia", "activo"]
        widgets = {"biografia": forms.Textarea(attrs={"rows": 4})}


class CategoriaForm(BootstrapModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activo"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4})}


class LibroForm(BootstrapModelForm):
    class Meta:
        model = Libro
        fields = [
            "titulo",
            "isbn",
            "descripcion",
            "portada",
            "cantidad",
            "estado",
            "fecha_publicacion",
            "autor",
            "categoria",
            "activo",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
            "fecha_publicacion": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].replace("-", "").replace(" ", "")
        qs = Libro.objects.filter(isbn=isbn)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un libro registrado con este ISBN.")
        return isbn

