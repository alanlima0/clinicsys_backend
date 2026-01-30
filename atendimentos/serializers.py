from rest_framework import serializers
from .models import Atendimento, Triagem, Anamnese, Prescricao
from caixa.models import CaixaDiario


from pacientes.serializers import PacienteSerializer
from procedimentos.serializers import ProcedimentoSerializer

class AtendimentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = ['paciente', 'procedimento', 'prioridade', 'forma_pagamento']
    
    def create(self, validated_data):
        # Cria o atendimento
        atendimento = Atendimento.objects.create(**validated_data)
        
        # Cria automaticamente o registro no caixa diário
        CaixaDiario.objects.create(
            atendimento=atendimento,
            valor=atendimento.procedimento.valor,
            forma_pagamento=atendimento.forma_pagamento
        )
        
        return atendimento
    


class AtendimentoListSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    procedimento_nome = serializers.CharField(source='procedimento.nome', read_only=True)
    
    class Meta:
        model = Atendimento
        fields = [
            'id', 'paciente_nome', 'procedimento_nome', 
            'prioridade', 'criado_em', 'chamado', 'finalizado'
        ]

# Serializers do prontuário
class TriagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triagem
        fields = '__all__'

class AnamneseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anamnese
        fields = '__all__'

class PrescricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescricao
        fields = '__all__'

# Serializer COMPLETO do atendimento (para prontuário)
class AtendimentoDetalheSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    procedimento = ProcedimentoSerializer(read_only=True)
    triagem = TriagemSerializer(read_only=True)
    anamnese = AnamneseSerializer(read_only=True)
    prescricoes = PrescricaoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Atendimento
        fields = '__all__'