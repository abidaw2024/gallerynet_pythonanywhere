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
        referencia = str(uuid.uuid4())
        mensaje = Mensaje(
            remitente=remitente,
            destinatario=destinatario,
            asunto=asunto,
            contenido=contenido,
            referencia=referencia,
            encargo=encargo
        )
        mensaje.full_clean()
        mensaje.save()
        
        asunto_email = f"[GalleryNet #{referencia}] {asunto}"
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
        asunto = email_data.get('subject', '')
        referencia = None
        if '[GalleryNet #' in asunto:
            try:
                referencia = asunto.split('[GalleryNet #')[1].split(']')[0]
            except IndexError:
                return None
        if not referencia:
            return None
        try:
            mensaje_original = Mensaje.objects.get(referencia=referencia)
        except Mensaje.DoesNotExist:
            return None
        nuevo_mensaje = Mensaje(
            remitente=mensaje_original.destinatario,
            destinatario=mensaje_original.remitente,
            asunto=f"Re: {mensaje_original.asunto}",
            contenido=email_data.get('body', ''),
            referencia=str(uuid.uuid4()),
            encargo=mensaje_original.encargo
        )
        nuevo_mensaje.full_clean()
        nuevo_mensaje.save()
        send_mail(
            subject=f"[GalleryNet #{nuevo_mensaje.referencia}] Re: {mensaje_original.asunto}",
            message=email_data.get('body', ''),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mensaje_original.remitente.email],
            fail_silently=False,
        )
        return nuevo_mensaje 