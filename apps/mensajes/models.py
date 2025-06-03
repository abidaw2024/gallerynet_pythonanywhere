from django.db import models
from django.conf import settings
from apps.sales.models import Encargo
import uuid

class Mensaje(models.Model):
    """
    Modelo para gestionar los mensajes entre usuarios.
    
    Campos:
    - remitente: Usuario que envía el mensaje
    - destinatario: Usuario que recibe el mensaje
    - encargo: Encargo relacionado (opcional)
    - asunto: Asunto del mensaje
    - contenido: Contenido del mensaje
    - referencia: ID único para rastrear la conversación
    - fecha_envio: Fecha y hora de envío
    - leido: Indica si el mensaje ha sido leído
    """
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados'
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos'
    )
    encargo = models.ForeignKey(
        Encargo,
        on_delete=models.CASCADE,
        related_name='mensajes',
        null=True,
        blank=True
    )
    asunto = models.CharField(max_length=200)
    contenido = models.TextField()
    referencia = models.CharField(
        max_length=50,
        unique=True,
        default=uuid.uuid4,
        help_text="ID único para seguimiento del correo"
    )
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"Mensaje de {self.remitente} a {self.destinatario} - {self.asunto}" 