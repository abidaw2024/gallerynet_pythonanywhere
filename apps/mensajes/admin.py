from django.contrib import admin
from .models import Mensaje

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('remitente', 'destinatario', 'asunto', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('asunto', 'contenido', 'remitente__email', 'destinatario__email')
    readonly_fields = ('referencia',)
    date_hierarchy = 'fecha_envio'
