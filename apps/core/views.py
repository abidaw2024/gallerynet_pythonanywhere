from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging

# para validar el email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#Configuración del logger para registrar errores
logger = logging.getLogger(__name__)

def contacto(request):
    #Procesamiento del formulario cuando se envía (POST)
    if request.method == 'POST':
        # Obtener y limpiar los datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        # Validación de campos vacíos
        if not nombre or not email or not mensaje:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'contacto.html')

        #Validación del formato del email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Por favor, ingresa un correo electrónico válido.')
            return render(request, 'contacto.html')

        #Proceso de envío del email
        try:
             #Formato del mensaje
            mensaje_completo = f"""
            Nombre: {nombre}
            Email: {email}
            
            Mensaje:
            {mensaje}
            """
            
            # Envío del email al correo de la empresa
            send_mail(
                subject=f'Contacto de {nombre} <{email}>',
                message=mensaje_completo,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Email del sistema
                recipient_list=['gallerynet2025@gmail.com'],
                fail_silently=False,
            )
            
            # Mensaje de éxito y redirección
            messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Pronto nos pondremos en contacto contigo.')
            return redirect('contacto')
            
        # Manejo de errores en el envío del email
        except Exception as e:
            logger.error(f"Error al enviar correo de contacto: {str(e)}")
            messages.error(request, 'Ocurrió un error al enviar el mensaje. Por favor, intenta de nuevo más tarde o contacta directamente a gallerynet2025@gmail.com')

    #renderizado 
    return render(request, 'contacto.html')
