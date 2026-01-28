from django.db import models

class Paciente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F','Feminino'

    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome