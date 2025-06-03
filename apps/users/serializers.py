from rest_framework import serializers
from .models import Usuario

# Serializador para la API REST
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #campos que se incluirán en la serialización:

        fields = ['id', 'username', 'correo', 'es_vendedor', 
                  'es_comprador', 'first_name', 'last_name', 
                  'is_active']
