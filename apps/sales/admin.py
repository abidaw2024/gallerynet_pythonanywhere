from django.contrib import admin
from .models import Order, OrderItem, Encargo

# Register your models here.
admin.site.register(Order)

admin.site.register(OrderItem)

@admin.register(Encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'artista', 'obra', 'plan', 'estado', 'fecha')
    list_filter = ('estado', 'plan', 'fecha')
    search_fields = ('cliente__username', 'artista__username', 'obra__titulo', 'descripcion')