"""
Modelos para la gestión de comisiones y comentarios
Este archivo contiene los modelos relacionados con:
- Comisiones de arte
- Comentarios en comisiones
"""

from django.db import models
from apps.users.models import Usuario  # importa tu modelo de usuario
from decimal import Decimal

""" =============== MODELO DE COMISIÓN =============== """
class Comision(models.Model):
    """
    Modelo para representar una comisión de arte.
    Incluye información sobre la obra, el vendedor y el estado.
    """
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    ]

    ESTILOS = [
        ('realista', 'Realista'),
        ('impresionista', 'Impresionista'),
        ('abstracto', 'Abstracto'),
        ('surrealista', 'Surrealista'),
        ('pop_art', 'Pop Art'),
        ('arte_digital', 'Arte Digital'),
        ('pixel_art', 'Pixel Art'),
        ('anime', 'Anime'),
        ('cartoon', 'Cartoon'),
        ('semi_realista', 'Semi Realista'),
        ('caricatura', 'Caricatura'),
        ('fantasia', 'Fantasía'),
        ('conceptual', 'Conceptual'),
        ('minimalista', 'Minimalista'),
        ('otro', 'Otro'),
    ]

    TECNICAS = [
        ('digital', 'Digital'),
        ('acrilico', 'Acrílico'),
        ('oleo', 'Óleo'),
        ('acuarela', 'Acuarela'),
        ('tinta', 'Tinta'),
        ('lapiz', 'Lápiz'),
        ('carboncillo', 'Carboncillo'),
        ('pastel', 'Pastel'),
        ('gouache', 'Gouache'),
        ('aerografo', 'Aerógrafo'),
        ('mixta', 'Mixta'),
        ('vectorial', 'Vectorial'),
        ('3d', '3D'),
        ('otra', 'Otra'),
    ]

    TEMAS = [
        ('retrato', 'Retrato'),
        ('paisaje', 'Paisaje'),
        ('naturaleza', 'Naturaleza'),
        ('fantasia', 'Fantasía'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('horror', 'Horror'),
        ('comedia', 'Comedia'),
        ('romantico', 'Romántico'),
        ('accion', 'Acción'),
        ('deportes', 'Deportes'),
        ('animales', 'Animales'),
        ('mitologia', 'Mitología'),
        ('religion', 'Religión'),
        ('abstracto', 'Abstracto'),
        ('conceptual', 'Conceptual'),
        ('otro', 'Otro'),
    ]

    # Relación con el vendedor
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comisiones')
    
    # Información básica de la comisión
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estilo = models.CharField(max_length=30, choices=ESTILOS, default='otro')
    tecnica = models.CharField(max_length=30, choices=TECNICAS, default='otra')
    tema = models.CharField(max_length=30, choices=TEMAS, default='otro')
    
    # Imágenes de la comisión
    imagen_principal = models.ImageField(upload_to='comisiones/')
    imagen_adicional_1 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    imagen_adicional_2 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    imagen_adicional_3 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    
    # Nivel Básico
    precio_basico = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_basico = models.TextField()
    
    # Nivel Estándar
    precio_estandar = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_estandar = models.TextField()
    
    # Nivel Premium
    precio_premium = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_premium = models.TextField()
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def __str__(self):
        return f"{self.titulo} - {self.vendedor.username}"

    def get_precio_basico(self):
        """Retorna el precio básico incrementado en 2.50€"""
        return self.precio_basico + Decimal('2.50')

    def get_precio_estandar(self):
        """Retorna el precio estándar incrementado en 2.50€"""
        return self.precio_estandar + Decimal('2.50')

    def get_precio_premium(self):
        """Retorna el precio premium incrementado en 2.50€"""
        return self.precio_premium + Decimal('2.50')

    class Meta:
        verbose_name = 'Comisión'
        verbose_name_plural = 'Comisiones'
        ordering = ['-fecha_creacion']

""" =============== MODELO DE COMENTARIO =============== """
class Comentario(models.Model):
    """
    Modelo para los comentarios en las comisiones.
    Permite a los usuarios comentar en las comisiones de arte.
    """
    # Relaciones
    obra = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE)
    
    # Contenido del comentario
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']  #ordena del mas recientw al mas antiguo

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.obra.titulo}'
