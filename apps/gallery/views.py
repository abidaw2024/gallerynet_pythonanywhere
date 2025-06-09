from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comision
from apps.mensajes.models import Mensaje
from .serializers import ComisionSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ComisionForm
from django.db.models import Q
from apps.users.models import Categoria
from django.core.paginator import Paginator

def is_admin(user):
    """Verifica si un usuario tiene permisos de administrador"""
    return user.is_staff

# ====================== API REST ======================
class ComisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la API REST de comisiones.
    Permite operaciones CRUD a través de la API.
    """
    queryset = Comision.objects.all()
    serializer_class = ComisionSerializer

# ====================== VISTAS PARA obras ======================
@login_required
def lista_obras_view(request):
    """
    Vista para listar todas las obras disponibles.
    Requiere que el usuario esté autenticado.
    """
    obras_list = Comision.objects.all()
    categorias = Categoria.objects.all()
    paginator = Paginator(obras_list, 12)  # 12 obras por página
    page_number = request.GET.get('page')
    obras = paginator.get_page(page_number)
    return render(request, 'gallery/obras_list.html', {
        'obras': obras,
        'categorias': categorias
    })

@login_required
def detalle_obra_view(request, obra_id):
    """
    Vista para mostrar los detalles de una obra específica.
    Incluye información detallada y opciones de compra.
    """
    obra = get_object_or_404(Comision, id=obra_id)
    return render(request, 'gallery/detalle_obra.html', {
        'obra': obra,
    })

@login_required
def buscar_obras_view(request):
    """
    Vista para buscar obras por título.
    Retorna obras que coincidan con la búsqueda.
    """
    query = request.GET.get('q', '')
    obras = Comision.objects.filter(titulo__icontains=query) if query else Comision.objects.none()
    return render(request, 'buscar_obras.html', {'obras': obras, 'query': query})

# ====================== MIXINS Y VISTAS DE ADMINISTRACIÓN ======================
class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar permisos de administrador"""
    def test_func(self):
        return self.request.user.is_staff

class ObraListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    """
    Vista para listar obras en el panel de administración.
    Permite ordenar por fecha de creación.
    """
    model = Comision
    template_name = 'backoffice/admin_obras_list.html'
    context_object_name = 'obras'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering', 'desc')
        if ordering == 'asc':
            queryset = queryset.order_by('fecha_creacion')
        else:
            queryset = queryset.order_by('-fecha_creacion')
        return queryset

class ObraDetailView(AdminRequiredMixin, LoginRequiredMixin, DetailView):
    """Vista para ver detalles de una obra en el panel de administración"""
    model = Comision
    template_name = 'backoffice/obra_detail.html'
    context_object_name = 'obra'

class ObraCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Vista para crear obras en el panel de administración.
    Incluye mensajes de éxito y redirección.
    """
    model = Comision
    template_name = 'backoffice/obra_form.html'
    fields = ['titulo', 'descripcion', 'estilo', 'tecnica', 'tema',
              'imagen_principal', 'imagen_adicional_1', 'imagen_adicional_2', 'imagen_adicional_3',
              'precio_basico', 'descripcion_basico',
              'precio_estandar', 'descripcion_estandar',
              'precio_premium', 'descripcion_premium',
              'estado']
    success_message = "Obra creada exitosamente"
    
    def get_success_url(self):
        return reverse_lazy('gallery:admin_obras_list')
    
    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Obra '{self.object.titulo}' creada exitosamente.")
        return response

class ObraUpdateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista para actualizar obras en el panel de administración.
    Incluye mensajes de éxito y redirección.
    """
    model = Comision
    template_name = 'backoffice/obra_form.html'
    fields = ['titulo', 'descripcion', 'estilo', 'tecnica', 'tema',
              'imagen_principal', 'imagen_adicional_1', 'imagen_adicional_2', 'imagen_adicional_3',
              'precio_basico', 'descripcion_basico',
              'precio_estandar', 'descripcion_estandar',
              'precio_premium', 'descripcion_premium',
              'estado']
    success_message = "Obra actualizada exitosamente"
    success_url = reverse_lazy('gallery:admin_obras_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Obra '{self.object.titulo}' actualizada exitosamente.")
        return response

class ObraDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar obras en el panel de administración.
    Incluye confirmación y mensajes de éxito.
    """
    model = Comision
    template_name = 'backoffice/obra_confirm_delete.html'
    success_url = reverse_lazy('gallery:admin_obras_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Confirmar eliminación de obra"
        context['mensaje_confirmacion'] = f"¿Estás seguro de que deseas eliminar la obra '{self.object.titulo}'?"
        return context

# ====================== VISTAS PARA VENDEDORES ======================
class CrearComisionView(LoginRequiredMixin, CreateView):
    """
    Vista para que los vendedores creen nuevas comisiones.
    Redirige al perfil del usuario después de crear.
    """
    model = Comision
    form_class = ComisionForm
    template_name = 'gallery/crear_comision.html'

    def get_success_url(self):
        return reverse_lazy('users:perfil', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        form.instance.estado = 'disponible'  # Establecemos el estado como disponible por defecto
        return super().form_valid(form)

class EliminarObraView(LoginRequiredMixin, DeleteView):
    """
    Vista para que los vendedores eliminen sus propias obras.
    Solo permite eliminar obras propias.
    """
    model = Comision
    template_name = 'gallery/obra_propia_detalle.html'
    success_url = reverse_lazy('users:perfil')

    def get_success_url(self):
        return reverse_lazy('users:perfil', kwargs={'username': self.request.user.username})

    def get_queryset(self):
        return self.model.objects.filter(vendedor=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, f"La obra '{self.get_object().titulo}' ha sido eliminada correctamente.")
        return super().delete(request, *args, **kwargs)