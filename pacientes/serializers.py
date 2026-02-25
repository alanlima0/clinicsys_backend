import re

from rest_framework import serializers
from .models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            'id',
            'nome',
            'data_nascimento',
            'telefone',
            'sexo',
            'data_cadastro',
            'altura'
        ]
        read_only_fields = ['id', 'data_cadastro']
    
    def validate_telefone(self, value):
        # remove tudo que não for número
        telefone = re.sub(r'\D', '', value)

        if len(telefone) not in [10, 11]:
            raise serializers.ValidationError(
                'Telefone deve conter 10 ou 11 dígitos.'
            )

        return telefone