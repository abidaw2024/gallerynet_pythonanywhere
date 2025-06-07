from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    user_home, registro, iniciar_sesion, cerrar_sesion, perfil, editar_perfil,
    UsuarioListView, UsuarioDetailView, UsuarioUpdateView, UsuarioCreateView,
    UsuarioViewSet, cambiar_password, buscar_usuarios, seguir_usuario, lista_mensajes,
    conver_mensajes, UsuarioDeleteView, seguidos, seguidores
)

app_name = 'users'  # Definir el nombre de la aplicación

# ===== ROUTER =====
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    # ===== API REST =====
    path('api/', include(router.urls)),
    
    # ===== ADMIN =====
    path('admin/usuarios/', UsuarioListView.as_view(), name='admin_usuarios_list'),
    path('admin/usuarios/crear/', UsuarioCreateView.as_view(), name='admin_usuarios_create'),
    path('admin/usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='admin_usuarios_detail'),
    path('admin/usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='admin_usuarios_update'),
    path('admin/usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='admin_usuarios_delete'),
    
    # ===== USUARIOS =====
    path('', user_home, name='user_home'),  # Ruta para /users/
    
    path('register/', registro, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),

    path('perfil/<str:username>/', perfil, name='perfil'),  # Ruta para el perfil con username
    path('seguir/<str:username>/', seguir_usuario, name='seguir_usuario'),  # Ruta para seguir/dejar de seguir
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('cambiar-password/', cambiar_password, name='cambiar_password'),
    
    path('buscar/', buscar_usuarios, name='buscar'),
    path('mensajes/', lista_mensajes, name='lista_mensajes'),
    path('conver_mensajes/', conver_mensajes, name='conver_mensajes'),
    path('seguidos/<str:username>/', seguidos, name='seguidos'),
    path('seguidores/<str:username>/', seguidores, name='seguidores'),
]
