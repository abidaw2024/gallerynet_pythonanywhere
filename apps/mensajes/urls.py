from django.urls import path
from . import views

app_name = 'mensajes'

urlpatterns = [
    path('', views.lista_mensajes, name='lista_mensajes'),
    path('conversacion/<int:encargo_id>/', views.detalle_conversacion, name='detalle_conversacion'),
    path('conversacion-general/', views.conversacion_general, name='conversacion_general'),
    path('enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('enviar/<int:encargo_id>/', views.enviar_mensaje, name='enviar_mensaje_encargo'),
    path('encargo/<int:obra_id>/', views.enviar_mensaje_encargo, name='enviar_mensaje_encargo'),
   

    #admin
    path('admin/mensajes/', views.AdminMensajeListView.as_view(), name='admin_mensajes_list'),
    path('admin/mensajes/<int:pk>/', views.AdminMensajeDetailView.as_view(), name='admin_mensaje_detail'),
    path('admin/mensajes/<int:pk>/eliminar/', views.AdminMensajeDeleteView.as_view(), name='admin_mensaje_delete'),
] 