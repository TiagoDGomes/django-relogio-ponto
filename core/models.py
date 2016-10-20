from __future__ import unicode_literals

from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    pis = models.CharField(max_length=25, unique=True)
    verificar_digital = models.NullBooleanField()

class Matricula(models.Model):
    colaborador = models.ForeignKey(Colaborador)
    numero = models.IntegerField()


    
    
