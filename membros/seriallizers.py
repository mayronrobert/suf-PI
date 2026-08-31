from rest_framework import serializers, viewsets
from .models import Membro

class MembroSerializer(serializers.ModelSerializer):     
    class Meta:         
        model = Membro         
        fields = ['id', 'nome_completo', 'email', 'telefone', 'tipo_membro', 'status'] 

class MembroViewSet(viewsets.ModelViewSet):     
    queryset = Membro.objects.all()
    serializer_class = MembroSerializer
