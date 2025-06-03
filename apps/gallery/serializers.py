"""
Serializadores para la API REST de Gallery
Este archivo contiene los serializadores que convierten los modelos a JSON y viceversa.
"""

from rest_framework import serializers
from .models import Comision

# NO INCLUIDO !!!
# Serializador para la API REST
class ComisionSerializer(serializers.ModelSerializer):
    """
    Convierte objetos Comision a JSON y viceversa para la API REST.
    
    * Incluye todos los campos del modelo (fields = '__all__')
    * vendedor: se muestra como string (nombre de usuario)
    * fecha_creacion: solo lectura, se genera automáticamente
    
    Campos de solo lectura:
    - vendedor: no se puede modificar a través de la API
    - fecha_creacion: se genera automáticamente al crear
    """
    class Meta:
        model = Comision
        fields = '__all__'
        read_only_fields = ('vendedor', 'fecha_creacion')

    # Convierte el vendedor a su representación en string (username)
    vendedor = serializers.StringRelatedField()