from django.urls import path
from .views import (
    CategoriaListView, CategoriaCreateView,
    CategoriaUpdateView, CategoriaDeleteView
)

app_name = 'categories'

urlpatterns = [
    path('admin/categorias/', CategoriaListView.as_view(), name='admin_categorias_list'),
    path('admin/categorias/crear/', CategoriaCreateView.as_view(), name='admin_categoria_create'),
    path('admin/categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='admin_categoria_update'),
    path('admin/categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='admin_categoria_delete'),
] 