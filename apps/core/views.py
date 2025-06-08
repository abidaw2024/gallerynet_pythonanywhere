from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging

# para validar el email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        if not nombre or not email or not mensaje:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'contacto.html')

        # ✅ Validar el formato del email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Por favor, ingresa un correo electrónico válido.')
            return render(request, 'contacto.html')

        try:
            mensaje_completo = f"""
            Nombre: {nombre}
            Email: {email}
            
            Mensaje:
            {mensaje}
            """
            
            send_mail(
                subject=f'Contacto de {nombre} <{email}>',
                message=mensaje_completo,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Mejor usar el email del sistema
                recipient_list=['gallerynet2025@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Pronto nos pondremos en contacto contigo.')
            return redirect('contacto')
            
        except Exception as e:
            logger.error(f"Error al enviar correo de contacto: {str(e)}")
            messages.error(request, 'Ocurrió un error al enviar el mensaje. Por favor, intenta de nuevo más tarde o contacta directamente a gallerynet2025@gmail.com')

    return render(request, 'contacto.html')
