from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        if nombre and email and mensaje:
            try:
                # Preparar el mensaje
                mensaje_completo = f"""
                Nombre: {nombre}
                Email: {email}
                
                Mensaje:
                {mensaje}
                """
                
                # Enviar el correo
                send_mail(
                    subject=f'Contacto de {nombre} <{email}>',
                    message=mensaje_completo,
                    from_email=email,  # Usar el email del remitente
                    recipient_list=['gallerynet2025@gmail.com'],
                    fail_silently=False,
                )
                
                messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Pronto nos pondremos en contacto contigo.')
                return redirect('contacto')
                
            except Exception as e:
                logger.error(f"Error al enviar correo de contacto: {str(e)}")
                messages.error(request, 'Ocurrió un error al enviar el mensaje. Por favor, intenta de nuevo más tarde o contacta directamente a gallerynet2025@gmail.com')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
            
    return render(request, 'contacto.html')

