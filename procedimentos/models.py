from django.db import models

class Procedimento(models.Model):
    nome = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.nome