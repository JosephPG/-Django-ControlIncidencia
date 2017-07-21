from django import forms
from .models import DetalleIncidencia


class DetalleForm(forms.ModelForm):
    """ Arma el formulario para agregar detalle que sera rellenado por el
     usuario """
    class Meta:
        model = DetalleIncidencia
        fields = [
            'detalle',
        ]
        labels = {
            'detalle': 'Detalle de incidencia'
        }
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control',
            'style': 'height: 95%'})
        }
