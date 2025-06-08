from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import politicas_privacidad, terminos_condiciones, contacto, home
from rest_framework.routers import DefaultRouter
from apps.gallery.views import ComisionViewSet
from apps.sales.views import OrderViewSet
from apps.users.views import UsuarioViewSet

from django.views.generic import TemplateView # Importa TemplateView


#API
router = DefaultRouter()
router.register(r'obras', ComisionViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    # Redirección de index.html a la raíz
    path('index.html', lambda request: redirect('/')),
    
    # Página de inicio
    path('', home, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),

    # Backoffice
    path('backoffice/', include('apps.backoffice.urls', namespace='backoffice')),

    # API
    path('api/', include(router.urls)),  # Todas las rutas de la API en /api/

    # Apps frontend (versión web)
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('sales/', include('apps.sales.urls', namespace='sales')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('categories/', include('apps.categories.urls', namespace='categories')),
    path('mensajes/', include('apps.mensajes.urls', namespace='mensajes')),
    
    # Páginas estáticas
    path('politicas-privacidad/', politicas_privacidad, name='politicas-privacidad'),
    path('terminos-condiciones/', terminos_condiciones, name='terminos-condiciones'),

    path('core/', include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else []

# Manejadores de error
handler400 = 'gallerynet.views.error_400'
handler403 = 'gallerynet.views.error_403'
handler404 = 'gallerynet.views.error_404'
handler500 = 'gallerynet.views.error_500'