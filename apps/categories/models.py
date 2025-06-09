from django.db import models

# Modelo que representa las categorías de artisas
class Categoria(models.Model):
    #Campos básicos de la categoría
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    #fechas creación y update(se actualizan automáticamente)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Configuración del modelo para el admin y ordenamiento
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    #Como se muestra la categoría
    def __str__(self):
        return self.nombre 