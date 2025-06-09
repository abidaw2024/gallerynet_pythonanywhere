from django.db import models
from django.conf import settings
from apps.sales.models import Encargo
import uuid
import re
from django.core.exceptions import ValidationError

def validar_contenido_sin_info_personal(value):
    """
    Valida que el contenido no contenga información personal
    """
    # Patrones para detectar información personal
    patrones = [
        r'\b\d{9}\b',  # Números de 9 dígitos
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Correos electrónicos
        r'https?://\S+|www\.\S+'  # URLs
    ]
    
    # Verificar cada patrón
    for patron in patrones:
        if re.search(patron, value):
            raise ValidationError('No puedes enviar información personal en los mensajes')

class Mensaje(models.Model):
    """
    Modelo para gestionar los mensajes entre usuarios.
    
    - referencia: ID único para rastrear la conversación
    """
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    encargo = models.ForeignKey(Encargo, on_delete=models.CASCADE, related_name='mensajes', null=True, blank=True)
    asunto = models.CharField(max_length=200)
    contenido = models.TextField(validators=[validar_contenido_sin_info_personal])
    referencia = models.CharField(max_length=50, unique=True, default=uuid.uuid4, help_text="ID único para seguimiento del correo")
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"Mensaje de {self.remitente} a {self.destinatario} - {self.asunto}" 

    def clean(self):
        """
        Validación adicional antes de guardar el mensaje
        """
        super().clean()
        validar_contenido_sin_info_personal(self.contenido)
        validar_contenido_sin_info_personal(self.asunto) 