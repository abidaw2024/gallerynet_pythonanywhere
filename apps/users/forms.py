"""
Formularios para el manejo de credenciales de usuario
Este archivo contiene los formularios relacionados con:
- Registro de usuarios (creación de credenciales)
- Edición de perfil
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para el registro de nuevos usuarios.
    Maneja las credenciales iniciales:
    - first_name: nombre
    - username: nombre de usuario único
    - email: correo electrónico único
    - password1: contraseña
    - password2: confirmación de contraseña
    """
    class Meta:
        model = Usuario
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class EditarPerfilForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario.
    No incluye campos de credenciales sensibles.
    """
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'email', 'profile_picture', 'biografia', 'categorias']
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 300}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }