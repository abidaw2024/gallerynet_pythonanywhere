from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Mensaje
from apps.sales.models import Encargo
from apps.users.models import Usuario
from apps.gallery.models import Comision
from .services import EmailService
from apps.sales.models import Encargo
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.decorators import admin_required
from django.utils.decorators import method_decorator

@login_required
def lista_mensajes(request):
    # Obtener mensajes donde el usuario es remitente o destinatario
    mensajes = Mensaje.objects.filter(
        Q(remitente=request.user) | Q(destinatario=request.user)
    ).order_by('-fecha_envio')

    # Agrupar mensajes por encargo
    conversaciones = {}
    for mensaje in mensajes:
        if mensaje.encargo:
            if mensaje.encargo.id not in conversaciones:
                conversaciones[mensaje.encargo.id] = {
                    'encargo': mensaje.encargo,
                    'ultimo_mensaje': mensaje,
                    'no_leidos': 0
                }
            if not mensaje.leido and mensaje.destinatario == request.user:
                conversaciones[mensaje.encargo.id]['no_leidos'] += 1
        else:
            if 'general' not in conversaciones:
                conversaciones['general'] = {
                    'encargo': None,
                    'ultimo_mensaje': mensaje,
                    'no_leidos': 0
                }
            if not mensaje.leido and mensaje.destinatario == request.user:
                conversaciones['general']['no_leidos'] += 1

    return render(request, 'mensajes/lista_mensajes.html', {
        'conversaciones': conversaciones.values()
    })

@login_required
def detalle_conversacion(request, encargo_id):
    encargo = get_object_or_404(Encargo, id=encargo_id)
    
    # Verificar que el usuario es parte del encargo
    if request.user not in [encargo.cliente, encargo.artista]:
        messages.error(request, 'No tienes permiso para ver esta conversación')
        return redirect('mensajes:lista_mensajes')

    mensajes = Mensaje.objects.filter(encargo=encargo).order_by('fecha_envio')
    
    # Marcar mensajes como leídos
    mensajes.filter(destinatario=request.user, leido=False).update(leido=True)

    # Procesar el formulario POST
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            # Determinar el destinatario basado en el rol del usuario
            destinatario = encargo.artista if request.user == encargo.cliente else encargo.cliente
            
            # Enviar mensaje usando el servicio
            email_service = EmailService()
            email_service.enviar_mensaje(
                remitente=request.user,
                destinatario=destinatario,
                asunto=f"Re: Encargo #{encargo.id} - {encargo.obra.titulo}",
                contenido=contenido,
                encargo=encargo
            )
            
            messages.success(request, 'Mensaje enviado correctamente')
            return redirect('mensajes:detalle_conversacion', encargo_id=encargo.id)

    return render(request, 'mensajes/detalle_conversacion.html', {
        'encargo': encargo,
        'mensajes': mensajes
    })

@login_required
def conversacion_general(request):
    mensajes = Mensaje.objects.filter(
        Q(remitente=request.user) | Q(destinatario=request.user),
        encargo__isnull=True
    ).order_by('fecha_envio')
    
    # Marcar mensajes como leídos
    mensajes.filter(destinatario=request.user, leido=False).update(leido=True)

    # Procesar el formulario POST
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            # Obtener el último destinatario de la conversación
            ultimo_mensaje = mensajes.first()
            if ultimo_mensaje:
                destinatario = ultimo_mensaje.remitente if ultimo_mensaje.destinatario == request.user else ultimo_mensaje.destinatario
                
                # Enviar mensaje usando el servicio
                email_service = EmailService()
                email_service.enviar_mensaje(
                    remitente=request.user,
                    destinatario=destinatario,
                    asunto=f"Re: Mensaje General",
                    contenido=contenido
                )
                
                messages.success(request, 'Mensaje enviado correctamente')
                return redirect('mensajes:conversacion_general')

    return render(request, 'mensajes/detalle_conversacion.html', {
        'mensajes': mensajes
    })

@login_required
def enviar_mensaje(request, encargo_id=None):
    encargo = None
    destinatario = None
    
    if encargo_id:
        encargo = get_object_or_404(Encargo, id=encargo_id)
        # Determinar el destinatario basado en el rol del usuario
        destinatario = encargo.artista if request.user == encargo.cliente else encargo.cliente

    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        contenido = request.POST.get('contenido')
        destinatario_id = request.POST.get('destinatario')
        
        if destinatario_id:
            destinatario = get_object_or_404(Usuario, id=destinatario_id)
        
        if not destinatario:
            messages.error(request, 'Debes seleccionar un destinatario')
            return redirect('mensajes:enviar_mensaje')

        # Enviar mensaje usando el servicio
        email_service = EmailService()
        email_service.enviar_mensaje(
            remitente=request.user,
            destinatario=destinatario,
            asunto=asunto,
            contenido=contenido,
            encargo=encargo
        )

        messages.success(request, 'Mensaje enviado correctamente')
        if encargo:
            return redirect('mensajes:detalle_conversacion', encargo_id=encargo.id)
        return redirect('mensajes:conversacion_general')

    # Obtener posibles destinatarios si no hay encargo
    destinatarios = []
    if not encargo:
        destinatarios = Usuario.objects.exclude(id=request.user.id)

    return render(request, 'mensajes/enviar_mensaje.html', {
        'encargo': encargo,
        'destinatario': destinatario,
        'destinatarios': destinatarios
    })

@login_required
def enviar_mensaje_encargo(request, obra_id):
    """
    Vista para enviar un mensaje relacionado con un encargo de una obra.
    Crea un encargo si no existe y envía el mensaje inicial.
    """
    obra = get_object_or_404(Comision, id=obra_id)
    plan = request.GET.get('plan', 'basico')  # Por defecto 'basico'
    # Verificar que el usuario no es el vendedor
    if request.user == obra.vendedor:
        messages.error(request, 'No puedes enviar mensajes sobre tus propias obras')
        return redirect('gallery:detalle_obra', obra_id=obra_id)
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        # Crear o obtener el encargo
        encargo, created = Encargo.objects.get_or_create(
            cliente=request.user,
            artista=obra.vendedor,
            obra=obra,
            defaults={
                'estado': 'pendiente',
                'plan': plan  # Usar el plan seleccionado
            }
        )
        # Enviar mensaje usando el servicio
        email_service = EmailService()
        email_service.enviar_mensaje(
            remitente=request.user,
            destinatario=obra.vendedor,
            asunto=f'Nuevo encargo - {obra.titulo}',
            contenido = (
                f"{request.user.username} ha enviado un nuevo encargo de la obra: {obra.titulo}\n"
                f"Tipo de encargo: {plan.capitalize()}\n\n"
                f"{contenido}"
            ),
            encargo=encargo
        )
        messages.success(request, 'Mensaje enviado correctamente')
        return redirect('mensajes:detalle_conversacion', encargo_id=encargo.id)
    
    return render(request, 'mensajes/enviar_mensaje_encargo.html', {
        'obra': obra,
        'plan': plan
    })

# ====================== VISTAS ADMINISTRATIVAS ======================
@method_decorator(admin_required, name='dispatch')
class AdminMensajeListView(LoginRequiredMixin, ListView):
    model = Mensaje
    template_name = 'backoffice/admin_mensajes_list.html'
    context_object_name = 'mensajes'
    ordering = ['-fecha_envio']

@method_decorator(admin_required, name='dispatch')
class AdminMensajeDetailView(LoginRequiredMixin, DetailView):
    model = Mensaje
    template_name = 'backoffice/admin_mensaje_detail.html'
    context_object_name = 'mensaje'

@method_decorator(admin_required, name='dispatch')
class AdminMensajeDeleteView(LoginRequiredMixin, DeleteView):
    model = Mensaje
    template_name = 'backoffice/admin_mensaje_confirm_delete.html'
    success_url = reverse_lazy('mensajes:admin_mensajes_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Mensaje eliminado correctamente.")
        return super().delete(request, *args, **kwargs) 