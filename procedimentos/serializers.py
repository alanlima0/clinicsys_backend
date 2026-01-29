from rest_framework import serializers
from .models import Procedimento


class ProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimento
        fields = ['id', 'nome', 'valor']
