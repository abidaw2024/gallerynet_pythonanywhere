from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

def contacto(request):
    if request.method == 'POST':
        print("¡Recibido POST en contacto!")
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        print(f"Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}")
        if nombre and email and mensaje:
            try:
                send_mail(
                    subject=f'Contacto de {nombre} <{email}>',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['gallerynet2025@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Pronto nos pondremos en contacto contigo.')
                return redirect('contacto')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al enviar el mensaje. Intenta de nuevo más tarde.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    return render(request, 'contacto.html')
