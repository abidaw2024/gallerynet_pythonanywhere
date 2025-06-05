"""
MODELO DE USUARIO PERSONALIZADO DE ABSTRACTUSER.
Incluye autenticación de usuario, y campos adicionales para el vendedor/comprador.
"""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from apps.categories.models import Categoria

"""
Perfiles de usuario diferenciados

Extiende el usuario base de Django para implementar:
- Roles de usuario (normal y admin)
- Método is_admin() para verificar permisos
- Campos adicionales para usuarios

Los roles permiten:
- Usuarios normales: acceso básico a la plataforma
- Administradores: acceso al backoffice y gestión de obras
"""

"""==============================  USUARIO =============================="""
class UsuarioManager(UserManager):
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        if extra_fields.get('rol') != 'admin':
            raise ValueError('El superusuario debe tener rol=admin')
        return super().create_superuser(email=email, username=username, password=password, **extra_fields)

class Usuario(AbstractUser):
    """
    Configuración de credenciales:
    - USERNAME_FIELD = 'email': usa el email como campo principal de autenticación
    - REQUIRED_FIELDS = ['username']: campos adicionales requeridos
    """
    ROLES = (
        ('normal', 'Usuario Normal'),
        ('admin', 'Administrador'),
    )
    
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
    )
    
    #--- credenciales ---
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=128)  #Contraseña encriptada
    last_login = models.DateTimeField(null=True, blank=True)  #último inicio de sesióan
    
    # #--- campos para los usuarios ---
    es_vendedor = models.BooleanField(default=False)  
    es_comprador = models.BooleanField(default=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='normal')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')
    ultima_conexion = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, related_name='usuarios', blank=True)
    seguidores = models.ManyToManyField('self', symmetrical=False, related_name='siguiendo', blank=True)
    
    #--- permisos ---
    '''Estas relaciones son parte fundamental del sistema de autenticación de Django 
    y mi implementación de normal/admin'''
    # Relación con GRUPOS de Django - grupos de permisos para usuarios
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuarios",
        blank=True
    )
    # Relacion con permisos INDIVIDUALES - Permite asignar permisos específicos a usuarios
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuarios_permisos",
        blank=True
    )

    #campos de credenciales configuración
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']  #campo adicional requerido

    objects = UsuarioManager()

    """ ===============  MÉTODOS =============== """
    #retorna el nombre de usuario para en admin y shell
    def __str__(self):
        return self.username  

    #Verifica si el usuario tiene rol de administrador
    def is_admin(self):
        return self.rol == 'admin'
        
    # Cuenta el número de seguidores
    def get_seguidores_count(self):
        return self.seguidores.count()
        
    #Cuenta el número total de usuarios que el usuario sigue
    def get_siguiendo_count(self):
        return self.siguiendo.count()


