"""
Modelos para la gestión de ventas y pedidos
Este archivo define los modelos necesarios para:
- Gestión de órdenes y pedidos
- Items de pedidos
- Encargos de obras
"""

from django.db import models
from django.conf import settings
from apps.gallery.models import Comision

class Order(models.Model):
    """
    Modelo para gestionar las órdenes de compra.
    
    Campos:
    - user: Usuario que realiza la compra
    - status: Estado de la orden (Pendiente/Completado)
    - total: Monto total de la orden
    - created_at: Fecha y hora de creación
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    """
    Modelo para los items individuales de una orden.
    
    Campos:
    - order: Orden a la que pertenece el item
    - artwork_name: Nombre de la obra
    - quantity: Cantidad de items
    - price: Precio unitario
    
    Métodos:
    - save: Actualiza el total de la orden al guardar
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    artwork_name = models.CharField(max_length=200, default="Obra sin nombre")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total()  # Actualiza el total cuando se guarda un item

# Modelo Encargo
class Encargo(models.Model):
    """
    Modelo para gestionar los encargos de obras.
    
    Campos:
    - cliente: Usuario que realiza el encargo
    - artista: Usuario que recibe el encargo
    - obra: Comisión encargada
    - plan: Tipo de plan seleccionado (básico, estándar, premium)
    - estado: Estado actual del encargo
    - fecha: Fecha y hora de creación del encargo
    """
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='encargos_realizados')
    artista = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='encargos_recibidos')
    obra = models.ForeignKey(Comision, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='Pendiente')
    fecha = models.DateTimeField(auto_now_add=True)