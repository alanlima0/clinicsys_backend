from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class TipoUsuario(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        MEDICO = 'MEDICO','Médico'
        RECEPCAO = 'RECEPCAO','Recepção'

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.RECEPCAO)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','nome']

    def __str__(self):
        return self.nome