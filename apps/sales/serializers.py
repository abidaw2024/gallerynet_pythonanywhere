from rest_framework import serializers
from .models import Order, OrderItem

# Serializador para la API REST
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        #campos que se incluirán en la serialización:
        fields = ['id', 'artwork', 'quantity', 'price']  # artwork será el ID

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'items']