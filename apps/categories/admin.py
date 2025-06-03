from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'created_at')
    list_filter = ('activa', 'created_at')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-created_at',)
