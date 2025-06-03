"""
Implementa un sistema de control de acceso basado en que:
- Verifica si el usuario esta autenticado
- Comprueba si tiene rol de administrador
- Redirige según los permisos del usuario
"""

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        #redireccion
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_admin():
            return redirect('home') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view 