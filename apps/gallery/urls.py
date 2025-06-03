"""
Configuración de URLs para la aplicación Gallery
Este archivo define todas las rutas URL para la gestión de obras y comisiones.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    lista_obras_view, 
    detalle_obra_view, 
    buscar_obras_view,
    ObraListView, ObraDetailView, ObraCreateView, 
    ObraUpdateView, ObraDeleteView,
    ComisionViewSet,
    CrearComisionView,
    EliminarObraView,
    EditarComisionView,
    agregar_comentario
)

# router
router = DefaultRouter()
router.register(r'obras', ComisionViewSet) 

app_name = 'gallery'  # Namespace para las URLs de la aplicación

urlpatterns = [
    # =============== URLs PARA LA API REST ===============
    path('api/', include(router.urls)),  #todas las rutas de API
    
    # =============== URLs PARA EL FRONTEND ===============
    # obras
    path('obras/', lista_obras_view, name='lista_obras'),
    path('obras/<int:obra_id>/', detalle_obra_view, name='detalle_obra'),
    path('obras/<int:obra_id>/comentar/', agregar_comentario, name='agregar_comentario'),
    path('buscar/', buscar_obras_view, name='buscar_obras'),
    
    #Gestión de comisiones
    path('crear-comision/', CrearComisionView.as_view(), name='crear_comision'),
    path('obras/<int:pk>/eliminar/', EliminarObraView.as_view(), name='eliminar_obra'),
    path('obras/<int:pk>/editar/', EditarComisionView.as_view(), name='editar_comision'),
    
    # =============== URLs PARA EL PANEL DE ADMINISTRACIÓN ===============
    #Lista de obras en el panel admin
    path('admin/obras/', ObraListView.as_view(), name='admin_obras_list'),
    
    #Detalles de una obra en el panel admin
    path('admin/obras/<int:pk>/', ObraDetailView.as_view(), name='obra_detail'),
    
    #Creación de obras en el panel admin
    path('admin/obras/crear/', ObraCreateView.as_view(), name='obra_create'),
    
    #Edición de obras en el panel admin
    path('admin/obras/<int:pk>/editar/', ObraUpdateView.as_view(), name='obra_update'),
    
    #Eliminación de obras en el panel admin
    path('admin/obras/<int:pk>/eliminar/', ObraDeleteView.as_view(), name='obra_delete'),
]
