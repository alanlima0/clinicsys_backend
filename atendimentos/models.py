from django.db import models
from pacientes.models import Paciente
from procedimentos.models import Procedimento

class Atendimento(models.Model):

    class Prioridade(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal'
        PREFERENCIAL = 'PREFERENCIAL', 'Preferencial'
        URGENTE = 'URGENTE', 'Urgente'
    
    class FormaPagamento(models.TextChoices):
        DINHEIRO = 'DINHEIRO', 'Dinheiro'
        CARTAO = 'CARTAO', 'Cartão'
        PIX = 'PIX', 'Pix'

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT)

    prioridade = models.CharField(max_length=20, choices=Prioridade.choices)
    forma_pagamento = models.CharField(max_length=20, choices=FormaPagamento.choices)

    # CONTROLE DE FILA
    criado_em = models.DateTimeField(auto_now_add=True)
    chamado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    hora_chamada = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.paciente.nome} - {self.procedimento.nome}'


class Triagem(models.Model):
    atendimento = models.OneToOneField(
        Atendimento,
        on_delete=models.CASCADE,
        related_name='triagem'
    )

    peso = models.DecimalField(max_digits=5, decimal_places=2)
    pressao_arterial = models.CharField(max_length=10)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)
    saturacao = models.PositiveSmallIntegerField()
    frequencia_cardiaca = models.PositiveSmallIntegerField()
    
    criado_em = models.DateTimeField(auto_now_add=True)


class Anamnese(models.Model):
    atendimento = models.OneToOneField(
        Atendimento,
        on_delete=models.CASCADE,
        related_name='anamnese'
    )

    queixa_principal = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

class Prescricao(models.Model):
    atendimento = models.ForeignKey(
        Atendimento,
        on_delete=models.CASCADE,
        related_name='prescricoes'
    )

    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

