# apps/gallery/views_backoffice.py (por claridad, puedes separarlo del resto)

"""
Vistas para el Panel de Administración de Gallery
Este archivo contiene las vistas específicas para la gestión administrativa de obras.

Características de seguridad:
- LoginRequiredMixin: Asegura que el usuario esté autenticado
- @admin_required: Verifica que el usuario tenga rol de administrador
- Control de acceso granular para operaciones CRUD
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.users.decorators import admin_required
from django.utils.decorators import method_decorator
from .models import Comision
from .forms import ComisionForm


# ====================== CREAR ======================
@method_decorator(admin_required, name='dispatch')
class ObraCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear nuevas obras en el panel de administración.
    
    Características:
    - Requiere autenticación y rol de administrador
    - Usa ComisionForm para la validación de datos
    - Muestra mensajes de éxito
    - Redirige a la página de edición después de crear
    """
    model = Comision
    form_class = ComisionForm
    template_name = "backoffice/base_create_update.html"

    def form_valid(self, form):
        messages.success(self.request, f"Obra '{form.instance.titulo}' creada correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('obra_update', kwargs={'pk': self.object.pk})


# ====================== ACTUALIZAR ======================
@method_decorator(admin_required, name='dispatch')
class ObraUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar obras existentes en el panel de administración.
    
    Características:
    - Requiere autenticación y rol de administrador
    - Usa ComisionForm para la validación de datos
    - Muestra mensajes de éxito
    - Redirige a la lista de obras después de actualizar
    """
    model = Comision
    form_class = ComisionForm
    template_name = "backoffice/base_create_update.html"
    success_url = reverse_lazy('obra_list')

    def form_valid(self, form):
        messages.success(self.request, f"Obra '{form.instance.titulo}' actualizada correctamente.")
        return super().form_valid(form)


# ====================== eliminar ======================
@method_decorator(admin_required, name='dispatch')
class ObraDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar obras en el panel de administración.
    
    Características:
    - Requiere autenticación y rol de administrador
    - Muestra mensajes de éxito
    - Redirige a la lista de obras después de eliminar
    """
    model = Comision
    template_name = "gallery/backoffice/admin_lista_obras.html"
    success_url = reverse_lazy('obra_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, f"Obra '{self.get_object()}' eliminada correctamente.")
        return super().delete(request, *args, **kwargs)


# ====================== LIST ======================
@method_decorator(admin_required, name='dispatch')
class ObraListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todas las obras en el panel de administración.
    
    Características:
    - Requiere autenticación y rol de administrador
    - Muestra todas las obras en una lista
    - Usa el contexto 'obras' para la plantilla
    """
    model = Comision
    template_name = "backoffice/obra_list.html"
    context_object_name = 'obras'
