from django import forms
from .models import Comision

class ComisionForm(forms.ModelForm):
    """
    Formulario para crear y editar comisiones.
    Incluye todos los campos necesarios para una comisión.
    """
    class Meta:
        model = Comision
        fields = [
            'titulo', 'descripcion', 'estilo', 'tecnica', 'tema',
            'imagen_principal', 'imagen_adicional_1', 'imagen_adicional_2', 'imagen_adicional_3',
            'precio_basico', 'descripcion_basico',
            'precio_estandar', 'descripcion_estandar',
            'precio_premium', 'descripcion_premium'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 300}),
            'imagen_principal': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
            'imagen_adicional_1': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen_adicional_2': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen_adicional_3': forms.FileInput(attrs={'class': 'form-control'}),
            'precio_basico': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_basico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True, 'maxlength': 500}),
            'precio_estandar': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_estandar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True, 'maxlength': 500}),
            'precio_premium': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_premium': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True, 'maxlength': 500}),
        }

    def clean(self):
        cleaned_data = super().clean()
        imagen_principal = cleaned_data.get('imagen_principal')
        
        if not imagen_principal:
            raise forms.ValidationError('La imagen principal es obligatoria.')
        
        return cleaned_data

    def clean_precio_basico(self):
        precio = self.cleaned_data.get('precio_basico')
        if precio is not None and (precio < 1 or precio > 1000):
            raise forms.ValidationError('El precio básico debe estar entre 1 € y 10 00 €.')
        return precio

    def clean_precio_estandar(self):
        precio = self.cleaned_data.get('precio_estandar')
        if precio is not None and (precio < 1 or precio > 1000):
            raise forms.ValidationError('El precio estándar debe estar entre 1 € y 10 00 €.')
        return precio

    def clean_precio_premium(self):
        precio = self.cleaned_data.get('precio_premium')
        if precio is not None and (precio < 1 or precio > 1000):
            raise forms.ValidationError('El precio premium debe estar entre 1 € y 10 00 €.')
        return precio

