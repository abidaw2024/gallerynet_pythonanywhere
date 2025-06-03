from django.core.mail import send_mail
from django.conf import settings
from .models import Mensaje
import uuid

class EmailService:
    @staticmethod
    def enviar_mensaje(remitente, destinatario, asunto, contenido, encargo=None):
        """
        Envía un mensaje y lo guarda en la base de datos.
        
        Args:
            remitente: Usuario que envía el mensaje
            destinatario: Usuario que recibe el mensaje
            asunto: Asunto del mensaje
            contenido: Contenido del mensaje
            encargo: Encargo relacionado (opcional)
        """
        # Generar ID único para seguimiento
        referencia = str(uuid.uuid4())
        
        # Crear el mensaje en la base de datos
        mensaje = Mensaje.objects.create(
            remitente=remitente,
            destinatario=destinatario,
            asunto=asunto,
            contenido=contenido,
            referencia=referencia,
            encargo=encargo
        )
        
        # Preparar el asunto con la referencia
        asunto_email = f"[GalleryNet #{referencia}] {asunto}"
        
        # Enviar el correo
        send_mail(
            subject=asunto_email,
            message=contenido,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[destinatario.email],
            fail_silently=False,
        )
        
        return mensaje

    @staticmethod
    def procesar_respuesta_email(email_data):
        """
        Procesa una respuesta de correo electrónico.
        - Guarda el mensaje en la base de datos (Mensajes)
        - Reenvía la respuesta al cliente (comprador)
        Args:
            email_data: Diccionario con los datos del correo recibido
        """
        # Extraer la referencia del asunto
        asunto = email_data.get('subject', '')
        referencia = None
        # Buscar la referencia en el asunto
        if '[GalleryNet #' in asunto:
            try:
                referencia = asunto.split('[GalleryNet #')[1].split(']')[0]
            except IndexError:
                return None
        if not referencia:
            return None
        # Buscar el mensaje original
        try:
            mensaje_original = Mensaje.objects.get(referencia=referencia)
        except Mensaje.DoesNotExist:
            return None
        # Crear el nuevo mensaje en la base de datos (respuesta)
        nuevo_mensaje = Mensaje.objects.create(
            remitente=mensaje_original.destinatario,  # El artista que responde
            destinatario=mensaje_original.remitente,  # El cliente original
            asunto=f"Re: {mensaje_original.asunto}",
            contenido=email_data.get('body', ''),
            referencia=str(uuid.uuid4()),
            encargo=mensaje_original.encargo
        )
        # Reenviar el mensaje al cliente (comprador)
        send_mail(
            subject=f"[GalleryNet #{nuevo_mensaje.referencia}] Re: {mensaje_original.asunto}",
            message=email_data.get('body', ''),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mensaje_original.remitente.email],
            fail_silently=False,
        )
        return nuevo_mensaje 