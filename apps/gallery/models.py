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
    #Lista de estados posibles para una comisión
    #Define si la obra está disponible, en proceso, etc.
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    ]

    #Lista de estilos artísticos disponibles
    ESTILOS = [
        ('realista', 'Realista'),
        ('impresionista', 'Impresionista'),
        ('abstracto', 'Abstracto'),
        ('surrealista', 'Surrealista'),
        ('pop_art', 'Pop Art'),
        ('arte_digital', 'Arte Digital'),
        ('anime', 'Anime'),
        ('cartoon', 'Cartoon'),
        ('semi_realista', 'Semi Realista'),
        ('caricatura', 'Caricatura'),
        ('fantasia', 'Fantasía'),
        ('conceptual', 'Conceptual'),
        ('minimalista', 'Minimalista'),
        ('gótico', 'Gótico'),
        ('steampunk', 'Steampunk'),
        ('cyperpunk', 'Ciberpunk'),
        ('otro', 'Otro'),
    ]

    #Lista de técnicas artísticas
    TECNICAS = [
        ('digital', 'Digital'),
        ('acrilico', 'Acrílico'),
        ('oleo', 'Óleo'),
        ('acuarela', 'Acuarela'),
        ('tinta', 'Tinta'),
        ('lapiz', 'Lápiz'),
        ('gouache', 'Gouache'),
        ('aerografo', 'Aerógrafo'),
        ('mixta', 'Mixta'),
        ('vectorial', 'Vectorial'),
        ('modelado_3d', 'Modelado 3D'),
        ('pixel_art', 'Pixel Art'),
        ('Glitch Art', 'Glitch Art'),
        ('collage_digital', 'Collage Digital'),
        ('otra', 'Otra'),
    ]

    #Lista de temas para las obras
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
        ('urbano', 'Urbano'),
        ('otro', 'Otro'),
    ]

    #Relación con el vendedor
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comisiones')
    
    #Información básica de la comisión
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    estilo = models.CharField(max_length=30, choices=ESTILOS, default='otro')
    tecnica = models.CharField(max_length=30, choices=TECNICAS, default='otra')
    tema = models.CharField(max_length=30, choices=TEMAS, default='otro')
    
    #Imágenes de la comisión
    imagen_principal = models.ImageField(upload_to='comisiones/')
    imagen_adicional_1 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    imagen_adicional_2 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    imagen_adicional_3 = models.ImageField(upload_to='comisiones/', blank=True, null=True)
    
    #precio básico
    precio_basico = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_basico = models.TextField()
    
    #precio estándar
    precio_estandar = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_estandar = models.TextField()
    
    #precio premium
    precio_premium = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion_premium = models.TextField()
    
    #Fechas de creación y actualización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

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

    # Configuración de metadatos del modelo:
    # - Nombres para el panel de administración
    # - Ordenacion (más recientes primero)
    class Meta:
        verbose_name = 'Comisión'
        verbose_name_plural = 'Comisiones'
        ordering = ['-fecha_creacion']

