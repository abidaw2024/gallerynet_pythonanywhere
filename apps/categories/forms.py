from django import forms
from .models import Categoria

# Formulario para crear/editar categorías
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        #Solo necesito estos campos en el formulario
        fields = ['nombre', 'descripcion']
        # Personalización de como se ven los campos
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control bg-white text-dark',  
                'placeholder': 'Nombre de la categoría' 
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control bg-white text-dark', 
                'placeholder': 'Descripción de la categoría',  
                'rows': 3  #Altura del área de texto
            })
        } 