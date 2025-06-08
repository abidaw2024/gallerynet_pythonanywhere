"""
Vistas para la gestión de ventas y compras
Este archivo maneja todas las operaciones relacionadas con:
- Procesamiento de pedidos
- Checkout y pagos
- Gestión de encargos
- Historial de compras y ventas
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem, Encargo
from django.contrib import messages
from apps.gallery.models import Comision
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from apps.mensajes.services import EmailService
from django.conf import settings
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.users.decorators import admin_required
from django.utils.decorators import method_decorator

# ====================== API REST ======================
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la API REST de órdenes.
    Permite a los usuarios ver y gestionar sus propias órdenes.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la API REST de items de orden.
    Permite gestionar los items individuales de cada orden.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

# ====================== VISTAS DE ENCARGOS ======================
@login_required
def encargos_recibidos(request):
    """
    Vista para mostrar los encargos recibidos por un artista.
    Muestra los encargos ordenados por fecha (más recientes primero).
    """
    encargos = Encargo.objects.filter(artista=request.user).order_by('-fecha')
    return render(request, 'sales/encargos_recibidos.html', {'encargos': encargos})

@login_required
def encargos_enviados(request):
    """
    Vista para mostrar los encargos enviados por un cliente.
    Muestra los encargos ordenados por fecha (más recientes primero).
    """
    encargos = Encargo.objects.filter(cliente=request.user).order_by('-fecha')
    return render(request, 'sales/encargos_enviados.html', {'encargos': encargos})

# ====================== PROCESO DE CHECKOUT ======================
@login_required
def checkout(request):
    """
    Vista para el proceso de checkout.
    Maneja:
    - Selección del plan (básico, estándar, premium)
    - Cálculo de precios
    - Creación de encargos
    - Redirección según resultado del pago
    """
    obra_id = request.POST.get('obra_id') or request.GET.get('obra_id')
    plan = request.POST.get('plan') or request.GET.get('plan', 'basico')
    descripcion = request.POST.get('descripcion') or request.GET.get('descripcion', '')

    # Obtener obra y calcular precio según plan
    obra = Comision.objects.get(id=obra_id) if obra_id else None
    if obra:
        if plan == 'basico':
            precio = obra.get_precio_basico()
            descripcion_plan = obra.descripcion_basico
        elif plan == 'estandar':
            precio = obra.get_precio_estandar()
            descripcion_plan = obra.descripcion_estandar
        elif plan == 'premium':
            precio = obra.get_precio_premium()
            descripcion_plan = obra.descripcion_premium
        else:
            precio = obra.get_precio_basico()
            descripcion_plan = obra.descripcion_basico
    else:
        precio = 0
        descripcion_plan = ''

    # Fee de la empresa
    fee = getattr(settings, 'EMPRESA_FEE', 2.50)
    total = float(precio) + float(fee)

    # Procesar el pago y crear encargo
    if request.method == 'POST':
        payment_success = request.POST.get('payment_success', 'true') == 'true'
        if payment_success:
            Encargo.objects.create(
                cliente=request.user,
                artista=obra.vendedor,
                obra=obra,
                plan=plan,
                estado='Pendiente',
            )
            return redirect('sales:payment_success')
        else:
            return redirect('sales:payment_error')

    return render(request, 'sales/checkout.html', {
        'obra': obra,
        'plan': plan,
        'precio': precio,
        'fee': fee,
        'total': total,
        'descripcion_plan': descripcion_plan,
        'descripcion': descripcion,
    })

# ====================== VISTAS DE RESULTADO DE PAGO ======================
def payment_success(request):
    """Vista para mostrar el éxito del pago y marcar el encargo como completado"""
    encargo_id = request.GET.get('encargo_id')
    if encargo_id:
        try:
            encargo = Encargo.objects.get(id=encargo_id)
            encargo.estado = 'completado'
            encargo.save()
        except Encargo.DoesNotExist:
            pass  # O puedes mostrar un mensaje de error si lo prefieres
    return render(request, 'sales/payment_success.html', {
        'order': {'total': 400.00}
    })

def payment_error(request):
    """Vista para mostrar el error en el pago"""
    return render(request, 'sales/payment_error.html', {
        'order': {'total': 400.00}
    })

def order_complete(request):
    """Vista para mostrar la confirmación de pedido completado"""
    return render(request, 'sales/pedido_completado.html')

# ====================== HISTORIAL DE COMPRAS Y VENTAS ======================
def mis_compras(request):
    """
    Vista para mostrar el historial de compras del usuario.
    Actualmente usa datos de ejemplo (debe ser implementado con datos reales).
    """
    compras = [
        {
            'obra': 'La Noche Estrellada',
            'artista': 'Vincent van Gogh',
            'fecha': '2023-10-01',
            'precio': '$1,000,000',
            'estado': 'Entregado',
        },
        {
            'obra': 'Los Girasoles',
            'artista': 'Vincent van Gogh',
            'fecha': '2023-09-15',
            'precio': '$800,000',
            'estado': 'En proceso',
        }
    ]
    return render(request, 'sales/mis_compras.html', {'compras': compras})

def mis_ventas(request):
    """
    Vista para mostrar el historial de ventas del usuario.
    Actualmente usa datos de ejemplo (debe ser implementado con datos reales).
    """
    ventas = [
        {
            'obra': 'La Noche Estrellada',
            'comprador': 'Juan Pérez',
            'fecha': '2023-10-01',
            'precio': '$1,000,000',
            'estado': 'Entregado',
        },
        {
            'obra': 'Los Girasoles',
            'comprador': 'María García',
            'fecha': '2023-09-15',
            'precio': '$800,000',
            'estado': 'En proceso',
        }
    ]
    return render(request, 'sales/mis_ventas.html', {'ventas': ventas})

# ====================== DETALLES DE COMISIÓN ======================
@login_required
def commission_details(request, obra_id):
    """
    Vista para mostrar los detalles de una comisión específica.
    Permite al usuario seleccionar un plan y agregar una descripción.
    """
    obra = Comision.objects.get(id=obra_id)
    plan = request.GET.get('plan', 'basico')
    
    # Obtener el precio según el plan seleccionado
    if plan == 'basico':
        precio = obra.get_precio_basico()
    elif plan == 'estandar':
        precio = obra.get_precio_estandar()
    else:  # premium
        precio = obra.get_precio_premium()
    
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        return redirect(f"{reverse('sales:checkout')}?obra_id={obra.id}&plan={plan}&descripcion={descripcion}")
    
    return render(request, 'sales/commission-details.html', {
        'obra': obra,
        'plan': plan,
        'precio': precio
    })

@login_required
def artist_commissions(request):
    """
    Vista para mostrar los encargos recibidos por el artista.
    Actualmente usa datos de ejemplo (debe ser implementado con datos reales).
    """
    encargos = [
        {
            'cliente': 'usuario1',
            'obra': 'Retrato digital',
            'plan': 'Básico',
            'descripcion': 'Quiero un retrato con fondo azul',
            'estado': 'Pendiente',
        },
        {
            'cliente': 'usuario2',
            'obra': 'Mascota caricatura',
            'plan': 'Premium',
            'descripcion': 'Caricatura de mi perro con fondo verde',
            'estado': 'Pendiente',
        },
    ]
    return render(request, 'sales/artist-commissions.html', {'encargos': encargos})

@staff_member_required
def admin_pedidos_list(request):
    """
    Vista para que los administradores puedan ver y gestionar todos los encargos.
    Muestra: cliente, artista, estado, obra, plan y fecha.
    """
    encargos = Encargo.objects.select_related('cliente', 'artista', 'obra').order_by('-fecha')
    return render(request, 'sales/admin_pedidos_list.html', {
        'encargos': encargos
    })

@login_required
def confirmar_pedido(request, obra_id):
    """
    Vista para confirmar un pedido y generar el enlace de pago.
    Solo el vendedor puede confirmar el pedido.
    """
    obra = get_object_or_404(Comision, id=obra_id)
    
    # Verificar que el usuario es el vendedor
    if request.user != obra.vendedor:
        messages.error(request, 'No tienes permiso para confirmar este pedido')
        return redirect('gallery:detalle_obra', obra_id=obra_id)
    
    # Buscar el encargo más reciente sin confirmar
    encargo = Encargo.objects.filter(
        obra=obra,
        estado='pendiente'
    ).order_by('-fecha_creacion').first()
    
    if not encargo:
        messages.error(request, 'No hay pedidos pendientes para esta obra')
        return redirect('gallery:detalle_obra', obra_id=obra_id)
    
    # Crear la orden
    order = Order.objects.create(
        user=encargo.cliente,
        total=obra.precio,
        status='pending'
    )
    
    # Actualizar el estado del encargo
    encargo.estado = 'confirmado'
    encargo.save()
    
    # Enviar email al cliente con el enlace de pago
    email_service = EmailService()
    email_service.enviar_mensaje(
        remitente=request.user,
        destinatario=encargo.cliente,
        asunto=f'Pedido confirmado - {obra.titulo}',
        contenido=f'''
        Tu pedido ha sido confirmado. Por favor, realiza el pago usando el siguiente enlace:
        {request.build_absolute_uri(reverse('sales:procesar_pago', args=[order.id]))}
        
        Total a pagar: ${obra.precio}
        ''',
        encargo=encargo
    )
    
    messages.success(request, 'Pedido confirmado y enlace de pago enviado al cliente')
    return redirect('gallery:detalle_obra', obra_id=obra_id)

# ====================== VISTAS ADMINISTRATIVAS ======================
@method_decorator(admin_required, name='dispatch')
class AdminOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'backoffice/admin_orders_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

@method_decorator(admin_required, name='dispatch')
class AdminOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'backoffice/admin_order_detail.html'
    context_object_name = 'order'

@method_decorator(admin_required, name='dispatch')
class AdminOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'backoffice/admin_order_update.html'
    fields = ['status', 'total', 'notes']
    success_url = reverse_lazy('sales:admin_orders_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Pedido actualizado correctamente.")
        return super().form_valid(form)

@login_required
def aceptar_encargo(request, encargo_id):
    """
    Vista para aceptar un encargo.
    Solo el artista puede aceptar sus propios encargos.
    """
    encargo = get_object_or_404(Encargo, id=encargo_id, artista=request.user)
    if encargo.estado == 'Pendiente':
        encargo.estado = 'Aceptado'
        encargo.save()
        messages.success(request, 'Has aceptado el encargo exitosamente.')
    return redirect('sales:encargos_recibidos')

@login_required
def rechazar_encargo(request, encargo_id):
    """
    Vista para rechazar un encargo.
    Solo el artista puede rechazar sus propios encargos.
    """
    encargo = get_object_or_404(Encargo, id=encargo_id, artista=request.user)
    if encargo.estado == 'Pendiente':
        encargo.estado = 'Rechazado'
        encargo.save()
        messages.warning(request, 'Has rechazado el encargo.')
    return redirect('sales:encargos_recibidos')

@login_required
def cancelar_encargo(request, encargo_id):
    """
    Vista para cancelar un encargo.
    Solo el cliente que lo creó puede cancelarlo si está pendiente.
    """
    encargo = get_object_or_404(Encargo, id=encargo_id, cliente=request.user)
    if encargo.estado == 'Pendiente':
        encargo.delete()
        messages.success(request, 'Has cancelado el encargo exitosamente.')
    return redirect('sales:encargos_enviados')