from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('admin/categorias/', views.admin_categoria_list, name='admin_categoria_list'),
    path('admin/categorias/<int:pk>/', views.admin_categoria_detail, name='admin_categoria_detail'),
    path('admin/categorias/<int:pk>/editar/', views.admin_categoria_update, name='admin_categoria_update'),
    path('admin/categorias/crear/', views.admin_categoria_create, name='admin_categoria_create'),
    path('admin/categorias/<int:pk>/eliminar/', views.admin_categoria_delete, name='admin_categoria_delete'),
] 