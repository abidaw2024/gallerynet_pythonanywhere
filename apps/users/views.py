"""
Manejo de credenciales y autenticación de usuarios
Este archivo contiene las vistas relacionadas con el manejo de credenciales de usuario:
- Registro de nuevos usuarios
- Inicio de sesión
- Cierre de sesión
- Cambio de contraseña
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditarPerfilForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from rest_framework import viewsets, permissions
from .models import Usuario, Categoria
from .serializers import UsuarioSerializer

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from apps.users.decorators import admin_required

""" =============== API VIEWS =============== """
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)

""" =============== VISTAS BÁSICAS =============== """
def user_home(request):
    return HttpResponse("Bienvenido a la sección de usuarios")

""" =============== AUTENTICACIÓN =============== """
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('users:perfil', username=user.username)
    else:
        form = RegistroUsuarioForm()
    return render(request, 'users/register.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            if user.is_admin():
                return redirect('backoffice:admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'users/login.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("users:login")

""" =============== PERFIL DE USUARIO =============== """
@login_required
def perfil(request, username):
    usuario = Usuario.objects.get(username=username)
    comisiones = usuario.comisiones.all().order_by('-fecha_creacion')
    siguiendo = request.user in usuario.seguidores.all() if request.user.is_authenticated else False
    return render(request, 'users/perfil.html', {
        'usuario': usuario, 
        'obras': comisiones,
        'siguiendo': siguiendo
    })

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:perfil', username=request.user.username)
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'users/editar_perfil.html', {'form': form})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('users:perfil', username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/cambiar_password.html', {'form': form})

""" =============== VISTAS DE ADMINISTRACIÓN =============== """
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'backoffice/admin_usuarios_list.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering', 'desc')
        if ordering == 'asc':
            queryset = queryset.order_by('date_joined')
        else:
            queryset = queryset.order_by('-date_joined')
        return queryset

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'backoffice/admin_usuarios_detail.html'
    context_object_name = 'usuario'

class UsuarioUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Usuario
    template_name = 'backoffice/admin_usuarios_update.html'
    fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']
    success_message = "Usuario actualizado exitosamente"
    success_url = reverse_lazy('users:admin_usuarios_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Usuario '{self.object.get_full_name()}' actualizado exitosamente.")
        return response

class UsuarioCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Usuario
    template_name = 'backoffice/admin_usuarios_create.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    success_message = "Usuario creado exitosamente"
    success_url = reverse_lazy('users:admin_usuarios_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Usuario '{self.object.get_full_name()}' creado exitosamente.")
        return response

@method_decorator(admin_required, name='dispatch')
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'backoffice/admin_usuario_confirm_delete.html'
    success_url = reverse_lazy('users:admin_usuarios_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, f"Usuario '{self.get_object().get_full_name()}' eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

""" =============== BÚSQUEDA Y SEGUIMIENTO =============== """
def buscar_usuarios(request):
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    usuarios = Usuario.objects.filter(rol='normal')
    
    if query:
        usuarios = usuarios.filter(
            username__icontains=query
        ) | usuarios.filter(
            first_name__icontains=query
        ) | usuarios.filter(
            last_name__icontains=query
        ) | usuarios.filter(
            email__icontains=query
        )
        usuarios = usuarios.distinct()
    
    if categoria_id:
        usuarios = usuarios.filter(categorias__id=categoria_id)
    
    categorias = Categoria.objects.all()
    return render(request, 'buscar.html', {
        'usuarios': usuarios,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id
    })

@login_required
@require_POST
def seguir_usuario(request, username):
    usuario_a_seguir = Usuario.objects.get(username=username)
    if request.user != usuario_a_seguir:
        if request.user in usuario_a_seguir.seguidores.all():
            usuario_a_seguir.seguidores.remove(request.user)
            siguiendo = False
        else:
            usuario_a_seguir.seguidores.add(request.user)
            siguiendo = True
        return JsonResponse({
            'siguiendo': siguiendo,
            'seguidores_count': usuario_a_seguir.get_seguidores_count()
        })
    return JsonResponse({'error': 'No puedes seguirte a ti mismo'}, status=400)

""" =============== MENSAJERÍA =============== """
@login_required
def lista_mensajes(request):
    return render(request, 'users/lista_mensajes.html')

@login_required
def conver_mensajes(request):
    return render(request, 'users/conver_mensajes.html')