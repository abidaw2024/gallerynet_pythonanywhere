"""
Configuración de URLs para la aplicación Sales
Este archivo define todas las rutas para:
- API REST de órdenes y pedidos
- Interfaz de usuario para compras y ventas
- Gestión de encargos y pagos
"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

app_name = 'sales'  # Namespace para las URLs de la aplicación

# Configuración del router para la API REST
router = DefaultRouter()
router.register(r'orders', OrderViewSet)  # Endpoint para órdenes
router.register(r'order-items', OrderItemViewSet)  # Endpoint para items de órdenes

urlpatterns = [
    # ====================== RUTAS DE LA API REST ======================
    path('api/', include(router.urls)),  # Incluye todas las rutas de la API
    
    # ====================== RUTAS DE LA INTERFAZ DE USUARIO ======================
    # Detalles y gestión de comisiones
    path('commission/<int:obra_id>/details/', views.commission_details, name='commission_details'),
    path('artist/commissions/', views.artist_commissions, name='artist_commissions'),
    path('encargos/recibidos/', views.encargos_recibidos, name='encargos_recibidos'),
    path('encargos/enviados/', views.encargos_enviados, name='encargos_enviados'),
    path('encargos/<int:encargo_id>/aceptar/', views.aceptar_encargo, name='aceptar_encargo'),
    path('encargos/<int:encargo_id>/rechazar/', views.rechazar_encargo, name='rechazar_encargo'),
    path('confirmar-pedido/<int:obra_id>/', views.confirmar_pedido, name='confirmar_pedido'),
    
    # Proceso de checkout y pagos
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/error/', views.payment_error, name='payment_error'),
    path('pedido_completado/', views.order_complete, name='pedido_completado'),
    
    # Historial de compras y ventas
    path('mis_compras/', views.mis_compras, name='mis_compras'),
    path('mis_ventas/', views.mis_ventas, name='mis_ventas'),
    
    # Rutas de administración
    path('admin/pedidos/', views.admin_pedidos_list, name='admin_pedidos_list'),
    path('admin/pedidos/<int:encargo_id>/cancelar/', views.admin_cancelar_encargo, name='admin_cancelar_encargo'),
    path('admin/pedidos/<int:encargo_id>/', views.admin_pedidos_detail, name='admin_pedidos_detail'),
]
