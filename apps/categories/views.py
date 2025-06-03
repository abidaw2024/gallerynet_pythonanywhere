from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categoria
from .forms import CategoriaForm

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'backoffice/categorias/admin_categorias_list.html'
    context_object_name = 'categorias'
    ordering = ['nombre']

class CategoriaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'backoffice/categorias/admin_categoria_form.html'
    success_url = reverse_lazy('categories:admin_categorias_list')
    success_message = 'Categoría creada exitosamente'

class CategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'backoffice/categorias/admin_categoria_form.html'
    success_url = reverse_lazy('categories:admin_categorias_list')
    success_message = 'Categoría actualizada exitosamente'

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'backoffice/categorias/admin_categoria_confirm_delete.html'
    success_url = reverse_lazy('categories:admin_categorias_list') 