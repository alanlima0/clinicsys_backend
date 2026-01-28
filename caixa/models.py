# caixa/models.py
from django.db import models
from atendimentos.models import Atendimento

class CaixaDiario(models.Model):
    atendimento = models.OneToOneField(
        Atendimento,
        on_delete=models.CASCADE,
        related_name='caixa'
    )

    valor = models.DecimalField(max_digits=8, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Atendimento {self.atendimento.id} - R$ {self.valor}'
