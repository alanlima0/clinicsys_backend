from rest_framework import serializers
from .models import CaixaDiario

class CaixaDiarioSerializer(serializers.ModelSerializer):
    atendimento_id = serializers.IntegerField(source='atendimento.id', read_only=True)
    paciente_nome = serializers.CharField(source='atendimento.paciente.nome', read_only=True)
    procedimento_nome = serializers.CharField(source='atendimento.procedimento.nome', read_only=True)
    
    class Meta:
        model = CaixaDiario
        fields = '__all__'